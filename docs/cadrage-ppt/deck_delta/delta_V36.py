"""Delta V36 (base V35) : delta maitre, empile les lots (regroupement par phase d'abord, puis refontes de slides, puis restyle des encarts).

vF : Demarche detaillee regroupee par phase (suiveur de phases), legende d'origine retiree de « De la douleur au produit »
vE : planning et livrables (slide 24, illustration supprimee) ; w : slide 23 sans zones duree et montant
vA : convictions 1 a 6 (+ ligne de lecture de la grille) ; vB : convictions 7 a 9 ; vC : convictions 10 et 11 ; vD : convictions 12 et 13 — zones critere observable / chantier retirees (vers les notes)
vG : encarts ILLUSTRATION sobres, legendes d'origine retirees (vers les notes)
"""
import delta_V36vA
import delta_V36vB
import delta_V36vC
import delta_V36vD
import delta_V36vE
import delta_V36vF
import delta_V36vG
import delta_V36w

BASE = "V35"
NOTE = "V36 : zones critere observable/chantier retirees, convictions recomposees, slides 23 et 24 allegees, Demarche detaillee regroupee par phase, encarts illustration sobres"
LOTS = [delta_V36vF, delta_V36vE, delta_V36w, delta_V36vA, delta_V36vB, delta_V36vC, delta_V36vD, delta_V36vG]
OPS = [op for lot in LOTS for op in lot.OPS]
ETAPES = [etape for lot in LOTS for etape in lot.ETAPES]
