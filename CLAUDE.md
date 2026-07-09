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
- `docs/vscode1-export/` : miroir local de `export/` du projet frère VSCode1
  (kit PPT `ppt-toolkit.md`, méthode tokens `optimisation-tokens.md`, design
  system/template/backlog du deck OCTO). Copie de référence, pas la source de
  vérité — resynchroniser manuellement contre VSCode1 si besoin.
- `docs/cadrage-ppt/` : le deck OCTO annoncé comme « à réactiver si un jour »
  ci-dessus est désormais réel — `template-octo.pptx` (copie du template de
  marque, masters/layouts/thème OCTO) + `pptx_deck.py` (copie synchronisée du
  skill global `pptx-deck`) + `generate_deck.py` (11 slides de synthèse du
  cadrage BMAD IAP, dessinées sur le vrai template via ses layouts `04 -
  Titre seul` et `40 - Couverture [1]`) → `bmad-iap-cadrage-synthese.pptx`.
  Regénérer avec `python generate_deck.py` depuis ce dossier ; toute nouvelle
  version du cadrage qui change une affirmation déjà reprise en slide doit
  répercuter le changement ici, pas seulement dans le `.md` source.
  `analyse-template-alternatif.md` : analyse (pas d'implémentation) d'un
  second template PPT trouvé dans VSCode2 — pistes de design retenues/
  écartées pour ce générateur, sans copier le template lui-même (contenu
  client redacté).

## Optimisation tokens

Pratiques issues de `docs/vscode1-export/optimisation-tokens.md` (§1-5),
opérationnalisées pour ce dépôt :

- **Ne pas re-dériver ce que le wiki ou une mémoire documente déjà** —
  consulter `docs/wiki.html`/`docs/wiki/` et les mémoires projet avant de
  relire des fichiers sources pour reconstruire un contexte déjà écrit.
- **Lire des portions ciblées, pas des fichiers entiers** — Grep/Glob puis
  `Read` avec `offset`/`limit` sur la zone utile plutôt qu'une lecture
  intégrale d'un gros fichier (le wiki fait ~1800 lignes, le cadrage BMAD IAP
  ~99K).
- **Pas de sous-agent par défaut** — ce dépôt est petit et le contexte est
  déjà chargé la plupart du temps ; ne déléguer à un `Agent` que si la tâche
  est explicitement large/exploratoire ou demandée comme telle.
- **Documenter une décision une fois plutôt que la rejouer** — toute décision
  de cadrage ou de convention actée va dans le wiki, `docs/vscode1-export/`
  ou une mémoire projet, pas seulement dans la réponse de conversation.
- **Enchaîner les actions sans pause longue** — le cache prompt a un TTL
  d'~5 min ; éviter les silences de plusieurs minutes en plein enchaînement
  d'outils.
