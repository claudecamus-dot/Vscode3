"""Non-regression pour `.claude/hooks/warn_verif_before_commit.py`.

Ecrit AVANT le correctif du 2026-09-02 (revue de securite du 2026-09-01,
finding « le kit publie embarque les chemins surveilles d'un AUTRE projet »).

Ce fichier est la SOURCE publiee par le hub de supervision dans le kit
agentic installe par cinq depots (export_agentic.GENERIQUE pointe
`~/Documents/VSCode3/.claude/hooks`). Avant correction, `_WATCHED_PREFIXES`
et `_VERIF_BASH` etaient des tuples fixes adaptes a VSCode3
(`docs/cadrage-ppt/`, `pytest`), pendant que le docstring et le message
utilisateur decrivaient encore le canal VSCode1 (`app/**`, `npm test`) —
jamais mis a jour le 2026-07-24. Un depot tiers installant le kit heritait
donc soit d'un garde-fou muet (mauvais perimetre : `docs/cadrage-ppt/`
n'existe pas chez lui), soit, si quelqu'un adaptait les constantes sans
toucher au message, d'un rappel qui pointe vers la mauvaise commande.

Ces tests verrouillent :
(a) un depot sans configuration obtient un declencheur generique non vide ;
(b) le message cite les perimetres et preuves REELS, plus jamais `npm test`
    ni `app/` en dur dans la fonction qui le construit ;
(c) VSCode3 conserve exactement son comportement actuel via sa propre
    configuration (`.claude/warn_verif_before_commit.json`) ;
(d) le fail-open tient sur une configuration illisible ou malformee.
"""
import importlib.util
import inspect
import io
import json
import pathlib
import subprocess
import sys

HOOK = pathlib.Path(__file__).resolve().parents[1] / ".claude" / "hooks" / "warn_verif_before_commit.py"


def _load():
    spec = importlib.util.spec_from_file_location("warn_verif_before_commit", HOOK)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


hook = _load()


# --- (a) repli generique non vide sans configuration -------------------------

def test_defaut_generique_non_vide_sans_configuration(monkeypatch, tmp_path):
    monkeypatch.setattr(hook, "_config_path", lambda: str(tmp_path / "absent.json"))
    watched, verif_bash, verif_skill = hook._load_config()
    assert watched and isinstance(watched, tuple)
    assert verif_bash and isinstance(verif_bash, tuple)
    assert verif_skill and isinstance(verif_skill, tuple)
    assert watched == hook._DEFAULT_WATCHED_PREFIXES
    assert verif_bash == hook._DEFAULT_VERIF_BASH
    assert verif_skill == hook._DEFAULT_VERIF_SKILL


# --- (d) fail-open sur configuration illisible / malformee --------------------

def test_config_json_invalide_fait_repli_silencieux(monkeypatch, tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text("{ceci n'est pas du json valide", encoding="utf-8")
    monkeypatch.setattr(hook, "_config_path", lambda: str(bad))
    watched, verif_bash, verif_skill = hook._load_config()  # ne doit jamais lever
    assert watched == hook._DEFAULT_WATCHED_PREFIXES
    assert verif_bash == hook._DEFAULT_VERIF_BASH
    assert verif_skill == hook._DEFAULT_VERIF_SKILL


def test_config_chemin_est_un_dossier_fait_repli_silencieux(monkeypatch, tmp_path):
    # open() sur un dossier leve (PermissionError/IsADirectoryError selon l'OS) :
    # doit etre absorbe comme n'importe quelle autre erreur, pas propage.
    monkeypatch.setattr(hook, "_config_path", lambda: str(tmp_path))
    watched, verif_bash, verif_skill = hook._load_config()
    assert watched == hook._DEFAULT_WATCHED_PREFIXES


def test_config_liste_non_liste_fait_repli_pour_ce_champ(monkeypatch, tmp_path):
    cfg = tmp_path / "cfg.json"
    cfg.write_text(json.dumps({"watched_prefixes": "docs/"}), encoding="utf-8")  # str, pas list
    monkeypatch.setattr(hook, "_config_path", lambda: str(cfg))
    watched, verif_bash, verif_skill = hook._load_config()
    assert watched == hook._DEFAULT_WATCHED_PREFIXES


def test_config_partielle_complete_uniquement_les_champs_absents(monkeypatch, tmp_path):
    cfg = tmp_path / "cfg.json"
    cfg.write_text(json.dumps({"watched_prefixes": ["backend/"]}), encoding="utf-8")
    monkeypatch.setattr(hook, "_config_path", lambda: str(cfg))
    watched, verif_bash, verif_skill = hook._load_config()
    assert watched == ("backend/",)
    assert verif_bash == hook._DEFAULT_VERIF_BASH
    assert verif_skill == hook._DEFAULT_VERIF_SKILL


# --- (b) message derive des constantes reelles --------------------------------

def test_message_cite_les_perimetres_et_preuves_reels():
    msg = hook._build_warning(
        ("docs/cadrage-ppt/",),
        ("pytest", "test_generate_deck"),
        ("pptx-verify", "revue-increment"),
    )
    assert "docs/cadrage-ppt/" in msg
    assert "pytest" in msg
    assert "test_generate_deck" in msg
    assert "pptx-verify" in msg
    assert "revue-increment" in msg
    assert "npm test" not in msg
    assert "app/" not in msg


def test_message_ne_code_pas_npm_test_ni_app_en_dur():
    """`_build_warning` doit composer son texte a partir des PARAMETRES recus,
    jamais des chaines `npm test` / `app/` figees independamment d'eux."""
    src = inspect.getsource(hook._build_warning)
    assert "npm test" not in src
    assert '"app/"' not in src
    assert "'app/'" not in src


def test_matched_prefixes_ne_retient_que_ce_qui_a_reellement_declenche():
    hit = hook._matched_prefixes(
        ["docs/cadrage-ppt/generate_deck.py", "README.md"],
        ("docs/cadrage-ppt/", "app/"),
    )
    assert hit == ["docs/cadrage-ppt/"]


# --- (c) comportement observable de VSCode3 inchange --------------------------

def test_config_reelle_de_vscode3_reproduit_le_perimetre_historique():
    """La config posee a la racine .claude/ de VSCode3 doit restituer EXACTEMENT
    le perimetre fige avant correction : docs/cadrage-ppt/, pytest/test_generate_deck,
    pptx-verify/revue-increment."""
    assert hook._WATCHED_PREFIXES == ("docs/cadrage-ppt/",)
    assert set(hook._VERIF_BASH) == {"pytest", "-m pytest", "test_generate_deck"}
    assert set(hook._VERIF_SKILL) == {"pptx-verify", "revue-increment"}


def _fake_git_run(staged, unstaged=None, calls=None):
    def fake_run(args, cwd=None, capture_output=None, text=None, timeout=None,
                 encoding=None, errors=None):
        # Ne PAS assert-echouer ici : une exception levee dans ce double serait
        # avalee par le try/except fail-open de `_staged_watched`, et le test
        # verrait un simple silence au lieu du vrai signal. On enregistre les
        # kwargs recus et on les verifie APRES l'appel, hors du perimetre du
        # fail-open.
        if calls is not None:
            calls.append({"encoding": encoding, "errors": errors,
                          "capture_output": capture_output, "text": text})
        out = ""
        if "diff" in args and "--cached" in args:
            out = "\n".join(staged)
        elif "diff" in args:
            out = "\n".join(unstaged or [])
        return subprocess.CompletedProcess(args, 0, stdout=out, stderr="")
    return fake_run


def _run_main(monkeypatch, capsys, tmp_path, staged, transcript_tool_use=None, calls=None):
    monkeypatch.setattr(hook.subprocess, "run", _fake_git_run(staged, calls=calls))
    transcript = tmp_path / "transcript.jsonl"
    if transcript_tool_use is not None:
        transcript.write_text(json.dumps(transcript_tool_use) + "\n", encoding="utf-8")
    else:
        transcript.write_text("", encoding="utf-8")
    payload = {
        "tool_input": {"command": "git commit -m 'x'"},
        "cwd": "C:/VSCode3",
        "transcript_path": str(transcript),
    }
    monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps(payload)))
    hook.main()
    return capsys.readouterr().out


def test_vscode3_declenche_sur_docs_cadrage_ppt_avec_message_correct(monkeypatch, tmp_path, capsys):
    out = _run_main(monkeypatch, capsys, tmp_path, staged=["docs/cadrage-ppt/generate_deck.py"])
    assert out.strip(), "le hook aurait du se declencher"
    data = json.loads(out)
    msg = data["systemMessage"]
    assert "docs/cadrage-ppt/" in msg
    assert "pytest" in msg or "test_generate_deck" in msg
    assert "npm test" not in msg
    assert "app/" not in msg
    assert data["hookSpecificOutput"]["additionalContext"] == msg


def test_staged_watched_appelle_git_avec_encoding_utf8_errors_replace(monkeypatch, tmp_path, capsys):
    """Piege deja paye sur ce depot : sans encoding='utf-8', errors='replace' explicites,
    subprocess.run decode avec l'encodage LOCAL (cp1252 sur ce poste) — un seul nom de
    fichier accentue peut tuer le thread lecteur et transformer le fail-open promis en
    fail-hard (stdout a None, returncode a 0)."""
    calls = []
    _run_main(monkeypatch, capsys, tmp_path,
              staged=["docs/cadrage-ppt/generate_deck.py"], calls=calls)
    assert calls, "git diff --cached aurait du etre appele au moins une fois"
    for kwargs in calls:
        assert kwargs["encoding"] == "utf-8"
        assert kwargs["errors"] == "replace"


def test_vscode3_reste_muet_hors_perimetre(monkeypatch, tmp_path, capsys):
    out = _run_main(monkeypatch, capsys, tmp_path, staged=["README.md"])
    assert out == ""


def test_vscode3_silencieux_si_pytest_a_deja_tourne(monkeypatch, tmp_path, capsys):
    tool_use = {"message": {"content": [
        {"type": "tool_use", "name": "Bash", "input": {"command": "pytest tests/"}}
    ]}}
    out = _run_main(
        monkeypatch, capsys, tmp_path,
        staged=["docs/cadrage-ppt/generate_deck.py"],
        transcript_tool_use=tool_use,
    )
    assert out == ""


def test_vscode3_silencieux_si_pptx_verify_a_tourne(monkeypatch, tmp_path, capsys):
    tool_use = {"message": {"content": [
        {"type": "tool_use", "name": "Skill", "input": {"skill": "pptx-verify"}}
    ]}}
    out = _run_main(
        monkeypatch, capsys, tmp_path,
        staged=["docs/cadrage-ppt/generate_deck.py"],
        transcript_tool_use=tool_use,
    )
    assert out == ""
