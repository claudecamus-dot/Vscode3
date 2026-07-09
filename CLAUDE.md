# CLAUDE.md

<!-- TODO: paragraphe de contexte projet — ce que fait l'app, le vocabulaire
     métier à préserver tel quel (ne pas laisser traduire/angliciser des
     termes établis), pointeur vers un roadmap/docs plus profonds (avec un
     avertissement s'ils peuvent être obsolètes). -->

## Commandes

<!-- TODO: setup/run/test, copier-collables, avec un exemple de lancement
     d'un test unique et d'un sous-ensemble de tests par mot-clé. -->

## Architecture

<!-- TODO: le flux de requête (couches), le modèle de données, puis une
     sous-section par module non trivial avec des décisions non
     redérivables du code (le "pourquoi", pas le "quoi"), référence
     fichier:ligne à l'appui. -->

## Claude Code project setup

- `.claude/settings.json` (versionné) : hook `PreToolUse` sur `Bash|PowerShell`
  qui appelle `.claude/hooks/guard_destructive_git.py` — bloque
  `git push --force` (sans `--force-with-lease`) et `git reset --hard`.
  Bloque aussi la lecture de `.env`, `secrets/**`, `config/credentials.json`.
- `.claude/settings.local.json` et `CLAUDE.local.md` (gitignorés) : réglages
  propres à une machine/personne, jamais partagés.
- `.claude/skills/` (à créer au besoin) : skills projet-local documentant une
  séquence opérationnelle déjà découverte une fois (voir gabarit dans
  `claude-code-setup-export.md` §3).
- `.roadmap/` (à créer au besoin) : `.roadmap/roadmap.json` versionné,
  `.roadmap/*.svg` gitignoré (régénéré par le skill `roadmap-keeper`) — ce
  fichier peut être en avance/retard sur le code réel, vérifier contre
  `git log`/`git status` avant de lui faire confiance.
