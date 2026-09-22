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


# --- (e) `-a`/`--all`, y compris en option courte GROUPEE ---------------------
# Finding robustesse de l'audit VScode5 du 2026-09-02 : `_staged_files` ne
# reconnaissait que les tokens EXACTS "-a"/"--all", alors que `_commit_message`
# savait deja decomposer un groupe court (`-am`, `-amwip`). Un `git commit -am`
# faisait donc rater au garde-fou les fichiers modifies-non-stages du perimetre
# surveille — c'est-a-dire tout le commit dans la forme la plus courante.

def _staged_for(monkeypatch, commande, staged, unstaged):
    monkeypatch.setattr(hook.subprocess, "run", _fake_git_run(staged, unstaged=unstaged))
    flags = hook._git_commit_flags(commande)
    assert flags is not None, f"{commande!r} aurait du etre reconnu comme un git commit"
    return hook._staged_files("C:/VSCode3", flags)


FORMES_ALL = [
    'git commit -am "msg"',
    "git commit -am wip",
    "git commit -amwip",
    "git commit -a -m x",
    "git commit --all -m x",
    "git commit -a",
    "git commit --all",
]


def test_toutes_les_formes_de_all_ajoutent_les_modifs_non_stagees(monkeypatch):
    for commande in FORMES_ALL:
        files = _staged_for(monkeypatch, commande,
                            staged=["README.md"],
                            unstaged=["docs/cadrage-ppt/generate_deck.py"])
        assert files == ["README.md", "docs/cadrage-ppt/generate_deck.py"], (
            f"{commande!r} vaut --all : le fichier surveille modifie-non-stage "
            f"doit entrer dans le perimetre du garde-fou (obtenu {files!r})")


def test_sans_all_le_perimetre_reste_l_index(monkeypatch):
    for commande in ['git commit -m "x"', "git commit -mwip", "git commit"]:
        files = _staged_for(monkeypatch, commande,
                            staged=["README.md"],
                            unstaged=["docs/cadrage-ppt/generate_deck.py"])
        assert files == ["README.md"], f"{commande!r} ne vaut pas --all (obtenu {files!r})"


def test_un_a_dans_le_message_n_est_pas_le_drapeau_all(monkeypatch):
    """`-ma` et `-m -a` portent un message qui commence par « a » / vaut « -a » :
    ce qui suit le `m` d'un groupe court est le message, jamais un drapeau."""
    for commande in ["git commit -ma", "git commit -m -a", 'git commit -m "--all"']:
        files = _staged_for(monkeypatch, commande,
                            staged=["README.md"],
                            unstaged=["docs/cadrage-ppt/generate_deck.py"])
        assert files == ["README.md"], f"{commande!r} ne vaut pas --all (obtenu {files!r})"


def test_declenche_sur_un_fichier_surveille_seulement_modifie_avec_am(monkeypatch, tmp_path, capsys):
    """Bout en bout : `git commit -am` sur un fichier surveille non stage doit
    reveiller le rappel de verif, pas passer en silence."""
    monkeypatch.setattr(hook.subprocess, "run",
                        _fake_git_run([], unstaged=["docs/cadrage-ppt/generate_deck.py"]))
    transcript = tmp_path / "transcript.jsonl"
    transcript.write_text("", encoding="utf-8")
    payload = {
        "tool_input": {"command": 'git commit -am "wip"'},
        "cwd": "C:/VSCode3",
        "transcript_path": str(transcript),
    }
    monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps(payload)))
    hook.main()
    out = capsys.readouterr().out
    assert out.strip(), "le hook aurait du se declencher sur `git commit -am`"
    assert "docs/cadrage-ppt/" in json.loads(out)["systemMessage"]


# --- (f) casse des motifs lus dans la configuration du depot ------------------
# Finding audit VScode5 du 2026-09-19 : la commande analysee est passee en
# `.lower()` (ligne `cmd = (inp.get("command") or "").lower()`), mais les motifs
# lus dans `.claude/warn_verif_before_commit.json` ne l'etaient pas. Un depot qui
# declarait `"verif_bash": ["Pytest"]` obtenait un garde-fou INDESARMABLE : la
# preuve reellement produite n'etait jamais reconnue, le rappel tombait a CHAQUE
# commit — le mode de defaillance qui fait debrancher un garde-fou.

def _config_casse_mixte(monkeypatch, tmp_path):
    cfg = tmp_path / "warn_verif_before_commit.json"
    cfg.write_text(json.dumps({
        "watched_prefixes": ["docs/cadrage-ppt/"],
        "verif_bash": ["Pytest", "-m PyTest"],
        "verif_skill": ["PPTX-Verify"],
    }), encoding="utf-8")
    monkeypatch.setattr(hook, "_config_path", lambda: str(cfg))
    watched, verif_bash, verif_skill = hook._load_config()
    monkeypatch.setattr(hook, "_WATCHED_PREFIXES", watched)
    monkeypatch.setattr(hook, "_VERIF_BASH", verif_bash)
    monkeypatch.setattr(hook, "_VERIF_SKILL", verif_skill)


def test_motif_bash_en_casse_mixte_reconnait_la_verification(monkeypatch, tmp_path, capsys):
    _config_casse_mixte(monkeypatch, tmp_path)
    tool_use = {"message": {"content": [
        {"type": "tool_use", "name": "Bash", "input": {"command": "py -m pytest tests/"}}
    ]}}
    out = _run_main(monkeypatch, capsys, tmp_path,
                    staged=["docs/cadrage-ppt/generate_deck.py"],
                    transcript_tool_use=tool_use)
    assert out == "", (
        "motif 'Pytest' en casse mixte : la verification reellement lancee doit "
        "etre reconnue, sinon le garde-fou est indesarmable\n" + out)


def test_motif_skill_en_casse_mixte_reconnait_la_verification(monkeypatch, tmp_path, capsys):
    _config_casse_mixte(monkeypatch, tmp_path)
    tool_use = {"message": {"content": [
        {"type": "tool_use", "name": "Skill", "input": {"skill": "pptx-verify"}}
    ]}}
    out = _run_main(monkeypatch, capsys, tmp_path,
                    staged=["docs/cadrage-ppt/generate_deck.py"],
                    transcript_tool_use=tool_use)
    assert out == "", "motif de skill en casse mixte non reconnu\n" + out


def test_casse_mixte_le_garde_fou_crie_toujours_sans_verification(monkeypatch, tmp_path, capsys):
    """Contre-epreuve : la normalisation de casse ne doit pas neutraliser la garde.
    Sans aucune preuve dans le transcript, elle DOIT crier."""
    _config_casse_mixte(monkeypatch, tmp_path)
    out = _run_main(monkeypatch, capsys, tmp_path,
                    staged=["docs/cadrage-ppt/generate_deck.py"])
    assert out.strip(), "sans verification, le garde-fou doit crier"
    assert "docs/cadrage-ppt/" in json.loads(out)["systemMessage"]


# --- memoisation de _read_config_dict (finding risque_technique VScode5 2026-09-19) --

def test_read_config_dict_ouvre_le_fichier_une_seule_fois(monkeypatch, tmp_path):
    """_load_config, _load_extra_config et _load_gardes_config appellent toutes
    _read_config_dict : avant memoisation, le fichier etait rouvert trois fois
    pour un contenu identique. Compte les ouvertures reelles via un wrapper
    autour de `open` builtin, cible sur ce seul chemin de fichier."""
    hook._CONFIG_DICT_CACHE.clear()
    cfg = tmp_path / "cfg.json"
    cfg.write_text(json.dumps({"watched_prefixes": ["backend/"]}), encoding="utf-8")
    monkeypatch.setattr(hook, "_config_path", lambda: str(cfg))

    import builtins
    ouvertures = []
    reel_open = builtins.open

    def _open_compte(*args, **kwargs):
        if args and str(args[0]) == str(cfg):
            ouvertures.append(args[0])
        return reel_open(*args, **kwargs)

    monkeypatch.setattr(hook, "open", _open_compte, raising=False)

    hook._load_config()
    hook._load_extra_config()
    hook._load_gardes_config()

    assert len(ouvertures) == 1, (
        f"_read_config_dict a rouvert le fichier {len(ouvertures)} fois "
        "au lieu d'une seule (cache par chemin attendu)")
