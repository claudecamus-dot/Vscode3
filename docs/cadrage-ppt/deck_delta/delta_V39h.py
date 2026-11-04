"""Delta V39h (base V38) : convictions 1, 7, 8, 9 (ranks 10, 13, 14, 15) - user arbitrage « goutte réduite, pleine largeur ».

Common rule (identical in delta_V39i) : `goutte_reduite` scales the rail teardrop + its pictogram to a 56 x 56 pt box at (45, 94).
Content then uses the top band x 113 -> 659.25, y 92 -> 150 and the full width x 45 -> 659.25 below y 158.
Existing shapes are only moved / resized / re-sized in type (text, ids, colours untouched) ; one connector removed on rank 15.
Usage (from docs/cadrage-ppt/) : py deck_delta/deck.py delta_V39h --base V38 --sortie C:/tmp/deck-v39-h/V39h.pptx --sans-rendu
"""
import deck_base
import deck_draw
from forme_v9 import deplacer, par_id, supprimer
from pptx import Presentation
from pptx.util import Pt

BASE = "V38"
NOTE = "V39h : convictions 1, 7, 8, 9 - goutte reduite 56 pt, contenu pleine largeur"
OPS = []

EMU = 12700
X0, X1 = 45, 659.25
W = X1 - X0
GX, GY, GD = 45, 94, 56  # common rule : drop box


def goutte_reduite(slide):
    """Scale the rail teardrop and its pictogram to a GD x GD box at (GX, GY), keeping proportions and colours."""
    drop = next(sh for sh in slide.shapes if sh.name.startswith("Teardrop"))
    ox, oy, k = drop.left, drop.top, GD * EMU / drop.width
    x1, y1 = ox + drop.width, oy + drop.height
    for sh in list(slide.shapes):
        if sh.is_placeholder or not (ox <= sh.left <= x1 and oy <= sh.top <= y1):
            continue
        sh.left = int(GX * EMU + (sh.left - ox) * k)
        sh.top = int(GY * EMU + (sh.top - oy) * k)
        sh.width, sh.height = int(sh.width * k), int(sh.height * k)
        try:
            if sh.line.width:
                sh.line.width = int(sh.line.width * k)
        except (AttributeError, ValueError):
            pass


def _sz(sh, sz):
    for p in sh.text_frame.paragraphs:
        for r in p.runs:
            r.font.size = Pt(sz(r.font.size.pt) if callable(sz) else sz)


def _g(d, i, x=None, y=None, w=None, h=None, sz=None):
    sh = deplacer(d[i], x, y, w, h)
    if sz is not None:
        _sz(sh, sz)
    return sh


def _coche_suit(d, ti, x, y):
    """Move the 3-shape check (oval + 2 strokes, ids ti-3..ti-1) so it keeps its offset to text ti placed at (x, y)."""
    t = d[ti]
    dx, dy = x * EMU - t.left, y * EMU - t.top
    for i in (ti - 3, ti - 2, ti - 1):
        d[i].left, d[i].top = int(d[i].left + dx), int(d[i].top + dy)


# ------------------------------------------------------------------ rank 10 : conviction 1
def c1(prs):
    s = deck_draw.slide_par_titre(prs, T1)
    goutte_reduite(s)
    d = par_id(s)
    _g(d, 112, 113, 92, X1 - 113, 120)                 # navy panel, top band then down
    _g(d, 113, 123, 97, X1 - 133, 28, 21)
    _g(d, 114, 113 + (X1 - 113) / 2 - 120, 127, 240)
    _g(d, 116, 123, 133, X1 - 133, 22, 15)
    pw = (X1 - 113 - 2 * 16 - 3 * 10) / 4
    for k, (r, t) in enumerate(((148, 149), (150, 151), (152, 153), (154, 155))):
        x = 113 + 16 + k * (pw + 10)
        _g(d, r, x, 166, pw, 32)
        _g(d, t, x, 166, pw, 32, 14)
    cw = (W - 10) / 2
    for k, (card, head, fil, body) in enumerate(((107, 108, 109, 111), (117, 118, 119, 120))):
        x = X0 + k * (cw + 10)
        _g(d, card, x, 222, cw, 144)
        _g(d, head, x + 10, 229, cw - 20, 24, 16)
        _g(d, fil, x + 16, 257, cw - 32)
        _g(d, body, x + 14, 266, cw - 28, 94, 15)


# ------------------------------------------------------------------ rank 13 : conviction 7
def c7(prs):
    s = deck_draw.slide_par_titre(prs, T7)
    goutte_reduite(s)
    d = par_id(s)
    # AVANT : top band then down, at x 113
    _g(d, 149, 113, 101, X1 - 113, 77)
    _g(d, 150, 127, 92)
    _g(d, 151, 127, 92, sz=11)
    _g(d, 152, 129, 113, 220, 22, 16)
    _g(d, 153, 129, 137, 220, 32, 13)
    _g(d, 154, 360, 111, None, 58)
    _g(d, 155, 372, 107, X1 - 384, 42, 13)
    _g(d, 156, 372, 151, X1 - 384, 22, 13)
    _g(d, 165, 373.5, 174)                              # chevron
    # APRES : full width
    _g(d, 157, X0, 195, W, 81)
    _g(d, 158, 59, 186)
    _g(d, 159, 59, 186, sz=11)
    _g(d, 160, 61, 208, 270, 22, 16)
    _g(d, 161, 61, 232, 270, 34, 13)
    _g(d, 162, 345, 206, None, 60)
    _g(d, 163, 357, 205, X1 - 369, 32, 13)
    _g(d, 164, 357, 234, X1 - 369, 32, 13)
    # PRODUIT OU COMPOSANT : full width
    _g(d, 166, X0, 293, W, 73)
    _g(d, 167, 59, 284)
    _g(d, 168, 59, 284, sz=11)
    _g(d, 169, 61, 304, W - 32, 22, 14)
    _g(d, 170, 61, 333, 280, 22, 14)
    _g(d, 171, 357, 333, X1 - 369, 22, 14)


# ------------------------------------------------------------------ rank 14 : conviction 8
def c8(prs):
    s = deck_draw.slide_par_titre(prs, T8)
    goutte_reduite(s)
    d = par_id(s)
    # row 1 : equipe produit, top band then down at x 113
    x, w = 113, X1 - 113
    _g(d, 149, x, 92, w, 114)
    _g(d, 150, x + 12, 100)
    _g(d, 151, x + 12, 100, sz=13)
    _g(d, 152, x + 42, 100, 220, 22, 15)
    _g(d, 153, x + w - 12 - 90, 102)
    _g(d, 154, x + w - 12 - 90, 102, sz=10.5)
    for k, ti in enumerate((158, 162, 166, 170)):
        yy = 128 + k * 19
        _coche_suit(d, ti, x + 32, yy)
        _g(d, ti, x + 32, yy, w - 44, 18, 13)
    _g(d, 171, 373.5, 199)                              # chevron
    # row 2 : equipe augmentee, full width
    y = 216
    _g(d, 172, X0, y, W, 150)
    _g(d, 173, X0 + 12, y + 8)
    _g(d, 174, X0 + 12, y + 8, sz=13)
    _g(d, 175, X0 + 42, y + 8, 220, 22, 15)
    _g(d, 176, X1 - 12 - 218, y + 10)
    _g(d, 177, X1 - 12 - 218, y + 10, sz=10.5)
    cw = (W - 32) / 3
    for k, ti in enumerate((181, 185, 189)):
        cx = X0 + 32 + k * cw
        _coche_suit(d, ti, cx, y + 42)
        _g(d, ti, cx, y + 42, cw - 26, 40, 14)
    _g(d, 190, X0 + 16, y + 96, W - 32)
    _g(d, 191, X0 + 16, y + 101, 430, 40, 12)
    _g(d, 192, X1 - 12 - 120, y + 112, 120, 19)
    _g(d, 193, X1 - 12 - 120, y + 112, 120, 19, 10.5)


# ------------------------------------------------------------------ rank 15 : conviction 9
def c9(prs):
    s = deck_draw.slide_par_titre(prs, T9)
    goutte_reduite(s)
    d = par_id(s)
    supprimer(d[175])                                  # row1->row2 link : the two numbers are no longer aligned
    # row 1 (COMOP) : top band
    x, w = 113, X1 - 113
    _g(d, 154, x, 92, w, 58)
    _g(d, 155, x + 12, 109)
    _g(d, 156, x + 12, 109)
    _g(d, 157, x + 46, 93, w - 58, 22, lambda v: 17 if v > 13 else 12)
    _g(d, 158, x + 46, 114, w - 58, 18, 13)
    _g(d, 159, x + 46, 131, 310, 17, 12)
    _g(d, 160, x + 356, 132, w - 368, 16, 11)
    # rows 2 and 3 : full width
    for (card, num, numt, tit, dec, avec, cad), y, h in (((161, 162, 163, 164, 165, 166, 167), 160, 98),
                                                        ((168, 169, 170, 171, 172, 173, 174), 268, 98)):
        _g(d, card, X0, y, W, h)
        _g(d, num, X0 + 14, y + 14, 28, 28)
        _g(d, numt, X0 + 14, y + 14, 28, 28, 14)
        _g(d, tit, X0 + 56, y + 12, W - 70, 28, lambda v: 19 if v > 13 else 13)
        _g(d, dec, X0 + 56, y + 42, W - 70, 20, 14)
        _g(d, avec, X0 + 56, y + 63, W - 70, 18, 13)
        _g(d, cad, X0 + 56, y + 80, W - 70, 16, 11)
    _g(d, 176, X0 + 28, 202, None, 80)


T1 = "Conviction 1 : le mode produit est d'abord une culture, pas un outil"
T7 = "Conviction 7 : financer des produits et des équipes stables"
T8 = "Conviction 8 : une petite équipe produit qui construit et exploite"
T9 = "Conviction 9 : trois instances, chacune avec sa décision"


def _id(t):
    prs = Presentation(deck_base.resoudre_base(BASE))
    return [f"id:{deck_draw.slide_par_titre(prs, t).slide_id}"]


ETAPES = [
    {"declarer": _id(T1), "f": c1, "nouvelles_max": 0, "nom": "conviction 1 : goutte reduite, pleine largeur"},
    {"declarer": _id(T7), "f": c7, "nouvelles_max": 0, "nom": "conviction 7 : goutte reduite, pleine largeur"},
    {"declarer": _id(T8), "f": c8, "nouvelles_max": 0, "nom": "conviction 8 : goutte reduite, pleine largeur"},
    {"declarer": _id(T9), "f": c9, "nouvelles_max": 0, "nom": "conviction 9 : goutte reduite, pleine largeur"},
]
