"""Delta V32 (base V31) : assemblage des quatre lots de la revue du 2026-11-03, dans cet ordre.

- A (delta_V32a) : couverture (pastilles retirees, date), ouverture « demande / reponse », introduction des convictions, slide IA « cognitive acceleration » ;
- B (delta_V32b + alt3) : Guichet et Infra as a Product sur le vocabulaire de l'exemple de reference, Six leviers en variante 3 (cinq cartes-resultats) choisie par l'utilisateur ;
- D (delta_V32d) : slide d'illustration de la grille a cinq piliers dans « Demarche detaillee » (surtitres n/11) ;
- C (delta_V32c) : conviction 13 (modeles d'organisation), chapitre « Nos convictions » n/13, introduction « Treize » — appliquee APRES A, dont elle reprend la slide 9.
Les lots touchent des slides disjointes, sauf C sur la slide 9 et les surtitres des convictions (A l'a deja refaite : C la retrouve par texte).
Usage (depuis docs/cadrage-ppt/) : py deck_delta/deck.py delta_V32
"""
import delta_V32a
import delta_V32b
import delta_V32b_alt3
import delta_V32c
import delta_V32d

BASE = "V31"
NOTE = "V32 : couverture, ouverture, Guichet, Infra as a Product, Six leviers (cartes-resultats), introduction des convictions, conviction 13, slide IA, grille a cinq piliers"
OPS = []


def _lot_b(prs):
    delta_V32b.guichet(prs)
    delta_V32b.produit(prs)
    delta_V32b_alt3.leviers_alt3(prs)


_etape_b = dict(delta_V32b.ETAPES[0], f=_lot_b, nom="Guichet, Infra as a Product, Six leviers (cartes-resultats) : formes de l'exemple de reference")

ETAPES = [*delta_V32a.ETAPES, _etape_b, *delta_V32d.ETAPES, *delta_V32c.ETAPES]
