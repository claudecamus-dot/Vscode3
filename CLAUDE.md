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
- `.claude/skills/` : `pptx-framed-image` et `slide-text-polish`, greffés
  depuis VSCode1 (2026-07-15) via le kit `docs/vscode1-export/ppt-toolkit.md`
  — tests rejoués après copie (9/9 et 9/9). `.claude/agents/ppt-designer.md` :
  agent projet-local, adapté du `ppt-designer` de VSCode1 pour piloter
  `docs/cadrage-ppt/generate_deck.py` (voir aussi le gabarit générique dans
  `claude-code-setup-export.md` §3 pour créer d'autres skills projet-local).
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
  skill global `pptx-deck`) + `generate_deck.py` (29 slides de synthèse du
  cadrage BMAD IAP v2.1, dessinées sur le vrai template) → `bmad-iap-cadrage-
  synthese.pptx`. Structure : couverture, executive summary, 1 slide « vision »
  (claim + puces + visuel encadré, layout "63 - cadre blanc" — recadrée sur le
  pourquoi du projet/les enjeux/une difficulté de mise en œuvre/le risque IA,
  plutôt que le seul point de doctrine IA qui n'en est plus qu'une puce parmi
  d'autres), 3 chapitres (Cadrage/Méthode/Trajectoire — intercalaires sur le
  vrai layout dédié "50 - Chapitre", **avec image encadrée** : cadre teardrop
  rempli via le skill `pptx-framed-image` greffé depuis VSCode1, reprenant le
  design du REX "⛱️ L'Été de l'IA" v3 ; un premier essai texte-seul sur ce
  layout avait été abandonné avant d'en comprendre les deux bugs réels — cf.
  mémoire de session et commentaire dans `slide_chapitre`/`_sans_puce`),
  3 slides « agents IA à créer » (why/what/gain, ancrées sur des familles de
  gaspillage déjà cadrées : triage RUN, veille FinOps, documentaire cognitif)
  en fin de chapitre Cadrage, 1 slide « prudence IA » (décompose le facteur
  confidentialité/supervision/criticité de la formule de priorisation) juste
  après `slide_gaspillages`, 3 slides d'exemples générés (priorisation
  chiffrée, diagnostic, recommandation) après le chapitre Méthode, 1 slide
  « schéma de fonctionnement » (bandeau Gate IA transversal + pipeline
  COLLECTE→DIAGNOSTIC→CONCEPTION→RESTITUTION + bandeau iap-risk-reviewer +
  bandeau boucle de réévaluation ⟲ — jusqu'ici seulement résumé en une ligne
  dans `slide_trajectoire`, jamais sa propre slide) juste avant
  `slide_trajectoire` en tête du chapitre Trajectoire, 1 slide schéma
  bout-en-bout après `slide_trajectoire`, 1 slide « architecture SI » (lien
  avec le SI client selon le niveau d'ambition A/B/C) après `slide_ambition`,
  3 slides KPIs (pourquoi/quoi, mise en place, exemple chiffré) en clôture.
  Détail à retenir sur le glyphe « ⟲ » : sa variante **grasse** manque dans la
  police du template (rendu LibreOffice = case vide dans les badges colorés)
  alors que la variante normale s'affiche correctement — tous les badges/
  bandeaux utilisant ce symbole (slide_trajectoire, slide_schema_bout_en_bout,
  slide_livrables_ppt, slide_schema_fonctionnement) forcent donc `bold=False`
  spécifiquement pour ce caractère.
  Les images encadrées sont de vraies photos libres de droit (Openverse,
  CC0, sans clé API — `stock_images.py`, greffé dans `pptx-framed-image` le
  2026-07-15), avec repli automatique sur le générateur procédural
  `nature_images.py` si le réseau n'est pas disponible ; **toujours vérifier
  chaque photo par rendu réel avant de la garder** — la recherche par
  mot-clé n'a aucun jugement (un `"ocean waves aerial"` a d'abord renvoyé
  une photo de plage bondée de vacanciers). Fichiers dans
  `docs/cadrage-ppt/_img/` (gitignoré, régénérable) ; provenance (requête,
  auteur, source, licence) journalisée dans `images-manifest.json`
  (versionné, lui). Ne référence plus explicitement VSCode1/VSCode2 (noms de projets
  internes, pas des livrables client) — utilise les noms réels des outils
  sources (Grille Assessment V3.2, Interview-to-Deck). Régénérer avec
  `python generate_deck.py` depuis ce dossier ; toute nouvelle version du
  cadrage qui change une affirmation déjà reprise en slide doit répercuter le
  changement ici, pas seulement dans le `.md` source. Piloté par l'agent
  `.claude/agents/ppt-designer.md` (voir aussi ci-dessous). Après toute
  modification : `python test_generate_deck.py` (suite de tests fonctionnels
  — structure, cadres photo alignés exactement sur leur cadre template,
  régression numéro de chapitre, obstructions de cadre en liste blanche,
  rendu réel via LibreOffice) **en plus** du rendu PowerPoint + relecture à
  l'œil (le test ne remplace pas l'œil sur la qualité d'une photo, juste sur
  son cadrage géométrique).
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

## Skills & agents — comment ça se lance (post-BMAD, 2026-07-16)

Depuis l'install de **BMAD-METHOD v6.10.0** (`_bmad/`), `.claude/skills/` contient ~46 skills `bmad-*` en plus des skills projet :

- **Routeur BMAD** : en cas de doute, invoquer **`bmad-help`**.
- **Agents BMAD (personas)** : par nom — « Amelia » (dev), « John » (PM), « Winston » (architecte), « Sally » (UX), « Mary » (analyste), « Paige » (tech writer) = skills `bmad-agent-*`. Workflows : `bmad-product-brief`/`bmad-prd`/`bmad-architecture`/`bmad-create-story`/`bmad-dev-story`, plus `bmad-code-review`/`bmad-retrospective`. Sorties → `_bmad-output/` (candidat `.gitignore`).
- **Skills projet** (non-`bmad-`) : `pptx-framed-image`, `slide-text-polish`, `revue-increment` (definition-of-done — délègue à `bmad-code-review`/`bmad-retrospective`).
- **Agent projet** `.claude/agents/ppt-designer.md` : sous-agent PPT antérieur à BMAD ; recoupe partiellement `bmad-agent-ux-designer` — préférer une seule voie par tâche.
- Le hook **SessionStart** (`.claude/hooks/remind_revue_increment.py`) rappelle la discipline et route vers `bmad-help`.

## Agent orchestrateur & superviseur (porté depuis VSCode2, 2026-07-21)

Config d'installation complète (skills + scripts + hooks) reprise depuis
`export/agent-orchestrator/` et `export/agent-supervisor/` de VSCode2, suivant la procédure
de son `README.md` §7. Deux étages qui se nourrissent mutuellement (le superviseur mesure,
l'orchestrateur applique) :

- **`agent-orchestrator`** (`.claude/skills/agent-orchestrator/SKILL.md`) : point d'entrée
  des demandes multi-étapes/multi-agents — qualifie, cherche un playbook matchant avant de
  composer à vide, exécute (cascade/parallèle/asynchrone), journalise dans
  `.claude/orchestration/runs.jsonl` (gitignoré). Routé par le hook `UserPromptSubmit`
  (`.claude/hooks/orchestrator_gate.py`, ~50 tokens, silencieux sur les commandes slash).
- **`agent-supervisor`** (`.claude/skills/agent-supervisor/SKILL.md`) : diagnostic
  qualitatif (étage 2) sur les données de l'étage 1 — à lancer depuis `revue-increment` ou
  quand le SessionStart signale un diagnostic périmé (cadence 14 j). Écrit
  `.claude/supervision/diagnostic.json` (gitignoré) via `write_diagnostic.py`.
- **Étage 1 (mesure, 0 token)** : `.claude/supervision/scan_transcripts.py` (hook
  SessionStart, scan incrémental) + `.claude/supervision/log_usage.py` (hook PostToolUse
  sur `Skill|Agent|Task`) → régénèrent `docs/wiki/technical/agents-supervision.md` et la
  section `TODO-AGENTS` de `docs/wiki/index.md`. `docs/wiki.html` a une section
  `TODO-AGENTS-HTML` prévue par le script mais ses marqueurs n'ont jamais été posés dans ce
  dépôt — le bloc HTML reste donc silencieusement non mis à jour tant qu'ils n'y sont pas.
- **`.claude/orchestration/catalogue.md` + `playbooks/`** : **adaptés**, pas copiés
  verbatim — `dev-verifie` a perdu son étape `run-dev-server` (pas d'app web/dev server
  ici), `export-ppt-verifie` référence le vrai pipeline (`generate_deck.py`, `pptx_deck.py`,
  `test_generate_deck.py`), `cycle-produit-bmad` est régénéré depuis le `bmad-help.csv` de
  **ce** dépôt (`py .claude/orchestration/generate_bmad_playbook.py` — ne jamais l'éditer à
  la main).
- **`docs/reflexions/agent-orchestrateur.md` / `agent-superviseur.md`** : conception
  d'origine, écrite dans le contexte de VSCode2 (précédents, arbitrages, phasage) — le
  rationale reste valable, mais les statuts d'usage/précédents cités y datent de ce
  projet-là, pas de celui-ci.
- Fraîchement installé : aucune mesure réelle n'existe encore côté VSCode3 (premier scan
  déjà lancé le 2026-07-21 : 46 skills BMAD + les 5 skills projet jamais invoqués sur ce
  dépôt). Ne pas se fier aux statuts « éprouvé » hérités des docs de conception — vérifier
  `docs/wiki/technical/agents-supervision.md` avant de router vers un agent « jamais
  utilisé ».
- Pas d'`.opencode/` (OpenHub) sur ce dépôt — la couverture correspondante de
  `scan_transcripts.py` reste optionnelle et no-op ici (base absente).
- **Tests** : `tests/test_agent_orchestration.py` + `tests/test_agent_supervision.py`
  (portés de VSCode2 le 2026-07-21, 28 tests) exercent les scripts en subprocess avec des
  chemins surchargés par env — aucun accès aux vrais transcripts/wiki. Rejouer après toute
  modif des scripts superviseur/orchestrateur : `py -m pytest tests/test_agent_*.py`
  (sur Windows, passer `--basetemp` sur un dossier neuf — le nettoyage du symlink
  `pytest-current` plante en teardown sinon, sans que ce soit un échec de test).
  `test_scan_counts_and_generates_page_and_index` a été adapté (échantillon
  `run-dev-server`, skill projet de VSCode2 inexistante ici → `revue-increment`).

## Hiérarchie de modèles pour les sous-agents (2026-07-16)

`ppt-designer` n'a pas de champ `model:` en frontmatter (hérite du thread principal) — délibérément laissé ainsi : c'est un rôle de jugement visuel (géométrie, mise en page, vérification par rendu réel), pas un rapport mécanique templaté, donc pas un bon candidat pour une bascule vers un modèle plus léger.

## Discipline de gestion des tokens (2026-07-16, cf. `docs/vscode1-export/optimisation-tokens.md`)

Le contexte est un cache actif facturé à chaque tour, pas une mémoire gratuite (source : OCTO Playbook Agentique, partie « Optimiser la consommation Tokens »). Règles concrètes, pas de changement de ton/style de réponse :

- **Ne pas parcourir** `_bmad/`, `_bmad-output/`, `__pycache__/` sauf demande explicite.
- **Lire avant d'écrire, grep les appelants avant de modifier** une section partagée (ex. `docs/wiki/`).
- **Préférer un grep/read ciblé à un dump récursif** — surtout sur `.claude/skills/bmad-*` (~46 skills).
- **Sous-agent pour toute sortie volumineuse** plutôt que de la laisser polluer le contexte principal.
- **`/compact` dès ~40 %** de fenêtre de contexte utilisée si la session doit continuer longtemps sur le même sujet.
