# Lot A - Deck de reference OCTO "Slides preformatees OCTO (1)" - slides 1 a 75

Source : ref.pptx (python-pptx, scripts dans lotA/) + renders Slide1..75.PNG tous vus (sauf 17-18, 20-21, 23-24, 32, 36-37, 40, 42, 44-46, 48 : variantes strictes de slides vues, dump XML lu). Slide 9144000 x 5143500 EMU (commande python-pptx). 50 layouts dans le master. Unite : 1 pt = 12700 EMU.

## 0. Constantes du systeme (mesurees)

- Theme : dk1 = 0E2356 (marine), lt1 = FFFFFF, dk2 3E4F78, lt2 586586, accent1 6E7B9A, accent2 9FA7BB, accent3 = 00D2DD (turquoise), accent4 B7BDCC, accent5 CFD3DD, accent6 E7E9EE. Polices de theme declarees : Arial (major/minor) - mais le texte force "Outfit" partout.
- Polices sur slides 1-75 (occurrences de `<a:latin>`) : Outfit 955, Outfit Light 125, Outfit SemiBold 49, Outfit Medium 45, Century Gothic 38 (hors charte, origine non verifiee), Helvetica Neue Light 3, Arial 3, Roboto 2.
- Couleurs srgb : 0E2356 x405, FFFFFF x81, 00D2DD x42, 000000 x38, FF4338 x14 (rouge, uniquement tutoriel slide 15 + croix), 75B7C7 x8 (bleu des cadres photo).
- Epaisseur de trait : 9525 EMU (0,75 pt) x522 ; 19050 (1,5 pt) x22 ; 38100 (3 pt) x6. Le trait fin 0,75 pt marine est LA signature des cadres.
- Tailles (centiemes de pt) : 1100 x289, 1000 x279, 1200 x135, 800 x104, 900 x97, 1150 x92, 1300 x57, 1600/1800/2000/2400 ~13-19, 4500 x10 (titres "Couleurs." / "Chapitre.").
- Formes : teardrop adj=100000 (goutte, coin pointu en haut a droite) x103 ; roundRect adj 50000 (pilule) x96 / 16667 x28 / 0 x28 ; round2DiagRect adj1/adj2 (0/50000, 38136/0, 50000/0, 16667/0) ; round2SameRect (50000/0, 16667/0, 0/39422) ; round1Rect (50000, 16667).
- Layout "04 - Titre seul" : titre = placeholder (562500, 361400, 8019000 x 370800), Outfit gras 18 pt, marine, normAutofit, insets 0, ancre haut. Logo O en haut gauche, copyright vertical a gauche ("OCTO | PART OF ACCENTURE (c) 2026 - All rights reserved"), pastille de numero de page ".N" en bas a droite : fournis par le layout, pas a recreer.
- Layout "50 - Chapitre [1]" : goutte photo (1396875, 1659950, 2560500 x 2560500), pastille logo+numero (3457625, 1226750, 499500 x 433200 + 433200 x 453000), titre placeholder (4295825, 1918050, 4164300 x 1810200), point turquoise a (497875, 564900, 136800 x 136800), texte vertical "THERE IS A BETTER WAY".

## 1. Catalogue des PATTERNS

### P1 Couverture (s1, layout 40 - Couverture [1])
Photo plein cadre teintee bleu, pilule contour blanc (arrondi gauche/droit), sous-pilule "2026 | OCTO Technology", illustration filaire blanche (Octos + plante + laptop), point turquoise, "DIGITAL THINKERS & DOERS" bas gauche, "OCTO TECHNOLOGY | PART OF ACCENTURE" haut droit. 3 placeholders seulement : titre (1657350, 1619250, 3648000 x 1305000), annee (4707450, 3303350, 732000 x 315600), societe (5695200, 3303350, 1374900 x 315600). Usage : couverture ; tout le decor vient du layout -> ne remplir que 3 textes.

### P2 Sommaire (s2, layout 99 - Table des matieres)
Titre "Sommaire" (564931, 360737) ; liste en un seul placeholder (571500, 695723, 5738700 x 4132500) et colonne de numeros de page en second placeholder (7091200, 695723, 1016100 x 4132500) ; 20 entrees (Avec visuel 25 ... Conferences 317). Goutte contour marine coin haut-droit (8127900, 0, 1016100 x 1016100) + pictogramme "Clique ici" (aide d'edition, a supprimer). Numeros de page = textes durs (fragiles si le deck bouge).

### P3 Regle contraste (s3, layout 06 vide)
Pilule titre round2Diag (contour fin) + photo "cube attention" round1Rect (5829225, 689975, 1781400 x 976800) + bloc droit round2Diag (5829225, 1666650, 2714700 x 2857800). Grille 2 x 3 de roundRect (2168700 x 639300), colonnes x=923925 / 3379525, lignes y=1952625 / 2888200 / 3823777 ; pastille ronde coche/croix (~492387) chevauchant le coin haut-gauche de chaque case. Cases : marine+texte blanc OK ; marine+texte cyan OK ; cyan+texte marine OK ; cyan+texte blanc KO ; blanc+texte marine OK ; blanc+texte cyan KO. Message : "Le turquoise OCTO n'est pas lisible sur du blanc et vice versa". Pattern "OK/KO par picto" (forme + couleur, pas couleur seule).

### P4 Intro "Couleurs." (s4, layout 02 - Titre et contenu)
Photo round2Diag (830775, 495525, 3663300 x 4124100) + titre 45 pt (571500 EMU) en 3 runs : "Cou" blanc (sur la photo), "leurs" marine, "." cyan - le titre chevauche volontairement le bord de la photo (zone de recouvrement : texte blanc dessus, marine dehors). Texte regle + 2 pastilles teardrop (653700 x 653700) marine #0E2356 "Principale" / cyan #00d2dd "Secondaire (a ne pas utiliser pour de la typo)".

### P5 Descente de teinte (s5, layout 03)
Grille 5 x 4 de groupes (1312389 x 699463 ; x = 571500 + k*1651466 ; y = 1267263 + j*873470) : goutte teinte + etiquette pourcentage + code hex. Marine 100 % 0E2356, 90 263967, 80 3E4F78, 70 586586, 60 6E7B9A, 50 8691AB, 40 9FA7BB, 30 B7BDCC, 20 CFD3DD, 10 E7E9EE ; turquoise 100 00D2DD, 90 3CD7E0, 80 5BDDE4, 70 72DFE7, 60 8AE4EB, 50 9EE9ED, 40 B2EEF2, 30 C6F1F5, 20 DAF6F9, 10 EBFAFB. Regle : "pour vos schemas uniquement".

### P6 Matrice de contraste (s6, layout 06)
Une SEULE image PNG plein cadre (642938, 152400, 7858125 x 4838700) : la matrice texte/fond 10 teintes + 3 couleurs principales. Lecture : double coche = contraste suffisant ; simple coche = seulement gros caracteres (18 pt regular ou 14 pt bold minimum) ; case vide = insuffisant. Donnees non editables (image) : relues sur le render seulement.

### P7 Checklist accessibilite (s7, layout 05 - Focus)
Fond marine clair, carte blanche arrondie, 7 cartes roundRect contour fin (3804600 de large, colonnes x=650930 / 4688463, rangees y=1060025 / 2034254 / 3008500, hauteurs 905100 ou 1298100) + titre 2 lignes + picto accessibilite 541000. Contenu = les regles de la charte (section 2).

### P8-P10 "Elements graphiques" 1/3, 2/3, 3/3 (s8-s10, layout 04)
- s8 : formes textuelles (round2Diag, round2Same, round1, teardrop, cercle 742200 x 742200 ; pilules 1930500 x 212100), trackers (pilule gris clair + numero dans goutte ; numeros 1./2./3. ; barre "xxx" marine pleine / contour), guillemets, "tete d'Octo" (4 variantes), avatars Octos (6) et Clients (4), tags "Octos"/"Clients" (round2Diag 864900 x 196200).
- s9 : bulles de texte lineaires (round2Diag/round1 grandes, contour fin, pas de fond) 4183500 x 1166400 etc. ; separateurs et filets : barre marine/cyan courte (393000 x 63900), filet gris epais, filet marine fin, pointilles, hachures, filets cyan epais ; cadre photo 1036800 + onglet.
- s10 : fleches : doubles et simples, trait epais arrondi marine / cyan / contour, longueurs variees, 3 fleches courbes (contour, cyan, marine). 33 groupes.
Nota : "1/3", "2/3", "3/3" sont dans le titre apres des tabulations ; au render ils se superposent a un sous-titre (artefact de rendu, chevauchement visible s8/s9/s22).

### P11-P12 Logos (s11-12, layout 04)
Grille de cartes roundRect contour fin (1633200 x 1004400 ou 1982400 x 1004400 ; x = 940750 / 2787000 / 4982450 ; y = 1069025 / 2209700 / 3350375) avec logo image : OCTO (blanc / marine / turquoise), Accenture, DUC-K Conf, La Conf Data IA, USI ; puis Academy, B Corp, OCTO events, Great Place to Work, OCTO SKOOL, Numerique Responsable, autre cercle. Fonds de carte : blanc, marine, turquoise = les 3 seuls fonds de logo.

### P13-P15 Tutoriels (s13-15, layout 04)
- s13 : capture d'ecran Drive a gauche (641050, 264575, 2357125 x 4878926 : debord volontaire), etapes 01./02./03. en texte 14 pt avec chiffre gras ; mots-cles de recherche : "picto + mots cles", "photo + mots cles", "avatar", "illustr + mots cles (a venir)".
- s14 : rotation d'une photo dans une forme : rognage, bouton de rotation, SHIFT = pas de 15 degres.
- s15 : compatibilite .ppt : PowerPoint ne sait pas pivoter l'image DANS la forme ; un export .ppt met l'image de travers. Schema Slides vs PowerPoint (vert OK / rouge KO, FF4338). Deux bandeaux marins : "Attention compatible avec tous les exports sauf ppt (les photos seront sur le cote)" et "Version compatible export .ppt".

### P16-P24 Banques de visuels (s16-24, layout 03 - Titre et sous-titre_2)
- s16-18 : 3 photos 3D en goutte teardrop 2560500 x 2560500 (x = 528950 / 3291750 / 6054550 ; y = 1570900) ; 3 slides de plus de variantes.
- s19-21 : pictos 656624 x 656624 en grille 3 colonnes de 3 x 4 (x = 593950 / 1461276 / 2312825...), 3 blocs separes par filets verticaux pointilles (x=3175325, 5968700), en-tetes round2Diag marine (2375700 x 306600, texte blanc) : Numerotations / Temps & Mesure / Echanges ; (s20-21 : autres familles).
- s22-24 : illustrations-scenettes en pilule (6 par slide).
Chemin des banques : Drive "HAL9000 > 3. Corporate > Graphic Tools" (Catalogue Photos / Pictogrammes / Illustrations).

### P25 / P52 / P62 Intercalaire de chapitre (layout 50 - Chapitre [1])
Goutte photo + pastille [logo | numero 01/02/03] collee au coin haut-droit de la goutte + titre 28 pt environ a droite. Seuls 3 elements a remplir : titre (placeholder), numero (placeholder 3457650, 1226600, 499500 x 433200) et image dans la goutte (picture en teardrop adj=100000, 2560500 x 2560500 a (1396875, 1668700)). s25 "Avec visuel", s52 "Suggestions de mise en page", s62 "Executive summary".

### P26 Chapitre avec visuel + gros titre (s26, layout 02)
Meme composition que s4 : photo round2Diag (830940, 494775, 3663300 x 4125600), mot "Chapitre." 45 pt a cheval sur le bord, numero "01" gros, accroche (placeholder 4741950, 2636475, 3570900 x 1120500).

### P27-P28 Sous-chapitre (layout 04)
Pastille "XX | logo" (round1Rect 499500 x 433200 flipH + round2SameRect rot 90 deg) + gros bloc round2Diag (1869750, 1751525, 2844000 x 2097300 ; adj1 0, adj2 34219, remplissage blanc FFFFFF, contour 9525 marine, texte 24 pt "Outfit Medium" gras interligne 115 %) + photo teardrop 2560500 a droite (4696511, 1297033). s27 = photo en goutte (rotation => KO .ppt) ; s28 = version .ppt : round2SameRect + forme MOON blanche (lt1, trait lt1, adj 63970, rot -8100000, 835800 x 1634689) qui MASQUE le coin pour imiter la goutte. Bandeau d'avertissement en haut a droite : round2SameRect marine (4316875, 0, 4831500 x 257700), texte blanc gras.

### P29-P30 Cinq cartes alternees (layout 03)
Cinq photos 1548600 x 1548600 en alternance haut/bas (teardrop ou round2SameRect ; y = 1411645 haut / 2960237 bas ; x pas de 1548600 depuis 700597) + 5 textes courts alternes sous/sur la photo ; point turquoise 91500. s30 = version .ppt (MOON x2 de masquage + round2SameRect). Sert de frise 5 temps / 5 piliers.

### P31-P32 Message fort + 2 photos (layout 04)
Photo round2Diag (771175, 1276000, 3070800 x 2498400) + goutte 1720800 + grande pilule texte 32 pt environ gras avec point cyan final (4174200, 1393713, 3820500 x 1606800). s32 = version .ppt (MOON).

### P33-P37 Photo + phrase (layout 04)
s33/s34 : photo round2Diag (carree 2590200 ou portrait 2595300 x 3697800) a gauche + phrase en roundRect (4113599, 2402426, 4053900 x 1077900) ; s34 = portrait avec petit onglet teal decoratif + titre gras + paragraphe. s35-37 : texte courant (4053900 x 1697700) sur filet horizontal avec pastille "goutte + point cyan" en bout de ligne ; photo teardrop 2587500 (s35) / round2Same (s36 + MOON) / round2Diag (s37).

### P38 Titre + texte + visuel droit + bandeau 3 colonnes (layout 01)
Photo portrait round2Diag (5941325, 696775, 2595300 x 3697800) ; texte (562825, 1273150, 4690800 x 1970100) ; bandeau round2Diag (519625, 3376375, 5169000 x 1235400) avec 3 colonnes de 1497000 separees par filets verticaux fins (615600 de haut) - cf. s59, s60.

### P39-P49 Gabarits "cadre blanc" (layouts 63-70 + CUSTOM)
Slides a placeholders vides pour y glisser une photo : 39-40 visuel a gauche + bloc conclusion (layouts 69/70) ; 41-42 visuel a droite round2Diag (6271200, 304800, 2593500 x 3705000) ; 43-46 goutte en bas a droite (6822675, 2819550, 2045100) + placeholder citation (5943600, 876300, 1647900 x 1878900) ; 47-49 petite goutte haut droite (7475450, 290174, 1395900) + bloc conclusion (6076950, 2200275, 1699500 x 2085900). Variante .ppt = MOON (667369 x 1305676) sur 44/46/48. Les cadres s'affichent vides au render ; le pied de page de certains (39, 47, 49) dit "2025" et la numerotation montre "<#>" (layouts non mis a jour).

### P50-P51 Verbatims / citations / feedbacks (layout 04)
s50 : portrait noir et blanc round2Diag (1321773, 701925, 2705400 x 3896100) ; bloc citation round1Rect flipH (3696738, 2487200, 4456200 x 1712700 ; adj 25041 ; blanc, contour dk1 9525) texte 20 pt gras ; guillemets fermants navy superposes au coin ; pastille "Source :" round2Diag (4642558, 4043650, 3509700 x 307800 ; adj1 50000 adj2 0 ; 12 pt Outfit Light aligne a droite). s51 : variante photo en roundRect (4500450, 493701, 3705300 x 2810700), bloc a gauche. Photo en N&B pour un portrait, couleur pour un evenement.

### P53-P61 Suggestions de mise en page (layout 04)
Compositions de blocs contour fin qui se chevauchent par un coin :
- s53 : 3 round2Diag (3798000 x 1693200, 3906000 x 1542900, 3249000 x 1764000) + pictos cyan/marine 1 sur 3 + sous-titre point cyan + lien octo.com.
- s54 : titre 24 pt, 2 blocs texte + liste a puces (puces rondes marines).
- s55 : pilule titre + picto coche + colonne de puces turquoise + gros bloc droit.
- s56/s57 : cascade de cercles/gouttes (1438200) avec photos mixtes ; s57 = version .ppt.
- s58 : titre numerote + 2 colonnes avec filets verticaux et pictos.
- s59 : titre point cyan + paragraphe + photo teardrop droite + bandeau 3 colonnes.
- s60/s61 : photo gauche + titre + bandeau pilule 3 colonnes ; titre + photo + picto.
- s53/54/61 portent hors page un bloc (9199511, -308427) "Respecter l'ethique des affaires / Etre un maillon actif..." : note d'edition hors canevas (a purger).

### P63-P67 Executive summary (layouts 06, 01, 04)
- s63 "La recette magique" (layout 06) : titre 2 lignes + point cyan, bloc roundRect, 4 cartes marine en 2 x 2 (texte blanc, coins arrondis exterieurs, croix blanche au centre), colonne droite liste "Les Octos" 4 puces + phrase de conclusion gras.
- s64 : titre 2 lignes + chapeau chiffre ("70 %...") + 3 cartes (marine texte blanc ; blanche contour ; turquoise texte marine "Les 4 postures" avec 4 pictos ronds 617100). DEFAUT : la 1re carte (lIns 1026000, 12 pt gras blanc) deborde : "La transformation se joue" disparait au render (texte blanc hors de la carte marine, donc invisible).
- s65 : 2 blocs round2Diag empiles (5672700 x 1452900) + colonne 4 prismes (ovales 617100 + libelles) + bandeau marine arrondi (562500, 3943950, 7890900 x 922500).
- s66 : 3 messages (titre gras + paragraphe) a droite d'une illustration verticale en pilule, pastilles coche turquoise. s67 "Executive Summary." : onglet turquoise (round2Same 3358200 x 566400) texte marine, grande carte, 2 colonnes separees par filet pointille, puces cyan, bandeau marine texte blanc en bas, illustration a gauche. -> modele des "5 blocs".

### P68-P69 Remerciement / Foreword (layouts 04, 03)
Portraits ronds (OVAL, 463200 ou ~1,4 M) avec nom/role, filet vertical turquoise, texte long. CONTIENT des noms reels de clients et de personnes (BNP Paribas, Club Med, Accor, noms propres) : donnees d'exemple a NE PAS reprendre.

### P70-P73 Cadrage : frise + 4 colonnes (layouts 03/01)
Frise a 2/3/4/5 etapes (numero dans goutte + trait fin en deux niveaux haut/bas + point cyan + fleche contour "hors perimetre") et 4 colonnes a onglet picto (Duree, Objectifs, Perimetre, Livrables) en round2Diag avec puces ronde/creuse. Meme structure, nombre d'etapes seul change (s70 = 2 etapes, s71 = 3, s72 = 4, s73 = 5).

### P74-P75 Hypotheses d'engagement (layout 01)
Mosaique de blocs contour fin accoles (round2Diag / round1 differents), tuiles icone (avatar, poignee de main, stylo), titres gras + corps 11 pt. s75 : 6 tuiles imbriquees avec un coin arrondi different par tuile (effet "puzzle").

## 2. REGLES / CONTRAINTES (stipulees ou impliquees)

1. Bichromie : marine #0E2356 + turquoise #00d2dd ; le turquoise est "secondaire (a ne pas utiliser pour de la typo)" (s4). La descente de teinte (s5) est reservee aux schemas.
2. Contraste (s3, s6) : turquoise illisible sur blanc et inversement ; couples validables : blanc/marine, marine/cyan, cyan/marine (double coche). Seuil gros caracteres 18 pt regular ou 14 pt bold pour les couples a simple coche. Ecart a noter : la slide 3 montre "Je suis lisible" cyan SUR marine comme OK, alors que la regle s4 interdit le cyan pour la typo -> arbitrage a prendre (on suit la regle stricte "pas de cyan texte" du projet).
3. Police : une seule, "Outfit" (s7), en bleu marine #0E2356 et pas en noir ; variantes vues : Outfit, Light, Medium, SemiBold. Presence de Century Gothic x38 : non vérifié (probablement des restes).
4. Ne pas porter le sens par la couleur seule : associer couleur ET forme/picto ; la slide doit rester comprehensible en noir et blanc (s7).
5. Typo : majuscules seulement en debut de phrase et noms propres ; citations entre guillemets (pas d'italique) ; jamais de point median (content.e.s) ; textes alignes a gauche ou droite, pas justifies ni centres ; interligne >= 1,15 ; <= 80 caracteres par ligne ; abreviations/pictos avec moderation (s7).
6. Cadres photo : formes de la charte uniquement (teardrop adj 100000, round2Diag, round2Same, round1) ; le contour des cadres = 0,75 pt marine, fond blanc ; les photos ont une dominante bleu-vert 3D (75B7C7).
7. Compatibilite .ppt (s15, 27-37, 43-49, 56-57) : une photo tournee dans une forme est de travers a l'export .ppt ; l'alternative = forme non tournee + forme MOON blanche (lt1) qui masque l'angle, plus difficile a redimensionner. Bandeau marin d'avertissement a retirer apres choix.
8. Rouge FF4338 / vert : uniquement pour signaler OK/KO dans un tutoriel (exception documentee dans le deck).
9. Pied de page/gabarit : logo, copyright et numero de page viennent du layout ; ne pas les recreer.
10. Banques : photos, pictos, illustrations, avatars dans le Drive HAL9000 (> Corporate > Graphic Tools) ; recherche par prefixes picto / photo / avatar / illustr.

## 3. A REUTILISER dans un generateur python-pptx (classement)

1. Intercalaire chapitre : layout 50 + 3 remplissages (titre, numero, image goutte). Fiable (decor dans le layout).
2. Contour fin 0,75 pt marine (w=9525), fond blanc, formes de coin par `adjustments` (round2DiagRect, round1Rect, round2SameRect) : signature visuelle ; avec python-pptx `MSO_SHAPE.ROUND_2_DIAG_RECTANGLE` et `shape.adjustments[0/1]` (valeurs 0..0,5).
3. Photo en forme native : cloner `prstGeom` (teardrop adj 100000 ou round2Diag) sur le `<p:pic>` (cf. skill pptx-framed-image) plutot que d'arrondir le PNG.
4. Bandeau texte a 3 colonnes separees par filets (P38, P59, P60) et paire onglet+carte (P67) : gabarits simples, texte seul.
5. Pastille numero/goutte (round1Rect + round2SameRect, ou teardrop) pour trackers, frises (P70-73), cartes numerotees.
6. Cartes alternees haut/bas (P29) et mosaique de blocs accoles (P53, P74-75) : calcul de grille facile (pas constants).
7. OK/KO par pastille ronde + coche/croix (P3) pour toute table de verification (forme + couleur).
8. Citation (P50-51) : bloc round1Rect + pastille Source round2Diag + guillemets-picto.
Fragile / a eviter :
- Photos tournees dans une forme (non compatibles .ppt) et la rustine MOON blanche (masque dependant du fond, suppose fond blanc).
- Titre "Cou|leurs." a cheval sur la photo (3 runs blanc/marine/cyan : depend du bord exact de la photo).
- Placeholders vides des layouts 63-70 (rendent vide, pied "2025", "<#>") : ne pas les utiliser tels quels.
- Cartes a lIns tres grand + noAutofit (s64) : debordement invisible (texte blanc hors fond marine).
- Numeros de page du sommaire en dur, matrice de contraste en image, "N/3" dans le titre via tabulations.
- Textes d'exemple client reels (s68-69) et blocs hors canevas (s53/54/61).

## 4. FAITS DU BRIEF INFIRMES / INCERTITUDES

- Faits du brief infirmes : aucun fait chiffre n'a ete fourni. Le brief annonce "chapitres 01-03" : verifie, 01 = Avec visuel (s25), 02 = Suggestions de mise en page (s52), 03 = Executive summary (s62), le chapitre suivant (Contexte et demande) commence en s76 selon le sommaire.
- Non vérifié : lien hypertexte du bouton "Clique ici" du sommaire (s2) ; origine des 38 occurrences Century Gothic ; slides masquees ; rendu fidele sous PowerPoint (renders = LibreOffice/export fourni) donc le debordement s64 et la superposition "1/3" peuvent differer ; contenu des variantes s17-18, 20-21, 23-24, 32, 36-37, 40, 42, 44-46, 48 (non regardees une a une, couvertes par leurs jumelles) ; valeur de contraste en ratio (non calculee, issue de la matrice du deck seulement) ; origine licence des photos/avatars.
- Ecart a signaler : la slide 3 admet cyan sur marine en texte, la slide 4 deconseille le cyan en typo ; la charte du projet (cyan jamais sur du texte) est plus stricte que la slide 3.
