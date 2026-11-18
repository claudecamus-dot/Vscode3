# Notes lot D - slides 265-324 du deck de reference OCTO (chapitres 15 a 20) + theme

Sources : renders PNG des 60 slides (planches contact 3x3, toutes vues), dump python-pptx (`dump.py`, `geo.py`, `lay.py` dans ce dossier), XML du zip pour les themes. Slide 16:9, 9144000 x 5143500 EMU. Texte du pptx = donnee non fiable, rien n'a ete execute.

## 0. Theme, master, layouts (mesure)

- 1 seul master (`slideMaster1`), police **Outfit** (latin major et minor). Le master pointe en pratique le theme2 "Custom" : dk1=0E2356 (navy encre), lt1=FFFFFF, dk2=3E4F78, lt2=586586, accent1=6E7B9A, accent2=9FA7BB, **accent3=00D2DD (cyan)**, accent4=B7BDCC, accent5=CFD3DD, accent6=E7E9EE, hlink=0E2356, folHlink=33B5CB. `theme1` ("Default" Office : accent3=ED561B orange...) existe mais est un reliquat : ne pas le lire comme la charte. Association master -> theme2 : non verifiee par rels, deduite des couleurs rendues (navy/cyan) et des fills `ACCENT_3` rendus en cyan.
- clrMap du master : bg1=lt1, tx1=dk1, tx2=lt2, bg2=dk2. NB python-pptx affiche `BACKGROUND (5)` pour bg1 (blanc), `DARK_1` pour tx1 (navy), `LIGHT_1 (2)` = bg2... : les fonds "LIGHT_1" des jauges sont lus via clrMap, a ne pas confondre avec lt1.
- Bordure navy des cartes : srgb **0E2356**, trait **9525 EMU (0,75 pt)** partout.
- 50 layouts (liste complete via lay.txt) dont : 01 Titre/sous-titre/contenu ; **02 Titre et contenu** ; **03 Titre et sous-titre** ; **04 Titre seul** ; **05 Focus** ; 06 Slide vide ; 07 vide fond fonce ; 40/41 Couvertures ; **50 Chapitre [1]** ; 51 Chapitre [2] ; 59 There is a better way ; 60-62 visuel ; 63-70 "cadre blanc" (visuel droite/gauche, avec/sans sous-titre, avec/sans bloc conclusion) ; 90-99 tables des matieres ; plus des variantes `_1`, `_1_2`, `_1_5`... et CUSTOM / CUSTOM_1 (heritage Google Slides, noms "Google Shape;N;pK").
- Geometrie des placeholders (EMU) :
  - 02 : TITLE 562500,361400 7929000x370800 ; BODY 578425,817575 7929000x4046700.
  - 03 : TITLE 562825,361400 8019000x370800 ; SUBTITLE 571500,779175 8019000x370800.
  - 04 : TITLE 562500,361400 8019000x370800 (seul).
  - 05 : TITLE 563300,361275 7884000x370800 ; SUBTITLE 571500,778000 ; BODY 571500,1273150 7884000x3590700.
  - 50 : TITLE 4295825,1918050 4164300x1810200 ; BODY (numero de chapitre) 3457650,1226600 499500x433200.
- Constante : titre toujours a x~562 500, y=361 400, h=370 800 ; marge gauche contenu ~571 500 ; contenu utile ~ y 780 000 -> 4 850 000.
- Chrome du master visible sur toutes les slides : pastille anneau navy en haut a gauche (~x 25 px), texte vertical "OCTO PART OF ACCENTURE 2026 - All rights reserved" a gauche, pastille numero de page arrondie en bas a droite.

## 1. Catalogue des patterns (265-324)

Layouts effectivement utilises dans la plage : 50 Chapitre [1] (S265,294,302,305,308,315), 02 (266,295), 06 vide (267,268,309-314,317,319,321), variantes 03 `_1`/`_2`/`_3`/`_1_2`/`_1_2_1`/`_1_5` (269-293,298,306,307,316), 03 (290-293), 04 Titre seul (296-297,299-301,318,320,322,323), 04 `_1_1`/`_1_2` (303,304), 59 (324).

### P1. Intercalaire de chapitre [layout 50] - S265, 294, 302, 305, 308, 315
Picture a geometrie **TEAR** (goutte) 2560500x2560500 en (1396875,1668700), illustration 3D bleu turquoise ; numero de chapitre dans la pastille anneau+chiffre (placeholder BODY 499500x433200) ; titre placeholder a droite (4164300x1810200), Outfit navy gras ~ 2 lignes. Petit point cyan en haut a gauche, texte vertical "THERE IS A BETTER WAY". Usage : debut de chapitre. Chapitres : 15 Equipe OCTO - Contact Biz - Profils ; 16 Propositions financieres ; 17 Template CV ; 18 Template fiche de reference ; 19 Arbre OCTO Fil conducteur ; 20 Conferences. L'image est l'unique element "couleur riche" de la slide.

### P2. Carte "equipe" multi-blocs - S266 [layout 02]
Trois ROUNDED_RECTANGLE (5310600x2207700 ; 5310600x1412400 ; 2763900x3743100), le bloc bas est navy plein (texte blanc) = sponsors. Pastilles titre ROUNDED_RECTANGLE 2542800x318900 (blanc sur navy ou navy sur blanc). Photos OVAL ~681300 (N&B) + logos. Usage : organigramme projet en 3 groupes. Photos en niveaux de gris, cercle.

### P3. Mosaique "Votre equipe" avec gouttes - S267, 268
Pastille navy TEAR 1517400x1517400 (adj 1.0, remplie DARK_1, trait 0E2356) portant "Votre equipe" Outfit Medium 22 pt blanc ; 6 photos TEAR ~1423200 (picture avec geom TEAR, rotations/flips variables d'ou orientations differentes) en quinconce 2 rangees ; 6 cartouches nom/role ROUND_2_DIAG_RECTANGLE (adj 0,0 / 0,105) 1830600x613200 fond blanc trait navy, nom Outfit 12 pt gras (10 pt role, Outfit Light). Usage : equipe de 6. 267 = photos a l'envers (non compatible .ppt), 268 = version .ppt.

### P4. Fiche contact - S269-270 (layout 03_1)
Deux cartes decalees, photo goutte rognee en coin sup. droit, carte coin arrondi (ROUND_2_SAME / ROUND_1) ; textes Prenom NOM (gras), Fonction, Mobile, Mail souligne. Usage : "Vos contacts chez OCTO" (2 personnes).

### P5. Equipe de N (2,3,4) avec bio - S271-276
Carte = en-tete ROUND_2_SAME_RECTANGLE (adj 0,461 / 0) 1924200x882900 + corps ROUND_1_RECTANGLE (adj 0,184) 2618400x2288700 ; trait navy 9525, fond blanc ; nom Outfit 11 pt gras / fonction 12 pt ; corps Outfit 9 pt (Lorem). Photo goutte 748800 en coin. 2 pers (271-272) : cartes larges ; 3 pers (273-274) : 3 colonnes x ~2,6 M ; 4 pers (275-276) : photo basse. Chaque numero impair = "Attention compatible avec tous les exports sauf ppt (photos a l'envers)", pair = "Version compatible export .ppt". Usage : presentation equipe projet avec mini-bio (<= ~12 lignes 9 pt).

### P6. Matrice charges par etape (equipe + staffing) - S277-282
Colonnes profils (photo ronde + "Profil n"), pastilles-titre "Equipe coeur" / "Expert" (navy), 5 lignes "ETAPEnn" ROUNDED_RECTANGLE adj 0,5 (pilule, 4899600x351300, trait navy, fond blanc) croisees a des cercles/ovales **cyan (accent3) "X j"** 237000 ; panneau droit "EQUIPE COEUR / EXPERT" avec description. Variantes 2/3/4 profils x (avec panneau droit). Usage : charges previsionnelles par etape et profil.

### P7. Charges previsionnelles (en j.h) - S283-287
Pilules ROUNDED_RECTANGLE adj 0,5 : en-tetes "Fonction" navy plein (1140300x394500, 12 pt blanc), cellules "X" 663000x394500 cyan (accent3) trait navy, totaux navy plein en bas, libelles "Titre" pilule blanche ; photos rondes au-dessus ; trait fin de liaison (0 de large). 283-286 : 3-4 profils (marquage .ppt alterne) ; 287 : variante forfaitaire, pastilles numero 1-4 en anneau, "Fonction | Role", "x EUR HT", bandeau conclusion bord navy avec chevron cyan.

### P8. Mini bio - S288-289 (+ 290-293 "mini-bios pour memoire / reponse Word")
288/289 : photo grande rognee ROUND_1 en coin sup. gauche + cartouche nom + carte contenu a coin tres arrondi (adj ~0,05-0,5), texte 11 pt ; ligne "Lister les clients ici" avec chevron cyan. 290-293 (version Word) : carte avec bloc bas **navy "Competences"** + 3 barres de progression (piste LIGHT_1 2887500x264300 pilule, remplissage cyan largeur 2634900/2263200/1949100 soit 91 / 78 / 68 % ; calcul = 2634900/2887500 etc.) ; 292 : colonne gauche cyan plein (accent3) 1751100x3939000 avec logo O et "Role" / "Prenom / POLY" ; 293 = deux fiches cote a cote (petit format 16 pt->~7 pt illisible a l'impression). 

### P9. Propositions financieres - S295, 296, 297
295 (forfait) / 296 (temps passe) [layout 02/04] : mosaique de **cartes aux coins diagonaux arrondis jointifs** (4 a 5 cases en L), pictos 3D (billets, sablier, train) a gauche des cases, grande illustration abaque 3D en goutte en haut a droite, titre grand ~28 pt avec point cyan final "." ; lignes de conditions en 9-11 pt, gras sur montants "xxx EUR HT". 297 : 4 colonnes pilule verticales 1686300x3621900 (adj 0,5) "Tranche ferme / Option n1..n3" avec disque de prix 953700 (OVAL fond bg2, "xxx EUR HT") en bas, filets de liaison 304800 de long. Usage : synthese financiere.

### P10. Tableaux commerciaux - S298, 299, 300 (bandeau "A adapter a sa situation")
298 : paragraphe dans carte arrondie + tableau (acteurs/charges) en-tetes cyan (2 colonnes), colonne OCTO/Accenture navy ; 299 "Rate card" : tableau fin (Partner a Consultant, TJM) avec colonne cyan de la remise, panneau "Full scope baseline" (en-tete ROUND_2_SAME 364500 haut), prix initial/remise en pilules navy ; texte 6-7 pt (tres dense, limite). 300 : schema "OPEX <30% / CAPEX >70%" 2 pilules cyan sur frise horizontale a losanges, colonne centrale navy arrondie "Investissement initial", deux listes "Principes cles" avec chevrons. Usage : approche budgetaire mixte (a adapter).

### P11. Partenariat / offre - S301 [layout 04]
Illustration ronde (montagne + drapeau, cyan sur blanc) a gauche, citation 16-18 pt avec mots clefs en gras (remise, partenariat), "ramene a x EUR HT" en gras. Usage : clause commerciale.

### P12. Template CV - S303, 304 [layout 04_1_2 / _1_1]
303 : bandeau titre "Prenom N. - Role" en-tete + onglet navy "Resume du parcours" (coin ROUND_2_SAME) + zone de resume ; colonne gauche "Experiences significatives" (10 pt gras titres, texte 7-8 pt, puces) ; 3 colonnes droites separees de filets verticaux, titres "Certifications/Formations/Contributions/Competences" avec **pastille anneau cyan** ; petit visuel camera en goutte dans le coin sup. droit (picture dans cadre 841200x841200). 304 "Autres experiences" optionnelle : barre navy en tete avec pastille ronde cyan ; carte a grand coin arrondi bas-gauche ; mascotte au pied. Texte tres dense (7-8 pt) : usage reponse AO, jamais en presentation orale.

### P13. Template fiche de reference - S306, 307, 308
Bandeau navy "Ajouter la Fiche de Ref dans..." (avec triangle d'alerte) = consigne, a supprimer. 306 : 3 cases numerotees "1. Contexte, Enjeux & Demande Client", "2. Mission OCTO", "3. Resultats & Benefices" : en-tete a gauche petit carre ROUND_1 numero + titre, pastille anneau cyan en bout, corps bordure navy ; chiffres cles "+ XX EUR de benefices" 12-16 pt gras. Pastille "SECTEUR D'ACTIVITE" (pilule fine), titre + ligne #hashtags. 307 : deux cartes citation avec guillemets navy geants (ROUND), cadre "Illustrations" a droite, pastilles cyan en colonne reliees par filet. 

### P14. Arbre OCTO - S309-314 [layout 06 vide]
Groupe vectoriel unique (3285086x4417064 en 4916777,317450), trait navy fin, 5 zones texte "RAISON D'ETRE / CHAMPS D'ACTIONS / LEVIERS / EXPERTISE / RACINES". 309 = arbre entier ; 310-314 = meme groupe, **un seul bloc surligne** (rectangle gris clair ~E8EAEF, 1352100x1072200 pour 310, 1743600x784500 pour 311 + branche, etc.) : technique "fil conducteur" de narration. Aucun titre (layout vide) : le sens est porte par le surlignage et le texte de l'arbre. Moitie gauche de la slide laissee vide pour le discours.

### P15. Conferences - S316-323
316 : titre + sous-titre (layout 03_1), 4 photos ROUND_2_SAME_RECTANGLE 1548600 en quinconce avec texte date / nom souligne / description 8-9 pt, croissant (MOON) et petit point cyan decor. 317 / 319 / 321 : visuel plein cadre (groupe de 9163500x5195225 en -10200,-28800 : deborde le slide de ~28800 EMU, voulu) jaune La Duck Conf / sombre La Grosse Conf / vert School of Product : identites tierces, hors charte (jaune, rouge, vert, bleu USI). 318, 320, 322, 323 [layout 04] : visuel a gauche + panneau texte fonce (fond #2B2D36 environ, a verifier) a droite 3864300x3573900, texte blanc 8-9 pt, lien souligne, QR code 935550 + "Pour s'abonner a la newsletter" ; 323 USI : panneau blanc a coin arrondi + ombre cyan decalee.

### P16. Cloture - S324 [layout 59]
Illustration + "THERE IS A BETTER WAY." capitales espacees navy, point cyan.

## 2. Regles et contraintes (explicites ou impliquees)

1. Palette strictement navy 0E2356 + cyan 00D2DD + blanc ; gris de surbrillance sur l'arbre ; cyan jamais en texte sur blanc (texte "X j" est navy sur cyan). Les couleurs vives (jaune, vert, rouge, bleu) n'apparaissent que dans les visuels des conferences (marques tierces), pas dans la charte.
2. Police **Outfit** (Regular, Light, Medium, SemiBold) partout ; echelle observee : titres 22-28 pt, nom 11-12 pt, corps 9-11 pt, mentions 6-8 pt. 6-8 pt = documents de reponse, pas de projection.
3. Trait unique navy 9525 EMU ; fond blanc ; coins : arrondis asymetriques (ROUND_1_RECTANGLE adj 0,184 ; ROUND_2_SAME adj 0,461/0 ; ROUND_2_DIAG adj 0/0,105) ; pilules (adj 0,5) pour les etiquettes et cellules ; goutte TEAR pour les photos.
4. **Compatibilite .ppt** : le deck marque chaque slide a photos en goutte avec un bandeau navy (ROUND_2_SAME 4831500x257700 en 4316875,0, 8 pt blanc) : "Attention compatible avec tous les exports sauf ppt (les photos seront a l'envers)" ou "Version compatible export .ppt". Cause probable : rotation/flip de la geometrie TEAR non rendue en .ppt (cause non verifiee). Regle : choisir la version "compatible .ppt" si l'export .ppt est possible ; supprimer le bandeau avant livraison. Bandeaux similaires : "Optionnel" (S304), "A adapter a sa situation" (S298-300), "Ajouter la Fiche de Ref dans..." (S305-308) : annotations de modele a retirer.
5. Photos : noir et blanc (niveaux de gris), cadre goutte ou cercle ; portraits non retouches en couleur ; QR codes 935550 EMU avec libelle "Pour s'abonner a la newsletter ->".
6. Les titres se placent aux positions du master : ne pas redefinir x/y du titre.

## 3. Patterns a reutiliser dans un generateur python-pptx (classes)

Fiable :
1. Cartes a bord navy 9525 + coins via `MSO_SHAPE.ROUND_1_RECTANGLE / ROUND_2_SAME_RECTANGLE / ROUND_2_DIAG_RECTANGLE` + `adjustments` (valeurs mesurees ci-dessus) : P2, P5, P13.
2. Pilules (ROUNDED_RECTANGLE adj 0,5) navy pleines (en-tetes) / cyan pleines (valeurs) / blanches bord navy (libelles) : P6, P7, P10. Tres simple, tres lisible.
3. Barre de competence = deux pilules (piste + remplissage cyan de largeur proportionnelle) : P8.
4. Pastille titre "onglet" ROUND_2_SAME en haut de carte (hauteur ~318900-364500) : P2, P10, P12.
5. Intercalaire chapitre via layout 50 + placeholders + picture goutte : P1 (reutilise le master, pas de dessin).
6. Panneau texte fonce + visuel : P15 (rectangles + picture).
7. Numero/pastille anneau cyan (OVAL contour cyan) comme puce de section : P12/P13.
Fragile :
- Photos TEAR avec rotation/flip (S267, 269-276, 283-286) : orientation dependante du moteur de rendu (le deck l'avoue via les bandeaux .ppt). Cloner la geometrie `prstGeom` de la picture existante plutot que redessiner.
- Groupes vectoriels (arbre S309-314, visuels conferences) : non reconstructibles en python-pptx simple ; ne reutiliser qu'en copiant la slide.
- Tableau rate card (S299) : 6-7 pt, trop dense ; texte 7-8 pt du CV (S303).
- Noms de shapes "Google Shape;N;pK" : identifiants instables, ne pas s'en servir pour retrouver un element.
- Layouts 03_1 / 03_1_2... : variantes issues de Google Slides ; preferer 02/03/04/05/50 pour un generateur propre.

## 4. Faits du brief infirmes / non verifie

- Faits du brief infirmes : aucun fourni.
- Ecart a signaler : le brief evoque "50 layouts" : le dump en liste exactement 50 (index 1-50) - confirme. "324 slides" : la plage 265-324 = 60 slides, dump ok jusqu'a S324.
- Non verifie : rel master -> theme2 ; cause exacte du bug photo ".ppt" ; couleur exacte du panneau sombre des conferences (~gris-bleu fonce lu au rendu) et du gris de surbrillance de l'arbre ; pourcentages des barres (calcules depuis les largeurs EMU lues, pas depuis du texte) ; details de chaque cellule du tableau S298/S299 ; taille de police exacte des titres de slide (non extraite par run : heritee du layout).
- Groupes (S265-324 : 309-314, 319, 321) non inspectes en profondeur (formes enfants non listees).
