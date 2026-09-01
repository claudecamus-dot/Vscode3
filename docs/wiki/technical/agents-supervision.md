---
updated: 2026-09-01
generated-by: .claude/supervision/scan_transcripts.py (superviseur d'agents, étage 1)
---

# Supervision des agents — tableau de bord d'usage

> ⚠️ **Page générée automatiquement** (hook SessionStart → `.claude/supervision/scan_transcripts.py`).
> **Ne pas éditer à la main** — toute modification serait écrasée au prochain scan.

Dernier scan : 2026-09-01T17:44:03+02:00 · **15 sessions** (transcripts) · **24** invocations de skills · **53** lancements de sous-agents.

## Skills — usage réel

| Skill | Famille | Invocations | Première | Dernière |
| --- | --- | --- | --- | --- |
| `agent-orchestrator` | projet | 8 | 2026-07-21 | 2026-09-01 |
| `agent-supervisor` | projet | 6 | 2026-07-21 | 2026-07-23 |
| `artifact-design` | (builtin/session) | 2 | 2026-07-06 | 2026-07-07 |
| `pptx-deck` | global | 2 | 2026-07-08 | 2026-07-09 |
| `revue-increment` | projet | 2 | 2026-07-21 | 2026-07-22 |
| `bmad-agent-pm` | BMAD | 1 | 2026-07-22 | 2026-07-22 |
| `pptx-verify` | global | 1 | 2026-07-08 | 2026-07-08 |
| `restitution-deck-design` | global | 1 | 2026-07-08 | 2026-07-08 |
| `roadmap-keeper` | global | 1 | 2026-07-07 | 2026-07-07 |

## Sous-agents

| Sous-agent | Lancements | Premier | Dernier |
| --- | --- | --- | --- |
| `general-purpose` | 31 | 2026-07-06 | 2026-07-23 |
| `ppt-designer` | 13 | 2026-07-21 | 2026-09-01 |
| `Explore` | 7 | 2026-07-21 | 2026-09-01 |
| `Plan` | 1 | 2026-07-21 | 2026-07-21 |
| `claude-code-guide` | 1 | 2026-07-21 | 2026-07-21 |

## Jamais utilisés

**projet** — 4/10 jamais invoqués :

`audit-technique`, `deck-design-library`, `deck-design-review`, `veille-agentic`

**BMAD** — 45/46 jamais invoqués :

<details><summary>Voir la liste</summary>

`bmad-advanced-elicitation`, `bmad-agent-analyst`, `bmad-agent-architect`, `bmad-agent-dev`, `bmad-agent-tech-writer`, `bmad-agent-ux-designer`, `bmad-architecture`, `bmad-brainstorming`, `bmad-check-implementation-readiness`, `bmad-checkpoint-preview`, `bmad-code-review`, `bmad-correct-course`, `bmad-create-architecture`, `bmad-create-epics-and-stories`, `bmad-create-prd`, `bmad-create-story`, `bmad-customize`, `bmad-dev-auto`, `bmad-dev-story`, `bmad-document-project`, `bmad-domain-research`, `bmad-edit-prd`, `bmad-editorial-review-prose`, `bmad-editorial-review-structure`, `bmad-forge-idea`, `bmad-generate-project-context`, `bmad-help`, `bmad-index-docs`, `bmad-market-research`, `bmad-party-mode`, `bmad-prd`, `bmad-prfaq`, `bmad-product-brief`, `bmad-qa-generate-e2e-tests`, `bmad-quick-dev`, `bmad-retrospective`, `bmad-review-adversarial-general`, `bmad-review-edge-case-hunter`, `bmad-shard-doc`, `bmad-spec`, `bmad-sprint-planning`, `bmad-sprint-status`, `bmad-technical-research`, `bmad-ux`, `bmad-validate-prd`

</details>

**global** — 1/5 jamais invoqués :

`skill-creator`

## Skills bibliothèque / référence

_Consommés en lisant/exécutant leurs `scripts/`, ou via un sous-agent qui les suit (ex. `ppt-designer`, qui n'a pas l'outil Skill) — le compteur d'invocations ne peut structurellement pas les voir. `n=0` n'y vaut donc PAS « mort » : ne pas désinstaller sur ce seul signal (constat superviseur #2)._

`pdf-quality`, `pptx-framed-image`, `slide-text-polish`

## TODO agents (constats automatiques)

1. **Skills projet sans usage** : `audit-technique`, `deck-design-review`, `veille-agentic` — vérifier pertinence et déclencheurs.
2. **Skills en sommeil (>30 j sans usage)** : `agent-supervisor`, `artifact-design`, `bmad-agent-pm`, `pptx-deck`, `pptx-verify`, `restitution-deck-design`, `revue-increment`, `roadmap-keeper`.

## Arbitrages enregistrés

_Constats clos par décision humaine (`.claude/supervision/arbitrages.json`) — l'usage réel reste mesuré ci-dessus._

- **`tri-BMAD-retraits-D`** (2026-07-23) : Constat agent-mort 2026-07-23 CLOS par décision utilisateur (« oublie les 4 retraits bmad ») : les 4 skills restantes arbitrées retrait (bmad-dev-auto, bmad-quick-dev, bmad-qa-generate-e2e-tests, bmad-prfaq) RESTENT sur disque — le retrait demeure documenté (pas de réactivation), la suppression physique est abandonnée comme geste. L'écart décision/terrain est assumé et ne doit plus remonter en constat. Rappel : bmad-market-research et bmad-domain-research requalifiées sur-demande le même jour (entrées dédiées).
- **`ppt-designer`** (2026-07-23) : Constat verification-manquante 2026-07-23 CLOS : fix shell 82db57a confirmé en conditions réelles le 2026-07-23 (spawn préflight-only : PowerShell ET Bash opérationnels, Python 3.14.5, python-pptx 1.0.2, verdict SHELL OK, zéro édition). La voie unique deck arbitrée le 2026-07-21 est donc effective : l'étape generation d'export-ppt-verifie s'instancie via le sous-agent ppt-designer. Le précédent inline des runs du 2026-07-22 (motivé par le shell non vérifié) ne fait plus jurisprudence pour la génération structurelle ; une passe de contenu ciblée reste possible inline avec rendu réel, en le notant au run.
- **`agent-orchestrator`** (2026-07-23) : Constat interaction 2026-07-23 CLOS : règle de journalisation codifiée au catalogue (section routage par défaut) — tout travail inline multi-étapes sur un livrable suivi (deck) journalise un run minimal via log_run.py (étapes inline), même sans sous-agent. Pas de rétro-journalisation des sessions du 2026-07-22 matin.
- **`ppt-designer`** (2026-07-21) : Conservé et ACTIVÉ comme voie unique de conception/génération du deck. L'étape 'generation' de export-ppt-verifie l'instancie désormais comme sous-agent (modèle hérité du thread principal, pas de bascule — jugement visuel). bmad-agent-ux-designer n'est PAS la voie deck : préférer une seule voie par tâche (CLAUDE.md).
- **`pptx-framed-image`** (2026-07-21) : used-as-library — conservée. Portée par le pipeline deck comme code vendored (cadres teardrop du template OCTO via generate_deck.py), pas invoquée via l'outil Skill : elle restera dans jamais_utilises par construction. Ne PAS la retirer au tri des skills mortes.
- **`deck-design-library`** (2026-07-23) : used-as-reference — greffée depuis VSCode2 le 2026-07-23 (SKILL.md adapté + catalogue-restitution.md verbatim, 22 patterns de decks de soutenance OCTO). Consultée comme documentation de référence par la session et le sous-agent ppt-designer (lecture de fichiers, pas invocation Skill) : elle peut rester dans jamais_utilises par construction, même en usage actif. Ne PAS la retirer au tri des skills mortes. Copie de référence dans VSCode2 — resynchroniser manuellement si le catalogue y évolue (même règle que docs/vscode1-export/).
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

1. **Un correctif de sécurité ne vit que dans la copie locale : la resynchronisation documentée le supprimerait** — Ne pas resynchroniser stock_images.py depuis VSCode1 en l'état. Faire remonter la garde vers le canon (hub) pour qu'elle reparte par export/, plutôt que de la laisser dans une copie feuille. · **Proposition** : Deux gestes, à arbitrer ensemble : (1) annoter docs/vscode1-export/ppt-toolkit.md d'une ligne « stock_images.py : VSCode3 est EN AVANCE (garde schéma + plafond taille, 2026-09-01) — ne pas re-synchroniser depuis VSCode1 tant que le correctif n'est pas remonté au hub » ; (2) porter le correctif au hub (.claude/skills/ puis export_agentic.py) pour que les 6 copies vulnérables soient servies corrigées. À défaut de (2), ajouter à la doctrine de resynchro une vérification préalable « la copie est-elle en avance ? » (diff avant tout resync) : sans elle, la prochaine resynchro est une régression de sécurité silencieuse.
2. **La discipline tokens et 4 autres sections de CLAUDE.md ont été supprimées le 2026-09-01 sans arbitrage, dont un correctif flotte adopté** — Restaurer les seules sections qui portent une règle non redite ailleurs, corriger le compte de slides, et tracer la coupe si elle était voulue. · **Proposition** : Restaurer depuis git show c465ea7:CLAUDE.md les deux sections orphelines : « Optimisation tokens » (à réaligner sur la « Discipline de gestion des tokens » du hub, re-mesurée depuis) et « Deck — contraintes durables » (cible du renvoi README) ; corriger « 40 slides » en 42. Laisser supprimées les 3 autres (skills/agents, orchestrateur, hiérarchie de modèles) : elles sont couvertes par .claude/orchestration/catalogue.md et playbooks/FORMAT.md. Si la coupe était délibérée, l'inverse est requis : tracer l'entrée dans arbitrages.json et retirer le renvoi mort du README — l'état actuel n'est ni l'un ni l'autre.
3. **Le générateur monolithique a crû de 13 % depuis l'audit : la pastille « risque technique moyen » repose sur un chiffre périmé** — Re-coter le risque sur le fichier réel avant d'agir : la pastille actuelle s'appuie sur un chiffre faux de 382 lignes. · **Proposition** : Relancer audit-technique sur VSCode3 (skill installée et jamais utilisée d'après routing-hints) pour re-coter risque_technique sur les 3149 lignes réelles. Puis, seulement si l'audit le confirme, acter un plafond au prochain incrément deck : extraire les fonctions slide_* par chapitre en modules chap0X.py importés par build(), le test fonctionnel existant servant de filet de non-régression. Ne rien découper avant arbitrage — le fichier est en évolution active (v2.7 du jour).
4. **Deux instruments de revue de design, zéro exécution en 23 runs — dont une skill réécrite pour CE deck et câblée nulle part** — Trancher entre les deux instruments plutôt que d'en garder deux morts. · **Proposition** : Option A — l'étape design-review d'export-ppt-verifie pointe sur deck-design-review (la version réécrite pour ce deck, pas la skill générique) et cesse d'être conditionnelle une fois par version majeure : le déclencheur devient « toute version qui ajoute ou restructure des slides », pour que la revue ne soit plus auto-délivrée par le producteur. Option B — deck-design-review est désinstallée comme doublon de restitution-deck-design et l'étape reste conditionnelle. Le statu quo cumule le coût des deux (deux skills à maintenir) et le bénéfice d'aucune.
5. **Le diagnostic a affiché 3 constats déjà clos pendant 40 jours, et le journal des arbitrages est figé depuis autant** — Coupler l'écriture de l'arbitrage au solde du run, et la réécriture du diagnostic à l'arbitrage — aucun des deux ne doit attendre le passage suivant du superviseur. · **Proposition** : Ajouter au contrat de clôture des playbooks (étape revue-increment / solde) : « un run dont la demande est une décision utilisateur appliquée écrit son entrée arbitrages.json dans le même geste que log_run.py --solde ; un constat arbitré est retiré de diagnostic.json à ce moment-là, pas au diagnostic suivant ». Sans ce couplage, la péremption à 14 jours du diagnostic ne protège de rien : elle signale un fichier vieux, pas un fichier faux.

---

_Étage O-C (croisement modèle × tâche × reprises, exploitation de `runs.jsonl`) : voir `.claude/orchestration/routing-hints.json`, régénéré à chaque session._
