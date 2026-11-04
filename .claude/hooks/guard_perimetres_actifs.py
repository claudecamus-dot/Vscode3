"""PreToolUse (Agent) — verrou de perimetre d'ecriture entre agents EN VOL (story 14.14).

Motif : rien n'empechait deux agents d'ecrire le meme fichier en meme temps ;
`coalition_planner.py` serialise les perimetres declares au moment du PLAN, pas
pendant l'execution. Ce hook tient un registre des perimetres DECLARES par les
agents ecrivants en vol et refuse un second ecrivain dont le perimetre chevauche.

Contrat :
  - le prompt d'un agent ecrivant porte une ligne `PERIMETRE ECRIT: a, b` (chemins
    relatifs ou absolus, separes par virgule ou point-virgule ; des absolus peuvent aussi
    l'etre par des blancs, voir `_decouper_blancs`) ou une liste de lignes
    `- chemin` juste dessous. `PERIMETRE ECRIT: aucun` = agent en lecture seule : passe sans bruit ;
  - chaque chemin recoit une CLE CANONIQUE (`cle`, story 14.22) : absolue, `..` resolu
    lexicalement, `/`, NFC, casefold sous Windows. Un chemin relatif garde tous les refus de
    `_norm` (copie de `coalition_planner._norm`, inchangee, un test verifie l'equivalence)
    puis est resolu contre le `cwd` de l'entree du hook (repli os.getcwd() SEULEMENT si le
    champ est absent ; present mais invalide -> les relatifs sont ignores). Refuses (donc
    ignores avec avertissement) : `:` hors de `X:` en position 1, `C:x`, `/x` sans lecteur
    sous Windows, UNC `//serveur/partage`, `~` (nom court 8.3), racine seule, noms reserves ;
  - chevauchement = meme cle ou prefixe de SEGMENT (dans un sens ou l'autre) -> deny,
    exit 0 ; deux worktrees differents ne se chevauchent donc jamais. Les anciennes entrees
    a cle relative ne chevauchent plus rien et expirent avec leur TTL (pas de migration) ;
  - sans declaration : on laisse passer ET on avertit (jamais de blocage d'un agent
    de lecture) ;
  - liberation : `liberer_perimetres.py` (SubagentStop, script a part, fail-open) retire les
    entrees expirees et l'entree DE L'AGENT QUI S'ARRETE (story 14.22 AC.2, voie (b) arbitree
    le 2026-11-04) : premier message `user` de son `agent_transcript_path` (lecture bornee a
    TRANSCRIPT_CAP octets), declaration recalculee par le meme parseur et la meme cle, entree
    vivante de la meme session au meme ensemble de cles (la plus ancienne des egales).
    Transcript lisible mais rien a liberer (`aucun`, pas de ligne, aucune entree vivante
    appariee) -> rien n'est libere. Transcript ILLISIBLE -> repli sur la plus ancienne
    entree de la session. Lecture du transcript AVANT le verrou ; motif journalise dans
    `liberations` du registre (motif seul, jamais de contenu) ; sinon l'entree expire apres le TTL
    (`GUARD_PERIMETRES_TTL_S`, defaut 3600 s). Registre : `GUARD_PERIMETRES_REGISTRE`
    ou `../orchestration/perimetres_actifs.json`.

  - relance (story 14.22, D3 amende F2) : un appel de la MEME session, de MEME description et
    de MEME ensemble de cles qu'une entree vivante n'est pas refuse par elle — cas d'un appel
    refuse par une garde suivante apres l'enregistrement. Il AJOUTE sa propre entree ; aucune
    expiration existante n'est rafraichie (chaque entree garde son TTL). Deux jumeaux de meme
    session tiennent donc deux entrees, et un arret n'en libere qu'une.

Limites HONNETES : le hook controle des perimetres DECLARES, pas les ecritures reelles
(un agent peut ecrire hors de sa declaration, ou mentir) ; la cle est LEXICALE (liens et
jonctions non suivis) ; aucun identifiant n'est commun a PreToolUse:Agent et SubagentStop
(`agent_id` n'apparait qu'au PostToolUse, `tool_response.agentId`) : la liberation passe
donc par le prompt relu dans le transcript ; son REPLI (plus ancienne entree de la session)
reste heuristique et le TTL est le filet ; un transcript LISIBLE sans perimetre verrouillable
(`aucun`, pas de ligne, tous chemins refuses) ne libere RIEN (cet agent n'a jamais enregistre
d'entree ; motif `aucun-perimetre-declare`) ;
une declaration non normalisable est
ignoree avec avertissement. Et encore :
  - casefold Unicode : `ß` et `ss` (ou toute paire que casefold confond) donnent la meme cle
    sous Windows — sur-verrouillage prudent, jamais un trou ;
  - cle lexicale : jonctions, liens symboliques et alias UNC ou 8.3 d'un meme fichier ne
    sont pas rapproches (un alias UNC ou `~` est refuse, donc ignore) ;
  - declaration entierement ignoree -> avertissement seulement, l'appel passe (fail-open, D31) ;
  - hypothese NON verifiee : le `cwd` du hook d'un agent `isolation: worktree` est celui de
    la session, si bien que ses chemins RELATIFS sont cles sous la racine de la session et
    non sous son worktree ;
  - relance avec un ensemble de cles DIFFERENT : toujours refusee par sa propre entree
    jusqu'au TTL (limite documentee, volontairement non elargie) ;
  - absolu contenant des blancs (`_couper`, sans lecture du disque) : `C:/tmp/a.py b/c` est
    pris pour un chemin qui continue (regle b) -> cle fantome entiere, sans avertissement ;
    la regle (c'') verrouille aussi le prefixe avant le premier blanc, qui peut etre un
    vrai voisin (`.../VScode5` a cote de `.../VScode5 - Supervision projets`) : un ecrivain
    sans rapport peut etre refuse a tort — echec prudent, jamais un verrou perdu. Fail-open integral :
entree illisible, registre corrompu ou verrou indisponible -> exit 0 (sauf absence totale
de stdin : refus prudent du regime commun des gardes).
"""
import datetime
import json
import os
import posixpath
import re
import sys
import time
import unicodedata

for _flux, _enc in ((sys.stdin, "utf-8-sig"), (sys.stdout, "utf-8"), (sys.stderr, "utf-8")):
    if hasattr(_flux, "reconfigure"):
        _flux.reconfigure(encoding=_enc)

ICI = os.path.dirname(os.path.abspath(__file__))
TTL_DEFAUT_S = 3600
MAX_CHEMIN_LEN = 260
MAX_CHEMINS = 100
TRANSCRIPT_CAP = 1_000_000   # bytes read at most in the stopping agent's transcript (route b)
JOURNAL_MAX = 50             # release journal entries kept in the registry
MAX_JUMEAUX = 3              # same-call twins kept per (session, description, key set)
RESERVES = {"con", "prn", "aux", "nul", "conin$", "conout$"} | {f"com{i}" for i in range(1, 10)} | {f"lpt{i}" for i in range(1, 10)}
INTERDITS = set('*?<>"|:~')
RE_DECL = re.compile(r"^[ \t]*PERIMETRE[ \t]+ECRIT[ \t]*:[ \t]*(.*)$", re.I | re.M)


class _Refuse(ValueError):
    pass


def _norm(p):
    """Copie de coalition_planner._norm (equivalence verifiee par test)."""
    if type(p) is not str:
        raise _Refuse("path must be a string")
    if len(p) > MAX_CHEMIN_LEN:
        raise _Refuse("path too long")
    if any(ord(c) < 32 or ord(c) == 127 for c in p):
        raise _Refuse("control character")
    if any(c in INTERDITS for c in p):
        raise _Refuse("forbidden character")
    q = unicodedata.normalize("NFC", p.replace("\\", "/"))
    if q.startswith("/"):
        raise _Refuse("absolute path")
    n = posixpath.normpath(q)
    if n in ("", ".") or n == ".." or n.startswith("../"):
        raise _Refuse("empty or escaping path")
    segs = []
    for seg in n.split("/"):
        seg = seg.rstrip(". ")
        if not seg:
            raise _Refuse("empty segment")
        if seg.split(".")[0].rstrip(" ").casefold() in RESERVES:
            raise _Refuse("reserved device name")
        segs.append(seg)
    return "/".join(segs).casefold()


INTERDITS_ABS = INTERDITS - {":", "~"}   # drive colon checked by position; `~` on Windows only


def _canon_abs(q, nt, racine_ok=False):
    """Canonical key of an absolute path `q` (forward slashes, NFC) — story 14.22, D1.

    Windows: `X:/...` only (the colon at position 1); a driveless `/x`, a drive-relative
    `C:x` and a UNC `//server/share` are REFUSED (a UNC or `\\\\?\\` alias of a local file
    cannot be keyed lexically). POSIX: `/...`, no colon. `..` is resolved lexically and
    clamps at the root, like the OS; links/junctions are NOT followed (lexical key: the
    path may not exist yet). On Windows, trailing dots/spaces of a segment are stripped
    and the key is casefolded."""
    if nt:
        if not (len(q) >= 3 and q[0].isascii() and q[0].isalpha() and q[1] == ":" and q[2] == "/"):
            raise _Refuse("absolute path needs a drive (X:/)")
        tete, reste = q[:2].casefold(), q[2:]
    else:
        if not q.startswith("/"):
            raise _Refuse("not an absolute path")
        tete, reste = "", q
    if ":" in reste:
        raise _Refuse("forbidden character")
    if reste.startswith("//"):
        raise _Refuse("UNC or double-slash root")
    n = posixpath.normpath(reste)
    segs = []
    for seg in (n.split("/")[1:] if n != "/" else []):
        if nt:
            seg = seg.rstrip(". ")
        if not seg or seg in (".", ".."):
            raise _Refuse("empty segment")
        if nt and seg.split(".")[0].rstrip(" ").casefold() in RESERVES:  # V6: Windows only
            raise _Refuse("reserved device name")
        segs.append(seg)
    if not segs and not racine_ok:
        raise _Refuse("root path")
    k = unicodedata.normalize("NFC", tete + "/" + "/".join(segs))
    return k.casefold() if nt else k


def _valider(p, nt):
    if type(p) is not str:
        raise _Refuse("path must be a string")
    if len(p) > MAX_CHEMIN_LEN:
        raise _Refuse("path too long")
    if any(ord(c) < 32 or ord(c) == 127 for c in p):
        raise _Refuse("control character")
    if any(c in INTERDITS_ABS for c in p) or (nt and "~" in p):  # V6: `~` (8.3) Windows only
        raise _Refuse("forbidden character")
    return unicodedata.normalize("NFC", p.replace("\\", "/"))


def _est_absolu(q, nt):
    return q.startswith("/") or (nt and q[1:2] == ":")


def _base(cwd, nt):
    """Canonical key of the hook's `cwd`. ABSENT (None) -> os.getcwd(). PRESENT but invalid
    (8.3 `~`, reserved segment, not absolute...) -> its realpath is tried (an existing 8.3
    name expands to its long form); still invalid -> _Refuse, so the relative path is
    ignored with the warning, NEVER resolved against the process cwd (T2 voice 1, F1)."""
    if cwd is None:
        try:
            cwd = os.getcwd()
        except OSError:
            raise _Refuse("no absolute base for a relative path") from None
    candidats = [cwd]
    # realpath of a RELATIVE cwd would resolve it against the process cwd: absolute only
    if isinstance(cwd, str) and _est_absolu(cwd.replace("\\", "/"), nt):
        try:
            candidats.append(os.path.realpath(cwd))
        except (OSError, ValueError):
            pass
    for c in candidats:
        try:
            q = _valider(c, nt)
            if _est_absolu(q, nt):
                return _canon_abs(q, nt, racine_ok=True)
        except _Refuse:
            continue
    raise _Refuse("invalid cwd: no absolute base for a relative path")


def cle(p, cwd=None, nt=None):
    """Canonical key of a declared path (story 14.22, D1): absolute, resolved, `/`, NFC,
    casefolded on Windows. A relative path keeps every refusal of `_norm` (unchanged) and
    is then resolved against `cwd` (the hook input's field, fallback os.getcwd())."""
    nt = (os.name == "nt") if nt is None else nt
    q = _valider(p, nt)
    if _est_absolu(q, nt):
        return _canon_abs(q, nt)
    _norm(p)
    return _canon_abs(_base(cwd, nt).rstrip("/") + "/" + q, nt)


def chevauche(a, b):
    return a == b or a.startswith(b + "/") or b.startswith(a + "/")


RE_DEBUT_ABS = re.compile(r"^[A-Za-z]:[\\/]") if os.name == "nt" else re.compile(r"^/")
RE_COUPE_ABS = (re.compile(r"\s+(?=[`'\"]?[A-Za-z]:[\\/])") if os.name == "nt"
                else re.compile(r"\s+(?=[`'\"]?/)"))


def _decouper_blancs(jeton):
    """Story 14.22: real briefs separate absolute paths with spaces. A token is cut ONLY
    before whitespace that is followed by the start of an absolute path (`X:/`, `X:\\` on
    Windows, `/` on POSIX) — T2 voice 3, V3/V5. A relative path containing spaces
    (`VScode5 - Supervision projets/x`) stays whole, and so does an absolute path followed
    by plain text; `_couper` then decides what an absolute piece with whitespace keys."""
    return [m.strip().strip("`'\"") for m in RE_COUPE_ABS.split(jeton) if m.strip()]


def _couper(j):
    """-> (pieces to key, note for the warning or None) for one token. Never drops a lock to
    avoid a phantom: a phantom key with a warning is the lesser harm (P1 after 730c4cd0).
    Deterministic, no filesystem lookup. For an ABSOLUTE token that still contains
    whitespace (on Windows, trailing dots/spaces of a segment do not count — the OS strips
    them, `C:/tmp/dir. /f.py` is `c:/tmp/dir/f.py`):
      (a) a whitespace followed by "(" -> cut there, the rest goes to the warning;
      (b) the text after the FIRST whitespace contains "/" or "\\" -> the path continues:
          the whole token is the key, no warning (a real path with spaces);
      (c'') otherwise key BOTH the whole token and the prefix before the first whitespace,
          with a warning (`.../VScode5 - Supervision projets` and `.../file.py et rien
          d'autre` cannot be told apart: lock both)."""
    s = re.sub(r"[ .]+(?=[\\/]|$)", "", j) if os.name == "nt" else j
    if not (RE_DEBUT_ABS.match(j) and re.search(r"\s", s)):
        return [j], None
    m = re.search(r"\s+\(", j)
    if m:                                                        # (a)
        return [j[:m.start()]], j[m.start():].strip()
    premier = re.search(r"\s", j)
    if re.search(r"[\\/]", j[premier.end():]):                   # (b)
        return [j], None
    return [j, j[:premier.start()]], f"{j} (verrouille entier ET jusqu'au premier blanc)"  # (c'')


def declaration(texte, cwd=None):
    """(None, []) sans declaration ; ([], []) si `aucun` ; sinon (cles canoniques, ignores)."""
    m = RE_DECL.search(texte or "")
    if not m:
        return None, []
    brut = [m.group(1)]
    for ligne in (texte[m.end():]).split("\n")[1:]:
        s = ligne.strip()
        if s.startswith(("- ", "* ")):
            brut.append(s[2:])
        else:
            break
    jetons = []
    for morceau in brut:
        for j in re.split(r"[;,]", morceau):
            jetons += _decouper_blancs(j.strip().strip("`'\""))
    jetons = [j for j in jetons if j]
    if not jetons or (len(jetons) == 1 and jetons[0].casefold() in ("aucun", "aucune", "none")):
        return [], []
    ok, ignores = [], []
    for j in jetons[:MAX_CHEMINS]:
        morceaux, note = _couper(j)
        if note:
            ignores.append(note)
        for p in morceaux:
            try:
                ok.append(cle(p, cwd))
            except _Refuse:
                ignores.append(p)
    return ok[:MAX_CHEMINS], ignores


def _maintenant():
    return datetime.datetime.now(datetime.UTC)


def _chemin_registre():
    return os.environ.get("GUARD_PERIMETRES_REGISTRE") or os.path.join(
        ICI, "..", "orchestration", "perimetres_actifs.json")


def _ttl():
    try:
        return max(1, int(os.environ.get("GUARD_PERIMETRES_TTL_S", TTL_DEFAUT_S)))
    except ValueError:
        return TTL_DEFAUT_S


def _lire(chemin):
    try:
        with open(chemin, encoding="utf-8") as fh:
            d = json.load(fh)
        e = d.get("agents") if isinstance(d, dict) else None
        return [x for x in e if isinstance(x, dict)] if isinstance(e, list) else []
    except (OSError, ValueError):
        return []


def _vivants(entrees, now):
    out = []
    for e in entrees:
        try:
            if datetime.datetime.fromisoformat(e["expire_utc"]) > now:
                out.append(e)
        except (KeyError, ValueError, TypeError):
            continue
    return out


def _lire_journal(chemin):
    try:
        with open(chemin, encoding="utf-8") as fh:
            d = json.load(fh)
        j = d.get("liberations") if isinstance(d, dict) else None
        return [x for x in j if isinstance(x, dict)] if isinstance(j, list) else []
    except (OSError, ValueError):
        return []


def _ecrire(chemin, entrees, journal=None):
    """Writes the registry; the release journal (`liberations`, last JOURNAL_MAX) is kept
    when not given (a PreToolUse registration must not erase it)."""
    journal = _lire_journal(chemin) if journal is None else journal
    d = {"agents": entrees}
    if journal:
        d["liberations"] = journal[-JOURNAL_MAX:]
    tmp = f"{chemin}.{os.getpid()}.tmp"   # V8: per process, two writers never share it
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(d, fh, ensure_ascii=True, indent=1)
    os.replace(tmp, chemin)


class _Verrou:
    """Verrou de fichier O_EXCL, attente bornee ; indisponible -> on continue sans (fail-open)."""
    def __init__(self, chemin):
        self.chemin, self.pris = chemin + ".lock", False

    def __enter__(self):
        debut = time.time()
        while time.time() - debut < 3:
            try:
                os.close(os.open(self.chemin, os.O_CREAT | os.O_EXCL | os.O_WRONLY))
                self.pris = True
                break
            except FileExistsError:
                try:
                    if time.time() - os.path.getmtime(self.chemin) > 30:
                        os.remove(self.chemin)
                except OSError:
                    pass
                time.sleep(0.05)
            except OSError:
                break
        return self

    def __exit__(self, *a):
        if self.pris:
            try:
                os.remove(self.chemin)
            except OSError:
                pass


def _meme_appel(e, sid, desc, chemins):
    """Story 14.22, D3 amended by T2 voice 1 (F2): a relaunch of the SAME call (same
    session, same description, same canonical path set) is not blocked by that entry — e.g.
    the Agent call was refused by a later hook after this one recorded it. It APPENDS its
    own entry and never refreshes the existing one's expiry (each entry keeps its own TTL,
    and one stop frees one entry). At most MAX_JUMEAUX twins are kept, the oldest being
    replaced (T2 voice 3, V7): the cap BOUNDS the registry (a relaunch loop no longer
    grows it without limit). It does not end the hold: a session that keeps relaunching
    the same call keeps a fresh entry and so keeps its perimeter, as D3 intends; the lock
    lapses one TTL after the last relaunch. Another session, description or path set is
    still denied."""
    p = e.get("paths")
    return (bool(sid) and e.get("session_id") == sid and e.get("description") == desc
            and isinstance(p, list) and set(p) == set(chemins))


def decider(data, chemin, now=None):
    """-> ('deny'|'warn'|'allow', texte). Enregistre le perimetre si accepte."""
    now = now or _maintenant()
    entree = data.get("tool_input")
    if not isinstance(entree, dict):
        return "allow", ""
    prompt = entree.get("prompt") if isinstance(entree.get("prompt"), str) else ""
    chemins, ignores = declaration(prompt, data.get("cwd"))
    if chemins is None:
        return "warn", ("PERIMETRE ECRIT: absent du prompt - perimetre non verrouille. Si cet "
                        "agent ecrit des fichiers, ajouter `PERIMETRE ECRIT: chemin1, chemin2` "
                        "(ou `aucun` en lecture seule).")
    avert = (" Chemins ignores (non normalisables): " + ", ".join(ignores) + ".") if ignores else ""
    if not chemins:
        return ("warn", avert.strip()) if avert else ("allow", "")
    desc = str(entree.get("description", ""))[:120]
    sid = str(data.get("session_id", ""))
    with _Verrou(chemin):
        vivants = _vivants(_lire(chemin), now)
        jumeaux = [e for e in vivants if _meme_appel(e, sid, desc, chemins)]
        for e in vivants:
            if _meme_appel(e, sid, desc, chemins):
                continue   # D3/F2: not blocked by it; this call APPENDS its own entry below
            for a in chemins:
                for b in e.get("paths", []):
                    if isinstance(b, str) and chevauche(a, b):
                        return "deny", (
                            f"Perimetre d'ecriture deja tenu par un agent en vol "
                            f"({str(e.get('description', '?'))[:80]!r}, depuis {e.get('start_utc')}) : "
                            f"`{a}` chevauche `{b}`. Un seul ecrivain par perimetre : attendre sa "
                            f"fin (SubagentStop) ou le TTL, ou reduire/serialiser les perimetres.")
        if len(jumeaux) >= MAX_JUMEAUX:   # V7: a relaunch loop holds at most 3 twins
            vivants.remove(jumeaux[0])     # the oldest twin is replaced
        vivants.append({
            "description": desc,
            "session_id": sid,
            "start_utc": now.isoformat(timespec="seconds"),
            "expire_utc": (now + datetime.timedelta(seconds=_ttl())).isoformat(timespec="seconds"),
            "paths": chemins})
        try:
            _ecrire(chemin, vivants)
        except OSError:
            return "warn", "registre des perimetres non ecrit - perimetre non verrouille." + avert
    return ("warn", avert.strip()) if avert else ("allow", "")


class _Repli(Exception):
    """Route (b) cannot identify the stopping agent: fall back, with this reason."""


class _Rien(Exception):
    """Readable transcript, no lockable declaration (`aucun`, no line, every path refused):
    that agent never registered an entry -> release NOTHING (main's decision 2026-11-04,
    user wording of route b: the fallback is for an UNREADABLE transcript only)."""


def _premier_message_user(chemin_t):
    """(text, cwd) of the FIRST `type: user` entry of the stopping agent's transcript.

    Format verified on one real hub subagent transcript (2026-11-04, first line only):
    `type`, `message.content` (a str; a list of `{type: text, text}` blocks is accepted
    too), `cwd`. Streamed line by line, at most TRANSCRIPT_CAP bytes read in all, stops
    at the first user entry; non-JSON lines are skipped. Nothing else is kept."""
    if not isinstance(chemin_t, str) or not chemin_t:
        raise _Repli("champ agent_transcript_path absent")
    try:
        fh = open(chemin_t, "rb")
    except FileNotFoundError:
        raise _Repli("transcript absent") from None
    except OSError:
        raise _Repli("transcript illisible") from None
    lu = 0
    with fh:
        while True:
            try:
                ligne = fh.readline(TRANSCRIPT_CAP - lu + 1)
            except OSError:
                raise _Repli("transcript illisible") from None
            if not ligne:
                raise _Repli("aucune entree user")
            lu += len(ligne)
            if lu > TRANSCRIPT_CAP:
                raise _Repli("plafond depasse")
            try:
                e = json.loads(ligne)
            except ValueError:
                continue
            if not (isinstance(e, dict) and e.get("type") == "user") or e.get("isMeta") is True:
                continue   # V4: meta entries are not the prompt
            m = e.get("message")
            c = m.get("content") if isinstance(m, dict) else None
            if isinstance(c, list):
                if not c:
                    raise _Repli("entree user vide")
                textes = [b["text"] for b in c if isinstance(b, dict) and isinstance(b.get("text"), str)]
                if not textes:
                    continue   # V4: e.g. a tool_result entry, not the prompt
                c = "\n".join(textes)
            if not isinstance(c, str):
                continue
            if not c.strip():
                raise _Repli("entree user vide")
            return c, e.get("cwd")


def _entree_de_l_agent(data, vivants, sid, lu):
    """Index of the live entry of THIS session whose canonical key set equals the
    declaration recomputed from the stopping agent's first prompt `lu` = (text, cwd),
    oldest of equals. Recomputed against the transcript's `cwd` (the agent's own launch
    cwd) FIRST, then the payload `cwd`. A cwd under which every path is refused moves on
    to the next cwd (V1). Readable transcript but nothing to release -> _Rien: no line or
    `aucun` / nothing lockable under any cwd ("aucun-perimetre-declare"), or a lockable
    declaration with no live entry, e.g. TTL expired ("entree-absente", V2)."""
    texte, cwd_t = lu
    verrouillable = False
    for cwd in [c for c in (cwd_t, data.get("cwd")) if c is not None] or [None]:
        chemins, ignores = declaration(texte, cwd)
        if chemins is None or (not chemins and not ignores):   # no line, or `aucun`
            raise _Rien("aucun-perimetre-declare")
        if not chemins:
            continue   # V1: every path refused under THIS cwd -> try the next one
        verrouillable = True
        for i, e in enumerate(vivants):  # ordre d'ajout = du plus ancien au plus recent
            p = e.get("paths")
            if e.get("session_id") == sid and isinstance(p, list) and set(p) == set(chemins):
                return i
    raise _Rien("entree-absente" if verrouillable else "aucun-perimetre-declare")


def liberer(data, chemin, now=None):
    """SubagentStop: route (b) (story 14.22 AC.2, user arbitration 2026-11-04) releases the
    stopping agent's own entry. Readable transcript but nothing to release -> nothing is
    released; an UNREADABLE (absent, capped, malformed) transcript falls back to the oldest
    entry of the session. Reason journaled (`liberations`, never transcript content).
    The transcript is read BEFORE the registry lock is taken (V8)."""
    now = now or _maintenant()
    data = data if isinstance(data, dict) else {}
    sid = str(data.get("session_id", ""))
    try:
        lu = _premier_message_user(data.get("agent_transcript_path"))
    except _Repli as r:
        lu = r
    except Exception:  # noqa: BLE001 - fail-open (D31)
        lu = _Repli("erreur inattendue")
    with _Verrou(chemin):
        vivants = _vivants(_lire(chemin), now)
        trace = {"ts": now.isoformat(timespec="seconds"), "session_id": sid,
                 "agent_id": str(data.get("agent_id", ""))[:64]}
        try:
            if not sid:
                raise _Repli("session_id absent")
            if isinstance(lu, _Repli):
                raise lu
            del vivants[_entree_de_l_agent(data, vivants, sid, lu)]
            trace.update(mode="transcript", motif="entree appariee")
        except _Rien as r:
            trace.update(mode="rien", motif=str(r))
        except Exception as r:  # noqa: BLE001 - fail-open (D31): every failure falls back
            trace.update(mode="repli", motif=str(r) if isinstance(r, _Repli) else "erreur inattendue")
            for e in vivants:  # comportement d'avant 14.22 : la plus ancienne de la session
                if sid and e.get("session_id") == sid:
                    vivants.remove(e)
                    break
        if os.path.exists(chemin) or vivants:
            _ecrire(chemin, vivants, _lire_journal(chemin) + [trace])


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


class _Fd0:
    """Raw fd 0 reader: a daemon thread blocked in BufferedReader.read crashes the
    interpreter at shutdown (0xC0000005, measured); os.read holds no Python lock."""

    def read(self):
        morceaux = []
        while True:
            b = __import__("os").read(0, 65536)
            if not b:
                return b"".join(morceaux)
            morceaux.append(b)


_FLUX_STDIN = _Fd0()


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


def _sortie(hso):
    print(json.dumps({"hookSpecificOutput": dict(hso, hookEventName="PreToolUse")}))


def main() -> None:
    try:
        brut = _stdin_ou_refus()
        data = json.loads(brut.decode("utf-8", "replace") if isinstance(brut, bytes) else brut)
    except Exception:   # noqa: BLE001 - fail-open
        sys.exit(0)
    try:
        if not isinstance(data, dict):
            sys.exit(0)
        chemin = _chemin_registre()
        if data.get("tool_name") != "Agent":
            sys.exit(0)
        verdict, texte = decider(data, chemin)
        if verdict == "deny":
            _sortie({"permissionDecision": "deny", "permissionDecisionReason": texte})
        elif verdict == "warn":
            _sortie({"additionalContext": texte})
    except SystemExit:
        raise
    except Exception:   # noqa: BLE001 - fail-open
        pass
    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception:   # noqa: BLE001 - dernier filet
        sys.exit(0)
