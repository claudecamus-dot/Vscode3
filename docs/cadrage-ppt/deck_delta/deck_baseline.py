"""Baseline figee des defauts geometriques du dernier livrable (port adapte de Vscode8 `tests/test_garde_livrable.py`).

Cle d'un defaut = (genre, constat SANS le numero de slide) : une renumerotation ne fait pas sortir un defaut connu de la baseline.
Le fichier `charte/baseline_defauts.json` porte la version mesuree et les cles (avec leur nombre). Un defaut en plus = regression ;
un defaut en moins = dette payee, a retirer en refigeant (`py deck_baseline.py --figer`).
Usage (depuis docs/cadrage-ppt/deck_delta/) : py deck_baseline.py --figer   (mesure le dernier livrable et ecrit la baseline)
"""
import collections
import json
import os
import re
import sys

import deck_base
import deck_garde_rendu
from pptx import Presentation

FICHIER = os.path.join(deck_base.RACINE, "charte", "baseline_defauts.json")
_SLIDE = re.compile(r"^slide \d+: ")


def cles(prs):
    """Counter {(genre, constat sans numero de slide): nombre}."""
    return collections.Counter((genre, _SLIDE.sub("", detail)) for genre, detail in deck_garde_rendu.detecter_defauts(prs))


def charger(chemin=FICHIER):
    with open(chemin, encoding="utf8") as f:
        d = json.load(f)
    return d["version"], collections.Counter({(g, c): n for g, c, n in d["defauts"]})


def comparer(mesures, baseline):
    """(nouveaux, disparus) : listes de cles, repetees selon l'ecart de comptage."""
    nouveaux = sorted((mesures - baseline).elements())
    disparus = sorted((baseline - mesures).elements())
    return nouveaux, disparus


def figer(chemin_pptx, version, fichier=FICHIER):
    mesures = cles(Presentation(str(chemin_pptx)))
    donnees = {"version": version, "defauts": [[g, c, n] for (g, c), n in sorted(mesures.items())]}
    with open(fichier, "w", encoding="utf8") as f:
        json.dump(donnees, f, ensure_ascii=False, indent=1)
    return sum(mesures.values())


if __name__ == "__main__":
    if "--figer" not in sys.argv:
        sys.exit(__doc__)
    chemin, n = deck_base.dernier_livrable()
    print(f"baseline figee sur la V{n} : {figer(chemin, n)} defaut(s) -> {FICHIER}")
