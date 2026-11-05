"""Lot s-stash-correctif3 (review confirmed against git 2.54.0.windows.1).

1 - git alias names are case-insensitive: `[alias] x = stash` then `git X` runs stash.
2 - git honours the subsection form `[alias "x"] command = stash`.
3 - config includes are capped GLOBALLY per guard call: an include DAG fan-out can no
    longer stall the guard (main session allows, sub-agent denies).

Hooks tested like production: payload JSON on stdin of a real interpreter, cwd in a
throwaway repo, HOME/USERPROFILE/GIT_CONFIG_GLOBAL pinned into tmp_path.
"""

import json
import os
import subprocess
import sys
import time

import pytest
from test_guard_stash_correctif import GUARD, _git, _payload

DELAI = 10   # a mutant without the global cap must not hang the suite


def _env(tmp_path, globale=""):
    maison = tmp_path / "maison"
    maison.mkdir(exist_ok=True)
    cfg = tmp_path / "globale.cfg"
    cfg.write_text(globale, encoding="utf-8")
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_CONFIG")}
    env.update(GIT_CONFIG_GLOBAL=str(cfg), GIT_CONFIG_NOSYSTEM="1",
               HOME=str(maison), USERPROFILE=str(maison))
    return env


def _garde(commande, sous_agent, cwd, env):
    """True = deny. A timeout counts as a failure (red), never as a pass."""
    r = subprocess.run([sys.executable, GUARD],
                       input=json.dumps(_payload(commande, sous_agent, str(cwd))),
                       capture_output=True, text=True, encoding="utf-8",
                       timeout=DELAI, env=env, cwd=str(cwd))
    assert r.returncode == 0, (r.returncode, r.stderr)
    return '"deny"' in r.stdout


@pytest.fixture
def depot(tmp_path):
    d = tmp_path / "depot"
    d.mkdir()
    _git("init", "-q", cwd=d)
    return d


# --- 1: case-insensitive alias names ---------------------------------------------------

def test_alias_majuscule_persistant_refuse_au_sous_agent(depot, tmp_path):
    env = _env(tmp_path)
    _git("config", "alias.x", "stash", cwd=depot)
    assert _garde("git X", True, depot, env)
    assert _garde("git X list", False, depot, env) is False


def test_alias_majuscule_en_ligne_refuse_au_sous_agent(depot, tmp_path):
    env = _env(tmp_path)
    # `stash list` itself is allowed by policy: the bare form (stash push) is the proof
    assert _garde("git -c alias.x=stash X", True, depot, env)
    assert _garde("git -c alias.x=stash X drop", True, depot, env)
    assert _garde("git -c alias.x=stash X", False, depot, env) is False


def test_alias_majuscule_dans_la_config_refuse_au_sous_agent(depot, tmp_path):
    env = _env(tmp_path, "[alias]\n\tX = stash\n")
    assert _garde("git x", True, depot, env)


def test_stash_majuscule_resolu_comme_alias(depot, tmp_path):
    # the built-in is case-sensitive: `git STASH` runs the alias `stash`, if any
    env = _env(tmp_path)
    _git("config", "alias.stash", "stash", cwd=depot)
    assert _garde("git STASH", True, depot, env)
    assert _garde("git STASH", False, depot, env) is False


def test_stash_majuscule_resout_l_alias_pas_le_built_in(depot, tmp_path):
    # git 2.54: `git -c alias.stash="reset --hard" STASH` runs reset --hard, not stash.
    # (`alias.stash=status` + `git STASH` stays a sub-agent false refusal: the later
    # stash check reads the lowered words -- fail-closed, out of this lot.)
    env = _env(tmp_path)
    assert _garde('git -c alias.stash="reset --hard" STASH', False, depot, env)
    assert _garde("git -c alias.stash=stash STASH", True, depot, env)


def test_majuscule_vers_commande_sure_reste_permise(depot, tmp_path):
    env = _env(tmp_path)
    _git("config", "alias.x", "status", cwd=depot)
    assert _garde("git X", True, depot, env) is False


# --- 2: subsection form [alias "x"] command = ... -------------------------------------

def test_alias_sous_section_command_refuse_au_sous_agent(depot, tmp_path):
    env = _env(tmp_path, '[alias "x"]\n\tcommand = stash\n')
    assert _garde("git x", True, depot, env)
    assert _garde("git x", False, depot, env) is False


def test_alias_sous_section_dans_le_depot_refuse_au_sous_agent(depot, tmp_path):
    env = _env(tmp_path)
    with open(depot / ".git" / "config", "a", encoding="utf-8") as fh:
        fh.write('[alias "Zz"]\n\tcommand = stash drop\n')
    assert _garde("git zz", True, depot, env)


def test_alias_sous_section_en_ligne_refuse_au_sous_agent(depot, tmp_path):
    env = _env(tmp_path)
    assert _garde("git -c alias.x.command=stash x", True, depot, env)


# --- 3: global include cap -------------------------------------------------------------

def _dag(tmp_path, niveaux=4, largeur=30):
    """f0 includes f1 `largeur` times, f1 includes f2 `largeur` times... no cycle on the
    stack, but largeur**niveaux reads without a global cap."""
    d = tmp_path / "dag"
    d.mkdir()
    for n in range(niveaux + 1):
        corps = "[core]\n\tx = 1\n"
        if n < niveaux:
            cible = (d / f"f{n + 1}.cfg").as_posix()
            corps += "".join(f"[include]\n\tpath = {cible}\n" for _ in range(largeur))
        (d / f"f{n}.cfg").write_text(corps, encoding="utf-8")
    return d / "f0.cfg"


def test_eventail_d_includes_borne(depot, tmp_path):
    racine = _dag(tmp_path)
    env = _env(tmp_path, f"[include]\n\tpath = {racine.as_posix()}\n")
    _git("config", "alias.x", "status", cwd=depot)
    t0 = time.monotonic()
    principal = _garde("git x", False, depot, env)
    sous = _garde("git x", True, depot, env)
    duree = time.monotonic() - t0
    assert principal is False          # main session: fail-open
    assert sous is True                # sub-agent: fail-closed
    assert duree < 3, duree


def test_quelques_includes_restent_lus(depot, tmp_path):
    # below the cap: an alias defined in an included file is still resolved
    inc = tmp_path / "inc.cfg"
    inc.write_text("[alias]\n\ty = stash\n", encoding="utf-8")
    env = _env(tmp_path, f"[include]\n\tpath = {inc.as_posix()}\n")
    assert _garde("git y", True, depot, env)
    assert _garde("git -c alias.z=status z", True, depot, env) is False
