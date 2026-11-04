"""Delta V39f (base V38) : Demarche detaillee slides with ILLUSTRATION panels re-spaced (user request V39).

- Mission pilote : right ILLUSTRATION panel stretched to the left column bottom (y 84.6 -> 362),
  the floating grey note moved inside the panel as its subtitle, 4 steps re-spaced ; left card 3 to 362.
- Livrables 1/2 : priorisation matrix picture enlarged to the panel (206 -> 255 pt wide), panel to 356.
- IA gouvernee : RACI row + autonomy row grouped in one grey panel (y 280 -> 364) ; RACI cards re-fitted.
Same text, phase chips and ILLUSTRATION pill style untouched. Shapes are moved, never re-written.
Usage (from docs/cadrage-ppt/) : py deck_delta/deck.py delta_V39f --base V38 --sortie C:/tmp/deck-v39-f/V39f.pptx --sans-rendu
"""
import deck_base
import deck_draw
from forme_v9 import BLANC, PANEL, S, forme
from pptx import Presentation

BASE = "V38"
NOTE = "V39f : mission pilote, livrables 1/2, IA gouvernee - espace occupe, groupes delimites"
OPS = []

T_MISSION = "De la douleur au produit : une mission pilote de bout en bout"
T_LIVR = "Exemples de livrables (1/2) : comprendre et décider"
T_IA = "L'IA est gouvernée : données, droits, validations et traçabilité"
EMU = 12700


def _par_id(s):
    return {sh.shape_id: sh for sh in s.shapes}


def _pos(sh, x=None, y=None, w=None, h=None):
    if x is not None:
        sh.left = int(x * EMU)
    if y is not None:
        sh.top = int(y * EMU)
    if w is not None:
        sh.width = int(w * EMU)
    if h is not None:
        sh.height = int(h * EMU)


def mission(prs):
    s = deck_draw.slide_par_titre(prs, T_MISSION)
    d = _par_id(s)
    bas = 362
    # left column : card 3 down to the common bottom
    _pos(d[55], h=bas - 272.3)
    # right panel : from the scenario pill top to the common bottom
    _pos(d[65], y=84.6, h=bas - 84.6)
    _pos(d[66], y=92)
    _pos(d[67], y=92)
    _pos(d[68], y=92)
    _pos(d[44], x=405, y=113, w=246, h=28)  # note becomes the panel subtitle
    d[65]._element.addnext(d[44]._element)  # in front of the panel
    pas, y0 = 52, 158
    for k, (carre, num, tit, sous) in enumerate([(70, 71, 72, 73), (74, 75, 76, 77), (78, 79, 80, 81), (82, 83, 84, 85)]):
        y = y0 + k * pas
        _pos(d[carre], y=y + 2)
        _pos(d[num], y=y + 2)
        _pos(d[tit], y=y)
        _pos(d[sous], y=y + 15)
    _pos(d[69], y=y0 + 24, h=3 * pas - 22)


def livrables(prs):
    s = deck_draw.slide_par_titre(prs, T_LIVR)
    d = _par_id(s)
    _pos(d[92], h=354.7 - 80 + 1.3)  # panel bottom aligned on card 4 bottom (356)
    img = d[96]
    w, h = 255.0, 255.0 * img.height / img.width
    _pos(img, x=369 + (290 - w) / 2, y=108 + (356 - 108 - h) / 2, w=w, h=h)


def ia(prs):
    s = deck_draw.slide_par_titre(prs, T_IA)
    d = _par_id(s)
    y0, y1 = 280, 364
    panel = forme(s, S.ROUNDED_RECTANGLE, 45, y0, 614, y1 - y0, PANEL, None, adj=0.08)
    d[101]._element.addprevious(panel._element)  # behind the RACI / autonomy rows
    # RACI row
    _pos(d[101], x=53, y=y0 + 6, w=182, h=46)
    xs, cw, g = 245, 97, 6.67
    for k, (carte, lib, pil, ptx) in enumerate([(102, 103, 104, 105), (106, 107, 108, 109), (110, 111, 112, 113), (114, 115, 116, 117)]):
        x = xs + k * (cw + g)
        _pos(d[carte], x=x, y=y0 + 6, w=cw, h=48)
        _pos(d[lib], x=x + 5, y=y0 + 8, w=cw - 10)
        _pos(d[pil], x=x + (cw - 61) / 2, y=y0 + 36)
        _pos(d[ptx], x=x + (cw - 61) / 2, y=y0 + 36)
    # autonomy row
    ya = y0 + 62
    _pos(d[118], x=53, y=ya)
    pw, cg = 108.5, 12
    for k, (pil, ptx) in enumerate([(119, 120), (122, 123), (125, 126), (128, 129)]):
        x = 180 + k * (pw + cg)
        _pos(d[pil], x=x, y=ya, w=pw)
        if d[pil].fill.fore_color.rgb == PANEL:  # grey pill on the grey panel -> white
            d[pil].fill.fore_color.rgb = BLANC
        _pos(d[ptx], x=x + 3, y=ya, w=pw - 6)
    for k, ch in enumerate((121, 124, 127)):
        _pos(d[ch], x=180 + (k + 1) * (pw + cg) - cg + 3, y=ya + 4)


def _ids(titre):
    prs = Presentation(deck_base.resoudre_base(BASE))
    return [f"id:{deck_draw.slide_par_titre(prs, titre).slide_id}"]


ETAPES = [
    {"declarer": _ids(T_MISSION), "f": mission, "nouvelles_max": 0, "nom": "mission pilote : panneau etire"},
    {"declarer": _ids(T_LIVR), "f": livrables, "nouvelles_max": 0, "nom": "livrables 1/2 : matrice agrandie"},
    {"declarer": _ids(T_IA), "f": ia, "nouvelles_max": 0, "nom": "IA gouvernee : RACI et autonomie groupes"},
]
