"""Lint de charte et baseline de defauts sur le DERNIER livrable reel (port de Vscode8 : test_lint_charte, test_garde_livrable).

Mutants : une couleur ou une police hors charte injectee dans une copie doit faire echouer le controle. La baseline fige les defauts
geometriques connus ; elle echoue sur un defaut en plus ET sur un defaut disparu (dette payee : refiger). Ne remplace pas le rendu regarde."""
import os
import sys
import zipfile

import pytest

DELTA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs", "cadrage-ppt", "deck_delta")
if DELTA not in sys.path:
    sys.path.insert(0, DELTA)

import deck_baseline  # noqa: E402
import lint_charte  # noqa: E402
from pptx import Presentation  # noqa: E402


def _muter(src, dst, ancien, nouveau):
    """Copie `src` en remplacant `ancien` par `nouveau` dans la 1re slide qui le contient ; True si un remplacement a eu lieu."""
    fait = False
    with zipfile.ZipFile(src) as zin, zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zout:
        for it in zin.infolist():
            data = zin.read(it.filename)
            if not fait and it.filename.startswith("ppt/slides/slide") and ancien in data:
                data = data.replace(ancien, nouveau, 1)  # MUTANT: couleur/police hors charte
                fait = True
            zout.writestr(it, data)
    return fait


def test_livrable_sans_defaut_de_charte(livrable):
    defauts, _ = lint_charte.controler(str(livrable[0]))
    assert defauts == [], defauts


def test_couleur_hors_charte_detectee(livrable, tmp_path):
    mauvais = tmp_path / "c.pptx"
    assert _muter(livrable[0], mauvais, b'srgbClr val="0E2356"', b'srgbClr val="12AB34"')
    assert any("12AB34" in d for d in lint_charte.controler(str(mauvais))[0])


def test_police_hors_charte_detectee(livrable, tmp_path):
    mauvais = tmp_path / "p.pptx"
    assert _muter(livrable[0], mauvais, b'<a:latin typeface="Outfit"', b'<a:latin typeface="Comic Sans MS"')
    assert any("Comic Sans MS" in d for d in lint_charte.controler(str(mauvais))[0])


def test_defauts_du_livrable_dans_la_baseline(livrable):
    version_baseline, baseline = deck_baseline.charger()
    mesures = deck_baseline.cles(Presentation(str(livrable[0])))
    nouveaux, disparus = deck_baseline.comparer(mesures, baseline)
    assert not nouveaux, f"V{livrable[1]} : defaut(s) HORS baseline (V{version_baseline}) a corriger dans le delta : {nouveaux}"
    assert not disparus, f"V{livrable[1]} : defaut(s) de la baseline disparu(s), dette payee : refiger (py deck_baseline.py --figer) : {disparus}"


def test_comparer_voit_un_defaut_en_plus_et_un_en_moins():
    a = deck_baseline.collections.Counter({("t", "x"): 2, ("t", "y"): 1})
    b = deck_baseline.collections.Counter({("t", "x"): 1, ("t", "z"): 1})
    assert deck_baseline.comparer(b, a) == ([("t", "z")], [("t", "x"), ("t", "y")])


@pytest.mark.parametrize("detail,attendu", [("slide 12: texte ~0.9in > boite 0.6in (abc)", "texte ~0.9in > boite 0.6in (abc)")])
def test_la_cle_ignore_le_numero_de_slide(detail, attendu):
    assert deck_baseline._SLIDE.sub("", detail) == attendu
