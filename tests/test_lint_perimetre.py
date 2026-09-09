"""Perimetre du linter (finding risque_technique « dette de lint » de l'audit
2026-09-02) : `py -m ruff check .` doit mesurer le code VIVANT du depot, pas les
copies figees de `docs/cadrage-ppt/archives/`.

Ces copies sont, de l'aveu du .gitignore qui les ecarte deja (« scratch de travail
regenerable via generate_deck.py »), des instantanes d'anciennes versions : les
lignes qu'ils portent ne seront jamais corrigees, puisque corriger une archive n'a
pas de sens. Les laisser dans le perimetre gonfle la mesure — 16 erreurs dont 10
venues d'un seul snapshot, mesure le 2026-09-09 — et noie les vraies, qui sont
justement ce que l'audit demande de traiter.

La verification n'ouvre PAS le depot : elle rejoue la configuration reelle
(`pyproject.toml` copie tel quel) sur un mini-depot jetable, ce qui la rend
portable — `archives/` est un dossier local non versionne, absent d'un clone neuf.
Deux sens verifies : l'archive est ignoree, ET le code vivant reste bien lu (une
exclusion trop large casserait le linter en silence).
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

RACINE = Path(__file__).resolve().parents[1]
PYPROJECT = RACINE / "pyproject.toml"

# Un snapshot d'archive tel qu'on en trouve reellement dans docs/cadrage-ppt/
# archives/ : imports non tries (I001) et variable morte (F841).
FICHIER_FAUTIF = "import sys, os\n\n\ndef f():\n    inutile = 1\n    return os, sys\n"


def _ruff(cwd):
    """-> liste des diagnostics ruff, ou skip si ruff n'est pas installe."""
    if shutil.which("ruff") is None:
        try:
            subprocess.run([sys.executable, "-m", "ruff", "--version"],
                           capture_output=True, check=True)
        except Exception:
            pytest.skip("ruff absent de l'environnement")
    r = subprocess.run([sys.executable, "-m", "ruff", "check",
                        "--output-format=json", "."],
                       cwd=str(cwd), capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    return json.loads(r.stdout or "[]")


@pytest.fixture
def depot_jetable(tmp_path):
    """Mini-depot portant la VRAIE configuration ruff du projet."""
    shutil.copy(PYPROJECT, tmp_path / "pyproject.toml")
    archive = tmp_path / "docs" / "cadrage-ppt" / "archives"
    archive.mkdir(parents=True)
    (archive / "generate_deck-v0.0-snapshot.py").write_text(
        FICHIER_FAUTIF, encoding="utf-8")
    vivant = tmp_path / "docs" / "cadrage-ppt"
    (vivant / "generate_deck.py").write_text(FICHIER_FAUTIF, encoding="utf-8")
    return tmp_path


def _relatifs(diagnostics, racine):
    """-> (chemin POSIX relatif au mini-depot, code) — jamais le chemin absolu :
    le dossier temporaire porte le nom du test, donc « archives »."""
    for d in diagnostics:
        chemin = Path(d.get("filename", ""))
        try:
            yield chemin.relative_to(racine).as_posix(), d.get("code")
        except ValueError:  # pragma: no cover — hors du mini-depot
            continue


def test_les_archives_figees_sortent_du_perimetre_du_linter(depot_jetable):
    diagnostics = _ruff(depot_jetable)
    dans_archives = [(c, code) for c, code in _relatifs(diagnostics, depot_jetable)
                     if c.startswith("docs/cadrage-ppt/archives/")]
    assert not dans_archives, (
        "ruff lit encore docs/cadrage-ppt/archives/ : la dette mesuree melange "
        "le code vivant et des instantanes qui ne seront jamais corriges — "
        f"{dans_archives}")


def test_le_code_vivant_reste_bien_lu(depot_jetable):
    """Ceinture et bretelles : l'exclusion ne doit pas eteindre le linter."""
    diagnostics = _ruff(depot_jetable)
    vivants = [(c, code) for c, code in _relatifs(diagnostics, depot_jetable)
               if c == "docs/cadrage-ppt/generate_deck.py"]
    assert vivants, (
        "plus aucun diagnostic sur generate_deck.py : l'exclusion posee pour "
        "les archives est trop large et neutralise la mesure de dette")
