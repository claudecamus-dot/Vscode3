"""Delta V35g (base V34) : le bandeau de navigation passe a droite, le surtitre de navigation et le texte « PROPOSITION A VALIDER » disparaissent.

- les six pastilles « nav-* » gardent largeur, hauteur, ecart et ordre ; la bande se cale a droite, sur le bord droit du contenu (659,25 pt) ;
- le surtitre « 0n · CHAPITRE · n/N » (et « OUVERTURE » de la slide 2), redondant avec les pastilles, est retire ; le filet cyan qui le soulignait part avec lui sauf sur les
  slides de conviction, ou la rangee de 13 points de progression prend sa place : les points se calent alors a gauche (bord 45 pt), la ou etait le surtitre ;
- la pilule « PROPOSITION A VALIDER » (forme + texte) est retiree de toutes les slides qui la portent ; la pilule « PROPOSITION » du bloc cyan de la slide « Reussir » reste (autre texte).
L'espace libere sous le titre est reutilise par les etapes suivantes (decalage vertical des slides, refontes de contenu) : cette etape ne bouge que la navigation.
Usage (depuis docs/cadrage-ppt/) : py deck_delta/deck.py delta_V35g --base V34 --sortie C:/tmp/deck-v35/V35g.pptx
"""
import re

import deck_base
from pptx import Presentation

BASE = "V34"
NOTE = "V35g : navigation a droite, surtitre de navigation et pilule PROPOSITION A VALIDER retires, points de progression a gauche"

EMU_PT = 12700
BORD_DROIT = round(659.25 * EMU_PT)
KICKER = re.compile(r"^(\d{2}|A) · [A-ZÉÈÀÂÊÎÔÛÇ' ]+ · \d+/\d+$|^OUVERTURE$")
PROPOSITION = "PROPOSITION À VALIDER"
Y_SURTITRE = 67 * EMU_PT
Y_FILET = 86 * EMU_PT
TOL = EMU_PT  # 1 pt


def _texte(sh):
    return sh.text_frame.text if sh.has_text_frame else ""


def _retirer(sh):
    sh._element.getparent().remove(sh._element)


def _points(s):
    """Les points de progression : ovales de 8 pt de cote dans la rangee du surtitre."""
    return sorted((sh for sh in s.shapes if sh.name.startswith("Oval") and abs(sh.width - 8 * EMU_PT) < TOL and abs(sh.height - 8 * EMU_PT) < TOL and abs(sh.top - 70 * EMU_PT) < 2 * EMU_PT),
                  key=lambda sh: sh.left)


def _concerne(s):
    return any(sh.name.startswith("nav-") or KICKER.match(_texte(sh)) or _texte(sh) == PROPOSITION for sh in s.shapes)


def _ids():
    prs = Presentation(deck_base.resoudre_base(BASE))
    return [f"id:{s.slide_id}" for s in prs.slides if _concerne(s)]


def chrome(prs):
    for s in prs.slides:
        if not _concerne(s):
            continue
        pastilles = [sh for sh in s.shapes if sh.name.startswith("nav-")]
        if pastilles:
            dx = BORD_DROIT - max(sh.left + sh.width for sh in pastilles)
            if dx:
                for sh in pastilles:
                    sh.left = sh.left + dx
        points = _points(s)
        for sh in [x for x in s.shapes if KICKER.match(_texte(x))]:
            _retirer(sh)
        for sh in [x for x in s.shapes if _texte(x) == PROPOSITION]:
            fond = next((x for x in s.shapes if x is not sh and x.shape_type == 1 and not _texte(x) and (x.left, x.top, x.width, x.height) == (sh.left, sh.top, sh.width, sh.height)), None)
            if fond is None:  # la pilule peut etre un peu plus large que son texte
                fond = next((x for x in s.shapes if x.shape_type == 1 and not _texte(x) and x.top == sh.top and x.height == sh.height and x.left <= sh.left and x.left + x.width >= sh.left + sh.width), None)
            _retirer(sh)
            if fond is not None:
                _retirer(fond)
        if points:
            x = 45 * EMU_PT
            for sh in points:
                sh.left = x
                x += 11 * EMU_PT
        else:
            for sh in [x for x in s.shapes if x.name.startswith("Rounded Rectangle") and not _texte(x) and x.left == 45 * EMU_PT and x.top == Y_FILET and x.width == 44 * EMU_PT]:
                _retirer(sh)


ETAPES = [{"declarer": _ids(), "f": chrome, "nouvelles_max": 0, "nom": "navigation a droite, surtitre et pilule PROPOSITION A VALIDER retires"}]
OPS = []
