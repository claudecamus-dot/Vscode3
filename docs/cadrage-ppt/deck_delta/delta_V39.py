"""Delta V39 (base V38) : delta maitre, occupation de l'espace et delimitation des groupes d'idees (texte inchange).

h : convictions 1, 7, 8, 9 (slides 10, 13-15) ; i : convictions 10 a 13 (slides 16-19) — goutte reduite 56 pt, contenu pleine largeur (arbitrage utilisateur)
f : slides 28, 30, 36 (panneaux d'illustration, groupe RACI / autonomie encadre) ; g : slides 3 (sommaire 3 + 2), 33, 34
delta_V39c / delta_V39d (ancienne regle, goutte pleine taille) sont remplaces par h et i et ne sont pas empiles.
"""
import delta_V39f
import delta_V39g
import delta_V39h

import delta_V39i

BASE = "V38"
NOTE = "V39 : convictions en goutte reduite pleine largeur, slides 3, 28, 30, 33, 34, 36 mieux remplies"
LOTS = [delta_V39g, delta_V39f, delta_V39h, delta_V39i]
OPS = [op for lot in LOTS for op in lot.OPS]
ETAPES = [etape for lot in LOTS for etape in lot.ETAPES]
