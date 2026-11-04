"""Delta V34 (base V33) : assemblage des quatre lots de la revue du 2026-11-03 (soir), dans cet ordre.

- a (delta_V34a) : suppression du chapitre « Notre approche » (3 slides), navigation a six pastilles, sommaire, numeros de chapitre, annexe des enjeux ;
- p (delta_V34p) : chapitre « Demarche generale » (Deux temps, Planning avec encart, Boucle) et Calendrier du pilote ;
- q (delta_V34q) : De la douleur au produit, Exemples de livrables 1/2 et 2/2 (encarts), Nous mesurons la valeur ;
- r (delta_V34r) : Deux comites, Ce que nous attendons de vous, Du pilote a l'autonomie, L'IA est gouvernee (encart), Risques et objections.
Les lots p, q, r ne touchent ni les pastilles de navigation ni les surtitres : a passe donc en premier, sans conflit. Les provenances des images sont dans provenance_V34{p,q,r}.json.
Usage (depuis docs/cadrage-ppt/) : py deck_delta/deck.py delta_V34
"""
import delta_V34a
import delta_V34p
import delta_V34q
import delta_V34r

BASE = "V33"
NOTE = "V34 : chapitre Notre approche supprime, Demarche generale et Demarche detaillee retravaillees (formes maison, encarts ILLUSTRATION)"
OPS = [*delta_V34a.OPS, *delta_V34p.OPS, *delta_V34q.OPS, *delta_V34r.OPS]
ETAPES = [*delta_V34a.ETAPES, *delta_V34p.ETAPES, *delta_V34q.ETAPES, *delta_V34r.ETAPES]
