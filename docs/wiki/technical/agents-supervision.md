---
updated: 2026-07-21
generated-by: .claude/supervision/scan_transcripts.py (superviseur d'agents, étage 1)
---

# Supervision des agents — tableau de bord d'usage

> ⚠️ **Page générée automatiquement** (hook SessionStart → `.claude/supervision/scan_transcripts.py`).
> **Ne pas éditer à la main** — toute modification serait écrasée au prochain scan.
> Conception et phasage : [../../reflexions/agent-superviseur.md](../../reflexions/agent-superviseur.md).

Dernier scan : 2026-07-21T14:46:17+02:00 · **8 sessions** (transcripts) · **10** invocations de skills · **26** lancements de sous-agents.

## Skills — usage réel

| Skill | Famille | Invocations | Première | Dernière |
| --- | --- | --- | --- | --- |
| `artifact-design` | (builtin/session) | 2 | 2026-07-06 | 2026-07-07 |
| `pptx-deck` | global | 2 | 2026-07-08 | 2026-07-09 |
| `agent-orchestrator` | projet | 1 | 2026-07-21 | 2026-07-21 |
| `agent-supervisor` | projet | 1 | 2026-07-21 | 2026-07-21 |
| `pptx-verify` | global | 1 | 2026-07-08 | 2026-07-08 |
| `restitution-deck-design` | global | 1 | 2026-07-08 | 2026-07-08 |
| `revue-increment` | projet | 1 | 2026-07-21 | 2026-07-21 |
| `roadmap-keeper` | global | 1 | 2026-07-07 | 2026-07-07 |

## Sous-agents

| Sous-agent | Lancements | Premier | Dernier |
| --- | --- | --- | --- |
| `general-purpose` | 21 | 2026-07-06 | 2026-07-08 |
| `Explore` | 3 | 2026-07-21 | 2026-07-21 |
| `Plan` | 1 | 2026-07-21 | 2026-07-21 |
| `ppt-designer` | 1 | 2026-07-21 | 2026-07-21 |

## Jamais utilisés

**projet** — 2/5 jamais invoqués :

`pptx-framed-image`, `slide-text-polish`

**BMAD** — 46/46 jamais invoqués :

<details><summary>Voir la liste</summary>

`bmad-advanced-elicitation`, `bmad-agent-analyst`, `bmad-agent-architect`, `bmad-agent-dev`, `bmad-agent-pm`, `bmad-agent-tech-writer`, `bmad-agent-ux-designer`, `bmad-architecture`, `bmad-brainstorming`, `bmad-check-implementation-readiness`, `bmad-checkpoint-preview`, `bmad-code-review`, `bmad-correct-course`, `bmad-create-architecture`, `bmad-create-epics-and-stories`, `bmad-create-prd`, `bmad-create-story`, `bmad-customize`, `bmad-dev-auto`, `bmad-dev-story`, `bmad-document-project`, `bmad-domain-research`, `bmad-edit-prd`, `bmad-editorial-review-prose`, `bmad-editorial-review-structure`, `bmad-forge-idea`, `bmad-generate-project-context`, `bmad-help`, `bmad-index-docs`, `bmad-market-research`, `bmad-party-mode`, `bmad-prd`, `bmad-prfaq`, `bmad-product-brief`, `bmad-qa-generate-e2e-tests`, `bmad-quick-dev`, `bmad-retrospective`, `bmad-review-adversarial-general`, `bmad-review-edge-case-hunter`, `bmad-shard-doc`, `bmad-spec`, `bmad-sprint-planning`, `bmad-sprint-status`, `bmad-technical-research`, `bmad-ux`, `bmad-validate-prd`

</details>

**global** — 1/5 jamais invoqués :

`skill-creator`

## TODO agents (constats automatiques)

_(aucun constat — rien à signaler sur les données actuelles)_

## Arbitrages enregistrés

_Constats clos par décision humaine (`.claude/supervision/arbitrages.json`) — l'usage réel reste mesuré ci-dessus._

- **`ppt-designer`** (2026-07-21) : Conservé et ACTIVÉ comme voie unique de conception/génération du deck. L'étape 'generation' de export-ppt-verifie l'instancie désormais comme sous-agent (modèle hérité du thread principal, pas de bascule — jugement visuel). bmad-agent-ux-designer n'est PAS la voie deck : préférer une seule voie par tâche (CLAUDE.md).
- **`pptx-framed-image`** (2026-07-21) : used-as-library — conservée. Portée par le pipeline deck comme code vendored (cadres teardrop du template OCTO via generate_deck.py), pas invoquée via l'outil Skill : elle restera dans jamais_utilises par construction. Ne PAS la retirer au tri des skills mortes.
- **`slide-text-polish`** (2026-07-21) : used-as-library — conservée. Lint de copie (slide_lint) intégré au pipeline deck, invoquée comme code et non via l'outil Skill : elle restera dans jamais_utilises par construction. Ne PAS la retirer au tri des skills mortes.
- **`famille:BMAD`** (2026-07-21) : Tri des 46 skills BMAD EXÉCUTÉ (choix A). Classement en 5 catégories via inventaire de câblage (Explore) + stratégie (Plan) : A câblées=13 (5 délégations de revue-increment : bmad-code-review/retrospective/correct-course/checkpoint-preview/help ; 8 étapes du playbook généré cycle-produit-bmad : product-brief/prd/architecture/create-epics-and-stories/check-implementation-readiness/sprint-planning/create-story/dev-story) — reliées à l'orchestrateur comme voie de première intention (catalogue) ; B sous-skill/angle mort=5 (review-adversarial-general, review-edge-case-hunter, advanced-elicitation, party-mode, spec — invoquées en langage naturel par une skill câblée, ne pas qualifier agent-mort) ; C sur-demande=16 (6 personas bmad-agent-* + réserve produit/édition, via bmad-help) ; D candidat-retrait=8 (dev-auto, quick-dev, qa-generate-e2e-tests, market-research, domain-research, prfaq, index-docs, shard-doc — arbitrage retrait individuel à trancher, NON décidé ici) ; E deprecated-v7=4 (create-architecture, create-prd, edit-prd, validate-prd — purge par l'updater BMAD, jamais à la main). Effet : ferme le TODO d'élagage déterministe (jeton famille:BMAD, seul reconnu par build_todos) ; les 46 restent mesurées dans jamais_utilises ; l'étage-2 garde la main par cible exacte. Ne PAS rm _bmad/ ni éditer cycle-produit-bmad.md à la main (généré).
- **`bmad-dev-auto`** (2026-07-21) : retrait (catégorie D) — redondant avec bmad-dev-story (câblée, cat. A) + les builtins code-review/simplify ; boucle de dev non attendue sur ce dépôt (livrable = deck + outillage superviseur). Arbitrage documenté : suppression physique = geste humain séparé, aucun rm unilatéral, aucune édition de _bmad/.
- **`bmad-quick-dev`** (2026-07-21) : retrait (catégorie D) — redondant avec bmad-dev-story (câblée) + builtins ; pas de flux d'implémentation code récurrent ici. Arbitrage documenté, pas de suppression physique unilatérale.
- **`bmad-qa-generate-e2e-tests`** (2026-07-21) : retrait (catégorie D) — pas d'application ni de harnais e2e sur ce dépôt (cf. catalogue : pas d'app web/dev server). Sans objet. Arbitrage documenté, pas de suppression physique unilatérale.
- **`bmad-market-research`** (2026-07-21) : retrait (catégorie D) — veille marché hors mission (cadrage BMAD IAP / deck de restitution, pas de discovery marché). Arbitrage documenté, pas de suppression physique unilatérale.
- **`bmad-domain-research`** (2026-07-21) : retrait (catégorie D) — recherche domaine/industrie hors mission de ce dépôt. Arbitrage documenté, pas de suppression physique unilatérale.
- **`bmad-prfaq`** (2026-07-21) : retrait (catégorie D) — challenge PRFAQ/Working-Backwards produit, hors mission cadrage/deck. Arbitrage documenté, pas de suppression physique unilatérale.
- **`bmad-index-docs`** (2026-07-21) : conserver dormante (catégorie D) — utilitaire d'indexation de docs, inoffensif et bon marché ; gardé malgré 0 usage (bruit faible, option conservée). Pas retiré.
- **`bmad-shard-doc`** (2026-07-21) : conserver dormante (catégorie D) — utilitaire de découpe de gros markdown, inoffensif ; gardé malgré 0 usage (bruit faible). Pas retiré.

## Diagnostic qualitatif (étage 2 — `agent-supervisor`)

_Diagnostic ⚠️ à relancer (> 14 j)._

1. **revue-increment jamais invoquee en 7 sessions, y compris avant des commits de code produit** — Executer l'etape terminale revue-increment (checkpoint commit) des playbooks dev-verifie / export-ppt-verifie au prochain commit, au lieu de committer directement. · **Proposition** : Etape revue-increment deja cablee comme terminale non-conditionnelle dans dev-verifie et export-ppt-verifie (checkpoint non-false) : aucune modif de skill necessaire — il reste a l'executer avant le prochain commit plutot qu'a le court-circuiter via un 'commit' direct.
2. **general-purpose est le seul type de sous-agent jamais lance (x21), zero Explore / zero Plan** — Router les recherches / inventaires / lectures en lecture seule vers Explore (haiku), la conception de plan vers Plan (opus), et reserver general-purpose (sonnet) aux taches multi-etapes reellement deleguees. · **Proposition** : Au prochain besoin d'exploration read-only, instancier Explore (modele haiku) au lieu de general-purpose ; le prochain diagnostic croisera modele x tache x reprises pour confirmer le gain. Caveat mesure : les 21 lancements sont anterieurs au 2026-07-08 (avant l'orchestrateur) — a re-mesurer une fois quelques runs journalises dans runs.jsonl.

---

_Étage O-C (croisement modèle × tâche × reprises, exploitation de `runs.jsonl`) : voir `.claude/orchestration/routing-hints.json`, régénéré à chaque session._
