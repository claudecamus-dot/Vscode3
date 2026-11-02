"""Vocabulaire de formes de Vscode9 (deck_orga_echelle/build.py), porte pour les deltas du deck Infra as a Product. Dimensions en points (slide 720x405).
Le kit du hub (pptx_deck.add_forme/add_chip/add_rect) travaille en pouces sur un autre gabarit : on reutilise forme()/tx() de forme_v26 (meme sortie, en points).
Couleurs : NAVY, CYAN (aplat seulement, jamais en texte : texte navy sur cyan), SLATE, PANEL, PALE, LINE. Jamais d'orange.
Deux familles : creation (panneau_gris, carte_diag, carre_num_cyan, pilule_entete, chevron_sep) et restylage de formes existantes (restyle, texte_couleur), qui garde le texte intact."""
from forme_v26 import BLANC, CLAIR, CYAN, FONT, MUTED, NAVY, S, forme, pt, tx  # noqa: F401
from pptx.dml.color import RGBColor as C
from pptx.enum.text import MSO_ANCHOR as A
from pptx.enum.text import PP_ALIGN as P
from pptx.util import Pt

SLATE, PANEL = MUTED, CLAIR
PALE = C(0xEB, 0xFA, 0xFB)
LINE = C(0xCF, 0xD3, 0xDD)

_PRST = {"round2DiagRect": ("adj1", "adj2"), "roundRect": ("adj",), "rect": (), "chevron": ("adj",)}


def par_id(s):
    return {sh.shape_id: sh for sh in s.shapes}


def arriere(s, sh):
    """Envoie la forme tout derriere (apres nvGrpSpPr et grpSpPr de l'arbre)."""
    el = sh._element
    tree = el.getparent()
    tree.remove(el)
    tree.insert(2, el)
    return sh


def avant(ref, sh):
    """Place `sh` juste derriere `ref` (z-order) : sh se dessine sous ref."""
    el = sh._element
    el.getparent().remove(el)
    ref._element.addprevious(el)
    return sh


def panneau_gris(s, x, y, w, h):
    """Panneau PANEL (gris) a plat, derriere tout le corps (patron « bandeau fond » de Vscode9 s_options)."""
    return arriere(s, forme(s, S.RECTANGLE, x, y, w, h, PANEL))


def carte_diag(s, x, y, w, h, accent=False, adj=0.08):
    """Carte round2DiagRect : blanche a bord LINE, ou (accent) cyan sans bord. Texte navy dessus."""
    return forme(s, S.ROUND_2_DIAG_RECTANGLE, x, y, w, h, CYAN if accent else BLANC, None if accent else LINE, adj=adj, lw=0.75)


def carre_num_cyan(s, x, y, d, num, sz=10):
    """Carre arrondi cyan portant un numero navy."""
    forme(s, S.ROUNDED_RECTANGLE, x, y, d, d, CYAN, None, adj=0.22)
    return tx(s, x, y, d, d, [[(str(num), sz, True, NAVY)]], A.MIDDLE, P.CENTER)


def pilule_entete(s, x, y, w, h, texte, couleur, sz=9):
    """Pilule d'entete pleine : texte navy sur cyan, blanc sur navy/slate."""
    forme(s, S.ROUNDED_RECTANGLE, x, y, w, h, couleur, None, adj=0.5)
    return tx(s, x, y, w, h, [[(texte, sz, True, NAVY if couleur == CYAN else BLANC)]], A.MIDDLE, P.CENTER)


def chevron_sep(s, x, y, w, h):
    """Chevron cyan separateur entre deux colonnes."""
    return forme(s, S.CHEVRON, x, y, w, h, CYAN, None, adj=0.35)


# ---------------------------------------------------------------- restylage de formes existantes (le texte et les ids restent)
def restyle(sh, prst=None, adj=None, fill="garde", ligne="garde", lw=0.75):
    """prst : roundRect / round2DiagRect / rect ; adj : fraction du petit cote ; fill/ligne : RGBColor, None (aucun) ou 'garde'."""
    if prst:
        sp = sh._element.spPr
        g = sp.find("{http://schemas.openxmlformats.org/drawingml/2006/main}prstGeom")
        g.set("prst", prst)
        av = g.find("{http://schemas.openxmlformats.org/drawingml/2006/main}avLst")
        for c in list(av):
            av.remove(c)
        if adj is not None and _PRST[prst]:
            from lxml import etree
            ns = "http://schemas.openxmlformats.org/drawingml/2006/main"
            for k, nom in enumerate(_PRST[prst]):
                gd = etree.SubElement(av, f"{{{ns}}}gd")
                gd.set("name", nom)
                gd.set("fmla", f"val {int(round(adj * 100000)) if k == 0 else 0}")
    if fill != "garde":
        if fill is None:
            sh.fill.background()
        else:
            sh.fill.solid()
            sh.fill.fore_color.rgb = fill
    if ligne != "garde":
        if ligne is None:
            sh.line.fill.background()
        else:
            sh.line.color.rgb = ligne
            sh.line.width = Pt(lw)
    return sh


def texte_couleur(sh, rgb):
    for p in sh.text_frame.paragraphs:
        for r in p.runs:
            r.font.color.rgb = rgb


def deplacer(sh, x=None, y=None, w=None, h=None):
    if x is not None:
        sh.left = pt(x)
    if y is not None:
        sh.top = pt(y)
    if w is not None:
        sh.width = pt(w)
    if h is not None:
        sh.height = pt(h)
    return sh


def supprimer(sh):
    sh._element.getparent().remove(sh._element)
