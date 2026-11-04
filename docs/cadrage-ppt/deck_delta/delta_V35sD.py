"""Delta V35sD (base V34, apres le lot g) : « Conviction 10 » refaite autour de la gestion du flux d'entree (lot sD du chantier V35).

- Corps de la slide : une frise de trois etapes (DoR, qualifier, automatiser) lue deux fois, ligne « SANS IA » puis ligne « AVEC IA » ;
  un seul accent cyan (la qualification par l'IA), signalee comme option selon la maturite ;
- Bloc pictogramme + pilule « CONVICTION 10 », points de progression, filet cyan, pilules de navigation, titre : conserves tels quels (chrome) ;
- Bandeaux « LE CRITERE OBSERVABLE » / « LE CHANTIER » : texte elargi a la DoR, a l'automatisation et a la qualification assistee par l'IA ;
- Les phrases retirees du corps sont conservees dans les notes de la slide.
Aucune slide ajoutee ni retiree. Ne pas utiliser vider() : il supprimerait les points de progression et le filet (devenus chrome a gauche).
Usage (depuis docs/cadrage-ppt/) : py deck_delta/deck.py delta_V35sD --base C:/tmp/deck-v35/V35g.pptx --sortie C:/tmp/deck-v35-sD/V35sD.pptx --sans-rendu
"""
import deck_base
import deck_draw
from forme_v9 import (
    NAVY,
    PANEL,
    SLATE,
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

BASE = "V34"
NOTE = "V35sD : Conviction 10, flux d'entree sans IA / avec IA (DoR, qualification, automatisation)"
OPS = []

NB = "\u00a0"
T_C10 = "Conviction 10 : un flux d'entrée unique qui qualifie avant de servir"
TITRES = (T_C10,)

X_CORPS = 190          # a droite du bloc pictogramme + pilule (x 45..175)
X_FIN = 659.25
GAP = 14
LARGEUR = (X_FIN - X_CORPS - 2 * GAP) / 3
Y_ENTETE = 94
Y_LIGNE = (124, 196)   # haut de chaque ligne (pilule d'etiquette) ; les cartes sont 19 pt plus bas
H_CARTE = 48

ETAPES_ENTETE = [("DoR", "definition of ready"), ("Qualifier", "valeur, faisabilité, charge"), ("Automatiser", "demandes récurrentes")]
LIGNE_SANS = ("SANS IA", None, [
    "Un seul point d'entrée" + NB + "; critères d'entrée : problème, valeur, indicateur.",
    "Une grille explicite" + NB + "; au-delà d'un seuil de charge, un ROI est demandé.",
    "Statut visible" + NB + "; demandes récurrentes en self-service.",
])
LIGNE_AVEC = ("AVEC IA", "Option selon la maturité · IA gouvernée", [
    "L'IA contrôle la complétude de la demande au regard de la DoR.",
    "Qualification par l'IA" + NB + ": elle classe et oriente ; l'équipe décide.",
    "L'IA propose d'automatiser les demandes récurrentes.",
])
ACCENT = (1, 1)        # (ligne, colonne) : la qualification par l'IA, seul aplat cyan du corps

CRITERE = "Toute demande a une fiche, des critères d'entrée vérifiés (DoR) et un statut visibles" + NB + "; le délai de qualification est mesuré."
CHANTIER = ("Cartographier les flux entrants, fiche et DoR, grille de priorisation, demandes à automatiser, capacité répartie par décision"
            + NB + "; qualification par l'IA en option.")

NOTES = (
    "Texte retiré du corps de la slide (conservé ici)" + NB + ": Recevoir" + NB + ": un seul point d'entrée" + NB + "; une fiche" + NB + ": problème, valeur, indicateur. "
    "Qualifier" + NB + ": valeur, faisabilité et charge estimées avant d'engager l'équipe. "
    "Prioriser" + NB + ": une grille explicite" + NB + "; au-delà d'un seuil de charge, un ROI est demandé. "
    "Servir" + NB + ": statut visible" + NB + "; les demandes récurrentes passent en self-service. "
    "Ancien chantier" + NB + ": cartographier les flux entrants, fiche de demande standard, grille de priorisation, capacité répartie par décision. "
    "DoR" + NB + ": definition of ready, critères d'entrée d'une demande. "
    "La ligne « AVEC IA » est une option selon la maturité, jamais un prérequis" + NB + "; aucun gain n'est promis, à mesurer."
)


def _remplacer(sh, texte):
    runs = sh.text_frame.paragraphs[0].runs
    runs[0].text = texte
    for r in runs[1:]:
        r._r.getparent().remove(r._r)


def conviction10(prs):
    s = deck_draw.slide_par_titre(prs, T_C10)
    # 1. retirer l'ancien corps (frise Recevoir / Qualifier / Prioriser / Servir) : tout ce qui est a droite du bloc pictogramme, au-dessus des bandeaux
    for sh in list(s.shapes):
        if sh.left >= X_CORPS * 12700 - 12700 and 95 * 12700 <= sh.top < 270 * 12700:
            sh._element.getparent().remove(sh._element)
    # 2. entete : trois etapes numerotees, chevrons entre elles
    for k, (nom, sous) in enumerate(ETAPES_ENTETE):
        x = X_CORPS + k * (LARGEUR + GAP)
        carre_num_cyan(s, x, Y_ENTETE + 2, 20, k + 1, sz=10.5)
        tx(s, x + 27, Y_ENTETE - 2, LARGEUR - 27, 28, [[(nom, 11.5, True, NAVY)], [(sous, 10, False, SLATE)]], A.MIDDLE)
        if k:
            chevron_sep(s, x - GAP + 2, Y_ENTETE + 6, 10, 16)
    # 3. deux lignes : SANS IA puis AVEC IA
    for i, (etiq, drapeau, cellules) in enumerate((LIGNE_SANS, LIGNE_AVEC)):
        y = Y_LIGNE[i]
        pilule_entete(s, X_CORPS, y, 64, 16, etiq, NAVY, sz=10)
        if drapeau:
            forme(s, S.ROUNDED_RECTANGLE, X_CORPS + 72, y, 232, 16, PANEL, None, adj=0.5)
            tx(s, X_CORPS + 72, y, 232, 16, [[(drapeau, 10, False, NAVY)]], A.MIDDLE, P.CENTER)
        for k, texte in enumerate(cellules):
            x = X_CORPS + k * (LARGEUR + GAP)
            accent = (i, k) == ACCENT
            carte_diag(s, x, y + 19, LARGEUR, H_CARTE, accent=accent, adj=0.14)
            tx(s, x + 8, y + 19, LARGEUR - 16, H_CARTE, [[(texte, 10, False, NAVY)]], A.MIDDLE)
            if k:
                chevron_sep(s, x - GAP + 2, y + 19 + H_CARTE / 2 - 8, 10, 16)
    # 4. bandeaux critere / chantier : meme forme, texte elargi
    for sh in s.shapes:
        if not sh.has_text_frame:
            continue
        t = sh.text_frame.text
        if t.startswith("Toute demande a une fiche"):
            _remplacer(sh, CRITERE)
        elif t.startswith("Cartographier les flux"):
            _remplacer(sh, CHANTIER)
    s.notes_slide.notes_text_frame.text = NOTES


def _ids():
    prs = Presentation(deck_base.resoudre_base(BASE))
    return [f"id:{deck_draw.slide_par_titre(prs, t).slide_id}" for t in TITRES]


_I = dict(zip(TITRES, _ids(), strict=True))
ETAPES = [
    {"declarer": [_I[T_C10]], "f": conviction10, "nouvelles_max": 0, "nom": "conviction 10 : flux d'entree sans IA / avec IA (DoR, qualification, automatisation)"},
]
