# Slides préformatées OCTO (1) — analyse du deck de référence de la charte

Source : `Downloads/Slides préformatées OCTO (1).pptx` (modifié le 2026-11-05, 43 Mo, **324 slides**,
16:9 = 9144000×5143500 EMU, 50 layouts). Analyse du 2026-11-05 : rendu réel PowerPoint COM (324 PNG)
+ lecture python-pptx, 4 lecteurs en parallèle (slides 1-75, 76-154, 155-264, 265-324).
Le fichier sans « (1) » (43,4 Mo, daté du 2026-05-06) existe aussi : **non comparé**.
Détail par lot (patterns, EMU, slides citées) : `notes-lot-A.md` … `notes-lot-D.md` ici.

## Constantes mesurées
- Thème réellement utilisé : `theme2` (liaison master→theme2 déduite des couleurs rendues, non lue
  dans les rels). Navy `0E2356`, blanc, cyan `00D2DD`, rampe gris-bleu `6E7B9A / 9FA7BB / B7BDCC / CFD3DD / E7E9EE`
  (+ `3E4F78`, `586586`). `theme1` = reliquat Office (orange `ED561B`) : ne pas s'en servir.
- Police : **Outfit** (Regular, Light, Medium, SemiBold) ; Arial en fallback du thème ; résidus Century Gothic /
  Helvetica Neue (origine non vérifiée). Texte en navy, jamais en noir.
- Trait : 9525 EMU (0,75 pt) navy, plein ; séparateurs de lignes de tableau en pointillé.
- Tailles courantes 9-12 pt ; titre de slide 18 pt gras ; minimum rencontré 6 pt (calendriers, rate card, CV : projection exclue).
- Zone utile : x ≈ 549 k → 8,5 M, y ≈ 1,22 M → 4,86 M EMU. Titre placeholder (562500, 361400, ≈8,0 M × 370800).
- Formes dominantes : rect, roundRect, `round2SameRect`, `round2DiagRect`, `round1Rect`, pilule (adj 50000), teardrop (adj 100000).
- Aucun graphique natif : barres, jauges, anneaux, radar sont dessinés en formes ; 4 tables natives seulement (190-192, 249). 192 icônes = images.

## Règles que le deck pose (ou implique)
1. Bichromie navy + cyan ; cyan **en aplat**, jamais en texte sur blanc (sl. 4). Navy sur cyan, blanc sur navy : toujours.
2. La couleur ne porte pas le sens seule : forme/picto en plus, lisible en N&B. Rouge `FF4338`/vert : OK/KO des tutoriels seulement.
3. Rampe cyan en N pas (`DAF6F9`→`4ADBE2`) pour coder un **ordre** (SWOT, matrices), pas un jugement.
4. Accent « un sur N » (sl. 104, 154, 172, 176, 200, 252) ; descente de teinte navy/cyan 100→10 % réservée aux schémas.
5. Typo : majuscule en début de phrase seulement, guillemets (pas d'italique), pas de point médian, ≤ 80 car./ligne, interligne ≥ 1,15, alignement gauche/droite.
6. Photos : formes de la charte (goutte, round2Diag…) ; photos de conférence/équipe en N&B.
7. Compatibilité .ppt : une photo tournée/retournée dans une goutte part de travers à l'export ; variante « .ppt » = forme MOON blanche (adj 63970) qui masque le coin (suppose fond blanc). Cause exacte non vérifiée.
8. Bandeaux d'annotation de template à **supprimer avant livraison** : « A adapter à sa situation », « Optionnel », « Ajouter la Fiche de Ref… », pastille « A remplir en ligne ».

## Catalogue des patterns (renvoi aux lots pour les EMU)
| Chapitre (par nom) | Patterns clés |
| --- | --- |
| Charte / éléments (sl. 1-24) | couverture layout 40, grille OK/KO, descente de teinte, trackers, flèches, logos, banques de photos/pictos/illustrations |
| Avec visuel, Suggestions de mise en page, Executive summary (25-75) | intercalaire layout 50 (goutte + pastille n°), cinq cartes alternées, verbatim round1Rect, **exec summary en blocs (sl. 67)**, frise 2-5 étapes + 4 colonnes |
| Contexte, Démarche, Détails, Planning (76-133) | onglet vertical/haut + carte, cartes liées par + = chevron, matrice Activités/Livrables, Gantt à gélules (114-115), calendriers |
| Tableaux (134-154) | en-tête navy + cap round2Same navy en haut / cyan en pied, croisés, gélules, tableaux-cartes, grilles 4/6/8 |
| Listes, Réponses AO, Schémas, Graphiques, Audit, Canvas (155-264) | serpentin, grilles 2×2 à onglet, SWOT cyan, anneaux segmentés 3-8, jauges, radar, matrices 2×2/3×3, fiche reco Gain/Effort, lean canvas / persona / empathie |
| Équipe, Finance, CV, Fiche ref, Arbre, Conférences (265-324) | « Votre équipe » en quinconce, charges en pilules + cercles cyan, barres de compétence 2 pilules, rate card, arbre = groupe vectoriel |

## Pour reprendre dans `generate_deck.py` (par ordre de fiabilité)
1. Carte à coins asymétriques (`round1/2Same/2Diag`) + trait 9525 navy, via `adjustments` (mesurés : round2Diag 50000/0, round2Same 16667).
2. Pilules navy/cyan/blanches ; barres de compétence = piste + remplissage.
3. Onglet-titre + carte ; colonnes à onglet séparées par pointillés (motifs déjà dans `docs/imports/references/exemples-slides-octo-2026-11-04/NOTE.md`).
4. Intercalaires par layout 50 (3 placeholders) ; photo en forme native = **cloner le `prstGeom`** sur le `<p:pic>`.
5. Tableaux : cellules XML explicites + deux caps ; Gantt à gélules (114-115).
6. Rampe cyan N pas pour séries ordonnées ; grille « un sur N en accent ».

**Fragile / à éviter** : serpentins et arcs (92-93, 156, 204-206), formes dessinées main (infini, fishbone, entonnoir…),
anneaux chaînés (sensibles au z-order), texte tourné/oblique, 6-8 pt, groupes (arbre, visuels de conférences : copier tels quels),
noms `Google Shape;N`, layouts variantes `_1_2` (préférer 02, 03, 04, 05, 50), rustine MOON.

## Écarts, défauts du deck de référence et points d'attention
- **Charte projet plus stricte que le deck** : sl. 3 présente du cyan sur navy comme lisible, sl. 122 (SAM/DIM) met du cyan en texte. Garder la règle projet.
- Le deck cite les chapitres **par numéro** ; la règle VSCode3 impose le NOM — ne reprendre que les noms.
- Couleurs hors charte vues : `00A9C5 / 00A2D8 / 3F3F3F / C8E7E4` (sl. 229-230, artefact d'import Google Slides ? non vérifié).
- Défauts dans la référence : sl. 64 (carte qui déborde, texte blanc invisible hors fond navy), libellés « 1/3 » à tabulations qui se superposent (8, 9, 10, 22), étiquettes coupées (249 « Effor/t », 189, 190, 209), blocs hors canevas (53, 54, 61), pied « 2025 » et `<#>` sur layouts 63-70.
- **Vrais noms de clients/personnes** sur 68-69 ; visuels de marques tierces 316-323 ; licences non vérifiées → ne rien reprendre tel quel.

## Non vérifié (honnêteté)
Rendu = PowerPoint COM, pas LibreOffice (le pipeline du projet) ; ratios de contraste relus à l'œil, non calculés ; slides 227 et 238
non vues, ~15 slides du lot A vues via leurs jumelles ; lien du bouton « Clique ici » du sommaire ; slides masquées ; origine de Century Gothic ;
compatibilité .ppt réelle ; différences avec le fichier sans « (1) ».
