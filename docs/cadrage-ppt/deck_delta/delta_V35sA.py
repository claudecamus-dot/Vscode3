"""Delta V35sA (base V34 + lot g) : slide d'ouverture aeree, introduction des convictions, titres des convictions 2 a 6, conviction 1 (appropriation).

- « Votre demande, notre reponse en trois temps » : espace libere sous le titre reutilise pour aerer cartes / chevron / panneau / bandeau d'engagements ;
  premier engagement reformule (vision claire et partagee), « T0 / T1 » remplaces par des mots simples ;
- « Treize convictions en quatre themes » : titre = idee principale (couverture complete), bandeau « approche a 360° », grille remontee et aeree ;
- titres des deux slides « Trois convictions... » et « Deux convictions de plus... » : ils disent pourquoi les convictions vont ensemble ;
- « Conviction 1 » : la carte du milieu devient « Une culture que chacun s'approprie » (carte navy, quatre pastilles : qui s'approprie), plus de T0/T1.
Les phrases retirees vont dans les notes de la slide. Navigation, points de progression, filets et numeros de page ne sont pas touches.
Usage (depuis docs/cadrage-ppt/) : py deck_delta/deck.py delta_V35sA --base C:/tmp/deck-v35/V35g.pptx --sortie C:/tmp/deck-v35-sA/V35sA.pptx --sans-rendu
"""
import deck_base
import deck_draw
from forme_v9 import BLANC, CYAN, NAVY, PANEL, S, forme, tx
from forme_v9 import deplacer as mv
from pptx import Presentation
from pptx.enum.text import MSO_ANCHOR as A
from pptx.enum.text import PP_ALIGN as P
from pptx.util import Pt

BASE = "V34"
NOTE = "V35sA : ouverture aeree, intro des convictions (360°), titres des convictions 2 a 6, conviction 1 (appropriation de tous)"
OPS = []

NB = "\u00a0"
T_OUVERTURE = "Votre demande, notre réponse en trois temps" + NB + ": du guichet au produit"
T_GRILLE = "Treize convictions en quatre thèmes, déclinées une à une ensuite"
T_C1 = "Conviction 1" + NB + ": le mode produit est d'abord une culture, pas un outil"
T_C234 = "Trois convictions, chacune vérifiée par un critère et un chantier"
T_C56 = "Deux convictions de plus, vérifiées de la même façon"
TITRES = (T_OUVERTURE, T_GRILLE, T_C1, T_C234, T_C56)

N_GRILLE = "Treize convictions couvrent toute la transformation de l'Infra"
N_C234 = "Du besoin à la priorité" + NB + ": douleur mesurée, porteur, faits d'abord"
N_C56 = "Progrès et gain de l'IA" + NB + ": mesurés puis vérifiés, jamais promis"
BANDEAU_360 = "Une approche à 360°" + NB + ": treize convictions, de la culture au RUN et à l'IA"
ENGAGEMENT_1 = "Une vision claire et partagée, pour une trajectoire alignée avec les enjeux"


def _d(s):
    return {sh.shape_id: sh for sh in s.shapes}


def _run(sh, texte, p=0):
    """Fixe le texte du premier run du paragraphe p (les autres runs sont retires) ; ne touche a rien si identique."""
    para = sh.text_frame.paragraphs[p]
    runs = para.runs
    if len(runs) == 1 and runs[0].text == texte:
        return
    runs[0].text = texte
    for r in runs[1:]:
        r._r.getparent().remove(r._r)


def _taille(sh, sz, p=None):
    for k, para in enumerate(sh.text_frame.paragraphs):
        if p is None or k == p:
            for r in para.runs:
                r.font.size = Pt(sz)


def _couleur(sh, rgb):
    for para in sh.text_frame.paragraphs:
        for r in para.runs:
            r.font.color.rgb = rgb


def _supprimer_para(sh, p):
    el = sh.text_frame.paragraphs[p]._p
    el.getparent().remove(el)


def _notes(s, texte):
    s.notes_slide.notes_text_frame.text = texte


def _titre(s, texte):
    _run(s.shapes.title, texte)


# ================================================================ 1. Ouverture
def ouverture(prs):
    s = deck_draw.slide_par_titre(prs, T_OUVERTURE)
    d = _d(s)
    # carte Contexte / Demande
    mv(d[32], y=84, h=204)
    mv(d[33], y=186)
    mv(d[34], y=98, h=176)
    for ids, dy in (((35, 36, 37), -14.0), ((40, 41, 42), -15.7)):
        for i in ids:
            mv(d[i], y=d[i].top / 12700 + dy)
    mv(d[38], y=150)
    mv(d[43], y=251.3)
    for i, y in ((39, 90), (44, 192)):
        mv(d[i], y=y, w=148, h=90)
        _taille(d[i], 11, p=1)
    # chevron et panneau navy
    mv(d[45], x=295, y=176)
    mv(d[46], x=315, y=84, w=344, h=204)
    mv(d[47], x=333, y=98, w=308)
    mv(d[48], x=333, y=117)
    mv(d[49], x=349.25, y=151, h=112)
    for k, (oval, num, texte) in enumerate(((50, 51, 52), (53, 54, 55), (56, 57, 58))):
        y = 134 + k * 56
        mv(d[oval], x=333, y=y)
        mv(d[num], x=333, y=y)
        mv(d[texte], x=381, y=y - 1, w=262, h=50)
    _run(d[52], "Assessment flash" + NB + ": état des lieux de départ, choix d'un pilote.", p=1)
    _run(d[55], "Pilote Produit + IA" + NB + ": résultats mesurés et décision du client.", p=1)
    # bandeau d'engagements
    mv(d[59], y=308, h=52)
    mv(d[60], y=321)
    mv(d[61], y=321)
    for dot, texte, x_dot, x_txt, w in ((62, 63, 169, 183, 150), (64, 65, 343, 357, 150), (66, 67, 517, 531, 120)):
        mv(d[dot], x=x_dot, y=330)
        mv(d[texte], x=x_txt, y=312, w=w, h=44)
        _taille(d[texte], 10.5)
    _run(d[63], ENGAGEMENT_1)
    _notes(s, "Phrase retirée du bandeau « NOS ENGAGEMENTS »" + NB + ": « Aucun ROI promis" + NB + ": référence de départ, résultat mesuré »"
              " (formulation d'origine avec les repères techniques de mesure, remplacés par des mots simples). "
              "« Aucun ROI promis » reste énoncé sur d'autres slides du deck.")


# ================================================================ 2. Grille des treize convictions
def grille(prs):
    s = deck_draw.slide_par_titre(prs, T_GRILLE)
    d = _d(s)
    ancien_bandeau = d[74].text_frame.text
    _titre(s, N_GRILLE)
    mv(d[72], y=72, h=294)
    mv(d[73], y=80, h=24)
    mv(d[74], y=80, h=24)
    _run(d[74], BANDEAU_360)
    _taille(d[74], 12)
    for sh in s.shapes:
        if sh.shape_id in (2, 72, 73, 74, 146) or sh.name.startswith("nav-"):
            continue
        mv(sh, y=sh.top / 12700 - 10)
    mv(d[146], y=343, h=16)
    _notes(s, "Phrase retirée du bandeau" + NB + ": « " + ancien_bandeau + " » (la vérification une à une reste portée par la ligne « Comment lire la suite »)."
              " Ancien titre" + NB + ": « " + T_GRILLE + " »" + NB + "; il décrivait la structure de la slide, le nouveau dit l'idée (une approche à 360°).")


# ================================================================ 3. Conviction 1 : appropriation de tous
ACTEURS = ("Sponsor", "Managers", "Équipes Infra", "Consommateurs")


def conviction1(prs):
    s = deck_draw.slide_par_titre(prs, T_C1)
    d = _d(s)
    # trois cartes : 120 / 197 / 120, ecart 16
    for carte, titre, sep, corps, x, w in ((107, 108, 109, 111, 190, 120), (112, 113, 114, 116, 326, 197), (117, 118, 119, 120, 539, 120)):
        mv(d[carte], x=x, w=w)
        mv(d[titre], x=x + 8, w=w - 16)
        if carte == 107:
            mv(d[titre], x=x + 15, w=90)
        mv(d[sep], x=x + 12, w=w - 24)
        mv(d[corps], x=x + 10, w=w - 20)
    mv(d[110], x=313)
    mv(d[115], x=526)
    # carte du milieu : accent navy
    d[112].fill.solid()
    d[112].fill.fore_color.rgb = NAVY
    d[114].fill.solid()
    d[114].fill.fore_color.rgb = CYAN
    _run(d[113], "Une culture que chacun s'approprie")
    _couleur(d[113], BLANC)
    _run(d[116], "La culture, c'est l'appropriation de tous.")
    _supprimer_para(d[116], 1)
    _couleur(d[116], BLANC)
    mv(d[116], h=40)
    for k, nom in enumerate(ACTEURS):
        x = 338 + (k % 2) * 90
        y = 194 + (k // 2) * 26
        forme(s, S.ROUNDED_RECTANGLE, x, y, 83, 20, PANEL, None, adj=0.5)
        tx(s, x, y, 83, 20, [[(nom, 9.5, True, NAVY)]], A.MIDDLE, P.CENTER)
    _run(d[120], "La valeur est mesurée avant, puis après.", p=1)
    _notes(s, "Retiré de la slide pour faire place à l'appropriation par tous" + NB + ": « Une règle posée d'en haut » (titre de la carte du milieu)"
              " et « Chaque investissement est discuté en termes de valeur pour l'usager. Le sponsor porte ce message. »"
              " (le message du sponsor reste dans le chantier, la valeur pour l'usager dans le critère observable).")


# ================================================================ 4 et 5. Titres
def titre_c234(prs):
    s = deck_draw.slide_par_titre(prs, T_C234)
    _titre(s, N_C234)
    _notes(s, "Ancien titre" + NB + ": « " + T_C234 + " »" + NB + "; le nouveau dit pourquoi ces trois convictions vont ensemble (du besoin du consommateur à la décision de priorité).")


def titre_c56(prs):
    s = deck_draw.slide_par_titre(prs, T_C56)
    _titre(s, N_C56)
    _notes(s, "Ancien titre" + NB + ": « " + T_C56 + " »" + NB + "; le nouveau dit ce que les deux convictions ont en commun (mesurer puis vérifier, jamais promettre).")


def _ids():
    prs = Presentation(deck_base.resoudre_base(BASE))
    return [f"id:{deck_draw.slide_par_titre(prs, t).slide_id}" for t in TITRES]


_I = dict(zip(TITRES, _ids(), strict=True))
ETAPES = [
    {"declarer": [_I[T_OUVERTURE]], "f": ouverture, "nouvelles_max": 0, "nom": "ouverture aeree, engagement reformule, T0/T1 en mots simples"},
    {"declarer": [_I[T_GRILLE]], "f": grille, "nouvelles_max": 0, "nom": "grille des convictions : titre, bandeau 360 degres, aeree"},
    {"declarer": [_I[T_C1]], "f": conviction1, "nouvelles_max": 0, "nom": "conviction 1 : appropriation de tous"},
    {"declarer": [_I[T_C234]], "f": titre_c234, "nouvelles_max": 0, "nom": "titre convictions 2 a 4"},
    {"declarer": [_I[T_C56]], "f": titre_c56, "nouvelles_max": 0, "nom": "titre convictions 5 et 6"},
]
