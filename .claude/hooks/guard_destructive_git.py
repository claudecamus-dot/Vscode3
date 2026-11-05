r"""PreToolUse hook (Bash/PowerShell) — garde-fou deterministe, version unifiee
de la flotte (fusion des deux lignees le 2026-09-08).

Bloque trois familles de commandes :
1. l'HISTORIQUE : `git push --force` (sans `--force-with-lease`), la refspec
   forcee par `+` (`git push origin +main`) et `git reset --hard`, y compris
   ses abreviations non ambigues (`--har`, `--h`) ;
2. l'ARBRE : les commandes qui ecrasent le travail non commite d'un fichier
   (`git checkout -- <chemin>`, `git restore <chemin>`, `git clean -f`,
   `git stash drop/clear`, `git rm -f`, `git worktree remove --force`) ; et,
   pour un SOUS-AGENT seulement, tout `git stash` hors `list`/`show`.
   Sous-commande CALCULEE (lot s-stash-robuste, 2026-11-05) : un alias git est
   DEPLIE puis re-analyse dans tous les contextes -- en ligne (`git -c
   alias.r=reset r --hard`, `--config-env`, `GIT_CONFIG_KEY_<n>`, alias `!shell`)
   ou persistant. Lot s-stash-correctif (2026-11-05) : l'alias persistant est lu
   dans les FICHIERS de config (systeme, global, depot, worktree, include.path et
   includeIf suivis), AUCUN sous-processus -- le `git config --get` de 1433ba33
   bloquait la garde (petit-fils git gardant les tubes ouverts apres le timeout).
   Les variables GIT_CONFIG_* exportees dans un segment anterieur (`export`,
   `$env:`) sont suivies. Pour
   un SOUS-AGENT, la garde refuse en plus ce qu'elle ne sait pas decoder
   (fail-closed) : sous-commande non litterale (`git $S`, `git $(echo stash)`,
   backtick, `%S%`, `git (...)`, `echo stash | xargs git`), alias non resolu ou
   sous une configuration que la commande deplace ou ecrit (GIT_CONFIG_GLOBAL vers
   un fichier absent, HOME=, `>> .git/config`, valeur calculee), `git config` qui
   ecrit un alias, l'ecriture directe de `refs/stash` / `stash@{n}` (update-ref,
   reflog delete|expire), `--autostash` (et rebase/merge.autoStash = true), et
   une chaine d'interpreteur EN POSITION DE COMMANDE (`py -c`, `node -e`, `perl
   -e`, `ruby -e`, heredoc, `iex`) portant les mots `git` et `stash`. Limite :
   `_GIT_COMMANDES` est une liste figee (git 2.54) ; un built-in plus recent est
   traite comme inconnu, donc cherche comme alias par lecture de fichiers (peu
   couteux depuis ce lot). Ce qui PASSE encore : un
   script FICHIER qui calcule le mot (`py s.py` avec `'st'+'ash'`), ou une
   chaine d'interpreteur sans le mot `stash` en clair -- seulement DETECTE apres
   coup par `temoin_stash_sous_agent.py` (PostToolUse, refs/stash compare) ;
3. la LECTURE des chemins proteges (`.env`, `secrets/**`,
   `config/credentials.json`) — miroir des deny rules `Read(...)` de
   `.claude/settings.json`, qui ne couvrent QUE l'outil `Read` : cote shell,
   `cat .env` sortait sans aucune resistance.

Plus, transversalement, les WRAPPERS et INDIRECTIONS qui executent l'une de ces
commandes sans que le token de tete soit `git` : `eval`, `env`, `xargs`, `sudo`,
l'operateur d'appel PowerShell `&` et `.`, mais aussi `iex` /
`Invoke-Expression`, `powershell -Command`, `-EncodedCommand` (base64),
`bash -c`, `cmd /c`, et les executables `git.exe` / `git.cmd` / `git.bat` /
`git.ps1`.

CE QUE CE HOOK N'EST PAS. Un garde-fou contre l'accident et le contournement
de confort, pas une frontiere de securite. Il `fail open` sur tout ce qu'il ne
sait pas analyser, par choix : un bug ici ne doit jamais bloquer un usage shell
sans rapport. Ne pas s'en servir pour justifier de baisser la garde ailleurs.

LIMITE CONNUE : L'INDIRECTION D'EXECUTION — une CLASSE, pas un cas isole. Ce
docstring n'en declarait qu'UN (`$g = 'git'; & $g push --force`), ce qui laissait
croire a un trou a colmater. La sonde adversariale du 2026-09-19, rejouee par le
chemin de PRODUCTION (payload `PreToolUse` reel sur stdin, 16 commandes), a mesure
12 bloquees / 4 passees, et les 4 passees sont quatre visages du MEME defaut :
variable PowerShell, alias PowerShell (`Set-Alias`), `Invoke-Expression` sur une
chaine CONCATENEE, `xargs` qui reinjecte l'option depuis stdin, et `py -c` +
`subprocess`. Le point commun : le nom de la commande dangereuse n'existe PAS dans
le texte analyse — il est calcule a l'execution. AUCUNE analyse lexicale de la
ligne de commande ne rattrape cette classe, quel que soit le nombre de motifs
ajoutes ; la colmater cas par cas produirait une fausse assurance, qui est pire
que la limite declaree. `tests/test_guard_destructive_git_indirection.py` en
garde la trace en `xfail` (session PRINCIPALE, `push --force`) : un futur
durcissement s'y signalera en XPASS. Elle reste vraie en session principale.
Pour un SOUS-AGENT et la seule famille stash, le lot s-stash-robuste
(2026-11-05) la traite en profondeur plutot que par un motif de plus : (A) les
alias git sont deplies comme git les deplie, et ce que la garde ne decode pas
est refuse (fail-closed, voir plus haut) ; (B) `temoin_stash_sous_agent.py`
compare `refs/stash` avant/apres chaque appel shell d'un sous-agent et le
signale (journal `captures_gardes.jsonl` + message), y compris quand le mot n'a
jamais existe dans la ligne de commande -- detection apres coup, pas un refus ;
(C) un hook git `reference-transaction` qui refuserait la mise a jour de
`refs/stash` n'est PAS installe : aucune variable d'environnement mesuree ne
distingue un shell de sous-agent de celui de la session principale.

CE QUI TIENT, mesure le meme jour et a conserver : `cmd /c`, `sh -c`, prefixe de
variable d'environnement, chemin absolu, enchainement `;` / `&&` / retour a la
ligne, espaces multiples, casse, et `git -C ../VSCode2 reset --hard` (une cible
hors du depot courant).

LA GARDE ROBUSTE EST AILLEURS. Contre un `push --force`, ce qui protege vraiment
est cote depot DISTANT — protection de branche GitHub — et non cote prompt : le
serveur refuse l'operation quelle que soit la facon dont le client l'a formulee.
Ce hook reste utile comme friction sur l'accident ; il ne remplace pas ce reglage.

Analyse (tokenizer `shlex` du 2026-07-16, repris d'un projet frere : il gerait
deja les `VAR=value` de tete, la ou la version regex precedente
(`^git\s+push\b`) laissait passer `FOO=1 git push --force`) :
1. retirer les corps de heredoc (toujours de la donnee, jamais une commande —
   p.ex. un message de commit qui *decrit* ce hook via
   `git commit -F - <<'EOF' ... EOF`, convention documentee de ces depots) ;
2. decouper sur les operateurs shell (&&, ||, ;, |, (, ), saut de ligne) sans
   casser les segments a l'interieur des quotes ;
3. `shlex.split()` chaque segment, sauter les `VAR=value` de tete, puis
   normaliser l'executable (basename, sans `.exe`/`.cmd`/`.bat`/`.ps1`) ;
4. si la commande en EXECUTE une autre (wrapper ou indirection), re-analyser la
   charge utile comme une commande a part entiere, en bornant la recursion a
   `_MAX_DEPTH`.
"""
import base64
import json
import os
import re
import shlex
import sys
import time


def _contexte_sous_agent(data: dict) -> bool:
    """Same two signals as guard_service.contexte_sous_agent (duplicated: hooks
    are standalone scripts): a truthy `agent_id` / `agent_type`, or a
    `transcript_path` under `/subagents/`. `agent_type` is also set in a main
    session started with `claude --agent <name>`: kept anyway, consistent with
    guard_service -- a false refusal there costs less than a stash/pop here."""
    if data.get("agent_id") or data.get("agent_type"):
        return True
    tp = str(data.get("transcript_path") or "").replace("\\", "/")
    return "/subagents/" in tp


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
    """Les parentheses sont neutralisees ICI, en amont du decoupage : sans cela
    `(git push --force)` et `echo $(git push --force)` collaient le `(` au token de
    tete, qui n'etait donc plus `git` (verifie en rejouant le hook, 2026-08-31).
    Entre quotes elles restent intactes : `git commit -m "fix (bug)"` n'est pas coupe.

    Split on &&, ||, ;, |, (, ), newline — but not when inside '...' or "...". """
    return [s for s, _ in _segments_delims(cmd)]


def _segments_delims(cmd: str):
    """`_segments` plus the operator that ENDS each segment ("" for the last one):
    a sub-agent's `git (echo stash) pop` (PowerShell) is a segment `git` ended by `(`,
    i.e. a sub-command computed at run time (lot s-stash-robuste, A3)."""
    segs = []
    delims = []
    buf = []
    quote = None
    i = 0
    n = len(cmd)
    while i < n:
        c = cmd[i]
        if c == "\\" and quote != "'" and i + 1 < n:
            # escaped char (`\"`, `\;`): never opens a quote nor splits (POSIX).
            buf.append(cmd[i : i + 2])
            i += 2
            continue
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
            delims.append(cmd[i : i + 2])
            buf = []
            i += 2
            continue
        if c in (";", "|", "(", ")", "\n"):
            segs.append("".join(buf))
            delims.append(c)
            buf = []
            i += 1
            continue
        buf.append(c)
        i += 1
    segs.append("".join(buf))
    delims.append("")
    return [(s.strip(), d) for s, d in zip(segs, delims, strict=True)]


_MAX_DEPTH = 3

# Wrappers qui EXECUTENT leur argument : sans les reconnaitre,
# `eval "git push --force"` et `bash -c "git push --force"` passaient, le token de
# tete n'etant pas le mot `git`.
_WRAPPERS = frozenset({
    "eval", "exec", "command", "builtin", "env", "sudo", "doas", "nohup", "nice",
    "time", "xargs", "sh", "bash", "zsh", "dash", "ksh", "busybox",
    # `&` est l OPERATEUR D APPEL de PowerShell — le shell PRIMAIRE de cet
    # environnement, et ce hook est monte sur le matcher `Bash|PowerShell`. Il execute
    # ce qui le suit exactement comme `eval` : `& git push --force` passait, alors que
    # `git push --force` etait bloque. Verifie que l operateur lance bien git avant de
    # le traiter comme un wrapper (revue de securite du 2026-09-01).
    "&", ".",
})


def _nom_binaire(tok: str) -> str:
    """Nom du binaire invoque : `git`, `git.exe`, `/usr/bin/git` ou un chemin Windows
    absolu -> `git`. Le test litteral `lower[start] != "git"` exigeait le mot nu et
    laissait donc passer toute autre forme d'invocation (verifie en rejouant le hook
    avec un payload PreToolUse reel, 2026-08-31).

    Les extensions executables de Windows autres que `.exe` valent le meme
    contournement : `git.cmd push --force` PASSAIT ici alors qu'il etait bloque sur
    la lignee VSCode3 (mesure du 2026-09-07, rejeu par le chemin de production).
    `.cmd`/`.bat`/`.ps1` sont donc retirees comme `.exe`. Le `\\` est normalise en
    `/` avant le basename pour ne pas dependre du `os.path` de la plateforme."""
    nom = tok.replace("\\", "/").rstrip("/")
    nom = nom.rsplit("/", 1)[-1].lower()
    for ext in (".exe", ".cmd", ".bat", ".ps1"):
        if nom.endswith(ext):
            return nom[: -len(ext)]
    return nom


# --------------------------------------------------------------------------- #
# Indirections : la vraie commande est la CHARGE UTILE d'un argument
# --------------------------------------------------------------------------- #
# Repris de la lignee VSCode3 le 2026-09-08. Aucune de ces commandes ne commence
# par « git », donc aucune n'etait vue ici : mesure du 2026-09-07 par le chemin
# de production, `iex 'git push --force'`, `powershell -Command 'git checkout --
# f.txt'` et `git.cmd push --force` PASSAIENT au hub et sur VSCode1/2/4, et
# etaient bloques sur VSCode3. On re-analyse la charge utile comme une commande a
# part entiere, en bornant la recursion.
#
# Ces indirections ne remplacent PAS `_WRAPPERS` : `-EncodedCommand` demande un
# decodage base64 qu'aucune re-analyse token-par-token ne peut faire, et
# `_WRAPPERS` couvre a l'inverse `env`/`xargs`/`sudo`/`&`, absents ici.
_INDIRECTION = frozenset({"iex", "invoke-expression", "eval", "exec"})
_SHELL_RUNNERS = frozenset({"powershell", "pwsh", "cmd", "bash", "sh", "zsh"})
_RUNNER_FLAGS = frozenset({"-c", "-command", "/c", "/k"})
_ENCODED_FLAGS = frozenset({"-encodedcommand", "-enc", "-ec"})


def _commande_interne(tete: str, args: list):
    """La commande reellement executee par une indirection, ou None."""
    if tete in _INDIRECTION:
        return " ".join(args) if args else None
    if tete not in _SHELL_RUNNERS:
        return None
    for i, a in enumerate(args):
        al = a.lower()
        if tete in ("powershell", "pwsh") and al in _ENCODED_FLAGS and i + 1 < len(args):
            try:
                return base64.b64decode(args[i + 1]).decode("utf-16-le", "replace")
            except Exception:
                return None   # pas du base64 valide : on ne devine pas
        if al in _RUNNER_FLAGS and i + 1 < len(args):
            return " ".join(args[i + 1 :])
    return None


# --------------------------------------------------------------------------- #
# Lecture d'un chemin protege
# --------------------------------------------------------------------------- #
# Repris de la lignee VSCode3 le 2026-09-08. Miroir des deny rules `Read(...)` de
# .claude/settings.json, qui ne couvrent QUE l'outil Read : mesure du 2026-09-01,
# `cat .env`, `Get-Content .env` et `type config/credentials.json` sortaient sans
# aucune resistance cote shell.
_READERS = frozenset({"cat", "type", "more", "less", "head", "tail", "nl", "od", "xxd",
                      "strings", "get-content", "gc", "select-string", "sls", "findstr",
                      "grep", "rg", "copy", "cp", "move", "mv", "curl", "wget"})
_INTERPRETERS = frozenset({"python", "python3", "py", "node", "perl", "ruby", "deno"})


def _est_un_chemin_protege(token: str) -> bool:
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


def _analysable(segment: str) -> bool:
    try:
        shlex.split(segment, posix=True)
        return True
    except ValueError:
        return False


def _assainir(cmd: str) -> str:
    """Quote and backslash characters replaced, so no orphan quote can swallow an
    operator when the text is split again."""
    return cmd.replace("'", " ").replace('"', " ").replace("\\", "/")


# A continuation is an ODD run of backslashes right before the newline; an even run is
# literal backslashes and the newline then ends the command (`echo \\<LF>git ...`).
_CONTINUATION = re.compile(r"(?<!\\)((?:\\\\)*)\\\r?\n")
_ANSI_C = re.compile(r"(?<!\\)\$'((?:[^'\\]|\\.)*)'", re.DOTALL)
_DEFAULT_EXPANSION = re.compile(r"\$\{[A-Za-z_][A-Za-z0-9_]*:?-([^}]*)\}")
_SIMPLE_ESC = {"n": "\n", "t": "\t", "r": "\r", "\\": "\\", "'": "'", '"': '"', "a": "\a",
               "b": "\b", "e": "\x1b", "f": "\f", "v": "\v"}


def _decode_ansi_c(body: str) -> str:
    out = []
    i = 0
    while i < len(body):
        c = body[i]
        if c != "\\" or i + 1 >= len(body):
            out.append(c)
            i += 1
            continue
        d = body[i + 1]
        m = re.match(r"x([0-9A-Fa-f]{1,2})|([0-7]{1,3})|u([0-9A-Fa-f]{1,4})", body[i + 1 :])
        if m:
            code = m.group(1) or m.group(3)
            out.append(chr(int(code, 16) if code else int(m.group(2), 8)))
            i += 1 + m.end()
        else:
            out.append(_SIMPLE_ESC.get(d, "\\" + d))
            i += 2
    return "".join(out)


def _ansi_c_litteral(m) -> str:
    texte = _decode_ansi_c(m.group(1))
    return "'" + texte.replace("'", "'\\''") + "'"


def _normaliser(cmd: str) -> str:
    r"""Make the shell's own rewriting visible to the lexical analysis (SEC holes lot,
    2026-10-04): `\<LF>` continuations are joined (`git reset \<LF> --hard`,
    `--\<LF>hard`), `$'--hard'` becomes the literal `'--hard'`, and `${X:-word}`
    becomes its default word (`${X:---hard}`, `git ${X:-reset} --hard`). Conservative
    on purpose: a rewritten harmless text never forms a destructive command."""
    cmd = _CONTINUATION.sub(lambda m: m.group(1), cmd)
    cmd = _ANSI_C.sub(_ansi_c_litteral, cmd)
    for _ in range(3):  # nested defaults
        nouveau = _DEFAULT_EXPANSION.sub(lambda m: m.group(1), cmd)
        if nouveau == cmd:
            break
        cmd = nouveau
    return cmd


_TRAVAIL = [0]
_MAX_TRAVAIL = 1_000_000   # characters scanned for substitutions, per command
_MAX_CHARS_CORPS = 30_000   # total characters of bodies analysed
_MAX_CORPS = 64          # bodies analysed per top-level command
_DESTRUCTIF_BRUT = re.compile(
    r"\bgit\b[^\n]{0,300}?\b(?:reset|clean|push|checkout|restore|stash|rm|worktree|switch)\b",
    re.IGNORECASE)


def _corps_de_substitutions(cmd: str):
    """Bodies of backtick and `$(...)` substitutions (outermost first, nested ones
    listed too), active outside '...' and also INSIDE "...". ONE linear pass with a
    stack: the previous version re-scanned nested bodies at every recursion level
    (40 nested `$(` = 6 s). An unclosed `$(` runs to the end of the text."""
    trouves = []   # (start, body)
    pile = []      # start index of each open `(`; -1 for a plain paren
    n = len(cmd)
    i = 0
    quote = None
    while i < n:
        c = cmd[i]
        if c == "\\" and quote != "'":
            i += 2
            continue
        if quote == "'":
            if c == "'":
                quote = None
            i += 1
            continue
        if c == "'":
            quote = "'"
        elif c == '"':
            quote = None if quote == '"' else '"'
        elif c == "`":
            j = i + 1
            while j < n and cmd[j] != "`":
                j += 2 if cmd[j] == "\\" else 1
            trouves.append((i + 1, j, True))
            i = j
        elif c == "$" and cmd[i + 1 : i + 2] == "(":
            pile.append(i + 2)
            i += 1
        elif c == "(":
            pile.append(-1)
        elif c == ")" and pile:
            debut = pile.pop()
            if debut >= 0:
                trouves.append((debut, i, False))
        i += 1
    for debut in pile:
        if debut >= 0:
            trouves.append((debut, n, False))
    trouves.sort(key=lambda t: t[0])
    corps = []
    total = 0
    trop = len(trouves) > _MAX_CORPS
    for debut, fin, backtick in trouves[:_MAX_CORPS]:
        total += fin - debut
        if total > _MAX_CHARS_CORPS:   # analysed text bounded: never hang
            trop = True
            break
        texte = cmd[debut:fin]
        corps.append((texte.replace("\\`", "`") if backtick else texte, backtick))
    return corps, trop


def _alias_git(segs: list) -> dict:
    """`alias g=git` / `alias g='git -c x'` -> {"g": ["git", "-c", "x"]}."""
    alias = {}
    for seg in segs:
        try:
            toks = shlex.split(seg, posix=True)
        except ValueError:
            continue
        if len(toks) >= 2 and toks[0] == "alias":
            for t in toks[1:]:
                nom, sep, val = t.partition("=")
                if sep and re.match(r"^[A-Za-z_][\w.-]*$", nom):
                    mots = val.split()
                    if mots and _nom_binaire(mots[0]) == "git":
                        alias[nom] = mots
    return alias


def _developper_alias(seg: str, alias: dict) -> str:
    if not alias:
        return seg
    try:
        toks = shlex.split(seg, posix=True)
    except ValueError:
        return seg
    k = 0
    while k < len(toks) and re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", toks[k]):
        k += 1
    if k < len(toks) and toks[k] in alias:
        toks = toks[:k] + alias[toks[k]] + toks[k + 1 :]
        return " ".join(shlex.quote(t) for t in toks)
    return seg


def _analyser(cmd: str, profondeur: int = 0, extraire: bool = True,
              sous_agent: bool = False):
    cmd = _normaliser(cmd)
    if profondeur == 0:
        _TRAVAIL[0] = 0
        _LECTURES[0], _LECTURES[1] = 0, None
        env_cmd, opaque = _collecter_env_commande(cmd)
        _ENV_CMD.clear()
        _ENV_CMD.update(env_cmd)
        _OPAQUE[0] = opaque
    if extraire and profondeur < _MAX_DEPTH:
        _TRAVAIL[0] += len(cmd)
        if _TRAVAIL[0] > _MAX_TRAVAIL:   # total scanned text bounded: never hang
            corps, trop = [], True
        else:
            corps, trop = _corps_de_substitutions(cmd)
        for c, backtick in corps:
            # `$(...)` bodies are listed flat (nested ones too): no re-scan, else n^3
            raison = _analyser(c, profondeur + 1, backtick, sous_agent=sous_agent)
            if raison:
                return raison
        if trop and _DESTRUCTIF_BRUT.search(cmd):
            return ("Trop de substitutions imbriquees pour une analyse bornee, et un motif "
                    "git destructif apparait dans le texte brut : refus prudent.")
    paires = _segments_delims(cmd)
    segs = [s for s, _ in paires]
    alias = _alias_git(segs)
    if alias:
        segs = [_developper_alias(sg, alias) for sg in segs]
    if sous_agent:
        # PowerShell `git (echo stash) pop`: the sub-command is the value of `(...)`.
        for sg, delim in zip(segs, (d for _, d in paires), strict=True):
            if delim != "(":
                continue
            try:
                toks = shlex.split(sg, posix=True)
            except ValueError:
                continue
            k = 0
            while k < len(toks) and re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", toks[k]):
                k += 1
            if (k < len(toks) and _nom_binaire(toks[k]) == "git"
                    and _sous_commande_index([t.lower() for t in toks[k + 1 :]]) is None):
                return _REFUS_CALCULE.format(detail="`git (...)`")
    for seg in segs:
        raison = _blocked_reason(seg, profondeur, sous_agent=sous_agent)
        if raison:
            return raison
    if not all(_analysable(seg) for seg in segs):
        # An orphan quote also hides the operators that FOLLOW it (`echo it's;
        # git reset --hard` was one single segment). Re-split the sanitised text
        # and analyse every segment (SEC lot, D1, 2026-10-04).
        for seg in _segments(_assainir(cmd)):
            try:
                tokens = shlex.split(seg, posix=True)
            except ValueError:
                continue
            raison = (_blocked_reason_tokens(tokens, profondeur, sous_agent=sous_agent)
                      if tokens else None)
            if raison:
                return ("Commande non analysable (guillemets ou antislash non apparies) : "
                        "analyse lexicale prudente du texte brut, " + raison)
    return None


def _blocked_reason(segment: str, profondeur: int = 0, sous_agent: bool = False):
    # shlex respects quoting, so a quoted string like -m "... git push
    # --force ..." collapses into a single token instead of being split
    # into separate "git"/"push"/"--force" words.
    non_analysable = False
    try:
        tokens = shlex.split(segment, posix=True)
    except ValueError:
        # Unbalanced quote / dangling backslash. This used to fail OPEN, so
        # `git reset --hard # it's` ran (SEC lot, 2026-10-04). Conservative
        # lexical fallback: drop the quote and backslash characters and re-run
        # the SAME analysis on the raw words (comments are not told apart, on
        # purpose: a false block is cheaper than a destructive command passing).
        non_analysable = True
        try:
            tokens = shlex.split(
                segment.replace("'", " ").replace('"', " ").replace("\\", "/"), posix=True)
        except ValueError:
            return None  # cannot happen once the quotes are gone; kept for safety
    if not tokens:
        return None
    if non_analysable:
        raison = _blocked_reason_tokens(tokens, profondeur, sous_agent=sous_agent)
        if raison:
            return ("Commande non analysable (guillemets ou antislash non apparies) : "
                    "analyse lexicale prudente du texte brut, " + raison)
        return None
    return _blocked_reason_tokens(tokens, profondeur, sous_agent=sous_agent)


def _blocked_reason_tokens(tokens: list, profondeur: int = 0, sous_agent: bool = False):

    lower = [t.lower() for t in tokens]

    # Skip leading VAR=value env-var assignments so `FOO=1 git push --force`
    # is still recognized as a `git` invocation, not dismissed because the
    # segment doesn't start with the literal string "git".
    start = 0
    while start < len(tokens) and re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", tokens[start]):
        start += 1

    if start >= len(tokens):
        return None
    tete = _nom_binaire(tokens[start])
    apres_tete = tokens[start + 1 :]

    # 1. Indirection : la vraie commande est la CHARGE UTILE d'un argument
    #    (`iex '...'`, `powershell -Command '...'`, `-EncodedCommand <base64>`,
    #    `cmd /c ...`). On la re-analyse comme une commande a part entiere.
    if profondeur < _MAX_DEPTH:
        interne = _commande_interne(tete, apres_tete)
        if interne:
            raison = _analyser(_strip_heredocs(interne), profondeur + 1,
                               sous_agent=sous_agent)
            if raison:
                return raison

    # 2. `eval "git push --force"` : la vraie commande est dans les arguments du wrapper.
    # Profondeur bornee (fail-open assume : on ne devine pas au-dela).
    if tete in _WRAPPERS:
        if tete == "xargs" and sous_agent:
            raison = _xargs_git(apres_tete)
            if raison:
                return raison
        if profondeur >= _MAX_DEPTH:
            return None
        for candidat in [*apres_tete, " ".join(apres_tete)]:
            raison = _analyser(candidat, profondeur + 1, sous_agent=sous_agent)
            if raison:
                return raison
        return None

    # 3. Lecture d'un chemin protege par un lecteur ou un interpreteur.
    if tete in _READERS or tete in _INTERPRETERS:
        vises = [t for t in apres_tete if _est_un_chemin_protege(t)]
        if not vises and tete in _INTERPRETERS:
            # `python -c "print(open('.env').read())"` : le chemin est DANS la
            # charge utile, pas dans un argument a lui seul.
            for cand in re.findall(r"""['\"]([^'\"]+)['\"]""", " ".join(apres_tete)):
                if _est_un_chemin_protege(cand):
                    vises = [cand]
                    break
        if vises:
            return (
                f"Lecture d'un fichier protege ({vises[0]}) bloquee par un hook projet — "
                "meme perimetre que les deny rules Read(...) de .claude/settings.json, "
                "qui ne couvrent pas le shell. Confirmez explicitement avec l'utilisateur "
                "si cette lecture est legitime."
            )

    # 4. git destructif.
    if tete != "git":
        # A3 (sub-agent): a computed head (`$g`, `& $g`) followed by a `stash` word.
        if sous_agent and _non_litteral(tokens[start]) and "stash" in lower[start + 1 :]:
            return _REFUS_CALCULE.format(detail=f"executable `{tokens[start]}`")
        return None
    rest = lower[start + 1 :]

    raison = _sous_commande_calculee(tokens, start, rest, profondeur, sous_agent)
    if raison:
        return raison
    if sous_agent:
        raison = _autostash(tokens, start, rest)
        if raison:
            return raison

    if "push" in rest:
        # Grouped short flags (`-fu`, `-uf`, `-qf`) force exactly like `-f`;
        # `--force-if-includes` is a force variant, only safe next to a lease.
        has_force = (
            any(t == "--force" or t.startswith("--force=")
                or t.startswith("--force-if-includes")
                or _prefixe_de(t, "--force-if-includes", 9) for t in rest)
            or "f" in _flags_courts_groupes(rest)
        )
        has_lease = any(
            t == "--force-with-lease" or t.startswith("--force-with-lease=") for t in rest
        )
        # La forme LA PLUS COURANTE du push force ne contient pas le mot `--force` :
        # `git push origin +main` force la mise a jour. Reproduit sur un remote
        # jetable : `git push origin master` refuse (non fast-forward), `+master`
        # accepte avec « (forced update) ».
        has_plus = any(t.startswith("+") and len(t) > 1 for t in rest)
        if has_plus and not has_lease:
            return (
                "git push avec une refspec forcee (« + » devant la ref) est bloque par "
                "un hook projet : c'est un push force qui ne dit pas son nom. Utilisez "
                "--force-with-lease si necessaire, ou confirmez explicitement avec "
                "l'utilisateur."
            )
        if any(t == "--mirror" or t.startswith("--mirror=")
               or _prefixe_de(t, "--mirror", 4) for t in rest):
            return (
                "git push --mirror est bloque par un hook projet : il ecrase TOUTES les "
                "refs distantes (branches et tags) avec l'etat local. Poussez la ref "
                "voulue, ou confirmez explicitement avec l'utilisateur."
            )
        if has_force and not has_lease:
            return (
                "git push --force (sans --force-with-lease) est bloqué par un hook projet. "
                "Utilisez --force-with-lease si nécessaire, ou confirmez explicitement avec "
                "l'utilisateur avant de contourner ce garde-fou."
            )

    # git accepte tout PREFIXE NON AMBIGU d une option longue : `--har`, `--ha` et
    # meme `--h` font un reset dur complet — verifie par execution, le travail non
    # commite est bien detruit. Le test litteral `"--hard" in rest` les laissait tous
    # passer. On borne a 3 caracteres (`--h`), la plus courte forme que git accepte
    # ici, et on exige que ce soit un prefixe de `--hard` : `--hi` n est pas bloque,
    # un garde-fou qui crie a tort finit desarme.
    def _vaut_hard(t: str) -> bool:
        return t.startswith("--h") and "--hard".startswith(t)

    if "reset" in rest and any(_vaut_hard(t) for t in rest):
        return (
            "git reset --hard est bloqué par un hook projet (perte de modifications non "
            "commitées). Utilisez git stash, ou confirmez explicitement avec l'utilisateur."
        )

    raison = _blocked_worktree(tokens[start + 1 :], rest, sous_agent=sous_agent)
    if raison:
        return raison

    return None


# --------------------------------------------------------------------------- #
# Commandes qui DÉTRUISENT le travail non commité d'un fichier
# --------------------------------------------------------------------------- #
# Ajouté le 2026-09-02 (VSCode2), propagé à toute la flotte le 2026-09-07 sur un incident réel :
# un sous-agent de revue, dont le mandat dit pourtant qu'il « ne corrige rien », a joué
# `git checkout --` sur deux templates pour mesurer le code d'avant. Les correctifs non
# commités de la session appelante ont disparu du disque. Ils ont pu être reconstruits
# depuis des copies hors dépôt, mais rien dans le dispositif ne s'y opposait : le
# garde-fou ne connaissait que `push --force` et `reset --hard`, deux commandes qui
# touchent l'HISTORIQUE, alors que le travail perdu ce jour-là était dans l'ARBRE. C'est
# la classe entière qu'il fallait couvrir, pas le cas vu.
#
# Le remède n'est pas d'interdire de mesurer le code d'avant : c'est un besoin légitime
# d'une revue. Le message dit donc comment le faire sans rien détruire
# (`git show HEAD:<fichier>`, qui écrit sur la sortie standard).

_CREATION_DE_BRANCHE = frozenset({"-b", "-B", "--orphan", "--track", "--no-track", "--detach"})

_ALTERNATIVE = (
    "Pour lire le code d'avant sans toucher au disque : `git show HEAD:<fichier>` "
    "(ou `git diff` pour l'écart). Si l'écrasement est réellement voulu, copiez "
    "d'abord le fichier hors du dépôt et confirmez avec l'utilisateur."
)


def _est_un_chemin_du_depot(tok: str) -> bool:
    """Vrai si `tok` désigne un fichier ou un dossier réellement présent.

    C'est ce qui sépare `git checkout main` (une branche : rien à écraser) de
    `git checkout app/templates/x.html` (un fichier : ses modifications non
    commitées disparaissent). Deviner sur la forme du nom ne marcherait pas —
    une branche s'appelle souvent `feature/x`, avec une barre oblique comme un
    chemin. On regarde donc le disque, et on échoue en laissant passer."""
    if tok in (".", "./", ":/"):
        return True
    try:
        racine = os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
        return os.path.exists(os.path.join(racine, tok)) or os.path.exists(tok)
    except Exception:
        return False


def _prefixe_de(token: str, longue: str, minimum: int) -> bool:
    """True when `token` is an abbreviation of the long option `longue` that git accepts.

    git's option parser takes any UNAMBIGUOUS prefix: `git push --mir origin` is `--mirror`
    (a remote branch was deleted by it, reproduced on a throw-away bare repo by the closing
    review of 2026-10-12). `minimum` is the shortest prefix that cannot name another push
    option (`--force-` is ambiguous with `--force-with-lease`, so `--force-if-includes`
    starts at `--force-i`). The `=value` part is ignored."""
    nom = token.split("=", 1)[0]
    return nom.startswith("--") and len(nom) >= minimum and longue.startswith(nom)


def _flags_courts_groupes(rest: list) -> str:
    """Les lettres de tous les groupes de drapeaux courts (`-fdx` -> 'fdx').
    Sans ce dépliage, chercher `-f` laissait passer `git clean -fd`, qui est
    exactement la forme qu'on écrit en pratique."""
    lettres = []
    for t in rest:
        if t.startswith("-") and not t.startswith("--") and len(t) > 1:
            lettres.append(t[1:])
    return "".join(lettres)


# Options GLOBALES de `git` (avant la sous-commande) qui prennent leur valeur
# dans un TOKEN SEPARE : `git -C . checkout ...`, `git -c core.pager=cat push
# ...`. Sans les reconnaitre, chercher « le premier token qui ne commence pas
# par - » prenait la VALEUR pour la sous-commande, ce qui desarmait tout le
# volet arbre -- reproduit par revue adversariale le 2026-09-07 :
# `git -C . checkout -- f.txt` passait, alors que `-C` est precisement la
# forme employee pour agir sur un depot tiers, le metier de ce hub (R2/R3).
# Deja en minuscules ici : `rest` est lowercased avant d'atteindre cette
# fonction, donc `-C` (chemin) et `-c` (config) y sont indiscernables --
# les deux prennent un token separe, le traitement est donc identique.
_GLOBALES_AVEC_VALEUR = frozenset({
    "-c", "--git-dir", "--work-tree", "--namespace", "--exec-path",
    "--super-prefix", "--config-env",
})


def _sous_commande_index(rest: list):
    """Index de la vraie sous-commande dans `rest` (tokens apres `git`, deja
    en minuscules), en sautant les options globales et leur valeur quand
    elle est un token separe. None si aucune sous-commande trouvee."""
    i = 0
    n = len(rest)
    while i < n:
        t = rest[i]
        if not t.startswith("-"):
            return i
        if "=" not in t and t in _GLOBALES_AVEC_VALEUR and i + 1 < n:
            i += 2  # saute le drapeau ET sa valeur (token separe)
            continue
        i += 1
    return None


# --------------------------------------------------------------------------- #
# Sous-commande CALCULEE : alias git et texte non decode (lot s-stash-robuste)
# --------------------------------------------------------------------------- #
# Decision utilisateur du 2026-11-05 : « corriger et rendre robuste ». La garde
# lexicale ne voit que le texte ; elle DEPLIE donc ce que git deplierait lui-meme
# (alias en ligne `-c alias.x=...`, `--config-env`, `GIT_CONFIG_KEY_<n>`, alias
# persistant lu par `git config --get`), et, pour un SOUS-AGENT seulement, refuse
# ce qu'elle ne sait pas decoder dans la famille stash (fail-closed). La detection
# a posteriori de ce qui reste (un script qui calcule `'st'+'ash'`) est le role de
# temoin_stash_sous_agent.py, pas de cette garde.

# `git --list-cmds=builtins,main,nohelpers` (git 2.54.0.windows.1, 2026-11-05) : git
# ignore un alias qui porte le nom d'une commande existante, on ne le deplie donc pas.
_GIT_COMMANDES = frozenset((
    "add am annotate apply archive backfill bisect blame branch bugreport bundle cat-file "
    "check-attr check-ignore check-mailmap checkout checkout-index check-ref-format cherry "
    "cherry-pick citool clean clone column commit commit-graph commit-tree config "
    "count-objects credential credential-cache credential-store credential-wincred daemon "
    "describe diagnose diff diff-files diff-index diff-pairs difftool diff-tree fast-export "
    "fast-import fetch fetch-pack filter-branch fmt-merge-msg for-each-ref for-each-repo "
    "format-patch fsck fsck-objects gc get-tar-commit-id grep gui help history hook "
    "http-backend http-fetch http-push imap-send index-pack init init-db interpret-trailers "
    "last-modified log ls-files ls-remote ls-tree mailinfo mailsplit maintenance merge "
    "merge-base merge-file merge-index merge-octopus merge-one-file merge-ours "
    "merge-recursive merge-recursive-ours merge-recursive-theirs merge-resolve "
    "merge-subtree mergetool merge-tree mktag mktree multi-pack-index mv name-rev notes "
    "pack-objects pack-redundant pack-refs patch-id pickaxe prune prune-packed pull push "
    "quiltimport range-diff read-tree rebase receive-pack reflog refs remote remote-ext "
    "remote-fd remote-ftp remote-ftps remote-http remote-https repack replace replay repo "
    "request-pull rerere reset restore revert rev-list rev-parse rm send-email send-pack "
    "shortlog show show-branch show-index show-ref sparse-checkout stage stash status "
    "stripspace submodule subtree survey switch symbolic-ref tag unpack-file "
    "unpack-objects update update-index update-ref update-server-info upload-archive "
    "upload-pack var verify-commit verify-pack verify-tag version whatchanged worktree "
    "write-tree").split())
_NOM_ALIAS = re.compile(r"^[a-z0-9][a-z0-9._-]{0,63}$")
_ECHEC = object()        # config could not be read (unreadable, malformed): unknown, not absent
_INCONNU = object()      # alias defined but its value is not knowable (--config-env)
_CWD: list = [None]      # tool cwd from the payload, for persistent alias resolution
_BRUT: list = [""]       # raw command text (heredocs included), set by main()
_ENV_CMD: dict = {}      # config-related variables the command assigns or exports itself
_OPAQUE: list = [False]  # ... in a form the guard cannot decode (computed value, Set-Item...)

_REFUS_CALCULE = (
    "Sous-commande git calculee ({detail}) refusee pour un sous-agent par un hook "
    "projet : la garde ne peut pas verifier qu'il ne s'agit pas d'un `git stash` (la "
    "paire stash/pop reecrit l'arbre, qui porte le travail non commite d'autres "
    "sessions). Ecrivez la sous-commande en toutes lettres, lisez l'ancien etat avec "
    "`git show HEAD:<chemin>`, ou rendez la main a la session principale.")


def _non_litteral(tok: str) -> bool:
    """A token whose value is computed by the shell: `$S`, `$(`, backtick, `%S%`, `(`."""
    return any(c in tok for c in "$`(") or re.search(r"%[^%\s]+%", tok) is not None


def _env_effectif(tokens: list, start: int) -> dict:
    """The environment git will see: the hook's, then what the command exported or
    assigned in earlier segments (_ENV_CMD), then the segment's leading assignments."""
    env = dict(os.environ)
    env.update(_ENV_CMD)
    for t in tokens[:start]:
        k, _, v = t.partition("=")
        env[k] = v
    return env


def _parametres_config(texte: str) -> list:
    """GIT_CONFIG_PARAMETERS (`'k=v' 'k2=v2'`) -> [(k, v)]."""
    try:
        mots = shlex.split(texte, posix=True)
    except ValueError:
        mots = re.findall(r"[^\s']+=[^']*", texte)
    paires = []
    for m in mots:
        k, sep, v = m.partition("=")
        if k:
            paires.append((k.lower(), v if sep else None))
    return paires


def _config_commande(tokens: list, start: int, rest: list) -> list:
    """[(key, value)] of the COMMAND scope, in git's order: GIT_CONFIG_PARAMETERS,
    GIT_CONFIG_KEY_<n>/GIT_CONFIG_VALUE_<n> (hook env, earlier exports, leading
    assignments), then `-c k=v` and `--config-env[=]k=VAR` (VAR unknown -> _INCONNU).
    Keys lowercased."""
    env = _env_effectif(tokens, start)
    paires = _parametres_config(env.get("GIT_CONFIG_PARAMETERS", ""))
    for k in sorted((k for k in env if re.match(r"GIT_CONFIG_KEY_\d+$", k)),
                    key=lambda k: int(k[15:])):
        paires.append((env[k].lower(), env.get("GIT_CONFIG_VALUE_" + k[15:], "")))
    orig = tokens[start + 1 :]
    i = 0
    while i < len(rest) and rest[i].startswith("-"):
        t = rest[i]
        if t == "-c" and i + 1 < len(rest) and orig[i] == "-c":
            nom, sep, val = orig[i + 1].partition("=")
            paires.append((nom.lower(), val if sep else None))
            i += 2
            continue
        spec = None
        if t == "--config-env" and i + 1 < len(rest):
            spec, i = orig[i + 1], i + 2
        elif t.startswith("--config-env="):
            spec, i = orig[i][len("--config-env="):], i + 1
        elif "=" not in t and t in _GLOBALES_AVEC_VALEUR and i + 1 < len(rest):
            i += 2
            continue
        else:
            i += 1
            continue
        nom, sep, var = spec.partition("=")
        if sep:
            val = env.get(var)
            paires.append((nom.lower(), _INCONNU if val is None else val))
    return paires


def _alias_en_ligne(tokens: list, start: int, rest: list) -> dict:
    """{name: value} of the aliases the command scope defines (see _config_commande)."""
    return {k[6:]: ("" if v is None else v) for k, v in _config_commande(tokens, start, rest)
            if k.startswith("alias.")}


def _est_include(cle: str) -> bool:
    return cle == "include.path" or (cle.startswith("includeif.") and cle.endswith(".path"))


# --- git config files, read directly (lot s-stash-correctif, 2026-11-05) -------------
# The persistent alias used to be asked to `git config --get` in a subprocess bounded
# at 2 s. On a loaded machine that child hung; the timeout killed the Git for Windows
# launcher only, the real git grandchild kept the stdout/stderr pipes open and
# `communicate()` waited forever: the guard (and the PreToolUse dispatcher) stalled.
# The guard now spawns NOTHING: it reads the config files git would read.

_CONFIG_PROFONDEUR = 5          # include depth (git allows 10; deeper -> _ECHEC)
_CONFIG_MAX_OCTETS = 1_000_000  # one config file, beyond -> _ECHEC
# GLOBAL budget per guard call (lot s-stash-correctif3): the cycle check only sees the
# include STACK; a DAG where each file includes the next one 30 times over 4 levels
# meant 810 000 reads (> 60 s, main session blocked too). Beyond -> _ECHEC.
_CONFIG_MAX_LECTURES = 64       # config files read in total
_CONFIG_DELAI = 0.5             # seconds spent reading config, in total
_LECTURES: list = [0, None]     # [files read, monotonic deadline], reset by _analyser
_VARS_EMPLACEMENT = frozenset({  # variables that MOVE the config files git reads
    "GIT_CONFIG_GLOBAL", "GIT_CONFIG_SYSTEM", "GIT_CONFIG_NOSYSTEM", "GIT_CONFIG",
    "GIT_DIR", "GIT_COMMON_DIR", "HOME", "XDG_CONFIG_HOME", "USERPROFILE"})
_VAR_CONFIG = re.compile(r"(?i)^(?:GIT_CONFIG\w*|GIT_DIR|GIT_COMMON_DIR|HOME|"
                         r"XDG_CONFIG_HOME|USERPROFILE)$")
_MENTION_CONFIG = re.compile(r"(?i)(?<![\w])(?:GIT_CONFIG\w*|GIT_DIR|GIT_COMMON_DIR|"
                             r"XDG_CONFIG_HOME)(?![\w])")
_ECRIT_CONFIG = re.compile(r"(?i)\.git[/\\]+config|\.gitconfig|git[/\\]+config(?![\w.-])"
                           r"|config\.worktree")
_ECHAPPEMENTS = {'"': '"', "\\": "\\", "n": "\n", "t": "\t", "b": "\b"}


class _ErreurConfig(Exception):
    """A config file git would read cannot be read or parsed by the guard."""


def _valeur_config(texte: str, i: int):
    """One value from `texte[i:]` -> (value, index of the end of line)."""
    n, buf, protege, cite = len(texte), [], 0, False
    while i < n:
        c = texte[i]
        if c == "\n":
            if cite:
                raise _ErreurConfig("unterminated quote")
            break
        if not cite and c in "#;":
            j = texte.find("\n", i)
            i = n if j < 0 else j
            break
        if c == "\\":
            suivant = texte[i + 1] if i + 1 < n else ""
            if suivant == "\n":          # continuation
                i += 2
                continue
            if suivant and suivant in _ECHAPPEMENTS:
                buf.append(_ECHAPPEMENTS[suivant])
                protege = len(buf)
                i += 2
                continue
            raise _ErreurConfig("bad escape")
        if c == '"':
            cite = not cite
            protege = len(buf)
            i += 1
            continue
        buf.append(c)
        if cite:
            protege = len(buf)
        i += 1
    if cite:
        raise _ErreurConfig("unterminated quote")
    k = len(buf)
    while k > protege and buf[k - 1] in " \t":   # trailing unquoted blanks dropped
        k -= 1
    return "".join(buf[:k]), i


def _analyser_config(texte: str) -> list:
    """git config syntax -> [(key, value)]: key `section[.subsection].name` lowercased
    (`[alias]`, `[Alias]`, `[section "sub"]`, legacy `[section.sub]`), value None for a
    bare boolean key. Comments `;`/`#`, quotes, `\\` escapes and continuation. Raises
    _ErreurConfig on what git itself rejects."""
    texte = texte.replace("\r\n", "\n").lstrip("﻿")
    n, i, section, paires = len(texte), 0, None, []
    while i < n:
        c = texte[i]
        if c in " \t\n\r\f\v":
            i += 1
            continue
        if c in "#;":
            j = texte.find("\n", i)
            i = n if j < 0 else j
            continue
        if c == "[":
            j = i + 1
            while j < n and (texte[j].isalnum() or texte[j] in "-."):
                j += 1
            nom = texte[i + 1 : j].lower()
            if not nom:
                raise _ErreurConfig("empty section")
            if j < n and texte[j] == "]":
                section, i = nom, j + 1
                continue
            if j >= n or texte[j] not in " \t":
                raise _ErreurConfig("bad section header")
            while j < n and texte[j] in " \t":
                j += 1
            if j >= n or texte[j] != '"':
                raise _ErreurConfig("bad section header")
            j += 1
            sous = []
            while True:
                if j >= n or texte[j] == "\n":
                    raise _ErreurConfig("bad subsection")
                if texte[j] == '"':
                    break
                if texte[j] == "\\" and j + 1 < n and texte[j + 1] != "\n":
                    j += 1
                sous.append(texte[j])
                j += 1
            if j + 1 >= n or texte[j + 1] != "]":
                raise _ErreurConfig("bad section header")
            section, i = nom + "." + "".join(sous).lower(), j + 2
            continue
        if c.isalpha():
            j = i
            while j < n and (texte[j].isalnum() or texte[j] == "-"):
                j += 1
            cle = texte[i:j].lower()
            if section is None:
                raise _ErreurConfig("key outside a section")
            while j < n and texte[j] in " \t":
                j += 1
            if j >= n or texte[j] in "\n#;":
                paires.append((section + "." + cle, None))
                i = j
                continue
            if texte[j] != "=":
                raise _ErreurConfig("bad key")
            j += 1
            while j < n and texte[j] in " \t":
                j += 1
            valeur, i = _valeur_config(texte, j)
            paires.append((section + "." + cle, valeur))
            continue
        raise _ErreurConfig("unexpected character")
    return paires


def _vrai(v) -> bool:
    """git boolean: a bare key (None) or yes/on/true/1."""
    return v is None or (isinstance(v, str) and v.strip().lower() in ("yes", "on", "true", "1"))


def _maison(env: dict) -> str:
    h = env.get("HOME") or ""
    if os.name == "nt":
        m = re.match(r"^/([A-Za-z])(/.*)?$", h)   # MSYS `/c/Users/x`
        if m:
            h = m.group(1) + ":" + (m.group(2) or "/")
        if not h:
            h = (env.get("HOMEDRIVE", "") + env.get("HOMEPATH", "")) or env.get("USERPROFILE", "")
    return h or os.path.expanduser("~")


def _config_systeme(env: dict):
    """System config path without spawning git: GIT_CONFIG_SYSTEM, else `etc/gitconfig`
    next to the first `git` found on PATH (Git for Windows `<root>/cmd/git.exe` ->
    `<root>/etc/gitconfig`; `/usr/bin/git` -> `/etc/gitconfig`). None = skip."""
    if env.get("GIT_CONFIG_NOSYSTEM") and _vrai(env["GIT_CONFIG_NOSYSTEM"]):
        return None
    if env.get("GIT_CONFIG_SYSTEM") is not None:
        return env["GIT_CONFIG_SYSTEM"] or None
    noms = ("git.exe", "git") if os.name == "nt" else ("git",)
    for d in (env.get("PATH") or "").split(os.pathsep):
        if not d or not any(os.path.isfile(os.path.join(d, x)) for x in noms):
            continue
        parent = os.path.dirname(os.path.abspath(d))
        for racine in (parent, os.path.dirname(parent)):
            c = os.path.join(racine, "etc", "gitconfig")
            if os.path.isfile(c):
                return c
        return None
    return None


def _chemin_include(val: str, base: str, env: dict) -> str:
    if val == "~" or val.startswith(("~/", "~\\")):
        return os.path.join(_maison(env), val[2:])
    if val.startswith("%(prefix)/"):
        raise _ErreurConfig("%(prefix) include")
    return os.path.join(base, val)


def _lire_config(chemin: str, env: dict, acc: list, strict: bool, inclus_strict: bool,
                 profondeur: int = 0, pile: frozenset = frozenset()):
    """Append the (key, value) of `chemin` to `acc`, following include.path and
    includeIf.<cond>.path AT the point of inclusion (every includeIf counted as true:
    conservative). Absent file: skipped like git does, unless `strict` (a path the
    command itself set: it may be written by that same command). Unreadable, too big,
    malformed, too deep or cyclic: _ErreurConfig."""
    if profondeur > _CONFIG_PROFONDEUR:
        raise _ErreurConfig("include depth")
    reel = os.path.normcase(os.path.realpath(chemin))
    if reel in pile:
        raise _ErreurConfig("include cycle")
    if not os.path.lexists(chemin):
        if strict:
            raise _ErreurConfig("absent")
        return
    if _LECTURES[1] is None:
        _LECTURES[1] = time.monotonic() + _CONFIG_DELAI
    _LECTURES[0] += 1
    if _LECTURES[0] > _CONFIG_MAX_LECTURES or time.monotonic() > _LECTURES[1]:
        raise _ErreurConfig("include budget")
    try:
        if os.path.getsize(chemin) > _CONFIG_MAX_OCTETS:
            raise _ErreurConfig("too big")
        with open(chemin, "rb") as fh:
            texte = fh.read().decode("utf-8", "replace")
    except OSError as e:
        raise _ErreurConfig("unreadable") from e
    for cle, val in _analyser_config(texte):
        acc.append((cle, val))
        if _est_include(cle) and val:
            _lire_config(_chemin_include(val, os.path.dirname(os.path.abspath(chemin)), env),
                         env, acc, inclus_strict, inclus_strict, profondeur + 1, pile | {reel})


def _suivre_fichier_git(fichier: str) -> str:
    with open(fichier, encoding="utf-8", errors="replace") as fh:
        ligne = fh.read().strip()
    if not ligne.startswith("gitdir:"):
        raise _ErreurConfig("bad .git file")
    cible = ligne[len("gitdir:"):].strip()
    return os.path.join(os.path.dirname(os.path.abspath(fichier)), cible)


def _depot(depart: str, gitdir: str | None):
    """(gitdir, commondir) of the repository git would use, (None, None) outside one.
    Files only: `.git` dir, `.git` file -> `gitdir:`, bare repo, then `commondir`."""
    try:
        if gitdir:
            if os.path.isfile(gitdir):
                gitdir = _suivre_fichier_git(gitdir)
            if not os.path.isdir(gitdir):
                raise _ErreurConfig("bad --git-dir")
        else:
            if not os.path.isdir(depart):
                raise _ErreurConfig("cwd absent")
            d = os.path.abspath(depart)
            for _ in range(64):
                cand = os.path.join(d, ".git")
                if os.path.isdir(cand):
                    gitdir = cand
                    break
                if os.path.isfile(cand):
                    gitdir = _suivre_fichier_git(cand)
                    break
                if (os.path.isfile(os.path.join(d, "HEAD"))
                        and os.path.isdir(os.path.join(d, "objects"))
                        and os.path.isfile(os.path.join(d, "config"))):
                    gitdir = d   # bare repository
                    break
                parent = os.path.dirname(d)
                if parent == d:
                    return None, None
                d = parent
            else:
                return None, None
        commun = gitdir
        f = os.path.join(gitdir, "commondir")
        if os.path.isfile(f):
            with open(f, encoding="utf-8", errors="replace") as fh:
                commun = os.path.join(gitdir, fh.read().strip())
        return gitdir, commun
    except OSError as e:
        raise _ErreurConfig("repository unreadable") from e


def _config_fichiers(globales: list, env: dict, includes_cmd: list, vars_cmd: set,
                     sous_agent: bool) -> list:
    """[(key, value)] of the config FILES git reads, lowest precedence first: system,
    global (GIT_CONFIG_GLOBAL, else XDG then ~/.gitconfig), repository (common dir),
    worktree (extensions.worktreeConfig), then the command-scope include.path files.
    Raises _ErreurConfig."""
    depart = _CWD[0] or os.getcwd()
    gitdir = None
    i = 0
    while i < len(globales):
        t, tl = globales[i], globales[i].lower()
        valeur = None
        if t == "-C" and i + 1 < len(globales):
            valeur = globales[i + 1]
            if _non_litteral(valeur):
                raise _ErreurConfig("computed -C")
            if valeur:
                depart = os.path.join(depart, valeur)
            i += 2
            continue
        if tl == "--git-dir" and i + 1 < len(globales):
            valeur, i = globales[i + 1], i + 2
        elif tl.startswith("--git-dir="):
            valeur, i = t[len("--git-dir="):], i + 1
        else:
            if "=" not in tl and tl in _GLOBALES_AVEC_VALEUR:
                i += 1
            i += 1
            continue
        if _non_litteral(valeur):
            raise _ErreurConfig("computed --git-dir")
        gitdir = os.path.join(depart, valeur)
    if gitdir is None and env.get("GIT_DIR"):
        gitdir = os.path.join(depart, env["GIT_DIR"])
    acc = []
    systeme = _config_systeme(env)
    if systeme:
        _lire_config(systeme, env, acc, sous_agent and "GIT_CONFIG_SYSTEM" in vars_cmd,
                     sous_agent)
    if env.get("GIT_CONFIG_GLOBAL") is not None:
        if env["GIT_CONFIG_GLOBAL"]:
            _lire_config(env["GIT_CONFIG_GLOBAL"], env, acc,
                         sous_agent and "GIT_CONFIG_GLOBAL" in vars_cmd, sous_agent)
    else:
        maison = _maison(env)
        xdg = env.get("XDG_CONFIG_HOME")
        _lire_config(os.path.join(xdg, "git", "config") if xdg
                     else os.path.join(maison, ".config", "git", "config"),
                     env, acc, False, sous_agent)
        _lire_config(os.path.join(maison, ".gitconfig"), env, acc, False, sous_agent)
    gitdir, commun = _depot(depart, gitdir)
    if env.get("GIT_COMMON_DIR") and gitdir:
        commun = os.path.join(depart, env["GIT_COMMON_DIR"])
    if commun:
        debut = len(acc)
        _lire_config(os.path.join(commun, "config"), env, acc, False, sous_agent)
        if any(k == "extensions.worktreeconfig" and _vrai(v) for k, v in acc[debut:]):
            _lire_config(os.path.join(gitdir, "config.worktree"), env, acc, False, sous_agent)
    for inc in includes_cmd:
        if _non_litteral(inc):
            raise _ErreurConfig("computed include")
        _lire_config(_chemin_include(inc, depart, env), env, acc, sous_agent, sous_agent)
    return acc


def _config_complete(tokens: list, start: int, rest: list, idx: int, sous_agent: bool):
    """[(key, value)] files then command scope (later wins), or _ECHEC."""
    orig = tokens[start + 1 :]
    env = _env_effectif(tokens, start)
    commande = _config_commande(tokens, start, rest)
    includes = [v for k, v in commande if _est_include(k) and isinstance(v, str) and v]
    if any(_est_include(k) and v is _INCONNU for k, v in commande):
        return _ECHEC
    vars_cmd = set(_ENV_CMD) | {t.partition("=")[0].upper() for t in tokens[:start]}
    try:
        return _config_fichiers(orig[:idx], env, includes, vars_cmd, sous_agent) + commande
    except (_ErreurConfig, OSError, ValueError):
        return _ECHEC


def _resoudre_alias_persistant(tokens: list, start: int, rest: list, idx: int, nom: str,
                               sous_agent: bool):
    """Value of `alias.<nom>` (str), None when it is not an alias, _ECHEC when the
    config cannot be read. File reads only: no subprocess, no network."""
    paires = _config_complete(tokens, start, rest, idx, sous_agent)
    if paires is _ECHEC:
        return _ECHEC
    nom = nom.lower()   # alias names are case-insensitive (`git X` runs alias.x)
    cles = ("alias." + nom, "alias." + nom + ".command")   # [alias "x"] command = ...
    valeur = None
    for k, v in paires:
        if k.lower() in cles:
            valeur = "" if v is None else v
    return valeur


def _collecter_env_commande(cmd: str):
    """Config-related variables a command sets for the git it runs later -- `export
    A=1 B=2`, bare `A=1` (exported afterwards or not: conservative), `set A=1`,
    PowerShell `$env:A = 'v'` -> (dict, opaque). `opaque` is True when such a variable
    is mentioned in a form the guard does not decode (computed value, `Set-Item
    env:...`, `[Environment]::SetEnvironmentVariable`, `env A=$x ...`)."""
    env, opaque = {}, False
    for seg in _segments(cmd):
        if not (_MENTION_CONFIG.search(seg)
                or re.search(r"(?i)(?<![\w])(?:HOME|USERPROFILE)\s*=", seg)):
            continue
        m = re.match(r"(?is)^\$env:([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)$", seg.strip())
        if m:
            nom = m.group(1).upper()
            try:
                mots = shlex.split(m.group(2), posix=True)
            except ValueError:
                mots = []
            if len(mots) == 1 and not _non_litteral(mots[0]):
                env[nom] = mots[0]
            elif _VAR_CONFIG.match(nom):
                opaque = True
            continue
        try:
            toks = shlex.split(seg, posix=True)
        except ValueError:
            opaque = True
            continue
        k = 0
        if toks and toks[0].lower() in ("export", "set", "declare", "typeset", "local",
                                        "readonly", "env"):
            k = 1
            while k < len(toks) and toks[k].startswith("-"):
                k += 1
        while k < len(toks):
            nom, sep, val = toks[k].partition("=")
            if not re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", nom):
                break
            if sep:
                if _VAR_CONFIG.match(nom):
                    if _non_litteral(val):
                        opaque = True
                    else:
                        env[nom.upper()] = val
            elif toks[0].lower() not in ("export", "declare", "typeset", "readonly"):
                break   # a command word, not `export NAME`
            k += 1
        if any(_MENTION_CONFIG.search(t) for t in toks[k:]):
            opaque = True
    return env, opaque


def _sous_commande_calculee(tokens: list, start: int, rest: list, profondeur: int,
                            sous_agent: bool):
    """Expand a git-level alias and re-analyse (A1 inline, A2 persistent, all contexts);
    refuse a sub-agent's non-literal or unresolvable sub-command (A3 i, ii)."""
    idx = _sous_commande_index(rest)
    if idx is None:
        return None
    nom = rest[idx]
    orig = tokens[start + 1 :]
    if _non_litteral(nom):
        return _REFUS_CALCULE.format(detail=f"`{orig[idx]}`") if sous_agent else None
    # built-ins are case-SENSITIVE (`git STASH` is not the built-in: git resolves an
    # alias `stash`), alias names are case-insensitive (lot s-stash-correctif3)
    nom = nom.lower()
    if orig[idx] in _GIT_COMMANDES or not _NOM_ALIAS.match(nom):
        return None   # git runs the built-in, never an alias of the same name
    alias = {k.lower(): v for k, v in _alias_en_ligne(tokens, start, rest).items()}
    if nom not in alias and nom + ".command" in alias:
        nom_cle = nom + ".command"   # [alias "x"] command = ... given as -c alias.x.command
    else:
        nom_cle = nom
    valeur = alias.get(nom_cle)
    if nom_cle not in alias:
        if sous_agent:
            # 2a: the alias may come from a config the command itself redirects or
            # writes (GIT_CONFIG_GLOBAL=..., HOME=..., `>> .git/config`): unknowable.
            deplace = (set(_ENV_CMD) | {t.partition("=")[0].upper() for t in tokens[:start]}
                       ) & (_VARS_EMPLACEMENT - {"GIT_CONFIG_GLOBAL", "GIT_CONFIG_SYSTEM"})
            if _OPAQUE[0] or deplace or _ECRIT_CONFIG.search(_BRUT[0]):
                return _REFUS_CALCULE.format(
                    detail=f"alias `{nom}` sous une configuration git modifiee par la commande")
        valeur = _resoudre_alias_persistant(tokens, start, rest, idx, nom, sous_agent)
        if valeur is None:
            return None   # not an alias: an external `git-<nom>` or a typo
    if valeur is _ECHEC or valeur is _INCONNU or profondeur >= _MAX_DEPTH:
        return (_REFUS_CALCULE.format(detail=f"alias `{nom}` non resolu")
                if sous_agent else None)
    apres = orig[idx + 1 :]
    valeur = valeur.strip()
    if valeur.startswith("!"):
        # shell alias: git runs the body with the remaining arguments appended
        corps = valeur[1:] + "".join(" " + shlex.quote(a) for a in apres)
        return _analyser(corps, profondeur + 1, sous_agent=sous_agent)
    try:
        mots = shlex.split(valeur, posix=True)
    except ValueError:
        mots = valeur.split()
    return _blocked_reason_tokens(tokens[: start + 1] + orig[:idx] + mots + apres,
                                  profondeur + 1, sous_agent=sous_agent)


def _xargs_git(apres_xargs: list):
    """2b (sub-agent): `echo stash | xargs git` -- the sub-command comes from stdin, or
    is the `-I` replacement string: refused unless it is written literally."""
    remplacement = None
    k = 0
    while k < len(apres_xargs):
        t = apres_xargs[k]
        if _nom_binaire(t) == "git":
            break
        if t == "-I" and k + 1 < len(apres_xargs):
            remplacement, k = apres_xargs[k + 1], k + 2
            continue
        if t.startswith("-I") and len(t) > 2:
            remplacement = t[2:]
        elif t.startswith("--replace"):
            remplacement = t.partition("=")[2] or "{}"
        elif t.startswith("-i"):
            remplacement = t[2:] or "{}"
        k += 1
    else:
        return None
    suite = apres_xargs[k + 1 :]
    idx = _sous_commande_index([t.lower() for t in suite])
    if (idx is None or not _NOM_ALIAS.match(suite[idx].lower())
            or (remplacement and remplacement in suite[idx])):
        return _REFUS_CALCULE.format(detail="`xargs ... git` sans sous-commande litterale")
    return None


# 2c (sub-agent): the stash list IS refs/stash and its reflog; writing them directly
# (`update-ref`, `reflog delete|expire`) drops or forges stash entries.
_LECTEURS_DE_REFS = frozenset({
    "show", "log", "rev-parse", "rev-list", "diff", "diff-tree", "cat-file", "show-ref",
    "for-each-ref", "describe", "name-rev", "shortlog", "ls-tree", "grep", "whatchanged",
    "show-branch", "merge-base", "blame", "cherry", "range-diff", "format-patch",
    "verify-commit", "archive"})
_REF_STASH = re.compile(r"^\+?(?:[^:\s]*:)?(?:refs/stash(?![\w/-])|stash@\{)")
_REFUS_REFS_STASH = (
    "Ecriture directe de la remise git (refs/stash, stash@{n}, reflog de la remise) "
    "refusee pour un sous-agent par un hook projet : elle supprime ou forge des entrees "
    "de remise qui portent le travail non commite d'autres sessions. Les lectures "
    "restent permises (`git show stash@{0}`, `git log refs/stash`, `git stash list`) ; "
    "rendez la main a la session principale pour toute modification.")


def _ecrit_refs_stash(sous: str, bas: list) -> bool:
    nomme = any(_REF_STASH.match(t) for t in bas)
    if sous == "reflog":
        action = next((t for t in bas if not t.startswith("-")), None)
        return action in ("expire", "delete", "drop", "write") and (
            nomme or "--all" in bas or "stash" in bas)
    if sous == "update-ref" and "--stdin" in bas:
        return True   # the ref operations come from stdin: unknowable
    return nomme and sous not in _LECTEURS_DE_REFS


_AUTOSTASH_CLES = {"rebase": ("rebase.autostash",), "merge": ("merge.autostash",),
                   "pull": ("rebase.autostash", "merge.autostash")}
_REFUS_AUTOSTASH = (
    "git {sous} avec autostash ({source}) refuse pour un sous-agent par un hook projet : "
    "--autostash cree une remise interne (un `git stash`) avant l'operation et la "
    "re-applique apres -- la meme paire stash/pop qui reecrit l'arbre de travail, lequel "
    "porte le travail non commite d'autres sessions. Relancez sur un arbre propre avec "
    "--no-autostash, ou rendez la main a la session principale.")


def _autostash(tokens: list, start: int, rest: list):
    """2d (sub-agent): rebase/pull/merge with --autostash (prefix accepted), or with
    rebase.autoStash / merge.autoStash true in the command scope or the config files
    (an unreadable config is refused too)."""
    idx = _sous_commande_index(rest)
    if idx is None or rest[idx] not in _AUTOSTASH_CLES:
        return None
    sous = rest[idx]
    choix = None
    for t in rest[idx + 1 :]:
        if t == "--":
            break
        if t == "--autostash" or _prefixe_de(t, "--autostash", 8):
            choix = True
        elif t == "--no-autostash" or _prefixe_de(t, "--no-autostash", 11):
            choix = False
    if choix is True:
        return _REFUS_AUTOSTASH.format(sous=sous, source="--autostash")
    if choix is False:
        return None
    paires = _config_complete(tokens, start, rest, idx, True)
    if paires is _ECHEC:
        return _REFUS_AUTOSTASH.format(sous=sous, source="configuration git illisible")
    for cle in _AUTOSTASH_CLES[sous]:
        etat = None
        for k, v in paires:
            if k == cle:
                etat = v is not _INCONNU and _vrai(v)
                if v is _INCONNU:
                    etat = True
        if etat:
            return _REFUS_AUTOSTASH.format(sous=sous, source=f"{cle} = true")
    return None


_LECTURES_CONFIG = frozenset({"--get", "--get-all", "--get-regexp", "--get-urlmatch",
                              "--list", "-l", "--get-color", "--get-colorbool"})


def _config_ecrit_un_alias(bas: list) -> bool:
    """`git config` that WRITES (sets, adds, unsets, renames) an `alias.` key (A3 iii)."""
    positionnels = [t for t in bas if not t.startswith("-")]
    touche = (any(t.startswith("alias.") for t in positionnels)
              or ("alias" in positionnels
                  and any(t in ("--rename-section", "--remove-section") for t in bas)))
    if not touche:
        return False
    if any(t in _LECTURES_CONFIG for t in bas):
        return False
    if positionnels[0] in ("get", "list"):
        return False
    # old syntax: `git config alias.x` (one name, no value, no write flag) only reads
    ecritures = ("--unset", "--unset-all", "--add", "--replace-all", "--rename-section",
                 "--remove-section")
    return len(positionnels) > 1 or any(t.split("=")[0] in ecritures for t in bas)


_INTERPRETE = re.compile(
    r"(?i)(?<![\w.-])(?:py|python|python3|node|perl|ruby|deno)(?:\.exe)?(?![\w.-])"
    r"[^\n]*?(?:\s-[a-z]*[ce]\b|\s-\s|\s-$|<<)"
    r"|(?<![\w-])(?:iex|invoke-expression)(?![\w-])")
_MOT_GIT = re.compile(r"(?i)(?<![\w-])git(?![\w-])")
_MOT_STASH = re.compile(r"(?i)(?<![\w-])stash(?![\w-])")


_TETES_INTERPRETE = _INTERPRETERS | _SHELL_RUNNERS | {"iex", "invoke-expression"}


def _interpreteur_en_tete(cmd_brut: str) -> bool:
    """4: an interpreter (or shell runner, or iex) in COMMAND position of some segment
    -- not quoted inside a git argument (`git commit -m "py -c stash"` used to be a
    false refusal). Wrappers and leading assignments are skipped; an unparsable
    segment counts as True (conservative)."""
    for seg in _segments(_strip_heredocs(_normaliser(cmd_brut))):
        try:
            toks = shlex.split(seg, posix=True)
        except ValueError:
            return True
        k = 0
        while k < len(toks):
            t = toks[k].lstrip("`")
            if re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", t) or (k and t.startswith("-")):
                k += 1
                continue
            if k + 1 < len(toks) and toks[k + 1] == "=" and t.startswith("$"):
                k += 2   # PowerShell `$x = py -c ...`
                continue
            if _nom_binaire(t) in _WRAPPERS:
                k += 1
                continue
            break
        if k < len(toks) and _nom_binaire(toks[k].lstrip("`")) in _TETES_INTERPRETE:
            return True
    return False


def _interpreteur_stash(cmd_brut: str):
    """A3 iv (sub-agent): a string handed to an interpreter the guard does not decode
    (`py -c`, `node -e`, `perl -e`, `ruby -e`, a heredoc fed to one of them, `iex` on a
    concatenation) that carries both a `git` and a `stash` word. Read on the RAW text,
    heredoc bodies included: `py - <<EOF ... EOF` is code, not data, for this check."""
    if not _INTERPRETE.search(cmd_brut) or not _interpreteur_en_tete(cmd_brut):
        return None
    # The whole text, not only the interpreter's argument: `$a='stash'; iex ('git ' +
    # $a)` assembles its words before the call. Literal reads (`git stash list|show`)
    # are removed first: they are decoded by the main analysis and stay allowed.
    texte = re.sub(r"(?i)(?<![\w-])git\s+stash\s+(?:list|show)\b", " ", cmd_brut)
    if _MOT_GIT.search(texte) and _MOT_STASH.search(texte):
        return _REFUS_CALCULE.format(detail="chaine executee par un interpreteur")
    return None


def _blocked_worktree(tokens_apres_git: list, rest: list, sous_agent: bool = False):
    idx = _sous_commande_index(rest)
    if idx is None:
        return None
    sous_commande = rest[idx]
    args = tokens_apres_git[idx + 1 :]  # tokens ORIGINAUX (casse preservee), apres la sous-commande
    bas = rest[idx + 1 :]               # memes tokens, en minuscules

    if sous_commande == "config" and sous_agent and _config_ecrit_un_alias(bas):
        return _REFUS_CALCULE.format(detail="`git config` ecrit un alias")

    if sous_agent and sous_commande != "stash" and _ecrit_refs_stash(sous_commande, bas):
        return _REFUS_REFS_STASH

    if sous_commande == "checkout":
        # `-f`/`--force` ecrase TOUT l'arbre suivi, la forme la plus
        # destructive de la commande -- ne depend d'aucun chemin cite.
        # Reproduit (revue 2026-09-07) : `git checkout -f master` passait.
        if "--force" in bas or "f" in _flags_courts_groupes(bas):
            return (
                "git checkout -f/--force est bloqué par un hook projet : il ÉCRASE les "
                "modifications non commitées de TOUS les fichiers suivis, pas seulement "
                "d'un chemin. " + _ALTERNATIVE
            )
        # `git checkout … -- <chemin>` : tout ce qui suit `--` est un chemin, la
        # forme la plus explicite et la plus destructive.
        if "--" in bas:
            i = bas.index("--")
            if args[i + 1 :]:
                return (
                    "git checkout -- <chemin> est bloqué par un hook projet : il ÉCRASE "
                    "les modifications non commitées du fichier, sans copie de secours. "
                    + _ALTERNATIVE
                )
        if any(t in _CREATION_DE_BRANCHE for t in bas):
            return None  # création/bascule de branche : rien de l'arbre n'est perdu
        for t in args:
            if not t.startswith("-") and _est_un_chemin_du_depot(t):
                return (
                    f"git checkout <chemin> est bloqué par un hook projet : `{t}` existe "
                    "sur le disque, ses modifications non commitées seraient écrasées. "
                    "Pour changer de branche, le nom ne doit pas être celui d'un fichier "
                    "existant. " + _ALTERNATIVE
                )
        return None

    if sous_commande == "switch":
        # Forme moderne de `checkout <branche>` : `--discard-changes` (et
        # `-f`/`--force`, alias) ecrase l'arbre exactement comme
        # `checkout -f`. Reproduit (revue 2026-09-07) : passait sans ce bloc.
        if any(t in ("--discard-changes", "-f", "--force") for t in bas):
            return (
                "git switch --discard-changes est bloqué par un hook projet : il ÉCRASE "
                "les modifications non commitées, comme git checkout -f. " + _ALTERNATIVE
            )
        return None

    if sous_commande == "restore":
        # `-h`/`--help` n'ecrase rien : uniquement de la lecture.
        if "-h" in bas or "--help" in bas:
            return None
        # `git restore --staged <chemin>` ne touche QUE l'index : il désindexe,
        # il ne détruit rien. Il reste donc autorisé — sauf s'il est cumulé avec
        # `--worktree`, qui lui écrase bien le fichier. `-S`/`-W` sont les
        # formes courtes de git, EN MAJUSCULES (`-s` minuscule est un drapeau
        # different, --source) : les comparer a `bas` (deja en minuscules)
        # les rendait invisibles par construction -- reproduit (revue
        # 2026-09-07) : `git restore -S f.txt` bloquait a tort, `git restore
        # --staged -W f.txt` passait a tort. Compares ici aux tokens
        # ORIGINAUX (`args`), casse preservee.
        a_staged = "--staged" in bas or "-S" in args
        a_worktree = "--worktree" in bas or "-W" in args
        if a_staged and not a_worktree:
            return None
        return (
            "git restore <chemin> est bloqué par un hook projet : il ÉCRASE les "
            "modifications non commitées du fichier. `git restore --staged` (qui ne "
            "touche que l'index) reste autorisé. " + _ALTERNATIVE
        )

    if sous_commande == "clean":
        # `-n`/`--dry-run` ne supprime rien -- y compris cumule avec `-f`
        # dans un SEUL token groupe (`git clean -nfd`, precisement la forme
        # que le message de refus recommande pour lister avant de
        # confirmer) : verifie via _flags_courts_groupes, pas une egalite
        # de token entiere -- `"-n" in bas` ne matchait jamais "-nfd".
        # Reproduit (revue 2026-09-07) : `git clean -nfd` bloquait a tort.
        if "--dry-run" in bas or "n" in _flags_courts_groupes(args):
            return None
        if "--force" in bas or "f" in _flags_courts_groupes(args):
            return (
                "git clean -f est bloqué par un hook projet : il SUPPRIME les fichiers "
                "non suivis, donc tout fichier neuf pas encore ajouté (un test qu'on "
                "vient d'écrire, par exemple). Listez-les d'abord avec `git clean -n`, "
                "puis confirmez avec l'utilisateur."
            )
        return None

    if sous_commande == "stash":
        # Seul le PREMIER token qui n'est pas un drapeau, juste apres
        # `stash`, est la vraie sous-sous-commande -- chercher "drop"/
        # "clear" n'importe ou dans `bas` bloquait a tort un message qui
        # contient ce mot (`git stash push -m "clear le cache"`, un seul
        # token vu shlex). Reproduit (revue 2026-09-07, M2).
        stash_sous_commande = next((t for t in bas if not t.startswith("-")), None)
        if stash_sous_commande in ("drop", "clear"):
            return (
                "git stash drop/clear est bloqué par un hook projet : la remise ainsi "
                "supprimée n'est plus récupérable par aucune commande ordinaire. "
                "Confirmez avec l'utilisateur."
            )
        # Incident repete (2026-11-04, VSCode3, ppt-designer) : un sous-agent a
        # lance `git stash` puis `git stash pop` « pour comparer a HEAD ». Le pop
        # n'est pas une annulation : l'arbre porte le travail non commite
        # d'autres sessions, et la paire le reecrit ou le melange. Un sous-agent
        # lit (`git show HEAD:<chemin>`), il ne range pas l'arbre. Seule une
        # lecture ECRITE EN PREMIER apres `stash` passe : `git stash -m list`
        # est un push dont le message est « list ».
        if sous_agent and (not bas or bas[0] not in ("list", "show")):
            return (
                "git stash est bloqué pour un sous-agent par un hook projet : la paire "
                "stash/pop réécrit l'arbre de travail, qui porte le travail non commité "
                "d'autres sessions. Lisez l'ancien état avec `git show HEAD:<chemin>` ou "
                "copiez le fichier sous C:/tmp/, et rendez la main à la session principale "
                "si un stash semble nécessaire."
            )
        return None

    if sous_commande == "rm":
        # `git rm -f <chemin>` supprime le fichier du disque ET de l'index,
        # y compris ses modifications non commitees, sans copie de secours
        # -- meme classe que `clean -f`, jamais couverte (revue 2026-09-07,
        # M3). Sans -f, git refuse deja de lui-meme un fichier modifie.
        if "--force" in bas or "f" in _flags_courts_groupes(args):
            return (
                "git rm -f est bloqué par un hook projet : il SUPPRIME le fichier du "
                "disque ET de l'index, y compris ses modifications non commitées. "
                "Confirmez avec l'utilisateur, ou `git rm --cached` pour ne toucher que "
                "l'index."
            )
        return None

    if sous_commande == "worktree":
        # `git worktree remove --force` supprime un arbre de travail entier
        # -- pas un fichier, un arbre -- y compris tout travail non commite
        # qu'il contient. Classe differente, jamais couverte (revue
        # 2026-09-07, M3).
        sous_sous = next((t for t in bas if not t.startswith("-")), None)
        if sous_sous == "remove" and ("--force" in bas or "f" in _flags_courts_groupes(args)):
            return (
                "git worktree remove --force est bloqué par un hook projet : il SUPPRIME "
                "tout un arbre de travail, y compris son travail non commité. Confirmez "
                "avec l'utilisateur."
            )
        return None

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


def _stdin_ou_refus(delai=15.0):
    """Guard hook: no stdin within the bound is a prudent refusal (fail-closed).

    Exit 2 blocks the tool call and shows stderr to Claude. ``os._exit`` skips
    interpreter shutdown, which can crash (0xC0000005) while the reader thread
    is still blocked — a crash code other than 2 would be a silent fail-open.
    """
    v = _stdin_borne(delai)
    delai = globals().get("_DELAI_S", delai)
    if v is None:
        _refus_prudent(f"stdin non recu en {delai:g} s", "delai", delai)
    return v

def _journal_refus(motif, delai):
    """One JSON line per refusal (review 4, Dana: measure before tuning the
    bound), with the measured wait ``attente_s``; 1 MB then rotation."""
    _ecrire_journal_stdin({"motif": motif, "delai_s": float(delai),
                           "attente_s": globals().get("_ATTENTE_S")})

def _refus_prudent(cause, motif, delai=15.0):
    _os = __import__("os")
    nom = _os.path.splitext(_os.path.basename(__file__))[0]
    try:  # UTF-8 bytes on fd 2: the harness reads UTF-8, a cp1252 dash is mojibake
        _journal_refus(motif, delai)
        _os.write(2, f"{nom}: {cause} — refus prudent, relancer la commande\n".encode())
    finally:
        _os._exit(2)

def _json_ou_refus(delai=15.0):
    """Guard hook: an empty, non-JSON or non-object payload is refused too
    (review 4, Vex) — only a VALID payload reaches the guard's own fail-open."""
    brut = _stdin_ou_refus(delai)
    delai = globals().get("_DELAI_S", delai)
    try:
        if isinstance(brut, bytes):
            brut = brut.decode("utf-8", "replace")
        data = __import__("json").loads(brut)
    except Exception:  # noqa: BLE001
        data = None
    if not isinstance(data, dict):
        _refus_prudent("entree illisible", "illisible", delai)
    return data


# --------------------------------------------------------------------------- #
# Avis NON bloquant : commandes destructrices que ce hook ne refuse pas
# --------------------------------------------------------------------------- #
# Decision utilisateur : ces silences ne doivent plus etre muets, mais on
# n'etend pas la liste de refus. Un avis `additionalContext`, sans
# `permissionDecision`, que le dispatcher fusionne tel quel. Un refus l'emporte
# toujours : l'avis n'est calcule que si rien n'est bloque.

def _fait_log_env(sous, args, bas):
    return (sous in ("log", "show") and "--" in bas
            and any(".env" in t for t in bas[bas.index("--") + 1:])
            and ("-p" in bas or "--patch" in bas or "p" in _flags_courts_groupes(bas)))


_AVIS_TABLE = (
    ("push --delete", lambda sous, args, bas: sous == "push" and "--delete" in bas),
    ("push -d", lambda sous, args, bas: sous == "push"
        and "d" in _flags_courts_groupes(bas)),
    ("push :ref", lambda sous, args, bas: sous == "push"
        and any(t.startswith(":") and len(t) > 1 for t in bas)),
    # `-d -f`, `-df` et `--delete --force` valent `-D` (revue de cloture 2026-10-12).
    ("branch -D", lambda sous, args, bas: sous == "branch"
        and ("D" in _flags_courts_groupes(args)
             or {"d", "f"} <= set(_flags_courts_groupes(args))
             or ("--delete" in bas and "--force" in bas))),
    ("reflog expire", lambda sous, args, bas: sous == "reflog" and "expire" in bas),
    ("update-ref -d", lambda sous, args, bas: sous == "update-ref"
        and ("-d" in bas or "--delete" in bas)),
    ("reset --merge", lambda sous, args, bas: sous == "reset" and "--merge" in bas),
    ("log -p -- .env", _fait_log_env),
)


def _avis_segment(segment: str):
    try:
        tokens = shlex.split(segment, posix=True)
    except ValueError:
        return None
    start = 0
    while start < len(tokens) and re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", tokens[start]):
        start += 1
    if start >= len(tokens) or _nom_binaire(tokens[start]) != "git":
        return None
    reste = tokens[start + 1:]
    bas_tout = [t.lower() for t in reste]
    idx = _sous_commande_index(bas_tout)
    if idx is None:
        return None
    sous, args, bas = bas_tout[idx], reste[idx + 1:], bas_tout[idx + 1:]
    for forme, fait in _AVIS_TABLE:
        if fait(sous, args, bas):
            return forme
    return None


def _avis(cmd: str):
    """One-line French notice for an uncovered destructive form, else None."""
    try:
        for seg in _segments(_normaliser(cmd)):
            forme = _avis_segment(seg)
            if forme:
                return (f"Ce hook ne couvre pas cette commande ({forme}) : "
                        "verifiez la cible avant de l'executer.")
    except Exception:  # noqa: BLE001 - a notice must never break the guard
        return None
    return None


def main() -> None:
    try:
        data = _json_ou_refus()
    except Exception:
        return
    entree = data.get("tool_input")
    if entree is None:
        entree = {}
    if not isinstance(entree, dict):
        _refus_prudent("tool_input n'est pas un objet", "payload-malforme")
    cmd = entree.get("command", "")
    if not isinstance(cmd, str):
        # number, list, None, dict...: used to crash (exit 1 = NOT blocked).
        _refus_prudent("command n'est pas une chaine", "payload-malforme")
    cwd = data.get("cwd")
    _CWD[0] = cwd if isinstance(cwd, str) and cwd else None
    sous_agent = _contexte_sous_agent(data)
    brut = cmd
    _BRUT[0] = brut
    cmd = _strip_heredocs(cmd)

    blocked = _analyser(cmd, sous_agent=sous_agent)
    if not blocked and sous_agent:
        blocked = _interpreteur_stash(brut)

    if blocked:
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": blocked,
            }
        }))
        return
    avis = _avis(cmd)
    if avis:
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "additionalContext": avis,
            }
        }))


if __name__ == "__main__":
    main()
