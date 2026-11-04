"""Delta V35sC (base V34, apres le lot g) : trois slides de convictions refaites sur le fond (lot sC du chantier V35).

- Conviction 7 (financer) : AVANT -> APRES en deux cartes (equipe, RUN) puis un encart « Produit ou composant » (enonce, plus de question) ;
- Conviction 8 (equipe produit) : DEUX types d'equipe cote a cote, sans IA / avec IA (option selon la maturite) ;
- Conviction 9 (instances) : trois instances en echelle numerotee COMOP -> COPIL -> comite d'investissement (budgets, trimestriel).
Chrome conserve : pilules de navigation, titre, pastilles de progression (y 70), filet (y 86), bloc pictogramme + pilule CONVICTION n a gauche,
bandeaux LE CRITERE OBSERVABLE / LE CHANTIER en bas. Seul le corps (x >= 185, 92 <= y <= 270) est reconstruit.
Usage (depuis docs/cadrage-ppt/) : py deck_delta/deck.py delta_V35sC --base C:/tmp/deck-v35/V35g.pptx --sortie C:/tmp/deck-v35-sC/V35sC.pptx --sans-rendu
"""
import deck_base
import deck_draw
from forme_ground import coche, trait
from forme_v9 import (
    BLANC,
    CYAN,
    LINE,
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
NOTE = "V35sC : convictions 7 (avant/apres, produit ou composant), 8 (deux types d'equipe, sans et avec IA) et 9 (COMOP, COPIL, comite d'investissement)"
OPS = []

NB = "\u00a0"
T_FINANCER = "Conviction 7 : financer des produits et des équipes stables"
T_EQUIPE = "Conviction 8 : une petite équipe produit qui construit et exploite"
T_INSTANCES = "Conviction 9 : trois instances, chacune avec sa décision"
TITRES = (T_FINANCER, T_EQUIPE, T_INSTANCES)

ZX, ZW = 190, 469  # zone du corps : x 190..659
EMU = 12700


def _notes(s, texte):
    s.notes_slide.notes_text_frame.text = texte


def _vider_corps(s):
    """Retire le corps (x >= 185 pt, 92 <= y, bas <= 270) : ni navigation, ni titre, ni pastilles (y 70), ni filet (y 86), ni bloc gauche, ni bandeaux (y >= 273)."""
    for sh in list(s.shapes):
        if sh.is_placeholder or sh.name.startswith("nav-"):
            continue
        if sh.left >= 185 * EMU and sh.top >= 92 * EMU and sh.top + sh.height <= 270 * EMU:
            sh._element.getparent().remove(sh._element)


def _puce(s, x, y, w, h, texte, sz=10.5, couleur=NAVY):
    coche(s, x + 6.5, y + 7, 13)
    tx(s, x + 18, y, w - 18, h, [[(texte, sz, False, couleur)]], A.TOP)


# ================================================================ conviction 7
def financer(prs):
    s = deck_draw.slide_par_titre(prs, T_FINANCER)
    _vider_corps(s)
    cw, ch, cy = 224, 102, 102
    cartes = [
        (ZX, False, "AVANT", "Un budget par projet", "financé projet par projet",
         "dissoute à la fin du projet.", "transféré à d'autres équipes."),
        (ZX + ZW - cw, True, "APRÈS", "Une capacité par produit", "budget annuel rattaché au produit",
         "stable, elle construit et exploite.", "reste dans l'équipe qui construit."),
    ]
    for x, apres, pastille, titre, sous, equipe, run in cartes:
        if apres:
            forme(s, S.ROUND_2_DIAG_RECTANGLE, x, cy, cw, ch, NAVY, None, adj=0.1)
            ink, doux = BLANC, BLANC
        else:
            carte_diag(s, x, cy, cw, ch, adj=0.1)
            ink, doux = NAVY, SLATE
        pilule_entete(s, x + 14, cy - 8, 62, 16, pastille, CYAN if apres else PANEL, sz=9.5)
        tx(s, x + 14, cy + 14, cw - 28, 17, [[(titre, 12, True, ink)]], A.MIDDLE)
        tx(s, x + 14, cy + 31, cw - 28, 14, [[(sous, 10, False, doux)]], A.MIDDLE)
        forme(s, S.RECTANGLE, x + 14, cy + 50, cw - 28, 0.75, BLANC if apres else LINE, None)
        tx(s, x + 14, cy + 55, cw - 28, 18, [[("Équipe" + NB + ": ", 10.5, True, ink), (equipe, 10.5, False, ink)]], A.TOP)
        tx(s, x + 14, cy + 77, cw - 28, 18, [[("RUN" + NB + ": ", 10.5, True, ink), (run, 10.5, False, ink)]], A.TOP)
    chevron_sep(s, ZX + cw + 4, cy + 39, 13, 24)
    # produit ou composant : enonce, plus de question
    py_, ph = 222, 44
    forme(s, S.ROUNDED_RECTANGLE, ZX, py_, ZW, ph, PANEL, None, adj=0.15)
    pilule_entete(s, ZX + 14, py_ - 8, 152, 16, "PRODUIT OU COMPOSANT", NAVY, sz=9.5)
    coche(s, ZX + 21, py_ + 17, 13)
    tx(s, ZX + 34, py_ + 10, 190, 14, [[("Produits" + NB + ": ", 10.5, True, NAVY), ("Kubernetes, CI/CD, IAM", 10.5, False, NAVY)]], A.MIDDLE)
    tx(s, ZX + 247, py_ + 10, 215, 14, [[("Composants" + NB + ": ", 10.5, True, NAVY), ("VM, serveur, SAN", 10.5, False, NAVY)]], A.MIDDLE)
    tx(s, ZX + 14, py_ + 27, ZW - 28, 14, [[("Un produit a une offre, une valeur et des engagements.", 10.5, True, NAVY)]], A.MIDDLE)
    _notes(s, "Reformulé en V35 : la carte « Produit ou composant ? » posait une question ; elle devient un énoncé (« Un produit a une offre, une valeur et des engagements »)."
              " Phrase d'origine : « Puis-je décrire l'offre, la valeur, les engagements ? ». Les cartes « Un budget par projet » et « Une capacité par produit » passent en avant / après.")


# ================================================================ conviction 8
def equipe(prs):
    s = deck_draw.slide_par_titre(prs, T_EQUIPE)
    _vider_corps(s)
    cw, cy, ch = 227, 94, 172
    colonnes = [
        (ZX, 1, "Équipe produit", "SANS IA", PANEL, [
            ("Un binôme" + NB + ": responsable produit et référent technique. Pas un PO posé dans l'Infra.", 3),
            ("Une même équipe conçoit, livre et assure le service.", 2),
            ("Du temps de construction protégé.", 1),
            ("Demandes récurrentes automatisées, en self-service.", 2),
        ]),
        (ZX + ZW - cw, 2, "Équipe augmentée", "AVEC IA · OPTION SELON LA MATURITÉ", NAVY, [
            ("Mêmes rôles, plus des agents.", 1),
            ("Les agents préparent le travail récurrent et le diagnostic.", 2),
            ("L'IA prépare ; l'humain décide et en répond.", 2),
            ("Effets visés, à mesurer ; rien n'est promis.", 2),
        ]),
    ]
    for x, num, titre, chip, couleur, items in colonnes:
        carte_diag(s, x, cy, cw, ch, adj=0.08)
        carre_num_cyan(s, x + 10, cy + 6, 20, num, sz=10.5)
        tx(s, x + 38, cy + 6, cw - 48, 20, [[(titre, 12.5, True, NAVY)]], A.MIDDLE)
        forme(s, S.ROUNDED_RECTANGLE, x + 10, cy + 28, cw - 20, 16, couleur, None, adj=0.5)
        tx(s, x + 10, cy + 28, cw - 20, 16, [[(chip, 9.5, True, BLANC if couleur == NAVY else NAVY)]], A.MIDDLE, P.CENTER)
        y = cy + 49
        for t, lignes in items:
            h = 12.5 * lignes + 1
            _puce(s, x + 10, y, cw - 20, h, t, sz=10)
            y += h + (5 if num == 1 else 8)
    chevron_sep(s, ZX + cw + 1, cy + 74, 13, 24)
    _notes(s, "Reformulé en V35 : deux types d'équipe côte à côte, sans IA et avec IA (option selon la maturité, jamais un prérequis)."
              " Les trois cartes d'origine (« Construire et exploiter », « Un binôme porte le produit », « Moins de tickets ») sont réparties dans l'équipe sans IA."
              " Côté IA, les faits viennent de la slide « Infra agent-ready : une option selon la maturité, jamais un prérequis », de la conviction sur le RUN prêt (l'IA aide à diagnostiquer ; la décision reste humaine),"
              " de « L'IA est gouvernée » (l'agent prépare, l'humain décide et en répond) et de « Des agents augmentent le coach ; d'autres améliorent l'Infra du client » (exemples : triage de tickets, assistant documentaire)."
              " Aucun gain chiffré : effets visés, à mesurer. Retiré de la slide pour la tenir lisible : « chaque sortie est relue » (voir la slide de gouvernance de l'IA).")


# ================================================================ conviction 9
INSTANCES = [
    ("COMOP", "comité opérationnel", "ajustements, risques, escalades", "équipe, coach, relais client", "cadence à fixer avec vous"),
    ("COPIL", "comité de pilotage", "backlog et roadmap du produit", "responsable produit, métiers, équipe", "cadence à fixer avec vous"),
    ("Comité d'investissement", "revue trimestrielle des budgets", "arrêter, étendre ou pivoter une capacité", "sponsor, DSI, responsables produit", "cadence trimestrielle, à valider"),
]


def instances(prs):
    s = deck_draw.slide_par_titre(prs, T_INSTANCES)
    _vider_corps(s)
    h, pas = 50, 56
    y0 = 98
    for k, (nom, sous, decide, avec, cadence) in enumerate(INSTANCES):
        y = y0 + k * pas
        carte_diag(s, ZX, y, ZW, h, adj=0.2)
        carre_num_cyan(s, ZX + 10, y + 15, 20, k + 1, sz=10.5)
        tx(s, ZX + 40, y + 4, 160, h - 8, [[(nom, 11.5, True, NAVY)], [(sous, 10, False, SLATE)]], A.MIDDLE)
        forme(s, S.RECTANGLE, ZX + 206, y + 9, 0.75, h - 18, LINE, None)
        tx(s, ZX + 216, y + 4, ZW - 226, h - 8,
           [[("Décide" + NB + ": ", 10.5, True, NAVY), (decide, 10.5, True, NAVY)],
            [("Avec" + NB + ": ", 10, True, NAVY), (avec, 10, False, NAVY)],
            [(cadence, 10, False, SLATE)]], A.MIDDLE)
    # colonne vertebrale : relie les trois numeros (de l'operationnel vers le plus haut)
    for k in range(2):
        trait(s, ZX + 20, y0 + k * pas + 35, ZX + 20, y0 + (k + 1) * pas + 15, 1.25)
    _notes(s, "Reformulé en V35 : trois instances, du plus proche du travail au plus haut. « Suivi d'exécution » devient le COMOP (comité opérationnel) ;"
              " « Revue produit » devient le COPIL (comité de pilotage), qui décide du backlog et de la roadmap du produit ;"
              " la décision sur le budget du produit, auparavant en revue produit, monte au comité d'investissement, qui revoit les budgets chaque trimestre."
              " Les cadences restent à fixer avec le client (COMOP, COPIL) ou à valider (comité d'investissement).")


def _ids():
    prs = Presentation(deck_base.resoudre_base(BASE))
    return [f"id:{deck_draw.slide_par_titre(prs, t).slide_id}" for t in TITRES]


_I = dict(zip(TITRES, _ids(), strict=True))
ETAPES = [
    {"declarer": [_I[T_FINANCER]], "f": financer, "nouvelles_max": 0, "nom": "conviction 7 : avant / apres + produit ou composant"},
    {"declarer": [_I[T_EQUIPE]], "f": equipe, "nouvelles_max": 0, "nom": "conviction 8 : deux types d'equipe, sans IA / avec IA"},
    {"declarer": [_I[T_INSTANCES]], "f": instances, "nouvelles_max": 0, "nom": "conviction 9 : COMOP, COPIL, comite d'investissement"},
]
