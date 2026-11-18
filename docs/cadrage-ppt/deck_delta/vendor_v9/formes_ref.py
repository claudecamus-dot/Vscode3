# Vendored 2026-11-18 from C:/Users/claude.camus/Documents/Vscode9-PocAI-Orga/scripts/deck_accompagnement_agile/formes_ref.py (Vscode9 techniques validated 2026-11-17).
# Imports rewritten onto this project (vendor_v9.moa_outils shim; no kit / deck_synthese_agentic dependency).
"""Slide forms rebuilt from the reference deck « Slides préformatées OCTO » (geometry measured on its slides).

- serpentin   : « Notre proposition de démarche » (ref. slide 93) : two lines joined by an arc, numbered stations,
                small milestone circles with labels, and a rounded banner fed by the end of the path.
- grille      : « Activités / Livrables » grid by step (ref. slides 84-86) : navy side tab with turned labels.
- rangee      : row of ringed pictos with title and text (ref. slides 110-111).
- onglet      : picto tab + panel (ref. slides 98-101), in a short (row) and a tall (column) variant.
All lines are 0.75 pt navy, fills white, as in the reference.
"""
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn

from vendor_v9 import moa_outils as O
from vendor_v9.moa_outils import CYAN, ML, MSO_ANCHOR, NAVY, PP_ALIGN, SLATE, WHITE
from vendor_v9.pictos import picto

D = O.D
D.FORMES_PRST.setdefault("arc", MSO_SHAPE.ARC)
LW = 0.75


def _ligne(sl, x1, y1, x2, y2):
    return O.trait(sl, x1, y1, x2, y2, color=NAVY, w=LW, fleche=False)


def _centre(sl, x, y, w, h, texte, size=9, bold=False, color=NAVY):
    return O.ecrire(sl, x, y, w, h, [(texte, dict(size=size, bold=bold, color=color, align=PP_ALIGN.CENTER))],
                    anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)


# ------------------------------------------------------------------ serpentin (ref. 93)
def _station(sl, x, y, num, label, w):
    """Numbered station centred on the line: number tab (rounded left) + label (rounded right), 0.4 in high."""
    h, wn = 0.4, 0.42
    D.add_forme(sl, "round2SameRect", x + wn / 2 - h / 2, y - wn / 2, h, wn, fill=WHITE, line=NAVY, line_w=LW, adj=[0.5, 0], rot=270)
    wl = w - wn
    D.add_forme(sl, "round2SameRect", x + wn + wl / 2 - h / 2, y - wl / 2, h, wl, fill=WHITE, line=NAVY, line_w=LW, adj=[0.5, 0], rot=90)
    _centre(sl, x, y - h / 2, wn, h, num, size=10, bold=True)
    _centre(sl, x + wn, y - h / 2, wl - 0.08, h, label, size=10, bold=True)


def _jalon(sl, cx, y, texte, haut, fort):
    d = 0.26
    D.add_forme(sl, "ellipse", cx - d / 2, y - d / 2, d, d, fill=CYAN if fort else WHITE, line=NAVY, line_w=LW)
    if haut:
        _ligne(sl, cx, y - 0.3, cx, y - d / 2)
        _centre(sl, cx - 0.47, y - 0.66, 0.94, 0.36, texte, bold=fort)
    else:
        _ligne(sl, cx, y + d / 2, cx, y + 0.3)
        _centre(sl, cx - 0.47, y + 0.3, 0.94, 0.36, texte, bold=fort)


def serpentin(sl, phases, bandeau, y1=1.98):
    """phases = 5 x (label, [activités]) ; an activity starting with « * » is a key milestone (cyan, bold).
    Phases 1-3 run left to right on the first line, phases 4-5 right to left on the second one.
    bandeau = (kind, label, [items]) : the banner the path ends in."""
    x0, xr, dia = 0.62, 8.3, 1.5
    y2 = y1 + dia
    pas, sw, ecart = 0.5, 1.45, 0.3
    _ligne(sl, 0.9, y1, xr, y1)
    _ligne(sl, x0 + dia / 2, y2, xr, y2)
    D.add_forme(sl, "arc", xr - dia / 2, y1, dia, dia, fill=None, line=NAVY, line_w=LW, adj=[162.0, 54.0])
    D.add_forme(sl, "arc", x0, y2, dia, dia, fill=None, line=NAVY, line_w=LW, adj=[0.0, 54.0], rot=180)
    yb = y2 + dia / 2 + 0.12
    _ligne(sl, x0, y2 + dia / 2, x0, yb)
    # first line, left to right
    haut = lambda k: k % 2 == 1  # noqa: E731  (labels alternate below / above the line)
    blocs = [sw + ecart + (len(a) - 1) * pas for _l, a in phases[:3]]
    libre = (xr - 0.2 - 0.95 - sum(blocs)) / 2
    x = 0.95
    for i, (label, acts) in enumerate(phases[:3]):
        _station(sl, x, y1, f"{i + 1:02d}", label, sw)
        for k, a in enumerate(acts):
            _jalon(sl, x + sw + ecart + k * pas, y1, a.lstrip("*"), haut(k), a.startswith("*"))
        x += blocs[i] + libre
    # second line, right to left
    blocs = [sw + ecart + (len(a) - 1) * pas for _l, a in phases[3:]]
    libre = (xr - 0.1 - (x0 + dia / 2 + 0.1) - sum(blocs)) / max(1, len(blocs) - 1)
    xd = xr - 0.1
    for i, (label, acts) in enumerate(phases[3:]):
        _station(sl, xd - sw, y2, f"{i + 4:02d}", label, sw)
        for k, a in enumerate(acts):
            _jalon(sl, xd - sw - ecart - k * pas, y2, a.lstrip("*"), haut(k), a.startswith("*"))
        xd -= blocs[i] + libre
    # banner
    kind, label, items = bandeau
    hb = 5.26 - yb
    O.carte(sl, x0 + 0.14, yb, 8.41, hb, prst="roundRect", fill=WHITE, line=NAVY, adj=[0.117])
    picto(sl, kind, x0 + 0.66, yb + hb / 2, 0.62)
    O.ecrire(sl, x0 + 1.1, yb, 1.45, hb, [(label, dict(bold=True, size=10))], anchor=MSO_ANCHOR.MIDDLE)
    moitie = (len(items) + 1) // 2
    for c, col in enumerate((items[:moitie], items[moitie:])):
        O.ecrire(sl, x0 + 2.8 + c * 2.85, yb + 0.04, 2.75, hb - 0.08, [(t, dict(bullet=True, after=1)) for t in col],
                 size=9, anchor=MSO_ANCHOR.MIDDLE)


# ------------------------------------------------------------------ grille Activités / Livrables (ref. 86)
def _texte_tourne(sl, cx, cy, long, texte):
    tb = O.ecrire(sl, cx - long / 2, cy - 0.16, long, 0.32, [(texte, dict(size=10.5, bold=True, color=WHITE, align=PP_ALIGN.CENTER))],
                  anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER, verifier=False)
    tb._element.spPr.find(qn("a:xfrm")).set("rot", "16200000")


def grille(sl, colonnes, rangs=("Activités", "Livrables"), y=1.42, bas=5.1):
    """colonnes = [(kind, titre, [activités], [livrables])] ; navy side tab with the two turned row labels."""
    haut = len(colonnes) > 5
    xt, wt, ht = 0.62, 0.34, 0.74 if haut else 0.36
    x0 = xt + wt
    w = 9.0 - x0
    cw = w / len(colonnes)
    yc = y + ht
    hr = (bas - yc) / 2
    hh = bas - yc
    # left-rounded tab without rotation (the geometry check measures the unrotated frame): pill + square right half
    D.add_forme(sl, "roundRect", xt, yc, wt, hh, fill=NAVY, line=NAVY, line_w=LW, adj=[0.5])
    D.add_forme(sl, "rect", xt + wt / 2, yc, wt / 2, hh, fill=NAVY, line=NAVY, line_w=LW)
    for r, lab in enumerate(rangs):
        _texte_tourne(sl, xt + wt / 2, yc + hr * (r + 0.5), hr - 0.2, lab)
    O.trait(sl, xt, yc + hr, xt + wt, yc + hr, color=WHITE, w=LW, fleche=False)
    # the headers sit on the panel's top edge, so the rounded corner goes to the bottom right (flipV), not under a header
    panneau = D.add_forme(sl, "round1Rect", x0, yc, w, hh, fill=WHITE, line=NAVY, line_w=LW, adj=[min(0.5, 0.3 / hh)])
    panneau._element.spPr.get_or_add_xfrm().set("flipV", "1")
    _ligne(sl, x0, yc + hr, x0 + w, yc + hr)
    for i, (kind, titre, acts, livs) in enumerate(colonnes):
        x = x0 + i * cw
        if i:
            _ligne(sl, x, yc, x, bas)
        D.add_forme(sl, "round2SameRect", x, y, cw, ht, fill=WHITE, line=NAVY, line_w=LW, adj=[0.4, 0])
        if haut:
            picto(sl, kind, x + cw / 2, y + 0.2, 0.26)
            _centre(sl, x + 0.04, y + 0.36, cw - 0.08, 0.36, titre, size=9.5, bold=True)
        else:
            picto(sl, kind, x + 0.24, y + ht / 2, 0.28)
            O.ecrire(sl, x + 0.44, y, cw - 0.5, ht, [(titre, dict(bold=True, size=10))], anchor=MSO_ANCHOR.MIDDLE)
        for r, items in enumerate((acts, livs)):
            O.ecrire(sl, x + 0.08, yc + r * hr + 0.08, cw - 0.14, hr - 0.14, [(t, dict(bullet=True, after=3)) for t in items],
                     size=9)


# ------------------------------------------------------------------ rangée de pictos cerclés (ref. 110)
def rangee(sl, items, y=1.5, d=1.2):
    """items = [(kind, titre, texte)] : ringed picto with a small cyan dot, bold title, text."""
    n = len(items)
    cw = O.WU / n
    for i, (kind, titre, texte) in enumerate(items):
        cx = ML + cw * (i + 0.5)
        picto(sl, kind, cx, y + d / 2, d)
        D.add_forme(sl, "ellipse", cx + d * 0.3, y + d * 0.02, 0.17, 0.17, fill=CYAN, line=NAVY, line_w=LW)
        _centre(sl, cx - cw / 2 + 0.05, y + d + 0.14, cw - 0.1, 0.3, titre, size=11, bold=True)
        O.ecrire(sl, cx - cw / 2 + 0.08, y + d + 0.5, cw - 0.16, 1.1, [(texte, dict(size=10, align=PP_ALIGN.CENTER))],
                 align=PP_ALIGN.CENTER)


# ------------------------------------------------------------------ onglet picto + panneau (ref. 98-101)
def onglet(sl, x, y, w, h, kind, label, paras, wid=1.9, size=9.5):
    """Short row: tab (picto on the left, label on the right, outer corners rounded) + panel."""
    D.add_forme(sl, "round1Rect", x + wid / 2, y, w - wid / 2, h, fill=WHITE, line=NAVY, line_w=LW, adj=[min(0.5, 0.26 / h)])
    D.add_forme(sl, "round2SameRect", x + wid / 2 - h / 2, y + h / 2 - wid / 2, h, wid, fill=WHITE, line=NAVY, line_w=LW,
                adj=[0.5, 0], rot=270)
    picto(sl, kind, x + 0.48, y + h / 2, 0.58)
    O.ecrire(sl, x + 0.84, y, wid - 0.9, h, [(label, dict(bold=True, size=10))], anchor=MSO_ANCHOR.MIDDLE)
    O.ecrire(sl, x + wid + 0.14, y + 0.05, w - wid - 0.4, h - 0.1, paras, size=size, anchor=MSO_ANCHOR.MIDDLE)


def onglet_haut(sl, x, y, w, h, kind, label, paras, wid=1.2, size=11):
    """Tall column: tab with the picto above its label + panel (reference proportions)."""
    D.add_forme(sl, "round1Rect", x + wid / 2, y, w - wid / 2, h, fill=WHITE, line=NAVY, line_w=LW, adj=[min(0.5, 0.45 / min(h, w))])
    D.add_forme(sl, "round2SameRect", x + wid / 2 - h / 2, y + h / 2 - wid / 2, h, wid, fill=WHITE, line=NAVY, line_w=LW,
                adj=[0.5, 0], rot=270)
    picto(sl, kind, x + wid / 2, y + 0.62, 0.72)
    _centre(sl, x + 0.06, y + 1.08, wid - 0.12, 0.4, label, size=10.5, bold=True)
    O.ecrire(sl, x + wid + 0.16, y + 0.12, w - wid - 0.4, h - 0.24, paras, size=size, anchor=MSO_ANCHOR.MIDDLE)


# ------------------------------------------------------------------ trajectoire (ref. 70-73)
D.FORMES_PRST.setdefault("rightArrow", MSO_SHAPE.RIGHT_ARROW)


def _flipH(shp):
    shp._element.spPr.get_or_add_xfrm().set("flipH", "1")
    return shp


def _goutte(sl, x, y, d, num, miroir):
    """Numbered teardrop whose point touches the path (below right, or above right when mirrored)."""
    shp = D.add_forme(sl, "tear", x, y, d, d, fill=WHITE, line=NAVY, line_w=LW, adj=[1.0], rot=90)
    if miroir:
        _flipH(shp)
    _centre(sl, x, y, d, d, num, size=9, bold=True)


def trajectoire(sl, etapes, cible, onglets, bas=5.2):
    """etapes = 3 to 5 labels along an interlocking path that ends in a cyan dot and an arrow holding `cible`;
    onglets = [(kind, titre, [puces])] : the tabbed panel under the path (teardrop picto on each tab)."""
    n = len(etapes)
    x0, xe, yl, hl, dg = 0.91, 6.56, 1.85, 0.26, 0.33
    p = (xe - x0) / (n + 0.53)
    for k, lab in enumerate(etapes):
        xs = x0 + k * p
        seg = D.add_forme(sl, "round2DiagRect", xs, yl, min(2.06 * p, xe - xs), hl, fill=WHITE, line=NAVY, line_w=LW,
                          adj=[0, 0.5], rot=180 if k % 2 else 0)
        if k % 2:
            _flipH(seg)
            _ligne(sl, xs, yl + hl, xs, yl + hl + 0.12)
            _goutte(sl, xs - dg, yl + hl + 0.1, dg, f"{k + 1}", True)
            yt = yl + hl + 0.1
        else:
            _ligne(sl, xs, yl - 0.1, xs, yl)
            _goutte(sl, xs - dg, yl - 0.1 - dg, dg, f"{k + 1}", False)
            yt = yl - 0.1 - dg
        O.ecrire(sl, xs + 0.08, yt - 0.02, 2 * p - 0.5, dg + 0.04, [(lab, dict(bold=True, size=10))], anchor=MSO_ANCHOR.MIDDLE)
    D.add_forme(sl, "ellipse", xe + 0.12, yl, hl, hl, fill=CYAN, line=None)
    D.add_forme(sl, "rightArrow", 7.07, yl + hl / 2 - 0.56, 1.93, 1.12, fill=WHITE, line=NAVY, line_w=LW)
    _centre(sl, 7.12, yl + hl / 2 - 0.26, 1.3, 0.52, cible, size=9.5, bold=True)
    # tabbed panel
    xp, w, yt, ht = ML, O.WU, 3.1, 0.28
    yp = yt + ht
    hp = bas - yp
    cw = w / len(onglets)
    _flipH(D.add_forme(sl, "round2DiagRect", xp, yp, w, hp, fill=WHITE, line=NAVY, line_w=LW, adj=[min(0.5, 0.5 / hp), 0]))
    for i, (kind, titre, puces) in enumerate(onglets):
        x = xp + i * cw
        dernier = i == len(onglets) - 1
        wt = cw - 0.3 if dernier else cw
        D.add_forme(sl, "round2SameRect", x, yt, wt, ht, fill=WHITE, line=NAVY, line_w=LW, adj=[0.5, 0])
        D.add_forme(sl, "tear", x, yt - 0.3, 0.58, 0.58, fill=WHITE, line=NAVY, line_w=LW, adj=[1.0], rot=180)
        picto(sl, kind, x + 0.29, yt - 0.01, 0.32, cercle=False)
        O.ecrire(sl, x + 0.62, yt, wt - 0.66, ht, [(titre, dict(bold=True, size=9.5))], anchor=MSO_ANCHOR.MIDDLE)
        if i:
            _ligne(sl, x, yp, x, yp + hp)
        O.ecrire(sl, x + 0.1, yp + 0.1, cw - (0.34 if dernier else 0.18), hp - 0.2, [(t, dict(bullet=True, after=3)) for t in puces],
                 size=9)


# ------------------------------------------------------------------ piliers à pictos (ref. 94)
def piliers(sl, colonnes, bande, y=1.38, bas=5.2):
    """colonnes = [(kind, titre, [paras])] : ringed picto, connector, rounded header, body with one rounded corner;
    bande = (phrase, [libellés]) : bottom band holding light-cyan bars."""
    n = len(colonnes)
    ecart, d, hh = 0.13, 0.66, 0.42
    cw = (O.WU - ecart * (n - 1)) / n
    yh = y + d + 0.14
    hb = 0.95 if bande else 0
    yb = bas - hb
    hc = yb - 0.12 - (yh + hh) if bande else bas - (yh + hh)
    for i, (kind, titre, paras) in enumerate(colonnes):
        x = ML + i * (cw + ecart)
        _ligne(sl, x + cw / 2, y + d, x + cw / 2, yh)
        picto(sl, kind, x + cw / 2, y + d / 2, d)
        D.add_forme(sl, "round1Rect", x, yh + hh, cw, hc, fill=WHITE, line=NAVY, line_w=LW, adj=[min(0.5, 0.16 / min(cw, hc))], rot=180)
        D.add_forme(sl, "round2SameRect", x, yh, cw, hh, fill=WHITE, line=NAVY, line_w=LW, adj=[0.34, 0])
        _centre(sl, x + 0.1, yh, cw - 0.2, hh, titre, size=10.5, bold=True)
        O.ecrire(sl, x + 0.14, yh + hh + 0.1, cw - 0.28, hc - 0.2, paras, size=10)
    if bande:
        phrase, libelles = bande
        D.add_forme(sl, "round2DiagRect", ML, yb, O.WU, hb, fill=WHITE, line=NAVY, line_w=LW, adj=[0.244, 0])
        O.ecrire(sl, ML + 0.14, yb + 0.06, O.WU - 0.5, 0.38, [phrase], size=10, anchor=MSO_ANCHOR.MIDDLE)
        wl = (O.WU - 0.3 - 0.08 * (len(libelles) - 1)) / len(libelles)
        for k, lab in enumerate(libelles):
            xl = ML + 0.15 + k * (wl + 0.08)
            D.add_forme(sl, "roundRect", xl, yb + 0.52, wl, 0.3, fill="#72DFE7", line=NAVY, line_w=LW, adj=[0.1667])
            _centre(sl, xl + 0.05, yb + 0.52, wl - 0.1, 0.3, lab, size=9, bold=True)


# ------------------------------------------------------------------ bandeau navy de conclusion (ref. 65)
def conclusion(sl, y, h, paras, x=ML, w=None):
    """Navy rounded band with white text: the take-away of the slide."""
    w = O.WU if w is None else w
    D.add_forme(sl, "roundRect", x, y, w, h, fill=NAVY, line=NAVY, line_w=LW, adj=[0.1667])
    O.ecrire(sl, x + 0.2, y + 0.06, w - 0.4, h - 0.12, [(t, dict(color=WHITE, **o)) for t, o in paras], size=10,
             anchor=MSO_ANCHOR.MIDDLE)


# ------------------------------------------------------------------ trois panneaux emboîtés (ref. 53)
def trefle(sl, intro, panneaux, y=1.3, note=None):
    """intro = (accroche, texte) on the top left; panneaux = 3 x (kind, titre, [paras]) : top right, bottom left,
    bottom right. The bottom-left panel's picto sits on its top-right corner, at the junction (as in the reference)."""
    xs, ym = 5.0, y + 1.85
    O.ecrire(sl, ML, y + 0.05, 4.2, 0.4, [(intro[0], dict(bold=True, size=13))])
    O.ecrire(sl, ML, y + 0.5, 3.6, 1.0, [intro[1]], size=10)
    if note:
        O.ecrire(sl, ML, ym - 0.62, 3.2, 0.48, [(note, dict(size=8, color=SLATE))])
    boites = [(xs, y, O.XR - xs, ym - y, [0.27, 0], 180), (ML, ym, xs - ML, 1.7, [0.244, 0], 0),
              (xs, ym, 3.5, 1.92, [0, 0.293], 0)]
    for i, ((x, yy, w, h, adj, rot), (kind, titre, paras)) in enumerate(zip(boites, panneaux, strict=True)):
        D.add_forme(sl, "round2DiagRect", x, yy, w, h, fill=WHITE, line=NAVY, line_w=LW, adj=adj, rot=rot)
        wt = w - (0.4 if i == 1 else 1.3)
        O.ecrire(sl, x + 0.2, yy + 0.1, wt, 0.4, [(titre, dict(bold=True, size=12))], anchor=MSO_ANCHOR.MIDDLE)
        O.ecrire(sl, x + 0.2, yy + 0.55, wt, h - 0.65, [(t, dict(bullet=True, after=3)) for t in paras], size=9.5)
        if i == 1:
            picto(sl, kind, xs - 0.62, ym - 0.42, 0.75)
        else:
            picto(sl, kind, x + w - 0.62, yy + 0.62, 0.75)


# ------------------------------------------------------------------ mosaïque (ref. 54)
def mosaique(sl, accroche, droite, milieu, bas, y=1.2):
    """accroche : bold statement on the top left; droite = [paras] in the tall right panel;
    milieu = (kind, titre, texte) : picto panel under the statement; bas = [paras] in the wide bottom panel."""
    xr, ym, yb, hb = 5.6, 2.54, 3.64, 1.55
    O.ecrire(sl, ML, y, 4.85, ym - y - 0.1, [(accroche, dict(bold=True, size=15))], anchor=MSO_ANCHOR.MIDDLE)
    D.add_forme(sl, "round2DiagRect", xr, y, O.XR - xr, yb - y, fill=WHITE, line=NAVY, line_w=LW, adj=[0.13, 0])
    O.ecrire(sl, xr + 0.2, y + 0.15, O.XR - xr - 0.4, yb - y - 0.3, droite, size=9.5)
    D.add_forme(sl, "round2DiagRect", ML, ym, xr - ML, yb - ym, fill=WHITE, line=NAVY, line_w=LW, adj=[0, 0.216])
    kind, titre, texte = milieu
    picto(sl, kind, ML + 0.45, (ym + yb) / 2, 0.62)
    O.ecrire(sl, ML + 0.9, ym + 0.08, xr - ML - 1.05, yb - ym - 0.16, [(titre, dict(bold=True, after=2)), texte], size=9.5,
             anchor=MSO_ANCHOR.MIDDLE)
    D.add_forme(sl, "round2DiagRect", ML, yb, 7.9, hb, fill=WHITE, line=NAVY, line_w=LW, adj=[0.167, 0])
    O.ecrire(sl, ML + 0.3, yb + 0.12, 7.3, hb - 0.24, bas, size=9.5, anchor=MSO_ANCHOR.MIDDLE)


# ------------------------------------------------------------------ pilule et grande feuille (ref. 55)
def feuille(sl, pilule, puces, message, kind="check", y=1.2, bas=5.15):
    """pilule : heading in a pill rounded on the left, closed by a picto tab; puces : the list under it;
    message : the strong statement in the tall leaf on the right."""
    X, W, H = ML, 5.45, 0.8
    # pill rounded on the left: its right end runs under the picto tab (a rotated shape fails the frame check)
    D.add_forme(sl, "roundRect", X, y, W + 0.6, H, fill=WHITE, line=NAVY, line_w=LW, adj=[0.5])
    D.add_forme(sl, "round1Rect", X + W, y, 1.4, H, fill=WHITE, line=NAVY, line_w=LW, adj=[0.355])
    picto(sl, kind, X + W + 0.55, y + H / 2, 0.6)
    O.ecrire(sl, X + 0.35, y, W - 0.5, H, [(pilule, dict(bold=True, size=13))], anchor=MSO_ANCHOR.MIDDLE)
    O.ecrire(sl, X + 0.2, y + H + 0.2, W - 0.35, bas - y - H - 0.3, [(t, dict(bullet=True, after=9)) for t in puces], size=11)
    xl, yl = X + W, y + H + 0.02
    _flipH(D.add_forme(sl, "round2DiagRect", xl, yl, O.XR - xl, bas - yl, fill=WHITE, line=NAVY, line_w=LW, adj=[0.339, 0]))
    O.ecrire(sl, xl + 0.25, yl + 0.3, O.XR - xl - 0.5, bas - yl - 0.6, [(message, dict(bold=True, size=13))],
             anchor=MSO_ANCHOR.MIDDLE)


# ------------------------------------------------------------------ grille navy et feuille haute (ref. 63)
def grille_navy(sl, entete, texte, kind, blocs, droite, y=1.2, bas=5.15):
    """entete + texte in a leaf whose bottom holds a 2 x 2 navy grid (blocs = 4 x (titre, texte)), a picto tab
    on the leaf's top right; droite = (titre, [puces]) in the tall leaf on the right."""
    xl, wl, ht = ML, 5.0, 0.9
    xr = xl + wl + 0.1
    D.add_forme(sl, "round2DiagRect", xl + wl - 1.15, y, 1.15, ht, fill=WHITE, line=NAVY, line_w=LW, adj=[0, 0.256])
    picto(sl, kind, xl + wl - 0.575, y + ht / 2 + 0.03, 0.62)
    O.ecrire(sl, xl, y, wl - 1.3, ht, [(entete, dict(bold=True, size=13))], anchor=MSO_ANCHOR.BOTTOM)
    yl = y + ht
    D.add_forme(sl, "round2DiagRect", xl, yl, wl, bas - yl, fill=WHITE, line=NAVY, line_w=LW, adj=[0.18, 0])
    O.ecrire(sl, xl + 0.35, yl + 0.22, wl - 0.6, 0.6, [texte], size=10.5)
    bw, bh, g = (wl - 0.42) / 2, 1.0, 0.02
    gy = bas - 0.2 - 2 * bh - g
    for k, (t, tx) in enumerate(blocs):
        bx, by = xl + 0.2 + (k % 2) * (bw + g), gy + (k // 2) * (bh + g)
        shp = D.add_forme(sl, "round2DiagRect", bx, by, bw, bh, fill=NAVY, line=WHITE, line_w=LW, adj=[0, 0.35])
        if k in (1, 2):
            _flipH(shp)
        O.ecrire(sl, bx + 0.15, by + 0.04, bw - 0.3, bh - 0.08, [(t, dict(bold=True, size=9.5, color=WHITE, after=1)),
                                                                (tx, dict(size=8.5, color=WHITE))], anchor=MSO_ANCHOR.MIDDLE)
    titre, puces = droite
    D.add_forme(sl, "round2DiagRect", xr, y, O.XR - xr, bas - y, fill=WHITE, line=NAVY, line_w=LW, adj=[0, 0.145])
    O.ecrire(sl, xr + 0.2, y + 0.2, O.XR - xr - 0.4, 0.5, [(titre, dict(bold=True, size=12))], anchor=MSO_ANCHOR.MIDDLE)
    O.ecrire(sl, xr + 0.2, y + 0.8, O.XR - xr - 0.4, bas - y - 1.0, [(t, dict(bullet=True, after=10)) for t in puces], size=11)
