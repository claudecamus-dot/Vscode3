"""Delta d'exemple pour deck.py : copier ce fichier en delta_V<N>.py, l'adapter, puis `py deck.py delta_V<N> --dry-run`.

Ops du core (pptx_deck_core.appliquer_delta) ; `slide` = TITRE EXACT et COMPLET de la slide (placeholder titre, sinon premiere forme texte), « id:N » ou rang :
  {"slide": "Titre exact", "op": "remplacer_texte", "ancien": "texte actuel", "nouveau": "nouveau texte"}
  {"slide": "Titre exact", "op": "geometrie", "forme": {"texte": "debut du texte de la forme", "y": 1234567}}   # EMU ; None = inchange
  {"slide": "Titre exact", "op": "deplacer", "position": 5}  |  {"slide": "Titre exact", "op": "supprimer"}  |  {"slide": "Titre exact", "op": "copier", "index": 10}
Un `remplacer_texte` SANS `slide` vise tout le deck : deck.py le developpe en une op ciblee par slide qui contient `ancien`.
Une balise [À CONFIRMER] / [À CALIBRER] / [À VALIDER] / [À SOURCER] n'est jamais comblee par une valeur inventee : la retirer exige `source` (origine de la valeur).
ETAPES : dessin libre sous garde (ici : ajouter une slide sur le gabarit d'un chapitre). Appliquees APRES les ops.

Cet exemple vise la V4 (`--base V4`) : les titres ci-dessous en sont tires. Sur une autre version, adapter les titres.
"""
import deck_base
import deck_draw

BASE = None  # None = dernier livrable ; « V4 » ; ou le chemin d'un .pptx
NOTE = "Exemple : un texte remplace, une geometrie retouchee, une slide ajoutee sur le gabarit du chapitre « Prochain pas »"

TITRE = "Le guichet Infra atteint ses limites et l'IA accentue la pression"

OPS = [
    # 1. remplacer un texte (le style du run est conserve)
    {"slide": TITRE, "op": "remplacer_texte", "ancien": "Un parcours illisible", "nouveau": "Un parcours peu lisible"},
    # 2. retoucher une geometrie (EMU) : descend la boite « Des outils contournes » d'environ 1,4 pt (valeur d'origine : 1901952)
    {"slide": TITRE, "op": "geometrie", "forme": {"texte": "Des outils contourn", "y": 1920240}},
]


def ajouter_chapitre(prs):
    """Ajoute, juste apres le chapitre « Prochain pas », une copie de ce chapitre (image et layout compris) avec un nouveau titre et un nouveau numero."""
    deck_draw.ajouter_sur_gabarit(deck_base.core(), prs, "Prochain pas", {"Prochain pas": "Chapitre ajouté (exemple)", "07": "07 bis"})


ETAPES = [{"declarer": [], "f": ajouter_chapitre, "nouvelles_max": 1, "nom": "ajouter un chapitre sur gabarit"}]
