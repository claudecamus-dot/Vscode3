"""Delta V43c (base V42) : reprises de composition alignées sur « Slides préformatées OCTO (1).pptx ».

Demande utilisateur du 2026-11-05 : « reprend les compositions ». La V42 reste intacte (nouveau fichier).
Constat mesuré avant d'écrire : les cartes des slides 23, 33, 34, 35, 37 sont DÉJÀ en round2DiagRect à filet navy 0,75 pt ;
le mapping qui les disait symétriques était faux. Restent, vraiment, par slide :
  17 : en-tête de tableau cyan -> navy, texte blanc (réf. sl. 139 : en-tête navy, cap cyan en pied) + cap cyan fin sous le tableau ;
  40 : en-tête cyan -> navy, texte blanc ; ligne « Sous-total » navy -> cyan, texte navy (réf. sl. 299) ;
  20 : 6e carte, seul grand aplat cyan du deck -> navy, texte blanc ; pilule PROPOSITION inversée (cyan, texte navy) ;
  28 : grande carte de droite roundRect -> round2DiagRect (même coin que les cartes de gauche) ;
  32 : l'illustration roadmap était une image rognée à droite (la source l'est : 1517 x 1050, 3e colonne coupée) et
       issue du kit de référence (licence non vérifiée) -> remplacée par une roadmap en formes natives (2 streams x 3 horizons, Feat 1 à 5).
Usage (depuis docs/cadrage-ppt/) : py deck_delta/deck.py delta_V43c --base V42 --sortie C:/tmp/deck-v43-c/V43c.pptx --sans-rendu
"""
import deck_base
import deck_draw
from forme_v9 import BLANC, CYAN, NAVY, deplacer, par_id, restyle, supprimer, texte_couleur
from forme_v26 import S, forme, tx
from forme_v9 import A as ANCRE
from forme_v9 import P as ALIGN
from pptx import Presentation
from pptx.dml.color import RGBColor as C

BASE = "V42"
NOTE = "V43c : reprises de composition (tableaux 17/40 en-tête navy, slide 20 accent navy, carte 28, roadmap native 32)"
OPS = []

PALE = C(0xCB, 0xF5, 0xF8)   # cyan tres clair (rampe de la roadmap)
MOYEN = C(0x66, 0xE4, 0xEA)  # cyan moyen


def _slide(prs, ident):
    return next(s for s in prs.slides if s.slide_id == ident)


def _id_rang(rang):
    prs = Presentation(deck_base.resoudre_base(BASE))
    return f"id:{prs.slides[rang - 1].slide_id}"


def s17(prs, sid):
    s = _slide(prs, sid)
    d = par_id(s)
    restyle(d[181], fill=NAVY)
    texte_couleur(d[182], BLANC)
    texte_couleur(d[183], BLANC)
    forme(s, S.RECTANGLE, 45, 366.5, 614, 3, CYAN, None)  # cap cyan fin en pied de tableau


def s40(prs, sid):
    s = _slide(prs, sid)
    d = par_id(s)
    restyle(d[62], fill=NAVY)
    for i in (63, 64, 65, 66):
        if i in d and d[i].has_text_frame:
            texte_couleur(d[i], BLANC)
    restyle(d[82], fill=CYAN)
    for i in (83, 84, 85, 86):
        if i in d and d[i].has_text_frame:
            texte_couleur(d[i], NAVY)


def s20(prs, sid):
    s = _slide(prs, sid)
    d = par_id(s)
    restyle(d[21], fill=NAVY)
    texte_couleur(d[24], BLANC)
    restyle(d[22], fill=CYAN)
    texte_couleur(d[23], NAVY)


def s28(prs, sid):
    s = _slide(prs, sid)
    d = par_id(s)
    restyle(d[65], prst="round2DiagRect", adj=0.05)


def s32(prs, sid):
    s = _slide(prs, sid)
    d = par_id(s)
    x0, y0, w, h = d[97].left / 12700, d[97].top / 12700, d[97].width / 12700, d[97].height / 12700
    supprimer(d[97])
    lab = 26                      # largeur de la colonne des streams
    bas = 22                      # hauteur de la ligne des horizons
    gx, gy = x0 + lab + 4, y0
    gw, gh = w - lab - 4, h - bas - 4
    forme(s, S.ROUND_2_DIAG_RECTANGLE, gx, gy, gw, gh, BLANC, NAVY, adj=0.05, lw=0.75)
    col = gw / 3
    # horizons cumulés : trois nappes de cyan de plus en plus soutenu
    forme(s, S.RECTANGLE, gx + col, gy + 1, gw - col - 1, gh - 2, PALE, None)
    forme(s, S.RECTANGLE, gx + 2 * col, gy + 1, col - 1, gh - 2, MOYEN, None)
    ligne = gy + gh / 2
    forme(s, S.RECTANGLE, gx + 1, ligne - 0.4, gw - 2, 0.8, NAVY, None)
    for k in (1, 2):
        forme(s, S.RECTANGLE, gx + k * col - 0.4, gy + 1, 0.8, gh - 2, NAVY, None)
    # streams (colonne de gauche) et horizons (ligne du bas), pilules navy
    for i, nom in enumerate(("Stream X", "Stream Y")):
        yy = gy + i * gh / 2 + 2
        forme(s, S.ROUNDED_RECTANGLE, x0, yy, lab, gh / 2 - 4, NAVY, None, adj=0.2)
        t = tx(s, x0, yy, lab, gh / 2 - 4, [[(nom, 9, True, BLANC)]], ANCRE.MIDDLE, ALIGN.CENTER)
        t.rotation = 270
        # un texte tourné est fragile : on le cale sur la hauteur, pas sur la largeur
        t.width, t.height = int((gh / 2 - 4) * 12700), int(lab * 12700)
        t.left = int((x0 + lab / 2 - (gh / 2 - 4) / 2) * 12700)
        t.top = int((yy + (gh / 2 - 4) / 2 - lab / 2) * 12700)
    for k, nom in enumerate(("Horizon 1", "Horizon 2", "Horizon 3")):
        px = gx + k * col + 2
        forme(s, S.ROUNDED_RECTANGLE, px, y0 + h - bas, col - 4, bas, NAVY, None, adj=0.5)
        tx(s, px, y0 + h - bas, col - 4, bas, [[(nom, 9, True, BLANC)]], ANCRE.MIDDLE, ALIGN.CENTER)
    # features : (libelle, colonne, ligne de 0 à 1 dans la hauteur)
    for nom, c, v in (("Feat 1", 0, 0.30), ("Feat 2", 1, 0.22), ("Feat 3", 2, 0.16),
                      ("Feat 5", 2, 0.40), ("Feat 4", 1, 0.68)):
        fw, fh = 46, 18
        fx, fy = gx + c * col + (col - fw) / 2, gy + v * gh
        forme(s, S.ROUNDED_RECTANGLE, fx, fy, fw, fh, NAVY, None, adj=0.2)
        tx(s, fx, fy, fw, fh, [[(nom, 9, True, BLANC)]], ANCRE.MIDDLE, ALIGN.CENTER)


ETAPES = [
    {"declarer": [_id_rang(17)], "f": lambda prs: s17(prs, int(_id_rang(17)[3:])), "nouvelles_max": 0,
     "nom": "17 : en-tête de tableau navy + cap cyan"},
    {"declarer": [_id_rang(20)], "f": lambda prs: s20(prs, int(_id_rang(20)[3:])), "nouvelles_max": 0,
     "nom": "20 : accent navy sur la 6e carte"},
    {"declarer": [_id_rang(28)], "f": lambda prs: s28(prs, int(_id_rang(28)[3:])), "nouvelles_max": 0,
     "nom": "28 : coin de la grande carte"},
    {"declarer": [_id_rang(32)], "f": lambda prs: s32(prs, int(_id_rang(32)[3:])), "nouvelles_max": 0,
     "nom": "32 : roadmap en formes natives"},
    {"declarer": [_id_rang(40)], "f": lambda prs: s40(prs, int(_id_rang(40)[3:])), "nouvelles_max": 0,
     "nom": "40 : en-tête navy, sous-total cyan"},
]
