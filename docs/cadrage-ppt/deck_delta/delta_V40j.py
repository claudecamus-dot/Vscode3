"""Delta V40j (base V39) : convictions 1, 7, 8, 9 (ranks 10, 13, 14, 15) - content review (text only).

Applies arbitrable proposals of docs/exports/analyses/analyse-contenu-V37.md : P18, P19, P20 (rank 10), P26 (rank 13),
P28, P29 (rank 14), P31 (rank 15). Layout of V39h (goutte reduite, pleine largeur) untouched except the rank 14
bottom band (one more line). Every replaced sentence is copied verbatim to the slide notes.
Usage (from docs/cadrage-ppt/) : py deck_delta/deck.py delta_V40j --base V39 --sortie C:/tmp/deck-v40-j/V40j.pptx --sans-rendu
"""
import copy

import deck_base
import deck_draw
from forme_v9 import deplacer, par_id
from pptx import Presentation

BASE = "V39"
NOTE = "V40j : convictions 1, 7, 8, 9 - textes resserres (P18, P19, P20, P26, P28, P29, P31)"
OPS = []


def _texte(sh, lignes):
    """Replace the text of sh, one paragraph per line, keeping the first run's formatting of each paragraph."""
    tf = sh.text_frame
    paras = tf.paragraphs
    while len(paras) < len(lignes):
        tf._txBody.append(copy.deepcopy(paras[-1]._p))
        paras = tf.paragraphs
    for p in paras[len(lignes):]:
        p._p.getparent().remove(p._p)
    for p, t in zip(tf.paragraphs, lignes, strict=True):
        runs = p.runs
        runs[0].text = t
        for r in runs[1:]:
            r._r.getparent().remove(r._r)


def _note(s, texte):
    tf = s.notes_slide.notes_text_frame
    tf.text = (tf.text + "\n" + texte).strip()


def _remplacer(s, d, i, lignes, journal):
    ancien = d[i].text_frame.text.replace("\n", " ")
    _texte(d[i], lignes)
    journal.append(f"« {ancien} »")


def c1(prs):
    s = deck_draw.slide_par_titre(prs, T1)
    d, j = par_id(s), []
    _remplacer(s, d, 111, ["Les outils posés sans changer les habitudes finissent contournés.",
                           "Le mode produit change d'abord les décisions et les rôles."], j)        # P18
    _remplacer(s, d, 116, ["Des référents internes portent la pratique après notre départ."], j)   # P19
    _note(s, "Retiré en V40 (reformulé sur la slide) : " + " ; ".join(j)
          + "\nÀ dire : le changement se pilote comme un chantier, adoption suivie par population.")  # P20


def c7(prs):
    s = deck_draw.slide_par_titre(prs, T7)
    d, j = par_id(s), []
    _remplacer(s, d, 169, ["Un produit a un responsable, une offre, des engagements et un coût complet connu."], j)  # P26
    _note(s, "Retiré en V40 (reformulé sur la slide) : " + " ; ".join(j))


def c8(prs):
    s = deck_draw.slide_par_titre(prs, T8)
    d, j = par_id(s), []
    _remplacer(s, d, 191, ["Des agents sur une activité récurrente à la fois ; l'humain décide et en répond.",  # P28
                           "Ce que l'IA peut décider est fixé d'avance.",                                    # P29
                           "Effets visés, à mesurer ; rien n'est promis."], j)
    deplacer(d[191], None, 310, None, 54)
    _note(s, "Retiré en V40 (reformulé sur la slide) : " + " ; ".join(j))


def c9(prs):
    s = deck_draw.slide_par_titre(prs, T9)
    d, j = par_id(s), []
    _remplacer(s, d, 172, ["Décide\u00a0: poursuivre, étendre, pivoter ou arrêter une capacité"], j)  # P31
    _note(s, "Retiré en V40 (reformulé sur la slide) : " + " ; ".join(j))


T1 = "Conviction 1 : le mode produit est d'abord une culture, pas un outil"
T7 = "Conviction 7 : financer des produits et des équipes stables"
T8 = "Conviction 8 : une petite équipe produit qui construit et exploite"
T9 = "Conviction 9 : trois instances, chacune avec sa décision"


def _id(t):
    prs = Presentation(deck_base.resoudre_base(BASE))
    return [f"id:{deck_draw.slide_par_titre(prs, t).slide_id}"]


ETAPES = [
    {"declarer": _id(T1), "f": c1, "nouvelles_max": 0, "nom": "conviction 1 : textes P18 P19 P20"},
    {"declarer": _id(T7), "f": c7, "nouvelles_max": 0, "nom": "conviction 7 : texte P26"},
    {"declarer": _id(T8), "f": c8, "nouvelles_max": 0, "nom": "conviction 8 : textes P28 P29"},
    {"declarer": _id(T9), "f": c9, "nouvelles_max": 0, "nom": "conviction 9 : texte P31"},
]
