"""Delta V43 s29 (base V42) : split the dense slide « Le diagnostic s'appuie sur cinq piliers » into 2 slides.
Slide A keeps the original title, chapo and the 5-pillar card (widened). Slide B (new, right after) carries the IA-pillar
question card (widened) + the 3 principles + the footnote ; its title is NEW wording derived from that card's content.
No original text is deleted : every text box lands on A or B. Usage (from docs/cadrage-ppt/) :
py deck_delta/deck.py delta_V43_s29 --base V42 --sortie C:/tmp/deck-v43-s29/V43s29.pptx --sans-rendu
"""
import deck_base
import deck_draw
from forme_v9 import par_id

BASE = "V42"
NOTE = "V43 s29 : slide 29 scindée en 2 (cinq piliers / une question du pilier IA)"
OPS = []
T = "Le diagnostic s'appuie sur cinq piliers, du mode produit à l'agentic"
T_B = "Chaque pilier se lit sur une échelle de maturité : l'exemple du pilier IA"
PT = 12700

DROITE = list(range(69, 99))          # right card + 3 principles' block ids 69..98 (pills 90-98 included)
PILULES = list(range(90, 99))
GAUCHE_CHAPO = [42, 43, 44]
CARTE_G = list(range(45, 69))


def _set(sh, x=None, y=None, w=None, h=None):
    if x is not None: sh.left = int(x * PT)
    if y is not None: sh.top = int(y * PT)
    if w is not None: sh.width = int(w * PT)
    if h is not None: sh.height = int(h * PT)


def _suppr(d, ids):
    for i in ids:
        el = d[i]._element
        el.getparent().remove(el)


def decouper(prs):
    core = deck_base.core()
    a = deck_draw.slide_par_titre(prs, T)
    b = deck_draw.ajouter_sur_gabarit(core, prs, T, {})
    ext = deck_draw._sections(prs)
    if ext is not None:
        deck_draw._placer_dans_section(ext, deck_draw.id_de(prs, a), deck_draw.id_de(prs, b))
    da = par_id(a)
    _suppr(da, DROITE)                 # A : drop right card + pills (they live on B)
    # A : widen the pillar card to the full width, 5 rows of 40 pt
    _set(da[45], 45, 125, 614, 232)
    _set(da[46], 53, 131); _set(da[47], 53, 131)
    _set(da[48], 149, 131, 400)
    for k, base in enumerate((49, 53, 57, 61, 65)):
        y = 156 + k * 39
        _set(da[base], 53, y, 598, 33)
        _set(da[base + 1], 59, y + 6.5); _set(da[base + 2], 59, y + 6.5)
        _set(da[base + 3], 90, y + 2, 555, 29)
    # B : remove chapo + left card + (keep tabs, title)
    db = par_id(b)
    _suppr(db, GAUCHE_CHAPO + CARTE_G)
    db[2].text_frame.paragraphs[0].runs[0].text = T_B
    for r in db[2].text_frame.paragraphs[0].runs[1:]:
        r.text = ""
    _set(db[69], 45, 85, 614, 215)
    _set(db[70], 53, 91); _set(db[71], 53, 91)
    _set(db[72], 149, 91, 400)
    _set(db[73], 53, 114, 598, 24)
    for k, base in enumerate((74, 78, 82, 86)):
        y = 146 + k * 38
        _set(db[base], 53, y, 598, 32)
        _set(db[base + 1], 59, y + 6); _set(db[base + 2], 59, y + 6)
        _set(db[base + 3], 90, y + 2, 555, 28)
    for i, x in zip((90, 93, 96), (45, 253, 461)):
        pass                          # pills keep their original x/y (full width already)


def _id(t):
    from pptx import Presentation
    prs = Presentation(deck_base.resoudre_base(BASE))
    return [f"id:{deck_draw.slide_par_titre(prs, t).slide_id}"]


ETAPES = [{"declarer": _id(T), "f": decouper, "nouvelles_max": 1, "nom": "29 : scission cinq piliers / question du pilier IA"}]
