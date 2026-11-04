"""Delta V32b (base V31) : trois slides du chapitre « Contexte et enjeux » refaites sur le vocabulaire d'un exemple de reference (cartes, pictogrammes ronds, matrice a lignes arrondies).

- Guichet Infra : texte divise par deux. Quatre cartes arrondies a pictogramme rond qui chevauche le bord, bandeau navy (un verbatim + les deux chiffres Gartner) ;
  les deux verbatims retires de la slide passent dans les notes de la slide ;
- Infra as a Product : AVANT en colonne etroite de pastilles, APRES en quatre cartes a onglet (pictogramme + titre), exemple en trois etapes arrondies ;
- Six leviers / cinq resultats : panneau « LEVIERS » a pictogrammes, cinq pastilles d'entete, une ligne-pilule par levier, un marqueur identique par lien (grille stricte).
Memes mots que la V31 (sauf les coupes de la slide Guichet) ; la couleur ne porte pas le sens : marqueurs de meme teinte, differencies par la position.
Pictogrammes : famille de forme_ground.picto (trait navy, remplissage cyan), un meme pictogramme = un meme concept sur les trois slides.
Usage (depuis docs/cadrage-ppt/) : py deck_delta/deck.py delta_V32b --base V31 --sortie C:/tmp/deck-v32-b/V32b.pptx
"""
import re

import deck_base
import deck_draw
from forme_ground import picto
from forme_v9 import (
    BLANC,
    CYAN,
    LINE,
    NAVY,
    PANEL,
    SLATE,
    deplacer,
    forme,
    par_id,
    pt,
    supprimer,
    tx,
)
from lxml import etree
from pptx import Presentation
from pptx.enum.dml import MSO_LINE
from pptx.enum.shapes import MSO_CONNECTOR
from pptx.enum.shapes import MSO_SHAPE as S
from pptx.enum.text import MSO_ANCHOR as A
from pptx.enum.text import PP_ALIGN as P
from pptx.util import Pt

NS_A = "http://schemas.openxmlformats.org/drawingml/2006/main"
BASE = "V31"
NOTE = "V32b : slides Guichet (texte reduit de moitie), Infra as a Product (cartes a onglet) et Six leviers (matrice a lignes arrondies) sur le vocabulaire de l'exemple de reference"
OPS = []

T_5 = "Le guichet Infra atteint ses limites et l'IA accentue la pression"
T_6 = "Infra as a Product : des capacités pensées pour leurs consommateurs"
T_7 = "Six leviers au service de cinq résultats métier"
TITRES = (T_5, T_6, T_7)
NB = "\xa0"
GRIS_CLAIR = LINE  # texte secondaire sur fond navy

# Un pictogramme = un concept, sur les trois slides.
PICTO = {
    "delivery": "horloge", "experience": "personnes", "organisation": "grille", "valeur": "jauge",
    "fiabilite": "coche", "strategie": "cible", "catalogue": "classeurs", "ownership": "coche",
}


def _s(prs, t):
    return deck_draw.slide_par_titre(prs, t)


def _txt(sh):
    return sh.text_frame.text


def _garder(s, ids):
    """Garde titre, navigation, surtitre (« 01 · ... ») et les formes demandees ; supprime le reste."""
    for sh in list(s.shapes):
        if sh.is_placeholder or sh.name.startswith("nav-") or sh.shape_id in ids:
            continue
        if sh.has_text_frame and re.match(r"^\d\d · ", _txt(sh)):
            continue
        supprimer(sh)


def _sans_ombre(sh):
    """Supprime l'ombre de theme d'un connecteur ou d'une forme (effectLst vide)."""
    sp = sh._element.spPr
    for e in sp.findall(f"{{{NS_A}}}effectLst"):
        sp.remove(e)
    etree.SubElement(sp, f"{{{NS_A}}}effectLst")


def _picto(s, genre, cx, cy, d, disque=True, ratio=0.58, sans_ombre=False):
    """Pictogramme de forme_ground, epaisseur de trait proportionnelle a la taille ; disque blanc a bord navy derriere."""
    if disque:
        forme(s, S.OVAL, cx - d / 2, cy - d / 2, d, d, BLANC, NAVY, lw=1.0)
    n0 = len(s.shapes)
    pd = d * ratio
    picto(s, genre, cx, cy, pd)
    f = pd / 64.0
    for sh in list(s.shapes)[n0:]:
        try:
            w = sh.line.width.pt if sh.line.width else 1.5
            sh.line.width = int(max(0.6, w * f * 1.7) * 12700)
        except Exception:
            pass
        if sans_ombre:
            _sans_ombre(sh)


def _italique(tb):
    for p in tb.text_frame.paragraphs:
        for r in p.runs:
            r.font.italic = True
    return tb


# ---------------------------------------------------------------- slide 5
def guichet(prs):
    s = _s(prs, T_5)
    b = par_id(s)
    cols = [tuple(_txt(b[i]) for i in ids) for ids in ((8, 9, 10), (14, 15, 16), (20, 21, 22), (26, 27, 28))]
    chiffres = [(_txt(b[38]), _txt(b[39])), (_txt(b[41]), _txt(b[42]))]
    verbatims = [_txt(b[i]) for i in (31, 33, 35)]
    source = b[43]
    kick = [sh for sh in s.shapes if sh.has_text_frame and re.match(r"^\d\d · ", _txt(sh))]
    _garder(s, {3, 4, 43} | {k.shape_id for k in kick})

    # phrase d'accroche en une ligne
    r = b[4].text_frame.paragraphs[0].runs
    r[2].text = f" plus qu'elles ne pilotent la valeur{NB}; l'IA peut l'amplifier."
    deplacer(b[3], h=14)
    deplacer(b[4], h=16)

    # quatre cartes, pictogramme rond sur le bord haut
    pictos = ("delivery", "experience", "organisation", "valeur")
    W, G, Y, H = 146, 10, 144, 118
    for k, (titre, ligne, levier) in enumerate(cols):
        x = 45 + k * (W + G)
        forme(s, S.ROUNDED_RECTANGLE, x, Y, W, H, BLANC, NAVY, adj=0.1, lw=0.75)
        _picto(s, PICTO[pictos[k]], x + W / 2, Y, 38)
        tx(s, x + 8, Y + 24, W - 16, 30, [[(titre, 11.5, True, NAVY)]], A.MIDDLE, P.CENTER)
        tx(s, x + 10, Y + 55, W - 20, 28, [[(ligne, 10, False, NAVY)]], A.TOP, P.CENTER)
        forme(s, S.ROUNDED_RECTANGLE, x + 10, Y + 87, W - 20, 24, CYAN, None, adj=0.5)
        tx(s, x + 14, Y + 87, W - 28, 24, [[(levier, 9, True, NAVY)]], A.MIDDLE, P.CENTER)

    # bandeau navy : verbatim a gauche, chiffres a droite
    BY, BH = 270, 76
    forme(s, S.ROUNDED_RECTANGLE, 45, BY, 614, BH, NAVY, None, adj=0.12)
    tx(s, 61, BY + 9, 260, 12, [[("VERBATIM RECUEILLI" + NB + "— ILLUSTRATIF", 8.5, True, GRIS_CLAIR)]])
    _italique(tx(s, 61, BY + 26, 262, 44, [[(verbatims[0], 12, False, BLANC)]], A.TOP))
    forme(s, S.RECTANGLE, 340, BY + 10, 0.75, BH - 20, GRIS_CLAIR, None)
    tx(s, 356, BY + 9, 290, 12, [[("LA PRESSION MONTE AVEC L'IA" + NB + "— PRÉVISIONS GARTNER", 8.5, True, GRIS_CLAIR)]])
    for k, (chiffre, cap) in enumerate(chiffres):
        y = BY + 25 + k * 26
        cap = re.sub(r"\s*—\s*(prévision|projection) Gartner.*$", "", cap).rstrip(". ")
        tx(s, 356, y, 56, 24, [[(chiffre, 18, True, BLANC)]], A.MIDDLE)
        tx(s, 414, y, 233, 24, [[(cap, 10, False, BLANC)]], A.MIDDLE)

    deplacer(source, x=45, y=352, w=614, h=14.4)

    # les deux verbatims retires de la slide sont conserves dans les notes
    notes = s.notes_slide.notes_text_frame
    notes.text = ("Verbatims recueillis (illustratifs), retirés de la slide pour l'alléger :\n"
                  f"- {verbatims[1]}\n- {verbatims[2]}\n"
                  f"Verbatim conservé sur la slide : {verbatims[0]}\n"
                  "Légendes complètes des deux chiffres : "
                  + " ; ".join(f"{c} {d}" for c, d in chiffres))


# ---------------------------------------------------------------- slide 6
def produit(prs):
    s = _s(prs, T_6)
    b = par_id(s)
    avant_titre = b[8].text_frame.paragraphs[0].text
    avant = [p.text.lstrip("– -").strip() for p in b[8].text_frame.paragraphs[1:]]
    apres = [(b[i].text_frame.paragraphs[0].text, b[i].text_frame.paragraphs[1].text) for i in (14, 16, 18, 20)]
    label = _txt(b[21])
    etapes = [(_txt(b[i]), _txt(b[j])) for i, j in ((23, 24), (26, 27), (29, 30))]
    pied = b[31]
    kick = [sh for sh in s.shapes if sh.has_text_frame and re.match(r"^\d\d · ", _txt(sh))]
    _garder(s, {3, 4, 31} | {k.shape_id for k in kick})

    deplacer(b[3], h=14)
    deplacer(b[4], h=16)
    X_AV, W_AV, X_AP, W_AP = 45, 112, 177, 482
    PY = 122
    # entetes en pastilles
    forme(s, S.ROUNDED_RECTANGLE, X_AV, PY, W_AV, 16, SLATE, None, adj=0.5)
    tx(s, X_AV, PY, W_AV, 16, [[("AVANT", 9, True, BLANC)]], A.MIDDLE, P.CENTER)
    forme(s, S.ROUNDED_RECTANGLE, X_AP, PY, W_AP, 16, NAVY, None, adj=0.5)
    tx(s, X_AP, PY, W_AP, 16, [[("APRÈS", 9, True, BLANC)]], A.MIDDLE, P.CENTER)
    CY0, CH, GAP = 142, 76, 5
    # AVANT : panneau gris etroit, pains en pastilles blanches
    haut = CH * 2 + GAP
    forme(s, S.ROUNDED_RECTANGLE, X_AV, CY0, W_AV, haut, PANEL, None, adj=0.07)
    tx(s, X_AV + 10, CY0 + 7, W_AV - 20, 16, [[(avant_titre, 10.5, True, NAVY)]], A.TOP)
    for k, t in enumerate(avant):
        y = CY0 + 28 + k * 31
        forme(s, S.ROUNDED_RECTANGLE, X_AV + 8, y, W_AV - 16, 27, BLANC, None, adj=0.3)
        tx(s, X_AV + 14, y, W_AV - 28, 27, [[(t, 9.5, False, NAVY)]], A.MIDDLE)
    # chevron
    forme(s, S.CHEVRON, X_AV + W_AV + 5, CY0 + haut / 2 - 11, 12, 22, CYAN, None, adj=0.35)
    # APRES : quatre cartes a onglet
    cw = (W_AP - 8) / 2
    genres = ("experience", "catalogue", "ownership", "valeur")
    for k, (titre, corps) in enumerate(apres):
        x = X_AP + (k % 2) * (cw + 8)
        y = CY0 + (k // 2) * (CH + GAP)
        forme(s, S.ROUNDED_RECTANGLE, x, y, cw, CH, BLANC, NAVY, adj=0.1, lw=0.75)
        forme(s, S.ROUND_2_SAME_RECTANGLE, x, y, cw, 28, PANEL, None, adj=0.3)
        _picto(s, PICTO[genres[k]], x + 20, y + 14, 25)
        tx(s, x + 40, y, cw - 50, 28, [[(titre, 12, True, NAVY)]], A.MIDDLE)
        tx(s, x + 12, y + 32, cw - 24, 40, [[(corps, 10, False, NAVY)]], A.TOP)
    # exemple en trois etapes
    EY = CY0 + haut + 7
    tx(s, 45, EY, 614, 11, [[(label, 8.5, True, SLATE)]], A.TOP)
    sw, gp = 186, 28
    for k, (t1, t2) in enumerate(etapes):
        x = 45 + k * (sw + gp)
        accent = k == 2
        forme(s, S.ROUNDED_RECTANGLE, x, EY + 13, sw, 27, CYAN if accent else NAVY, None, adj=0.3)
        tx(s, x, EY + 13, sw, 27, [[(t1, 10.5, True, NAVY if accent else BLANC)], [(t2, 9.5, False, NAVY if accent else BLANC)]], A.MIDDLE, P.CENTER)
        if k < 2:
            forme(s, S.CHEVRON, x + sw + (gp - 12) / 2, EY + 13 + 5, 12, 18, CYAN, None, adj=0.35)
    deplacer(pied, x=45, y=EY + 44, w=614, h=12)


# ---------------------------------------------------------------- slide 7
def lire_leviers(s):
    """Donnees de la slide 7 telle que la V31 les porte : entetes, (numero+nom, citation) par levier, liens (ligne, colonne) lus sur les ovales."""
    b = par_id(s)
    entetes = [_txt(b[i]) for i in (6, 8, 10, 12, 14)]
    lignes = []
    for i in (16, 20, 25, 29, 33, 37):
        runs = b[i].text_frame.paragraphs[0].runs
        lignes.append((runs[0].text.strip(), runs[1].text.strip()))
    ovals = [sh for sh in s.shapes if sh.name.startswith("Oval")]
    cols_x = [256 + 37.5 + k * 81.2 for k in range(5)]
    liens = set()
    for o in ovals:
        cx = (o.left + o.width / 2) / 12700
        cy = (o.top + o.height / 2) / 12700
        col = min(range(5), key=lambda k: abs(cols_x[k] - cx))
        row = int((cy - 184) // 28.7)
        assert abs(cols_x[col] - cx) < 8 and 0 <= row < 6, (cx, cy)
        liens.add((row, col))
    assert len(liens) == len(ovals) == 13, len(ovals)
    return entetes, lignes, sorted(liens)


GENRES_LEVIERS = ("experience", "delivery", "organisation", "valeur", "fiabilite", "strategie")


def leviers(prs):
    """Variante 1 : matrice a bandes de colonnes grises, marqueurs numerotes, pictogrammes de 30 pt, separateurs pointilles."""
    s = _s(prs, T_7)
    entetes, lignes, liens = lire_leviers(s)
    b = par_id(s)
    kick = [sh for sh in s.shapes if sh.has_text_frame and re.match(r"^\d\d · ", _txt(sh))]
    _garder(s, {3, 4} | {k.shape_id for k in kick})
    deplacer(b[3], h=33)

    X_P, W_P = 45, 224
    X0, CW, PAS = 279, 72, 77
    HY, HH = 140, 24
    RY, RH, RP = 167, 28, 31
    bas = RY + 5 * RP + RH
    # bandes de colonnes grises, sous les pastilles d'entete
    for k in range(5):
        forme(s, S.ROUNDED_RECTANGLE, X0 + k * PAS, HY + HH / 2, CW, bas + 4 - (HY + HH / 2), PANEL, None, adj=0.14)
    # panneau des leviers
    forme(s, S.ROUNDED_RECTANGLE, X_P, HY, W_P, bas + 4 - HY, BLANC, NAVY, adj=0.06, lw=0.75)
    forme(s, S.ROUNDED_RECTANGLE, X_P + 3, HY + 3, W_P - 6, HH - 6, PANEL, None, adj=0.5)
    tx(s, X_P + 3, HY + 3, W_P - 6, HH - 6, [[("LEVIERS", 10.5, True, NAVY)]], A.MIDDLE, P.CENTER)
    for k, t in enumerate(entetes):
        x = X0 + k * PAS
        forme(s, S.ROUNDED_RECTANGLE, x, HY, CW, HH, NAVY, None, adj=0.5)
        tx(s, x + 4, HY, CW - 8, HH, [[(t, 8.5 if len(t) > 18 else 9, True, BLANC)]], A.MIDDLE, P.CENTER)
    for r, ((nom, cit), g) in enumerate(zip(lignes, GENRES_LEVIERS, strict=True)):
        y = RY + r * RP
        forme(s, S.ROUNDED_RECTANGLE, X0, y, 4 * PAS + CW, RH, None, NAVY, adj=0.5, lw=0.9)
        _picto(s, PICTO[g], X_P + 23, y + RH / 2, 48, disque=False, ratio=0.583, sans_ombre=True)
        tx(s, X_P + 46, y, W_P - 52, RH, [[(nom, 10.5, True, NAVY)], [(cit, 9.5, False, SLATE)]], A.MIDDLE)
        if r < 5:
            c = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, pt(X_P + 10), pt(y + RH + (RP - RH) / 2), pt(X_P + W_P - 10), pt(y + RH + (RP - RH) / 2))
            c.line.color.rgb = SLATE
            c.line.width = Pt(0.75)
            c.line.dash_style = MSO_LINE.ROUND_DOT
            _sans_ombre(c)
    for (r, k) in liens:
        cx = X0 + k * PAS + CW / 2
        cy = RY + r * RP + RH / 2
        forme(s, S.OVAL, cx - 12, cy - 12, 24, 24, NAVY, None)
        tx(s, cx - 12, cy - 12, 24, 24, [[(str(r + 1), 10.5, True, BLANC)]], A.MIDDLE, P.CENTER)
    ly = bas + 8
    forme(s, S.OVAL, X0, ly, 10, 10, NAVY, None)
    tx(s, X0 + 15, ly - 1, 240, 12, [[("Lien principal, à confirmer", 9.5, False, SLATE)]], A.MIDDLE)


def retouche(prs):
    guichet(prs)
    produit(prs)
    leviers(prs)


def _ids():
    prs = Presentation(deck_base.resoudre_base(BASE))
    return [f"id:{_s(prs, t).slide_id}" for t in TITRES]


ETAPES = [{"declarer": _ids(), "f": retouche, "nouvelles_max": 0, "nom": "Guichet, Infra as a Product, Six leviers : formes de l'exemple de reference"}]
