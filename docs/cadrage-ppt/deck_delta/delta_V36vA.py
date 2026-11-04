"""Delta V36vA (base V35) : slides de convictions 1 a 6 sans les zones « critere observable » et « chantier », formes refondues ; derniere ligne de la grille des convictions.

- conviction 1 : l'appropriation de tous devient le heros (grande carte navy, quatre pilules d'acteurs), deux cartes d'appui dessous ; le rail (goutte + pilule) est intact ;
- convictions 2 a 4 et 5 et 6 : cartes agrandies a la hauteur liberee, pictogrammes agrandis, pilule de conviction, enonce en gros, etape de la boucle ; « regle de passage » en carte navy ;
- grille des convictions : la ligne « Comment lire la suite » ne promet plus un critere et un chantier par conviction.
Les textes retires (critere observable, chantier, ancienne phrase) vont dans les notes de chaque slide, mot pour mot.
Usage (depuis docs/cadrage-ppt/) : py deck_delta/deck.py delta_V36vA --base V35 --sortie C:/tmp/deck-v36-vA/V36vA.pptx --sans-rendu
"""
import copy

import deck_base
import deck_draw
from forme_ground import pilule
from forme_v9 import BLANC, NAVY, restyle
from forme_v9 import deplacer as mv
from pptx import Presentation
from pptx.enum.text import MSO_ANCHOR as A
from pptx.enum.text import MSO_AUTO_SIZE
from pptx.enum.text import PP_ALIGN as P
from pptx.util import Pt

BASE = "V35"
NOTE = "V36vA : convictions 1 a 6 sans critere/chantier, formes refondues ; ligne de lecture de la grille"
OPS = []

NB = "\u00a0"
T_GRILLE = "Treize convictions couvrent toute la transformation de l'Infra"
T_C1 = "Conviction 1" + NB + ": le mode produit est d'abord une culture, pas un outil"
T_C234 = "Du besoin à la priorité" + NB + ": douleur mesurée, porteur, faits d'abord"
T_C56 = "Progrès et gain de l'IA" + NB + ": mesurés puis vérifiés, jamais promis"
TITRES = (T_GRILLE, T_C1, T_C234, T_C56)

LIGNE_9 = "une slide par conviction, ou par groupe de convictions liées."
X0, X1 = 258.0, 659.25


def _d(s):
    return {sh.shape_id: sh for sh in s.shapes}


def _notes_ajout(s, texte):
    tf = s.notes_slide.notes_text_frame
    ancien = tf.text.strip()
    tf.text = (ancien + "\n\n" if ancien else "") + texte


def _suppr(d, ids):
    for i in ids:
        d[i]._element.getparent().remove(d[i]._element)


def _zone(sh, x=None, y=None, w=None, h=None, sz=None, align=None, ancre=None, gras=None, couleur=None):
    """Repositionne une zone de texte existante, la fige (plus d'auto-ajustement) et regle taille / alignement / ancre."""
    mv(sh, x, y, w, h)
    tf = sh.text_frame
    tf.auto_size = MSO_AUTO_SIZE.SHAPE_TO_FIT_TEXT if ancre == A.TOP else MSO_AUTO_SIZE.NONE  # texte ancre en haut : la boite epouse le texte (comme en V35)
    tf.word_wrap = True
    if ancre is not None:
        tf.vertical_anchor = ancre
    for para in tf.paragraphs:
        if align is not None:
            para.alignment = align
        for r in para.runs:
            if sz is not None:
                r.font.size = Pt(sz)
            if gras is not None:
                r.font.bold = gras
            if couleur is not None:
                r.font.color.rgb = couleur


def _echelle(s, ids, ancien_centre, nouveau_centre, k):
    """Agrandit les formes `ids` (un pictogramme) d'un facteur k autour de l'ancien centre, puis les pose autour du nouveau."""
    d = _d(s)
    ox, oy = ancien_centre
    nx, ny = nouveau_centre
    for i in ids:
        sh = d[i]
        x, y, w, h = (v / 12700 for v in (sh.left, sh.top, sh.width, sh.height))
        mv(sh, x=nx + (x - ox) * k, y=ny + (y - oy) * k, w=w * k, h=h * k)


# ================================================================ 9. Ligne de lecture de la grille
def grille(prs):
    s = deck_draw.slide_par_titre(prs, T_GRILLE)
    d = _d(s)
    runs = d[146].text_frame.paragraphs[0].runs
    ancien = runs[0].text + runs[1].text
    runs[1].text = LIGNE_9
    _notes_ajout(s, "Phrase retirée de la ligne « Comment lire la suite »" + NB + ": « " + ancien.strip() + " » "
                    "(les zones « critère observable » et « chantier » ne figurent plus sur les slides de convictions ; leur texte est dans les notes de ces slides).")


# ================================================================ 10. Conviction 1 : l'appropriation de tous
def conviction1(prs):
    s = deck_draw.slide_par_titre(prs, T_C1)
    d = _d(s)
    critere, chantier = d[127].text_frame.text, d[134].text_frame.text
    _suppr(d, [110, 115] + list(range(121, 135)))  # points de liaison horizontaux et les deux bandes du bas
    # heros : grande carte navy
    mv(d[112], x=X0, y=100, w=X1 - X0, h=148)
    restyle(d[112], "roundRect", adj=0.16)
    cx = (X0 + X1) / 2
    _zone(d[113], x=X0 + 20, y=108, w=X1 - X0 - 40, h=28, sz=20, align=P.CENTER, ancre=A.MIDDLE)
    mv(d[114], x=cx - 120, y=142, w=240)
    _zone(d[116], x=X0 + 20, y=148, w=X1 - X0 - 40, h=22, sz=14, align=P.CENTER, ancre=A.MIDDLE)
    for k, (forme_id, texte_id) in enumerate(((148, 149), (150, 151), (152, 153), (154, 155))):
        x = cx + (-154 if k % 2 == 0 else 4)
        y = 179 + (k // 2) * 31
        mv(d[forme_id], x=x, y=y, w=150, h=26)
        _zone(d[texte_id], x=x, y=y, w=150, h=26, sz=12, align=P.CENTER, ancre=A.MIDDLE)
    # deux cartes d'appui
    w_c = 196.0
    for carte, titre, sep, corps, x in ((107, 108, 109, 111, X0), (117, 118, 119, 120, X1 - w_c)):
        mv(d[carte], x=x, y=258, w=w_c, h=108)
        restyle(d[carte], "roundRect", adj=0.16)
        _zone(d[titre], x=x + 10, y=264, w=w_c - 20, h=20, sz=12.5, align=P.CENTER, ancre=A.MIDDLE)
        mv(d[sep], x=x + 16, y=288, w=w_c - 32)
        _zone(d[corps], x=x + 12, y=294, w=w_c - 24, h=64, sz=12, align=P.LEFT, ancre=A.TOP)
    _notes_ajout(s, "Critère observable (retiré de la slide)" + NB + ": " + critere + "\n\n"
                    "Chantier (retiré de la slide)" + NB + ": " + chantier)


# ================================================================ 11 et 12. Trois colonnes de convictions
# colonne = (carte, [formes du pictogramme], disque, pastille, texte pastille, enonce, critere, chantier, etape de boucle)
COL_X = (45.0, 257.0, 469.0)
CARTE_W = 190.0
D_PICTO = 68.0


def _colonne(s, d, col, carte, picto, disque, pastille, pastille_txt, enonce, boucle):
    x = COL_X[col]
    cx = x + CARTE_W / 2
    mv(d[carte], x=x, y=134, w=CARTE_W, h=230)
    restyle(d[carte], "roundRect", adj=0.12)
    ancien = ((d[disque].left + d[disque].width / 2) / 12700, (d[disque].top + d[disque].height / 2) / 12700)
    _echelle(s, picto, ancien, (cx, 128.0), D_PICTO / 56.0)
    mv(d[pastille], x=cx - 60, y=172, w=120, h=22)
    _zone(d[pastille_txt], x=cx - 60, y=172, w=120, h=22, sz=11, align=P.CENTER, ancre=A.MIDDLE)
    _zone(d[enonce], x=x + 11, y=206, w=CARTE_W - 22, h=116, sz=16, align=P.CENTER, ancre=A.TOP, gras=True)
    if boucle:
        pilule(s, cx - 78, 334, 156, 22, "Boucle" + NB + ": " + boucle, "contour", 11)


def convictions_234(prs):
    s = deck_draw.slide_par_titre(prs, T_C234)
    d = _d(s)
    notes = []
    for n, ids in ((2, (110, 112)), (3, (125, 127)), (4, (141, 143))):
        notes.append((n, d[ids[0]].text_frame.text, d[ids[1]].text_frame.text))
    cols = (
        (100, (102, 103, 104, 105), 101, 107, 108, 106, "Explorer"),
        (113, tuple(range(115, 121)), 114, 122, 123, 121, "Ancrer"),
        (128, tuple(range(130, 137)), 129, 138, 139, 137, "Prioriser"),
    )
    for col, (carte, picto, disque, pastille, ptxt, enonce, boucle) in enumerate(cols):
        _colonne(s, d, col, carte, (disque,) + picto, disque, pastille, ptxt, enonce, boucle)
    _suppr(d, [109, 110, 111, 112, 124, 125, 126, 127, 140, 141, 142, 143])
    _notes_ajout(s, "Critère observable (retiré de la slide)" + NB + ":\n" + "\n".join(f"Conviction {n}" + NB + ": " + c for n, c, _ in notes) + "\n\n"
                    "Chantier (retiré de la slide)" + NB + ":\n" + "\n".join(f"Conviction {n}" + NB + ": " + h for n, _, h in notes))


def convictions_56(prs):
    s = deck_draw.slide_par_titre(prs, T_C56)
    d = _d(s)
    notes = [(5, d[108].text_frame.text, d[110].text_frame.text), (6, d[119].text_frame.text, d[121].text_frame.text)]
    cols = (
        (99, (101, 102, 103), 100, 105, 106, 104, "Mesurer"),
        (111, (113, 114), 112, 116, 117, 115, "Comprendre"),
    )
    for col, (carte, picto, disque, pastille, ptxt, enonce, boucle) in enumerate(cols):
        _colonne(s, d, col, carte, (disque,) + picto, disque, pastille, ptxt, enonce, boucle)
    _suppr(d, [107, 108, 109, 110, 118, 119, 120, 121])
    # regle de passage : carte navy, texte blanc
    mv(d[122], x=COL_X[2], y=134, w=CARTE_W, h=230)
    restyle(d[122], fill=NAVY, ligne=NAVY, lw=0.75)
    mv(d[123], x=COL_X[2] + 25, y=172, w=140, h=22)
    _zone(d[124], x=COL_X[2] + 25, y=172, w=140, h=22, sz=11, align=P.CENTER, ancre=A.MIDDLE)
    _zone(d[125], x=COL_X[2] + 14, y=204, w=CARTE_W - 28, h=146, sz=14, align=P.LEFT, ancre=A.TOP, couleur=BLANC)
    para = d[125].text_frame.paragraphs[0]
    haut, bas = para.runs[0].text.split(chr(10))
    para.runs[0].text = haut
    suite = copy.deepcopy(para._p)
    para._p.addnext(suite)
    d[125].text_frame.paragraphs[1].runs[0].text = bas
    d[125].text_frame.paragraphs[1].space_before = Pt(12)
    _notes_ajout(s, "Critère observable (retiré de la slide)" + NB + ":\n" + "\n".join(f"Conviction {n}" + NB + ": " + c for n, c, _ in notes) + "\n\n"
                    "Chantier (retiré de la slide)" + NB + ":\n" + "\n".join(f"Conviction {n}" + NB + ": " + h for n, _, h in notes))


def _ids():
    prs = Presentation(deck_base.resoudre_base(BASE))
    return [f"id:{deck_draw.slide_par_titre(prs, t).slide_id}" for t in TITRES]


_I = dict(zip(TITRES, _ids(), strict=True))
ETAPES = [
    {"declarer": [_I[T_GRILLE]], "f": grille, "nouvelles_max": 0, "nom": "grille : ligne « Comment lire la suite » reformulee"},
    {"declarer": [_I[T_C1]], "f": conviction1, "nouvelles_max": 0, "nom": "conviction 1 : appropriation en heros, sans critere ni chantier"},
    {"declarer": [_I[T_C234]], "f": convictions_234, "nouvelles_max": 0, "nom": "convictions 2 a 4 : cartes agrandies, sans critere ni chantier"},
    {"declarer": [_I[T_C56]], "f": convictions_56, "nouvelles_max": 0, "nom": "convictions 5 et 6 : cartes agrandies, regle de passage navy"},
]
