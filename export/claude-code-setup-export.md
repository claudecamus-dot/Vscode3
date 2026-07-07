# Export de configuration Claude Code — pour réintégration dans un nouveau projet

Ce document recense ce qui, dans la configuration Claude Code et les pratiques
de VSCode3, est **réutilisable tel quel** dans un autre projet, par opposition
à ce qui est spécifique à ce dépôt (le contenu du cadrage BMAD IAP). Objectif :
bootstrap rapide d'un nouveau projet — ou mise à niveau d'un projet existant —
sans redécouvrir ces réglages depuis zéro. Suit le même gabarit que
`docs/claude-code-setup-export.md` dans le projet frère VSCode2, en y ajoutant
ce qui a été établi depuis (wiki d'onboarding, pratiques agentic de cadrage).

**Cible actuelle de réintégration : VSCode1** (voir §8 pour un plan d'action
concret et daté, basé sur un vrai constat de ce qui y manque).

## 1. Fichiers projet à copier tels quels

### `.claude/settings.json` — copier la structure, PAS le contenu en l'état

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash|PowerShell",
        "hooks": [{ "type": "command", "command": "py .claude/hooks/guard_destructive_git.py", "timeout": 10 }]
      }
    ]
  },
  "permissions": {
    "disableBypassPermissionsMode": "disable",
    "deny": ["Read(./.env)", "Read(./secrets/**)", "Read(./config/credentials.json)"]
  }
}
```

Ce qui est réutilisable : le mécanisme de hook `PreToolUse` sur `Bash|PowerShell`,
et le pattern `permissions.deny` pour bloquer la lecture de secrets — adapter les
chemins à la structure du nouveau projet.

⚠️ **Ne pas copier `permissions.allow` tel quel.** Cette liste s'accumule au fil
des sessions avec des commandes one-off (chemins absolus machine-spécifiques,
UUID de scratchpad temporaires, fichiers de test ponctuels supprimés depuis) —
c'est du bruit accumulé, pas un réglage intentionnel. Repartir d'une liste vide
et laisser l'auto-approbation se reconstruire naturellement sur le nouveau projet.

### `.claude/hooks/guard_destructive_git.py` — copier tel quel

Garde-fou déterministe (pas une instruction de prompt) bloquant `git push --force`
(sans `--force-with-lease`) et `git reset --hard`. Agnostique du projet, aucune
adaptation nécessaire. Points d'implémentation à connaître si on l'étend :
- Fail-open : toute erreur de parsing laisse passer plutôt que de bloquer à tort.
- Découpe la commande en segments (`&&`, `||`, `;`, `|`, saut de ligne) sans se
  faire piéger par ces caractères à l'intérieur de guillemets.
- Neutralise d'abord le contenu des heredocs (`<<EOF ... EOF`) avant de chercher
  les motifs interdits — sans ça, un message de commit qui *décrit* la commande
  bloquée déclenche un faux positif.

### `.gitignore` — entrées Claude Code + roadmap

```gitignore
# Claude Code — réglages/notes propres à une machine ou une personne (jamais
# partagés), à distinguer de .claude/settings.json et .claude/skills|hooks|
# agents/ qui eux restent versionnés pour toute l'équipe.
.claude/settings.local.json
CLAUDE.local.md

# Roadmap — .roadmap/roadmap.json est la source de vérité versionnée ;
# le .svg est régénéré à la demande par le skill roadmap-keeper.
.roadmap/*.svg
```

## 2. Structure de `CLAUDE.md` à répliquer

Sections qui ont fait leurs preuves, dans cet ordre :

1. **Un paragraphe de contexte projet** : ce que fait l'app (ou, pour un dépôt
   documentaire comme VSCode3, ce que contient le dépôt), le vocabulaire métier
   à préserver tel quel, pointeur vers un roadmap et des docs plus profonds —
   avec un avertissement explicite s'ils peuvent être obsolètes.
2. **Commandes** : setup/run/test, copier-collables telles quelles.
3. **Architecture** : le flux de requête (couches), le modèle de données, puis
   une sous-section par module non trivial avec **des décisions non
   redérivables du code** (le « pourquoi », pas le « quoi »).
4. **Section « Claude Code project setup »** explicite : quels fichiers sont
   versionnés vs locaux, ce que bloque le hook, quels skills projet existent.

> **Enseignement propre à VSCode3** : un projet qui démarre sans code applicatif
> peut légitimement garder les sections « Commandes » et « Architecture » vides
> dans un premier temps — le squelette de titres signale ce qui est *attendu*
> avant même d'avoir du contenu à y mettre, plutôt que d'omettre la section et
> de la rajouter plus tard sans structure de référence.

## 3. Pattern de skill projet-local

Un skill projet (`.claude/skills/<nom>/SKILL.md`) documente une séquence
opérationnelle déjà découverte une fois. Gabarit qui fonctionne bien :
- Frontmatter avec `description` qui **nomme explicitement les déclencheurs**
  plutôt qu'une description vague.
- Sections numérotées, une par sous-capacité.
- Commandes **copier-collables**, pas de prose descriptive.
- Pièges d'environnement documentés explicitement.

## 4. Skills globaux (utilisateur) mobilisés par ce projet

Vivent dans `~/.claude/skills/` (partagés entre tous les projets, pas à copier
dans le dépôt) :

- `artifact-design` — calibrer l'investissement de design avant de produire une
  page HTML/Markdown ; a directement informé la palette/typographie/composants
  du wiki `docs/wiki.html` (voir §6).
- `roadmap-keeper` — suivi visuel Réflexion/Conception/Réalisation avec
  tracking optionnel de consommation de tokens ; démarre par un gabarit prêt à
  l'emploi (`{skill-root}/assets/starter-roadmap.json`), rendu en SVG autoporté
  sans dépendance navigateur.
- `code-review` / `simplify` — revue et nettoyage du diff courant (pas encore
  exercés sur VSCode3, dépôt sans code applicatif à ce stade).

## 5. Suivi de roadmap (`.roadmap/`)

- `.roadmap/roadmap.json` **versionné** (source de vérité éditable) ;
  `.roadmap/*.svg` **gitignoré** (régénéré à la demande par `roadmap-keeper`).
- `CLAUDE.md` doit préciser explicitement que ce fichier peut être en avance ou
  en retard sur le code réel — vérifier contre `git log`/`git status` avant de
  lui faire confiance.
- **VSCode1 est déjà la référence pour cette pratique** — `.roadmap/roadmap.json`
  y suit un modèle Epic/US (`epics[]` avec `subItems[]` statutés) plus riche que
  le modèle `items[]` simple utilisé sur VSCode3 ; s'en inspirer plutôt que
  l'inverse si le nouveau projet a une notion d'Epic/US établie.

## 6. Pattern wiki d'onboarding + rendu HTML autonome

Établi sur VSCode3 par réplication puis extension du pattern `docs/wiki/` de
VSCode2. Deux couches distinctes, à copier ensemble :

### 6.1 — Sources Markdown (`docs/wiki/`)

```
docs/wiki/
  index.md                          ← vue d'ensemble : god nodes, carte des domaines, points critiques, zones d'ombre
  business/index.md                 ← domaine métier : vue d'ensemble, concepts transversaux, utilisateurs cibles
  technical/stack.md                ← dépendances, variables d'env, contraintes de version
  technical/architecture.md         ← structure globale, arborescence, décisions notables, fragilités connues
  technical/conventions.md          ← linting, nommage, git, secrets, patterns d'équipe
  technical/tests.md                ← frameworks, organisation, seuil de couverture, philosophie
```

Chaque fichier porte un frontmatter `updated` / `confidence` (`confirmed` /
`mixed`) / `agents: [onboarder]`, et chaque assertion de fond est suivie d'un
tag de confiance en ligne : `` `CONFIRMÉ` ``, `` `DÉDUIT` `` ou `` `INCERTAIN` ``,
suivi de `agent · date · fichier:ligne source`. Règle : ne jamais poser
`CONFIRMÉ` sans un fichier source précis à citer ; `DÉDUIT` pour une inférence
raisonnable non vérifiée ligne à ligne ; `INCERTAIN` pour une hypothèse ouverte.
Ce triplet est directement hérité d'OpenHub (projet frère VSCode2) — le
réutiliser tel quel plutôt qu'inventer une échelle de confiance différente par
projet évite l'incohérence entre dépôts qui partagent des lecteurs.

### 6.2 — Rendu HTML autonome (`docs/wiki.html`)

Un seul fichier HTML, aucune dépendance externe, aucune étape de build —
ouvrable directement dans un navigateur (`file://`) ou publié comme Artifact.
Design system à copier tel quel (tokens CSS + classes de composants) :

**Tokens de couleur** (definis en `:root`, redéfinis sous
`@media (prefers-color-scheme: dark)` et sous `:root[data-theme="dark|light"]`
pour respecter le thème du viewer dans les deux sens) :
`--bg`, `--surface`, `--surface-2`, `--ink`, `--ink-soft`, `--ink-faint`,
`--line`, `--line-soft`, `--accent`/`--accent-soft`/`--accent-ink`,
`--confirmed`/`--confirmed-soft`, `--deduit`/`--deduit-soft`,
`--incertain`/`--incertain-soft` (ces trois dernières paires **doivent** rester
alignées sur les tags CONFIRMÉ/DÉDUIT/INCERTAIN du §6.1 — même vocabulaire
sémantique, pas une palette décorative indépendante).

**Typographie** : une display serif de caractère pour les titres (VSCode3 a
choisi Charter — éviter la même combinaison cream/serif/terracotta que
n'importe quel autre projet, en choisir une propre à chaque nouveau contexte),
une sans-serif système pour le corps, une mono pour code/chemins de fichiers.

**Classes de composants réutilisables** :
- `.sidebar` / `.toc-group` / `.toc-link` — navigation sticky par ancres, groupée par thème.
- `.fact` (bordure gauche neutre, claim sourcée) et son modificateur `.fact.accent` (bordure accent — clarification/décision) ; `.fact-label` pour la légende en tête de bloc.
- `.critical` (bordure/fond incertain — avertissement, point bloquant, tension).
- `.tag`/`.tag-confirme`/`.tag-deduit`/`.tag-incertain` — pastilles de tag de confiance.
- `.chip-row`/`.chip-pill`/`.chip-d0`..`.chip-d4` — pastilles de classification à 5 niveaux (réutilisé pour la classification de données D0–D4 du cadrage BMAD IAP, mais générique à toute échelle à 5 crans).
- `.table-wrap`+`table` — tables avec défilement horizontal propre sur mobile.
- `.tree` — bloc de diagramme ASCII/formule en police mono, fond `--surface-2`.
- `.stat-grid`/`.stat-card` (KPI en grille) et `.stat-strip` (KPI en ligne, plus léger).
- `.decision-grid`/`.decision-row`/`.decision-tag` — liste compacte de décisions taguées.
- `.mvp-timeline`/`.mvp-step`/`.mvp-step.future`/`.mvp-label` — frise verticale à puces, réutilisée aussi bien pour une roadmap MVP que pour un résumé texte de roadmap Réflexion/Conception/Réalisation (voir `docs/wiki.html` §Roadmap du projet sur VSCode3).
- `.agent-grid`/`.wf-list`/`.agent-card`/`.wf-card` — cartes de liste pour des inventaires (agents, workflows, ou tout catalogue similaire).
- `.shadow-list` — liste à puces « ? » pour des zones d'ombre/incertitudes.

**Pattern de composition à deux couches** : le fichier peut porter à la fois un
wiki d'onboarding court (§6.1) *et* la transcription intégrale d'un document de
référence plus long (sur VSCode3 : les 22 sections du cadrage BMAD IAP fusionnées
dans la même page, sous un second groupe de navigation dédié). Les deux
coexistent dans un seul fichier auto-porté plutôt que d'exiger un site multi-pages
ou un moteur de rendu Markdown — utile quand le nouveau projet a, comme
VSCode1, un document de cadrage volumineux (`cadrage/epics-us.md`,
`cadrage/experience-map.md`…) à rendre consultable sans quitter le wiki.

## 7. Pratiques agentic établies pendant le cadrage BMAD IAP

Enseignements de méthode, indépendants du contenu métier, à réappliquer sur
tout exercice de cadrage/revue similaire :

- **Tags de confiance sur les assertions de cadrage** (voir §6.1) — pas
  seulement pour du code onboarding, aussi pour des décisions de scope.
- **Règle dure par défaut + dérogation tracée**, plutôt qu'un choix binaire
  « règle stricte vs jugement libre » : quand une tension de gouvernance oppose
  un garde-fou anti-anti-pattern à l'arbitrage humain, trancher pour la règle
  dure par défaut, mais exiger qu'une dérogation soit consignée comme une
  décision à part entière (Statut/Contexte/Décision/Conséquences/Alternatives
  rejetées) et contre-signée par un rôle de revue — ni rigidité totale ni
  liberté totale.
- **Owner + échéance sur les points ouverts du cadrage lui-même**, pas
  seulement sur les décisions produit qu'il documente — un cadrage qui impose
  un format ADR strict à ses décisions mais laisse sa propre liste de
  questions ouvertes sans responsable ni horizon reproduit, à son propre
  niveau, l'anti-pattern qu'il dénonce ailleurs.
- **Redaction rétroactive dès détection** — si un document de cadrage contient
  des noms de clients réels ou une donnée identifiante, corriger immédiatement
  (alias sectoriels, chiffres généralisés) plutôt que de la noter comme point
  ouvert à traiter plus tard ; documenter que la redaction a été appliquée, à
  quelle date, par qui.
- **Dépendances externes versionnées et revues** — quand un cadrage réutilise
  un artefact d'un projet frère (une grille de maturité, un contrat d'agent),
  consigner une version pinnée, un fichier de référence local, et un
  déclencheur explicite de resynchronisation (boucle de réévaluation, jalon de
  projet) — jamais une dépendance flottante sans mécanisme de revue.

## 8. Plan de réintégration concret — VSCode1

Constat réel (pas un principe générique) au moment de la rédaction de ce
document : VSCode1 n'a **aucun** des fichiers `.claude/` listés en §1, et
**aucun** `CLAUDE.md` à la racine. Il a en revanche déjà `.roadmap/roadmap.json`
(avec un modèle Epic/US plus riche que celui de VSCode3, voir §5) et un skill
projet `.claude/skills/restitution-ppt`.

| Action | Statut sur VSCode1 | Priorité |
|---|---|---|
| Ajouter `.claude/settings.json` (hook + `permissions.deny`) | Absent | Haute — aucun garde-fou destructif actif aujourd'hui |
| Ajouter `.claude/hooks/guard_destructive_git.py` | Absent | Haute — dépend de l'action précédente |
| Nettoyer `permissions.allow` existant | Présent mais très bruité (chemins absolus machine-spécifiques, commandes one-off de debug) | Moyenne — pas bloquant, mais à assainir avant qu'il ne serve de modèle à un futur projet |
| Créer un `CLAUDE.md` racine (voir §2) | Absent | Haute — actuellement rien ne documente pour Claude Code la structure `app/` / `cadrage/` / `.roadmap/` déjà décrite dans `README.md` |
| Ajouter `docs/wiki/` + `docs/wiki.html` (voir §6) | Absent | Moyenne — VSCode1 a déjà des docs fonctionnelles (`cadrage/*.md`) mais rien au niveau onboarding technique confiance-tagué ; un bon candidat pour transcrire `cadrage/epics-us.md` et `app/README.md` dans le même pattern |
| `.roadmap/` | Déjà conforme, plus riche (Epic/US) que VSCode3 | Aucune action — VSCode3 devrait plutôt s'aligner sur VSCode1 ici |

Sur VSCode1, la vraie plus-value immédiate est **HAUTE** : un dépôt avec du
code applicatif réel (Node.js/Express, base SQLite, exports PPT) et **aucun**
garde-fou anti-destructif ni fichier `CLAUDE.md` est le profil exact que ce
mécanisme est censé protéger.
