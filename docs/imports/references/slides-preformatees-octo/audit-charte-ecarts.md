# Audit charte visuelle : code du deck vs deck de reference OCTO (2026-11-05)

Reference = ref.pptx (324 slides, 50 layouts). Mesures : scratchpad/audit/cmp.py (template vs ref) et stats.py (pptx genere). Lecture seule.
Limite majeure : le seul .pptx genere present (docs/cadrage-ppt/bmad-iap-cadrage-synthese.pptx, 35 slides, 2026-10-29) est ANTERIEUR au code actuel (generate_deck.py et test modifies, non commites). Les stats "rendu" ci-dessous sont indicatives ; les constats "code" sont, eux, sur le code courant.

## 1. Template vs reference : CONFORME

- Taille 9144000 x 5143500 des deux cotes. CONFORME.
- Theme du master : ref master->theme2.xml (dk1 0E2356, lt1 FFFFFF, dk2 3E4F78, lt2 586586, accent1..6 = 6E7B9A 9FA7BB 00D2DD B7BDCC CFD3DD E7E9EE). Template master->theme1.xml, memes 10 valeurs. Polices de theme Arial/Arial des deux cotes. CONFORME (la theme2 du template est un autre jeu, mais non reliee au master).
- Layouts : ref 50, template 34 (sous-ensemble). Geometries identiques sur 50 (titre 4295825,1918050,4164300x1810200 ; numero 3457650,1226600,499500x433200), 02 (titre 562500,361400,7929000x370800), 03 (562825,361400,8019000x370800 + sous-titre 571500,779175), 04 (562500,361400,8019000x370800), 05, 40 (1657350,1619250,3648000x1305000 ...). CONFORME. Le template n'a pas les layouts 00-01/variantes `_1_2`, non utilises (deck_theme.py:14-18 : idx 8, 5, 0, 2, 15).
- Decor (logo O, copyright vertical, pastille de page) vient du layout : code ne le recree pas. CONFORME.

## 2. ECARTS (tri par impact visuel decroissant)

### E1. Italiques omnipresents. Ref : sl. 7 (checklist) + SYNTHESE regle 5 : guillemets, pas d'italique. ECART
- Code : 44 occurrences `italic=True` dans generate_deck.py (ex. :701 sous-titre de sous-chapitre, :869, :987 chapo, :1620 chute, :2026 chapo, :1769, :1939) ; deck_shapes.py:279,311,343 ; slide_chapitre ecrit la ligne de couverture en italique (generate_deck.py:765-766). pptx_deck_vscode3.py:104 gere `italic` par defaut False.
- Mesure (deck genere, ancien) : 67 runs italiques sur 35 slides. Ref : 0 consigne italique.

### E2. Corps de texte tres petit : 8-8,5 pt dominant, 6,5-7,5 pt present. Ref : sl. 1-75 tailles 11 pt x289, 10 x279, 12 x135 ; 8 pt x104 ; mini rencontre 6 pt hors projection. ECART
- Code : 29 lignes a size<8 (generate_deck.py:1617 6.5, :2086 7, :2290 7, :2892 7, :2902 chip 6.5, :2907, :2914, :2916, :2934, :2949, :2951, :3472 7.5...) ; 139 lignes a 8-8,5. Echelle D.TYPE : "tiny" 9, "small" 10.5, "body" 12 (pptx_deck_vscode3.py:44-46) : la consigne de ref (10-11 pt courant) n'est atteinte que par "small".
- Mesure (deck genere ancien) : 8 pt = 257 runs, 8,5 = 112, 9 = 112 sur ~740 runs dimensionnes, soit ~65 % des runs en 8-9 pt (ref ~10 % a 8 pt). 0 run <8 dans l'ancien rendu : la mini-police 6,5-7,5 est nouvelle (code courant), non rendue.
- Pas de plancher de taille dans le code (aucune garde `min size`) : NON applique par test, constat par grep.

### E3. Epaisseur de trait 1,0 pt (12700) au lieu de 0,75 pt (9525), signature des cadres. Ref : 9525 x522, 19050 x22, 38100 x6 (sl. 1-75). ECART
- Code : defaut `line_w=1.0` dans pptx_deck_vscode3.py:109 (add_rect), deck_shapes.py (cards) ; deck_theme.py:81 idem ; `_onglet`/`_diag` generate_deck.py:~584,~603 `line_w=1.0` ; badge cercle `line_w=1.2` (pptx_deck_vscode3.py:237-238). Seul add_card pose 0.75 (pptx_deck_vscode3.py:179).
- Mesure (ancien rendu) : 9525 = 54 traits ; 12700 = 41, 15875 = 29, 19050 = 20, 13970/17780/11430 = 12 : 9525 ne pese que ~34 % des traits.

### E4. Titre de slide : taille adaptative 12-17 pt, kicker en MAJUSCULES, au lieu de 18 pt gras. Ref : layout 04 (sl. 8-24...) titre 18 pt gras, placeholder (562500,361400,8019000x370800) ; regle sl. 7 : majuscule en debut de phrase seulement. ECART
- Code : generate_deck.py:~655-676 `D.ajuster_police(..., 17, 12, ...)` : la taille max est 17 (jamais 18) et descend jusqu'a 12 selon la longueur ; texte compose `kicker.upper() + " · " + title`. Position du placeholder respectee (CONFORME).
- Mesure (ancien rendu) : tailles 17 x13, 16 x12, 18 x2 ; le titre n'a donc pas la taille unique de la ref.

### E5. Interlignes sous 1,15 et mixtes. Ref : sl. 7 interligne >= 1,15 ; sl. 27 : 115 %. ECART partiel
- Code : `line_spacing=1.0`, 1.1 : generate_deck.py:1891, 2304, 2934, deck_shapes.py:279 (1.0) ; 1.1 dans de nombreux dict.
- Mesure (ancien rendu) : spcPct 100000 x17, 105000 x26, 110000 x29 = 72 paragraphes < 115 % contre 75 a 115 % et ~140 au-dessus. Aucune garde dans le code.

### E6. Rayon de coin absolu unique (0,20 in) au lieu des adjustments de la ref. Ref : roundRect adj 50000 (pilule) / 16667 / 0 ; round2Diag (0/50000, 38136/0, 50000/0, 16667/0) ; round2Same 50000/0, 16667/0 ; round1 50000/16667 (sl. 3, 8, 27, 33-37). ECART
- Code : RAYON_COIN_IN = 0.20 (deck_theme.py:77, impose a tous les `add_rect(rounded=True)` par monkeypatch :81-89), `_coin()` generate_deck.py:581-582 ; round2Diag/round2Same : un seul grand coin parametre a la fois (adjustments[0]/[1] = a ou 0, :589-590, :608-609), jamais 38136 ni 16667 ni couples (50000,0) de la ref.
- Mesure (ancien rendu) : roundRect 233, round2Diag 11, teardrop 8, round2Same 0, round1Rect 0 sur 35 slides. Ref : round2Same et round1 sont des formes-signature (sl. 8, 50-51, 63, 67) ; le code en a la fonction (`_onglet`, :584) mais le rendu ancien ne l'emploie pas (a verifier sur rendu frais : NON VERIFIE).
- Une carte de 0,5 in de haut aura un rayon de 0,2 in (adj 0,4 ; presque pilule) quand la ref garde 16667 relatif ; incoherence de proportion entre petites et grandes cartes.

### E7. Couleurs hors palette 10 teintes de la ref. Ref : sl. 5 (rampes) + SYNTHESE (hors charte : 00A9C5, 3F3F3F...). ECART mineur
- Code : #c7cbe0 (15 occurrences : generate_deck.py:941, 2757, 2851, 2916, 3264, 3472, 3656, 4115, 4121, 4179, 4240, 4472...), #e8ebf5 (:3041), #8891b3 (:1133), #dce6f5 (:1109), #F2F4F8 (:1111, deck_shapes.py:307), #4A5A80 et #26386A (SEVERITE deck_theme.py:92 ; proches de 263967 et 3E4F78 mais pas identiques). Defauts historiques de pptx_deck_vscode3.py:51-56 (PALETTE bleu/vert/rouge/or/violet, INK 1c2330, LINE e6e8ee) : residuels, ecrasees par deck_theme mais PALETTE reste importable (160 sites redirigees vers ENCRE par arbitrage 2026-09-10 : CONFORME en pratique).
- Mesure (ancien rendu) : C7CBE0 x19, DCE6F5 x11, E6E8EE x4, F2F4F8 x4, 8891B3 x3, 4A5A80/26386A x1 ; 100 % des autres couleurs sont dans la palette (0E2356 597, FFFFFF 233, 586586 216, CFD3DD 58, E7E9EE 26, 00D2DD 19).

### E8. Intercalaire de chapitre : numero en 17 pt et ligne de couverture italique grise ; titre colore par `color`. Ref : sl. 25/52/62 (layout 50) : titre ~28 pt, numero dans pastille placeholder, 3 elements. ECART partiel
- Code : generate_deck.py:745-790 : layout 50 bien utilise (3 remplissages : titre idx0, numero idx1, photo teardrop clonee via `_find_frame_by_geom`/`_remplir_cadre`) = CONFORME sur la construction ; ECART sur le numero `Pt(17)` (:783) vs "titre 28 pt" de la ref (nota : le placeholder ref numero fait 499500x433200 EMU ; 17 pt est un choix documente pour eviter le debordement), sur le paragraphe de couverture en italique `D.TYPE["small"]` (:766), et sur la couleur `color` appliquee au titre/numero (:771, :784) alors que la ref reste navy. Photo : fond "scene" procedural 6 scenes (memoire projet) : NON VERIFIE vs "photos bleu-vert 3D 75B7C7" de la ref.

### E9. Fleches/chevrons et glyphes de texte unicode. Ref : fleches = formes (sl. 10, 33 groupes), pas des caracteres. ECART mineur
- Code : "↓" et "▾" en texte 8 pt (generate_deck.py:1039, 1043, 1075) comme connecteurs ; glyphes ①②③⟲ exclus d'Outfit et laisses en Arial (generate_deck.py:3504 ; mesure : 12 runs Arial). La ref n'a que 3 Arial dans 75 slides.

### E10. Majuscules et point median. Ref : sl. 7 majuscule en debut de phrase seulement ; jamais de point median (ecriture inclusive). ECART / NON VERIFIE
- Code : kicker en `.upper()` (E4) ; sous-en-tetes "majuscules 8-9 pt" delibere (deck_theme.py:138-139) ; separateur " · " (kicker, puces "·  " generate_deck.py:2290). Le point median de la ref vise l'ecriture inclusive (content·e·s) : l'usage comme separateur typographique n'est pas certain d'etre vise. NON VERIFIE sur l'interdiction exacte.

## 3. CONFORME (code vs reference)

- Palette principale : NAVY = dk1 0E2356, ACCENT = accent3 00D2DD, MUTED 586586, LINE CFD3DD, TRACK E7E9EE, ACCENT1/2 lus du theme (deck_theme.py:49-57). Rampe navy du theme 3E4F78/586586/6E7B9A/9FA7BB/CFD3DD/E7E9EE : conforme.
- Cyan jamais en texte sur blanc : `encre_de` (deck_theme.py:150-162) et garde chip (deck_shapes.py:65-82). Grep `color=ACCENT` en texte : 0 resultat dans generate_deck.py et deck_shapes.py ; ancien rendu : 19 usages de 00D2DD, tous en aplat. Plus strict que la ref (sl. 3 admet cyan sur marine, sl. 122 cyan texte) : voulu. CONFORME.
- Police Outfit sur tout le deck (generate_deck.py:3502-3511, application a chaque run) ; ancien rendu : Outfit 712 runs, Arial 12. Pas de tableau natif ni de groupe dans le code (aucun `add_table`/group), donc pas de run oublie par la boucle de `appliquer_police` (pptx_deck_vscode3.py:285-305 ne couvre que `slide.shapes` de premier niveau). CONFORME. Reserve : la ref emploie aussi Outfit Light/Medium/SemiBold (125/45/49 occurrences) ; le code n'utilise que Outfit Regular + gras (433 runs bold) : hierarchie plus pauvre, pas une violation.
- Minimum de marge : MARGIN 0.615 in = 562500 EMU = x titre ref (deck_theme.py:27) ; zone de contenu 1,15-5,45 in (CONTENT_TOP/BOTTOM, :29-30) vs ref x 549k-8,5M, y 1,22M-4,86M EMU : bord droit code 9,15 in = 8,37 M EMU, bas 5,45 in = 4,98 M EMU (ref 4,86 M) : debord de 0,12 M EMU (0,13 in) sous la zone ref : ECART mineur (pastille de page en bas droit a surveiller), NON VERIFIE au rendu.
- Un sur N en accent / numerotation par goutte / quinconce / forme-signature : vocabulaire declare deck_theme.py:122-143, conforme aux regles 3-4 de la SYNTHESE ; le test d'application par slide n'est pas mesure ici. Pilules (radius 0.5 = adj 50000 : `add_chip`, pptx_deck_vscode3.py:211-216) CONFORME. Teardrop 100000 du cadre photo cloné du layout : CONFORME.
- La couleur ne porte pas le sens : 160 sites PALETTE rabattus sur ENCRE (deck_theme.py:124-127) : CONFORME. Pas d'ombre (`_sans_ombre`, generate_deck.py:570) : CONFORME (ref sans ombre).
- Pas de justifie dans le code genere (aucune occurrence PP_ALIGN.JUSTIFY relevee par le grep sur les 3 fichiers) ; alignement centre present (CENTER) dans chips/numeros uniquement : NON verifie cas par cas.

## 4. Faits du brief infirmes
Aucun fait chiffre fourni ; rien a infirmer. Precision : le brief annonce generate_deck.py de 4585 lignes ; l'indexation montre du contenu jusqu'a la ligne ~4922 (appel `_appliquer_police_deck(prs)` ligne 4922) : le fichier courant est plus long que 4585 lignes.

## 5. Non verifie
- Rendu actuel (aucune regeneration : ecrirait dans le repo) ; toutes les statistiques "rendu" viennent d'un .pptx daté 2026-10-29, 35 slides, et sont donc possiblement perimees.
- Longueur de ligne <= 80 caracteres (aucun comptage fait), contraste calcule des couples (c7cbe0 sur navy ; 586586 sur E7E9EE), guillemets contre italique en citations, photos N&B des portraits, annotations/bandeaux de template (aucune "A adapter a sa situation" cherchee dans le texte genere), marqueurs de numerotation/tracker (goutte + connecteur) compares a sl. 8 en geometrie, cadres photo round2Diag (clonage prstGeom hors teardrop), chapitre « Cou|leurs. » (non repris), layouts 02/03/05 non utilises par le code.
- Verification que le code applique "un sur N" slide par slide.
