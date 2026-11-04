"""Delta V41a (base V40) : conviction 9 (rank 15) - actors and objectives of the three bodies.

User request : « slide 15 à revoir sur le fond : les acteurs et les objectifs ». Same three bodies (COMOP, COPIL,
comité d'investissement). Each now states Objectif / Décide / Avec / cadence. New wording comes from generic
governance patterns (no client name, person or figure) and from the deck itself. Layout keeps the V39 rule
(goutte réduite 56 pt at (45,94), already in the base) : a lead sentence in the top band (x 113 -> 659.25,
y 92 -> 150) and three full-width rows below (x 45 -> 659.25, y 158 -> 366). Old text goes verbatim to the notes.
Usage (from docs/cadrage-ppt/) : py deck_delta/deck.py delta_V41a --base V40 --sortie C:/tmp/deck-v41-a/V41a.pptx --sans-rendu
"""
import copy

import deck_base
import deck_draw
from forme_v9 import deplacer, par_id
from pptx import Presentation
from pptx.enum.text import MSO_AUTO_SIZE
from pptx.util import Pt

BASE = "V40"
NOTE = "V41a : conviction 9 - objectif, décisions et acteurs de chaque instance"
OPS = []

T9 = "Conviction 9 : trois instances, chacune avec sa décision"
NBSP = "\u00a0"

# (card, square, number, header box, body box, cadence box) per body - one full-width row each, ids of the V40 slide
COLONNES = [(154, 155, 156, 157, 158, 160), (161, 162, 163, 164, 165, 167), (168, 169, 170, 171, 172, 174)]
CORPS = [
    ("COMOP", "comité opérationnel",
     "lever les blocages au plus près de l'équipe",
     "ajustements, risques, escalades vers le COPIL",
     "responsable produit, équipe, coach OCTO, relais client",
     "cadence à fixer avec vous"),
    ("COPIL", "comité de pilotage",
     "piloter par l'impact mesuré, pas par l'avancement",
     "priorités du backlog et roadmap du produit",
     "sponsor, responsable produit, métiers, DSI, coach OCTO",
     "cadence à fixer avec vous"),
    ("Comité d'investissement", "revue trimestrielle des budgets",
     "financer les capacités qui produisent de la valeur",
     "poursuivre, étendre, pivoter ou arrêter une capacité",
     "sponsor, DSI, finance, responsables produit",
     "cadence trimestrielle, à valider"),
]
CHAPO = ("Chaque instance a son objectif, ses décisions et ses participants ; "
         "chaque séance laisse une décision tracée.")
PARTICIPANTS = "participants à valider"


def _paras(sh, spec, espace=0):
    """Rewrite sh as paragraphs of runs [(text, size, bold)], cloning the first run (colour kept)."""
    tf = sh.text_frame
    tf.word_wrap = True
    tf.auto_size = MSO_AUTO_SIZE.NONE
    p0 = tf.paragraphs[0]
    modele_p = copy.deepcopy(p0._p)
    modele_r = copy.deepcopy(p0.runs[0]._r)
    for p in list(tf.paragraphs):
        p._p.getparent().remove(p._p)
    for i, runs in enumerate(spec):
        p_el = copy.deepcopy(modele_p)
        for r in p_el.findall(modele_r.tag):
            p_el.remove(r)
        tf._txBody.append(p_el)
        p = tf.paragraphs[-1]
        for texte, taille, gras in runs:
            r_el = copy.deepcopy(modele_r)
            _inserer(p._p, r_el)
            r = p.runs[-1]
            r.text = texte
            r.font.size = Pt(taille)
            r.font.bold = gras
        if i and espace:
            p.space_before = Pt(espace)


def _inserer(p_el, r_el):
    """Insert a run before the end-paragraph properties if any."""
    fin = p_el.find("{http://schemas.openxmlformats.org/drawingml/2006/main}endParaRPr")
    if fin is not None:
        fin.addprevious(r_el)
    else:
        p_el.append(r_el)


def c9(prs):
    s = deck_draw.slide_par_titre(prs, T9)
    d = par_id(s)
    ancien = " | ".join(d[i].text_frame.text.replace("\n", " ")
                        for col in COLONNES for i in col[3:]) + " | " + d[159].text_frame.text \
        + " | " + d[166].text_frame.text + " | " + d[173].text_frame.text
    for k, (col, corps) in enumerate(zip(COLONNES, CORPS, strict=True)):
        carte, carre, num, tete, texte, cad = (d[i] for i in col)
        nom, sous, obj, dec, avec, cadence = corps
        y = 158 + k * 70
        deplacer(carte, 45, y, 614.25, 64)
        deplacer(carre, 57, y + 20, 24, 24)
        deplacer(num, 57, y + 20, 24, 24)
        _paras(num, [[(str(k + 1), 12.5, True)]])
        deplacer(tete, 91, y + 3, 176, 58)
        _paras(tete, [[(nom, 14, True)], [(sous, 11, False)], [(cadence, 11, False)]])
        tete.text_frame.vertical_anchor = 3  # middle
        deplacer(texte, 273, y + 3, 376, 58)
        _paras(texte, [[("Objectif" + NBSP + ": ", 12, True), (obj, 12, False)],
                       [("Décide" + NBSP + ": ", 12, True), (dec, 12, False)],
                       [("Avec" + NBSP + ": ", 12, True), (avec, 12, False)]])
        texte.text_frame.vertical_anchor = 3
        cad._element.getparent().remove(cad._element)
    # lead sentence in the top band, right of the reduced drop
    deplacer(d[159], 113, 96, 546.25, 50)
    _paras(d[159], [[(CHAPO + " " + PARTICIPANTS.capitalize() + ".", 13, False)]])
    d[159].text_frame.vertical_anchor = 3
    for i in (166, 173, 176):
        d[i]._element.getparent().remove(d[i]._element)
    tf = s.notes_slide.notes_text_frame
    tf.text = (tf.text + "\nRetiré en V41 (remplacé sur la slide : objectif, décisions, acteurs) : « " + ancien
               + " »\nMotifs génériques retenus (répertoire client non cité) : COPIL rythmé, compte rendu et "
               "décisions tracés en séance, animateur garant du temps, rétrospective trimestrielle du COPIL ; "
               "pilotage par l'impact plutôt que par l'avancement ; la gouvernance sponsor négocie les budgets et "
               "aide à la décision ; le budget d'un domaine est porté en binôme métier / IT.").strip()


def _id(t):
    prs = Presentation(deck_base.resoudre_base(BASE))
    return [f"id:{deck_draw.slide_par_titre(prs, t).slide_id}"]


ETAPES = [
    {"declarer": _id(T9), "f": c9, "nouvelles_max": 0, "nom": "conviction 9 : objectif, décisions, acteurs"},
]
