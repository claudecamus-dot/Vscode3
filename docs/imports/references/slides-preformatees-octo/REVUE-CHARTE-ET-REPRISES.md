# Revue de la charte du deck généré contre le PPT de référence — et slides à reprendre

Date : 2026-11-05. Référence unique : « Slides préformatées OCTO (1).pptx » (cf. `SYNTHESE.md`).
Artefact audité : `docs/exports/decks/bmad-iap-cadrage-synthese.pptx` (export du 2026-11-05 10:26, **36 slides**, rendu
PowerPoint COM) + code courant de `docs/cadrage-ppt/` (dont `generate_deck.py` non commité).
**Statut : PROPOSITION — rien n'est appliqué, en attente d'arbitrage.** Détail : `audit-charte-ecarts.md`,
`mapping-slides-1-18.md`, `mapping-slides-19-36.md` (même dossier).

## 1. Ce qui est déjà conforme (ne pas retoucher)
- Template : même format (9144000×5143500), même palette (le master du template utilise theme1 dont les 10 couleurs
  = theme2 de la référence), géométries des layouts 02/03/04/05/40/50 identiques à l'EMU. Le template a 34 layouts, la référence 50.
- Navy/blanc/cyan, cyan jamais en texte sur blanc (garde `encre_de`), sens non porté par la couleur, Outfit partout,
  pilules, goutte clonée du layout, pas d'ombre, marge gauche 0,615 in.

## 2. Écarts de charte (impact visuel décroissant)
Mesures sur l'export du jour (commande : `scratchpad/audit/stats2.py`, regex sur le XML des slides) :
| # | Écart | Référence | Mesuré (export) / code |
| --- | --- | --- | --- |
| 1 | Italiques | sl. 7 : pas d'italique, citations entre guillemets | 67 runs italiques sur 743 ; 44 `italic=True` dans le code (`generate_deck.py:701, 869, 987, 1620, 2026`, `deck_shapes.py:279, 311, 343`), chapô d'intercalaire en italique (`:765-766`) |
| 2 | Texte trop petit | 10-12 pt courant, ~10 % à 8 pt | 461 runs sur 731 à 8-9,5 pt (63 %) ; aucun run < 8 pt dans l'export mais 29 sites 6,5-7,5 pt dans le code (plancher à l'export, pas à l'écriture) |
| 3 | Épaisseur de trait | 0,75 pt (9525 EMU) navy, partout | 53 traits à 9525 contre 60 à 12700 (1 pt), 45 à 15875, 12 à 19050 ; défauts `line_w=1.0` (`pptx_deck_vscode3.py:109`, `deck_theme.py:81`) |
| 4 | Titre de slide | 18 pt gras, casse de phrase | taille adaptative 17→12 pt, kicker en `.upper()` (`generate_deck.py` ~655-676) |
| 5 | Interlignes | ≥ 1,15 | paragraphes < 115 % (`:1891, 2304, 2934`, `deck_shapes.py:279`), aucune garde |
| 6 | Coins | un seul grand coin arrondi / coins asymétriques (adj 50000, 16667, 0) | rayon unique 0,20 in (`deck_theme.py:77-89`) : cartes arrondies de partout, pas de round1Rect/round2Same |
| 7 | Couleurs hors palette | navy/blanc/cyan + rampe du thème | `C7CBE0` ×16, `DCE6F5` ×11, `E6E8EE`, `F2F4F8`, `8891B3`, `4A5A80`/`26386A` (`deck_theme.py:92`) ; bandeaux gris `E7E9EE` en pied (sl. 20, 24, 27, 32, 36) |
| 8 | Intercalaires | titre navy, numéro navy | numéro 17 pt et couleur de chapitre sur titre+numéro (`:771, :783-784`) |
| 9 | Glyphes | pas de pictos en texte | ①②③④ ↺ ↓ ▾ en police de repli, parfois case vide (sl. 24, 27, 30, 33) |
| 10 | Casse / séparateurs | majuscule de début de phrase ; point médian à proscrire | portée exacte de l'interdit non établie |

## 3. Slides de référence à reprendre (numéros = référence ; slide générée entre crochets)
**Top reprises** (recoupées sur les deux lots) :
1. **Intercalaires [4, 9, 13, 18, 22, 25, 31, 34]** — réf. 76 : titre gras navy, sans accroche italique (S).
2. **Matrice à bande navy [24, 27]** — réf. 84, un helper commun (L, texte tourné = risque).
3. **Gantt à gélules [33]** — réf. 114 + jalons 133 (M).
4. **Cartes à en-tête, filet, pastille** — [19] 166+172, [20] 87/88, [2] 82/67, [10] 88, [8] 149 (M).
5. **Goutte numérotée + disque cyan** — [23, 28] réf. 109, [6] réf. 80 (+) (M/S) ; remplace aussi les glyphes serif.
6. **Onglets verticaux + carte de conclusion** — [5] réf. 78 ; chevron cyan plein [17, 26] réf. 78/149 (M/S).
7. **Bandeau de conclusion arrondi** — [16] réf. 65/105 (S).

**Transversal, taille S, risque nul** : italiques → gras/guillemets ; texte centré → aligné à gauche (sl. 4, 6, 9, 13, 14, 15) ;
traits 0,75 pt ; bandeaux gris → filet + libellé ; fonds hors palette et recouvrement de la sl. 35 ; glyphes supprimés.

**CONSERVER** : 1 (couverture = réf. 1), 3, 7 (agrandir les cartes), 11, 21, 29, 30, 32 (≈ réf. 63).
**ARBITRER** : 2 (5 blocs complets ou courts), 3 (visuel), 12 (croix pincée de 153 = fragile), 14-15 (photo nébuleuse décorative), 26, 35 (corriger oui, refaire en chevrons non : 10 étapes), 36 (structure de 175 oui, panneaux cyan non — la couleur ne porte pas le sens).
**Ne pas reprendre** : pictos/images de la référence (licences non vérifiées), noms de clients (sl. 68-69), visuels de marques tierces (316-323), serpentins/arcs, texte 6-8 pt.

## 4. Réserves
Tailles de police des slides 1-18 non mesurées (planches 640×360) ; slides 3 et 5-8 jugées sur planche ; références 63, 88, 158, 165, 167, 252
citées d'après les notes ; correspondance slide ↔ fonction `slide_*` déduite des titres ; rendu PowerPoint ≠ LibreOffice (certains écarts de police
peuvent être de rendu) ; l'audit de code a cité à tort un ancien fichier (35 slides, 29/10) — chiffres de « rendu » remesurés ici sur l'export du jour ;
longueur de ligne ≤ 80, contrastes calculés et trackers non vérifiés. Cette revue ne touche pas aux slides à 6-8 pt de la référence elle-même (CV, rate card).
