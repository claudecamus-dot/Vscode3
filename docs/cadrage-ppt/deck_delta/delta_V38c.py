"""Delta V38c (base V37) : conviction 8 re-laid out to use the space (user request on slide 14).

- Cards widened from x=258 to x=186 (the 88 pt gap after the rail pictogram is used), width 473.25.
- Row 1 : the four bullets in one full-width column (one line each, no uneven columns).
- Row 2 : roles at 12.5 pt ; footer sentences and « RÔLES À VALIDER » pill on their own band under a hairline.
- Same text, notes untouched. Rail, dots, filet, nav pills, title : untouched.
Usage (from docs/cadrage-ppt/) : py deck_delta/deck.py delta_V38c --base V37 --sortie C:/tmp/deck-v38-c/V38c.pptx --sans-rendu
"""
import deck_base
import deck_draw
from forme_ground import coche
from forme_v9 import BLANC, CYAN, LINE, NAVY, PANEL, SLATE, S, carre_num_cyan, carte_diag, forme, tx
from pptx import Presentation
from pptx.enum.text import MSO_ANCHOR as A
from pptx.enum.text import PP_ALIGN as P

BASE = "V37"
NOTE = "V38c : conviction 8, cartes elargies, puces sur une colonne, pied degage"
OPS = []

NB = "\u00a0"
T_EQUIPE = "Conviction 8 : une petite équipe produit qui construit et exploite"
ZX, ZW = 186, 473.25
EMU = 12700


def _vider_corps(s):
    for sh in list(s.shapes):
        if sh.is_placeholder or sh.name.startswith("nav-"):
            continue
        if sh.left >= 185 * EMU and sh.top >= 92 * EMU:
            sh._element.getparent().remove(sh._element)


def _pastille(s, x, y, w, h, texte, couleur, sz=10.5):
    forme(s, S.ROUNDED_RECTANGLE, x, y, w, h, couleur, None, adj=0.5)
    tx(s, x, y, w, h, [[(texte, sz, True, BLANC if couleur == NAVY else NAVY)]], A.MIDDLE, P.CENTER)


def _entete(s, y, num, titre, chip, couleur, cw):
    carre_num_cyan(s, ZX + 12, y + 8, 22, num, sz=12)
    tx(s, ZX + 42, y + 8, 200, 22, [[(titre, 14, True, NAVY)]], A.MIDDLE)
    _pastille(s, ZX + ZW - 12 - cw, y + 10, cw, 18, chip, couleur, sz=10)


def equipe(prs):
    s = deck_draw.slide_par_titre(prs, T_EQUIPE)
    _vider_corps(s)
    pas = 19
    # ligne 1 : equipe produit, quatre puces sur une colonne
    y, h = 96, 116
    carte_diag(s, ZX, y, ZW, h, adj=0.08)
    _entete(s, y, 1, "Équipe produit", "SANS IA", PANEL, 90)
    puces = [
        "Un PO d'équipe dans une culture produit, en binôme avec un référent technique.",
        "Une même équipe construit (build) et exploite (run).",
        "Du temps de construction protégé.",
        "Demandes récurrentes automatisées, en self-service.",
    ]
    for k, t in enumerate(puces):
        yy = y + 37 + k * pas
        coche(s, ZX + 20.5, yy + 8, 13)
        tx(s, ZX + 32, yy, ZW - 44, 16, [[(t, 12, False, NAVY)]], A.TOP)
    forme(s, S.CHEVRON, ZX + ZW / 2 - 6.5, 211, 13, 24, CYAN, None, adj=0.35).rotation = 90
    # ligne 2 : roles augmentes
    y, h = 234, 132
    carte_diag(s, ZX, y, ZW, h, adj=0.08)
    _entete(s, y, 2, "Équipe augmentée", "AVEC IA · OPTION SELON LA MATURITÉ", NAVY, 218)
    roles = [
        ("PO augmenté" + NB + ":", " arbitrages préparés."),
        ("Référent technique augmenté" + NB + ":", " diagnostic préparé."),
        ("Exploitation augmentée" + NB + ":", " travail récurrent préparé."),
    ]
    for k, (role, reste) in enumerate(roles):
        yy = y + 37 + k * pas
        coche(s, ZX + 20.5, yy + 8, 13)
        tx(s, ZX + 32, yy, ZW - 44, 16, [[(role, 12, True, NAVY), (reste, 12, False, NAVY)]], A.TOP)
    yb = y + 98
    forme(s, S.RECTANGLE, ZX + 16, yb - 2, ZW - 32, 0.75, LINE, None)
    tx(s, ZX + 16, yb + 1, 320, 30, [[("Les agents préparent ; l'humain décide et en répond.", 11, False, SLATE)],
                                     [("Effets visés, à mesurer ; rien n'est promis.", 11, False, SLATE)]], A.MIDDLE)
    _pastille(s, ZX + ZW - 12 - 112, yb + 7, 112, 18, "RÔLES À VALIDER", PANEL, sz=10)


def _ids():
    prs = Presentation(deck_base.resoudre_base(BASE))
    return [f"id:{deck_draw.slide_par_titre(prs, T_EQUIPE).slide_id}"]


ETAPES = [{"declarer": _ids(), "f": equipe, "nouvelles_max": 0, "nom": "conviction 8 : mise en espace"}]
