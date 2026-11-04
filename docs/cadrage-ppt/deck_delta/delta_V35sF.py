"""Delta V35sF (base V34, apres le lot g) : conviction 12 « aucun produit livre sans RUN pret » refaite sur le fond (lot sF du chantier V35).

Demande : « la gestion du RUN a revoir au niveau du contenu » ; appui sur les notes RUN du projet Vscode6 (docs/run-ia : RUN Readiness Check,
douleurs du RUN, boucle post-mortem, niveaux d'autonomie de l'IA), generalisees : aucun nom client, aucun chiffre.
Nouveau corps (x >= 185, 92 <= y <= 270) :
- une frise Construire > Porte « RUN pret » > Exploiter > Apprendre (la porte en accent navy) ;
- la porte : quatre criteres numerotes, valides avant chaque mise en service (equipe, supervision, connaissance, budget) ;
- a droite, deux blocs nettement separes : « Apprendre » (post-mortem puis backlog) et « Avec IA, selon la maturite » (carte navy : l'IA aide, l'humain decide).
Chrome conserve : pilules de navigation, titre, pastilles de progression (y 70), filet (y 86), pictogramme + pilule CONVICTION 12 a gauche,
bandeaux LE CRITERE OBSERVABLE / LE CHANTIER en bas (textes inchanges).
Usage (depuis docs/cadrage-ppt/) : py deck_delta/deck.py delta_V35sF --base C:/tmp/deck-v35/V35g.pptx --sortie C:/tmp/deck-v35-sF/V35sF.pptx --sans-rendu
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

BASE = "V34"
NOTE = "V35sF : conviction 12 (RUN pret) : frise Construire > Porte > Exploiter > Apprendre, quatre criteres de la porte, bloc Apprendre, bloc Avec IA selon la maturite"
OPS = []

NB = "\u00a0"
T_RUN = "Conviction 12 : aucun produit livré sans RUN prêt"
TITRES = (T_RUN,)
EMU = 12700
ZX, ZW = 190, 469  # zone du corps : x 190..659

FRISE = [("Construire", 96, False), ("Porte" + NB + "« RUN" + NB + "prêt" + NB + "»", 142, True), ("Exploiter", 96, False), ("Apprendre", 96, False)]
CRITERES = [
    ("Équipe" + NB + ": ", "un propriétaire nommé, deux personnes capables par module."),
    ("Supervision" + NB + ": ", "alertes et astreinte définies."),
    ("Connaissance" + NB + ": ", "procédure d'incident documentée."),
    ("Budget" + NB + ": ", "RUN inscrit dans le business case."),
]
APPRENDRE = "Chaque incident majeur" + NB + ": un post-mortem, puis une action au backlog."
AVEC_IA = "L'IA aide à diagnostiquer et trier les incidents" + NB + "; l'humain décide, chaque sortie est relue et tracée."

NOTES = (
    "Reformulé en V35 (demande utilisateur : « la gestion du RUN à revoir au niveau du contenu », en s'appuyant sur les notes RUN de Vscode6)." + "\n"
    "Texte d'origine, conservé dans la logique : « La porte « RUN prêt » » (deux personnes capables par module ; supervision et astreinte définies ;"
    " budget RUN dans le business case ; procédure d'incident documentée) ; « La boucle d'apprentissage » (chaque incident majeur : un post-mortem,"
    " puis une action au backlog ; l'IA aide à diagnostiquer, la décision et la mise en œuvre restent humaines et tracées)."
    " Les bandeaux « Le critère observable » et « Le chantier » sont inchangés." + "\n"
    "Ajouts généralisés, sans nom client ni chiffre (source : notes RUN de Vscode6, docs/run-ia) :" + "\n"
    "- « un propriétaire nommé » : le contrôle de préparation au RUN demande un propriétaire par composant ;" + "\n"
    "- « trier les incidents » : qualification et déduplication des signaux, premier usage de l'IA en RUN ;" + "\n"
    "- « chaque sortie est relue » : même garde-fou que « L'IA est gouvernée » ; l'IA commence en lecture et préparation (autonomie à valider avec le client)." + "\n"
    "Critères du contrôle de préparation au RUN non repris sur la slide, à valider avec le client : architecture et flux critiques identifiés,"
    " tests sur les fonctions critiques, sécurité (secrets, droits, dépendances), dette connue, reprise possible sans l'équipe qui a construit, procédure de retour arrière."
)


def _notes(s, texte):
    s.notes_slide.notes_text_frame.text = texte


def _vider_corps(s):
    """Retire le corps (x >= 185 pt, 92 <= y, bas <= 270) : ni navigation, ni titre, ni pastilles (y 70), ni filet (y 86), ni bloc gauche, ni bandeaux (y >= 273)."""
    for sh in list(s.shapes):
        if sh.is_placeholder or sh.name.startswith("nav-"):
            continue
        if sh.left >= 185 * EMU and sh.top >= 92 * EMU and sh.top + sh.height <= 270 * EMU:
            sh._element.getparent().remove(sh._element)


def run_pret(prs):
    s = deck_draw.slide_par_titre(prs, T_RUN)
    _vider_corps(s)
    # frise : Construire > Porte « RUN pret » > Exploiter > Apprendre
    x = ZX
    for k, (nom, w, porte) in enumerate(FRISE):
        forme(s, S.ROUNDED_RECTANGLE, x, 98, w, 18, NAVY if porte else PANEL, None, adj=0.5)
        tx(s, x, 98, w, 18, [[(nom, 10, True, BLANC if porte else NAVY)]], A.MIDDLE, P.CENTER)
        x += w
        if k < len(FRISE) - 1:
            chevron_sep(s, x + 3, 101, 7, 12)
            x += 13
    # la porte : quatre criteres numerotes
    gx, gy, gw, gh = ZX, 130, 252, 132
    carte_diag(s, gx, gy, gw, gh, adj=0.08)
    pilule_entete(s, gx + 14, gy - 8, 224, 16, "4 CRITÈRES AVANT LA MISE EN SERVICE", NAVY, sz=9.5)
    for k, (label, texte) in enumerate(CRITERES):
        y = gy + 11 + k * 29
        carre_num_cyan(s, gx + 12, y + 5, 18, k + 1, sz=10)
        tx(s, gx + 38, y, gw - 48, 28, [[(label, 10.5, True, NAVY), (texte, 10.5, False, NAVY)]], A.MIDDLE)
    # a droite : Apprendre, puis Avec IA (carte navy, nettement separee)
    rx = ZX + gw + 10
    rw = ZX + ZW - rx
    forme(s, S.ROUNDED_RECTANGLE, rx, 130, rw, 50, PANEL, None, adj=0.12)
    pilule_entete(s, rx + 12, 122, 90, 16, "APPRENDRE", NAVY, sz=9.5)
    tx(s, rx + 12, 142, rw - 24, 36, [[(APPRENDRE, 10.5, False, NAVY)]], A.MIDDLE)
    forme(s, S.ROUND_2_DIAG_RECTANGLE, rx, 196, rw, 66, NAVY, None, adj=0.12)
    pilule_entete(s, rx + 12, 188, 170, 16, "AVEC IA · SELON LA MATURITÉ", CYAN, sz=9)
    tx(s, rx + 12, 208, rw - 24, 52, [[(AVEC_IA, 10.5, False, BLANC)]], A.MIDDLE)
    _notes(s, NOTES)


def _ids():
    prs = Presentation(deck_base.resoudre_base(BASE))
    return [f"id:{deck_draw.slide_par_titre(prs, t).slide_id}" for t in TITRES]


_I = dict(zip(TITRES, _ids(), strict=True))
ETAPES = [
    {"declarer": [_I[T_RUN]], "f": run_pret, "nouvelles_max": 0, "nom": "conviction 12 : porte RUN pret (4 criteres), apprendre, avec IA selon la maturite"},
]
