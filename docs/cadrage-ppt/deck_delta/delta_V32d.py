"""Delta V32d (base V31) : une slide d'illustration dans « Démarche détaillée » (la grille d'évaluation à cinq piliers, du mode produit à l'agentic).

- Nouvelle slide juste apres « De la douleur au produit : une mission pilote de bout en bout », sur le gabarit de cette slide (titre, surtitre, navigation, pied conserves) ;
- forme de la reference Vscode8 (slide 33) dans le vocabulaire V9 : bandeau-message, deux cadres « ILLUSTRATION » (les cinq piliers ; une question et ses quatre niveaux de reponse),
  trois cartes en pied a barre d'accent ; la grille est un instrument de LECTURE du diagnostic : ni score, ni pourcentage, ni donnee client ;
- les surtitres du chapitre passent de « n/10 » a « n/11 » (la nouvelle slide est 3/11).
Source des mots de la grille (lecture seule) : Grille-Assessment-Agile-V3.2-IA-Agentic-Complet.xlsx (VSCode1), onglets « Piliers et Objectifs Grille » et « Questions IA et Agentic ».
Usage (depuis docs/cadrage-ppt/) : py deck_delta/deck.py delta_V32d --base V31 --sortie C:/tmp/deck-v32-d/V32d.pptx
"""
import re

import deck_base
import deck_draw
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
    forme,
    pilule_entete,
    tx,
)
from forme_v26 import vider
from pptx import Presentation
from pptx.enum.text import MSO_ANCHOR as A

BASE = "V31"
NOTE = "V32d : slide d'illustration de la grille a cinq piliers dans Demarche detaillee (3/11) ; surtitres du chapitre n/10 -> n/11"
OPS = []

NB = "\u00a0"
T_APRES = "De la douleur au produit : une mission pilote de bout en bout"
T_NEUVE = "Le diagnostic s'appuie sur cinq piliers, du mode produit à l'agentic"
KICKER = re.compile(r"^05 · DÉMARCHE DÉTAILLÉE · \d+/\d+$")

BANDEAU = ("La grille cadre le diagnostic de l'Assessment flash" + NB + ":",
           " elle lit où en est le client sur chaque pilier et nourrit le choix du pilote" + NB + "; le client décide.")

# piliers de l'onglet « Piliers et Objectifs Grille » : nom, trois mots-cles tires des objectifs
PILIERS = [
    ("Équipe produit", "Backlog · Fonctionnement en équipe · Valeur"),
    ("Excellence technique", "Ingénierie et testing · DevOps · Qualité"),
    ("Culture (de l'entreprise) agile", "Rôles · Leadership · Ressources humaines"),
    ("Agilité à l'échelle", "Vision · Fonctionnement · Gouvernance"),
    ("IA, agentic et organisation augmentée", "Adoption de l'IA · Agentic Readiness · AgentOps"),
]
# onglet « Questions IA et Agentic », question 1 ; niveaux « choix 0 » a « choix 3 » (raccourcis par « … » seulement)
QUESTION = "Les collaborateurs maîtrisent-ils les concepts et usages de l'IA" + NB + "?"
NIVEAUX = [
    "Je ne sais pas ou aucune sensibilisation à l'IA n'a été réalisée.",
    "Les collaborateurs connaissent les principes généraux de l'IA générative et ses limites.",
    "En plus du choix 1, les collaborateurs utilisent des outils IA dans leurs activités…",
    "En plus du choix 2, les équipes développent une expertise IA, forment leurs pairs…",
]
CARTES = [
    ("Mêmes critères", "pour toutes les équipes"),
    ("Forces et points d'attention", "rendus explicites, sans score"),
    ("Le client décide", "du pilote, au vu du diagnostic"),
]
SOURCE = "Source" + NB + ": Grille d'évaluation OCTO — Assessment Agile V3.2, volet IA et agentic. Exemple illustratif, aucune donnée client."


def _cadre(s, x, titre):
    forme(s, S.ROUNDED_RECTANGLE, x, 124, 300 if x < 100 else 302, 186, PANEL, None, adj=0.05)
    pilule_entete(s, x + 8, 130, 88, 16, "ILLUSTRATION", NAVY, sz=9)
    tx(s, x + 104, 130, 190, 16, [[(titre, 11, True, NAVY)]], A.MIDDLE)


def _piliers(s):
    _cadre(s, 45, "Cinq piliers, leurs objectifs")
    for k, (nom, mots) in enumerate(PILIERS):
        y = 152 + k * 31.2
        carte_diag(s, 53, y, 284, 28, adj=0.4)
        carre_num_cyan(s, 58, y + 4, 20, k + 1, sz=10)
        tx(s, 86, y, 245, 28, [[(nom, 11, True, NAVY)], [(mots, 10.5, False, SLATE)]], A.MIDDLE)


def _echelle(s):
    _cadre(s, 357, "Une question du pilier IA")
    tx(s, 367, 150, 282, 28, [[("«" + NB + QUESTION + NB + "»", 11, True, NAVY)]], A.TOP)
    for k, texte in enumerate(NIVEAUX):
        y = 184 + k * 31
        carte_diag(s, 365, y, 286, 27, adj=0.4)
        carre_num_cyan(s, 369, y + 3.5, 20, k, sz=10)
        tx(s, 396, y, 250, 27, [[(texte, 10.5, False, NAVY)]], A.MIDDLE)


def _pied(s):
    for k, (claim, ligne) in enumerate(CARTES):
        x = 45 + k * 208
        carte_diag(s, x, 318, 198, 40, adj=0.15)
        forme(s, S.ROUNDED_RECTANGLE, x + 9, 326, 4, 24, CYAN, None, adj=0.5)
        tx(s, x + 21, 318, 172, 40, [[(claim, 11, True, NAVY)], [(ligne, 10.5, False, SLATE)]], A.MIDDLE)


def _renumeroter(prs):
    """« 05 · DÉMARCHE DÉTAILLÉE · n/N » : n dans l'ordre des slides, N = nombre de slides du chapitre ; ne reecrit que ce qui differe."""
    kickers = [sh for s in prs.slides for sh in s.shapes if sh.has_text_frame and KICKER.match(sh.text_frame.text)]
    n = len(kickers)
    for i, sh in enumerate(kickers, 1):
        voulu = f"05 · DÉMARCHE DÉTAILLÉE · {i}/{n}"
        if sh.text_frame.text != voulu:
            deck_draw.set_run(sh, voulu)


def illustration(prs):
    core = deck_base.core()
    modele = deck_draw.slide_par_titre(prs, T_APRES)
    rang = list(prs.slides).index(modele)
    s = core.copier_slide(prs, modele, index=rang + 1)
    ext = deck_draw._sections(prs)  # copier_slide ne met pas a jour les sections p14 : la nouvelle slide rejoint celle de sa reference
    if ext is not None:
        deck_draw._placer_dans_section(ext, deck_draw.id_de(prs, modele), deck_draw.id_de(prs, s))
    vider(s)
    deck_draw.set_run(s.shapes.title, T_NEUVE)
    kicker = next(sh for sh in s.shapes if sh.has_text_frame and KICKER.match(sh.text_frame.text))
    deck_draw.set_run(kicker, "05 · DÉMARCHE DÉTAILLÉE · 3/11")
    forme(s, S.ROUNDED_RECTANGLE, 45, 86, 614, 32, BLANC, LINE, adj=0.2, lw=0.75)  # blanc a bord LINE : PALE (EBFAFB) est deja hors charte sur la V31
    forme(s, S.ROUNDED_RECTANGLE, 53, 92, 4, 20, CYAN, None, adj=0.5)
    tx(s, 66, 86, 585, 32, [[(BANDEAU[0], 11.5, True, NAVY), (BANDEAU[1], 11.5, False, NAVY)]], A.MIDDLE)
    _piliers(s)
    _echelle(s)
    _pied(s)
    tx(s, 45, 364, 614, 12, [[(SOURCE, 9, False, SLATE)]], A.TOP)
    _renumeroter(prs)


def _ids():
    prs = Presentation(deck_base.resoudre_base(BASE))
    ids = [f"id:{s.slide_id}" for s in prs.slides if any(sh.has_text_frame and KICKER.match(sh.text_frame.text) for sh in s.shapes)]
    assert len(ids) == 10, f"{len(ids)} surtitres « DÉMARCHE DÉTAILLÉE » trouves, 10 attendus"
    return ids


ETAPES = [{"declarer": _ids(), "f": illustration, "nouvelles_max": 1, "nom": "slide d'illustration de la grille a cinq piliers + surtitres n/11"}]
