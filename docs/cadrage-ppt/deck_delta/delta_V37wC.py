"""Delta V37wC (base V36) : convictions 7 and 8 reworded after the user's review ; conviction 9 left identical.

- 7 : the AVANT team line says teams are most often in silos by specialty, sometimes dissolved at the end of the project.
- 8 : row 1 = a team PO in a product culture, one team that builds (build) and runs (run) ; row 2 = augmented roles
  (PO, technical referent, operations), role names flagged « à valider ».
- Left rail, progress dots, filet, nav pills, title, notes already present : untouched (the removed sentences are appended to the notes).
Usage (from docs/cadrage-ppt/) : py deck_delta/deck.py delta_V37wC --base V36 --sortie C:/tmp/deck-v37-wC/V37wC.pptx --sans-rendu
"""
import deck_base
import deck_draw
from forme_ground import coche
from forme_v9 import (
    BLANC,
    CYAN,
    LINE,
    NAVY,
    PANEL,
    SLATE,
    S,
    carre_num_cyan,
    carte_diag,
    forme,
    pilule_entete,
    tx,
)
from pptx import Presentation
from pptx.enum.text import MSO_ANCHOR as A
from pptx.enum.text import PP_ALIGN as P

BASE = "V36"
NOTE = "V37wC : conviction 7 (equipes souvent en silos), conviction 8 (PO d'equipe, build et run, roles augmentes)"
OPS = []

NB = "\u00a0"
T_FINANCER = "Conviction 7 : financer des produits et des équipes stables"
T_EQUIPE = "Conviction 8 : une petite équipe produit qui construit et exploite"
TITRES = (T_FINANCER, T_EQUIPE)

ZX, ZW = 258, 401.25
EMU = 12700


def _vider_corps(s):
    """Retire le corps (x >= 185 pt, y >= 92 pt) ; le rail, les points, le filet, les pastilles de navigation et le titre restent."""
    for sh in list(s.shapes):
        if sh.is_placeholder or sh.name.startswith("nav-"):
            continue
        if sh.left >= 185 * EMU and sh.top >= 92 * EMU:
            sh._element.getparent().remove(sh._element)


def _notes(s, retire):
    tf = s.notes_slide.notes_text_frame
    ancien = tf.text.strip()
    parts = [ancien] if ancien else []
    parts.append("Retiré en V37 (reformulé sur la slide)" + NB + ": " + " ".join(retire))
    tf.text = "\n".join(parts)


def _chevron_bas(s, cx, cy):
    c = forme(s, S.CHEVRON, cx - 6.5, cy - 12, 13, 24, CYAN, None, adj=0.35)
    c.rotation = 90
    return c


def _pastille(s, x, y, w, h, texte, couleur, sz=10.5):
    forme(s, S.ROUNDED_RECTANGLE, x, y, w, h, couleur, None, adj=0.5)
    tx(s, x, y, w, h, [[(texte, sz, True, BLANC if couleur == NAVY else NAVY)]], A.MIDDLE, P.CENTER)


# ================================================================ conviction 7
def financer(prs):
    s = deck_draw.slide_par_titre(prs, T_FINANCER)
    _vider_corps(s)
    rows = [
        (102, 96, False, "AVANT", "Un budget par projet", "financé projet par projet",
         "le plus souvent en silos par spécialité ; parfois dissoute à la fin du projet.", 3,
         "transféré à d'autres équipes."),
        (214, 76, True, "APRÈS", "Une capacité par produit", "budget annuel rattaché au produit",
         "stable, elle construit et exploite.", 2, "reste dans l'équipe qui construit."),
    ]
    for y, ch, apres, pastille, titre, sous, equipe, nl, run in rows:
        if apres:
            forme(s, S.ROUND_2_DIAG_RECTANGLE, ZX, y, ZW, ch, NAVY, None, adj=0.1)
            ink, doux = BLANC, BLANC
        else:
            carte_diag(s, ZX, y, ZW, ch, adj=0.1)
            ink, doux = NAVY, SLATE
        _pastille(s, ZX + 14, y - 9, 66, 18, pastille, CYAN if apres else PANEL)
        tx(s, ZX + 16, y + 16, 176, 22, [[(titre, 14, True, ink)]], A.TOP)
        tx(s, ZX + 16, y + 39, 168, 32, [[(sous, 11.5, False, doux)]], A.TOP)
        forme(s, S.RECTANGLE, ZX + 200, y + 12, 0.75, ch - 24, BLANC if apres else LINE, None)
        h_eq = 14.8 * nl + 2
        tx(s, ZX + 212, y + 9, ZW - 224, h_eq, [[("Équipe" + NB + ": ", 12, True, ink), (equipe, 12, False, ink)]], A.TOP)
        tx(s, ZX + 212, y + 9 + h_eq + 4, ZW - 224, 31, [[("RUN" + NB + ": ", 12, True, ink), (run, 12, False, ink)]], A.TOP)
    _chevron_bas(s, ZX + ZW / 2, 205)
    py_, ph = 308, 58
    forme(s, S.ROUNDED_RECTANGLE, ZX, py_, ZW, ph, PANEL, None, adj=0.15)
    pilule_entete(s, ZX + 14, py_ - 9, 170, 18, "PRODUIT OU COMPOSANT", NAVY, sz=10)
    tx(s, ZX + 16, py_ + 11, ZW - 32, 17, [[("Un produit a une offre, une valeur et des engagements.", 12.5, True, NAVY)]], A.MIDDLE)
    tx(s, ZX + 16, py_ + 33, 190, 17, [[("Produits" + NB + ": ", 12, True, NAVY), ("Kubernetes, CI/CD, IAM", 12, False, NAVY)]], A.MIDDLE)
    tx(s, ZX + 214, py_ + 33, 175, 17, [[("Composants" + NB + ": ", 12, True, NAVY), ("VM, serveur, SAN", 12, False, NAVY)]], A.MIDDLE)
    _notes(s, ["« Équipe" + NB + ": dissoute à la fin du projet. »"])


# ================================================================ conviction 8
def equipe(prs):
    s = deck_draw.slide_par_titre(prs, T_EQUIPE)
    _vider_corps(s)
    lignes = [
        (96, 124, 1, "Équipe produit", "SANS IA", PANEL, [
            [("Un PO d'équipe dans une culture produit, en binôme avec un référent technique.", 3),
             ("Une même équipe construit (build) et exploite (run).", 2)],
            [("Du temps de construction protégé.", 2),
             ("Demandes récurrentes automatisées, en self-service.", 2)],
        ]),
    ]
    colw = 182
    for y, h, num, titre, chip, couleur, cols in lignes:
        carte_diag(s, ZX, y, ZW, h, adj=0.08)
        carre_num_cyan(s, ZX + 12, y + 8, 22, num, sz=12)
        tx(s, ZX + 42, y + 8, 120, 22, [[(titre, 13.5, True, NAVY)]], A.MIDDLE)
        _pastille(s, ZX + ZW - 12 - 90, y + 10, 90, 18, chip, couleur, sz=10)
        for k, col in enumerate(cols):
            x = ZX + 14 + k * (colw + 12)
            yy = y + 38
            for t, nl in col:
                coche(s, x + 6.5, yy + 7.5, 13)
                tx(s, x + 18, yy, colw - 18, 14.8 * nl, [[(t, 12, False, NAVY)]], A.TOP)
                yy += 14.8 * nl + 6
    # ligne 2 : roles augmentes, une ligne par role
    y, h = 234, 132
    carte_diag(s, ZX, y, ZW, h, adj=0.08)
    carre_num_cyan(s, ZX + 12, y + 8, 22, 2, sz=12)
    tx(s, ZX + 42, y + 8, 120, 22, [[("Équipe augmentée", 13.5, True, NAVY)]], A.MIDDLE)
    _pastille(s, ZX + ZW - 12 - 218, y + 10, 218, 18, "AVEC IA · OPTION SELON LA MATURITÉ", NAVY, sz=10)
    roles = [
        ("PO augmenté" + NB + ":", " arbitrages préparés."),
        ("Référent technique augmenté" + NB + ":", " diagnostic préparé."),
        ("Exploitation augmentée" + NB + ":", " travail récurrent préparé."),
    ]
    for k, (role, reste) in enumerate(roles):
        yy = y + 37 + k * 19
        coche(s, ZX + 20.5, yy + 7.5, 13)
        tx(s, ZX + 32, yy, ZW - 48, 16, [[(role, 12, True, NAVY), (reste, 12, False, NAVY)]], A.TOP)
    # pied : decision humaine, rien n'est promis ; drapeau d'hypothese sur les intitules
    yb = y + 96
    tx(s, ZX + 16, yb, 270, 30, [[("Les agents préparent ; l'humain décide et en répond.", 11, False, SLATE)], [("Effets visés, à mesurer ; rien n'est promis.", 11, False, SLATE)]], A.MIDDLE)
    _pastille(s, ZX + ZW - 12 - 108, yb + 6, 108, 18, "RÔLES À VALIDER", PANEL, sz=10)
    _chevron_bas(s, ZX + ZW / 2, 230)
    _notes(s, [
        "« Un binôme" + NB + ": responsable produit et référent technique. Pas un PO posé dans l'Infra. »",
        "« Une même équipe conçoit, livre et assure le service. »",
        "« Mêmes rôles, plus des agents. »",
        "« Les agents préparent le travail récurrent et le diagnostic. »",
        "« L'IA prépare ; l'humain décide et en répond. »",
        "Intitulés des rôles augmentés (PO augmenté, référent technique augmenté, exploitation augmentée) : proposition, à valider.",
    ])


def _ids():
    prs = Presentation(deck_base.resoudre_base(BASE))
    return [f"id:{deck_draw.slide_par_titre(prs, t).slide_id}" for t in TITRES]


_I = dict(zip(TITRES, _ids(), strict=True))
ETAPES = [
    {"declarer": [_I[T_FINANCER]], "f": financer, "nouvelles_max": 0, "nom": "conviction 7 : equipes souvent en silos"},
    {"declarer": [_I[T_EQUIPE]], "f": equipe, "nouvelles_max": 0, "nom": "conviction 8 : PO d'equipe, build et run, roles augmentes"},
]
