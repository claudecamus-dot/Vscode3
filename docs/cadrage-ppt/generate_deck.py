"""Génère la synthèse PPT des RÉSULTATS du cadrage BMAD IAP
(docs/bmad-iap-cadrage.md) à partir des helpers pptx_deck, dessinée
PAR-DESSUS le vrai template de marque OCTO (template-octo.pptx) —
masters/layouts/thème conservés, pas un deck sur canevas vierge.

Le nombre de slides et la liste des chapitres ne sont PAS recopiés ici : ils
ont été faux deux fois (48 annoncées pour 53 réelles, « 9 chapitres » et une
liste décalée d'un rang après l'insertion du chapitre « Spécificités de
l'infra » le 2026-09-10). La source est `build()`, en bas de ce fichier ; le
fil rouge narratif reste celui des decks SCALE
(docs/Import/notes-extraction-scale.md : POURQUOI → QUI → QUOI → COMMENT →
RÉSULTAT).

CHARTE (arbitrage du 2026-09-10) : la couleur ne porte PAS le sens. Voir le
bloc « Vocabulaire de différenciation » près de `ENCRE`.

v2.6 : le sous-chapitre « Exemples » de la Proposition (séparateur + 3 slides
illustratives) est SUPPRIMÉ à la demande — git garde l'historique (v2.5) ; en
échange, 2 slides nouvelles (activités humaines de la démarche ; architecture
IAP en contexte client) et un badge de série « déploiement agentic chez le
client » sur les 4 slides de proposition agentic du chapitre IA (3 agents
candidats + export markdown), renvoyant au schéma du chapitre Outillage IAP.

v2.7 (2026-09-01) : 2 slides de plus (40 -> 42) sur ce que le cadrage
déclarait faisant foi pour le deck sans y être redescendu — « qui achète,
contre quoi » (les 4 achats alternatifs, chapitre Contexte, après les
déclencheurs) et « conditions de réussite et non-engagement » (ce que la
mission exige du client et ce que son absence déclenche, chapitre Démarche,
après le fil humain).

v2.8 (2026-09-02) : nouveau chapitre 01 « Exec summary », EN OUVERTURE du
deck (avant slide_vision, juste après le sommaire) — 3 slides de plus
(42 -> 45), tous les chapitres suivants glissent de +1. Reprend la slide 2 du
pitch source (l'offre : chapô + citation-thèse, verbatim) et son schéma du
parcours de mission — redessiné EN NATIF (pas une insertion d'image), sur 3
registres (mouvements du socle toujours présents, variantes conditionnées au
contexte, mécanismes additifs) — puis une synthèse en une page de l'offre qui
résume aussi le reste du deck (COMPRENDRE/DÉFINIR/FAIRE ADOPTER & PROUVER,
avec renvoi aux chapitres). Le nœud « Discovery gaspillages » du schéma garde
« 6 catégories » du document source pitch (verbatim jusqu'ici) — divergence
avec les 8 familles de gaspillage du chapitre Besoins & douleurs, arbitrée le
2026-09-18 (salle atelier-idees, storytelling) : cohérence interne du deck
préférée à la fidélité verbatim sur ce point précis. Nœud renommé « 8
familles » ; le reste de la slide (schéma, citation-thèse) reste verbatim.

v2.9 (2026-09-02) : le chapitre 01 « Exec summary » est REFONDU pour parler au
prospect plutôt que de résumer le deck deux fois (45 -> 46 slides ; 9 chapitres
inchangés). Arbitrages : `slide_offre_synthese` est SUPPRIMÉE — le sommaire du
deck reste `slide_executive_summary`, qui la précédait et ne bouge pas ;
`slide_offre_iap` (le grand schéma du parcours de mission) DÉMÉNAGE au chapitre
07 · Démarche, en tête du bloc des schémas, avec le kicker et l'or du chapitre
d'accueil. À leur place, deux slides neuves :
  - `slide_pitch_iap` — trois cartes ÉGALES à ne pas confondre (les douleurs de
    ces organisations ; notre démarche outillée par un module agentic, côté
    CONSULTANT ; déployer de l'agentic chez le CLIENT, en option sous gate IA),
    deux teintes et deux silhouettes distinctes pour les deux faces de l'agentic
    — un sponsor qui lit deux fois « agentic » sans étiquette croit qu'on lui
    vend la même chose deux fois, ce qui rendrait la slide fausse. Sous la
    rangée, une bande grise pleine largeur (poids visuel moindre, pas une 4e
    carte) sur le MATÉRIAU de cadrage : trois contextes sectoriels réels, sans
    jamais affirmer une mission — aucun REX n'existe dans les sources
    (docs/bmad-iap-cadrage.md:115 décrit une note de rédaction, `rex-library.md`
    est planifié et non peuplé).
  - `slide_demarche_avec_sans_agentic` — le niveau ZOOMÉ-ARRIÈRE de
    l'« avec ou sans agentic » : une ligne horizontale de trois temps
    (COMPRENDRE / DÉFINIR / FAIRE ADOPTER & PROUVER) et, sous chaque temps, des
    pastilles empilées (socle gris-navy, module teal, agentic client violet).
    Ne redessine ni `slide_activites_humaines` (phase par phase, ch. 07), ni
    `slide_iap_contexte_client` (topologie, ch. 08), ni `slide_export_markdown`
    (bifurcation, ch. 06) — renvois littéraux « décliné chapitre 07 » et
    « déployé chapitre 08 » portés sur la slide.

v2.10 (2026-09-03) : le chapitre 01 · Exec summary (slide_pitch_iap +
slide_demarche_avec_sans_agentic) était déjà groupé par son propre intercalaire
(`slide_chapitre(prs, "01", ...)`), mais restait invisible du sommaire
(`slide_executive_summary`) — sa rangée POURQUOI/QUOI/COMMENT/RÉSULTAT ne
renvoyait qu'aux chapitres 02 à 09. Un bloc OFFRE, accroché en tête de rangée
(même style « accent » — fond plein — que RÉSULTAT, pour border la rangée :
l'offre ouvre, la preuve ferme), renvoie maintenant au chapitre 01 et reprend
au mot près les deux sous-titres des slides qu'il annonce.

v2.11 (2026-09-03) : deux défauts graphiques signalés par relecture réelle
(vraie taille de deck, PAS le self-check géométrique) — départagés en
comparant le rendu LibreOffice ET un rendu PowerPoint réel (COM) sur les
mêmes slides, pour ne corriger que ce qui existe dans l'artefact que
l'utilisateur ouvre :
  - Slide 1 (couverture) : le trait qui semble mal rejoindre le coin arrondi
    du bandeau version est un ARTEFACT DE RENDU LIBREOFFICE (groupe pivoté à
    180° du template `template-octo.pptx`, composé différemment par les deux
    moteurs) — absent du rendu PowerPoint réel. Rien à corriger côté
    générateur ; toucher le template partagé (masters/layouts hors périmètre
    de ce script) aurait été le mauvais geste pour un défaut qui n'existe pas
    dans le livrable réel.
  - Slide 4 (`slide_pitch_iap`) : DÉFAUT RÉEL, confirmé dans les deux rendus.
    La carte « CE QU'ILS VIVENT » a 4 puces (4 personas) quand les 2 autres
    cartes n'en ont que 3, mais le budget vertical `dispo` était partagé sans
    tenir compte du nombre d'items — la 4e puce débordait sous le chip de
    pied, dont le fond plein la masquait entièrement (seul son disque de
    puce dépassait, visible comme une virgule rouge au-dessus du bouton).
    Corrigé par une taille/interligne de puce ADAPTATIVE (calculée par carte
    selon ce qui tient réellement dans `dispo`, avec marge de sécurité),
    plutôt que par un chiffre choisi à la main — corrige la classe de bug,
    pas seulement cette instance. Le mécanisme d'anomalies de build
    (`_ANOMALIES_BUILD`, jusque-là réservé aux photos manquantes) est
    généralisé à ce type de débordement : si aucune taille ne suffit même au
    plancher, le build le signale désormais comme un vrai défaut au lieu
    d'un print perdu — c'est l'évolution du check graphique demandée.

v2.12 (2026-09-03) : deuxième passe sur les mêmes 4 slides signalées, cette
fois avec un rendu PowerPoint réel de CHAQUE slide (pas un échantillon) —
deux défauts réels supplémentaires trouvés, tous deux présents dans les DEUX
moteurs de rendu (donc jamais des artefacts LibreOffice comme la slide 1) :
  - `slide_executive_summary` (slide 2) était le SEUL appel `content_slide()`
    de tout le générateur (~30 autres) sans `color=` explicite — son kicker
    retombait sur l'accent cyan générique au lieu du NAVY du chapitre 01
    qu'elle ouvre, déjà porté par ses deux slides suivantes. Corrigé en
    passant `color=NAVY`.
  - `slide_cover` (slide 1) affichait une version gelée sur "v2.8 ·
    2026-09-02" depuis 4 bumps de version consécutifs (v2.9 à v2.11) — la
    chaîne était écrite en dur dans la fonction plutôt que dérivée d'une
    source unique. Introduit `VERSION_DECK`/`DATE_VERSION_DECK` (constantes
    de module) + un test de régression (`test_generate_deck.py`) qui compare
    `VERSION_DECK` à la dernière entrée "vX.Y" du docstring de ce module et
    au texte réellement posé sur le placeholder de couverture — ce test a
    lui-même détecté l'écart en cours d'écriture de cette entrée.

v2.13 (2026-09-03) : diagnostic étage 2 rafraîchi (2 jours périmé) a trouvé
`content_slide(prs, kicker, title, color=None)` — sur 34 vrais appels
(37 occurrences moins 3 en commentaire), TOUS passent déjà `color=`
explicitement depuis ce module. Le repli `color or ACCENT` ne protégeait
donc plus personne : sa seule fonction résiduelle était de laisser un futur
appel oublié retomber en cyan silencieux, exactement le défaut de v2.12.
`color` devient un paramètre obligatoire (zéro régression mesurée, 34/34
appels déjà conformes) — un appel qui l'omettrait échoue maintenant au
build (`TypeError`), pas au rendu.

`slide_executive_summary` DÉMÉNAGE (arbitrage utilisateur 2026-09-03) de
juste après la couverture à juste après l'intercalaire du chapitre 01 —
modifié manuellement par l'utilisateur sur l'export, reporté dans `build()`
pour que toute régénération le conserve.

Brouillon `slide_synthese_pourquoi_quoi_comment` ajouté (demande
utilisateur) mais **NON câblé dans `build()`** — généré et vérifié en
isolation pour validation avant intégration, sur consigne explicite
("pour l'instant ne génère que cette slide").

v2.14 (2026-09-03) : `slide_synthese_pourquoi_quoi_comment` est CÂBLÉE dans
`build()` (46 -> 47 slides), au chapitre 01 entre le sommaire et le pitch en
trois faces : elle développe ce que le sommaire annonce, avant que le pitch
ne l'ouvre au client. La version isolée de v2.13 avait été demandée puis
n'était visible nulle part — le fichier d'aperçu avait été supprimé au
nettoyage après envoi de la capture, donc l'utilisateur cherchait une slide
qui n'existait dans aucun export ouvrable. Leçon : une slide "générée pour
validation" doit rester ouvrable quelque part, ou être câblée.
Décalage d'index : l'intercalaire du chapitre 01 reste en 2, tout ce qui
suit la nouvelle slide glisse de +1 (slide_vision 6 -> 7, intercalaires
7/11/14/17/21/28/37/41 -> 8/12/15/18/22/29/38/42).

v2.15 (2026-09-03) : `slide_synthese_pourquoi_quoi_comment` REFONDUE —
retour utilisateur : les chips "Chapitres X–Y" en pied de colonne étaient
l'inverse exact de la consigne ("sans faire référence au chapitre"), qui
posait aussi un test précis d'autonomie ("si je ne lis QUE cette slide, je
comprends sans les autres ?"). Chips retirées ; le pied de chaque colonne
COMMENT nomme désormais ses 3 temps en toutes lettres (Comprendre / Définir
/ Faire adopter, puis réévaluer) plutôt que des symboles ①②③⟲ nus qui
supposaient déjà connu le reste du deck. Une bande de clôture, sur le même
principe que la note "Bifurcation..." de slide_trajectoire, synthétise
POURQUOI→QUOI→COMMENT en une phrase — le résumé qu'on emporte seul.

v2.16 (2026-09-03) : `slide_synthese_pourquoi_quoi_comment` RETIRÉE de
`build()` (47 -> 46 slides) — 2 tours rejetée (v2.14 avec des chips de
chapitre, puis v2.15 malgré leur retrait). La fonction reste définie ;
demande explicite de repasser par une génération ISOLÉE (fichier `.pptx`
autonome, PAS supprimé après coup cette fois — leçon de la disparition
v2.13) pour validation avant toute réintégration.

v2.17 (2026-09-03) : `slide_synthese_pourquoi_quoi_comment` REFONDUE une 2e
fois — v2.15 avait REMPLACÉ les 4 vraies étapes de slide_trajectoire (durées,
descriptions, livrables-clés) par un cadre abstrait à 3 badges POURQUOI/QUOI/
COMMENT ; la consigne était de les CONSERVER, pas de les réinventer. Corrigé :
les 4 phases sont reprises À L'IDENTIQUE de slide_trajectoire (même source de
vérité), un chapô resserré en tête synthétise d'où l'on part (douleurs) et ce
qu'on vise (le produit assaini) pour contextualiser la démarche qui suit.
Génération isolée uniquement (fonction non câblée dans `build()`).

v2.18 (2026-09-03) : ajout d'une bande de clôture — le module agentic (côté
consultant : accélérateur, jamais un remplacement ; côté client : option sous
gate IA) ne figurait pas sur cette slide alors qu'elle porte justement la
démarche que ce module outille. Reprend le rôle des deux cartes concernées de
slide_pitch_iap ("NOTRE OUTILLAGE · CÔTÉ CONSULTANT" et "EN OPTION · CÔTÉ
CLIENT"), sans renvoi de chapitre, dans l'espace resté vide sous la rangée
des 4 temps. Toujours en génération isolée, non câblée.

v2.19 (2026-09-03) : ajout du gate IA clarifié, de la liste des agents
possibles côté consultant (accélérateur, module BMAD IAP) et côté client en
option (3 candidats agentic-implementation, chacun avec son objectif/résultat
— repris de slide_pitch_iap et des slide_agent_ia du chapitre IA), et des 3
familles de KPIs résumées (source slide_kpis) — arbitrage utilisateur via
AskUserQuestion : « slide unique, très compacte » plutôt qu'un découpage en 2
slides, malgré le volume. Chapô renforcé : douleurs mesurées → assainir le
gaspillage → chemin vertueux, démarche centrée sur l'agentic comme
accélérateur dès l'ouverture. Toujours en génération isolée, non câblée.

v2.20 (2026-09-03) : retour utilisateur — texte trop petit, objectifs et
livrables pas assez détaillés, pas de résultat tangible/observable. Police
remontée d'un cran partout ; chaque agent distingue désormais OBJECTIF et
RÉSULTAT ; le triage de tickets porte le chiffre EXACT du cas nominal RUN de
slide_kpis_exemple (25 min → 12 min, ≈15 tickets/mois) au lieu d'une
reformulation qualitative ; livrables des 4 phases restaurés en intégralité ;
la bande KPI ajoute ce même cas chiffré comme résultat tangible observable,
avec sa réserve d'origine (fixture illustrative, pas un client réel). Toujours
en génération isolée, non câblée.

v2.21 (2026-09-03) : (1) étape OPTIONNELLE « Constitution du TOM » ajoutée
entre ① et ②, encadré pointillé même grammaire visuelle que les « EXTENSION
POSSIBLE » de slide_offre_iap — livrables le TOM et la roadmap de déploiement.
(2) Livrable de ② corrigé : une ÉVALUATION du pilote, pas un plan (qui
viendrait avant, pas après avoir déployé). (3) Chaque phase porte désormais un
RÉSULTAT VISÉ en plus de son livrable. (4) Colonne consultant recentrée
verticalement dans sa carte (déséquilibre v2.20 avec la colonne client, plus
fournie). Toujours en génération isolée, non câblée.

v2.22 (2026-09-03) : retour utilisateur — l'étape optionnelle doit vivre SUR
la timeline, pas flotter au-dessus sans lien visuel. Remplacé par un nœud
pointillé (`_oval` + dash_style) posé directement sur la ligne, centré entre
① et ②, dont le centre est à la même hauteur que les 4 badges — l'encadré
descriptif touche le nœud sans espace (bulle rattachée à son point sur la
ligne, pas une annotation indépendante). Toujours en génération isolée, non
câblée.

v2.23 (2026-09-03) : retour utilisateur — l'encadré au-dessus de la timeline
poussait toute la rangée vers le bas sans rien gagner (« ça casse la
possibilité d'utiliser l'espace »). Le texte de l'étape optionnelle descend
au MÊME niveau que les 4 colonnes (même bandeau vertical, à côté d'elles) ;
seul le nœud reste sur la ligne. Deuxième retour dans la foulée : beaucoup de
blanc entre le titre de la slide et le début du contenu (CONTENT_TOP,
1.15in, laisse ~0.35in sous le vrai bas du placeholder titre à 0.80in) — une
constante `debut` LOCALE à cette fonction (0.85in) remplace CONTENT_TOP ici
sans toucher le rythme des 45 autres slides. Toujours en génération isolée,
non câblée.

v2.24 (2026-09-03) : le texte de l'étape optionnelle placé DANS le gap ①→②
(v2.23) chevauchait réellement le texte des colonnes voisines — le gap ne
fait que GAP=0.2in, la largeur utilisée (1.9in) débordait largement dessus.
`verifier_geometrie` ne l'a pas vu : elle mesure les sorties de slide, pas les
chevauchements entre formes — trouvé seulement au rendu réel. Corrigé par une
bande compacte PLEINE LARGEUR juste sous la rangée des 4 temps (au lieu d'un
texte étroit coincé entre deux colonnes) : reste juste après le contenu du
gap ①→②, sans recréer la collision. Toujours en génération isolée, non
câblée.

v2.25 (2026-09-03) : retour utilisateur — l'étape optionnelle doit être une
VRAIE colonne, structurée comme les 4 autres (titre, durée, description,
résultat visé, livrable), pas un texte à part. Passage à 5 colonnes (① →
Constitution du TOM [optionnel, badge pointillé] → ② → ③ → ⟲). Contenu
fourni : durée 3-4 sem., résultat visé "un cadre de référence adapté à
l'organisation et aux contraintes du client". Pour compenser la colonne
supplémentaire sur la même largeur, marges LOCALES à cette fonction
(marge_g=0.38in, gap inter-colonnes 0.14in) réduites par rapport aux
constantes globales (qui restent celles des 45 autres slides) — vérifiées
contre le chrome du template (badge de page x=9.25-9.70 y=5.09-5.32, jamais
franchi ; bord droit inchangé à 9.15 pour garder 0.10in de marge). Toujours
en génération isolée, non câblée.

v2.26 (2026-09-03) : retour utilisateur — utiliser encore plus d'espace à
droite et en bas, agrandir le texte. Bord droit 9.15 -> 9.2 (garde 0.05in
avant le badge de page) ; bas visé 5.55 -> 5.58in (garde 0.045in avant le
vrai bord de slide, 5.625in). Toutes les polices de la slide remontées d'un
cran (chapô 7->8, titres de colonne 6->7, badges 8.5->10, description/
résultat/livrable 5->6, gate IA 6->7, agents 5.5->6.5, KPI 5.25->6.5) ; gaps
internes resserrés en compensation pour rester dans le budget vertical.
Toujours en génération isolée, non câblée.

v2.27 (2026-09-03) : v2.26 débordait réellement (`bas_max` défini mais jamais
appliqué — trouvé au rendu réel, pas par `verifier_geometrie` qui ne mesure
que les sorties de SLIDE, pas les cibles internes) : bande KPI coupée de
~0.3in. Retour utilisateur, 3 demandes : (1) « Résultat tangible observable »
retiré de la bande KPI, qui ne liste plus que les 3 familles — kpi_h quasi
divisé par 2, le plus gros des gains ; (2) mots « markdown amendé » retirés
des livrables ② et ⟲ ; (3) les 5 séquences, jusque-là nues, sont désormais
encadrées d'une carte à bord arrondi (teinte pâle de la couleur de la phase,
nouveau helper `_pale`) comme le sont déjà gate/agents/KPI en dessous —
largeur de colonne inchangée (pas d'inset propre à la carte, seul `ecart`
sépare deux cartes visuellement). Écart inter-colonnes 0.14 -> 0.10in et pad
vertical des cartes agents 0.08 -> 0.05in (retour « gagner de la place »,
regagnent la marge nécessaire). Les offsets verticaux des 5 colonnes
(ty/chip_y/desc_y/resultat_y/livr_y) sont désormais calculés UNE FOIS avant
la boucle, plus dans chaque itération — évite de dupliquer la formule pour la
carte (la v2.26 avait déjà payé une fois le prix d'une formule dupliquée qui
divergeait silencieusement). Vérifié par recalcul : bas de slide à 5.56in,
sous `bas_max` (5.58in). Toujours en génération isolée, non câblée. (Cette
fonction reste un brouillon de travail, plusieurs itérations postérieures non
journalisées ici — cf. son propre historique inline.)

v2.28 (2026-09-03, demande utilisateur) : `slide_specificites_infra` AJOUTÉE
ET CÂBLÉE (46 -> 47 slides) — ouvre le chapitre 02 · Contexte, avant
slide_mission/slide_pourquoi_contexte. Deux paires constat → réponse
(sursollicitation/guichet → assainir le gaspillage ; mieux servir les
utilisateurs → infra as product) posent le terrain générique, un bloc
d'escalade explicite que l'arrivée de l'IA aggrave la sursollicitation, puis
la conclusion — « infra as a service », terme neuf et volontairement distinct
d'« infra as product » déjà établi ailleurs dans le deck. Décalage d'index :
tout ce qui suit glisse de +1 (les intercalaires 8/12/15/18/22/29/38/42 de la
v2.14 deviennent 9/13/16/19/23/30/39/43).

v2.29 (2026-09-03, demande utilisateur) : (1) `slide_specificites_infra`
retravaillée — palette simplifiée (les 4 pilules constat/réponse passent de
5 aplats vifs à des cartes blanches + liseré, seuls le bloc alerte IA et la
conclusion restent en fond plein), remise dans les couleurs du thème OCTO
(cyan `ACCENT`/accent3 du template — jamais utilisé sur cette slide jusqu'ici
— remplace le navy comme accent « réponse »), douleur équipe ajoutée
(décommissionnement jamais fait, trop de RUN, même vocabulaire que
slide_vision). (2) `slide_infra_as_product_exemple` AJOUTÉE ET CÂBLÉE
(47 -> 48 slides), juste après — rend tangible la conclusion de la slide
précédente avec un avant/après repris du cas nominal déjà établi ailleurs
(slide_kpis_exemple : 25 min -> 12 min, ≈15 tickets/mois), pas un exemple
inventé pour l'occasion. Décalage d'index : intercalaires 12/15/18/22/29/38/
42 de la v2.28 (chapitres 03 à 09) deviennent 13/16/19/23/30/39/43 (chapitre
01 et l'intercalaire du chapitre 02 lui-même, en 2 et 7, inchangés — l'ajout vient
après eux).

v2.33 (2026-09-10, demande utilisateur en 3 lots) : le deck passe EN CHARTE
OCTO et gagne un chapitre. (1) La couleur cesse de porter le sens — mesure
fondatrice : les 9 slides d'exemple du template ne posent que 3 couleurs
(#0E2356, #FFFFFF, #00D2DD). Les 160 sites `D.PALETTE[n]` tombent sur `ENCRE` ;
`SEVERITE` passe du vert->rouge a une rampe monochrome ; la differenciation
passe par « un sur N en accent », la numerotation, la position et la forme.
Le cyan ne porte JAMAIS de texte (1,86:1 sur blanc) : garde `encre_de()`.
(2) Nouveau chapitre 03 « Specificites de l'infra » — `slide_infra_run` et
`slide_infra_transverse` neuves, les 2 slides infra remontent du chapitre 01,
et 03..09 deviennent 04..10. Les renvois entre chapitres citent desormais le
NOM et plus le numero : une renumerotation ne peut plus les rendre faux.
(3) `slide_gaspillage_partage` neuve au chapitre Proposition : la chaine de
traitement, jusque-la presentee cote cabinet, est retournee en « qui fait quoi
et ce qui se tranche a deux ». 49 -> 53 slides. Les index de slides des tests
sont DERIVES du deck (layouts) au lieu d'etre recomptes a la main.

v2.30 (2026-09-04, demande utilisateur) : les 3 slides de refonte graphique
validées isolément (`check_slide_synthese-v3-refonte.pptx` — système "contour"
: conteneurs en trait, chevrons non pivotés, badges chevauchant un bord plutôt
que reliés par flèche, bandeau de citation) sont réintégrées dans le deck
final. `slide_specificites_infra` et `slide_infra_as_product_exemple`
DÉMÉNAGENT du chapitre 02 · Contexte vers le chapitre 01 · Exec summary (juste
après `slide_executive_summary`) ; `slide_synthese_pourquoi_quoi_comment`
(brouillon jamais câblé depuis son retrait v2.16) est AJOUTÉE entre les deux.
47 -> 48 slides retirées du chapitre 02 puis 48 -> 49 avec l'ajout : le
chapitre 02 commence directement par `slide_mission` après son intercalaire
(inchangé, en 10 — décalé de +3 par les 3 slides insérées dans le chapitre 01).
Décalage d'index : intercalaires 7/13/16/19/23/30/39/43 de la v2.29 deviennent
10/14/17/20/24/31/40/44 ; `slide_vision`, en 6, devient 9. Police "Outfit"
(Google Fonts, OFL) appliquée à TOUT le deck via `_appliquer_police_deck`,
avec repli en Arial sur les seuls glyphes hors couverture de la police
(①②③⟲ — vérifié par cmap sur les deux moteurs de rendu, LibreOffice ET
PowerPoint COM).

v2.34 (2026-09-11, demande utilisateur) : le chapitre 01 « Exec summary »
passe de 5 slides de contenu à 3 (« trop lourd, max 3 slides, plus
synthétique ») et gagne ce qui lui manquait (« une démarche centrée sur les
spécificités de l'infra sans forcément avec IA — que propose-t-on sans IA ? »).
`slide_pitch_iap` et `slide_demarche_avec_sans_agentic` sont SUPPRIMÉES
(54 -> 52 slides) : la première ouvrait le chapitre sur trois cartes dont deux
parlaient d'agentic, la seconde étalait « sans outillage / avec le module /
agentic chez le client » sur trois lignes d'égal poids visuel — un lecteur y
voyait un choix à faire, et l'IA comme sujet de l'exec summary. Restent
`slide_executive_summary` (le sommaire, inchangé hors son bloc OFFRE, qui
citait mot pour mot les deux slides supprimées), `slide_synthese_pourquoi_quoi_
comment` REFONDUE et `slide_vision` (intacte). Ce qui est sacrifié, pour
mémoire : la bande « MATÉRIAU DE CADRAGE » (trois contextes sectoriels), le
détail des 4 personas et des 11 agents du module, et la grille 3 temps ×
3 registres — tous encore portés par les chapitres Personas, Besoins &
douleurs, Outillage IAP et Démarche. Ce qui SURVIT, parce que l'utilisateur
l'avait défendu en table ronde : la distinction outillage-du-consultant vs
agentic-déployé-chez-le-client, réduite à une bande basse de deux encarts en
contour gris avec ses deux silhouettes `_picto`. La refonte inverse la
hiérarchie : la démarche infra (ORGANISATION / INFRA par temps, verbes repris
de `slide_fil_technique`) est le corps de la slide, l'agentic n'est plus qu'une
annotation, et la clôture affirme noir sur blanc qu'aucun des quatre temps ne
requiert l'IA.

Séparateurs : chapitres = intercalaire teardrop (photo + numéro, layout dédié) ;
sous-chapitres = `slide_sous_chapitre` (bloc-titre léger, sans photo ni numéro —
sans appelant depuis la v2.6, machinerie conservée).

Centré sur les résultats du cadrage (mission, doctrine, méthode, maturité,
ambition, KPIs, schéma de fonctionnement) plutôt que sur tout le détail de
mise en œuvre. Le commit 4f0c9b7 avait retiré ce détail d'implémentation ;
l'arbitrage utilisateur du 2026-07-21 rouvre ce périmètre sur DEUX points
précis seulement, désormais dans le deck :
  - l'architecture des 11 agents-workflows (slide_architecture_agents,
    inventaire des composants — complémentaire du schéma de flux, pas un
    doublon) ;
  - l'étude des personas / product discovery (slide_personas, réouverture de
    la discovery fusionnée en MVP1, §Décision de cadrage ligne 236).
Restent hors périmètre (toujours du support interne, pas une synthèse
exécutive) : le schéma des workflows détaillé, la roadmap MVP et les points
ouverts — les trois autres slides retirées au même commit ne sont PAS
réintroduites.

v2.35 (2026-09-18, restructuration validée en salle de délibération, arbitrage
utilisateur) : le sommaire passe de 10 à 9 chapitres — 8 chapitres de corps
dans l'ordre EXECUTIVE SUMMARY > CONTEXTE > ENJEUX > DOULEUR > OPPORTUNITES >
OFFRE > DEMARCHES > NEXT STEPS, plus un chapitre ANNEXES. Mapping :
  - Contexte reprend l'ancien Contexte + `slide_specificites_infra` (l'ancien
    chapitre Spécificités de l'infra).
  - Enjeux (NEUF, `slide_enjeux`) compose une lecture organisationnelle/macro
    des tensions personas (les 4 portraits détaillés partent en annexe) et
    récupère `slide_infra_run`/`slide_infra_transverse`/
    `slide_infra_as_product_exemple`.
  - Douleur = ancien Besoins & douleurs, inchangé.
  - Opportunités (NEUF, `slide_opportunites`) compose ce que le cadrage rend
    possible maintenant à partir de faits déjà écrits (gate IA, méthode
    scorée, team topologies) sans dupliquer leur détail.
  - Offre fusionne l'ancien Proposition et le reste de l'ancien IA (gate,
    prudence, 3 agents candidats, export markdown).
  - Démarches fusionne l'ancien Démarche et l'ancien Outillage IAP (l'ambition
    et le lien SI deviennent une sous-partie plutôt qu'un chapitre à part).
  - Next steps (NEUF, `slide_next_steps`) récupère `slide_conditions_reussite`
    (fin de l'ancien Démarche) et résume le KPI à 4 indicateurs de suivi.
  - Annexes (NEUF en v2.35) gardait, visibles et tracés, les 4 portraits
    personas (`slide_personas`, `slide_personas_divergences`) et le
    dispositif KPI complet (`slide_kpis`, `slide_kpis_pourquoi_quoi`,
    `slide_kpis_mise_en_place`, `slide_maturite`, `slide_kpis_exemple`).
`slide_executive_summary` (le sommaire) est mis à jour pour citer les 8
chapitres de corps. Toute citation de chapitre par
NOM dans les slides existantes a été corrigée pour pointer vers le nouveau
nom (`chapitre IA`/`Proposition` -> `chapitre Offre`, `chapitre Démarche` ->
`chapitre Démarches`, `chapitre Spécificités de l'infra` -> `chapitre
Contexte`, `chapitre Outillage IAP` -> `chapitre Démarches`) — jamais par
numéro, donc la renumérotation elle-même ne casse rien.

v2.36 (2026-09-18, demande utilisateur) : le chapitre Annexes est retiré du
deck — les 7 fonctions qu'il portait seules (`slide_personas`,
`slide_personas_divergences`, `slide_kpis`, `slide_kpis_pourquoi_quoi`,
`slide_kpis_mise_en_place`, `slide_maturite`, `slide_kpis_exemple`) sont
supprimées du fichier (récupérables dans l'historique git, dernier état au
commit 636f160). Le sommaire (`slide_executive_summary`) ne mentionne plus
l'annexe. La synthèse déjà composée dans Enjeux et Next steps reste seule
trace de ce contenu dans le deck.

v2.37 (2026-09-20, demande utilisateur « plus lisible ») : fils humain et
technique fusionnés en `slide_deux_fils`, les 3 slides d'agent regroupées en
`slide_agents_candidats`, `slide_livrables_ppt` supprimée — 45 -> 41 slides.

v2.38 (2026-09-23, arbitrages du cadrage v2.7) : IAP est une démarche et une
offre de conviction — `slide_conditions_reussite` ne parle plus de
non-engagement ni de test sponsor avant signature ; le nom « Infrastructure
as a Product » est gardé ; l'Assessment flash ouvre la démarche avant toute
action d'accompagnement ; la réévaluation est portée par `iap-strategy-lead`.

Usage : python generate_deck.py
Sortie : bmad-iap-cadrage-synthese.pptx (à côté de ce script).
"""
import os
import sys

sys.path.append(os.path.dirname(__file__))
import pptx_deck as D
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.dml import MSO_LINE_DASH_STYLE
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Emu, Inches, Pt

# Source unique du numero de version affiche sur la couverture (slide_cover) —
# jusqu'a v2.12 c'etait une chaine gelee dans slide_cover, jamais mise a jour a
# 4 bumps de version consecutifs (v2.9 a v2.11 ont toutes laisse "v2.8 · date
# perimee" sur la SLIDE LA PLUS VISIBLE du deck). Un seul endroit a changer
# desormais.
VERSION_DECK = "v2.38"
DATE_VERSION_DECK = "2026-09-23"

HERE = os.path.dirname(__file__)
TEMPLATE = os.path.join(HERE, "template-octo.pptx")
REPO_ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.append(os.path.join(REPO_ROOT, ".claude", "skills", "pptx-framed-image", "scripts"))
import nature_images  # noqa: E402
import stock_images  # noqa: E402
from framed_image import cover_crop_to_aspect, frame_obstructions, place_image_in_frame  # noqa: E402
from PIL import Image as _PILImage  # noqa: E402

IMG_DIR = os.path.join(HERE, "_img")
os.makedirs(IMG_DIR, exist_ok=True)
IMG_MANIFEST = os.path.join(HERE, "images-manifest.json")

LAYOUT_COUVERTURE = 8   # "40 - Couverture [1]" — idx0 titre, idx1 sous-titre, idx2/idx3 crédit+date
LAYOUT_TITRE_SEUL = 5   # "04 - Titre seul" — idx0 titre, garde logo/pied de page/n° de slide
LAYOUT_VIDE = 0         # "06 - Slide vide" — pas de placeholder, juste logo + badge de pagination
LAYOUT_CHAPITRE = 2     # "50 - Chapitre [1]" — idx0 titre (grand), idx1 numéro ; cadre photo teardrop
LAYOUT_VISUEL_DROITE = 15  # "63 - Titre, contenu et visuel à droite - cadre blanc"

# --- Géométrie du template OCTO réel (10 x 5.625 in, 16:9) — cf.
# docs/vscode1-export/template-octo.md §4-5, vérifiée localement contre
# template-octo.pptx (mêmes dims/layouts/thème). Contenu dessiné dans la
# zone de contenu du layout « Titre seul » (sous le titre, au-dessus du
# pied de page), marge gauche alignée sur le placeholder titre (0.615 in),
# marge droite plafonnée avant le badge de pagination bas-droit.
SLIDE_W, SLIDE_H = 10.0, 5.625
MARGIN = 0.615
BORD_DROIT = 9.15
CONTENT_TOP = 1.15
CONTENT_BOTTOM = 5.45
CONTENT_W = BORD_DROIT - MARGIN
CONTENT_H = CONTENT_BOTTOM - CONTENT_TOP
GAP = 0.2

def _exiger_template():
    """Garde à l'import (finding robustesse, audit 2026-07-23) : sans elle, un
    template absent remontait en FileNotFoundError brute depuis python-pptx. Le
    générateur est lancé à la main — l'échec doit nommer le fichier attendu et
    son emplacement, sans exiger de lire la stack."""
    if not os.path.isfile(TEMPLATE):
        raise SystemExit(
            "generate_deck : template introuvable — placer template-octo.pptx "
            f"à côté du générateur (attendu : {TEMPLATE})"
        )


_exiger_template()
TH = D.theme_colors(Presentation(TEMPLATE))
NAVY = TH.get("dk1", D.INK)          # #0E2356 — texte principal, titres
DK2 = TH.get("dk2", NAVY)            # #3E4F78 — navy secondaire (palier de gradient sans PALETTE)
WHITE = TH.get("lt1", "#FFFFFF")
ACCENT = TH.get("accent3", NAVY)    # #00D2DD — cyan OCTO, identité du deck
MUTED = TH.get("lt2", D.MUTED)       # #586586 — slate 600, texte secondaire
ACCENT1 = TH.get("accent1", MUTED)   # #6E7B9A — bleu-gris clair (palier de gradient sans PALETTE)
ACCENT2 = TH.get("accent2", ACCENT1)  # #9FA7BB — bleu-gris très clair, le plus clair du thème
LINE = TH.get("accent5", D.LINE)     # #CFD3DD — slate 200, bordures de cards
TRACK = TH.get("accent6", D.TRACK)   # #E7E9EE — slate 100, fonds d'encarts

# D0..D4 : rampe MONOCHROME de la famille navy, du clair au foncé. Une
# échelle ordonnée se rend par une rampe, pas par des teintes étrangères —
# le vert->rouge d'avant lisait comme un feu tricolore sur un thème qui n'a
# ni vert ni rouge. Les 5 tons portent tous du texte blanc (chip() écrit en
# blanc par défaut) : le plus clair, #586586, tient 5,80:1 — un chiffre estimé
# à 5,0 de tête ici le 2026-09-10, puis mesuré. Le rejouer plutôt que le citer :
#   ratio = (L1+0,05)/(L2+0,05), L = luminance relative WCAG 2.x.
# ATTENTION, mesuré aussi : la rampe ne discrimine plus ses paliers adjacents
# (1,18 / 1,18 / 1,40 / 1,33). D0 et D2 — « CONFIRMÉ » et « DÉDUIT » — ne se
# distinguent QUE par leur texte. C'est assumé tant qu'un libellé les
# accompagne ; une échelle lue à l'œil seul demanderait plus d'amplitude.
SEVERITE = ["#586586", "#4A5A80", "#3E4F78", "#26386A", "#0E2356"]


def _rgb(hexcolor):
    return RGBColor.from_string(hexcolor.lstrip("#").upper())


def new_prs():
    _exiger_template()
    prs = Presentation(TEMPLATE)
    # Retire les 9 slides d'exemple du template — masters/layouts/thème conservés.
    # Il faut aussi supprimer la relation (drop_rel), sinon les parties
    # ppt/slides/slideN.xml orphelines entrent en collision de nom avec les
    # nouvelles slides ajoutées ensuite (même numérotation réutilisée).
    xml_slides = prs.slides._sldIdLst
    for sld in list(xml_slides):
        rId = sld.get(D.qn("r:id"))
        prs.part.drop_rel(rId)
        xml_slides.remove(sld)
    return prs


# Il n'y a PLUS de couleur par chapitre. Un mecanisme `PALETTE_CHAPITRES` /
# `couleur_chapitre()` a existe quelques heures le 2026-09-10, entre la mesure
# de l'ecart a la charte et l'arbitrage qui a suivi : il cyclait 4 tons du
# theme sur les chapitres. L'arbitrage — la couleur ne porte pas le sens — l'a
# rendu caduc le jour meme. Retire plutot que laisse en place : ses 10 appels
# reels passaient deja `ENCRE` en dur, et ses 2 seuls appelants residuels
# donnaient un kicker GRIS a deux slides dont l'intercalaire est navy.
#
# --- Vocabulaire de différenciation SANS code couleur (arbitrage du 2026-09-10)
#
# La couleur ne porte plus le sens. Les 160 sites qui appelaient `D.PALETTE[n]`
# — un bleu pour l'infra, un teal pour l'utilisateur, un or pour le management,
# un violet pour le sponsor — pointent tous sur `ENCRE`. Ce qui différencie
# désormais deux éléments de même niveau, dans l'ordre où le catalogue des decks
# OCTO réels les emploie (`deck-design-library`) :
#
#   1. « UN SUR N EN ACCENT » — dans une série d'éléments égaux, un SEUL reçoit
#      un aplat plein (cyan ou navy), les autres restent blancs à contour. Le
#      catalogue le donne comme le mécanisme de hiérarchie le plus systématique
#      du deck, avant même la taille de police.
#   2. La NUMÉROTATION (badge « goutte » + connecteur) et la POSITION (quinconce
#      plutôt qu'alignement en tableau).
#   3. La FORME-SIGNATURE : coins arrondis + un coin coupé pour le contenu
#      riche, pilule pour les chips et étiquettes.
#   4. La TYPOGRAPHIE : accroche grasse + complément régulier, sous-en-têtes en
#      majuscules 8-9pt comme rupture sans bordure.
#
# RÈGLE DURE, mesurée au rendu du 2026-09-10 : le cyan ne porte JAMAIS de texte
# sur blanc — il plafonne à ~1,9:1 et le libellé se délave (constaté sur
# « Infra & RUN » de la slide personas). Cyan = aplat, badge, chip, connecteur.
ENCRE = NAVY                 # tout ce qui porte du sens : texte, contours, filets
ACCENT_PLEIN = ACCENT        # cyan — l'élément mis en avant d'une série, EN APLAT
SUPPORT = TRACK              # fond neutre d'encart, jamais porteur de sens
SUPPORT_LIGNE = LINE         # bordures discrètes


def encre_de(color):
    """Couleur de TEXTE sûre pour un élément dont l'accent est `color`.

    Beaucoup de renderers font piloter la bordure, la barre d'accent ET le
    libellé par une seule variable `color`. C'est commode tant que la couleur
    est sombre — et faux dès qu'elle vaut le cyan : le texte se délave à
    ~1,9:1 sur blanc (constaté au rendu du 2026-09-10 sur l'exec summary et sur
    « Infra & RUN »). Cette garde laisse passer les tons sombres et rabat le
    seul cyan sur l'encre, pour que l'accent reste VISIBLE (bordure, barre,
    aplat) sans que le libellé devienne illisible.
    """
    return ENCRE if str(color).lower() == str(ACCENT).lower() else color


def content_slide(prs, kicker, title, color):
    # v2.13 : `color` etait optionnel (repli sur ACCENT, cyan generique) —
    # diagnostic du 2026-09-03 : 34/34 appels reels de ce module passent deja
    # `color=` explicitement, le repli ne protegeait plus rien, il masquait
    # silencieusement un oubli (cf. le defaut kicker de slide_executive_summary,
    # v2.12). Obligatoire desormais : un oubli echoue au build, pas au rendu.
    layout = prs.slide_masters[0].slide_layouts[LAYOUT_TITRE_SEUL]
    s = prs.slides.add_slide(layout)
    ph = s.shapes.placeholders[0]
    box_w = Emu(ph.width).inches
    # `encre_de` ici et pas ailleurs : c'est LE chemin de kicker du deck, et
    # deux appelants lui passent ACCENT (kicker cyan sur blanc = 1,86:1).
    kicker_color = encre_de(color)
    texte_complet = f"{kicker.upper()}   ·   {title}"
    taille, _ = D.ajuster_police([texte_complet], box_w, 17, 12,
                                  lambda t, lignes_max: lignes_max <= 1)
    tf = ph.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    r1 = p.add_run()
    r1.text = kicker.upper() + "   ·   "
    r1.font.bold = True
    r1.font.size = Pt(taille)
    r1.font.color.rgb = _rgb(kicker_color)
    r2 = p.add_run()
    r2.text = title
    r2.font.bold = True
    r2.font.size = Pt(taille)
    r2.font.color.rgb = _rgb(NAVY)
    return s


def slide_sous_chapitre(prs, kicker, titre, sous_titre, color):
    """Séparateur de SOUS-chapitre (léger) : PAS l'intercalaire teardrop des
    chapitres (layout dédié + photo), juste un bloc-titre de section sur le layout
    « titre seul ». Introduit un groupe logique DANS un chapitre. Reste plus léger
    qu'un chapitre : pas de numéro, pas de photo, garde le pied de page du master.
    SANS APPELANT depuis la v2.6 : le seul groupe qui l'utilisait — « Exemples »
    dans la Proposition — a été supprimé à la demande (l'arbitrage 2026-07-22
    « un séparateur pour les Exemples » est caduc, les 3 slides d'exemple vivent
    dans git, v2.5). Machinerie des séparateurs à deux niveaux conservée (cf.
    CLAUDE.md §docs/cadrage-ppt) pour un futur groupe logique."""
    layout = prs.slide_masters[0].slide_layouts[LAYOUT_TITRE_SEUL]
    s = prs.slides.add_slide(layout)
    # Vider le placeholder titre (sinon prompt résiduel) — on pose notre propre bloc.
    s.shapes.placeholders[0].text_frame.text = ""
    bar_top, bar_h = 2.05, 1.55
    D.add_rect(s, MARGIN, bar_top, 0.14, bar_h, fill=color, rounded=True, radius=0.5)
    tx = MARGIN + 0.45
    tw = CONTENT_W - 0.45
    D.add_text(s, tx, bar_top, tw, bar_h, [
        (kicker.upper() + "  ·  SOUS-CHAPITRE",
         dict(size=D.TYPE["tiny"], bold=True, color=encre_de(color), line_spacing=1.0)),
        (titre, dict(size=34, bold=True, color=NAVY, space_before=8, line_spacing=1.0)),
        (sous_titre, dict(size=D.TYPE["small"], color=MUTED, italic=True, space_before=12, line_spacing=1.2)),
    ], anchor=MSO_ANCHOR.MIDDLE)
    return s


def _sans_puce(paragraph):
    """Retire l'indentation de puce héritée (marL/indent) et désactive le
    caractère de puce. Cause réelle du bug "01" qui passe à la ligne dans le
    petit encart numéro du layout Chapitre : son style de liste hérité pose
    marL=0.5in (indentation de puce) dans un encart large de 0.546in — il ne
    reste presque plus de largeur utile, donc chaque caractère wrap. Le REX
    V3 (VSCode1) corrige exactement ça avec un pPr marL=0/indent=0/buNone
    explicite ; python-pptx n'expose pas ces attributs, d'où la manipulation
    XML directe."""
    pPr = paragraph._p.get_or_add_pPr()
    pPr.set("marL", "0")
    pPr.set("indent", "0")
    for tag in ("a:buChar", "a:buAutoNum", "a:buNone"):
        for el in pPr.findall(qn(tag)):
            pPr.remove(el)
    pPr.append(pPr.makeelement(qn("a:buNone"), {}))


def _find_frame_by_geom(shapes, prst):
    """Cadre non groupé (top-level) portant un prstGeom donné — variante de
    pptx-framed-image.frame_geometry pour le cas où le cadre n'est pas niché
    dans un groupe (le layout Chapitre du template, à la différence des
    layouts « cadre blanc », place son cadre teardrop directement)."""
    for sh in shapes:
        spPr = getattr(sh._element, "spPr", None)
        if spPr is None:
            continue
        g = spPr.find(qn("a:prstGeom"))
        if g is not None and g.get("prst") == prst:
            return sh.left, sh.top, sh.width, sh.height, g
    return None


def _find_frame_in_group(shapes, group_name, inner_name):
    from framed_image import frame_geometry
    for sh in shapes:
        if sh.name == group_name:
            return frame_geometry(sh, inner_name)
    return None


# scene -> requête Openverse (photo réelle) ; la génération procédurale
# (nature_images) reste le nom de "scene" utilisé comme repli hors-ligne.
_REQUETES_PHOTO = {
    "mountains": "mountains landscape",
    "forest": "green forest sunlight",
    # Littoral rocheux turquoise (chapitre Besoins & douleurs) : « ocean waves aerial » (horizon
    # brumeux délavé en blanc) puis « turquoise sea water aerial » (0 résultat
    # Openverse -> repli procédural à ciel pâle) échouaient tous deux à ancrer le
    # haut du cadre teardrop sur le fond blanc de la slide. « turquoise water »
    # (seed 0) renvoie une vue plongeante roche+eau+écume, texturée et contrastée
    # sur les quatre bords — VÉRIFIÉE au rendu réel le 2026-07-21.
    "ocean": "turquoise water",
    "sunset": "sunset sky",
    # Chapitres à photo (restructurations 7 puis 8 puis 9 chapitres) : scènes réelles
    # distinctes, VÉRIFIÉES au rendu réel — une requête mot-clé n'a aucun jugement (cf. « plage
    # bondée », « desert dune » seed 0 → fossile de musée, « winding river » →
    # cloître de monastère), donc chaque photo est validée à l'œil (fetch du _brut
    # puis lecture image avant câblage). Le repli nature_images (procédural) ne se
    # déclenche que si Openverse est indisponible (SSL/0-résultat) ET que le nom de
    # scène est connu du fallback (forest/meadow/mountains/ocean/sunset/tropical) —
    # sinon le générateur PLANTE (ValueError unknown scene). Préférer une vraie photo
    # à du procédural ; cf. mémoire reference-deck-image-fetcher.
    #   dunes  (Proposition) = vue aérienne NASA ; nightsky (IA) = astrophoto ;
    #   canyon (Démarche)    = strates de roche (nom NEUF → repli qui PLANTE, comme
    #                          dunes/nightsky : dépend d'un vrai fetch) ;
    #   meadow (KPI, seed 1) = asters/verges d'or (nom CONNU du fallback → sûr).
    "dunes": "sand dunes",
    "nightsky": "starry night sky",
    "canyon": "canyon landscape",
    "meadow": "meadow wildflowers",
    # tropical (Outillage IAP, chapitre 08 — nommé chapitre 07 en v2.5) : nom CONNU
    # du fallback procédural (forest/meadow/mountains/ocean/sunset/tropical), donc
    # sûr même hors ligne. Photo à VÉRIFIER au rendu réel comme les autres.
    "tropical": "tropical palm leaves",
    # wheatfield (Exec summary, chapitre 01, nouveau v2.8) : épis de blé doré, gros
    # plan texturé — la récolte/le résultat, en écho au thème du chapitre (l'offre
    # ET sa synthèse, « ce que la mission produit »). « golden wheat field sunset »/
    # « wheat field golden hour » (0 résultat Openverse en aspect carré, le cadre
    # teardrop de ce layout est carré — pas « tall » comme les autres chapitres)
    # échouaient ; « wheat field » simple RENVOIE un résultat, gros plan contrasté
    # sur les 4 bords — VÉRIFIÉE au rendu réel le 2026-09-02. Nom NEUF → repli
    # procédural qui PLANTE sauf mapping _SCENE_REPLI (ci-dessous).
    "wheatfield": "wheat field",
    # riverdelta (Specificites de l'infra, chapitre 03, neuf en v2.33) : un delta
    # — un seul cours d'eau qui alimente toutes les branches — dit litteralement
    # le sujet du chapitre (une infra transverse sous plusieurs equipes). « canyon »
    # etait deja pris par la Demarche : deux chapitres a la meme photo se lisent
    # comme une erreur de montage. Nom NEUF -> repli obligatoire ci-dessous.
    # Photo A VERIFIER AU RENDU comme toutes les autres : une requete mot-cle
    # n'a aucun jugement (cf. « desert dune » -> fossile de musee, trouve puis
    # ecarte le 2026-09-01, jamais expose car hors des scenes REELLEMENT
    # appelees par le deck — seul « river delta aerial » l'etait).
    # « river delta aerial » (seed=0, requete d'origine) rendait le resultat
    # Openverse #0 : une image satellite en fausses couleurs arc-en-ciel
    # PORTANT UN FILIGRANE « rawpixel » tuile visible sur toute la photo —
    # trouve au rendu reel zoome du 2026-09-11, jamais vu au rendu non-zoome
    # (la vignette de slide le masque). Reciblee sur la requete plus large
    # « river delta » (7 resultats CC0) : l'index 5 (NASA, credit Openverse,
    # delta du Gange/Brahmapoutre) est SANS filigrane sur toute sa surface
    # (verifie par crop plein-cadre des 3 coins) et sa palette (chenaux
    # sombres/creme) est plus proche de la charte navy+cyan que l'original.
    # Ordre Openverse reverifie stable entre deux appels le 2026-09-11 (meme
    # URL) — meme fragilite structurelle que le reste de ce mapping mot-cle
    # (aucun jugement de contenu cote API), a re-verifier si jamais le
    # resultat change de nature au rendu.
    "riverdelta": "river delta",
}


# Repli procedural : nature_images ne connait que 6 scenes
# (forest/meadow/mountains/ocean/sunset/tropical). Les noms NEUFS choisis pour
# les chapitres (dunes, nightsky, canyon) n'y sont pas — hors reseau ou sur
# 0-resultat Openverse, generate_to levait ValueError HORS du try, ce qui tuait
# build() en entier : 0 slide produite alors que 37 des 40 n'ont pas de photo
# (mesure du 2026-09-01). On mappe donc chaque nom neuf sur la scene connue la
# plus proche visuellement. Ce n'est PAS la meme image — c'est un repli assume,
# dont le but est que le deck sorte, pas qu'il soit identique.
_SCENE_REPLI = {
    "dunes": "sunset",       # tons chauds sable/orange
    "nightsky": "sunset",    # composition de ciel (clair au lieu de sombre)
    "canyon": "mountains",   # relief rocheux
    "wheatfield": "meadow",  # champ ouvert, tons chauds proches
    # « ocean » aurait ete le repli visuellement le plus proche, mais c'est la
    # scene REELLE du chapitre 05 : hors ligne, les chapitres 03 et 05 auraient
    # rendu la meme image. « sunset » n'est la scene reelle d'aucun chapitre —
    # un repli doit degrader, pas dupliquer un voisin. (« canyon » -> mountains
    # porte le meme defaut, anterieur a ce chantier : mountains est la scene du
    # chapitre 02.)
    "riverdelta": "sunset",
}

# Anomalies relevees pendant le build (pas seulement d'image, malgre le nom
# historique), fusionnees dans `problemes` par build(). Sans cela, un defaut
# ne sortait qu'en print : le build annoncait « GEOMETRIE: OK » avec des
# photos manquantes (cadre introuvable/repli impossible) OU, depuis v2.11,
# avec un contenu qui deborde silencieusement sous un element de pied de
# carte (cf. slide_pitch_iap, supprimee en v2.34 -- voir archives/ : le
# self-check geometrique de pptx_deck.py ne
# mesure QUE les formes que NOUS dessinons hors-cadre — pas un debordement de
# texte dans son propre panneau).
_ANOMALIES_BUILD = []


def _image_cache_valide(path):
    """True si `path` est une image utilisable : fichier non vide, décodable
    par PIL, et de dimensions plausibles pour un cadre du deck (>= 32 px sur
    chaque côté, <= 8000 px). Un fichier de 0 octet laissé par un build
    interrompu (Ctrl-C pendant `fetch_to`/`save`) — ou, pour le contenu
    Openverse fraîchement téléchargé, une image corrompue/hors format —
    ne doit jamais être réputé valide (audit VSCode3 2026-09-23, constats
    R2/S1 : `os.path.exists()` seul ne prouve rien sur le contenu)."""
    try:
        if not os.path.exists(path) or os.path.getsize(path) <= 0:
            return False
        with _PILImage.open(path) as im:
            im.verify()
        with _PILImage.open(path) as im:
            largeur, hauteur = im.size
            if largeur < 32 or hauteur < 32 or largeur > 8000 or hauteur > 8000:
                return False
        return True
    except Exception:
        return False


def _remplir_cadre(slide, cadre, scene, seed=0):
    """Pose une vraie photo libre de droit (Openverse, CC0) à l'aspect exact
    du cadre, repli sur la génération procédurale (nature_images) si le
    réseau/l'API n'est pas disponible — cf. pptx-framed-image, greffé depuis
    VSCode1. Une photo réelle lit mieux qu'un aplat vectoriel généré, constat
    fait en comparant au REX "⛱️ L'Été de l'IA" (VSCode1) qui utilise de
    vraies photos sur ces mêmes cadres.

    Contrat du cache disque (``_img/``) : le nom de fichier ``path`` ci-dessous
    ne doit exister QUE pour une vraie photo Openverse — jamais pour un repli
    procédural. Avant ce correctif, le repli s'écrivait SOUS LE MÊME NOM que la
    photo réelle ; `os.path.exists(path)` passait alors à True pour de bon, et
    plus aucun build suivant ne retentait Openverse pour cette scène — même
    après le retour du réseau, un incident réseau transitoire dégradait le
    deck en PERMANENCE (repro : appel avec `fetch_to` en échec puis en succès,
    le 2e appel ne rappelait jamais `fetch_to`). Le repli est donc désormais
    écrit sous un nom distinct (`_repli`) : il ne bloque plus la case
    `os.path.exists(path)` qui protège la vraie photo, et chaque build retente
    Openverse tant qu'aucune vraie photo n'a été mise en cache."""
    if cadre is None:
        msg = f"cadre introuvable pour la scène '{scene}' — image non posée"
        print(f"  {msg}")
        _ANOMALIES_BUILD.append(msg)
        return
    left, top, width, height, geom = cadre
    aspect = Emu(width).inches / Emu(height).inches
    px_w = 960
    px_h = int(round(px_w / aspect))
    # Cache en .jpg, pas .png : le contenu est une PHOTO (network ou repli
    # procedural), et cover_crop_to_aspect()/generate_to() infèrent l'encodage
    # du seul suffixe du chemin passé. Une photo cachée en PNG (lossless) sur
    # ~1000px pèse 5 à 10× plus qu'un JPEG visuellement identique — c'était
    # la quasi-totalité des 26 Mo mesurés dans le .pptx exporté (2026-09-11).
    path = os.path.join(IMG_DIR, f"{scene}_{seed}_{px_w}x{px_h}.jpg")
    # Nom DISTINCT pour le repli procedural : il ne doit jamais faire passer
    # `os.path.exists(path)` (ci-dessus) a True a la place d'une vraie photo —
    # cf. docstring de la fonction pour le defaut que ce nom distinct ferme.
    path_repli = os.path.join(IMG_DIR, f"{scene}_{seed}_{px_w}x{px_h}_repli.jpg")
    path_a_poser = path
    if not _image_cache_valide(path):
        requete = _REQUETES_PHOTO.get(scene, scene)
        aspect_ratio = "wide" if aspect > 1.15 else "tall" if aspect < 0.85 else "square"
        brut = os.path.join(IMG_DIR, f"_brut_{scene}_{seed}.jpg")
        # Try restreint au seul appel réseau (constat R1, audit VSCode3
        # 2026-09-23) : une erreur d'import ou d'encodage ne doit plus être
        # rapportée « Openverse indisponible » — imports sortis en tête de
        # module, ré-encodage traité dans un second try au message distinct.
        try:
            stock_images.fetch_to(brut, requete, seed=seed, aspect_ratio=aspect_ratio,
                                   manifest_path=IMG_MANIFEST)
        except Exception as e:
            repli = _SCENE_REPLI.get(scene, scene)
            note = f" (scène '{scene}' inconnue du repli -> '{repli}')" if repli != scene else ""
            print(f"  Openverse indisponible pour '{scene}' ({e}) — repli sur nature_images{note}")
            try:
                nature_images.generate_to(path_repli, repli, px_w, px_h, seed=seed)
                path_a_poser = path_repli
            except Exception as e2:
                # Degrader, jamais planter : la slide sort sans photo et le
                # defaut remonte dans `problemes`, il ne disparait pas.
                msg = f"aucune image pour '{scene}' : Openverse KO ({e}) et repli KO ({e2})"
                print(f"  {msg}")
                _ANOMALIES_BUILD.append(msg)
                return
        else:
            try:
                cover_crop_to_aspect(brut, path, aspect)
                # cover_crop_to_aspect() sauve avec les défauts PIL (JPEG
                # qualité 75) : ré-encodage local à qualité 90 pour un rendu
                # plein cadre sur un deck client — le gain de poids vient de
                # PNG->JPEG, pas d'une compression agressive en plus.
                _PILImage.open(path).convert("RGB").save(path, quality=90, optimize=True)
                # Constat S1 : contenu tiers Openverse non validé avant usage
                # dans un livrable client — valider le fichier téléchargé
                # (format image décodable, dimensions bornées) avant de le
                # poser. Un fichier retenu invalide ne doit pas rester en
                # cache pour le build suivant (constat R2).
                if not _image_cache_valide(path):
                    raise ValueError(f"image Openverse invalide pour '{scene}' ({path})")
                print(f"  photo réelle posée pour '{scene}' ({requete!r}, via Openverse CC0)")
                path_a_poser = path
            except Exception as e:
                if os.path.exists(path):
                    os.remove(path)
                repli = _SCENE_REPLI.get(scene, scene)
                note = f" (scène '{scene}' inconnue du repli -> '{repli}')" if repli != scene else ""
                print(f"  image Openverse illisible pour '{scene}' ({e}) — repli sur nature_images{note}")
                try:
                    nature_images.generate_to(path_repli, repli, px_w, px_h, seed=seed)
                    path_a_poser = path_repli
                except Exception as e2:
                    msg = f"aucune image pour '{scene}' : encodage/validation KO ({e}) et repli KO ({e2})"
                    print(f"  {msg}")
                    _ANOMALIES_BUILD.append(msg)
                    return
    place_image_in_frame(slide, path_a_poser, left, top, width, height, geom=geom)


def slide_chapitre(prs, numero, titre, couverture, color, scene, seed=0):
    """Slide d'intercalaire de chapitre — vrai layout dédié du template
    (« 50 - Chapitre [1] »), repris tel qu'utilisé dans le REX
    "⛱️ L'Été de l'IA" (VSCode1) : cadre photo teardrop rempli (pas laissé
    vide), numéro à 17pt (pas la taille par défaut d'un texte de titre — un
    premier essai à 28pt débordait du petit encart sur le badge logo voisin,
    trouvé au rendu, cf. mémoire de session). Couleur de chapitre appliquée
    au numéro et au titre — le REX source ne le faisait pas, ajouté ici pour
    rester cohérent avec le code couleur déjà en place sur tout le deck."""
    layout = prs.slide_masters[0].slide_layouts[LAYOUT_CHAPITRE]
    s = prs.slides.add_slide(layout)
    phs = {ph.placeholder_format.idx: ph for ph in s.placeholders}

    phs[0].text_frame.text = titre
    p2 = phs[0].text_frame.add_paragraph()
    p2.text = couverture
    for r in p2.runs:
        r.font.size = Pt(D.TYPE["small"])
        r.font.italic = True
        r.font.color.rgb = _rgb(MUTED)
    for p in phs[0].text_frame.paragraphs[:1]:
        for r in p.runs:
            r.font.color.rgb = _rgb(color)

    tf1 = phs[1].text_frame
    tf1.text = numero
    # Marges par défaut (~0.1in/côté) mangent la largeur du minuscule encart
    # (0.55in) et forcent "01" à passer à la ligne — invisible tant qu'on ne
    # zéroute pas les marges comme le fait l'exemple qui fonctionne (REX V3).
    tf1.margin_left = tf1.margin_right = tf1.margin_top = tf1.margin_bottom = 0
    tf1.vertical_anchor = MSO_ANCHOR.MIDDLE
    for p in tf1.paragraphs:
        p.alignment = PP_ALIGN.CENTER
        _sans_puce(p)
        for r in p.runs:
            r.font.size = Pt(17)
            r.font.color.rgb = _rgb(color)

    cadre = _find_frame_by_geom(s.slide_layout.shapes, "teardrop")
    for pb in frame_obstructions(s, *cadre[:4]) if cadre else []:
        print(f"  [obstruction] chapitre {numero}:", pb["source"], pb["name"], pb["reason"])
    _remplir_cadre(s, cadre, scene, seed)
    return s


def dot_scale(slide, x, y, n, score, color, d=0.14, gap=0.06, empty_color=None):
    """Jauge à points 0..n (score plein en `color`, reste en `empty_color`) —
    pattern repris de la carte de recommandation valeur/complexité observée
    dans l'autre template analysé (analyse-template-alternatif.md §4)."""
    empty_color = empty_color or TRACK
    for i in range(n):
        fill = color if i < score else empty_color
        D.add_dot(slide, x + i * (d + gap), y, d, fill)


def col_x(i, n, w=CONTENT_W, x0=MARGIN, gap=GAP):
    col_w = (w - (n - 1) * gap) / n
    return x0 + i * (col_w + gap), col_w


def chip(slide, x, y, w, h, label, color, text_color="#ffffff", size=D.TYPE["tiny"]):
    """Wrapper de `D.add_chip` (extrait vers pptx_deck.py le 2026-09-11 ; garde
    ce nom pour ne pas toucher les ~12 sites d'appel du generateur, grep
    \\bchip\\( generate_deck.py hors ce commentaire).

    Garde D1 (arbitrage du 2026-09-10, ~1,9:1 sur blanc) : le cyan (ACCENT /
    ACCENT_PLEIN) ne porte JAMAIS de texte. Beaucoup d'appelants passent une
    `color` de palette (« un sur N en accent ») sans se soucier du texte par
    defaut blanc du chip — quand cette couleur vaut le cyan ET que l'appelant
    n'a pas deja choisi un texte lisible, l'aplat retombe sur NAVY : l'element
    distingue garde un aplat PLEIN (navy, pas cyan), le texte blanc reste
    lisible dessus. Un appelant qui a deja pose un `text_color` explicite
    (ex. NAVY sur un chip cyan sur panneau navy, slide gate) n'est pas
    touche : ce n'est pas le defaut corrige ici."""
    if str(color).lower() == str(ACCENT).lower() and str(text_color).lower() == "#ffffff":
        color = NAVY
    return D.add_chip(slide, x, y, w, h, label, color, text_color=text_color, size=size)


# --- Helpers du schéma « parcours de mission » (slide_offre_iap, v2.8) : pas de
# CONNECTOR/oval réutilisable ailleurs dans le générateur avant ce schéma, donc
# petits helpers dédiés plutôt qu'un détour par pptx_deck (déjà surchargé de
# add_rect/add_card génériques — ceux-ci sont spécifiques à ce diagramme).
def _oval(slide, x, y, w, h, fill=None, line=None, line_w=1.0):
    """Ellipse simple (nœuds « entrée/sortie » du schéma de parcours)."""
    shp = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x), Inches(y), Inches(w), Inches(h))
    try:
        shp.shadow.inherit = False
    except Exception:
        pass
    if fill is None:
        shp.fill.background()
    else:
        shp.fill.solid()
        shp.fill.fore_color.rgb = _rgb(fill)
    if line is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = _rgb(line)
        shp.line.width = Pt(line_w)
    shp.text_frame.paragraphs[0].text = ""
    return shp


def _pale(hexcolor, factor=0.1):
    """Teinte pâle d'une couleur PALETTE (mélange à `factor` avec du blanc) —
    fond de carte discret qui garde l'accent de couleur lisible sans l'écraser."""
    r, g, b = (int(hexcolor[i:i + 2], 16) for i in (1, 3, 5))
    mix = lambda c: round(c * factor + 255 * (1 - factor))
    return f"#{mix(r):02x}{mix(g):02x}{mix(b):02x}"


def _dashed_rect(slide, x, y, w, h, fill, line, line_w=1.0, radius=0.12):
    """Rectangle à bordure pointillée (« mécanisme additif » du schéma de parcours) —
    python-pptx n'expose le style de trait qu'en LineFormat.dash_style, pas via
    D.add_rect (qui ne prend pas ce paramètre)."""
    shp = D.add_rect(slide, x, y, w, h, fill=fill, line=line, line_w=line_w,
                      rounded=True, radius=radius)
    shp.line.dash_style = MSO_LINE_DASH_STYLE.DASH
    return shp


# ---- Helpers « refonte graphique v3 » (2026-09-04, exercice d'idéation sur 2
# decks OCTO réels — cf. gen_check_slide_synthese_v3_refonte.py pour la trace
# complète du système de design). Système : conteneur = contour seul, jamais
# un aplat plein ; étiquette courte = pilule pleine ; chevron = marqueur de
# séquence ; badge à cheval sur un bord plutôt que relié par une flèche ;
# emphase en ligne (mot-clé gras dans une phrase normale) plutôt qu'une
# phrase entière en gras/italique ; barre d'accent verticale ; bandeau de
# clôture citation (guillemet + point isolés, cyan).
QUOTE = "“"   # guillemet ouvrant décoratif (confirmé dans le cmap Outfit)
DOT = "•"     # point isolé de clôture (confirmé dans le cmap Outfit)


def _rich(slide, x, y, w, h, paragraphs, anchor=MSO_ANCHOR.TOP, wrap=True):
    """Zone de texte MULTI-RUNS par paragraphe : `paragraphs` = liste de
    (runs, para_opts) où runs = liste de (texte, run_opts). Nécessaire pour
    l'emphase EN LIGNE (mot-clé gras/coloré au milieu d'une phrase normale) —
    `D.add_text` ne pose qu'un seul run par paragraphe."""
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = wrap
    tf.vertical_anchor = anchor
    for m in ("margin_left", "margin_right", "margin_top", "margin_bottom"):
        setattr(tf, m, 0)
    for i, (runs, popts) in enumerate(paragraphs):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = popts.get("align", PP_ALIGN.LEFT)
        if "space_before" in popts:
            p.space_before = Pt(popts["space_before"])
        if "space_after" in popts:
            p.space_after = Pt(popts["space_after"])
        if "line_spacing" in popts:
            p.line_spacing = popts["line_spacing"]
        for texte, ropts in runs:
            r = p.add_run()
            r.text = texte
            r.font.size = Pt(ropts.get("size", 10))
            r.font.bold = ropts.get("bold", False)
            r.font.italic = ropts.get("italic", False)
            r.font.color.rgb = _rgb(ropts.get("color", NAVY))
    return box


def _split_emph(texte, emph):
    """Coupe `texte` en (avant, emph, après) — la sous-phrase `emph` doit
    exister MOT POUR MOT dans `texte` (lève si absente : garde-fou contre une
    emphase qui déviendrait du texte source)."""
    i = texte.index(emph)
    return texte[:i], emph, texte[i + len(emph):]


def _chevron_shape(slide, x, y, w, h, fill=WHITE, line=MUTED, line_w=1.25):
    """Silhouette « pilule + pointe » (encoche gauche, pointe droite) — le
    seul preset natif python-pptx qui rend cette silhouette SANS rotation
    (une rotation fausserait `verifier_geometrie`, qui mesure le cadre non
    pivoté — piège déjà documenté dans ce dépôt pour un groupe pivoté 180°)."""
    shp = slide.shapes.add_shape(MSO_SHAPE.CHEVRON, Inches(x), Inches(y), Inches(w), Inches(h))
    try:
        shp.shadow.inherit = False
    except Exception:
        pass
    if fill is None:
        shp.fill.background()
    else:
        shp.fill.solid()
        shp.fill.fore_color.rgb = _rgb(fill)
    if line is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = _rgb(line)
        shp.line.width = Pt(line_w)
    shp.text_frame.paragraphs[0].text = ""
    return shp


def _chevron_arrow(slide, x, y, w, h, color=MUTED, frac_w=0.72, frac_h=0.5):
    """Petite flèche de flux (chevron fin) centrée dans la cellule (x,y,w,h) —
    remplace le glyphe texte '→' entre 2 pilules constat/réponse."""
    cw, ch = w * frac_w, h * frac_h
    _chevron_shape(slide, x + (w - cw) / 2, y + (h - ch) / 2, cw, ch,
                   fill=WHITE, line=color, line_w=1.4)


def _badge(slide, cx, cy, d, color, symbol, filled=True, dashed=False, fill=None,
           text_color=None, size=12, bold=True):
    """Wrapper de `D.add_badge` (extrait vers pptx_deck.py le 2026-09-11 ; garde
    ce nom pour ne pas toucher les ~6 sites d'appel du generateur). WHITE
    (theme lt1 de CE gabarit) mesure a #FFFFFF, identique au litteral '#ffffff'
    dont add_badge se sert par defaut — repli confirme, pas suppose.

    Garde D1 (meme regle que `chip` ci-dessus) : un badge REMPLI (`filled`)
    dont la couleur vaut le cyan ET dont l'appelant n'a pas deja choisi un
    `text_color` retombe sur un aplat NAVY — pas de texte blanc sur cyan a
    ~1,9:1. Le badge CONTOUR (`filled=False`) n'est pas concerne : il n'a
    jamais de fond cyan plein, juste un trait."""
    if filled and str(color).lower() == str(ACCENT).lower() and text_color is None:
        color = NAVY
    return D.add_badge(slide, cx, cy, d, color, symbol, filled=filled, dashed=dashed,
                        fill=fill, text_color=text_color, size=size, bold=bold)


def _bandeau_cloture(slide, texte, bas_contenu, nom_slide, size=12):
    """Bandeau de clôture dimensionné par SON TEXTE et posé en bas de slide.

    Deux règles de dimensionnement coexistaient, dont une fausse. La variante
    « étirée » (`h = CONTENT_BOTTOM - y`) remplit tout le vide restant : quand
    le contenu est court, elle produit un pavé navy de plus d'un pouce de haut
    pour une phrase — constaté au rendu du 2026-09-10, et deux slides du même
    chapitre l'utilisaient encore juste à côté de deux slides corrigées.
    Ici la hauteur vient du texte, le blanc restant respire, et le
    chevauchement échoue AU BUILD plutôt qu'à la relecture.
    """
    h = _lignes(texte, CONTENT_W - 0.60, size) * (size * 1.2 / 72.0) + 0.34
    top = CONTENT_BOTTOM - h
    if top < bas_contenu:
        raise SystemExit(
            f"{nom_slide} : le bandeau de clôture chevauche le contenu "
            f"({bas_contenu - top:.3f}in de trop) — resserrer avant de régénérer."
        )
    _quote_banner(slide, MARGIN, top, CONTENT_W, h, texte, size=size)


def _quote_banner(slide, x, y, w, h, text, size=15.5):
    """Bandeau de clôture : fond navy plein (la phrase qu'on retient reste le
    SEUL aplat plein d'une slide en système « contour ») + guillemet décoratif
    cyan en coin + point isolé cyan après le dernier mot."""
    D.add_rect(slide, x, y, w, h, fill=NAVY, rounded=True, radius=0.10)
    D.add_text(slide, x + 0.14, y + 0.02, 0.4, min(0.4, h - 0.04), [
        (QUOTE, dict(size=24, bold=True, color=ACCENT)),
    ], anchor=MSO_ANCHOR.TOP)
    _rich(slide, x + 0.20, y, w - 0.40, h, [
        ([(text, dict(size=size, bold=True, color=WHITE)),
          ("  " + DOT, dict(size=size, bold=True, color=ACCENT))],
         dict(align=PP_ALIGN.CENTER)),
    ], anchor=MSO_ANCHOR.MIDDLE)


def _noeud_socle(slide, x, y, w, h, titre, sous_titre=None, oval=False):
    """Nœud « mouvement du socle » (toujours présent) du schéma de parcours —
    fill bleu-gris clair, bordure navy ; ellipse pour les nœuds d'entrée/sortie."""
    fill = "#dce6f5"
    if oval:
        _oval(slide, x, y, w, h, fill=fill, line=NAVY, line_w=1.0)
    else:
        D.add_rect(slide, x, y, w, h, fill=fill, line=NAVY, line_w=1.0, rounded=True, radius=0.14)
    lignes = [(titre, dict(size=7, bold=True, color=NAVY, align=PP_ALIGN.CENTER, line_spacing=1.0))]
    if sous_titre:
        lignes.append((sous_titre, dict(size=5.8, color=MUTED, align=PP_ALIGN.CENTER,
                                         italic=True, space_before=1, line_spacing=1.0)))
    D.add_text(slide, x + 0.04, y, w - 0.08, h, lignes, anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)


def _pilule_variante(slide, x, y, w, h, texte, size=6.2):
    """Pilule « variante conditionnée au contexte » (sable/or) du schéma de parcours.
    Si `h` est None, la hauteur est calculée à partir du texte (pilules « si contexte
    politique », plus longues que les pilules courtes « Contexte léger/politique ») —
    retourne toujours la hauteur effectivement utilisée."""
    pad = 0.03
    if h is None:
        lignes = _lignes(texte, w - 2 * pad, size)
        h = 2 * pad + lignes * (size * 1.15 / 72.0)
    D.add_rect(slide, x, y, w, h, fill="#E7E9EE", line=ENCRE, line_w=1.0,
               rounded=True, radius=0.35)
    D.add_text(slide, x + 0.05, y, w - 0.10, h, [
        (texte, dict(size=size, bold=True, color=ENCRE, align=PP_ALIGN.CENTER, line_spacing=1.05)),
    ], anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
    return h


def _note_mecanisme(slide, x, y, w, titre, corps, title_size=6.4, body_size=6.0, pad=0.04):
    """Encadré pointillé pâle = « mécanisme additif » (extension, checklist transverse)
    du schéma de parcours — hauteur calculée à partir du corps, jamais fixe (cf. défaut
    « panneau sur-étiré » du dépôt) ; retourne la hauteur effectivement utilisée."""
    lignes = _lignes(corps, w - 2 * pad, body_size)
    h = 2 * pad + (title_size * 1.1 / 72.0) + 0.02 + lignes * (body_size * 1.15 / 72.0)
    _dashed_rect(slide, x, y, w, h, fill="#F2F4F8", line=ENCRE, line_w=0.9, radius=0.10)
    D.add_text(slide, x + pad, y + pad * 0.6, w - 2 * pad, h - pad * 1.2, [
        (titre, dict(size=title_size, bold=True, color=ENCRE, line_spacing=1.05)),
        (corps, dict(size=body_size, color=MUTED, italic=True, space_before=2, line_spacing=1.15)),
    ])
    return h


def _fleche_h(slide, x, y, w, h, color=MUTED, size=10):
    """Flèche « → » centrée dans une cellule (vocabulaire de flux du schéma de
    parcours — même simplification texte que slide_iap_contexte_client)."""
    D.add_text(slide, x, y, w, h, [
        ("→", dict(size=size, bold=True, color=encre_de(color), align=PP_ALIGN.CENTER)),
    ], anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)


# --- Badge de série (v2.6, point ④) : les 4 slides « proposition de déploiement
# agentic chez le client » du chapitre IA (3 agents candidats + export
# markdown) portent le MÊME petit badge — signal visuel récurrent et discret qui
# les relie à la zone « déploiement agentic » du schéma d'architecture
# (slide_iap_contexte_client, chapitre 08). Renvoi par CHAPITRE, jamais par
# numéro de page (les numéros bougent). ENCRE = encre navy, la couleur du
# chapitre IA, la même que la zone du schéma.
BADGE_AGENTIC_W = 2.3


def badge_deploiement_agentic(slide):
    x = BORD_DROIT - BADGE_AGENTIC_W
    h = 0.42
    D.add_rect(slide, x, CONTENT_TOP, BADGE_AGENTIC_W, h, fill="#ffffff",
               line=ENCRE, line_w=1.0, rounded=True, radius=0.18)
    D.add_text(slide, x + 0.12, CONTENT_TOP, BADGE_AGENTIC_W - 0.24, h, [
        ("DÉPLOIEMENT AGENTIC CHEZ LE CLIENT",
         dict(size=6, bold=True, color=ENCRE, line_spacing=1.1)),
        ("cf. schéma d'architecture · chapitre Démarches",
         dict(size=6, italic=True, color=MUTED, space_before=1)),
    ], anchor=MSO_ANCHOR.MIDDLE)


# Le glyphe "⟲" (U+27F2) n'a pas de variante GRASSE dans la police du template
# (rendu LibreOffice = case vide/tofu dans un run bold) alors que sa variante
# normale s'affiche — même correctif que slide_trajectoire/slide_schema_*
# /slide_livrables_ppt : forcer bold=False pour ce SEUL caractère. Voir
# CLAUDE.md §docs/cadrage-ppt.
_GLYPHES_SANS_GRAS = ("⟲",)


def _header_cell(slide, x, y, w, h, label, size=7, color=MUTED, bold=True,
                 anchor=MSO_ANCHOR.TOP):
    """En-tête de colonne en un seul paragraphe multi-runs : chaque caractère de
    `_GLYPHES_SANS_GRAS` est posé en bold=False même si le libellé est en gras,
    pour éviter le tofu du "⟲" en fonte grasse (cf. _GLYPHES_SANS_GRAS)."""
    import re as _re
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    for m in ("margin_left", "margin_right", "margin_top", "margin_bottom"):
        setattr(tf, m, 0)
    p = tf.paragraphs[0]
    motif = "(" + "|".join(_re.escape(g) for g in _GLYPHES_SANS_GRAS) + ")"
    for part in _re.split(motif, label):
        if not part:
            continue
        r = p.add_run()
        r.text = part
        r.font.size = Pt(size)
        r.font.bold = bool(bold) and part not in _GLYPHES_SANS_GRAS
        r.font.color.rgb = _rgb(color)
    return box


def _lignes(texte, largeur_in, taille_pt):
    """Nombre de lignes estimé pour `texte` (helper de dimensionnement des
    panneaux à la hauteur de leur contenu — cf. « panneau sur-étiré »)."""
    return max(1, D.estimer_lignes(texte, largeur_in, taille_pt))


# ---------------------------------------------------------------- slide 1
def slide_cover(prs):
    layout = prs.slide_masters[0].slide_layouts[LAYOUT_COUVERTURE]
    s = prs.slides.add_slide(layout)
    phs = {ph.placeholder_format.idx: ph for ph in s.placeholders}
    phs[0].text_frame.text = "BMAD IAP"
    phs[1].text_frame.text = "Infra as a Product Transformation Pack — synthèse de cadrage"
    phs[2].text_frame.text = "OCTO Technology"
    # v2.8 (2026-09-02) : nouveau chapitre 01 « Exec summary » en ouverture du
    # deck (l'offre du pitch + sa synthèse) — tous les chapitres suivants
    # glissent de +1. (v2.6 : sous-chapitre « Exemples » supprimé (séparateur +
    # 3 slides illustratives, à la demande) ; nouvelles slides « activités
    # humaines avec/sans l'outil » (Démarche) et « architecture IAP en contexte
    # client » (ouvre l'Outillage IAP) ; badge de série « déploiement agentic
    # chez le client » sur les 4 slides de proposition agentic (chapitre IA).
    # v2.5 : restructuration 8 chapitres sur le fil rouge SCALE — fusion
    # trajectoire/bout-en-bout, executive summary réancré, chapitre Outillage
    # IAP. v2.4 : fil humain de la trajectoire.)
    phs[3].text_frame.text = f"{VERSION_DECK} · {DATE_VERSION_DECK}"
    # Bandeau de métadonnées (statut/langue/confidentialité/sources) retiré sur
    # demande — la couverture ne garde que titre, sous-titre, entité et version.
    return s


# ---------------------------------------------------------------- slide 2
# Réancré (v2.5, chantier ②) sur le fil rouge narratif SCALE
# (docs/Import/notes-extraction-scale.md) : 4 blocs POURQUOI → QUOI → COMMENT →
# RÉSULTAT, chacun une claim d'une ligne + le renvoi aux chapitres — pattern 7
# du catalogue deck-design-library (« rangée de cartes sur bandeau, une en
# accent ») : le RÉSULTAT (la preuve, ce que le sponsor achète in fine) est la
# seule carte en fill navy plein.
def slide_executive_summary(prs):
    # v2.12 : seul appel content_slide() de tout le deck SANS color= explicite
    # (les ~30 autres en passent tous un) -> kicker retombait sur ACCENT (cyan
    # generique) au lieu du NAVY du chapitre 01 Exec summary, dont cette slide
    # ouvre le fil (a l'epoque slide_pitch_iap et slide_demarche_avec_sans_agentic,
    # juste apres, portaient deja color=NAVY ; toutes deux supprimees en v2.34 --
    # c'est desormais slide_synthese_pourquoi_quoi_comment qui suit, en NAVY elle
    # aussi, donc la correction tient) -- visible dans les DEUX rendus (LibreOffice
    # ET PowerPoint), manquee lors d'une premiere relecture concentree sur le
    # contenu (bloc OFFRE) plutot que sur la couleur du kicker.
    s = content_slide(prs, "Executive summary",
                       "Du pourquoi à la preuve : une transformation cadrée de bout en bout",
                       color=NAVY)

    headline_h = 0.62
    D.add_text(s, MARGIN, CONTENT_TOP, CONTENT_W, headline_h, [
        ("Transformer l'infrastructure en plateforme opérée comme un produit, ET traiter "
         "structurellement le gaspillage qui l'en empêche — le deck suit le fil : l'offre, "
         "pourquoi, quoi, comment, la preuve.",
         dict(size=D.TYPE["small"], color=NAVY, italic=True, line_spacing=1.3)),
    ])

    # v2.10 : bloc OFFRE ajouté en tête de rangée (arbitrage utilisateur) — le
    # sommaire ne référençait aucun chapitre avant le bloc POURQUOI alors que le
    # chapitre 01 · Exec summary restait invisible ici. Accent (fond plein) comme
    # RÉSULTAT : les deux bornent la rangée (l'offre ouvre, la preuve ferme).
    # v2.34 : le bloc reprenait au mot près les sous-titres des deux slides
    # supprimées — il annonçait donc un contenu qui n'existe plus. Réaligné sur
    # la slide qui reste (la démarche infra en quatre temps).
    items = [
        ("OFFRE", NAVY, "Une démarche infra en quatre temps, sans prérequis d'IA.",
         "Ce qu'on fait dans l'organisation et sur la plateforme à chaque temps ; "
         "l'agentic accélère le consultant, en option chez le client.",
         "Exec summary"),
        ("POURQUOI", ENCRE, "L'infra subie coûte de plus en plus cher.",
         "Trois déclencheurs, un terrain pas comme un autre, ce qui se joue pour la DSI "
         "si rien ne change, des douleurs mesurables plutôt que des plaintes.",
         "Contexte → Douleur"),
        ("QUOI", ENCRE, "Ce que le moment ouvre, et ce qu'on livre pour le saisir.",
         "Des leviers déjà instruits, la thèse infra-as-a-product, la méthode scorée et "
         "l'IA sous gate — jamais la réponse à un problème d'abord organisationnel.",
         "Opportunités → Offre"),
        ("COMMENT", ENCRE, "Trois temps et une boucle, personnes comprises.",
         "Démarche ①②③⟲ avec son fil humain de bout en bout, l'outillage IAP au service "
         "de la démarche — jamais l'inverse.",
         "Démarches"),
        ("RÉSULTAT", NAVY, "Les jalons, et le signal minimal pour savoir si ça marche.",
         "Indicateurs de suivi dès le T0, même instrument à la réévaluation — la preuve, "
         "pas une opinion.",
         "Next steps"),
    ]
    n = len(items)
    pad = 0.16
    _, cw = col_x(0, n)
    usable = cw - 2 * pad
    desc_size = 8
    line_h = desc_size * 1.3 / 72.0
    claim_h = max(_lignes(c, usable, 9) for _, _, c, _, _ in items) * (9 * 1.2 / 72.0) + 0.06
    desc_h = max(_lignes(d, usable, desc_size) for _, _, _, d, _ in items) * line_h + 0.06
    # étages : label (0.24) + claim + desc + renvoi chapitres (0.26) + respirations
    card_h = 0.14 + 0.24 + claim_h + 0.10 + desc_h + 0.14 + 0.26 + 0.14
    top0 = CONTENT_TOP + headline_h + 0.30
    # bandeau de fond commun (pattern 7) : regroupe les 5 blocs en un seul
    # « bloc de lecture » — le fil se lit d'un trait, flèches dans les inter-colonnes.
    D.add_rect(s, MARGIN - 0.08, top0 - 0.16, CONTENT_W + 0.16, card_h + 0.32,
               fill=TRACK, rounded=True, radius=0.06)
    for i, (etape, color, claim, desc, renvoi) in enumerate(items):
        x, w = col_x(i, n)
        accent = etape in ("OFFRE", "RÉSULTAT")   # bornent la rangée : l'offre ouvre, la preuve ferme
        if accent:
            D.add_rect(s, x, top0, w, card_h, fill=NAVY, rounded=True, radius=0.08)
        else:
            D.add_rect(s, x, top0, w, card_h, fill="#ffffff", line=LINE, line_w=0.75,
                       rounded=True, radius=0.08)
        D.add_text(s, x + pad, top0 + 0.14, w - 2 * pad, 0.24, [
            (etape, dict(size=8, bold=True, color="#8fd6db" if accent else color)),
        ])
        D.add_text(s, x + pad, top0 + 0.38, w - 2 * pad, claim_h, [
            (claim, dict(size=9, bold=True, color="#ffffff" if accent else NAVY,
                         line_spacing=1.2)),
        ])
        D.add_text(s, x + pad, top0 + 0.38 + claim_h + 0.10, w - 2 * pad, desc_h, [
            (desc, dict(size=desc_size, color="#c7cbe0" if accent else MUTED,
                        line_spacing=1.3)),
        ])
        D.add_text(s, x + pad, top0 + card_h - 0.38, w - 2 * pad, 0.26, [
            # Deux branches valant toutes deux navy depuis la bascule : le
            # conditionnel se lisait comme une emphase et ne rendait rien.
            (renvoi, dict(size=7.5, bold=True,
                          color="#8fd6db" if accent else ENCRE)),
        ], anchor=MSO_ANCHOR.BOTTOM)
        if i < n - 1:   # le fil : flèche dans l'inter-colonne
            D.add_text(s, x + w - 0.02, top0 + card_h / 2 - 0.12, GAP + 0.04, 0.24, [
                ("→", dict(size=11, bold=True, color=MUTED, align=PP_ALIGN.CENTER)),
            ], anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
    return s


# ---------------------------------------------------------------- chapitre 07 (v2.9)
def slide_offre_iap(prs):
    """DÉPLACÉE en v2.9 (arbitrage utilisateur) du chapitre 01 · Exec summary vers
    le chapitre Démarche, juste avant slide_schema_fonctionnement : le
    parcours de mission détaillé est un objet de COMMENT, pas d'ouverture — le
    sommaire du deck reste slide_executive_summary. Contenu inchangé ; seuls le
    kicker et la couleur suivent le chapitre d'accueil (ENCRE — la glose
    « or » a survecu au remplacement de D.PALETTE[3], corrigee le 2026-09-10).

    Nouveau (v2.8) — reprend la slide 2 du pitch source (chapô + citation-thèse,
    VERBATIM — document source, ne pas reformuler) et son schéma du parcours de
    mission, redessiné EN NATIF (pas une insertion de l'image source) sur ses 3
    registres : mouvements du socle (toujours présents, bleu-gris), variantes
    conditionnées au contexte (sable/or), mécanismes additifs (encadrés pointillés
    pâles). Nœud Discovery gaspillages renommé « 8 familles » (2026-09-18, cf.
    docstring de module) — seul écart volontaire à la fidélité verbatim du
    schéma, pour ne plus afficher deux chiffres différents de la même notion
    dans le même deck."""
    s = content_slide(prs, "Démarche",
                       "Accompagnement Infra as a Product : transformer une fonction infra en produit interne",
                       color=ENCRE)

    chapo = ("L'offre proposée est une méthodologie d'accompagnement pour transformer « une "
             "fonction infra ou une plateforme interne » en un véritable produit interne : un "
             "service pensé pour ses utilisateurs, avec un parcours, une proposition de valeur "
             "et des indicateurs de pilotage, plutôt qu'un centre de coûts ou un guichet de "
             "tickets. Le détail de chaque étape ci-dessous se retrouve dans la trajectoire en "
             "temps et boucle, et dans le schéma de fonctionnement qui suit — trois lectures "
             "du même parcours, pas trois parcours différents.")
    chapo_h = _lignes(chapo, CONTENT_W, 8.5) * (8.5 * 1.2 / 72.0) + 0.05
    D.add_text(s, MARGIN, CONTENT_TOP, CONTENT_W, chapo_h, [
        (chapo, dict(size=8.5, color=NAVY, italic=True, line_spacing=1.2)),
    ])
    # (budget vertical serré — cf. contrainte de place du brief : chaque gap
    # ci-dessous a été resserré après un premier rendu réel qui montrait la
    # légende partiellement recouverte par le bandeau de citation, empiétement
    # que `verifier_geometrie` ne peut pas voir — seul le rendu le révèle.)

    citation = ("« Réussir une transformation Infra as a Product, ce n'est pas \"mettre des PO "
                "dans l'infra\". C'est concevoir, opérer et faire adopter une plateforme interne "
                "comme un produit, en équilibrant delivery, robustesse du RUN et valeur perçue "
                "par les utilisateurs internes. »")
    cit_pad = 0.10
    cit_usable = CONTENT_W - 2 * cit_pad
    cit_lines = _lignes(citation, cit_usable, 8.5)
    citation_h = cit_pad + (7 * 1.1 / 72.0) + 0.04 + cit_lines * (8.5 * 1.2 / 72.0) + cit_pad

    grid_n = 5
    row_h = 0.38
    schema_top = CONTENT_TOP + chapo_h + 0.06

    # --- Bande du haut : 2 mécanismes additifs (gauche/droite) + variantes (centre) ---
    x0n, w0n = col_x(0, grid_n)
    note_l_w = 2.55
    h_note_l = _note_mecanisme(s, x0n, schema_top, note_l_w, "EXTENSION POSSIBLE",
                                "Reconstitution d'incident avant Cadrage, si crise déclencheuse.")
    note_r_w = 2.85
    note_r_x = BORD_DROIT - note_r_w
    h_note_r = _note_mecanisme(s, note_r_x, schema_top, note_r_w, "EXTENSION POSSIBLE",
                                "Tri contraintes / habitudes entre Diagnostic et Segmentation, "
                                "si sites hétérogènes.")

    x1, w1 = col_x(1, grid_n)
    x2, w2 = col_x(2, grid_n)
    v_cx = (x1 + w1 + x2) / 2.0
    v_w = 1.35
    v_x = v_cx - v_w / 2.0
    D.add_text(s, v_x - 0.25, schema_top, v_w + 0.5, 0.14, [
        ("signal de contexte détecté ?", dict(size=6, italic=True, color=MUTED, align=PP_ALIGN.CENTER)),
    ], anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
    pill_h = 0.17
    pill1_top = schema_top + 0.12
    pill2_top = pill1_top + pill_h + 0.02
    _pilule_variante(s, v_x, pill1_top, v_w, pill_h, "Contexte léger")
    _pilule_variante(s, v_x, pill2_top, v_w, pill_h, "Contexte politique")
    variantes_bottom = pill2_top + pill_h

    band_a_bottom = max(schema_top + h_note_l, schema_top + h_note_r, variantes_bottom)

    # --- Rangée 1 : mouvements du socle ---
    row1_top = band_a_bottom + 0.14
    D.add_text(s, x0n + w0n * 0.15, band_a_bottom + 0.04, 0.5, 0.14, [
        ("↓", dict(size=8, bold=True, color=ENCRE, align=PP_ALIGN.CENTER)),
    ], anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
    x3, w3 = col_x(3, grid_n)
    D.add_text(s, x3 + w3 * 0.65, band_a_bottom + 0.04, 0.5, 0.14, [
        ("↓", dict(size=8, bold=True, color=ENCRE, align=PP_ALIGN.CENTER)),
    ], anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)

    socle_row1 = [
        ("Premier contact", None, True),
        ("Cadrage", "note de cadrage", False),
        ("Diagnostic", "base factuelle partagée", False),
        ("Discovery gaspillages", "8 familles", False),
        ("Segmentation / Product Discovery", None, False),
    ]
    for i, (titre, sous, oval) in enumerate(socle_row1):
        x, w = col_x(i, grid_n)
        _noeud_socle(s, x, row1_top, w, row_h, titre, sous, oval=oval)
        if i < grid_n - 1:
            _fleche_h(s, x + w, row1_top, GAP, row_h)
    row1_bottom = row1_top + row_h

    # --- + Contradictions structurelles (si contexte politique), sous Discovery gaspillages ---
    h_cs = _pilule_variante(s, x3, row1_bottom + 0.05, w3, None,
                             "+ Contradictions structurelles (si contexte politique)", size=6.0)
    cs_bottom = row1_bottom + 0.05 + h_cs

    # --- Connecteur en Z : fin rangée 1 (col 5) -> début rangée 2 (col 1) ---
    x4, w4 = col_x(grid_n - 1, grid_n)
    x0, w0 = col_x(0, grid_n)
    cx4, cx0 = x4 + w4 / 2.0, x0 + w0 / 2.0
    y_elbow = cs_bottom + 0.06
    row2_top = y_elbow + 0.10
    D.add_rect(s, cx4 - 0.01, row1_bottom, 0.02, y_elbow - row1_bottom, fill=LINE)
    D.add_rect(s, cx0 - 0.01, y_elbow, cx4 - cx0 + 0.02, 0.02, fill=LINE)
    D.add_rect(s, cx0 - 0.01, y_elbow, 0.02, row2_top - y_elbow, fill=LINE)
    D.add_text(s, cx0 - 0.11, y_elbow - 0.01, 0.22, row2_top - y_elbow + 0.02, [
        ("▾", dict(size=6, bold=True, color=MUTED, align=PP_ALIGN.CENTER)),
    ], anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)

    # --- Rangée 2 : mouvements du socle (suite, « boustrophédon ») ---
    socle_row2 = [
        ("Product Definition", "fiche produit cible", False),
        ("Operating Model", "responsabilités + mesure", False),
        ("Adoption / Pilote", "bilan avant / après", False),
        ("Mission close", None, True),
        ("Retour d'expérience", "vers la bibliothèque partagée", False),
    ]
    for i, (titre, sous, oval) in enumerate(socle_row2):
        x, w = col_x(i, grid_n)
        _noeud_socle(s, x, row2_top, w, row_h, titre, sous, oval=oval)
        if i < grid_n - 1:
            _fleche_h(s, x + w, row2_top, GAP, row_h)
    row2_bottom = row2_top + row_h

    # --- + Dispositif de revue (si contexte politique), sous Adoption / Pilote ---
    x2b, w2b = col_x(2, grid_n)
    h_dr = _pilule_variante(s, x2b, row2_bottom + 0.05, w2b, None,
                             "+ Dispositif de revue (si contexte politique)", size=6.0)
    dr_bottom = row2_bottom + 0.05 + h_dr

    # --- Checklist gouvernance IA (mécanisme transverse, pleine largeur) ---
    checklist_top = dr_bottom + 0.05
    h_checklist = _note_mecanisme(s, MARGIN, checklist_top, CONTENT_W,
                                   "CHECKLIST GOUVERNANCE IA — TRANSVERSE",
                                   "Indépendante des mouvements, mobilisable dès qu'un usage IA "
                                   "est identifié — à tout moment de la mission.")
    checklist_bottom = checklist_top + h_checklist

    # --- Légende (3 registres) ---
    legend_top = checklist_bottom + 0.04
    legend = [
        ("#dce6f5", NAVY, False, "mouvement du socle (toujours présent)"),
        ("#E7E9EE", ENCRE, False, "variante ou section conditionnée au contexte"),
        ("#F2F4F8", ENCRE, True, "mécanisme additif (extension, checklist transverse)"),
    ]
    lx = MARGIN
    sw = 0.14
    for fill, line, dashed, label in legend:
        if dashed:
            _dashed_rect(s, lx, legend_top, sw, sw, fill=fill, line=line, line_w=0.9, radius=0.3)
        else:
            D.add_rect(s, lx, legend_top, sw, sw, fill=fill, line=line, line_w=1.0, rounded=True, radius=0.3)
        tw = 2.55
        D.add_text(s, lx + sw + 0.06, legend_top - 0.02, tw, sw + 0.05, [
            (label, dict(size=6.3, color=MUTED)),
        ], anchor=MSO_ANCHOR.MIDDLE)
        lx += sw + 0.06 + tw + 0.12

    # --- Citation-thèse (verbatim), bandeau bas ---
    cit_top = CONTENT_BOTTOM - citation_h
    D.add_rect(s, MARGIN, cit_top, CONTENT_W, citation_h, fill=NAVY, rounded=True, radius=0.08)
    D.add_rect(s, MARGIN, cit_top, 0.07, citation_h, fill=ACCENT, rounded=True, radius=0.5)
    D.add_text(s, MARGIN + 0.24, cit_top + cit_pad * 0.5, CONTENT_W - 0.44, citation_h - cit_pad, [
        ("LA THÈSE", dict(size=7, bold=True, color="#8fd6db")),
        (citation, dict(size=8.5, bold=True, color="#ffffff", space_before=3, line_spacing=1.2)),
    ])
    return s


# --- Pictogrammes de la v2.9 : vocabulaire de SILHOUETTES (pas de glyphes
# exotiques, qui rendent en tofu dans la police du template — cf.
# _GLYPHES_SANS_GRAS). Deux formes, une par FACE de l'agentic :
#   "engrenage" (GEAR_6)        = le module qui outille LE CONSULTANT ;
#   "deploiement" (PENTAGON)    = l'agentic DÉPLOYÉ CHEZ LE CLIENT.
# C'est la SILHOUETTE, jamais la couleur, qui les distingue (la charte du
# 2026-09-10 interdit à la couleur de porter le sens) : un sponsor qui lit deux
# fois « agentic » sans les distinguer croit qu'on lui vend la même chose deux
# fois, ce qui rendrait la slide fausse — condition posée en table ronde.
# v2.34 (2026-09-11) : la 3e forme, "alerte" (ovale + « ! » = la douleur du
# client), est retirée avec son seul appelant (slide_pitch_iap, supprimée) —
# une branche sans appelant n'est pas une réserve, c'est du code mort.
# Seul appelant restant : slide_synthese_pourquoi_quoi_comment.
def _picto(slide, kind, x, y, d, color):
    forme = {"engrenage": MSO_SHAPE.GEAR_6, "deploiement": MSO_SHAPE.PENTAGON}[kind]
    shp = slide.shapes.add_shape(forme, Inches(x), Inches(y), Inches(d), Inches(d))
    try:
        shp.shadow.inherit = False
    except Exception:
        pass
    shp.fill.solid()
    shp.fill.fore_color.rgb = _rgb(color)
    shp.line.fill.background()
    shp.text_frame.paragraphs[0].text = ""


# v2.32 (2026-09-04, refonte graphique — 3e passage sur cette slide, cf.
# historique ci-dessus des 2 rejets précédents) : corps entièrement redessiné
# selon le système de design "contour" (cf. les helpers _rich/_chevron_shape/
# _badge/_quote_banner ci-dessus) après étude de 3 decks OCTO réels fournis en
# référence par l'utilisateur.
#
# v2.34 (2026-09-11, demande utilisateur) : REFONDUE une 4e fois, et c'est
# désormais la seule slide « démarche » du chapitre 01. Deux demandes dans le
# même retour : « exec summary trop lourd, max 3 slides, plus synthétique » et
# « manque une démarche centrée sur les spécificités de l'infra sans forcément
# avec IA — que propose-t-on sans IA ». Conséquences ici :
#   - le CORPS de la slide est la démarche infra, en deux registres par temps
#     (ORGANISATION / INFRA). Le volet INFRA n'est plus une note « TECH : » en
#     6 mots sous la description : il porte les verbes de `slide_fil_technique`
#     (cartographier, décommissionner & observer, standardiser & outiller,
#     mesurer & réengager), à même poids de lecture que l'organisationnel ;
#   - l'AGENTIC descend d'un cran : plus de rangée à poids égal qui laisserait
#     croire qu'on choisit entre « avec » et « sans », mais une bande basse en
#     contour gris, 7pt, sous la frise — les deux faces (module du consultant /
#     agents déployés chez le client) restent distinguées par leurs deux
#     SILHOUETTES `_picto`, condition posée en table ronde ;
#   - la clôture AFFIRME que rien de tout ça ne requiert l'IA. C'était implicite
#     dans les 5 slides précédentes, donc invisible pour un client qui dit
#     « pas d'IA chez moi ».
# Le terrain (RUN permanent, infra transverse, guichet sursollicité) est rappelé
# en tête pour que la slide reste AUTOPORTANTE — consigne utilisateur du
# 2026-09-03 : « si je ne lis QUE cette slide, je comprends sans les autres ».
# Le NOM de la fonction est conservé malgré la refonte : les trois scripts
# autonomes du dossier (gen_check_slide_synthese*.py) l'importent.
def slide_synthese_pourquoi_quoi_comment(prs):
    s = content_slide(prs, "Exec summary",
                       "Reprendre la main sur l'infra en quatre temps — organisation "
                       "et plateforme, sans prérequis d'IA",
                       color=NAVY)

    marge_g = 0.38
    bord_d = 9.2
    bas_max = 5.58
    largeur = bord_d - marge_g
    bord_d_haut = 10.0 - marge_g
    largeur_haut = bord_d_haut - marge_g
    ecart = 0.10

    debut = 0.85

    # --- Le terrain, d'abord : ce que la démarche a en face d'elle. Repris mot
    # pour mot des trois slides du chapitre Spécificités de l'infra (RUN comme
    # régime permanent, transversalité sans propriétaire, guichet sursollicité)
    # — pas une généralité réécrite ici, sinon les deux chapitres divergent.
    contraintes = [
        "Un RUN qui ne s'arrête jamais et puise dans les experts du BUILD.",
        "Une infra transverse que personne ne porte en propre.",
        "Un guichet sursollicité, sans self-service.",
    ]

    # (symbole, titre, durée, optionnel, (verbe orga, suite), (verbe infra, suite), livrable)
    # Les verbes INFRA sont ceux de `slide_fil_technique` (chapitre Démarche) :
    # deux slides du même deck qui nommeraient différemment le même geste se
    # liraient comme deux démarches.
    phases = [
        ("①", "Assessment flash", "1–2 sem.", False,
         ("Diagnostiquer", " et restituer avec les parties prenantes."),
         ("Cartographier", " la dette, les risques et les licences en tension."),
         "Deck exécutif de restitution."),
        ("+", "Constitution du TOM — optionnel", "3–4 sem.", True,
         ("Formaliser", " le Target Operating Model : rôles et gouvernance."),
         ("Poser", " le référentiel de standards et d'outillage à tenir."),
         "TOM et roadmap (hors ①②③⟲)."),
        ("②", "Premier déploiement", "4–5 sem.", False,
         ("Embarquer", " des équipes pilotes volontaires et prouver la valeur."),
         ("Décommissionner", " ce qui peut l'être, observer ce qui reste."),
         "Évaluation du déploiement pilote."),
        ("③", "Implémentation itérative", "→ T+6-12 mois", False,
         ("Généraliser", " équipe par équipe, en passant de coach à délégué."),
         ("Standardiser", " et outiller : CI/CD et infra as code par défaut."),
         "Deck de comité de pilotage."),
        ("⟲", "Boucle de réévaluation", "T+6-12 mois", False,
         ("Rejouer", " le diagnostic au même instrument qu'à T0."),
         ("Mesurer", " la dette technique et les KPI d'infra."),
         "Deck de bilan et de ré-évaluation."),
    ]

    # --- L'agentic, au second plan : contour gris, 7pt, sous la frise. Les deux
    # faces gardent leurs SILHOUETTES (`_picto`) — un sponsor qui lit deux fois
    # « agentic » sans les distinguer croit qu'on lui vend la même chose deux
    # fois, ce qui rendrait la slide fausse (condition posée en table ronde).
    agentic = [
        ("engrenage", "CÔTÉ CONSULTANT — LE MODULE BMAD IAP",
         "Il outille chaque temps sur notre poste et sort les livrables plus vite — "
         "rien ne s'installe chez le client."),
        ("deploiement", "CHEZ LE CLIENT — UNE OPTION, PAS UN PRÉREQUIS",
         "Déployer des agents (triage, FinOps, documentaire) reste une décision "
         "distincte, sous gate IA."),
    ]
    punch_txt = ("Aucun de ces temps ne requiert l'IA : l'agentic accélère, il ne remplace "
                 "ni la démarche ni le consultant.")

    n = len(phases)
    badge_d = 0.40
    overlap = 0.05
    chev_w_frac = 0.94
    chev_pad = 0.045
    chip_h = 0.20
    chip_sz = 7.5
    titre_sz = 8
    lbl_sz = 6.5
    corps_sz = 8
    livr_sz = 7.5
    lbl_h = 0.13

    # ---- 1) Hauteurs, toutes dérivées du CONTENU (jamais d'un budget deviné :
    # le piège récurrent de ce deck est le panneau étiré au reste de la page).
    ent_h = 0.14
    _, wpill = col_x(0, len(contraintes), w=largeur_haut, x0=marge_g, gap=0.14)
    pill_pad = 0.07
    pills_h = max(_lignes(c, wpill - 2 * 0.14, corps_sz)
                  for c in contraintes) * (corps_sz * 1.25 / 72.0) + 2 * pill_pad

    _, wcol = col_x(0, n, w=largeur_haut, x0=marge_g, gap=ecart)
    tw = wcol - 0.10
    chev_tw = wcol * chev_w_frac - 2 * chev_pad
    titre_h = max(_lignes(p[1], chev_tw, titre_sz)
                  for p in phases) * (titre_sz * 1.1 / 72.0) + 2 * chev_pad
    orga_h = max(_lignes(p[4][0] + p[4][1], tw, corps_sz)
                 for p in phases) * (corps_sz * 1.2 / 72.0) + 0.03
    infra_h = max(_lignes(p[5][0] + p[5][1], tw, corps_sz)
                  for p in phases) * (corps_sz * 1.2 / 72.0) + 0.03
    livr_h = max(_lignes("Livrable : " + p[6], tw, livr_sz)
                 for p in phases) * (livr_sz * 1.2 / 72.0) + 0.03
    card_h = (0.02 + badge_d - overlap + titre_h + 0.06 + chip_h + 0.10 + lbl_h
              + orga_h + 0.08 + lbl_h + infra_h + 0.07 + 0.06 + livr_h + 0.09)

    # Les deux encarts agentiques s'alignent sur la frise (bord droit commun à
    # 9.62in), pas sur `largeur` : seul le bandeau de clôture doit rentrer à
    # 9.2in, parce que LUI descend au niveau du badge de pagination du gabarit
    # (9.25-9.80 x 5.08-5.34). Aligner les trois sur le plus contraint laissait
    # un décrochage de 0,42in visible au rendu entre la frise et ce qui suit.
    ag_gap = 0.18
    ag_w = (largeur_haut - ag_gap) / 2
    picto_d = 0.20
    ag_pad = 0.09
    ag_txt_off = 0.12 + picto_d + 0.10
    ag_tw = ag_w - ag_txt_off - 0.12
    ag_sz = 7
    ag_label_h = max(_lignes(lb, ag_tw, ag_sz) for _, lb, _ in agentic) * (ag_sz * 1.15 / 72.0)
    ag_texte_h = max(_lignes(t, ag_tw, ag_sz) for _, _, t in agentic) * (ag_sz * 1.25 / 72.0)
    agents_h = ag_pad + ag_label_h + 3 / 72.0 + ag_texte_h + ag_pad

    punch_h = _lignes(punch_txt, largeur - 0.40, 12) * (12 * 1.2 / 72.0) + 0.1

    # ---- 2) Respiration : le mou restant est reversé dans les 3 inter-blocs,
    # plafonné — jamais dans la hauteur d'un panneau (qui se mettrait à flotter
    # autour d'un texte court).
    blocs_h = ent_h + pills_h + card_h + agents_h + punch_h
    gaps_min = (0.14, 0.10, 0.06)
    reste = bas_max - debut - blocs_h - sum(gaps_min)
    resp = max(0.0, min(0.10, reste / 3.0))
    g1, g2, g3 = (g + resp for g in gaps_min)

    # ---- 3) Ordonnées absolues, calculées UNE FOIS (une formule dupliquée dans
    # la boucle a déjà divergé en silence sur cette slide, cf. v2.27).
    pills_top = debut + ent_h
    top0 = pills_top + pills_h + g1
    badge_cy = top0 + badge_d / 2
    chev_top = top0 + badge_d - overlap
    chip_y = chev_top + titre_h + 0.06
    lbl_orga_y = chip_y + chip_h + 0.10
    orga_y = lbl_orga_y + lbl_h
    lbl_infra_y = orga_y + orga_h + 0.08
    infra_y = lbl_infra_y + lbl_h
    sep_y = infra_y + infra_h + 0.07
    livr_y = sep_y + 0.06
    card_top = top0 - 0.02
    agents_top = card_top + card_h + g2
    punch_top = agents_top + agents_h + g3

    # ---- 4) Le terrain (bande haute).
    D.add_text(s, marge_g, debut, largeur_haut, ent_h, [
        ("CE QUE CE TERRAIN IMPOSE", dict(size=lbl_sz, bold=True, color=MUTED)),
    ])
    for i, texte in enumerate(contraintes):
        x, w = col_x(i, len(contraintes), w=largeur_haut, x0=marge_g, gap=0.14)
        D.add_rect(s, x, pills_top, w, pills_h, fill=SUPPORT, rounded=True, radius=0.08)
        D.add_text(s, x + 0.14, pills_top, w - 0.28, pills_h, [
            (texte, dict(size=corps_sz, color=NAVY, line_spacing=1.25)),
        ], anchor=MSO_ANCHOR.MIDDLE)

    # ---- 5) La frise : conteneurs en CONTOUR, l'étape optionnelle en pointillé
    # (sa différence est portée par la FORME et le gris, jamais par une teinte
    # qui signifierait « optionnel »), et « un sur N en accent » — la boucle,
    # qui est ce qui transforme la mission en delta mesuré.
    for i, (sym, titre, duree, optionnel, orga, infra, livrable) in enumerate(phases):
        x, w = col_x(i, n, w=largeur_haut, x0=marge_g, gap=ecart)
        cx = x + w / 2
        accent = (sym == "⟲")
        color = MUTED if optionnel else (ACCENT_PLEIN if accent else ENCRE)
        texte_color = MUTED if optionnel else NAVY

        if optionnel:
            _dashed_rect(s, x, card_top, w, card_h, WHITE, color, line_w=1.1, radius=0.08)
        else:
            D.add_rect(s, x, card_top, w, card_h, fill=WHITE, line=color, line_w=1.1,
                       rounded=True, radius=0.08)

        chev_x = cx - chev_w_frac * w / 2
        _chevron_shape(s, chev_x, chev_top, chev_w_frac * w, titre_h, fill=WHITE,
                       line=color, line_w=1.1)
        D.add_text(s, chev_x + chev_pad, chev_top, chev_w_frac * w - 2 * chev_pad, titre_h, [
            (titre, dict(size=titre_sz, bold=True, color=texte_color,
                         align=PP_ALIGN.CENTER, line_spacing=1.05)),
        ], anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)

        _badge(s, cx, badge_cy, badge_d, color, sym,
               filled=not optionnel, dashed=optionnel, fill=(TRACK if optionnel else None),
               # Le chiffre est DANS l'aplat : sur le badge cyan, le blanc
               # tomberait à 1,86:1 — `encre_de` ne protège pas ce cas-là.
               text_color=(NAVY if accent else None),
               bold=(sym not in ("⟲", "+")), size=12)

        chip(s, cx - 0.48, chip_y, 0.96, chip_h, duree, color,
             text_color=(NAVY if accent else WHITE), size=chip_sz)

        for lbl, lbl_y, (verbe, suite), corps_y in (
                ("ORGANISATION", lbl_orga_y, orga, orga_y),
                ("INFRA", lbl_infra_y, infra, infra_y)):
            D.add_text(s, x + 0.05, lbl_y, tw, lbl_h, [
                (lbl, dict(size=lbl_sz, bold=True, color=MUTED)),
            ])
            _rich(s, x + 0.05, corps_y, tw, (orga_h if lbl == "ORGANISATION" else infra_h), [
                ([(verbe, dict(size=corps_sz, bold=True, color=texte_color)),
                  (suite, dict(size=corps_sz, color=texte_color))],
                 dict(line_spacing=1.2)),
            ])

        D.add_rect(s, x + 0.05, sep_y, tw, 0.012, fill=LINE)
        _rich(s, x + 0.05, livr_y, tw, livr_h, [
            ([("Livrable : ", dict(size=livr_sz, color=MUTED)),
              (livrable, dict(size=livr_sz, bold=True, color=texte_color))],
             dict(line_spacing=1.2)),
        ])

    # ---- 6) L'agentic, au second plan (contour gris, pas de barre d'accent :
    # elle mettrait ces deux encarts au même poids que la frise).
    for i, (picto, label, texte) in enumerate(agentic):
        x = marge_g + i * (ag_w + ag_gap)
        D.add_rect(s, x, agents_top, ag_w, agents_h, fill=WHITE, line=SUPPORT_LIGNE,
                   line_w=1.0, rounded=True, radius=0.07)
        _picto(s, picto, x + 0.12, agents_top + agents_h / 2 - picto_d / 2, picto_d, MUTED)
        D.add_text(s, x + ag_txt_off, agents_top + ag_pad / 2, ag_tw, agents_h - ag_pad, [
            (label, dict(size=ag_sz, bold=True, color=MUTED, line_spacing=1.1)),
            (texte, dict(size=ag_sz, color=MUTED, space_before=3, line_spacing=1.25)),
        ], anchor=MSO_ANCHOR.MIDDLE)

    # ---- 7) Clôture : la seule affirmation que le client doit emporter s'il ne
    # veut pas d'IA du tout.
    _quote_banner(s, marge_g, punch_top, largeur, punch_h, punch_txt, size=12)

    bas_reel = punch_top + punch_h
    if bas_reel > bas_max:
        raise SystemExit(
            f"slide_synthese_pourquoi_quoi_comment : contenu déborde de "
            f"{bas_reel - bas_max:.3f}in sous bas_max ({bas_max}in, bas réel "
            f"{bas_reel:.3f}in) — resserrer avant de régénérer."
        )
    return s


# v2.32 (2026-09-04, refonte graphique) : DÉPLACÉE du chapitre 02 · Contexte
# vers le chapitre 01 · Exec summary (demande utilisateur) — puis REMONTÉE au
# chapitre 03 « Spécificités de l'infra » le 2026-09-10, où elle est
# aujourd'hui. Corps redessiné selon le
# même système de design "contour" (voir historique ci-dessus pour le détail
# du contenu — inchangé, seule la forme change).
def slide_specificites_infra(prs):
    s = content_slide(prs, "Spécificités de l'infra",
                       "D'un guichet sursollicité à une infra as a product — l'IA rend ce virage nécessaire.",
                       color=ACCENT)

    COUL_DOULEUR = MUTED
    COUL_REPONSE = ACCENT

    arrow_w = 0.60
    pill_w = (CONTENT_W - arrow_w) / 2
    pill_pad = 0.17

    def _pill_h(texte, taille=11):
        return _lignes(texte, pill_w - 2 * pill_pad, taille) * (taille * 1.2 / 72.0) + 2 * pill_pad

    def _pill(x, y, w, h, texte, accent, taille=11, radius=0.5):
        D.add_rect(s, x, y, w, h, fill=WHITE, line=accent, line_w=1.3, rounded=True, radius=radius)
        D.add_text(s, x + pill_pad, y, w - 2 * pill_pad, h, [
            (texte, dict(size=taille, bold=True, color=NAVY, align=PP_ALIGN.CENTER, line_spacing=1.15)),
        ], anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)

    douleur_titre = "Sortir de la sursollicitation et du guichet"
    douleur_sub_plain = ("Des équipiers qui font trop de choses, sont engorgés — "
                          "décommissionnement jamais fait, trop de RUN au quotidien.")
    dw = pill_w - 2 * pill_pad
    titre_h1 = _lignes(douleur_titre, dw, 11) * (11 * 1.2 / 72.0) + 0.03
    sub_h1 = _lignes(douleur_sub_plain, dw, 9) * (9 * 1.25 / 72.0) + 0.03
    h1 = max(2 * pill_pad + titre_h1 + 0.06 + sub_h1, _pill_h("Assainir et travailler le gaspillage"))

    y = CONTENT_TOP + 0.02
    # 0,13 -> 0,08 : migrer le bandeau de cloture vers la regle dimensionnee
    # a fait apparaitre un debordement de 0,153in que la variante ETIREE
    # masquait — elle absorbait la place restante, si petite soit-elle.
    row_gap = 0.08
    D.add_rect(s, MARGIN, y, pill_w, h1, fill=WHITE, line=COUL_DOULEUR, line_w=1.3, rounded=True, radius=0.13)
    inner_y = y + (h1 - (titre_h1 + 0.06 + sub_h1)) / 2
    D.add_text(s, MARGIN + pill_pad, inner_y, dw, titre_h1, [
        (douleur_titre, dict(size=11, bold=True, color=NAVY, align=PP_ALIGN.CENTER, line_spacing=1.15)),
    ], align=PP_ALIGN.CENTER)
    avant_e, emph_e, apres_e = _split_emph(
        douleur_sub_plain, "décommissionnement jamais fait, trop de RUN au quotidien.")
    _rich(s, MARGIN + pill_pad, inner_y + titre_h1 + 0.06, dw, sub_h1, [
        ([(avant_e, dict(size=9, italic=True, color=MUTED)),
          (emph_e, dict(size=9, bold=True, color=NAVY))],
         dict(align=PP_ALIGN.CENTER, line_spacing=1.25)),
    ])
    _chevron_arrow(s, MARGIN + pill_w, y, arrow_w, h1, color=MUTED)
    _pill(MARGIN + pill_w + arrow_w, y, pill_w, h1, "Assainir et travailler le gaspillage",
          COUL_REPONSE, radius=0.13)
    y += h1 + row_gap

    intention_servir = "Mieux servir les utilisateurs, avec une approche as a service"
    reponse_utilisateurs = "Une infra plus recentrée sur ces utilisateurs"
    h2 = max(_pill_h(intention_servir), _pill_h(reponse_utilisateurs))
    _pill(MARGIN, y, pill_w, h2, intention_servir, COUL_DOULEUR)
    _chevron_arrow(s, MARGIN + pill_w, y, arrow_w, h2, color=MUTED)
    _pill(MARGIN + pill_w + arrow_w, y, pill_w, h2, reponse_utilisateurs, COUL_REPONSE)
    y += h2 + row_gap

    label_h = 0.13
    D.add_text(s, MARGIN, y + 0.02, CONTENT_W, label_h, [
        ("AVEC L'ARRIVÉE DE L'IA", dict(size=8, bold=True, color=NAVY)),
    ])
    esc_top = y + 0.02 + label_h + 0.06
    badge_d = 0.46
    card_x = MARGIN + badge_d / 2
    card_top = esc_top + badge_d / 2
    card_w = BORD_DROIT - card_x
    alert_pad = 0.22
    alert_tw = card_w - 2 * alert_pad
    alert_title = "UNE SURSOLLICITATION EXACERBÉE"
    alert_body = ("Trop de demandes, des équipes engorgées — la même pression que le "
                  "guichet d'hier, amplifiée par l'IA plutôt que résolue par elle.")
    title_h = _lignes(alert_title, alert_tw, 9.5) * (9.5 * 1.2 / 72.0) + 0.03
    body_h = _lignes(alert_body, alert_tw, 9) * (9 * 1.25 / 72.0) + 0.03
    text_top = card_top + badge_d / 2 + 0.05
    title_y = text_top
    body_y = title_y + title_h + 0.05
    card_h = (body_y + body_h + 0.13) - card_top

    D.add_rect(s, card_x, card_top, card_w, card_h, fill=WHITE, line=DK2, line_w=1.4, rounded=True, radius=0.09)
    D.add_text(s, card_x + alert_pad, title_y, alert_tw, title_h, [
        (alert_title, dict(size=9.5, bold=True, color=DK2)),
    ])
    av_e, em_e, ap_e = _split_emph(alert_body, "amplifiée par l'IA plutôt que résolue par elle.")
    _rich(s, card_x + alert_pad, body_y, alert_tw, body_h, [
        ([(av_e, dict(size=9, color=NAVY)),
          (em_e, dict(size=9, bold=True, color=DK2))],
         dict(line_spacing=1.25)),
    ])
    _badge(s, card_x, card_top, badge_d, NAVY, "IA", filled=True, size=11)
    y = card_top + card_h + 0.14

    _bandeau_cloture(s, "L'objectif : infra as a product.",
                     y, "slide_specificites_infra")
    return s


# v2.32 (2026-09-04, refonte graphique) : DÉPLACÉE du chapitre 02 · Contexte
# vers le chapitre 01 · Exec summary (demande utilisateur) — puis REMONTÉE au
# chapitre 03 « Spécificités de l'infra » le 2026-09-10, où elle ferme le
# chapitre. Corps redessiné selon le même système
# de design "contour" (contenu inchangé, seule la forme change).
def slide_infra_as_product_exemple(prs):
    s = content_slide(prs, "Spécificités de l'infra",
                       "Ce que change l'infra as a product, concrètement — un exemple avant/après.",
                       color=ACCENT)

    col_w = (CONTENT_W - 0.90) / 2
    card_top = CONTENT_TOP - 0.251
    card_h = 3.3
    pad = 0.24
    tag_h = 0.30

    avant_x = MARGIN
    D.add_rect(s, avant_x, card_top, col_w, card_h, fill=WHITE, line=MUTED, line_w=1.3, rounded=True, radius=0.09)
    tag1_w = 1.05
    D.add_rect(s, avant_x + pad - 0.06, card_top + 0.16, tag1_w, tag_h, fill=MUTED, rounded=True, radius=0.5)
    D.add_text(s, avant_x + pad - 0.06, card_top + 0.16, tag1_w, tag_h, [
        ("AVANT", dict(size=11, bold=True, color=WHITE, align=PP_ALIGN.CENTER)),
    ], anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)

    avant_items = [
        ("Guichet de tickets", " — personne n'est propriétaire du service."),
        ("Le triage du RUN trop long", ", traité au fil de l'eau."),
        ("Backlog invisible", ", aucun indicateur de pilotage."),
        ("Plein de projets lancés, peu d'indicateurs",
         ", du contrôle et du reporting à tous les niveaux."),
        ("Un pilotage dans la douleur",
         ", on prend tout et l'on ne sait plus comment bien prioriser les bons sujets à "
         "réaliser avec trop peu de capacité à faire."),
    ]
    avant_paragraphs = [
        ([("—  ", dict(size=9, color=MUTED)),
          (lead, dict(size=9, bold=True, color=NAVY)),
          (rest, dict(size=9, color=MUTED))],
         dict(line_spacing=1.2, space_before=(0 if i == 0 else 7)))
        for i, (lead, rest) in enumerate(avant_items)
    ]
    _rich(s, avant_x + pad, card_top + 0.66, col_w - 2 * pad, card_h - 0.9, avant_paragraphs,
          anchor=MSO_ANCHOR.MIDDLE)

    fleche_x = avant_x + col_w + 0.14
    fleche_w = 0.62
    arrow = s.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(fleche_x),
                                Inches(card_top + card_h * 0.30),
                                Inches(fleche_w), Inches(card_h * 0.40))
    try:
        arrow.shadow.inherit = False
    except Exception:
        pass
    arrow.fill.solid()
    arrow.fill.fore_color.rgb = _rgb(WHITE)
    arrow.line.color.rgb = _rgb(ACCENT)
    arrow.line.width = Pt(2.25)
    arrow.text_frame.paragraphs[0].text = ""

    apres_x = fleche_x + fleche_w + 0.14
    D.add_rect(s, apres_x, card_top, col_w, card_h, fill=WHITE, line=ACCENT, line_w=1.6, rounded=True, radius=0.09)
    tag2_w = 2.55
    D.add_rect(s, apres_x + pad - 0.06, card_top + 0.16, tag2_w, tag_h, fill=ACCENT, rounded=True, radius=0.5)
    D.add_text(s, apres_x + pad - 0.06, card_top + 0.16, tag2_w, tag_h, [
        ("APRÈS — démarche + agentique", dict(size=10, bold=True, color=NAVY, align=PP_ALIGN.CENTER)),
    ], anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)

    apres_items = [
        ("Un propriétaire produit et un pilotage serein",
         ", une roadmap, des indicateurs de pilotage."),
        ("Temps de triage du RUN fortement réduit", " — capacité RUN récupérée."),
        ("Backlog visible", ", priorisé, mesuré dans le temps."),
        ("Process explicite, rôles définis", " — piste retenue : agentique-implementation."),
        ("Des évolutions tech", " qui sont possibles et atteignables."),
    ]
    apres_paragraphs = [
        ([("✓  ", dict(size=9, color=ACCENT, bold=True)),
          (lead, dict(size=9, bold=True, color=NAVY)),
          (rest, dict(size=9, color=NAVY))],
         dict(line_spacing=1.2, space_before=(0 if i == 0 else 6)))
        for i, (lead, rest) in enumerate(apres_items)
    ]
    _rich(s, apres_x + pad, card_top + 0.66, col_w - 2 * pad, card_h - 0.9, apres_paragraphs,
          anchor=MSO_ANCHOR.MIDDLE)

    _bandeau_cloture(
        s,
        ("Infra as a product, concrètement : le retour à une maîtrise de faire les "
         "bonnes choses au bon moment, un backlog piloté, des résultats concrets — "
         "dans notre approche l'agentique accélère la démarche, il ne la remplace pas."),
        card_top + card_h + 0.16, "slide_infra_as_product_exemple")
    return s


# --- Chapitre 03 · Spécificités de l'infra (v2.33, demande utilisateur du
# 2026-09-10 : « un chapitre dédié au traitement des spécificités de l'INFRA
# comme le RUN ou le fait que l'infra soit transverse »). Les deux slides
# ci-dessus (slide_specificites_infra, slide_infra_as_product_exemple) y sont
# DÉPLACÉES depuis le chapitre 01 · Exec summary : elles traitaient déjà le
# sujet, l'exec summary les portait faute de chapitre d'accueil. Les deux
# suivantes sont NEUVES et couvrent ce que la demande nommait explicitement et
# que le deck ne disait nulle part : ce qui rend le RUN structurellement à part,
# et ce que la transversalité fait au gaspillage.
def slide_infra_run(prs):
    """Ce qui rend le RUN d'infra structurellement différent d'un projet.

    Flux numéroté (deck-design-library #4) plutôt que des cartes : les quatre
    traits ne sont pas une liste d'inconvénients, ils s'enchaînent — il ne
    s'arrête jamais, donc il n'est pas planifiable, donc il prend sur le BUILD,
    et sa dette ne se voit pas le jour où on l'accumule.
    """
    s = content_slide(prs, "Spécificités de l'infra",
                      "Le RUN n'est pas une phase du projet : c'est un régime permanent, "
                      "et c'est ce qui le rend impossible à traiter comme du BUILD",
                      color=ENCRE)

    rows = [
        ("Il ne s'arrête jamais",
         "Un projet se termine, le RUN non. L'astreinte, la veille et le maintien en "
         "condition sont un coût fixe qu'aucune fin de phase ne libère.",
         "Aucune date de fin ne le fait retomber"),
        ("Sa charge arrive de l'extérieur",
         "Elle n'est pas planifiée : elle est déclenchée par les incidents, les demandes "
         "et les obsolescences. On subit le rythme au lieu de le choisir.",
         "Le carnet se remplit sans arbitrage"),
        ("Il puise dans les MÊMES experts que le BUILD",
         "Les seniors capables de tenir la production sont ceux qui construisent. À "
         "chaque conflit, l'incident du jour gagne contre le chantier de fond.",
         "Le BUILD paie, toujours dans le même sens"),
        ("Sa dette ne se voit pas le jour où on la crée",
         "Ne pas décommissionner, ne pas documenter, ne pas automatiser ne casse rien "
         "aujourd'hui. Le coût se paie plus tard, et ailleurs.",
         "Rien ne tombe le jour de l'arbitrage"),
    ]

    n = len(rows)
    lane_gap = 0.16
    lane_w = (CONTENT_W - (n - 1) * lane_gap) / n
    pad = 0.06
    body_w = lane_w - 2 * pad

    lane_top = CONTENT_TOP + 0.30
    badge_d = 0.5
    connector_h = 0.16
    titre_size, corps_size, chute_size = 8.5, 9, 8
    titre_h = max(_lignes(r[0], body_w, titre_size) for r in rows) * (titre_size * 1.2 / 72.0) + 0.05
    corps_h = max(_lignes(r[1], body_w, corps_size) for r in rows) * (corps_size * 1.25 / 72.0) + 0.04
    chute_h = max(_lignes(r[2], body_w, chute_size) for r in rows) * (chute_size * 1.2 / 72.0) + 0.04

    connector_top = lane_top + badge_d
    titre_top = connector_top + connector_h
    corps_top = titre_top + titre_h + 0.04
    chute_label_top = corps_top + corps_h + 0.10
    chute_top = chute_label_top + 0.16

    # « Un sur N en accent » : le 3e trait est celui qui coûte le plus cher à la
    # transformation — c'est lui qui explique pourquoi le BUILD n'avance pas.
    i_accent = 2

    for i, (titre, corps, chute) in enumerate(rows):
        x = MARGIN + i * (lane_w + lane_gap)
        cxm = x + lane_w / 2.0
        couleur = ACCENT_PLEIN if i == i_accent else ENCRE
        D.add_dot(s, cxm - badge_d / 2, lane_top, badge_d, couleur)
        D.add_text(s, x, lane_top, lane_w, badge_d, [
            # Le chiffre est DANS l'aplat : sur le badge accentue (cyan) le
            # blanc tombe a 1,86:1. `encre_de` protege le libelle en dessous,
            # pas le texte pose sur la couleur elle-meme.
            (str(i + 1), dict(size=13, bold=True,
                              color=NAVY if couleur == ACCENT_PLEIN else WHITE,
                              align=PP_ALIGN.CENTER)),
        ], anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
        D.add_rect(s, cxm - 0.011, connector_top, 0.022, connector_h, fill=couleur)
        D.add_text(s, x, titre_top, lane_w, titre_h, [
            (titre, dict(size=titre_size, bold=True, color=encre_de(couleur),
                         align=PP_ALIGN.CENTER, line_spacing=1.2)),
        ], anchor=MSO_ANCHOR.TOP, align=PP_ALIGN.CENTER)
        D.add_text(s, x + pad, corps_top, body_w, corps_h, [
            (corps, dict(size=corps_size, color=NAVY, line_spacing=1.25)),
        ])
        D.add_text(s, x + pad, chute_label_top, body_w, 0.14, [
            ("CE QUI LE REND INVISIBLE", dict(size=6.5, bold=True, color=MUTED)),
        ])
        D.add_text(s, x + pad, chute_top, body_w, chute_h, [
            (chute, dict(size=chute_size, color=MUTED, italic=True, line_spacing=1.2)),
        ])

    _bandeau_cloture(s, "Traiter le RUN comme un projet, c'est le perdre à chaque arbitrage.",
                     chute_top + chute_h + 0.14, "slide_infra_run")
    return s


def slide_infra_transverse(prs):
    """L'infra sert toutes les équipes et n'appartient à aucune.

    Composition « sandwich » (deck-design-library #5) : les équipes servies en
    haut, la plateforme qui les porte en bandeau plein, et dessous la
    conséquence qui n'est jamais dite — un gaspillage que personne ne porte en
    propre n'est réduit par personne. C'est la charnière vers le chapitre
    Besoins & douleurs, et le fondement de la démarche partagée.
    """
    s = content_slide(prs, "Spécificités de l'infra",
                      "L'infra sert toutes les équipes et n'appartient à aucune — "
                      "c'est ce qui rend son gaspillage orphelin",
                      color=ENCRE)

    servies = [
        ("Équipes produit", "Livrent de la valeur métier — l'infra est un moyen, jamais leur sujet."),
        ("Équipes applicatives", "Consomment la plateforme, ou la contournent si elle freine."),
        ("Sécurité, conformité & résilience", "Exigences transverses que personne ne budgète — "
         "l'offre s'y arrime, ne les remplace pas (cf. chapitre Démarches)."),
        ("Direction", "Voit une ligne de coût, pas les arbitrages qui la produisent."),
    ]

    n = len(servies)
    gap = 0.16
    card_w = (CONTENT_W - (n - 1) * gap) / n
    pad = 0.12
    tw = card_w - 2 * pad

    titre_size, corps_size = 9, 8
    t_h = max(_lignes(t, tw, titre_size) for t, _ in servies) * (titre_size * 1.2 / 72.0) + 0.04
    c_h = max(_lignes(c, tw, corps_size) for _, c in servies) * (corps_size * 1.25 / 72.0) + 0.04
    card_h = pad + t_h + 0.05 + c_h + pad

    top = CONTENT_TOP + 0.24
    D.add_text(s, MARGIN, CONTENT_TOP - 0.02, CONTENT_W, 0.18, [
        ("CE QUE L'INFRA SERT", dict(size=8, bold=True, color=MUTED)),
    ])
    for i, (titre, corps) in enumerate(servies):
        x = MARGIN + i * (card_w + gap)
        D.add_rect(s, x, top, card_w, card_h, fill=WHITE, line=ENCRE, line_w=1.15,
                   rounded=True, radius=0.09)
        D.add_text(s, x + pad, top + pad, tw, t_h, [
            (titre, dict(size=titre_size, bold=True, color=ENCRE, line_spacing=1.15)),
        ])
        D.add_text(s, x + pad, top + pad + t_h + 0.05, tw, c_h, [
            (corps, dict(size=corps_size, color=MUTED, line_spacing=1.25)),
        ])

    # Le bandeau plein : la seule forme accentuée de la slide (« un sur N »).
    # Elle porte l'infra, littéralement sous les équipes qu'elle sert.
    bande_top = top + card_h + 0.16
    bande_txt = "UNE SEULE INFRA, SOUS TOUTES CES ÉQUIPES"
    bande_h = 0.42
    D.add_rect(s, MARGIN, bande_top, CONTENT_W, bande_h, fill=ENCRE, rounded=True, radius=0.09)
    D.add_text(s, MARGIN, bande_top, CONTENT_W, bande_h, [
        (bande_txt, dict(size=10, bold=True, color=WHITE, align=PP_ALIGN.CENTER)),
    ], anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)

    consequences = [
        ("PERSONNE NE PORTE LE COÛT",
         "Le gaspillage d'infra est mutualisé : il ne pèse sur le budget d'aucune équipe "
         "en particulier, donc aucune n'a de raison propre de le réduire."),
        ("PERSONNE N'ARBITRE SEUL",
         "Décommissionner, standardiser ou fermer un service touche tous les consommateurs "
         "à la fois — la décision ne peut pas être prise dans un seul couloir."),
    ]
    cons_top = bande_top + bande_h + 0.16
    cons_gap = 0.18
    cons_w = (CONTENT_W - cons_gap) / 2
    ctw = cons_w - 2 * pad
    ct_h = 0.16
    cc_h = max(_lignes(c, ctw, corps_size) for _, c in consequences) * (corps_size * 1.25 / 72.0) + 0.04
    cons_h = pad * 0.8 + ct_h + 0.04 + cc_h + pad * 0.8

    for i, (titre, corps) in enumerate(consequences):
        x = MARGIN + i * (cons_w + cons_gap)
        D.add_rect(s, x, cons_top, cons_w, cons_h, fill=SUPPORT, rounded=True, radius=0.09)
        D.add_rect(s, x + 0.10, cons_top + pad * 0.5, 0.045, cons_h - pad,
                   fill=ACCENT_PLEIN, rounded=True, radius=0.5)
        D.add_text(s, x + 0.26, cons_top + pad * 0.8, ctw - 0.14, ct_h, [
            (titre, dict(size=8, bold=True, color=ENCRE)),
        ])
        D.add_text(s, x + 0.26, cons_top + pad * 0.8 + ct_h + 0.04, ctw - 0.14, cc_h, [
            (corps, dict(size=corps_size, color=NAVY, line_spacing=1.25)),
        ])

    _bandeau_cloture(s, "Un gaspillage que personne ne porte, personne ne le réduit.",
                     cons_top + cons_h + 0.14, "slide_infra_transverse")
    return s


def slide_mission(prs):
    s = content_slide(prs, "Contexte", "Une double mission : transformer ET assainir", color=ENCRE)
    cards = [
        ("TRANSFORMER", ENCRE,
         "Cible produit/plateforme : utilisateurs identifiés, valeur, roadmap, "
         "engagements de qualité, gouvernance lisible.",
         "La vision à moyen terme — ce que le sponsor achète."),
        ("ASSAINIR", ENCRE,
         "Traitement mesurable des gaspillages : flux, RUN, humain, financier, "
         "cognitif, décisionnel, environnemental, IA.",
         # v2.3 : promesse instrumentée, pas un acquis — même honnêteté que le
         # statut interne du cadrage (fin du double discours, finding C1).
         # 2026-09-01 : la moitié CONDITIONNELLE de la formule du cadrage (l.23,
         # « Hypothèse porteuse à prouver, pas un invariant acquis […] suppose un
         # mécanisme de réallocation budgétaire côté client ») avait été effacée —
         # la slide affirmait au présent un KPI qui est un point ouvert MVP3.
         "La capacité récupérée finance la trajectoire produit — hypothèse à "
         "prouver, qui suppose une réallocation budgétaire côté client."),
    ]
    # v2.5 (chantier ③) : les cartes flottaient à CONTENT_TOP+0.5 sans rien
    # au-dessus (~0.5in de blanc sous le titre). La note « ni séquentiels ni
    # optionnels » devient le CHAPEAU (à CONTENT_TOP), les cartes suivent, et
    # la rangée de tensions gagne son étiquette — l'espace se redistribue dans
    # le contenu, pas en vide.
    chapeau_h = 0.5
    D.add_text(s, MARGIN, CONTENT_TOP, CONTENT_W, chapeau_h, [
        ("Deux piliers ni séquentiels ni optionnels : une cible produit sans traitement du "
         "gaspillage manque de capacité pour s'y déployer ; l'inverse reste une réduction "
         "de coûts sans vision.",
         dict(size=D.TYPE["small"], color=NAVY, italic=True, line_spacing=1.25)),
    ])
    card_h = 1.95
    top0 = CONTENT_TOP + chapeau_h + 0.12
    for i, (titre, color, vise, finance) in enumerate(cards):
        x, w = col_x(i, 2)
        D.add_card(s, x, top0, w, card_h, color)
        pad = 0.22
        D.add_text(s, x + pad, top0 + 0.18, w - 2 * pad, 0.3, [
            (titre, dict(size=D.TYPE["h3"], bold=True, color=encre_de(color)))
        ])
        D.add_text(s, x + pad, top0 + 0.58, w - 2 * pad, 0.62, [
            ("CE QU'IL VISE", dict(size=D.TYPE["tiny"], bold=True, color=MUTED)),
            (vise, dict(size=D.TYPE["tiny"], color=NAVY, space_before=2, line_spacing=1.25)),
        ])
        D.add_text(s, x + pad, top0 + 1.28, w - 2 * pad, 0.58, [
            ("CE QU'IL FINANCE", dict(size=D.TYPE["tiny"], bold=True, color=MUTED)),
            (finance, dict(size=D.TYPE["tiny"], color=NAVY, space_before=2, line_spacing=1.25)),
        ])

    label_top = top0 + card_h + 0.22
    D.add_text(s, MARGIN, label_top, CONTENT_W, 0.22, [
        ("L'ÉQUILIBRE QUE LA DOUBLE MISSION TIENT EN PERMANENCE",
         dict(size=7.5, bold=True, color=MUTED)),
    ])
    tens_top = label_top + 0.26
    tens_h = 0.62
    tensions = ["Efficacité du delivery", "Robustesse du RUN", "Valeur perçue (utilisateurs internes)"]
    for i, t in enumerate(tensions):
        x, w = col_x(i, 3)
        D.add_rect(s, x, tens_top, w, tens_h, fill=TRACK, rounded=True, radius=0.12)
        D.add_text(s, x + 0.1, tens_top, w - 0.2, tens_h, [
            (t, dict(size=D.TYPE["tiny"], bold=True, color=NAVY, align=PP_ALIGN.CENTER))
        ], anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
    return s


def slide_pourquoi_contexte(prs):
    """Nouveau (point ②) : dans le chapitre Contexte, le POURQUOI — pourquoi
    proposer cette transformation à un client infra, et maintenant. Trois
    déclencheurs + un pont trait-pour-trait vers la double mission (slide_mission).
    Forme (refonte graphique, deck-design-library pattern 4 « schéma des N
    freins en flux numéroté ») : badge rond numéroté + connecteur vertical +
    titre/corps, SANS carte à bordure — les 3 cartes plates précédentes
    (bordure colorée + paragraphe) ne portaient aucune idée de forme propre,
    juste une redite du gabarit générique du deck. Le badge remplace le
    micro-label « DÉCLENCHEUR N » : l'ordinal se lit d'un coup d'œil."""
    s = content_slide(prs, "Contexte",
                       "Pourquoi cette transformation, pour un client infra — et maintenant",
                       color=ENCRE)
    D.add_text(s, MARGIN, CONTENT_TOP, CONTENT_W, 0.5, [
        ("Trois bascules rendent l'Infra-as-a-Product pertinente — et urgente — pour un client "
         "dont l'infrastructure est encore vécue comme un centre de coûts et un guichet.",
         dict(size=D.TYPE["small"], color=NAVY, italic=True, line_spacing=1.25)),
    ])
    triggers = [
        (ENCRE, "L'infra subie n'est plus tenable",
         "RUN subi, experts seniors drainés sur du répétitif, gaspillage cloud non maîtrisé, "
         "plateforme contournée : le coût du statu quo ne cesse de monter."),
        # Le « MAIS » du cadrage (l.43) est le motif d'achat du pilier Assainir :
        # sans lui, ce declencheur ne declenche rien. Restaure le 2026-09-01.
        (ENCRE, "Le modèle produit/plateforme est prouvé",
         "Devenu un standard — mais Gartner : 80 % de grandes organisations avec platform "
         "team en 2026, moins de 30 % de gains mesurables. C'est cet écart qu'Assainir adresse."),
        (ENCRE, "L'IA rebat les cartes — l'organisation d'abord",
         "L'IA amplifie une organisation mûre, jamais l'inverse. S'y préparer maintenant "
         "(doctrine confidentialité-first) évite de la subir plus tard."),
    ]
    lead_h, bridge_h = 0.55, 0.72
    top0 = CONTENT_TOP + lead_h + 0.1
    badge_d = 0.46
    connector_h = 0.16
    text_top = top0 + badge_d + connector_h + 0.05

    def lh(pt, spacing):
        return pt * spacing / 72.0

    # Bloc badge+texte dimensionné à SON contenu (pas étiré jusqu'au pont du
    # bas) — sinon la suppression de la carte à bordure (qui absorbait le vide
    # visuellement) laisse un grand blanc entre le texte et le pont, trouvé au
    # rendu (cf. « panneau sur-étiré »).
    _, col_w3 = col_x(0, 3)
    text_h_besoin = max(
        _lignes(titre, col_w3, D.TYPE["small"]) * lh(D.TYPE["small"], 1.05)
        + lh(8, 1.0) + _lignes(corps, col_w3, 9) * lh(9, 1.25)
        for _, titre, corps in triggers)
    for i, (color, titre, corps) in enumerate(triggers):
        x, w = col_x(i, 3)
        cx = x + badge_d / 2
        _badge(s, cx, top0 + badge_d / 2, badge_d, color, str(i + 1), size=15)
        D.add_rect(s, cx - 0.011, top0 + badge_d, 0.022, connector_h, fill=NAVY,
                   rounded=True, radius=0.5)
        D.add_text(s, x, text_top, w, text_h_besoin, [
            (titre, dict(size=D.TYPE["small"], bold=True, color=encre_de(color), line_spacing=1.05)),
            (corps, dict(size=9, color=NAVY, space_before=8, line_spacing=1.25)),
        ])
    bridge_top = min(text_top + text_h_besoin + 0.32, CONTENT_BOTTOM - bridge_h)
    D.add_rect(s, MARGIN, bridge_top, CONTENT_W, bridge_h, fill=TRACK, rounded=True, radius=0.1)
    D.add_rect(s, MARGIN, bridge_top, 0.08, bridge_h, fill=ENCRE, rounded=True, radius=0.5)
    D.add_text(s, MARGIN + 0.28, bridge_top, CONTENT_W - 0.46, bridge_h, [
        ("Et surtout — nos deux missions répondent trait pour trait aux deux douleurs du client.",
         dict(size=8.5, bold=True, color=NAVY, line_spacing=1.05)),
        ("Subir le RUN → TRANSFORMER (cible produit/plateforme) ; le gaspillage → ASSAINIR "
         "(capacité récupérée à réinvestir dans la trajectoire — sous réserve d'une "
         "réallocation côté client).",
         dict(size=8, color=MUTED, space_before=2, line_spacing=1.15)),
    ], anchor=MSO_ANCHOR.MIDDLE)
    return s


# --- Nouveau (2026-09-01) : « qui achète, contre quoi ». La section
# §Positionnement & achat du cadrage (l.36) fait foi POUR LE DECK depuis la
# v2.3, mais n'y avait jamais été redescendue : 40 slides disaient COMMENT on
# fait la mission, aucune contre quel achat alternatif elle se gagne.
# Forme (refonte graphique 2026-09-07, deck-design-library) : la 1re version
# (grille-référentiel pattern 15) restait un tableau déguisé — 4 lignes x 3
# colonnes, l'audit design l'a signalé. Remplacée par 4 fiches signature
# (coin coupé, ROUND_2_DIAG_RECTANGLE) à DEUX zones empilées : haut blanc
# neutre = ce que l'achat alternatif apporte, bas navy plein = ce qui lui
# manque + la réponse IAP (variante du « ticket » bipartite, pattern 21 —
# le contraste de fond porte le message avant même la lecture du texte).
# La ligne de partage est à la MÊME hauteur pour les 4 cartes (dimensionnée
# sur le contenu le plus long, pas étirée) : le nom et le "ce qui manque" de
# chaque alternative restent alignés en rangée malgré des textes de longueur
# différente. En pied, bandeau transverse (pattern 18) inchangé : collision
# de nom (l.63) et réponse au sponsor « je ne veux que la baisse de coûts »
# (l.57, l.78).
def slide_qui_achete(prs):
    s = content_slide(prs, "Contexte",
                       "Le sponsor est la DSI — l'offre se gagne contre quatre achats partiels",
                       color=ENCRE)

    def lh(pt):
        return pt * 1.25 / 72.0

    # --- Chapeau : qui achète, et dans quel langage (cadrage l.48) -----------
    lead1 = ("Sponsor qualifié : DSI (direction des systèmes d'information) ou direction "
             "infrastructure, sur une ligne budgétaire transformation — jamais le budget "
             "RUN (exploitation courante).")
    lead2 = ("La modernisation infra recule face à la cyber dans les priorités budgétaires "
             "2026 (baromètre Abraxio) : le langage de vente est « récupérer de la capacité "
             "humaine rare », pas « moderniser l'infra ».")
    lead_h = (_lignes(lead1, CONTENT_W, 9.5) * lh(9.5)
              + _lignes(lead2, CONTENT_W, 7.5) * lh(7.5) + 0.09)
    D.add_text(s, MARGIN, CONTENT_TOP, CONTENT_W, lead_h, [
        (lead1, dict(size=9.5, color=NAVY, italic=True, line_spacing=1.25)),
        (lead2, dict(size=7.5, color=MUTED, space_before=3, line_spacing=1.25)),
    ])

    # --- Bandeau transverse : dimensionné AVANT la grille, qui prend le reste
    # (jamais de panneau étiré sur la hauteur restante).
    bandeaux = [
        (TRACK, MUTED, NAVY, "CE QUE LES QUATRE ALTERNATIVES N'ONT PAS",
         "L'étiquette « Infrastructure as a Product » existe ailleurs — Thoughtworks (conseil), "
         "Itential (plateforme) ; nous la gardons. Le différenciateur est le couplage produit "
         "+ gaspillage + doctrine IA, angle mort commun des quatre."),
        (NAVY, "#8891b3", "#ffffff", "LA RÉPONSE AU « JE NE VEUX QUE LA BAISSE DE COÛTS »",
         "Un Assessment flash d'entrée, avant toute action d'accompagnement — puis la "
         "trajectoire ; jamais l'assainissement seul. Sous pression IA, un cas d'usage sur "
         "données publiques est packagé dès l'intake : « celui-ci, tout de suite, sous gate » "
         "(chapitre Offre)."),
    ]
    _, band_w = col_x(0, 2)
    band_pad = 0.12
    band_lignes = max(_lignes(b[4], band_w - 2 * band_pad - 0.04, 7) for b in bandeaux)
    band_h = 2 * band_pad + lh(7) + 0.04 + band_lignes * lh(7) + 0.03
    band_top = CONTENT_BOTTOM - band_h

    # --- 4 fiches signature (coin coupé) à deux zones empilées --------------
    alternatives = [
        ("Ne rien faire",
         "Zéro coût apparent.",
         "Le coût du statu quo monte",
         "C'est lui que l'Assessment flash chiffre (déclencheur ①)."),
        ("FinOps outillé seul",
         "Mesure le gaspillage : marché mature, gaspillage cloud estimé à 29 % (Flexera).",
         "Ni cible produit, ni réallocation",
         "IAP se place en aval : le chiffre devient une capacité produit gouvernée, pas "
         "seulement une économie."),
        ("Platform engineering pur",
         "La cible produit/plateforme, un modèle devenu standard.",
         "La cible sans le financement",
         "Reproduit l'écart 80/30 déjà posé au déclencheur ② : 80 % de platform teams en 2026, "
         "moins de 30 % de gains mesurables (Gartner)."),
        ("AIOps / agentic outillé",
         "Time-to-value court (ServiceNow, Datadog).",
         "Automatise le RUN sans transformer",
         "Plus de 40 % des projets agentic seront abandonnés d'ici 2027 (Gartner, juin 2025)."),
    ]
    col_w = (CONTENT_W - 3 * GAP) / 4
    pad_x = 0.13
    label_h = lh(6) + 0.04  # « ACHAT ALTERNATIF » / « RÉPONSE IAP », 1 ligne fixe

    def _zone_h(titre, corps, titre_size, pad_top, pad_bot):
        return (pad_top + label_h
                + _lignes(titre, col_w - 2 * pad_x, titre_size) * lh(titre_size) + 0.04
                + _lignes(corps, col_w - 2 * pad_x, 7.3) * lh(7.3) + pad_bot)

    # Hauteur de chaque zone dimensionnée sur l'alternative la PLUS longue à
    # décrire, pas étirée à l'espace disponible (cf. « panneau sur-étiré ») —
    # la ligne de partage reste néanmoins à la MÊME hauteur pour les 4 cartes :
    # nom et « ce qui manque » s'alignent en rangée malgré des textes inégaux.
    top_h = max(_zone_h(nom, apporte, 8.5, 0.07, 0.06) for nom, apporte, _, _ in alternatives)
    bot_h = max(_zone_h(manque, reponse, 7.5, 0.08, 0.09) for _, _, manque, reponse in alternatives)
    card_h = top_h + bot_h
    grid_top = CONTENT_TOP + lead_h + 0.14
    row_top = grid_top + max(0.0, (band_top - 0.16 - grid_top - card_h) / 2)

    for i, (nom, apporte, manque, reponse) in enumerate(alternatives):
        x, w = col_x(i, 4)
        carte = s.shapes.add_shape(MSO_SHAPE.ROUND_2_DIAG_RECTANGLE,
                                    Inches(x), Inches(row_top), Inches(w), Inches(card_h))
        try:
            carte.shadow.inherit = False
        except Exception:
            pass
        carte.fill.solid()
        carte.fill.fore_color.rgb = _rgb("#ffffff")
        carte.line.color.rgb = _rgb(LINE)
        carte.line.width = Pt(1.0)
        carte.text_frame.paragraphs[0].text = ""
        # Zone basse navy pleine = la réponse IAP — le contraste de fond porte
        # le message avant même la lecture du texte (« un sur N » appliqué à
        # la ZONE partagée par les 4 cartes, pas à une carte isolée : les 4
        # réponses pèsent également).
        D.add_rect(s, x + 0.05, row_top + top_h, w - 0.10, bot_h - 0.05,
                   fill=NAVY, rounded=True, radius=0.10)
        D.add_text(s, x + pad_x, row_top + 0.07, w - 2 * pad_x, top_h - 0.07, [
            ("ACHAT ALTERNATIF", dict(size=6, bold=True, color=MUTED)),
            (nom, dict(size=8.5, bold=True, color=NAVY, space_before=3, line_spacing=1.05)),
            (apporte, dict(size=7.3, color=NAVY, space_before=4, line_spacing=1.2)),
        ])
        D.add_text(s, x + pad_x, row_top + top_h + 0.08, w - 2 * pad_x, bot_h - 0.08, [
            ("RÉPONSE IAP", dict(size=6, bold=True, color="#8891b3")),
            (manque, dict(size=7.5, bold=True, color=ACCENT, space_before=3, line_spacing=1.1)),
            (reponse, dict(size=7.3, color="#ffffff", space_before=3, line_spacing=1.2)),
        ])

    for i, (fill, label_c, texte_c, label, corps) in enumerate(bandeaux):
        x, w = col_x(i, 2)
        D.add_rect(s, x, band_top, w, band_h, fill=fill, rounded=True, radius=0.08)
        D.add_text(s, x + band_pad + 0.02, band_top + band_pad, w - 2 * band_pad - 0.04,
                   band_h - 2 * band_pad, [
            (label, dict(size=7, bold=True, color=label_c)),
            (corps, dict(size=7, color=texte_c, space_before=3, line_spacing=1.25)),
        ])
    return s


# ---------------------------------------------------------------- slide 4
def slide_gate_ia(prs):
    s = content_slide(prs, "IA", "Les données du client gouvernent le choix du modèle IA", color=ENCRE)
    D.add_text(s, MARGIN, CONTENT_TOP, CONTENT_W, 0.35, [
        ("Checkpoint toujours humain avant tout usage IA sur données client — "
         "iap-ai-data-confidentiality-gate, quel que soit le mode d'exécution retenu.",
         dict(size=D.TYPE["tiny"], color=MUTED, line_spacing=1.2)),
    ])
    rows = [
        ("D0", "Public", "Articles publics, docs méthodo", "IA externe possible"),
        ("D1", "Interne", "Organisation macro, catalogue anonymisé", "IA client recommandée"),
        ("D2", "Confidentiel", "Notes d'interview, reporting, portefeuille", "IA client ou LLM privé"),
        ("D3", "Restreint", "Tickets détaillés, logs, CMDB, IAM", "LLM local, contrôles forts"),
        ("D4", "Critique", "Secrets de production, données réglementées", "Local/on-prem, sans IA générative"),
    ]
    row_top = CONTENT_TOP + 0.45
    row_h = 0.62
    row_gap = 0.1
    label_w = 1.35
    desc_w = 4.2
    usage_w = CONTENT_W - label_w - desc_w - 2 * 0.2
    for i, (code, nom, exemples, usage) in enumerate(rows):
        y = row_top + i * (row_h + row_gap)
        chip(s, MARGIN, y, label_w, row_h, f"{code} · {nom}", SEVERITE[i], size=D.TYPE["tiny"])
        D.add_text(s, MARGIN + label_w + 0.2, y, desc_w, row_h, [
            (exemples, dict(size=D.TYPE["tiny"], color=NAVY, line_spacing=1.1)),
        ], anchor=MSO_ANCHOR.MIDDLE)
        D.add_text(s, MARGIN + label_w + 0.2 + desc_w + 0.2, y, usage_w, row_h, [
            (usage, dict(size=D.TYPE["tiny"], color=MUTED, italic=True, line_spacing=1.1)),
        ], anchor=MSO_ANCHOR.MIDDLE)
    return s


# ---------------------------------------------------------------- slide 5
def slide_why_iap(prs):
    """Nouveau (point ⑤) : OUVRE le chapitre Proposition (la thèse). Le POURQUOI de
    l'Infra-as-a-Product — trois bascules produit, chacune ancrée sur un persona/une
    douleur déjà posés. (2e passe : la maturité est partie au chapitre KPI, le
    sous-chapitre « Technique IAP » a donc disparu — why_iap ouvre la Proposition.)"""
    s = content_slide(prs, "Proposition",
                       "Pourquoi « Infrastructure as a Product » — le socle de la proposition",
                       color=ENCRE)
    claim_h = 0.95
    D.add_rect(s, MARGIN, CONTENT_TOP, CONTENT_W, claim_h, fill=TRACK, rounded=True, radius=0.1)
    D.add_rect(s, MARGIN, CONTENT_TOP, 0.08, claim_h, fill=ENCRE, rounded=True, radius=0.5)
    D.add_text(s, MARGIN + 0.3, CONTENT_TOP, CONTENT_W - 0.5, claim_h, [
        ("Traiter l'infrastructure comme un produit, pas comme un guichet de tickets.",
         dict(size=14, bold=True, color=NAVY, line_spacing=1.05)),
        ("Un produit a des utilisateurs, un cycle de vie et une valeur mesurée — trois bascules "
         "qui répondent directement aux personas et à leurs douleurs.",
         dict(size=9, color=MUTED, space_before=4, line_spacing=1.15)),
    ], anchor=MSO_ANCHOR.MIDDLE)

    piliers = [
        (ENCRE, "Des utilisateurs, pas des tickets",
         "On conçoit l'adoption — self-service, onboarding, parcours — au lieu de subir un "
         "guichet que le contournement rend inutile.",
         "l'Utilisateur applicatif"),
        (ENCRE, "Un cycle de vie, une équipe qui en répond",
         "Le produit a un propriétaire, une roadmap et une dette gérée : on sort du RUN subi "
         "et on récupère de la capacité.",
         "Infra & RUN"),
        (ENCRE, "Un pilotage par la valeur",
         "On mesure l'usage et la valeur produite, pas l'activité : un signal de flux fiable, "
         "des KPIs de mission — pas du reporting-miroir.",
         "Management & Sponsor"),
    ]

    # Refonte graphique (lot 2, ch.05) : les 3 cartes bordées cédaient un effet
    # de simple répétition — remplacées par le pattern deck-design-library #14
    # ("processus en étapes numérotées, colonnes de détail dans UNE carte") :
    # 3 badges numérotés en frise, reliés par un connecteur à UNE carte unique
    # divisée par de fins séparateurs — la forme dit "une seule thèse à 3
    # facettes", pas 3 idées indépendantes. Le motif « légende + chip couleur »
    # reprend celui de slide_douleurs (fil rouge visuel entre les 2 slides).
    n = len(piliers)
    badge_d = 0.32
    connector_h = 0.12
    badge_gap = 0.16
    badge_top = CONTENT_TOP + claim_h + badge_gap
    card_top = badge_top + badge_d + connector_h
    card_h = CONTENT_BOTTOM - card_top
    col_w = CONTENT_W / n
    pad_h = 0.24

    D.add_rect(s, MARGIN, card_top, CONTENT_W, card_h, fill="#ffffff", line=LINE,
               line_w=0.75, rounded=True, radius=0.05)

    corps_size = 9
    corps_lh = corps_size * 1.25 / 72.0
    content_w = col_w - 2 * pad_h
    corps_lines = max(_lignes(p[2], content_w, corps_size) for p in piliers)
    title_h, title_gap, corps_gap, footer_h = 0.34, 0.05, 0.16, 0.42
    corps_h = corps_lines * corps_lh + 0.04
    block_h = title_h + title_gap + corps_h + corps_gap + footer_h
    block_top = card_top + max(0.14, (card_h - block_h) / 2.0)

    for i, (color, titre, corps, ancre) in enumerate(piliers):
        cx = MARGIN + i * col_w
        col_cx = cx + col_w / 2.0
        D.add_dot(s, col_cx - badge_d / 2, badge_top, badge_d, color)
        D.add_text(s, cx, badge_top, col_w, badge_d, [
            (str(i + 1), dict(size=10, bold=True, color="#ffffff", align=PP_ALIGN.CENTER)),
        ], anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
        D.add_rect(s, col_cx - 0.011, badge_top + badge_d, 0.022, connector_h, fill=color)
        if i > 0:
            D.add_rect(s, cx, card_top + 0.16, 0.012, card_h - 0.32, fill=LINE)

        tx = cx + pad_h
        D.add_text(s, tx, block_top, content_w, title_h, [
            (titre, dict(size=D.TYPE["small"], bold=True, color=encre_de(color), line_spacing=1.1)),
        ])
        corps_top = block_top + title_h + title_gap
        D.add_text(s, tx, corps_top, content_w, corps_h, [
            (corps, dict(size=corps_size, color=NAVY, line_spacing=1.25)),
        ])
        footer_top = corps_top + corps_h + corps_gap
        D.add_text(s, tx, footer_top, content_w, 0.14, [
            ("RÉPOND À", dict(size=6.5, bold=True, color=MUTED)),
        ])
        chip(s, tx, footer_top + 0.16, content_w, footer_h - 0.16, ancre, color, size=8)
    return s

# ---------------------------------------------------------------- Besoins & douleurs
# Nouveau (restructuration 2026-07-22) : la grille des 8 familles de gaspillage,
# jusqu'ici empaquetée dans slide_gaspillages avec la chaîne de traitement et le
# score, est isolée ici — elle appartient au chapitre « Besoins & douleurs » (le
# langage commun qui rend une douleur nommable, donc détectable et traitable),
# tandis que la MÉTHODE de traitement (chaîne + score) reste au chapitre
# Proposition. Accent unifié sur la couleur du chapitre Douleurs (PALETTE[2]) :
# les 8 familles se distinguent par leur libellé, pas par 8 teintes sans clé.
# Passe de design 2026-07-23 — règle « un sur N en accent » (principes
# transversaux + pattern 3 du catalogue deck-design-library) : la famille IA,
# seule famille que cette méthode NOMME comme gaspillage (cas gadget,
# automatisation sans garde-fous — la doctrine du deck), reçoit un fill navy
# plein ; les 7 autres restent des cartes blanches identiques.
def slide_familles(prs):
    s = content_slide(prs, "Besoins & douleurs",
                       "Les 8 familles de gaspillage — le langage commun qui rend les douleurs traitables",
                       color=ENCRE)
    D.add_text(s, MARGIN, CONTENT_TOP, CONTENT_W, 0.42, [
        ("Nommer la famille, c'est déjà pouvoir la détecter, la quantifier et la prioriser "
         "(méthode de traitement → chapitre Offre).",
         dict(size=D.TYPE["small"], color=NAVY, italic=True, line_spacing=1.25)),
    ])
    familles = [
        ("Flux", "Attentes, validations multiples"),
        ("Humain", "Experts seniors sur tâches répétitives"),
        ("RUN", "Incidents récurrents, demandes répétées"),
        ("Financier", "Surdimensionnement, ressources non décommissionnées"),
        ("Cognitif", "Trop d'outils, procédures complexes"),
        ("Décisionnel", "Arbitrages subjectifs, priorisation opaque"),
        ("Environnemental", "Ressources inutilisées, environnements non éteints"),
        ("IA", "Cas d'usage gadget, automatisation sans garde-fous"),
    ]
    # 2 colonnes x 4 rangées : remplit la hauteur de la slide dédiée sans étirer
    # chaque carte (défaut « panneau sur-étiré »). Lecture gauche->droite par
    # paire (col = i % 2, row = i // 2).
    n_rows = 4
    region_top = CONTENT_TOP + 0.55
    row_gap = 0.14
    row_h = (CONTENT_BOTTOM - region_top - (n_rows - 1) * row_gap) / n_rows
    for i, (nom, ex) in enumerate(familles):
        col = i % 2
        row = i // 2
        x, w = col_x(col, 2)
        y = region_top + row * (row_h + row_gap)
        accent = (nom == "IA")   # « un sur N » : la famille portée par la doctrine
        if accent:
            D.add_rect(s, x, y, w, row_h, fill=NAVY, rounded=True, radius=0.1)
        else:
            D.add_rect(s, x, y, w, row_h, fill="#ffffff", line=LINE, line_w=0.75,
                       rounded=True, radius=0.1)
        D.add_rect(s, x, y, 0.06, row_h, fill=ENCRE, rounded=True, radius=0.5)
        D.add_text(s, x + 0.2, y + 0.06, w - 0.34, row_h - 0.12, [
            (f"{i + 1}. {nom}", dict(size=D.TYPE["small"], bold=True,
                                     color="#ffffff" if accent else NAVY)),
            (ex, dict(size=8, color="#c7cbe0" if accent else MUTED,
                      space_before=2, line_spacing=1.1)),
        ], anchor=MSO_ANCHOR.MIDDLE)
    return s


# ---------------------------------------------------------------- Proposition
# Reframe (restructuration 2026-07-22) : la grille des 8 familles est partie au
# chapitre « Besoins & douleurs » (slide_familles). Ne reste ici que la MÉTHODE
# de traitement — la chaîne Détecter->Prévenir et le score de priorisation — ré-
# ancrée vers le haut pour combler l'espace libéré par la grille retirée, avec
# une accroche en tête pour éviter un vide sous le titre.
# Passe de design 2026-07-23 : la chaîne, jusqu'ici 10 pilules grises identiques
# en grille 2×5 (effet « tableau de chips »), est redessinée selon le pattern 4
# du catalogue deck-design-library (« flux numéroté en quinconce, badges +
# connecteur, sans cadres ») : badges numérotés reliés par un fil, 2e rangée
# décalée d'un demi-slot, et « un sur N en accent » — seule l'étape 6 (Prioriser)
# est remplie en couleur pleine, car c'est elle qui produit le score détaillé
# dans le panneau navy juste en dessous.
def slide_gaspillages(prs):
    s = content_slide(prs, "Proposition",
                       "Du gaspillage au backlog priorisé : chaîne de traitement + score",
                       color=ENCRE)
    D.add_text(s, MARGIN, CONTENT_TOP, CONTENT_W, 0.5, [
        ("Chaque famille de gaspillage (chapitre précédent) passe par la même chaîne de "
         "traitement, puis reçoit un score explicite qui la classe dans un backlog priorisé "
         "— jamais un tri à l'intuition.",
         dict(size=D.TYPE["small"], color=NAVY, italic=True, line_spacing=1.25)),
    ])

    chain_top = CONTENT_TOP + 0.65
    D.add_text(s, MARGIN, chain_top, CONTENT_W, 0.24, [
        ("CHAÎNE DE TRAITEMENT — de la détection à la prévention",
         dict(size=8, bold=True, color=MUTED))
    ])
    etapes = ["Détecter", "Qualifier", "Quantifier", "Cause racine", "Pattern",
              "Prioriser", "Expérimenter", "Mesurer", "Industrialiser", "Prévenir"]
    step_top = chain_top + 0.34
    n = 5
    slot = CONTENT_W / (n + 0.5)   # 2e rangée décalée d'un demi-slot (quinconce)
    badge_d = 0.32
    unit_h = 0.62                  # badge + libellé
    row_gap2 = 0.10
    accent_idx = 5                 # « Prioriser » — l'étape qui produit le score
    for row in range(2):
        x0 = MARGIN + (slot / 2 if row == 1 else 0.0)
        y = step_top + row * (unit_h + row_gap2)
        cy = y + badge_d / 2
        # fil du flux : connecteur horizontal reliant les badges de la rangée
        D.add_rect(s, x0 + slot / 2, cy - 0.01, (n - 1) * slot, 0.02, fill=LINE)
        for col in range(n):
            i = row * n + col
            accent = (i == accent_idx)
            bx = x0 + col * slot + slot / 2 - badge_d / 2
            D.add_rect(s, bx, y, badge_d, badge_d,
                       fill=ENCRE if accent else "#ffffff",
                       line=None if accent else ENCRE, line_w=1.0,
                       rounded=True, radius=0.5)
            D.add_text(s, bx, y, badge_d, badge_d, [
                (str(i + 1), dict(size=8, bold=True,
                                  color="#ffffff" if accent else ENCRE,
                                  align=PP_ALIGN.CENTER)),
            ], anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
            D.add_text(s, x0 + col * slot, y + badge_d + 0.04, slot, 0.22, [
                (etapes[i], dict(size=8, bold=True,
                                 color=ENCRE if accent else NAVY,
                                 align=PP_ALIGN.CENTER)),
            ], align=PP_ALIGN.CENTER)

    score_top = step_top + 2 * unit_h + row_gap2 + 0.30
    score_h = CONTENT_BOTTOM - score_top - 0.12
    D.add_rect(s, MARGIN, score_top, CONTENT_W, score_h, fill=NAVY, rounded=True, radius=0.08)
    text_w = CONTENT_W * 0.5
    D.add_text(s, MARGIN + 0.22, score_top, text_w - 0.3, score_h, [
        ("Priorité = (impact × faisabilité) − prudence IA",
         dict(size=D.TYPE["small"], bold=True, color="#ffffff", line_spacing=1.15)),
        ("Support de discussion ORDINAL, pas une métrique calculée : à lire en paliers "
         "(fort / moyen / faible), jamais comme un nombre exact. Il rend la discussion "
         "explicite et classe les candidats — il ne remplace pas l'arbitrage humain.",
         dict(size=8, color="#c7cbe0", space_before=4, line_spacing=1.2)),
    ], anchor=MSO_ANCHOR.MIDDLE)

    # Jauge à points — pattern repris de l'autre template analysé
    # (analyse-template-alternatif.md §4) pour illustrer un score 1-5.
    gauge_x = MARGIN + text_w
    gauge_w = CONTENT_W - text_w
    D.add_text(s, gauge_x, score_top + 0.12, gauge_w - 0.15, 0.18, [
        ("SCORE ILLUSTRATIF · ORDINAL", dict(size=7, bold=True, color="#8891b3")),
    ])
    rows_top = score_top + 0.38
    row_h2 = (score_h - 0.38 - 0.1) / 3
    gauge_rows = [
        ("Impact", 4, "#ffffff"),
        ("Faisabilité", 3, ACCENT),
        ("Prudence IA", 1, ACCENT2),
    ]
    for i, (label, score, color) in enumerate(gauge_rows):
        ry = rows_top + i * row_h2
        D.add_text(s, gauge_x, ry, 1.2, row_h2, [
            (label, dict(size=7, color="#c7cbe0")),
        ], anchor=MSO_ANCHOR.MIDDLE)
        dot_scale(s, gauge_x + 1.25, ry + row_h2 / 2 - 0.07, 5, score, color,
                  empty_color="#3a4568")
    return s


# v2.33 (2026-09-10, demande utilisateur) : « une démarche plus centrée sur
# comment traiter le gaspillage comme partagé ». Arbitrage : les DEUX lectures
# à la fois — mutualisé entre équipes (chapitre 03 · Spécificités de l'infra :
# « un gaspillage que personne ne porte, personne ne le réduit ») ET co-traité
# avec le client, pas rendu comme un verdict de consultant.
#
# Cette slide ne remplace pas `slide_gaspillages` : elle la RETOURNE. La chaîne
# des 10 étapes et le score y étaient présentés côté cabinet, de bout en bout —
# ce qui décrit exactement le contraire de ce que la demande vise. On reprend la
# même chaîne, regroupée en trois moments, et on dit qui fait quoi. La colonne
# qui compte est la troisième de chaque bloc : ce qui se tranche À DEUX, seul
# endroit où un gaspillage mutualisé acquiert un porteur.
def slide_gaspillage_partage(prs):
    s = content_slide(prs, "Proposition",
                      "Un gaspillage partagé se traite à deux — sinon il retourne à personne",
                      color=ENCRE)

    # Chapô DIMENSIONNÉ par son texte : posé à une distance fixe, sa 2e ligne
    # mordait sur les pilules de moment (vu au rendu du 2026-09-10 — le
    # self-check géométrique ne voit pas un chevauchement de zones de texte,
    # seulement une forme hors cadre).
    # Deux lignes, MESURÉES (`_lignes`) et non estimées : à trois, le bandeau de
    # clôture chevauchait les colonnes de 0,234in et la garde de fin de fonction
    # refusait le build. Raccourcir la copie plutôt que réduire le corps ou
    # rogner les marges — règle du catalogue de design.
    chapo = ("Cette chaîne se joue AVEC le client, moment par moment. Sans décision "
             "partagée, une économie qui ne pèse sur aucun budget d'équipe ne trouve "
             "pas de porteur.")
    chapo_size = D.TYPE["small"]
    chapo_h = _lignes(chapo, CONTENT_W, chapo_size) * (chapo_size * 1.25 / 72.0) + 0.04
    D.add_text(s, MARGIN, CONTENT_TOP - 0.02, CONTENT_W, chapo_h, [
        (chapo, dict(size=chapo_size, color=NAVY, italic=True, line_spacing=1.25)),
    ])

    moments = [
        ("Objectiver ensemble", "Détecter → Quantifier",
         "Ouvre ses données — CMDB, facturation, tickets — et nomme ce qui le gêne "
         "vraiment, au-delà de ce qui se mesure facilement.",
         "Apporte la grille des 8 familles et la méthode de quantification, sans "
         "présumer du résultat.",
         "Le périmètre mesuré, et ce qu'on accepte d'appeler gaspillage."),
        ("Décider ensemble", "Cause racine → Prioriser",
         "Arbitre entre ses équipes ce qu'aucune ne peut trancher seule : fermer un "
         "service, standardiser, décommissionner.",
         "Instruit les causes racines et propose le score — une proposition argumentée, "
         "jamais un verdict.",
         "Le backlog priorisé et, pour chaque ligne, le porteur nommé."),
        ("Tenir dans la durée", "Expérimenter → Prévenir",
         "Porte les expérimentations dans ses équipes et libère le temps qu'elles "
         "demandent.",
         "Outille, mesure le delta réel et industrialise ce qui a marché.",
         "Le seuil au-delà duquel on généralise — ou on arrête."),
    ]

    n = len(moments)
    gap = 0.18
    col_w = (CONTENT_W - (n - 1) * gap) / n
    pad = 0.13
    tw = col_w - 2 * pad

    chip_h = 0.34
    lbl_h = 0.135
    corps_size = 8
    corps_lh = corps_size * 1.25 / 72.0

    def _h(idx):
        return max(_lignes(m[idx], tw, corps_size) for m in moments) * corps_lh + 0.04

    client_h, octo_h, ens_h = _h(2), _h(3), _h(4)
    sous_titre_h = 0.16

    chip_top = CONTENT_TOP - 0.02 + chapo_h + 0.06
    st_top = chip_top + chip_h + 0.05
    carte_top = st_top + sous_titre_h + 0.06

    # Deux blocs « qui fait quoi », puis le bloc à deux — visuellement détaché
    # par son fond de support et sa barre cyan : c'est l'unique accent de la
    # slide, et il tombe sur ce que la demande visait.
    y_client_lbl = carte_top + pad
    y_client = y_client_lbl + lbl_h
    y_octo_lbl = y_client + client_h + 0.07
    y_octo = y_octo_lbl + lbl_h
    ens_bloc_top = y_octo + octo_h + 0.09
    ens_h_bloc = pad * 0.7 + lbl_h + ens_h + pad * 0.7
    carte_h = (ens_bloc_top + ens_h_bloc + pad) - carte_top

    for i, (titre, etapes, client, octo, ensemble) in enumerate(moments):
        x = MARGIN + i * (col_w + gap)
        chip(s, x, chip_top, col_w, chip_h, f"{i + 1}.  {titre}", ENCRE,
             size=9.5)
        D.add_text(s, x, st_top, col_w, sous_titre_h, [
            (etapes, dict(size=7, bold=True, color=MUTED, align=PP_ALIGN.CENTER)),
        ], align=PP_ALIGN.CENTER)

        D.add_rect(s, x, carte_top, col_w, carte_h, fill=WHITE, line=ENCRE,
                   line_w=1.15, rounded=True, radius=0.09)
        for lbl, texte, y_lbl, y_txt, h_txt in (
                ("CÔTÉ CLIENT", client, y_client_lbl, y_client, client_h),
                ("CÔTÉ OCTO", octo, y_octo_lbl, y_octo, octo_h)):
            D.add_text(s, x + pad, y_lbl, tw, lbl_h, [
                (lbl, dict(size=6.5, bold=True, color=MUTED)),
            ])
            D.add_text(s, x + pad, y_txt, tw, h_txt, [
                (texte, dict(size=corps_size, color=NAVY, line_spacing=1.25)),
            ])

        D.add_rect(s, x + 0.07, ens_bloc_top, col_w - 0.14, ens_h_bloc,
                   fill=SUPPORT, rounded=True, radius=0.07)
        D.add_rect(s, x + 0.14, ens_bloc_top + pad * 0.5, 0.045,
                   ens_h_bloc - pad, fill=ACCENT_PLEIN, rounded=True, radius=0.5)
        D.add_text(s, x + 0.28, ens_bloc_top + pad * 0.7, tw - 0.16, lbl_h, [
            ("TRANCHÉ ENSEMBLE", dict(size=6.5, bold=True, color=ENCRE)),
        ])
        D.add_text(s, x + 0.28, ens_bloc_top + pad * 0.7 + lbl_h, tw - 0.16, ens_h, [
            (ensemble, dict(size=corps_size, bold=True, color=NAVY, line_spacing=1.25)),
        ])

    _bandeau_cloture(
        s,
        ("Ce qui change depuis le chapitre Contexte : le gaspillage "
         "cesse d'être orphelin — il a un porteur nommé et un objectif partagé."),
        carte_top + carte_h + 0.12, "slide_gaspillage_partage")
    return s


# ---------------------------------------------------------------- Besoins & douleurs
# Nouveau (restructuration 2026-07-22) : va PLUS LOIN que slide_personas (qui porte
# un irritant + une attente d'une ligne par persona). Ici chaque douleur est
# approfondie, dotée d'un signal/mesure qui la rend objectivable, et rattachée à
# une ou plusieurs familles de gaspillage — le pont direct vers slide_familles.
# La distinction par couleur d'accent persona d'origine (Infra/Utilisateur/
# Management/Sponsor en teintes propres) a été retirée à la bascule de charte
# du 2026-09-10 (couleur non porteuse de sens). Accent "un sur N" reposé le
# 2026-09-11 sur la seule lane Infra & RUN (cohérence avec slide_personas, qui
# accentue déjà ce persona) — les 3 autres lanes restent ENCRE. Rangées
# dimensionnées à leur contenu.
def slide_douleurs(prs):
    s = content_slide(prs, "Besoins & douleurs",
                       "Les douleurs des clients infra : mesurables, pas des plaintes",
                       color=ENCRE)
    D.add_text(s, MARGIN, CONTENT_TOP, CONTENT_W, 0.4, [
        ("Chaque douleur appartient à un persona et se range dans une famille de gaspillage "
         "— c'est ce qui la rend traitable plutôt que subie.",
         dict(size=8, color=MUTED, italic=True, line_spacing=1.2)),
    ])

    rows = [
        ("Infra & RUN", ACCENT_PLEIN,
         "RUN subi : les mêmes incidents reviennent et mobilisent les experts seniors, le BUILD "
         "est sacrifié à l'astreinte.",
         "Tickets récurrents/mois, part du temps en RUN non maîtrisé.",
         "RUN · Humain"),
        ("Utilisateur applicatif", ENCRE,
         "Aucun self-service ni parcours conçu : tout passe par un guichet, le contournement "
         "(shadow IT) va plus vite que la demande officielle.",
         "Taux de contournement, délai de mise à disposition.",
         "Flux · Cognitif"),
        ("Management", ENCRE,
         "« Expert devenu manager malgré lui » : reporting miroir et micromanagement "
         "compensatoire, faute de signal fiable sur le flux.",
         "Ratio temps reporting / temps résolution d'obstacles.",
         "Décisionnel · Humain"),
        ("Sponsor", ENCRE,
         "Pression à « mettre de l'IA » sans cas d'usage, peur d'une transformation cosmétique : "
         "beaucoup d'activité, peu de valeur démontrée.",
         "Valeur / capacité récupérée démontrée vs promise.",
         "Décisionnel · IA (gadget)"),
    ]

    # Refonte graphique (lot 2, ch.04) : la table Persona/Signal/Famille cédait
    # à l'effet tableau plat — remplacée par un flux diagnostique en 4 lanes
    # verticales (deck-design-library #4, "schéma des N freins en flux
    # numéroté, badge + connecteur") : badge numéroté → connecteur → persona →
    # douleur → signal mesuré → famille(s), plutôt que des colonnes alignées.
    # Hauteurs de bloc calées sur le contenu le PLUS long (pas d'étirement par
    # lane) : chaque étape (douleur, signal) partage la même hauteur dans les
    # 4 lanes pour que badges/connecteurs/chips restent alignés horizontalement.
    n = len(rows)
    lane_gap = 0.16
    lane_w = (CONTENT_W - (n - 1) * lane_gap) / n
    lane_xs = [MARGIN + i * (lane_w + lane_gap) for i in range(n)]
    pad = 0.06
    body_w = lane_w - 2 * pad

    lane_top = CONTENT_TOP + 0.44
    badge_d = 0.5
    connector_h = 0.16
    headline_size = 8.5
    headline_h = 0.34
    douleur_size = 9
    douleur_lh = douleur_size * 1.25 / 72.0
    signal_size = 8
    signal_lh = signal_size * 1.2 / 72.0

    douleur_lines = max(_lignes(r[2], body_w, douleur_size) for r in rows)
    douleur_h = douleur_lines * douleur_lh + 0.04
    signal_lines = max(_lignes(r[3], body_w, signal_size) for r in rows)
    signal_h = signal_lines * signal_lh + 0.04

    badge_top = lane_top
    connector_top = badge_top + badge_d
    headline_top = connector_top + connector_h
    douleur_top = headline_top + headline_h
    signal_label_top = douleur_top + douleur_h + 0.10
    signal_top = signal_label_top + 0.16
    famille_top = signal_top + signal_h + 0.14
    famille_h = 0.3

    for i, (nom, color, douleur, signal, famille) in enumerate(rows):
        x = lane_xs[i]
        cxm = x + lane_w / 2.0
        D.add_dot(s, cxm - badge_d / 2, badge_top, badge_d, color)
        D.add_text(s, x, badge_top, lane_w, badge_d, [
            (str(i + 1), dict(size=13, bold=True, color="#ffffff", align=PP_ALIGN.CENTER)),
        ], anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
        D.add_rect(s, cxm - 0.011, connector_top, 0.022, connector_h, fill=color)
        D.add_text(s, x, headline_top, lane_w, headline_h, [
            (nom, dict(size=headline_size, bold=True, color=encre_de(color),
                       align=PP_ALIGN.CENTER, line_spacing=1.05)),
        ], anchor=MSO_ANCHOR.TOP, align=PP_ALIGN.CENTER)
        D.add_text(s, x + pad, douleur_top, body_w, douleur_h, [
            (douleur, dict(size=douleur_size, color=NAVY, line_spacing=1.25)),
        ])
        D.add_text(s, x + pad, signal_label_top, body_w, 0.14, [
            ("SIGNAL / MESURE", dict(size=6.5, bold=True, color=MUTED)),
        ])
        D.add_text(s, x + pad, signal_top, body_w, signal_h, [
            (signal, dict(size=signal_size, color=MUTED, italic=True, line_spacing=1.2)),
        ])
        chip(s, x + pad, famille_top, body_w, famille_h, famille, color, size=7)

    note_top = famille_top + famille_h + 0.18
    note_h = CONTENT_BOTTOM - note_top
    if note_h > 0.3:
        D.add_rect(s, MARGIN, note_top, CONTENT_W, note_h, fill=TRACK, rounded=True, radius=0.14)
        D.add_rect(s, MARGIN, note_top, 0.07, note_h, fill=ENCRE, rounded=True, radius=0.5)
        D.add_text(s, MARGIN + 0.26, note_top, CONTENT_W - 0.5, note_h, [
            ("Ces 4 douleurs se rangent en 8 familles de gaspillage → slide suivante.",
             dict(size=9, bold=True, color=ENCRE, line_spacing=1.15)),
        ], anchor=MSO_ANCHOR.MIDDLE)
    return s


# ---------------------------------------------------------------- slide 9
def slide_team_topologies(prs):
    s = content_slide(prs, "Proposition", "La cible IAP est une Platform Team — agents IA compris", color=ENCRE)
    D.add_text(s, MARGIN, CONTENT_TOP, CONTENT_W, 0.26, [
        ("Team Topologies décrit 4 archétypes reliés entre eux, pas des silos : les 3 autres "
         "s'articulent tous autour de la Platform Team.",
         dict(size=8, color=MUTED, italic=True, line_spacing=1.15)),
    ])

    # Refonte graphique (lot 2, ch.05) : 4 cartes plates cédaient la place à un
    # diagramme de topologie (deck-design-library situation "Modèle
    # d'organisation cible") — 3 archétypes en frise convergent, par un
    # connecteur en arête, vers la Platform Team en hub accentué ("un sur N en
    # accent") : la FORME dit "un réseau qui converge", pas "4 cases égales".
    # Aucune paire archétype/mode d'interaction n'est assertée par une étiquette
    # (le détail des 3+1 modes reste dans l'encart ci-dessous, texte inchangé)
    # pour ne pas fabriquer une affirmation absente de la source.
    satellites = [
        ("Stream-aligned", ENCRE, "Flux de valeur métier continu",
         "Équipes applicatives clientes de la plateforme infra"),
        ("Enabling", ENCRE, "Montée en compétence temporaire",
         "Posture du coach BMAD IAP — jamais permanente"),
        ("Complicated-subsystem", ENCRE, "Expertise pointue, compétences rares",
         "Un vrai sous-système complexe, pas un produit plateforme classique"),
    ]
    platform = ("Platform", ENCRE, "Capacités en self-service (X-as-a-Service)",
                "La cible même de la transformation IAP")

    n = len(satellites)
    node_top = CONTENT_TOP + 0.36
    node_h = 0.92
    node_bot = node_top + node_h
    stub_h = 0.14
    bus_y = node_bot + stub_h
    trunk_h = 0.32
    platform_top = bus_y + trunk_h
    platform_h = 1.0
    platform_w = 3.6
    platform_x = MARGIN + (CONTENT_W - platform_w) / 2.0
    pad = 0.14

    centers = []
    for i, (titre, color, role, lecture) in enumerate(satellites):
        x, w = col_x(i, n)
        centers.append(x + w / 2.0)
        D.add_card(s, x, node_top, w, node_h, color)
        D.add_text(s, x + pad, node_top, w - 2 * pad, node_h, [
            (titre, dict(size=8.5, bold=True, color=encre_de(color), line_spacing=1.1)),
            (role, dict(size=7.5, color=NAVY, space_before=3, line_spacing=1.1)),
            (lecture, dict(size=7, color=MUTED, italic=True, space_before=3, line_spacing=1.1)),
        ], anchor=MSO_ANCHOR.MIDDLE)

    platform_cx = platform_x + platform_w / 2.0
    # Bus horizontal reliant les 3 archétypes (agrégation neutre), puis tronc
    # unique jusqu'à la Platform Team (coloré à son accent : le flux "devient
    # plateforme" en y entrant).
    D.add_rect(s, min(centers), bus_y - 0.01, max(centers) - min(centers), 0.02, fill=LINE)
    for cx in centers:
        D.add_rect(s, cx - 0.011, node_bot, 0.022, stub_h, fill=LINE)
        D.add_dot(s, cx - 0.035, bus_y - 0.035, 0.07, MUTED)
    D.add_rect(s, platform_cx - 0.014, bus_y, 0.028, trunk_h, fill=ENCRE)
    D.add_text(s, platform_cx - 0.2, platform_top - 0.16, 0.4, 0.16, [
        ("▾", dict(size=9, bold=True, color=ENCRE, align=PP_ALIGN.CENTER)),
    ], anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)

    titre, color, role, lecture = platform
    D.add_rect(s, platform_x, platform_top, platform_w, platform_h, fill=color,
               rounded=True, radius=0.09)
    D.add_text(s, platform_x + 0.3, platform_top, platform_w - 0.6, platform_h, [
        (titre.upper(), dict(size=11, bold=True, color="#ffffff", line_spacing=1.05)),
        (role, dict(size=8.5, color="#ffffff", space_before=4, line_spacing=1.15)),
        (lecture, dict(size=8, bold=True, color="#ffffff", space_before=4, line_spacing=1.15)),
    ], anchor=MSO_ANCHOR.MIDDLE)

    note_top = platform_top + platform_h + 0.16
    note_h = min(1.5, CONTENT_BOTTOM - note_top)
    D.add_rect(s, MARGIN, note_top, CONTENT_W, note_h, fill=TRACK, rounded=True, radius=0.08)
    D.add_text(s, MARGIN + 0.22, note_top, CONTENT_W - 0.44, note_h, [
        ("Extension — les agents IA comme coéquipiers, et leur mise en œuvre (v1.7)",
         dict(size=D.TYPE["tiny"], bold=True, color=NAVY)),
        ("Un agent peut être membre d'une Stream-aligned team ou capacité exposée par la "
         "Platform Team. Aux 3 modes d'interaction Team Topologies — Collaboration, "
         "X-as-a-Service, Facilitating — s'ajoute un 4e candidat : Supervision. "
         "L'adoption suit la trajectoire "
         "Coach → Délégué (assisté → supervisé → délégué) : mandat écrit (ce que l'agent "
         "décide seul / ce qui escalade / qui répond de ses erreurs) avant tout palier "
         "au-delà de l'assisté — jamais un usage qui dérive à l'implicite.",
         dict(size=8, color=NAVY, space_before=3, line_spacing=1.25)),
    ], anchor=MSO_ANCHOR.MIDDLE)
    return s


# ---------------------------------------------------------------- slide 8
# Formes inspirées des slides d'exemple du template lui-même (« Notre
# approche ») : badges circulaires connectés par une ligne, chip de durée,
# description centrée sous chaque étape.
# Nouveau (v2.3) : le schéma de fonctionnement du §Trajectoire de
# bmad-iap-cadrage.md n'avait jusqu'ici qu'un résumé en une ligne dans
# slide_trajectoire (phase ①, "= Schéma de fonctionnement déjà cadré") —
# jamais sa propre slide. Reprend la lecture verticale du schéma ASCII
# source : bandeau Gate IA transversal, 4 colonnes du pipeline, bandeau
# iap-risk-reviewer, bandeau boucle de réévaluation.
def slide_schema_fonctionnement(prs):
    # v2.5 (chantier ④) : déplacée de la Proposition vers la Démarche — c'est
    # « comment la mission tourne », pas ce qu'on propose.
    s = content_slide(prs, "Démarche",
                       "La Gate IA s'applique à chaque étape, de la collecte à la boucle de réévaluation",
                       color=ENCRE)
    D.add_text(s, MARGIN, CONTENT_TOP, CONTENT_W, 0.26, [
        ("Deux sources de collecte convergent vers un diagnostic structuré ; une boucle de "
         "réévaluation referme le cycle.", dict(size=8, color=MUTED, italic=True, line_spacing=1.1)),
    ])

    band_top = CONTENT_TOP + 0.3
    band_h = 0.36
    D.add_rect(s, MARGIN, band_top, CONTENT_W, band_h, fill=NAVY, rounded=True, radius=0.12)
    D.add_text(s, MARGIN + 0.2, band_top, CONTENT_W - 0.4, band_h, [
        ("GATE IA & CONFIDENTIALITÉ — checkpoint humain, transversal à chaque étape qui invoque un LLM",
         dict(size=8, bold=True, color="#ffffff", line_spacing=1.1)),
    ], anchor=MSO_ANCHOR.MIDDLE)

    etapes = [
        ("COLLECTE", ENCRE,
         ["Interviews par persona (trame / thème / question)",
          "Import outils : ServiceNow/Jira/CMDB si accès"]),
        ("DIAGNOSTIC", ENCRE,
         ["Synthèse par thème puis synthèse globale",
          "Registre de gaspillage (tags CONFIRMÉ/DÉDUIT/INCERTAIN)"]),
        ("CONCEPTION", ENCRE,
         ["Définition produit (+ cible MVP)",
          "Operating model + traitement du gaspillage (décisions actées)"]),
        ("RESTITUTION", ENCRE,
         ["Deck exécutif : axes valeur/complexité",
          "+ radar de maturité"]),
    ]
    n = len(etapes)
    col_top = band_top + band_h + 0.16
    card_h = 1.85
    for i, (titre, color, lignes) in enumerate(etapes):
        x, w = col_x(i, n)
        D.add_rect(s, x, col_top, w, 0.05, fill=color)
        D.add_text(s, x, col_top + 0.1, w, 0.26, [
            (titre, dict(size=8, bold=True, color=encre_de(color), align=PP_ALIGN.CENTER)),
        ], align=PP_ALIGN.CENTER)
        card_y = col_top + 0.4
        D.add_rect(s, x, card_y, w, card_h - 0.4, fill=TRACK, rounded=True, radius=0.08)
        lignes_fmt = [(f"·  {l}", dict(size=7, color=NAVY, space_after=4, line_spacing=1.2)) for l in lignes]
        D.add_text(s, x + 0.1, card_y + 0.12, w - 0.2, card_h - 0.4 - 0.24, lignes_fmt,
                   anchor=MSO_ANCHOR.MIDDLE)
        if i < n - 1:
            D.add_text(s, x + w, col_top + 0.08, GAP, 0.26, [
                ("→", dict(size=10, bold=True, color=MUTED, align=PP_ALIGN.CENTER)),
            ], anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)

    reviewer_top = col_top + card_h + 0.16
    reviewer_h = 0.4
    D.add_rect(s, MARGIN, reviewer_top, CONTENT_W, reviewer_h, fill="#ffffff", line=LINE,
               rounded=True, radius=0.1)
    D.add_text(s, MARGIN + 0.2, reviewer_top, CONTENT_W - 0.4, reviewer_h, [
        ("iap-risk-reviewer — lecture seule, challenge Product definition / Operating model → Deck exécutif",
         dict(size=7.5, italic=True, color=MUTED, line_spacing=1.1)),
    ], anchor=MSO_ANCHOR.MIDDLE)

    loop_top = reviewer_top + reviewer_h + 0.14
    loop_h = min(0.55, CONTENT_BOTTOM - loop_top)
    D.add_rect(s, MARGIN, loop_top, CONTENT_W, loop_h, fill=ENCRE, rounded=True, radius=0.1)
    D.add_text(s, MARGIN + 0.2, loop_top, CONTENT_W - 0.4, loop_h, [
        ("⟲ Boucle de réévaluation — iap-strategy-lead, T+6-12 mois, alimente la bibliothèque de REX, "
         "reboucle vers la Collecte", dict(size=8, bold=False, color="#ffffff", line_spacing=1.15)),
    ], anchor=MSO_ANCHOR.MIDDLE)
    return s


# Fusion v2.5 (chantier ①) : slide_trajectoire et slide_schema_bout_en_bout
# déroulaient la même trame ①②③⟲ sur deux slides — fusionnées ici. La ligne de
# badges + durées + actions clés (de l'ancienne trajectoire) est enrichie du
# LIVRABLE-CLÉ par phase en une ligne (l'apport de la vue bout-en-bout — les
# NOMS seulement ; le détail des 4 profils de deck reste à slide_livrables_ppt).
def slide_trajectoire(prs):
    s = content_slide(prs, "Démarche",
                       "Trois temps et une boucle — chaque phase produit son livrable de décision",
                       color=ENCRE)
    phases = [
        ("①", "Assessment flash", "1–2 sem.", ENCRE,
         "= Schéma de fonctionnement déjà cadré (Collecte → Diagnostic → Conception → Restitution).",
         "Deck exécutif de restitution", "Sponsor · comité de lancement"),
        ("②", "Premier déploiement", "4–5 sem.", ENCRE,
         "1-2 équipes pilotes, mode Coach dominant. Piste agent IA (si retenue) : qualifier, cadrer, mandater.",
         "Deck de plan de déploiement · export markdown", "Équipes pilotes · management"),
        ("③", "Implémentation itérative", "→ T+6-12 mois", ENCRE,
         "Généralisation équipe par équipe, bascule Coach → Délégué. Piste agent IA : supervisé puis délégué.",
         "Deck de comité de pilotage (périodique)", "Instance de comitologie"),
        ("⟲", "Boucle de réévaluation", "T+6-12 mois", ENCRE,
         "La réévaluation reboucle vers la Collecte — alimente la bibliothèque de REX.",
         "Deck de bilan / ré-évaluation · markdown amendé", "Sponsor"),
    ]
    n = len(phases)
    badge_d = 0.55
    top0 = CONTENT_TOP + 0.1
    line_y = top0 + badge_d / 2 - 0.012
    D.add_rect(s, MARGIN + badge_d / 2, line_y, CONTENT_W - badge_d, 0.024, fill=LINE)
    _, wcol = col_x(0, n)
    desc_h = max(_lignes(p[4], wcol - 0.1, 7) for p in phases) * (7 * 1.2 / 72.0) + 0.05
    livr_h = (max(_lignes(p[5], wcol - 0.2, 7.5) for p in phases) * (7.5 * 1.2 / 72.0)
              + 0.24 + 0.15)
    for i, (sym, titre, duree, color, desc, livrable, pour_qui) in enumerate(phases):
        x, w = col_x(i, n)
        cx = x + w / 2 - badge_d / 2
        D.add_rect(s, cx, top0, badge_d, badge_d, fill=color, rounded=True, radius=0.5)
        D.add_text(s, cx, top0, badge_d, badge_d, [
            # bold=False pour "⟲" : sa variante grasse manque dans la police du
            # template (rendu LibreOffice = case vide) — ①②③ n'ont pas ce problème.
            (sym, dict(size=16, bold=(sym != "⟲"), color="#ffffff", align=PP_ALIGN.CENTER))
        ], anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
        ty = top0 + badge_d + 0.12
        D.add_text(s, x, ty, w, 0.35, [
            (titre, dict(size=8, bold=True, color=NAVY, align=PP_ALIGN.CENTER, line_spacing=1.05)),
        ], align=PP_ALIGN.CENTER)
        chip_y = ty + 0.36
        chip(s, x + w / 2 - 0.55, chip_y, 1.1, 0.24, duree, color, size=7)
        desc_y = chip_y + 0.34
        D.add_text(s, x + 0.05, desc_y, w - 0.1, desc_h, [
            (desc, dict(size=7, color=MUTED, align=PP_ALIGN.CENTER, line_spacing=1.2)),
        ], align=PP_ALIGN.CENTER)
        # Livrable-clé : le NOM du livrable ET son audience, encadrés au pied
        # de chaque colonne. v2.37 : l'audience vient de slide_livrables_ppt,
        # SUPPRIMÉE — elle redisait les mêmes 4 phases et les mêmes 4 decks pour
        # n'ajouter que cette ligne, au prix d'une 5e slide au squelette ①②③⟲.
        livr_y = desc_y + desc_h + 0.10
        D.add_rect(s, x, livr_y, w, livr_h, fill=TRACK, rounded=True, radius=0.1)
        D.add_text(s, x + 0.1, livr_y, w - 0.2, livr_h, [
            ("LIVRABLE-CLÉ", dict(size=6.5, bold=True, color=MUTED, align=PP_ALIGN.CENTER)),
            (livrable, dict(size=7.5, bold=True, color=encre_de(color), space_before=2,
                            align=PP_ALIGN.CENTER, line_spacing=1.15)),
            (pour_qui, dict(size=6.5, color=MUTED, italic=True, space_before=3,
                            align=PP_ALIGN.CENTER, line_spacing=1.1)),
        ], anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)

    note_top = top0 + badge_d + 0.12 + 0.36 + 0.34 + desc_h + 0.10 + livr_h + 0.18
    note_h = min(1.05, CONTENT_BOTTOM - note_top)
    D.add_rect(s, MARGIN, note_top, CONTENT_W, note_h, fill=TRACK, rounded=True, radius=0.08)
    D.add_text(s, MARGIN + 0.2, note_top, CONTENT_W - 0.4, note_h, [
        ("Bifurcation avec/sans agents IA déployés", dict(size=8, bold=True, color=NAVY)),
        ("Le tronc commun ①→②→③→⟲ ne change pas de structure — la piste agent IA (si retenue) "
         "se greffe sur ②/③ via la démarche d'accompagnement en 5 phases déjà cadrée, plutôt "
         "que d'être un chemin séparé à maintenir. Les 4 livrables-clés ci-dessus sont "
         "4 profils d'un même générateur modulaire, pas 4 outils distincts.",
         dict(size=7, color=NAVY, space_before=3, line_spacing=1.25)),
    ], anchor=MSO_ANCHOR.MIDDLE)
    return s


# --- v2.37 (arbitrage utilisateur du 2026-09-20) : slide_fil_humain et
# slide_fil_technique FUSIONNENT ici. Elles déclinaient la même trame ①②③⟲ sur
# le même gabarit (une carte, 4 colonnes, badge à cheval) à une slide d'écart —
# au rendu réel, deux slides que le lecteur ne distinguait pas, dans un chapitre
# qui enchaînait DÉJÀ cinq fois ce squelette. Les mettre en deux RANGÉES d'une
# même carte dit ce que deux slides ne disaient pas : ces fils sont simultanés,
# pas successifs.
#
# Les pieds de colonne en slugs d'agents (`iap-change-coach · iap-intake`…,
# 8 occurrences) sont SUPPRIMÉS et non traduits : dans un deck sponsor ils
# nommaient des composants internes — dont certains n'existent pas encore.
# L'accroche Kotter (70 %) reste le seul aplat plein de la slide
# (« un sur N en accent »).
_FILS_PHASES = [
    ("①", "ASSESSMENT FLASH"),
    ("②", "PREMIER DÉPLOIEMENT"),
    ("③", "IMPLÉMENTATION ITÉRATIVE"),
    ("⟲", "BOUCLE DE RÉÉVALUATION"),
]

_FIL_HUMAIN = [
    ("Engager",
     "L'engagement du sponsor se construit dès l'intake ; la restitution revient "
     "aux interviewés, pas au seul sponsor."),
    ("Expérimenter",
     "Équipes pilotes volontaires, jamais désignées ; formation sur les cas réels "
     "— « pas de formation sans coaching »."),
    ("Outiller & relayer",
     "Les résistances sont un signal ; relais internes formés — le consultant se "
     "rend dispensable."),
    ("Mesurer",
     "Satisfaction et adhésion au même instrument qu'à T0 — le delta humain à côté "
     "du delta de maturité."),
]

_FIL_TECHNIQUE = [
    ("Cartographier",
     "Dette, plateformes vieillissantes, dépendances non maîtrisées : une base "
     "factuelle, pas une checklist."),
    ("Décommissionner & observer",
     "Sur les pilotes : ce qui peut être décommissionné l'est, l'observabilité du "
     "reste est posée."),
    ("Standardiser & outiller",
     "CI/CD et infra as code deviennent le mode par défaut — la plateforme produit "
     "prend forme."),
    ("Mesurer & réengager",
     "Dette et KPI infra rejoués au même instrument qu'à T0 — le delta technique à "
     "côté des deux autres."),
]


def slide_deux_fils(prs):
    s = content_slide(prs, "Démarche",
                       "Deux fils courent dans les mêmes phases : les personnes et la technique",
                       color=ENCRE)

    # --- Accroche argumentaire : le chiffre Kotter en bloc accent + intro.
    stat_w, stat_h = 1.05, 0.56
    strip_top = CONTENT_TOP + 0.02
    D.add_rect(s, MARGIN, strip_top, stat_w, stat_h, fill=NAVY, rounded=True, radius=0.12)
    D.add_text(s, MARGIN, strip_top, stat_w, stat_h, [
        ("70 %", dict(size=17, bold=True, color="#ffffff", align=PP_ALIGN.CENTER)),
    ], anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
    tx = MARGIN + stat_w + 0.18
    tw = CONTENT_W - stat_w - 0.18
    D.add_text(s, tx, strip_top, tw, stat_h, [
        ("des transformations sont inachevées ou échouent parce que les facteurs humains "
         "et culturels sont mal pris en compte (Kotter, Harvard Business Review).",
         dict(size=8, bold=True, color=NAVY, line_spacing=1.15)),
        # ⟲ en run NON gras (paragraphe italic non-bold) — cf. _GLYPHES_SANS_GRAS.
        ("Aucun des deux n'est un stream séparé : ce sont deux fils DANS les phases "
         "①②③⟲ de la trajectoire, menés en parallèle.",
         dict(size=7.5, italic=True, color=MUTED, space_before=3, line_spacing=1.15)),
    ], anchor=MSO_ANCHOR.MIDDLE)

    n = len(_FILS_PHASES)
    badge_d = 0.42
    pad = 0.14
    lbl_w = 0.82          # gouttiere gauche portant le nom de la rangee
    _, col_w = col_x(0, n, gap=0)

    # Les colonnes partent APRES la gouttiere de libelle : sans ce decalage, la
    # 1re cellule passerait sous « LES PERSONNES » (collision invisible au
    # controle geometrique, qui ne voit que les bords de slide).
    grille_x = MARGIN + lbl_w
    grille_w = CONTENT_W - lbl_w
    cell_w = grille_w / n
    usable = cell_w - 2 * pad

    # Hauteurs derivees du CONTENU, jamais « jusqu'a CONTENT_BOTTOM ».
    h_hum = max(_lignes(t, usable, 7) for _, t in _FIL_HUMAIN) * (7 * 1.25 / 72.0)
    h_tec = max(_lignes(t, usable, 7) for _, t in _FIL_TECHNIQUE) * (7 * 1.25 / 72.0)
    verbe_h = 0.26
    row_h_hum = verbe_h + h_hum + 0.12
    row_h_tec = verbe_h + h_tec + 0.12
    head_h = 0.20
    band_h = 0.62

    top1 = strip_top + stat_h + 0.20 + badge_d / 2
    card_top = top1 + badge_d / 2
    card_h = 0.10 + head_h + row_h_hum + row_h_tec + 0.12

    D.add_rect(s, MARGIN, card_top, CONTENT_W, card_h, fill="#ffffff",
               line=LINE, line_w=0.75, rounded=True, radius=0.06)

    # En-tetes de colonne (badge a cheval sur le bord haut + libelle de phase).
    for i, (sym, phase) in enumerate(_FILS_PHASES):
        x = grille_x + i * cell_w
        if i > 0:
            D.add_rect(s, x, card_top + 0.12, 0.012, card_h - 0.24, fill=LINE)
        cx = x + cell_w / 2 - badge_d / 2
        D.add_rect(s, cx, top1, badge_d, badge_d, fill=ENCRE, rounded=True, radius=0.5)
        D.add_text(s, cx, top1, badge_d, badge_d, [
            # bold=False pour "⟲" : variante grasse absente de la police du
            # template (tofu au rendu) — meme correctif que slide_trajectoire.
            (sym, dict(size=12, bold=(sym != "⟲"), color="#ffffff", align=PP_ALIGN.CENTER)),
        ], anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
        D.add_text(s, x + pad, card_top + 0.10 + badge_d / 2, usable, head_h, [
            (phase, dict(size=6, bold=True, color=MUTED, align=PP_ALIGN.CENTER)),
        ], align=PP_ALIGN.CENTER)

    # Les deux rangees. La rangee « personnes » est teintee (pattern 8 : la
    # teinte distingue une famille sans lire l'etiquette) ; elle reste un aplat
    # pale, jamais un fond porteur de texte cyan.
    y = card_top + 0.10 + head_h + badge_d / 2
    for nom_rangee, contenu, row_h, teinte in (
            ("LES PERSONNES", _FIL_HUMAIN, row_h_hum, TRACK),
            ("LA TECHNIQUE", _FIL_TECHNIQUE, row_h_tec, None)):
        if teinte:
            D.add_rect(s, MARGIN + 0.06, y - 0.04, CONTENT_W - 0.12, row_h, fill=teinte,
                       rounded=True, radius=0.06)
        D.add_text(s, MARGIN + 0.10, y - 0.04, lbl_w - 0.14, row_h, [
            (nom_rangee, dict(size=7, bold=True, color=ENCRE, line_spacing=1.1)),
        ], anchor=MSO_ANCHOR.MIDDLE)
        for i, (verbe, texte) in enumerate(contenu):
            x = grille_x + i * cell_w
            D.add_text(s, x + pad, y, usable, verbe_h, [
                (verbe, dict(size=8.5, bold=True, color=NAVY, line_spacing=1.05)),
            ])
            D.add_text(s, x + pad, y + verbe_h, usable, row_h - verbe_h - 0.08, [
                (texte, dict(size=7, color=NAVY, line_spacing=1.25)),
            ])
        y += row_h

    band_top = card_top + card_h + 0.16
    band_h = min(band_h, CONTENT_BOTTOM - band_top)
    if band_h > 0.3:
        D.add_rect(s, MARGIN, band_top, CONTENT_W, band_h, fill=TRACK, rounded=True, radius=0.08)
        D.add_text(s, MARGIN + 0.2, band_top, CONTENT_W - 0.4, band_h, [
            ("Ce que ces deux fils ne créent pas", dict(size=8, bold=True, color=NAVY)),
            ("Pas de phase en plus, pas de chantier d'architecture à part, et jamais "
             "d'évaluation individuelle des personnes (déontologie du consultant). La "
             "gouvernance sécurité, conformité et résilience opérationnelle reste celle "
             "du client — ces fils s'y arriment, ils ne la remplacent pas.",
             dict(size=7, color=NAVY, space_before=3, line_spacing=1.25)),
        ], anchor=MSO_ANCHOR.MIDDLE)
    else:
        _ANOMALIES_BUILD.append("slide_deux_fils: plus de place pour le bandeau bas")
    return s


# --- Nouveau (v2.6, point ②) : les activités humaines de la démarche, en DEUX
# registres — outillées par IAP vs purement humaines (sans l'outil). Contenu
# ancré dans docs/Import/notes-extraction-scale.md (micro-lancement sponsor,
# ateliers collaboratifs, communauté de managers N+1/N+2, coaching sous
# déontologie, relais internes, présence dégressive) et docs/bmad-iap-cadrage.md
# §Accompagnement de l'humain dans la trajectoire (v2.4) — rien d'inventé.
# Pattern 11 du catalogue deck-design-library (« trajectoire à 4 phases en
# colonnes × lignes de catégorie ») : colonnes = les temps ①②③⟲ (mêmes badges
# et couleurs que slide_trajectoire/slide_fil_humain), lignes = les deux
# registres — bande « avec IAP » teintée cyan pâle (la teinte distingue une
# famille sans lire l'étiquette, pattern 8), bande « sans IAP » blanche à
# contour. Cellules ancrées MIDDLE dans leur bande et hauteurs dérivées du
# contenu (défaut récurrent « panneau sur-étiré », évité d'office).
def slide_activites_humaines(prs):
    s = content_slide(prs, "Démarche",
                       "IAP outille une partie du fil humain — le reste est de la présence de consultant",
                       color=ENCRE)
    D.add_text(s, MARGIN, CONTENT_TOP, CONTENT_W, 0.28, [
        ("Les mêmes quatre temps que la trajectoire : en haut, ce que le consultant fait "
         "avec le module ; en bas, ce qu'il fait sans lui.",
         dict(size=8, color=MUTED, italic=True, line_spacing=1.15)),
    ])

    phases = [
        ("①", "Assessment flash", ENCRE),
        ("②", "Premier déploiement", ENCRE),
        ("③", "Implémentation itérative", ENCRE),
        ("⟲", "Boucle de réévaluation", ENCRE),
    ]
    avec_iap = [
        ["Trames d'interview par persona, versées à la Collecte",
         "La restitution s'appuie sur le deck exécutif généré",
         "Sondage humain de référence (T0)"],
        ["Deck de plan de déploiement · export markdown (1re version)"],
        ["Comité de pilotage : deck périodique, santé humaine incluse"],
        ["KPI humain rejoué au même instrument : delta T0 → réévaluation",
         "Export markdown amendé · deck de bilan"],
    ]
    sans_iap = [
        ["Le sponsor présente lui-même l'ambition (micro-lancement)",
         "Restitution-embarquement : feedback des interviewés"],
        ["Équipes pilotes volontaires, ateliers co-construits",
         "Formation sur les cas réels — pas de formation sans coaching"],
        ["Communauté de managers, N+1/N+2 embarqués",
         "Coaching individuel sous déontologie · relais internes formés"],
        ["Présence dégressive : le consultant se rend dispensable",
         "Lecture du delta humain avec les équipes"],
    ]

    label_w = 1.05
    grid_x0 = MARGIN + label_w + 0.12
    grid_w = BORD_DROIT - grid_x0
    n = 4
    col_gap = 0.08
    col_w = (grid_w - (n - 1) * col_gap) / n

    def _col_px(i):
        return grid_x0 + i * (col_w + col_gap)

    # En-têtes de phase : badge rond + nom, centrés par colonne (⟲ jamais en
    # gras — cf. _GLYPHES_SANS_GRAS, même correctif que slide_trajectoire).
    head_top = CONTENT_TOP + 0.34
    badge_d = 0.26
    for i, (sym, nom, color) in enumerate(phases):
        x = _col_px(i)
        cx = x + col_w / 2 - badge_d / 2
        D.add_rect(s, cx, head_top, badge_d, badge_d, fill=color, rounded=True, radius=0.5)
        D.add_text(s, cx, head_top, badge_d, badge_d, [
            (sym, dict(size=9, bold=(sym != "⟲"), color="#ffffff", align=PP_ALIGN.CENTER)),
        ], anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
        D.add_text(s, x, head_top + badge_d + 0.02, col_w, 0.16, [
            (nom, dict(size=6.5, bold=True, color=encre_de(color), align=PP_ALIGN.CENTER)),
        ], align=PP_ALIGN.CENTER)

    # Hauteur de bande dérivée du CONTENU (colonne la plus fournie).
    cell_usable = col_w - 0.16
    line_h = 7 * 1.2 / 72.0

    def _band_h(cells):
        return max(sum(_lignes(t, cell_usable, 7) for t in c) * line_h
                   + (len(c) - 1) * 0.06 for c in cells) + 0.24

    bands_top = head_top + badge_d + 0.24
    note_h = 0.34
    hA = _band_h(avec_iap)
    hB = _band_h(sans_iap)
    # Le mou vertical restant se répartit DANS les bandes (cellules centrées),
    # pas en vide sous la grille.
    slack = max(0.0, (CONTENT_BOTTOM - note_h - 0.12) - (bands_top + hA + 0.10 + hB))
    hA += slack / 2
    hB += slack / 2

    registres = [
        (bands_top, hA, "AVEC IAP", "outillé par le module", "#E1FDFA", None, avec_iap),
        (bands_top + hA + 0.10, hB, "SANS IAP", "présence du consultant", "#ffffff", LINE, sans_iap),
    ]
    for top, h, label, sous, fill, line, cells in registres:
        D.add_rect(s, MARGIN, top, CONTENT_W, h, fill=fill, line=line, line_w=0.75,
                   rounded=True, radius=0.06)
        D.add_text(s, MARGIN + 0.12, top, label_w - 0.12, h, [
            (label, dict(size=8, bold=True, color=NAVY, line_spacing=1.1)),
            (sous, dict(size=6.5, color=MUTED, italic=True, space_before=2, line_spacing=1.1)),
        ], anchor=MSO_ANCHOR.MIDDLE)
        D.add_rect(s, grid_x0 - 0.10, top + 0.10, 0.012, h - 0.20, fill=LINE)
        for i, items in enumerate(cells):
            x = _col_px(i)
            if i > 0:  # séparateurs fins (pattern 11 : la grille sans le tableau)
                D.add_rect(s, x - col_gap / 2, top + 0.10, 0.012, h - 0.20, fill=LINE)
            lignes_fmt = [(t, dict(size=7, color=NAVY, line_spacing=1.2,
                                   space_before=(4 if j else 0)))
                          for j, t in enumerate(items)]
            D.add_text(s, x + 0.08, top + 0.08, col_w - 0.16, h - 0.16, lignes_fmt,
                       anchor=MSO_ANCHOR.MIDDLE)

    note_top = CONTENT_BOTTOM - note_h
    D.add_text(s, MARGIN, note_top, CONTENT_W, note_h, [
        ("La rangée du bas ne s'outille pas : c'est la présence du consultant — dégressive, "
         "jusqu'aux relais internes qui portent le modèle après la mission (offre SCALE, transposée).",
         dict(size=8, color=MUTED, italic=True, line_spacing=1.2)),
    ], anchor=MSO_ANCHOR.BOTTOM)
    return s


# --- Nouveau (2026-09-01) : conditions de réussite et non-engagement. Le deck
# ne disait nulle part ce que la mission EXIGE du client ni ce qui la fait
# échouer — un sponsor destinataire ne pouvait pas savoir à quoi il s'engage.
# Prolonge (sans la répéter) la phrase du fil humain « testé dès l'intake ».
# Forme retenue (deck-design-library) : chaîne verticale de conditions reliées
# par un connecteur + encart de mise en exergue latéral (pattern 6) — la
# colonne porte le processus, le panneau porte le message, ici l'issue
# NÉGATIVE. Bandeau transverse en pied pour le critère de sortie (l.949).
# Matière : cadrage l.934 (non-engagement), l.951 (test à l'intake, RH),
# l.172 (anti-patterns), l.455 (deskilling-risk), l.667 (management-posture-risk).
def slide_conditions_reussite(prs):
    s = content_slide(prs, "Démarche",
                       "Quatre conditions de réussite de la démarche",
                       color=ENCRE)
    couleur = ENCRE

    def lh(pt):
        return pt * 1.25 / 72.0

    lead = ("Nos convictions fixent les conditions dans lesquelles la démarche réussit — "
            "et ce qu'elle refuse de faire, même quand on le lui demande.")
    lead_h = _lignes(lead, CONTENT_W, 9.5) * lh(9.5) + 0.06
    D.add_text(s, MARGIN, CONTENT_TOP, CONTENT_W, lead_h, [
        (lead, dict(size=9.5, color=NAVY, italic=True, line_spacing=1.25)),
    ])

    # --- Bandeau transverse (critère de sortie, l.949) : dimensionné d'abord,
    # la région centrale prend le reste — jamais l'inverse.
    sortie = ("L'équipe et ses relais tiennent-ils le modèle une période sans le consultant ? "
              "Le consultant se rend dispensable : il n'évalue jamais les personnes, ne fait "
              "pas le reporting à leur place et ne s'installe pas en intermédiaire permanent "
              "entre l'équipe et le sponsor.")
    band_pad = 0.12
    band_h = 2 * band_pad + lh(7) + 0.04 + _lignes(sortie, CONTENT_W - 0.28, 7) * lh(7) + 0.03
    band_top = CONTENT_BOTTOM - band_h

    region_top = CONTENT_TOP + lead_h + 0.10
    region_h = band_top - 0.16 - region_top

    # --- Colonne gauche : les 4 conditions, en chaîne -----------------------
    conditions = [
        ("Un sponsor qui porte la cible",
         "La transformation ne va pas plus loin que ce que le sponsor peut porter : son "
         "engagement se construit dès l'intake, il ne se suppose pas."),
        ("Des équipes réellement disponibles",
         "Interviews et ateliers supposent du temps réservé — la disponibilité réelle se "
         "vérifie à l'intake, jamais en cours de mission."),
        ("Une RH embarquée sur rôles et évaluation",
         "« Frein ou principal accélérateur » : coacher une posture que les grilles "
         "d'évaluation punissent revient à ramer contre le système."),
        ("Un processus documenté avant tout agent",
         "Sinon on fige une pratique mal définie dans du code — préalable non négociable de "
         "la doctrine d'automatisation."),
    ]
    gauche_w = 3.65
    fil_x = MARGIN + 0.13
    badge_d = 0.26
    card_x = MARGIN + 0.26
    card_w = MARGIN + gauche_w - card_x
    card_pad = 0.14
    card_usable = card_w - 0.08 - 2 * card_pad
    card_gap = 0.09
    card_h = (region_h - (len(conditions) - 1) * card_gap) / len(conditions)

    # Connecteur continu : une seule ligne, pas de flèches (pattern 6).
    D.add_rect(s, fil_x - 0.01, region_top + card_h / 2, 0.02,
               (len(conditions) - 1) * (card_h + card_gap), fill=LINE)
    for i, (titre, corps) in enumerate(conditions):
        y = region_top + i * (card_h + card_gap)
        D.add_card(s, card_x, y, card_w, card_h, couleur)
        D.add_rect(s, fil_x - badge_d / 2, y + card_h / 2 - badge_d / 2, badge_d, badge_d,
                   fill=couleur if i == 0 else "#ffffff",
                   line=None if i == 0 else couleur, line_w=1.0, rounded=True, radius=0.5)
        D.add_text(s, fil_x - badge_d / 2, y + card_h / 2 - badge_d / 2, badge_d, badge_d, [
            (str(i + 1), dict(size=8, bold=True,
                              color="#ffffff" if i == 0 else couleur,
                              align=PP_ALIGN.CENTER)),
        ], anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
        D.add_text(s, card_x + 0.08 + card_pad, y, card_usable, card_h, [
            (titre, dict(size=8, bold=True, color=couleur, line_spacing=1.05)),
            (corps, dict(size=7, color=NAVY, space_before=3, line_spacing=1.25)),
        ], anchor=MSO_ANCHOR.MIDDLE)

    # --- Panneau droit : l'issue négative (le seul aplat plein de la slide) --
    pan_x = MARGIN + gauche_w + 0.24
    pan_w = BORD_DROIT - pan_x
    pad = 0.16
    tw = pan_w - 2 * pad

    chip_l, chip_h = 1.42, 0.22
    accroche = ("Nos convictions disent aussi ce que la démarche ne fera pas.")
    nuance = ("Ce ne sont pas des conditions posées au client : ce sont les lignes que "
              "la démarche tient, et qu'elle explique dès l'Assessment flash.")
    refus = ["Automatiser un processus mal conçu",
             "Livrer une plateforme techniquement bonne mais peu adoptée",
             "Séparer transformation organisationnelle et technique"]
    risques = [
        ("deskilling-risk — perte de la capacité tacite",
         "L'équipe saurait-elle reprendre la main une semaine sans l'agent ?"),
        ("management-posture-risk — incitations RH contraires",
         "Qu'est-ce qui, dans vos grilles d'évaluation, récompense encore le comportement "
         "qu'on vient de décourager ?"),
    ]
    b1_h = (chip_h + 0.06 + _lignes(accroche, tw, 9) * lh(9) + 0.04
            + _lignes(nuance, tw, 7.5) * lh(7.5))
    b2_h = (lh(7) + 0.03 + sum(_lignes(r, tw - 0.14, 7) for r in refus) * lh(7)
            + (len(refus) - 1) * 0.03)
    b3_h = (lh(7) + 0.03
            + sum(_lignes(a, tw, 7) + _lignes(b, tw, 7) for a, b in risques) * lh(7)
            + (len(risques) - 1) * 0.05)

    # Panneau dimensionné à SON contenu (le mou part dans les interlignes de
    # blocs, jamais en vide au pied du panneau).
    gap_int = 0.14
    contenu_h = 2 * pad + b1_h + b2_h + b3_h + 2 * gap_int
    slack = region_h - contenu_h
    if slack > 0:
        gap_int += min(slack / 2.0, 0.18)
        contenu_h = 2 * pad + b1_h + b2_h + b3_h + 2 * gap_int
    pan_h = min(region_h, contenu_h)
    pan_top = region_top + max(0.0, (region_h - pan_h) / 2.0)

    D.add_rect(s, pan_x, pan_top, pan_w, pan_h, fill=NAVY, rounded=True, radius=0.08)
    y = pan_top + pad
    # Pastille CYAN sur le panneau navy : en `ENCRE` elle etait navy sur navy,
    # donc invisible, et son texte blanc flottait seul. Texte en navy parce
    # que du blanc sur cyan ne vaut que 1,86:1.
    D.add_rect(s, pan_x + pad, y, chip_l, chip_h, fill=ACCENT_PLEIN, rounded=True, radius=0.5)
    D.add_text(s, pan_x + pad, y, chip_l, chip_h, [
        ("NOS REFUS", dict(size=7, bold=True, color=NAVY, align=PP_ALIGN.CENTER)),
    ], anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
    D.add_text(s, pan_x + pad, y + chip_h + 0.06, tw, b1_h - chip_h - 0.06, [
        (accroche, dict(size=9, bold=True, color="#ffffff", line_spacing=1.15)),
        (nuance, dict(size=7.5, color="#c7cbe0", space_before=3, line_spacing=1.25)),
    ])

    y += b1_h + gap_int
    D.add_rect(s, pan_x + pad, y - gap_int / 2, tw, 0.012, fill="#3a4568")
    D.add_text(s, pan_x + pad, y, tw, lh(7), [
        ("CE QU'ON REFUSE DE FAIRE — LES ANTI-PATTERNS DU CADRAGE",
         dict(size=7, bold=True, color="#8891b3")),
    ])
    ry = y + lh(7) + 0.03
    for r in refus:
        n = _lignes(r, tw - 0.14, 7)
        D.add_dot(s, pan_x + pad + 0.02, ry + 0.04, 0.05, ACCENT)
        D.add_text(s, pan_x + pad + 0.14, ry, tw - 0.14, n * lh(7), [
            (r, dict(size=7, color="#ffffff", line_spacing=1.25)),
        ])
        ry += n * lh(7) + 0.03

    y += b2_h + gap_int
    D.add_rect(s, pan_x + pad, y - gap_int / 2, tw, 0.012, fill="#3a4568")
    D.add_text(s, pan_x + pad, y, tw, lh(7), [
        ("CE QU'ON NE RÉSOUT PAS — MAIS QU'ON CONSIGNE ET QU'ON POSE",
         dict(size=7, bold=True, color="#8891b3")),
    ])
    ry = y + lh(7) + 0.03
    for nom, question in risques:
        n = _lignes(nom, tw, 7) + _lignes(question, tw, 7)
        D.add_text(s, pan_x + pad, ry, tw, n * lh(7), [
            # Sur PANNEAU NAVY : blanc, comme l'accroche au-dessus. `ENCRE`
            # ici valait navy sur navy — 1,00:1, libelle invisible.
            (nom, dict(size=7, bold=True, color="#ffffff", line_spacing=1.25)),
            (question, dict(size=7, color="#c7cbe0", line_spacing=1.25)),
        ])
        ry += n * lh(7) + 0.05

    D.add_rect(s, MARGIN, band_top, CONTENT_W, band_h, fill=TRACK, rounded=True, radius=0.08)
    D.add_text(s, MARGIN + band_pad + 0.02, band_top + band_pad, CONTENT_W - 0.28,
               band_h - 2 * band_pad, [
        ("LE CRITÈRE DE SORTIE EST LE MIROIR DES CONDITIONS D'ENTRÉE",
         dict(size=7, bold=True, color=MUTED)),
        (sortie, dict(size=7, color=NAVY, space_before=3, line_spacing=1.25)),
    ])
    return s


# slide_livrables_ppt SUPPRIMÉE (v2.37, arbitrage utilisateur du 2026-09-20).
# Elle redisait les 4 mêmes phases et les 4 mêmes decks que slide_trajectoire,
# sur le même squelette ①②③⟲ — 5e slide consécutive à ce gabarit dans le
# chapitre Démarches, d'où le « on ne voit pas l'idée directrice » remonté par
# l'utilisateur. Sa seule matière propre, l'AUDIENCE de chaque livrable, est
# reprise dans l'encadré livrable-clé de slide_trajectoire (champ `pour_qui`).
# Dernier état complet : git show avant le commit v2.37.


# Nouveau — brainstorm de design (v2.2) : reprend le pattern « cadre blanc »
# du template (déjà utilisé dans le REX "⛱️ L'Été de l'IA", VSCode1, en
# alternance gauche/droite pour chaque slide de contenu) — claim + puces à
# gauche, illustration encadrée à droite.
# Révisé (restructuration 2026-07-22) : slide 3 est l'énoncé de problème qui ouvre
# le deck — 3 puces d'une seule colonne vertébrale ancrées dans l'utilisateur
# (le constat → ce que ça coûte → ce qu'un bon diagnostic exige). La puce
# « l'IA amplifie l'organisation » a été RETIRÉE : elle est implicite dans la
# puce 2 et son point de doctrine est développé au chapitre IA. Le
# titre et l'image encadrée (sunset, cadre round2DiagRect) sont conservés.
def slide_vision(prs):
    """Slide 3 — la thèse qui lance le deck. Passe design 2026-07-23 : le pavé
    de 3 puces longues (dernier mur de texte du deck) devient un enchaînement
    vertical constat → coût → exigence (deck-design-library, pattern 6 « flux
    vertical connecté » transposé) : badges numérotés reliés par une ligne,
    un bloc par idée, kicker + claim + détail. « Un sur N en accent »
    (pattern 7) : le bloc 3 — LA thèse (partir des utilisateurs réels, pas
    d'une réponse toute faite) — est le seul en fond navy, mêmes teintes que
    la carte RÉSULTAT de l'executive summary (#8fd6db / #c7cbe0) pour rester
    dans le langage visuel déjà en place. Photo + cadre inchangés."""
    layout = prs.slide_masters[0].slide_layouts[LAYOUT_VISUEL_DROITE]
    s = prs.slides.add_slide(layout)
    phs = {ph.placeholder_format.idx: ph for ph in s.placeholders}

    phs[0].text_frame.text = ("Le risque n'est pas de manquer d'outils : "
                               "c'est de traiter le mauvais problème")
    for p in phs[0].text_frame.paragraphs:
        for r in p.runs:
            r.font.color.rgb = _rgb(NAVY)
    # Le corps est dessiné en blocs absolus — le placeholder BODY du layout
    # resterait un textframe vide par-dessus les cartes, on le retire.
    ph_body = phs[1]._element
    ph_body.getparent().remove(ph_body)

    # Les 3 blocs passent tous ENCRE — la distinction bleu/rouge/navy d'origine
    # a été retirée à la bascule de charte du 2026-09-10 (comment corrigé le
    # 2026-09-11). Le 3e bloc (l'exigence — la thèse) reste seul en fill navy
    # plein (`accent = i == len(blocs)-1`, un sur N) : c'est LUI qui porte la
    # mise en avant désormais, pas une couleur sémantique par bloc.
    blocs = [
        ("LE CONSTAT", ENCRE,
         "Une infrastructure guichet ou centre de coûts subit la demande au lieu "
         "de la piloter.",
         "Ni utilisateurs identifiés, ni feuille de route, ni levier d'adoption."),
        ("CE QUE ÇA COÛTE", ENCRE,
         "La capacité disponible part en gaspillage.",
         "RUN subi (l'exploitation quotidienne), ressources orphelines, seniors "
         "sur du répétitif — et le réflexe « plus d'outils » ou « mettons de "
         "l'IA » aggrave le mal."),
        ("CE QU'UN BON DIAGNOSTIC EXIGE", NAVY,
         "Partir des utilisateurs réels et de leurs douleurs — pas d'une réponse "
         "toute faite.",
         "Le fil que déroulent tous les chapitres qui suivent."),
    ]

    # Colonne de gauche : s'arrête net avant le cadre photo (groupe du layout
    # à x=6.857in) — badges à la marge, cartes décalées à droite de la chaîne.
    badge_d = 0.34
    chain_cx = MARGIN + badge_d / 2
    card_x = MARGIN + 0.50
    card_w = 6.63 - card_x
    text_x = card_x + 0.22
    usable = card_w - 0.22 - 0.18
    kicker_h, gap_blocs = 0.20, 0.22

    # Hauteur de chaque bloc = son contenu (pas de panneau sur-étiré). Le
    # cpi_ref par défaut de l'estimateur (11.0) sous-estime nettement la
    # police du template sur cette largeur (mesuré au rendu réel : ~15-16
    # équivalent 10.5pt) — 14.0 garde une marge de sécurité sans laisser
    # 0.3in de vide sous la ligne de détail des cartes (défaut vu au zoom).
    def _est(texte, taille):
        return max(1, D.estimer_lignes(texte, usable, taille, cpi_ref=14.0))

    dims = []
    for _, _, claim, detail in blocs:
        claim_h = _est(claim, 10.5) * (10.5 * 1.2 / 72.0) + 0.04
        detail_h = _est(detail, 9) * (9 * 1.3 / 72.0) + 0.04
        h = 0.13 + kicker_h + claim_h + 0.07 + detail_h + 0.13
        dims.append((h, claim_h, detail_h))

    top0 = 1.40
    tops, y = [], top0
    for h, _, _ in dims:
        tops.append(y)
        y += h + gap_blocs

    # La chaîne : UNE ligne verticale continue sous les badges (pattern 6 —
    # pas de flèches), du centre du bloc 1 au centre du bloc 3.
    c1 = tops[0] + dims[0][0] / 2
    c3 = tops[2] + dims[2][0] / 2
    D.add_rect(s, chain_cx - 0.01, c1, 0.02, c3 - c1, fill=LINE)

    for i, ((label, color, claim, detail), (h, claim_h, detail_h), top) in \
            enumerate(zip(blocs, dims, tops, strict=True)):
        accent = (i == len(blocs) - 1)   # « un sur N » : l'exigence, la thèse
        if accent:
            D.add_rect(s, card_x, top, card_w, h, fill=NAVY, rounded=True, radius=0.06)
            D.add_rect(s, card_x, top, 0.07, h, fill=ACCENT, rounded=True, radius=0.5)
        else:
            D.add_card(s, card_x, top, card_w, h, color)
        D.add_text(s, text_x, top + 0.13, usable, kicker_h, [
            (label, dict(size=8, bold=True, color="#8fd6db" if accent else color)),
        ])
        D.add_text(s, text_x, top + 0.13 + kicker_h, usable, claim_h, [
            (claim, dict(size=10.5, bold=True, color="#ffffff" if accent else NAVY,
                         line_spacing=1.2)),
        ])
        D.add_text(s, text_x, top + 0.13 + kicker_h + claim_h + 0.07, usable, detail_h, [
            (detail, dict(size=9, color="#c7cbe0" if accent else MUTED,
                          line_spacing=1.3)),
        ])
        # Badge numéroté sur la chaîne, centré sur son bloc.
        by = top + h / 2 - badge_d / 2
        D.add_rect(s, chain_cx - badge_d / 2, by, badge_d, badge_d,
                   fill=color, rounded=True, radius=0.5)
        D.add_text(s, chain_cx - badge_d / 2, by, badge_d, badge_d, [
            (str(i + 1), dict(size=11, bold=True, color="#ffffff",
                              align=PP_ALIGN.CENTER)),
        ], anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)

    cadre = _find_frame_in_group(s.slide_layout.shapes, "Google Shape;212;p17", "Google Shape;213;p17")
    for pb in frame_obstructions(s, *cadre[:4]) if cadre else []:
        print("  [obstruction] vision:", pb["source"], pb["name"], pb["reason"])
    _remplir_cadre(s, cadre, "sunset", seed=1)
    return s


# (v2.5 — slide_schema_bout_en_bout supprimée, chantier ① : sa trame ①②③⟲
# doublonnait slide_trajectoire ; son apport — le livrable-clé par phase — est
# fusionné dans slide_trajectoire ci-dessus.)


# ---------------------------------------------------------------- slide 10
# Nouveau (v2.0) : la bifurcation "avec/sans agent IA" de slide_trajectoire
# gagne un livrable concret, distinct des 4 decks PPT — un markdown pour
# l'équipe qui exécute, pas pour le sponsor. Deux cartes (mêmes proportions
# que slide_mission) + un bandeau de routage + une note "pas un aller simple".
def slide_export_markdown(prs):
    s = content_slide(prs, "IA",
                       "Export markdown — agentic ou documentation, selon le contexte client (piste à valider)",
                       color=ENCRE)
    # v2.6 (point ④) : badge de série (comme les 3 slides d'agent candidat) —
    # l'intro cède la largeur du badge. Le renvoi aux 4 decks vise le chapitre
    # Démarche (slide_livrables_ppt y a déménagé en v2.5 — la mention
    # « Proposition » était restée, corrigée ici).
    badge_deploiement_agentic(s)
    D.add_text(s, MARGIN, CONTENT_TOP, CONTENT_W - BADGE_AGENTIC_W - 0.2, 0.5, [
        ("Pas un 5e deck PPT : un livrable markdown pour l'équipe qui exécute (versionnable, "
         "committable) — les 4 decks du chapitre Démarches restent pour sponsor et comité de pilotage.",
         dict(size=8, color=MUTED, italic=True, line_spacing=1.2)),
    ])

    cards = [
        ("DOCUMENTATION-FIRST", ENCRE,
         "Agentic Readiness [0]-[1], données D3-D4 sans LLM local, ou score de gaspillage faible.",
         "Runbook du processus", "iap-adoption-plan"),
        ("AGENTIC-IMPLEMENTATION", ENCRE,
         "Agentic Readiness [2]-[3], données D0-D2 (ou D3-D4 avec LLM local), score positif.",
         "Plan d'implémentation agentic", "iap-agentic-opportunities"),
    ]
    # v2.6 : +0.13 — l'intro, rétrécie par le badge de série, passe à 3 lignes.
    top0 = CONTENT_TOP + 0.55
    card_h = 1.55
    for i, (titre, color, quand, fichier, owner) in enumerate(cards):
        x, w = col_x(i, 2)
        D.add_card(s, x, top0, w, card_h, color)
        pad = 0.2
        D.add_text(s, x + pad, top0 + 0.14, w - 2 * pad, 0.3, [
            (titre, dict(size=D.TYPE["h3"], bold=True, color=encre_de(color))),
        ])
        D.add_text(s, x + pad, top0 + 0.5, w - 2 * pad, 0.55, [
            ("QUAND", dict(size=D.TYPE["tiny"], bold=True, color=MUTED)),
            (quand, dict(size=8, color=NAVY, space_before=2, line_spacing=1.2)),
        ])
        D.add_text(s, x + pad, top0 + 1.08, w - 2 * pad, 0.4, [
            ("LIVRABLE · OWNER", dict(size=7, bold=True, color=MUTED)),
            (f"{fichier} — {owner}", dict(size=8, bold=True, color=NAVY, space_before=2)),
        ])

    signals_top = top0 + card_h + 0.15
    signals_h = 0.55
    signals = [
        ("PILIER AGENTIC READINESS", "[0-1] → documentation · [2-3] → agentic"),
        ("DONNÉES (GATE IA)", "D3-D4 sans LLM local → doc · D0-D2 → agentic"),
        ("SCORE DE GASPILLAGE", "faible/négatif → doc · positif → agentic"),
    ]
    for i, (label, mapping) in enumerate(signals):
        x, w = col_x(i, 3)
        D.add_rect(s, x, signals_top, w, signals_h, fill=TRACK, rounded=True, radius=0.1)
        D.add_text(s, x + 0.12, signals_top + 0.06, w - 0.24, signals_h - 0.12, [
            (label, dict(size=7, bold=True, color=NAVY)),
            (mapping, dict(size=7, color=MUTED, space_before=2, line_spacing=1.15)),
        ])

    note_top = signals_top + signals_h + 0.15
    note_h = min(1.05, CONTENT_BOTTOM - note_top)
    D.add_rect(s, MARGIN, note_top, CONTENT_W, note_h, fill=NAVY, rounded=True, radius=0.08)
    D.add_text(s, MARGIN + 0.22, note_top, CONTENT_W - 0.44, note_h, [
        ("Pas un aller simple", dict(size=D.TYPE["tiny"], bold=True, color="#ffffff")),
        ("À chaque boucle de réévaluation, le même fichier est amendé — jamais dupliqué — sur le "
         "modèle du registre de risques IA : un client documentation-first peut basculer en agentic si "
         "son Agentic Readiness progresse, et inversement en cas de perte de compétence avérée.",
         dict(size=8, color="#c7cbe0", space_before=4, line_spacing=1.25)),
    ], anchor=MSO_ANCHOR.MIDDLE)
    return s


# --- Nouveau (v2.6, point ③) : le schéma d'architecture de fonctionnement
# d'IAP en contexte client — joue aussi le rôle de la slide « ce que le module
# met dans les mains du consultant » annoncée par le plan v2.5 et jamais
# écrite. Trois zones (pattern 8 du catalogue deck-design-library : des zones
# teintées qui se saisissent sans lire les étiquettes) reliées par un
# vocabulaire de flèches uniforme (pattern 9) : le POSTE DU CONSULTANT (le
# module — 4 étapes aux couleurs de slide_schema_fonctionnement, 11 agents,
# gate confidentialité bloquant en bandeau navy comme slide_architecture_agents),
# le CONTEXTE CLIENT (sponsor/équipes + SI selon l'ambition A/B/C des slides
# SUIVANTES), et entre les deux les FLUX (collecte entrante, livrables
# sortants, agents retenus). La zone « déploiement agentic chez le client »
# est le seul bloc en aplat plein (« un sur N en accent »), violet
# ENCRE = encre navy — le chapitre IA ne se signale plus par sa teinte
# posé sur les 4 slides de proposition agentic (point ④).
def slide_iap_contexte_client(prs):
    s = content_slide(prs, "Outillage IAP",
                       "IAP tourne sur le poste du consultant — seuls les agents retenus passent chez le client",
                       color=ENCRE)
    D.add_text(s, MARGIN, CONTENT_TOP, CONTENT_W, 0.30, [
        ("Rien ne s'installe côté client par défaut : les interviews et les exports entrent, "
         "les livrables sortent — le déploiement d'agents est une décision de ②/③, pas un prérequis.",
         dict(size=8, color=MUTED, italic=True, line_spacing=1.15)),
    ])

    z_top = CONTENT_TOP + 0.40
    z_h = 2.90
    cons_x, cons_w = MARGIN, 3.30
    flux_x, flux_w = cons_x + cons_w + 0.12, 1.30
    cli_x = flux_x + flux_w + 0.12
    cli_w = BORD_DROIT - cli_x
    pad = 0.16

    # --- Zone 1 : poste du consultant (le module IAP).
    D.add_rect(s, cons_x, z_top, cons_w, z_h, fill=TRACK, rounded=True, radius=0.06)
    D.add_text(s, cons_x + pad, z_top + 0.12, cons_w - 2 * pad, 0.42, [
        ("POSTE DU CONSULTANT", dict(size=8, bold=True, color=NAVY)),
        ("Le module IAP · 11 workflows outillés", dict(size=7, color=MUTED, space_before=2)),
    ])
    etapes = [("COLLECTE", ENCRE), ("DIAGNOSTIC", ENCRE),
              ("CONCEPTION", ENCRE), ("RESTITUTION", ENCRE)]
    pill_w = (cons_w - 2 * pad - 0.10) / 2
    pill_h = 0.30
    pills_top = z_top + 0.60
    for i, (nom, color) in enumerate(etapes):
        px = cons_x + pad + (i % 2) * (pill_w + 0.10)
        py = pills_top + (i // 2) * (pill_h + 0.08)
        chip(s, px, py, pill_w, pill_h, nom, color, size=6.5)
    caption_top = pills_top + 2 * pill_h + 0.08 + 0.10
    D.add_text(s, cons_x + pad, caption_top, cons_w - 2 * pad, 0.40, [
        ("Mêmes étapes que le schéma de fonctionnement (chapitre Démarches) — "
         "fonctionne aussi sans IA externe si le gate l'impose (mode M0).",
         dict(size=6.5, color=MUTED, italic=True, line_spacing=1.2)),
    ])
    gate_h = 0.62
    gate_top = z_top + z_h - gate_h - 0.12
    D.add_rect(s, cons_x + pad - 0.04, gate_top, cons_w - 2 * pad + 0.08, gate_h,
               fill=NAVY, rounded=True, radius=0.10)
    D.add_text(s, cons_x + pad + 0.08, gate_top, cons_w - 2 * pad - 0.16, gate_h, [
        ("GATE CONFIDENTIALITÉ — BLOQUANT", dict(size=7, bold=True, color="#ffffff")),
        ("Classe la donnée (D0-D4) avant tout usage IA sur donnée client",
         dict(size=6.5, color="#c7cbe0", space_before=2, line_spacing=1.15)),
    ], anchor=MSO_ANCHOR.MIDDLE)

    # --- Zone 2 (milieu) : les flux — vocabulaire de flèches uniforme, une
    # flèche par ligne, cyan = données de la mission, violet = agents déployés.
    flux = [
        ("←", ACCENT, "COLLECTE ENTRANTE", "interviews · exports d'outils"),
        ("→", ACCENT, "LIVRABLES SORTANTS", "deck exécutif · export markdown"),
        ("→", ENCRE, "AGENTS RETENUS (②/③)", "supervisés puis délégués"),
    ]
    f_h = 0.72
    f_gap = (z_h - 3 * f_h) / 2
    for i, (fleche, color, label, detail) in enumerate(flux):
        fy = z_top + i * (f_h + f_gap)
        D.add_text(s, flux_x, fy, flux_w, 0.30, [
            (fleche, dict(size=16, bold=True, color=encre_de(color), align=PP_ALIGN.CENTER)),
        ], anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
        D.add_text(s, flux_x - 0.06, fy + 0.30, flux_w + 0.12, f_h - 0.30, [
            (label, dict(size=6.5, bold=True, color=NAVY, align=PP_ALIGN.CENTER, line_spacing=1.1)),
            (detail, dict(size=6, color=MUTED, space_before=1, align=PP_ALIGN.CENTER, line_spacing=1.1)),
        ], align=PP_ALIGN.CENTER)

    # --- Zone 3 : contexte client.
    D.add_rect(s, cli_x, z_top, cli_w, z_h, fill="#ffffff", line=LINE, line_w=1.0,
               rounded=True, radius=0.06)
    D.add_text(s, cli_x + pad, z_top + 0.12, cli_w - 2 * pad, 0.24, [
        ("CONTEXTE CLIENT", dict(size=8, bold=True, color=NAVY)),
    ])
    bloc_x = cli_x + pad
    bloc_w = cli_w - 2 * pad
    b1_top = z_top + 0.42
    D.add_rect(s, bloc_x, b1_top, bloc_w, 0.55, fill=TRACK, rounded=True, radius=0.10)
    D.add_text(s, bloc_x + 0.12, b1_top, bloc_w - 0.24, 0.55, [
        ("SPONSOR & ÉQUIPES INTERVIEWÉES", dict(size=7, bold=True, color=NAVY)),
        ("les voix du diagnostic — interviews par persona",
         dict(size=6.5, color=MUTED, space_before=1, line_spacing=1.15)),
    ], anchor=MSO_ANCHOR.MIDDLE)
    b2_top = b1_top + 0.55 + 0.10
    b2_h = 0.72
    D.add_rect(s, bloc_x, b2_top, bloc_w, b2_h, fill=TRACK, rounded=True, radius=0.10)
    D.add_text(s, bloc_x + 0.12, b2_top, bloc_w - 0.24, b2_h, [
        ("SI CLIENT", dict(size=7, bold=True, color=NAVY)),
        ("ServiceNow · Jira · Confluence · Datadog · CMDB · FinOps — accès selon "
         "l'ambition A/B/C (slides suivantes)",
         dict(size=6.5, color=MUTED, space_before=1, line_spacing=1.15)),
    ], anchor=MSO_ANCHOR.MIDDLE)
    # Zone mise en évidence — le seul aplat plein du schéma (« un sur N »).
    b3_top = b2_top + b2_h + 0.12
    b3_h = z_top + z_h - 0.14 - b3_top
    D.add_rect(s, bloc_x, b3_top, bloc_w, b3_h, fill=ENCRE, rounded=True, radius=0.10)
    D.add_text(s, bloc_x + 0.12, b3_top, bloc_w - 0.24, b3_h, [
        ("DÉPLOIEMENT AGENTIC CHEZ LE CLIENT", dict(size=7, bold=True, color="#ffffff")),
        ("Les agents candidats retenus se déploient ici en ②/③ — supervisés puis délégués",
         dict(size=6.5, color="#CFD3DD", space_before=2, line_spacing=1.2)),
    ], anchor=MSO_ANCHOR.MIDDLE)

    # --- Renvoi de focus (point ④a) : même langage visuel que le badge de
    # série posé sur les 4 slides visées — liseré violet, renvoi par CHAPITRE.
    band_top = z_top + z_h + 0.16
    band_h = min(0.66, CONTENT_BOTTOM - band_top)
    D.add_rect(s, MARGIN, band_top, CONTENT_W, band_h, fill="#ffffff",
               line=ENCRE, line_w=1.0, rounded=True, radius=0.10)
    D.add_text(s, MARGIN + 0.2, band_top, CONTENT_W - 0.4, band_h, [
        ("QUATRE PROPOSITIONS DE DÉPLOIEMENT AGENTIC — DÉTAILLÉES AU CHAPITRE OFFRE",
         dict(size=7, bold=True, color=ENCRE)),
        ("Agent de triage RUN · veille FinOps · agent documentaire (RAG) · export markdown "
         "(qui porte la décision agentic/documentation) — chacune porte le badge "
         "« déploiement agentic chez le client ».",
         dict(size=7, color=NAVY, space_before=2, line_spacing=1.2)),
    ], anchor=MSO_ANCHOR.MIDDLE)
    return s


# ---------------------------------------------------------------- slide 11
def slide_ambition(prs):
    # v2.5 (chantier ④) : déplacée de la Proposition vers l'Outillage IAP —
    # le niveau d'ambition qualifie l'outil, pas la proposition de transformation.
    s = content_slide(prs, "Outillage IAP", "Trois niveaux d'ambition, pas un spectre linéaire", color=ENCRE)
    niveaux = [
        ("A", "Aide au coach", ENCRE,
         "Génère un livrable à la demande — aucune initiative propre. Le consultant pilote à 100 %.",
         "État actuel du cadrage (MVP0–MVP5)"),
        ("B", "Assistant interactif", ENCRE,
         "Guide pas à pas, pose des questions de clarification, signale les incohérences.",
         "Palier intermédiaire, entre MVP5 et MVP6"),
        ("C", "Companion connecté", ENCRE,
         # « quasi autonome » seul survendait C comme une autonomie décisionnelle,
         # ce que le cadrage (l.733) demande explicitement d'éviter.
         "Connecté en direct à ServiceNow/Jira/Confluence/Datadog/CMDB/FinOps : quasi "
         "autonome sur la collecte et la préparation — jamais sur l'arbitrage.",
         "= MVP6, non engagé"),
    ]
    n = 3
    pad = 0.2
    _, wcol = col_x(0, n)
    usable = wcol - 2 * pad
    # Légende roadmap collée SOUS le texte de rôle (au lieu d'un y fixe en bas
    # de carte) et carte plafonnée à son contenu : supprime le « trou mort »
    # entre le rôle et la légende, et le sur-étirement de la carte (slide 26).
    # Passe de design 2026-07-23 — pattern 7 du catalogue deck-design-library
    # (« un sur N en accent ») : le niveau A, ÉTAT ACTUEL assumé du cadrage
    # (cf. executive summary, posture de gouvernance), est la seule carte en
    # fill navy plein — B et C restent des cartes blanches identiques.
    role_lines = max(_lignes(niv[3], usable, 8) for niv in niveaux)
    role_h = role_lines * (8 * 1.25 / 72.0) + 0.06
    roadmap_y = 0.55 + role_h + 0.12
    card_h = roadmap_y + 0.28 + 0.14
    top0 = CONTENT_TOP + 0.45
    accent_idx = 0   # A · Aide au coach — l'état actuel
    for i, (code, titre, color, role, roadmap) in enumerate(niveaux):
        x, w = col_x(i, n)
        accent = (i == accent_idx)
        if accent:
            D.add_rect(s, x, top0, w, card_h, fill=NAVY, rounded=True, radius=0.06)
            # Lisere CYAN sur la carte accentuee : en `color` (= ENCRE) il
            # etait navy sur navy, donc la carte mise en avant etait la
            # SEULE sans marqueur visible.
            D.add_rect(s, x, top0, 0.07, card_h, fill=ACCENT_PLEIN, rounded=True, radius=0.5)
        else:
            D.add_card(s, x, top0, w, card_h, color)
        D.add_text(s, x + pad, top0 + 0.15, w - 2 * pad, 0.35, [
            (f"{code} · {titre}", dict(size=D.TYPE["small"], bold=True,
                                       color="#ffffff" if accent else color)),
        ])
        D.add_text(s, x + pad, top0 + 0.55, w - 2 * pad, role_h, [
            (role, dict(size=8, color="#e8ebf5" if accent else NAVY, line_spacing=1.25)),
        ])
        D.add_text(s, x + pad, top0 + roadmap_y, w - 2 * pad, 0.3, [
            (roadmap, dict(size=8, bold=True, color="#ffffff" if accent else MUTED)),
        ])

    note_top = top0 + card_h + 0.18
    note_h = CONTENT_BOTTOM - note_top
    D.add_text(s, MARGIN, note_top, CONTENT_W, note_h, [
        ("Monter de A à C n'est pas qu'une question de fonctionnalités : le niveau C suppose "
         "un accès direct aux données de production du client — risque sécurité/confidentialité "
         "d'un tout autre ordre. Un cabinet peut durablement rester au niveau A ou B par choix "
         "de gouvernance, pas seulement par contrainte technique transitoire. "
         "MVP0–6 = jalons de la roadmap de mise en œuvre ; MVP6, le « companion connecté », n'est pas engagé.",
         dict(size=8, color=MUTED, italic=True, line_spacing=1.3)),
    ])
    return s


_ICONES_FAMILLE_AGENT = {
    "RUN": MSO_SHAPE.GEAR_6,
    "Financier": MSO_SHAPE.CLOUD,
    "Cognitif": MSO_SHAPE.FOLDED_CORNER,
}


# --- v2.37 (arbitrage utilisateur du 2026-09-20, demande « plus lisible ») :
# les 3 appels de slide_agent_ia produisaient 3 slides au gabarit IDENTIQUE
# (médaillon + spine verticale + 3 pilules), chacune à ~40 % vide. Vu au rendu
# réel, le lecteur ne les distinguait pas : c'est le défaut « cartes uniformes /
# on ne voit pas l'idée directrice » remonté par l'utilisateur. Les trois
# candidats tiennent en UNE slide à 3 colonnes — la comparaison devient
# possible, ce que 3 slides successives interdisaient. Copie resserrée au
# passage (même substance, moins de mots) et le slug technique du gate retiré
# de la note au profit de « gate confidentialité » : un deck sponsor ne porte
# pas les noms internes du module.
_AGENTS_CANDIDATS = [
    ("Agent de triage de tickets", "RUN",
     "Les mêmes tickets reviennent depuis des années et mobilisent des seniors "
     "sur du répétitif à faible valeur.",
     "Lit chaque ticket, le classe selon un runbook déjà documenté, le route vers "
     "la bonne équipe. Le processus doit être explicite AVANT l'agent — jamais "
     "l'inverse.",
     "Jusqu'à 15 tickets/mois sans intervention humaine, temps de triage divisé "
     "par deux (cas nominal du cadrage)."),
    ("Agent de veille FinOps", "Financier",
     "Les ressources cloud surdimensionnées ou orphelines n'apparaissent qu'aux "
     "audits ponctuels — le gaspillage s'accumule entre deux revues.",
     "Scanne en continu la CMDB et la facturation, repère l'inactif et le "
     "surdimensionné, propose une liste à valider — ne décommissionne jamais seul.",
     "Coût récupéré directement mesurable — un KPI de mission déjà cadré."),
    ("Agent documentaire (RAG)", "Cognitif",
     "Trop d'outils, procédures dispersées : retrouver l'information ralentit les "
     "équipes et sollicite toujours les mêmes experts.",
     "Indexe runbooks, wikis et tickets résolus, répond aux questions fréquentes "
     "avec la source citée — jamais de réponse sans preuve.",
     "Charge cognitive réduite, onboarding plus rapide, moins d'interruptions des "
     "experts seniors."),
]


def slide_agents_candidats(prs):
    s = content_slide(prs, "IA", "Trois candidats d'agent, un par famille de gaspillage",
                      color=ENCRE)
    badge_deploiement_agentic(s)

    D.add_text(s, MARGIN, CONTENT_TOP, CONTENT_W - BADGE_AGENTIC_W - 0.2, 0.34, [
        ("Le gaspillage d'abord, l'IA ensuite : chaque candidat répond à une famille "
         "déjà cadrée au chapitre Douleur — aucun n'est inventé pour l'occasion.",
         dict(size=9, color=MUTED, italic=True, line_spacing=1.2)),
    ])

    note = ("Ces 3 candidats restent soumis au scoring et au gate confidentialité "
            "(tous deux dans ce chapitre) avant toute décision — des exemples "
            "illustratifs, pas une liste actée.")
    note_h = 0.34
    top = CONTENT_TOP + 0.46
    bas = CONTENT_BOTTOM - note_h - 0.12

    gap = 0.24
    col_w = (CONTENT_W - gap * 2) / 3.0
    icon_d = 0.30
    txt_size = 8
    line_h = txt_size * 1.25 / 72.0
    lbl_h = 0.16

    for i, (nom, famille, why, what, gain) in enumerate(_AGENTS_CANDIDATS):
        x = MARGIN + i * (col_w + gap)
        icon = s.shapes.add_shape(_ICONES_FAMILLE_AGENT[famille], Inches(x),
                                  Inches(top), Inches(icon_d), Inches(icon_d))
        try:
            icon.shadow.inherit = False
        except Exception:
            pass
        icon.fill.solid()
        icon.fill.fore_color.rgb = _rgb(ENCRE)
        icon.line.fill.background()
        icon.text_frame.paragraphs[0].text = ""
        D.add_text(s, x + icon_d + 0.12, top - 0.02, col_w - icon_d - 0.12, icon_d + 0.04, [
            (nom, dict(size=10, bold=True, color=NAVY, line_spacing=1.05)),
            ("Gaspillage " + famille, dict(size=7.5, color=MUTED, italic=True, space_before=1)),
        ], anchor=MSO_ANCHOR.MIDDLE)

        # Ce qui sépare les 3 candidats est la POSITION et le filet, jamais une
        # couleur d'accent par famille (charte du 2026-09-10 : la couleur ne
        # porte pas le sens).
        y = top + icon_d + 0.22
        D.add_rect(s, x, y - 0.10, col_w, 0.014, fill=ENCRE)

        for label, texte in (("POURQUOI", why), ("CE QUE FAIT L'AGENT", what), ("GAIN", gain)):
            D.add_text(s, x, y, col_w, lbl_h, [
                (label, dict(size=7, bold=True, color=ENCRE)),
            ])
            n_lignes = _lignes(texte, col_w, txt_size)
            h = n_lignes * line_h + 0.04
            D.add_text(s, x, y + lbl_h, col_w, h, [
                (texte, dict(size=txt_size, color=NAVY, line_spacing=1.22)),
            ])
            y += lbl_h + h + 0.12

        if y > bas:
            _ANOMALIES_BUILD.append(
                f"slide_agents_candidats: colonne {i + 1} deborde ({y:.2f} > {bas:.2f})")

    D.add_text(s, MARGIN, CONTENT_BOTTOM - note_h, CONTENT_W, note_h, [
        (note, dict(size=8, color=MUTED, italic=True, line_spacing=1.2)),
    ])
    return s


# --- Nouveau (brainstorm) : la formule de priorisation (chapitre Proposition)
# cite "prudence IA" sans jamais l'expliquer — cette slide la décompose. Dans le
# chapitre IA, juste après le gate IA (qui l'a rejoint) et avant les 3 candidats
# d'agent : on pose d'abord le frein, ensuite seulement les cas d'usage.
#
# Refonte graphique lot 3/4 (audit design, ch.06) : les 3 facteurs ne sont pas
# 3 items juxtaposés, ils s'ADDITIONNENT en un seul score (déjà dit par le
# sous-titre) — 3 cartes plates isolées ne montrait pas cette composition.
# Nouvelle forme : UNE carte à colonnes (pattern 14 du catalogue
# deck-design-library) avec des badges numérotés chevauchant son bord haut
# (pattern 10, déjà utilisé par slide_fil_humain — cohérence intra-deck) et
# des signes « + » posés sur les séparateurs internes ; la carte se prolonge
# vers un chip « = SCORE DE PRUDENCE IA » qui introduit l'encart d'explication
# — la lecture verticale devient littéralement l'équation du sous-titre.
def slide_prudence_ia(prs):
    s = content_slide(prs, "IA", "La prudence IA est un frein chiffré, pas un veto", color=ENCRE)
    D.add_text(s, MARGIN, CONTENT_TOP, CONTENT_W, 0.4, [
        ("Prudence IA = confidentialité + besoin de supervision + criticité de la décision",
         dict(size=D.TYPE["small"], bold=True, color=NAVY, line_spacing=1.2)),
    ])

    facteurs = [
        ("1", "CONFIDENTIALITÉ", ENCRE,
         "Reprend directement la classification du gate IA (D0-D4, slide précédente) — "
         "plus la donnée est sensible, plus le score monte."),
        ("2", "BESOIN DE SUPERVISION", ENCRE,
         "Le palier d'adoption visé (assisté / supervisé / délégué) — un agent encore "
         "au stade assisté pèse plus lourd qu'un agent déjà éprouvé."),
        ("3", "CRITICITÉ DE LA DÉCISION", ENCRE,
         "L'impact d'une erreur si l'agent se trompe seul — une recommandation "
         "réversible pèse moins qu'une décision irréversible."),
    ]
    n = len(facteurs)
    badge_d = 0.42
    pad = 0.16
    col_w = CONTENT_W / n
    usable = col_w - 2 * pad

    # Hauteurs dérivées du CONTENU (jamais « jusqu'à CONTENT_BOTTOM »).
    label_h = 0.36
    body_lines = max(_lignes(t, usable, 8) for _, _, _, t in facteurs)
    body_h = body_lines * (8 * 1.25 / 72.0) + 0.04
    card_h = badge_d / 2 + 0.10 + label_h + 0.05 + body_h + 0.14

    top1 = CONTENT_TOP + 0.55
    card_top = top1 + badge_d / 2
    D.add_rect(s, MARGIN, card_top, CONTENT_W, card_h, fill="#ffffff",
               line=LINE, line_w=0.75, rounded=True, radius=0.06)

    for i, (num, label, color, texte) in enumerate(facteurs):
        x = MARGIN + i * col_w
        if i > 0:
            D.add_rect(s, x, card_top + 0.14, 0.012, card_h - 0.28, fill=LINE)
            # Les facteurs s'ADDITIONNENT — un « + » à cheval sur le
            # séparateur, à hauteur des badges, pas une simple liste côte à côte.
            D.add_text(s, x - 0.18, top1 - 0.02, 0.36, badge_d + 0.04, [
                ("+", dict(size=16, bold=True, color=MUTED, align=PP_ALIGN.CENTER)),
            ], anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
        cx = x + col_w / 2 - badge_d / 2
        D.add_rect(s, cx, top1, badge_d, badge_d, fill=color, rounded=True, radius=0.5)
        D.add_text(s, cx, top1, badge_d, badge_d, [
            (num, dict(size=13, bold=True, color="#ffffff", align=PP_ALIGN.CENTER)),
        ], anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
        label_y = top1 + badge_d + 0.10
        D.add_text(s, x + pad, label_y, usable, label_h, [
            (label, dict(size=8, bold=True, color=encre_de(color), align=PP_ALIGN.CENTER, line_spacing=1.1)),
        ], align=PP_ALIGN.CENTER)
        text_y = label_y + label_h + 0.02
        D.add_text(s, x + pad, text_y, usable, body_h, [
            (texte, dict(size=8, color=NAVY, line_spacing=1.25)),
        ])

    # Convergence visuelle : les 3 termes ci-dessus = un score, explicité par
    # l'encart en dessous — pas un simple bloc de conclusion posé à côté.
    card_bottom = card_top + card_h
    pill_w, pill_h = 2.7, 0.32
    pill_x = MARGIN + CONTENT_W / 2 - pill_w / 2
    pill_y = card_bottom + 0.14
    D.add_rect(s, pill_x, pill_y, pill_w, pill_h, fill=ENCRE, rounded=True, radius=0.5)
    D.add_text(s, pill_x, pill_y, pill_w, pill_h, [
        ("=  SCORE DE PRUDENCE IA", dict(size=8.5, bold=True, color="#ffffff", align=PP_ALIGN.CENTER)),
    ], anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)

    note_top = pill_y + pill_h + 0.14
    note_texte = ("Le score est SOUSTRAIT de impact × faisabilité — les trois scores sont "
                  "ordinaux (un rang, pas une mesure absolue, même statut que le score "
                  "d'impact) : un candidat facile et à fort impact peut quand même être "
                  "écarté si sa prudence IA est trop "
                  "haute. Le score ne remplace pas l'arbitrage humain : il le rend "
                  "explicite. Avancer malgré un score élevé reste possible, mais se documente comme une "
                  "décision à part entière (même discipline que la dérogation du gate DevOps).")
    note_lines = _lignes(note_texte, CONTENT_W - 0.44, 8)
    note_h = min(0.20 + note_lines * (8 * 1.25 / 72.0) + 0.28, CONTENT_BOTTOM - note_top)
    D.add_rect(s, MARGIN, note_top, CONTENT_W, note_h, fill=NAVY, rounded=True, radius=0.08)
    D.add_text(s, MARGIN + 0.22, note_top, CONTENT_W - 0.44, note_h, [
        ("Un frein, pas un veto automatique", dict(size=D.TYPE["tiny"], bold=True, color="#ffffff")),
        (note_texte, dict(size=8, color="#c7cbe0", space_before=3, line_spacing=1.25)),
    ], anchor=MSO_ANCHOR.MIDDLE)
    return s


# --- Nouveau (brainstorm) : comment le tronc commun se branche concrètement
# sur le SI du client, et ce que ça change selon le niveau d'ambition déjà
# cadré (slide précédente) — synthèse d'éléments déjà posés (§Ambition de
# l'outil, §Solution technique envisagée), pas une nouvelle doctrine.
def slide_architecture_si(prs):
    # v2.5 (chantier ④) : déplacée de la Proposition vers l'Outillage IAP, avec
    # slide_ambition (qui reste la slide précédente).
    #
    # Refonte graphique lot 4/4 (audit design, ch.08) : le tableau plat
    # NIVEAU/SOURCES/CONNEXION/LIVRABLES cédait à l'effet tableau — l'index
    # situation de deck-design-library mappe justement « Architecture / vision
    # en couches » sur le pattern #8 (blueprint en bandes teintées). Chaque
    # niveau A/B/C devient une bande pleine largeur teintée (badge-lettre au
    # lieu d'une cellule de texte). La correspondance de couleur A/B/C avec
    # slide_ambition (bleu/or/rouge) a été retirée à la bascule de charte du
    # 2026-09-10 (couleur non porteuse de sens). Accent "un sur N" repositionné
    # le 2026-09-11 sur le seul niveau A (ACCENT_PLEIN), pour la même raison de
    # cohérence que l'accent de slide_ambition sur ce même niveau — sans
    # réintroduire un code couleur par niveau. Volontairement AUCUN connecteur/flèche entre
    # les bandes : slide_ambition affirme explicitement « pas un spectre
    # linéaire » et cette slide dit qu'un cabinet peut rester durablement au
    # niveau A/B — un fil descendant aurait suggéré une progression forcée que
    # la doctrine dément.
    s = content_slide(prs, "Outillage IAP",
                       "Le lien avec le SI du client change avec le niveau d'ambition, pas la méthode",
                       color=ENCRE)
    rows = [
        ("A", ACCENT_PLEIN, "Aide au coach",
         "Exports ponctuels (ServiceNow/Jira), interviews",
         "Aucune — tout est apporté par le consultant",
         "Markdown + deck, à la demande"),
        ("B", ENCRE, "Assistant interactif",
         "Exports + App companion (capture terrain)",
         "Site web centralisé, orchestration assistée",
         "+ tableau de bord multi-engagements"),
        ("C", ENCRE, "Companion connecté (non engagé)",
         "ServiceNow/Jira/Confluence/Datadog/CMDB/FinOps",
         "Connecteurs API directs, en continu",
         "Livrables mis à jour en continu"),
    ]
    champs = ["SOURCES", "MODE DE CONNEXION", "LIVRABLES"]

    accent_w = 0.06
    badge_d = 0.42
    left_w = 1.95
    badge_cx = MARGIN + accent_w + 0.16 + badge_d / 2
    text_x = badge_cx + badge_d / 2 + 0.14
    text_w = MARGIN + left_w - text_x
    field_x0 = MARGIN + left_w + 0.18
    field_gap = 0.16
    field_w = (CONTENT_W - left_w - 0.18 - 2 * field_gap) / 3
    field_pad = 0.16
    usable_field = field_w - 2 * field_pad
    label_h = 0.16
    body_size = 8
    body_lh = body_size * 1.25 / 72.0
    band_pad_y = 0.16

    band_hs = []
    for (_code, _color, _niveau, sources, connexion, livrables) in rows:
        lignes = max(_lignes(t, usable_field, body_size) for t in (sources, connexion, livrables))
        contenu_h = label_h + 0.03 + lignes * body_lh
        band_hs.append(max(badge_d + 2 * band_pad_y, contenu_h + 2 * band_pad_y))

    row_gap = 0.16
    note_h = 0.5
    note_gap = 0.16
    total = sum(band_hs) + 2 * row_gap + note_gap + note_h
    top0 = CONTENT_TOP + max(0.03, (CONTENT_H - total) / 2)

    y = top0
    for i, (code, color, niveau, sources, connexion, livrables) in enumerate(rows):
        band_h = band_hs[i]
        pale = _pale(color, 0.14)
        D.add_rect(s, MARGIN, y, CONTENT_W, band_h, fill=pale, rounded=True, radius=0.08)
        D.add_rect(s, MARGIN, y, accent_w, band_h, fill=color, rounded=True, radius=0.5)
        cy = y + band_h / 2
        _badge(s, badge_cx, cy, badge_d, color, code, size=14)
        D.add_text(s, text_x, y, text_w, band_h, [
            (f"NIVEAU {code}", dict(size=6.5, bold=True, color=MUTED)),
            (niveau, dict(size=9, bold=True, color=encre_de(color), space_before=2, line_spacing=1.1)),
        ], anchor=MSO_ANCHOR.MIDDLE)
        D.add_rect(s, MARGIN + left_w, y + band_pad_y, 0.012, band_h - 2 * band_pad_y, fill=LINE)
        valeurs = [sources, connexion, livrables]
        for j, (label, val) in enumerate(zip(champs, valeurs, strict=True)):
            x = field_x0 + j * (field_w + field_gap)
            if j > 0:
                D.add_rect(s, x - field_gap / 2, y + band_pad_y, 0.012,
                           band_h - 2 * band_pad_y, fill=LINE)
            D.add_text(s, x, y + band_pad_y, field_w, band_h - 2 * band_pad_y, [
                (label, dict(size=6.5, bold=True, color=MUTED)),
                (val, dict(size=body_size, color=NAVY, space_before=3, line_spacing=1.25)),
            ])
        y += band_h + row_gap

    note_top = y - row_gap + note_gap
    note_h = min(note_h, CONTENT_BOTTOM - note_top)
    D.add_text(s, MARGIN, note_top, CONTENT_W, note_h, [
        ("Le niveau C suppose un accès direct aux données de production du client — un cabinet "
         "peut durablement rester au niveau A ou B par choix de gouvernance (slide précédente).",
         dict(size=8, color=MUTED, italic=True, line_spacing=1.25)),
    ])
    return s


# --- Nouveau (réouverture de périmètre, arbitrage 2026-07-21) : l'architecture
# des 11 agents-workflows (§Workflows, ligne 587+), délibérément retirée du deck
# au commit 4f0c9b7, est rouverte sur ce seul point. COMPLÉMENTAIRE de
# slide_schema_fonctionnement (le FLUX de données Collecte→Diagnostic→Conception
# →Restitution, avec flèches) : ici c'est l'INVENTAIRE des composants — les 11
# agents nommés, regroupés par étape en cartes (pas de flèches), le gate
# confidentialité posé comme un socle transversal et bloquant. Couleurs des
# familles reprises de slide_schema_fonctionnement (Diagnostic=violet,
# Conception=or, etc.) — cohérence inter-slides voulue, pas un hasard.
# v2.5 (chantier ④) : déplacée de l'IA vers la Démarche, juste après
# slide_schema_fonctionnement (le flux) — l'inventaire des composants.
def slide_architecture_agents(prs):
    s = content_slide(prs, "Démarche",
                       "Onze workflows outillés, un seul bloquant : le gate confidentialité les traverse tous",
                       color=ENCRE)
    D.add_text(s, MARGIN, CONTENT_TOP, CONTENT_W, 0.5, [
        ("Un mandat unique par workflow, regroupés par étape. Le gate confidentialité est le seul "
         "à pouvoir arrêter la chaîne — transversal, il précède tout usage d'un modèle IA sur "
         "donnée client.", dict(size=8, color=MUTED, italic=True, line_spacing=1.2)),
    ])

    familles = [
        ("INTAKE", ENCRE, [
            ("iap-intake",
             "Qualifie le contexte client, le positionne sur les deux échelles de maturité, "
             "puis choisit le chemin de mission : diagnostic, pilote, adoption ou gate d'abord."),
        ]),
        ("DIAGNOSTIC", ENCRE, [
            ("iap-diagnostic-systemique", "Structure, flux, RUN, posture management"),
            ("iap-discovery-gaspillage", "Preuves, causes racines, options de traitement"),
        ]),
        ("CONCEPTION", ENCRE, [
            ("iap-waste-treatment", "Backlog priorisé et scoré des gaspillages"),
            ("iap-product-definition", "Personas, capacités, valeur, roadmap"),
            ("iap-operating-model", "Rôles, gouvernance, financement (décisions actées)"),
            ("iap-agentic-opportunities", "Le gaspillage d'abord, l'IA ensuite"),
        ]),
        ("ADOPTION & RESTITUTION", ENCRE, [
            ("iap-adoption-plan", "Onboarding, documentation, communautés"),
            ("iap-scenario-playbook", "Adapte la démarche au scénario client"),
            ("iap-deck-builder", "Deck modulaire, restitution exécutive"),
        ]),
    ]
    n = len(familles)
    # Cartes de MÊME hauteur (cadence sur la colonne la plus fournie, CONCEPTION
    # à 4 agents) — mais au lieu d'un slot fixe aligné en haut qui laissait un
    # grand vide sous l'agent unique d'INTAKE, chaque colonne RÉPARTIT ses agents
    # sur toute la zone : chaque bloc-agent est dimensionné à SON texte, puis les
    # blocs sont espacés (space-between) pour couvrir la hauteur — colonne à 4 =
    # remplie ; colonne à 2-3 = espacée régulièrement ; colonne à 1 = centrée. La
    # rangée se lit ainsi « équilibrée » (cf. brief ppt-designer, défaut INTAKE).
    top0 = CONTENT_TOP + 0.6
    gate_h = 0.6
    note_h = 0.36
    card_h = CONTENT_BOTTOM - top0 - 0.15 - gate_h - 0.12 - note_h
    _, wcol = col_x(0, n)
    pad = 0.14
    usable_col = wcol - 2 * pad
    region_top = top0 + 0.52
    region_h = card_h - 0.52 - 0.08
    for i, (nom, color, agents) in enumerate(familles):
        x, w = col_x(i, n)
        D.add_card(s, x, top0, w, card_h, color)
        D.add_text(s, x + pad, top0 + 0.12, w - 2 * pad, 0.36, [
            (nom, dict(size=8, bold=True, color=encre_de(color), line_spacing=1.0)),
            (f"{len(agents)} workflow" + ("s" if len(agents) > 1 else ""),
             dict(size=6.5, color=MUTED, space_before=1)),
        ])
        blocs = [0.16 + _lignes(role, usable_col, 6.5) * (6.5 * 1.15 / 72.0)
                 for _, role in agents]
        na = len(agents)
        total = sum(blocs)
        if na == 1:
            gap_a = 0.0
            start = region_top  # top-align le bloc unique (INTAKE) sous l'en-tête : le centrer le faisait flotter (défaut « panneau flottant », cf. revue 2026-07-21)
        else:
            gap_a = min(0.5, (region_h - total) / (na - 1))
            span = total + gap_a * (na - 1)
            start = region_top + max(0.0, (region_h - span) / 2)
        ay = start
        for j, (agent, role) in enumerate(agents):
            D.add_text(s, x + pad, ay, w - 2 * pad, blocs[j], [
                (agent, dict(size=7, bold=True, color=NAVY, line_spacing=1.0)),
                (role, dict(size=6.5, color=MUTED, space_before=2, line_spacing=1.1)),
            ], anchor=MSO_ANCHOR.TOP)
            ay += blocs[j] + gap_a

    gate_top = top0 + card_h + 0.15
    D.add_rect(s, MARGIN, gate_top, CONTENT_W, gate_h, fill=NAVY, rounded=True, radius=0.1)
    chip_w = 1.15
    chip(s, MARGIN + 0.16, gate_top + gate_h / 2 - 0.14, chip_w, 0.28, "BLOQUANT",
         ACCENT_PLEIN, text_color=NAVY, size=7)
    D.add_text(s, MARGIN + 0.16 + chip_w + 0.2, gate_top + 0.1, CONTENT_W - chip_w - 0.55, gate_h - 0.2, [
        ("iap-ai-data-confidentiality-gate", dict(size=8, bold=True, color="#ffffff")),
        ("Classe les données (D0-D4), décide le mode d'exécution IA et pose les garde-fous — "
         "transversal, avant tout usage d'un modèle IA sur donnée client.",
         dict(size=7.5, color="#c7cbe0", space_before=2, line_spacing=1.15)),
    ], anchor=MSO_ANCHOR.MIDDLE)

    note_top = gate_top + gate_h + 0.12
    note_h_real = min(note_h, CONTENT_BOTTOM - note_top)
    D.add_text(s, MARGIN, note_top, CONTENT_W, note_h_real, [
        ("Onze mandats distincts, un seul peut arrêter la chaîne — tous les autres proposent et "
         "produisent, la décision finale reste humaine.",
         dict(size=8, color=MUTED, italic=True, line_spacing=1.2)),
    ])
    return s


# v2.32 (2026-09-04, refonte graphique, demande utilisateur explicite) : la
# police du thème (Arial) est remplacée par **Outfit** (Google Font, licence
# OFL) sur TOUT le deck — pas seulement les 3 slides de l'exec summary.
# Mécanisme identique à celui validé sur le check isolé (gen_check_slide_
# synthese_v3_refonte.py) : Outfit n'est posée nulle part dans le code des
# ~37 fonctions de slide (elles héritent d'Arial via le thème) — un
# POST-TRAITEMENT en fin de `build()` force le nom de police sur chaque run
# de texte de la présentation déjà construite, SAUF 4 glyphes absents du
# cmap d'Outfit (①②③⟲, vérifié via fonttools) qui resteraient en tofu sur
# PowerPoint sinon (confirmé au rendu réel croisé LibreOffice/PowerPoint COM
# lors du chantier sur le check isolé) — ceux-là restent en Arial, qui les
# couvre tous. Outfit est installée pour l'utilisateur courant sur CE poste
# (téléchargée depuis github.com/google/fonts) — PAS embarquée dans le
# fichier .pptx (python-pptx ne le permet pas) : un poste tiers sans Outfit
# affichera un repli tant qu'elle n'est pas incorporée manuellement
# (PowerPoint : Options > Enregistrer > Incorporer les polices) ou installée
# là-bas aussi.
POLICE_DECK = "Outfit"
POLICE_SECOURS = "Arial"
GLYPHES_HORS_POLICE_DECK = {"①", "②", "③", "⟲"}


def _appliquer_police_deck(prs, police=POLICE_DECK, secours=POLICE_SECOURS):
    """Alias — logique extraite vers `pptx_deck.appliquer_police` le 2026-09-11
    (finding audit VScode5) ; le choix de police (Outfit) reste ici, propre a
    ce projet, jamais un défaut du module réutilisable."""
    return D.appliquer_police(prs, police, secours, GLYPHES_HORS_POLICE_DECK)


def _controler(prs):
    """Le self-check de `build()` : tous les filets consultés, en un seul endroit.

    Extrait de `build()` pour être testable sans reconstruire les 49 slides —
    la couture qui manquait pour prouver qu'un filet est réellement BRANCHÉ et
    pas seulement présent dans `pptx_deck.py` (finding du hub du 2026-09-09 :
    les trois filets étaient portés et testés, aucun n'était appelé).

    `verifier_debordements_texte` reste volontairement DEHORS : il rend deux
    ordres de grandeur de constats de plus que les trois autres sur un deck
    correct, dont une part vient de l'estimateur qui ignore `line_spacing`. Or
    ce résultat gouverne le NOM du fichier écrit (`.INVALIDE.pptx` si non
    vide) : le brancher avant d'avoir réglé son seuil contre un rendu
    PowerPoint réel bloquerait la livraison d'un deck correct. Pour re-mesurer
    l'écart plutôt que croire un chiffre daté (58 contre 0 le 2026-09-10) :

        py -c "import sys;sys.path.insert(0,'docs/cadrage-ppt');\
    import pptx_deck as D;from pptx import Presentation;\
    p=Presentation('docs/cadrage-ppt/bmad-iap-cadrage-synthese.pptx');\
    print(len(D.verifier_debordements_texte(p)))"

    Les trois zéros des filets branchés ne sont pas de même nature, et les lire
    comme trois mesures équivalentes tromperait : `verifier_plancher_de_dessin`
    rend une liste vide parce qu'il n'y a AUCUN recouvrement horizontal — le
    bord droit du contenu passe à gauche du badge de numéro. Son zéro dit « rien
    ne se chevauche ici », pas « le plancher a été mesuré propre » ; le cas qui
    le ferait parler est verrouillé par les tests de `pptx_deck.py`, pas par ce
    deck-ci.
    """
    return list(D.verifier_geometrie(prs)
                + D.verifier_chrome_gabarit(prs)
                + D.verifier_plancher_de_dessin(prs, CONTENT_BOTTOM,
                                                bord_droit_in=BORD_DROIT)
                + _ANOMALIES_BUILD)


# ==================================================================
# v2.35 (restructuration 8 chapitres, arbitrage utilisateur en salle de
# délibération) : 3 chapitres neufs — chacun compose une synthèse à partir de
# faits déjà écrits ailleurs dans ce fichier (aucun fait inventé), plutôt que
# de renommer une slide existante. Voir docstring de tête + `build()` pour le
# mapping complet des 10 -> 8 chapitres.
# ==================================================================

def slide_enjeux(prs):
    """Lecture organisationnelle/macro des tensions entre parties prenantes
    (ex-`slide_personas_divergences`, retirée en v2.36) — pas les 4 portraits
    détaillés (supprimés du deck), seulement ce qui se joue pour la DSI si
    rien ne change."""
    s = content_slide(prs, "Enjeux",
                       "Si rien ne change : RUN qui s'aggrave, adoption qui stagne, "
                       "confiance qui s'érode", color=ENCRE)
    D.add_text(s, MARGIN, CONTENT_TOP, CONTENT_W, 0.42, [
        ("Quatre parties prenantes interrogées séparément convergent sur "
         "un même constat, lu ici à l'échelle de la DSI plutôt que persona par persona.",
         dict(size=D.TYPE["small"], color=NAVY, italic=True, line_spacing=1.25)),
    ])
    enjeux = [
        ("Pilotage", "Un signal de flux que personne ne partage encore",
         "Le management pilote à vue faute d'un métrique commun — l'infra comme guichet "
         "ne produit qu'un reporting-miroir, jamais un signal de confiance."),
        ("Adoption", "Un self-service qui reste un guichet si personne ne le choisit",
         "Tant que le contournement reste plus rapide que la plateforme, l'utilisateur "
         "applicatif la déserte — l'adoption ne se décrète pas, elle se conçoit."),
        ("Confiance business", "Une promesse business que la structure actuelle ne tient pas",
         "Le sponsor porte un problème business, pas un chantier cosmétique — sans capacité "
         "RUN récupérée ni KPI de mission, la promesse reste déclarative."),
        ("Conformité", "Une vitesse de preuve bridée par un gate non instruit",
         "La tension entre vitesse de démonstration et gate confidentialité (RSSI non "
         "interrogé à ce stade) reste un angle mort qui peut bloquer toute preuve par l'IA."),
    ]
    n_rows = 2
    region_top = CONTENT_TOP + 0.55
    row_gap = 0.16
    _, colw = col_x(0, 2)
    inner_w = colw - 0.34
    label_h = 0.13
    titre_h = max(_lignes(t, inner_w, D.TYPE["small"]) for _, t, _ in enjeux) * (D.TYPE["small"] * 1.1 / 72.0) + 0.03
    corps_h = max(_lignes(c, inner_w, 8) for *_, c in enjeux) * (8 * 1.2 / 72.0) + 0.03
    row_h = 0.12 + label_h + titre_h + 0.06 + corps_h + 0.16
    region_h = n_rows * row_h + (n_rows - 1) * row_gap
    region_top = CONTENT_TOP + 0.55 + max(0.0, (CONTENT_BOTTOM - CONTENT_TOP - 0.55 - region_h) / 2)
    for i, (label, titre, corps) in enumerate(enjeux):
        col = i % 2
        row = i // 2
        x, w = col_x(col, 2)
        y = region_top + row * (row_h + row_gap)
        D.add_rect(s, x, y, w, row_h, fill="#ffffff", line=LINE, line_w=0.75,
                   rounded=True, radius=0.1)
        D.add_rect(s, x, y, 0.06, row_h, fill=ENCRE, rounded=True, radius=0.5)
        D.add_text(s, x + 0.2, y + 0.12, w - 0.34, row_h - 0.24, [
            (label.upper(), dict(size=7, bold=True, color=MUTED)),
            (titre, dict(size=D.TYPE["small"], bold=True, color=NAVY, space_before=3, line_spacing=1.1)),
            (corps, dict(size=8, color=MUTED, space_before=4, line_spacing=1.2)),
        ])
    return s


def slide_opportunites(prs):
    """Ce que la situation rend possible MAINTENANT — pas le détail d'implémentation
    (agents candidats, méthode scorée : chapitre Offre), le pourquoi-maintenant."""
    s = content_slide(prs, "Opportunités",
                       "Ce que la situation ouvre maintenant — un espace de leviers cadrés, "
                       "pas un jaillissement gadget", color=ENCRE)
    D.add_text(s, MARGIN, CONTENT_TOP, CONTENT_W, 0.42, [
        ("Trois bascules déjà instruites par le cadrage rendent le moment favorable — le "
         "détail de ce qu'on livre pour les saisir suit au chapitre Offre.",
         dict(size=D.TYPE["small"], color=NAVY, italic=True, line_spacing=1.25)),
    ])
    leviers = [
        ("Une méthode déjà scorée", "8 familles de gaspillage nommées et priorisables "
         "(impact × faisabilité − prudence IA) : la priorisation n'est plus à inventer."),
        ("Un régime RUN devenu traitable", "Le RUN comme régime permanent, une fois nommé, "
         "ouvre la voie à une infra as a product plutôt qu'à un guichet subi."),
        ("Une IA sous gate, jamais la réponse d'abord", "Le gate confidentialité "
         "(iap-ai-data-confidentiality-gate) et le principe « process explicite avant l'agent » "
         "sécurisent l'usage — l'IA amplifie une réponse déjà là, elle ne la remplace pas."),
        ("Une organisation cible déjà pensée", "Team topologies et partage gaspillage "
         "mutualisé/tranché-à-deux donnent un porteur à ce qui, aujourd'hui, n'en a pas."),
    ]
    n = len(leviers)
    pad = 0.2
    _, w1 = col_x(0, n)
    usable = w1 - 2 * pad
    corps_h = max(_lignes(c, usable, 8.5) for _, c in leviers) * (8.5 * 1.22 / 72.0) + 0.06
    card_h = 0.16 + 0.30 + 0.10 + corps_h + 0.18
    top0 = CONTENT_TOP + max(0.55, (CONTENT_H - 0.55 - card_h) / 2 + 0.55)
    for i, (titre, corps) in enumerate(leviers):
        x, w = col_x(i, n)
        accent = (i == 2)   # « un sur N » : le gate IA, seul principe non négociable de la série
        if accent:
            D.add_rect(s, x, top0, w, card_h, fill=NAVY, rounded=True, radius=0.08)
        else:
            D.add_rect(s, x, top0, w, card_h, fill="#ffffff", line=LINE, line_w=0.75,
                       rounded=True, radius=0.08)
        D.add_text(s, x + pad, top0 + 0.16, w - 2 * pad, 0.30, [
            (str(i + 1), dict(size=8, bold=True, color="#8fd6db" if accent else ENCRE)),
        ])
        D.add_text(s, x + pad, top0 + 0.46, w - 2 * pad, 0.34, [
            (titre, dict(size=9, bold=True, color="#ffffff" if accent else NAVY, line_spacing=1.1)),
        ])
        D.add_text(s, x + pad, top0 + 0.46 + 0.34 + 0.06, w - 2 * pad, corps_h, [
            (corps, dict(size=8.5, color="#c7cbe0" if accent else MUTED, line_spacing=1.22)),
        ])
    return s


def slide_next_steps(prs):
    """Jalons immédiats + indicateurs de suivi minimaux (3-4, pas le détail
    complet des 3 familles de KPIs ni de la grille de maturité, retiré du
    deck en v2.36)."""
    s = content_slide(prs, "Next steps",
                       "Les jalons immédiats, et le signal minimal pour savoir si ça marche",
                       color=ENCRE)
    D.add_text(s, MARGIN, CONTENT_TOP, CONTENT_W, 0.36, [
        ("Le signal à suivre après l'assessment flash — un instrument, pas un rapport.",
         dict(size=8, color=MUTED, italic=True)),
    ])
    jalons = [
        ("①", "Assessment flash", "Cadrage express : douleurs mesurées, familles de "
         "gaspillage scorées, gate IA positionné."),
        ("②", "Mise en place", "Priorisation actée, porteur désigné par gaspillage, "
         "premiers agents candidats instruits sous gate."),
        ("⟲", "Réévaluation T+6-12 mois", "Même instrument qu'au T0 : delta mesuré, "
         "pas une nouvelle opinion."),
    ]
    top0 = CONTENT_TOP + 0.5
    row_h = 0.72
    row_gap = 0.12
    n = len(jalons)
    for i, (num, titre, corps) in enumerate(jalons):
        y = top0 + i * (row_h + row_gap)
        D.add_rect(s, MARGIN, y, CONTENT_W, row_h, fill=TRACK, rounded=True, radius=0.1)
        # bold=False pour "⟲" (tofu en gras dans la police du template, cf.
        # _GLYPHES_SANS_GRAS) — les chiffres encerclés "①②" le supportent, pas lui.
        D.add_text(s, MARGIN + 0.18, y, 0.5, row_h, [
            (num, dict(size=14, bold=(num not in _GLYPHES_SANS_GRAS), color=ENCRE,
                       align=PP_ALIGN.CENTER)),
        ], anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
        D.add_text(s, MARGIN + 0.75, y + 0.1, CONTENT_W - 1.0, row_h - 0.2, [
            (titre, dict(size=9.5, bold=True, color=NAVY, line_spacing=1.1)),
            (corps, dict(size=8.5, color=MUTED, space_before=3, line_spacing=1.2)),
        ], anchor=MSO_ANCHOR.MIDDLE)

    indic_top = top0 + n * row_h + (n - 1) * row_gap + 0.2
    D.add_text(s, MARGIN, indic_top, CONTENT_W, 0.24, [
        ("INDICATEURS DE SUIVI MINIMAUX", dict(size=8, bold=True, color=MUTED)),
    ])
    indicateurs = [
        "Gaspillage traité — capacité RUN récupérée",
        "Adoption produit — usage du self-service",
        "Fiabilité & SLA — MTTR, respect des engagements",
        "Maturité — delta par pilier, T0 → réévaluation",
    ]
    ind_top = indic_top + 0.28
    ind_h = CONTENT_BOTTOM - ind_top
    n2 = len(indicateurs)
    for i, texte in enumerate(indicateurs):
        x, w = col_x(i, n2)
        D.add_rect(s, x, ind_top, w, ind_h, fill="#ffffff", line=LINE, line_w=0.75,
                   rounded=True, radius=0.1)
        D.add_rect(s, x, ind_top, w, 0.05, fill=ENCRE, rounded=True, radius=0.5)
        D.add_text(s, x + 0.14, ind_top + 0.14, w - 0.28, ind_h - 0.24, [
            (texte, dict(size=8, color=NAVY, line_spacing=1.2)),
        ], anchor=MSO_ANCHOR.MIDDLE)
    return s


def build():
    # Les anomalies sont accumulees dans une liste de MODULE : sans cette remise
    # a zero, deux build() dans le meme processus additionnent leurs constats et
    # le second ecrit un .INVALIDE.pptx pour des defauts deja corriges.
    _ANOMALIES_BUILD[:] = []
    prs = new_prs()
    slide_cover(prs)

    # === Chapitre 01 — EXEC SUMMARY : le pitch de l'offre (v2.8, refondu v2.9) ===
    # v2.13 (2026-09-03, arbitrage utilisateur) : slide_executive_summary
    # DÉMÉNAGE d'avant l'intercalaire à juste après — modifié manuellement par
    # l'utilisateur sur l'export, reporté ici pour que toute régénération le
    # conserve (sinon un rebuild écraserait l'édition manuelle sans bruit).
    # v2.34 (2026-09-11, demande utilisateur) : le chapitre retombe à 3 slides de
    # contenu (« trop lourd, max 3 slides, plus synthétique ») — le sommaire, la
    # démarche infra en quatre temps, la thèse. slide_pitch_iap et
    # slide_demarche_avec_sans_agentic sont SUPPRIMÉES : la première ouvrait le
    # chapitre sur trois cartes dont deux parlaient d'agentic, la seconde
    # remettait « sans outillage / avec le module / agentic chez le client » sur
    # trois lignes d'égal poids — ensemble, elles faisaient de l'IA le sujet de
    # l'exec summary, exactement l'inverse de la demande.
    slide_chapitre(prs, "01", "Executive summary",
                   "La démarche infra en quatre temps — ce qu'on fait dans l'organisation "
                   "et sur la plateforme, sans prérequis d'IA — et ce qui la rend nécessaire.",
                   NAVY, "wheatfield", seed=0)
    slide_executive_summary(prs)
    slide_vision(prs)

    # === Chapitre 02 — CONTEXTE : le problème (ancien 02 + la moitié « pourquoi
    # ce terrain n'est pas un terrain comme un autre » de l'ancien 03, v2.35
    # restructuration 8 chapitres) ===
    slide_chapitre(prs, "02", "Contexte",
                   "La double mission, pourquoi cette transformation a du sens maintenant, "
                   "et pourquoi ce terrain n'est pas un terrain comme un autre.",
                   ENCRE, "mountains", seed=0)
    slide_mission(prs)
    slide_pourquoi_contexte(prs)
    # 2026-09-01 : « qui achète, contre quoi » — la section §Positionnement &
    # achat du cadrage (l.36) fait foi pour le deck depuis la v2.3 sans y avoir
    # jamais été redescendue. Vient APRÈS les 3 déclencheurs, qu'elle prolonge
    # (le déclencheur ① et l'écart 80/30 y sont repris comme réponse d'achat).
    slide_qui_achete(prs)
    slide_specificites_infra(prs)

    # === Chapitre 03 — ENJEUX (NOUVEAU, v2.35) : lecture organisationnelle/
    # macro des tensions personas (détail des 4 portraits en annexe) + le reste
    # du RUN/infra transverse de l'ancien chapitre « Spécificités de l'infra »
    # (v2.33) — ce qui se joue pour la DSI si rien ne change, pas le détail
    # terrain (ça, c'est Douleur). ===
    slide_chapitre(prs, "03", "Enjeux",
                   "Ce que la situation coûte à la DSI si rien ne change — pilotage, "
                   "adoption, confiance business, conformité.",
                   # seed=5 (pas 0) : c'est l'index Openverse VÉRIFIÉ sans filigrane
                   # pour la requête "river delta" — cf. commentaire _REQUETES_PHOTO.
                   ENCRE, "riverdelta", seed=5)
    slide_enjeux(prs)
    slide_infra_run(prs)
    slide_infra_transverse(prs)
    slide_infra_as_product_exemple(prs)

    # === Chapitre 04 — DOULEUR : ce qui fait mal (ancien chapitre « Besoins &
    # douleurs », inchangé — c'est la seule cible qui avait déjà sa maison
    # exacte, v2.35) ===
    slide_chapitre(prs, "04", "Douleur",
                   "Les douleurs approfondies et mesurables, et les 8 familles de gaspillage qui les rangent.",
                   ENCRE, "ocean", seed=0)
    slide_douleurs(prs)
    slide_familles(prs)

    # === Chapitre 05 — OPPORTUNITES (NOUVEAU, v2.35) : ce que la situation
    # rend possible maintenant — pas le détail d'implémentation (ça, c'est
    # Offre). Composée à partir des faits déjà écrits pour la Proposition et
    # l'IA (chapitres suivants), sans les répéter en détail. ===
    slide_chapitre(prs, "05", "Opportunités",
                   "Ce que la situation rend possible maintenant — les leviers déjà "
                   "instruits par le cadrage, pas encore ce qu'on livre pour les saisir.",
                   ENCRE, "dunes", seed=0)
    slide_opportunites(prs)

    # === Chapitre 06 — OFFRE : ce qu'on livre concrètement pour saisir
    # l'opportunité (ancien chapitre « Proposition » + reste de l'ancien
    # chapitre « IA », v2.35). Fil rouge : la THÈSE (why_iap) ouvre, puis la
    # MÉTHODE scorée (gaspillages), l'organisation cible, puis l'IA au service
    # de la réponse (gate, prudence, agents candidats, export). ===
    slide_chapitre(prs, "06", "Offre",
                   "Traiter l'infra comme un produit : la thèse, la méthode scorée, "
                   "l'organisation cible et l'IA au service de la réponse.",
                   ENCRE, "dunes", seed=0)
    slide_why_iap(prs)
    slide_gaspillages(prs)
    # v2.33 : la chaine de traitement ci-dessus est presentee cote cabinet de
    # bout en bout. Celle-ci la retourne — qui fait quoi, et ce qui se tranche
    # a deux — parce qu'un gaspillage mutualise n'acquiert de porteur que la.
    slide_gaspillage_partage(prs)
    slide_team_topologies(prs)
    # IA tirée APRÈS la thèse (l'IA amplifie, n'est jamais la réponse) —
    # regroupée dans Offre depuis v2.35 (n'avait pas assez de substance propre
    # pour justifier son propre chapitre dans un sommaire de 8).
    slide_gate_ia(prs)
    slide_prudence_ia(prs)
    # v2.37 : les 3 slides d'agent (gabarit identique, ~40 % de vide chacune)
    # fusionnent en une seule slide a 3 colonnes — cf. _AGENTS_CANDIDATS.
    slide_agents_candidats(prs)
    slide_export_markdown(prs)

    # === Chapitre 07 — DÉMARCHES : le COMMENT (fusion des anciens chapitres
    # « Démarche » et « Outillage IAP », v2.35 — l'outillage devient une
    # sous-partie de la démarche plutôt qu'un chapitre à lui seul) ===
    slide_chapitre(prs, "07", "Démarches",
                   "La trajectoire et ses livrables par phase, le fil humain, le schéma de "
                   "fonctionnement, l'inventaire des agents et l'outillage IAP.",
                   ENCRE, "canyon", seed=0)
    # v2.5 (chantier ①) : trajectoire fusionnée avec la vue bout-en-bout.
    slide_trajectoire(prs)
    # v2.4 : le fil humain décline la trame ①②③⟲ de slide_trajectoire côté
    # personnes — placé juste après elle.
    slide_deux_fils(prs)
    # v2.6 (point ②) : les activités humaines de la démarche, avec/sans l'outil
    # — juste après le fil humain, qu'elle décline en registres d'activités.
    slide_activites_humaines(prs)
    # v2.9 (arbitrage utilisateur) : le parcours de mission détaillé arrive du
    # chapitre Executive summary. Placé ICI, en tête du bloc des schémas (parcours
    # de mission → schéma de fonctionnement → inventaire des agents → livrables),
    # plutôt qu'accolé à slide_trajectoire : le fil humain ①②③⟲ (trajectoire →
    # fil humain → activités) reste d'un seul tenant. Les conditions de
    # réussite MIGRENT vers Next steps (v2.35), dont elles ouvrent le fil.
    slide_offre_iap(prs)
    # v2.5 (chantier ④) : déplacées de la Proposition (schéma, livrables) et de
    # l'IA (inventaire des agents) vers la Démarche.
    slide_schema_fonctionnement(prs)
    slide_architecture_agents(prs)
    # v2.35 : l'outillage IAP (ancien chapitre à part entière) rejoint la
    # Démarche comme sous-partie — le chapitre OUVRE sur le schéma d'architecture
    # en contexte client, ambition et lien SI le déclinent ensuite (v2.6, point ③).
    slide_iap_contexte_client(prs)
    slide_ambition(prs)
    slide_architecture_si(prs)

    # === Chapitre 08 — NEXT STEPS (NOUVEAU, v2.35) : clôture du deck — les
    # conditions de réussite et les jalons (fin de l'ancien chapitre Démarche),
    # puis un résumé de 4 indicateurs de suivi (le détail des 3 familles de
    # KPIs complètes et de la grille de maturité migre en annexe). ===
    slide_chapitre(prs, "08", "Next steps",
                   "Ce que la mission exige du client, les jalons immédiats, et le "
                   "signal minimal pour savoir si ça marche.",
                   ENCRE, "meadow", seed=1)
    slide_conditions_reussite(prs)
    slide_next_steps(prs)

    # Chapitre Annexes retiré (v2.36, demande utilisateur) : les 4 portraits
    # personas détaillés, leurs divergences, et le détail KPI complet (3
    # familles, grille de maturité, mise en place, cas chiffré) sont
    # supprimés du deck — leur synthèse reste dans Enjeux et Next steps.
    # slide_personas, slide_personas_divergences, slide_kpis,
    # slide_kpis_pourquoi_quoi, slide_kpis_mise_en_place, slide_maturite,
    # slide_kpis_exemple : fonctions retirées du fichier (récupérables dans
    # l'historique git, cf. commit 636f160 pour leur dernier état).

    _appliquer_police_deck(prs)

    # « GEOMETRIE » annoncait UNE nature de controle quand il y en a desormais
    # quatre : un recouvrement du numero de page ou une photo manquante
    # s'affichait a l'operateur comme un defaut de geometrie, et le message de
    # succes promettait moins que ce qui avait ete verifie.
    problemes = _controler(prs)
    if problemes:
        print(f"CONTROLE: {len(problemes)} probleme(s)")
        for p in problemes:
            print(" -", p)
    else:
        print("CONTROLE: OK — geometrie, chrome du gabarit, plancher de dessin,"
              " anomalies de build")

    # Un deck dont le controle signale un defaut n'ecrase PLUS le livrable.
    # `prs.save(out)` etait inconditionnel : seul le code de sortie signalait
    # l'echec, donc tout appelant qui l'ignore (IDE, double-clic, script sans
    # `set -e`) livrait un deck casse en silence (mesure du 2026-09-01). En cas
    # de defaut on ecrit a cote, sous un nom qui ne trompe personne, et l'export
    # precedent — valide — reste en place.
    base = os.path.join(os.path.dirname(__file__), "bmad-iap-cadrage-synthese")
    if problemes:
        out = base + ".INVALIDE.pptx"
        prs.save(out)
        print(f"Ecrit (NON LIVRABLE, {len(problemes)} probleme(s)):", out)
        print("Export livrable inchange:", base + ".pptx")
    else:
        out = base + ".pptx"
        prs.save(out)
        print("Ecrit:", out)
    return problemes


if __name__ == "__main__":
    problemes = build()
    sys.exit(1 if problemes else 0)
