"""Point d'entree unique de generation d'une version du deck « Offre Infra as a Product » : applique un DELTA a une base, via le core du hub.

    py deck.py <delta> [--base V4|chemin.pptx] [--sortie chemin.pptx] [--dry-run] [--sans-rendu] [--dossier-rendu DIR]

Port adapte de Vscode8 `scripts/deck.py`. <delta> : nom d'un module de ce dossier (« delta_exemple ») ou chemin d'un .py exposant OPS (liste d'ops du core : {slide, op, ...}),
NOTE, BASE et ETAPES optionnels (voir delta_exemple.py). ETAPES : etapes de dessin gardees [{"declarer": [titres], "f": fonction(prs), "nouvelles_max": n,
"source": "origine d'une valeur qui comble une balise" (optionnel), "nom": "libelle" (optionnel)}] (voir deck_garde.appliquer_etape) ; appliquees APRES les ops.
Les slides sont designees par TITRE EXACT (deck_garde.selecteur_titre), « id:N » ou rang ; jamais par prefixe.
Passe TOUJOURS par `core.run_delta` (ecriture en .tmp puis controle puis remplacement). Un livrable existant n'est jamais ecrase.
Le statut final ne dit jamais « valide » : « RENDU PRODUIT — À REGARDER » (deck_rapport.statut) ; le rendu image des slides modifiees doit etre regarde.
Aucun chemin de version ni nombre de slides en dur : deck_base les resout.
Non porte : lint_charte (Vscode8 le lance ; ici aucune charte tokens.json : la charte OCTO est en prose dans CLAUDE.md) ; il est signale « non evalue » au rapport.
"""
import argparse
import importlib.util
import os
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import deck_base  # noqa: E402
import deck_garde  # noqa: E402
import deck_garde_rendu  # noqa: E402
import deck_integrite  # noqa: E402
import deck_rapport  # noqa: E402

MOTIF_MIN = 10  # longueur minimale de la demande qui justifie un forcage
SKILL_VERIFY = os.path.join(deck_base.RACINE, ".claude", "skills", "pptx-verify", "scripts")


def _core():
    return deck_base.core()


def charger_delta(spec):
    """Module de delta : nom d'un fichier de ce dossier (sans .py) ou chemin d'un .py. Expose OPS ; BASE, NOTE, ETAPES optionnels."""
    chemin = spec if spec.endswith(".py") else os.path.join(HERE, spec + ".py")
    if not os.path.isfile(chemin):
        raise ValueError(f"delta introuvable : {chemin}")
    s = importlib.util.spec_from_file_location("delta_charge", chemin)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    if not isinstance(getattr(m, "OPS", None), list):
        raise ValueError(f"{chemin} doit exposer OPS (liste d'ops du core)")
    for e in getattr(m, "ETAPES", None) or []:
        if not (isinstance(e, dict) and callable(e.get("f")) and isinstance(e.get("declarer"), (list, tuple))):
            raise ValueError("ETAPES : chaque etape est {'declarer': [titres exacts...], 'f': fonction(prs), 'nouvelles_max': n} ; `declarer` est resolu AVANT l'execution")
    return m


def _pas(durees, nom, depuis):
    durees[nom] = time.perf_counter() - depuis
    return time.perf_counter()


def _rendre(sortie, rangs, dossier):
    """PNG des slides modifiees : PowerPoint COM d'abord (Windows, lecture seule), puis la skill pptx-verify (LibreOffice + PyMuPDF). [] si aucun rendu n'est possible : le statut dit alors « NON REGARDÉ »."""
    erreurs = []
    for essai in (1, 2):  # le premier appel COM echoue parfois a froid (PowerPoint en cours de demarrage) : un seul nouvel essai
        try:
            import rendu_com
            return rendu_com.rendre(sortie, rangs, dossier)
        except Exception as e:  # le livrable est deja ecrit et controle : un rendu qui echoue ne le retire pas
            erreurs.append(f"PowerPoint COM (essai {essai}) : {type(e).__name__}: {e}")
            time.sleep(3)
    if SKILL_VERIFY not in sys.path:
        sys.path.append(SKILL_VERIFY)
    try:
        import rendu_slide
        return rendu_slide.rendre(sortie, rangs, dossier)
    except Exception as e:
        erreurs.append(f"LibreOffice : {type(e).__name__}: {e}")
    print("AVERTISSEMENT rendu indisponible : " + " ; ".join(erreurs), file=sys.stderr)
    return []


def executer(argv=None):
    ap = argparse.ArgumentParser(description="Applique un delta au deck via le core du hub.")
    ap.add_argument("delta")
    ap.add_argument("--base")
    ap.add_argument("--sortie")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--sans-rendu", action="store_true")
    ap.add_argument("--forcer-finie", action="append", default=[], metavar="TITRE", help="autorise une op sur cette slide FINIE (titre) ; exige --demande")
    ap.add_argument("--demande", default="", help="mots de l'utilisateur qui demande le forcage (obligatoire avec --forcer-finie ; un agent ne force jamais de lui-meme)")
    ap.add_argument("--dossier-rendu", default=os.path.join(tempfile.gettempdir(), "rendu_deck"))
    a = ap.parse_args(argv)
    durees, t = {}, time.perf_counter()
    delta = charger_delta(a.delta)
    base = deck_base.resoudre_base(a.base or getattr(delta, "BASE", None))
    sortie = a.sortie or deck_base.chemin_sortie()
    if os.path.exists(sortie):
        raise ValueError(f"la sortie existe deja : {sortie} (un livrable n'est jamais ecrase)")
    core = _core()
    avant_prs = core._ouvrir(base)
    # titres exacts -> id:N AVANT toute garde (ops et `declarer` des etapes) ; un titre ambigu ou absent est refuse ici
    etapes = [dict(e, declarer=[deck_garde.selecteur_titre(avant_prs, x) for x in e["declarer"]]) for e in (getattr(delta, "ETAPES", None) or [])]
    ops_titrees = deck_garde.resoudre_titres(avant_prs, delta.OPS)
    forcer = {deck_garde.cle_titre(x) for x in a.forcer_finie}
    if forcer and len(a.demande.strip()) < MOTIF_MIN:
        raise ValueError("un forcage vient d'une demande EXPLICITE de l'utilisateur : joindre --demande \"<ses mots, date>\" ; un agent ne force jamais de lui-meme")
    cles = deck_garde.cles_finies()
    ops, ignorees = deck_garde.developper_ops(core, avant_prs, ops_titrees, exclure_ids=deck_garde.ids_finies(avant_prs, cles - forcer))
    deck_garde.verifier_balises(ops)
    declares = deck_garde.ids_declares(core, avant_prs, ops)  # une seule resolution des titres pour la garde des finies ET la simulation
    forcees = deck_garde.verifier_finies(core, avant_prs, ops, cles, forcer, declares)
    extras = [f"Slide FINIE epargnee par un remplacement global : slide {rang} — {deck_rapport.titre_slide(avant_prs.slides[rang - 1])}" for rang, _ in ignorees]
    extras += [f"Etape de dessin « {e.get('nom', e['f'].__name__)} » : slides declarees {list(e['declarer'])}, {e.get('nouvelles_max', 0)} creation(s) autorisee(s)" for e in etapes]
    extras += [f"FORÇAGE d'une slide finie « {x} » sur demande utilisateur : {a.demande.strip()}" for x in forcees]
    bloquees = deck_garde.ids_finies(avant_prs, cles - forcer)  # slides finies non forcees : ni les ops (verifier_finies) ni les etapes ne les modifient
    constat = deck_garde.simuler(core, base, ops, etapes, declares, bloquees)
    t = _pas(durees, "simulation", t)
    note = getattr(delta, "NOTE", "")
    if a.dry_run:
        return deck_rapport.lignes(base, sortie, note, avant_prs, constat["prs_apres"], constat, [], durees, [], True, simulation=True, extras=extras)

    verrou = sortie + ".verrou"  # reservation de la sortie : deux deck.py sans --sortie calculent la meme version
    try:
        os.close(os.open(verrou, os.O_CREAT | os.O_EXCL | os.O_WRONLY))
    except FileExistsError:
        raise ValueError(f"un autre deck.py ecrit deja {sortie} (verrou {verrou} ; le supprimer s'il est orphelin)") from None
    pret = f"{sortie}.pret{os.getpid()}"  # nom propre au processus
    temporaires = [verrou]
    try:
        courant = base
        if ops or not etapes:  # un delta vide passe aussi par le core (copie controlee)
            courant = pret + ".ops"
            temporaires.append(courant)
            core.run_delta(base, courant, ops)  # .tmp + integrite de la skill + refus d'une slide hors perimetre, puis os.replace
        for i, e in enumerate(etapes):
            suivant = f"{pret}.e{i}"
            temporaires.append(suivant)
            deck_garde.etape_gardee(core, courant, suivant, e["declarer"], e["f"], e.get("nouvelles_max", 0), e.get("source", ""), bloquees)
            courant = suivant
        t = _pas(durees, "core.run_delta + etapes", t)
        problemes = deck_integrite.controler(courant)
        if problemes:
            raise ValueError("integrite (projet) KO : " + " ; ".join(problemes))
        defauts_avant, defauts_apres = deck_garde_rendu.compter_defauts(base), deck_garde_rendu.compter_defauts(courant)
        if defauts_apres > defauts_avant:  # un defaut deja present dans la base n'est pas un defaut du delta
            from pptx import Presentation
            nouveaux = [d for d in deck_garde_rendu.detecter_defauts(Presentation(courant)) if d not in deck_garde_rendu.detecter_defauts(Presentation(base))]
            raise ValueError(f"garde_rendu : {defauts_apres} defaut(s) contre {defauts_avant} dans la base ; nouveaux : {nouveaux[:6]}")
        t = _pas(durees, "controles", t)
        if os.path.exists(sortie):
            raise ValueError(f"la sortie est apparue pendant la generation : {sortie} (un livrable n'est jamais ecrase)")
        os.replace(courant, sortie)
    finally:
        for fichier in temporaires:
            if os.path.exists(fichier):
                os.remove(fichier)
    apres_prs = core._ouvrir(sortie)
    controles = [("integrite (skill, par le core)", "OK"), ("integrite (projet)", "OK"),
                 ("garde_rendu", f"{defauts_apres} defaut(s) (base : {defauts_avant} ; geometrie/debordement, rendu reel non verifie)"),
                 ("lint_charte", "non evalue (aucune charte tokens.json dans ce projet)"),
                 ("balises [À …]", f"{deck_garde.compter_balises(avant_prs)} -> {deck_garde.compter_balises(apres_prs)}")]
    rang = {sl.slide_id: i for i, sl in enumerate(apres_prs.slides, 1)}
    a_rendre = sorted(rang[i] for i in (constat["touchees"] | constat["ajoutees"]) if i in rang)
    pngs = []
    if a_rendre and not a.sans_rendu:
        pngs = _rendre(sortie, a_rendre, a.dossier_rendu)
        t = _pas(durees, "rendu", t)
    return deck_rapport.lignes(base, sortie, note, avant_prs, apres_prs, constat, controles, durees, pngs, a.sans_rendu, extras=extras)


def main(argv=None):
    try:
        for ligne in executer(argv):
            print(ligne)
        return 0
    except ValueError as e:
        print("REFUS : " + str(e), file=sys.stderr)
        return 2


if __name__ == "__main__":
    # Le rapport cite le texte des slides (« ● », « → », guillemets...) : le flux standard Windows est en cp1252 quand il est redirige.
    for _flux in (sys.stdout, sys.stderr):
        _flux.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(main())
