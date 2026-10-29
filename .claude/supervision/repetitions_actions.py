"""Detecteur LECTURE SEULE : actions agentiques repetees -> « candidates a un script 0 token ».

Decision utilisateur du 2026-10-24 (N=3) : une meme action vue dans >= 3 sessions
DISTINCTES sur 30 jours est seulement MARQUEE candidate. Creer le script reste un
arbitrage (R4) : ce module ne cree, n'ecrit ni ne lance rien.

Source : usage.jsonl (etage 1), lu par la FIN (bornee). Seules les invocations Agent/Skill
y sont journalisees ; les commandes Bash viennent de la source 2 ci-dessous.
Signature = outil | type d'agent ou skill | 3 premiers mots utiles de la description,
chiffres/ids/chemins retires. Exclus : git/ls/cat/grep nus, scripts deja versionnes,
reprises (retry), et les boucles (comptees par session distincte, pas par appel).
Aucun hook : appele par point_du_jour (fail-open).
Source 2 (gmah-collecte-flotte) : ../orchestration/gravite/collecte.jsonl, signatures Bash
deja normalisees par le hook gmah_collecte (jamais de commande brute), meme regle N=3.
Chaque source est optionnelle : absente ou illisible, elle ne contribue rien.
"""
import datetime as dt
import json
import os
import re
import unicodedata

N_SESSIONS = 3
FENETRE_JOURS = 30
OCTETS_LUS = 1_500_000
_NUS = {"git", "ls", "cat", "grep", "dir", "echo", "head", "tail", "pwd"}
_REPRISE = re.compile(r"\b(retry|reprise|relance|rerun|nouvel essai|re-?essai)\b")
_BRUIT = re.compile(r"[a-z]:/\S*|\S*[/\\]\S*|\b[0-9a-f]{7,}\b|\d+")
_MOTS_VIDES = {"de", "du", "la", "le", "les", "des", "un", "une", "et", "pour", "a", "en"}


def _ascii(t):
    return unicodedata.normalize("NFKD", t or "").encode("ascii", "ignore").decode().lower()


def signature(evt):
    """(signature, mots) d'une invocation, ou None si exclue/inexploitable."""
    desc = _BRUIT.sub(" ", _ascii(str(evt.get("description") or "")))
    mots = [m for m in re.findall(r"[a-z_]+", desc) if m not in _MOTS_VIDES]
    if not mots or mots[0] in _NUS or _REPRISE.search(desc):
        return None
    genre = evt.get("skill") or evt.get("subagent_type") or ""
    return f"{evt.get('tool')}|{genre}|{' '.join(mots[:3])}", mots


def _lignes_bornees(chemin):
    if not os.path.isfile(chemin):
        return
    with open(chemin, "rb") as fh:
        fh.seek(0, os.SEEK_END)
        taille = fh.tell()
        fh.seek(max(0, taille - OCTETS_LUS))
        brut = fh.read().decode("utf-8", "replace")
    for i, ligne in enumerate(brut.splitlines()):
        if i == 0 and taille > OCTETS_LUS:
            continue   # premiere ligne probablement coupee par la borne
        try:
            e = json.loads(ligne)
        except ValueError:
            continue
        if isinstance(e, dict):
            yield e


def _evenements(repertoire):
    for e in _lignes_bornees(os.path.join(repertoire, "usage.jsonl")):
        if e.get("tool") in ("Agent", "Skill") and e.get("session_id"):
            yield e


def signature_bash(evt):
    """(signature, mots) d'une ligne Bash de collecte.jsonl, ou None si exclue."""
    sig = evt.get("bash_signature")
    if not isinstance(sig, str) or not sig.strip():
        return None
    mots = re.findall(r"[a-z_]+", _ascii(sig))
    if not mots or (mots[0] in _NUS and len(sig.split()) <= 2):
        return None
    return f"Bash|{sig.strip()}", mots


def _evenements_collecte(repertoire):
    chemin = os.path.join(os.path.dirname(repertoire), "orchestration", "gravite", "collecte.jsonl")
    for e in _lignes_bornees(chemin):
        if e.get("tool") == "Bash" and e.get("session_id"):
            yield e


def candidats(repertoire, maintenant=None, n=N_SESSIONS, fenetre_jours=FENETRE_JOURS,
              scripts_connus=None):
    """Liste triee [{signature, sessions, exemple}] des actions vues dans >= n sessions."""
    maintenant = maintenant or dt.datetime.now(dt.UTC)
    debut = maintenant - dt.timedelta(days=fenetre_jours)
    connus = {_ascii(s) for s in (scripts_connus or ())}
    vues = {}
    sources = [(e, signature) for e in _evenements(repertoire)]
    sources += [(e, signature_bash) for e in _evenements_collecte(repertoire)]
    for e, signer in sources:
        try:
            ts = dt.datetime.fromisoformat(e["ts"])
            if ts.tzinfo is None:
                ts = ts.replace(tzinfo=dt.UTC)
        except (KeyError, ValueError, TypeError):
            continue
        if ts < debut or ts > maintenant:
            continue
        sig = signer(e)
        if sig is None or connus.intersection(sig[1]):
            continue
        exemple = e.get("description") or e.get("bash_signature")
        vues.setdefault(sig[0], (set(), exemple))[0].add(e["session_id"])
    out = [{"signature": s, "sessions": len(v[0]), "exemple": v[1]}
           for s, v in vues.items() if len(v[0]) >= n]
    return sorted(out, key=lambda c: (-c["sessions"], c["signature"]))


def scripts_versionnes(racine):
    """Noms (sans .py) des scripts deja versionnes sous scripts/ et .claude/."""
    noms = set()
    for base in ("scripts", ".claude"):
        for _, _, fs in os.walk(os.path.join(racine, base)):
            noms.update(f[:-3] for f in fs if f.endswith(".py"))
    return noms


def ligne_candidats(repertoire, maintenant=None, scripts_connus=None):
    """Une ligne ASCII pour le point du jour, ou None. Fail-open : toute erreur -> None."""
    try:
        c = candidats(repertoire, maintenant=maintenant, scripts_connus=scripts_connus)
        if not c:
            return None
        noms = ", ".join(f"{x['exemple']!s:.40} ({x['sessions']} sessions)" for x in c[:2])
        return _ascii(f"{len(c)} action(s) agentique(s) repetee(s) : candidate(s) a un script "
                      f"0 token -- {noms} -- creation = votre arbitrage (jamais automatique)")
    except Exception:  # noqa: BLE001
        return None
