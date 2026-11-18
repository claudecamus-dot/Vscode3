# Lot C - Slides 155-264 du deck de reference OCTO (chapitres 09 a 14)

Methode : renders PNG vus (tous les patterns, ~100 des 110 slides vues ; les autres sont des variantes directes d'un pattern vu : 162/165-167 variantes de 166, 217-223 variantes de 217/220/223, 258/260/263 doublons de 257/259/262 FR/EN ou remplis/vides). Geometrie et couleurs : python-pptx (scripts dans lotC/). Tous les nombres viennent d'une commande ou d'un render.

## 0. Constantes mesurees sur la plage 155-264

- Slide 9144000 x 5143500 EMU. Layouts : `50 - Chapitre [1]` (155,170,193,216,247,254), `03 - Titre et sous-titre_1` / `03 - Titre et sous-titre`, `04 - Titre seul`, `01 - Titre, sous-titre et contenu`, `02 - Titre et contenu`. Titre = placeholder (rect 562500,361400 8019000x370800), sous-titre = placeholder (571500,779171). Beaucoup de slides n'ont aucun titre rempli (modeles libres).
- Theme (lu dans theme1) : dk1 0E2356 (navy encre), lt1 FFFFFF, dk2 3E4F78, lt2 586586, accent1 6E7B9A, accent2 9FA7BB, accent3 00D2DD (cyan), accent4 B7BDCC, accent5 CFD3DD, accent6 E7E9EE.
- Frequence des couleurs sur la plage (compte de balises) : schemeClr dk1 6416, srgb 0E2356 994, FFFFFF 372, accent3 563, 00D2DD 84, 3E4F78 93. Teintes cyan par lumMod/lumOff ou srgb : DAF6F9, C6F1F5, B1F1F2, 9EE9ED, 8AE4EB, 72DFE7, 4ADBE2 (rampe de 6-7 pas du blanc au cyan 00D2DD, utilisee en radars, matrices, camemberts).
- Hors charte vus : 00A9C5 (24), 00A2D8 (14), 3F3F3F/38383F (44), C8E7E4/8BDEE0 (teal, slides 229-230), 566589/627091 (gris-bleus). Non vérifié : lesquels sont des artefacts d'import Google Slides (les shapes sont nommees "Google Shape;NNNN;pNNN").
- Polices (compte de balises typeface) : Outfit 14251, Outfit SemiBold 2108, Outfit Light 1402, Outfit Medium 952 ; residus Century Gothic 1303, Helvetica Neue Light 1224, Arial 339 (probablement dans groupes/icones importes). Tailles les plus frequentes (sz en 1/100 pt) : 900, 1000, 1100, 1200, 800, 700 ; titres de carte 1300-1900 ; gros chiffres 2200-2800.
- Traits : 9525 EMU (0,75 pt) navy dk1, `prstDash solid` (2170 occurrences), `dot` 383, `dash` 25, `lgDash` 16. Connecteurs et fleches d'axe plus epais (visuellement 4-5 pt, non mesure).
- Geometries (compte) : rect 1284, roundRect 615, straightConnector1 323, ellipse 310, round2SameRect 174, round2DiagRect 146, arc 103, teardrop 52, round1Rect 46, flowChartConnector 30, blockArc 20, triangle 5, donut 2, homePlate 2.
- Types : 813 autoshapes, 378 textbox, 321 groupes, 229 placeholders, 192 images, 181 lignes, 76 freeforms, 4 tables (slides 190,191,192,249 seulement). AUCUN graphicFrame de type chart : tous les graphiques (barres 231-233, courbe 234, donuts 217-225, radar 228) sont des formes dessinees a la main.
- Pastille de statut en haut a droite (rect 7534150,0 1614000x257700, navy, texte blanc gras) : "A adapter a sa situation" (slides 171-252 environ) ou "A remplir en ligne ou a imprimer" (kit canvas 256-264). Marqueur de contenu a retoucher, pas de la decoration finale.
- Bas de page : pied vertical "OCTO | PART OF ACCENTURE (c) 2026 - All rights reserved" (gauche), numero `.NNN` dans pilule (bas droite) ; ce sont des elements du layout. Canvas : mention "OCTO Technology sous licence Creative Commons" + icones CC en bas droite (slides 255-264).

## 1. Catalogue des patterns

Convention : "carte-cle" = forme OCTO signature : round2DiagRect adj1=50000 adj2=0 (deux coins diagonaux tres arrondis, deux coins droits), remplissage blanc, trait navy 9525.

### A. Chapitre 09 - Listes (155-169)
- 155 / 170 / 193 / 216 / 247 / 254 intercalaires : layout Chapitre ; pastille cyan ronde en haut gauche ; goutte (teardrop 2560500x2560500 EMU en (1396875,1668700)) contenant une illustration 3D (image) ; pilule logo+numero (ex. "09", "10") au coin de la goutte ; titre navy gras a droite. Photo : cadre = prstGeom teardrop sur la picture (cf. skill pptx-framed-image).
- 156 Serpentin 5 etapes : S sinueux en arcs (outline navy double trait), 5 pastilles numerotees cyan (icone image "1".."5"), titres + texte centres alternant dessus/dessous avec filet pointille vertical. 18 shapes. Usage : parcours/processus 5 temps. Fragile (arcs a calibrer).
- 157 Frise 5 blocs capsules alternes sur une ligne horizontale : capsule haute/basse (roundRect rayon max) texte centre, icone cyan/navy (image) en face. 
- 158 Grille 2x2 "carte a onglet" : groupe = round2DiagRect 3881830x1618399 EMU (549420,1202750), onglet num round2DiagRect 954600x1617600 (adj1 50000, flipH) + round1Rect 2926500x1164600 pour corps ; "1." sz 2400 gras, filet navy 267600 EMU, "Titre" sz 1100, puces sz 900 (interligne 150 %). Usage : 4 volets listes. Variante 159 : 2x2 en miroir (onglets aux extremites), 160 : 4 petales (round2DiagRect) autour d'un cercle central avec icone, 161 : 4 colonnes "gelule fleche" (titre dans round2DiagRect + fleche ligne + pastille numero), 162 : meme en 4 lignes (titre a gauche, texte large a droite).
- 163/164 : lignes "numero + titre gras en round2DiagRect + 2 colonnes texte a puces ronds creux, separees d'un pointille gris", filet navy bas ; 2 lignes (163) ou 3 (164).
- 165/166/167 : empilement 2/3/4 cartes "onglet-titre + corps" : onglet round1Rect 4326600x336900 (titre sz 1200 gras + pastille cyan ronde 336734 EMU), corps round2SameRect 7719600x852900 (166, 3 cartes). Trait navy, fond blanc. Usage : liste de 2 a 4 messages a titre court.
- 168/169 : 5 colonnes "pilule" verticales (roundRect rayon max, hauteur ~495 px/720) ; 168 = icone en bas, 169 = chiffre cyan "1..5" en haut (cercle + icone). Texte sz ~1100 sans puces.

### B. Chapitre 10 - Reponses AO (171-192)
- 171 SWOT : 4 cartes onglet (comme 158) avec onglet teinte en rampe cyan (DAF6F9, B1F1F2, 72DFE7, 00D2DD) : la couleur code l'ordre (S->T), pas un sens. Lettre sz 2400.
- 172 3 etapes SHU/HA/RI : teardrop navy + numero, entete round2DiagRect 1469400x591300 (blanc / cyan 00D2DD / navy 0E2356 avec texte blanc), corps round2DiagRect 1937700x1509900 blanc, pied round1Rect 1937700x343500 + sablier + duree, fleche entre colonnes (groupe de lignes). Texte navy sur cyan OK (HA, gras 1800).
- 173 Cercle central cyan "CULTURE" + 4 quadrants roundRect (coins exterieurs arrondis seulement) avec icones : un cote texte aligne a droite, l'autre a gauche. 
- 174 Serpentin 2 niveaux "Projet / Produit" : cartes roundRect a onglet cyan (texte navy gras) + pastille numero navy (01/02), 2 colonnes de puces, titre-claim a droite, pied avec lunette + citation.
- 175 Comparatif projet/produit : 2 entetes navy round2SameRect 2268600x393000 (texte blanc gras), 2 grands panneaux (cyan clair B1F1F2 / cyan plein 00D2DD) contenant 6 roundRect blancs (gras partiel) ; chevron navy entre les deux.
- 176 Grille 3x4 de cartes : 9 blanches + 3 accents (cyan clair, cyan plein, navy avec texte blanc en bas a droite) = exemple de "1 sur N en accent".
- 177 3 colonnes "01 / 02 / 03" : pastille numero ronde + entete cyan, 3 etages (objectifs en gras, activites a puces, livrables) avec icones a gauche (image). Dense (sz ~900-1000).
- 178 Pipeline 6 colonnes sur bandeau cyan plein (00D2DD) avec separateurs tirets navy, icones en tete, boucle de retour (connecteur coude) en bas. Texte navy sur grand aplat cyan : lisible mais cyan large.
- 179 Cadrage 360 : 8 cartes a entete cyan + pastille de tag blanche (PRODUIT/TECH/ORGA) de part et d'autre d'une fleche navy epaisse ; sz 700-900.
- 180 Frise "MVP -> produit" : multi-icones (21 images), fleches cyan epaisses, boucle ronde cyan, bande de phases (roundRect) sur une fleche navy en bas, sprints en petites pilules. 56 shapes.
- 181 Scrum : flux fleches navy/cyan, cartes rondes, "3 roles/3 artefacts/4 evenements" en cartouche (3 colonnes, pastilles cyan roundRect).
- 182/183 Organisation (PROCESS / PRODUCT / PEOPLE) : colonnes cyan clair et plein, bandeaux navy etiquettes, personnages (images) ; 182 = + Venn Metier/IT.
- 184 Frise de livraison (timeline) : ligne navy epaisse + colis (images) + 3 colonnes de puces a icone ; texte sz ~800 en anglais (fragile en lisibilite).
- 185 Escalier de 4 chevrons cyan en degrade (DAF6F9 -> 00D2DD) sur axes navy : texte tourne ; complexe (freeforms).
- 186 Layer cake : colonne navy + colonne cyan, cartes blanches arrondies, connecteurs vers pastilles et puces a droite.
- 187 Slide d'engagement RSE : logos en images, goutte image 3D, cartouche avec icones rondes. 188 demarche accessible : barres navy/cyan, tuiles. 189 bulles (flowChartConnector, donut) : "IA" panorama. 190 TABLEAU natif (graphicFrame, 4 colonnes performers) : entete navy, lignes pointillees, bande basse cyan. 191 TABLEAU natif "comitologie" : entete navy, bande cyan en pied (roundRect). 192 TABLEAU natif matrice de charge (% par role) : entete cyan (equipe OCTO) / navy (client), colonne de lots tournee a 270 deg, cellules pointillees.

### C. Chapitre 11 - Schemas pre-remplis (194-215)
- 194 infini DEV/OPS (freeforms blockArc/arcs) cyan plein / cyan clair / blanc. 195 Venn Metier/IT (cercles chevauches avec transparence). 196/197 chaine d'anneaux : cercles blancs + arcs "blockArc" cyan avec pointe de fleche triangle, 5 (196) ou 4 (197) etapes + icone au centre + titre/texte dessous. 198 3 cercles pointilles (organisation/equipe/individu) avec etiquettes roundRect fines sz ~700, bordure epaisse grise pour "deleguables". 199 rectangles imbriques (4 niveaux navy/cyan/cyan clair/navy) pour definitions emboitees. 200 echelle + 4 lignes gauche blanc / droite cyan (dernier accent navy). 201 roadmap multi-stream (aplats cyan en escalier, axes navy epais, features en pilules navy). 202 3 phases (spirales navy 2 tons slate + pilules 6E7B9A/3E4F78/0E2356 : ici le gris-bleu porte la gradation, pas le cyan). 203 cycle de vie : courbe cyan pleine (freeform) + colonnes pointillees + tuiles roundRect. 204/205 parcours sinueux (freeform 41BDD3-like, non mesure) avec personnages et horaires. 206 route + icones en cercles. 207 Maison du Lean (freeform/round) + vue en 3 segments. 208 barometre : 6 smileys cyan + rampe cyan de 6 pas + fleche indicatrice. 209 triangle en 3 segments (blanc/navy/cyan) + cercle central. 210 losange "espace solution" cyan/blanc avec texte tourne + 4 jalons. 211 8 cercles autour de "Fails". 212 nuage de mots sur panneau navy : texte blanc, cyan 00D2DD ET cyan clair 9EE9ED SUR navy (la regle "jamais de cyan sur du texte" vaut pour fond blanc ; ici contraste eleve, mais a ne pas reprendre sans verification). 213 courbe de Gartner (freeform) + 5 cases. 214 matrice 3x3 en rampe cyan avec coins arrondis (roundRect/round2Diag), axes navy fleches. 215 Wardley map (cases cyan clair/plein, traits pointilles, noeuds cercles blancs).

### D. Chapitre 12 - Graphiques, radars, diagrammes (217-246)
- 217-223 anneaux segmentes 3 a 8 parts (donut + parts "pie" a bord navy) : rampe cyan, une part en cyan plein = focus ; 220/223 : anneau en chevrons (arrow ring) avec 4 ou 7 textes autour, titres sz ~1200 + texte ~900.
- 224 jauges "pointilles" 10 a 100 % : 8 couronnes de ~32 petits traits (roundRect, cyan actifs, gris CFD3DD-like inactifs) ; chiffre sz ~2800. 225 jauges arc (blockArc/arc epais cyan, bouts ronds, anneau fin navy en fond) 8 niveaux ; 226 grande jauge 75 % + texte + epingle (pin) verticale.
- 227 non vu individuellement (5 shapes, sans texte) : non vérifié. 228 radar 3 axes : cercles concentriques gris-bleu clair (B7BDCC), axe cyan, polygone navy, noeuds cyan 00D2DD cercle navy, graduations 1-4 dans pastilles ; texte a droite avec filets pointilles.
- 229 matrice priorisation 2x2 : 4 roundRect (blanc, teal clair, cyan clair, cyan) ; points navy/gris selon theme ; liste a puces gauche avec gras "W :" ; points a puces de 3 niveaux de gris-bleu. 230 cadran de decision APM : 4 quadrants, axes navy epais, grilles pointillees, graduations 0-5. 
- 231/232 histogrammes (rect navy / cyan, libelles blancs sur navy et navy sur cyan, icone sous chaque barre, lignes de grille pointillees). 233 histogramme 11 tribus (57 shapes, ligne navy fine vers etiquettes decalees). 234 courbe : points cyan cercles bordes navy, ligne fine navy, valeurs seulement sur certains points (anti-bruit), axe navy fleche.
- 235 anneaux chaines 4 etapes (cf. 196). 236 fleur 8 petales (teardrop alternes + cercle central cyan). 237 8 fleches cyan (rayonnantes) autour d'un cercle. 238 (3 shapes, non vu) non vérifié. 239 4 arcs cyan epais autour d'un cercle avec chapeaux pointilles. 240 4 quartiers + pastille cyan par quartier. 241 entonnoir 5 niveaux (ellipses cyan + troncs blancs) + etiquettes roundRect. 242 cone d'ellipses cyan croissantes. 243 pyramide 3 etages cyan avec pastilles de legende (blanc/navy/gris 9FA7BB). 244 3 cercles concentriques (blanc/cyan/navy, texte blanc sur navy) "Pourquoi/Comment/Quoi". 245 Venn 3 cercles (cyan, navy, blanc, transparences) + legende. 246 Fishbone : ligne navy, noeuds cyan, tete et queue en freeform.

### E. Chapitre 13 - Audit et reco (248-253)
- 248 Fiche recommandation : titre + pastille cyan "2-A" (texte navy gras) + 2 mini-jauges Gain/Effort ; bloc "Description" entete navy round2SameRect (texte blanc gras sz ~1400) et 3 cartes (Benefices/Points d'attention/Profils) avec onglet-icone en coin. 249 Matrice gain/effort : TABLEAU natif a gauche (bande verticale Court/Moyen/Long terme en teinte cyan croissante 3 pas) + matrice 2x2 a droite avec etiquettes "1-A" en roundRect (teinte = horizon). Defaut visible : libelle d'axe "Effort" coupe en "Effor/t" (render 249) -> boite trop etroite.
- 250 Referentiel d'architecture 5 volets x 4 domaines : tableau fait de roundRect (entetes navy et cyan 00D2DD, cellules blanches), sz ~900. 251 Demarche audit/cadrage : ligne navy pleine largeur, 3 epingles cyan (goutte + icone), cartes a entete navy (round2DiagRect) + tag "GOALS" cyan, puces avec gras. 252 6 cartes dont 1 navy (texte blanc, icone) et 1 cyan : "1 sur N en accent" ; roundRect trait navy ~2 pt. 253 6 lignes icone dans cercle + titre gras + texte.

### F. Chapitre 14 - Kit Canvas (255-264)
- 255/256 Lean canvas (rempli/vide) : grille 5 colonnes + pied 2 colonnes, coins exterieurs haut-gauche et bas arrondis (rayon ~36 px), colonnes extremes cyan tres clair (C6F1F5), separateurs pleins navy et pointilles lavande ; titres navy gras sz ~1400, aide en gris-bleu 3E4F78-like. Tag "A remplir en ligne ou a imprimer" (256).
- 257/258 Persona : colonne gauche cyan clair (photo ronde, bord navy, noir et blanc) + chips blanches "Trait de caractere" sur cyan plein ; 3 bandeaux navy (texte blanc gras) ; curseurs bipolaires (ligne + point cyan). 259/260 These d'investissement : bandeaux navy, mini-jauges (25/85/50 %), champs "Note" en pilule, 4 colonnes cyan clair. 261 Experience map : grille 6 colonnes x 5 lignes de roundRect, etiquettes de ligne tournees 270 deg sur rect navy, ligne "Emotion" cyan clair + 3 smileys. 262/263 North Star (FR/EN) : colonnes de cartes + fleches navy epaisses + coude, etoile cyan. 264 Carte d'empathie : deux triangles cyan 00D2DD (texte navy gras 3E4F78-like) + icone centrale + 2 champs cyan clair.

## 2. Regles et contraintes (stated/implied)

1. Palette : navy 0E2356 pour texte, traits, fleches, aplats forts ; cyan 00D2DD en aplat ; rampe de teintes cyan (DAF6F9...72DFE7) pour hierarchiser une serie ordonnee ; un seul aplat navy par ensemble de cartes (176, 252, 200). Texte navy sur cyan : omnipresent (172 "HA", 175, 178, 195, 264) ; texte blanc sur navy : toujours. Texte cyan sur fond blanc : NON observe (cyan sert aux pastilles, jauges, icones, tag "GOALS" avec texte navy). Seule exception de cyan-comme-texte : 212, sur panneau navy. Conforme a la charte VSCode3.
2. Differenciation sans couleur-sens : accent "un sur N" (176, 252, 200, 172), numerotation (156, 158, 163), position (201), forme (round2Diag vs roundRect). La rampe cyan code l'ORDRE (SWOT 171, matrices 214/229, gain/effort 249), pas un jugement bon/mauvais.
3. Contour : trait navy 9525 EMU sur presque toutes les formes blanches ; pas d'ombre. Fond de slide blanc. Pointille (dot) pour separations secondaires et grilles ; tirets (dash) pour jalons.
4. Typographie : Outfit uniquement (Regular/Light/Medium/SemiBold). Titres de carte 1100-1300 SemiBold, corps 900-1100, gros chiffres 2200-2800, mentions 700-800 (denses : 179, 184, 198). Interligne 150 % dans les cartes de 158.
5. Coins : coins arrondis en paires diagonales (round2DiagRect adj1=50000) pour les titres/onglets ; round2SameRect/round1Rect pour onglets d'angle ; roundRect pour tuiles ; coins droits conserves la ou une forme "s'appuie" sur une autre (onglets 166).
6. Compatibilite .ppt : le deck utilise teardrop, round2DiagRect, round2SameRect, blockArc, freeforms, groupes imbriques, images PNG en cadre de forme : non vérifié pour un export .ppt (aucune instruction du deck sur ce point ; aucun test fait). Les objets natifs presents sont des tables (4 slides) ; aucun chart natif.
7. Photos/cadres : photo d'intercalaire dans une goutte (teardrop 2560500 EMU) ; photo persona en cercle ; le cadre = geometrie clonee sur la picture. Les icones sont des images (192 pictures), pas du vectoriel editable.
8. Pastilles "A adapter a sa situation"/"A remplir en ligne ou a imprimer" : marqueurs de statut du template, a retirer dans un livrable client.
9. Canvas : licence Creative Commons mentionnee en pied (255-264) : a conserver si on reprend un canvas.

## 3. Patterns a reprendre en generateur python-pptx (classes)

Robustes (formes standard, parametrables, peu de freeforms) :
1. Carte a onglet (158/171/163-167/172/248/251) : round2DiagRect/round2SameRect + trait 9525 navy + entete rempli ; adj1 par `shape.adjustments[0]=0.5` ; remplir texte dans la forme.
2. Rampe cyan en N pas pour series ordonnees (214, 229, 249, 171, 208) : teintes lues dans la liste ci-dessus.
3. "Un sur N en accent" (176, 252) : grille roundRect, 1 navy + 1 cyan.
4. Tableau natif (190, 191, 192, 249) avec entete navy, lignes pointillees, pied cyan : seule vraie table native du deck ; reproductible via XML (bordures dot).
5. Jauges (225, 226, 259) : blockArc ou arc a bouts ronds epais cyan + anneau navy fin ; histogrammes en rect (231-232) ; points + courbe (234) ; grille pointillee.
6. Matrices 2x2/3x3 (214, 229, 230, 249) : roundRect/round2Diag avec axes en fleches navy epaisses.
7. Colonnes pilule (168/169), liste icone-cercle (253), canvas a grille (255-264), titres a bandeau navy (248, 257-259).
8. Diagrammes radiaux : fleur 8 petales (236), 8 fleches (237), anneaux segmentes (217-223).

Fragiles (a eviter ou valider au rendu) :
- Serpentins, parcours et routes (156, 174, 204-206) : arcs/freeforms/connecteurs coudes calibres a la main + personnages en images.
- Infini 194, escalier 185, Maison du Lean 207, Fishbone 246, Gartner 213, entonnoir 241 : freeforms/ellipses calibres.
- Chaine d'anneaux 196/197/235 : blockArc + triangles de pointe, jonctions visuelles sensibles a l'ordre z.
- Tout ce qui est tourne a 270 deg ou texte oblique (185, 210, 261) : rendu LibreOffice vs PowerPoint non vérifié.
- Slides denses sz 700-800 (179, 184, 198) : lisibilite projetee limite.
- Defaut observe dans la reference : "Effort" coupe (249), "Indicateur/s de vitesse" coupe (190), "Maîtris/e du code" (209), "L'intelligenc/e Artificielle" (189) : boites trop etroites ; a tester par rendu.

## 4. Faits du brief infirmes / incertitudes

- Faits du brief infirmes : aucun fait donne.
- Chapitres : le brief annonce 09-14 pour 155-264 : confirme par les intercalaires 155 (09 Listes), 170 (10 Slides de reponses pour appels d'offres), 193 (11 Schemas pre-rempli), 216 (12 Graphiques - Radars - Diagrammes), 247 (13 Audit et Recommandations), 254 (14 Kit Canvas). Le chapitre 12 inclut aussi 217-246 (graphiques et diagrammes divers) ; 213-215 (Gartner, priorisation, Wardley) sont dans le chapitre 11.
- Non vérifié : slides 227 et 238 (sans texte) non regardees ; 205 vue ; couleurs exactes du chemin des parcours 204/205 ; compatibilite .ppt ; rendu PowerPoint reel (renders = ceux fournis) ; epaisseurs de traits epais (fleches/axes) ; appartenance des couleurs hors charte (00A9C5, 3F3F3F, teal) a la charte ou a un artefact d'import ; valeurs adj des autres formes (seul round2DiagRect adj1=50000 adj2=0 et round2SameRect adj1=16667 mesures).
- Le nombre de chapitre dans le deck est cite par numero (09-14) : contraire a la regle VSCode3 (citer par NOM) ; ne reprendre que les noms.
