# Epics et stories — VSCode3

Amorçage story-obligatoire, 2026-10-28, à compléter avec le PO. Document minimal : seules les stories
observables dans le dépôt sont écrites ; tout ce qui est une hypothèse est marqué « à confirmer par le PO ».
Objet du projet (source : `README.md`, `CLAUDE.md`) : cadrage BMAD IAP, dont le livrable est un deck de
synthèse (`docs/cadrage-ppt/`) dessiné sur le template de marque OCTO.

## Epic 1 : Socle existant et travaux en cours

Maintenir le livrable (deck de cadrage) régénérable et testé, et suivre les chantiers visibles dans l'arbre de travail.

### Story 1.1: Garder le deck de cadrage régénérable et ses tests verts

En tant que responsable du cadrage BMAD IAP,
je veux que le deck de synthèse se régénère et que ses tests passent,
afin de ne livrer qu'un deck dont la structure et le rendu ont été vérifiés.

**Statut : en cours, non revérifié aujourd'hui** (commandes documentées dans `CLAUDE.md` ; modifications non commitées sur `docs/cadrage-ppt/*` et `tests/test_livrable_deck_present.py`, nouveau `docs/cadrage-ppt/generate_offre_v2.py` et `tests/test_generate_offre_v2.py` non suivis ; périmètre exact à confirmer par le PO)

**Acceptance Criteria [3 critères]:** (sources : `CLAUDE.md`, `README.md`, `docs/cadrage-ppt/`)

- AC1.1.1 — **Given** le dépôt à jour, **When** on lance `python generate_deck.py` depuis `docs/cadrage-ppt/`, **Then** le deck est régénéré sans erreur (non exécuté).
- AC1.1.2 — **Given** le générateur modifié, **When** on lance `python test_generate_deck.py` depuis `docs/cadrage-ppt/`, **Then** le test passe, rendu LibreOffice compris (non exécuté).
- AC1.1.3 — **Given** le dépôt, **When** on lance `py -m pytest tests/` (avec `--basetemp` sur un dossier neuf sous Windows), **Then** tous les tests passent ; le compte n'est pas figé ici (non exécuté).

### Story 1.2: Moteur GMAH canari, désactivé

En tant que propriétaire de la flotte,
je veux que le moteur GMAH reçu du hub reste éteint dans VSCode3,
afin que ce projet serve de canari sans activer le mode par accident.

**Statut : fait côté livraison** (commit `bb7d569`, « moteur GMAH (canari, désactivé) depuis le hub ») ; **désactivation lue aujourd'hui** : `.claude/orchestration/etat.json` absent, `.claude/hooks/provenance_gmah.py` absent, aucune occurrence de `provenance` dans `.claude/settings.json` ; la clé de provenance n'a pas été recherchée hors dépôt (non exécuté, à confirmer par le PO)

**Acceptance Criteria [3 critères]:** (sources : `.claude/orchestration/gravite.py`, `.claude/settings.json`)

- AC1.2.1 — **Given** le dépôt, **When** on liste `.claude/orchestration/`, **Then** aucun `etat.json` actif n'existe (vérifié 2026-10-28 : absent).
- AC1.2.2 — **Given** le dépôt, **When** on cherche `provenance` dans `.claude/settings.json` et `provenance_gmah.py` dans `.claude/hooks/`, **Then** aucun hook de provenance n'est branché (vérifié 2026-10-28 : 0 occurrence, fichier absent).
- AC1.2.3 — **Given** le poste, **When** on cherche une clé de provenance GMAH (`%APPDATA%/claude-gmah/jeton.key`, chemin cité par le hub), **Then** aucune clé n'existe pour ce projet (non exécuté, chemin à confirmer par le PO).

### Story 1.3: Isoler le travail de réorganisation de `docs/` avant de le valider

En tant que responsable du dépôt,
je veux que la réorganisation des dossiers `docs/` (`docs/exports/`, `docs/imports/`) soit validée et commitée à part,
afin qu'elle ne se mélange pas aux changements du deck.

**Statut : ouvert, hypothèse** (l'index git contient des renommages `docs/Import/` vers `docs/imports/`, `docs/reflexions/` vers `docs/exports/reflexions/`, etc., posés par une autre session ; intention et propriétaire à confirmer par le PO)

**Acceptance Criteria [2 critères]:** (sources : `git status --short`, `README.md`)

- AC1.3.1 — **Given** la réorganisation validée, **When** on lance `git diff --cached --name-only`, **Then** seuls des chemins de `docs/` renommés y figurent (non exécuté sous cette forme).
- AC1.3.2 — **Given** la réorganisation commitée, **When** on ouvre les liens de `README.md` (`docs/exports/cadrage/product-brief.md`, `docs/exports/cadrage/bmad-iap-cadrage.md`), **Then** les fichiers existent (non exécuté).
