---
updated: 2026-07-07
confidence: mixed
agents: [onboarder]
---

# Conventions — VSCode3 (dépôt de cadrage BMAD IAP)

## Linting & formatage

- Aucun outil de linting/formatage configuré pour le seul script Python du dépôt (`guard_destructive_git.py`)
  — `CONFIRMÉ` · onboarder · 2026-07-07
- Pas de pre-commit hooks git (à ne pas confondre avec le hook Claude Code `PreToolUse`, qui est un garde-fou d'agent, pas un hook git)
  — `CONFIRMÉ` · onboarder · 2026-07-07

## Nommage

- Documents de cadrage : `kebab-case.md` sous `docs/` (ex. `bmad-iap-cadrage.md`)
  — `CONFIRMÉ` · onboarder · 2026-07-07 · `docs/`
- Script hook Python : `snake_case.py`
  — `CONFIRMÉ` · onboarder · 2026-07-07 · `.claude/hooks/guard_destructive_git.py`
- Langue : français pour toute la documentation de cadrage, vocabulaire technique anglais conservé (RUN/BUILD, gate, checklist, MVP…)
  — `CONFIRMÉ` · onboarder · 2026-07-07 · `docs/bmad-iap-cadrage.md`

## Git

- Un seul commit à ce jour, message en anglais avec co-auteur Claude explicite
  — `CONFIRMÉ` · onboarder · 2026-07-07 · `git log`
- `.gitignore` exclut `.claude/settings.local.json` et `CLAUDE.local.md` — réglages propres à une machine/personne, jamais partagés
  — `CONFIRMÉ` · onboarder · 2026-07-07 · `.gitignore`

## Configuration & secrets

- `.claude/settings.json` bloque explicitement la lecture de `.env`, `secrets/**`, `config/credentials.json` par l'agent (permissions `deny`), même si ces fichiers n'existent pas encore dans ce dépôt
  — `CONFIRMÉ` · onboarder · 2026-07-07 · `.claude/settings.json:12`

## Patterns spécifiques à l'équipe

- Garde-fou destructif « fail open » — le hook `guard_destructive_git.py` ne bloque que sur un motif reconnu avec certitude ; toute erreur de parsing laisse passer la commande plutôt que de bloquer à tort
  — `CONFIRMÉ` · onboarder · 2026-07-07 · `.claude/hooks/guard_destructive_git.py:139-141`
- Tags de confiance `CONFIRMÉ` / `DÉDUIT` / `INCERTAIN` systématiques sur toute assertion de cadrage, avec agent · date · source — convention empruntée au projet frère VSCode2 (OpenHub) et reprise telle quelle dans ce wiki d'onboarding
  — `CONFIRMÉ` · onboarder · 2026-07-07 · `docs/bmad-iap-cadrage.md` §Agents BMAD
