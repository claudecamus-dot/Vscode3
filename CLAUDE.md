# CLAUDE.md

Cadrage BMAD IAP : le livrable est un deck de synthèse (`docs/cadrage-ppt/`,
40 slides sur le vrai template OCTO). L'historique des versions du deck vit dans
`git log docs/cadrage-ppt/` — ne pas le re-narrer ici.

## Commandes

- Régénérer le deck : `python generate_deck.py` depuis `docs/cadrage-ppt/`.
- Après toute modif du générateur : `python test_generate_deck.py` (structure, cadres
  photo, régression numéro de chapitre, obstructions en liste blanche, rendu réel
  LibreOffice) **en plus** du rendu PowerPoint + relecture à l'œil — le test valide le
  cadrage géométrique, pas la qualité d'une photo.
- Scripts superviseur/orchestrateur : `py -m pytest tests/test_agent_*.py` (sur Windows,
  passer `--basetemp` sur un dossier neuf — le nettoyage du symlink `pytest-current`
  plante en teardown sinon, sans que ce soit un échec de test).

## Claude Code project setup

- `.claude/settings.json` (versionné) : hooks `PreToolUse` sur `Bash|PowerShell` —
  `guard_destructive_git.py` (bloque `git push --force` sans lease, `git reset --hard`,
  lecture de `.env`/`secrets/**`/`config/credentials.json`) et
  `warn_verif_before_commit.py` (rappel non bloquant : vérif réelle avant commit de
  `docs/cadrage-ppt/`).
- `.claude/settings.local.json` et `CLAUDE.local.md` (gitignorés) : réglages machine.
- `.claude/skills/` projet : `pptx-framed-image`, `slide-text-polish` (greffées de
  VSCode1, vendored — invoquées en Python par le pipeline deck, PAS via l'outil Skill),
  `revue-increment`, `deck-design-library` (greffée de VSCode2, copie de référence —
  resynchroniser manuellement). `.claude/agents/ppt-designer.md` : agent projet qui
  pilote `generate_deck.py` — voie unique deck (arbitrage 2026-07-21).
- `docs/vscode1-export/` : miroir local du kit PPT de VSCode1 — copie de référence,
  pas la source de vérité.

## Deck (`docs/cadrage-ppt/`) — état courant et contraintes durables

- **v2.6, 8 chapitres sur le fil SCALE** (01 Contexte · 02 Personas · 03 Besoins &
  douleurs · 04 Proposition · 05 IA · 06 Démarche · 07 Outillage IAP · 08 KPI) ;
  executive summary en 4 blocs POURQUOI/QUOI/COMMENT/RÉSULTAT ; renvois entre slides
  par CHAPITRE, jamais par numéro de page. Doctrine : l'IA reste tirée APRÈS la
  proposition (`slide_gate_ia`), jamais la réponse à un problème d'abord
  organisationnel.
- Les exports archivés `-v2.3.pptx` / `-v2.4.pptx` ne se régénèrent pas. La slide
  « Conditions de réussite » du plan v2.5 reste **à décider** — pas un oubli de build.
- **Séparateurs** : chapitres = intercalaire teardrop (photo + numéro,
  `slide_chapitre`) ; `slide_sous_chapitre` est conservé mais sans appelant depuis v2.6.
- ⚠️ **Cadre teardrop CARRÉ** : le build fetche en aspect `square`, souvent une photo
  différente d'un probe `wide` — juger sur la slide rendue, pas sur un probe.
- ⚠️ **Glyphe ⟲ : la variante grasse manque** dans la police du template (LibreOffice
  rend une case vide) — tout badge/bandeau l'utilisant force `bold=False` pour ce
  caractère.
- **Photos** : vraies photos Openverse CC0 via `stock_images.py` (repli procédural
  `nature_images.py` hors réseau) ; **toujours vérifier chaque photo au rendu réel**
  (la recherche par mot-clé n'a aucun jugement). `_img/` gitignoré (régénérable),
  provenance dans `images-manifest.json` (versionné).
- Ne pas référencer VSCode1/VSCode2 dans le deck (noms internes) — utiliser les noms
  réels des outils (Grille Assessment V3.2, Interview-to-Deck).
- Toute nouvelle version du cadrage qui change une affirmation reprise en slide doit
  répercuter le changement dans le générateur, pas seulement dans le `.md` source.
- `analyse-template-alternatif.md` : analyse (sans implémentation) d'un second template
  vu dans VSCode2 — pistes retenues/écartées, template non copié (contenu client).

## Optimisation tokens (cf. `docs/vscode1-export/optimisation-tokens.md`)

- Ne pas re-dériver ce que le wiki (`docs/wiki/`) ou une mémoire documente déjà.
- Lire des portions ciblées (Grep/Glob puis Read offset/limit) — le wiki fait
  ~1800 lignes, le cadrage BMAD IAP ~99K.
- Ne pas parcourir `_bmad/`, `_bmad-output/`, `__pycache__/` sauf demande explicite.
- Sous-agent pour toute sortie volumineuse ; sinon pas de sous-agent par défaut
  (dépôt petit, contexte déjà chargé).
- Documenter une décision actée (wiki/mémoire) plutôt que la rejouer ;
  `/compact` dès ~40 % de contexte si la session continue longtemps.

## Skills & agents — comment ça se lance (post-BMAD v6.10.0)

- **Routeur BMAD** : en cas de doute, invoquer `bmad-help`. Agents personas par prénom
  (« Amelia » dev, « John » PM, « Winston » archi, « Sally » UX, « Mary » analyste,
  « Paige » tech writer). Sorties → `_bmad-output/`.
- `ppt-designer` recoupe partiellement `bmad-agent-ux-designer` — une seule voie par
  tâche (arbitrage : ppt-designer pour le deck).
- Le hook SessionStart (`remind_revue_increment.py`) rappelle la discipline.

## Agent orchestrateur & superviseur (porté de VSCode2)

- **`agent-orchestrator`** : demandes multi-étapes — qualifie, cherche un playbook,
  journalise dans `.claude/orchestration/runs.jsonl` (gitignoré). Routé par le hook
  `UserPromptSubmit` (`orchestrator_gate.py`).
- **`agent-supervisor`** (étage 2) : diagnostic qualitatif sur les mesures de l'étage 1
  (`scan_transcripts.py` en SessionStart + `log_usage.py` en PostToolUse) → écrit
  `diagnostic.json` via `write_diagnostic.py`. Cadence 14 j.
- `docs/wiki.html` n'a pas les marqueurs `TODO-AGENTS-HTML` — le bloc HTML n'est pas
  mis à jour tant qu'ils n'y sont pas posés.
- **`catalogue.md` + `playbooks/`** : adaptés à CE dépôt (pas de `run-dev-server` ;
  `export-ppt-verifie` référence le vrai pipeline). `cycle-produit-bmad.md` est généré
  (`py .claude/orchestration/generate_bmad_playbook.py`) — ne jamais l'éditer à la main.
- **Arbitrages** : la source de vérité est `.claude/supervision/arbitrages.json`
  (versionné, jamais écrit par le scan) — voie unique deck, skills vendored
  `used-as-library` (toujours listées « jamais utilisées », ne pas les retirer au tri),
  jeton `famille:BMAD` (ferme le TODO d'élagage, les 46 restent mesurées), tri BMAD
  A/B/C/D/E documenté. Une cible arbitrée sort des TODO mais reste mesurée.
- Ne pas se fier aux statuts « éprouvé » hérités des docs de conception VSCode2 —
  vérifier `docs/wiki/technical/agents-supervision.md` avant de router.
- Pas d'`.opencode/` ici — la couverture OpenHub de `scan_transcripts.py` est no-op.

## Hiérarchie de modèles pour les sous-agents

`ppt-designer` n'a pas de champ `model:` (hérite du thread principal) — délibéré :
rôle de jugement visuel, pas un rapport mécanique templaté.
