"""Delta V29 (base V28) : varier les FORMES de trois slides monotones (rangees de rectangles arrondis), meme texte, memes affirmations.

- « Risques et objections » : objection -> reponse en deux cartes reliees par une fleche, garde-fou en pilule a contour ;
- « Les alternatives sont des complements » : quatre colonnes a onglet reliees par un point cyan (au lieu d'un tableau a lignes) ;
- « Chaque enjeu cite trouve sa reponse » : carte d'enjeu -> noeud -> partie de l'offre, reliees par des traits (carte-reseau).
Usage (depuis docs/cadrage-ppt/) : py deck_delta/deck.py delta_V29
"""
import deck_base
import deck_draw
from forme_ground import (
    BLANC,
    CYAN,
    MUTED,
    NAVY,
    X0,
    A,
    S,
    carte,
    coche,
    forme,
    noeud,
    onglet,
    pilule,
    point_cyan,
    signature_cyan,
    trait,
    tx,
)
from pptx import Presentation

BASE = "V28"
NOTE = "V29 : formes variees sur trois slides (objections en fleches, alternatives en colonnes a onglet, enjeux en carte-reseau)"
OPS = []

T_OBJ = "Risques et objections : ce que nous répondons, ce que nous mesurons"
T_ALT = "Les alternatives sont des compléments que l'offre intègre"
T_ENJ = "Chaque enjeu cité trouve sa réponse dans une partie de l'offre"


def _slide(prs, titre):
    return deck_draw.slide_par_titre(prs, titre)


def _retirer(s):
    """Retire le corps (tout ce qui est sous y=88 pt), garde titre, navigation, surtitre et etiquette d'etat."""
    for sh in list(s.shapes):
        if sh.is_placeholder or sh.name.startswith("nav-") or sh.top < 88 * 12700:
            continue
        sh._element.getparent().remove(sh._element)


def _textes(s):
    """[(left_pt, top_pt, texte)] des zones de texte du corps."""
    return sorted((round(sh.left / 12700), round(sh.top / 12700), sh.text_frame.text) for sh in s.shapes
                  if sh.has_text_frame and sh.text_frame.text.strip() and sh.top >= 88 * 12700 and not sh.name.startswith("nav-"))


# ---------------------------------------------------------------- objections : objection -> reponse -> garde-fou
def objections(prs):
    s = _slide(prs, T_OBJ)
    tt = _textes(s)
    heads = [t for (_, y, t) in tt if y < 100]
    rows = {}
    for x, y, t in tt:
        if 100 <= y < 340:
            rows.setdefault(round((y - 110) / 46), {})["o" if x < 150 else "r" if x < 400 else "g"] = t
    note = [t for (_, y, t) in tt if y >= 340][0]
    _retirer(s)
    signature_cyan(s)
    for (x, w), h_ in zip(((45, 185), (256, 240), (508, 151)), heads, strict=True):
        pilule(s, x, 95, w, 17, h_, "navy", 9)
    for r, y0 in enumerate(sorted(rows)):
        d = rows[y0]
        y = 118 + r * 46
        forme(s, S.ROUNDED_RECTANGLE, 45, y, 185, 42, NAVY, None, adj=0.33)
        tx(s, 57, y, 163, 42, [[(d["o"], 10, True, BLANC)]], A.MIDDLE)
        forme(s, S.RIGHT_ARROW, 234, y + 14, 18, 14, CYAN, NAVY, lw=0.75)
        carte(s, 256, y, 240, 42, 14)
        tx(s, 266, y, 220, 42, [[(d["r"], 9.5, False, NAVY)]], A.MIDDLE)
        trait(s, 496, y + 21, 508, y + 21, 1)
        pilule(s, 508, y + 6, 151, 30, d["g"], "contour", 9)
    tx(s, X0, 348, 614, 12, [[(note, 9, False, MUTED)]])


# ---------------------------------------------------------------- alternatives : quatre colonnes a onglet
def alternatives(prs):
    s = _slide(prs, T_ALT)
    tt = _textes(s)
    heads = [t for (_, y, t) in tt if 88 <= y < 100]
    rows = {}
    for x, y, t in tt:
        if 100 <= y < 320:
            rows.setdefault(round((y - 110) / 51), {})["n" if x < 150 else "a" if x < 400 else "j"] = t
    concl = [t for (x, y, t) in tt if y >= 320 and x > 80][0]
    _retirer(s)
    signature_cyan(s)
    W, G = 144, 12
    for k in sorted(rows):
        d = rows[k]
        x = X0 + k * (W + G)
        onglet(s, x, 98, W, 226, d["n"], 10.5)
        if k < 3:
            point_cyan(s, x + W + G / 2, 98 + 24)
        tx(s, x + 12, 152, W - 24, 12, [[(heads[1], 9.5, True, MUTED)]])
        tx(s, x + 12, 165, W - 24, 40, [[(d["a"], 10, False, NAVY)]])
        tx(s, x + 12, 210, W - 24, 12, [[(heads[2], 9.5, True, MUTED)]])
        tx(s, x + 12, 223, W - 24, 96, [[(d["j"], 10, False, NAVY)]])
    forme(s, S.ROUNDED_RECTANGLE, X0, 332, 614, 28, BLANC, NAVY, adj=0.5, lw=1.0)
    coche(s, X0 + 20, 346, 18)
    tx(s, X0 + 38, 332, 560, 28, [[(concl, 10, True, NAVY)]], A.MIDDLE)


# ---------------------------------------------------------------- enjeux : carte-reseau enjeu -> noeud -> partie de l'offre
ORDRE_CIBLES = ["Contexte et enjeux", "Nos convictions", "Notre approche", "Démarche", "Démarche détaillée", "Dispositif et prix"]


def enjeux(prs):
    s = _slide(prs, T_ENJ)
    tt = _textes(s)
    heads = [t for (_, y, t) in tt if y < 100]
    rows = {}
    for x, y, t in tt:
        if y >= 110:
            rows.setdefault(round((y - 110) / 34), {})["e" if x < 150 else "r" if x < 400 else "c"] = t
    _retirer(s)
    signature_cyan(s)
    lignes = [rows[y] for y in sorted(rows)]
    pilule(s, 45, 95, 150, 17, heads[0], "navy", 9)
    pilule(s, 215, 95, 150, 17, heads[1], "navy", 9)
    pilule(s, 540, 95, 119, 17, heads[2], "navy", 9)
    cy = {c: 134 + i * 41 for i, c in enumerate(ORDRE_CIBLES)}
    for r, d in enumerate(lignes):
        y = 118 + r * 34
        yc = y + 15
        trait(s, 430, yc, 532, cy[d["c"]], 1)
    for r, d in enumerate(lignes):
        y = 118 + r * 34
        carte(s, 45, y, 380, 30, 12)
        tx(s, 57, y, 150, 30, [[(d["e"], 9.5, True, NAVY)]], A.MIDDLE)
        tx(s, 215, y, 202, 30, [[(d["r"], 9.5, False, NAVY)]], A.MIDDLE)
        point_cyan(s, 430, y + 15, 10)
    for c, yc in cy.items():
        noeud(s, 532, yc, 14)
        pilule(s, 544, yc - 13, 115, 26, c, "navy", 9)


def retouche(prs):
    objections(prs)
    alternatives(prs)
    enjeux(prs)


def _ids():
    prs = Presentation(deck_base.resoudre_base(BASE))
    out = []
    for t in (T_OBJ, T_ALT, T_ENJ):
        out.append(f"id:{_slide(prs, t).slide_id}")
    return out


ETAPES = [{"declarer": _ids(), "f": retouche, "nouvelles_max": 0, "nom": "formes variees : objections, alternatives, enjeux"}]
