---
updated: 2026-07-21
generated-by: .claude/supervision/scan_transcripts.py (superviseur d'agents, étage 1)
---

# Supervision des agents — tableau de bord d'usage

> ⚠️ **Page générée automatiquement** (hook SessionStart → `.claude/supervision/scan_transcripts.py`).
> **Ne pas éditer à la main** — toute modification serait écrasée au prochain scan.
> Conception et phasage : [../../reflexions/agent-superviseur.md](../../reflexions/agent-superviseur.md).

Dernier scan : 2026-07-21T11:32:25+02:00 · **7 sessions** (transcripts) · **8** invocations de skills · **21** lancements de sous-agents.

## Skills — usage réel

| Skill | Famille | Invocations | Première | Dernière |
| --- | --- | --- | --- | --- |
| `artifact-design` | (builtin/session) | 2 | 2026-07-06 | 2026-07-07 |
| `pptx-deck` | global | 2 | 2026-07-08 | 2026-07-09 |
| `agent-supervisor` | projet | 1 | 2026-07-21 | 2026-07-21 |
| `pptx-verify` | global | 1 | 2026-07-08 | 2026-07-08 |
| `restitution-deck-design` | global | 1 | 2026-07-08 | 2026-07-08 |
| `roadmap-keeper` | global | 1 | 2026-07-07 | 2026-07-07 |

## Sous-agents

| Sous-agent | Lancements | Premier | Dernier |
| --- | --- | --- | --- |
| `general-purpose` | 21 | 2026-07-06 | 2026-07-08 |

## Jamais utilisés

**projet** — 4/5 jamais invoqués :

`agent-orchestrator`, `pptx-framed-image`, `revue-increment`, `slide-text-polish`

**BMAD** — 46/46 jamais invoqués :

<details><summary>Voir la liste</summary>

`bmad-advanced-elicitation`, `bmad-agent-analyst`, `bmad-agent-architect`, `bmad-agent-dev`, `bmad-agent-pm`, `bmad-agent-tech-writer`, `bmad-agent-ux-designer`, `bmad-architecture`, `bmad-brainstorming`, `bmad-check-implementation-readiness`, `bmad-checkpoint-preview`, `bmad-code-review`, `bmad-correct-course`, `bmad-create-architecture`, `bmad-create-epics-and-stories`, `bmad-create-prd`, `bmad-create-story`, `bmad-customize`, `bmad-dev-auto`, `bmad-dev-story`, `bmad-document-project`, `bmad-domain-research`, `bmad-edit-prd`, `bmad-editorial-review-prose`, `bmad-editorial-review-structure`, `bmad-forge-idea`, `bmad-generate-project-context`, `bmad-help`, `bmad-index-docs`, `bmad-market-research`, `bmad-party-mode`, `bmad-prd`, `bmad-prfaq`, `bmad-product-brief`, `bmad-qa-generate-e2e-tests`, `bmad-quick-dev`, `bmad-retrospective`, `bmad-review-adversarial-general`, `bmad-review-edge-case-hunter`, `bmad-shard-doc`, `bmad-spec`, `bmad-sprint-planning`, `bmad-sprint-status`, `bmad-technical-research`, `bmad-ux`, `bmad-validate-prd`

</details>

**global** — 1/5 jamais invoqués :

`skill-creator`

## TODO agents (constats automatiques)

1. **Trier les skills BMAD** : 46 installés, 0 invocation à ce jour — décider lesquels garder, customiser ou désinstaller.
2. **`revue-increment` jamais invoquée** malgré le rappel SessionStart à chaque session — revoir son déclencheur (l'ancrer au flux de commit ?) ou la simplifier.
3. **Skills projet sans usage** : `agent-orchestrator`, `pptx-framed-image`, `slide-text-polish` — vérifier pertinence et déclencheurs.

## Diagnostic qualitatif (étage 2 — `agent-supervisor`)

_Diagnostic à jour._

1. **revue-increment jamais invoquee en 7 sessions, y compris avant des commits de code** — Faire respecter l'etape terminale revue-increment (checkpoint commit) des playbooks dev-verifie / export-ppt-verifie au prochain commit, au lieu de committer directement. · **Proposition** : Etape revue-increment deja cablee comme terminale non-conditionnelle dans dev-verifie et export-ppt-verifie (checkpoint non-false) : aucune modif de skill necessaire — il reste a l'executer avant le prochain commit plutot qu'a court-circuiter via un 'commit' direct.
2. **general-purpose est le seul type de sous-agent jamais lance (x21), zero Explore / zero Plan** — Router les recherches / inventaires / lectures en lecture seule vers Explore (haiku), la conception de plan vers Plan (opus), et reserver general-purpose (sonnet) aux taches multi-etapes reellement deleguees. · **Proposition** : Au prochain besoin d'exploration read-only, instancier Explore (modele haiku) au lieu de general-purpose ; le prochain diagnostic croisera modele x tache x reprises pour confirmer le gain. Caveat mesure : les 21 lancements sont anterieurs au 2026-07-08 (avant l'orchestrateur) — donnee a re-mesurer une fois quelques runs journalises dans runs.jsonl.

---

_Étage O-C (croisement modèle × tâche × reprises, exploitation de `runs.jsonl`) : voir `.claude/orchestration/routing-hints.json`, régénéré à chaque session._
