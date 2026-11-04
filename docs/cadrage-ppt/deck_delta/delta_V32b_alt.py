"""Delta V32b_alt (base V31) : variante 2 de la slide « Six leviers au service de cinq resultats metier », pour APERCU seulement.

Pas de matrice : une ligne arrondie par levier (pictogramme, numero, nom, citation) et, a droite, les NOMS des resultats lies en pastilles navy.
Memes 13 liens que la V31 (lus sur ses ovales), meme phrase d'accroche, memes pictogrammes que delta_V32b.
Usage (depuis docs/cadrage-ppt/) : py deck_delta/deck.py delta_V32b_alt --base V31 --sortie C:/tmp/deck-v32-b/V32b_alt.pptx
"""
import re

import deck_base
from delta_V32b import GENRES_LEVIERS, PICTO, T_7, _garder, _picto, _s, _txt, lire_leviers
from forme_v9 import BLANC, NAVY, PANEL, SLATE, deplacer, forme, par_id, tx
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE as S
from pptx.enum.text import MSO_ANCHOR as A
from pptx.enum.text import PP_ALIGN as P

BASE = "V31"
NOTE = "V32b_alt : slide Six leviers en lignes-pilules, resultats lies nommes en pastilles (apercu)"
OPS = []
TITRES = (T_7,)


def leviers_alt(prs):
    s = _s(prs, T_7)
    entetes, lignes, liens = lire_leviers(s)
    b = par_id(s)
    kick = [sh for sh in s.shapes if sh.has_text_frame and re.match(r"^\d\d · ", _txt(sh))]
    _garder(s, {3, 4} | {k.shape_id for k in kick})
    deplacer(b[3], h=33)

    X_L, W_L = 45, 614
    X_C = 282  # debut commun des pastilles de resultats
    HY, HH = 142, 18
    RY, RH, RP = 166, 30, 34
    forme(s, S.ROUNDED_RECTANGLE, X_L, HY, X_C - 8 - X_L, HH, PANEL, None, adj=0.5)
    tx(s, X_L, HY, X_C - 8 - X_L, HH, [[("LEVIERS", 9.5, True, NAVY)]], A.MIDDLE, P.CENTER)
    forme(s, S.ROUNDED_RECTANGLE, X_C, HY, X_L + W_L - X_C, HH, PANEL, None, adj=0.5)
    tx(s, X_C, HY, X_L + W_L - X_C, HH, [[("RÉSULTATS MÉTIER", 9.5, True, NAVY)]], A.MIDDLE, P.CENTER)
    for r, ((nom, cit), g) in enumerate(zip(lignes, GENRES_LEVIERS, strict=True)):
        y = RY + r * RP
        forme(s, S.ROUNDED_RECTANGLE, X_L, y, W_L, RH, BLANC, NAVY, adj=0.5, lw=0.9)
        _picto(s, PICTO[g], X_L + 24, y + RH / 2, 44, disque=False, ratio=0.6, sans_ombre=True)
        tx(s, X_L + 48, y, X_C - X_L - 56, RH, [[(nom, 10.5, True, NAVY)], [(cit, 9.5, False, SLATE)]], A.MIDDLE)
        x = X_C
        for k in sorted(c for (rr, c) in liens if rr == r):
            t = entetes[k]
            w = len(t) * 5.4 + 18
            forme(s, S.ROUNDED_RECTANGLE, x, y + 5, w, RH - 10, NAVY, None, adj=0.5)
            tx(s, x, y + 5, w, RH - 10, [[(t, 9.5, True, BLANC)]], A.MIDDLE, P.CENTER)
            x += w + 6


def _ids():
    prs = Presentation(deck_base.resoudre_base(BASE))
    return [f"id:{_s(prs, t).slide_id}" for t in TITRES]


ETAPES = [{"declarer": _ids(), "f": leviers_alt, "nouvelles_max": 0, "nom": "Six leviers : variante en lignes-pilules"}]
