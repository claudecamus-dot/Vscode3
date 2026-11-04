"""Delta V37zA (base V36) : suppression du chapitre « Annexes » et toutes ses consequences (demande : « supprime les annexes »).

Meme methode que delta_V34a (chapitre « Notre approche ») :
- l'intercalaire « Annexes » et ses 12 slides sont retires par l'op `supprimer` du core (la seule voie que deck_garde accepte) ; ils sont identifies par titre exact / gabarit a
  l'import sur la base, jamais par rang ; 13 slides attendues (53 -> 40) ;
- navigation : la pastille « nav-Annexes » disparait de chaque slide ; les 5 restantes gardent largeur, hauteur, ecart (50 800 EMU) et ordre, et sont recalees pour que leur
  bord DROIT reste a x = 659,25 pt (8 372 475 EMU) : la bande glisse vers la droite de la largeur de la pastille retiree + l'ecart ; la pastille active n'est pas retouchee
  (style), seule sa position suit la bande ;
- sections p14 : la section « Annexes », vide, est retiree ;
- sommaire : l'entree « A · Annexes » (placeholder, goutte, lettre) est retiree ; 01 a 05 restent sur les emplacements du gabarit (4 a gauche, 1 a droite), les deux masques blancs
  qui cachent les pastilles 06 et 07 du gabarit restent en place.
Aucune slide visible hors sommaire ne mentionne les annexes ; les references des notes sont rapportees, pas editees (slides d'autres lots).
Usage (depuis docs/cadrage-ppt/) : py deck_delta/deck.py delta_V37zA --base V36 --sortie C:/tmp/deck-v37-zA/V37zA.pptx --sans-rendu
"""
import deck_base
import deck_draw
from pptx import Presentation

BASE = "V36"
NOTE = "V37zA : chapitre Annexes supprime (13 slides), navigation a 5 pastilles alignee a droite, sommaire a 5 entrees"

CHAPITRE = "Annexes"
TITRES = [
    "Problèmes 1 à 5 : chacun trouve son apport et son indicateur",
    "Problèmes 6 à 10 : chacun trouve son apport et son indicateur",
    "Les alternatives sont des compléments que l'offre intègre",
    "Qui décide quoi, quand entrer, quand passer la main : modèle d'engagement",
    "Infra agent-ready : une option selon la maturité, jamais un prérequis",
    "Chaque enjeu cité trouve sa réponse dans une partie de l'offre",
    "Fiche de phase : l'Assessment flash fixe la référence et choisit le pilote",
    "Fiche de phase type, appliquée au pilote : un gabarit pour chaque phase",
    "Fiche référence : un gabarit prêt à recevoir les références d'OCTO",
    "Le scénario déroule six étapes, du problème au choix du client",
    "Des agents augmentent le coach ; d'autres améliorent l'Infra du client",
    "Trois principes de conduite : le service, l'adoption, le binôme",
]
EMU_ECART = 50800
X_DROIT = 8372475  # 659,25 pt : bord droit de la bande de navigation
NS_A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"


def _base():
    return Presentation(deck_base.resoudre_base(BASE))


def _texte(sh):
    return sh.text_frame.text if sh.has_text_frame else ""


def _titre(s):
    return s.shapes.title.text_frame.text if s.shapes.title is not None else ""


def _est_intercalaire(s):
    return s.slide_layout.name.startswith("50 -") and any(_texte(sh) == CHAPITRE for sh in s.shapes)


def _a_supprimer():
    """Les slides du chapitre : titre exact (12) ou intercalaire (1). Un titre commence par le debut de celui de la base (le titre complet peut etre plus long)."""
    prs = _base()
    trouvees = []
    for s in prs.slides:
        t = _titre(s)
        if _est_intercalaire(s) or any(t == x or (len(t) > 40 and x.startswith(t[:40])) for x in TITRES):
            trouvees.append(s)
    assert len(trouvees) == 13, f"{len(trouvees)} slides du chapitre trouvees, 13 attendues"
    return trouvees


def _ids_a_supprimer():
    return [f"id:{s.slide_id}" for s in _a_supprimer()]


def _ids_nav():
    prs = _base()
    supprimees = {s.slide_id for s in _a_supprimer()}
    return [f"id:{s.slide_id}" for s in prs.slides if s.slide_id not in supprimees and any(sh.name.startswith("nav-") for sh in s.shapes)]


def _ids_sommaire():
    return [f"id:{s.slide_id}" for s in _base().slides if s.slide_layout.name.startswith("95 -")]


# ---------------------------------------------------------------- etape 1 : navigation + section
def navigation(prs):
    """Retire « nav-Annexes » et recale les 5 pastilles restantes pour que leur bord droit soit a 659,25 pt (meme largeur, meme ecart, meme ordre)."""
    for s in prs.slides:
        pastilles = sorted((sh for sh in s.shapes if sh.name.startswith("nav-")), key=lambda sh: sh.left)
        if not pastilles:
            continue
        noms = [sh.name[4:] for sh in pastilles]
        if CHAPITRE not in noms:
            continue
        if len(pastilles) != 6 or noms[-1] != CHAPITRE:
            raise ValueError(f"{len(pastilles)} pastilles, « Annexes » pas en derniere position : {noms}")
        ecart = pastilles[1].left - (pastilles[0].left + pastilles[0].width)
        if ecart != EMU_ECART:
            raise ValueError(f"ecart entre pastilles {ecart} EMU, {EMU_ECART} attendus")
        annexes, restantes = pastilles[-1], pastilles[:-1]
        annexes._element.getparent().remove(annexes._element)
        decalage = X_DROIT - (restantes[-1].left + restantes[-1].width)
        for sh in restantes:
            sh.left = sh.left + decalage


def section_vide(prs):
    """Retire la section p14 « Annexes » (vide apres la suppression de ses slides)."""
    for sec in list(prs.part._element.iter(f"{{{deck_draw.P14}}}section")):
        if sec.get("name") == CHAPITRE:
            if list(sec.iter(f"{{{deck_draw.P14}}}sldId")):
                raise ValueError("la section « Annexes » n'est pas vide")
            sec.getparent().remove(sec)


def etape_navigation(prs):
    navigation(prs)
    section_vide(prs)


# ---------------------------------------------------------------- etape 2 : sommaire
def sommaire(prs):
    """Retire l'entree « A · Annexes » : placeholder, goutte, lettre. Les masques blancs des pastilles 06 et 07 du gabarit restent."""
    s = next(x for x in prs.slides if x.slide_layout.name.startswith("95 -"))
    entree = [sh for sh in s.shapes if sh.is_placeholder and _texte(sh) == CHAPITRE]
    goutte = [sh for sh in s.shapes if not sh.is_placeholder and sh._element.spPr.find(f".//{NS_A}prstGeom") is not None
              and sh._element.spPr.find(f".//{NS_A}prstGeom").get("prst") == "teardrop"]
    lettre = [sh for sh in s.shapes if not sh.is_placeholder and _texte(sh) == "A"]
    if len(entree) != 1 or len(goutte) != 1 or len(lettre) != 1:
        raise ValueError(f"entree Annexes inattendue : {len(entree)} placeholder, {len(goutte)} goutte, {len(lettre)} lettre")
    for sh in entree + goutte + lettre:
        sh._element.getparent().remove(sh._element)


OPS = [{"slide": sel, "op": "supprimer"} for sel in _ids_a_supprimer()]

ETAPES = [
    {"declarer": _ids_nav(), "f": etape_navigation, "nouvelles_max": 0, "nom": "navigation a 5 pastilles alignee a droite + section Annexes retiree"},
    {"declarer": _ids_sommaire(), "f": sommaire, "nouvelles_max": 0, "nom": "sommaire a cinq entrees"},
]
