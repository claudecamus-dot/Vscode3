"""Delta V40 (base V39) : delta maitre, contenu des slides de conviction (propositions P de l'analyse de contenu) et conviction 13 avec ou sans IA.

j : convictions 1, 7, 8, 9 (slides 10, 13-15) ; k : convictions 10 a 13 (slides 16-19), dont le tableau SANS IA / AVEC IA des modeles d'organisation
"""
import delta_V40j
import delta_V40k

BASE = "V39"
NOTE = "V40 : contenu des convictions resserre, conviction 13 avec ou sans IA"
LOTS = [delta_V40j, delta_V40k]
OPS = [op for lot in LOTS for op in lot.OPS]
ETAPES = [etape for lot in LOTS for etape in lot.ETAPES]
