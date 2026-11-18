"""Delta V43 s21 (base V42) : split the dense slide « L'IA apporte au coach du temps et de la matière, pas la décision » in two.

User request (2026-11-05) : « revois les slides trop denses en conservant l'ancienne version » (V42 stays untouched).
Slide A (original, same title) keeps the two equation cards, the central circle and the navy banner.
Slide B (new, right after A) takes the 5-step strip « Où l'IA aide dans la boucle » and the three « Ce que cela change pour vous » lines.
No text is reworded or dropped; shapes are only moved/stretched vertically to fill each slide. Slide B's title is built from
the strip's own heading and the banner's « contrôle humain ».
Usage (from docs/cadrage-ppt/) : py deck_delta/deck.py delta_V43_s21 --base V42 --sortie C:/tmp/deck-v43-s21/V43s21.pptx --sans-rendu
"""
import deck_base
import deck_draw
from pptx import Presentation
from pptx.util import Emu

BASE = "V42"
NOTE = "V43 s21 : slide 21 scindée en deux (équation + bandeau / frise de la boucle + trois effets)"
OPS = []

T_A = "L'IA apporte au coach du temps et de la matière, pas la décision"
T_B = "Où l'IA aide dans la boucle : cinq moments sous contrôle humain"
HAUT, BAS = 84, 352  # useful zone (pt)
PT = 12700


def _supprimer(s, ids):
    for sh in list(s.shapes):
        if sh.shape_id in ids:
            sh._element.getparent().remove(sh._element)


def _reflow(s, src_top, src_bot, dst_top, dst_bot, etire):
    """Map each shape's vertical centre linearly from [src_top, src_bot] to [dst_top, dst_bot]; `etire` ids are also stretched."""
    k = (dst_bot - dst_top) / (src_bot - src_top)
    for sh in s.shapes:
        if sh.shape_id in (2,) or sh.top < 80 * PT:
            continue
        c = (sh.top + sh.height / 2) / PT
        h = sh.height / PT * (k if sh.shape_id in etire else 1)
        nc = dst_top + (c - src_top) * k
        sh.height = Emu(int(h * PT))
        sh.top = Emu(int((nc - h / 2) * PT))


def scinder(prs):
    core = deck_base.core()
    modele = deck_draw.slide_par_titre(prs, T_A)
    rang = list(prs.slides).index(modele)
    b = core.copier_slide(prs, modele, index=rang + 1)
    ext = deck_draw._sections(prs)
    if ext is not None:
        deck_draw._placer_dans_section(ext, deck_draw.id_de(prs, modele), deck_draw.id_de(prs, b))
    tb = [sh for sh in b.shapes if sh.shape_id == 2][0]
    deck_draw.set_run(tb, T_B)
    # B : strip + effects (ids 160-192)
    _supprimer(b, set(range(130, 160)))
    ids_b = {sh.shape_id for sh in b.shapes}
    etire_b = {161, 163, 165, 167, 169, 172, 174, 176, 173, 175, 177, 162, 164, 166, 168, 170}
    _reflow(b, 250, 360, 100, 345, etire_b & ids_b)
    # A : equation + banner (ids 130-159)
    _supprimer(modele, set(range(160, 193)))
    _reflow(modele, 84, 236, 100, 340, {130, 142, 156, 157, 159})
    return b


def _id(t):
    prs = Presentation(deck_base.resoudre_base(BASE))
    return [f"id:{deck_draw.slide_par_titre(prs, t).slide_id}"]


ETAPES = [{"declarer": _id(T_A), "f": scinder, "nouvelles_max": 1, "nom": "21 : scission en deux slides"}]
