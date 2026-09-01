"""Garde du template de generate_deck (finding robustesse de l'audit 2026-07-23,
arbitré le 2026-07-29) : un template absent doit produire un SystemExit qui nomme
le fichier attendu et son emplacement — pas une FileNotFoundError brute de
python-pptx. Le générateur est lancé à la main : l'échec doit se comprendre sans
lire la stack.
"""
import importlib.util
from pathlib import Path

import pytest

CADRAGE = Path(__file__).resolve().parents[1] / "docs" / "cadrage-ppt"
VENDORED = (Path(__file__).resolve().parents[1] / ".claude" / "skills"
            / "pptx-framed-image" / "scripts")


@pytest.fixture(scope="module")
def generate_deck():
    spec = importlib.util.spec_from_file_location(
        "generate_deck_sous_test", CADRAGE / "generate_deck.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # template présent : l'import doit passer
    return mod


def test_import_avec_template_present_charge_le_theme(generate_deck):
    assert generate_deck.TH, "le thème doit être chargé depuis le vrai template"


def test_garde_nomme_le_chemin_attendu_si_template_absent(generate_deck, monkeypatch):
    absent = str(CADRAGE / "template-absent-volontaire.pptx")
    monkeypatch.setattr(generate_deck, "TEMPLATE", absent)
    with pytest.raises(SystemExit) as exc:
        generate_deck._exiger_template()
    message = str(exc.value)
    assert "template introuvable" in message
    assert "template-octo.pptx" in message
    assert "template-absent-volontaire.pptx" in message


def test_new_prs_porte_la_meme_garde(generate_deck, monkeypatch):
    monkeypatch.setattr(generate_deck, "TEMPLATE",
                        str(CADRAGE / "template-absent-volontaire.pptx"))
    with pytest.raises(SystemExit):
        generate_deck.new_prs()



# --- Repli hors ligne (revue du 2026-09-01) -------------------------------
#
# `nature_images` ne connait que 6 scenes. Les noms neufs choisis pour les
# chapitres (dunes, nightsky, canyon) n'en font pas partie : hors reseau ou sur
# 0-resultat Openverse, `generate_to` levait ValueError HORS du try de
# `_remplir_cadre`, ce qui tuait build() en entier — 0 slide produite, alors que
# 39 des 42 n'ont pas de photo. Reproduit puis corrige le 2026-09-01.


@pytest.fixture(scope="module")
def nature_images():
    spec = importlib.util.spec_from_file_location(
        "nature_images_sous_test", VENDORED / "nature_images.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_toute_scene_du_deck_a_un_repli_connu(generate_deck, nature_images):
    """L'invariant qui a manque : ajouter une scene sans repli casse le build.

    Se declenche des qu'une 10e scene est cablee dans `_REQUETES_PHOTO` sans
    etre ni connue de `nature_images.SCENES` ni mappee dans `_SCENE_REPLI`.
    """
    connues = set(nature_images.SCENES)
    orphelines = []
    for scene in generate_deck._REQUETES_PHOTO:
        repli = generate_deck._SCENE_REPLI.get(scene, scene)
        if repli not in connues:
            orphelines.append((scene, repli))
    assert not orphelines, (
        "scene(s) sans repli procedural connu -> build() plantera hors ligne : "
        f"{orphelines} ; scenes connues : {sorted(connues)}")


def test_le_repli_produit_bien_une_image_pour_les_scenes_neuves(generate_deck, nature_images, tmp_path):
    """Le mapping n'est pas qu'une table : il doit generer une vraie image."""
    for scene in ("dunes", "nightsky", "canyon"):
        repli = generate_deck._SCENE_REPLI[scene]
        cible = tmp_path / f"{scene}.png"
        nature_images.generate_to(str(cible), repli, 80, 60, seed=0)
        assert cible.exists() and cible.stat().st_size > 0


def test_un_repli_impossible_degrade_au_lieu_de_planter(generate_deck, monkeypatch, tmp_path):
    """Ceinture ET bretelles : meme si le repli echoue, build() ne meurt pas.

    Le defaut remonte alors dans `_ANOMALIES_IMAGE`, donc dans `problemes` —
    il ne disparait pas en silence.
    """
    monkeypatch.setattr(generate_deck, "IMG_DIR", str(tmp_path))
    generate_deck._ANOMALIES_IMAGE[:] = []

    def echec(*a, **k):
        raise RuntimeError("reseau coupe (simulation)")

    monkeypatch.setattr(generate_deck.stock_images, "fetch_to", echec)
    monkeypatch.setattr(generate_deck.nature_images, "generate_to", echec)

    prs = generate_deck.new_prs()
    generate_deck.slide_chapitre(prs, "01", "titre", "couverture",
                                 generate_deck.D.PALETTE[0], "canyon", seed=0)
    assert any("canyon" in a for a in generate_deck._ANOMALIES_IMAGE),         "un repli impossible doit remonter dans les anomalies, pas disparaitre"


def test_cadre_introuvable_remonte_dans_les_problemes(generate_deck):
    """Un cadre absent du template ne doit plus se contenter d'un print."""
    generate_deck._ANOMALIES_IMAGE[:] = []
    generate_deck._remplir_cadre(None, None, "canyon")
    assert generate_deck._ANOMALIES_IMAGE,         "cadre introuvable : le defaut doit rejoindre les problemes remontes par build()"
