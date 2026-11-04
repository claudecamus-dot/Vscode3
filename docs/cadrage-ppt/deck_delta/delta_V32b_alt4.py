"""Delta V32b_alt4 (base V31) : variante 4 de la slide « Six leviers au service de cinq resultats metier », pour APERCU seulement.

Deux colonnes : six cartes-leviers a gauche (pictogramme, numero, nom, citation), cinq pastilles-resultats a droite (pictogramme, nom),
et les 13 liens tires en connecteurs courbes navy de meme epaisseur, de point rond a point rond. Les resultats sont ordonnes pour reduire les croisements
(19 croisements dans l'ordre V31, 16 apres echange de « Maitrise des couts » et « Anticipation de l'IA », meilleur ordre des 120 permutations).
Memes 13 liens que la V31 (lus sur ses ovales). Usage (depuis docs/cadrage-ppt/) : py deck_delta/deck.py delta_V32b_alt4 --base V31 --sortie C:/tmp/deck-v32-b/V32b_alt4.pptx
"""
import re

import deck_base
from delta_V32b import (
    GENRES_LEVIERS,
    PICTO,
    T_7,
    _garder,
    _picto,
    _s,
    _sans_ombre,
    _txt,
    lire_leviers,
)
from forme_v9 import BLANC, NAVY, SLATE, deplacer, forme, par_id, tx
from pptx import Presentation
from pptx.enum.shapes import MSO_CONNECTOR
from pptx.enum.shapes import MSO_SHAPE as S
from pptx.enum.text import MSO_ANCHOR as A
from pptx.util import Pt

BASE = "V31"
NOTE = "V32b_alt4 : slide Six leviers en deux colonnes reliees par des connecteurs (apercu)"
OPS = []
TITRES = (T_7,)
PICTO_RESULTAT = ("cycle", "personnes", "coche", "jauge", "ampoule")  # dans l'ordre de la V31
ORDRE = (0, 1, 2, 4, 3)  # ordre d'affichage des resultats (index V31) : minimise les croisements


def leviers_alt4(prs):
    s = _s(prs, T_7)
    entetes, lignes, liens = lire_leviers(s)
    b = par_id(s)
    kick = [sh for sh in s.shapes if sh.has_text_frame and re.match(r"^\d\d · ", _txt(sh))]
    _garder(s, {3, 4} | {k.shape_id for k in kick})
    deplacer(b[3], h=33)

    XL, WL, HL, PL, Y0 = 45, 250, 32, 36, 146
    XR, WR, HR, PR, YR0 = 509, 150, 34, 42, 150
    yl = [Y0 + HL / 2 + i * PL for i in range(6)]
    yr = {k: YR0 + HR / 2 + j * PR for j, k in enumerate(ORDRE)}
    # un point d'attache PAR lien, repartis sur le bord (carte : pas 8 pt ; pastille : pas 7 pt), tries par ordre d'arrivee pour ne pas croiser pres des points
    def decale(n, i, pas):
        return (i - (n - 1) / 2) * pas

    def inset(dy, h):
        r = h / 2
        return r - (r * r - dy * dy) ** 0.5

    par_levier = {r: sorted((k for rr, k in liens if rr == r), key=lambda k: ORDRE.index(k)) for r in range(6)}
    par_resultat = {k: sorted(r for r, kk in liens if kk == k) for k in range(5)}
    attaches = []
    for (r, k) in liens:
        i, n = par_levier[r].index(k), len(par_levier[r])
        dy1 = decale(n, i, 8)
        j, m = par_resultat[k].index(r), len(par_resultat[k])
        dy2 = decale(m, j, 7)
        attaches.append(((XL + WL - inset(dy1, HL), yl[r] + dy1), (XR + inset(dy2, HR), yr[k] + dy2)))
    for (x1, y1), (x2, y2) in attaches:  # liens sous les cartes, meme epaisseur et couleur
        c = s.shapes.add_connector(MSO_CONNECTOR.CURVE, int(x1 * 12700), int(y1 * 12700), int(x2 * 12700), int(y2 * 12700))
        c.line.color.rgb = NAVY
        c.line.width = Pt(1.25)
        _sans_ombre(c)
    for r, ((nom, cit), g) in enumerate(zip(lignes, GENRES_LEVIERS, strict=True)):
        y = Y0 + r * PL
        forme(s, S.ROUNDED_RECTANGLE, XL, y, WL, HL, BLANC, NAVY, adj=0.5, lw=0.9)
        _picto(s, PICTO[g], XL + 22, y + HL / 2, 44, disque=False, ratio=0.6, sans_ombre=True)
        tx(s, XL + 44, y, WL - 56, HL, [[(nom, 10.5, True, NAVY)], [(cit, 10, False, SLATE)]], A.MIDDLE)
    for k, t in enumerate(entetes):
        y = yr[k] - HR / 2
        forme(s, S.ROUNDED_RECTANGLE, XR, y, WR, HR, BLANC, NAVY, adj=0.5, lw=0.9)
        _picto(s, PICTO_RESULTAT[k], XR + 22, y + HR / 2, 42, disque=False, ratio=0.6, sans_ombre=True)
        tx(s, XR + 42, y, WR - 52, HR, [[(t, 10, True, NAVY)]], A.MIDDLE)
    for (x1, y1), (x2, y2) in attaches:  # points ronds aux deux bouts de chaque lien
        for x, y in ((x1, y1), (x2, y2)):
            forme(s, S.OVAL, x - 3.5, y - 3.5, 7, 7, NAVY, None)


def _ids():
    prs = Presentation(deck_base.resoudre_base(BASE))
    return [f"id:{_s(prs, t).slide_id}" for t in TITRES]


ETAPES = [{"declarer": _ids(), "f": leviers_alt4, "nouvelles_max": 0, "nom": "Six leviers : deux colonnes et connecteurs"}]
