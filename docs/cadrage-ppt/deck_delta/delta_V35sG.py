"""Delta V35sG (base V34, lot sG du chantier V35) : « Conviction 13 » passe de dix modeles techniques a cinq formes lisibles.

- la liste M1..M10 et les trois combinaisons laissent la place a CINQ formes d'organisation en cartes cote a cote (nom, definition en une ligne, « Pour ... »),
  sous une fleche de lecture « par specialite technique -> par produit et par service rendu » ;
- un bandeau navy porte le message : chaque entite choisit sa forme (maturite, criticite, taille), aucune n'est imposee ;
- le bas de slide (LE CRITERE OBSERVABLE / LE CHANTIER) est conserve tel quel, remonte pour laisser la place aux cartes ;
- les cinq autres modeles du benchmark, les combinaisons et la reserve sur la predominance partent dans les notes.
Forme copiee de la slide 15 du deck Vscode8 (v5.117, « modeles d'organisation observes sur le marche ») : fleche de spectre + cinq cartes numerotees cote a cote
+ bandeau bas ; reproduite en vocabulaire maison (round2DiagRect, carres numerotes cyan, panneaux gris), aucun texte repris.
Chrome intact : points de progression (y 70), filet cyan (y 86), pastilles « nav-* », titre, numero de page, pilule CONVICTION 13.
Usage (depuis docs/cadrage-ppt/) : py deck_delta/deck.py delta_V35sG --base C:/tmp/deck-v35/V35g.pptx --sortie C:/tmp/deck-v35-sG/V35sG.pptx --sans-rendu
"""
import deck_base
import deck_draw
from forme_v9 import BLANC, LINE, NAVY, PANEL, S, carre_num_cyan, carte_diag, forme, tx
from pptx import Presentation
from pptx.enum.text import MSO_ANCHOR as A
from pptx.enum.text import PP_ALIGN as P

BASE = "V34"
NOTE = "V35sG : Conviction 13, cinq formes d'organisation en cartes cote a cote (fleche de lecture, bandeau « choisi, pas impose »), bas de slide conserve"
OPS = []

NB = "\u00a0"
EMU = 12700

# (nom, definition en une ligne, « Pour ... ») : formes M1, M3, M4, M9, M10 du benchmark ; contextes pertinents = fiches section 5 du benchmark
FORMES = [
    ("Silos technologiques", "Une équipe par spécialité technique.", "Pour parcs historiques et expertises rares"),
    ("Services mutualisés", "Un centre commun livre des services sur catalogue.", "Pour plusieurs entités aux besoins répétables"),
    ("Orienté services", "Un responsable garantit le service de bout en bout.", "Pour des services traversant plusieurs équipes"),
    ("Plateforme produit", "Des plateformes internes gérées comme des produits.", "Pour demandes répétées, nombreux clients internes"),
    ("Fédéré / hybride", "Un noyau commun et des équipes autonomes.", "Pour grands groupes aux entités multiples"),
]
MESSAGE = "Chaque entité choisit sa forme selon sa maturité, sa criticité et sa taille" + NB + ": aucune n'est imposée."
FLECHE_G, FLECHE_D = "Par spécialité technique", "Par produit et par service rendu"
SOURCE = ("Source" + NB + ": benchmark des modèles d'organisation Infrastructure IT (3 novembre 2026)" + NB
          + ": synthèse de référentiels, hypothèses de travail, non représentative.")
NOTES = (
    "V35sG. Le benchmark ne mesure pas la part de chaque modèle dans les directions Infra (section 2.4 : aucune enquête ne le permet) : les cinq formes ne sont donc pas "
    "classées par fréquence mais retenues parce que la grille de diagnostic du benchmark les nomme (silos, services mutualisés, plateforme, fédéré, section 10.1) "
    "et que la matrice par profil (section 7.1) recommande surtout l'orientation services (7 profils sur 9) et la plateforme (6 sur 9). La fleche les lit de la spécialité technique au produit. "
    "Les cinq autres modèles du benchmark : Build / Run séparés, décentralisation par BU ou domaine, externalisation / SIAM, Cloud / CCoE, DevOps / SRE. "
    "Combinaisons fréquentes citées par le benchmark (section 4.2) : silos + orienté services ; services mutualisés + plateforme ; fédéré + orienté services + plateforme."
)


def _titre():
    prs = Presentation(deck_base.resoudre_base(BASE))
    t = [s.shapes.title.text_frame.text for s in prs.slides if s.shapes.title is not None and s.shapes.title.text_frame.text.startswith("Conviction 13")]
    if len(t) != 1:
        raise ValueError(f"Conviction 13 : {len(t)} slide(s) ; 1 exigee")
    return t[0]


T_CONV13 = _titre()


def _retirer(sh):
    sh._element.getparent().remove(sh._element)


def _est_pilule_conviction(sh):
    """La pilule « CONVICTION 13 » (forme arrondie 130 x 22 a (45, 98) et son texte) : chrome de la famille, conservee."""
    return abs(sh.top - 98 * EMU) < EMU and abs(sh.left - 45 * EMU) < EMU and abs(sh.width - 130 * EMU) < EMU and abs(sh.height - 22 * EMU) < EMU or (
        sh.has_text_frame and sh.text_frame.text.startswith("CONVICTION"))


def conviction13(prs):
    s = deck_draw.slide_par_titre(prs, T_CONV13)
    dy_pied = 15  # le pied remonte de 284 -> 299 (cartes) : pilules +15, cadres +15, contenu +7,5
    for sh in list(s.shapes):
        if sh.is_placeholder or sh.name.startswith("nav-"):
            continue
        h = sh.top / EMU
        if h < 92:  # points de progression (y 70) et filet cyan (y 86) : chrome
            continue
        if _est_pilule_conviction(sh):
            continue
        if h < 268:  # corps ancien : dix modeles + combinaisons
            _retirer(sh)
            continue
        if h > 360:  # ligne de source
            if sh.has_text_frame and sh.text_frame.text.startswith("Source"):
                r = sh.text_frame.paragraphs[0].runs
                r[0].text = SOURCE
                for extra in r[1:]:
                    extra.text = ""
            continue
        # pied : pilules d'etiquette (h 22), cadres (h 76), contenu (pictos, textes)
        hh = sh.height / EMU
        if abs(hh - 22) < 1 or abs(hh - 76) < 1:
            sh.top = sh.top + int(dy_pied * EMU)
            if abs(hh - 76) < 1:
                sh.height = int(62 * EMU)
        else:
            sh.top = sh.top + int(7.5 * EMU)
    # fleche de lecture, a droite de la pilule CONVICTION 13
    forme(s, S.PENTAGON, 190, 98, 469, 22, PANEL, None, adj=0.5)
    tx(s, 204, 98, 200, 22, [[(FLECHE_G, 10, True, NAVY)]], A.MIDDLE, P.LEFT)
    tx(s, 400, 98, 235, 22, [[(FLECHE_D, 10, True, NAVY)]], A.MIDDLE, P.RIGHT)
    # cinq cartes
    n, gap, x0, w, y0, h = len(FORMES), 8, 45, 0, 128, 132
    w = (614 - gap * (n - 1)) / n
    for k, (nom, defin, pour) in enumerate(FORMES):
        x = x0 + k * (w + gap)
        carte_diag(s, x, y0, w, h, adj=0.08)
        carre_num_cyan(s, x + 8, y0 + 9, 18, k + 1, sz=10)
        tx(s, x + 31, y0 + 6, w - 37, 24, [[(nom, 10.5, True, NAVY)]], A.MIDDLE)
        forme(s, S.RECTANGLE, x + 8, y0 + 36, w - 16, 0.75, LINE, None)
        tx(s, x + 8, y0 + 41, w - 16, 44, [[(defin, 10, False, NAVY)]], A.TOP)
        forme(s, S.ROUNDED_RECTANGLE, x + 6, y0 + 86, w - 12, 40, PANEL, None, adj=0.18)
        tx(s, x + 11, y0 + 86, w - 22, 40, [[(pour, 10, False, NAVY)]], A.MIDDLE)
    # bandeau message
    forme(s, S.ROUNDED_RECTANGLE, 45, 265, 614, 17, NAVY, None, adj=0.5)
    tx(s, 55, 265, 594, 17, [[(MESSAGE, 10.5, True, BLANC)]], A.MIDDLE, P.CENTER)
    s.notes_slide.notes_text_frame.text = NOTES


def _ids():
    prs = Presentation(deck_base.resoudre_base(BASE))
    return f"id:{deck_draw.slide_par_titre(prs, T_CONV13).slide_id}"


ETAPES = [
    {"declarer": [_ids()], "f": conviction13, "nouvelles_max": 0, "nom": "Conviction 13 : cinq formes d'organisation en cartes + bandeau choisi/pas impose"},
]
