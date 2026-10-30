"""Delta V13 (base V12) : titres de la fiche reference ramenes sur une ligne (ils passaient sur deux lignes dans les cartes 1 et 3 de la V12)."""
import deck_base
import deck_draw
from pptx import Presentation

BASE = "V12"
NOTE = "V13 : titres de la fiche reference sur une ligne"
OPS = []
T_REFERENCE = "Fiche référence : un gabarit prêt à recevoir les références d'OCTO"


def titres(prs):
    formes = list(deck_draw.slide_par_titre(prs, T_REFERENCE).shapes)
    deck_draw.set_run(formes[9], "Contexte, enjeux et demande")
    deck_draw.set_run(formes[23], "Résultats et horizon estimé")


ETAPES = [{"declarer": [T_REFERENCE], "f": titres, "nouvelles_max": 0, "nom": "titres de la fiche reference"}]
