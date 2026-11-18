# Vendored 2026-11-18 from C:/Users/claude.camus/Documents/Vscode9-PocAI-Orga/scripts/deck_accompagnement_agile/pictos.py (Vscode9 techniques validated 2026-11-17).
# Imports rewritten onto this project (vendor_v9.moa_outils shim; no kit / deck_synthese_agentic dependency).
"""Official OCTO pictograms (taken from the reference deck « Slides préformatées OCTO », slides 21 and 90-112).

picto(sl, kind, cx, cy, d) is centred on (cx, cy). From d >= 0.45 in the picto sits in a thin navy ring
(the « picto cerclé » of reference slides 110-111); below, the bare picto is placed at size d.
Files: ./pictos_octo/<kind>.png. Kinds: board (tools), doc, chart, link, inbox, clock (calendar), team, target,
check, alert, ia, route, gears, compass, shield, puzzle, cycle, chrono, diagnostic, ecrire, choix, valeur,
medal, checklist, box.
"""
import os

from PIL import Image
from pptx.util import Inches

from vendor_v9 import moa_outils as O
from vendor_v9.moa_outils import NAVY, WHITE

D = O.D
DOSSIER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pictos_octo")
_RATIO = {}


def _ratio(kind):
    if kind not in _RATIO:
        chemin = os.path.join(DOSSIER, kind + ".png")
        if not os.path.isfile(chemin):
            raise FileNotFoundError(f"picto inconnu : {kind!r} ({chemin})")
        with Image.open(chemin) as im:
            _RATIO[kind] = im.size[0] / im.size[1]
    return _RATIO[kind]


def picto(sl, kind, cx, cy, d=0.7, cercle=None):
    """Official picto `kind` centred on (cx, cy); ringed when d >= 0.45 (or when cercle=True)."""
    cercle = d >= 0.45 if cercle is None else cercle
    if cercle:
        D.add_forme(sl, "ellipse", cx - d / 2, cy - d / 2, d, d, fill=WHITE, line=NAVY, line_w=0.75)
    cote = d * 0.62 if cercle else d
    r = _ratio(kind)
    w, h = (cote, cote / r) if r >= 1 else (cote * r, cote)
    return sl.shapes.add_picture(os.path.join(DOSSIER, kind + ".png"), Inches(cx - w / 2), Inches(cy - h / 2),
                                 Inches(w), Inches(h))
