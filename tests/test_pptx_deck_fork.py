"""Le fork pptx_deck de VSCode3 reste un fork nomme (arbitrage du 2026-09-23)."""
import os
import re

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CADRAGE = os.path.join(RACINE, "docs", "cadrage-ppt")
ACTIFS = ["generate_deck.py", "deck_theme.py", "deck_images.py", "deck_shapes.py"]


def test_aucune_copie_nommee_comme_la_skill_ne_revient():
    assert not os.path.exists(os.path.join(CADRAGE, "pptx_deck.py")), (
        "un pptx_deck.py est revenu a cote du fork : deux copies divergentes a nouveau")
    assert os.path.isfile(os.path.join(CADRAGE, "pptx_deck_vscode3.py"))


def test_le_generateur_importe_le_fork_et_jamais_la_skill():
    for nom in ACTIFS:
        s = open(os.path.join(CADRAGE, nom), encoding="utf-8").read()
        assert not re.search(r"^\s*import pptx_deck( |$)", s, re.M), nom
        assert "skills\", \"pptx-deck\"" not in s and "skills/pptx-deck" not in s, nom
