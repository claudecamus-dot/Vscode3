# Catalogue des agents — routage orchestrateur

> Utilisé par la skill `agent-orchestrator` pour composer ses plans. Descriptions et
> recommandations maintenues à la main ; les **statuts d'usage vivants** (invocations,
> dates, jamais-utilisés) seront dans `routing-hints.json` (généré à chaque session par le
> scan superviseur, avec les stats plan-vs-réel de `runs.jsonl`) et, en version lisible,
> dans `docs/wiki/technical/agents-supervision.md` — toujours les vérifier avant de router
> vers un agent « jamais utilisé ». Statuts ci-dessous : instantané du 2026-07-21, **install
> initiale** — aucune mesure réelle n'existe encore (premier `scan_transcripts.py` à lancer).
> Les décisions humaines qui closent un constat d'usage (skill conservée malgré
> zéro invocation, tri exécuté) seront dans `.claude/supervision/arbitrages.json`.
> Si **aucune entrée ne couvre le besoin** : inventaire git présents + supprimés via
> `py .claude/orchestration/git_agents_inventory.py`, puis proposition de
> restauration/évolution/création (procédure dans la skill, étape 2).
> Conception : `docs/reflexions/agent-orchestrateur.md` (portée depuis un projet frère,
> VSCode2 — le rationale et les décisions y sont pris dans ce contexte d'origine).

## Skills projet

| Skill | Quand l'utiliser | Mode typique | Modèle | Statut |
| --- | --- | --- | --- | --- |
| `revue-increment` | Definition-of-done : fin d'incrément, avant commit | Synchrone, étape terminale obligatoire des plans de dev | (session) | Pas encore mesuré |
| `pptx-framed-image` | Remplir les cadres photo d'un template PPT (round2DiagRect) — étape conditionnelle du playbook `export-ppt-verifie` | Synchrone | (session) | Pas encore mesuré |
| `slide-text-polish` | Lint de la qualité rédactionnelle des slides — étape conditionnelle du playbook `export-ppt-verifie` | Synchrone | (session) | Pas encore mesuré |
| `agent-orchestrator` | Point d'entrée des demandes multi-étapes/multi-agents (routé par le hook UserPromptSubmit) | Synchrone | (session) | Pas encore mesuré |
| `agent-supervisor` | Diagnostic qualitatif des agents (étage 2) — depuis `revue-increment` ou sur signal SessionStart | Synchrone, ≤ 1×/14 j | (session) | Pas encore mesuré |

## Agents projet

| Agent | Quand l'utiliser | Mode typique | Modèle | Statut |
| --- | --- | --- | --- | --- |
| `ppt-designer` | Génération/amélioration du deck `docs/cadrage-ppt/` — jugement visuel (géométrie, mise en page, vérif par rendu réel) | Synchrone (colonne vertébrale du playbook `export-ppt-verifie`) | hérite du thread principal (pas de bascule — jugement visuel, pas un rapport mécanique) | Pas encore mesuré |

## Skills globaux clés

| Skill | Quand l'utiliser | Mode typique | Modèle | Statut |
| --- | --- | --- | --- | --- |
| `roadmap-keeper` | Mettre à jour/rendre la roadmap (`.roadmap/roadmap.json`) | Synchrone | (session) | Pas encore mesuré |
| `pptx-deck` / `pptx-verify` | Aide de génération PPT (`docs/cadrage-ppt/pptx_deck.py`) / vérification en rendu réel — colonne vertébrale du playbook `export-ppt-verifie` | Synchrone, toujours en paire | (session) | Pas encore mesuré |
| `restitution-deck-design` | Deck techniquement correct (géométrie OK) mais visuellement pauvre — étape conditionnelle du playbook `export-ppt-verifie` | Synchrone | (session) | Pas encore mesuré |
| `dataviz` | Tout graphique/chart/dashboard, dans un artifact ou un deck | Synchrone | (session) | Pas encore mesuré |
| `code-review` / `verify` / `simplify` | Revue du diff / vérification bout-en-bout / nettoyage | Synchrone, fin de plan de dev | (session) | Builtins |

## Sous-agents (seuls à accepter un choix de modèle)

| Sous-agent | Quand l'utiliser | Mode typique | Modèle conseillé | Statut |
| --- | --- | --- | --- | --- |
| `Explore` | Recherche large en lecture seule, conclusion sans les dumps | Parallèle (fan-out ≤4) ou async | Haiku/Sonnet (mécanique/standard) | Pas encore mesuré |
| `Plan` | Concevoir une stratégie d'implémentation | Synchrone | Opus/Fable (structurant) | Pas encore mesuré |
| `general-purpose` | Tâche multi-étapes déléguée, sortie volumineuse | Async ou synchrone | Sonnet ; Opus/Fable si structurant | Pas encore mesuré |
| `claude-code-guide` | Questions sur Claude Code / SDK / API | Synchrone | (défaut) | Pas encore mesuré |

## Familles sous condition

| Famille | Règle de routage |
| --- | --- |
| **BMAD (~46 skills `bmad-*`, install 2026-07-16, tri jamais exécuté ici)** | Contrairement à VSCode2 (39 skills après tri), aucun tri n'a encore été arbitré sur ce dépôt — ne pas présumer qu'une skill BMAD est morte avant d'avoir des données réelles. Router uniquement sur demande explicite de l'utilisateur, en passant par `bmad-help`. |

> Angle mort de mesure (hérité de la conception d'origine) : les sous-skills invoquées par
> un sous-agent via un prompt en langage naturel (pattern utilisé par `bmad-code-review`
> pour lancer `bmad-review-adversarial-general`/`bmad-review-edge-case-hunter`)
> n'apparaissent pas dans `state.json`/`routing-hints.json` — seules les invocations
> directes de la session principale sont trackées. Une absence de trace sur ces
> sous-skills ne signifie donc pas absence d'exécution : ne pas les qualifier `agent-mort`
> sur cette seule base.

## Playbooks

Workflows récurrents pré-composés — la skill cherche un playbook matchant **avant** de
composer à vide. Format : `.claude/orchestration/playbooks/FORMAT.md`.

| Playbook | Pour | Source | Statut |
| --- | --- | --- | --- |
| `dev-verifie` | Implémentation/correction (scripts, hooks, skills) : tests + vérif réelle conditionnelle + `revue-increment` avant commit | Manuel (adapté de VSCode2 — pas d'app web/dev server ici) | Jamais joué |
| `export-ppt-verifie` | Livrable = le deck `docs/cadrage-ppt/` : génération + enrichissements conditionnels (cadres photo, polish, design) + `pptx-verify`/`test_generate_deck.py` obligatoire + `revue-increment` | Manuel (adapté de VSCode2 — colonne vertébrale déjà pratiquée sur ce projet, ex. commit `1cb15fc`) | Jamais joué en tant que playbook formel |
| `revue-design-parallele` | Revue multi-angles d'un livrable en fan-out (≤4 `Explore`) puis consolidation | Manuel | Jamais joué en tant que playbook formel |
| `cycle-produit-bmad` | Cycle produit BMAD (brief→PRD→archi→epics→dev→review), clos par `revue-increment` | `generate_bmad_playbook.py` (généré depuis `_bmad/_config/bmad-help.csv` de ce dépôt — regénérer, ne pas éditer) | Jamais joué — sur demande explicite |
