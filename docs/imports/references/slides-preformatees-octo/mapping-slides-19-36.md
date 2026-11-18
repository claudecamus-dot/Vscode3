# Mapping deck généré (slides 19-36) -> slides du deck de référence OCTO

Méthode : les 18 PNG générés (gen/png/Slide19..36) ont tous été vus ; les slides de référence citées ont été vues (PNG ref) avant citation : 67, 84, 87, 94, 106, 109, 114, 133, 147, 149, 151, 166, 172, 175. Catalogue : SYNTHESE.md + notes-lot-A..D. Les autres numéros de référence cités le sont d'après les notes, marqués « (notes) ».
Chapitres cités par NOM. Aucun nom de client / personne / marque tierce repris. Je n'ai pas lu generate_deck.py (aucun besoin pour le mapping visuel : effort estimé depuis le rendu, non mesuré).

## Constat transversal (le plus gros écart, vu sur 14 slides de référence)
- Référence : cartes à **un seul grand coin arrondi** (round1/round2Same/round2Diag) ou carte à onglet, trait **0,75 pt navy**, fond blanc, séparateurs en pointillé, numéros en **goutte** (teardrop) + point cyan, aucun aplat gris.
- Généré : cartes à **tous les coins très arrondis** (pilules/roundRect), traits plus épais (navy ~2 pt ou gris clair), **bandeaux gris `E7E9EE`** en pied de slide (20, 24, 27, 32, 36...), pastilles rondes pleines. Lisible mais « autre langage » : c'est l'écart de ton n°1.
- Défauts de rendu à corriger (vus) : caractères ①②③④ et ↺ rendus en police serif de repli, parfois en case « tofu » (24 sous-titre, 33 ligne « Réévaluation ») ; 27 et 30 idem pour ②/③. Remplacer par « 1. », « 2. » en Outfit (ou goutte numérotée).

---

## Slide 19 — « Pourquoi Infrastructure as a Product » (3 bascules)
- Pattern actuel : bandeau navy très arrondi (barre cyan à gauche) + photo ciel en coin diagonal, puis 3 lignes-cartes blanches (cercle navy numéroté, titre, texte, pilule « répond à »). Dense mais aéré, texte 11-12 pt.
- Réf. proches : **166** (empilement de cartes « onglet-titre + corps », pastille cyan), **172** (3 étapes : goutte numérotée, en-tête blanc / cyan / navy), **67** (grande carte à grand coin + onglet cyan + bandeau navy).
- Écart : cartes pleinement arrondies vs corps à coin unique ; numéros en cercle plein vs goutte ; la pilule « répond à » est contour navy épais, alourdit.
- Reco : **REPRENDRE 166** (onglet-titre = titre de bascule, corps = texte, pastille ronde ; la pilule « répond à » devient un 3e élément en pied de corps, filet pointillé) ; numéros en goutte (cf. 109/172). Garder bandeau navy + photo (déjà proche de 67).
- Effort **M**. Risque faible (formes round1/round2Same standard).

## Slide 20 — « Repérer, prioriser, tenir »
- Actuel : 3 colonnes cartes arrondies contour navy épais, cercle navy numéroté à cheval en haut, sections CÔTÉ CLIENT / CÔTÉ OCTO, encart gris « TRANCHÉ ENSEMBLE » (barre cyan), flèches entre colonnes. Texte ~10-11 pt, très dense.
- Réf. : **87** (carte à titre + filet, pastille numéro double anneau en coin, filet puis « LIVRABLES » en majuscules gras, coin bas-droit arrondi seul) ; **84** (en-têtes numérotés). (88, variante 3 groupes : notes.)
- Écart : encart gris plein vs filet + intitulé majuscule ; numéro au centre-haut vs coin ; contour trop épais.
- Reco : **REPRENDRE 87/88** : titre en haut avec filet, numéro en pastille à cheval sur le coin haut-droit, « TRANCHÉ ENSEMBLE » = filet + libellé majuscule gras (plus d'aplat gris), un seul coin arrondi. Les flèches entre colonnes peuvent rester (chevron cyan plein, cf. 149).
- Effort **M**. Risque : densité (9-10 pt) ; pas de texte tourné.

## Slide 21 — « La cible IAP est une Platform Team » (tableau en pilules)
- Actuel : tableau fait de pilules : étiquette navy pleine (ligne 1, « un sur N »), pilules contour, dernière ligne en tirets (« + Agents IA »), en-têtes gris majuscule.
- Réf. : **147** (tableau de gélules : en-tête navy en pilule, étiquette de ligne rect + coin droit arrondi, liaison pointillée, cellules séparées par filets verticaux).
- Écart : proche. Différences : en-tête navy absent (ici texte gris), pas de filets verticaux entre colonnes, pas de pointillé de liaison, traits gris très clairs.
- Reco : **CONSERVER** + retouche : en-tête en pilule navy (texte blanc) au-dessus des 2 colonnes, filet vertical entre cellules, pointillé de liaison. Garder « un sur N » (ligne 1 navy) et la ligne en tirets.
- Effort **S**. Risque faible.

## Slides 22, 25, 31, 34 — intercalaires (La démarche / L'expertise agentic d'OCTO / Réussir et démarrer / Annexes)
- Actuel : goutte photo (coin pointu haut-droit) + pastille [logo | numéro] au coin + titre navy à droite + sous-titre italique gris ; point cyan en haut-gauche ; texte vertical « THERE IS A BETTER WAY ».
- Réf. : intercalaire layout Chapitre (notes lot A/B/C : goutte 2560500 EMU, pastille numéro, point cyan) — même composition (je n'ai pas ouvert un intercalaire de réf. : **non revérifié visuellement**, comparaison faite sur la description des notes).
- Écart : aucun visible sur la structure. Le sous-titre italique gris est un ajout (non vu dans les notes).
- Reco : **CONSERVER**. Seule vérif : les photos (canyon, plage, lavande, dunes martiennes) sont choisies sans cohérence de teinte — à arbitrer côté image (cf. mémoire « Deck image fetcher »), pas côté forme.
- Effort **S** (0). Risque : photo tournée dans la goutte = fragile à l'export .ppt (SYNTHESE, non concerné ici : pipeline PPTX).

## Slide 23 — « Trois temps et une boucle » (frise 4 étapes + livrables)
- Actuel : ligne grise horizontale, 4 cercles (1 navy plein = « un sur N ») avec ①②③ en glyphe serif et ↺, titre / durée italique / texte centrés, 4 cartes « LIVRABLE-CLÉ » (1 contour épais), bandeau navy à citation en pied.
- Réf. : **109** (5 colonnes : goutte numérotée « 1. » + disque cyan au coin + pointillé vertical + titre + texte centré) ; **84** pour les cartes en pied (cases à filets).
- Écart : chiffres en glyphes de repli (ni Outfit ni gras) ; cercles vs gouttes ; pas de pointillé de liaison ; ligne grise vs pointillé.
- Reco : **REPRENDRE 109** : goutte avec « 1. » en Outfit gras, disque cyan (aplat, sans texte) au coin, pointillé vertical vers le titre ; la 4e (boucle) reste une goutte avec ↺ dessiné en forme, pas en glyphe. Cartes livrable-clé en round1Rect 0,75 pt, 1 sur 4 en contour épais conservé.
- Effort **M**. Risque faible (109 = formes simples). Éviter serpentin (92-93, 156).

## Slide 24 — « Deux fils courent dans les mêmes phases » (matrice personnes / technique)
- Actuel : « 70 % » en pilule navy + texte ; grande carte arrondie : 4 colonnes (cercles ①-④), 2 lignes (LES PERSONNES sur fond gris, LA TECHNIQUE), séparateurs verticaux ; bandeau gris en pied ; sous-titre avec glyphes cassés (« ①②③⮿ »).
- Réf. : **84** — LE modèle : en-têtes numérotés en haut (rond + titre), bande verticale navy à gauche avec libellés tournés (« Activités / Livrables ») → ici « Les personnes / La technique », filets verticaux et horizontal central, coin bas-droit arrondi.
- Écart : la matrice actuelle est une carte à lignes grises sans bande navy ; l'ancrage de lignes est faible (libellé texte simple).
- Reco : **REPRENDRE 84** (4 colonnes, 2 lignes) ; bande navy 303 k EMU avec texte blanc tourné 270°. Remplacer le chapeau « 70 % » par un bandeau type 67 ou le garder (déjà proche). Supprimer les glyphes ①②③ du sous-titre.
- Effort **L** (nouvelle fonction réutilisable aussi pour la slide 27). Risque moyen : **texte tourné** listé fragile dans SYNTHESE (alternative : libellé horizontal dans un onglet navy vertical sans rotation).

## Slide 26 — « Une expertise OCTO qui complète notre démarche » (besoin -> frein -> apport)
- Actuel : 3 lignes : étiquette navy pleine à gauche, carte grise claire (frein), chevron contour, carte contour navy (apport) ; bandeau navy-citation en pied ; en-têtes gris majuscule.
- Réf. : **149** (tableau-carte : en-tête navy à un coin arrondi, lignes à filets, **chevron cyan plein** vers une carte de conclusion à grand coin) ; **106** (pilules empilées à gauche, panneau navy à droite).
- Écart : 3 étiquettes navy pleines + bandeau navy = beaucoup de navy plein, pas de « un sur N » ; chevrons contour gris vs chevron cyan plein (aplat cyan autorisé) ; cartes pleinement arrondies.
- Reco : **ARBITRER** : (a) rapide **S** : chevron cyan plein, coins asymétriques, une seule étiquette navy (la première) et les autres contour ; (b) **M** : refaire en tableau-carte 149 (colonne besoin = en-têtes navy). Je recommande (a).
- Risque faible.

## Slide 27 — « L'outillage prend en charge une partie du fil humain » (AVEC / SANS IAP x 4 temps)
- Actuel : 4 pictos ①-④/↺ (glyphes), 2 grandes cartes (AVEC IAP : contour navy + barre cyan gauche ; SANS IAP : contour gris), 4 colonnes séparées de filets, bandeau gris « ONZE WORKFLOWS » en pied. Texte ~9-10 pt (dense), titre sur 2 lignes.
- Réf. : **84** (même matrice 4/2 avec bande verticale navy, filets) ; **166** pour le bandeau en pied (onglet + corps).
- Écart : la distinction AVEC/SANS repose sur contour navy vs gris + barre cyan (acceptable : forme + position) ; pas de bande navy ; ①-④ en glyphes ; le bandeau gris très texte (8-9 pt) déborde en densité.
- Reco : **REPRENDRE 84** avec le même helper que la slide 24 (AVEC/SANS = bandes verticales navy, SANS = bande contour pour garder « un sur 2 »). Bandeau de pied : filet + libellé majuscule + 2 lignes (comme 87 « LIVRABLES »), sans aplat gris.
- Effort **M** (si helper 24 existe) sinon **L**. Risque : texte tourné ; densité 9 pt.

## Slide 28 — « Trois candidats d'agent » (3 colonnes POURQUOI / CE QUE FAIT L'AGENT / GAIN)
- Actuel : 3 colonnes à filet navy, picto = formes procédurales (engrenage, nuage, carré) peu lisibles, 3 sections à intitulés majuscules, texte 10-11 pt, pastille « DÉPLOIEMENT AGENTIC » en coin, note en pied italique.
- Réf. : **94** (4 piliers : picto en tête sur pointillé vertical, carte avec en-tête titre + filet, corps à puces gras partiel) ; **109** pour numéros.
- Écart : pictos procéduraux incohérents (une des 3 formes est un blob) ; colonnes sans carte : texte flotte ; pas de coins arrondis spécifiques.
- Reco : **REPRENDRE 94** en 3 colonnes : picto remplacé par goutte numérotée (cf. 109) ou pictos neutres cyan/navy plats ; chaque colonne = carte round2Same (en-tête filet + 3 blocs). Les pictos de la bibliothèque OCTO (192 images) : licence non vérifiée, ne pas copier tels quels.
- Effort **M**. Risque : pictos (si on veut des icônes, il faut les dessiner).

## Slide 29 — « Sous contrôle : la donnée fixe le mode » (D0-D4 + panneau PRUDENCE IA)
- Actuel : 5 pilules en dégradé navy (D0 clair -> D4 foncé), colonnes de texte et mode en italique ; grand panneau navy arrondi à droite, texte blanc.
- Réf. : **106** (pilules empilées à gauche + séparateur pointillé vertical + panneau navy à droite avec en-tête navy puis corps blanc) ; **175** (rampe d'ordre).
- Écart : déjà très proche. Le dégradé navy est autorisé pour un ordre/un schéma (SYNTHESE règle 4). Le panneau navy plein est lourd ; 106 fait en-tête navy + corps blanc.
- Reco : **CONSERVER**. Option **S** : panneau à en-tête navy (titre « PRUDENCE IA… ») + corps blanc contour 0,75 pt, filet pointillé entre les deux colonnes.
- Risque faible.

## Slide 30 — « Trois niveaux d'ambition » (A / B / C)
- Actuel : tableau de 3 lignes-cartes ; onglet gauche = A navy plein, B/C gris clair avec disque navy lettre ; 3 colonnes de texte ; en-têtes gris.
- Réf. : **172** (3 étapes : en-tête blanc / cyan / navy = « un sur N »/ordre) ; **166** (onglet-titre + corps).
- Écart : proche. Le coin arrondi unique est déjà utilisé sur l'onglet. Fonds gris `E7E9EE` pour B/C (hors vocabulaire carte-blanche) ; ②/③ en glyphes dans la note de bas.
- Reco : **CONSERVER**. Retouche **S** : B/C en blanc + filet 0,75 pt (la distinction A = navy reste le « un sur N »), note sans glyphes.
- Risque faible.

## Slide 32 — « Quatre conditions de réussite » (2x2 navy + carte NOS REFUS)
- Actuel : 4 blocs navy 2x2 (coins extérieurs arrondis, croisement net), carte contour navy avec pastille cyan « NOS REFUS » (cyan en aplat, texte navy : conforme), bandeau gris en pied.
- Réf. : **151** (grille 2x2 contour avec croix « pincée » au centre) ; **63** (4 cartes marine 2x2 + croix blanche, notes lot A, non vue) ; **87** pour la carte de droite.
- Écart : déjà équivalent à 63 sans la croix centrale ; la carte de droite est pleinement arrondie (2 coins) ; bandeau gris.
- Reco : **CONSERVER**. Option **S** : bandeau de pied remplacé par filet + libellé majuscule. Ne pas ajouter la croix pincée (4 quarts de cercle : fragile).
- Risque : faible si on ne touche pas à la croix.

## Slide 33 — « Deux semaines d'Assessment flash » (planning + engagements)
- Actuel : échelle S1…S7 / T+6-12 mois avec petits cercles (S2 cyan), 4 lignes de phases avec barre : pilule navy pleine, pilule contour, pilule tirets, losange cyan et losange contour ; sous : 2 cartes numérotées + 4 cartes à barre navy gauche. Texte 9-10 pt, très dense ; glyphe « ⮿ » en case cassée devant « Réévaluation ».
- Réf. : **114** (gantt à gélules : en-tête navy en pilule avec échelle, étiquettes « ETAPE 0N » en pilules contour, pistes en pilules contour, barre cyan texte navy, colonne LIVRABLES) ; **133** (losanges jalons cyan/contour, légende).
- Écart : pas d'en-tête navy en pilule ni de piste : les barres flottent ; jalons déjà proches de 133 ; cercles de semaine peu utiles.
- Reco : **REPRENDRE 114** : en-tête navy pilule (S1…S7 …), pistes contour, barres en trois états forme+position (navy plein / contour / tirets conservés — l'état se lit par la forme, pas la couleur), losanges de 133 conservés. Remplacer les glyphes ①/⮿ par « 1. ».
- Effort **M**. Risque : densité de la moitié basse (9-10 pt) ; garder au-dessus de 9 pt.

## Slide 35 — « Accompagnement Infra as a Product » (flux 2 rangées + extensions)
- Actuel : 2 rangées de pilules/ovales reliés par flèches, fonds **bleu clair teinté hors palette** (≈ `DCE6F5`) et gris, extensions en pointillés, légende à 3 formes, bandeau navy-thèse en pied. Texte 8-10 pt ; l'étiquette « signal de contexte détecté ? » se superpose aux mini-pilules (« Contexte léger / Contexte politique »).
- Réf. : **133** (chevrons Cadrage -> Mise en production avec rampe cyan DAF6F9 -> 00D2DD -> navy, jalons losanges, cartes blanches filet) ; **94** (cadre inférieur à bandeau d'échelle).
- Écart : fonds bleutés hors charte (la référence n'en pose pas : seules 3 couleurs dans ses slides) ; flux de 10 étapes en 2 rangées au lieu de chevrons ; recouvrement visible.
- Reco : **ARBITRER**. (a) **S, à faire** : fonds en blanc ou `E7E9EE`, contour navy 0,75 pt, corriger le recouvrement. (b) **L, risqué** : refaire en frise de chevrons 133 sur 2 lignes — 10 étapes + 3 extensions, très dense ; non recommandé.
- Risque : (b) élevé ; texte < 9 pt déjà présent.

## Slide 36 — « Export markdown — documentation-first ou agentic » (2 cartes + 3 pilules + bandeau)
- Actuel : 2 grandes cartes contour avec barre navy gauche, titres majuscules, 3 pilules grises, bandeau navy large « Pas un aller simple ».
- Réf. : **175** (comparatif : 2 en-têtes navy à coins asymétriques, 2 panneaux, chevron entre) ; **106** (pilules empilées + panneau navy).
- Écart : 175 colore les panneaux (cyan clair / cyan plein) pour opposer : à ne **pas** reprendre (la couleur ne porte pas le sens). Structure 2 colonnes à en-tête navy est bien plus proche de la charte que les barres gauches.
- Reco : **ARBITRER** : reprendre la structure 175 (2 en-têtes navy en tab + panneau blanc 0,75 pt, chevron ou « ou » au centre), panneaux identiques en couleur ; trois pilules du bas en filet blanc (plus de gris) ; bandeau navy conservé.
- Effort **M**. Risque faible.

---

## Top 5 des réutilisations à plus fort impact
1. **84 (matrice Activités/Livrables à bandes navy)** -> slides 24 et 27 (un seul helper) ; c'est LE pattern de la charte pour une démarche à N temps. Effort L, risque : texte tourné.
2. **114 (gantt à gélules) + jalons 133** -> slide 33 ; remplace des barres flottantes par la piste/en-tête de la charte. Effort M.
3. **87/88 (carte à filet + pastille numéro + « LIVRABLES ») + 166 (onglet-titre + corps)** -> slides 20 et 19 (et pied de 27/32). Effort M.
4. **109 (goutte numérotée + disque cyan + pointillé)** -> slides 23 et 28 (et 19 pour les numéros) ; remplace aussi les glyphes ①②③ rendus en serif. Effort M.
5. **Correctifs transversaux S** : fonds de 35 hors palette (bleutés), bandeaux gris `E7E9EE` remplacés par filet + libellé majuscule, traits 0,75 pt, chevron cyan plein (149) en 26, glyphes ①-④/↺/⮿ supprimés (23, 24, 27, 30, 33).

## Faits du brief infirmes
Aucun (aucun fait donné par le brief n'a été contredit).

## Non vérifié
- Intercalaires 22/25/31/34 : comparés aux notes, pas à un intercalaire de référence ouvert.
- Références 63, 88, 158, 165, 167, 252 : citées d'après les notes, **non vues** dans cette passe.
- Rendu du deck généré = celui fourni (gen/png) ; aucun re-rendu LibreOffice/COM de ma part. Les tailles de police (9-12 pt) sont estimées à l'œil sur PNG, pas lues dans le PPTX.
- Efforts S/M/L = estimation, non mesurée ; generate_deck.py non lu.
- Aucune reprise d'image/pictogramme de la référence recommandée (licences non vérifiées, cf. SYNTHESE).
