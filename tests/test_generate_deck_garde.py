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

    Le defaut remonte alors dans `_ANOMALIES_BUILD`, donc dans `problemes` —
    il ne disparait pas en silence.
    """
    monkeypatch.setattr(generate_deck, "IMG_DIR", str(tmp_path))
    generate_deck._ANOMALIES_BUILD[:] = []

    def echec(*a, **k):
        raise RuntimeError("reseau coupe (simulation)")

    monkeypatch.setattr(generate_deck.stock_images, "fetch_to", echec)
    monkeypatch.setattr(generate_deck.nature_images, "generate_to", echec)

    prs = generate_deck.new_prs()
    generate_deck.slide_chapitre(prs, "01", "titre", "couverture",
                                 generate_deck.D.PALETTE[0], "canyon", seed=0)
    assert any("canyon" in a for a in generate_deck._ANOMALIES_BUILD),         "un repli impossible doit remonter dans les anomalies, pas disparaitre"


def test_cadre_introuvable_remonte_dans_les_problemes(generate_deck):
    """Un cadre absent du template ne doit plus se contenter d'un print."""
    generate_deck._ANOMALIES_BUILD[:] = []
    generate_deck._remplir_cadre(None, None, "canyon")
    assert generate_deck._ANOMALIES_BUILD,         "cadre introuvable : le defaut doit rejoindre les problemes remontes par build()"


# --- Les trois filets sont-ils BRANCHÉS, pas seulement présents ? ------------
# Finding du hub du 2026-09-09 : verifier_debordements_texte,
# verifier_chrome_gabarit et verifier_plancher_de_dessin étaient portés et
# testés dans pptx_deck.py (16 tests, 8 mutants) sans qu'aucun ne soit appelé
# par generate_deck. Un filet non branché ne protège rien, et sa suite de tests
# verte donne l'illusion inverse. Ces tests-ci portent sur le CÂBLAGE.

@pytest.fixture
def prs_minimal(generate_deck):
    """Une présentation vide : on teste le câblage, pas le contenu du deck."""
    generate_deck._ANOMALIES_BUILD[:] = []
    return generate_deck.new_prs()


def _faux_capturant(marqueur):
    """Un faux qui ENREGISTRE ses arguments, là où une lambda `*a, **k` les avale.

    La distinction n'est pas théorique : `verifier_plancher_de_dessin` appelé
    sans `bord_droit_in` rend un constat sur le deck réel (mesuré le
    2026-09-10), donc chaque build écrirait `.INVALIDE.pptx` et le livrable ne
    serait plus jamais mis à jour — pendant qu'une lambda tolérante laissait la
    suite au vert.
    """
    appels = []

    def faux(*a, **k):
        appels.append((a, k))
        return [marqueur]

    faux.appels = appels
    return faux


@pytest.mark.parametrize("filet", [
    "verifier_geometrie",
    "verifier_chrome_gabarit",
    "verifier_plancher_de_dessin",
])
def test_chaque_filet_branche_remonte_dans_le_self_check(
        generate_deck, prs_minimal, monkeypatch, filet):
    """Un constat injecté dans un filet doit ressortir du contrôle de build().

    Le test échoue si le filet est débranché — c'est exactement l'état que le
    finding décrivait, et le seul que la suite de pptx_deck.py ne pouvait pas
    voir puisqu'elle teste les filets isolément.
    """
    marqueur = f"CONSTAT INJECTE PAR LE TEST ({filet})"
    faux = _faux_capturant(marqueur)
    monkeypatch.setattr(generate_deck.D, filet, faux)
    assert marqueur in generate_deck._controler(prs_minimal), (
        f"{filet} n'est pas consulte par le self-check de build() : "
        "un filet non branche ne protege rien")
    assert faux.appels, f"{filet} n'a pas ete appele du tout"


def test_le_plancher_recoit_les_constantes_du_module(
        generate_deck, prs_minimal, monkeypatch):
    """Le filet doit recevoir les BONNES constantes, pas seulement etre appele.

    `verifier_plancher_de_dessin(prs, 5.45)` sans `bord_droit_in` rend 1 constat
    sur le deck reel la ou l'appel complet en rend 0 : perdre ce kwarg condamne
    tous les builds a `.INVALIDE.pptx`. Verifier la reference du filet sans
    verifier ses arguments ne voyait pas ce cas.
    """
    # On DEPLACE les constantes du module vers des valeurs sentinelles : c'est
    # ce qui distingue « le filet recoit CONTENT_BOTTOM » de « le filet recoit
    # 5.45 ». Comparer les valeurs laissait passer un litteral recopie, qui
    # decroche silencieusement le jour ou la constante bouge.
    monkeypatch.setattr(generate_deck, "CONTENT_BOTTOM", -111.0)
    monkeypatch.setattr(generate_deck, "BORD_DROIT", -222.0)
    faux = _faux_capturant("peu importe")
    monkeypatch.setattr(generate_deck.D, "verifier_plancher_de_dessin", faux)
    generate_deck._controler(prs_minimal)

    (args, kwargs), = faux.appels
    assert -111.0 in args, (
        "le plancher doit venir de CONTENT_BOTTOM, pas d'un litteral recopie")
    assert kwargs.get("bord_droit_in") == -222.0, (
        "bord_droit_in manquant, faux, ou recopie en litteral : sans lui le "
        "filet rend un constat sur le deck reel, donc chaque build ecrit "
        ".INVALIDE.pptx")


def test_sans_injection_le_controle_est_vert(generate_deck, prs_minimal):
    """La ligne de base : le cote FAUX POSITIF, celui qui bloque la livraison.

    Tous les autres tests asserent « marqueur present/absent » et resteraient
    verts si un filet se mettait a rendre un constat constant — ce qui
    condamnerait pourtant chaque build.
    """
    assert generate_deck._controler(prs_minimal) == [], (
        "le controle doit etre vert sans injection : un constat constant "
        "enverrait chaque deck en .INVALIDE.pptx")


def test_les_anomalies_de_build_restent_dans_le_self_check(
        generate_deck, prs_minimal):
    """Le câblage des filets ne doit pas avoir évincé _ANOMALIES_BUILD."""
    generate_deck._ANOMALIES_BUILD.append("ANOMALIE INJECTEE PAR LE TEST")
    try:
        assert "ANOMALIE INJECTEE PAR LE TEST" in generate_deck._controler(prs_minimal)
    finally:
        generate_deck._ANOMALIES_BUILD[:] = []


def test_debordements_texte_reste_hors_du_self_check(
        generate_deck, prs_minimal, monkeypatch):
    """Décision explicite, pas un oubli : son seuil n'est pas réglé.

    Mesuré sur le deck réel du 2026-09-10 : 58 constats, contre 0 aux trois
    autres filets. Ce résultat gouverne le nom du fichier écrit (.INVALIDE.pptx
    si non vide), donc le brancher bloquerait la livraison d'un deck correct.
    Ce test tombera le jour où quelqu'un le branche — c'est le but : la décision
    devra être reprise avec sa mesure, pas glissée dans un diff.
    """
    monkeypatch.setattr(generate_deck.D, "verifier_debordements_texte",
                        lambda *a, **k: ["CONSTAT QUI NE DOIT PAS REMONTER"])
    assert "CONSTAT QUI NE DOIT PAS REMONTER" not in generate_deck._controler(prs_minimal), (
        "verifier_debordements_texte a ete branche sans que son seuil soit "
        "regle contre un rendu PowerPoint reel : il rendait 58 constats sur un "
        "deck correct, ce qui ecrit .INVALIDE.pptx et bloque la livraison")
