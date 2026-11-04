"""Delta V41b (base V40) : separate the MISSION governance (ranks 27, 34) from the RECOMMENDED target governance (rank 15).

User request : « il faut distinguer la gouvernance de la mission et la conviction d'une gouvernance pour la
recommandation de l'organisation ». Rank 15 = V41a (approved by the user) + one framing touch in the lead sentence.
Ranks 27 and 34 are labelled as the mission's governance; the mission Pilotage decides the pilot go/no-go and its
extension (COPIL name reserved for the target body of rank 15); a bridge sentence hands over to « Nos convictions ».
Layouts unchanged; replaced text goes verbatim to the notes.
Usage (from docs/cadrage-ppt/) : py deck_delta/deck.py delta_V41b --base V40 --sortie C:/tmp/deck-v41-b/V41b.pptx
"""
import deck_draw
import delta_V41a as A
from forme_v9 import deplacer, par_id

BASE = "V40"
NOTE = "V41b : gouvernance de la mission (27, 34) distincte de la gouvernance cible recommandée (15)"
OPS = []

T27 = "Calendrier du pilote : étapes et jalons, durées à valider"
T34 = "Deux comités en parallèle : l'un suit l'exécution, l'autre décide"

A.CHAPO = A.CHAPO.replace("Chaque instance", "Dans l'organisation cible recommandée, chaque instance", 1)


def _texte(sh, txt):
    """Replace the text of the first run of each paragraph, keeping its formatting; extra runs emptied."""
    lignes = txt.split("\n")
    paras = sh.text_frame.paragraphs
    for p, ligne in zip(paras, lignes, strict=False):
        p.runs[0].text = ligne
        for r in p.runs[1:]:
            r.text = ""


def _note(s, anciens):
    tf = s.notes_slide.notes_text_frame
    tf.text = (tf.text + "\nRemplacé en V41b (gouvernance de la mission vs gouvernance cible) : "
               + " | ".join("« " + a + " »" for a in anciens)).strip()


def s27(prs):
    s = deck_draw.slide_par_titre(prs, T27)
    d = par_id(s)
    av = [d[i].text_frame.text for i in (81, 118, 121)]
    _texte(d[81], "Pilotage\u00a0: go / no-go du sponsor")
    _texte(d[118], "LIVRABLE PAR ÉCHÉANCE\n◆ = Pilotage")
    _texte(d[121], "GOUVERNANCE DE LA MISSION\u00a0: TROIS INSTANCES")
    _note(s, av)


def s34(prs):
    s = deck_draw.slide_par_titre(prs, T34)
    d = par_id(s)
    av = [d[i].text_frame.text for i in (84, 88, 102)]
    _texte(d[84], "décider le go / no-go et l'extension du pilote")
    _texte(d[88], "Valider priorités et périmètre du pilote\u00a0; décider go / no-go et extension sur des preuves.")
    deplacer(d[102], 45, 350, 614.25, 30)
    _texte(d[102], "Gouvernance de la mission. La revue de valeur, rituel de la mission, est décrite avec le "
                   "calendrier du pilote. En fin de mission, ces instances passent la main à la gouvernance cible "
                   "recommandée dans « Nos convictions ».")
    d[102].text_frame.word_wrap = True
    _note(s, av)


def _id(t):
    import deck_base
    from pptx import Presentation
    prs = Presentation(deck_base.resoudre_base(BASE))
    return [f"id:{deck_draw.slide_par_titre(prs, t).slide_id}"]


ETAPES = A.ETAPES + [
    {"declarer": _id(T27), "f": s27, "nouvelles_max": 0, "nom": "27 : gouvernance de la mission"},
    {"declarer": _id(T34), "f": s34, "nouvelles_max": 0, "nom": "34 : gouvernance de la mission + passerelle"},
]
