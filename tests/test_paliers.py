"""Verrouille les paliers de test : un test oublie par la partition ferait sauter un palier sans bruit.

Collecte en sous-processus sur TOUT `tests/` (lance seul, ce fichier ne contiendrait que lui-meme)."""
import subprocess
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent


def _collecte(*marqueur):
    r = subprocess.run([sys.executable, "-m", "pytest", "tests", "--collect-only", "-q", "--no-cov", "-p", "no:cacheprovider", *marqueur],
                       cwd=str(RACINE), capture_output=True, text=True, timeout=120)
    return {ligne.replace("\\", "/").strip() for ligne in r.stdout.splitlines() if "::" in ligne}


def test_les_paliers_partitionnent_la_suite():
    tout = _collecte()
    dispositif = {n for n in tout if n.split("::")[0].split("/")[-1].startswith(("test_agent_", "test_guard_", "test_warn_", "test_lint_perimetre"))}
    livrable = {n for n in tout if n.split("::")[0].split("/")[-1].startswith(("test_deck_delta", "test_charte_livrable", "test_paliers"))}
    assert dispositif and livrable and not dispositif & livrable
    assert _collecte("-m", "dispositif") == dispositif
    assert _collecte("-m", "livrable") == livrable
