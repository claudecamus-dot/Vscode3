"""Delta V38b (base V37) : slide « Besoins mesures, porteur nomme, priorites fondees sur des faits » - occupation de l'espace.

- trois cartes elargies (190 -> 198 pt, gouttiere 22 -> 10 pt), pictogrammes et pilules recentres ;
- enonces : conviction 2 a 12,5 pt, convictions 3 et 4 a 15 pt, pour des hauteurs voisines (fin de la bande vide sous les enonces courts) ;
- filets remontes, puces a 12 pt (au lieu de 11) sur une colonne plus large, pas regulier jusqu'au bas de la carte.
Texte inchange. Usage (depuis docs/cadrage-ppt/) : py deck_delta/deck.py delta_V38b --base V37 --sortie C:/tmp/deck-v38-b/V38b.pptx --sans-rendu
"""
import deck_base
import deck_draw
from forme_v9 import CYAN, NAVY, S, forme, tx
from forme_v9 import deplacer as mv
from pptx import Presentation
from pptx.enum.text import MSO_ANCHOR as A
from pptx.enum.text import PP_ALIGN as P
from pptx.util import Pt

BASE = "V37"
NOTE = "V38b : convictions 2 a 4, cartes elargies, enonces de hauteur voisine, puces 12 pt"
OPS = []

T = "Besoins mesurés, porteur nommé, priorités fondées sur des faits"
W, GAP = 198.0, 10.0
ENONCE_Y, ENONCE_H = 177.0, 64.0
PAS = 14.6  # interligne d'une puce a 12 pt


def _d(s):
    return {sh.shape_id: sh for sh in s.shapes}


def _x(sh):
    return sh.left / 12700


def convictions_234(prs):
    s = deck_draw.slide_par_titre(prs, T)
    d = _d(s)
    cartes = [sh for sh in s.shapes if sh.shape_type == 1 and round(sh.width / 12700) == 190 and round(sh.height / 12700) == 246]
    cartes.sort(key=_x)
    assert len(cartes) == 3, len(cartes)
    enonces = sorted([sh for sh in s.shapes if sh.has_text_frame and round(sh.top / 12700) == 177], key=_x)
    filets = [sh for sh in s.shapes if sh.shape_type == 1 and sh.height < 12700 and sh.top / 12700 > 240]
    puces_y = [sh for sh in s.shapes if sh.top / 12700 > 265 and sh.top / 12700 < 364 and sh.width / 12700 < 160]
    textes = {}
    for sh in sorted(puces_y, key=lambda z: (_x(z), z.top)):
        if sh.has_text_frame and sh.text_frame.text.strip():
            textes.setdefault(round(_x(sh)), []).append(sh.text_frame.text)
    cols_txt = [textes[k] for k in sorted(textes)]
    assert len(cols_txt) == 3 and all(len(c) == 3 for c in cols_txt), cols_txt
    for sh in filets + puces_y:
        sh._element.getparent().remove(sh._element)
    tailles = (12.5, 15, 15)
    for i, carte in enumerate(cartes):
        ox = _x(carte)
        nx = 45.0 + i * (W + GAP)
        dx = nx + W / 2 - (ox + 95.0)
        # tout ce qui est dans la colonne au-dessus des puces (picto, pilule) : translation
        for sh in list(s.shapes):
            if sh is carte or sh.shape_id in (2,) or sh.top / 12700 < 80 or sh.top / 12700 > 175 or (sh.top / 12700 < 92 and sh.height / 12700 < 6):
                continue
            cx = _x(sh) + sh.width / 25400
            if ox <= cx <= ox + 190:
                mv(sh, x=_x(sh) + dx)
        mv(carte, x=nx, w=W)
        en = enonces[i]
        mv(en, x=nx + 12, y=ENONCE_Y, w=W - 20, h=ENONCE_H)
        for para in en.text_frame.paragraphs:
            for r in para.runs:
                r.font.size = Pt(tailles[i])
        ys = ENONCE_Y + ENONCE_H + 3
        forme(s, S.RECTANGLE, nx + 12, ys, W - 24, 0.75, NAVY)
        y = ys + 7
        for texte in cols_txt[i]:
            forme(s, S.OVAL, nx + 14, y + 3.8, 7, 7, CYAN, NAVY, lw=0.75)
            h = 2 * PAS
            tx(s, nx + 28, y, W - 40, h, [[(texte, 12, False, NAVY)]], A.TOP, P.LEFT)
            y += h + 5
    del d


def _ids():
    prs = Presentation(deck_base.resoudre_base(BASE))
    return f"id:{deck_draw.slide_par_titre(prs, T).slide_id}"


ETAPES = [
    {"declarer": [_ids()], "f": convictions_234, "nouvelles_max": 0, "nom": "convictions 2 a 4 : occupation de l'espace"},
]
