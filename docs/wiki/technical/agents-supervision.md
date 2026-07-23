---
updated: 2026-07-23
generated-by: .claude/supervision/scan_transcripts.py (superviseur d'agents, étage 1)
---

# Supervision des agents — tableau de bord d'usage

> ⚠️ **Page générée automatiquement** (hook SessionStart → `.claude/supervision/scan_transcripts.py`).
> **Ne pas éditer à la main** — toute modification serait écrasée au prochain scan.
> Conception et phasage : [../../reflexions/agent-superviseur.md](../../reflexions/agent-superviseur.md).

Dernier scan : 2026-07-23T09:44:15+02:00 · **12 sessions** (transcripts) · **12** invocations de skills · **37** lancements de sous-agents.

## Skills — usage réel

| Skill | Famille | Invocations | Première | Dernière |
| --- | --- | --- | --- | --- |
| `agent-supervisor` | projet | 2 | 2026-07-21 | 2026-07-21 |
| `artifact-design` | (builtin/session) | 2 | 2026-07-06 | 2026-07-07 |
| `pptx-deck` | global | 2 | 2026-07-08 | 2026-07-09 |
| `agent-orchestrator` | projet | 1 | 2026-07-21 | 2026-07-21 |
| `bmad-agent-pm` | BMAD | 1 | 2026-07-22 | 2026-07-22 |
| `pptx-verify` | global | 1 | 2026-07-08 | 2026-07-08 |
| `restitution-deck-design` | global | 1 | 2026-07-08 | 2026-07-08 |
| `revue-increment` | projet | 1 | 2026-07-21 | 2026-07-21 |
| `roadmap-keeper` | global | 1 | 2026-07-07 | 2026-07-07 |

## Sous-agents

| Sous-agent | Lancements | Premier | Dernier |
| --- | --- | --- | --- |
| `general-purpose` | 27 | 2026-07-06 | 2026-07-23 |
| `ppt-designer` | 5 | 2026-07-21 | 2026-07-23 |
| `Explore` | 3 | 2026-07-21 | 2026-07-21 |
| `Plan` | 1 | 2026-07-21 | 2026-07-21 |
| `claude-code-guide` | 1 | 2026-07-21 | 2026-07-21 |

## Jamais utilisés

**projet** — 2/5 jamais invoqués :

`pptx-framed-image`, `slide-text-polish`

**BMAD** — 45/46 jamais invoqués :

<details><summary>Voir la liste</summary>

`bmad-advanced-elicitation`, `bmad-agent-analyst`, `bmad-agent-architect`, `bmad-agent-dev`, `bmad-agent-tech-writer`, `bmad-agent-ux-designer`, `bmad-architecture`, `bmad-brainstorming`, `bmad-check-implementation-readiness`, `bmad-checkpoint-preview`, `bmad-code-review`, `bmad-correct-course`, `bmad-create-architecture`, `bmad-create-epics-and-stories`, `bmad-create-prd`, `bmad-create-story`, `bmad-customize`, `bmad-dev-auto`, `bmad-dev-story`, `bmad-document-project`, `bmad-domain-research`, `bmad-edit-prd`, `bmad-editorial-review-prose`, `bmad-editorial-review-structure`, `bmad-forge-idea`, `bmad-generate-project-context`, `bmad-help`, `bmad-index-docs`, `bmad-market-research`, `bmad-party-mode`, `bmad-prd`, `bmad-prfaq`, `bmad-product-brief`, `bmad-qa-generate-e2e-tests`, `bmad-quick-dev`, `bmad-retrospective`, `bmad-review-adversarial-general`, `bmad-review-edge-case-hunter`, `bmad-shard-doc`, `bmad-spec`, `bmad-sprint-planning`, `bmad-sprint-status`, `bmad-technical-research`, `bmad-ux`, `bmad-validate-prd`

</details>

**global** — 1/5 jamais invoqués :

`skill-creator`

## TODO agents (constats automatiques)

_(aucun constat — rien à signaler sur les données actuelles)_

## Arbitrages enregistrés

_Constats clos par décision humaine (`.claude/supervision/arbitrages.json`) — l'usage réel reste mesuré ci-dessus._

- **`ppt-designer`** (2026-07-23) : Constat verification-manquante 2026-07-23 CLOS : fix shell 82db57a confirmé en conditions réelles le 2026-07-23 (spawn préflight-only : PowerShell ET Bash opérationnels, Python 3.14.5, python-pptx 1.0.2, verdict SHELL OK, zéro édition). La voie unique deck arbitrée le 2026-07-21 est donc effective : l'étape generation d'export-ppt-verifie s'instancie via le sous-agent ppt-designer. Le précédent inline des runs du 2026-07-22 (motivé par le shell non vérifié) ne fait plus jurisprudence pour la génération structurelle ; une passe de contenu ciblée reste possible inline avec rendu réel, en le notant au run.
- **`agent-orchestrator`** (2026-07-23) : Constat interaction 2026-07-23 CLOS : règle de journalisation codifiée au catalogue (section routage par défaut) — tout travail inline multi-étapes sur un livrable suivi (deck) journalise un run minimal via log_run.py (étapes inline), même sans sous-agent. Pas de rétro-journalisation des sessions du 2026-07-22 matin.
- **`ppt-designer`** (2026-07-21) : Conservé et ACTIVÉ comme voie unique de conception/génération du deck. L'étape 'generation' de export-ppt-verifie l'instancie désormais comme sous-agent (modèle hérité du thread principal, pas de bascule — jugement visuel). bmad-agent-ux-designer n'est PAS la voie deck : préférer une seule voie par tâche (CLAUDE.md).
- **`pptx-framed-image`** (2026-07-21) : used-as-library — conservée. Portée par le pipeline deck comme code vendored (cadres teardrop du template OCTO via generate_deck.py), pas invoquée via l'outil Skill : elle restera dans jamais_utilises par construction. Ne PAS la retirer au tri des skills mortes.
- **`slide-text-polish`** (2026-07-21) : used-as-library — conservée. Lint de copie (slide_lint) intégré au pipeline deck, invoquée comme code et non via l'outil Skill : elle restera dans jamais_utilises par construction. Ne PAS la retirer au tri des skills mortes.
- **`famille:BMAD`** (2026-07-21) : Tri des 46 skills BMAD EXÉCUTÉ (choix A). Classement en 5 catégories via inventaire de câblage (Explore) + stratégie (Plan) : A câblées=13 (5 délégations de revue-increment : bmad-code-review/retrospective/correct-course/checkpoint-preview/help ; 8 étapes du playbook généré cycle-produit-bmad : product-brief/prd/architecture/create-epics-and-stories/check-implementation-readiness/sprint-planning/create-story/dev-story) — reliées à l'orchestrateur comme voie de première intention (catalogue) ; B sous-skill/angle mort=5 (review-adversarial-general, review-edge-case-hunter, advanced-elicitation, party-mode, spec — invoquées en langage naturel par une skill câblée, ne pas qualifier agent-mort) ; C sur-demande=16 (6 personas bmad-agent-* + réserve produit/édition, via bmad-help) ; D candidat-retrait=8 (dev-auto, quick-dev, qa-generate-e2e-tests, market-research, domain-research, prfaq, index-docs, shard-doc — arbitrage retrait individuel à trancher, NON décidé ici) ; E deprecated-v7=4 (create-architecture, create-prd, edit-prd, validate-prd — purge par l'updater BMAD, jamais à la main). Effet : ferme le TODO d'élagage déterministe (jeton famille:BMAD, seul reconnu par build_todos) ; les 46 restent mesurées dans jamais_utilises ; l'étage-2 garde la main par cible exacte. Ne PAS rm _bmad/ ni éditer cycle-produit-bmad.md à la main (généré).
- **`bmad-dev-auto`** (2026-07-21) : retrait (catégorie D) — redondant avec bmad-dev-story (câblée, cat. A) + les builtins code-review/simplify ; boucle de dev non attendue sur ce dépôt (livrable = deck + outillage superviseur). Arbitrage documenté : suppression physique = geste humain séparé, aucun rm unilatéral, aucune édition de _bmad/.
- **`bmad-quick-dev`** (2026-07-21) : retrait (catégorie D) — redondant avec bmad-dev-story (câblée) + builtins ; pas de flux d'implémentation code récurrent ici. Arbitrage documenté, pas de suppression physique unilatérale.
- **`bmad-qa-generate-e2e-tests`** (2026-07-21) : retrait (catégorie D) — pas d'application ni de harnais e2e sur ce dépôt (cf. catalogue : pas d'app web/dev server). Sans objet. Arbitrage documenté, pas de suppression physique unilatérale.
- **`bmad-market-research`** (2026-07-23) : REQUALIFIÉE sur-demande (2026-07-23, annule le retrait du 21/07) — le retrait était motivé par « veille marché hors mission » ; la demande utilisateur du 23/07 (revue produit + research + market-research du projet global, cf. docs/reflexions/revue-produit-marche.md) est le contre-exemple exact. Substance exécutée via sous-agent general-purpose + web (les workflows BMAD interactifs restent une voie possible sur demande). Rejoint la catégorie C (sur-demande, via bmad-help).
- **`bmad-domain-research`** (2026-07-23) : REQUALIFIÉE sur-demande (2026-07-23, annule le retrait du 21/07) — même motif que bmad-market-research : la revue research domaine/technique du 23/07 (état de l'art vs paris IAP, cf. docs/reflexions/revue-produit-marche.md) est exactement une recherche domaine/industrie sur la mission de ce dépôt. Rejoint la catégorie C (sur-demande, via bmad-help).
- **`bmad-prfaq`** (2026-07-21) : retrait (catégorie D) — challenge PRFAQ/Working-Backwards produit, hors mission cadrage/deck. Arbitrage documenté, pas de suppression physique unilatérale.
- **`bmad-index-docs`** (2026-07-21) : conserver dormante (catégorie D) — utilitaire d'indexation de docs, inoffensif et bon marché ; gardé malgré 0 usage (bruit faible, option conservée). Pas retiré.
- **`bmad-shard-doc`** (2026-07-21) : conserver dormante (catégorie D) — utilitaire de découpe de gros markdown, inoffensif ; gardé malgré 0 usage (bruit faible). Pas retiré.
- **`export-ppt-verifie`** (2026-07-21) : Proposition superviseur (diagnostic 2026-07-21, constat prio 3) ACCEPTÉE et APPLIQUÉE : la vérification par rendu réel nomme désormais le défaut « panneau flottant/étiré » comme contrôle explicite par NOUVEAU type de slide (contenu centré par slot laissant un vide sous l'en-tête, ou panneau sur-étiré). Amendés : brief .claude/agents/ppt-designer.md (étape 4 real render) + contrat de l'étape verification-rendu du playbook export-ppt-verifie. Constat clos.
- **`docs/wiki.html`** (2026-07-21) : Proposition superviseur (diagnostic 2026-07-21, constat prio 1) ACCEPTÉE et APPLIQUÉE : marqueurs TODO-AGENTS-HTML posés dans docs/wiki.html (+ entrée TOC #agents-supervision), option « compléter le câblage » retenue plutôt que retirer le chemin HTML du scan. Le scan peuple désormais le dashboard HTML (plus d'avertissement « sans marqueurs »). Constat clos.

## Diagnostic qualitatif (étage 2 — `agent-supervisor`)

_Diagnostic à jour._

1. **6 retraits BMAD arbitrés le 2026-07-21 toujours physiquement présents** — Un geste humain unique : supprimer les 6 dossiers, ou re-arbitrer en « dormantes » si le geste est refusé — l'écart décision/terrain fait re-remonter ces 6 skills dans jamais_utilises à chaque scan. · **Proposition** : Suppression des 6 dossiers listés, à valider et exécuter par l'humain (jamais auto). À défaut, requalifier l'arbitrage de « retrait » à « dormante » pour que l'état documenté colle au terrain.

---

_Étage O-C (croisement modèle × tâche × reprises, exploitation de `runs.jsonl`) : voir `.claude/orchestration/routing-hints.json`, régénéré à chaque session._
