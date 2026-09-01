r"""PreToolUse hook (Bash/PowerShell) — garde-fou deterministe.

Bloque deux familles de commandes :
1. `git push --force` (sans `--force-with-lease`) et `git reset --hard` ;
2. la lecture des chemins proteges (`.env`, `secrets/**`,
   `config/credentials.json`) — miroir des deny rules `Read(...)` de
   `.claude/settings.json`, qui ne couvrent QUE l'outil `Read` : cote shell,
   `cat .env` sortait sans aucune resistance.

CE QUE CE HOOK N'EST PAS. Un garde-fou contre l'accident et le contournement
de confort, pas une frontiere de securite. Il `fail open` sur tout ce qu'il ne
sait pas analyser, par choix : un bug ici ne doit jamais bloquer un usage shell
sans rapport. Une indirection construite dynamiquement (`$g = 'git'; & $g push
--force`) lui echappe encore. Ne pas s'en servir pour justifier de baisser la
garde ailleurs.

Analyse :
1. retirer les corps de heredoc (toujours de la donnee, jamais une commande —
   p.ex. un message de commit qui *decrit* ce hook via `git commit -F - <<'EOF'`,
   convention documentee de ce depot) ;
2. decouper sur les operateurs shell (&&, ||, ;, |, saut de ligne) sans casser
   les segments a l'interieur des quotes ;
3. `shlex.split()` chaque segment, sauter les `VAR=value` de tete et
   l'operateur d'appel PowerShell `&`, puis normaliser l'executable
   (basename, sans `.exe`/`.cmd`/`.bat`/`.ps1`) ;
4. si la commande en EXECUTE une autre (`iex`, `Invoke-Expression`, `eval`,
   `powershell -Command`, `bash -c`, `-EncodedCommand` en base64), re-analyser
   la charge utile comme une commande a part entiere, en bornant la recursion.

Historique. Le tokenizer `shlex` (2026-07-16, repris d'un projet frere) gerait
deja les `VAR=value` de tete, la ou la version regex precedente (`^git\s+push\b`)
laissait passer `FOO=1 git push --force`. Mais il ne comparait qu'au token
litteral « git » et ne regardait aucune lecture de fichier : mesure du
2026-09-01 sur 10 variantes dangereuses, **6 passaient** — `git.exe`,
`& git`, `iex "..."`, `Invoke-Expression`, `powershell -Command`, et toutes les
lectures de `.env`. Verrouille depuis par `tests/test_guard_destructive_git.py`
(39 cas, dont les faux positifs a ne PAS bloquer).
"""
import base64
import json
import re
import shlex
import sys

_HEREDOC_START = re.compile(r"<<-?\s*(['\"]?)(\w+)\1")


def _strip_heredocs(cmd: str) -> str:
    out = []
    i = 0
    for m in _HEREDOC_START.finditer(cmd):
        if m.start() < i:
            continue  # inside a heredoc body we already stripped
        out.append(cmd[i:m.end()])
        delim = m.group(2)
        nl = cmd.find("\n", m.end())
        if nl == -1:
            i = len(cmd)
            break
        body_start = nl + 1
        end_pat = re.compile(r"^[ \t]*" + re.escape(delim) + r"[ \t]*$", re.MULTILINE)
        end_m = end_pat.search(cmd, body_start)
        i = end_m.end() if end_m else len(cmd)
    out.append(cmd[i:])
    return "".join(out)


def _segments(cmd: str):
    """Split on &&, ||, ;, |, newline — but not when inside '...' or "...". """
    segs = []
    buf = []
    quote = None
    i = 0
    n = len(cmd)
    while i < n:
        c = cmd[i]
        if quote:
            buf.append(c)
            if c == quote:
                quote = None
            i += 1
            continue
        if c in ("'", '"'):
            quote = c
            buf.append(c)
            i += 1
            continue
        if cmd[i : i + 2] in ("&&", "||"):
            segs.append("".join(buf))
            buf = []
            i += 2
            continue
        if c in (";", "|", "\n"):
            segs.append("".join(buf))
            buf = []
            i += 1
            continue
        buf.append(c)
        i += 1
    segs.append("".join(buf))
    return [s.strip() for s in segs]


_MAX_DEPTH = 3

# Un `git` peut s'ecrire de plusieurs facons que le tokenizer d'origine ne
# reconnaissait pas : il ne comparait qu'au token litteral « git ». Mesure du
# 2026-09-01 sur 10 variantes dangereuses : 6 passaient, dont `git.exe push
# --force` et `& git push --force` (operateur d'appel PowerShell, shell
# primaire de ce poste).
def _exe_name(token: str) -> str:
    """Nom de commande normalise : basename, sans extension Windows, minuscules."""
    t = token.replace("\\", "/").rstrip("/")
    t = t.rsplit("/", 1)[-1].lower()
    for ext in (".exe", ".cmd", ".bat", ".ps1"):
        if t.endswith(ext):
            return t[: -len(ext)]
    return t


# Commandes qui EXECUTENT leur argument. Aucune ne commence par « git », donc
# aucune n'etait vue : `iex "git push --force"` executait bel et bien la
# commande bloquee. On re-analyse la charge utile comme une commande a part
# entiere, en bornant la recursion.
_INDIRECTION = {"iex", "invoke-expression", "eval", "exec"}
_SHELL_RUNNERS = {"powershell", "pwsh", "cmd", "bash", "sh", "zsh"}
_RUNNER_FLAGS = {"-c", "-command", "/c", "/k"}
_ENCODED_FLAGS = {"-encodedcommand", "-enc", "-ec"}


def _inner_command(head: str, args: list):
    """La commande reellement executee par une indirection, ou None."""
    if head in _INDIRECTION:
        return " ".join(args) if args else None
    if head not in _SHELL_RUNNERS:
        return None
    for i, a in enumerate(args):
        al = a.lower()
        if head in ("powershell", "pwsh") and al in _ENCODED_FLAGS and i + 1 < len(args):
            try:
                return base64.b64decode(args[i + 1]).decode("utf-16-le", "replace")
            except Exception:
                return None   # pas du base64 valide : on ne devine pas
        if al in _RUNNER_FLAGS and i + 1 < len(args):
            return " ".join(args[i + 1 :])
    return None


# Miroir des deny rules `Read(...)` de .claude/settings.json, qui ne couvrent
# QUE l'outil Read : mesure du 2026-09-01, `cat .env`, `Get-Content .env` et
# `type config/credentials.json` sortaient sans aucune resistance cote shell.
_READERS = {"cat", "type", "more", "less", "head", "tail", "nl", "od", "xxd",
            "strings", "get-content", "gc", "select-string", "sls", "findstr",
            "grep", "rg", "copy", "cp", "move", "mv", "curl", "wget"}
_INTERPRETERS = {"python", "python3", "py", "node", "perl", "ruby", "deno"}


def _is_protected_path(token: str) -> bool:
    # `curl -d @.env` / `curl -d@.env` : la syntaxe « @fichier » des clients HTTP
    # est un vecteur d'exfiltration direct, et le chemin n'y est pas un argument
    # nu. On teste donc aussi ce qui suit le « @ ».
    if token.startswith("@"):
        token = token[1:]
    elif token.startswith("-") and "@" in token:
        token = token.split("@", 1)[1]
    p = token.replace("\\", "/")
    while p.startswith("./"):
        p = p[2:]
    p = p.lower()
    parts = [seg for seg in p.split("/") if seg not in ("", ".")]
    if not parts:
        return False
    # basename exact : bloque .env, ./.env, foo/.env — jamais .env.example
    if parts[-1] == ".env":
        return True
    if "secrets" in parts:
        return True
    return p.endswith("config/credentials.json")


def _blocked_reason(segment: str, _depth: int = 0):
    # shlex respecte les quotes, donc une chaine citee comme -m "... git push
    # --force ..." reste un seul token au lieu d'etre eclatee en "git"/"push".
    try:
        tokens = shlex.split(segment, posix=True)
    except ValueError:
        return None  # quotes desequilibrees etc. — fail open, on ne devine pas
    if not tokens:
        return None

    # Sauter les affectations d'env en tete (`FOO=1 git push --force`) et
    # l'operateur d'appel PowerShell (`& git push --force`).
    start = 0
    while start < len(tokens) and (
        re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", tokens[start]) or tokens[start] == "&"
    ):
        start += 1
    if start >= len(tokens):
        return None

    tokens = tokens[start:]
    head = _exe_name(tokens[0])
    args = tokens[1:]

    # 1. Indirection : la vraie commande est dans l'argument, on la ré-analyse.
    if _depth < _MAX_DEPTH:
        inner = _inner_command(head, args)
        if inner:
            for seg in _segments(_strip_heredocs(inner)):
                raison = _blocked_reason(seg, _depth + 1)
                if raison:
                    return raison

    # 2. Lecture d'un chemin protege par un lecteur ou un interpreteur.
    if head in _READERS or head in _INTERPRETERS:
        vises = [t for t in args if _is_protected_path(t)]
        if not vises and head in _INTERPRETERS:
            # `python -c "print(open('.env').read())"` : le chemin est DANS la
            # charge utile, pas dans un argument a lui seul.
            for cand in re.findall(r"""['\"]([^'\"]+)['\"]""", " ".join(args)):
                if _is_protected_path(cand):
                    vises = [cand]
                    break
        if vises:
            return (
                f"Lecture d'un fichier protege ({vises[0]}) bloquee par un hook projet — "
                "meme perimetre que les deny rules Read(...) de .claude/settings.json, "
                "qui ne couvrent pas le shell. Confirmez explicitement avec l'utilisateur "
                "si cette lecture est legitime."
            )

    # 3. git destructif.
    if head != "git":
        return None
    rest = [t.lower() for t in args]

    if "push" in rest:
        has_force = any(t in ("--force", "-f") or t.startswith("--force=") for t in rest)
        has_lease = any(
            t == "--force-with-lease" or t.startswith("--force-with-lease=") for t in rest
        )
        if has_force and not has_lease:
            return (
                "git push --force (sans --force-with-lease) est bloque par un hook projet. "
                "Utilisez --force-with-lease si necessaire, ou confirmez explicitement avec "
                "l'utilisateur avant de contourner ce garde-fou."
            )

    if "reset" in rest and "--hard" in rest:
        return (
            "git reset --hard est bloque par un hook projet (perte de modifications non "
            "commitees). Utilisez git stash, ou confirmez explicitement avec l'utilisateur."
        )

    return None


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except Exception:
        return
    cmd = (data.get("tool_input") or {}).get("command") or ""
    cmd = _strip_heredocs(cmd)

    blocked = None
    for seg in _segments(cmd):
        blocked = _blocked_reason(seg)
        if blocked:
            break

    if blocked:
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": blocked,
            }
        }))


if __name__ == "__main__":
    main()
