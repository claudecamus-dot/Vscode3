"""Delta V37p (base V36) : le mot « Conviction » n'apparait plus deux fois sur les slides de conviction.

Sur les slides « Conviction n : … » le titre porte deja le mot et le numero (les points de progression donnent la position) ; la pilule navy « CONVICTION n » du rail de gauche le redisait.
La pilule (forme + texte) est retiree ; le bloc pictogramme du rail reste. Les slides a trois cartes (convictions 2 a 6) ne sont pas concernees : leur titre ne porte pas le mot.
Idempotent : s'applique apres les lots qui refont ces slides ; ne touche rien d'autre.
Usage (depuis docs/cadrage-ppt/) : py deck_delta/deck.py delta_V37p --base V36 --sortie C:/tmp/deck-v37/V37p.pptx --sans-rendu
"""
import re

import deck_base
from pptx import Presentation

BASE = "V36"
NOTE = "V37p : pilule CONVICTION n retiree des slides Conviction n (doublon avec le titre)"
TITRE = re.compile(r"^Conviction \d+\s*:")  # \s : la slide 17 a une espace insecable avant les deux-points
PILULE = re.compile(r"^CONVICTION \d+$")
EMU_PT = 12700


def _texte(sh):
    return sh.text_frame.text if sh.has_text_frame else ""


def _titre(s):
    return _texte(s.shapes.title) if s.shapes.title is not None else ""


def _ids():
    prs = Presentation(deck_base.resoudre_base(BASE))
    ids = [f"id:{s.slide_id}" for s in prs.slides if TITRE.match(_titre(s))]
    assert len(ids) == 8, f"{len(ids)} slides « Conviction n : » trouvees, 8 attendues"
    return ids


def pastille(prs):
    for s in prs.slides:
        if not TITRE.match(_titre(s)):
            continue
        for tb in [x for x in s.shapes if PILULE.match(_texte(x))]:
            fonds = [x for x in s.shapes if x is not tb and x.shape_type == 1 and not _texte(x)
                     and abs(x.top - tb.top) < EMU_PT and abs(x.left - tb.left) < 8 * EMU_PT and abs(x.width - tb.width) < 16 * EMU_PT and abs(x.height - tb.height) < 2 * EMU_PT]
            tb._element.getparent().remove(tb._element)
            for f in fonds:
                f._element.getparent().remove(f._element)


ETAPES = [{"declarer": _ids(), "f": pastille, "nouvelles_max": 0, "nom": "pilule CONVICTION n retiree (doublon avec le titre)"}]
OPS = []
