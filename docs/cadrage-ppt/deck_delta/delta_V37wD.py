"""Delta V37wD (base V36) : conviction 11 retravaillee sur le fond ; conviction 10 inchangee (le doublon du mot est traite par le lot p).

Demande : « slide 17 : conviction en doublon + slide a revoir sur le fond ».
- Conviction 11 : trois temps Mesurer -> Montrer -> Agir (une carte chacun, 3 points), puis UN contraste compact SLA / service vecu (2 paires).
- Ce qui sort de la slide va, verbatim, dans les notes. Rail gauche, points, filet, navigation, titre : non touches.
Usage (depuis docs/cadrage-ppt/) : py deck_delta/deck.py delta_V37wD --base V36 --sortie C:/tmp/deck-v37-wD/V37wD.pptx --sans-rendu
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

BASE = "V36"
NOTE = "V37wD : conviction 11 recomposee sur le fond (Mesurer, Montrer, Agir + contraste SLA / vecu)"
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
RETIRE = (
    "Ligne retirée du contraste SLA / service vécu (V37) : « Tickets traités » | « Du temps passé à subir plutôt qu'à améliorer » | « Part de RUN subi et maîtrisé ».\n"
    "Colonne « Ce que nous suivons » (V36), reprise dans les trois temps : « Objectif de service publié par capacité » (Agir : un objectif de service par capacité) ; "
    "« Taux d'incidents récurrents » (retiré, l'incident qui revient reste dans le contraste) ; « Part de RUN subi et maîtrisé » (Mesurer).\n"
    "Boucle V36 : « Mesurer : l'écart entre le SLA et le service vécu ↔ en continu ↔ Montrer : à rythme régulier, les écarts et la charge de RUN » : devenue les trois temps Mesurer, Montrer, Agir, relus en continu.\n"
    "Sources des ajouts V37 : satisfaction et effort perçu = slide des indicateurs de valeur client (expérience utilisateur) et conviction sur les besoins utilisateurs ; "
    "COMOP et COPIL = slide des trois instances (cadence à fixer avec le client) ; objectif de service par capacité et revue trimestrielle des écarts = chantier d'origine ci-dessus ; "
    "écarts au backlog = le COPIL décide du backlog et de la roadmap. Destinataires de la restitution et lien écarts / backlog : à valider."
)


def _retirer_corps(s):
    """Retire le corps (x >= 189, y >= 88) ; le rail, les points, le filet, la navigation et le titre restent."""
    for sh in list(s.shapes):
        if sh.is_placeholder or sh.name.startswith("nav-"):
            continue
        if sh.left / 12700 >= 189 and sh.top / 12700 >= 88:
            sh._element.getparent().remove(sh._element)


def _navy(carte):
    carte.fill.solid()
    carte.fill.fore_color.rgb = NAVY
    carte.line.fill.background()


def conviction11(prs):
    s = deck_draw.slide_par_titre(prs, T_C11)
    _retirer_corps(s)
    cw = 127.0
    gap = (LARG - 3 * cw) / 2
    y0, h = 94.0, 146.0
    for k, (nom, points) in enumerate(ETAPES_TXT):
        x = X0 + k * (cw + gap)
        accent = k == 2
        col = BLANC if accent else NAVY
        carte = carte_diag(s, x, y0, cw, h, adj=0.12)
        if accent:
            _navy(carte)
        carre_num_cyan(s, x + 9, y0 + 9, 24, k + 1, sz=13)
        tx(s, x + 40, y0 + 9, cw - 46, 24, [[(nom, 15, True, col)]], A.MIDDLE)
        tx(s, x + 10, y0 + 44, cw - 18, h - 50, [[(p, 11, False, col)] for p in points], A.TOP, espace=5)
        if k:
            chevron_sep(s, x - gap / 2 - 4, y0 + 15, 8, 14)
    # contraste SLA / service vecu, compact
    yc, ht, hl = 256.0, 26.0, 40.0
    c0, c1 = 128.0, LARG - 128.0
    forme(s, S.ROUNDED_RECTANGLE, X0, yc, LARG, ht, CYAN, None, adj=0.5)
    tx(s, X0 + 12, yc, c0 - 14, ht, [[(EN_TETE[0], 11, True, NAVY)]], A.MIDDLE)
    tx(s, X0 + c0 + 12, yc, c1 - 14, ht, [[(EN_TETE[1], 11, True, NAVY)]], A.MIDDLE)
    for k, (a, b) in enumerate(PAIRES):
        y = yc + ht + 3 + k * hl
        if k % 2 == 0:
            forme(s, S.RECTANGLE, X0, y, LARG, hl, PANEL, None)
        tx(s, X0 + 12, y, c0 - 16, hl, [[(a, 11, False, NAVY)]], A.MIDDLE)
        tx(s, X0 + c0 + 12, y, c1 - 16, hl, [[(b, 11, True, NAVY)]], A.MIDDLE)
    ancien = s.notes_slide.notes_text_frame.text.strip() if s.has_notes_slide else ""
    s.notes_slide.notes_text_frame.text = (ancien + "\n\n" if ancien else "") + RETIRE


def _ids():
    prs = Presentation(deck_base.resoudre_base(BASE))
    return [f"id:{deck_draw.slide_par_titre(prs, t).slide_id}" for t in TITRES]


_I = dict(zip(TITRES, _ids(), strict=True))
ETAPES = [
    {"declarer": [_I[T_C11]], "f": conviction11, "nouvelles_max": 0, "nom": "conviction 11 : Mesurer, Montrer, Agir + contraste SLA / vecu"},
]
