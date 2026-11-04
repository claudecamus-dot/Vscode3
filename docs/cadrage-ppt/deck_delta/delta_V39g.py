"""Delta V39g (base V38) : space and grouping on Sommaire, Du pilote a l'autonomie, Deux comites.

- Sommaire : five entries rebalanced 3 + 2 (01-03 left, 04-05 right). The template teardrops
  are kept: the unused ones are masked in white (same idiom as V34a), the right column
  teardrops are copies of the layout's own shapes with their number re-set (04, 05).
- Du pilote a l'autonomie : the three cards grow to the body bottom (342 pt), text 11 -> 13 pt,
  card titles 13 -> 14 pt, pills anchored at the card bottom, note moved to 350 pt.
- Deux comites : grey panel down to 348 pt, cards to 342 pt, rows re-spaced, row text 10.5 -> 11 pt,
  note moved to 352 pt.
Same text. Chrome untouched.
Usage (from docs/cadrage-ppt/) : py deck_delta/deck.py delta_V39g --base V38 --sortie C:/tmp/deck-v39-g/V39g.pptx --sans-rendu
"""
import copy

import deck_base
import deck_draw
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.util import Pt

BASE = "V38"
NOTE = "V39g : sommaire 3+2, cartes des trois modes et panneau des deux comites jusqu'au bas du corps"
OPS = []

T_SOM = "Sommaire"
T_MODES = "Du pilote à l'autonomie : trois modes d'interaction entre OCTO et le client"
T_COM = "Deux comités en parallèle : l'un suit l'exécution, l'autre décide"
EMU = 12700


def _e(v):
    return int(round(v * EMU))


def _ids(titre):
    return [f"id:{deck_draw.slide_par_titre(Presentation(deck_base.resoudre_base(BASE)), titre).slide_id}"]


def _taille(sh, pt):
    for r in (r for p in sh.text_frame.paragraphs for r in p.runs):
        r.font.size = Pt(pt)


def _masque(s, x, y, nom):
    m = s.shapes.add_shape(1, _e(x), _e(y), _e(57), _e(57))
    m.fill.solid()
    m.fill.fore_color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    m.line.fill.background()
    m.shadow.inherit = False
    m.name = nom
    return m


def sommaire(prs):
    s = deck_draw.slide_par_titre(prs, T_SOM)
    for sh in list(s.shapes):  # previous masks (rows 2-3 of the right column) are redrawn below
        if not sh.is_placeholder and sh.width == _e(57) and sh.left == _e(373):
            sh._element.getparent().remove(sh._element)
    lay = {sh.shape_id: sh for sh in s.slide_layout.shapes}
    ph = {sh.placeholder_format.idx: sh for sh in s.placeholders}
    _masque(s, 66.5, 278.5, "Masque pastille 04 gauche")  # layout teardrop at (69.6, 281.6)
    for k, y in enumerate((106.5, 163.4, 220.3)):
        _masque(s, 373.6, y, f"Masque pastille 0{5 + k}")
    nid = max(sh.shape_id for sh in s.shapes) + 1
    for num, dy in (("04", 0.0), ("05", 56.9)):
        for src in (lay[458], lay[469]):
            el = copy.deepcopy(src._element)
            el.nvSpPr.cNvPr.set("id", str(nid))
            el.nvSpPr.cNvPr.set("name", f"Pastille {num} droite" + (" texte" if src is lay[469] else ""))
            nid += 1
            off = el.spPr.find("{http://schemas.openxmlformats.org/drawingml/2006/main}xfrm").find(
                "{http://schemas.openxmlformats.org/drawingml/2006/main}off")
            off.set("y", str(int(off.get("y")) + _e(dy)))
            if src is lay[469]:
                for t in el.iter("{http://schemas.openxmlformats.org/drawingml/2006/main}t"):
                    t.text = num
            s.shapes._spTree.append(el)
    for idx, (x, y) in ((4, (442.5, 109.1)), (5, (442.5, 165.5))):
        p = ph[idx]  # an inherited placeholder needs its full xfrm, else width/height read 0
        p.left, p.top, p.width, p.height = _e(x), _e(y), _e(230.0), _e(46.7)


def modes(prs):
    s = deck_draw.slide_par_titre(prs, T_MODES)
    bas = 342.0
    for sh in s.shapes:
        top = sh.top / EMU
        if "Diagonal" in sh.name and sh.height > _e(150):
            sh.height = _e(bas) - sh.top
        elif abs(top - 282.0) < 1:  # pills
            sh.top = _e(bas - 29)
        elif abs(top - 199.5) < 1 and sh.has_text_frame:
            sh.top, sh.height = _e(200), _e(100)
            sh.width = _e(175)
            _taille(sh, 13)
        elif abs(top - 173.8) < 1 and sh.has_text_frame:
            _taille(sh, 14)
        elif sh.name.startswith("Chevron"):
            sh.top = _e((142.3 + bas) / 2 - 11)
        elif sh.has_text_frame and sh.text_frame.text.startswith("Modes de Team"):
            sh.top = _e(350)


# old top -> (new top, new height or None) for the rows of each committee card
_ROWS = [
    (171.4, 173.0, 46.0), (171.7, 174.0, None),
    (214.7, 223.0, None),
    (219.5, 228.0, None), (220.5, 229.0, None),
    (240.1, 252.0, None),
    (245.2, 257.0, 32.0), (245.9, 258.0, None),
    (276.2, 292.0, None),
    (281.6, 297.0, 44.0), (282.0, 298.0, None),
]


def comites(prs):
    s = deck_draw.slide_par_titre(prs, T_COM)
    for sh in s.shapes:
        if sh.is_placeholder or sh.name.startswith(("nav-", "phase-")):
            continue
        top = sh.top / EMU
        if sh.name.startswith("Rounded Rectangle") and sh.width > _e(600):
            sh.height = _e(348) - sh.top
            continue
        if "Diagonal" in sh.name:
            sh.height = _e(342) - sh.top
            continue
        if sh.name.startswith("Chevron"):
            sh.top = _e((103.3 + 342) / 2 - 12)
            continue
        if sh.has_text_frame and sh.text_frame.text.startswith("Une troisième"):
            sh.top = _e(352)
            continue
        for old, new, h in _ROWS:
            if abs(top - old) < 0.2:
                sh.top = _e(new)
                if h:
                    sh.height = _e(h)
                if sh.has_text_frame and sh.left in (_e(153), _e(459)):
                    _taille(sh, 11)
                break


ETAPES = [
    {"declarer": _ids(T_SOM), "f": sommaire, "nouvelles_max": 0, "nom": "sommaire : entrees 3 + 2"},
    {"declarer": _ids(T_MODES), "f": modes, "nouvelles_max": 0, "nom": "trois modes : cartes jusqu'au bas du corps"},
    {"declarer": _ids(T_COM), "f": comites, "nouvelles_max": 0, "nom": "deux comites : panneau jusqu'au bas du corps"},
]
