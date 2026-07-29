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
