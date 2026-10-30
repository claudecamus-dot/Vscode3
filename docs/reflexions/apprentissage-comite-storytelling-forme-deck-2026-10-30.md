# Apprentissages : comités « fil rouge » et « forme » sur le deck Offre Infra as a Product (VSCode3)

Origine : session VSCode3 du 2026-10-30, à la demande de l'utilisateur (« trace ces apprentissages pour le hub et envoie lui ce message »), après les comités multi-tours lancés par `/orchestre` (storytelling, puis forme des slides) et les versions V20 à V24 du deck.
Statut : constats et propositions, à arbitrer par le hub. Tout chiffre cite sa source ; « rapport d'agent » = relevé par un sous-agent, non rejoué ; sinon « non mesuré ».

## 1. Constats de méthode (comités)

- **La forme a été optimisée alors que la demande portait sur le récit.** Rétrospective par agent sur les docstrings des deltas V9 à V19 : 9 versions sur 11 portent sur cartes, en-têtes, polices ; aucune relecture du deck « comme une histoire » avant l'utilisateur (rapport d'agent, non rejoué). Les comités qui ont corrigé le tir (3 tours, 7 agents) ont d'abord extrait la **suite des titres** de la V19 puis celle de 4 offres de référence.
- **Un agent audite mieux quand il regarde le rendu, et un second lecteur corrige le premier.** Audit visuel de la V22 (2 bras × 23 slides rendues et lues) puis 2 concepteurs : ils ont infirmé 3 constats du premier tour, p. ex. « carte 1 cyan » faux sur la slide 5 (seul le disque numéro 1 l'était), « marge basse nulle » non confirmée sur la slide 23, et écarté des actions qui obligeaient à ajouter du texte (rapports d'agents).
- **Confusion d'unités dans 2 audits sur 2** : les rendus font 1280 × 720 px pour 720 × 405 pt (1 px = 0,5625 pt) ; les deux audits citent des « pt » qui sont des pixels (constaté à la lecture des rapports ; corrigé au tour suivant). Règle utile pour un brief : donner l'échelle du rendu.
- **Durées relevées (`duration_ms` des notifications de tâche)** : tour 1 « storytelling » 317 s, 2 867 s, 2 785 s, 2 876 s pour un budget déclaré de 12 min par bras (3 bras sur 4 à ×4 le budget, sans interruption) ; tour 2 : 343, 136, 139 s ; tour 3 : 217 s. Comité « forme » : 113, 118, 332, 513 s puis 418 et 430 s.
- **Corpus de comparaison** : 458 `.pptx` hors VSCode3 sous Téléchargements et Documents (`Get-ChildItem -Recurse -Include *.pptx`, filtré), très majoritairement des dossiers de mission et des doublons ; les agents n'ont trouvé aucune offre « infra » ni aucun prix exploitable (rapports d'agents). Conséquence : le comité ne peut dire que la forme et le récit, pas le contenu commercial.

## 2. Constats outils (`deck_delta`)

- **Un livrable n'est jamais écrasé, et la sortie est numérotée automatiquement** (dernier livrable + 1) : relancer le même delta après un correctif crée une version de plus (ici V22 puis un doublon V23, supprimé). Le nom du fichier delta ne commande pas le numéro de sortie. Proposition : un `--sortie` explicite, ou un refus « identique à la dernière version ».
- **Fragilité de chaîne d'import** : `delta_V9` résout sa base au chargement ; après archivage des versions anciennes, tout delta qui l'importe (V10, V11, V16, V19) échoue avec `REFUS : base introuvable : 'V8' (ni fichier, ni version de …\docs\exports\decks)`. Constaté le 2026-10-30 ; contourné en rendant `delta_V20` autonome. Proposition : ne rien résoudre à l'import, sortir les helpers dans un module sans base.
- **Ordre des calques** : les formes ajoutées sont posées au premier plan ; une pastille navy envoyée à l'arrière avant sa carte est passée SOUS la carte (texte blanc invisible, vu au rendu de la slide 40 de la première tentative du lot D). Un helper « envoyer à l'arrière » doit être appliqué dans l'ordre carte puis pastille. Le garde géométrique ne peut pas le voir.
- **Le garde de débordement a joué son rôle** : texte de carte monté de 9,5 à 10,5 pt sur la slide 29 → `REFUS : garde_rendu : 35 défaut(s) contre 33 dans la base` ; après réglage 33 contre 33. Mais « rendu réel non vérifié » reste écrit : le rendu regardé est resté obligatoire (les six slides retouchées ont été relues à l'œil ; les 40 autres non).
- **Mode GMAH « augmenté » non activable** : `ADOPTE GMAH AUGMENTE` tapé par l'utilisateur ; l'arbitrage `hub:gmah` est écrit, mais `gravite.py status` reste `plafond_bras=4` car `.claude/orchestration/gravite/jetons.jsonl` ne porte que des jetons de type `adopte` (aucun `adopte-augmente` émis) et `provenance_gmah_cible.py` n'a aucune occurrence de « augment » (grep). Le comité du jour a donc tourné à 4 bras par tour.

## 3. Ce qui a servi (à reprendre ailleurs)

- Extraction de la suite de titres + tableau « demande → slide → critère mesurable par script » avant toute version ; plan en lots de ~6 slides, un delta par lot, rendu regardé entre deux lots.
- Un concepteur par moitié du deck avec lecture de la géométrie réelle (noms de formes, coordonnées en pt) plutôt que de la seule capture.

## À arbitrer côté hub

1. Corriger `provenance_gmah_cible.py` pour émettre `adopte-augmente` sur la phrase `ADOPTE GMAH AUGMENTE`, puis resynchroniser les projets.
2. Kit `deck-ppt-qualite` : `deck.py` sans résolution de base à l'import ; sortie explicite ou refus d'un doublon de la dernière version.
3. Règle de brief pour les agents qui regardent un rendu : donner l'échelle px/pt, exiger le nombre de slides réellement regardées, faire relire le constat par un second agent contre la géométrie.
4. Étape « suite de titres lue comme une histoire » avant toute version d'un deck (playbook `export-ppt-iteration`), avec critères d'acceptation par demande soumis à l'utilisateur.
5. Plafond de durée effectif pour un bras de comité (3 bras sur 4 à ×4 le budget déclaré sans arrêt) : relier le budget à `convergence.py`.
