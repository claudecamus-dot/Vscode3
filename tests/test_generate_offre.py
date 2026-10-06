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


@pytest.fixture
def img_synthetiques(offre, tmp_path, monkeypatch):
    """docs/cadrage-ppt/_img/ est gitignore (absent en CI) : le generateur est
    pointe vers un dossier temporaire garni d'images sources synthetiques."""
    from PIL import Image
    for i, scene in enumerate(offre.PHOTOS):
        im = Image.linear_gradient("L").resize((1600, 1000)).convert("RGB")
        im = Image.blend(im, Image.new("RGB", im.size, (40 + 25 * i, 90, 160)), 0.5)
        im.save(tmp_path / f"_brut_{scene}.jpg", quality=80)
    Image.new("RGB", (400, 400), (120, 140, 160)).save(tmp_path / "_equipe_claude_camus_brut.png")
    monkeypatch.setattr(offre, "IMG_DIR", str(tmp_path))
    return tmp_path


def test_construire_produit_un_deck_sans_defaut_de_geometrie(offre, img_synthetiques):
    prs = offre.construire()
    assert len(prs.slides) >= 10
    assert offre.D.verifier_geometrie(prs) == []
    assert not [1 for _, t in offre.texte_deck(prs) if "gaspill" in t.lower()]
