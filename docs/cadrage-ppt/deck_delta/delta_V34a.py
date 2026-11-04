"""Delta V34a (base V33) : suppression du chapitre « Notre approche » et toutes ses consequences.

- les 3 slides du chapitre (intercalaire + 2 slides « 03 · NOTRE APPROCHE · n/2 ») sont retirees par l'op `supprimer` du core (la voie que deck_garde accepte : une etape de dessin
  n'a pas le droit de faire disparaitre une slide) ; la section p14 « Notre approche », devenue vide, est retiree dans la premiere etape ;
- navigation : la pastille « nav-Notre approche » disparait de chaque slide, les 6 restantes gardent largeur, hauteur, police, ecart (50 800 EMU) et bord gauche : la bande raccourcit,
  la pastille active n'est pas touchee ;
- sommaire : six entrees (01 Contexte et enjeux, 02 Nos convictions, 03 Demarche generale, 04 Demarche detaillee, 05 Dispositif et prix, A Annexes), 4 + 2 : le gabarit
  fixe 4 pastilles a gauche et 3 a droite (05, 06, 07) ; la pastille « 06 » du gabarit est masquee et remplacee par « A », comme l'etait deja la « 07 » ;
- numeros de chapitre : intercalaires et surtitres Demarche generale 04 -> 03, Demarche detaillee 05 -> 04, Dispositif et prix 06 -> 05 ;
- annexe « Chaque enjeu cite trouve sa reponse... » : la cible « Notre approche » est retiree, les 5 cibles restantes sont reparties sur la meme hauteur, chaque trait garde son
  enjeu et rejoint sa cible ; le trait qui allait a « Notre approche » est reroute vers « Demarche » (decision de contenu a valider).
Les slides que d'autres lots refont ne sont touchees que sur leurs pastilles de navigation et leurs surtitres.
Usage (depuis docs/cadrage-ppt/) : py deck_delta/deck.py delta_V34a --base V33 --sortie C:/tmp/deck-v34-a/V34a.pptx
"""
import copy
import re

import deck_base
import deck_draw
from pptx import Presentation

BASE = "V33"
NOTE = "V34a : chapitre Notre approche supprime (3 slides), navigation a 6 pastilles, sommaire a 6 entrees, numeros de chapitre 03/04/05, annexe des enjeux reroutee"

CHAPITRE = "Notre approche"
T_COACH = "Le coach produit augmenté est le moteur de la transformation"
T_ENTREE = "Un point d'entrée adapté à la maturité et à la criticité de chaque entité"
T_ENJEUX = "Chaque enjeu cité trouve sa réponse dans une partie de l'offre"
CIBLE_REROUTAGE = "Démarche"  # cible de l'annexe qui prend les traits de « Notre approche » : la plus proche apres elle
NUMEROS = {"DÉMARCHE GÉNÉRALE": "03", "DÉMARCHE DÉTAILLÉE": "04", "DISPOSITIF ET PRIX": "05"}
NUMERO_CHAPITRE = {"Démarche générale": "03", "Démarche détaillée": "04", "Dispositif et prix": "05"}
KICKER = re.compile(r"^(\d{2}) · (DÉMARCHE GÉNÉRALE|DÉMARCHE DÉTAILLÉE|DISPOSITIF ET PRIX) · (\d+/\d+)$")

EMU_ECART = 50800
X_NAV_FIN_TRAIT = 5461000  # bord droit des traits cote enjeu
LIBELLES_CIBLES = ["Contexte et enjeux", "Nos convictions", "Notre approche", "Démarche", "Démarche détaillée", "Dispositif et prix"]


def _base():
    return Presentation(deck_base.resoudre_base(BASE))


def _texte(sh):
    return sh.text_frame.text if sh.has_text_frame else ""


def _titre(s):
    return s.shapes.title.text_frame.text if s.shapes.title is not None else ""


def _est_intercalaire_approche(s):
    return s.slide_layout.name.startswith("50 -") and any(_texte(sh) == CHAPITRE for sh in s.shapes)


def _ids_a_supprimer():
    prs = _base()
    trouvees = [s for s in prs.slides if _est_intercalaire_approche(s) or _titre(s) in (T_COACH, T_ENTREE)]
    assert len(trouvees) == 3, f"{len(trouvees)} slides du chapitre trouvees, 3 attendues"
    return [f"id:{s.slide_id}" for s in trouvees]


def _ids_nav():
    prs = _base()
    supprimees = {int(x[3:]) for x in _ids_a_supprimer()}
    return [f"id:{s.slide_id}" for s in prs.slides if s.slide_id not in supprimees and any(sh.name.startswith("nav-") for sh in s.shapes)]


def _ids_chapitres():
    """Intercalaires numerotes et slides portant un surtitre « 0n · DEMARCHE... / DISPOSITIF ET PRIX · n/N »."""
    prs = _base()
    ids = []
    for s in prs.slides:
        interc = s.slide_layout.name.startswith("50 -") and not any(_texte(sh) == CHAPITRE for sh in s.shapes)
        if interc or any(KICKER.match(_texte(sh)) for sh in s.shapes):
            ids.append(f"id:{s.slide_id}")
    return ids


def _ids_sommaire():
    return [f"id:{s.slide_id}" for s in _base().slides if s.slide_layout.name.startswith("95 -")]


def _ids_enjeux():
    return [f"id:{s.slide_id}" for s in _base().slides if _titre(s) == T_ENJEUX]


# ---------------------------------------------------------------- etape 1 : navigation + section
def navigation(prs):
    """Retire « nav-Notre approche » et rejoint les pastilles restantes (meme largeur, meme ecart, meme bord gauche) ; la pastille active n'est pas touchee."""
    for s in prs.slides:
        pastilles = sorted((sh for sh in s.shapes if sh.name.startswith("nav-")), key=lambda sh: sh.left)
        if not pastilles:
            continue
        noms = [sh.name[4:] for sh in pastilles]
        if CHAPITRE not in noms:
            continue
        if len(pastilles) != 7:
            raise ValueError(f"{len(pastilles)} pastilles au lieu de 7 : {noms}")
        ecart = pastilles[1].left - (pastilles[0].left + pastilles[0].width)
        if ecart != EMU_ECART:
            raise ValueError(f"ecart entre pastilles {ecart} EMU, {EMU_ECART} attendus")
        for sh in pastilles:
            if sh.name == f"nav-{CHAPITRE}":
                sh._element.getparent().remove(sh._element)
        x = pastilles[0].left
        for sh in (p for p in pastilles if p.name != f"nav-{CHAPITRE}"):
            if sh.left != x:
                sh.left = x
            x += sh.width + ecart


def section_vide(prs):
    """Retire la section p14 « Notre approche » (vide apres la suppression de ses slides)."""
    for sec in list(prs.part._element.iter(f"{{{deck_draw.P14}}}section")):
        if sec.get("name") == CHAPITRE:
            if list(sec.iter(f"{{{deck_draw.P14}}}sldId")):
                raise ValueError("la section « Notre approche » n'est pas vide")
            sec.getparent().remove(sec)


def etape_navigation(prs):
    navigation(prs)
    section_vide(prs)


# ---------------------------------------------------------------- etape 2 : numeros de chapitre
def numeros(prs):
    for s in prs.slides:
        if s.slide_layout.name.startswith("50 -"):
            nom = next((_texte(sh) for sh in s.shapes if sh.is_placeholder and sh.top > 1500000 and _texte(sh) and not re.fullmatch(r"\d{2}|[A-Z]", _texte(sh))), None)
            if nom in NUMERO_CHAPITRE:
                for sh in s.shapes:
                    if sh.is_placeholder and re.fullmatch(r"\d{2}", _texte(sh)) and _texte(sh) != NUMERO_CHAPITRE[nom]:
                        deck_draw.set_run(sh, NUMERO_CHAPITRE[nom])
        for sh in s.shapes:
            m = KICKER.match(_texte(sh))
            if m and m.group(1) != NUMEROS[m.group(2)]:
                deck_draw.set_run(sh, f"{NUMEROS[m.group(2)]} · {m.group(2)} · {m.group(3)}")


# ---------------------------------------------------------------- etape 3 : sommaire
def sommaire(prs):
    s = next(x for x in prs.slides if x.slide_layout.name.startswith("95 -"))
    suite = {"Notre approche": "Démarche générale", "Démarche générale": "Démarche détaillée", "Démarche détaillée": "Dispositif et prix", "Dispositif et prix": "Annexes"}
    phs = {_texte(sh): sh for sh in s.shapes if sh.is_placeholder and _texte(sh) in suite}
    if set(phs) != set(suite):
        raise ValueError(f"entrees du sommaire inattendues : {sorted(phs)}")
    for ancien, sh in phs.items():
        deck_draw.set_run(sh, suite[ancien])
    boite_annexes = next(sh for sh in s.shapes if not sh.is_placeholder and _texte(sh) == "Annexes")
    boite_annexes._element.getparent().remove(boite_annexes._element)  # l'entree « Annexes » est desormais un emplacement du gabarit
    goutte = next(sh for sh in s.shapes if not sh.is_placeholder and sh._element.spPr.find(".//{http://schemas.openxmlformats.org/drawingml/2006/main}prstGeom").get("prst") == "teardrop")
    lettre = next(sh for sh in s.shapes if not sh.is_placeholder and _texte(sh) == "A")
    masque = next(sh for sh in s.shapes if sh.name.startswith("Rectangle") and not _texte(sh) and sh.width == 723900)
    # la pastille « A » remonte de l'emplacement 07 a l'emplacement 06 du gabarit (meme pas vertical que le gabarit : 722 925 EMU pour la goutte, 733 451 pour le chiffre)
    goutte.top = goutte.top - 722925
    lettre.top = lettre.top - 733451
    neuf = copy.deepcopy(masque._element)  # masque blanc de la pastille « 06 » du gabarit, sous la goutte
    neuf.nvSpPr.cNvPr.set("id", str(max(sh.shape_id for sh in s.shapes) + 1))
    neuf.nvSpPr.cNvPr.set("name", "Masque pastille 06")
    neuf.spPr.xfrm.off.set("y", str(masque.top - 722925))
    goutte._element.addprevious(neuf)


# ---------------------------------------------------------------- etape 4 : annexe des enjeux
def annexe_enjeux(prs):
    s = deck_draw.slide_par_titre(prs, T_ENJEUX)
    formes = list(s.shapes)
    etiquettes = {sh.top: _texte(sh) for sh in formes if sh.shape_type == 17 and sh.left == 6985000 and _texte(sh) in LIBELLES_CIBLES}
    if sorted(etiquettes.values()) != sorted(LIBELLES_CIBLES):
        raise ValueError(f"cibles inattendues : {sorted(etiquettes.values())}")
    # groupes cibles : les 4 formes (2 ovales, pilule, texte) dont le haut tombe dans la bande de la pilule
    groupes = {}
    for top, libelle in etiquettes.items():
        pilule = next(sh for sh in formes if sh.shape_type == 1 and sh.left == 6908800 and sh.top == top)
        bande = (pilule.top, pilule.top + pilule.height)
        groupes[libelle] = [sh for sh in formes if sh.shape_type != 9 and sh.left >= 6667500 and bande[0] <= sh.top + sh.height / 2 <= bande[1]]
        if len(groupes[libelle]) != 4:
            raise ValueError(f"cible {libelle} : {len(groupes[libelle])} formes au lieu de 4")
    centre = {lib: next(sh for sh in g if sh.shape_type == 1 and sh.left == 6908800) for lib, g in groupes.items()}
    ancien_centre = {lib: p.top + p.height // 2 for lib, p in centre.items()}
    restants = [lib for lib in LIBELLES_CIBLES if lib != CHAPITRE]
    premier, dernier = ancien_centre[restants[0]], ancien_centre[restants[-1]]
    nouveau_centre = {lib: premier + k * (dernier - premier) // (len(restants) - 1) for k, lib in enumerate(restants)}
    # traits : (enjeu y, cible y) -> nouvelle cible, avant tout deplacement
    traits = []
    for sh in formes:
        if sh.shape_type == 9:
            flip = sh._element.spPr.xfrm.get("flipV") == "1"
            y_enjeu, y_cible = (sh.top + sh.height, sh.top) if flip else (sh.top, sh.top + sh.height)
            lib = min(ancien_centre, key=lambda k: abs(ancien_centre[k] - y_cible))
            if abs(ancien_centre[lib] - y_cible) > 2000:
                raise ValueError(f"trait {sh.name} : fin a {y_cible} ne rejoint aucune cible")
            traits.append((sh, y_enjeu, lib))
    for sh in groupes[CHAPITRE]:
        sh._element.getparent().remove(sh._element)
    for lib in restants:
        d = nouveau_centre[lib] - ancien_centre[lib]
        for sh in groupes[lib]:
            sh.top = sh.top + d
    for sh, y_enjeu, lib in traits:
        cible = CIBLE_REROUTAGE if lib == CHAPITRE else lib
        y_cible = nouveau_centre[cible]
        xfrm = sh._element.spPr.xfrm
        sh.top, sh.height = min(y_enjeu, y_cible), abs(y_cible - y_enjeu)
        if y_cible < y_enjeu:
            xfrm.set("flipV", "1")
        elif "flipV" in xfrm.attrib:
            del xfrm.attrib["flipV"]


OPS = [{"slide": sel, "op": "supprimer"} for sel in _ids_a_supprimer()]

ETAPES = [
    {"declarer": _ids_nav(), "f": etape_navigation, "nouvelles_max": 0, "nom": "navigation a 6 pastilles + section Notre approche retiree"},
    {"declarer": _ids_chapitres(), "f": numeros, "nouvelles_max": 0, "nom": "numeros de chapitre 03/04/05 (intercalaires et surtitres)"},
    {"declarer": _ids_sommaire(), "f": sommaire, "nouvelles_max": 0, "nom": "sommaire a six entrees"},
    {"declarer": _ids_enjeux(), "f": annexe_enjeux, "nouvelles_max": 0, "nom": "annexe des enjeux : cible Notre approche retiree, traits reroutes"},
]
