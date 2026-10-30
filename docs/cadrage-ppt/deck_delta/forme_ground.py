"""Vocabulaire de formes releve dans la proposition OCTO_GROUND (comites G1 et P2) : fond blanc, UN trait navy fin, cyan en aplat decoratif seulement (jamais porteur de texte),
cartes a grands coins, goutte (teardrop) a un coin pointu, colonnes a onglet reliees par un point cyan, barres-pilules navy / contour, anneaux enchaines, frise a cartouches,
pastilles a coche cyan, grands pictogrammes au trait navy remplis de cyan (redessines ici en formes natives). Dimensions en points (slide 720x405, zone utile x 45..659, y 98..362)."""
from forme_v26 import A, BLANC, CLAIR, CYAN, FONT, MUTED, NAVY, P, S, X0, X1, forme, garder, pt, signature_cyan, tx, vider  # noqa: F401
from pptx.enum.shapes import MSO_CONNECTOR
from pptx.util import Pt

LW = 1.0


def trait(s, x1, y1, x2, y2, lw=1.5, col=NAVY):
    c = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, pt(x1), pt(y1), pt(x2), pt(y2))
    c.line.color.rgb = col
    c.line.width = Pt(lw)
    return c


def carte(s, x, y, w, h, rayon=26, fill=BLANC):
    """Carte blanche a bord navy fin et grands coins."""
    return forme(s, S.ROUNDED_RECTANGLE, x, y, w, h, fill, NAVY, adj=min(0.5, rayon / min(w, h)), lw=LW)


def panneau(s, x, y, w, h, rayon=34, fill=BLANC):
    """Panneau a UN seul grand coin arrondi (haut droit) : signature des pages de constat."""
    return forme(s, S.ROUND_1_RECTANGLE, x, y, w, h, fill, NAVY, adj=min(0.5, rayon / min(w, h)), lw=LW)


def goutte_contour(s, x, y, d, fill=BLANC):
    """Goutte (teardrop) a contour navy : trois coins ronds, un pointu."""
    return forme(s, S.TEAR, x, y, d, d, fill, NAVY, lw=LW)


def pilule(s, x, y, w, h, texte_, style="navy", sz=10.5):
    """Barre-pilule : navy (texte blanc), contour (texte navy) ou cyan (texte navy, jamais blanc)."""
    fill = {"navy": NAVY, "contour": BLANC, "cyan": CYAN}[style]
    forme(s, S.ROUNDED_RECTANGLE, x, y, w, h, fill, NAVY if style == "contour" else None, adj=0.5, lw=LW)
    return tx(s, x + 6, y, w - 12, h, [[(texte_, sz, True, BLANC if style == "navy" else NAVY)]], A.MIDDLE, P.CENTER)


def point_cyan(s, cx, cy, d=10):
    return forme(s, S.OVAL, cx - d / 2, cy - d / 2, d, d, CYAN, NAVY, lw=0.75)


def coche(s, cx, cy, d=18):
    """Pastille a coche : disque cyan a trait navy, coche navy."""
    forme(s, S.OVAL, cx - d / 2, cy - d / 2, d, d, CYAN, NAVY, lw=0.75)
    trait(s, cx - d * 0.25, cy, cx - d * 0.05, cy + d * 0.2, 1.5)
    trait(s, cx - d * 0.05, cy + d * 0.2, cx + d * 0.27, cy - d * 0.2, 1.5)


def puces_coche(s, x, y, w, lignes, sz=10.5, pas=None, couleur=NAVY):
    pas = pas or (sz + 12)
    for k, t in enumerate(lignes):
        coche(s, x + 8, y + k * pas + 8, 16)
        tx(s, x + 24, y + k * pas, w - 24, pas, [[(t, sz, False, couleur)]], A.TOP)


def onglet(s, x, y, w, h, titre, sz=12):
    """Colonne a onglet : carte a grands coins, titre centre en haut, filet sous le titre."""
    carte(s, x, y, w, h, 24)
    tx(s, x + 10, y + 8, w - 20, 34, [[(titre, sz, True, NAVY)]], A.MIDDLE, P.CENTER)
    forme(s, S.RECTANGLE, x + 14, y + 46, w - 28, 0.75, NAVY, None)


def anneau(s, x, y, d, cyan=True):
    """Anneau (donut) du cycle enchaine : cyan en aplat ou blanc, bord navy."""
    r = forme(s, S.DONUT, x, y, d, d, CYAN if cyan else BLANC, NAVY, lw=LW)
    r.adjustments[0] = 0.22
    return r


def cartouche(s, x, y, num, texte_, w2=96, h=26):
    """Cartouche de frise : cellule numero + cellule libelle, deux pilules a contour navy."""
    forme(s, S.ROUNDED_RECTANGLE, x, y, 34, h, BLANC, NAVY, adj=0.5, lw=LW)
    tx(s, x, y, 34, h, [[(num, 10.5, True, NAVY)]], A.MIDDLE, P.CENTER)
    forme(s, S.ROUNDED_RECTANGLE, x + 38, y, w2, h, BLANC, NAVY, adj=0.5, lw=LW)
    tx(s, x + 38, y, w2, h, [[(texte_, 10.5, True, NAVY)]], A.MIDDLE, P.CENTER)


def noeud(s, cx, cy, d=16):
    forme(s, S.OVAL, cx - d / 2, cy - d / 2, d, d, BLANC, NAVY, lw=LW)
    forme(s, S.OVAL, cx - d / 5, cy - d / 5, d * 0.4, d * 0.4, CYAN, None)


# ---------------------------------------------------------------- pictogrammes au trait navy rempli de cyan (formes natives)
def picto(s, genre, cx, cy, d=64):
    f = d / 64.0
    def o(kind, dx, dy, w, h, fill=BLANC, lw=1.5, adj=None):
        return forme(s, kind, cx + dx * f, cy + dy * f, w * f, h * f, fill, NAVY, adj=adj, lw=lw)
    if genre == "cible":
        o(S.OVAL, -30, -30, 60, 60); o(S.OVAL, -20, -20, 40, 40, CYAN); o(S.OVAL, -10, -10, 20, 20); o(S.OVAL, -3, -3, 6, 6, NAVY)
        trait(s, cx, cy, cx + 30 * f, cy - 30 * f, 2); trait(s, cx + 30 * f, cy - 30 * f, cx + 22 * f, cy - 30 * f, 2); trait(s, cx + 30 * f, cy - 30 * f, cx + 30 * f, cy - 22 * f, 2)
    elif genre == "horloge":
        o(S.OVAL, -28, -28, 56, 56); o(S.OVAL, -3, -3, 6, 6, CYAN)
        trait(s, cx, cy, cx, cy - 18 * f, 2); trait(s, cx, cy, cx + 13 * f, cy + 6 * f, 2)
    elif genre == "calendrier":
        o(S.ROUNDED_RECTANGLE, -28, -24, 56, 52, adj=0.12); o(S.RECTANGLE, -28, -24, 56, 14, CYAN)
        for i in range(4):
            for j in range(2):
                o(S.RECTANGLE, -20 + i * 11, -2 + j * 12, 7, 7, CYAN, 1)
    elif genre == "jauge":
        o(S.BLOCK_ARC, -30, -26, 60, 60, CYAN); trait(s, cx, cy + 4 * f, cx + 14 * f, cy - 14 * f, 2.5); o(S.OVAL, -4, 0, 8, 8, NAVY)
    elif genre == "personnes":
        o(S.OVAL, -10, -28, 20, 20, CYAN); o(S.ROUNDED_RECTANGLE, -20, -4, 40, 30, CYAN, adj=0.45)
        o(S.OVAL, 14, -22, 14, 14); o(S.ROUNDED_RECTANGLE, 10, -4, 24, 22, adj=0.45)
    elif genre == "document":
        o(S.FLOWCHART_DOCUMENT, -20, -28, 40, 52); [trait(s, cx - 12 * f, cy + (-16 + 8 * i) * f, cx + 12 * f, cy + (-16 + 8 * i) * f, 1.5) for i in range(3)]
        o(S.OVAL, 10, 10, 18, 18, CYAN)
    elif genre == "classeurs":
        for i, c in enumerate((BLANC, CYAN, BLANC)):
            o(S.ROUNDED_RECTANGLE, -30 + i * 21, -26, 18, 52, c, adj=0.2)
            trait(s, cx + (-30 + i * 21 + 9) * f, cy - 14 * f, cx + (-30 + i * 21 + 9) * f, cy + 14 * f, 1)
    elif genre == "fleche":
        o(S.RIGHT_ARROW, -30, -16, 60, 32, CYAN)
    elif genre == "cycle":
        o(S.CIRCULAR_ARROW, -28, -28, 56, 56, CYAN); o(S.OVAL, -6, -6, 12, 12, NAVY)
    elif genre == "ampoule":
        o(S.OVAL, -18, -28, 36, 36, CYAN); o(S.ROUNDED_RECTANGLE, -9, 10, 18, 14, BLANC, adj=0.3)
        for ang in (-1, 0, 1):
            trait(s, cx + ang * 22 * f, cy - 30 * f, cx + ang * 28 * f, cy - 36 * f, 1.5)
    elif genre == "coche":
        o(S.OVAL, -28, -28, 56, 56, CYAN); trait(s, cx - 14 * f, cy, cx - 4 * f, cy + 11 * f, 3.5); trait(s, cx - 4 * f, cy + 11 * f, cx + 15 * f, cy - 11 * f, 3.5)
    elif genre == "grille":
        for i in range(2):
            for j in range(2):
                o(S.ROUNDED_RECTANGLE, -26 + i * 28, -26 + j * 28, 24, 24, CYAN if (i + j) % 2 == 0 else BLANC, adj=0.2)


def disque_picto(s, cx, cy, genre, d=110, goutte=True):
    """Grand disque (ou goutte) blanc a bord navy portant un pictogramme."""
    if goutte:
        goutte_contour(s, cx - d / 2, cy - d / 2, d)
    else:
        forme(s, S.OVAL, cx - d / 2, cy - d / 2, d, d, BLANC, NAVY, lw=LW)
    picto(s, genre, cx, cy, d * 0.56)
