"""Politique de non-regression du projet, AU-DESSUS du core du hub (port de Vscode8 `scripts/deck_garde.py`).

Pourquoi une couche locale : `pptx_deck_core.run_delta` desactive TOUTE garde hors perimetre des qu'une op est globale (constate : un remplacement global modifie 42 slides, dont
une « finie », sans refus) et n'a aucune detection des slides disparues (une suppression non declaree passe : 73 -> 71). Le core est un canon du hub : on ne le modifie pas ici,
on lui donne des ops que SA garde sait surveiller et on controle nous-memes les ensembles de slides. Adaptations VSCode3 : registre des slides finies local et OPTIONNEL (voir cles_finies), designation des slides par titre exact (selecteur_titre).
Ce module ne connait ni chemins, ni versions, ni rendu : il juge des ops et des empreintes.
"""

import hashlib
import json
import os
import re
from collections import Counter

from deck_lib import plat
from deck_rapport import titre_slide
from lxml import etree
from pptx.enum.shapes import MSO_SHAPE_TYPE

# Registre OPTIONNEL des slides finies : {cle_titre: ...} (seules les cles comptent). Vscode8 le lit via `feedbacks_reprise.lire_finies` (module du hub absent ici : non porte).
# Absent ou illisible : aucune slide finie, comme la-bas.
FINIES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "slides_finies.json")

OPS_SANS_SLIDE = ("remplacer_texte", "garder")  # seules ops qui peuvent ne pas viser une slide ; `remplacer_texte` est developpee, `garder` porte sa propre liste

# Balises volontaires du livrable (CLAUDE.md) : [À CONFIRMER] / [À CALIBRER] / [À VALIDER] / [À SOURCER] = donnee absente, JAMAIS comblee par une valeur inventee.
BALISE = re.compile(r"\[À[\s ]+[A-ZÉÈÀ][A-ZÉÈÀ  '’-]{1,40}\]", re.IGNORECASE)  # une ou plusieurs mots, casse libre, espace insecable


def balises(texte):
    """Compteur des balises [À …] d'un texte."""
    return Counter(BALISE.findall(texte or ""))


def _textes(formes):
    """Textes de toutes les formes, groupes et cellules de tableau compris."""
    for sh in formes:
        if sh.shape_type == MSO_SHAPE_TYPE.GROUP:
            yield from _textes(sh.shapes)
            continue
        if sh.has_text_frame:
            yield sh.text_frame.text
        if getattr(sh, "has_table", False) and sh.has_table:
            for r in sh.table.rows:
                for c in r.cells:
                    yield c.text_frame.text


def balises_par_slide(prs):
    """{sldId: Counter des balises [À …] de la slide} (formes, groupes, cellules)."""
    return {sl.slide_id: sum((balises(x) for x in _textes(sl.shapes)), Counter()) for sl in prs.slides}


def compter_balises(prs):
    """Nombre total de balises [À …] du deck."""
    return sum(sum(c.values()) for c in balises_par_slide(prs).values())


def verifier_balises_deck(avant, apres, autorisees=frozenset()):
    """ValueError si une slide PERD une balise [À …] (comparaison des decks, `balises_par_slide`) hors des sldId `autorisees` (ops portant `source`, etape portant `source`).
    C'est la garde qui fait foi : celle de `verifier_balises` ne lit que les chaines `ancien`/`nouveau` d'une op et ne voit ni un fragment, ni une etape de dessin."""
    for i, avant_i in avant.items():
        retirees = avant_i - apres.get(i, avant_i)
        if retirees and i not in autorisees:
            raise ValueError(f"slide sldId {i} : balise(s) {sorted(retirees)} retiree(s) sans `source` : une balise [À …] n'est jamais comblee par une valeur inventee ; "
                             "citer l'origine de la valeur (cle `source` de l'op ou de l'etape)")


def ids_avec_source(core, prs, ops, etapes=()):
    """sldId des slides dont une op ou une etape porte une `source` non vide : seules autorisees a perdre une balise."""
    ids = set()
    toutes = {i: sl.slide_id for i, sl in enumerate(prs.slides, 1)}
    for d in ops:
        if str(d.get("source", "")).strip() and d.get("slide") is not None:
            ids |= {toutes[r] for r in core.resoudre_slides(prs, [d["slide"]])}
    return ids


def verifier_balises(ops):
    """ValueError si un `remplacer_texte` RETIRE une balise [À …] (presente dans `ancien`, absente de `nouveau`) sans porter `source` : la valeur qui comble la balise doit avoir une source.
    Changer une balise pour une autre (ex. CONFIRMER -> VALIDER) compte comme un retrait : sans source, c'est un contournement."""
    for d in ops:
        if d.get("op") != "remplacer_texte":
            continue
        retirees = balises(d["ancien"]) - balises(d["nouveau"])
        if retirees and not str(d.get("source", "")).strip():
            raise ValueError(f"balise(s) {sorted(retirees)} retiree(s) sans `source` : une balise [À …] n'est jamais comblee par une valeur inventee ; "
                             "citer l'origine de la valeur dans l'op (cle `source`)")


def developper_ops(core, prs, ops, exclure_ids=frozenset()):
    """Remplace chaque `remplacer_texte` global par une op CIBLEE par slide qui contient `ancien` (selecteur `id:N`) : la garde hors perimetre du core reste alors active.
    Les slides de `exclure_ids` (slides finies) sont EPARGNEES par une op globale ; renvoie (ops, ignorees) ou `ignorees` = [(rang, sldId)] des slides epargnees, pour le rapport.
    ValueError si `ancien` n'apparait nulle part, s'il n'apparait QUE dans des slides epargnees, ou si une autre op n'a pas de `slide`."""
    sortie, ignorees = [], []
    for d in ops:
        if d.get("slide") is not None or d.get("op") == "garder":
            sortie.append(d)
        elif d.get("op") == "remplacer_texte":
            touchees = core.remplacer_texte(prs, d["ancien"], d["nouveau"], dry_run=True)  # {rang: occurrences}
            if not touchees:
                raise ValueError(f"remplacer_texte global : {d['ancien']!r} introuvable dans le deck")
            retenues = [r for r in sorted(touchees) if prs.slides[r - 1].slide_id not in exclure_ids]
            ignorees += [(r, prs.slides[r - 1].slide_id) for r in sorted(touchees) if prs.slides[r - 1].slide_id in exclure_ids]
            if not retenues:
                raise ValueError(f"remplacer_texte global : {d['ancien']!r} n'apparait que dans des slides finies (epargnees)")
            sortie += [dict(d, slide=core.id_ref(prs.slides[rang - 1], prs)) for rang in retenues]
        else:
            raise ValueError(f"op {d.get('op')!r} sans `slide` : seules {OPS_SANS_SLIDE} peuvent viser le deck entier")
    return sortie, ignorees


def ids_declares(core, prs, ops):
    """(portee, supprimees) : sldId des slides que les ops ont le droit de modifier, et de faire disparaitre (op `supprimer`, ou toute slide hors de `garder`)."""
    portee, supprimees = set(), set()
    toutes = {i: sl.slide_id for i, sl in enumerate(prs.slides, 1)}
    for d in ops:
        if d.get("op") == "garder":
            gardees = core.resoudre_slides(prs, d["slides"])
            supprimees |= {sid for r, sid in toutes.items() if r not in gardees}
            continue
        (rang,) = core.resoudre_slides(prs, [d["slide"]])
        portee.add(toutes[rang])
        if d.get("op") == "supprimer":
            supprimees.add(toutes[rang])
    return portee, supprimees


def verifier_disparues(ids_avant, ids_apres, declarees):
    """ValueError si une slide a disparu sans qu'une op `supprimer` (ou `garder`) l'ait declaree : le core ne le voit pas (sa comparaison itere sur les slides d'apres)."""
    non_declarees = (set(ids_avant) - set(ids_apres)) - set(declarees)
    if non_declarees:
        raise ValueError(f"slide(s) disparue(s) sans etre declaree(s) (sldId {sorted(non_declarees)})")


P14 = "http://schemas.microsoft.com/office/powerpoint/2010/main"


def _sections_par_slide(prs):
    """{sldId (chaine): nom de section p14}."""
    ext = prs.part._element.find(f".//{{{P14}}}sectionLst")
    if ext is None:
        return {}
    return {x.get("id"): sec.get("name") for sec in ext for x in sec.find(f"{{{P14}}}sldIdLst")}


def empreintes_completes(core, prs):
    """{sldId: (empreinte du core, empreinte complementaire)}. Le core hache texte + geometrie + XML des formes ; il est AVEUGLE aux notes, a la section p14 et au layout de la slide
    (mesure : changer l'un des trois ne change pas son empreinte). L'empreinte complementaire les couvre."""
    base = core.empreintes_slides(prs)
    sections = _sections_par_slide(prs)
    sortie = {}
    for sl in prs.slides:
        notes = sl.notes_slide.notes_text_frame.text if sl.has_notes_slide and sl.notes_slide.notes_text_frame is not None else ""
        layout = hashlib.md5(etree.tostring(sl.slide_layout._element)).hexdigest()
        comp = hashlib.md5("|".join([notes, sl.slide_layout.name, layout, sections.get(str(sl.slide_id), "")]).encode("utf-8")).hexdigest()
        sortie[sl.slide_id] = (base[sl.slide_id], comp)
    return sortie


def empreinte_modeles(prs):
    """Hash des masters et de tous les layouts : un changement les touche TOUS sans modifier aucune slide."""
    h = hashlib.md5()
    for m in prs.slide_masters:
        h.update(etree.tostring(m._element))
        for lay in m.slide_layouts:
            h.update(etree.tostring(lay._element))
    return h.hexdigest()


def appliquer_etape(core, prs, declarer, f, nouvelles_max=0, avant=None, source="", interdites=frozenset()):
    """Execute l'etape de dessin `f(prs)` EN MEMOIRE sous garde. `declarer` (selecteurs de slides existantes) est resolu AVANT l'execution : une etape ne declare jamais elle-meme ce qu'elle touche.
    ValueError si, apres `f` : une slide a disparu (retirer une slide est l'op `supprimer`), plus de `nouvelles_max` slides ont ete creees (defaut 0 : creer une slide se declare),
    une slide non declaree a change (texte, forme, style, notes, section, layout) ou un master/layout a change. Renvoie {touchees, ajoutees, apres} (sldId ; `apres` = empreintes completes, a repasser en `avant` de
    l'etape suivante : un passage d'empreinte coute ~1,6 s sur 73 slides).
    `avant` : empreintes completes DEJA calculees sur `prs` dans son etat courant (sinon calculees ici).
    `source` : origine d'une valeur qui comble une balise [À …] ; sans elle, l'etape ne peut retirer aucune balise. `interdites` : sldId des slides FINIES non forcees, qu'elle ne peut pas modifier."""
    declarees = {prs.slides[r - 1].slide_id for r in core.resoudre_slides(prs, list(declarer))}
    avant = avant if avant is not None else empreintes_completes(core, prs)
    modeles = empreinte_modeles(prs)
    balises_avant = balises_par_slide(prs)
    f(prs)
    apres = empreintes_completes(core, prs)
    disparues = set(avant) - set(apres)
    if disparues:
        raise ValueError(f"etape de dessin : slide(s) disparue(s) (sldId {sorted(disparues)}) ; retirer une slide est l'op `supprimer`")
    nouvelles = set(apres) - set(avant)
    if len(nouvelles) > nouvelles_max:
        raise ValueError(f"etape de dessin : {len(nouvelles)} slide(s) creee(s) pour {nouvelles_max} declaree(s) (nouvelles_max)")
    modifiees = {i for i in avant if apres[i] != avant[i]}
    if modifiees - declarees:
        raise ValueError(f"etape de dessin : slide(s) modifiee(s) hors perimetre declare (sldId {sorted(modifiees - declarees)})")
    if modifiees & set(interdites):
        raise ValueError(f"etape de dessin : slide(s) FINIE(S) modifiee(s) (sldId {sorted(modifiees & set(interdites))}) : ne plus les modifier sans demande explicite (--forcer-finie)")
    verifier_balises_deck(balises_avant, balises_par_slide(prs), declarees if str(source).strip() else frozenset())
    if empreinte_modeles(prs) != modeles:
        raise ValueError("etape de dessin : un master ou un layout a ete modifie (il touche toutes les slides)")
    return {"touchees": modifiees, "ajoutees": nouvelles, "apres": apres}


def etape_gardee(core, src, dst, declarer, f, nouvelles_max=0, source="", interdites=frozenset()):
    """Ouvre `src`, applique l'etape gardee, ecrit `dst` en .tmp, controle l'integrite (skill), puis remplace : un echec ne laisse aucun `dst`. Renvoie le constat de l'etape."""
    prs = core._ouvrir(src)
    constat = appliquer_etape(core, prs, declarer, f, nouvelles_max, source=source, interdites=interdites)
    tmp = dst + ".tmp"
    try:
        prs.save(tmp)
        problemes = core._integrite().controler(tmp)["problemes"]
        if problemes:
            raise ValueError("etape de dessin : integrite KO : " + " ; ".join(problemes))
        os.replace(tmp, dst)
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)
    return constat


def simuler(core, base, ops, etapes=(), declares=None, interdites=frozenset()):
    """Applique `ops` puis `etapes` EN MEMOIRE sur la base et juge le resultat : disparues non declarees, slides modifiees hors perimetre (empreinte du core + complementaire). Rien n'est ecrit.
    Sert au --dry-run (le core saute sa propre garde en dry) et de pre-controle avant l'ecriture. `etapes` : [{"declarer": [...], "f": fn, "nouvelles_max": n}]. Renvoie le constat pour le rapport."""
    prs = core._ouvrir(base)
    avant = empreintes_completes(core, prs)
    ordre_avant = [sl.slide_id for sl in prs.slides]
    portee, supprimees = declares if declares is not None else ids_declares(core, prs, ops)  # `declares` : calcule une fois par l'appelant sur la meme base
    modeles = empreinte_modeles(prs)
    balises_avant, autorisees = balises_par_slide(prs), ids_avec_source(core, prs, ops)
    core.appliquer_delta(prs, ops)
    apres = empreintes_completes(core, prs)
    verifier_balises_deck(balises_avant, balises_par_slide(prs), autorisees)
    verifier_disparues(avant, apres, supprimees)
    hors = {i for i in apres if i in avant and apres[i] != avant[i]} - portee
    if hors:
        raise ValueError(f"slide(s) modifiee(s) hors perimetre (sldId {sorted(hors)})")
    if empreinte_modeles(prs) != modeles:
        raise ValueError("un master ou un layout a ete modifie par les ops")
    for e in etapes:  # l'empreinte « apres » d'une etape est l'« avant » de la suivante
        apres = appliquer_etape(core, prs, e["declarer"], e["f"], e.get("nouvelles_max", 0), avant=apres, source=e.get("source", ""), interdites=interdites)["apres"]
    ordre_apres = [sl.slide_id for sl in prs.slides]
    communs_avant = [i for i in ordre_avant if i in apres]
    communs_apres = [i for i in ordre_apres if i in avant]
    return {"touchees": {i for i in apres if i in avant and apres[i] != avant[i]}, "ajoutees": {i for i in apres if i not in avant},
            "supprimees": set(avant) - set(apres), "ordre_modifie": communs_avant != communs_apres, "avant": avant, "apres": apres, "prs_apres": prs}


# --- slides finies (registre optionnel deck_delta/slides_finies.json ; ce module le LIT) -------------------------------------------

def cle_titre(texte):
    """Cle du registre : titre normalise, sans ponctuation ni casse, 40 caracteres (meme formule que Vscode8)."""
    return re.sub(r"[\W_]+", "", texte.lower())[:40]


def titre_registre(slide):
    """Titre de la slide : placeholder titre uniquement, espaces aplatis (Vscode8 appliquait en plus `feedbacks_reprise.norm`, non porte)."""
    return plat(slide.shapes.title.text_frame.text) if slide.shapes.title is not None else ""


def cles_finies():
    """Cles des slides finies (registre absent ou illisible : aucune)."""
    try:
        with open(FINIES, encoding="utf-8") as f:
            return set(json.load(f))
    except (OSError, ValueError):
        return set()


def ids_finies(prs, cles):
    """sldId des slides dont la cle de titre est dans `cles` ; une slide sans titre n'a pas de cle (jamais « finie »)."""
    return {sl.slide_id for sl in prs.slides if (k := cle_titre(titre_registre(sl))) and k in cles}


def verifier_finies(core, prs, ops, cles, forcer=frozenset(), declares=None):
    """ValueError si une op vise (modifie, supprime, deplace) une slide finie dont la cle n'est pas dans `forcer`. Renvoie les titres des slides finies touchees AVEC forçage (pour le rapport)."""
    portee, supprimees = declares if declares is not None else ids_declares(core, prs, ops)
    touchees = portee | supprimees
    forcees = []
    for sl in prs.slides:
        k = cle_titre(titre_registre(sl))
        if sl.slide_id in touchees and k and k in cles:
            if k not in forcer:
                raise ValueError(f"slide « {titre_registre(sl)} » est FINIE (registre slides_finies.json) : ne plus la modifier sans demande explicite "
                                 "(--forcer-finie \"<titre>\" --demande \"<mots de l'utilisateur>\")")
            forcees.append(titre_registre(sl))
    return forcees


# --- designation par TITRE EXACT ---------------------------------------------------------------------------------------------------------------------------

def selecteur_titre(prs, sel):
    """Un rang (int) ou « id:N » passent tels quels ; une chaine est un TITRE EXACT (deck_rapport.titre_slide, casse et espaces normalises) resolu en « id:N ».
    ValueError si aucune ou plusieurs slides portent ce titre : jamais de prefixe, jamais de choix silencieux (le core, lui, cherche le texte de N'IMPORTE QUELLE forme :
    un titre de chapitre repris dans le sommaire y serait ambigu)."""
    if not isinstance(sel, str) or sel.startswith("id:"):
        return sel
    cible = plat(sel).casefold()
    trouvees = [sl for sl in prs.slides if titre_slide(sl).casefold() == cible]
    if len(trouvees) != 1:
        raise ValueError(f"titre exact {sel!r} : {len(trouvees)} slide(s) ; 1 exigee (le titre doit etre COMPLET, sans prefixe)")
    return f"id:{trouvees[0].slide_id}"


def resoudre_titres(prs, ops):
    """Copie des ops avec `slide` (et `slides` d'un `garder`) convertis par selecteur_titre ; les autres cles sont inchangees."""
    sortie = []
    for d in ops:
        d = dict(d)
        if d.get("slide") is not None:
            d["slide"] = selecteur_titre(prs, d["slide"])
        if d.get("slides"):
            d["slides"] = [selecteur_titre(prs, x) for x in d["slides"]]
        sortie.append(d)
    return sortie
