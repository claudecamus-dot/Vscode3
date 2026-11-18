# Vendored 2026-11-18 from C:/Users/claude.camus/Documents/Vscode9-PocAI-Orga/scripts/deck_modeles_orga_agentique/moa_outils.py
# (trait() and pointille() copied verbatim in logic) + a minimal shim of the Vscode9 `kit` / `D` helpers they rely on
# (add_forme, ecrire, carte), rewritten on python-pptx so this project does not depend on deck_synthese_agentic.
"""Minimal Vscode9 drawing kit, in inches : D.add_forme, ecrire, carte, trait, coude, pointille."""
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt

NAVY, CYAN, SLATE, MUTED = "#0E2356", "#00D2DD", "#586586", "#6E7B9A"
WHITE = "#FFFFFF"
CYAN_CLAIR, CYAN_VOILE = "#B1F0F2", "#DAF6F9"
ML, XR = 0.6, 9.0
WU = XR - ML
TROP_LONGS = []
FONT = "Outfit"


def _rgb(h):
    h = h.lstrip("#")
    return RGBColor(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


class _D:
    """Namespace mimicking the kit's `D` module (only what the vendored code uses)."""

    FORMES_PRST = {}
    rgb = staticmethod(_rgb)

    @staticmethod
    def add_forme(sl, prst, x, y, w, h, fill=None, line=None, line_w=0.75, adj=None, rot=0, dash=None):
        shp = sl.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
        geom = shp._element.spPr.find(qn("a:prstGeom"))
        geom.set("prst", prst)
        av = geom.find(qn("a:avLst"))
        if adj:
            names = {"round2DiagRect": ("adj1", "adj2"), "round2SameRect": ("adj1", "adj2")}.get(prst)
            for k, v in enumerate(adj):
                nom = names[k] if names else ("adj" if len(adj) == 1 else f"adj{k + 1}")
                val = int(round(v * (60000 if prst in ("arc", "tear") and v > 1.5 else 100000)))
                gd = av.makeelement(qn("a:gd"), {"name": nom, "fmla": f"val {val}"})
                av.append(gd)
        if fill:
            shp.fill.solid()
            shp.fill.fore_color.rgb = _rgb(fill)
        else:
            shp.fill.background()
        if line:
            shp.line.color.rgb = _rgb(line)
            shp.line.width = Pt(line_w)
            if dash:
                shp.line._get_or_add_ln().append(shp.line._get_or_add_ln().makeelement(qn("a:prstDash"), {"val": dash}))
        else:
            shp.line.fill.background()
        if rot:
            shp.rotation = rot
        shp.shadow.inherit = False
        return shp


D = _D


def ecrire(sl, l, t, w, h, paras, size=10, color=NAVY, anchor=MSO_ANCHOR.TOP, align=PP_ALIGN.LEFT, verifier=True):
    """Paragraphs (str or (str, opts)) in a margin-free text box ; opts : size, bold, color, align."""
    if isinstance(paras, str):
        paras = [paras]
    tb = sl.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = Inches(0.03)
    for i, p in enumerate(paras):
        texte, o = (p, {}) if isinstance(p, str) else p
        para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        para.alignment = o.get("align", align)
        r = para.add_run()
        r.text = texte
        r.font.name = FONT
        r.font.size = Pt(max(8, o.get("size", size)))
        r.font.bold = bool(o.get("bold", False))
        r.font.color.rgb = _rgb(o.get("color", color))
    return tb


def carte(sl, l, t, w, h, prst="round2DiagRect", fill=WHITE, line=NAVY, line_w=0.75, adj=None, dash=None):
    """Card with navy 0.75 pt outline (Vscode9 kit.carte)."""
    if adj is None:
        adj = {"round2DiagRect": [0.12, 0], "round2SameRect": [0.12, 0], "round1Rect": [0.14], "roundRect": [0.06]}.get(prst)
    return D.add_forme(sl, prst, l, t, w, h, fill=fill, line=line, line_w=line_w, adj=adj, dash=dash)


def trait(sl, x1, y1, x2, y2, color=NAVY, w=1.25, dash=None, fleche=True, double=False):
    """Straight connector with optional triangle arrowhead. The geometry check refuses zero-size
    boxes, so an axis-aligned line gets a 1-EMU offset (invisible) instead of a visible slope."""
    e1x, e1y, e2x, e2y = Inches(x1), Inches(y1), Inches(x2), Inches(y2)
    if abs(e2x - e1x) < 1:
        e2x = e1x + 1
    if abs(e2y - e1y) < 1:
        e2y = e1y + 1
    c = sl.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, e1x, e1y, e2x, e2y)
    c.line.color.rgb = _rgb(color)
    c.line.width = Pt(w)
    ln = c.line._get_or_add_ln()
    if dash:
        ln.append(ln.makeelement(qn("a:prstDash"), {"val": dash}))
    if double:
        ln.append(ln.makeelement(qn("a:headEnd"), {"type": "triangle", "w": "med", "len": "lg"}))
    if fleche:
        ln.append(ln.makeelement(qn("a:tailEnd"), {"type": "triangle", "w": "med", "len": "lg"}))
    return c


def coude(sl, points, color=NAVY, w=1.5):
    """Orthogonal polyline through `points` [(x, y), ...]; arrowhead on the last segment only."""
    for i in range(len(points) - 1):
        (xa, ya), (xb, yb) = points[i], points[i + 1]
        trait(sl, xa, ya, xb, yb, color=color, w=w, fleche=(i == len(points) - 2))


def pointille(sl, x1, y1, x2, y2):
    """Dashed navy separator drawn as ONE line (a 0.01 in high dashed rectangle renders wavy)."""
    return trait(sl, x1, y1, x2, y2, color=NAVY, w=0.75, dash="dash", fleche=False)
