"""Delta V34r (base V33) : cinq slides de « Démarche détaillée » refaites en plus lisible (lot r du chantier V34).

- Deux comités en parallèle : deux cartes à pictogramme rond sur un panneau gris, chevron « prépare les décisions » entre elles ;
- Ce que nous attendons de vous : deux panneaux (besoins / passage de relais), cartes numérotées, limite en bandeau navy ;
- Du pilote à l'autonomie : trois modes en cartes à pictogramme rond, flèche de progression (« OCTO porte le début » -> « le client prend la main ») ;
- L'IA est gouvernée : allégée (quatre dimensions, RACI humain / agent en frise, échelle d'autonomie) + UN encart « ILLUSTRATION » tiré de la grille agentic OCTO
  (evaluation-agentic-octo.pptx, slide 5, rangées Borner / Exécuter / Livrer et valider ; aucun nom client) ; le reste va dans les notes ;
- Risques et objections : cinq lignes numérotées objection -> réponse -> garde-fou, avec chevrons.
Aucune slide ajoutée ni retirée ; navigation, surtitres, pastilles d'état (PROPOSITION À VALIDER) et numéros de page conservés (vider() les garde).
Usage (depuis docs/cadrage-ppt/) : py deck_delta/deck.py delta_V34r --base V33 --sortie C:/tmp/deck-v34-r2/V34r.pptx
"""
import os
import sys

import deck_base
import deck_draw
from forme_ground import coche, disque_picto
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
from forme_v26 import vider
from pptx import Presentation
from pptx.enum.text import MSO_ANCHOR as A
from pptx.enum.text import PP_ALIGN as P

BASE = "V33"
NOTE = "V34r : comites, attentes et passage de relais, trois modes d'interaction, gouvernance de l'IA (encart grille agentic OCTO), risques et objections"
OPS = []

NB = "\u00a0"
T_COMITES = "Deux comités en parallèle : l'un suit l'exécution, l'autre décide"
T_ATTENTES = "Ce que nous attendons de vous, et comment nous passons la main"
T_MODES = "Du pilote à l'autonomie : trois modes d'interaction entre OCTO et le client"
T_IA = "L'IA est gouvernée : données, droits, validations et traçabilité"
T_RISQUES = "Risques et objections : ce que nous répondons, ce que nous mesurons"
TITRES = (T_COMITES, T_ATTENTES, T_MODES, T_IA, T_RISQUES)

IMAGE_IA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "encart_eval_V34r.png")  # evaluation-agentic-octo.pptx, slide 5, rendu 2560x1440, crop (146, 536, 1620, 568) : voir provenance_V34r.json
IMAGE_IA_ASPECT = 1620 / 568


def _tx_i(s, x, y, w, h, texte, sz=10, ancre=A.TOP, couleur=SLATE):
    """Texte italique (la zone de texte du kit n'a pas d'option italique)."""
    tb = tx(s, x, y, w, h, [[(texte, sz, False, couleur)]], ancre)
    for r in tb.text_frame.paragraphs[0].runs:
        r.font.italic = True
    return tb


def _notes(s, texte):
    s.notes_slide.notes_text_frame.text = texte


def _filet(s, x, y, w):
    forme(s, S.RECTANGLE, x, y, w, 0.75, LINE, None)


def _image(s, chemin, x, y, w, h, geom_adj=7000):
    """Image rognee a la forme d'un cadre round2DiagRect (la geometrie est clonee sur l'image : skill pptx-framed-image)."""
    scripts = os.path.join(deck_base.RACINE, ".claude", "skills", "pptx-framed-image", "scripts")
    if scripts not in sys.path:
        sys.path.append(scripts)
    from framed_image import place_image_in_frame, round2diag_geom
    pt = deck_draw.pt
    return place_image_in_frame(s, chemin, pt(x), pt(y), pt(w), pt(h), geom=round2diag_geom(geom_adj, 0))


# ================================================================ 1. Deux comites en parallele
COMITES = [
    ("Suivi opérationnel", "piloter l'exécution", "cycle",
     "Suivre l'avancement du pilote, lever les blocages, préparer les décisions du pilotage.",
     "fréquence" + NB + ": à valider",
     "Plan et risques à jour, décisions à prendre, éléments de preuve.",
     "Coach produit OCTO, propriétaires de produits et de capacités" + NB + "; noms et rôles à fournir."),
    ("Pilotage", "décider et passer à l'échelle", "cible",
     "Valider priorités et périmètre" + NB + "; décider go / no-go sur des preuves.",
     "fréquence" + NB + ": à valider",
     "Décisions formelles, arbitrages, résultat du jalon.",
     "Sponsor (DSI ou direction Infra) et coach OCTO" + NB + "; noms et rôles à fournir."),
]
NOTE_COMITES = "Une troisième instance, la revue de valeur, est décrite avec le calendrier du pilote."


def comites(prs):
    s = deck_draw.slide_par_titre(prs, T_COMITES)
    vider(s)
    forme(s, S.ROUNDED_RECTANGLE, 45, 96, 614, 246, PANEL, None, adj=0.04)
    for k, (nom, sous, genre, objectifs, freq, sorties, participants) in enumerate(COMITES):
        x = 55 if k == 0 else 361
        w = 288
        carte_diag(s, x, 118, w, 216, adj=0.1)
        disque_picto(s, x + w / 2, 118, genre, d=40, goutte=False)
        tx(s, x + 10, 142, w - 20, 16, [[(nom, 12.5, True, NAVY)]], A.MIDDLE, P.CENTER)
        tx(s, x + 10, 158, w - 20, 14, [[(sous, 10.5, False, SLATE)]], A.MIDDLE, P.CENTER)
        _filet(s, x + 10, 176, w - 20)
        lignes = [("OBJECTIFS", objectifs, 181, 42, False), ("FRÉQUENCE", freq, 227, 18, True),
                  ("SORTIES", sorties, 251, 28, False), ("PARTICIPANTS", participants, 285, 40, False)]
        for k2, (lab, texte, y, h, ital) in enumerate(lignes):
            if k2:
                _filet(s, x + 10, y - 4, w - 20)
            forme(s, S.ROUNDED_RECTANGLE, x + 10, y + 1, 78, 17, PANEL, None, adj=0.5)
            tx(s, x + 10, y + 1, 78, 17, [[(lab, 9.5, True, NAVY)]], A.MIDDLE, P.CENTER)
            if ital:
                _tx_i(s, x + 98, y, w - 108, h, texte, 10.5)
            else:
                tx(s, x + 98, y, w - 108, h, [[(texte, 10.5, False, NAVY)]], A.TOP)
    chevron_sep(s, 345, 219, 14, 24)
    _tx_i(s, 45, 347, 614, 14, NOTE_COMITES, 10)


# ================================================================ 2. Ce que nous attendons de vous
BESOINS = [
    "Un sponsor nommé et un périmètre prioritaire.",
    "Accès aux personnes et aux données autorisées.",
    "Une capacité dédiée aux décisions et à l'expérimentation.",
    "Des experts Infra, applicatifs et sécurité mobilisables.",
]
RELAIS = [
    "Le client lit et tient ses indicateurs.",
    "Il anime lui-même discovery et arbitrages.",
    "Des relais internes formés portent les rituels.",
]
NOTE_BESOINS = "Effort attendu côté client et dimensionnement" + NB + ": à compléter selon le périmètre."
NOTE_RELAIS = "Seuils chiffrés à fixer avec le client."
LIMITE = ("Limite" + NB + ":", " hors périmètre, toute action de l'IA en production.")


def _colonne(s, x, titre, genre, items):
    forme(s, S.ROUNDED_RECTANGLE, x, 106, 296, 246, PANEL, None, adj=0.04)
    disque_picto(s, x + 148, 106, genre, d=40, goutte=False)
    tx(s, x + 10, 130, 276, 18, [[(titre, 11, True, NAVY)]], A.MIDDLE, P.CENTER)
    for k, texte in enumerate(items):
        y = 154 + k * 42
        carte_diag(s, x + 10, y, 276, 36, adj=0.3)
        carre_num_cyan(s, x + 19, y + 8, 20, k + 1, sz=10)
        tx(s, x + 48, y, 232, 36, [[(texte, 10.5, False, NAVY)]], A.MIDDLE)


def attentes(prs):
    s = deck_draw.slide_par_titre(prs, T_ATTENTES)
    vider(s)
    _colonne(s, 45, "CE DONT NOUS AVONS BESOIN DE VOUS", "coche", BESOINS)
    _tx_i(s, 57, 326, 272, 24, NOTE_BESOINS, 10)
    _colonne(s, 363, "PASSAGE DE RELAIS", "fleche", RELAIS)
    _tx_i(s, 375, 284, 272, 14, NOTE_RELAIS, 10)
    forme(s, S.ROUND_2_DIAG_RECTANGLE, 373, 304, 276, 40, NAVY, None, adj=0.3)
    tx(s, 387, 304, 252, 40, [[(LIMITE[0], 11, True, BLANC), (LIMITE[1], 11, False, BLANC)]], A.MIDDLE)


# ================================================================ 3. Trois modes d'interaction
MODES = [
    ("Collaboration", "personnes",
     "Le coach OCTO et les équipes du client construisent le pilote ensemble, le temps d'apprendre à décider sur des faits.",
     "Conduit par" + NB + ": OCTO et le client ensemble.", "pilote"),
    ("Facilitation", "ampoule",
     "Les relais formés du client portent l'accompagnement" + NB + "; OCTO outille, conseille et reste en appui.",
     "Conduit par" + NB + ": le client, OCTO en appui.", "extension éventuelle"),
    ("X-as-a-Service", "grille",
     "L'équipe plateforme du client fournit la capacité comme un service" + NB + "; les consommateurs l'utilisent sans passer par OCTO.",
     "Conduit par" + NB + ": le client, avec ses relais.", "autonomie"),
]
NOTE_MODES = "Modes de Team Topologies" + NB + "; répartition à valider avec le client."


def modes(prs):
    s = deck_draw.slide_par_titre(prs, T_MODES)
    vider(s)
    pilule_entete(s, 45, 90, 195, 20, "OCTO PORTE LE DÉBUT", NAVY, sz=10)
    forme(s, S.PENTAGON, 254, 90, 405, 20, PANEL, None, adj=0.5)
    tx(s, 262, 90, 380, 20, [[("LE CLIENT PREND LA MAIN, PAS À PAS", 10, True, NAVY)]], A.MIDDLE, P.CENTER)
    for k, (nom, genre, corps, conduit, chip) in enumerate(MODES):
        x = 45 + k * 209.5
        carte_diag(s, x, 150, 195, 180, adj=0.1)
        carre_num_cyan(s, x + 10, 160, 20, k + 1, sz=10)
        disque_picto(s, x + 97.5, 150, genre, d=50, goutte=False)
        tx(s, x + 10, 180, 175, 18, [[(nom, 13, True, NAVY)]], A.MIDDLE, P.CENTER)
        tx(s, x + 12, 204, 164, 60, [[(corps, 11, False, NAVY)]], A.TOP)
        _filet(s, x + 12, 268, 171)
        tx(s, x + 12, 272, 171, 26, [[(conduit, 10.5, True, NAVY)]], A.TOP)
        forme(s, S.ROUNDED_RECTANGLE, x + 12, 303, 171, 19, PANEL, None, adj=0.5)
        tx(s, x + 12, 303, 171, 19, [[(chip, 10, False, NAVY)]], A.MIDDLE, P.CENTER)
        if k < 2:
            chevron_sep(s, x + 191, 228, 12, 22)
    _tx_i(s, 45, 338, 614, 14, NOTE_MODES, 10)


# ================================================================ 4. L'IA est gouvernee
GARDE_FOUS = ("Garde-fous" + NB + ":", " aucune donnée traitée sans accord · outils validés par le client · chaque sortie relue · sources tracées")
DIMENSIONS = [
    ("Données", ["Sources autorisées", "Classification", "Minimisation"]),
    ("Autorisations", ["Lecture seule par défaut", "Droits bornés par agent"]),
    ("Qualité", ["Évaluation avant usage", "Limites testées avant délégation"]),
    ("Supervision", ["Validation humaine", "Traçabilité", "Réversibilité et arrêt"]),
]
RACI = [("Préparer la sortie", "AGENT"), ("Valider", "HUMAIN"), ("Décider", "HUMAIN"), ("Répondre du résultat", "HUMAIN")]
AUTONOMIE = ["Assistance", "Recommandation", "Exécution bornée", "Action Infra validée"]
ENCART_IA_TITRE = "Borner le travail des agents"
ENCART_IA_LEGENDE = "Illustration" + NB + ": extrait de la grille d'évaluation agentic OCTO, anonymisé — à valider avant diffusion."
NOTES_IA = (
    "Retiré de la slide pour l'alléger (rien n'est abandonné)" + NB + ":\n"
    "- Phrase d'enjeu" + NB + ": « Deux faces" + NB + ": l'IA accélère le coach, et sa gouvernance chez le client reste humaine. » ; "
    "repère « Face 2 · gouvernance de l'IA chez le client (mécanisme générique) ».\n"
    "- Trois rappels de gouvernance" + NB + ":\n"
    "  Accountability humaine — un humain nommé répond de chaque sortie utilisée.\n"
    "  Gates humains — une validation humaine à chaque étape du processus.\n"
    "  Charte IA — un propriétaire nommé" + NB + "; hallucination et dérive revues à chaque revue.\n"
    "- Matrice RACI humain / agent (« plein = porte l'action »)" + NB + ": l'agent porte « Préparer la sortie »" + NB + "; l'humain porte « Valider », « Décider » et « Répondre du résultat »."
    " Elle est rendue en frise (quatre étapes, chacune marquée AGENT ou HUMAIN).\n"
    "Illustration" + NB + ": grille d'évaluation agentic OCTO (evaluation-agentic-octo.pptx, slide 5, rangées Borner / Exécuter / Livrer et valider), sans nom client."
)


def ia(prs):
    s = deck_draw.slide_par_titre(prs, T_IA)
    vider(s)
    # bandeau-message : les garde-fous
    forme(s, S.ROUNDED_RECTANGLE, 45, 86, 614, 28, BLANC, LINE, adj=0.2, lw=0.75)
    forme(s, S.ROUNDED_RECTANGLE, 53, 91, 4, 18, CYAN, None, adj=0.5)
    tx(s, 66, 86, 585, 28, [[(GARDE_FOUS[0], 11, True, NAVY), (GARDE_FOUS[1], 11, False, NAVY)]], A.MIDDLE)
    # quatre dimensions en 2 x 2
    for k, (nom, puces) in enumerate(DIMENSIONS):
        x = 45 + (k % 2) * 154
        y = 120 + (k // 2) * 82
        carte_diag(s, x, y, 146, 74, adj=0.12)
        carre_num_cyan(s, x + 8, y + 7, 18, k + 1, sz=10)
        tx(s, x + 32, y + 6, 108, 20, [[(nom, 11, True, NAVY)]], A.MIDDLE)
        tx(s, x + 10, y + 29, 132, 40, [[("– " + p, 10, False, NAVY)] for p in puces], A.TOP)
    # encart ILLUSTRATION (grille agentic OCTO)
    ex, ey, ew, eh = 357, 120, 302, 156
    forme(s, S.ROUNDED_RECTANGLE, ex, ey, ew, eh, PANEL, None, adj=0.05)
    pilule_entete(s, ex + 8, ey + 6, 88, 16, "ILLUSTRATION", NAVY, sz=9)
    tx(s, ex + 104, ey + 6, ew - 112, 16, [[(ENCART_IA_TITRE, 11, True, NAVY)]], A.MIDDLE)
    pw = ew - 16
    ph = pw / IMAGE_IA_ASPECT
    _image(s, IMAGE_IA, ex + 8, ey + 28, pw, ph)
    _tx_i(s, ex + 8, ey + 28 + ph + 3, pw, 20, ENCART_IA_LEGENDE, 9)
    # RACI humain / agent en frise
    tx(s, 45, 284, 190, 50, [[("RACI humain / agent (mécanisme générique)", 10.5, True, NAVY)],
                             [("l'agent prépare, l'humain décide et en répond", 10, False, SLATE)]], A.MIDDLE)
    for k, (verbe, qui) in enumerate(RACI):
        x = 245 + k * 105
        carte_diag(s, x, 284, 99, 50, adj=0.15)
        tx(s, x + 6, 287, 87, 26, [[(verbe, 10.5, True, NAVY)]], A.MIDDLE, P.CENTER)
        pilule_entete(s, x + 19, 315, 61, 14, qui, CYAN if qui == "AGENT" else NAVY, sz=9)
    # echelle d'autonomie
    tx(s, 45, 342, 130, 18, [[("AUTONOMIE DE L'IA", 10.5, True, NAVY)]], A.MIDDLE)
    for k, nom in enumerate(AUTONOMIE):
        x = 180 + k * 123
        dernier = k == len(AUTONOMIE) - 1
        forme(s, S.ROUNDED_RECTANGLE, x, 342, 110, 18, NAVY if dernier else PANEL, None, adj=0.5)
        tx(s, x + 3, 342, 104, 18, [[(nom, 9.5, True, BLANC if dernier else NAVY)]], A.MIDDLE, P.CENTER)
        if not dernier:
            chevron_sep(s, x + 114, 346, 6, 10)
    _notes(s, NOTES_IA)


# ================================================================ 5. Risques et objections
LIGNES_RISQUES = [
    ("«" + NB + "Nous ne pouvons pas ouvrir nos données" + NB + "»",
     "L'accès aux données autorisées est un prérequis d'entrée, vérifié avant le pilote" + NB + "; lecture seule par défaut.",
     "Premier go / no-go"),
    ("«" + NB + "Une plateforme de plus que personne n'utilise" + NB + "»",
     "Nous partons des consommateurs et de douleurs mesurées" + NB + "; l'adoption est suivie, pas supposée.",
     "Taux d'adoption, usages hors plateforme"),
    ("«" + NB + "Notre Run est critique" + NB + ": pas de risque" + NB + "»",
     "La criticité est un critère du diagnostic" + NB + "; le Run reste une responsabilité de service.",
     "SLO, incidents liés aux changements"),
    ("«" + NB + "L'IA est un risque pour nos données" + NB + "»",
     "Données, droits, qualité et supervision sont cadrés" + NB + "; les décisions restent humaines.",
     "Validation humaine, traçabilité"),
    ("«" + NB + "Quels gains garantissez-vous" + NB + "?" + NB + "»",
     "Aucun ROI promis" + NB + ": référence au T0, résultats au T1" + NB + "; la contribution de l'IA est vérifiée, jamais présumée.",
     "Écart entre T0 et T1"),
]
NOTE_RISQUES = "Objections formulées par nous, à confronter à celles de chaque client."


def risques(prs):
    s = deck_draw.slide_par_titre(prs, T_RISQUES)
    vider(s)
    pilule_entete(s, 45, 90, 176, 18, "OBJECTION ANTICIPÉE", NAVY, sz=9.5)
    for x, w, t in ((238, 244, "NOTRE RÉPONSE"), (502, 157, "GARDE-FOU SUIVI")):
        forme(s, S.ROUNDED_RECTANGLE, x, 90, w, 18, PANEL, None, adj=0.5)
        tx(s, x, 90, w, 18, [[(t, 9.5, True, NAVY)]], A.MIDDLE, P.CENTER)
    for k, (objection, reponse, garde) in enumerate(LIGNES_RISQUES):
        y = 114 + k * 47
        carre_num_cyan(s, 45, y + 11, 20, k + 1, sz=10)
        forme(s, S.ROUND_2_DIAG_RECTANGLE, 71, y, 150, 42, NAVY, None, adj=0.25)
        tx(s, 79, y, 136, 42, [[(objection, 10.5, True, BLANC)]], A.MIDDLE)
        chevron_sep(s, 224, y + 13, 10, 16)
        carte_diag(s, 238, y, 244, 42, adj=0.2)
        tx(s, 246, y, 230, 42, [[(reponse, 10, False, NAVY)]], A.MIDDLE)
        chevron_sep(s, 486, y + 13, 10, 16)
        forme(s, S.ROUNDED_RECTANGLE, 502, y, 157, 42, PANEL, None, adj=0.3)
        coche(s, 515, y + 21, 16)
        tx(s, 529, y, 124, 42, [[(garde, 10, True, NAVY)]], A.MIDDLE)
    _tx_i(s, 45, 352, 614, 12, NOTE_RISQUES, 10)


def _ids():
    prs = Presentation(deck_base.resoudre_base(BASE))
    return [f"id:{deck_draw.slide_par_titre(prs, t).slide_id}" for t in TITRES]


_I = dict(zip(TITRES, _ids(), strict=True))
ETAPES = [
    {"declarer": [_I[T_COMITES]], "f": comites, "nouvelles_max": 0, "nom": "deux comites : cartes a pictogramme rond"},
    {"declarer": [_I[T_ATTENTES]], "f": attentes, "nouvelles_max": 0, "nom": "attentes et passage de relais : deux panneaux"},
    {"declarer": [_I[T_MODES]], "f": modes, "nouvelles_max": 0, "nom": "trois modes d'interaction : cartes a pictogramme et fleche"},
    {"declarer": [_I[T_IA]], "f": ia, "nouvelles_max": 0, "nom": "gouvernance de l'IA allegee + encart grille agentic OCTO"},
    {"declarer": [_I[T_RISQUES]], "f": risques, "nouvelles_max": 0, "nom": "risques et objections : lignes numerotees objection -> reponse -> garde-fou"},
]
