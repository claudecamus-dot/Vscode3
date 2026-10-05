"""Le brut Openverse est validé AVANT d'être décodé (audit VSCode3 2026-10-04)."""
import os

from test_generate_deck_garde import generate_deck  # noqa: F401  (fixture)


def _lancer(generate_deck, monkeypatch, tmp_path, ecrire_brut):  # noqa: F811
    monkeypatch.setattr(generate_deck.deck_images, "IMG_DIR", str(tmp_path))
    generate_deck._ANOMALIES_BUILD[:] = []
    monkeypatch.setattr(generate_deck.stock_images, "fetch_to",
                        lambda brut, *a, **k: ecrire_brut(brut))
    decodes = []
    monkeypatch.setattr(generate_deck.deck_images, "cover_crop_to_aspect",
                        lambda brut, dest, aspect: decodes.append(brut))

    def faux_repli(dest, *a, **k):
        from PIL import Image
        Image.new("RGB", (80, 60)).save(dest)

    monkeypatch.setattr(generate_deck.nature_images, "generate_to", faux_repli)
    monkeypatch.setattr(generate_deck.deck_images, "place_image_in_frame",
                        lambda *a, **k: None)
    from pptx.util import Emu, Inches
    cadre = (0, 0, Emu(Inches(10)), Emu(Inches(7.5)), None)
    generate_deck._remplir_cadre(None, cadre, "canyon", seed=0)
    return decodes


def test_brut_hors_format_n_est_pas_decode(generate_deck, monkeypatch, tmp_path):  # noqa: F811
    decodes = _lancer(generate_deck, monkeypatch, tmp_path,
                      lambda b: open(b, "wb").write(b"pas une image"))
    assert decodes == [], "un brut non image a été décodé avant validation"
    assert not os.path.exists(tmp_path / "_brut_canyon_0.jpg")


def test_brut_surdimensionne_n_est_pas_decode(generate_deck, monkeypatch, tmp_path):  # noqa: F811
    from PIL import Image

    def gros(b):
        Image.new("L", (9000, 20)).save(b)

    decodes = _lancer(generate_deck, monkeypatch, tmp_path, gros)
    assert decodes == [], "un brut hors bornes a été décodé avant validation"


def test_brut_valide_est_decode(generate_deck, monkeypatch, tmp_path):  # noqa: F811
    from PIL import Image
    decodes = _lancer(generate_deck, monkeypatch, tmp_path,
                      lambda b: Image.new("RGB", (200, 150)).save(b))
    assert len(decodes) == 1
