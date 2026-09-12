"""Les trois helpers portes dans pptx_deck.py le 2026-09-11 (finding risque
technique de l'audit-technique VScode5 du 2026-09-09 : `pptx_deck.py` restait
en-deca en helpers reutilisables — add_chip/add_badge/gestion de police de
marque — presents chez les homologues VSCode2/VSCode4, alors que
`generate_deck.py` les redefinissait localement et les appelait 18 fois —
12 chip() + 6 _badge(), compte verifie par grep sur generate_deck.py le 2026-09-11).

Chaque test verifie que la fonction EXTRAITE se comporte exactement comme la
fonction locale qu'elle remplace (repli de couleur, style pointille, bascule
de police) — pas seulement qu'elle existe.

`add_encart` (dernier de la meme liste de finding, non porte le 2026-09-11 —
seul celui-la manquait encore le 2026-09-12) est teste plus bas : geometrie du
rectangle de fond, du lisere d'accent et de la zone de texte, pas seulement
« ca ne plante pas ».
"""
import importlib.util
from pathlib import Path

import pytest
from pptx import Presentation
from pptx.enum.dml import MSO_LINE_DASH_STYLE
from pptx.util import Inches

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


# --- add_encart --------------------------------------------------------------

def test_add_encart_sans_accent_pose_un_rectangle_track_et_le_texte_centre(D):
    prs = _prs_vide()
    l, t, w, h = 1.0, 1.0, 3.0, 1.0
    D.add_encart(prs.slides[0], l, t, w, h, "Texte")

    formes = list(prs.slides[0].shapes)
    assert len(formes) == 2, "un rectangle de fond + une zone de texte (pas de lisere sans accent)"

    fond = formes[0]
    assert (fond.left, fond.top, fond.width, fond.height) == (
        Inches(l), Inches(t), Inches(w), Inches(h)), "le rectangle de fond occupe exactement la boite"
    assert str(fond.fill.fore_color.rgb) == D.TRACK.lstrip("#").upper(), \
        "fond neutre = TRACK, la piste deja definie dans ce module (pas une ENCART_BG dediee)"

    zone = formes[-1]
    pad = 0.24
    assert (zone.left, zone.width) == (Inches(l + pad), Inches(w - 2 * pad)), \
        "la zone de texte est retiree du pad par defaut (sans lisere d'accent)"
    run = zone.text_frame.paragraphs[0].runs[0]
    assert run.text == "Texte"
    assert run.font.bold is True, "sans label, le texte seul porte l'emphase (bold = label is None)"
    assert run.font.size.pt == D.TYPE["h3"], "taille par defaut = TYPE['h3']"
    assert zone.text_frame.vertical_anchor == D.MSO_ANCHOR.MIDDLE, \
        "le texte est ancre au milieu de la boite, comme les homologues"


def test_add_encart_avec_accent_ajoute_un_lisere_gauche_et_elargit_le_pad(D):
    prs = _prs_vide()
    l, t, w, h = 1.0, 1.0, 3.0, 1.0
    accent = D.PALETTE[0]
    D.add_encart(prs.slides[0], l, t, w, h, "Texte", accent=accent)

    formes = list(prs.slides[0].shapes)
    assert len(formes) == 3, "rectangle de fond + lisere d'accent + zone de texte"

    fond, lisere, zone = formes
    assert (lisere.left, lisere.top, lisere.width, lisere.height) == (
        Inches(l), Inches(t), Inches(0.06), Inches(h)), \
        "le lisere colle au bord gauche, pleine hauteur, largeur fixe 0.06in"
    assert str(lisere.fill.fore_color.rgb) == accent.lstrip("#").upper()

    pad = 0.28
    assert (zone.left, zone.width) == (Inches(l + pad), Inches(w - 2 * pad)), \
        "un accent presence elargit le pad a 0.28in (place pour le lisere)"


def test_add_encart_avec_label_ajoute_un_paragraphe_gras_au_dessus_et_le_texte_nest_plus_gras(D):
    prs = _prs_vide()
    D.add_encart(prs.slides[0], 1.0, 1.0, 3.0, 1.0, "corps", label="LABEL")

    zone = prs.slides[0].shapes[-1]
    paras = zone.text_frame.paragraphs
    assert len(paras) == 2, "un paragraphe label + un paragraphe texte"
    lbl_run = paras[0].runs[0]
    txt_run = paras[1].runs[0]
    assert (lbl_run.text, lbl_run.font.bold) == ("LABEL", True), "le label est toujours en gras"
    assert (txt_run.text, txt_run.font.bold) == ("corps", False), \
        "avec un label, le texte n'est plus en gras par defaut (bold = label is None)"


def test_add_encart_taille_de_police_explicite_est_appliquee_au_texte(D):
    prs = _prs_vide()
    D.add_encart(prs.slides[0], 1.0, 1.0, 3.0, 1.0, "corps", size=8)

    run = prs.slides[0].shapes[-1].text_frame.paragraphs[0].runs[0]
    assert run.font.size.pt == 8


def test_add_encart_reste_dans_les_bornes_de_la_boite_declaree(D):
    """Non-regression geometrique : ni le lisere ni la zone de texte ne
    depassent le rectangle de fond declare par (l, t, w, h) — le defaut
    classique que `verifier_geometrie` traque sur un deck reel."""
    prs = _prs_vide()
    l, t, w, h = 1.0, 1.0, 3.0, 1.0
    D.add_encart(prs.slides[0], l, t, w, h, "Un texte assez long pour tester",
                 accent=D.PALETTE[1], label="LABEL")

    droite, bas = Inches(l + w), Inches(t + h)
    for shp in prs.slides[0].shapes:
        assert shp.left >= Inches(l) and shp.top >= Inches(t)
        assert shp.left + shp.width <= droite
        assert shp.top + shp.height <= bas
