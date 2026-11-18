# Lot B : slides 76-154 du deck de reference OCTO (chapitres 04 a 08)

Sources : 79 slides vues en planches de contact (m00..m13.png, 6 slides chacune, toutes lues), dump python-pptx (dump.txt, det1.txt, det2.txt). Slide 16:9, 9144000 x 5143500 EMU.

## 0. Faits de base (mesures)

- Le theme REELLEMENT utilise par le master est `ppt/theme/theme2.xml` (theme1 = palette Google par defaut, inutilisee ici) : dk1 = 0E2356 (navy), lt1 = FFFFFF, dk2 = 3E4F78, lt2 = 586586, accent1 = 6E7B9A, accent2 = 9FA7BB, accent3 = 00D2DD (cyan), accent4 = B7BDCC, accent5 = CFD3DD, accent6 = E7E9EE. Les formes referencent des `schemeClr` (dk1/lt1/accent3...), pas des RGB : un generateur qui ecrit des RGB en dur ne suit pas le theme.
- Polices : Outfit (corps), Outfit Medium (en-tetes de tableau, 12 pt), Outfit SemiBold (numeros/titres), Outfit Light (calendrier). Theme majorFont/minorFont = Arial (fallback). Quelques residus : Century Gothic, Helvetica Neue Light sur des formes vides (heritage Google Slides, a ne pas reproduire).
- Tailles de texte mesurees : titres de cartes 11 pt, puces 9 pt (niveau 1) / 8 pt (niveau 2), en-tetes de tableau 12 pt, cellules de tableau 9 pt, gantt 9-10 pt, calendrier 8-9 pt (6 pt pour les dates de semaines en S128, mesure sz=600).
- Filet standard : 9525 EMU (0,75 pt), solidFill dk1, prstDash solid. Pointilles `dot` pour les separateurs de lignes de tableau, `dash` observe en S128.
- Layouts utilises : "50 - Chapitre [1]" (intercalaires), "03 - Titre et sous-titre_1" (majorite, 40 slides, sans titre rempli sur les maquettes), "04 - Titre seul" (tableaux + quelques cartes), "03 - Titre et sous-titre" (calendriers/planning), plus variantes _2, _1_1, "01 - Titre, sous-titre et contenu" (S94).
- Les slides `03 - Titre et sous-titre_1` ont deux placeholders (titre y=361400 h=370800, sous-titre y=779171 h=370800, x=562825/571500, w=8019000/8041500) souvent vides : zone utile commence a y ~ 1,2 M EMU (1218475-1218950 constant).

## 1. Catalogue des patterns

Marges recurrentes : x gauche ~ 549-700 k, droite ~ 8,45-8,6 M ; haut utile ~ 1,21 M ; bas ~ 4,86 M. Numero de page = pastille en bas a droite (layout).

### Intercalaires de chapitre (S76 Contexte et demande 04, S83 Demarche 05, S95 Details etapes 06, S113 Planning 07, S134 Tableaux 08)
Layout "50 - Chapitre [1]". Placeholders : titre (4295825,1918050 ; 4164300x1810200), numero "NN" (3457650,1226600 ; 499500x433200), image goutte 2560500x2560500 en (1396875,1668700) (S113/S134 : y=1659800). Goutte = photo/3D dans un cadre a coins arrondis (forme teardrop-like), titre navy gras. Point cyan decoratif haut-gauche. Regle projet existante : un chapitre se cite par son NOM.

### P1 Onglet vertical + carte, paires (S77, S78, S96, S97)
- Onglet gauche : round2DiagRect (adj 50000/0) 919500 x 2891400 (S77) ou 1024500x1700400 (S78), fill lt1, filet dk1 9525. Contient un cercle 641100 (S77) / 714300 (S78) avec pictogramme (~375-430k) et un libelle 11 pt dessous ("Contexte", "Demande").
- Carte contenu : round1Rect adj 19420, 2818800 x 2495700 (S77), colle a l'onglet (x onglet+920k), texte puces 9/8 pt dessus.
- S77 : 2 blocs cote a cote (x=697300 et 4707550, y=1218475) + bandeau de synthese rounded rect en bas (S77, chevron cyan a gauche). S78 : onglets empiles (2) + grande carte 4726800x3400500 a gauche + carte de conclusion a droite (6279375 x ... , chevron cyan entre les deux, 179627x239247). S96/S97 : variantes "Demarche/Livrables/Prerequis" (onglet 954600 x 3398400 ; carte 2926500 x 2952300 ; deux colonnes x=549425 et 4712775). S98 : meme chose en 4 groupes 3881830x1618399.
- Quand : paires contexte/demande, demarche/livrables, prerequis ; 2 a 4 blocs.

### P2 Onglet haut ("tab") + carte, S99-S102
Onglet round2SameRect 1041600 x 354000 pose au-dessus de la carte round1Rect (S99, carte 2926500x2952300), cercle-pictogramme qui deborde a gauche. S100/S101 : grilles 2x2 de groupes 3881125 x 1554600 (x=550125/4713463 ; y=1296475/3048175). S102 : onglets a 3 hauteurs (1434900 / 2689500 / ...) + bandeau "Resultats pour le client" (rounded rect 7677300 x 624900, chevron cyan). Variante S103 : une carte 7621500x1902000 en 3 colonnes de 3 puces avec onglets 2538600 de large.

### P3 Trois ou quatre cartes avec en-tete et signes + / = / puces cyan (S80, S81, S82)
- S80 : 3 cartes round1Rect adj 16667, 2168400 x 3407100 (y=1457275), entete round2SameRect 2168400 x 240600 (y=1216669), pictogramme dans un cercle 506400 (+ disque cyan 00D2DD de 328200 portant "+" et "=") : equation Contexte + Cas d'usage = Format.
- S81 : 3 cartes 2285100 x 3189300, entete 472200 de haut, disques cyan 295800 entre les cartes (chevauchement du joint). S82 : 4 cartes 1771800 x 3189300. Le disque cyan est un aplat sans texte (OK charte : cyan en aplat).
- Pas fixe : espacement ~ 2,0-2,8 M selon N. Quand : composition de formule, etapes liees causalement.

### P4 Matrice Activites / Livrables par etape (S84, S85, S86) -- pattern central du chapitre Demarche
- Rangee d'en-tetes en haut y=1370200 h=243900 : round2DiagRect (adj 0/50000) pour les premiers, round2SameRect (adj 33836/0) pour le dernier ; pastilles "1." "2." ... = teardrop (prst `teardrop`) 309900 x 309900 centrees sur la jonction (x - ~165k).
- Corps : un grand rect arrondi 7529700 x 1385700 (adj 20445) par ligne, filets verticaux (LINE 9525) entre colonnes, filet horizontal central. Bande verticale navy (dk1, round... adj 50000) 303300 de large a gauche avec libelles "Activites"/"Livrables" pivotes a 270 deg, texte lt1 11 pt (zones 1687800 x 293700, 1365000 x 293700).
- Largeur colonnes : 3 colonnes ~ 2,2-3,06 M ; 4 : ~2,3-3,06 M ; 5 : ~1,65-2,29 M (largeurs inegales dans la maquette = a regulariser).
- Quand : 3 a 5 etapes avec double lecture activites/livrables. Texte puces 9/8 pt. Reutilisable tel quel.

### P5 Cartes numerotees avec bande Livrables (S87, S88, S89, S91)
- S87-S89 : 2/3/4 groupes (3807727 / 2513402 / 1843975 de large, 3645899 de haut, y=1218650) : carte rect arrondi, titre, pastille ronde numerotee (cercle double filet, numero 1..4, cyan sur le cercle de contour), puces, filet horizontal, libelle "LIVRABLES" (gras navy majuscule) puis puces.
- S91 : cartes avec onglet haut + numero hors carte a gauche (cercle 1/2/3 a cheval sur le bord) + zone LIVRABLES en bas : icone fichier (326050 x 426318), filet pointille (LINE 6520200 de long, y=3942902), textes 1874100 x 835500.
- Quand : etapes sequentielles avec livrable propre a chaque etape.

### P6 Colonnes "ongles" numerotees avec pictogramme (S90)
4 cartes round1Rect adj 26397, 1580100 x 2801400, encadrees d'un onglet haut compose de 2 formes (round1Rect 516000x441900 pictogramme + round2SameRect 441900x462300 numero "1." en Outfit SemiBold 11 pt). Texte plein (lorem 4 paragraphes, 9 pt). Quand : 4 axes avec beaucoup de texte descriptif.

### P7 Chemin en serpentin (S92) et Notre proposition de demarche (S93, S94)
- S92 : deux onglets "1. Demarche" / "2. Livrables" relies par un chemin (LINE + ARC 1430100 de diametre aux virages), 2 colonnes de puces separees par filet, pastille objectif cyan (disque 426300) + "Objectif de l'etape" en pied.
- S93 : timeline sinueuse "Notre proposition de demarche" (titre rempli en 18 pt environ dans le placeholder), 5 phases en gelules (01 Lancement... 05 Trajectoire) sur un chemin a ARC, jalons = cercles 2 anneaux dont un cyan plein, etiquettes alternant dessus/dessous avec filets pointilles, bandeau Objectifs en rounded rect 7690500 x 1313400 avec pictogramme cible. Tag "A adapter a sa situation" en haut a droite. Quand : demarche en 4-5 phases avec jalons.
- S94 (layout 01) : 4 piliers : ovales 845700 (pictos cyan) au-dessus de 4 cartes titre+puces, + bandeau d'application en bas (puces cyan numerotees = aplat cyan avec texte navy). Titre en anglais dans le gabarit, sans impact.

### P8 Bandeaux de synthese (S104, S105, S106, S107)
- S105 : 3 gelules (rounded rect 3082800 x 703500 etc.) "OBJECTIFS / PRE-REQUIS / INDICATEURS" avec pictogramme a gauche, sous-titre en majuscules 7-8 pt, + rangee de 5 cercles 1..5 (notation) et bloc texte. S106 : "Template recommendation" : 4 gelules empilees (3109200 x 820800) + gros panneau navy a droite "NOTRE PROPOSITION DE VALEUR" (rounded rect 4026000 x 4009200, texte blanc sur dk1) ; l'entete navy contient le texte blanc, le plan d'action en dessous sur fond blanc. S107 : "Profil exemple entite" : tableau d'entete (1 ligne), radar (cyan), bandeaux navy "Perimetre", "Les constats cles" (pastilles 1-4), citation avec guillemets, 3 cartes Forces/Faiblesses/Perspectives (round2SameRect titre navy 244500 de haut).
- S104 : 3 colonnes de 3 puces dans une grande carte + colonne droite ; 4 dernieres cartes (S103-S104) dont une navy pleine (texte blanc) pour l'accent « 1 sur N ».

### P9 Pictogramme en pastille + bloc texte (S109, S110, S111, S112)
- S108 : 5 "gouttes/cloches" (round2SameRect hautes) sur un axe temporel (LINE 7034400 de long, y=4095627) avec jalons ovales cyan 295800 et mois dessous (Janvier..Mai). Rend une frise courte.
- S109/S110 : 5 colonnes de pas 1,725 M (x=538744, 2263468, 3988191...), pastille teardrop 728400 (numero "1." gras 24 pt environ, a verifier) + disque cyan 295800 au coin + filet vertical pointille 612600 + bloc "Title text block" (titre + 9 pt). S110 : meme chose avec pictogrammes. S111 : 4 colonnes de 1355620 x 1185837 (pas 2228625), pastille numero cyan 4 coins. S112 : 6 blocs 2x3, cercle pictogramme 1072469 + etiquette "01..06" en onglet.
- Quand : 4 a 6 items egaux avec pictogramme et courte description.

### P10 Plannings a barres (gantt) (S114, S115, S116, S117, S119, S120, S121)
- S114/S115 : gantt a lignes. Entete temporel = rounded rect (adj 50000) plein dk1, texte lt1 9 pt, 5608800 de large, h=289800 (y~1,21 M) ; colonne LIVRABLES = gelule dk1 1497000 x 289800 ; chaque ligne : etiquette "ETAPE 0N" (gelule filet 696900 x 268800, 9 pt gras majuscule), piste = gelule filet 5608800 x 268800, barre cyan accent3 de largeur variable (ex. 3660300) au meme y, texte 10 pt navy sur cyan ; case livrable gelule filet. Pas de ligne : ~ 336-505 k.
- S116 : gantt avec bandeaux d'etapes (rounded rect 8002500 x 666900) contenant barres navy (Termine), cyan (En cours), gris-bleu bordure (A faire) + losange jalon (diamond filet) ; legende en rounded rect haut-droit. S117 : variante epuree : barres fines (FREEFORM h=66572) + labels etape dans blocs round2DiagRect.
- S119 : planning ateliers par axes (3 bandeaux gelule 8061600 x 795300, y=1665308/2544154/3422976, pas 878846), entete "Semaine N" gelules navy, labels pivotes a 45 deg, jalons cercles, legende (losange cyan / cercle / fleche).
- S120 : projection par lots (cercle numero + gelule label 150-200k, piste, barre navy avec marqueurs/pastilles de texte 6-7 pt, ligne Pilotage cyan pleine). S121 : planning annuel sur 2 annees (labels 2025/2026, gelules de mois, lignes Team building navy / Retro blanc, bloc central). Tag "A adapter".
- Quand : echeancier d'etapes avec livrables.

### P11 Frises / timelines (S118, S129, S133)
- S118 : 4 phases (Observer, S'orienter, Decider, Agir) = axe horizontal (4 segments, le dernier fleche navy), batons verticaux de hauteur variable (LINE) avec etiquettes ; phase en 18 pt navy sous l'axe. Fond blanc, segments cyan puis navy (progression de teinte, pas de sens ecrit).
- S129 : retroplanning par phases : 3 colonnes de teinte cyan croissante (RECTANGLE 2098800 x 2403000, 3 niveaux de cyan clair -> cyan), pastilles etiquettes navy a coins arrondis, ovales cyan (Ateliers), cadre rounded rect 8641500 x 2403000, illustration en bas-gauche, legende 2 pastilles (navy Product Design / cyan Data).
- S133 : retroplanning en fleches (chevrons) : Cadrage / Conception / Construction / Mise en production : 4 chevrons (hauteur ~343475 ; largeurs 1779885..2962909, cyan clair -> cyan -> navy), losanges jalons, cartes-livrables rounded rect blanches filet, texte de validation en 7-8 pt, durees "1 mois" en onglets.

### P12 Calendriers (S122-S128, S123)
- S122 : semaine de 7 jours : numeros 19..25 en tres grand (~44 pt, a verifier), jours "LUN..DIM" en dessous, week-end en cyan (texte cyan : A NE PAS REPRENDRE, voir contraintes), lignes de notes pointillees, titre mois "OCTOBRE 2026".
- S123 : 12 mini-calendriers (TABLE chacun, 8 lignes, lignes de 128400 a 205750, police 8 pt Outfit Light/Medium) ; en-tete mois navy, jours hors mois en gris clair, numeros de semaine en colonne cyan. S124/S125 : 6 mini-calendriers + 3 blocs de commentaires, jours surlignes cyan clair. S126/S127 : semestre en semaines (TABLE 2 x 26 colonnes de 303375, en-tete mois 381000 navy ; ligne semaines cyan "S1..S26", colonnes pointillees pour poser des barres). S128/S130/S131/S132 : trimestre (13 semaines, dates "du .. au .." en 6 pt). Quand : calendrier de reference sous lequel on dessine des barres.

### P13 Tableaux (S135-S148) -- chapitre 08
- Tableaux simples (S135-S141) : calque identique. TABLE a 3-5 colonnes (largeur totale 7239000 = 3x2413000 en S135, x=952500, y=1212300), 1 ligne d'en-tete h=382675 fill dk1 (navy), texte lt1 Outfit Medium 12 pt aligne a gauche, marges cellule 91425 ; lignes de corps (h 1032300 pour 3 lignes, 3096925 pour 1 ligne...) texte 9 pt Outfit navy. Bordures de cellule 9525 dk1 ; filets horizontaux internes en `dot`, verticaux `solid`. Style de tableau {B3D40B02-709E-48B9-A1EB-56233A99632D}, tblPr noFill. Habillage par formes : round2SameRect navy 7239000 x 172200 au-dessus (y=1131850) pour arrondir les coins de l'en-tete, et round2SameRect accent3 (cyan, 172200 de haut) en pied (y=4691900) comme bandeau de fin ; le tableau lui-meme a des angles droits cache par ces caps.
- Tableaux croises (S142-S146) : meme habillage mais colonne titres a gauche (round2SameRect 5794200 de large pour l'en-tete decale, x=2397250), colonne de gauche 1444750 de large, 2 colonnes de donnees 2897125, titres de lignes 12 pt Outfit Medium navy.
- S147 : tableau de gelules : en-tete gelule dk1 (round... 5 colonnes), lignes = gelules a filet ; chaque rangee = 1 etiquette gelule a gauche + piste de 5 cellules (chaque cellule = rounded rect filet), reliees par un filet pointille. S148 : meme grille avec indicateurs de maturite = 3 cercles (blanc / cyan / navy) par cellule.
- S149/S150 : tableau-carte : en-tete navy ROUND_1 (465000 h), lignes avec pictogramme + libelle gras + puces, chevron cyan, carte de conclusion a droite (round2Diag 2147700 x 3645600). S151-S153 : grilles de 4, 6, 8 cellules : rect arrondi unique 2 coins diag + croix centrale "pincee" (4 quarts de cercle formant des arcs concaves aux croisements), texte 9-10 pt. S154 : template CIR : 7 cartes (3x2 + 1 + 1 large) avec en-tetes navy round2SameRect 2475600 x 340000 et deux en-tetes cyan (accent3) pour les cartes de sortie (Livrables, Benefices) — meme logique « un sur N en accent ».

## 2. Regles et contraintes observees ou implicites

1. Palette : navy dk1 0E2356 pour tous filets, textes et aplats sombres ; blanc lt1 pour fonds et texte sur navy ; cyan accent3 00D2DD en aplat uniquement (barres, disques, pied de tableau, pastilles). Le cyan sert aussi de TEXTE dans la maquette S122 (24 / SAM, 25 / DIM) : c'est une exception du template a NE PAS reprendre (charte projet : le cyan ne porte jamais de texte, contraste ~1,9:1 sur blanc, non remesure ici). Palette secondaire gris-bleus (dk2 3E4F78, accent1 6E7B9A, accent2 9FA7BB, accent4-6) pour calendriers, jours hors mois, etats "A faire".
2. Teintes cyan clair des phases (S129, S133, S115) = tints du cyan accent3 (non verifie les valeurs exactes de lumMod/alpha).
3. Filets : 9525 EMU solid navy partout ; pas d'ombre ; pas de degrade sur les formes (a part les photos des intercalaires).
4. Coins : trois familles de geometrie, toujours avec des angles opposes arrondis : round1Rect (un angle), round2SameRect (deux angles hauts, "onglet/en-tete"), round2DiagRect (deux angles diagonaux, "feuille"), plus rounded rect adj 50000 (gelule) pour pistes/gantt/KPI, et teardrop (goutte) pour pastilles numerotees. Rayon via adj (valeurs vues : 16667, 19420, 20445, 26397, 33836, 50000 ; les petites valeurs 5301 etc. sont des quasi-rectangles).
5. Hierarchie typographique : titre de slide (placeholder, navy gras) ; sous-titre 18 pt ; titre de carte 11 pt ; puces 9 pt / 8 pt ; libelles gantt/legendes 6-10 pt ; tableaux 12 pt (en-tete) / 9 pt (corps). Le plancher observe est 6 pt (dates S128) : trop petit pour du fond de slide.
6. Compatibilite .ppt vs .pptx : aucune mention explicite dans ces slides ; les formes round1Rect/round2SameRect/round2DiagRect/teardrop sont des presets OOXML (ISO 29500), absents ou approximes dans l'ancien format .ppt binaire ; le tableau utilise un tableStyleId (rendu fidele seulement en PowerPoint recent). Non verifie : aucune conversion .ppt testee.
7. Etiquette meta "A adapter a sa situation" (round2SameRect dk1, 1614000 x 257700, en (7534150, 0), texte blanc) presente sur S93, S114, S115, S118, S119, S120, S121, S129, S133 : c'est une annotation du template, a supprimer en production. Note : x + largeur = 9148150 > 9144000 (depasse de 4150 EMU) donc ce tag deborde de la slide ; ne pas reprendre sa geometrie.
8. Pictogrammes : images PNG (PICTURE, ~293-430k de cote) dans cercle double filet, cyan+navy bicolore ; aucune icone vectorielle ici.
9. Photos (intercalaires) : cadre goutte 2560500 x 2560500 forme "round2DiagRect"/teardrop ; la geometrie est celle de la forme, pas du PNG (cf. skill pptx-framed-image) -- non verifie ici (image seule vue).
10. Cartes : bord interne de texte, marges 91425 (7,2 pt) ; zone texte de carte = bord - ~100 k.
11. Cle d'alignement : toutes les cartes de la zone utile partent de y ~ 1,2 M et finissent a y ~ 4,86 M (hauteur utile ~ 3,65 M) ; colonne gauche x ~ 549-700 k ; droite ~ 8,43-8,6 M.

## 3. Patterns a reprendre en python-pptx (classement)

Robustes (a reprendre en priorite) :
1. Matrice Activites/Livrables (P4, S84-S86) : formes simples (round2Diag/Same, rect arrondi, lignes) + texte pivote 270 deg ; reglage par pas de colonne.
2. Gantt a gelules (P10, S114/S115) : une piste gelule + barre cyan + case livrable ; calculer x/largeur a partir de dates ; trivial, tres lisible. A decliner en barre navy pour l'« un sur N ».
3. Tableaux simples/croises (P13, S135-S146) : python-pptx cree le tableau ; il faut poser fill/borders par cellule (XML tcPr lnL/lnR/lnT/lnB, solidFill) et ajouter les deux caps round2SameRect (navy en tete, cyan en pied) ; borders `dot` via prstDash. Le style id n'est pas indispensable (tout est explicite dans tcPr).
4. Cartes avec onglet (P1/P2/P5, S77-S102) : 2 formes (onglet + carte) a coller ; adj via `shape.adjustments`.
5. Pastilles numerotees teardrop / cercle (S84-S86, S109-S112) et colonnes pictogramme + bloc texte (P9) : repetition d'un module a pas constant ; regulier.
6. Frise a 4 phases (S118) et retroplanning en chevrons (S133) : chevrons = preset `homePlate`/`chevron` ; simples.
7. Bandeaux gelule de synthese (S105, S106) et panneau navy d'enonce (S106 droite) : formes + texte ; faciles.

Fragiles (a eviter ou a simplifier) :
- Calendriers multi-tables (S123-S132) : 12 tables ou 2 x 26 colonnes ; lignes de 128400 EMU (< hauteur minimale d'une ligne a 8 pt ; PowerPoint reetire les hauteurs), rendu different entre LibreOffice et PowerPoint ; texte 6 pt illisible. A construire par formes (rectangles) ou a eviter.
- Chemin en serpentin et arcs (S92, S93) : ARC + LINE alignes a la main, jalons positionnes a l'oeil ; les ARC se parametrent en angles `adj` peu intuitifs ; fragile.
- Texte pivote a 45 deg avec jalons (S119) : etiquettes serrees, collisions facilement.
- Grilles 4/6/8 cellules en rect arrondi + « croix pincee » (S151-S153) : formes ARC/freeform ; fragile et peu portable.
- Radar S107 (formes libres), illustration decorative S129 (image) : specifiques.
- Gantt S116/S120/S121 (marqueurs 6-7 pt, losanges, chevauchements) : trop dense pour du texte lisible.
- Groupes (GROUP 6) utilises dans S79, S87-S89, S98-S101, S109, S111 : python-pptx ne peut pas facilement re-parametrer les groupes ; reconstruire en formes libres.

## 4. FAITS DU BRIEF INFIRMES / NON VERIFIE

- Faits du brief infirmes : aucun fait chiffre n'etait donne dans le brief (le sous-titre "chapitres 04-08" est confirme : 04 Contexte et demande S76, 05 Demarche S83, 06 Details etapes S95, 07 Planning S113, 08 Tableaux S134). Le brief dit "324 slides" : non verifie dans ce lot (plage 76-154 seulement vue, 79 slides, 76 a 154 inclus). Le brief dit "9144000x5143500 EMU" : conforme aux dimensions de slide du fichier (donnees lues dans le dump, confirme par les positions maximales 9144000).
- Observation contraire a une idee recue : le theme "evident" (theme1.xml, dk1=000000, accent3=ED561B orange) N'est PAS celui utilise ; lire theme2.xml. Un generateur qui lirait theme1 verrait du noir et de l'orange.
- Non verifie : tailles exactes des chiffres XXL de S122 et S109 (taille de police non extraite) ; valeurs lumMod/alpha des teintes cyan clair des phases (S115, S129, S133) ; couleur precise du texte cyan en S122 (visuellement cyan) ; compatibilite .ppt (aucune conversion testee) ; hauteurs de ligne reelles dans PowerPoint pour les tableaux a 128400 EMU (seul le rendu des PNG fourni a ete regarde, produit par un moteur non precise) ; formes exactes des photos des intercalaires (round2Diag ou teardrop) ; espacements precis inter-cartes (ecarts approximes depuis les x des dumps, ex. pas 2,0-2,8 M).
- Nombre de formes utilisees : lu dans dump.txt (79 lignes pour 79 slides).
