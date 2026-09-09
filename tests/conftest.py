"""Un git qui fonctionne dans les dossiers de test, même lancé depuis un bac à sable.

Bloc REPORTÉ du conftest du hub VScode5 (mesuré là-bas le 2026-09-08, 36 échecs sur
1274), à l'identique de son commentaire d'origine résumé ici. Le reste du conftest du
hub (isolation de `jobs.jsonl`/`vues.jsonl`) est propre au hub et n'est pas repris :
VSCode3 n'a ni serveur de wiki ni ces journaux.

Deux causes DISTINCTES, invisibles au code testé, faisaient échouer tout `git init` /
`git config` / `git status` dans un dossier de test :

1. Python >= 3.13 honore le mode 0o700 sous Windows : `tmp_path`, `mkdtemp` et le
   `--basetemp` de pytest naissent avec une ACL « propriétaire seul », sans héritage.
   Le git lancé depuis le bac à sable d'une session Claude Code n'y entre pas :
   « fatal: unable to get current working directory ».
2. Les dossiers créés depuis ce bac à sable appartiennent à BUILTIN\\Administrators, et
   git refuse alors le dépôt qu'il vient de créer : « detected dubious ownership » dès
   la commande suivante.

Ce n'est donc ni la longueur du chemin ni l'emplacement : six essais de `--basetemp`
(chemin court, %TEMP%, le projet lui-même) n'y avaient rien changé.

Les deux gestes, chacun conditionné par un SONDAGE de session (un poste où git
travaille normalement ne paie rien et ne change rien) : rétablir l'héritage de l'ACL
parente sur le basetemp puis sur chaque `tmp_path` (override du fixture, qui demande le
fixture natif du même nom) ; et poser `safe.directory=*` par l'environnement
(`GIT_CONFIG_COUNT`, lu par tous les git fils), jamais dans un fichier de configuration
— la session seule le voit.
"""

import os
import subprocess

import pytest


def _relacher_acl(chemin) -> None:
    """Rétablit l'héritage de l'ACL parente — le dossier redevient un dossier
    ordinaire, sans ajouter de droit qui n'existe pas déjà sur son parent."""
    subprocess.run(["icacls", str(chemin), "/inheritance:e"],
                   capture_output=True, check=False)


def _git(cwd, *args) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=str(cwd), capture_output=True,
                          check=False)


def _git_refuse_un_dossier_0o700(base) -> bool:
    sonde = base / "sonde-acl-0o700"
    try:
        sonde.mkdir(0o700)
    except OSError:
        return False
    return _git(sonde, "init", "-q").returncode != 0


def _git_doute_du_proprietaire(base) -> bool:
    sonde = base / "sonde-proprietaire"
    try:
        sonde.mkdir()
    except OSError:
        return False
    if _git(sonde, "init", "-q").returncode != 0:
        return False
    r = _git(sonde, "status", "--porcelain")
    return r.returncode != 0 and b"dubious ownership" in r.stderr


def _autoriser_tout_depot_pour_la_session() -> None:
    n = int(os.environ.get("GIT_CONFIG_COUNT", "0") or 0)
    os.environ[f"GIT_CONFIG_KEY_{n}"] = "safe.directory"
    os.environ[f"GIT_CONFIG_VALUE_{n}"] = "*"
    os.environ["GIT_CONFIG_COUNT"] = str(n + 1)


@pytest.fixture(scope="session", autouse=True)
def _git_dans_les_dossiers_de_test(tmp_path_factory) -> bool:
    """Rend True si l'ACL de chaque `tmp_path` est à relâcher."""
    if os.name != "nt":
        return False
    base = tmp_path_factory.getbasetemp()
    relacher = _git_refuse_un_dossier_0o700(base)
    if relacher:
        _relacher_acl(base)
    if _git_doute_du_proprietaire(base):
        _autoriser_tout_depot_pour_la_session()
    return relacher


@pytest.fixture
def tmp_path(tmp_path, _git_dans_les_dossiers_de_test):  # noqa: F811 — override voulu
    if _git_dans_les_dossiers_de_test:
        _relacher_acl(tmp_path)
    return tmp_path
