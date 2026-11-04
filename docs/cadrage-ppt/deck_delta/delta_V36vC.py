"""Delta V36vC (base V35) : convictions 10 et 11 sans les zones « critere observable » / « chantier », corps recompose sur toute la hauteur.

Demande : « supprimer dans les slides de convictions les 2 zones "criteres observables" et "le chantier" et revoir la forme de chacune des slides ».
- Les deux bandeaux du bas sont supprimes ; leur texte, verbatim, est ajoute aux notes (« Critere observable (retire de la slide) » / « Chantier (retire de la slide) »).
- Conviction 10 : frise DoR -> Qualifier -> Automatiser lue deux fois (SANS IA / AVEC IA), cartes plus grandes, texte 11 pt ; un seul accent navy (la qualification par l'IA).
- Conviction 11 : boucle Mesurer <-> Montrer (en continu) puis tableau SLA / service vecu / ce que nous suivons, sur 92 -> 366 pt.
Rail gauche (filet, bloc pictogramme, pilule « CONVICTION n »), points de progression, pilules de navigation, titre : non touches.
Usage (depuis docs/cadrage-ppt/) : py deck_delta/deck.py delta_V36vC --base V35 --sortie C:/tmp/deck-v36-vC/V36vC.pptx --sans-rendu
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
    pilule_entete,
    tx,
)
from pptx import Presentation
from pptx.enum.text import MSO_ANCHOR as A
from pptx.enum.text import PP_ALIGN as P

BASE = "V35"
NOTE = "V36vC : convictions 10 et 11 sans critere observable ni chantier, corps recompose"
OPS = []

NB = "\u00a0"
T_C10 = "Conviction 10 : un flux d'entrée unique qui qualifie avant de servir"
T_C11 = "Conviction 11" + NB + ": évaluer en continu le service vécu, le mesurer et le montrer"
TITRES = (T_C10, T_C11)

X0 = 258.0
X1 = 659.25
LARG = X1 - X0
Y_BANDEAUX = 268          # les deux bandeaux du bas commencent a y = 273
SLATE_TXT = NAVY


def _retirer_corps_et_bandeaux(s):
    """Retire le corps (x >= 189, 88 <= y < 268) et les deux bandeaux (y >= 268), et renvoie les deux textes verbatim (critere, chantier).

    Le rail (x < 189, y < 268), les points (y = 70), le filet (y = 86), la navigation et le titre restent."""
    critere = chantier = None
    for sh in list(s.shapes):
        if sh.is_placeholder or sh.name.startswith("nav-"):
            continue
        y = sh.top / 12700
        x = sh.left / 12700
        if sh.has_text_frame and y >= Y_BANDEAUX:
            t = sh.text_frame.text
            if t.startswith("LE CRIT") or t.startswith("LE CHANTIER") or not t.strip():
                pass
            elif critere is None and x < 300:
                critere = t
            else:
                chantier = t
        if y >= Y_BANDEAUX or (x >= 189 and y >= 88):
            sh._element.getparent().remove(sh._element)
    if not critere or not chantier:
        raise ValueError("critere / chantier introuvables")
    return critere, chantier


def _notes(s, critere, chantier, retire=""):
    ancien = s.notes_slide.notes_text_frame.text.strip() if s.has_notes_slide else ""
    bloc = (
        "Critère observable (retiré de la slide)" + NB + ": " + critere + "\n"
        "Chantier (retiré de la slide)" + NB + ": " + chantier
    )
    if retire:
        bloc += "\n" + retire
    s.notes_slide.notes_text_frame.text = (ancien + "\n\n" if ancien else "") + bloc


def _navy(carte):
    carte.fill.solid()
    carte.fill.fore_color.rgb = NAVY
    carte.line.fill.background()


# ------------------------------------------------------------------------------------------------ conviction 10
ENTETES = [("DoR", "definition of ready"), ("Qualifier", "valeur, faisabilité, charge"), ("Automatiser", "demandes récurrentes")]
LIGNE_SANS = [
    "Un seul point d'entrée" + NB + "; critères d'entrée" + NB + ": problème, valeur, indicateur.",
    "Une grille explicite" + NB + "; au-delà d'un seuil de charge, un ROI est demandé.",
    "Statut visible" + NB + "; demandes récurrentes en self-service.",
]
LIGNE_AVEC = [
    "L'IA contrôle la complétude de la demande au regard de la DoR.",
    "Qualification par l'IA" + NB + ": elle classe et oriente" + NB + "; l'équipe décide.",
    "L'IA propose d'automatiser les demandes récurrentes.",
]
DRAPEAU = "Option selon la maturité · IA gouvernée"


def conviction10(prs):
    s = deck_draw.slide_par_titre(prs, T_C10)
    critere, chantier = _retirer_corps_et_bandeaux(s)
    cw = 124.0
    gap = (LARG - 3 * cw) / 2
    xs = [X0 + k * (cw + gap) for k in range(3)]
    # 1. frise : trois etapes numerotees, lues sur les deux lignes
    for k, (nom, sous) in enumerate(ENTETES):
        carre_num_cyan(s, xs[k], 96, 26, k + 1, sz=13)
        tx(s, xs[k] + 33, 94, cw + gap - 38, 44, [[(nom, 14, True, NAVY)], [(sous, 11, False, NAVY)]], A.TOP)
        if k:
            chevron_sep(s, xs[k] - gap / 2 - 5, 101, 10, 16)
    # 2. deux lignes : SANS IA puis AVEC IA
    for (etiq, y_lab, cellules, drap) in (("SANS IA", 152, LIGNE_SANS, False), ("AVEC IA", 262, LIGNE_AVEC, True)):
        pilule_entete(s, X0, y_lab, 76, 20, etiq, NAVY, sz=11)
        if drap:
            forme(s, S.ROUNDED_RECTANGLE, X0 + 86, y_lab, 250, 20, PANEL, None, adj=0.5)
            tx(s, X0 + 86, y_lab, 250, 20, [[(DRAPEAU, 11, False, NAVY)]], A.MIDDLE, P.CENTER)
        for k, texte in enumerate(cellules):
            y = y_lab + 24
            accent = drap and k == 1
            carte = carte_diag(s, xs[k], y, cw, 72, adj=0.14)
            if accent:
                _navy(carte)
            tx(s, xs[k] + 6, y, cw - 12, 72, [[(texte, 11, False, BLANC if accent else NAVY)]], A.MIDDLE)
            if k:
                chevron_sep(s, xs[k] - gap / 2 - 5, y + 28, 10, 16)
    _notes(s, critere, chantier)


# ------------------------------------------------------------------------------------------------ conviction 11
MESURER = ("Mesurer", "l'écart entre le SLA et le service vécu")
MONTRER = ("Montrer", "à rythme régulier, les écarts et la charge de RUN")
EN_TETE = ("Ce que mesure le SLA", "Ce que vit le consommateur", "Ce que nous suivons")
LIGNES = [
    ("Disponibilité du service", "Une demande qui attend, même quand le service est « vert »", "Objectif de service publié par capacité"),
    ("Incidents clos dans le délai", "Le même incident qui revient", "Taux d'incidents récurrents"),
    ("Tickets traités", "Du temps passé à subir plutôt qu'à améliorer", "Part de RUN subi et maîtrisé"),
]
COLS = ((X0, 108.0), (X0 + 108.0, 158.0), (X0 + 266.0, LARG - 266.0))


def _carte_etape(s, x, y, w, h, nom, sous, accent):
    carte = carte_diag(s, x, y, w, h, adj=0.14)
    if accent:
        _navy(carte)
    col = BLANC if accent else NAVY
    tx(s, x + 12, y + 8, w - 24, 20, [[(nom, 15, True, col)]], A.MIDDLE)
    tx(s, x + 12, y + 30, w - 24, h - 34, [[(sous, 11, False, col)]], A.TOP)


def conviction11(prs):
    s = deck_draw.slide_par_titre(prs, T_C11)
    critere, chantier = _retirer_corps_et_bandeaux(s)
    # boucle Mesurer <-> Montrer, en continu
    _carte_etape(s, X0, 94, 150, 78, *MESURER, accent=True)
    _carte_etape(s, X1 - 150, 94, 150, 78, *MONTRER, accent=False)
    cx = (X0 + X1) / 2
    forme(s, S.OVAL, cx - 24, 99, 48, 48, BLANC, NAVY, lw=1.25)
    for rot in (0, 180):
        fl = forme(s, S.CIRCULAR_ARROW, cx - 17, 106, 34, 34, CYAN, NAVY, lw=1)
        fl.rotation = rot
    tx(s, cx - 45, 153, 90, 16, [[("en continu", 11, True, NAVY)]], A.MIDDLE, P.CENTER)
    # contraste SLA / service vecu
    y0, h_tete, h_ligne = 180, 32, 48
    forme(s, S.ROUNDED_RECTANGLE, X0, y0, LARG, h_tete, CYAN, None, adj=0.5)
    for (x, w), titre in zip(COLS, EN_TETE, strict=True):
        tx(s, x + 10, y0, w - 14, h_tete, [[(titre, 11, True, NAVY)]], A.MIDDLE)
    for k, ligne in enumerate(LIGNES):
        y = y0 + h_tete + 4 + k * h_ligne
        if k % 2 == 0:
            forme(s, S.RECTANGLE, X0, y, LARG, h_ligne, PANEL, None)
        for j, ((x, w), texte) in enumerate(zip(COLS, ligne, strict=True)):
            tx(s, x + 10, y, w - 14, h_ligne, [[(texte, 11, j == 2, NAVY)]], A.MIDDLE)
    _notes(s, critere, chantier)


def _ids():
    prs = Presentation(deck_base.resoudre_base(BASE))
    return [f"id:{deck_draw.slide_par_titre(prs, t).slide_id}" for t in TITRES]


_I = dict(zip(TITRES, _ids(), strict=True))
ETAPES = [
    {"declarer": [_I[T_C10]], "f": conviction10, "nouvelles_max": 0, "nom": "conviction 10 : flux d'entree, bandeaux retires, frise recomposee"},
    {"declarer": [_I[T_C11]], "f": conviction11, "nouvelles_max": 0, "nom": "conviction 11 : boucle et tableau, bandeaux retires"},
]
