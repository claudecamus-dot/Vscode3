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

Le seul artefact substantiel du dépôt est `docs/bmad-iap-cadrage.md` (v1.6) — mirroir local d'un wiki de cadrage claude.ai, revu et corrigé le 2026-07-07 (compteurs de templates/checklists, redaction des noms clients, dépendances externes versionnées, gate de maturité DevOps tranché, schéma module.yaml résolu).
— `CONFIRMÉ` · onboarder · 2026-07-07 · `docs/bmad-iap-cadrage.md:5`

## God nodes — concepts les plus connectés

| Concept | Pages liées | Criticité |
|---------|-------------|-----------|
| Gate IA & confidentialité | [technical/architecture.md](technical/architecture.md), [business/index.md](business/index.md) | Critique |
| BMAD IAP (11 agents / 11 workflows / 14 templates / 9 checklists) | [technical/architecture.md](technical/architecture.md), [business/index.md](business/index.md) | Haute |

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
