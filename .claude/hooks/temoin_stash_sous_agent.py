"""PreToolUse + PostToolUse (Bash|PowerShell) -- stash witness for a SUB-AGENT.

Lot s-stash-robuste (user decision 2026-11-05, « corriger et rendre robuste »). The
lexical guard (guard_destructive_git.py) refuses what it can read; a sub-command
COMPUTED at run time inside a script (`py script.py` that builds `'st' + 'ash'`)
is invisible to any analysis of the command line. This hook does not read the
command at all: it reads the repository.

- PreToolUse (run IN-PROCESS by guard_dispatch_pretooluse.py, no extra interpreter):
  locate the git COMMON dir of the tool cwd and of CLAUDE_PROJECT_DIR by reading files
  only (`.git` dir, or `.git` file -> `gitdir:` -> `commondir`), record the value of
  `refs/stash` (loose ref, else packed-refs) and the size of `logs/refs/stash` in ONE
  STATE FILE PER tool_use_id (`<state dir>/<sanitised id>.json`, temp file +
  os.replace; files older than 1 h or beyond the count cap are pruned).
- PostToolUse (own settings entry, one interpreter per shell call): read and delete
  its own state file, compare. On change, append one line to the guard capture
  journal (`captures_gardes.jsonl`, garde `temoin_stash_sous_agent`) and tell the
  sub-agent to stop touching the tree and report to the main session. A failing
  journal write never suppresses the message.

State dir: $TEMOIN_STASH_ETAT, else `<user temp>/claude-temoin-stash/` -- outside
the repository, nothing lands in `.claude/supervision/`.

Lot s-stash-correctif (2026-11-05): the single shared state file lost entries under
parallel PreToolUse (read-modify-write without a lock: 12 parallel calls, 8 entries
left, 1/12 Post reporting in the test); one file per tool_use_id removes the shared
write. Main-session cost: PostToolUse returns before any import beyond json/os/sys
when the payload is not a sub-agent's.

Detection, not prevention: the stash already happened when it speaks. Sub-agent
context only (same two signals as guard_destructive_git._contexte_sous_agent).
Never blocks on its own error: any error is a silent exit 0. No git subprocess:
file reads only.

NOT SEEN (declared, no code):
- a reftable ref backend (`extensions.refStorage = reftable`): no loose ref and no
  packed-refs to read, the witness stays silent;
- `cd other_repo && git stash` or `git -C other_repo stash`: only the payload cwd and
  CLAUDE_PROJECT_DIR are watched;
- a stash made by ANOTHER session during the call is attributed to the sub-agent's
  call: the message therefore says « détecté pendant votre appel », never that the
  sub-agent did it.
"""
import json
import os
import sys

GARDE_CAPTURE = "temoin_stash_sous_agent"
ENV_JOURNAL_CAPTURES = "GUARD_CAPTURES_LOG"   # same variable as guard_terminaison_etayee
ENV_ETAT = "TEMOIN_STASH_ETAT"                # state DIRECTORY (one file per tool_use_id)
TTL_S = 3600          # a Pre without Post (refused call, crash) is pruned after 1 h
MAX_ENTREES = 500
_ICI = os.path.dirname(os.path.abspath(__file__))

MESSAGE = (
    "Temoin stash : changement de la remise git (refs/stash) du depot {depot} "
    "détecté pendant votre appel (avant : {avant}, apres : {apres}). Il vient de votre "
    "commande ou d'une autre session active au meme moment. Un sous-agent ne range pas "
    "l'arbre de travail : il porte le travail non commite d'autres sessions. "
    "N'executez plus aucune commande qui touche l'arbre ou la remise, et rendez la main "
    "a la session principale en lui signalant ce changement (elle seule decide "
    "d'un `git stash pop` ou d'une restauration).")


def _contexte_sous_agent(data: dict) -> bool:
    """Same two signals as guard_destructive_git._contexte_sous_agent."""
    if data.get("agent_id") or data.get("agent_type"):
        return True
    tp = str(data.get("transcript_path") or "").replace("\\", "/")
    return "/subagents/" in tp


def _lire(chemin):
    with open(chemin, encoding="utf-8", errors="replace") as fh:
        return fh.read()


def _dossier_commun(depart):
    """Git common dir of `depart` (walk up for `.git`), or None. Files only."""
    d = os.path.abspath(depart)
    for _ in range(64):
        g = os.path.join(d, ".git")
        if os.path.isdir(g):
            gitdir = g
            break
        if os.path.isfile(g):
            ligne = _lire(g).strip()
            if not ligne.startswith("gitdir:"):
                return None
            cible = ligne[len("gitdir:"):].strip()
            gitdir = cible if os.path.isabs(cible) else os.path.join(d, cible)
            break
        parent = os.path.dirname(d)
        if parent == d:
            return None
        d = parent
    else:
        return None
    fichier = os.path.join(gitdir, "commondir")
    if os.path.isfile(fichier):
        val = _lire(fichier).strip()
        commun = val if os.path.isabs(val) else os.path.join(gitdir, val)
    else:
        commun = gitdir
    return os.path.normcase(os.path.normpath(commun))


def _ref_packee(commun):
    try:
        for ligne in _lire(os.path.join(commun, "packed-refs")).splitlines():
            if ligne.endswith(" refs/stash"):
                return ligne.split(" ", 1)[0]
    except OSError:
        pass
    return None


def _etat_stash(commun):
    """{"ref": sha or None, "log": size of logs/refs/stash or -1}."""
    try:
        ref = _lire(os.path.join(commun, "refs", "stash")).strip() or None
    except OSError:
        ref = _ref_packee(commun)
    try:
        taille = os.path.getsize(os.path.join(commun, "logs", "refs", "stash"))
    except OSError:
        taille = -1
    return {"ref": ref, "log": taille}


def _depots(data):
    vus = {}
    for depart in (data.get("cwd"), os.environ.get("CLAUDE_PROJECT_DIR")):
        if isinstance(depart, str) and depart:
            commun = _dossier_commun(depart)
            if commun and commun not in vus:
                vus[commun] = _etat_stash(commun)
    return vus


def _dossier_etat():
    if os.environ.get(ENV_ETAT):
        return os.environ[ENV_ETAT]
    temp = (os.environ.get("TEMP") or os.environ.get("TMP") or os.environ.get("TMPDIR")
            or "/tmp")
    return os.path.join(temp, "claude-temoin-stash")


def _nom_fichier(tid):
    """tool_use_id -> a plain file name that cannot leave the state dir."""
    sur = "".join(c if (c.isascii() and c.isalnum()) or c in "_-" else "_" for c in tid)
    return sur[:120] + ".json"


def _elaguer(dossier, maintenant):
    """Drop state files older than TTL_S, then the oldest beyond MAX_ENTREES."""
    try:
        entrees = []
        with os.scandir(dossier) as it:
            for e in it:
                if e.name.endswith(".json") and e.is_file():
                    entrees.append((e.stat().st_mtime, e.path))
    except OSError:
        return
    entrees.sort()
    for i, (mtime, chemin) in enumerate(entrees):
        if maintenant - mtime > TTL_S or i < len(entrees) - MAX_ENTREES:
            try:
                os.remove(chemin)
            except OSError:
                pass


def _ecrire_etat(chemin, contenu):
    tmp = f"{chemin}.{os.getpid()}.tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(contenu, fh)
    os.replace(tmp, chemin)


def _journal(data, depot, avant, apres):
    import datetime
    chemin = os.environ.get(ENV_JOURNAL_CAPTURES) or os.path.join(
        _ICI, "..", "supervision", "captures_gardes.jsonl")
    ligne = json.dumps({
        "ts": datetime.datetime.now(datetime.UTC).isoformat(timespec="seconds"),
        "garde": GARDE_CAPTURE, "motif": "stash_modifie",
        "session_id": str(data.get("session_id") or "")[:200],
        "agent_id": str(data.get("agent_id") or "")[:200],
        "agent_type": str(data.get("agent_type") or "")[:200],
        "tool_use_id": str(data.get("tool_use_id") or "")[:200],
        "depot": depot, "avant": avant, "apres": apres}) + "\n"
    os.makedirs(os.path.dirname(os.path.abspath(chemin)), exist_ok=True)
    with open(chemin, "a", encoding="utf-8") as fh:
        fh.write(ligne)


def traiter(data):
    """The hook's work for one payload -> JSON text to print, or None."""
    if not isinstance(data, dict) or not _contexte_sous_agent(data):
        return None
    tid = data.get("tool_use_id")
    evt = data.get("hook_event_name")
    if not isinstance(tid, str) or not tid:
        return None
    dossier = _dossier_etat()
    chemin = os.path.join(dossier, _nom_fichier(tid))
    if evt == "PreToolUse":
        import time
        maintenant = time.time()
        os.makedirs(dossier, exist_ok=True)
        _elaguer(dossier, maintenant)
        _ecrire_etat(chemin, {"ts": maintenant, "tid": tid, "depots": _depots(data)})
        return None
    if evt != "PostToolUse":
        return None
    try:
        brut = _lire(chemin)
    except OSError:
        return None
    try:
        os.remove(chemin)
    except OSError:
        pass
    try:
        entree = json.loads(brut)
    except ValueError:
        return None
    if not isinstance(entree, dict) or entree.get("tid") != tid:
        return None
    avant_tous = entree.get("depots")
    if not isinstance(avant_tous, dict):
        return None
    apres_tous = _depots(data)
    for depot, avant in avant_tous.items():
        apres = apres_tous.get(depot)
        if not isinstance(avant, dict) or apres is None or apres == avant:
            continue
        try:   # a failing journal never suppresses the message
            _journal(data, depot, avant, apres)
        except Exception:  # noqa: BLE001
            pass
        texte = MESSAGE.format(depot=depot, avant=avant.get("ref") or "aucune",
                               apres=apres.get("ref") or "aucune")
        return json.dumps({
            "decision": "block",
            "reason": texte,
            "hookSpecificOutput": {"hookEventName": "PostToolUse",
                                   "additionalContext": texte},
        })
    return None


# --- bounded stdin read (anthropics/claude-code#87289) -------------------------
# Single source: _stdin_borne.lier_stdin (imported via a path relative to __file__).
try:
    sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
    from _stdin_borne import lier_stdin as _lier
    from _stdin_borne import lire_stdin_borne as _lsb
    _stdin_borne, _ecrire_journal_stdin, _journal_attente = _lier(globals(), __file__)
except Exception:  # noqa: BLE001 - exported without the helper: still bounded
    def _lsb(delai=15.0, flux=None):
        import threading
        f = flux if flux is not None else sys.stdin
        boite = {}

        def _c():
            try:
                boite["v"] = f.read()
            except BaseException:  # noqa: BLE001
                boite["v"] = None
        t = threading.Thread(target=_c, daemon=True)
        t.start()
        t.join(delai)
        return None if t.is_alive() else boite.get("v")

    def _ecrire_journal_stdin(champs, cap=1_000_000, suffixe="", rotation=True):
        pass  # journal unavailable without the helper; the refusal itself is unchanged

    def _journal_attente(attente, delai):
        pass

    def _stdin_borne(delai=15.0):
        globals()["_DELAI_S"] = delai
        globals()["_ATTENTE_S"] = None
        return _lsb(delai, globals().get("_FLUX_STDIN"))


def main() -> None:
    """Fail-open everywhere: a witness never blocks a tool call."""
    try:
        data = json.loads(_stdin_borne() or "")
        sortie = traiter(data)
    except Exception:  # noqa: BLE001 - silent, journal-free
        return
    if sortie:
        print(sortie)


if __name__ == "__main__":
    main()
