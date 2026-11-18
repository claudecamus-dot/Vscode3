"""Delta V45 (base V44) : slides de contenu recomposees dans le vocabulaire de formes du deck Vscode9
(accompagnement-agilite-agentique-octo-v1.pptx) - AUCUN texte modifie, aucun shape ajoute ou supprime.

Regles de transformation (mesurees dans le deck Vscode9 et formes_ref.py) :
- grande carte (>= 1,4 x 0,7 in), blanche ou gris pale -> round2DiagRect, rayon 0,19 in (adj = r / petit cote), trait navy 0,75 pt,
  fond blanc ; le coin arrondi alterne (flipH une carte sur deux), comme les panneaux emboites des slides 53-55 / 63 / 94 ;
- grande carte navy -> meme round2DiagRect (fond navy conserve, texte blanc intact) ;
- carre numerote cyan (0,3-0,5 in) -> disque blanc cercle navy (disque des pictos, ref. 110-111) ; le chiffre navy reste lisible ;
- pilule d'etiquette (haut 0,2-0,35 in) -> roundRect a 50 % ; pilule grise -> blanche cerclee navy ;
- bandeau large court (>= 2 in, 0,25-0,7 in) -> round2SameRect, adj 0,4 (en-tete d'onglet / de colonne, ref. 94 et 86) ;
- grand panneau gris (rect) -> round2DiagRect blanc cercle navy.
Le chrome (bandeau de chapitres, haut < 0,45 in) et les 13 points d'indicateur (0,11 in) ne sont jamais touches.
Usage : py deck_delta/deck.py delta_V45 --base V44 --sortie docs/exports/decks/offre-infra-as-a-product-V45.pptx
"""
import deck_base
from lxml import etree
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.util import Pt

BASE = "V44"
NOTE = "V45 : formes Vscode9 (cartes round2DiagRect, disques, pilules, en-tetes) sur les slides de contenu, aucun texte modifie"
OPS = []
A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
NAVY = RGBColor(0x0E, 0x23, 0x56)
BLANC = RGBColor(0xFF, 0xFF, 0xFF)
EMU = 914400
RAYON = 0.19
RANGS = (6, 7, 8, 10, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 25, 26, 29, 30, 31, 33, 34, 35, 36, 37, 38, 39, 40, 41, 43)


def _fill(sh):
    try:
        if sh.fill.type == 1:
            return str(sh.fill.fore_color.rgb)
    except (AttributeError, TypeError):
        pass
    return None


def _forme(sh, prst, adj=()):
    g = sh._element.spPr.find(A + "prstGeom")
    g.set("prst", prst)
    av = g.find(A + "avLst")
    for c in list(av):
        av.remove(c)
    noms = {"round2DiagRect": ("adj1", "adj2"), "round2SameRect": ("adj1", "adj2"), "roundRect": ("adj",)}.get(prst, ())
    for nom, v in zip(noms, adj, strict=False):
        etree.SubElement(av, A + "gd", name=nom, fmla=f"val {int(round(v * 100000))}")


def _trait(sh, fill=None):
    if fill is not None:
        sh.fill.solid()
        sh.fill.fore_color.rgb = fill
    sh.line.color.rgb = NAVY
    sh.line.width = Pt(0.75)


def _flip(sh, oui):
    x = sh._element.spPr.find(A + "xfrm")
    if oui:
        x.set("flipH", "1")
    elif "flipH" in x.attrib:
        del x.attrib["flipH"]


def reformer(s, compte):
    """Applique les regles ci-dessus ; `compte` accumule le nombre de formes changees par type."""
    carte = 0
    for sh in list(s.shapes):
        if sh.is_placeholder or sh.shape_type != 1:  # AUTO_SHAPE seulement (ni texte, ni ligne, ni image)
            continue
        g = sh._element.spPr.find(A + "prstGeom")
        if g is None:
            continue
        prst = g.get("prst")
        w, h, y = sh.width / EMU, sh.height / EMU, sh.top / EMU
        if y < 0.45 or min(w, h) < 0.15:
            continue
        f = _fill(sh)
        pale = f in ("FFFFFF", "E7E9EE", "EBFAFB", "F2F3F6", "DAF6F9")
        grande = w >= 1.4 and h >= 0.7
        if prst in ("roundRect", "round2DiagRect", "rect") and grande and (pale or f == "0E2356"):
            if prst == "rect" and w < 3:
                continue
            if f == "0E2356" and prst == "rect":
                continue
            _forme(sh, "round2DiagRect", (min(0.5, RAYON / min(w, h)), 0))
            _trait(sh, BLANC if pale else None)
            _flip(sh, carte % 2 == 1)
            carte += 1
            compte["carte"] = compte.get("carte", 0) + 1
        elif prst == "roundRect" and f == "00D2DD" and 0.3 <= w <= 0.5 and 0.3 <= h <= 0.5 and abs(w - h) < 0.03:
            _forme(sh, "ellipse")
            _trait(sh, BLANC)
            compte["disque"] = compte.get("disque", 0) + 1
        elif prst == "roundRect" and 0.2 <= h <= 0.35 and w > 0.6 and f in ("00D2DD", "0E2356", "E7E9EE", "FFFFFF"):
            _forme(sh, "roundRect", (0.5,))
            if f in ("E7E9EE", "FFFFFF"):
                _trait(sh, BLANC)
            compte["pilule"] = compte.get("pilule", 0) + 1
        elif prst in ("rect", "roundRect") and w >= 2 and 0.25 <= h <= 0.7 and (f == "0E2356" or (w >= 3.5 and f in ("E7E9EE", "EBFAFB", "DAF6F9"))):
            _forme(sh, "round2SameRect", (0.4, 0))
            if f != "0E2356":
                _trait(sh, BLANC)
            compte["entete"] = compte.get("entete", 0) + 1


def _id_rang(rang):
    prs = Presentation(deck_base.resoudre_base(BASE))
    return f"id:{prs.slides[rang - 1].slide_id}"


def _etape(r):
    ident = _id_rang(r)

    def f(prs):
        s = next(x for x in prs.slides if f"id:{x.slide_id}" == ident)
        c = {}
        reformer(s, c)
        print(f"V45 slide {r} : {c}")

    return {"declarer": [ident], "f": f, "nouvelles_max": 0, "nom": f"{r} : formes Vscode9"}


ETAPES = [_etape(r) for r in RANGS]
