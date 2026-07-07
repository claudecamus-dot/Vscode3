---
updated: 2026-07-07
confidence: confirmed
agents: [onboarder]
---

# Stack — VSCode3 (dépôt de cadrage BMAD IAP)

## Dépendances principales

Aucune dépendance applicative — ce dépôt ne contient pas d'application exécutable, seulement de la documentation et le scaffolding Claude Code.
— `CONFIRMÉ` · onboarder · 2026-07-07 · absence de `requirements.txt` / `package.json` / `pyproject.toml`

| Catégorie | Technologie | Rôle |
|-----------|-------------|------|
| Outillage IA | Claude Code CLI | Assistant de développement, exécute le hook `PreToolUse` |
| Scripting hook | Python 3 (stdlib uniquement : `json`, `re`, `shlex`, `sys`) | `guard_destructive_git.py` — aucune dépendance tierce |
| Versionnement | Git | Un seul commit à ce jour |

— `CONFIRMÉ` · onboarder · 2026-07-07 · `.claude/hooks/guard_destructive_git.py`, `.claude/settings.json`

## Variables d'environnement requises

Aucune détectée — pas de `.env` ni `.env.example` dans ce dépôt.
— `CONFIRMÉ` · onboarder · 2026-07-07

## Contraintes de version

- Pas de `.python-version` ni de version Python figée pour le hook — dépend de l'interpréteur `py` disponible sur la machine (invocation `py .claude/hooks/guard_destructive_git.py`)
  — `CONFIRMÉ` · onboarder · 2026-07-07 · `.claude/settings.json:6`
- Aucune dépendance à figer par ailleurs : le dépôt n'a ni lockfile ni environnement virtuel
  — `CONFIRMÉ` · onboarder · 2026-07-07
