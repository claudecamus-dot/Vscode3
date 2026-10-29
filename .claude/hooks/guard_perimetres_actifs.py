"""PreToolUse (Agent) — verrou de perimetre d'ecriture entre agents EN VOL (story 14.14).

Motif : rien n'empechait deux agents d'ecrire le meme fichier en meme temps ;
`coalition_planner.py` serialise les perimetres declares au moment du PLAN, pas
pendant l'execution. Ce hook tient un registre des perimetres DECLARES par les
agents ecrivants en vol et refuse un second ecrivain dont le perimetre chevauche.

Contrat :
  - le prompt d'un agent ecrivant porte une ligne `PERIMETRE ECRIT: a, b` (chemins
    relatifs, separes par virgule ou point-virgule) ou une liste de lignes `- chemin`
    juste dessous. `PERIMETRE ECRIT: aucun` = agent en lecture seule : passe sans bruit ;
  - chevauchement = meme chemin ou prefixe de repertoire (dans un sens ou l'autre),
    apres la normalisation de `coalition_planner._norm` (copiee ici pour rester
    exportable ; un test verifie l'equivalence) -> deny, exit 0 ;
  - sans declaration : on laisse passer ET on avertit (jamais de blocage d'un agent
    de lecture) ;
  - liberation : `liberer_perimetres.py` (SubagentStop, script a part, fail-open) retire les entrees expirees et la plus
    ancienne entree de la session ; sinon l'entree expire apres le TTL
    (`GUARD_PERIMETRES_TTL_S`, defaut 3600 s). Registre : `GUARD_PERIMETRES_REGISTRE`
    ou `../orchestration/perimetres_actifs.json`.

Limites HONNETES : le hook controle des perimetres DECLARES, pas les ecritures reelles
(un agent peut ecrire hors de sa declaration, ou mentir) ; la liberation par
SubagentStop est heuristique (le payload ne dit pas quel agent s'arrete : on retire
la plus ancienne entree de la session) et le TTL est le filet ; si une autre garde de
la chaine refuse l'appel apres l'enregistrement, l'entree reste jusqu'au TTL ; une
declaration non normalisable est ignoree avec avertissement. Fail-open integral :
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


def chevauche(a, b):
    return a == b or a.startswith(b + "/") or b.startswith(a + "/")


def declaration(texte):
    """(None, []) sans declaration ; ([], []) si `aucun` ; sinon (chemins normalises, ignores)."""
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
        jetons += [j.strip().strip("`'\"") for j in re.split(r"[;,]", morceau)]
    jetons = [j for j in jetons if j]
    if not jetons or (len(jetons) == 1 and jetons[0].casefold() in ("aucun", "aucune", "none")):
        return [], []
    ok, ignores = [], []
    for j in jetons[:MAX_CHEMINS]:
        try:
            ok.append(_norm(j))
        except _Refuse:
            ignores.append(j)
    return ok, ignores


def _maintenant():
    return datetime.datetime.now(datetime.timezone.utc)


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


def _ecrire(chemin, entrees):
    tmp = chemin + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump({"agents": entrees}, fh, ensure_ascii=True, indent=1)
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


def decider(data, chemin, now=None):
    """-> ('deny'|'warn'|'allow', texte). Enregistre le perimetre si accepte."""
    now = now or _maintenant()
    entree = data.get("tool_input")
    if not isinstance(entree, dict):
        return "allow", ""
    prompt = entree.get("prompt") if isinstance(entree.get("prompt"), str) else ""
    chemins, ignores = declaration(prompt)
    if chemins is None:
        return "warn", ("PERIMETRE ECRIT: absent du prompt - perimetre non verrouille. Si cet "
                        "agent ecrit des fichiers, ajouter `PERIMETRE ECRIT: chemin1, chemin2` "
                        "(ou `aucun` en lecture seule).")
    avert = (" Chemins ignores (non normalisables): " + ", ".join(ignores) + ".") if ignores else ""
    if not chemins:
        return ("warn", avert.strip()) if avert else ("allow", "")
    with _Verrou(chemin):
        vivants = _vivants(_lire(chemin), now)
        for e in vivants:
            for a in chemins:
                for b in e.get("paths", []):
                    if isinstance(b, str) and chevauche(a, b):
                        return "deny", (
                            f"Perimetre d'ecriture deja tenu par un agent en vol "
                            f"({str(e.get('description', '?'))[:80]!r}, depuis {e.get('start_utc')}) : "
                            f"`{a}` chevauche `{b}`. Un seul ecrivain par perimetre : attendre sa "
                            f"fin (SubagentStop) ou le TTL, ou reduire/serialiser les perimetres.")
        vivants.append({
            "description": str(entree.get("description", ""))[:120],
            "session_id": str(data.get("session_id", "")),
            "start_utc": now.isoformat(timespec="seconds"),
            "expire_utc": (now + datetime.timedelta(seconds=_ttl())).isoformat(timespec="seconds"),
            "paths": chemins})
        try:
            _ecrire(chemin, vivants)
        except OSError:
            return "warn", "registre des perimetres non ecrit - perimetre non verrouille." + avert
    return ("warn", avert.strip()) if avert else ("allow", "")


def liberer(data, chemin, now=None):
    now = now or _maintenant()
    with _Verrou(chemin):
        vivants = _vivants(_lire(chemin), now)
        sid = str(data.get("session_id", "")) if isinstance(data, dict) else ""
        for e in vivants:  # ordre d'ajout = du plus ancien au plus recent
            if sid and e.get("session_id") == sid:
                vivants.remove(e)
                break
        if os.path.exists(chemin) or vivants:
            _ecrire(chemin, vivants)


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
