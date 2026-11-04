"""Delta V38d (base V37) : conviction 11, occupation de l'espace (cartes a puces, tableau SLA / vecu a colonnes egales).

Demande : « slide 17 : conviction en doublon + slide a revoir sur le fond ».
- Conviction 11 : trois temps Mesurer -> Montrer -> Agir (une carte chacun, 3 points), puis UN contraste compact SLA / service vecu (2 paires).
- Ce qui sort de la slide va, verbatim, dans les notes. Rail gauche, points, filet, navigation, titre : non touches.
Usage (depuis docs/cadrage-ppt/) : py deck_delta/deck.py delta_V38d --base V37 --sortie C:/tmp/deck-v38-d/V38d.pptx --sans-rendu
"""
import deck_base
import deck_draw
from forme_v9 import (
    BLANC,
    CYAN,
    NAVY,
    PANEL,
    S,
    carre_num_cyan,
    carte_diag,
    chevron_sep,
    forme,
    tx,
)
from pptx import Presentation
from pptx.enum.text import MSO_ANCHOR as A

BASE = "V37"
NOTE = "V38d : conviction 11, cartes a puces et tableau SLA / vecu equilibre (meme texte)"
OPS = []

NB = "\u00a0"
T_C11 = "Conviction 11" + NB + ": évaluer en continu le service vécu, le mesurer et le montrer"
TITRES = (T_C11,)

X0 = 258.0
X1 = 659.25
LARG = X1 - X0

ETAPES_TXT = [
    ("Mesurer", ["L'écart entre le SLA et le service vécu", "Satisfaction et effort perçu", "Part de RUN subi et maîtrisé"]),
    ("Montrer", ["À rythme régulier", "Aux consommateurs, au COMOP et au COPIL (à valider)", "Écarts et charge de RUN"]),
    ("Agir", ["Un objectif de service par capacité", "Revue trimestrielle des écarts", "Écarts au backlog (à valider)"]),
]
EN_TETE = ("Ce que dit le SLA", "Ce que vit le consommateur")
PAIRES = [
    ("Disponibilité du service", "Une demande qui attend, même quand le service est « vert »"),
    ("Incidents clos dans le délai", "Le même incident qui revient"),
]
def _retirer_corps(s):
    """Retire le corps (x >= 189, y >= 88) ; rail, points, filet, navigation et titre restent."""
    for sh in list(s.shapes):
        if sh.is_placeholder or sh.name.startswith("nav-"):
            continue
        if sh.left / 12700 >= 189 and sh.top / 12700 >= 88:
            sh._element.getparent().remove(sh._element)


def _navy(carte):
    carte.fill.solid()
    carte.fill.fore_color.rgb = NAVY
    carte.line.fill.background()


# nombre de lignes par point a 11 pt sur ~102 pt de large (mesure au rendu)
LIGNES = [[2, 2, 2], [1, 4, 2], [2, 2, 2]]
LH = 13.6


def conviction11(prs):
    s = deck_draw.slide_par_titre(prs, T_C11)
    _retirer_corps(s)
    gap = 12.0
    cw = (LARG - 2 * gap) / 3
    y0, h = 94.0, 156.0
    for k, (nom, points) in enumerate(ETAPES_TXT):
        x = X0 + k * (cw + gap)
        accent = k == 2
        col = BLANC if accent else NAVY
        carte = carte_diag(s, x, y0, cw, h, adj=0.12)
        if accent:
            _navy(carte)
        carre_num_cyan(s, x + 10, y0 + 10, 26, k + 1, sz=14)
        tx(s, x + 44, y0 + 10, cw - 50, 26, [[(nom, 16, True, col)]], A.MIDDLE)
        y = y0 + 46
        for p, n in zip(points, LIGNES[k], strict=True):
            forme(s, S.OVAL, x + 10, y + 4.5, 5, 5, CYAN, None)
            tx(s, x + 19, y, cw - 25, n * LH, [[(p, 11, False, col)]], A.TOP)
            y += n * LH + 6
        if k:
            chevron_sep(s, x - gap / 2 - 3, y0 + 16, 6, 14)
    # contraste SLA / service vecu : deux colonnes egales, en-tete plein
    yc, ht, hl, g = 260.0, 30.0, 36.0, 4.0
    c = LARG / 2
    forme(s, S.ROUNDED_RECTANGLE, X0, yc, LARG, ht, CYAN, None, adj=0.5)
    tx(s, X0 + 16, yc, c - 20, ht, [[(EN_TETE[0], 13, True, NAVY)]], A.MIDDLE)
    tx(s, X0 + c + 12, yc, c - 24, ht, [[(EN_TETE[1], 13, True, NAVY)]], A.MIDDLE)
    for k, (a, b) in enumerate(PAIRES):
        y = yc + ht + g + k * (hl + g)
        forme(s, S.RECTANGLE, X0, y, LARG, hl, PANEL, None)
        tx(s, X0 + 16, y, c - 20, hl, [[(a, 12, False, NAVY)]], A.MIDDLE)
        tx(s, X0 + c + 12, y, c - 24, hl, [[(b, 12, True, NAVY)]], A.MIDDLE)


def _ids():
    prs = Presentation(deck_base.resoudre_base(BASE))
    return [f"id:{deck_draw.slide_par_titre(prs, t).slide_id}" for t in TITRES]


_I = dict(zip(TITRES, _ids(), strict=True))
ETAPES = [
    {"declarer": [_I[T_C11]], "f": conviction11, "nouvelles_max": 0, "nom": "conviction 11 : cartes a puces + tableau SLA / vecu equilibre"},
]
