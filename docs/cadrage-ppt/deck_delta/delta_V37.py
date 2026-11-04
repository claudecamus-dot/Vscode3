"""Delta V37 (base V36) : delta maitre, empile les lots (suppression des Annexes d'abord, puis refontes de slides, puis retraits de doublons).

zA : chapitre Annexes supprime (13 slides), navigation et sommaire recales
wA : slide 7 (leviers -> resultats) ; wB : convictions 2 a 6 (+ deux libelles de la grille) ; wC : convictions 7 et 8 ; wD : conviction 11
xB : slide 23 en puces, sans « Conduit par » ni jalon ; yA : slide 28, encart diagnostic natif ; z : slide 33 sans « Conduit par »
xA : doublons du titre (slides 2 et 20) ; p : pilule CONVICTION n retiree ; f : coquille « de Explorer » de la slide 23
"""
import deck_base
import delta_V37p
import delta_V37wA
import delta_V37wB
import delta_V37wC
import delta_V37wD
import delta_V37xA
import delta_V37xB
import delta_V37yA
import delta_V37z
import delta_V37zA
from pptx import Presentation

BASE = "V36"
NOTE = "V37 : Annexes supprimees, slides 7, 11-14, 17, 23, 28, 33 refaites, doublons du titre retires"
TITRE_23 = "Deux temps d'engagement"


def _slide_23(prs):
    s = [x for x in prs.slides if x.shapes.title is not None and x.shapes.title.text_frame.text.startswith(TITRE_23)]
    if len(s) != 1:
        raise ValueError(f"{len(s)} slides « {TITRE_23}… »")
    return s[0]


def coquille(prs):
    nb = 0
    for sh in _slide_23(prs).shapes:
        if not sh.has_text_frame:
            continue
        for p in sh.text_frame.paragraphs:
            for r in p.runs:
                if "de Explorer" in r.text:
                    r.text = r.text.replace("de Explorer", "d'Explorer")
                    nb += 1
    if nb != 1:
        raise ValueError(f"{nb} occurrences de « de Explorer »")


LOTS = [delta_V37zA, delta_V37wA, delta_V37wB, delta_V37wC, delta_V37wD, delta_V37xB, delta_V37yA, delta_V37z, delta_V37xA, delta_V37p]
OPS = [op for lot in LOTS for op in lot.OPS]
ETAPES = [etape for lot in LOTS for etape in lot.ETAPES] + [
    {"declarer": [f"id:{_slide_23(Presentation(deck_base.resoudre_base(BASE))).slide_id}"], "f": coquille, "nouvelles_max": 0, "nom": "coquille de Explorer -> d'Explorer"}]
