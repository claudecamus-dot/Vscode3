"""Le volet ARBRE du garde-fou git, backporté de VSCode2 le 2026-09-07.

`guard_destructive_git.py` ne connaissait que deux commandes qui touchent
l'HISTORIQUE (`push --force`, `reset --hard`). Un incident réel du 2026-09-02 (VSCode2) a
montré la classe manquante : les commandes qui écrasent le travail non commité d'un
fichier dans l'ARBRE (`git checkout -- <chemin>`, `git restore <chemin>`, `git clean -f`,
`git stash drop/clear`). VSCode2 avait écrit le correctif sans test — ce fichier ferme ce
trou pour la version canon.

Chaque cas est vérifié par le CHEMIN RÉEL (stdin JSON, stdout JSON), plus un contrôle par
EFFET RÉEL sur un dépôt jetable pour `checkout --` : sans ça on bloquerait une syntaxe sur
la foi d'un raisonnement, pas d'une preuve (même discipline que
`test_guard_destructive_contournements.py`).
"""

import importlib.util
import json
import os
import subprocess
import sys

import pytest

HUB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOOK = os.path.join(HUB, ".claude", "hooks", "guard_destructive_git.py")

_spec = importlib.util.spec_from_file_location("guard_test_arbre", HOOK)
guard = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(guard)


def _bloque(commande, cwd=None):
    env = dict(os.environ)
    if cwd is not None:
        env["CLAUDE_PROJECT_DIR"] = str(cwd)
    r = subprocess.run(
        [sys.executable, HOOK],
        input=json.dumps({"tool_input": {"command": commande}}),
        capture_output=True, text=True, encoding="utf-8",
        cwd=str(cwd) if cwd is not None else None, env=env)
    # Sans ce controle, un hook casse a l'import (returncode != 0) rendait
    # "deny" absent de stdout comme un hook sain qui laisse passer -- les
    # assertions `not _bloque(...)` passaient TOUTES au vert sur un
    # garde-fou entierement mort (revue adversariale du 2026-09-07).
    assert r.returncode == 0 and not r.stderr, (
        f"le hook a plante au lieu de repondre : code={r.returncode} stderr={r.stderr!r}")
    return "deny" in r.stdout


class TestCheckoutDeChemin:
    def test_checkout_double_tiret_chemin_bloque(self, tmp_path):
        (tmp_path / "f.txt").write_text("v1\n", encoding="utf-8")
        assert _bloque("git checkout -- f.txt", cwd=tmp_path)

    def test_checkout_chemin_existant_sans_double_tiret_bloque(self, tmp_path):
        (tmp_path / "app").mkdir()
        (tmp_path / "app" / "x.html").write_text("v1\n", encoding="utf-8")
        assert _bloque("git checkout app/x.html", cwd=tmp_path)

    def test_checkout_branche_reste_autorise(self, tmp_path):
        assert not _bloque("git checkout main", cwd=tmp_path)
        assert not _bloque("git checkout -b feature/x", cwd=tmp_path)

    def test_checkout_effet_reel_ecrase_le_travail_non_commite(self, tmp_path):
        depot = tmp_path / "d"
        depot.mkdir()

        def git(*a):
            return subprocess.run(["git", *a], cwd=str(depot), capture_output=True,
                                   text=True, encoding="utf-8")
        git("init", "-q")
        git("config", "user.email", "t@t")
        git("config", "user.name", "t")
        (depot / "f.txt").write_text("v1\n", encoding="utf-8")
        git("add", "-A")
        git("commit", "-qm", "c1")
        (depot / "f.txt").write_text("TRAVAIL-NON-COMMITE\n", encoding="utf-8")
        r = git("checkout", "--", "f.txt")
        assert r.returncode == 0, f"git a refuse le checkout : {r.stderr}"
        assert (depot / "f.txt").read_text(encoding="utf-8") == "v1\n", (
            "le checkout ne détruit rien — le garde-fou n'aurait pas à le bloquer")


class TestRestoreDeChemin:
    def test_restore_chemin_bloque(self, tmp_path):
        (tmp_path / "f.txt").write_text("v1\n", encoding="utf-8")
        assert _bloque("git restore f.txt", cwd=tmp_path)

    def test_restore_staged_seul_reste_autorise(self, tmp_path):
        assert not _bloque("git restore --staged f.txt", cwd=tmp_path)

    def test_restore_staged_et_worktree_bloque(self, tmp_path):
        (tmp_path / "f.txt").write_text("v1\n", encoding="utf-8")
        assert _bloque("git restore --staged --worktree f.txt", cwd=tmp_path)


class TestCleanForce:
    def test_clean_f_bloque(self, tmp_path):
        assert _bloque("git clean -f", cwd=tmp_path)

    def test_clean_fd_groupe_bloque(self, tmp_path):
        assert _bloque("git clean -fd", cwd=tmp_path)

    def test_clean_dry_run_reste_autorise(self, tmp_path):
        assert not _bloque("git clean -n", cwd=tmp_path)


class TestStashDropClear:
    def test_stash_drop_bloque(self, tmp_path):
        assert _bloque("git stash drop", cwd=tmp_path)

    def test_stash_clear_bloque(self, tmp_path):
        assert _bloque("git stash clear", cwd=tmp_path)

    def test_stash_push_et_pop_restent_autorises(self, tmp_path):
        assert not _bloque("git stash push -u", cwd=tmp_path)
        assert not _bloque("git stash pop", cwd=tmp_path)
        assert not _bloque("git stash list", cwd=tmp_path)


class TestCommandesInoffensivesToujoursAutorisees:
    def test_status_et_diff_passent(self, tmp_path):
        assert not _bloque("git status", cwd=tmp_path)
        assert not _bloque("git diff", cwd=tmp_path)

    def test_show_reste_le_chemin_recommande(self, tmp_path):
        assert not _bloque("git show HEAD:f.txt", cwd=tmp_path)


# Kept from VSCode3's own copy (not in the hub version): its protected-path
# reads must not fire on ordinary worktree commands.
class TestNInterfereJamaisAvecLesDefensesExistantes:
    """Les defenses lecture-protegee/indirection de ce depot ne doivent pas
    se declencher sur les commandes worktree ordinaires."""

    def test_checkout_dun_fichier_non_protege_nest_pas_pris_pour_une_lecture(self, tmp_path):
        (tmp_path / "normal.txt").write_text("v1\n", encoding="utf-8")
        assert _bloque("git checkout -- normal.txt", cwd=tmp_path)  # bloque par le volet arbre

    def test_env_reste_bloque_en_lecture_normale(self, tmp_path):
        (tmp_path / ".env").write_text("SECRET=1\n", encoding="utf-8")
        assert _bloque("cat .env", cwd=tmp_path)  # toujours le volet lecture-protegee


class TestCorrectifsRevueAdversariale20260907:
    """Bugs trouves par la revue bmad-code-review du 2026-09-07 sur le volet
    arbre fraichement fusionne, chacun reproduit ici pour verrouiller le
    correctif (le hub/VSCode1/VSCode3 partagent le meme code corrige)."""

    def test_option_globale_C_ne_desarme_plus_checkout(self, tmp_path):
        (tmp_path / "f.txt").write_text("v1\n", encoding="utf-8")
        assert _bloque("git -C . checkout -- f.txt", cwd=tmp_path), (
            "B1 : `-C <valeur>` etait pris pour la sous-commande, desarmant "
            "tout le volet arbre -- forme employee pour agir sur un depot tiers")

    def test_option_globale_c_ne_desarme_plus_clean(self, tmp_path):
        assert _bloque("git -c core.pager=cat clean -fd", cwd=tmp_path)

    def test_option_globale_C_ne_desarme_plus_stash(self, tmp_path):
        assert _bloque("git -C . stash drop", cwd=tmp_path)

    def test_checkout_force_bloque_meme_sans_chemin(self, tmp_path):
        assert _bloque("git checkout -f master", cwd=tmp_path), (
            "B2 : checkout -f ecrase tout l'arbre suivi, pas seulement un chemin")
        assert _bloque("git checkout --force master", cwd=tmp_path)

    def test_switch_discard_changes_bloque(self, tmp_path):
        assert _bloque("git switch --discard-changes master", cwd=tmp_path)

    def test_switch_ordinaire_reste_autorise(self, tmp_path):
        assert not _bloque("git switch main", cwd=tmp_path)

    def test_restore_S_majuscule_bloque_correctement(self, tmp_path):
        (tmp_path / "f.txt").write_text("v1\n", encoding="utf-8")
        assert not _bloque("git restore -S f.txt", cwd=tmp_path), (
            "A1 : -S (majuscule, --staged) etait compare a une liste "
            "minusculisee, jamais reconnu -- bloquait a tort un restore "
            "qui ne touche que l'index")

    def test_restore_staged_et_W_majuscule_bloque(self, tmp_path):
        (tmp_path / "f.txt").write_text("v1\n", encoding="utf-8")
        assert _bloque("git restore --staged -W f.txt", cwd=tmp_path), (
            "A1 : -W (majuscule, --worktree) invisible faisait passer un "
            "restore destructeur")

    def test_clean_dry_run_et_force_ensemble_reste_autorise(self, tmp_path):
        assert not _bloque("git clean -nfd", cwd=tmp_path), (
            "A3 : -n/--dry-run ne supprime rien, meme cumule avec -f")
        assert not _bloque("git clean --dry-run --force", cwd=tmp_path)

    def test_restore_help_reste_autorise(self, tmp_path):
        assert not _bloque("git restore --help", cwd=tmp_path)
        assert not _bloque("git restore -h", cwd=tmp_path)


class TestCorrectifsMineursRevue20260907:
    """M2/M3 de la revue bmad-code-review du 2026-09-07 -- couverture
    etendue au-dela des bugs bloquants B1/B2 et des correctifs A1/A3."""

    def test_stash_message_contenant_drop_reste_autorise(self, tmp_path):
        assert not _bloque('git stash push -m "drop le cache"', cwd=tmp_path), (
            "M2 : chercher drop/clear n'importe ou dans les tokens bloquait "
            "a tort un message de stash qui contient ce mot")

    def test_stash_message_contenant_clear_reste_autorise(self, tmp_path):
        assert not _bloque('git stash push -m "clear le cache"', cwd=tmp_path)

    def test_stash_drop_reel_reste_bloque(self, tmp_path):
        assert _bloque("git stash drop", cwd=tmp_path)
        assert _bloque("git stash clear", cwd=tmp_path)

    def test_rm_force_bloque(self, tmp_path):
        assert _bloque("git rm -f f.txt", cwd=tmp_path), (
            "M3 : git rm -f supprime le fichier du disque ET de l'index, "
            "jamais couvert")
        assert _bloque("git rm --force f.txt", cwd=tmp_path)

    def test_rm_sans_force_reste_autorise(self, tmp_path):
        assert not _bloque("git rm f.txt", cwd=tmp_path)

    def test_rm_cached_reste_autorise(self, tmp_path):
        assert not _bloque("git rm --cached f.txt", cwd=tmp_path)

    def test_worktree_remove_force_bloque(self, tmp_path):
        assert _bloque("git worktree remove --force wt", cwd=tmp_path), (
            "M3 : worktree remove --force supprime tout un arbre, jamais couvert")
        assert _bloque("git worktree remove -f wt", cwd=tmp_path)

    def test_worktree_remove_sans_force_reste_autorise(self, tmp_path):
        assert not _bloque("git worktree remove wt", cwd=tmp_path)

    def test_worktree_list_reste_autorise(self, tmp_path):
        assert not _bloque("git worktree list", cwd=tmp_path)


def _reponse(commande, extra, cwd=None):
    """Production path (subprocess, JSON on stdin, no -X utf8) with extra
    PreToolUse fields (`agent_id`, `agent_type`, `transcript_path`) merged
    into the payload. Returns the hook's stdout."""
    env = dict(os.environ)
    if cwd is not None:
        env["CLAUDE_PROJECT_DIR"] = str(cwd)
    charge = {"tool_input": {"command": commande}}
    charge.update(extra)
    r = subprocess.run(
        [sys.executable, HOOK], input=json.dumps(charge), capture_output=True,
        text=True, encoding="utf-8", cwd=str(cwd) if cwd is not None else None, env=env)
    assert r.returncode == 0 and not r.stderr, (r.returncode, r.stderr)
    return r.stdout


def _bloque_payload(commande, extra, cwd=None):
    return "deny" in _reponse(commande, extra, cwd)


def _refus_sous_agent(commande, extra, cwd=None):
    """True only when the refusal is the SUB-AGENT stash rule: another rule
    denying the same command (wrapper fallback, `-EncodedCommand`...) must
    not make a forwarding test pass."""
    sortie = _reponse(commande, extra, cwd)
    if "deny" not in sortie:
        return False
    raison = json.loads(sortie)["hookSpecificOutput"]["permissionDecisionReason"]
    return "pour un sous-agent" in raison


_SIGNAUX = ({"agent_id": "a1b2c3"}, {"agent_type": "ppt-designer"},
            {"transcript_path": "/x/s/subagents/agent-a1.jsonl"},
            {"transcript_path": r"x\s\subagents\agent-a1.jsonl"})
_SOUS_AGENT = {"agent_id": "a1"}


class TestStashSousAgent:
    """Incident 2026-11-04 (VSCode3, repete) : un sous-agent a lance `git stash`
    puis `git stash pop` « pour comparer a HEAD ». La session principale garde
    ses stash ; le sous-agent ne garde que la lecture (`list`, `show`)."""

    @pytest.mark.parametrize("sig", _SIGNAUX, ids=["agent_id", "agent_type", "tp_slash",
                                                   "tp_antislash"])
    @pytest.mark.parametrize("cmd", ["git stash", "git stash push -u", "git stash pop",
                                     "git stash apply", "git stash save wip",
                                     "git -C . stash pop"])
    def test_stash_bloque_en_sous_agent(self, tmp_path, cmd, sig):
        assert _refus_sous_agent(cmd, sig, cwd=tmp_path), (cmd, sig)

    @pytest.mark.parametrize("cmd", ["git stash list", "git stash show -p",
                                     "git stash show --stat", "git -C . stash list"])
    def test_stash_lecture_reste_permis_en_sous_agent(self, tmp_path, cmd):
        assert not _bloque_payload(cmd, _SOUS_AGENT, cwd=tmp_path), cmd

    @pytest.mark.parametrize("extra", [
        {}, {"agent_id": ""}, {"agent_type": ""}, {"agent_id": "", "agent_type": ""},
        {"transcript_path": "/x/s/main.jsonl"},
        {"transcript_path": "/x/mysubagents/a.jsonl"},
        {"transcript_path": "/x/subagentsx/a.jsonl"},
    ], ids=["vide", "agent_id_vide", "agent_type_vide", "deux_vides", "tp_principal",
            "tp_mysubagents", "tp_subagentsx"])
    @pytest.mark.parametrize("cmd", ["git stash", "git stash pop", "git stash push -u"])
    def test_session_principale_inchangee(self, tmp_path, cmd, extra):
        assert not _bloque_payload(cmd, extra, cwd=tmp_path), (cmd, extra)

    @pytest.mark.parametrize("cmd", [
        "git stash -p",                       # patch mode, no sub-command
        "git -c a=b stash apply",             # global option with a value
        "git --git-dir=x stash push",
        "git --git-dir x stash push",
        "cd x && git stash",                  # chained
        "git status; git stash pop",
        "git stash create",
        "git stash store abc123",
        "git stash -m list",                  # a push whose message is "list"
    ])
    def test_contournements_directs(self, tmp_path, cmd):
        assert _refus_sous_agent(cmd, _SOUS_AGENT, cwd=tmp_path), cmd

    # One case per forwarding path of the `sous_agent` flag, each asserting the
    # refusal comes from the sub-agent rule (review T2, voice 3, 2026-11-05).
    @pytest.mark.parametrize("cmd", [
        # `_commande_interne` only (not in _WRAPPERS): indirection payload
        'cmd /c "git stash pop"',
        'powershell -Command "git stash pop"',
        "iex 'git stash pop'",
        # both paths
        "sh -c 'git stash pop'",
        'bash -c "git stash pop"',
        'eval "git stash"',
        # `_WRAPPERS` (`candidat`) only
        "env git stash",
        "sudo git stash pop",
        "& git stash pop",
        # alias expansion inside `_analyser`
        "alias g=git; g stash pop",
        # `$(...)` and backtick bodies
        "echo $(git stash pop)",
        "echo `git stash pop`",
    ], ids=["cmd_c", "powershell_command", "iex", "sh_c", "bash_c", "eval", "env",
            "sudo", "call_operator", "alias", "dollar_paren", "backtick"])
    def test_drapeau_transmis_par_chaque_chemin(self, tmp_path, cmd):
        assert _refus_sous_agent(cmd, _SOUS_AGENT, cwd=tmp_path), cmd

    def test_drapeau_explicite_sans_etat_global(self):
        # Direct importers of `_analyser` get the main-session behaviour by
        # default and the sub-agent one only when they ask for it.
        assert guard._analyser("git stash pop") is None
        assert guard._analyser("git stash pop", sous_agent=True)
        assert guard._analyser("git stash pop") is None
