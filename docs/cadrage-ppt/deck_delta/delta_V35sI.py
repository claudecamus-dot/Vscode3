"""Delta V35sI (base V34, apres le lot g) : la slide « L'IA apporte au coach du temps et de la matiere » est aeree et rendue plus lisible.

Meme idee que V32 / V33 (modele « cognitive acceleration » de Vscode8) : deux leviers (GAGNER DU TEMPS / APPORTER DE LA MATIERE) qui convergent vers un disque
« L'IA augmente le coach », un socle de controle humain, les moments de la boucle, ce que cela change pour le client. Changements :
- texte >= 11 pt (legendes >= 10,5 pt), ecarts verticaux doubles, un seul alignement gauche (x 45) ;
- les cinq moments de la boucle deviennent UNE frise de chevrons (plus de cinq cases grises separees), pictogrammes copies de la slide ;
- les trois effets pour le client sont des enonces courts sous un trait cyan ; « Rien n'est promis » reste ; « T0 puis T1 » devient « avant, puis apres ».
Aucune phrase retiree : tout le contenu reste sur la slide (voir les notes). La navigation, le titre et le numero de page ne sont pas touches.
Usage (depuis docs/cadrage-ppt/) : py deck_delta/deck.py delta_V35sI --base C:/tmp/deck-v35/V35g.pptx --sortie C:/tmp/deck-v35-sI/V35sI.pptx --sans-rendu
"""
import copy

import deck_base
import deck_draw
from forme_v9 import (
    BLANC,
    CYAN,
    NAVY,
    PANEL,
    S,
    carre_num_cyan,
    forme,
    pilule_entete,
    tx,
)
from pptx import Presentation
from pptx.enum.text import MSO_ANCHOR as A
from pptx.enum.text import PP_ALIGN as P

BASE = "V34"
NOTE = "V35sI : slide IA aeree (texte >= 11 pt, frise de chevrons pour la boucle, trois effets courts)"
OPS = []

NB = "\u00a0"
T_IA = "L'IA apporte au coach du temps et de la matière, pas la décision"
X0, X1 = 45, 659
Y_CORPS = 90  # tout ce qui est au-dessous est le corps (le titre, la navigation et le numero de page sont au-dessus ou hors de ce corps)

LEVIERS = (
    ("GAGNER DU TEMPS", ((1, "Un diagnostic plus rapide"), (2, "Un tri assisté des demandes"), (3, "Une capitalisation continue"))),
    ("APPORTER DE LA MATIÈRE", ((4, "Des mesures consolidées"), (5, "Des cas d'usage bornés"))),
)
SOCLE_LIBELLE = ("SOCLE COMMUN", "CONTRÔLE HUMAIN")
SOCLE_TEXTE = f"L'IA prépare, nos coachs challengent, le client décide{NB}: chaque apport est borné et relu."
MOMENTS = (("loupe", "Comprendre"), ("barres", "Prioriser"), ("engrenage", "Ancrer"), ("cible", "Mesurer"), ("eclair", "Explorer"))
EFFETS = (
    (f"Comprendre plus vite{NB}:", " un diagnostic et un tri assistés"),
    (f"Garder la main{NB}:", " chaque apport est relu, le client décide"),
    (f"Rien n'est promis{NB}:", " gains à mesurer avant, puis après"),
)
NOTES = (
    "Mise en page allégée (V35sI), rien n'est retiré" + NB + ":\n"
    "- Deux leviers" + NB + ": gagner du temps (diagnostic plus rapide, tri assisté des demandes, capitalisation continue) ; apporter de la matière (mesures consolidées, cas d'usage bornés).\n"
    "- Socle commun, contrôle humain" + NB + ": l'IA prépare, nos coachs challengent, le client décide" + NB + "; chaque apport est borné et relu.\n"
    "- Où l'IA aide dans la boucle" + NB + ": comprendre, prioriser, ancrer, mesurer, explorer.\n"
    "- Ce que cela change pour vous" + NB + ": comprendre plus vite (un diagnostic et un tri assistés) ; garder la main (chaque apport est relu, le client décide) ; "
    "rien n'est promis (gains à mesurer avant, puis après)."
)


def _picto_sources(s):
    """Pour chaque moment : (ids des formes du pictogramme, centre de la forme de contour) ; les formes sont nommees picto-<cle> et picto-<cle>-glyphe."""
    sources = {}
    for cle, _nom in MOMENTS:
        formes = [sh for sh in s.shapes if sh.name in (f"picto-{cle}", f"picto-{cle}-glyphe")]
        contour = [sh for sh in formes if sh.name == f"picto-{cle}"]
        if not contour:
            raise ValueError(f"pictogramme {cle!r} introuvable sur la slide")
        c = contour[0]
        sources[cle] = ([sh.shape_id for sh in formes], ((c.left + c.width / 2) / 12700, (c.top + c.height / 2) / 12700))
    return sources


def _pt(v):
    return int(round(v * 12700))


def _copier_picto(s, ids, cx, cy, centre_src, scale=1.0):
    """Copie les formes `ids` de la slide vers (cx, cy) en points ; dimensions et traits x scale (meme principe que delta_V32a.copier_picto)."""
    ns = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
    par = {sh.shape_id: sh for sh in s.shapes}
    base_id = max(sh.shape_id for sh in s.shapes) + 1
    for k, i in enumerate(ids):
        el = copy.deepcopy(par[i]._element)
        xf = next(el.iter(f"{ns}xfrm"))
        off, ext = xf.find(f"{ns}off"), xf.find(f"{ns}ext")
        ox, oy = int(off.get("x")) / 12700, int(off.get("y")) / 12700
        w, h = int(ext.get("cx")) / 12700, int(ext.get("cy")) / 12700
        off.set("x", str(_pt(cx + (ox - centre_src[0]) * scale)))
        off.set("y", str(_pt(cy + (oy - centre_src[1]) * scale)))
        ext.set("cx", str(_pt(w * scale)))
        ext.set("cy", str(_pt(h * scale)))
        for ln in el.iter(f"{ns}ln"):
            if ln.get("w"):
                ln.set("w", str(max(9525, int(int(ln.get("w")) * min(1.0, scale * 1.15)))))
        [e for e in el.iter() if e.tag.endswith("}cNvPr")][0].set("id", str(base_id + k))
        s.shapes._spTree.append(el)


def ia(prs):
    s = deck_draw.slide_par_titre(prs, T_IA)
    ancien = {sh.shape_id for sh in s.shapes if not sh.is_placeholder and not sh.name.startswith("nav-") and sh.top >= _pt(Y_CORPS)}
    pic = _picto_sources(s)

    # ---- zone 1 : deux leviers qui convergent vers le disque
    PY, PH, PW = 84, 108, 226
    cxm, cym = (X0 + X1) / 2, PY + PH / 2
    for x, (titre, apports) in zip((X0, X1 - PW), LEVIERS, strict=True):
        forme(s, S.ROUND_2_DIAG_RECTANGLE, x, PY, PW, PH, BLANC, NAVY, adj=0.1, lw=1.25)
        pilule_entete(s, x + 14, PY + 9, 176, 20, titre, NAVY, sz=10.5)
        decal = (3 - len(apports)) * 11  # deux apports : bloc centre sous l'entete, meme gabarit que trois
        for k, (n, t) in enumerate(apports):
            y = PY + 37 + k * 22 + decal
            carre_num_cyan(s, x + 14, y, 18, n, sz=10.5)
            tx(s, x + 40, y, PW - 50, 18, [[(t, 12, True, NAVY)]], A.MIDDLE, P.LEFT)
    forme(s, S.RIGHT_ARROW, X0 + PW + 8, cym - 9, 18, 18, CYAN, None)
    forme(s, S.LEFT_ARROW, X1 - PW - 8 - 18, cym - 9, 18, 18, CYAN, None)
    forme(s, S.OVAL, cxm - 50, cym - 50, 100, 100, BLANC, NAVY, lw=1.25)
    forme(s, S.OVAL, cxm - 43, cym - 43, 86, 86, NAVY, None)
    tx(s, cxm - 42, cym - 20, 84, 40, [[("L'IA augmente", 12, True, BLANC)], [("le coach", 12, True, BLANC)]], A.MIDDLE, P.CENTER)

    # ---- zone 2 : le socle commun, une seule bande
    SY, SH = PY + PH + 12, 32
    forme(s, S.ROUNDED_RECTANGLE, X0, SY, X1 - X0, SH, NAVY, None, adj=0.25)
    tx(s, X0 + 16, SY, 118, SH, [[(SOCLE_LIBELLE[0], 10.5, True, BLANC)], [(SOCLE_LIBELLE[1], 10.5, True, BLANC)]], A.MIDDLE, P.LEFT)
    forme(s, S.RECTANGLE, X0 + 138, SY + 7, 0.75, SH - 14, PANEL)
    tx(s, X0 + 152, SY, X1 - X0 - 162, SH, [[(SOCLE_TEXTE, 11, False, BLANC)]], A.MIDDLE, P.LEFT)

    # ---- zone 3 : la boucle, une frise de cinq chevrons
    LY = SY + SH + 14
    tx(s, X0, LY, 400, 13, [[("OÙ L'IA AIDE DANS LA BOUCLE", 10.5, True, NAVY)]], A.MIDDLE, P.LEFT)
    FY, FH, D, G = LY + 17, 34, 12.6, 4
    w = (X1 - X0 + 4 * (D - G)) / 5  # largeur d'un chevron : 5 w - 4 (D - G) = largeur de la frise
    pas = w - D + G
    placements = []
    for k, (cle, nom) in enumerate(MOMENTS):
        x = X0 + k * pas
        forme(s, S.PENTAGON if k == 0 else S.CHEVRON, x, FY, w, FH, PANEL, None, adj=0.35)
        dx = 12 if k == 0 else D + 8
        placements.append((cle, x + dx + 14, FY + FH / 2))
        tx(s, x + dx + 34, FY, w - dx - 34 - D - 4, FH, [[(nom, 11, True, NAVY)]], A.MIDDLE, P.LEFT)

    # ---- zone 4 : ce que cela change pour vous
    CY = FY + FH + 14
    tx(s, X0, CY, 400, 13, [[("CE QUE CELA CHANGE POUR VOUS", 10.5, True, NAVY)]], A.MIDDLE, P.LEFT)
    g = 20
    ew = (X1 - X0 - 2 * g) / 3
    for k, (a, t) in enumerate(EFFETS):
        x = X0 + k * (ew + g)
        forme(s, S.RECTANGLE, x, CY + 17, 3, 28, CYAN)
        tx(s, x + 11, CY + 17, ew - 11, 28, [[(a, 11, True, NAVY), (t, 11, False, NAVY)]], A.MIDDLE, P.LEFT)

    # ---- pictogrammes (copies des formes de la slide) puis retrait de l'ancien corps
    for cle, cx, cy in placements:
        ids, centre = pic[cle]
        _copier_picto(s, ids, cx, cy, centre)
    for sh in list(s.shapes):
        if sh.shape_id in ancien:
            sh._element.getparent().remove(sh._element)
    s.notes_slide.notes_text_frame.text = NOTES


def _ids():
    prs = Presentation(deck_base.resoudre_base(BASE))
    return [f"id:{deck_draw.slide_par_titre(prs, T_IA).slide_id}"]


ETAPES = [{"declarer": _ids(), "f": ia, "nouvelles_max": 0, "nom": "slide IA : aeree, frise de chevrons, effets courts"}]
