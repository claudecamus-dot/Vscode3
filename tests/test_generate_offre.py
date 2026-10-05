"""generate_offre.py : filet minimal (audit VSCode3 2026-10-04, risque_technique)."""
import importlib.util
import sys
from pathlib import Path

import pytest

CADRAGE = Path(__file__).resolve().parents[1] / "docs" / "cadrage-ppt"


@pytest.fixture(scope="module")
def offre():
    sys.path.insert(0, str(CADRAGE))
    spec = importlib.util.spec_from_file_location("generate_offre_sous_test", CADRAGE / "generate_offre.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_ouvrir_brut_refuse_un_fichier_non_image(offre, tmp_path):
    faux = tmp_path / "_brut_x.jpg"
    faux.write_bytes(b"pas une image")
    with pytest.raises(SystemExit, match="invalide"):
        offre.ouvrir_brut(str(faux))


def test_ouvrir_brut_refuse_un_fichier_absent(offre, tmp_path):
    with pytest.raises(SystemExit):
        offre.ouvrir_brut(str(tmp_path / "absent.jpg"))


def test_ouvrir_brut_accepte_une_image_valide(offre, tmp_path):
    from PIL import Image
    ok = tmp_path / "ok.png"
    Image.new("RGB", (64, 64)).save(ok)
    assert offre.ouvrir_brut(str(ok)).size == (64, 64)


def test_construire_produit_un_deck_sans_defaut_de_geometrie(offre):
    prs = offre.construire()
    assert len(prs.slides) >= 10
    assert offre.D.verifier_geometrie(prs) == []
    assert not [1 for _, t in offre.texte_deck(prs) if "gaspill" in t.lower()]
