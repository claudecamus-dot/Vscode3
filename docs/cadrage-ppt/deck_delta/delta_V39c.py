"""Delta V39c (base V38) : conviction 8, fill the empty zone under the rail pictogram (user: "trop d'espace non occupé").

- Row 1 « Équipe produit » stays right of the pictogram (x=186, w=473.25), bullets 12 pt (12.5/13 force a break on bullet 1).
- Row 2 « Équipe augmentée » now spans the full body width x 45 → 659.25 under the pictogram;
  the three roles become three columns (role bold on line 1, effect on line 2, 13 pt),
  footer sentences 12 pt + « RÔLES À VALIDER » pill under a hairline.
- Same text, notes untouched. Rail pictogram, dots, filet, nav pills, title : untouched.
Usage (from docs/cadrage-ppt/) : py deck_delta/deck.py delta_V39c --base V38 --sortie C:/tmp/deck-v39-c/V39c.pptx --sans-rendu
"""
import deck_base
import deck_draw
from forme_ground import coche
from forme_v9 import BLANC, CYAN, LINE, NAVY, PANEL, SLATE, S, carre_num_cyan, carte_diag, forme, tx
from pptx import Presentation
from pptx.enum.text import MSO_ANCHOR as A
from pptx.enum.text import PP_ALIGN as P

BASE = "V38"
NOTE = "V39c : conviction 8, equipe augmentee en pleine largeur sous le pictogramme"
OPS = []

NB = "\u00a0"
T_EQUIPE = "Conviction 8 : une petite équipe produit qui construit et exploite"
X0, X1 = 45, 659.25
ZX = 186
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


def _entete(s, x, w, y, num, titre, chip, couleur, cw):
    carre_num_cyan(s, x + 12, y + 8, 22, num, sz=12)
    tx(s, x + 42, y + 8, 220, 22, [[(titre, 14, True, NAVY)]], A.MIDDLE)
    _pastille(s, x + w - 12 - cw, y + 10, cw, 18, chip, couleur, sz=10)


def equipe(prs):
    s = deck_draw.slide_par_titre(prs, T_EQUIPE)
    _vider_corps(s)
    # ligne 1 : equipe produit (a droite du pictogramme)
    zw = X1 - ZX
    y, h = 94, 122
    carte_diag(s, ZX, y, zw, h, adj=0.08)
    _entete(s, ZX, zw, y, 1, "Équipe produit", "SANS IA", PANEL, 90)
    puces = [
        "Un PO d'équipe dans une culture produit, en binôme avec un référent technique.",
        "Une même équipe construit (build) et exploite (run).",
        "Du temps de construction protégé.",
        "Demandes récurrentes automatisées, en self-service.",
    ]
    for k, t in enumerate(puces):
        yy = y + 37 + k * 20.5
        coche(s, ZX + 20.5, yy + 8.5, 13)
        tx(s, ZX + 32, yy, zw - 44, 17, [[(t, 12, False, NAVY)]], A.TOP)
    forme(s, S.CHEVRON, ZX + zw / 2 - 6.5, 212, 13, 24, CYAN, None, adj=0.35).rotation = 90
    # ligne 2 : equipe augmentee, pleine largeur sous le pictogramme
    w = X1 - X0
    y, h = 232, 134
    carte_diag(s, X0, y, w, h, adj=0.08)
    _entete(s, X0, w, y, 2, "Équipe augmentée", "AVEC IA · OPTION SELON LA MATURITÉ", NAVY, 218)
    roles = [
        ("PO augmenté" + NB + ":", "arbitrages préparés."),
        ("Référent technique augmenté" + NB + ":", "diagnostic préparé."),
        ("Exploitation augmentée" + NB + ":", "travail récurrent préparé."),
    ]
    cols = [(0, 150), (150, 232), (382, 200)]  # widths sized to the bold role (no forced break)
    for (dx, cw), (role, reste) in zip(cols, roles, strict=True):
        cx = X0 + 16 + dx
        coche(s, cx + 4.5, y + 48.5, 13)
        tx(s, cx + 16, y + 40, cw - 20, 38, [[(role, 13, True, NAVY)], [(reste, 13, False, NAVY)]], A.TOP)
    yb = y + 92
    forme(s, S.RECTANGLE, X0 + 16, yb, w - 32, 0.75, LINE, None)
    tx(s, X0 + 16, yb + 4, 420, 32, [[("Les agents préparent ; l'humain décide et en répond.", 12, False, SLATE)],
                                    [("Effets visés, à mesurer ; rien n'est promis.", 12, False, SLATE)]], A.MIDDLE)
    _pastille(s, X0 + w - 12 - 120, yb + 11, 120, 19, "RÔLES À VALIDER", PANEL, sz=10.5)


def _ids():
    prs = Presentation(deck_base.resoudre_base(BASE))
    return [f"id:{deck_draw.slide_par_titre(prs, T_EQUIPE).slide_id}"]


ETAPES = [{"declarer": _ids(), "f": equipe, "nouvelles_max": 0, "nom": "conviction 8 : equipe augmentee pleine largeur"}]
