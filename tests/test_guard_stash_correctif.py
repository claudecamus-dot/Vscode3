"""Lot s-stash-correctif (user, 2026-11-05: « corrige cette regression »).

1 - the guard resolves a persistent git alias by READING config files: no subprocess on
    its hot path (the `git config --get` child of 1433ba33 hung the guard: on timeout
    only the launcher was killed, the git grandchild kept the pipes open).
2 - review voice 1: sub-agent bypasses (alias defined outside the analysed segment,
    `xargs git`, direct refs/stash writes, `--autostash`).
3 - review voice 3: witness race (one state file per tool_use_id), journal failure,
    packed-refs / drop / corrupted state proofs, state dir outside the repo.
4 - `git commit -m "py -c stash"` is no longer a false refusal.

Hooks tested like production: payload JSON on stdin of a real interpreter.
"""

import json
import os
import subprocess
import sys
import threading
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


def _env_isole(tmp_path, **extra):
    """Global/system config pinned to empty files: the user's real ~/.gitconfig must
    not decide a test."""
    vide = tmp_path / "vide.cfg"
    vide.write_text("", encoding="utf-8")
    env = dict(os.environ, GIT_CONFIG_GLOBAL=str(vide), GIT_CONFIG_NOSYSTEM="1")
    for k in [k for k in env if k.startswith("GIT_CONFIG_") and k not in
              ("GIT_CONFIG_GLOBAL", "GIT_CONFIG_NOSYSTEM")]:
        env.pop(k)
    env.update(extra)
    return env


def _garde_brut(commande, sous_agent, cwd=None, env=None):
    r = subprocess.run([sys.executable, GUARD],
                       input=json.dumps(_payload(commande, sous_agent, cwd)),
                       capture_output=True, text=True, encoding="utf-8", timeout=60, env=env)
    assert r.returncode == 0, (r.returncode, r.stderr)
    return r.stdout


def _garde(commande, sous_agent, cwd=None, env=None):
    return "deny" in _garde_brut(commande, sous_agent, cwd, env)


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


# --- 1: no subprocess on the hot path ------------------------------------------------

_AMORCE = r'''
import contextlib, io, json, os, runpy, subprocess, sys, time
appels = []
def _interdit(*a, **k):
    appels.append(repr(a[:1])[:80])
    raise OSError("subprocess forbidden by the test")
subprocess.Popen = _interdit
os.system = _interdit
os.popen = _interdit
for nom in ("spawnv", "spawnve", "spawnl", "startfile", "posix_spawn", "execv"):
    if hasattr(os, nom):
        setattr(os, nom, _interdit)
t0 = time.perf_counter()
sortie = io.StringIO()
with contextlib.redirect_stdout(sortie):
    try:
        runpy.run_path(sys.argv[1], run_name="__main__")
    except SystemExit:
        pass
sys.__stdout__.write(json.dumps({"out": sortie.getvalue(), "appels": appels,
                                 "s": time.perf_counter() - t0}))
'''


def _garde_sans_sous_processus(tmp_path, commande, sous_agent, cwd, env):
    amorce = tmp_path / "amorce.py"
    amorce.write_text(_AMORCE, encoding="utf-8")
    r = subprocess.run([sys.executable, str(amorce), GUARD],
                       input=json.dumps(_payload(commande, sous_agent, cwd)),
                       capture_output=True, text=True, encoding="utf-8", timeout=60, env=env)
    assert r.returncode == 0, r.stderr
    return json.loads(r.stdout)


def test_alias_persistant_resolu_sans_aucun_sous_processus(depot, tmp_path):
    """The hang of 1433ba33: the guard must resolve `git rh` (= reset --hard, repo
    config) with every process-spawning API forbidden, and return in < 3 s."""
    env = _env_isole(tmp_path)
    res = _garde_sans_sous_processus(tmp_path, "git rh", False, str(depot), env)
    print("in-process guard time:", round(res["s"], 3), "s; spawns:", res["appels"])
    assert res["appels"] == []
    assert "deny" in res["out"]
    assert res["s"] < 3.0


def test_sous_agent_alias_stash_sans_sous_processus(depot, tmp_path):
    env = _env_isole(tmp_path)
    res = _garde_sans_sous_processus(tmp_path, "git s pop", True, str(depot), env)
    assert res["appels"] == [] and "deny" in res["out"]
    res = _garde_sans_sous_processus(tmp_path, "git st", True, str(depot), env)
    assert res["appels"] == [] and "deny" not in res["out"]


# --- 1: the config-file reader --------------------------------------------------------

def test_alias_global_via_git_config_global(tmp_path):
    cfg = tmp_path / "g.cfg"
    cfg.write_text("[alias]\n\trh = reset --hard\n", encoding="utf-8")
    env = _env_isole(tmp_path, GIT_CONFIG_GLOBAL=str(cfg))
    assert _garde("git rh", False, cwd=str(tmp_path), env=env) is True


def test_alias_via_chaine_include_path(depot, tmp_path):
    b = tmp_path / "b.cfg"
    b.write_text("[alias]\n  zz = reset --hard\n", encoding="utf-8")
    a = tmp_path / "a.cfg"
    a.write_text("[include]\n  path = b.cfg\n", encoding="utf-8")   # relative to a.cfg
    _git("config", "include.path", str(a), cwd=depot)
    env = _env_isole(tmp_path)
    assert _garde("git zz", False, cwd=str(depot), env=env) is True


def test_alias_via_include_if(depot, tmp_path):
    c = tmp_path / "c.cfg"
    c.write_text("[alias]\n  yy = stash\n", encoding="utf-8")
    with open(depot / ".git" / "config", "a", encoding="utf-8") as fh:
        fh.write(f'[includeIf "gitdir:/nulle/part/"]\n\tpath = {c.as_posix()}\n')
    env = _env_isole(tmp_path)
    assert _garde("git yy pop", True, cwd=str(depot), env=env) is True


def test_valeur_citee_continuation_commentaire_casse(depot, tmp_path):
    with open(depot / ".git" / "config", "a", encoding="utf-8") as fh:
        fh.write('[Alias]\n\tXq = "sta"\\\n"sh" ; a comment\n\tvv = status # c\n')
    env = _env_isole(tmp_path)
    assert _garde("git xq pop", True, cwd=str(depot), env=env) is True
    assert _garde("git vv", True, cwd=str(depot), env=env) is False


def test_alias_depuis_un_worktree(depot, tmp_path):
    _git("-c", "user.email=t@t", "-c", "user.name=t", "commit", "-q", "--allow-empty",
         "-m", "i", cwd=depot)
    wt = tmp_path / "wt"
    _git("worktree", "add", "-q", str(wt), cwd=depot)
    env = _env_isole(tmp_path)
    assert _garde("git rh", False, cwd=str(wt), env=env) is True


def test_fichier_illisible_echec_refus_sous_agent_permis_principal(tmp_path):
    dossier = tmp_path / "pas_un_fichier"
    dossier.mkdir()
    env = _env_isole(tmp_path, GIT_CONFIG_GLOBAL=str(dossier))
    assert _garde("git zz", True, cwd=str(tmp_path), env=env) is True
    assert _garde("git zz", False, cwd=str(tmp_path), env=env) is False


def test_fichier_mal_forme_echec(tmp_path):
    cfg = tmp_path / "bad.cfg"
    cfg.write_text("[alias\n  zz = stash\n", encoding="utf-8")
    env = _env_isole(tmp_path, GIT_CONFIG_GLOBAL=str(cfg))
    assert _garde("git zz", True, cwd=str(tmp_path), env=env) is True
    assert _garde("git zz", False, cwd=str(tmp_path), env=env) is False


def test_commande_inconnue_sans_alias_permise(depot, tmp_path):
    env = _env_isole(tmp_path)
    assert _garde("git frobnicate", True, cwd=str(depot), env=env) is False
    assert _garde("git frobnicate", False, cwd=str(depot), env=env) is False


# --- 2a: alias defined outside the analysed segment -----------------------------------

HORS_SEGMENT = [
    ("export en une fois", "export GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=alias.s "
                           "GIT_CONFIG_VALUE_0=stash; git s"),
    ("trois exports", "export GIT_CONFIG_COUNT=1; export GIT_CONFIG_KEY_0=alias.s; "
                      "export GIT_CONFIG_VALUE_0=stash; git s"),
    ("affectation puis export", "GIT_CONFIG_COUNT=1 && GIT_CONFIG_KEY_0=alias.s && "
                                "GIT_CONFIG_VALUE_0=stash && export GIT_CONFIG_COUNT "
                                "GIT_CONFIG_KEY_0 GIT_CONFIG_VALUE_0 && git s pop"),
    ("powershell env", "$env:GIT_CONFIG_COUNT=1; $env:GIT_CONFIG_KEY_0='alias.s'; "
                       "$env:GIT_CONFIG_VALUE_0='stash'; git s pop"),
    ("powershell env espaces", "$env:GIT_CONFIG_PARAMETERS = \"'alias.s=stash'\"; git s pop"),
    ("include.path en ligne absent", "git -c include.path=/tmp/x_absent_zz.cfg s"),
    ("GIT_CONFIG_GLOBAL absent", "GIT_CONFIG_GLOBAL=/tmp/x_absent_zz.cfg git s"),
    ("fichier ecrit dans la commande", "printf '[alias]\\n s = stash\\n' > /tmp/x_zz.cfg; "
                                       "GIT_CONFIG_GLOBAL=/tmp/x_zz.cfg git s pop"),
    ("valeur calculee", "export GIT_CONFIG_GLOBAL=$F; git s pop"),
]


@pytest.mark.parametrize(("nom", "cmd"), HORS_SEGMENT, ids=[n for n, _ in HORS_SEGMENT])
def test_alias_hors_segment_refuse_pour_un_sous_agent(nom, cmd, tmp_path):
    assert _garde(cmd, True, cwd=str(tmp_path), env=_env_isole(tmp_path)) is True


def test_include_path_en_ligne_lu(tmp_path):
    cfg = tmp_path / "x.cfg"
    cfg.write_text("[alias]\n rh = reset --hard\n", encoding="utf-8")
    env = _env_isole(tmp_path)
    assert _garde(f'git -c include.path="{cfg.as_posix()}" rh', False,
                  cwd=str(tmp_path), env=env) is True


def test_git_config_global_en_ligne_lu(tmp_path):
    cfg = tmp_path / "x.cfg"
    cfg.write_text("[alias]\n rh = reset --hard\n", encoding="utf-8")
    env = _env_isole(tmp_path)
    assert _garde(f'GIT_CONFIG_GLOBAL="{cfg.as_posix()}" git rh', False,
                  cwd=str(tmp_path), env=env) is True


def test_export_suivi_en_session_principale(tmp_path):
    cmd = ("export GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=alias.r "
           "GIT_CONFIG_VALUE_0='reset --hard'; git r")
    assert _garde(cmd, False, cwd=str(tmp_path), env=_env_isole(tmp_path)) is True


def test_variable_config_sans_alias_ne_gene_pas_un_builtin(tmp_path):
    env = _env_isole(tmp_path)
    assert _garde("GIT_CONFIG_GLOBAL=/tmp/x_absent_zz.cfg git status", True,
                  cwd=str(tmp_path), env=env) is False


# --- 2b: xargs git ---------------------------------------------------------------------

XARGS = [
    ("xargs git", "echo stash | xargs git"),
    ("xargs git avec pop", "echo stash pop | xargs git"),
    ("xargs -I", "echo stash | xargs -I{} git {} pop"),
    ("xargs -n1 -c", "echo stash | xargs -n1 git -c core.pager=cat"),
]


@pytest.mark.parametrize(("nom", "cmd"), XARGS, ids=[n for n, _ in XARGS])
def test_xargs_git_sans_sous_commande_litterale_refuse(nom, cmd):
    assert _garde(cmd, True) is True
    assert _garde(cmd, False) is False


def test_xargs_git_litteral_permis():
    assert _garde("echo f.txt | xargs git add", True) is False


# --- 2c: direct refs/stash writes ------------------------------------------------------

ECRITURES_STASH = [
    ("update-ref", "git update-ref refs/stash HEAD"),
    ("update-ref -d", "git update-ref -d refs/stash"),
    ("reflog delete", "git reflog delete stash@{0}"),
    ("reflog expire", "git reflog expire --expire=now refs/stash"),
    ("reflog expire --all", "git reflog expire --expire=now --all"),
    ("update-ref --stdin", "echo 'delete refs/stash' | git update-ref --stdin"),
]


@pytest.mark.parametrize(("nom", "cmd"), ECRITURES_STASH, ids=[n for n, _ in ECRITURES_STASH])
def test_ecriture_directe_de_refs_stash(nom, cmd):
    assert _garde(cmd, True) is True
    assert _garde(cmd, False) is False   # main context unchanged


LECTURES_STASH = [
    ("show", "git show stash@{0}"),
    ("log", "git log refs/stash"),
    ("rev-parse", "git rev-parse stash@{0}"),
    ("reflog show", "git reflog show stash"),
    ("commit qui cite refs/stash", 'git commit -m "fix refs/stash reader"'),
]


@pytest.mark.parametrize(("nom", "cmd"), LECTURES_STASH, ids=[n for n, _ in LECTURES_STASH])
def test_lecture_de_refs_stash_permise(nom, cmd):
    assert _garde(cmd, True) is False


# --- 2d: --autostash -------------------------------------------------------------------

AUTOSTASH = [
    ("rebase", "git rebase --autostash main"),
    ("pull", "git pull --autostash"),
    ("merge", "git merge --autostash feature"),
    ("prefixe", "git rebase --autost main"),
    ("config en ligne", "git -c rebase.autoStash=true rebase main"),
]


@pytest.mark.parametrize(("nom", "cmd"), AUTOSTASH, ids=[n for n, _ in AUTOSTASH])
def test_autostash_refuse_pour_un_sous_agent(nom, cmd):
    sortie = _garde_brut(cmd, True)
    assert "deny" in sortie and "autostash" in sortie.lower()
    assert _garde(cmd, False) is False


def test_autostash_par_config_du_depot(depot, tmp_path):
    _git("config", "rebase.autoStash", "true", cwd=depot)
    env = _env_isole(tmp_path)
    assert _garde("git rebase main", True, cwd=str(depot), env=env) is True
    assert _garde("git rebase --no-autostash main", True, cwd=str(depot), env=env) is False
    assert _garde("git rebase main", False, cwd=str(depot), env=env) is False


def test_sans_autostash_permis(tmp_path):
    env = _env_isole(tmp_path)
    assert _garde("git rebase main", True, cwd=str(tmp_path), env=env) is False


# --- 4: interpreter only in command position -------------------------------------------

def test_commit_qui_cite_py_c_stash_permis():
    assert _garde('git commit -m "py -c stash"', True) is False


def test_interpreteur_en_tete_toujours_refuse():
    assert _garde("py -c \"import os; os.system('git stash')\"", True) is True
    assert _garde("cd x && node -e \"require('child_process').execSync('git stash')\"",
                  True) is True


# --- 3: the witness --------------------------------------------------------------------

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
    etat = tmp_path / "etat"
    env = dict(os.environ, GUARD_CAPTURES_LOG=str(tmp_path / "captures.jsonl"),
               TEMOIN_STASH_ETAT=str(etat))
    env.pop("CLAUDE_PROJECT_DIR", None)
    return d, env, tmp_path / "captures.jsonl", etat


def _evt(evt, depot, sous_agent=True, tid="toolu_1"):
    data = _payload("py script.py", sous_agent, cwd=str(depot), tool_use_id=tid)
    data["hook_event_name"] = evt
    return data


def _stasher(depot, contenu="b"):
    (depot / "f.txt").write_text(contenu, encoding="utf-8")
    _git("-c", "user.email=t@t", "-c", "user.name=t", "stash", cwd=depot)


def _sha_stash(depot):
    return subprocess.run(["git", "rev-parse", "refs/stash"], cwd=depot, capture_output=True,
                          text=True, check=True, timeout=30).stdout.strip()


def test_temoin_concurrence_douze_appels_paralleles(banc):
    """3a: 12 parallel PreToolUse with distinct tool_use_id, then a stash, then 12
    parallel PostToolUse: every Post must report (a lost state entry = silent Post)."""
    depot, env, _, _ = banc
    n = 12

    def _lancer(evt):
        procs = []
        for _ in range(n):
            p = subprocess.Popen([sys.executable, TEMOIN], stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
            procs.append(p)
        # every interpreter started, then all payloads released together; communicate()
        # (one thread each) tolerates the EINVAL a Windows pipe raises on a raw write
        sorties = [""] * n
        barriere = threading.Barrier(n)

        def _un(i):
            barriere.wait()
            out, _ = procs[i].communicate(
                json.dumps(_evt(evt, depot, tid=f"toolu_c{i}")).encode(), timeout=120)
            sorties[i] = out.decode("utf-8", "replace")

        time.sleep(1.5)
        fils = [threading.Thread(target=_un, args=(i,)) for i in range(n)]
        for f in fils:
            f.start()
        for f in fils:
            f.join(180)
        return sorties

    assert all(s == "" for s in _lancer("PreToolUse"))
    _stasher(depot)
    sorties = _lancer("PostToolUse")
    signales = sum(1 for s in sorties if "refs/stash" in s)
    print(f"concurrency: {signales}/{n} Post reported")
    assert signales == n


def test_temoin_message_emis_meme_si_le_journal_echoue(banc, tmp_path):
    """3b: journal path = a directory, the write fails, the message is still emitted."""
    depot, env, _, _ = banc
    jdir = tmp_path / "journal_dossier"
    jdir.mkdir()
    env = dict(env, GUARD_CAPTURES_LOG=str(jdir))
    _temoin(_evt("PreToolUse", depot), env)
    _stasher(depot)
    out = _temoin(_evt("PostToolUse", depot), env)
    assert "refs/stash" in out


def test_temoin_message_dit_detecte_pendant_votre_appel(banc):
    """3d: another session may have stashed during the call."""
    depot, env, _, _ = banc
    _temoin(_evt("PreToolUse", depot), env)
    _stasher(depot)
    texte = json.loads(_temoin(_evt("PostToolUse", depot), env))["reason"]
    assert "détecté pendant votre appel" in texte
    assert "vous avez modifié" not in texte.lower()


def test_temoin_packed_refs_seul(banc):
    """3c: refs/stash only in packed-refs (`git pack-refs --all`): the Pre snapshot must
    carry the packed value (a neutralised packed-refs read gives None)."""
    depot, env, journal, _ = banc
    _stasher(depot, "b")
    sha_a = _sha_stash(depot)
    _git("pack-refs", "--all", cwd=depot)
    assert not (depot / ".git" / "refs" / "stash").exists()
    _temoin(_evt("PreToolUse", depot), env)
    _stasher(depot, "c")
    sha_b = _sha_stash(depot)
    assert "refs/stash" in _temoin(_evt("PostToolUse", depot), env)
    ligne = json.loads(journal.read_text(encoding="utf-8").splitlines()[-1])
    assert ligne["avant"]["ref"] == sha_a
    assert ligne["apres"]["ref"] == sha_b


def test_temoin_remise_videe_par_drop(banc):
    """3c: the last stash dropped deletes refs/stash: reported, after = none."""
    depot, env, journal, _ = banc
    _stasher(depot)
    _temoin(_evt("PreToolUse", depot), env)
    _git("stash", "drop", cwd=depot)
    assert "aucune" in _temoin(_evt("PostToolUse", depot), env)
    ligne = json.loads(journal.read_text(encoding="utf-8").splitlines()[-1])
    assert ligne["apres"]["ref"] is None


def test_temoin_etat_corrompu_silencieux(banc):
    depot, env, journal, etat = banc
    _temoin(_evt("PreToolUse", depot), env)
    fichiers = list(etat.iterdir())
    assert len(fichiers) == 1
    fichiers[0].write_text("{pas du json", encoding="utf-8")
    _stasher(depot)
    assert _temoin(_evt("PostToolUse", depot), env) == ""
    assert not journal.exists()


def test_temoin_post_supprime_son_fichier(banc):
    depot, env, _, etat = banc
    _temoin(_evt("PreToolUse", depot, tid="toolu_x"), env)
    _temoin(_evt("PreToolUse", depot, tid="toolu_y"), env)
    assert len(list(etat.iterdir())) == 2
    _temoin(_evt("PostToolUse", depot, tid="toolu_x"), env)
    assert len(list(etat.iterdir())) == 1


def test_temoin_tid_hostile_reste_dans_le_dossier(banc, tmp_path):
    depot, env, _, etat = banc
    _temoin(_evt("PreToolUse", depot, tid="../../evade"), env)
    assert not (tmp_path / "evade.json").exists()
    assert len(list(etat.iterdir())) == 1


def test_temoin_etat_par_defaut_sous_le_temp_utilisateur(banc, tmp_path):
    """3e: default state dir under the user temp dir, nothing in .claude/supervision."""
    depot, env, _, _ = banc
    temp = tmp_path / "temp_user"
    temp.mkdir()
    env = dict(env, TEMP=str(temp), TMP=str(temp), TMPDIR=str(temp))
    env.pop("TEMOIN_STASH_ETAT")
    _temoin(_evt("PreToolUse", depot, tid="toolu_def"), env)
    assert (temp / "claude-temoin-stash" / "toolu_def.json").is_file()


def test_temoin_principal_demarrage_a_froid(banc):
    """5: PostToolUse main-session path = immediate exit; median cold start quoted
    against an empty interpreter (printed, loosely bounded: the machine is loaded)."""
    depot, env, _, _ = banc
    brut = json.dumps(_evt("PostToolUse", depot, sous_agent=False))

    def _mediane(argv, entree):
        d = []
        for _ in range(9):
            t0 = time.perf_counter()
            subprocess.run(argv, input=entree, capture_output=True, text=True, env=env,
                           timeout=60)
            d.append(time.perf_counter() - t0)
        d.sort()
        return d[len(d) // 2]

    vide = _mediane([sys.executable, "-c", "pass"], "")
    temoin = _mediane([sys.executable, TEMOIN], brut)
    print(f"cold start median: empty interpreter {vide * 1000:.0f} ms, "
          f"witness main-session Post {temoin * 1000:.0f} ms")
    assert temoin < vide + 0.5
