"""Delta V38e (base V37) : slide « Deux temps d'engagement » : occupation de l'espace.

- les puces des trois cartes sont posees sur une grille commune de 4 rangees (pas 30 pt) : les rangees
  s'alignent d'une carte a l'autre et la carte Ancrage n'a plus de vide en bas ;
- les cartes sont raccourcies a leur contenu (bas a 336 pt) ;
- la ligne « Financement : ... » n'erre plus sous les cartes : elle est posee dans un bandeau gris pleine
  largeur (y 344 -> 364), qui ferme le corps jusqu'a la limite basse.
Aucun mot change.
Usage (depuis docs/cadrage-ppt/) : py deck_delta/deck.py delta_V38e --base V37 --sortie C:/tmp/deck-v38-e/V38e.pptx --sans-rendu
"""
import deck_base
import deck_draw
from forme_v9 import panneau_gris
from pptx import Presentation
from pptx.enum.text import MSO_ANCHOR
from pptx.util import Pt

BASE = "V37"
NOTE = "V38e : Deux temps d'engagement : grille de puces commune, cartes a la taille du contenu, bandeau Financement"
OPS = []

TITRE = "Deux temps d'engagement : diagnostiquer, puis expérimenter et déployer"
EMU = 12700
Y0 = 207.0
PAS = 30.0
BAS_CARTE = 336.0
BANDEAU_Y, BANDEAU_H = 344.0, 20.0


def _ids():
    return [f"id:{deck_draw.slide_par_titre(Presentation(deck_base.resoudre_base(BASE)), TITRE).slide_id}"]


def refondre(prs):
    s = deck_draw.slide_par_titre(prs, TITRE)
    cartes = sorted((x for x in s.shapes if "Diagonal" in x.name and x.height > 150 * EMU), key=lambda x: x.left)
    if len(cartes) != 3:
        raise ValueError(f"{len(cartes)} cartes au lieu de 3")
    for carte in cartes:
        x0, x1 = carte.left, carte.left + carte.width
        dans = [x for x in s.shapes if x0 <= x.left < x1 and x.top > 200 * EMU and x.top < 340 * EMU]
        puces = sorted((x for x in dans if x.has_text_frame and x.text_frame.text), key=lambda x: x.top)
        if len(puces) != 4:
            raise ValueError(f"{len(puces)} puces au lieu de 4")
        bornes = [p.top for p in puces] + [carte.top + carte.height]
        deltas = [int((Y0 + i * PAS) * EMU) - p.top for i, p in enumerate(puces)]
        for sh in dans:
            i = max(k for k in range(4) if sh.top >= bornes[k] - 2 * EMU)
            sh.top = sh.top + deltas[i]
        carte.height = int(BAS_CARTE * EMU) - carte.top
    fin = next(x for x in s.shapes if x.has_text_frame and x.text_frame.text.startswith("Financement"))
    panneau_gris(s, 45, BANDEAU_Y, 614.25, BANDEAU_H)
    fin.left, fin.top, fin.width, fin.height = 45 * EMU, int(BANDEAU_Y * EMU), int(614.25 * EMU), int(BANDEAU_H * EMU)
    tf = fin.text_frame
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left, tf.margin_top, tf.margin_bottom = Pt(10), 0, 0
    for r in (r for p in tf.paragraphs for r in p.runs):
        if r.font.size is None or r.font.size < Pt(11):
            r.font.size = Pt(11)


ETAPES = [{"declarer": _ids(), "f": refondre, "nouvelles_max": 0, "nom": "deux temps : grille de puces, bandeau Financement"}]
