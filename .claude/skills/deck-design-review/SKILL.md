---
name: deck-design-review
description: Revue de design slide-par-slide du deck de synthèse de CE projet (cadrage BMAD IAP, docs/cadrage-ppt/generate_deck.py, 49 slides sur 8 chapitres, template OCTO rendu via LibreOffice) — régénérer le vrai export, rendre TOUTES les slides, et confronter chaque type de slide à son propre contrat de design (couverture, exec summary 5 blocs, intercalaires teardrop, personas, douleurs, gaspillages, gate IA, trajectoire, schémas, KPI, maturité). C'est L'ÉTAPE design-review du playbook export-ppt-verifie — obligatoire dès qu'une version ajoute ou restructure des slides — et elle se lance aussi à la demande quand le PPT exporté « n'est pas au niveau ».
---

# deck-design-review — la revue de design du deck ENTIER (cadrage IAP)

`pptx-verify` (skill globale) dit **comment** regarder (rendre + zoomer + checklist
générique) ; `deck-design-library` (locale) dit **quelle forme** donner à un contenu.
Ce skill ajoute le **contrat par slide de CE deck** — pour que chaque type de slide
soit revu contre SA définition, pas une impression d'ensemble. Adapté de la version
VSCode2 le 2026-07-24 (finding pratique-design du superviseur, « VSCode3 reste à
traiter ») — réécrit pour le canal réel de ce projet, pas copié.

## 0. Sur le BON artefact, TOUTES les slides

- Ce projet **n'a pas d'app qui tourne** : le deck est régénéré par
  `python generate_deck.py` depuis `docs/cadrage-ppt/` → `bmad-iap-cadrage-synthese.pptx`
  (dessiné sur `template-octo.pptx`). Ne jamais réviser sur un ancien export : régénérer
  d'abord. Les archives `-v2.3.pptx` / `-v2.4.pptx` ne se régénèrent pas — ignorer.
- Rendre **toutes** les slides au moteur réel (**LibreOffice `soffice`**, cf.
  `test_generate_deck.py:_soffice_path`), pas un échantillon — le rendu LibreOffice diffère
  de PowerPoint sur les polices et certains glyphes (voir § 2).

## 1. Contrat par type de slide

Le deck suit le fil rouge **SCALE en 8 chapitres** (01 Contexte · 02 Personas ·
03 Besoins & douleurs · 04 Proposition · 05 IA · 06 Démarche · 07 Outillage IAP ·
08 KPI), chaque chapitre = une couleur `D.PALETTE` (mapping en tête de `generate_deck.py`).

**Recâblée le 2026-09-01**, après 40 jours à zéro invocation : l'étape `design-review`
du playbook `export-ppt-verifie` nommait une AUTRE skill (`restitution-deck-design`),
elle-même jamais utilisée sur ce dépôt. Le projet payait deux instruments de revue de
design et n'en lançait aucun. L'étape pointe désormais ici, et n'est plus conditionnelle.

**TROU CONNU, à dire au lieu de le taire.** La table ci-dessous couvre **27 des 40**
fonctions `slide_*` du générateur (compte mesuré le 2026-09-07 : 34 au 2026-09-01 + 6
créées depuis, dont les 3 de la refonte graphique intégrée le 2026-09-04). Les 13
suivantes n'ont PAS de contrat écrit : `slide_ambition`, `slide_architecture_si`,
`slide_conditions_reussite`, `slide_export_markdown`, `slide_fil_humain`,
`slide_kpis_mise_en_place`, `slide_kpis_pourquoi_quoi`, `slide_mission`,
`slide_pourquoi_contexte`, `slide_qui_achete`, `slide_team_topologies`, `slide_vision`,
`slide_why_iap`. Une revue qui les traverse en silence rendrait un « tout va bien » qui
ne porte que sur les deux tiers du deck : les signaler comme NON REVUES fait partie du
verdict. Leur écrire un contrat est un travail à part, qui appartient à ce projet — il
n'a pas été fait ici, pour ne pas inventer des exigences de design sur des slides
qu'aucune mesure n'a instruites. **6 autres fonctions étaient un angle mort NON déclaré**
(créées après la dernière mesure du 2026-09-01, ni dans les 21 couvertes ni dans les 13
listées ci-dessus) — trouvées par l'audit du 2026-09-07 et comblées ci-dessous : ce
deuxième trou-là est clos, le premier (les 13) reste ouvert.

| Slide (fonction) | Contrat (au rendu) |
| --- | --- |
| `slide_cover` | Couverture de marque OCTO : titre = cadrage BMAD IAP, sous-titre, date. Bandeau métadonnées (statut/langue/confidentialité) **retiré** — ne pas le réintroduire. |
| `slide_executive_summary` | **5 blocs** OFFRE + POURQUOI / QUOI / COMMENT / RÉSULTAT (le bloc OFFRE a été acté le 2026-09-07, arbitrage utilisateur, suite à l'ajout du chapitre 01 Exec Summary — 4 blocs faisait référence avant cet ajout), avec renvois par CHAPITRE (jamais par numéro de page). |
| `slide_chapitre` | Intercalaire teardrop : **numéro DANS l'encart** + titre coloré (couleur du chapitre) + **vraie photo clippée au teardrop**. ⚠️ Le cadre teardrop est **CARRÉ** : juger sur la photo rendue (aspect `square`), pas sur un probe `wide`. Le numéro est une exigence PERSISTANTE. |
| `slide_sous_chapitre` | Bloc-titre léger, sans photo ni numéro. **Sans appelant depuis v2.6** : s'il réapparaît, c'est un régression. |
| `slide_personas` | Cartes **2×2** + pastille de posture (allié / sceptique / vigilant). Parité des 4 cartes (même gabarit). |
| `slide_personas_divergences` | Tensions inter-personas + une ligne de synthèse « pont » vers la Proposition. Glyphe ⟂ rendu par le connecteur texte « en tension avec », **pas** par le caractère. |
| `slide_douleurs` | Douleurs par persona, **mesurées** (pas de puce vague). |
| `slide_familles` | Les 8 familles de gaspillage — grille homogène. |
| `slide_gaspillages` | Méthode scorée (chaîne + score) ; couleur = score, pas identité. |
| `slide_gate_ia` | Doctrine « jamais la réponse à un problème d'abord organisationnel » — l'IA APRÈS la proposition, visuellement subordonnée. |
| `slide_trajectoire` | Timeline ①②③⟲ + ligne LIVRABLE-CLÉ + note de bifurcation. ⚠️ voir § 2 pour le glyphe ⟲. |
| `slide_activites_humaines` | Grille **2 registres × 4 temps** (outillé IAP vs purement humain). |
| `slide_schema_fonctionnement` / `slide_architecture_agents` / `slide_iap_contexte_client` | Schémas : boîtes alignées, zones colorées cohérentes avec le chapitre, renvois par badge de série (« cf. chapitre 07 »), jamais de flèche qui traverse une boîte. |
| `slide_kpis*` (3 familles) → `slide_maturite` → `slide_kpis_exemple` | Familles KPI homogènes ; la grille de maturité porte « à quoi sert chaque échelle » + message « le KPI = le DELTA T0→réévaluation, pas le niveau ». |
| `slide_agent_ia` / `slide_prudence_ia` | Cartes agent (why/what/gain) ancrées sur une famille de gaspillage réelle ; prudence = décomposition confidentialité/supervision/criticité. |
| `slide_pitch_iap` | 3 cartes côte à côte (douleurs vécues / outillage côté consultant / option côté client), badge-icône + couleur `D.PALETTE` distincte par carte (rouge / teal / violet), pied de carte en pastille colorée avec renvoi par CHAPITRE (jamais par page). Bandeau gris « matériau de cadrage » en pied de slide. |
| `slide_demarche_avec_sans_agentic` | Grille 3 étapes (①②③, badges NAVY communs sur une frise reliée par flèches — la démarche ne se dédouble JAMAIS) × 3 registres (sans outillage / avec le module côté consultant / agentic chez le client), une ligne « ce que ça change » entre les deux ; seule la couleur de FOND par registre change (gris-bleu / teal / violet), jamais les badges d'étape. |
| `slide_synthese_pourquoi_quoi_comment` | Frise de 5 phases (①②③⟲ + une étape OPTIONNELLE en cercle à CONTOUR POINTILLÉ marquée « + », jamais pleine comme les 4 autres) avec durée, description, repère TECH et livrable par phase ; 2 encarts « AGENTIQUE » (consultant / client) sous la frise. |
| `slide_offre_iap` | Chapo + citation-thèse VERBATIM (document source, ne pas reformuler) puis un schéma en 2 rangées (parcours de mission) où chaque forme suit l'une de 3 conventions déclarées dans une LÉGENDE EXPLICITE en pied de schéma : contour navy plein = mouvement du socle (toujours présent) ; contour or plein = variante conditionnée au contexte ; contour or POINTILLÉ = mécanisme additif (extension/checklist). Kicker « Démarche », couleur or (`D.PALETTE[3]`). |
| `slide_specificites_infra` | 2 paires « douleur → réponse » en cartes à coins arrondis reliées par un chevron (douleur bordure `MUTED`, réponse bordure `ACCENT`), plus un encart « avec l'arrivée de l'IA » distinct (badge rond « IA ») qui reformule la même douleur comme amplifiée — jamais résolue — par l'IA. |
| `slide_infra_as_product_exemple` | 2 cartes AVANT/APRÈS reliées par une flèche horizontale centrale, badge tagué en coin haut-gauche par carte ; items à tiret « — » côté AVANT vs coche « ✓ » (accent) côté APRÈS — jamais l'inverse. |

## 2. Transversal (tout le deck, à chaque revue)

1. **Police du THÈME partout** (Arial sur OCTO) — jamais une police non installée forcée
   (elle rend en substitution LibreOffice). Une seule famille attendue dans le zip.
2. ⚠️ **Glyphe ⟲ : la variante GRASSE manque** dans la police du template → LibreOffice
   rend une **case vide / tofu** dans un run bold. Tout badge/bandeau l'utilisant force
   `bold=False` pour ce seul caractère (`slide_trajectoire`, `slide_schema_*`,
   `slide_livrables_ppt`, en-tête « ⟲ RÉÉVALUATION » de `slide_kpis_exemple`). Vérifier
   au rendu réel qu'aucun ⟲ n'est en case vide.
3. **Échelle** : titres à l'échelle typo de `D.TYPE`, aucun point-size littéral hors token ;
   espacement cohérent de slide en slide.
4. **Couleur = un seul métier** : identité (couleur DU CHAPITRE) vs sémantique
   (vert/rouge/ambre d'un score) — jamais mélangées sur une même slide.
5. **Composants identiques partout** : une carte / un encart / un badge qui diffère d'une
   slide à l'autre est un défaut.
6. **Chrome** : rien ne recouvre le numéro de page, le logo, le pied — zoomer (crop) ces
   zones au moindre doute.
7. **Images** : vraies photos Openverse CC0, **photographiques** (une illustration/clipart
   dans une requête générique est un défaut) ; le procédural (`nature_images.py`) n'est
   acceptable qu'hors réseau. Toujours juger la photo au rendu réel — la recherche par
   mot-clé n'a aucun jugement.

## 3. Boucle

Régénérer (`python generate_deck.py`) → défauts listés **par n° de slide** (crops si
subtil) → corriger → re-générer → **re-rendre** (jamais « corrigé » sans re-rendu réel
LibreOffice). Un invariant découvert devient un test dans `test_generate_deck.py` (le test
verrouille le défaut trouvé, l'œil trouve le suivant). Pour un changement d'INTENTION de
design : **validation utilisateur sur le rendu réel avant commit** (non-convergence :
l'utilisateur est l'oracle sur SON artefact, ne pas re-deviner à l'aveugle).
