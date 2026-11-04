"""Delta V32b_alt3 (base V31) : variante 3 de la slide « Six leviers au service de cinq resultats metier », pour APERCU seulement.

Cinq cartes hautes, une par resultat metier, chacune coiffee d'un pictogramme rond qui chevauche son bord haut (vocabulaire de l'exemple de reference) et listant
les leviers qui l'alimentent en pastilles numerotees ; un bandeau gris rappelle les six leviers et leur citation. Memes 13 liens que la V31 (lus sur ses ovales).
Usage (depuis docs/cadrage-ppt/) : py deck_delta/deck.py delta_V32b_alt3 --base V31 --sortie C:/tmp/deck-v32-b/V32b_alt3.pptx
"""
import re

import deck_base
from delta_V32b import T_7, _garder, _picto, _s, _txt, lire_leviers
from forme_v9 import BLANC, NAVY, PANEL, SLATE, deplacer, forme, par_id, tx
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE as S
from pptx.enum.text import MSO_ANCHOR as A
from pptx.enum.text import PP_ALIGN as P

BASE = "V31"
NOTE = "V32b_alt3 : slide Six leviers en cinq cartes-resultats a pictogramme rond (apercu)"
OPS = []
TITRES = (T_7,)
PICTO_RESULTAT = ("cycle", "personnes", "coche", "jauge", "ampoule")  # un pictogramme par resultat, dans l'ordre de la V31


def leviers_alt3(prs):
    s = _s(prs, T_7)
    entetes, lignes, liens = lire_leviers(s)
    b = par_id(s)
    kick = [sh for sh in s.shapes if sh.has_text_frame and re.match(r"^\d\d · ", _txt(sh))]
    _garder(s, {3, 4} | {k.shape_id for k in kick})
    deplacer(b[3], h=33)

    W, G, Y, H = 114, 11, 160, 148
    for k, titre in enumerate(entetes):
        x = 45 + k * (W + G)
        forme(s, S.ROUNDED_RECTANGLE, x, Y, W, H, BLANC, NAVY, adj=0.1, lw=0.75)
        _picto(s, PICTO_RESULTAT[k], x + W / 2, Y, 46, ratio=0.6, sans_ombre=True)
        tx(s, x + 6, Y + 25, W - 12, 28, [[(titre, 11, True, NAVY)]], A.MIDDLE, P.CENTER)
        for j, r in enumerate(sorted(r for (r, c) in liens if c == k)):
            y = Y + 58 + j * 22
            forme(s, S.ROUNDED_RECTANGLE, x + 10, y, W - 20, 18, NAVY, None, adj=0.5)
            tx(s, x + 18, y, W - 32, 18, [[(lignes[r][0], 10, True, BLANC)]], A.MIDDLE)
    # bandeau gris : les six leviers et leur citation
    BY, BH = 316, 44
    forme(s, S.ROUNDED_RECTANGLE, 45, BY, 614, BH, PANEL, None, adj=0.2)
    tx(s, 59, BY, 62, BH, [[("LEVIERS", 10, True, NAVY)]], A.MIDDLE)
    for r, (nom, cit) in enumerate(lignes):
        x = 128 + (r // 3) * 270
        y = BY + 5 + (r % 3) * 12.5
        tx(s, x, y, 262, 12.5, [[(nom, 10, True, NAVY), (f"  {cit}", 10, False, SLATE)]], A.MIDDLE)


def _ids():
    prs = Presentation(deck_base.resoudre_base(BASE))
    return [f"id:{_s(prs, t).slide_id}" for t in TITRES]


ETAPES = [{"declarer": _ids(), "f": leviers_alt3, "nouvelles_max": 0, "nom": "Six leviers : cartes par resultat"}]
