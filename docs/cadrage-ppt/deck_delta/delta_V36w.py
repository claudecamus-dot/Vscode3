"""Delta V36w (base V35) : slide « Deux temps d'engagement » : les zones « durée » et « montant » des trois cartes disparaissent.

- retire les pastilles « durée : à valider » (3 cartes) et « MONTANT : 0 — À VALIDER » (2 cartes) ; la pastille « JALON : RESTITUTION DU SPONSOR » de la 3e carte n'est ni une duree ni un montant : elle reste ;
- les cartes se raccourcissent (201 -> 190 pt) pour ne pas garder un vide, la ligne « Financement : … » remonte d'autant ;
- le texte retire est conserve dans les notes de la slide (les durees restent « a valider » sur les slides de planning et de calendrier).
Usage (depuis docs/cadrage-ppt/) : py deck_delta/deck.py delta_V36w --base V35 --sortie C:/tmp/deck-v36/V36w.pptx --sans-rendu
"""
import deck_base
from pptx import Presentation

BASE = "V35"
NOTE = "V36w : slide Deux temps d'engagement : zones duree et montant retirees"
TITRE = "Deux temps d'engagement : diagnostiquer, puis expérimenter et déployer"
NB = "\u00a0"
RETIRES = ("durée" + NB + ": à valider", "MONTANT" + NB + ": 0 — À VALIDER")
EMU_PT = 12700
HAUT_CARTE = 190 * EMU_PT


def _slide(prs):
    s = [x for x in prs.slides if x.shapes.title is not None and x.shapes.title.text_frame.text == TITRE]
    if len(s) != 1:
        raise ValueError(f"{len(s)} slides « {TITRE} »")
    return s[0]


def _ids():
    return [f"id:{_slide(Presentation(deck_base.resoudre_base(BASE))).slide_id}"]


def _retirer(sh):
    sh._element.getparent().remove(sh._element)


def zones(prs):
    s = _slide(prs)
    retire = []
    for tb in [x for x in s.shapes if x.has_text_frame and x.text_frame.text in RETIRES]:
        fond = next((x for x in s.shapes if x is not tb and x.shape_type == 1 and not x.text_frame.text
                     and x.top == tb.top and x.height == tb.height and x.left <= tb.left and x.left + x.width >= tb.left + tb.width), None)
        if fond is None:
            raise ValueError(f"pastille de « {tb.text_frame.text} » introuvable")
        retire.append(tb.text_frame.text)
        _retirer(tb)
        _retirer(fond)
    if len(retire) != 5:
        raise ValueError(f"{len(retire)} zones retirees au lieu de 5 : {retire}")
    cartes = [x for x in s.shapes if "Diagonal" in x.name and 190 * EMU_PT < x.height < 215 * EMU_PT]
    if len(cartes) != 3:
        raise ValueError(f"{len(cartes)} cartes au lieu de 3")
    for c in cartes:
        c.height = HAUT_CARTE
    reste = [x for x in s.shapes if x.has_text_frame and x.text_frame.text.startswith("JALON")]
    for tb in reste:  # la pastille JALON se cale au bas de sa carte
        fond = next(x for x in s.shapes if x is not tb and x.shape_type == 1 and not x.text_frame.text and x.top == tb.top and x.height == tb.height)
        haut = cartes[0].top + HAUT_CARTE - 8 * EMU_PT - tb.height
        tb.top = haut
        fond.top = haut
    fin = next(x for x in s.shapes if x.has_text_frame and x.text_frame.text.startswith("Financement"))
    fin.top = cartes[0].top + HAUT_CARTE + 10 * EMU_PT
    notes = s.notes_slide.notes_text_frame
    notes.text = (notes.text + "\n\n" if notes.text else "") + (
        "Zones retirees de la slide (demande de supprimer « montant » et « duree ») : « durée : à valider » sur les trois cartes ; « MONTANT : 0 — À VALIDER » sur les deux premières. "
        "Les durees restent à valider : voir les slides de planning et de calendrier.")


ETAPES = [{"declarer": _ids(), "f": zones, "nouvelles_max": 0, "nom": "zones duree et montant retirees, cartes raccourcies"}]
OPS = []
