"""Delta V35sH (base V34 + lot g) : « Réussir : cinq conditions que nous posons avant de commencer ».

- les cinq phrases « dans la démarche : … » sont supprimées ; chaque carte reçoit UNE phrase qui dit pourquoi la condition compte
  (sources : slides « Ce que nous attendons de vous… », « Du pilote à l'autonomie… », « L'IA est gouvernée… », « Nous mesurons la valeur client… »,
  fiches de phase, conviction 1) ;
- le nom de l'étape de la boucle (Prioriser, Explorer, Mesurer, Ancrer, Comprendre) reste en pastille secondaire « Boucle : … » au bas de la carte ;
- la bande libérée sous le titre sert à agrandir les cartes : bandeau d'intro et panneau remontés, cartes de 108 pt ; le pictogramme descend au bas de la carte.
Titres, numéros, pictogrammes, pastilles « LA CONDITION » et bloc « PROPOSITION » (hypothèse) ne changent pas ; la phrase retirée va dans les notes.
Usage (depuis docs/cadrage-ppt/) : py deck_delta/deck.py delta_V35sH --base C:/tmp/deck-v35/V35g.pptx --sortie C:/tmp/deck-v35-sH/V35sH.pptx --sans-rendu
"""
import deck_base
import deck_draw
from forme_v9 import NAVY, PANEL, SLATE, S, forme, tx
from forme_v9 import deplacer as mv
from pptx import Presentation
from pptx.enum.text import MSO_ANCHOR as A
from pptx.enum.text import PP_ALIGN as P
from pptx.util import Pt

BASE = "V34"
NOTE = "V35sH : cinq conditions, phrase « dans la démarche » supprimée, une phrase de sens par condition, étape de la boucle en pastille secondaire"
OPS = []

NB = "\u00a0"
T_COND = "Réussir : cinq conditions que nous posons avant de commencer"
TITRES = (T_COND,)

# (carte, numero, texte, pictogramme + glyphes, entete, pastille, etape de la boucle, phrase ajoutee)
CARTES = [
    (5, 7, 8, (26, 27, 28, 29), 51, 52, "Prioriser", "Il arbitre les priorités, décide du go / no-go et porte le message."),
    (9, 10, 11, (30, 31, 32), 53, 54, "Explorer", "Utile pour prouver la valeur, et gardé figé pendant le pilote."),
    (12, 13, 14, (33, 34, 35, 36), 55, 56, "Mesurer", "Sans référence de départ, on ne peut pas mesurer l'apport."),
    (15, 16, 17, (37, 38, 39), 57, 58, "Ancrer", "Des relais formés portent les rituels" + NB + ": le client prend ensuite la main."),
    (18, 19, 20, (40, 41, 42), 59, 60, "Comprendre", "Données, droits et validations d'abord" + NB + ": aucune donnée traitée sans accord."),
]
H_CARTE = 108.0
NOTES = (
    "Retiré de la slide" + NB + ": la phrase « dans la démarche" + NB + ": Prioriser / Explorer / Mesurer / Ancrer / Comprendre » sous chaque numéro "
    "(1 sponsor" + NB + "→ Prioriser, 2 périmètre" + NB + "→ Explorer, 3 référence" + NB + "→ Mesurer, 4 relais" + NB + "→ Ancrer, 5 IA cadrée" + NB + "→ Comprendre). "
    "L'étape de la boucle reste visible en pastille secondaire « Boucle" + NB + ": … » au bas de chaque carte."
)


def _d(s):
    return {sh.shape_id: sh for sh in s.shapes}


def _run(sh, texte):
    runs = sh.text_frame.paragraphs[0].runs
    if len(runs) == 1 and runs[0].text == texte:
        return
    runs[0].text = texte
    for r in runs[1:]:
        r._r.getparent().remove(r._r)


def _pt(sh, attr):
    return getattr(sh, attr) / 12700


def conditions(prs):
    s = deck_draw.slide_par_titre(prs, T_COND)
    d = _d(s)
    # bandeau d'intro et panneau remontes dans la bande libre sous le titre
    for i in (3, 4):
        mv(d[i], y=_pt(d[i], "top") - 20)
    mv(d[69], y=_pt(d[69], "top") - 20, h=245)
    y_haut = _pt(d[69], "top") + 11
    y_bas = y_haut + H_CARTE + 10
    for k, (carte, num, texte, pictos, entete, pastille, etape, phrase) in enumerate(CARTES):
        y0_ancien = _pt(d[carte], "top")
        y0 = y_haut if k < 3 else y_bas
        x = _pt(d[carte], "left")
        dy = y0 - y0_ancien
        mv(d[carte], y=y0, h=H_CARTE)
        mv(d[entete], y=y0)
        mv(d[pastille], y=_pt(d[pastille], "top") + dy)
        mv(d[num], x=x + 8, y=y0 + 38, w=30, h=36)
        # la phrase « dans la demarche » devient la phrase de sens
        _run(d[texte], phrase)
        for r in d[texte].text_frame.paragraphs[0].runs:
            r.font.size = Pt(10.5)
            r.font.color.rgb = NAVY
        mv(d[texte], x=x + 38, y=y0 + 41, w=149, h=58)
        # pictogramme au bas de la carte, aligne sur la pastille
        for i in pictos:
            mv(d[i], y=_pt(d[i], "top") + dy + 30)
        # etape de la boucle : pastille secondaire
        forme(s, S.ROUNDED_RECTANGLE, x + 8, y0 + 84, 108, 16, PANEL, None, adj=0.5)
        tx(s, x + 8, y0 + 84, 108, 16, [[("Boucle" + NB + ": " + etape, 10, False, SLATE)]], A.MIDDLE, P.CENTER)
    # sixieme tuile (proposition) : meme rangee, meme hauteur
    dy6 = y_bas - _pt(d[21], "top")
    mv(d[21], y=y_bas, h=H_CARTE)
    for i in (22, 23, 24):
        mv(d[i], y=_pt(d[i], "top") + dy6)
    s.notes_slide.notes_text_frame.text = NOTES


def _ids():
    prs = Presentation(deck_base.resoudre_base(BASE))
    return [f"id:{deck_draw.slide_par_titre(prs, t).slide_id}" for t in TITRES]


_I = dict(zip(TITRES, _ids(), strict=True))
ETAPES = [
    {"declarer": [_I[T_COND]], "f": conditions, "nouvelles_max": 0, "nom": "cinq conditions : une phrase de sens par carte, etape de la boucle en pastille"},
]
