"""Delta V38 (base V37) : delta maitre, occupation de l'espace des slides 7, 11, 14, 17 et 23 (texte inchange).

a : slide 7 (colonnes leviers / resultats reequilibrees) ; b : slide 11 (enonces de hauteur voisine, puces 12 pt)
c : slide 14 (cartes elargies, puces sur une colonne) ; d : slide 17 (puces, tableau SLA / vecu a colonnes egales)
e : slide 23 (grille de puces commune, bandeau Financement)
"""
import delta_V38a
import delta_V38b
import delta_V38c
import delta_V38d
import delta_V38e

BASE = "V37"
NOTE = "V38 : occupation de l'espace des slides 7, 11, 14, 17 et 23"
LOTS = [delta_V38a, delta_V38b, delta_V38c, delta_V38d, delta_V38e]
OPS = [op for lot in LOTS for op in lot.OPS]
ETAPES = [etape for lot in LOTS for etape in lot.ETAPES]
