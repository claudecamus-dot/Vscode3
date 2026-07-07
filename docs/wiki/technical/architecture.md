---
updated: 2026-07-07
confidence: confirmed
agents: [onboarder]
---

# Architecture — VSCode3 (dépôt de cadrage BMAD IAP)

## Structure globale

Dépôt documentaire, pas d'architecture logicielle : scaffolding Claude Code (hooks, permissions) autour d'un unique livrable de fond, `docs/bmad-iap-cadrage.md`.
— `CONFIRMÉ` · onboarder · 2026-07-07 · arborescence racine

## Arborescence

```
VSCode3/
  .claude/
    settings.json                    ← hook PreToolUse (garde-fou git) + permissions deny (.env, secrets/**, config/credentials.json)
    hooks/guard_destructive_git.py   ← bloque `git push --force` sans --force-with-lease et `git reset --hard`
  docs/
    bmad-iap-cadrage.md              ← wiki de cadrage BMAD IAP, v1.6, mirroir local d'un artifact claude.ai
    wiki/                            ← ce wiki d'onboarding (généré 2026-07-07)
  CLAUDE.md                          ← instructions projet (structure attendue de .claude/, .roadmap/, skills locaux)
  .gitignore                        ← exclut settings.local.json et CLAUDE.local.md (réglages machine, jamais partagés)
```
— `CONFIRMÉ` · onboarder · 2026-07-07

## Architecture du contenu documenté (BMAD IAP)

Le vrai « système » que ce dépôt documente n'est pas du code mais une méthode consulting : 11 agents, 11 workflows, 14 templates, 9 checklists, 9+ fichiers knowledge, 1 gate IA transversal non-automatisable — rien de tout cela n'est encore implémenté physiquement ici, seul le cadrage l'est.
— `CONFIRMÉ` · onboarder · 2026-07-07 · `docs/bmad-iap-cadrage.md` §Structure

## Décisions architecturales notables

- **Isolation multi-client** — `engagements/<client-slug>/` séparé de la méthode générique (`agents/`, `workflows/`, `knowledge/`), pour qu'une même installation serve plusieurs missions sans mélange de données
  — `CONFIRMÉ` · onboarder · 2026-07-07 · `docs/bmad-iap-cadrage.md` §Isolation multi-client
- **Gate IA toujours checkpoint humain** — quel que soit le mode d'autonomie choisi à l'intake (manuel/semi-auto/auto), la décision de confidentialité IA n'est jamais automatisable (principe hérité d'ADR-006, projet frère VSCode2/OpenHub)
  — `CONFIRMÉ` · onboarder · 2026-07-07 · `docs/bmad-iap-cadrage.md` §Gate IA & confidentialité
- **Dépendances externes versionnées** — grille de maturité VSCode1 (pin V3.2) et contrats OpenHub (VSCode2, ADR-006/ADR-009), revus à chaque boucle de réévaluation (`iap-re-assessment`) et à chaque MVP gate
  — `CONFIRMÉ` · onboarder · 2026-07-07 · `docs/bmad-iap-cadrage.md` §Modèles de maturité, "Dépendances externes — versionnage"

## Points de fragilité connus

- Le module `bmad-iap/` (agents/, workflows/, templates/, knowledge/) n'existe pas encore physiquement — l'implémentation démarre en MVP0/MVP1
  — `CONFIRMÉ` · onboarder · 2026-07-07 · absence de dossier `bmad-iap/`
- Aucune CI/CD
  — `CONFIRMÉ` · onboarder · 2026-07-07
