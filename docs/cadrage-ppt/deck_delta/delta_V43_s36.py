"""Delta V43 s36 (base V42) : relieve slide 36 « L'IA est gouvernée » (5 blocs, étiquettes B4..B9 de l'illustration ~7 pt).
Slide 36 garde les garde-fous, les 4 cartes (en rangée) et l'illustration AGRANDIE (étiquettes lisibles) ; le RACI et l'autonomie de l'IA passent
sur une slide suivante, recomposée pleine page. Aucun texte supprimé ni reformulé ; seul le titre de la nouvelle slide est ajouté.
L'illustration est une image : ses étiquettes ne sont pas du texte éditable (leur taille n'est que mise à l'échelle).
Usage (depuis docs/cadrage-ppt/) : py deck_delta/deck.py delta_V43_s36 --base V42 --sortie C:/tmp/deck-v43-s36/V43s36.pptx --sans-rendu
"""
import copy

import deck_draw
from forme_v9 import NAVY, deplacer, par_id
from pptx.util import Pt

BASE = "V42"
NOTE = "V43 s36 : slide 36 scindée (garde-fous + illustration agrandie | RACI + autonomie de l'IA)"
OPS = []
T36 = "L'IA est gouvernée : données, droits, validations et traçabilité"
T36B = "L'IA est gouvernée : qui décide, jusqu'où l'IA agit"
CHROME = (2, 64, 65, 67, 68, 69, 130, 131, 132, 133)


def _taille(sh, pts_):
    for p in sh.text_frame.paragraphs:
        for r in p.runs:
            r.font.size = Pt(pts_)


def s36(prs):
    s = deck_draw.slide_par_titre(prs, T36)
    d = par_id(s)
    # cartes en rangée de 4 (x, w en points ; offsets internes gardés)
    w, gap, h, y = 147.5, 8, 80, 115
    for k, (card, badge, num, titre, corps) in enumerate(
            [(75, 76, 77, 78, 79), (80, 81, 82, 83, 84), (85, 86, 87, 88, 89), (90, 91, 92, 93, 94)]):
        x = 45 + k * (w + gap)
        deplacer(d[card], x, y, w, h)
        deplacer(d[badge], x + 8, y + 7.3)
        deplacer(d[num], x + 8, y + 7.3)
        deplacer(d[titre], x + 32, y + 6, w - 40)
        deplacer(d[corps], x + 8, y + 30, w - 14, h - 32)
    # illustration agrandie sous les cartes
    py, ph = 203, 161
    deplacer(d[95], 45, py, 614, ph)
    deplacer(d[96], 53, py + 7)
    deplacer(d[97], 53, py + 7)
    deplacer(d[98], 53 + 88 + 8, py + 7, 614 - 8 - 104 - 8)
    pic = d[99]
    ph_pic = 126
    wp = ph_pic * pic.width / pic.height
    deplacer(pic, 45 + (614 - wp) / 2, py + 30, wp, ph_pic)
    # le RACI / l'autonomie quittent cette slide (ils sont recomposés sur la suivante)
    from forme_v9 import supprimer
    for i in [134, 101] + list(range(102, 130)):
        if i in d:
            supprimer(d[i])
    tf = s.notes_slide.notes_text_frame
    tf.text = (tf.text + "\nV43 s36 : RACI humain / agent et autonomie de l'IA déplacés sur la slide suivante ; cartes en rangée, illustration agrandie.").strip()


def s36b(prs):
    src = deck_draw.slide_par_titre(prs, T36)  # lue AVANT que s36 ne supprime : voir ordre des étapes (cette étape passe d'abord)
    new = deck_draw.nouvelle_apres(prs, src, src.slide_layout)
    sd = par_id(src)
    clones = {}
    for i in CHROME + (134, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117,
                       118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129):
        clones[i] = deck_draw.clone_forme(sd[i], new)
    # second panneau gris : copie de 134, id unique
    p2 = deck_draw.clone_forme(sd[134], new)
    p2._element.nvSpPr.cNvPr.set("id", "900")
    deck_draw.set_run(clones[2], T36B)
    c = clones
    # panneau 1 : RACI
    deplacer(c[134], 45, 80, 614, 135)
    deplacer(c[101], 55, 90, 594, 40)
    _taille(c[101], 12)
    cw, cg = 143.5, 8
    for k, (card, tit, pil, pt_) in enumerate([(102, 103, 104, 105), (106, 107, 108, 109),
                                               (110, 111, 112, 113), (114, 115, 116, 117)]):
        x = 53 + k * (cw + cg)
        deplacer(c[card], x, 136, cw, 70)
        deplacer(c[tit], x + 5, 141, cw - 10, 32)
        _taille(c[tit], 12)
        deplacer(c[pil], x + 25, 182, cw - 50, 18)
        deplacer(c[pt_], x + 25, 182, cw - 50, 18)
        _taille(c[pt_], 10)
    # panneau 2 : autonomie de l'IA
    deplacer(p2, 45, 227, 614, 137)
    p2.zorder = None if False else None
    deplacer(c[118], 55, 240, 300, 20)
    _taille(c[118], 12)
    pw, pg = 133, 22
    for k, (pil, txt, chev) in enumerate([(119, 120, 121), (122, 123, 124), (125, 126, 127), (128, 129, None)]):
        x = 53 + k * (pw + pg)
        deplacer(c[pil], x, 275, pw, 44)
        deplacer(c[txt], x + 4, 275, pw - 8, 44)
        _taille(c[txt], 12)
        if chev:
            deplacer(c[chev], x + pw + 7, 290, 8, 14)
    # le panneau 2 doit passer derrière ses pilules : l'insérer juste après le panneau 1 dans l'arbre
    c[134]._element.addnext(p2._element)
    tf = new.notes_slide.notes_text_frame
    tf.text = "V43 s36 : RACI et autonomie de l'IA issus de la slide « " + T36 + " » (contenu inchangé)."


def _id(t):
    import deck_base
    from pptx import Presentation
    prs = Presentation(deck_base.resoudre_base(BASE))
    return [f"id:{deck_draw.slide_par_titre(prs, t).slide_id}"]


ETAPES = [
    {"declarer": _id(T36), "f": s36b, "nouvelles_max": 1, "nom": "36b : RACI + autonomie sur une slide pleine page"},
    {"declarer": _id(T36), "f": s36, "nouvelles_max": 0, "nom": "36 : cartes en rangée, illustration agrandie"},
]
