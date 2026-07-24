---
name: deck-design-review
description: Revue de design slide-par-slide du deck de synthèse de CE projet (cadrage BMAD IAP, docs/cadrage-ppt/generate_deck.py, ~40 slides sur 8 chapitres, template OCTO rendu via LibreOffice) — régénérer le vrai export, rendre TOUTES les slides, et confronter chaque type de slide à son propre contrat de design (couverture, exec summary 4 blocs, intercalaires teardrop, personas, douleurs, gaspillages, gate IA, trajectoire, schémas, KPI, maturité). À lancer avant de déclarer « fait » un changement de design du deck, quand le PPT exporté « n'est pas au niveau », ou comme étape de revue du playbook export-ppt-verifie.
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

| Slide (fonction) | Contrat (au rendu) |
| --- | --- |
| `slide_cover` | Couverture de marque OCTO : titre = cadrage BMAD IAP, sous-titre, date. Bandeau métadonnées (statut/langue/confidentialité) **retiré** — ne pas le réintroduire. |
| `slide_executive_summary` | **4 blocs** POURQUOI / QUOI / COMMENT / RÉSULTAT (pas 3, pas 5), avec renvois par CHAPITRE (jamais par numéro de page). |
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
