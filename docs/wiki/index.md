---
updated: 2026-07-07
confidence: confirmed
agents: [onboarder]
---

# BMAD IAP Cadrage — Index Wiki

## Nature du dépôt

Dépôt Claude Code sans application exécutable : scaffolding de projet (hooks, réglages de permissions) + documentation de cadrage pour le module de transformation consulting BMAD IAP (Infra as a Product).
— `CONFIRMÉ` · onboarder · 2026-07-07 · `CLAUDE.md`, `docs/bmad-iap-cadrage.md`

## Contenu critique

Le seul artefact substantiel du dépôt est `docs/bmad-iap-cadrage.md` (v2.1) — mirroir local d'un wiki de cadrage claude.ai, revu et corrigé le 2026-07-07 (compteurs de templates/checklists, redaction des noms clients, dépendances externes versionnées, gate de maturité DevOps tranché, schéma module.yaml résolu).
— `CONFIRMÉ` · onboarder · 2026-07-07 · `docs/bmad-iap-cadrage.md:5`

Enrichi le 2026-07-15 en deux passes : (v2.0) un export markdown de recommandation d'implémentation — agentic ou documentation, selon le contexte client — en complément des 4 profils PPT déjà cadrés, et un cas nominal illustratif (intake → amélioration de la recommandation) ; puis (v2.1) un brainstorm KPIs relancé — pourquoi, quoi, mise en place, exemple chiffré sur le même cas nominal. Le stack de skills PPT du kit portable (`ppt-toolkit.md`) a aussi été greffé dans ce dépôt : `pptx-framed-image`, `slide-text-polish`, l'agent `ppt-designer` ; le PPT de synthèse est passé de 12 à 22 slides (chapitres, exemples générés, schéma bout-en-bout, KPIs) et ne référence plus explicitement VSCode1. Passe design supplémentaire le même jour : intercalaires de chapitre sur le vrai layout « 50 - Chapitre » avec image encadrée (reprend le design du REX "⛱️ L'Été de l'IA" v3, VSCode1), nouvelle slide « vision » (claim + puces + visuel encadré), texte de tout le deck relu au linter `slide-text-polish` — deck porté à 23 slides.
— `CONFIRMÉ` · 2026-07-15 · `docs/bmad-iap-cadrage.md` §Trajectoire, §KPIs, `.claude/skills/`, `.claude/agents/ppt-designer.md`

Suite de passes le même jour (2026-07-15) : images encadrées passées de formes générées à de vraies photos libres de droit (Openverse CC0, `stock_images.py`, chaque photo vérifiée par rendu réel) ; ajout de `test_generate_deck.py` (première suite de tests fonctionnels du générateur — structure, alignement exact des images sur leur cadre, régressions, rendu réel LibreOffice) ; ajout de la rubrique « TODO — reprise de session » (portée aussi vers VSCode1 et VSCode2) ; puis 5 nouvelles slides — 3 « agents IA à créer » (why/what/gain, chapitre Cadrage), 1 « prudence IA » (chapitre Méthode), 1 « architecture SI » selon le niveau d'ambition A/B/C (chapitre Trajectoire) — deck porté à 28 slides.
— `CONFIRMÉ` · 2026-07-15 · `docs/cadrage-ppt/generate_deck.py`, `test_generate_deck.py`

Retour utilisateur le même jour (2026-07-15) : (1) le schéma de fonctionnement du §Trajectoire (COLLECTE→DIAGNOSTIC→CONCEPTION→RESTITUTION, bandeau Gate IA transversal, bandeau iap-risk-reviewer, boucle de réévaluation ⟲) n'avait jamais sa propre slide — ajout de `slide_schema_fonctionnement` en tête du chapitre Trajectoire, deck porté à 29 slides. (2) La slide « vision » (slide 3), centrée sur le seul point de doctrine IA, a été recadrée sur le pourquoi du projet, les enjeux, une difficulté de mise en œuvre et ce même risque IA (devenu une puce parmi d'autres). En vérifiant le rendu réel : la variante **grasse** du glyphe « ⟲ » manque dans la police du template (case vide sous LibreOffice) — bug pré-existant sur 3 slides plus anciennes, corrigé au passage (`bold=False` ciblé sur ce caractère).
— `CONFIRMÉ` · 2026-07-15 · `docs/cadrage-ppt/generate_deck.py`

## God nodes — concepts les plus connectés

| Concept | Pages liées | Criticité |
|---------|-------------|-----------|
| Gate IA & confidentialité | [technical/architecture.md](technical/architecture.md), [business/index.md](business/index.md) | Critique |
| BMAD IAP (11 agents / 11 workflows / 14 templates / 9 checklists) | [technical/architecture.md](technical/architecture.md), [business/index.md](business/index.md) | Haute |
| Export markdown agentic-ou-documentation (nouveau, v2.0) | [business/index.md](business/index.md) | Haute |

## Carte des domaines métier

- [Transformation Infra as a Product](business/index.md) — module de cadrage consulting pour transformer une organisation infra en plateforme produit tout en traitant structurellement le gaspillage

## Points critiques actifs 🔴

- Le module `bmad-iap/` lui-même (agents/, workflows/, templates/, knowledge/) n'existe pas encore physiquement dans ce dépôt — seul le cadrage est rédigé à ce stade
  — `CONFIRMÉ` · onboarder · 2026-07-07 · absence de dossier `bmad-iap/`
- Le `module.yaml` du futur module dépend d'un outillage externe (`bmb`, bmad-builder) non encore invoqué localement — scaffolding prévu en MVP1
  — `CONFIRMÉ` · onboarder · 2026-07-07 · `docs/bmad-iap-cadrage.md` §Structure, "Résolution module.yaml"

## Zones d'ombre

- Pas de CI/CD, pas de tests automatisés (dépôt documentaire, voir [technical/tests.md](technical/tests.md))
- `.roadmap/` et `.claude/skills/` mentionnés dans `CLAUDE.md` comme "à créer au besoin" — pas encore présents dans l'arborescence
- Process de redaction du REX source formalisé en principe seulement (voir `docs/bmad-iap-cadrage.md` §Points ouverts) — pas encore une étape de workflow reproductible

<!-- TODO-AGENTS:START — section générée par .claude/supervision/scan_transcripts.py, ne pas éditer à la main -->
## TODO agents 🤖

Constats automatiques du superviseur d'agents (usage mesuré dans les transcripts de session) :

- **Trier les skills BMAD** : 46 installés, 0 invocation à ce jour — décider lesquels garder, customiser ou désinstaller.
- **`revue-increment` jamais invoquée** malgré le rappel SessionStart à chaque session — revoir son déclencheur (l'ancrer au flux de commit ?) ou la simplifier.
- **Skills projet sans usage** : `agent-orchestrator`, `agent-supervisor`, `pptx-framed-image`, `slide-text-polish` — vérifier pertinence et déclencheurs.

Tableau de bord complet : [technical/agents-supervision.md](technical/agents-supervision.md) — régénéré à chaque session.
<!-- TODO-AGENTS:END -->
