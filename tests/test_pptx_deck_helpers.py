"""Les trois helpers portes dans pptx_deck.py le 2026-09-11 (finding risque
technique de l'audit-technique VScode5 du 2026-09-09 : `pptx_deck.py` restait
en-deca en helpers reutilisables — add_chip/add_badge/gestion de police de
marque — presents chez les homologues VSCode2/VSCode4, alors que
`generate_deck.py` les redefinissait localement et les appelait 18 fois —
12 chip() + 6 _badge(), compte verifie par grep sur generate_deck.py le 2026-09-11).

Chaque test verifie que la fonction EXTRAITE se comporte exactement comme la
fonction locale qu'elle remplace (repli de couleur, style pointille, bascule
de police) — pas seulement qu'elle existe.
"""
import importlib.util
from pathlib import Path

import pytest
from pptx import Presentation
from pptx.enum.dml import MSO_LINE_DASH_STYLE

CADRAGE = Path(__file__).resolve().parents[1] / "docs" / "cadrage-ppt"


@pytest.fixture(scope="module")
def D():
    spec = importlib.util.spec_from_file_location(
        "pptx_deck_sous_test_helpers", CADRAGE / "pptx_deck.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _prs_vide():
    prs = Presentation()
    prs.slides.add_slide(prs.slide_layouts[6])  # « Blank »
    return prs


def _seule_couleur_texte(slide):
    shp = slide.shapes[-1]
    return shp.text_frame.paragraphs[0].runs[0].font.color.rgb


# --- add_chip ------------------------------------------------------------

def test_add_chip_dessine_une_pastille_pleine_avec_le_libelle(D):
    prs = _prs_vide()
    D.add_chip(prs.slides[0], 0.5, 0.5, 1.2, 0.3, "3j", D.PALETTE[0])

    formes = list(prs.slides[0].shapes)
    assert len(formes) == 2, "un rectangle (fond) + une zone de texte (libelle)"
    texte = formes[-1].text_frame.paragraphs[0].runs[0]
    assert texte.text == "3j"
    assert texte.font.size.pt == D.TYPE["tiny"], "taille par defaut = TYPE['tiny']"


def test_add_chip_respecte_la_couleur_de_texte_explicite(D):
    prs = _prs_vide()
    D.add_chip(prs.slides[0], 0.5, 0.5, 1.2, 0.3, "X", D.PALETTE[0],
               text_color=D.INK)

    assert str(_seule_couleur_texte(prs.slides[0])) == D.INK.lstrip("#").upper()


# --- add_badge -------------------------------------------------------------

def test_add_badge_plein_replie_le_texte_en_blanc_sans_text_color(D):
    prs = _prs_vide()
    D.add_badge(prs.slides[0], 1.0, 1.0, 0.3, D.PALETTE[1], "1", filled=True)

    assert str(_seule_couleur_texte(prs.slides[0])) == "FFFFFF"


def test_add_badge_contour_seul_replie_le_texte_sur_la_couleur_de_contour(D):
    prs = _prs_vide()
    D.add_badge(prs.slides[0], 1.0, 1.0, 0.3, D.PALETTE[2], "?", filled=False)

    assert str(_seule_couleur_texte(prs.slides[0])) == D.PALETTE[2].lstrip("#").upper()


def test_add_badge_dashed_applique_le_style_pointille_sur_le_contour(D):
    prs = _prs_vide()
    D.add_badge(prs.slides[0], 1.0, 1.0, 0.3, D.PALETTE[2], "?", filled=False,
                dashed=True)

    cercle = prs.slides[0].shapes[0]
    assert cercle.line.dash_style == MSO_LINE_DASH_STYLE.DASH


def test_add_badge_text_color_explicite_prevaut_sur_le_repli(D):
    prs = _prs_vide()
    D.add_badge(prs.slides[0], 1.0, 1.0, 0.3, D.PALETTE[1], "1", filled=True,
                text_color=D.INK)

    assert str(_seule_couleur_texte(prs.slides[0])) == D.INK.lstrip("#").upper()


# --- appliquer_police --------------------------------------------------------

def test_appliquer_police_bascule_les_glyphes_hors_couverture_en_secours(D):
    prs = _prs_vide()
    D.add_text(prs.slides[0], 0.5, 0.5, 2.0, 0.5, [("texte normal", {})])
    D.add_text(prs.slides[0], 0.5, 1.5, 2.0, 0.5, [("①", {})])

    n_police, n_secours = D.appliquer_police(prs, "Outfit", "Arial",
                                             glyphes_hors_police={"①"})

    runs = [r for s in prs.slides[0].shapes for p in s.text_frame.paragraphs
            for r in p.runs]
    polices = {r.text: r.font.name for r in runs}
    assert polices["texte normal"] == "Outfit"
    assert polices["①"] == "Arial"
    assert (n_police, n_secours) == (1, 1)


def test_appliquer_police_sans_glyphe_exclu_bascule_tout_en_police_principale(D):
    prs = _prs_vide()
    D.add_text(prs.slides[0], 0.5, 0.5, 2.0, 0.5, [("texte normal", {})])

    n_police, n_secours = D.appliquer_police(prs, "Outfit", "Arial")

    assert (n_police, n_secours) == (1, 0)
