"""Delta V44 (base V43) : reprises de mise en forme uniquement (aucun texte change), sur les slides ou le rendu PowerPoint
reel montrait un defaut mesurable : 7, 15, 20, 22, 23, 26. Les slides 29, 34, 39 (candidates du brief) ont ete revues
en pleine resolution et laissees intactes : lisibles, sans collision.
Technique Vscode9 adoptee : separateur pointille = UN connecteur prstDash (vendor_v9.moa_outils.pointille), filet navy 0,75 pt,
ordre de rampe navy/gris, pas de forme inventee. Les formes restylees sont celles deja presentes (round2DiagRect, chevron).
Usage (depuis docs/cadrage-ppt/) : py deck_delta/deck.py delta_V44 --base V43 --sortie docs/exports/decks/offre-infra-as-a-product-V44.pptx
"""
import deck_base
from forme_v9 import BLANC, NAVY, arriere, deplacer, par_id, restyle, texte_couleur
from pptx import Presentation
from vendor_v9.moa_outils import pointille

BASE = "V43"
NOTE = "V44 : mise en forme (slides 7, 15, 20, 22, 23, 26), aucun texte modifie"
OPS = []
PT = 12700


def _id_rang(rang):
    prs = Presentation(deck_base.resoudre_base(BASE))
    return f"id:{prs.slides[rang - 1].slide_id}"


def _slide(prs, ident):
    return next(s for s in prs.slides if s.slide_id == ident)


def _decaler(s, dy, haut, bas=10_000, hors=()):
    """Decale de dy pt toutes les formes (hors placeholders) dont le haut est dans [haut, bas[."""
    for sh in s.shapes:
        if sh.is_placeholder or sh.shape_id in hors:
            continue
        if haut * PT <= sh.top < bas * PT:
            sh.top = sh.top + int(dy * PT)


def s07(prs, sid):
    s = _slide(prs, sid)
    _decaler(s, -14, 99)


def s22(prs, sid):
    s = _slide(prs, sid)
    _decaler(s, -14, 99)


def s23(prs, sid):
    s = _slide(prs, sid)
    d = par_id(s)
    for i in (161, 163, 165, 167, 169):  # chevrons : gris pale -> navy, texte blanc (rampe navy/gris, un sur N non necessaire)
        restyle(d[i], fill=NAVY)
    for i in (162, 164, 166, 168, 170):
        texte_couleur(d[i], BLANC)
    _decaler(s, -26, 100, 215)   # bandeau + chevrons + pictos
    _decaler(s, -12, 215)        # trois effets


def s20(prs, sid):
    s = _slide(prs, sid)
    d = par_id(s)
    for i in (213, 221, 229, 237, 245):  # cellules grises : ne mordent plus sur le coin arrondi de la ligne
        deplacer(d[i], w=214)
    deplacer(d[252], y=349)
    deplacer(d[253], y=349)
    deplacer(d[254], y=349)
    deplacer(d[196], y=368)


def s15(prs, sid):
    s = _slide(prs, sid)
    d = par_id(s)
    _decaler(s, 8, 216)          # carte 2 et son contenu : plus d'air sous la carte 1
    deplacer(d[172], h=160)
    deplacer(d[171], y=203)      # chevron centre dans l'interstice


def s26(prs, sid):
    s = _slide(prs, sid)
    d = par_id(s)
    for i in (68, 71, 74):       # libelles decolles des losanges
        deplacer(d[i], x=d[i].left / PT - 9)
    for i, x in ((55, 198), (56, 352), (57, 505)):  # separateurs de trimestre : un connecteur pointille navy
        d[i]._element.getparent().remove(d[i]._element)
        c = pointille(s, x / 72, 127 / 72, x / 72, 226 / 72)
        arriere(s, c)


def _etape(r, f, nom):
    return {"declarer": [_id_rang(r)], "f": lambda prs: f(prs, int(_id_rang(r)[3:])), "nouvelles_max": 0, "nom": nom}


ETAPES = [
    _etape(7, s07, "7 : contenu remonte sous le titre"),
    _etape(15, s15, "15 : chevron centre, carte 2 dilatee"),
    _etape(20, s20, "20 : cellules, A VALIDER et source degages"),
    _etape(22, s22, "22 : contenu remonte sous le titre"),
    _etape(23, s23, "23 : chevrons navy, vide reduit"),
    _etape(26, s26, "26 : libelles, separateurs pointilles"),
]
