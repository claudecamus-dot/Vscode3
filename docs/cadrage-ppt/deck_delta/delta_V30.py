"""Delta V30 (base V29) : vocabulaire de formes de Vscode9 (forme_v9.py) sur neuf slides, memes mots, memes tailles de texte.

- Ouverture (trois temps) : entetes en pilules navy / cyan / slate, cartes de la reponse en PALE, chevrons cyan, le tout sur panneau gris ;
- Guichet Infra : quatre carres numerotes cyan sans bord de carte, sur panneau gris ;
- Reussir : cinq cartes round2DiagRect blanches + la proposition en cyan, sur panneau gris ;
- Problemes 1 a 5 / 6 a 10 : cartes round2DiagRect, numeros « n / 10 » en carres cyan ;
- Fiches de phase (2 slides) : bandeau navy (phase affichee), cartes round2DiagRect, bandeau gris en pied ;
- corrections V29 : Risques et objections (note descendue, cartes plus basses), Alternatives (cartes a la hauteur du contenu le plus long).
Usage (depuis docs/cadrage-ppt/) : py deck_delta/deck.py delta_V30
"""
import deck_base
import deck_draw
from forme_v9 import (
    BLANC,
    CYAN,
    LINE,
    NAVY,
    PALE,
    PANEL,
    SLATE,
    avant,
    chevron_sep,
    deplacer,
    forme,
    panneau_gris,
    par_id,
    restyle,
    supprimer,
    texte_couleur,
)
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE as S
from pptx.enum.text import MSO_ANCHOR as A

BASE = "V29"
NOTE = "V30 : formes Vscode9 (pilules, panneaux gris, carres cyan, round2DiagRect, bandeaux) sur 9 slides ; corrections slides risques et alternatives"
OPS = []

T_2 = "En trois temps et trois engagements, votre Infra passe du guichet au produit"
T_5 = "Le guichet Infra atteint ses limites et l'IA accentue la pression"
T_19 = "Réussir : cinq conditions que nous posons avant de commencer"
T_38 = "Risques et objections : ce que nous répondons, ce que nous mesurons"
T_43 = "Problèmes 1 à 5 : chacun trouve son apport et son indicateur"
T_44 = "Problèmes 6 à 10 : chacun trouve son apport et son indicateur"
T_45 = "Les alternatives sont des compléments que l'offre intègre"
T_49 = "Fiche de phase : l'Assessment flash fixe la référence et choisit le pilote"
T_50 = "Fiche de phase type, appliquée au pilote : un gabarit pour chaque phase"
TITRES = (T_2, T_5, T_19, T_38, T_43, T_44, T_45, T_49, T_50)


def _s(prs, t):
    return deck_draw.slide_par_titre(prs, t)


# ---------------------------------------------------------------- slide 2
def ouverture(prs):
    s = _s(prs, T_2)
    b = par_id(s)
    for pid, tid, col, txt in ((3, 4, NAVY, BLANC), (5, 6, CYAN, NAVY), (7, 8, SLATE, BLANC)):
        restyle(b[pid], fill=col, ligne=None)
        texte_couleur(b[tid], txt)
    for pid in (13, 17, 21):
        restyle(b[pid], fill=PALE)
    for pid in (9, 10):
        o = b[pid]
        x, y, w, h = (v / 12700 for v in (o.left, o.top, o.width, o.height))
        supprimer(o)
        chevron_sep(s, x, y, w, h)
    panneau_gris(s, 37, 93, 630, 270)


# ---------------------------------------------------------------- slide 5
def guichet(prs):
    s = _s(prs, T_5)
    b = par_id(s)
    for card, ov, num in ((5, 6, 7), (11, 12, 13), (17, 18, 19), (23, 24, 25)):
        supprimer(b[card])
        restyle(b[ov], prst="roundRect", adj=0.22, fill=CYAN, ligne=None)
        texte_couleur(b[num], NAVY)
    panneau_gris(s, 37, 140, 630, 105)


# ---------------------------------------------------------------- slide 19
def conditions(prs):
    s = _s(prs, T_19)
    b = par_id(s)
    for body, head in ((5, 51), (9, 53), (12, 55), (15, 57), (18, 59)):
        e, c = b[head], b[body]
        bas = c.top + c.height
        deplacer(c, y=e.top / 12700, h=(bas - e.top) / 12700)
        restyle(c, prst="round2DiagRect", adj=0.08, fill=BLANC, ligne=LINE)
        restyle(e, prst="rect", fill=None, ligne=None)
        texte_couleur(e, NAVY)
    restyle(b[21], prst="round2DiagRect", adj=0.08, fill=CYAN, ligne=None)
    texte_couleur(b[24], NAVY)
    panneau_gris(s, 37, 133, 630, 225)


# ---------------------------------------------------------------- slides 43 et 44
def problemes(prs, titre):
    s = _s(prs, titre)
    b = par_id(s)
    for base in (56, 60, 64, 68, 72):
        corps, ent, pas, txt = b[base], b[base + 1], b[base + 2], b[base + 3]
        restyle(corps, prst="round2DiagRect", adj=0.14, fill=BLANC, ligne=LINE)
        deplacer(corps, y=112, h=188)
        restyle(pas, prst="roundRect", adj=0.25, fill=CYAN, ligne=None)
        texte_couleur(pas, NAVY)
        deplacer(pas, x=corps.left / 12700 + 9, y=120, w=56, h=20)
        restyle(ent, prst="rect", fill=None, ligne=None)
        texte_couleur(ent, NAVY)
        ent.text_frame.vertical_anchor = A.TOP
        deplacer(ent, y=144, h=42)
        deplacer(txt, y=190, h=105)


def p43(prs):
    problemes(prs, T_43)


def p44(prs):
    problemes(prs, T_44)


# ---------------------------------------------------------------- slides 49 et 50
def fiche(prs, titre):
    s = _s(prs, titre)
    b = par_id(s)
    for pid in (18, 22, 26, 30, 34):
        restyle(b[pid], prst="round2DiagRect", adj=0.12, fill=BLANC, ligne=LINE)
    band = forme(s, S.ROUNDED_RECTANGLE, 45, 133, 614, 27, NAVY, None, adj=0.3)
    avant(b[15], band)
    deplacer(b[15], x=55, y=133, h=27)
    b[15].text_frame.vertical_anchor = A.MIDDLE
    texte_couleur(b[15], BLANC)
    deplacer(b[16], x=513)
    deplacer(b[17], x=516)
    pied = forme(s, S.ROUNDED_RECTANGLE, 45, 344, 614, 18, PANEL, None, adj=0.3)
    avant(b[38], pied)
    deplacer(b[38], x=53, y=344, w=598, h=18)
    b[38].text_frame.vertical_anchor = A.MIDDLE


def p49(prs):
    fiche(prs, T_49)


def p50(prs):
    fiche(prs, T_50)


# ---------------------------------------------------------------- slide 38 : note qui ne touche plus la derniere carte
def objections(prs):
    s = _s(prs, T_38)
    for sh in s.shapes:
        if sh.name.startswith("nav-") or sh.is_placeholder:
            continue
        top, h = sh.top / 12700, sh.height / 12700
        if 118 <= top < 344:
            k = int((top - 118) // 46)
            extra = 0 if round(h) == 42 else 2
            deplacer(sh, y=top - 4 * k - extra, h=38 if round(h) == 42 else None)
        elif sh.has_text_frame and round(top) == 348:
            deplacer(sh, y=336)


# ---------------------------------------------------------------- slide 45 : cartes a la hauteur du contenu le plus long
def alternatives(prs):
    s = _s(prs, T_45)
    for sh in s.shapes:
        top, h = sh.top / 12700, sh.height / 12700
        if round(top) == 98 and round(h) == 226:
            deplacer(sh, h=H45)
        elif round(top) == 223 and round(h) == 96:
            deplacer(sh, h=H45 - 131)
        elif top >= 332 and not sh.name.startswith("nav-") and not sh.is_placeholder:
            deplacer(sh, y=top - (332 - (98 + H45 + 8)))


H45 = 216

def retouche(prs):
    ouverture(prs)
    guichet(prs)
    conditions(prs)
    p43(prs)
    p44(prs)
    p49(prs)
    p50(prs)
    objections(prs)
    alternatives(prs)


def _ids():
    prs = Presentation(deck_base.resoudre_base(BASE))
    return [f"id:{_s(prs, t).slide_id}" for t in TITRES]


ETAPES = [{"declarer": _ids(), "f": retouche, "nouvelles_max": 0, "nom": "formes Vscode9 sur neuf slides"}]
