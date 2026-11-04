"""Delta V38a (base V37) : rang 7 « Six leviers au service de cinq résultats métier » — rééquilibrage des colonnes (lot a du chantier V38).

Demande : « revoir les slides 7, 11, 14, 17, 23 dans la façon dont les formes et le texte occupent l'espace ».
Colonne leviers resserrée à la largeur de son texte (316 -> 270 pt), colonne résultats élargie (265 -> 312 pt) pour que les noms
de résultats tiennent sur une ligne ; texte inchangé.
Usage (depuis docs/cadrage-ppt/) : py deck_delta/deck.py delta_V38a --base V37 --sortie C:/tmp/deck-v38-a/V38a.pptx --sans-rendu
"""
import deck_base
import deck_draw
from forme_ground import disque_picto
from forme_v9 import (
    BLANC,
    CYAN,
    NAVY,
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

BASE = "V37"
NOTE = "V38a : Six leviers, colonnes reequilibrees (leviers 270 pt, resultats 312 pt)"
OPS = []

NB = "\u00a0"
T_LEVIERS = "Six leviers au service de cinq résultats métier"

BANDEAU = [("Les constats que vous reconnaissez appellent ", False), ("des leviers que nous activons", True),
           (" selon le diagnostic" + NB + "; les résultats se mesurent. Liens principaux, à confirmer.", False)]
# (numero, nom, verbatim, pictogramme) : le pictogramme reprend celui du resultat lie quand le lien est direct (personnes, coche, jauge)
LEVIERS = [
    (1, "Expérience", "trop compliquée", "personnes"),
    (2, "Delivery", "nous sommes trop lents", "horloge"),
    (3, "Organisation", "tout remonte à l'équipe centrale", "grille"),
    (4, "Valeur", "on dépense sans savoir pourquoi", "jauge"),
    (5, "Fiabilité", "nos systèmes sont fragiles", "coche"),
    (6, "Stratégie", "un levier stratégique", "cible"),
]
RESULTATS = [
    ("Efficacité opérationnelle", "cycle", [1, 2, 3, 4]),
    ("Expérience utilisateur", "personnes", [1, 5]),
    ("Robustesse", "coche", [2, 5]),
    ("Maîtrise des coûts", "jauge", [4, 6]),
    ("Anticipation de l'IA", "ampoule", [2, 3, 6]),
]
ENTETE_G = "LES SIX LEVIERS"
AIDE_G = "numéros repris sur chaque résultat"
ENTETE_D = "LES CINQ RÉSULTATS MÉTIER"
NOTES = ("Mise en page" + NB + ": deux colonnes, des leviers vers les résultats ; le numéro du levier figure dans la carte de chaque résultat "
         "(liens principaux, à confirmer). Le libellé et le verbatim de chaque levier sont dans la colonne de gauche.")

Y0, HAUT = 140.0, 226.0          # zone des rangees
XG, WG = 45.0, 270.0              # colonne des leviers
XD, WD = 347.0, 312.25            # colonne des resultats (bord droit 659.25)


def leviers(prs):
    s = deck_draw.slide_par_titre(prs, T_LEVIERS)
    vider(s)
    forme(s, S.ROUNDED_RECTANGLE, 45, 74, 4, 28, CYAN, None, adj=0.5)
    tx(s, 57, 72, 602, 32, [[(t, 11.5, g, NAVY) for t, g in BANDEAU]], A.MIDDLE)
    # en-tetes de colonnes
    pilule_entete(s, XG, 118, 110, 17, ENTETE_G, SLATE, sz=10.5)
    tx(s, XG + 114, 118, WG - 114, 17, [[(AIDE_G, 10, False, SLATE)]], A.MIDDLE)
    pilule_entete(s, XD, 118, 168, 17, ENTETE_D, NAVY, sz=10.5)
    # six leviers
    h, gap = 34.0, (HAUT - 6 * 34.0) / 5
    for k, (num, nom, verbatim, genre) in enumerate(LEVIERS):
        y = Y0 + k * (h + gap)
        carte_diag(s, XG, y, WG, h, adj=0.22)
        disque_picto(s, XG + 22, y + h / 2, genre, d=28, goutte=False)
        carre_num_cyan(s, XG + 44, y + (h - 20) / 2, 20, num, sz=11)
        tx(s, XG + 72, y, WG - 80, h, [[(nom, 12, True, NAVY)], [("«" + NB + verbatim + NB + "»", 10.5, False, SLATE)]], A.MIDDLE)
    # sens de lecture : un seul chevron
    chevron_sep(s, XG + WG + 7.5, Y0 + HAUT / 2 - 17, 17, 34)
    # cinq resultats
    h, gap = 42.0, (HAUT - 5 * 42.0) / 4
    for k, (nom, genre, nums) in enumerate(RESULTATS):
        y = Y0 + k * (h + gap)
        forme(s, S.ROUND_2_DIAG_RECTANGLE, XD, y, WD, h, NAVY, None, adj=0.2)
        disque_picto(s, XD + 24, y + h / 2, genre, d=32, goutte=False)
        tx(s, XD + 48, y, WD - 48 - len(nums) * 24 - 12, h, [[(nom, 12, True, BLANC)]], A.MIDDLE)
        n = len(nums)
        x_fin = XD + WD - 12
        for j, num in enumerate(nums):
            carre_num_cyan(s, x_fin - (n - j) * 20 - (n - 1 - j) * 4, y + (h - 20) / 2, 20, num, sz=11)
    s.notes_slide.notes_text_frame.text = NOTES


def _ids():
    prs = Presentation(deck_base.resoudre_base(BASE))
    return [f"id:{deck_draw.slide_par_titre(prs, T_LEVIERS).slide_id}"]


ETAPES = [
    {"declarer": _ids(), "f": leviers, "nouvelles_max": 0, "nom": "six leviers : deux colonnes leviers -> resultats, numeros = lien"},
]

