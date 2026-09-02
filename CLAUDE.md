# VSCode3

Cadrage BMAD IAP : le livrable est un deck de synthèse (`docs/cadrage-ppt/`,
42 slides sur le vrai template OCTO) — l'historique de ses versions vit dans
`git log docs/cadrage-ppt/`, pas ici.

## Commandes

- Régénérer le deck : `python generate_deck.py` depuis `docs/cadrage-ppt/`.
- Après toute modif du générateur : `python test_generate_deck.py` **en plus** du
  rendu réel relu à l'œil — le test valide le cadrage géométrique, pas la qualité
  d'une photo.
- Scripts superviseur/orchestrateur : `py -m pytest tests/test_agent_*.py`
  (sur Windows, `--basetemp` sur un dossier neuf : le nettoyage du symlink
  `pytest-current` plante en teardown sinon, sans que ce soit un échec).
- Un seul test : `py -m pytest tests/test_agent_supervision.py::test_scan_counts_and_generates_page_and_index`.
- Couverture : `py -m pytest tests/ --cov=docs/cadrage-ppt` (`requirements-dev.txt`).
  Aucun seuil imposé — on mesure d'abord.
- Linter : `py -m ruff check .` (baseline F/I/UP/B dans `pyproject.toml`).
  **Jamais `--fix` en aveugle** : sur VSCode2 il a supprimé un ré-export et cassé
  un import.

## Claude Code — configuration du projet

- `.claude/settings.json` (versionné) : garde-fou git destructif, rappel de vérif
  réelle avant commit (le hook `.claude/hooks/warn_verif_before_commit.py` est
  générique — SOURCE publiée par le hub dans le kit agentic — et lit le canal de
  CE projet dans `.claude/warn_verif_before_commit.json` ; adapter ce JSON, pas
  le hook, depuis le 2026-09-02), gate orchestrateur, scan supervision en
  SessionStart, deny rules secrets.
- `.claude/skills/` : orchestrateur (compose et exécute les plans multi-étapes),
  superviseur (diagnostic étage 2), revue-increment (definition of done),
  veille-agentic (état de l'art), audit-technique.
- `.claude/agents/` : les sous-agents porteurs que l'orchestrateur dispatche.
- `.claude/supervision/` + `.claude/orchestration/` : dispositif de supervision.
  Journal des orchestrations : `log_run.py` (`--solde` pour requalifier un run en
  attente). Arbitrages humains : `arbitrages.json`.

Le dispositif vient du hub de supervision : **corriger là-bas puis régénérer
l'export**, jamais localement — les copies locales divergent (leçon P1).

## Règles de travail

- Propose → arbitre → applique : aucun correctif auto-appliqué sans arbitrage humain.
- Jamais `succes` au journal sur un livrable que l'utilisateur doit encore valider.
- Tout chiffre écrit s'appuie sur la commande qui l'a produit.
