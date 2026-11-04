"""Delta V37yA (base V36) : slide « De la douleur au produit… » : l'encart ILLUSTRATION (cycle Discovery/Delivery) devient un flux de diagnostic natif.

Aucun visuel generique propre trouve dans les PPT (radar de maturite : legende et bandeau de copyright traversent les libelles ; « Demarche standard pour un audit / cadrage » : texte factice ;
cartes d'empathie / experience map : gabarits vides ; restitutions de demo : noms de personnes) : l'encart est construit en formes natives, depuis le contenu de la slide.
Usage (depuis docs/cadrage-ppt/) : py deck_delta/deck.py delta_V37yA --base V36 --sortie C:/tmp/deck-v37-yA/V37yA.pptx --sans-rendu
"""
import os

import deck_base
import deck_draw
from forme_v9 import LINE, NAVY, SLATE, S, carre_num_cyan, forme, tx
from pptx import Presentation
from pptx.enum.text import MSO_ANCHOR as A

BASE = "V36"
NOTE = "V37yA : encart de la mission pilote refait en flux de diagnostic natif (interviews, analyse, restitution et choix)"
OPS = []
NB = "\u00a0"
T = "De la douleur au produit : une mission pilote de bout en bout"
ETAPES_FLUX = [
    ("Cadrer", "Périmètre et référence de départ"),
    ("Interviewer", "Le coach conduit les interviews"),
    ("Analyser", "Les agents repèrent les motifs récurrents"),
    ("Restituer", "Le client décide de la suite du pilote"),
]
NOTE_ADD = ("Encart ILLUSTRATION (V37yA)" + NB + ": l'image Discovery / Delivery est remplacée par un flux de diagnostic natif (cadrer, interviewer, analyser, restituer), "
            "derive du contenu de la slide ; aucune image importee (aucun visuel generique adapte trouve dans les supports OCTO ; voir provenance_V37yA.json). À valider avant diffusion.")


def refaire(prs):
    s = deck_draw.slide_par_titre(prs, T)
    pic = next(sh for sh in s.shapes if sh.name == "illustration")
    pic._element.getparent().remove(pic._element)
    titre = next(sh for sh in s.shapes if sh.has_text_frame and sh.text_frame.text == "Discovery, puis Delivery")
    titre.text_frame.paragraphs[0].runs[0].text = "Du diagnostic à la restitution"
    x0, y0, pas = 405, 144, 42
    forme(s, S.RECTANGLE, x0 + 11, y0 + 20, 1.25, pas * 3, LINE, None)
    for k, (nom, sous) in enumerate(ETAPES_FLUX):
        y = y0 + k * pas
        carre_num_cyan(s, x0, y, 22, k + 1, sz=11)
        tx(s, x0 + 32, y - 2, 215, 16, [[(nom, 12, True, NAVY)]], A.MIDDLE)
        tx(s, x0 + 32, y + 13, 215, 14, [[(sous, 11, False, SLATE)]], A.MIDDLE)
    notes = s.notes_slide.notes_text_frame
    notes.text = (notes.text.rstrip() + "\n" + NOTE_ADD) if notes.text.strip() else NOTE_ADD
    prov = os.path.join(os.path.dirname(os.path.abspath(__file__)), "provenance_V37yA.json")
    assert os.path.exists(prov)


def _ids():
    prs = Presentation(deck_base.resoudre_base(BASE))
    return [f"id:{deck_draw.slide_par_titre(prs, T).slide_id}"]


ETAPES = [{"declarer": _ids(), "f": refaire, "nouvelles_max": 0, "nom": "encart mission pilote : flux de diagnostic natif"}]
