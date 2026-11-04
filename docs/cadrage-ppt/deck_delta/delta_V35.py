"""Delta V35 (base V34) : delta maitre, empile les lots dans l'ordre (la navigation d'abord, puis les textes, puis l'aeration, puis les refontes de slides).

g  : bandeau de navigation a droite, surtitre et « PROPOSITION A VALIDER » retires, points de progression a gauche
t  : T0 / T1 retires hors de la slide de mesure (qui les definit)
sH : slide « Reussir » (dans la demarche supprime, phrase de sens par condition)
gA : espace libere par le surtitre rendu en air sur 30 slides
sA : slides 2, 9, 10 et titres 11, 12 ; sB : slides 6, 7 ; sC : convictions 7, 8, 9 ; sD : conviction 10 ; sE : conviction 11 ; sF : conviction 12 ;
sG : conviction 13 ; sI : slide « L'IA apporte au coach… »
"""
import delta_V35g
import delta_V35gA
import delta_V35sA
import delta_V35sB
import delta_V35sC
import delta_V35sD
import delta_V35sE
import delta_V35sF
import delta_V35sG
import delta_V35sH
import delta_V35sI
import delta_V35t

BASE = "V34"
NOTE = "V35 : navigation a droite, surtitre et PROPOSITION A VALIDER retires, T0/T1 expliques une seule fois, slides 2, 6, 7, 9 a 21 refaites, 30 slides aerees"
LOTS = [delta_V35g, delta_V35t, delta_V35sH, delta_V35gA, delta_V35sA, delta_V35sB, delta_V35sC, delta_V35sD, delta_V35sE, delta_V35sF, delta_V35sG, delta_V35sI]
OPS = [op for lot in LOTS for op in lot.OPS]
ETAPES = [etape for lot in LOTS for etape in lot.ETAPES]
