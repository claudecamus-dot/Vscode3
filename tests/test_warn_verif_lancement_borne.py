"""Migration of warn_verif_before_commit's git calls to `_lancement_borne`.

Each migrated site (`_staged_files`, `_diff_ajoute`, `_sites_nus`) must return
the same value as before on a forced timeout, a forced launch error and a
non-zero exit code -- with the module present AND absent (fallback to the
previous `subprocess.run` call).
"""

import importlib.util
import pathlib
import subprocess
import sys

import pytest

HOOKS = pathlib.Path(__file__).resolve().parents[1] / ".claude" / "hooks"


def _load(nom, fichier):
    spec = importlib.util.spec_from_file_location(nom, HOOKS / fichier)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


hook = _load("warn_verif_lb_sous_test", "warn_verif_before_commit.py")
LB = hook._lancement_borne()

SITES = [
    ("staged", lambda: hook._staged_files(None, None), None),
    ("diff", lambda: hook._diff_ajoute(None, None), ""),
    ("grep", lambda: hook._sites_nus(None, "x(", ["app/"]), []),
]

ERREURS = [
    subprocess.TimeoutExpired(["git"], 8),
    FileNotFoundError("git"),
    PermissionError("git"),
    subprocess.SubprocessError("OSError: boom"),
]


def test_module_present_et_charge():
    assert LB is not None and hasattr(LB, "lancer_texte")


@pytest.mark.parametrize("erreur", ERREURS, ids=lambda e: type(e).__name__)
@pytest.mark.parametrize("nom,site,attendu", SITES, ids=[s[0] for s in SITES])
def test_erreur_forcee_meme_valeur_avec_module(monkeypatch, nom, site, attendu, erreur):
    def leve(*a, **k):
        raise erreur
    appels = []
    monkeypatch.setattr(LB, "lancer_borne", lambda *a, **k: (appels.append(1), leve())[1])
    monkeypatch.setattr(subprocess, "run", lambda *a, **k: pytest.fail("old call used"))
    assert site() == attendu
    assert appels, "bounded launcher not used"


@pytest.mark.parametrize("erreur", ERREURS, ids=lambda e: type(e).__name__)
@pytest.mark.parametrize("nom,site,attendu", SITES, ids=[s[0] for s in SITES])
def test_erreur_forcee_meme_valeur_sans_module(monkeypatch, nom, site, attendu, erreur):
    monkeypatch.setitem(sys.modules, "_lancement_borne", None)  # import fails
    appels = []

    def leve(*a, **k):
        appels.append(k)
        raise erreur
    monkeypatch.setattr(subprocess, "run", leve)
    assert site() == attendu
    assert appels and appels[0].get("capture_output") and appels[0].get("errors") == "replace"


@pytest.mark.parametrize("nom,site,attendu", SITES, ids=[s[0] for s in SITES])
def test_code_non_nul_meme_valeur(monkeypatch, nom, site, attendu):
    monkeypatch.setattr(LB, "lancer_borne", lambda cmd, **k: subprocess.CompletedProcess(
        cmd, 128, b"a.py\n", b"fatal"))
    assert site() == attendu
    monkeypatch.setitem(sys.modules, "_lancement_borne", None)
    monkeypatch.setattr(subprocess, "run", lambda cmd, **k: subprocess.CompletedProcess(
        cmd, 128, "a.py\n", "fatal"))
    assert site() == attendu


def test_succes_decode_comme_avant(monkeypatch):
    monkeypatch.setattr(LB, "lancer_borne", lambda cmd, **k: subprocess.CompletedProcess(
        cmd, 0, "app/\xe9.py\r\n".encode("utf-8") + b"\xff\n", b""))
    assert hook._sites_nus(None, "x(", ["app/"]) == ["app/\xe9.py", "�"]
