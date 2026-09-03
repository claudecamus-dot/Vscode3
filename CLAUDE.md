# VSCode3

Cadrage BMAD IAP : le livrable est un deck de synthèse (`docs/cadrage-ppt/`,
46 slides sur le vrai template OCTO) — l'historique de ses versions vit dans
`git log docs/cadrage-ppt/`, pas ici.

## Commandes

- Régénérer le deck : `python generate_deck.py` depuis `docs/cadrage-ppt/`.
- Après toute modif du générateur : `python test_generate_deck.py` **en plus** du
  rendu réel relu à l'œil — le test valide le cadrage géométrique, pas la qualité
  d'une photo.
- Suite complète : `py -m pytest tests/` (90 tests — sur Windows, `--basetemp`
  sur un dossier neuf : le nettoyage du symlink `pytest-current` plante en
  teardown sinon, sans que ce soit un échec). **Pas** `tests/test_agent_*.py` :
  ce glob exclut `tests/test_generate_deck_garde.py` — un renommage l'a cassé
  et poussé sur `main` sans que ce filtre ne le détecte (2026-09-03).
- Un seul test : `py -m pytest tests/test_agent_supervision.py::test_scan_counts_and_generates_page_and_index`.
- Couverture : `py -m pytest tests/ --cov=docs/cadrage-ppt` mesure le
  dispositif de supervision (appelé en subprocess depuis `tests/`), **pas**
  `generate_deck.py` (exercé par `test_generate_deck.py`, un script autonome
  hors pytest) — les deux affichés ensemble sous-comptent massivement le
  second (7 % mesuré, écart trouvé le 2026-09-03). Mesurer le deck
  séparément : `py -m coverage run docs/cadrage-ppt/test_generate_deck.py`
  puis `py -m coverage report docs/cadrage-ppt/generate_deck.py` (~95 % au
  2026-09-03 — pas de chiffre figé ici, le fichier change vite : rejouer la
  commande plutôt que citer ce nombre). Aucun seuil imposé — on mesure d'abord.
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

## Optimisation tokens (cf. `docs/vscode1-export/optimisation-tokens.md`)

- Ne pas re-dériver ce que le wiki (`docs/wiki/`) ou une mémoire documente déjà.
- Lire des portions ciblées (Grep/Glob puis Read offset/limit), pas des fichiers entiers.
- Sous-agent pour toute sortie volumineuse ; sinon pas de sous-agent par défaut.
- Documenter une décision actée plutôt que la rejouer.

## Règles de travail

- Propose → arbitre → applique : aucun correctif auto-appliqué sans arbitrage humain.
- Jamais `succes` au journal sur un livrable que l'utilisateur doit encore valider.
- Tout chiffre écrit s'appuie sur la commande qui l'a produit.
