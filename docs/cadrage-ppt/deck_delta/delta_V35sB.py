"""Delta V35sB (base V34, apres le lot g) : deux slides de « Contexte et enjeux » refaites (lot sB du chantier V35).

- Infra as a Product : AVANT / APRES en cartes a pictogramme, UN bandeau dedie « gain sur le RUN » (navy, a mesurer) cote APRES,
  la limite « le Run reste une responsabilite de service » en bloc separe a droite, et l'exemple (consommateur -> capacite -> resultats observes)
  seul sur un panneau gris en bas ;
- Six leviers : cinq cartes de resultat (numeros de leviers en petits carres) + UN encart navy « LES SIX LEVIERS » (six tuiles numerotees : nom en gras, verbatim en leger).
Aucune slide ajoutee ni retiree ; navigation, titres et numeros de page conserves (vider() les garde).
Usage (depuis docs/cadrage-ppt/) : py deck_delta/deck.py delta_V35sB --base C:/tmp/deck-v35/V35g.pptx --sortie C:/tmp/deck-v35-sB/V35sB.pptx --sans-rendu
"""
import deck_base
import deck_draw
from forme_ground import disque_picto
from forme_v9 import (
    BLANC,
    CYAN,
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
from forme_v26 import vider
from pptx import Presentation
from pptx.enum.text import MSO_ANCHOR as A
from pptx.enum.text import PP_ALIGN as P

BASE = "V34"
NOTE = "V35sB : Infra as a Product (gain sur le RUN, zone basse separee) et Six leviers (encart dedie aux leviers)"
OPS = []

NB = "\u00a0"
T_IAAP = "Infra as a Product : des capacités pensées pour leurs consommateurs"
T_LEVIERS = "Six leviers au service de cinq résultats métier"
TITRES = (T_IAAP, T_LEVIERS)


def _notes(s, texte):
    s.notes_slide.notes_text_frame.text = texte


def _tx_i(s, x, y, w, h, texte, sz=10, ancre=A.TOP, couleur=SLATE):
    tb = tx(s, x, y, w, h, [[(texte, sz, False, couleur)]], ancre)
    for r in tb.text_frame.paragraphs[0].runs:
        r.font.italic = True
    return tb


def _bandeau(s, y, runs, h=20, sz=12.5):
    forme(s, S.ROUNDED_RECTANGLE, 45, y + 2, 4, h - 4, CYAN, None, adj=0.5)
    tx(s, 57, y, 602, h, [runs], A.MIDDLE)


# ================================================================ 1. Infra as a Product
PHRASE = ("On ne transforme pas tout en produit" + NB + ": on pilote comme des produits ", "les capacités qui le justifient", ".")
AVANT_TITRE = "Un guichet saturé"
AVANT = ["Des délais qui s'allongent", "Un parcours illisible", "Des outils contournés", "Des coûts sans valeur visible"]
APRES = [
    ("Consommateurs", "personnes", "Partir des équipes qui consomment l'Infra et de leurs douleurs mesurées."),
    ("Catalogue", "classeurs", "Des capacités lisibles, en self-service quand c'est pertinent, avec un niveau de service explicite."),
    ("Ownership", "coche", "Un ownership clair par produit ou capacité" + NB + "; la forme du rôle dépend de l'organisation."),
    ("Mesure", "jauge", "Les décisions combinent expérience, usage, fiabilité, risques, coût et valeur."),
]
GAIN_LABEL = "GAIN SUR LE RUN"
GAIN_PILULE = "à mesurer"
GAIN_TEXTE = "Moins de RUN subi" + NB + ": de la capacité libérée, puis réallouée"
RUN_PILULE = "RUN"
RUN_TEXTE = "Le Run reste une responsabilité de service" + NB + ": tout ne devient pas produit."
EXEMPLE = "EXEMPLE" + NB + ": ENVIRONNEMENT APPLICATIF PRÊT À L'EMPLOI"
CHAINE = [("Consommateur", "Équipe de développement"), ("Capacité", "Environnement prêt à l'emploi"), ("Résultats observés", "Délai, autonomie, conformité")]
NOTES_IAAP = (
    "Mise en page" + NB + ": le gain sur le RUN (« Moins de RUN subi" + NB + ": de la capacité libérée, puis réallouée ») est un effet visé, à mesurer"
    " (indicateur « Capacité Run libérée, puis réallouée » ; aucun chiffre promis)."
)


def iaap(prs):
    s = deck_draw.slide_par_titre(prs, T_IAAP)
    vider(s)
    _bandeau(s, 66, [(PHRASE[0], 12.5, False, NAVY), (PHRASE[1], 12.5, True, NAVY), (PHRASE[2], 12.5, False, NAVY)], h=18)
    # en-tetes AVANT / APRES
    pilule_entete(s, 45, 87, 112, 17, "AVANT", SLATE, sz=10.5)
    pilule_entete(s, 177, 87, 482, 17, "APRÈS", NAVY, sz=10.5)
    # AVANT : le guichet sature
    forme(s, S.ROUNDED_RECTANGLE, 45, 106, 112, 152, PANEL, None, adj=0.06)
    tx(s, 53, 112, 98, 18, [[(AVANT_TITRE, 11, True, NAVY)]], A.MIDDLE)
    for k, t in enumerate(AVANT):
        y = 134 + k * 30
        forme(s, S.ROUNDED_RECTANGLE, 53, y, 96, 25, BLANC, None, adj=0.3)
        tx(s, 58, y, 88, 25, [[(t, 10, False, NAVY)]], A.MIDDLE)
    chevron_sep(s, 162, 172, 11, 20)
    # APRES : quatre cartes
    for k, (nom, genre, corps) in enumerate(APRES):
        x = 177 + (k % 2) * 244
        y = 106 + (k // 2) * 78
        carte_diag(s, x, y, 238, 74, adj=0.12)
        disque_picto(s, x + 23, y + 15, genre, d=26, goutte=False)
        tx(s, x + 42, y + 2, 188, 26, [[(nom, 12.5, True, NAVY)]], A.MIDDLE)
        tx(s, x + 12, y + 30, 218, 38, [[(corps, 10.5, False, NAVY)]], A.TOP)
    # RUN : le gain (navy, dedie) et la limite (bloc a part)
    ry, rh = 270, 33
    forme(s, S.ROUND_2_DIAG_RECTANGLE, 45, ry, 360, rh, NAVY, None, adj=0.25)
    disque_picto(s, 67, ry + rh / 2, "cycle", d=28, goutte=False)
    tx(s, 92, ry + 2, 140, 13, [[(GAIN_LABEL, 9.5, True, BLANC)]], A.MIDDLE)
    pilule_entete(s, 340, ry + 2, 55, 13, GAIN_PILULE, CYAN, sz=9.5)
    tx(s, 92, ry + 16, 308, 16, [[(GAIN_TEXTE, 11.5, True, BLANC)]], A.MIDDLE)
    forme(s, S.ROUNDED_RECTANGLE, 417, ry + 2, 242, rh - 4, BLANC, NAVY, adj=0.2, lw=1.0)
    pilule_entete(s, 427, ry + rh / 2 - 8, 40, 18, RUN_PILULE, NAVY, sz=10)
    tx(s, 477, ry + 2, 176, rh - 4, [[(RUN_TEXTE, 10.5, False, NAVY)]], A.MIDDLE)
    # exemple : panneau gris seul
    ey, eh = 315, 51
    forme(s, S.ROUNDED_RECTANGLE, 45, ey, 614, eh, PANEL, None, adj=0.12)
    tx(s, 57, ey + 4, 590, 11, [[(EXEMPLE, 10, True, SLATE)]], A.MIDDLE)
    bw, gap = 170, 40
    for k, (nom, sous) in enumerate(CHAINE):
        x = 57 + k * (bw + gap)
        forme(s, S.ROUNDED_RECTANGLE, x, ey + 22, bw, 24, NAVY if k < 2 else CYAN, None, adj=0.3)
        coul = BLANC if k < 2 else NAVY
        tx(s, x, ey + 22, bw, 24, [[(nom, 10.5, True, coul)], [(sous, 10, False, coul)]], A.MIDDLE, P.CENTER)
        if k < 2:
            chevron_sep(s, x + bw + 13.5, ey + 26, 13, 16)
    _notes(s, NOTES_IAAP)


# ================================================================ 2. Six leviers
BANDEAU = [("Les constats que vous reconnaissez appellent ", False), ("des leviers que nous activons", True),
           (" selon le diagnostic" + NB + "; les résultats se mesurent. Liens principaux, à confirmer.", False)]
RESULTATS = [
    ("Efficacité opérationnelle", "cycle", [1, 2, 3, 4]),
    ("Expérience utilisateur", "personnes", [1, 5]),
    ("Robustesse", "coche", [2, 5]),
    ("Maîtrise des coûts", "jauge", [4, 6]),
    ("Anticipation de l'IA", "ampoule", [2, 3, 6]),
]
LEVIERS = [
    (1, "Expérience", "trop compliquée"),
    (2, "Delivery", "nous sommes trop lents"),
    (3, "Organisation", "tout remonte à l'équipe centrale"),
    (4, "Valeur", "on dépense sans savoir pourquoi"),
    (5, "Fiabilité", "nos systèmes sont fragiles"),
    (6, "Stratégie", "un levier stratégique"),
]
LEVIERS_TITRE = "LES SIX LEVIERS"
LEVIERS_AIDE = "leurs numéros sont repris sur chaque carte de résultat"
NOTES_LEVIERS = "Mise en page" + NB + ": les numéros des leviers figurent sur chaque carte de résultat (liens principaux, à confirmer) ; leur libellé et leur verbatim sont dans l'encart « LES SIX LEVIERS »."


def leviers(prs):
    s = deck_draw.slide_par_titre(prs, T_LEVIERS)
    vider(s)
    forme(s, S.ROUNDED_RECTANGLE, 45, 82, 4, 28, CYAN, None, adj=0.5)
    tx(s, 57, 80, 602, 32, [[(t, 11.5, g, NAVY) for t, g in BANDEAU]], A.MIDDLE)
    # cinq cartes de resultat
    cw, gap = 116, 8.5
    for k, (nom, genre, nums) in enumerate(RESULTATS):
        x = 45 + k * (cw + gap)
        y = 134
        carte_diag(s, x, y, cw, 86, adj=0.12)
        disque_picto(s, x + cw / 2, y, genre, d=34, goutte=False)
        tx(s, x + 6, y + 21, cw - 12, 30, [[(nom, 11, True, NAVY)]], A.MIDDLE, P.CENTER)
        n = len(nums)
        x0 = x + (cw - (n * 20 + (n - 1) * 5)) / 2
        for j, num in enumerate(nums):
            carre_num_cyan(s, x0 + j * 25, y + 57, 20, num, sz=10.5)
    # encart dedie aux leviers
    py_, ph = 232, 134
    forme(s, S.ROUNDED_RECTANGLE, 45, py_, 614, ph, NAVY, None, adj=0.06)
    pilule_entete(s, 57, py_ + 9, 118, 19, LEVIERS_TITRE, CYAN, sz=10.5)
    tx(s, 186, py_ + 9, 460, 19, [[(LEVIERS_AIDE, 10.5, False, BLANC)]], A.MIDDLE)
    tw, th = 292, 29
    for k, (num, nom, verbatim) in enumerate(LEVIERS):
        x = 57 + (k // 3) * (tw + 6)
        y = py_ + 36 + (k % 3) * (th + 5)
        carte_diag(s, x, y, tw, th, adj=0.25)
        carre_num_cyan(s, x + 6, y + 4.5, 20, num, sz=10.5)
        tx(s, x + 34, y, tw - 40, th, [[(nom, 11.5, True, NAVY), ("  «" + NB + verbatim + NB + "»", 10.5, False, SLATE)]], A.MIDDLE)
    _notes(s, NOTES_LEVIERS)


def _ids():
    prs = Presentation(deck_base.resoudre_base(BASE))
    return [f"id:{deck_draw.slide_par_titre(prs, t).slide_id}" for t in TITRES]


_I = dict(zip(TITRES, _ids(), strict=True))
ETAPES = [
    {"declarer": [_I[T_LEVIERS]], "f": leviers, "nouvelles_max": 0, "nom": "six leviers : encart navy dedie + cinq cartes de resultat"},
    {"declarer": [_I[T_IAAP]], "f": iaap, "nouvelles_max": 0, "nom": "Infra as a Product : gain sur le RUN, limite et exemple separes"},
]
