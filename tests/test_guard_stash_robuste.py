"""Lot s-stash-robuste (user decision 2026-11-05): defence in depth against a COMPUTED
git sub-command, tested like production (payload JSON on stdin, subprocess).

A - prevention in guard_destructive_git.py: inline git aliases (A1, all contexts),
persistent git aliases (A2, all contexts), sub-agent fail-closed on what the guard
cannot decode in the stash family (A3).
B - detection: temoin_stash_sous_agent.py compares refs/stash between PreToolUse and
PostToolUse for a sub-agent (catches `py script.py`, invisible to any lexical rule).
"""

import json
import os
import subprocess
import sys
import time

import pytest

HUB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOOKS = os.path.join(HUB, ".claude", "hooks")
GUARD = os.path.join(HOOKS, "guard_destructive_git.py")
TEMOIN = os.path.join(HOOKS, "temoin_stash_sous_agent.py")


def _payload(commande, sous_agent, cwd=None, **extra):
    data = {"tool_name": "Bash", "tool_input": {"command": commande},
            "session_id": "sess-test", "cwd": cwd or HUB}
    if sous_agent:
        data["agent_id"] = "agent-test"
        data["agent_type"] = "general-purpose"
    data.update(extra)
    return data


def _garde(commande, sous_agent, cwd=None):
    r = subprocess.run([sys.executable, GUARD],
                       input=json.dumps(_payload(commande, sous_agent, cwd)),
                       capture_output=True, text=True, encoding="utf-8", timeout=60)
    assert r.returncode == 0, (r.returncode, r.stderr)
    return "deny" in r.stdout


# --- A: computed sub-commands -------------------------------------------------------

CALCULEES = [
    ("alias -c en ligne", "git -c alias.s=stash s pop"),
    ("variable shell", "S=stash; git $S"),
    ("substitution", "git $(echo stash) pop"),
    ("py -c os.system", "py -c \"import os; os.system('git stash')\""),
    ("backtick", "git `echo stash` pop"),
    ("variable cmd", "git %S% pop"),
    ("parenthese powershell", "git (echo stash) pop"),
    ("tete calculee", "$g = 'git'; & $g stash pop"),
    ("node -e", "node -e \"require('child_process').execSync('git stash')\""),
    ("iex concatene", "$a='stash'; Invoke-Expression ('git ' + $a + ' pop')"),
    ("config-env", "V=stash git --config-env=alias.s=V s pop"),
    ("GIT_CONFIG_KEY", "GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=alias.s GIT_CONFIG_VALUE_0=stash "
                       "git s pop"),
    ("alias shell !", "git -c 'alias.s=!git stash' s"),
    ("config ecrit un alias", "git config alias.s stash"),
    ("config --global alias", "git config --global alias.s stash"),
    ("config set alias", "git config set alias.s stash"),
]


@pytest.mark.parametrize(("nom", "cmd"), CALCULEES, ids=[n for n, _ in CALCULEES])
def test_sous_commande_calculee_refusee_pour_un_sous_agent(nom, cmd):
    assert _garde(cmd, sous_agent=True) is True


LITTERAUX_PERMIS = [
    ("commit qui cite stash", 'git commit -m "fix stash rule"'),
    ("log --grep stash", "git log --grep stash"),
    ("stash list", "git stash list"),
    ("stash show", "git stash show -p"),
    ("config lit un alias", "git config --get alias.s"),
    ("config get alias", "git config get alias.s"),
    ("status", "git status --short"),
    ("commit parentheses", 'git commit -m "fix (bug)"'),
    ("py sans git", "py -c \"print('stash')\""),
    ("alias builtin ignore par git", "git -c alias.log=stash log --oneline"),
]


@pytest.mark.parametrize(("nom", "cmd"), LITTERAUX_PERMIS, ids=[n for n, _ in LITTERAUX_PERMIS])
def test_forme_litterale_permise_pour_un_sous_agent(nom, cmd):
    assert _garde(cmd, sous_agent=True) is False


ALIAS_PRINCIPAL = [
    ("reset en ligne", "git -c alias.r=reset r --hard"),
    ("stash drop en ligne", "git -c alias.s=stash s drop"),
    ("valeur multi-mots", "git -c 'alias.rh=reset --hard' rh"),
    ("alias shell !", "git -c 'alias.x=!git reset --hard' x"),
    ("config-env", "V='reset --hard' git --config-env=alias.z=V z"),
]


@pytest.mark.parametrize(("nom", "cmd"), ALIAS_PRINCIPAL, ids=[n for n, _ in ALIAS_PRINCIPAL])
def test_alias_en_ligne_refuse_aussi_en_session_principale(nom, cmd):
    assert _garde(cmd, sous_agent=False) is True


PRINCIPAL_INCHANGE = [
    ("variable status", "git $X status"),
    ("variable seule", "S=stash; git $S"),
    ("stash pop principal", "git stash pop"),
    ("alias inoffensif", "git -c alias.st=status st"),
]


@pytest.mark.parametrize(("nom", "cmd"), PRINCIPAL_INCHANGE, ids=[n for n, _ in PRINCIPAL_INCHANGE])
def test_session_principale_inchangee(nom, cmd):
    assert _garde(cmd, sous_agent=False) is False


def _git(*args, cwd):
    subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, timeout=30)


@pytest.fixture
def depot(tmp_path):
    d = tmp_path / "depot"
    d.mkdir()
    _git("init", "-q", cwd=d)
    _git("config", "alias.s", "stash", cwd=d)
    _git("config", "alias.rh", "reset --hard", cwd=d)
    _git("config", "alias.st", "status", cwd=d)
    return d


def test_alias_persistant_stash_refuse_pour_un_sous_agent(depot):
    assert _garde("git s pop", sous_agent=True, cwd=str(depot)) is True


def test_alias_persistant_reset_hard_refuse_en_principal(depot):
    assert _garde("git rh", sous_agent=False, cwd=str(depot)) is True


def test_alias_persistant_via_moins_C(depot, tmp_path):
    assert _garde(f'git -C "{depot.as_posix()}" rh', sous_agent=False,
                  cwd=str(tmp_path)) is True


def test_alias_persistant_inoffensif_permis(depot):
    assert _garde("git st", sous_agent=True, cwd=str(depot)) is False


def test_commande_inconnue_sans_alias_permise(depot):
    assert _garde("git lfs ls-files", sous_agent=True, cwd=str(depot)) is False


def test_alias_irresolvable_refuse_pour_sous_agent_permis_en_principal(tmp_path):
    """A3(ii): the -C directory does not exist, git config fails (exit 128)."""
    absent = (tmp_path / "absent").as_posix()
    assert _garde(f'git -C "{absent}" zz', sous_agent=True, cwd=str(tmp_path)) is True
    assert _garde(f'git -C "{absent}" zz', sous_agent=False, cwd=str(tmp_path)) is False


# --- B: the stash witness -----------------------------------------------------------

def _temoin(data, env):
    r = subprocess.run([sys.executable, TEMOIN], input=json.dumps(data),
                       capture_output=True, text=True, encoding="utf-8", timeout=60, env=env)
    assert r.returncode == 0, (r.returncode, r.stderr)
    return r.stdout


@pytest.fixture
def banc(tmp_path):
    d = tmp_path / "w"
    d.mkdir()
    _git("init", "-q", cwd=d)
    _git("-c", "user.email=t@t", "-c", "user.name=t", "commit", "-q", "--allow-empty",
         "-m", "init", cwd=d)
    (d / "f.txt").write_text("a", encoding="utf-8")
    _git("add", "f.txt", cwd=d)
    _git("-c", "user.email=t@t", "-c", "user.name=t", "commit", "-q", "-m", "f", cwd=d)
    env = dict(os.environ, GUARD_CAPTURES_LOG=str(tmp_path / "captures.jsonl"),
               TEMOIN_STASH_ETAT=str(tmp_path / "etat"))
    env.pop("CLAUDE_PROJECT_DIR", None)
    return d, env, tmp_path / "captures.jsonl"


def _evt(evt, depot, sous_agent=True, tid="toolu_1"):
    data = _payload("py script.py", sous_agent, cwd=str(depot), tool_use_id=tid)
    data["hook_event_name"] = evt
    return data


def _stasher(depot):
    (depot / "f.txt").write_text("b", encoding="utf-8")
    _git("-c", "user.email=t@t", "-c", "user.name=t", "stash", cwd=depot)


def test_temoin_signale_un_stash_entre_pre_et_post(banc):
    depot, env, journal = banc
    assert _temoin(_evt("PreToolUse", depot), env) == ""
    _stasher(depot)
    out = _temoin(_evt("PostToolUse", depot), env)
    sortie = json.loads(out)
    assert sortie["hookSpecificOutput"]["hookEventName"] == "PostToolUse"
    assert "session principale" in sortie["hookSpecificOutput"]["additionalContext"]
    lignes = [json.loads(x) for x in journal.read_text(encoding="utf-8").splitlines()]
    assert len(lignes) == 1
    assert lignes[0]["garde"] == "temoin_stash_sous_agent"
    assert lignes[0]["tool_use_id"] == "toolu_1"
    assert lignes[0]["agent_id"] == "agent-test"
    assert lignes[0]["avant"]["ref"] is None and lignes[0]["apres"]["ref"]


def test_temoin_dans_un_worktree_lit_le_dossier_commun(banc, tmp_path):
    depot, env, journal = banc
    wt = tmp_path / "wt"
    _git("worktree", "add", "-q", str(wt), cwd=depot)
    assert _temoin(_evt("PreToolUse", wt), env) == ""
    _stasher(depot)
    assert "session principale" in _temoin(_evt("PostToolUse", wt), env)


def test_temoin_silencieux_sans_changement(banc):
    depot, env, journal = banc
    _temoin(_evt("PreToolUse", depot), env)
    assert _temoin(_evt("PostToolUse", depot), env) == ""
    assert not journal.exists()


def test_temoin_silencieux_hors_sous_agent(banc):
    depot, env, journal = banc
    _temoin(_evt("PreToolUse", depot, sous_agent=False), env)
    _stasher(depot)
    assert _temoin(_evt("PostToolUse", depot, sous_agent=False), env) == ""
    assert not journal.exists()


@pytest.mark.parametrize("brut", ["", "pas du json", "[1, 2]", '{"tool_input": 3}'])
def test_temoin_payload_casse_exit_0(banc, brut):
    _, env, journal = banc
    r = subprocess.run([sys.executable, TEMOIN], input=brut, capture_output=True,
                       text=True, encoding="utf-8", timeout=60, env=env)
    assert r.returncode == 0 and r.stdout == ""
    assert not journal.exists()


def test_temoin_latence_en_processus(banc):
    """< 50 ms per call, measured in-process (interpreter start-up excluded: it is
    paid once by the dispatcher on PreToolUse)."""
    depot, env, _ = banc
    sys.path.insert(0, HOOKS)
    import importlib

    import temoin_stash_sous_agent as t
    importlib.reload(t)
    os.environ["TEMOIN_STASH_ETAT"] = env["TEMOIN_STASH_ETAT"]
    try:
        durees = []
        for i in range(20):
            for evt in ("PreToolUse", "PostToolUse"):
                d0 = time.perf_counter()
                t.traiter(_evt(evt, depot, tid=f"toolu_{i}"))
                durees.append(time.perf_counter() - d0)
    finally:
        os.environ.pop("TEMOIN_STASH_ETAT", None)
    durees.sort()
    print(f"temoin latency over {len(durees)} calls: median "
          f"{durees[len(durees) // 2] * 1000:.2f} ms, max {durees[-1] * 1000:.2f} ms")
    assert durees[len(durees) // 2] < 0.05   # median: the max is printed, not pinned (load)


def test_temoin_cable_en_pre_par_le_dispatcher_et_en_post():
    with open(os.path.join(HUB, ".claude", "settings.json"), encoding="utf-8") as fh:
        hooks = json.load(fh)["hooks"]
    pre = [h["command"] for e in hooks["PreToolUse"] if e["matcher"] == "Bash|PowerShell"
           for h in e["hooks"]]
    post = [h["command"] for e in hooks["PostToolUse"] if e["matcher"] == "Bash|PowerShell"
            for h in e["hooks"]]
    assert any("guard_dispatch_pretooluse.py" in c and "temoin_stash_sous_agent.py" in c
               for c in pre)
    assert any("temoin_stash_sous_agent.py" in c for c in post)


def test_temoin_par_le_dispatcher_ne_bloque_pas(banc):
    """PreToolUse goes through the dispatcher (one interpreter): the witness must run
    there silently and record its snapshot."""
    depot, env, _ = banc
    data = _evt("PreToolUse", depot)
    r = subprocess.run([sys.executable, os.path.join(HOOKS, "guard_dispatch_pretooluse.py"),
                        "temoin_stash_sous_agent.py"], input=json.dumps(data),
                       capture_output=True, text=True, encoding="utf-8", timeout=60, env=env)
    assert r.returncode == 0, r.stderr
    assert "deny" not in r.stdout
    fichier = os.path.join(env["TEMOIN_STASH_ETAT"], "toolu_1.json")
    assert json.loads(open(fichier, encoding="utf-8").read())["tid"] == "toolu_1"
