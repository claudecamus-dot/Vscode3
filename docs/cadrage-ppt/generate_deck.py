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
avec renvoi aux chapitres). Le nœud « Discovery problématiques » du schéma garde
« 6 catégories » du document source pitch (verbatim jusqu'ici) — divergence
avec les 8 familles de douleur du chapitre Besoins & douleurs, arbitrée le
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
problématique → chemin vertueux, démarche centrée sur l'agentic comme
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
(sursollicitation/guichet → assainir la problématique ; mieux servir les
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
(3) `slide_problematique_partagee` neuve au chapitre Proposition : la chaine de
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

v2.39 (2026-09-23, revue design) : charte — guillemet et point final des
bandeaux de clôture plus jamais en texte cyan, fiches signature remplacées par
la chaîne de paires (transformation-commerciale n°13), photo « forest » pour
éviter deux intercalaires consécutifs identiques.

v2.40 (2026-09-23, trame arbitrée par l'utilisateur) : 7 chapitres nommés —
Contexte, Ce que ça coûte, Nos convictions, L'offre, l'IA (devenu en v2.41 l'expertise agentic), La
démarche, Réussir et démarrer — plus une ouverture (kicker EXECUTIVE SUMMARY,
sans intercalaire) et une annexe (kicker ANNEXE). Kicker de chaque slide =
nom de son chapitre (`_CHAPITRE_COURANT`). Nouvelle `slide_convictions`
(formation-po n°30) ; exec summary à un seul bloc navy et pieds = noms de
chapitres ; avant/après en lignes appariées (transfo-co n°12) ; slide de
clôture refondue en décision (Assessment flash 2 semaines, restitution n°12 +
n°3). Renvois positionnels et identifiants internes (iap-*, *-risk) retirés
du texte visible.

v2.41 (2026-09-23, restructuration validée par l'utilisateur) : L'offre en 4
slides, dont `slide_problematiques` réécrite en trois temps (repérer, chiffrer,
prioriser) ; La démarche réduite à la trajectoire et aux deux fils ; nouveau
chapitre « L'expertise agentic d'OCTO » après elle — `slide_intro_agentic`,
activités outillées (+ workflows par étape), agents candidats,
`slide_ia_sous_controle` (fusion gate + prudence), `slide_ambition_si`
(fusion ambition + SI + contexte client). Supprimées : schéma de
fonctionnement, workflows à part, gate/prudence/ambition/SI/contexte client
séparés. Annexe : schéma d'accompagnement + export markdown.

v2.42 (2026-09-23, six retours utilisateur) : « Ce que ça coûte » en 3 slides
(`slide_cout_si_rien_ne_change` fusionne enjeux, RUN et infra transverse ;
Opportunités retirée ; `slide_familles` refondue en badges + pilules) ;
« L'offre » en 3 slides (`slide_offre_mecanique` fusionne les trois temps et
le traitement à deux ; `slide_team_topologies` refondue en pilules
archétype → rôle) ; « notre démarche » dans le chapitre agentic ; vrai
chapitre « Annexes » avec intercalaire.

v2.43 (2026-09-23, phase design) : slide_why_iap (thèse en bandeau + liste
numérotée), slide_trajectoire (sans mention d'agent IA, ≥ 8 pt, clôture en
bandeau), slide_specificites_infra (paires constat → réponse),
slide_mission (sandwich piliers) refondues ; activités outillées passées à
8 pt ; retouches s18 (chapô) et s19 (titre sans « agents IA compris »).

Usage : python generate_deck.py
Sortie : bmad-iap-cadrage-synthese.pptx (à côté de ce script).

v2.44 (2026-09-23, demande utilisateur) : la slide convictions devient deux
slides — nos convictions fusionnées avec celles de l'exemple client
(docs/Import/Convictions.pptx), sept au total, plus un pavé « notre conviction
sur l'agentic » (contour épais + filet cyan, pas de 2e aplat navy).

v2.45 (2026-09-23, demande utilisateur) : formes plus arrondies — un rayon de
coin absolu unique (RAYON_COIN_IN) branché sur D.add_rect — et trois photos
réelles CC0 déjà en cache pour aérer (convictions 1/2 et 2/2, pourquoi IaaP),
dans le cadre round2DiagRect du gabarit, sans image générée.
"""
import os
import sys

sys.path.append(os.path.dirname(__file__))
import pptx_deck_vscode3 as D
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Emu, Inches, Pt

# Source unique du numero de version affiche sur la couverture (slide_cover) —
# jusqu'a v2.12 c'etait une chaine gelee dans slide_cover, jamais mise a jour a
# 4 bumps de version consecutifs (v2.9 a v2.11 ont toutes laisse "v2.8 · date
# perimee" sur la SLIDE LA PLUS VISIBLE du deck). Un seul endroit a changer
# desormais.
VERSION_DECK = "v2.45"
DATE_VERSION_DECK = "2026-09-23"

import deck_images  # noqa: E402,F401 — module accede par les tests (generate_deck.deck_images)
import deck_theme  # noqa: E402,F401 — module accede par les tests (generate_deck.deck_theme)
from deck_theme import (  # noqa: E402,F401 — extraction mécanique v2.46
    ACCENT,
    ACCENT1,
    ACCENT2,
    ACCENT_PLEIN,
    BORD_DROIT,
    CONTENT_BOTTOM,
    CONTENT_H,
    CONTENT_TOP,
    CONTENT_W,
    DK2,
    ENCRE,
    GAP,
    HERE,
    LAYOUT_CHAPITRE,
    LAYOUT_COUVERTURE,
    LAYOUT_TITRE_SEUL,
    LAYOUT_VIDE,
    LAYOUT_VISUEL_DROITE,
    LINE,
    MARGIN,
    MUTED,
    NAVY,
    RAYON_COIN_IN,
    SEVERITE,
    SUPPORT,
    SUPPORT_LIGNE,
    TEMPLATE,
    TH,
    TRACK,
    WHITE,
    _add_rect_arrondi,
    _add_rect_brut,
    _exiger_template,
    _rgb,
    encre_de,
    new_prs,
)

_CHAPITRE_COURANT = [None]


def _sans_ombre(shape):
    """Desactive l'ombre heritee d'une forme. Un echec n'est plus avale en
    silence (ancien `except Exception: pass`) : seul l'AttributeError d'une
    forme sans ombre est toleree, et elle est tracee sur stderr."""
    try:
        shape.shadow.inherit = False
    except AttributeError as exc:
        print(f"[generate_deck] ombre non desactivee : {exc}", file=sys.stderr)


def content_slide(prs, kicker, title, color):
    if kicker is None:
        kicker = _CHAPITRE_COURANT[0]
    if not kicker:
        raise SystemExit(f"content_slide({title!r}) : aucun chapitre courant pour le kicker")
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


from deck_images import (  # noqa: E402,F401 — extraction mécanique v2.46
    _ANOMALIES_BUILD,
    _REQUETES_PHOTO,
    _SCENE_REPLI,
    IMG_DIR,
    IMG_MANIFEST,
    REPO_ROOT,
    _find_frame_by_geom,
    _find_frame_in_group,
    _image_cache_valide,
    _photo_libre,
    _PILImage,
    _remplir_cadre,
    cover_crop_to_aspect,
    frame_obstructions,
    nature_images,
    place_image_in_frame,
    stock_images,
)


def slide_chapitre(prs, numero, titre, couverture, color, scene, seed=0):
    """Slide d'intercalaire de chapitre — vrai layout dédié du template
    (« 50 - Chapitre [1] »), repris tel qu'utilisé dans le REX
    "⛱️ L'Été de l'IA" (VSCode1) : cadre photo teardrop rempli (pas laissé
    vide), numéro à 17pt (pas la taille par défaut d'un texte de titre — un
    premier essai à 28pt débordait du petit encart sur le badge logo voisin,
    trouvé au rendu, cf. mémoire de session). Couleur de chapitre appliquée
    au numéro et au titre — le REX source ne le faisait pas, ajouté ici pour
    rester cohérent avec le code couleur déjà en place sur tout le deck."""
    _CHAPITRE_COURANT[0] = titre
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


from deck_shapes import (  # noqa: E402,F401 — extraction mécanique v2.46
    _GLYPHES_SANS_GRAS,
    BADGE_AGENTIC_W,
    DOT,
    QUOTE,
    _badge,
    _bandeau_cloture,
    _chevron_arrow,
    _chevron_shape,
    _dashed_rect,
    _fleche_h,
    _header_cell,
    _lignes,
    _noeud_socle,
    _note_mecanisme,
    _oval,
    _pale,
    _pilule_variante,
    _quote_banner,
    _rich,
    _split_emph,
    badge_deploiement_agentic,
    chip,
    col_x,
    dot_scale,
)


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
    s = content_slide(prs, None,
                       "Du pourquoi à la preuve : une transformation cadrée de bout en bout",
                       color=NAVY)

    headline_h = 0.62
    D.add_text(s, MARGIN, CONTENT_TOP, CONTENT_W, headline_h, [
        ("Transformer l'infrastructure en plateforme opérée comme un produit, ET traiter "
         "structurellement la problématique qui l'en empêche — le deck suit le fil : pourquoi, "
         "nos convictions, l'offre, comment, et comment démarrer.",
         dict(size=D.TYPE["small"], color=NAVY, italic=True, line_spacing=1.3)),
    ])

    # v2.10 : bloc OFFRE ajouté en tête de rangée (arbitrage utilisateur) — le
    # sommaire ne référençait aucun chapitre avant le bloc POURQUOI alors que le
    # chapitre 01 · Exec summary restait invisible ici. Accent (fond plein) comme
    # RÉSULTAT : les deux bornent la rangée (l'offre ouvre, la preuve ferme).
    # v2.34 : le bloc reprenait au mot près les sous-titres des deux slides
    # supprimées — il annonçait donc un contenu qui n'existe plus. Réaligné sur
    # la slide qui reste (la démarche infra en quatre temps).
    # v2.40 : les pieds de bloc = NOMS des nouveaux chapitres (jamais leurs
    # numéros) ; un seul bloc navy (« un sur N ») : l'offre, cœur du deck.
    items = [
        ("POURQUOI", ENCRE, "L'infra subie coûte de plus en plus cher.",
         "Trois déclencheurs, un terrain pas comme un autre, ce que coûte le statu quo, "
         "des douleurs mesurables et nommées.",
         "Contexte · Ce que ça coûte"),
        ("CONVICTIONS", ENCRE, "Partir des utilisateurs, traiter la problématique d'abord.",
         "Sept convictions et une conviction agentic sur ce qui fait réussir — et un "
         "exemple avant/après de ce qu'elle change.",
         "Nos convictions"),
        ("OFFRE", NAVY, "Traiter l'infra comme un produit, sans prérequis d'IA.",
         "La thèse, la problématique traitée à deux — repéré, priorisé, tenu dans la durée — "
         "et la cible Platform Team.",
         "L'offre"),
        ("COMMENT", ENCRE, "Trois temps et une boucle, personnes comprises.",
         "Démarche ①②③⟲ et ses deux fils ; en complément, jamais en prérequis, le "
         "chapitre L'expertise agentic d'OCTO.",
         "La démarche · L'expertise agentic d'OCTO"),
        ("DÉMARRER", ENCRE, "Deux semaines pour un premier signal mesuré.",
         "Les conditions de réussite, ce que la DSI engage, et le signal minimal suivi dès "
         "le T0 — la preuve, pas une opinion.",
         "Réussir et démarrer"),
    ]
    n = len(items)
    pad = 0.16
    _, cw = col_x(0, n)
    usable = cw - 2 * pad
    desc_size = 8
    line_h = desc_size * 1.3 / 72.0
    # v2.40 : cpi_ref=14 (comme slide_vision) — `_lignes` surestimait les
    # lignes sur ces colonnes étroites et laissait ~0,4in de vide sous chaque
    # accroche (défaut « panneau sur-étiré » vu au rendu).
    def _est(texte, taille):
        return max(1, D.estimer_lignes(texte, usable, taille, cpi_ref=14.0))

    claim_h = max(_est(c, 9) for _, _, c, _, _ in items) * (9 * 1.2 / 72.0) + 0.08
    desc_h = max(_est(d, desc_size) for _, _, _, d, _ in items) * line_h + 0.08
    # étages : label (0.24) + claim + desc + renvoi chapitres + respirations
    renvoi_h = max(_est(r, 8) for *_, r in items) * (7.5 * 1.2 / 72.0) + 0.06
    card_h = 0.14 + 0.24 + claim_h + 0.10 + desc_h + 0.14 + renvoi_h + 0.14
    top0 = CONTENT_TOP + headline_h + 0.30
    # bandeau de fond commun (pattern 7) : regroupe les 5 blocs en un seul
    # « bloc de lecture » — le fil se lit d'un trait, flèches dans les inter-colonnes.
    D.add_rect(s, MARGIN - 0.08, top0 - 0.16, CONTENT_W + 0.16, card_h + 0.32,
               fill=TRACK, rounded=True, radius=0.06)
    for i, (etape, color, claim, desc, renvoi) in enumerate(items):
        x, w = col_x(i, n)
        accent = etape == "OFFRE"   # « un sur N » : un seul aplat navy (v2.40)
        if accent:
            D.add_rect(s, x, top0, w, card_h, fill=NAVY, rounded=True, radius=0.08)
        else:
            D.add_rect(s, x, top0, w, card_h, fill="#ffffff", line=LINE, line_w=0.75,
                       rounded=True, radius=0.08)
        D.add_text(s, x + pad, top0 + 0.14, w - 2 * pad, 0.24, [
            (etape, dict(size=8, bold=True, color="#ffffff" if accent else color)),
        ])
        D.add_text(s, x + pad, top0 + 0.38, w - 2 * pad, claim_h, [
            (claim, dict(size=9, bold=True, color="#ffffff" if accent else NAVY,
                         line_spacing=1.2)),
        ])
        D.add_text(s, x + pad, top0 + 0.38 + claim_h + 0.10, w - 2 * pad, desc_h, [
            (desc, dict(size=desc_size, color="#c7cbe0" if accent else MUTED,
                        line_spacing=1.3)),
        ])
        D.add_text(s, x + pad, top0 + card_h - 0.14 - renvoi_h, w - 2 * pad, renvoi_h, [
            # Deux branches valant toutes deux navy depuis la bascule : le
            # conditionnel se lisait comme une emphase et ne rendait rien.
            (renvoi, dict(size=8, bold=True,
                          color="#ffffff" if accent else ENCRE)),
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
    pâles). Nœud Discovery problématiques renommé « 8 familles » (2026-09-18, cf.
    docstring de module) — seul écart volontaire à la fidélité verbatim du
    schéma, pour ne plus afficher deux chiffres différents de la même notion
    dans le même deck."""
    s = content_slide(prs, None,
                       "Accompagnement Infra as a Product : transformer une fonction infra en produit interne",
                       color=ENCRE)

    chapo = ("Transformer une fonction infra en produit interne : pensé pour ses utilisateurs, "
             "avec parcours, valeur et pilotage — pas un centre de coûts.")
    # v2.39 (revue design 2026-09-23) : la phrase de renvoi (« le détail de
    # chaque étape se retrouve dans la trajectoire… ») est retirée du chapô —
    # elle n'était pas du verbatim source, et sa ligne manquait en bas : la
    # légende passait sous l'encart « LA THÈSE » et la checklist était rognée.
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
    cit_pad = 0.08
    cit_usable = CONTENT_W - 2 * cit_pad
    # Libellé « LA THÈSE » en tête de la MÊME ligne que la citation (plus de
    # ligne à lui seul) : ~0,15in rendus au schéma.
    cit_lines = _lignes("LA THÈSE   " + citation, cit_usable - 0.30, 8.5)
    citation_h = 2 * cit_pad + cit_lines * (8.5 * 1.25 / 72.0)

    grid_n = 5
    row_h = 0.38
    schema_top = CONTENT_TOP + chapo_h + 0.06

    # --- Bande du haut : 2 mécanismes additifs (gauche/droite) + variantes (centre) ---
    x0n, w0n = col_x(0, grid_n)
    note_l_w = 2.55
    h_note_l = _note_mecanisme(s, x0n, schema_top, note_l_w, "EXTENSION POSSIBLE",
                                "Reconstitution d'incident, si crise.")
    note_r_w = 2.85
    note_r_x = BORD_DROIT - note_r_w
    h_note_r = _note_mecanisme(s, note_r_x, schema_top, note_r_w, "EXTENSION POSSIBLE",
                                "Tri contraintes / habitudes, si sites hétérogènes.")

    x1, w1 = col_x(1, grid_n)
    x2, w2 = col_x(2, grid_n)
    v_cx = (x1 + w1 + x2) / 2.0
    v_w = 1.35
    v_x = v_cx - v_w / 2.0
    D.add_text(s, v_x - 0.25, schema_top, v_w + 0.5, 0.14, [
        ("signal de contexte détecté ?", dict(size=8, italic=True, color=MUTED, align=PP_ALIGN.CENTER)),
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
        ("Discovery problématiques", "8 familles", False),
        ("Segmentation / Product Discovery", None, False),
    ]
    for i, (titre, sous, oval) in enumerate(socle_row1):
        x, w = col_x(i, grid_n)
        _noeud_socle(s, x, row1_top, w, row_h, titre, sous, oval=oval)
        if i < grid_n - 1:
            _fleche_h(s, x + w, row1_top, GAP, row_h)
    row1_bottom = row1_top + row_h

    # --- + Contradictions structurelles (si contexte politique), sous Discovery problématiques ---
    h_cs = _pilule_variante(s, x3, row1_bottom + 0.05, w3, None,
                             "+ Contradictions structurelles (si contexte politique)", size=8)
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
        ("▾", dict(size=8, bold=True, color=MUTED, align=PP_ALIGN.CENTER)),
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
                             "+ Dispositif de revue (si contexte politique)", size=8)
    dr_bottom = row2_bottom + 0.05 + h_dr

    # --- Checklist gouvernance IA (mécanisme transverse, pleine largeur) ---
    checklist_top = dr_bottom + 0.05
    h_checklist = _note_mecanisme(s, MARGIN, checklist_top, CONTENT_W,
                                   "CHECKLIST GOUVERNANCE IA — TRANSVERSE",
                                   "Mobilisable dès qu'un usage IA est identifié, à tout moment.")
    checklist_bottom = checklist_top + h_checklist

    # --- Légende (3 registres) ---
    legend_top = checklist_bottom + 0.02
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
            (label, dict(size=8, color=MUTED)),
        ], anchor=MSO_ANCHOR.MIDDLE)
        lx += sw + 0.06 + tw + 0.12

    # --- Citation-thèse (verbatim), bandeau bas ---
    cit_top = CONTENT_BOTTOM - citation_h
    D.add_rect(s, MARGIN, cit_top, CONTENT_W, citation_h, fill=NAVY, rounded=True, radius=0.08)
    D.add_rect(s, MARGIN, cit_top, 0.07, citation_h, fill=ACCENT, rounded=True, radius=0.5)
    # « LA THÈSE » était en cyan clair (#8fd6db) : texte cyan, interdit par la
    # charte — même gris-bleu que les autres libellés sur navy du deck.
    _rich(s, MARGIN + 0.24, cit_top, CONTENT_W - 0.44, citation_h, [
        ([("LA THÈSE   ", dict(size=8, bold=True, color="#8891b3")),
          (citation, dict(size=8.5, bold=True, color=WHITE))], dict(line_spacing=1.15)),
    ], anchor=MSO_ANCHOR.MIDDLE)
    # Garde : l'empiétement légende/encart n'est visible ni par
    # `verifier_geometrie` ni par le test — seul le rendu le montrait. Marge de
    # 0,10in pour l'écart estimé/rendu de LibreOffice.
    if legend_top + sw + 0.10 > cit_top:
        raise SystemExit(f"slide_offre_iap : la légende passe sous l'encart LA THÈSE "
                         f"({legend_top + sw + 0.10 - cit_top:.3f}in) — resserrer.")
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
    _sans_ombre(shp)
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
    s = content_slide(prs, None,
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
        ("①", "Assessment flash", "2 sem.", False,
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
# slide_specificites_infra : refondue en v2.43, nouvelle définition avant build().


# v2.32 (2026-09-04, refonte graphique) : DÉPLACÉE du chapitre 02 · Contexte
# vers le chapitre 01 · Exec summary (demande utilisateur) — puis REMONTÉE au
# chapitre 03 « Spécificités de l'infra » le 2026-09-10, où elle ferme le
# chapitre. Corps redessiné selon le même système
# de design "contour" (contenu inchangé, seule la forme change).
def slide_infra_as_product_exemple(prs):
    """v2.40 — transformation-commerciale n°12 « avant/après en 2 colonnes +
    grande flèche », en LIGNES APPARIÉES : chaque constat « avant » fait face à
    sa réponse « après » sur la même rangée. Aucun contour cyan porteur de sens
    (l'après se distingue par sa pilule navy pleine, son contour navy épais et
    sa puce ✓ — forme et typo, pas couleur). Plus d'identifiant interne."""
    s = content_slide(prs, None,
                       "Ce que change l'infra as a product, concrètement — un exemple avant/après.",
                       color=ENCRE)
    paires = [
        (("Guichet de tickets", " — personne n'est propriétaire du service."),
         ("Un propriétaire produit", " — une roadmap, des indicateurs de pilotage.")),
        (("Le triage du RUN trop long", " — traité au fil de l'eau."),
         ("Temps de triage du RUN réduit", " — capacité RUN récupérée.")),
        (("Backlog invisible", " — aucun indicateur de pilotage."),
         ("Backlog visible", " — priorisé, mesuré dans le temps.")),
        (("Beaucoup de projets, peu d'indicateurs", " — du contrôle et du reporting partout."),
         ("Process explicite, rôles définis", " — l'agent n'arrive qu'une fois le process écrit.")),
        (("Un pilotage dans la douleur", " — trop de sujets pour trop peu de capacité."),
         ("Des évolutions tech atteignables", " — un pilotage serein, des priorités tenues.")),
    ]
    fleche_w = 0.70
    col_w = (CONTENT_W - fleche_w - 0.24) / 2
    avant_x = MARGIN
    apres_x = MARGIN + col_w + fleche_w + 0.24
    tag_h = 0.28
    head_top = CONTENT_TOP + 0.02
    # Pilule AVANT grise (texte blanc sur MUTED, 5,8:1) / APRÈS navy pleine.
    D.add_rect(s, avant_x, head_top, 1.0, tag_h, fill=MUTED, rounded=True, radius=0.5)
    D.add_text(s, avant_x, head_top, 1.0, tag_h, [
        ("AVANT", dict(size=10, bold=True, color=WHITE, align=PP_ALIGN.CENTER)),
    ], anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
    D.add_rect(s, apres_x, head_top, 2.6, tag_h, fill=NAVY, rounded=True, radius=0.5)
    D.add_text(s, apres_x, head_top, 2.6, tag_h, [
        ("APRÈS — infra as a product", dict(size=10, bold=True, color=WHITE,
                                            align=PP_ALIGN.CENTER)),
    ], anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)

    size = 8.5
    pad = 0.14
    usable = col_w - 2 * pad - 0.22
    row_h = max(_lignes(a + b, usable, size) for pa in paires for a, b in pa) * (size * 1.25 / 72.0) + 0.20
    row_gap = 0.08
    rows_top = head_top + tag_h + 0.14
    for i, ((la, ra), (lb, rb)) in enumerate(paires):
        y = rows_top + i * (row_h + row_gap)
        D.add_rect(s, avant_x, y, col_w, row_h, fill=WHITE, line=LINE, line_w=0.75,
                   rounded=True, radius=0.12)
        D.add_rect(s, apres_x, y, col_w, row_h, fill=WHITE, line=NAVY, line_w=1.5,
                   rounded=True, radius=0.12)
        _rich(s, avant_x + pad, y, col_w - 2 * pad, row_h, [
            ([("—  ", dict(size=size, color=MUTED)),
              (la, dict(size=size, bold=True, color=NAVY)),
              (ra, dict(size=size, color=MUTED))], dict(line_spacing=1.2)),
        ], anchor=MSO_ANCHOR.MIDDLE)
        _rich(s, apres_x + pad, y, col_w - 2 * pad, row_h, [
            ([("✓  ", dict(size=size, bold=True, color=NAVY)),
              (lb, dict(size=size, bold=True, color=NAVY)),
              (rb, dict(size=size, color=NAVY))], dict(line_spacing=1.2)),
        ], anchor=MSO_ANCHOR.MIDDLE)
    rows_bas = rows_top + len(paires) * row_h + (len(paires) - 1) * row_gap

    # La grande flèche de transformation : CONTOUR navy épais, fond blanc.
    fx = avant_x + col_w + 0.12
    arrow = s.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(fx),
                                Inches(rows_top + 0.25), Inches(fleche_w),
                                Inches(rows_bas - rows_top - 0.50))
    _sans_ombre(arrow)
    arrow.fill.solid()
    arrow.fill.fore_color.rgb = _rgb(WHITE)
    arrow.line.color.rgb = _rgb(NAVY)
    arrow.line.width = Pt(2.25)

    _bandeau_cloture(
        s,
        ("Faire les bonnes choses au bon moment, un backlog piloté, des résultats concrets — "
         "l'agentique accélère la démarche, il ne la remplace pas."),
        rows_bas + 0.14, "slide_infra_as_product_exemple", size=11)
    return s


# --- Chapitre 03 · Spécificités de l'infra (v2.33, demande utilisateur du
# 2026-09-10 : « un chapitre dédié au traitement des spécificités de l'INFRA
# comme le RUN ou le fait que l'infra soit transverse »). Les deux slides
# ci-dessus (slide_specificites_infra, slide_infra_as_product_exemple) y sont
# DÉPLACÉES depuis le chapitre 01 · Exec summary : elles traitaient déjà le
# sujet, l'exec summary les portait faute de chapitre d'accueil. Les deux
# suivantes sont NEUVES et couvrent ce que la demande nommait explicitement et
# que le deck ne disait nulle part : ce qui rend le RUN structurellement à part,
# et ce que la transversalité fait à la problématique.
def slide_infra_run(prs):
    """Ce qui rend le RUN d'infra structurellement différent d'un projet.

    Flux numéroté (deck-design-library #4) plutôt que des cartes : les quatre
    traits ne sont pas une liste d'inconvénients, ils s'enchaînent — il ne
    s'arrête jamais, donc il n'est pas planifiable, donc il prend sur le BUILD,
    et sa dette ne se voit pas le jour où on l'accumule.
    """
    s = content_slide(prs, None,
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
    conséquence qui n'est jamais dite — une problématique que personne ne porte en
    propre n'est réduit par personne. C'est la charnière vers le chapitre
    Besoins & douleurs, et le fondement de la démarche partagée.
    """
    s = content_slide(prs, None,
                      "L'infra sert toutes les équipes et n'appartient à aucune — "
                      "c'est ce qui rend sa problématique orpheline",
                      color=ENCRE)

    servies = [
        ("Équipes produit", "Livrent de la valeur métier — l'infra est un moyen, jamais leur sujet."),
        ("Équipes applicatives", "Consomment la plateforme, ou la contournent si elle freine."),
        ("Sécurité, conformité & résilience", "Exigences transverses que personne ne budgète — "
         "l'offre s'y arrime, ne les remplace pas (cf. chapitre La démarche)."),
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
         "La problématique d'infra est mutualisée : il ne pèse sur le budget d'aucune équipe "
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

    _bandeau_cloture(s, "Une problématique que personne ne porte, personne ne la réduit.",
                     cons_top + cons_h + 0.14, "slide_infra_transverse")
    return s


# slide_mission : refondue en v2.43, nouvelle définition avant build().


# slide_pourquoi_contexte : réécrite en v2.43, nouvelle définition avant build().


# --- Nouveau (2026-09-01) : « qui achète, contre quoi ». La section
# §Positionnement & achat du cadrage (l.36) fait foi POUR LE DECK depuis la
# v2.3, mais n'y avait jamais été redescendue : 40 slides disaient COMMENT on
# fait la mission, aucune contre quel achat alternatif elle se gagne.
# v2.39 (2026-09-23) : fiches signature REMPLACÉES par la chaîne de paires
# constat→réponse (com 13) — voir le commentaire dans le corps ; l'historique
# ci-dessous décrit la forme précédente.
# v2.39 (2026-09-23) : fiches signature REMPLACÉES par la chaîne de paires
# constat→réponse (com 13) — voir le commentaire dans le corps ; l'historique
# ci-dessous décrit la forme précédente.
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
    s = content_slide(prs, None,
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
              + _lignes(lead2, CONTENT_W, 8) * lh(8) + 0.09
              # v2.40 : l'estimateur compte lead2 sur 1 ligne quand le rendu en
              # pose 2 — l'étiquette ACHAT ALTERNATIF chevauchait sa fin.
              + 0.11)
    D.add_text(s, MARGIN, CONTENT_TOP, CONTENT_W, lead_h, [
        (lead1, dict(size=9.5, color=NAVY, italic=True, line_spacing=1.25)),
        (lead2, dict(size=8, color=MUTED, space_before=3, line_spacing=1.25)),
    ])

    # --- Bandeau transverse : dimensionné AVANT la grille, qui prend le reste
    # (jamais de panneau étiré sur la hauteur restante).
    bandeaux = [
        (TRACK, MUTED, NAVY, "CE QUE LES QUATRE ALTERNATIVES N'ONT PAS",
         "« Infrastructure as a Product » existe ailleurs (Thoughtworks, Itential) ; nous "
         "gardons l'étiquette. Le différenciateur : produit + problématique + doctrine IA."),
        (TRACK, MUTED, NAVY, "LA RÉPONSE AU « JE NE VEUX QUE LA BAISSE DE COÛTS »",
         "Un Assessment flash d'entrée, puis la trajectoire — jamais l'assainissement seul. "
         "Sous pression IA : un cas d'usage public, « tout de suite, sous gate »."),
    ]
    _, band_w = col_x(0, 2)
    band_pad = 0.12
    band_lignes = max(_lignes(b[4], band_w - 2 * band_pad - 0.04, 8) for b in bandeaux)
    band_h = 2 * band_pad + lh(8) + 0.04 + band_lignes * lh(8) + 0.03
    band_top = CONTENT_BOTTOM - band_h

    # --- 4 fiches signature (coin coupé) à deux zones empilées --------------
    alternatives = [
        ("Ne rien faire",
         "Zéro coût apparent.",
         "Le coût du statu quo monte",
         "C'est lui que l'Assessment flash chiffre (déclencheur ①)."),
        ("FinOps outillé seul",
         "Mesure la problématique : marché mature, coût cloud estimé à 29 % (Flexera).",
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
    # v2.39 (revue design 2026-09-23) : forme com 13 « Chaîne de paires
    # constat→réponse reliées par chevron » (catalogue-transformation-
    # commerciale). La version fiches signature posait une carte navy DANS une
    # carte blanche (débordement au rendu) et titrait la réponse en cyan —
    # interdit par la charte. Ici : constat = contour, réponse = aplat navy
    # texte blanc, une rangée par achat alternatif, hauteur calée sur le texte.
    constat_w = 3.30
    chev_w = 0.42
    rep_w = CONTENT_W - constat_w - chev_w
    pad_x, pad_y = 0.13, 0.07
    tete_h = lh(8) + 0.03
    tete_y = CONTENT_TOP + lead_h + 0.08
    D.add_text(s, MARGIN, tete_y, constat_w, tete_h, [
        ("ACHAT ALTERNATIF", dict(size=8, bold=True, color=MUTED)),
    ])
    D.add_text(s, MARGIN + constat_w + chev_w, tete_y, rep_w, tete_h, [
        ("CE QUI LUI MANQUE — LA RÉPONSE IAP", dict(size=8, bold=True, color=MUTED)),
    ])
    y = tete_y + tete_h + 0.04
    row_gap = 0.07
    for nom, apporte, manque, reponse in alternatives:
        g_h = (_lignes(nom + " — " + apporte, constat_w - 2 * pad_x, 8)) * lh(8)
        d_h = (_lignes(manque + " — " + reponse, rep_w - 2 * pad_x, 8)) * lh(8)
        h = max(g_h, d_h) + 2 * pad_y
        D.add_rect(s, MARGIN, y, constat_w, h, fill=WHITE, line=ENCRE, line_w=1.1,
                   rounded=True, radius=0.18)
        _rich(s, MARGIN + pad_x, y, constat_w - 2 * pad_x, h, [
            ([(nom, dict(size=8, bold=True, color=NAVY)),
              (" — " + apporte, dict(size=8, color=NAVY))], dict(line_spacing=1.1)),
        ], anchor=MSO_ANCHOR.MIDDLE)
        _chevron_arrow(s, MARGIN + constat_w, y, chev_w, h, color=MUTED)
        D.add_rect(s, MARGIN + constat_w + chev_w, y, rep_w, h, fill=NAVY,
                   rounded=True, radius=0.18)
        _rich(s, MARGIN + constat_w + chev_w + pad_x, y, rep_w - 2 * pad_x, h, [
            ([(manque, dict(size=8, bold=True, color=WHITE)),
              (" — " + reponse, dict(size=8, color=WHITE))], dict(line_spacing=1.1)),
        ], anchor=MSO_ANCHOR.MIDDLE)
        y += h + row_gap
    if y - row_gap > band_top - 0.12:
        raise SystemExit(f"slide_qui_achete : paires chevauchent le bandeau "
                         f"({y - row_gap - band_top + 0.12:.3f}in)")

    for i, (fill, label_c, texte_c, label, corps) in enumerate(bandeaux):
        x, w = col_x(i, 2)
        D.add_rect(s, x, band_top, w, band_h, fill=fill, rounded=True, radius=0.08)
        D.add_text(s, x + band_pad + 0.02, band_top + band_pad, w - 2 * band_pad - 0.04,
                   band_h - 2 * band_pad, [
            (label, dict(size=8, bold=True, color=label_c)),
            (corps, dict(size=8, color=texte_c, space_before=3, line_spacing=1.25)),
        ])
    return s


# ---------------------------------------------------------------- slide 4
def slide_gate_ia(prs):
    s = content_slide(prs, None, "Les données du client gouvernent le choix du modèle IA", color=ENCRE)
    D.add_text(s, MARGIN, CONTENT_TOP, CONTENT_W, 0.35, [
        ("Checkpoint toujours humain avant tout usage IA sur données client — "
         "le gate de confidentialité des données, quel que soit le mode d'exécution retenu.",
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
# slide_why_iap : refondue en v2.43, nouvelle définition avant build().

# ---------------------------------------------------------------- Besoins & douleurs
# Nouveau (restructuration 2026-07-22) : la grille des 8 familles de douleur,
# jusqu'ici empaquetée dans slide_problematiques avec la chaîne de traitement et le
# score, est isolée ici — elle appartient au chapitre « Besoins & douleurs » (le
# langage commun qui rend une douleur nommable, donc détectable et traitable),
# tandis que la MÉTHODE de traitement (chaîne + score) reste au chapitre
# Proposition. Accent unifié sur la couleur du chapitre Douleurs (PALETTE[2]) :
# les 8 familles se distinguent par leur libellé, pas par 8 teintes sans clé.
# Passe de design 2026-07-23 — règle « un sur N en accent » (principes
# transversaux + pattern 3 du catalogue deck-design-library) : la famille IA,
# seule famille que cette méthode NOMME comme problématique (cas gadget,
# automatisation sans garde-fous — la doctrine du deck), reçoit un fill navy
# plein ; les 7 autres restent des cartes blanches identiques.
# slide_familles : refondue en v2.42, nouvelle définition avant build().


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
def slide_problematiques(prs):
    """v2.41 (retour utilisateur : « à revoir, je ne la comprends pas ») — la
    chaîne de 10 étapes en quinconce et la jauge de score cèdent la place à
    TROIS temps lisibles, une phrase chacun, le score réduit à une ligne.
    Pattern : restitution n°10 (fiches-étapes à chip chevauchant), en 3."""
    s = content_slide(prs, None,
                       "De la problématique au backlog priorisé, en trois temps",
                       color=ENCRE)
    D.add_text(s, MARGIN, CONTENT_TOP, CONTENT_W, 0.30, [
        ("Chaque famille de problématique (chapitre Ce que ça coûte) suit le même chemin — "
         "jamais un tri à l'intuition.",
         dict(size=D.TYPE["small"], color=NAVY, italic=True)),
    ])
    temps = [
        ("Repérer", "la problématique",
         "On le détecte et on le qualifie à partir des douleurs mesurées et des données "
         "du client, famille par famille."),
        ("Chiffrer", "ce qu'il coûte",
         "On le quantifie et on remonte à sa cause racine, preuves à l'appui — une "
         "économie démontrée, pas supposée."),
        ("Prioriser", "dans un backlog",
         "Chaque problématique reçoit un score et prend sa place dans un backlog priorisé, "
         "que l'on expérimente puis industrialise."),
    ]
    n = len(temps)
    fleche = 0.40
    col_w = (CONTENT_W - (n - 1) * fleche) / n
    pad = 0.22
    usable = col_w - 2 * pad
    corps_size = 10
    corps_h = max(_lignes(c, usable, corps_size) for *_, c in temps) * (corps_size * 1.3 / 72.0) + 0.08
    chip_h = 0.40
    top0 = CONTENT_TOP + 0.75
    card_h = chip_h / 2 + 0.18 + 0.34 + 0.08 + corps_h + 0.22
    for i, (verbe, objet, corps) in enumerate(temps):
        x = MARGIN + i * (col_w + fleche)
        accent = i == n - 1   # « un sur N » : le backlog, l'aboutissement
        D.add_rect(s, x, top0, col_w, card_h, fill=WHITE, line=NAVY if accent else LINE,
                   line_w=1.5 if accent else 0.75, rounded=True, radius=0.10)
        # Chip numéroté qui chevauche le haut de la fiche.
        D.add_rect(s, x + pad, top0 - chip_h / 2, 0.40, chip_h,
                   fill=NAVY if accent else WHITE, line=NAVY, line_w=1.25,
                   rounded=True, radius=0.5)
        D.add_text(s, x + pad, top0 - chip_h / 2, 0.40, chip_h, [
            (str(i + 1), dict(size=13, bold=True, color=WHITE if accent else NAVY,
                              align=PP_ALIGN.CENTER)),
        ], anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
        y = top0 + chip_h / 2 + 0.18
        _rich(s, x + pad, y, usable, 0.34, [
            ([(verbe, dict(size=15, bold=True, color=NAVY)),
              (" " + objet, dict(size=11, color=MUTED))], dict()),
        ])
        D.add_text(s, x + pad, y + 0.42, usable, corps_h, [
            (corps, dict(size=corps_size, color=NAVY, line_spacing=1.3)),
        ])
        if i < n - 1:
            _fleche_h(s, x + col_w + 0.06, top0 + card_h / 2 - 0.15, fleche - 0.12, 0.30)
    score_top = top0 + card_h + 0.35
    D.add_rect(s, MARGIN, score_top, CONTENT_W, 0.46, fill=TRACK, rounded=True, radius=0.12)
    _rich(s, MARGIN + 0.25, score_top, CONTENT_W - 0.5, 0.46, [
        ([("Score de priorité = (impact × faisabilité) − prudence IA", dict(size=10, bold=True, color=NAVY)),
          (" — ordinal : il éclaire l'arbitrage humain, il ne le remplace pas.",
           dict(size=10, color=NAVY))], dict()),
    ], anchor=MSO_ANCHOR.MIDDLE)
    return s


# v2.33 (2026-09-10, demande utilisateur) : « une démarche plus centrée sur
# comment traiter la problématique comme partagée ». Arbitrage : les DEUX lectures
# à la fois — mutualisé entre équipes (chapitre 03 · Spécificités de l'infra :
# « une problématique que personne ne porte, personne ne la réduit ») ET co-traitée
# avec le client, pas rendu comme un verdict de consultant.
#
# Cette slide ne remplace pas `slide_problematiques` : elle la RETOURNE. La chaîne
# des 10 étapes et le score y étaient présentés côté cabinet, de bout en bout —
# ce qui décrit exactement le contraire de ce que la demande vise. On reprend la
# même chaîne, regroupée en trois moments, et on dit qui fait quoi. La colonne
# qui compte est la troisième de chaque bloc : ce qui se tranche À DEUX, seul
# endroit où une problématique mutualisée acquiert un porteur.
def slide_problematique_partagee(prs):
    s = content_slide(prs, None,
                      "Une problématique partagée se traite à deux — sinon elle retourne à personne",
                      color=ENCRE)

    # Chapô DIMENSIONNÉ par son texte : posé à une distance fixe, sa 2e ligne
    # mordait sur les pilules de moment (vu au rendu du 2026-09-10 — le
    # self-check géométrique ne voit pas un chevauchement de zones de texte,
    # seulement une forme hors cadre).
    # Deux lignes, MESURÉES (`_lignes`) et non estimées : à trois, le bandeau de
    # clôture chevauchait les colonnes de 0,234in et la garde de fin de fonction
    # refusait le build. Raccourcir la copie plutôt que réduire le corps ou
    # rogner les marges — règle du catalogue de design.
    # v2.40 : une seule ligne — à deux, elle touchait encore les pilules.
    chapo = ("Cette chaîne se joue AVEC le client : sans décision partagée, le "
             "problématique reste sans porteur.")
    chapo_size = D.TYPE["small"]
    chapo_h = _lignes(chapo, CONTENT_W, chapo_size) * (chapo_size * 1.25 / 72.0) + 0.04
    D.add_text(s, MARGIN, CONTENT_TOP, CONTENT_W, chapo_h, [
        (chapo, dict(size=chapo_size, color=NAVY, italic=True, line_spacing=1.25)),
    ])

    moments = [
        ("Objectiver ensemble", "Détecter → Quantifier",
         "Ouvre ses données — CMDB, facturation, tickets — et nomme ce qui le gêne "
         "vraiment, au-delà de ce qui se mesure facilement.",
         "Apporte la grille des 8 familles et la méthode de quantification, sans "
         "présumer du résultat.",
         "Le périmètre mesuré, et ce qu'on accepte d'appeler problématique."),
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
        ("Ce qui change depuis le chapitre Ce que ça coûte : la problématique "
         "cesse d'être orphelin — il a un porteur nommé et un objectif partagé."),
        carte_top + carte_h + 0.12, "slide_problematique_partagee")
    return s


# ---------------------------------------------------------------- Besoins & douleurs
# Nouveau (restructuration 2026-07-22) : va PLUS LOIN que slide_personas (qui porte
# un irritant + une attente d'une ligne par persona). Ici chaque douleur est
# approfondie, dotée d'un signal/mesure qui la rend objectivable, et rattachée à
# une ou plusieurs familles de douleur — le pont direct vers slide_familles.
# La distinction par couleur d'accent persona d'origine (Infra/Utilisateur/
# Management/Sponsor en teintes propres) a été retirée à la bascule de charte
# du 2026-09-10 (couleur non porteuse de sens). Accent "un sur N" reposé le
# 2026-09-11 sur la seule lane Infra & RUN (cohérence avec slide_personas, qui
# accentue déjà ce persona) — les 3 autres lanes restent ENCRE. Rangées
# dimensionnées à leur contenu.
def slide_douleurs(prs):
    s = content_slide(prs, None,
                       "Les douleurs des clients infra : mesurables, pas des plaintes",
                       color=ENCRE)
    D.add_text(s, MARGIN, CONTENT_TOP, CONTENT_W, 0.4, [
        ("Chaque douleur appartient à un persona et se range dans une famille de douleur "
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
            (str(i + 1), dict(size=13, bold=True,
                               color=NAVY if color == ACCENT_PLEIN else "#ffffff",
                               align=PP_ALIGN.CENTER)),
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
            ("SIGNAL / MESURE", dict(size=8, bold=True, color=MUTED)),
        ])
        D.add_text(s, x + pad, signal_top, body_w, signal_h, [
            (signal, dict(size=signal_size, color=MUTED, italic=True, line_spacing=1.2)),
        ])
        chip(s, x + pad, famille_top, body_w, famille_h, famille, color, size=8)

    note_top = famille_top + famille_h + 0.18
    note_h = CONTENT_BOTTOM - note_top
    if note_h > 0.3:
        D.add_rect(s, MARGIN, note_top, CONTENT_W, note_h, fill=TRACK, rounded=True, radius=0.14)
        D.add_rect(s, MARGIN, note_top, 0.07, note_h, fill=ENCRE, rounded=True, radius=0.5)
        D.add_text(s, MARGIN + 0.26, note_top, CONTENT_W - 0.5, note_h, [
            ("Ces 4 douleurs se rangent en 8 familles de douleur, le langage commun qui les rend traitables.",
             dict(size=9, bold=True, color=ENCRE, line_spacing=1.15)),
        ], anchor=MSO_ANCHOR.MIDDLE)
    return s


# ---------------------------------------------------------------- slide 9
# slide_team_topologies : refondue en v2.42, nouvelle définition avant build().


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
    s = content_slide(prs, None,
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
          "Registre de problématiques (tags CONFIRMÉ/DÉDUIT/INCERTAIN)"]),
        ("CONCEPTION", ENCRE,
         ["Définition produit (+ cible MVP)",
          "Operating model + traitement des problématiques (décisions actées)"]),
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
        ("Revue des risques — lecture seule, challenge définition produit / modèle opératoire → deck exécutif",
         dict(size=7.5, italic=True, color=MUTED, line_spacing=1.1)),
    ], anchor=MSO_ANCHOR.MIDDLE)

    loop_top = reviewer_top + reviewer_h + 0.14
    loop_h = min(0.55, CONTENT_BOTTOM - loop_top)
    D.add_rect(s, MARGIN, loop_top, CONTENT_W, loop_h, fill=ENCRE, rounded=True, radius=0.1)
    D.add_text(s, MARGIN + 0.2, loop_top, CONTENT_W - 0.4, loop_h, [
        ("⟲ Boucle de réévaluation — pilotage stratégique, T+6-12 mois, alimente la bibliothèque de REX, "
         "reboucle vers la Collecte", dict(size=8, bold=False, color="#ffffff", line_spacing=1.15)),
    ], anchor=MSO_ANCHOR.MIDDLE)
    return s


# Fusion v2.5 (chantier ①) : slide_trajectoire et slide_schema_bout_en_bout
# déroulaient la même trame ①②③⟲ sur deux slides — fusionnées ici. La ligne de
# badges + durées + actions clés (de l'ancienne trajectoire) est enrichie du
# LIVRABLE-CLÉ par phase en une ligne (l'apport de la vue bout-en-bout — les
# NOMS seulement ; le détail des 4 profils de deck reste à slide_livrables_ppt).
# slide_trajectoire : refondue en v2.43, nouvelle définition avant build().


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
     "Dette, plateformes vieillissantes, dépendances : une base factuelle."),
    ("Décommissionner & observer",
     "Sur les pilotes : ce qui peut être décommissionné l'est, l'observabilité du "
     "reste est posée."),
    ("Standardiser & outiller",
     "CI/CD et infra as code deviennent le mode par défaut."),
    ("Mesurer & réengager",
     "Dette et KPI infra rejoués au même instrument qu'à T0."),
]


def slide_deux_fils(prs):
    s = content_slide(prs, None,
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
         dict(size=8, italic=True, color=MUTED, space_before=3, line_spacing=1.15)),
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
    h_hum = max(D.estimer_lignes(t, usable, 8, cpi_ref=14.0) for _, t in _FIL_HUMAIN) * (8 * 1.25 / 72.0)
    h_tec = max(D.estimer_lignes(t, usable, 8, cpi_ref=14.0) for _, t in _FIL_TECHNIQUE) * (8 * 1.25 / 72.0)
    verbe_h = 0.26
    row_h_hum = verbe_h + h_hum + 0.12
    row_h_tec = verbe_h + h_tec + 0.12
    head_h = 0.20
    band_h = 0.50

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
            (phase, dict(size=8, bold=True, color=MUTED, align=PP_ALIGN.CENTER)),
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
            (nom_rangee, dict(size=8, bold=True, color=ENCRE, line_spacing=1.1)),
        ], anchor=MSO_ANCHOR.MIDDLE)
        for i, (verbe, texte) in enumerate(contenu):
            x = grille_x + i * cell_w
            D.add_text(s, x + pad, y, usable, verbe_h, [
                (verbe, dict(size=8.5, bold=True, color=NAVY, line_spacing=1.05)),
            ])
            D.add_text(s, x + pad, y + verbe_h, usable, row_h - verbe_h - 0.08, [
                (texte, dict(size=8, color=NAVY, line_spacing=1.25)),
            ])
        y += row_h

    band_top = card_top + card_h + 0.16
    band_h = min(band_h, CONTENT_BOTTOM - band_top)
    if band_h > 0.3:
        D.add_rect(s, MARGIN, band_top, CONTENT_W, band_h, fill=TRACK, rounded=True, radius=0.08)
        D.add_text(s, MARGIN + 0.2, band_top, CONTENT_W - 0.4, band_h, [
            ("Ce que ces deux fils ne créent pas", dict(size=8, bold=True, color=NAVY)),
            ("Ni phase en plus, ni chantier d'architecture à part, ni évaluation des "
             "personnes ; la gouvernance sécurité et conformité reste celle du client.",
             dict(size=8, color=NAVY, space_before=3, line_spacing=1.25)),
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
    s = content_slide(prs, None,
                       "L'outillage prend en charge une partie du fil humain — le consultant garde le reste",
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
            (nom, dict(size=8, bold=True, color=encre_de(color), align=PP_ALIGN.CENTER)),
        ], align=PP_ALIGN.CENTER)

    # Hauteur de bande dérivée du CONTENU (colonne la plus fournie).
    cell_usable = col_w - 0.16
    line_h = 8 * 1.2 / 72.0

    def _band_h(cells):
        return max(sum(_lignes(t, cell_usable, 8) for t in c) * line_h
                   + (len(c) - 1) * 0.06 for c in cells) + 0.24

    bands_top = head_top + badge_d + 0.24
    # v2.41 : la bande de pied porte l'essentiel de l'ex-slide « Onze workflows »
    # (supprimée) — les workflows outillés, par étape.
    note_h = 0.74
    hA = _band_h(avec_iap)
    hB = _band_h(sans_iap)
    # Le mou vertical restant se répartit DANS les bandes (cellules centrées),
    # pas en vide sous la grille.
    slack = max(0.0, (CONTENT_BOTTOM - note_h - 0.12) - (bands_top + hA + 0.10 + hB))
    hA += slack / 2
    hB += slack / 2

    registres = [
        # v2.39 (revue design 2026-09-23) : le fond turquoise pâle distinguait
        # le registre par la seule couleur. Les deux bandes sont blanches ; la
        # rangée outillée garde « un sur N en accent » par un contour encre et
        # un filet cyan EN APLAT sur son bord gauche.
        (bands_top, hA, "AVEC IAP", "outillé par le module", "#ffffff", ENCRE, avec_iap),
        (bands_top + hA + 0.10, hB, "SANS IAP", "présence du consultant", "#ffffff", LINE, sans_iap),
    ]
    for top, h, label, sous, fill, line, cells in registres:
        D.add_rect(s, MARGIN, top, CONTENT_W, h, fill=fill, line=line, line_w=0.75,
                   rounded=True, radius=0.06)
        if line == ENCRE:
            D.add_rect(s, MARGIN, top, 0.06, h, fill=ACCENT, rounded=True, radius=0.5)
        D.add_text(s, MARGIN + 0.12, top, label_w - 0.12, h, [
            (label, dict(size=8, bold=True, color=NAVY, line_spacing=1.1)),
            (sous, dict(size=8, color=MUTED, italic=True, space_before=2, line_spacing=1.1)),
        ], anchor=MSO_ANCHOR.MIDDLE)
        D.add_rect(s, grid_x0 - 0.10, top + 0.10, 0.012, h - 0.20, fill=LINE)
        for i, items in enumerate(cells):
            x = _col_px(i)
            if i > 0:  # séparateurs fins (pattern 11 : la grille sans le tableau)
                D.add_rect(s, x - col_gap / 2, top + 0.10, 0.012, h - 0.20, fill=LINE)
            lignes_fmt = [(t, dict(size=8, color=NAVY, line_spacing=1.15,
                                   space_before=(4 if j else 0)))
                          for j, t in enumerate(items)]
            D.add_text(s, x + 0.08, top + 0.08, col_w - 0.16, h - 0.16, lignes_fmt,
                       anchor=MSO_ANCHOR.MIDDLE)

    note_top = CONTENT_BOTTOM - note_h
    D.add_rect(s, MARGIN, note_top, CONTENT_W, note_h, fill=TRACK, rounded=True, radius=0.08)
    _rich(s, MARGIN + 0.16, note_top, CONTENT_W - 0.32, note_h, [
        ([("ONZE WORKFLOWS OUTILLÉS, PAR ÉTAPE — UN SEUL BLOQUANT : LE GATE DE CONFIDENTIALITÉ",
           dict(size=8, bold=True, color=NAVY))], dict()),
        ([("Intake : ", dict(size=8, bold=True, color=NAVY)),
          ("qualification du contexte · ", dict(size=8, color=NAVY)),
          ("Diagnostic : ", dict(size=8, bold=True, color=NAVY)),
          ("diagnostic systémique, découverte de la problématique · ", dict(size=8, color=NAVY)),
          ("Conception : ", dict(size=8, bold=True, color=NAVY)),
          ("traitement de la problématique, définition produit, modèle opératoire, opportunités "
           "agentic · ", dict(size=8, color=NAVY)),
          ("Adoption & restitution : ", dict(size=8, bold=True, color=NAVY)),
          ("plan d'adoption, playbook de scénario, restitution exécutive.",
           dict(size=8, color=NAVY))], dict(space_before=3, line_spacing=1.2)),
    ], anchor=MSO_ANCHOR.MIDDLE)
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
# slide_conditions_reussite : réécrite en v2.43, nouvelle définition avant build().


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

    # v2.40 : même kicker que content_slide (nom du chapitre d'ouverture).
    p0 = phs[0].text_frame.paragraphs[0]
    rk = p0.add_run()
    rk.text = _CHAPITRE_COURANT[0].upper() + "   ·   "
    rt = p0.add_run()
    rt.text = "Le vrai risque : traiter le mauvais problème"
    for r in (rk, rt):
        r.font.size = Pt(20)
        r.font.bold = True
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
         "La capacité disponible alimente la problématique.",
         "RUN subi (l'exploitation quotidienne), ressources orphelines, seniors "
         "sur du répétitif — et le réflexe « plus d'outils » ou « mettons de "
         "l'IA » aggrave le mal."),
        ("CE QU'UN BON DIAGNOSTIC EXIGE", NAVY,
         "Partir des utilisateurs réels et de leurs douleurs — pas d'une réponse "
         "toute faite.",
         "Le fil que déroule tout le deck, du constat à la démarche."),
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
            (label, dict(size=8, bold=True, color="#ffffff" if accent else color)),
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
    s = content_slide(prs, None,
                       "Export markdown — agentic ou documentation, selon le contexte client (piste à valider)",
                       color=ENCRE)
    # v2.6 (point ④) : badge de série (comme les 3 slides d'agent candidat) —
    # l'intro cède la largeur du badge. Le renvoi aux 4 decks vise le chapitre
    # Démarche (slide_livrables_ppt y a déménagé en v2.5 — la mention
    # « Proposition » était restée, corrigée ici).
    badge_deploiement_agentic(s)
    D.add_text(s, MARGIN, CONTENT_TOP, CONTENT_W - BADGE_AGENTIC_W - 0.2, 0.5, [
        ("Pas un 5e deck PPT : un livrable markdown pour l'équipe qui exécute (versionnable, "
         "committable) — les 4 decks du chapitre La démarche restent pour sponsor et comité de pilotage.",
         dict(size=8, color=MUTED, italic=True, line_spacing=1.2)),
    ])

    cards = [
        ("DOCUMENTATION-FIRST", ENCRE,
         "Agentic Readiness [0]-[1], données D3-D4 sans LLM local, ou score de problématique faible.",
         "Runbook du processus", "plan d'adoption"),
        ("AGENTIC-IMPLEMENTATION", ENCRE,
         "Agentic Readiness [2]-[3], données D0-D2 (ou D3-D4 avec LLM local), score positif.",
         "Plan d'implémentation agentic", "opportunités agentic"),
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
            ("LIVRABLE · OWNER", dict(size=8, bold=True, color=MUTED)),
            (f"{fichier} — {owner}", dict(size=8, bold=True, color=NAVY, space_before=2)),
        ])

    signals_top = top0 + card_h + 0.15
    signals_h = 0.55
    signals = [
        ("PILIER AGENTIC READINESS", "[0-1] → documentation · [2-3] → agentic"),
        ("DONNÉES (GATE IA)", "D3-D4 sans LLM local → doc · D0-D2 → agentic"),
        ("SCORE DE PROBLÉMATIQUE", "faible/négatif → doc · positif → agentic"),
    ]
    for i, (label, mapping) in enumerate(signals):
        x, w = col_x(i, 3)
        D.add_rect(s, x, signals_top, w, signals_h, fill=TRACK, rounded=True, radius=0.1)
        D.add_text(s, x + 0.12, signals_top + 0.06, w - 0.24, signals_h - 0.12, [
            (label, dict(size=8, bold=True, color=NAVY)),
            (mapping, dict(size=8, color=MUTED, space_before=2, line_spacing=1.15)),
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
    s = content_slide(prs, None,
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
        ("Mêmes étapes que le schéma de fonctionnement (chapitre L'expertise agentic d'OCTO) — "
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
         "le niveau d'ambition A, B ou C",
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
        ("QUATRE PROPOSITIONS DE DÉPLOIEMENT AGENTIC — CHAPITRE L'EXPERTISE AGENTIC D'OCTO ET ANNEXE",
         dict(size=7, bold=True, color=ENCRE)),
        ("Agent de triage RUN · veille FinOps · agent documentaire (RAG) · export markdown "
         "(qui porte la décision agentic/documentation) — chacune signalée par le badge "
         "de déploiement agentic.",
         dict(size=7, color=NAVY, space_before=2, line_spacing=1.2)),
    ], anchor=MSO_ANCHOR.MIDDLE)
    return s


# ---------------------------------------------------------------- slide 11
def slide_ambition(prs):
    # v2.5 (chantier ④) : déplacée de la Proposition vers l'Outillage IAP —
    # le niveau d'ambition qualifie l'outil, pas la proposition de transformation.
    s = content_slide(prs, None, "Trois niveaux d'ambition, pas un spectre linéaire", color=ENCRE)
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
     "audits ponctuels — la problématique s'accumule entre deux revues.",
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
    s = content_slide(prs, None, "Trois candidats d'agent, un par famille de problématique",
                      color=ENCRE)
    badge_deploiement_agentic(s)

    D.add_text(s, MARGIN, CONTENT_TOP, CONTENT_W - BADGE_AGENTIC_W - 0.2, 0.34, [
        ("La problématique d'abord, l'IA ensuite : chaque candidat répond à une famille "
         "déjà cadrée au chapitre Ce que ça coûte — aucun n'est inventé pour l'occasion.",
         dict(size=9, color=MUTED, italic=True, line_spacing=1.2)),
    ])

    note = ("Ces 3 candidats restent soumis au scoring (chapitre L'offre) et au gate "
            "de confidentialité avant toute décision — des exemples illustratifs, pas "
            "une liste actée.")
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
        _sans_ombre(icon)
        icon.fill.solid()
        icon.fill.fore_color.rgb = _rgb(ENCRE)
        icon.line.fill.background()
        icon.text_frame.paragraphs[0].text = ""
        D.add_text(s, x + icon_d + 0.12, top - 0.02, col_w - icon_d - 0.12, icon_d + 0.04, [
            (nom, dict(size=10, bold=True, color=NAVY, line_spacing=1.05)),
            ("Problématique " + famille, dict(size=8, color=MUTED, italic=True, space_before=1)),
        ], anchor=MSO_ANCHOR.MIDDLE)

        # Ce qui sépare les 3 candidats est la POSITION et le filet, jamais une
        # couleur d'accent par famille (charte du 2026-09-10 : la couleur ne
        # porte pas le sens).
        y = top + icon_d + 0.22
        D.add_rect(s, x, y - 0.10, col_w, 0.014, fill=ENCRE)

        for label, texte in (("POURQUOI", why), ("CE QUE FAIT L'AGENT", what), ("GAIN", gain)):
            D.add_text(s, x, y, col_w, lbl_h, [
                (label, dict(size=8, bold=True, color=ENCRE)),
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
    s = content_slide(prs, None, "La prudence IA est un frein chiffré, pas un veto", color=ENCRE)
    D.add_text(s, MARGIN, CONTENT_TOP, CONTENT_W, 0.4, [
        ("Prudence IA = confidentialité + besoin de supervision + criticité de la décision",
         dict(size=D.TYPE["small"], bold=True, color=NAVY, line_spacing=1.2)),
    ])

    facteurs = [
        ("1", "CONFIDENTIALITÉ", ENCRE,
         "Reprend directement la classification D0-D4 du gate de confidentialité — "
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
    s = content_slide(prs, None,
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
        # v2.39 (revue design 2026-09-23) : fond pâle IDENTIQUE pour les trois
        # niveaux — le turquoise pâle du niveau A distinguait par la couleur de
        # fond ; l'accent « un sur N » reste porté par le filet et le badge.
        D.add_rect(s, MARGIN, y, CONTENT_W, band_h, fill=TRACK, rounded=True, radius=0.08)
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
         "peut durablement rester au niveau A ou B par choix de gouvernance.",
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
    s = content_slide(prs, None,
                       "Onze workflows outillés, un seul bloquant : le gate confidentialité les traverse tous",
                       color=ENCRE)
    D.add_text(s, MARGIN, CONTENT_TOP, CONTENT_W, 0.5, [
        ("Un mandat unique par workflow, regroupés par étape. Le gate confidentialité est le seul "
         "à pouvoir arrêter la chaîne — transversal, il précède tout usage d'un modèle IA sur "
         "donnée client.", dict(size=8, color=MUTED, italic=True, line_spacing=1.2)),
    ])

    familles = [
        ("INTAKE", ENCRE, [
            ("Qualification du contexte",
             "Qualifie le contexte client, le positionne sur les deux échelles de maturité, "
             "puis choisit le chemin de mission : diagnostic, pilote, adoption ou gate d'abord."),
        ]),
        ("DIAGNOSTIC", ENCRE, [
            ("Diagnostic systémique", "Structure, flux, RUN, posture management"),
            ("Découverte de la problématique", "Preuves, causes racines, options de traitement"),
        ]),
        ("CONCEPTION", ENCRE, [
            ("Traitement de la problématique", "Backlog priorisé et scoré des problématiques"),
            ("Définition produit", "Personas, capacités, valeur, roadmap"),
            ("Modèle opératoire", "Rôles, gouvernance, financement (décisions actées)"),
            ("Opportunités agentic", "La problématique d'abord, l'IA ensuite"),
        ]),
        ("ADOPTION & RESTITUTION", ENCRE, [
            ("Plan d'adoption", "Onboarding, documentation, communautés"),
            ("Playbook de scénario", "Adapte la démarche au scénario client"),
            ("Restitution exécutive", "Deck modulaire, restitution exécutive"),
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
        ("Gate de confidentialité des données", dict(size=8, bold=True, color="#ffffff")),
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
    import pptx_deck_vscode3 as D;from pptx import Presentation;\
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
    s = content_slide(prs, None,
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
    s = content_slide(prs, None,
                       "Ce que la situation ouvre maintenant — un espace de leviers cadrés, "
                       "pas un jaillissement gadget", color=ENCRE)
    D.add_text(s, MARGIN, CONTENT_TOP, CONTENT_W, 0.42, [
        ("Trois bascules déjà instruites par le cadrage rendent le moment favorable — le "
         "détail de ce qu'on livre pour les saisir suit au chapitre L'offre.",
         dict(size=D.TYPE["small"], color=NAVY, italic=True, line_spacing=1.25)),
    ])
    leviers = [
        ("Une méthode déjà scorée", "8 familles de problématique nommées et priorisables "
         "(impact × faisabilité − prudence IA) : la priorisation n'est plus à inventer."),
        ("Un régime RUN devenu traitable", "Le RUN comme régime permanent, une fois nommé, "
         "ouvre la voie à une infra as a product plutôt qu'à un guichet subi."),
        ("Une IA sous gate, jamais la réponse d'abord", "Le gate confidentialité "
         "des données et le principe « process explicite avant l'agent » "
         "sécurisent l'usage — l'IA amplifie une réponse déjà là, elle ne la remplace pas."),
        ("Une organisation cible déjà pensée", "Team topologies et partage problématique "
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
            (str(i + 1), dict(size=8, bold=True, color="#ffffff" if accent else ENCRE)),
        ])
        D.add_text(s, x + pad, top0 + 0.46, w - 2 * pad, 0.34, [
            (titre, dict(size=9, bold=True, color="#ffffff" if accent else NAVY, line_spacing=1.1)),
        ])
        D.add_text(s, x + pad, top0 + 0.46 + 0.34 + 0.06, w - 2 * pad, corps_h, [
            (corps, dict(size=8.5, color="#c7cbe0" if accent else MUTED, line_spacing=1.22)),
        ])
    return s


def slide_next_steps(prs):
    """v2.40 — la slide de clôture pose une DÉCISION : lancer un Assessment
    flash de 2 semaines (arbitrage utilisateur du 2026-09-23), ce que la DSI
    engage (les deux premières conditions de slide_conditions_reussite), et le
    moment du premier signal (restitution de l'assessment, mesures T0 — cf.
    cadrage §Livrables par phase). Patterns : restitution n°12 (Gantt
    simplifié, pastilles de jalon, frise de points) + n°3 (cartes stat pour le
    signal minimal). Aucun chiffre hors cadrage : 2 semaines (arbitré),
    4 à 5 semaines et T+6-12 mois (trajectoire du cadrage)."""
    s = content_slide(prs, None,
                       "Deux semaines d'Assessment flash pour un premier signal mesuré",
                       color=ENCRE)
    D.add_text(s, MARGIN, CONTENT_TOP, CONTENT_W, 0.26, [
        ("Décision demandée : lancer l'Assessment flash. La DSI engage un sponsor et des "
         "équipes disponibles ; le premier signal arrive à sa restitution, fin de semaine 2.",
         dict(size=8.5, color=NAVY, italic=True)),
    ])

    # --- Gantt simplifié -----------------------------------------------------
    lab_x, lab_w = MARGIN, 1.95
    sem_x0, sem_w, n_sem = MARGIN + 2.05, 0.60, 7
    t_x = 7.75
    t_w = BORD_DROIT - t_x
    head_top = CONTENT_TOP + 0.38
    for k in range(n_sem):
        D.add_text(s, sem_x0 + k * sem_w, head_top, sem_w, 0.18, [
            (f"S{k + 1}", dict(size=8, bold=True, color=MUTED, align=PP_ALIGN.CENTER)),
        ], align=PP_ALIGN.CENTER)
    D.add_text(s, sem_x0 + n_sem * sem_w, head_top, t_x - sem_x0 - n_sem * sem_w, 0.18, [
        ("…", dict(size=8, bold=True, color=MUTED, align=PP_ALIGN.CENTER)),
    ], align=PP_ALIGN.CENTER)
    D.add_text(s, t_x, head_top, t_w, 0.18, [
        ("T+6–12 MOIS", dict(size=8, bold=True, color=MUTED, align=PP_ALIGN.CENTER)),
    ], align=PP_ALIGN.CENTER)
    # Frise de points : une pastille par semaine, la seule en aplat cyan =
    # la restitution de fin de S2 (le premier signal).
    dot_d, dot_y = 0.12, head_top + 0.22
    for k in range(n_sem):
        cx = sem_x0 + (k + 0.5) * sem_w
        _oval(s, cx - dot_d / 2, dot_y, dot_d, dot_d,
              fill=ACCENT_PLEIN if k == 1 else WHITE, line=NAVY, line_w=0.75)
    _oval(s, t_x + t_w / 2 - dot_d / 2, dot_y, dot_d, dot_d, fill=WHITE, line=NAVY, line_w=0.75)

    lanes = [
        ("①  Assessment flash", 0, 2, "2 semaines", "plein"),
        ("②  Premier déploiement", 2, 8, "4 à 5 semaines", "contour"),
        ("③  Implémentation itérative", 8, None, "en continu", "pointille"),
        ("⟲  Réévaluation", None, None, "même instrument qu'au T0", "jalon"),
    ]
    lane_h, lane_gap = 0.27, 0.07
    lane_top0 = dot_y + dot_d + 0.10
    for i, (label, deb, fin, txt, style) in enumerate(lanes):
        y = lane_top0 + i * (lane_h + lane_gap)
        D.add_rect(s, MARGIN, y + lane_h + lane_gap / 2 - 0.005, CONTENT_W, 0.01, fill=TRACK)
        D.add_text(s, lab_x, y, lab_w, lane_h, [
            (label, dict(size=8, bold=not label.startswith(_GLYPHES_SANS_GRAS), color=NAVY)),
        ], anchor=MSO_ANCHOR.MIDDLE)
        if style == "jalon":
            cx = t_x + t_w / 2
            losange = s.shapes.add_shape(MSO_SHAPE.FLOWCHART_DECISION, Inches(cx - 0.13),
                                         Inches(y + 0.02), Inches(0.26), Inches(lane_h - 0.04))
            losange.fill.solid()
            losange.fill.fore_color.rgb = _rgb(WHITE)
            losange.line.color.rgb = _rgb(NAVY)
            losange.line.width = Pt(1.25)
            D.add_text(s, sem_x0 + 3 * sem_w, y, cx - 0.18 - sem_x0 - 3 * sem_w, lane_h, [
                ("Delta mesuré — " + txt, dict(size=8, italic=True, color=MUTED,
                                              align=PP_ALIGN.RIGHT)),
            ], anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.RIGHT)
            continue
        x0 = sem_x0 + deb * sem_w + 0.03
        x1 = (sem_x0 + fin * sem_w - 0.03) if fin is not None else BORD_DROIT
        if style == "plein":
            D.add_rect(s, x0, y, x1 - x0, lane_h, fill=NAVY, rounded=True, radius=0.5)
            couleur_txt = WHITE
        elif style == "contour":
            D.add_rect(s, x0, y, x1 - x0, lane_h, fill=WHITE, line=NAVY, line_w=1.25,
                       rounded=True, radius=0.5)
            couleur_txt = NAVY
        else:
            _dashed_rect(s, x0, y, x1 - x0, lane_h, fill=WHITE, line=NAVY, line_w=1.0,
                         radius=0.5)
            couleur_txt = NAVY
        D.add_text(s, x0, y, x1 - x0, lane_h, [
            (txt, dict(size=8, bold=True, color=couleur_txt, align=PP_ALIGN.CENTER)),
        ], anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
    gantt_bas = lane_top0 + len(lanes) * (lane_h + lane_gap)
    # Jalon du premier signal : losange sur la fin de S2, légende dessous.
    jx = sem_x0 + 2 * sem_w
    jal = s.shapes.add_shape(MSO_SHAPE.FLOWCHART_DECISION, Inches(jx - 0.13),
                             Inches(lane_top0 + 0.02), Inches(0.26), Inches(lane_h - 0.04))
    jal.fill.solid()
    jal.fill.fore_color.rgb = _rgb(ACCENT_PLEIN)
    jal.line.color.rgb = _rgb(NAVY)
    jal.line.width = Pt(1.25)
    D.add_text(s, sem_x0, gantt_bas + 0.01, 5.0, 0.2, [
        ("◆ Fin S2 : premier signal — mesures T0 restituées au sponsor",
         dict(size=8, bold=True, color=NAVY)),
    ])

    # --- Bas : ce que la DSI engage | signal minimal (cartes stat) -----------
    bas_top = gantt_bas + 0.34
    bas_h = CONTENT_BOTTOM - bas_top
    eng_w = 3.05
    D.add_text(s, MARGIN, bas_top, eng_w, 0.2, [
        ("CE QUE LA DSI ENGAGE", dict(size=8, bold=True, color=MUTED)),
    ])
    engagements = [
        ("Un sponsor qui porte la cible", "DSI ou direction infrastructure, engagé dès l'intake."),
        ("Des équipes réellement disponibles", "Interviews et ateliers sur du temps réservé, "
         "vérifié avant le démarrage."),
    ]
    eg_top = bas_top + 0.24
    eg_h = (bas_h - 0.24 - 0.08) / 2
    for i, (t, c) in enumerate(engagements):
        y = eg_top + i * (eg_h + 0.08)
        D.add_rect(s, MARGIN, y, eng_w, eg_h, fill=WHITE, line=NAVY, line_w=1.0,
                   rounded=True, radius=0.12)
        _badge(s, MARGIN + 0.24, y + eg_h / 2, 0.26, NAVY, str(i + 1), size=8)
        D.add_text(s, MARGIN + 0.46, y, eng_w - 0.56, eg_h, [
            (t, dict(size=8.5, bold=True, color=NAVY, line_spacing=1.1)),
            (c, dict(size=8, color=MUTED, space_before=2, line_spacing=1.15)),
        ], anchor=MSO_ANCHOR.MIDDLE)

    ind_x = MARGIN + eng_w + 0.25
    ind_w = BORD_DROIT - ind_x
    D.add_text(s, ind_x, bas_top, ind_w, 0.2, [
        ("SIGNAL MINIMAL — MESURÉ AU T0, REMESURÉ À T+6–12 MOIS",
         dict(size=8, bold=True, color=MUTED)),
    ])
    indicateurs = [
        ("Problématique traitée", "capacité RUN récupérée"),
        ("Adoption produit", "usage du self-service"),
        ("Fiabilité & SLA", "MTTR, respect des engagements"),
        ("Maturité", "delta par pilier, T0 → réévaluation"),
    ]
    g = 0.10
    cw = (ind_w - g) / 2
    ch = (bas_h - 0.24 - g) / 2
    for i, (lead, det) in enumerate(indicateurs):
        x = ind_x + (i % 2) * (cw + g)
        y = eg_top + (i // 2) * (ch + g)
        D.add_rect(s, x, y, cw, ch, fill=WHITE, line=LINE, line_w=0.75, rounded=True, radius=0.12)
        D.add_rect(s, x, y + 0.08, 0.05, ch - 0.16, fill=NAVY, rounded=True, radius=0.5)
        D.add_text(s, x + 0.16, y, cw - 0.24, ch, [
            (lead, dict(size=10, bold=True, color=NAVY, line_spacing=1.05)),
            (det, dict(size=8, color=MUTED, space_before=1, line_spacing=1.15)),
        ], anchor=MSO_ANCHOR.MIDDLE)
    return s


# v2.44 (demande utilisateur du 2026-09-23 : « il me manque la slide convictions
# présente dans le PPT convictions.pptx et à compléter d'un pavé convictions sur
# l'agentic » — puis « Fusionner les deux ») : nos convictions et celles de
# l'exemple client (docs/Import/Convictions.pptx, slides 2-3), adaptées à
# l'infra, sur deux slides, plus un pavé agentic. Aucune mention du client
# d'origine. Pattern : formation-po n°30 (liste numérotée de principes) en
# frise verticale, comme l'exemple — onglet numéroté + filet + point de fin.
_CONVICTIONS_1 = [
    ("Partir des utilisateurs et de leurs douleurs, pas du catalogue d'outils.",
     ["Une plateforme n'est adoptée que si elle résout une douleur mesurée chez ceux "
      "qui la consomment."]),
    ("Bien choisir les premiers périmètres de transformation.",
     ["Significatifs au regard de ce que la transformation doit résoudre.",
      "Ni trop complexes, pour réussir et apprendre ; ni trop simples, pour créer du "
      "mouvement et faire émerger des promoteurs."]),
    ("Traiter la problématique avant de construire, et prioriser sur des critères partagés.",
     ["Nommer, scorer, prioriser (valeur, coût, complexité) libère la capacité que le RUN "
      "confisque aujourd'hui.",
      "Des décisions ritualisées, reliées au budget."]),
    ("Un propriétaire, une roadmap, une valeur mesurée.",
     ["Sans porteur produit, l'infra retourne au guichet."]),
]
_CONVICTIONS_2 = [
    ("Articuler la transformation à tous les niveaux.",
     ["Central (DSI et sponsor, garants de l'approche) ; opérationnel (animation des "
      "équipes) ; transverse (fluidifier les interactions entre équipes).",
      "RH : rôles, parcours de formation, accompagnement des profils clés."]),
    ("S'améliorer en continu, au rythme des saisons.",
     ["Mesure systématique et transparente des progrès, à tous les niveaux.",
      "Des équipes redevables de leurs améliorations ; succès et erreurs partagés."]),
    ("Nous rendre dispensables.",
     ["Transmettre pour que vos équipes portent et incarnent la transformation : la "
      "réussite se mesure au jour où elles tiennent le modèle sans nous."]),
]
_CONVICTION_AGENTIC = (
    "L'IA fait gagner du temps là où il est perdu, pas là où on décide.",
    ["Elle accélère le diagnostic, la qualification des demandes et la restitution : le "
     "temps de triage du RUN est rendu aux équipes, mesuré dès le T0, pas promis.",
     "Une expertise OCTO qui complète notre démarche : jamais un prérequis, toujours "
     "après le gate de confidentialité."],
)


def _frise_convictions(s, items, debut, txt_w, accent_idx, top0):
    tab_w, tab_h = 0.50, 0.34
    tab_x = MARGIN
    fil_x = tab_x + 0.10
    txt_x = MARGIN + tab_w + 0.30
    t_size, b_size = 10.5, 9

    def lh(pt, ls):
        return pt * ls / 72.0

    hauteurs = []
    for claim, puces in items:
        h = _lignes(claim, txt_w, t_size) * lh(t_size, 1.15) + 0.05
        pw = txt_w - (0.16 if len(puces) > 1 else 0)
        h += sum(_lignes(p, pw, b_size) * lh(b_size, 1.2) + 0.03 for p in puces)
        hauteurs.append(max(tab_h, h))
    dispo = CONTENT_BOTTOM - top0
    gap = min(0.34, (dispo - sum(hauteurs)) / max(1, len(hauteurs) - 1))
    if gap < 0.10:
        raise SystemExit(f"convictions : contenu trop haut ({gap:.2f}in d'interligne)")
    y = top0
    for i, ((claim, puces), h) in enumerate(zip(items, hauteurs, strict=True)):
        accent = i == accent_idx
        onglet = s.shapes.add_shape(MSO_SHAPE.ROUND_2_DIAG_RECTANGLE, Inches(tab_x),
                                    Inches(y), Inches(tab_w), Inches(tab_h))
        _sans_ombre(onglet)
        onglet.fill.solid()
        onglet.fill.fore_color.rgb = _rgb(NAVY if accent else WHITE)
        onglet.line.color.rgb = _rgb(NAVY)
        onglet.line.width = Pt(1.25)
        D.add_text(s, tab_x, y, tab_w, tab_h, [
            (f"{debut + i}.", dict(size=12, bold=True, color=WHITE if accent else NAVY,
                                   align=PP_ALIGN.CENTER)),
        ], anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
        bas = y + h + gap * 0.45
        D.add_rect(s, fil_x - 0.008, y + tab_h, 0.016, bas - (y + tab_h), fill=NAVY)
        _oval(s, fil_x - 0.04, bas - 0.04, 0.08, 0.08, fill=NAVY)
        paras = [([(claim, dict(size=t_size, bold=True, color=NAVY))], dict(line_spacing=1.15))]
        for p in puces:
            runs = ([("–  ", dict(size=b_size, bold=True, color=NAVY))] if len(puces) > 1 else []) \
                + [(p, dict(size=b_size, color=MUTED))]
            paras.append((runs, dict(line_spacing=1.2, space_before=2)))
        _rich(s, txt_x, y - 0.02, txt_w, h + 0.04, paras, anchor=MSO_ANCHOR.TOP)
        y += h + gap


def slide_convictions(prs):
    s = content_slide(prs, None, "Nos convictions sur votre transformation en mode produit "
                      "(1/2) — les conditions qui favorisent le succès", color=ENCRE)
    txt_x = MARGIN + 0.50 + 0.30
    ph_w = 2.30
    _frise_convictions(s, _CONVICTIONS_1, 1, BORD_DROIT - ph_w - 0.30 - txt_x, 0, CONTENT_TOP + 0.10)
    _photo_libre(s, "tropical", 0, BORD_DROIT - ph_w, CONTENT_TOP + 0.10, ph_w, 3.90)
    return s


def slide_convictions_2(prs):
    """Suite de la frise (5 à 7), sans aplat navy : le pavé agentic à droite
    porte l'unique accent de la slide par un contour épais navy et un filet
    cyan EN APLAT — jamais un 2e fond navy (charte : un seul accent)."""
    s = content_slide(prs, None, "Nos convictions sur votre transformation en mode produit (2/2)",
                       color=ENCRE)
    pav_w = 3.05
    pav_x = BORD_DROIT - pav_w
    txt_x = MARGIN + 0.50 + 0.30
    _frise_convictions(s, _CONVICTIONS_2, 5, pav_x - 0.35 - txt_x, -1, CONTENT_TOP + 0.10)
    titre, puces = _CONVICTION_AGENTIC
    top = CONTENT_TOP + 0.10
    h = 2.95   # dimensionné au contenu (étiré, il laissait ~1in de vide)
    D.add_rect(s, pav_x, top, pav_w, h, fill=WHITE, line=NAVY, line_w=2.25, rounded=True, radius=0.08)
    D.add_rect(s, pav_x + 0.12, top + 0.18, 0.06, h - 0.36, fill=ACCENT_PLEIN, rounded=True, radius=0.5)
    paras = [
        ([("NOTRE CONVICTION SUR L'AGENTIC", dict(size=8, bold=True, color=MUTED))], dict()),
        ([(titre, dict(size=11.5, bold=True, color=NAVY))], dict(space_before=6, line_spacing=1.15)),
    ]
    for p in puces:
        paras.append(([("–  ", dict(size=9, bold=True, color=NAVY)), (p, dict(size=9, color=NAVY))],
                      dict(space_before=8, line_spacing=1.25)))
    _rich(s, pav_x + 0.34, top + 0.22, pav_w - 0.52, h - 0.4, paras, anchor=MSO_ANCHOR.TOP)
    _photo_libre(s, "nightsky", 0, pav_x, top + h + 0.18, pav_w, CONTENT_BOTTOM - (top + h + 0.18))
    return s


# --- v2.41 : chapitre « L'expertise agentic d'OCTO » (retour utilisateur du
# 2026-09-23 : « la démarche agentic tombe comme un cheveu dans la soupe, il
# faudrait l'introduire comme une expertise d'OCTO qui permet de compléter une
# démarche existante en répondant à des besoins complémentaires »).
def slide_intro_agentic(prs):
    """Ouvre le chapitre par les BESOINS, pas par l'outil. Pattern :
    transformation-commerciale n°13 (chaîne de paires constat → réponse reliées
    par chevron) + bandeau de clôture signature."""
    s = content_slide(prs, None, "Une expertise OCTO qui complète notre démarche",
                       color=ENCRE)
    D.add_text(s, MARGIN, CONTENT_TOP, CONTENT_W, 0.30, [
        ("Là où notre démarche a des besoins complémentaires, l'expertise agentic d'OCTO "
         "y répond — sans rien remplacer de ce qui existe.",
         dict(size=D.TYPE["small"], color=NAVY, italic=True)),
    ])
    paires = [
        ("Accélérer le diagnostic",
         "Les interviews et les données s'accumulent plus vite que l'équipe ne les lit.",
         "Des workflows outillés préparent les trames d'interview, la synthèse et le deck "
         "de restitution — le consultant garde l'analyse."),
        ("Trier le RUN",
         "Les mêmes tickets reviennent et mobilisent les experts seniors.",
         "Un agent de triage classe et route les tickets selon un runbook déjà écrit, "
         "sous gate, supervisé avant d'être délégué."),
        ("Capitaliser le savoir",
         "Le savoir-faire reste dans quelques têtes et dans des procédures dispersées.",
         "Un agent documentaire répond avec sa source, et un export markdown versionné "
         "reste à l'équipe après la mission."),
    ]
    besoin_w = 1.75
    constat_w = 2.55
    chev_w = 0.40
    rep_x = MARGIN + besoin_w + 0.12 + constat_w + chev_w
    rep_w = BORD_DROIT - rep_x
    size = 9
    lh = size * 1.25 / 72.0
    row_h = max(max(_lignes(c, constat_w - 0.3, size), _lignes(r, rep_w - 0.3, size))
                for _, c, r in paires) * lh + 0.22
    head_top = CONTENT_TOP + 0.38
    for x, w, lab in ((MARGIN, besoin_w, "BESOIN COMPLÉMENTAIRE"),
                      (MARGIN + besoin_w + 0.12, constat_w, "CE QUI FREINE AUJOURD'HUI"),
                      (rep_x, rep_w, "CE QU'OCTO APPORTE")):
        D.add_text(s, x, head_top, w, 0.2, [(lab, dict(size=8, bold=True, color=MUTED))])
    gap = 0.10
    y = head_top + 0.24
    for besoin, constat, reponse in paires:
        D.add_rect(s, MARGIN, y, besoin_w, row_h, fill=NAVY, rounded=True, radius=0.12)
        D.add_text(s, MARGIN + 0.14, y, besoin_w - 0.28, row_h, [
            (besoin, dict(size=10, bold=True, color=WHITE, line_spacing=1.1)),
        ], anchor=MSO_ANCHOR.MIDDLE)
        cx = MARGIN + besoin_w + 0.12
        D.add_rect(s, cx, y, constat_w, row_h, fill=WHITE, line=LINE, line_w=0.75,
                   rounded=True, radius=0.12)
        D.add_text(s, cx + 0.15, y, constat_w - 0.3, row_h, [
            (constat, dict(size=size, color=MUTED, line_spacing=1.25)),
        ], anchor=MSO_ANCHOR.MIDDLE)
        _chevron_shape(s, cx + constat_w + 0.08, y + row_h / 2 - 0.18, chev_w - 0.16, 0.36)
        D.add_rect(s, rep_x, y, rep_w, row_h, fill=WHITE, line=NAVY, line_w=1.25,
                   rounded=True, radius=0.12)
        D.add_text(s, rep_x + 0.15, y, rep_w - 0.3, row_h, [
            (reponse, dict(size=size, color=NAVY, line_spacing=1.25)),
        ], anchor=MSO_ANCHOR.MIDDLE)
        y += row_h + gap
    _bandeau_cloture(
        s, "Jamais un prérequis : la démarche tient sans elle — l'expertise agentic "
           "l'accélère là où le temps est perdu.",
        y - gap + 0.10, "slide_intro_agentic", size=10)
    return s


def slide_ia_sous_controle(prs):
    """v2.41 : fusion de slide_gate_ia (D0-D4) et slide_prudence_ia (frein
    chiffré). Pattern : grille de maturité à libellés par ligne (restitution
    n°15) à gauche + encart de mise en exergue (pattern 6) à droite."""
    s = content_slide(prs, None,
                       "Sous contrôle : la donnée fixe le mode d'exécution, la prudence freine le score",
                       color=ENCRE)
    D.add_text(s, MARGIN, CONTENT_TOP, CONTENT_W, 0.30, [
        ("Checkpoint toujours humain avant tout usage IA sur donnée client — le gate de "
         "confidentialité, quel que soit le mode d'exécution retenu.",
         dict(size=8.5, color=MUTED, italic=True)),
    ])
    rows = [
        ("D0", "Public", "Articles publics, docs méthodo", "IA externe possible"),
        ("D1", "Interne", "Organisation macro, catalogue anonymisé", "IA client recommandée"),
        ("D2", "Confidentiel", "Notes d'interview, reporting", "IA client ou LLM privé"),
        ("D3", "Restreint", "Tickets détaillés, logs, CMDB, IAM", "LLM local, contrôles forts"),
        ("D4", "Critique", "Secrets de production, données réglementées", "Local, sans IA générative"),
    ]
    gauche_w = 5.15
    top0 = CONTENT_TOP + 0.62
    D.add_text(s, MARGIN, top0 - 0.26, gauche_w, 0.2, [
        ("LE GATE DE CONFIDENTIALITÉ — LA DONNÉE DÉCIDE DU MODE",
         dict(size=8, bold=True, color=MUTED)),
    ])
    row_h, row_gap = 0.50, 0.08
    chip_w = 1.30
    ex_w = 2.05
    for i, (code, nom, ex, mode) in enumerate(rows):
        y = top0 + i * (row_h + row_gap)
        chip(s, MARGIN, y, chip_w, row_h, f"{code} · {nom}", SEVERITE[i], size=8.5)
        D.add_text(s, MARGIN + chip_w + 0.14, y, ex_w, row_h, [
            (ex, dict(size=8.5, color=NAVY, line_spacing=1.15)),
        ], anchor=MSO_ANCHOR.MIDDLE)
        D.add_text(s, MARGIN + chip_w + 0.14 + ex_w + 0.08, y,
                   gauche_w - chip_w - ex_w - 0.22, row_h, [
            (mode, dict(size=8.5, italic=True, color=MUTED, line_spacing=1.15)),
        ], anchor=MSO_ANCHOR.MIDDLE)
    bas = top0 + len(rows) * row_h + (len(rows) - 1) * row_gap

    pan_x = MARGIN + gauche_w + 0.25
    pan_w = BORD_DROIT - pan_x
    pan_top = top0 - 0.26
    pan_h = bas - pan_top
    D.add_rect(s, pan_x, pan_top, pan_w, pan_h, fill=NAVY, rounded=True, radius=0.08)
    pad = 0.18
    facteurs = [
        ("Confidentialité", "reprend la classe D0-D4 : plus la donnée est sensible, plus le score monte."),
        ("Supervision", "un agent encore au stade assisté pèse plus lourd qu'un agent éprouvé."),
        ("Criticité", "une décision irréversible pèse plus qu'une recommandation réversible."),
    ]
    paras = [
        ([("PRUDENCE IA — UN FREIN CHIFFRÉ", dict(size=8, bold=True, color="#c7cbe0"))], dict()),
        ([("= confidentialité + supervision + criticité", dict(size=10.5, bold=True, color=WHITE))],
         dict(space_before=4)),
    ]
    for nom, txt in facteurs:
        paras.append(([(nom + " : ", dict(size=8.5, bold=True, color=WHITE)),
                       (txt, dict(size=8.5, color="#c7cbe0"))],
                      dict(space_before=7, line_spacing=1.2)))
    paras.append(([("Soustraite de impact × faisabilité : un frein, pas un veto — avancer malgré "
                    "un score élevé reste possible, et se documente.",
                    dict(size=8.5, bold=True, color=WHITE))], dict(space_before=10, line_spacing=1.2)))
    _rich(s, pan_x + pad, pan_top + pad, pan_w - 2 * pad, pan_h - 2 * pad, paras,
          anchor=MSO_ANCHOR.TOP)
    return s


def slide_ambition_si(prs):
    """v2.41 : fusion de slide_ambition, slide_architecture_si et
    slide_iap_contexte_client — trois niveaux d'ambition, et ce que chacun
    change dans le lien au SI et dans ce qui passe chez le client. Pattern :
    restitution n°8 (blueprint en bandes), une bande par niveau, sans flèche
    entre elles (« pas un spectre linéaire »). Niveau A en accent (un sur N)."""
    s = content_slide(prs, None,
                       "Trois niveaux d'ambition : seul ce qui passe chez le client change, pas la méthode",
                       color=ENCRE)
    rows = [
        ("A", "Aide au coach", "État actuel (MVP0–MVP5)",
         "Génère un livrable à la demande ; le consultant pilote à 100 %.",
         "Exports ponctuels et interviews — aucune connexion.",
         "Rien ne s'installe : livrables markdown et deck, sur le poste du consultant."),
        ("B", "Assistant interactif", "Palier intermédiaire",
         "Guide pas à pas, pose des questions, signale les incohérences.",
         "Exports + app de capture terrain, site centralisé.",
         "L'app de capture et un tableau de bord multi-engagements."),
        ("C", "Companion connecté", "MVP6, non engagé",
         "Quasi autonome sur la collecte et la préparation — jamais sur l'arbitrage.",
         "Connecteurs API directs, en continu (ServiceNow, Jira, CMDB, FinOps…).",
         "Un accès direct aux données de production : un risque d'un autre ordre."),
    ]
    champs = ["CE QU'IL FAIT", "LIEN AU SI", "CE QUI PASSE CHEZ LE CLIENT"]
    left_w = 2.0
    fx0 = MARGIN + left_w + 0.15
    fgap = 0.14
    fw = (BORD_DROIT - fx0 - 2 * fgap) / 3
    size = 8.5
    lh = size * 1.25 / 72.0
    head_top = CONTENT_TOP + 0.05
    for k, c in enumerate(champs):
        D.add_text(s, fx0 + k * (fw + fgap), head_top, fw, 0.2, [
            (c, dict(size=8, bold=True, color=MUTED)),
        ])
    y = head_top + 0.28
    gap = 0.14
    for i, (code, nom, etat, fait, si, client) in enumerate(rows):
        lignes = max(_lignes(t, fw - 0.1, size) for t in (fait, si, client))
        h = max(0.80, lignes * lh + 0.30)
        accent = i == 0
        D.add_rect(s, MARGIN, y, CONTENT_W, h, fill=WHITE, line=NAVY if accent else LINE,
                   line_w=1.25 if accent else 0.75, rounded=True, radius=0.10)
        D.add_rect(s, MARGIN, y, left_w, h, fill=NAVY if accent else TRACK, rounded=True, radius=0.10)
        _badge(s, MARGIN + 0.32, y + h / 2, 0.40, WHITE if accent else NAVY, code,
               text_color=NAVY if accent else WHITE, size=13)
        D.add_text(s, MARGIN + 0.62, y, left_w - 0.7, h, [
            (nom, dict(size=10, bold=True, color=WHITE if accent else NAVY, line_spacing=1.1)),
            (etat, dict(size=8, italic=True, color="#c7cbe0" if accent else MUTED, space_before=2)),
        ], anchor=MSO_ANCHOR.MIDDLE)
        for k, t in enumerate((fait, si, client)):
            D.add_text(s, fx0 + k * (fw + fgap), y, fw, h, [
                (t, dict(size=size, color=NAVY, line_spacing=1.25, bold=(k == 2))),
            ], anchor=MSO_ANCHOR.MIDDLE)
        y += h + gap
    D.add_text(s, MARGIN, y - gap + 0.10, CONTENT_W, 0.40, [
        ("À tout niveau, les agents candidats retenus ne passent chez le client qu'en ②/③, sous "
         "gate. Un cabinet peut durablement rester au niveau A ou B par choix de gouvernance.",
         dict(size=8.5, italic=True, color=MUTED, line_spacing=1.2)),
    ])
    return s


# --- v2.42 (retours utilisateur du 2026-09-23) ---------------------------------
def slide_cout_si_rien_ne_change(prs):
    """v2.42 : fusion de slide_enjeux, slide_infra_run et slide_infra_transverse
    (chapitre « Ce que ça coûte » ramené à 3 slides). Pattern : restitution n°7
    (rangée de cartes, une en accent) + bandeau de clôture."""
    s = content_slide(prs, None,
                       "Si rien ne change : un RUN permanent, une infra orpheline, une DSI qui pilote à vue",
                       color=ENCRE)
    D.add_text(s, MARGIN, CONTENT_TOP, CONTENT_W, 0.30, [
        ("Quatre parties prenantes interrogées séparément convergent sur un même constat, "
         "lu ici à l'échelle de la DSI.",
         dict(size=D.TYPE["small"], color=NAVY, italic=True)),
    ])
    cartes = [
        ("LE RUN", "Il ne s'arrête jamais, et il puise dans les mêmes experts que le BUILD",
         ["Régime permanent : aucune fin de phase ne libère l'astreinte ni le maintien.",
          "Sa charge vient de l'extérieur — incidents, demandes, obsolescences.",
          "Sa dette ne se voit pas le jour où on la crée : elle se paie plus tard."]),
        ("L'INFRA TRANSVERSE", "Elle sert toutes les équipes et n'appartient à aucune",
         ["Sa problématique est mutualisée : elle ne pèse sur le budget d'aucune équipe.",
          "Personne ne porte le coût, donc personne n'a de raison de le réduire.",
          "Personne n'arbitre seul : fermer un service touche tout le monde."]),
        ("LA DSI", "Elle pilote à vue, et sa promesse reste déclarative",
         ["Aucun signal de flux partagé : un reporting-miroir, pas un pilotage.",
          "Le self-service reste un guichet tant que le contournement va plus vite.",
          "Un gate de confidentialité non instruit peut bloquer toute preuve par l'IA."]),
    ]
    n = len(cartes)
    pad = 0.20
    _, cw = col_x(0, n)
    usable = cw - 2 * pad
    t_size, b_size = 10.5, 9
    titre_h = max(_lignes(t, usable, t_size) for _, t, _ in cartes) * (t_size * 1.2 / 72.0) + 0.06
    corps_h = max(sum(_lignes(b, usable - 0.14, b_size) for b in bs) for *_, bs in cartes) \
        * (b_size * 1.25 / 72.0) + 3 * 0.06 + 0.06
    card_h = 0.18 + 0.22 + titre_h + 0.10 + corps_h + 0.18
    top0 = CONTENT_TOP + 0.48
    for i, (lab, titre, puces) in enumerate(cartes):
        x, w = col_x(i, n)
        accent = i == 0   # « un sur N » : le RUN, cœur du coût
        if accent:
            D.add_rect(s, x, top0, w, card_h, fill=NAVY, rounded=True, radius=0.08)
        else:
            D.add_rect(s, x, top0, w, card_h, fill=WHITE, line=LINE, line_w=0.75,
                       rounded=True, radius=0.08)
        c_txt = WHITE if accent else NAVY
        c_sec = "#c7cbe0" if accent else MUTED
        D.add_text(s, x + pad, top0 + 0.18, usable, 0.22, [
            (f"{i + 1} · {lab}", dict(size=8, bold=True, color=c_sec)),
        ])
        D.add_text(s, x + pad, top0 + 0.40, usable, titre_h, [
            (titre, dict(size=t_size, bold=True, color=c_txt, line_spacing=1.15)),
        ])
        _rich(s, x + pad, top0 + 0.40 + titre_h + 0.10, usable, corps_h, [
            ([("—  ", dict(size=b_size, color=c_sec)), (b, dict(size=b_size, color=c_txt))],
             dict(line_spacing=1.2, space_before=(0 if j == 0 else 4)))
            for j, b in enumerate(puces)
        ])
    _bandeau_cloture(s, "Traiter le RUN comme un projet, c'est le perdre à chaque arbitrage.",
                     top0 + card_h + 0.14, "slide_cout_si_rien_ne_change", size=11)
    return s


_FAMILLES = [
    ("Flux", "Attentes, validations multiples"),
    ("Humain", "Experts seniors sur des tâches répétitives"),
    ("RUN", "Incidents récurrents, demandes répétées"),
    ("Financier", "Surdimensionnement, ressources non décommissionnées"),
    ("Cognitif", "Trop d'outils, procédures complexes"),
    ("Décisionnel", "Arbitrages subjectifs, priorisation opaque"),
    ("Environnemental", "Ressources inutilisées, environnements non éteints"),
    ("IA", "Cas d'usage gadget, automatisation sans garde-fous"),
]


def slide_familles(prs):
    """v2.42 (retour utilisateur : « revoir la forme et le design ») — la grille
    2×4 de cartes quasi vides devient une liste à badge numéroté + pilule de
    définition (formation-po n°20), sur deux colonnes. Reprend en clôture la
    charnière de l'ex-slide Opportunités : nommée, la douleur est traitable."""
    s = content_slide(prs, None,
                       "Les 8 familles de douleur — le langage commun qui rend les douleurs traitables",
                       color=ENCRE)
    D.add_text(s, MARGIN, CONTENT_TOP, CONTENT_W, 0.30, [
        ("Nommer la famille, c'est déjà pouvoir la détecter, la chiffrer et la prioriser.",
         dict(size=D.TYPE["small"], color=NAVY, italic=True)),
    ])
    badge = 0.46
    row_h, row_gap = 0.52, 0.12
    col_gap = 0.35
    colw = (CONTENT_W - col_gap) / 2
    top0 = CONTENT_TOP + 0.48
    for i, (nom, ex) in enumerate(_FAMILLES):
        col, row = i // 4, i % 4
        x = MARGIN + col * (colw + col_gap)
        y = top0 + row * (row_h + row_gap)
        accent = nom == "IA"   # « un sur N » : la famille propre à ce deck
        D.add_rect(s, x, y + (row_h - badge) / 2, badge, badge,
                   fill=NAVY if accent else WHITE, line=NAVY, line_w=1.5,
                   rounded=True, radius=0.18)
        D.add_text(s, x, y + (row_h - badge) / 2, badge, badge, [
            (str(i + 1), dict(size=16, bold=True, color=WHITE if accent else NAVY,
                              align=PP_ALIGN.CENTER)),
        ], anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
        px = x + badge + 0.12
        D.add_rect(s, px, y, colw - badge - 0.12, row_h, fill=WHITE, line=NAVY,
                   line_w=1.0, rounded=True, radius=0.5)
        _rich(s, px + 0.22, y, colw - badge - 0.12 - 0.36, row_h, [
            ([(nom, dict(size=11, bold=True, color=NAVY)),
              ("  —  " + ex, dict(size=9, color=MUTED))], dict()),
        ], anchor=MSO_ANCHOR.MIDDLE)
    bas = top0 + 4 * row_h + 3 * row_gap
    _bandeau_cloture(
        s, "Nommée, une douleur devient traitable : la méthode existe déjà — détaillée au "
           "chapitre L'offre.", bas + 0.14, "slide_familles", size=11)
    return s


def slide_offre_mecanique(prs):
    """v2.42 : fusion de slide_problematiques (trois temps) et
    slide_problematique_partagee (le « à deux ») — chaque temps porte ce que fait le
    client, ce que fait OCTO et ce qui se tranche ensemble. Pattern :
    restitution n°10 (fiches-étapes à chip chevauchant) + n°13 (rubriques)."""
    s = content_slide(prs, None,
                       "Repérer, prioriser, tenir : la problématique se traite à deux, sinon elle retourne à personne",
                       color=ENCRE)
    D.add_text(s, MARGIN, CONTENT_TOP, CONTENT_W, 0.28, [
        ("Même chemin pour chaque famille, avec le client — score = (impact × faisabilité) "
         "− prudence IA, ordinal : il éclaire l'arbitrage, sans le remplacer.",
         dict(size=9, color=NAVY, italic=True)),
    ])
    temps = [
        ("Repérer", "et chiffrer", "On détecte chaque problématique et on la quantifie, preuves à l'appui.",
         "Ouvre ses données — CMDB, facturation, tickets — et nomme ce qui le gêne vraiment.",
         "Apporte la grille des 8 familles et la méthode de quantification.",
         "Le périmètre mesuré, et ce qu'on accepte d'appeler problématique."),
        ("Prioriser", "dans un backlog", "Chaque problématique reçoit un score et prend sa place dans le backlog.",
         "Arbitre ce qu'aucune équipe ne tranche seule : fermer, standardiser, décommissionner.",
         "Instruit les causes racines et propose le score — une proposition, jamais un verdict.",
         "Le backlog priorisé et, pour chaque ligne, le porteur nommé."),
        ("Tenir", "dans la durée", "On expérimente, on mesure le delta réel, puis on industrialise.",
         "Porte les expérimentations et libère le temps qu'elles demandent.",
         "Outille, mesure le delta réel et industrialise ce qui a marché.",
         "Le seuil au-delà duquel on généralise — ou on arrête."),
    ]
    n = 3
    fl = 0.30
    colw = (CONTENT_W - (n - 1) * fl) / n
    pad = 0.16
    u = colw - 2 * pad
    sz = 8.5
    lh = sz * 1.2 / 72.0

    def hh(key):
        return max(_lignes(t[key], u, sz) for t in temps) * lh + 0.04

    h_phr, h_cli, h_oct = hh(2), hh(3), hh(4)
    h_tr = max(_lignes(t[5], u - 0.12, sz) for t in temps) * lh + 0.04
    lab = 0.17
    chip_h = 0.36
    top0 = CONTENT_TOP + 0.62
    y_titre = top0 + chip_h / 2 + 0.08
    y_phr = y_titre + 0.30
    y_cli = y_phr + h_phr + 0.10
    y_oct = y_cli + lab + h_cli + 0.06
    y_tr = y_oct + lab + h_oct + 0.10
    tr_h = lab + h_tr + 0.14
    card_h = y_tr + tr_h + 0.10 - top0
    for i, (verbe, objet, phrase, cli, oct_, tr) in enumerate(temps):
        x = MARGIN + i * (colw + fl)
        D.add_rect(s, x, top0, colw, card_h, fill=WHITE, line=NAVY, line_w=1.0,
                   rounded=True, radius=0.08)
        D.add_rect(s, x + pad, top0 - chip_h / 2, 0.36, chip_h, fill=NAVY, rounded=True, radius=0.5)
        D.add_text(s, x + pad, top0 - chip_h / 2, 0.36, chip_h, [
            (str(i + 1), dict(size=12, bold=True, color=WHITE, align=PP_ALIGN.CENTER)),
        ], anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
        _rich(s, x + pad, y_titre, u, 0.28, [
            ([(verbe, dict(size=13, bold=True, color=NAVY)),
              (" " + objet, dict(size=10, color=MUTED))], dict()),
        ])
        D.add_text(s, x + pad, y_phr, u, h_phr, [(phrase, dict(size=sz, color=NAVY, line_spacing=1.2))])
        D.add_text(s, x + pad, y_cli, u, lab + h_cli, [
            ("CÔTÉ CLIENT", dict(size=8, bold=True, color=MUTED)),
            (cli, dict(size=sz, color=NAVY, line_spacing=1.2)),
        ])
        D.add_text(s, x + pad, y_oct, u, lab + h_oct, [
            ("CÔTÉ OCTO", dict(size=8, bold=True, color=MUTED)),
            (oct_, dict(size=sz, color=NAVY, line_spacing=1.2)),
        ])
        D.add_rect(s, x + 0.08, y_tr, colw - 0.16, tr_h, fill=TRACK, rounded=True, radius=0.08)
        D.add_rect(s, x + 0.08, y_tr + 0.06, 0.05, tr_h - 0.12, fill=ACCENT_PLEIN, rounded=True, radius=0.5)
        D.add_text(s, x + pad + 0.06, y_tr + 0.07, u - 0.06, tr_h - 0.1, [
            ("TRANCHÉ ENSEMBLE", dict(size=8, bold=True, color=NAVY)),
            (tr, dict(size=sz, bold=True, color=NAVY, line_spacing=1.2)),
        ])
        if i < n - 1:
            _fleche_h(s, x + colw, top0 + card_h / 2 - 0.15, fl, 0.30)
    if top0 + card_h > CONTENT_BOTTOM:
        raise SystemExit("slide_offre_mecanique : contenu trop haut")
    return s


def slide_team_topologies(prs):
    """v2.42 (retour utilisateur « revoir la slide ») — l'organigramme et son
    gros encart gris deviennent une correspondance archétype → rôle en pilules
    (transformation-commerciale n°6, variante pilule label + pilule contour).
    La Platform Team en accent ; l'extension « agents IA » en pilule pointillée."""
    s = content_slide(prs, None, "La cible IAP est une Platform Team", color=ENCRE)
    D.add_text(s, MARGIN, CONTENT_TOP, CONTENT_W, 0.28, [
        ("Team Topologies décrit 4 archétypes reliés entre eux : les 3 autres s'articulent "
         "autour de la Platform Team.",
         dict(size=9, color=NAVY, italic=True)),
    ])
    rows = [
        ("Platform Team", "Capacités en self-service (X-as-a-Service)",
         "La cible même de la transformation IAP", True, False),
        ("Stream-aligned", "Flux de valeur métier continu",
         "Les équipes applicatives, clientes de la plateforme", False, False),
        ("Enabling", "Montée en compétence temporaire",
         "La posture du coach — jamais permanente", False, False),
        ("Complicated-subsystem", "Expertise pointue, compétences rares",
         "Un vrai sous-système complexe, pas un produit plateforme", False, False),
        ("+ Agents IA", "Coéquipier d'équipe ou capacité de la plateforme",
         "4e mode d'interaction, la Supervision : mandat écrit, assisté → supervisé → délégué",
         False, True),
    ]
    lab_w = 2.25
    row_h, gap = 0.56, 0.12
    top0 = CONTENT_TOP + 0.48
    D.add_text(s, MARGIN + lab_w + 0.18, top0 - 0.24, 3.0, 0.2, [
        ("CE QU'IL APPORTE", dict(size=8, bold=True, color=MUTED))])
    D.add_text(s, MARGIN + lab_w + 0.18 + 3.1, top0 - 0.24, 3.0, 0.2, [
        ("DANS LA CIBLE IAP", dict(size=8, bold=True, color=MUTED))])
    for i, (nom, apport, cible, accent, pointille) in enumerate(rows):
        y = top0 + i * (row_h + gap) + (0.08 if pointille else 0)
        if pointille:
            _dashed_rect(s, MARGIN, y, lab_w, row_h, fill=WHITE, line=NAVY, line_w=1.0, radius=0.5)
        else:
            D.add_rect(s, MARGIN, y, lab_w, row_h, fill=NAVY if accent else WHITE,
                       line=NAVY, line_w=1.25, rounded=True, radius=0.5)
        D.add_text(s, MARGIN, y, lab_w, row_h, [
            (nom, dict(size=10.5, bold=True, color=WHITE if accent else NAVY, align=PP_ALIGN.CENTER)),
        ], anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
        px = MARGIN + lab_w + 0.10
        pw = BORD_DROIT - px
        if pointille:
            _dashed_rect(s, px, y, pw, row_h, fill=WHITE, line=NAVY, line_w=1.0, radius=0.5)
        else:
            D.add_rect(s, px, y, pw, row_h, fill=WHITE, line=NAVY if accent else LINE,
                       line_w=1.5 if accent else 0.75, rounded=True, radius=0.5)
        D.add_text(s, px + 0.25, y, 2.85, row_h, [
            (apport, dict(size=9, bold=accent, color=NAVY, line_spacing=1.15)),
        ], anchor=MSO_ANCHOR.MIDDLE)
        D.add_text(s, px + 3.1, y, pw - 3.25, row_h, [
            (cible, dict(size=9, bold=accent, color=NAVY if accent else MUTED, line_spacing=1.15)),
        ], anchor=MSO_ANCHOR.MIDDLE)
    return s


# --- v2.43 : phase design (demande utilisateur « rendre plus jolies toutes les
# slides »). Nouvelles définitions ; les anciennes sont retirées du fichier.
def slide_why_iap(prs):
    """v2.43 — la thèse en bandeau navy (seul aplat plein), puis les trois
    bascules en liste numérotée (formation-po n°30) : badge, bascule, détail, et
    à droite le persona auquel elle répond."""
    s = content_slide(prs, None,
                       "Pourquoi « Infrastructure as a Product » — le socle de la proposition",
                       color=ENCRE)
    th_h = 1.00
    ph_w = 2.10
    th_w = CONTENT_W - ph_w - 0.18
    D.add_rect(s, MARGIN, CONTENT_TOP, th_w, th_h, fill=NAVY, rounded=True, radius=0.10)
    _photo_libre(s, "sunset", 1, BORD_DROIT - ph_w, CONTENT_TOP, ph_w, th_h)
    D.add_rect(s, MARGIN + 0.10, CONTENT_TOP + 0.14, 0.06, th_h - 0.28, fill=ACCENT_PLEIN,
               rounded=True, radius=0.5)
    D.add_text(s, MARGIN + 0.34, CONTENT_TOP, th_w - 0.5, th_h, [
        ("Traiter l'infrastructure comme un produit, pas comme un guichet.",
         dict(size=13, bold=True, color=WHITE)),
        ("Des utilisateurs, un cycle de vie, une valeur mesurée — trois bascules qui "
         "répondent aux personas et à leurs douleurs.",
         dict(size=9, color="#c7cbe0", space_before=3)),
    ], anchor=MSO_ANCHOR.MIDDLE)
    bascules = [
        ("Des utilisateurs, pas des tickets",
         "On conçoit l'adoption — self-service, onboarding, parcours — au lieu de subir un "
         "guichet que le contournement rend inutile.", "l'utilisateur applicatif"),
        ("Un cycle de vie, une équipe qui en répond",
         "Le produit a un propriétaire, une roadmap et une dette gérée : on sort du RUN subi "
         "et on récupère de la capacité.", "l'infra & le RUN"),
        ("Un pilotage par la valeur",
         "On mesure l'usage et la valeur produite, pas l'activité : un signal de flux fiable, "
         "des KPIs de mission — pas du reporting-miroir.", "le management & le sponsor"),
    ]
    top0 = CONTENT_TOP + th_h + 0.30
    gap = 0.16
    row_h = (CONTENT_BOTTOM - top0 - 2 * gap) / 3
    badge = 0.50
    chip_w = 1.95
    for i, (titre, det, qui) in enumerate(bascules):
        y = top0 + i * (row_h + gap)
        D.add_rect(s, MARGIN, y, CONTENT_W, row_h, fill=WHITE, line=LINE, line_w=0.75,
                   rounded=True, radius=0.12)
        _badge(s, MARGIN + 0.22 + badge / 2, y + row_h / 2, badge, NAVY, str(i + 1), size=15)
        tx = MARGIN + 0.22 + badge + 0.22
        tw = CONTENT_W - (tx - MARGIN) - chip_w - 0.35
        D.add_text(s, tx, y, tw, row_h, [
            (titre, dict(size=11, bold=True, color=NAVY)),
            (det, dict(size=9, color=MUTED, space_before=2, line_spacing=1.2)),
        ], anchor=MSO_ANCHOR.MIDDLE)
        cx = BORD_DROIT - chip_w - 0.18
        D.add_rect(s, cx, y + row_h / 2 - 0.25, chip_w, 0.50, fill=WHITE, line=NAVY,
                   line_w=1.0, rounded=True, radius=0.5)
        D.add_text(s, cx, y + row_h / 2 - 0.25, chip_w, 0.50, [
            ("RÉPOND À", dict(size=8, bold=True, color=MUTED, align=PP_ALIGN.CENTER)),
            (qui, dict(size=9, bold=True, color=NAVY, align=PP_ALIGN.CENTER)),
        ], anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
    return s


def slide_trajectoire(prs):
    """v2.43 — retouche validée : plus de mention d'agent IA (la démarche tient
    sans IA ; le chapitre L'expertise agentic d'OCTO les couvre). Pattern :
    restitution n°11 (colonnes de phase), texte ≥ 8 pt, clôture en bandeau."""
    s = content_slide(prs, None,
                       "Trois temps et une boucle — chaque phase produit son livrable de décision",
                       color=ENCRE)
    phases = [
        ("①", "Assessment flash", "2 semaines",
         "Collecte, diagnostic, conception et restitution.",
         "Deck exécutif de restitution", "Sponsor · comité de lancement"),
        ("②", "Premier déploiement", "4 à 5 semaines",
         "1 à 2 équipes pilotes volontaires, mode Coach dominant.",
         "Deck de plan de déploiement · export markdown", "Équipes pilotes · management"),
        ("③", "Implémentation itérative", "jusqu'à T+6-12 mois",
         "Généralisation équipe par équipe, du mode Coach au mode Délégué.",
         "Deck de comité de pilotage (périodique)", "Instance de comitologie"),
        ("⟲", "Boucle de réévaluation", "T+6-12 mois",
         "La réévaluation reboucle vers la collecte et alimente la bibliothèque de REX.",
         "Deck de bilan · markdown amendé", "Sponsor"),
    ]
    n = len(phases)
    badge_d = 0.56
    top0 = CONTENT_TOP + 0.08
    D.add_rect(s, MARGIN + 0.4, top0 + badge_d / 2 - 0.012, CONTENT_W - 0.8, 0.024, fill=LINE)
    _, wcol = col_x(0, n)
    desc_h = max(_lignes(p[3], wcol - 0.1, 9) for p in phases) * (9 * 1.2 / 72.0) + 0.06
    livr_h = max(_lignes(p[4], wcol - 0.24, 9) for p in phases) * (9 * 1.2 / 72.0) + 0.62
    for i, (sym, titre, duree, desc, livrable, pour_qui) in enumerate(phases):
        x, w = col_x(i, n)
        cx = x + w / 2 - badge_d / 2
        accent = i == 0   # « un sur N » : l'Assessment flash, la décision demandée
        D.add_rect(s, cx, top0, badge_d, badge_d, fill=NAVY if accent else WHITE,
                   line=NAVY, line_w=1.5, rounded=True, radius=0.5)
        D.add_text(s, cx, top0, badge_d, badge_d, [
            (sym, dict(size=16, bold=(sym != "⟲"), color=WHITE if accent else NAVY,
                       align=PP_ALIGN.CENTER)),
        ], anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
        ty = top0 + badge_d + 0.12
        D.add_text(s, x, ty, w, 0.25, [
            (titre, dict(size=10.5, bold=True, color=NAVY, align=PP_ALIGN.CENTER)),
        ], align=PP_ALIGN.CENTER)
        D.add_text(s, x, ty + 0.26, w, 0.22, [
            (duree, dict(size=8.5, italic=True, color=MUTED, align=PP_ALIGN.CENTER)),
        ], align=PP_ALIGN.CENTER)
        dy = ty + 0.56
        D.add_text(s, x + 0.06, dy, w - 0.12, desc_h, [
            (desc, dict(size=9, color=NAVY, align=PP_ALIGN.CENTER, line_spacing=1.2)),
        ], align=PP_ALIGN.CENTER)
        ly = dy + desc_h + 0.12
        D.add_rect(s, x, ly, w, livr_h, fill=WHITE, line=NAVY if accent else LINE,
                   line_w=1.25 if accent else 0.75, rounded=True, radius=0.10)
        D.add_text(s, x + 0.12, ly, w - 0.24, livr_h, [
            ("LIVRABLE-CLÉ", dict(size=8, bold=True, color=MUTED, align=PP_ALIGN.CENTER)),
            (livrable, dict(size=9, bold=True, color=NAVY, space_before=2,
                            align=PP_ALIGN.CENTER, line_spacing=1.15)),
            (pour_qui, dict(size=8, italic=True, color=MUTED, space_before=3,
                            align=PP_ALIGN.CENTER)),
        ], anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
    bas = ly + livr_h
    _bandeau_cloture(s, "Quatre livrables-clés, quatre profils d'un même générateur modulaire "
                        "— pas quatre outils distincts.", bas + 0.16, "slide_trajectoire", size=11)
    return s


def slide_specificites_infra(prs):
    """v2.43 — chaîne de paires constat → réponse (transformation-commerciale
    n°13) : mêmes formes pour les deux lignes (avant : une pilule, une carte),
    l'IA en ligne pointillée qui amplifie le constat, clôture en bandeau."""
    s = content_slide(prs, None,
                       "D'un guichet sursollicité à une infra as a product — l'IA rend ce virage nécessaire.",
                       color=ENCRE)
    paires = [
        ("Sortir de la sursollicitation et du guichet",
         "Des équipiers qui font trop de choses, engorgés — décommissionnement jamais fait, "
         "trop de RUN au quotidien.",
         "Assainir et travailler la problématique"),
        ("Mieux servir les utilisateurs",
         "Passer d'un guichet de demandes à une approche as a service.",
         "Une infra recentrée sur ses utilisateurs"),
    ]
    cw = 4.45
    chev = 0.55
    rx = MARGIN + cw + chev
    rw = BORD_DROIT - rx
    D.add_text(s, MARGIN, CONTENT_TOP + 0.02, cw, 0.2, [("CE QUE VIT L'INFRA", dict(size=8, bold=True, color=MUTED))])
    D.add_text(s, rx, CONTENT_TOP + 0.02, rw, 0.2, [("CE QU'ON VISE", dict(size=8, bold=True, color=MUTED))])
    y = CONTENT_TOP + 0.28
    row_h = 0.88
    for titre, det, rep in paires:
        D.add_rect(s, MARGIN, y, cw, row_h, fill=WHITE, line=LINE, line_w=0.75, rounded=True, radius=0.12)
        D.add_text(s, MARGIN + 0.2, y, cw - 0.4, row_h, [
            (titre, dict(size=11, bold=True, color=NAVY)),
            (det, dict(size=9, color=MUTED, space_before=2, line_spacing=1.2)),
        ], anchor=MSO_ANCHOR.MIDDLE)
        _chevron_shape(s, MARGIN + cw + 0.12, y + row_h / 2 - 0.2, chev - 0.24, 0.40)
        D.add_rect(s, rx, y, rw, row_h, fill=WHITE, line=NAVY, line_w=1.5, rounded=True, radius=0.12)
        D.add_text(s, rx + 0.2, y, rw - 0.4, row_h, [
            (rep, dict(size=11.5, bold=True, color=NAVY)),
        ], anchor=MSO_ANCHOR.MIDDLE)
        y += row_h + 0.14
    y += 0.08
    ia_h = 0.80
    _dashed_rect(s, MARGIN, y, CONTENT_W, ia_h, fill=WHITE, line=NAVY, line_w=1.0, radius=0.12)
    _badge(s, MARGIN + 0.45, y + ia_h / 2, 0.50, NAVY, "IA", size=12)
    D.add_text(s, MARGIN + 0.9, y, CONTENT_W - 1.1, ia_h, [
        ("AVEC L'ARRIVÉE DE L'IA — UNE SURSOLLICITATION EXACERBÉE", dict(size=8.5, bold=True, color=NAVY)),
        ("Trop de demandes, des équipes engorgées : la même pression que le guichet d'hier, "
         "amplifiée par l'IA plutôt que résolue par elle.",
         dict(size=9.5, color=NAVY, space_before=3, line_spacing=1.2)),
    ], anchor=MSO_ANCHOR.MIDDLE)
    _bandeau_cloture(s, "L'objectif : infra as a product.", y + ia_h + 0.14,
                     "slide_specificites_infra", size=12)
    return s


def slide_mission(prs):
    """v2.43 — sandwich organisationnel (restitution n°5) : le principe en
    bandeau haut, les deux piliers, l'équilibre tenu en bandeau bas. Texte
    ≥ 9 pt ; la carte TRANSFORMER en accent (ce que le sponsor achète)."""
    s = content_slide(prs, None, "Une double mission : transformer ET assainir", color=ENCRE)
    D.add_rect(s, MARGIN, CONTENT_TOP, CONTENT_W, 0.52, fill=TRACK, rounded=True, radius=0.12)
    D.add_text(s, MARGIN + 0.25, CONTENT_TOP, CONTENT_W - 0.5, 0.52, [
        ("Deux piliers ni séquentiels ni optionnels : une cible produit sans traitement du "
         "problématique manque de capacité pour s'y déployer ; l'inverse reste une réduction de "
         "coûts sans vision.", dict(size=9.5, italic=True, color=NAVY, line_spacing=1.2)),
    ], anchor=MSO_ANCHOR.MIDDLE)
    piliers = [
        ("TRANSFORMER",
         "Cible produit/plateforme : utilisateurs identifiés, valeur, roadmap, engagements "
         "de qualité, gouvernance lisible.",
         "La vision à moyen terme — ce que le sponsor achète."),
        ("ASSAINIR",
         "Traitement mesurable des problématiques : flux, RUN, humain, financier, cognitif, "
         "décisionnel, environnemental, IA.",
         "La capacité récupérée finance la trajectoire produit — hypothèse à prouver, qui "
         "suppose une réallocation budgétaire côté client."),
    ]
    top0 = CONTENT_TOP + 0.52 + 0.20
    ph = 2.20
    for i, (nom, vise, fin) in enumerate(piliers):
        x, w = col_x(i, 2)
        accent = i == 0
        D.add_rect(s, x, top0, w, ph, fill=NAVY if accent else WHITE,
                   line=None if accent else NAVY, line_w=1.25, rounded=True, radius=0.08)
        ct, cs = (WHITE, "#c7cbe0") if accent else (NAVY, MUTED)
        D.add_text(s, x + 0.28, top0 + 0.18, w - 0.56, ph - 0.3, [
            (nom, dict(size=18, bold=True, color=ct)),
            ("CE QU'IL VISE", dict(size=8, bold=True, color=cs, space_before=10)),
            (vise, dict(size=9.5, color=ct, space_before=2, line_spacing=1.2)),
            ("CE QU'IL FINANCE", dict(size=8, bold=True, color=cs, space_before=10)),
            (fin, dict(size=9.5, color=ct, space_before=2, line_spacing=1.2)),
        ])
    by = top0 + ph + 0.20
    D.add_text(s, MARGIN, by, CONTENT_W, 0.2, [
        ("L'ÉQUILIBRE QUE LA DOUBLE MISSION TIENT EN PERMANENCE", dict(size=8, bold=True, color=MUTED)),
    ])
    tensions = ["Efficacité du delivery", "Robustesse du RUN", "Valeur perçue par les utilisateurs"]
    th = 0.55
    for i, t in enumerate(tensions):
        x, w = col_x(i, 3)
        D.add_rect(s, x, by + 0.26, w, th, fill=WHITE, line=NAVY, line_w=1.0, rounded=True, radius=0.5)
        D.add_text(s, x, by + 0.26, w, th, [
            (t, dict(size=10, bold=True, color=NAVY, align=PP_ALIGN.CENTER)),
        ], anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
    return s


def slide_pourquoi_contexte(prs):
    """v2.43 — trois bascules en cartes numérotées (restitution n°7, la 1re en
    accent) puis le pont vers la double mission en deux paires douleur → mission
    (transformation-commerciale n°13) ; plus de pont gris ni de vide dessous."""
    s = content_slide(prs, None,
                       "Pourquoi cette transformation, pour un client infra — et maintenant",
                       color=ENCRE)
    D.add_text(s, MARGIN, CONTENT_TOP, CONTENT_W, 0.30, [
        ("Trois bascules rendent l'Infra-as-a-Product pertinente — et urgente — maintenant.",
         dict(size=9.5, color=NAVY, italic=True)),
    ])
    triggers = [
        ("L'infra subie n'est plus tenable",
         "RUN subi, experts seniors drainés sur du répétitif, problématique cloud non maîtrisée, "
         "plateforme contournée : le coût du statu quo ne cesse de monter."),
        ("Le modèle produit/plateforme est prouvé",
         "Devenu un standard — mais Gartner : 80 % de grandes organisations avec platform team "
         "en 2026, moins de 30 % de gains mesurables. C'est cet écart qu'Assainir adresse."),
        ("L'IA rebat les cartes — l'organisation d'abord",
         "L'IA amplifie une organisation mûre, jamais l'inverse. S'y préparer maintenant "
         "(doctrine confidentialité-first) évite de la subir plus tard."),
    ]
    n = 3
    pad = 0.2
    _, cw = col_x(0, n)
    u = cw - 2 * pad
    # cpi_ref=14 : `_lignes` surestimait le titre d'une ligne — vide dans la carte.
    body_h = max(D.estimer_lignes(c, u, 9, cpi_ref=14.0) for _, c in triggers) * (9 * 1.25 / 72.0) + 0.10
    tit_h = max(D.estimer_lignes(t, u, 10.5, cpi_ref=14.0) for t, _ in triggers) * (10.5 * 1.2 / 72.0) + 0.06
    badge = 0.46
    top0 = CONTENT_TOP + 0.62
    card_h = badge / 2 + 0.14 + tit_h + 0.08 + body_h + 0.18
    for i, (t, c) in enumerate(triggers):
        x, w = col_x(i, n)
        accent = i == 0
        D.add_rect(s, x, top0, w, card_h, fill=NAVY if accent else WHITE,
                   line=None if accent else LINE, line_w=0.75, rounded=True, radius=0.08)
        _badge(s, x + pad + badge / 2, top0, badge, WHITE if accent else NAVY, str(i + 1),
               text_color=NAVY if accent else WHITE, size=14)
        ct, cs = (WHITE, "#c7cbe0") if accent else (NAVY, MUTED)
        D.add_text(s, x + pad, top0 + badge / 2 + 0.14, u, tit_h, [
            (t, dict(size=10.5, bold=True, color=ct, line_spacing=1.1))])
        D.add_text(s, x + pad, top0 + badge / 2 + 0.14 + tit_h + 0.08, u, body_h, [
            (c, dict(size=9, color=cs if accent else NAVY, line_spacing=1.2))])
    y = top0 + card_h + 0.28
    D.add_text(s, MARGIN, y, CONTENT_W, 0.22, [
        ("ET SURTOUT — NOS DEUX MISSIONS RÉPONDENT TRAIT POUR TRAIT AUX DEUX DOULEURS DU CLIENT",
         dict(size=8, bold=True, color=MUTED))])
    y += 0.28
    paires = [("Subir le RUN", "TRANSFORMER", "cible produit/plateforme"),
              ("La douleur", "ASSAINIR", "capacité récupérée à réinvestir — sous réserve "
               "d'une réallocation côté client")]
    ph = 0.66   # dimensionné au texte, jamais étiré jusqu'au bas de slide
    for i, (dl, mi, det) in enumerate(paires):
        x, w = col_x(i, 2)
        lw = 1.35
        D.add_rect(s, x, y, lw, ph, fill=WHITE, line=LINE, line_w=0.75, rounded=True, radius=0.5)
        D.add_text(s, x, y, lw, ph, [(dl, dict(size=9.5, bold=True, color=NAVY, align=PP_ALIGN.CENTER))],
                   anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
        _chevron_shape(s, x + lw + 0.06, y + ph / 2 - 0.16, 0.24, 0.32)
        rx = x + lw + 0.36
        D.add_rect(s, rx, y, x + w - rx, ph, fill=WHITE, line=NAVY, line_w=1.25, rounded=True, radius=0.5)
        D.add_text(s, rx + 0.2, y, x + w - rx - 0.3, ph, [
            (mi, dict(size=10, bold=True, color=NAVY)),
            (det, dict(size=8.5, color=MUTED, line_spacing=1.1)),
        ], anchor=MSO_ANCHOR.MIDDLE)
    return s


def slide_conditions_reussite(prs):
    """v2.43 — réécrite pour tenir à 8 pt minimum (demande utilisateur) : une
    phrase par condition, refus condensés, aucun retiré. Pattern : chaîne
    verticale numérotée + encart de mise en exergue (pattern 6), critère de
    sortie en bandeau."""
    s = content_slide(prs, None, "Quatre conditions de réussite de la démarche", color=ENCRE)
    D.add_text(s, MARGIN, CONTENT_TOP, CONTENT_W, 0.26, [
        ("Nos convictions fixent les conditions de réussite — et ce que la démarche refuse, "
         "même quand on le lui demande.", dict(size=9.5, color=NAVY, italic=True))])
    conditions = [
        ("Un sponsor qui porte la cible",
         "La transformation ne va pas plus loin que ce que le sponsor porte."),
        ("Des équipes réellement disponibles",
         "Interviews et ateliers sur du temps réservé, vérifié à l'intake."),
        ("Une RH embarquée sur rôles et évaluation",
         "Coacher une posture que les grilles punissent, c'est ramer à contre-courant."),
        ("Un processus documenté avant tout agent",
         "Sinon on fige dans le code une pratique mal définie."),
    ]
    band_h = 0.50
    band_top = CONTENT_BOTTOM - band_h
    top0 = CONTENT_TOP + 0.40
    reg_h = band_top - 0.16 - top0
    gw = 3.85
    gap = 0.08
    ch = (reg_h - 3 * gap) / 4
    fil_x = MARGIN + 0.16
    D.add_rect(s, fil_x - 0.01, top0 + ch / 2, 0.02, 3 * (ch + gap), fill=LINE)
    for i, (t, c) in enumerate(conditions):
        y = top0 + i * (ch + gap)
        cx = MARGIN + 0.40
        D.add_rect(s, cx, y, gw - 0.40, ch, fill=WHITE, line=LINE, line_w=0.75, rounded=True, radius=0.12)
        _badge(s, fil_x, y + ch / 2, 0.30, NAVY if i == 0 else WHITE, str(i + 1),
               text_color=WHITE if i == 0 else NAVY, size=9)
        D.add_text(s, cx + 0.16, y, gw - 0.72, ch, [
            (t, dict(size=9.5, bold=True, color=NAVY)),
            (c, dict(size=8.5, color=MUTED, space_before=1, line_spacing=1.15)),
        ], anchor=MSO_ANCHOR.MIDDLE)
    px = MARGIN + gw + 0.22
    pw = BORD_DROIT - px
    D.add_rect(s, px, top0, pw, reg_h, fill=NAVY, rounded=True, radius=0.08)
    pad = 0.18
    D.add_rect(s, px + pad, top0 + pad, 1.2, 0.24, fill=ACCENT_PLEIN, rounded=True, radius=0.5)
    D.add_text(s, px + pad, top0 + pad, 1.2, 0.24, [
        ("NOS REFUS", dict(size=8, bold=True, color=NAVY, align=PP_ALIGN.CENTER))],
        anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
    paras = [
        ([("Ce que la démarche ne fera pas.", dict(size=10, bold=True, color=WHITE))], dict()),
        ([("Des lignes qu'elle tient et explique dès l'Assessment flash — pas des conditions "
           "posées au client.", dict(size=8.5, color="#c7cbe0"))], dict(space_before=2, line_spacing=1.15)),
        ([("ON REFUSE", dict(size=8, bold=True, color="#8891b3"))], dict(space_before=8)),
    ]
    for r in ("Automatiser un processus mal conçu.",
              "Livrer une plateforme techniquement bonne mais peu adoptée.",
              "Séparer transformation organisationnelle et technique."):
        paras.append(([("—  " + r, dict(size=8.5, color=WHITE))], dict(space_before=2)))
    paras.append(([("ON NE LE RÉSOUT PAS, MAIS ON LE POSE", dict(size=8, bold=True, color="#8891b3"))],
                  dict(space_before=8)))
    for nom, q in (("Perte de savoir-faire", "l'équipe reprendrait-elle la main une semaine sans l'agent ?"),
                   ("Incitations RH contraires", "vos grilles récompensent-elles encore ce qu'on décourage ?")):
        paras.append(([(nom + " : ", dict(size=8.5, bold=True, color=WHITE)),
                       (q, dict(size=8.5, color="#c7cbe0"))], dict(space_before=2, line_spacing=1.15)))
    _rich(s, px + pad, top0 + pad + 0.32, pw - 2 * pad, reg_h - 2 * pad - 0.32, paras)
    D.add_rect(s, MARGIN, band_top, CONTENT_W, band_h, fill=TRACK, rounded=True, radius=0.08)
    D.add_text(s, MARGIN + 0.2, band_top, CONTENT_W - 0.4, band_h, [
        ("LE CRITÈRE DE SORTIE EST LE MIROIR DES CONDITIONS D'ENTRÉE", dict(size=8, bold=True, color=MUTED)),
        ("L'équipe tient-elle le modèle sans le consultant ? Il se rend dispensable : n'évalue "
         "jamais les personnes, ne fait pas leur reporting, ne s'installe pas entre l'équipe et le sponsor.",
         dict(size=8.5, color=NAVY, space_before=2, line_spacing=1.15)),
    ], anchor=MSO_ANCHOR.MIDDLE)
    return s


def build():
    # Les anomalies sont accumulees dans une liste de MODULE : sans cette remise
    # a zero, deux build() dans le meme processus additionnent leurs constats et
    # le second ecrit un .INVALIDE.pptx pour des defauts deja corriges.
    _ANOMALIES_BUILD[:] = []
    prs = new_prs()
    slide_cover(prs)

    # === v2.40 (arbitrage utilisateur du 2026-09-23) : trame en 7 chapitres +
    # ouverture sans intercalaire + annexe. Chaque kicker de slide de contenu
    # vaut le NOM de son chapitre (cf. _CHAPITRE_COURANT) ; l'historique des
    # trames précédentes (8 chapitres v2.35, Next steps, Opportunités...) vit
    # dans `git log docs/cadrage-ppt/`.
    #
    # Ouverture — kicker EXECUTIVE SUMMARY, sans intercalaire : le sommaire en
    # cinq blocs puis la thèse.
    _CHAPITRE_COURANT[0] = "Executive summary"
    slide_executive_summary(prs)
    slide_vision(prs)

    # Photos d'intercalaire : les 7 scènes sont des photos réelles déjà en
    # cache et vérifiées au rendu (mêmes scènes/seeds que la v2.39, réaffectées),
    # jamais deux fois la même d'un chapitre au suivant.
    slide_chapitre(prs, "01", "Contexte",
                   "Ce qui rend le terrain infra à part, la double mission, pourquoi "
                   "maintenant, et qui achète.",
                   ENCRE, "mountains", seed=0)
    slide_specificites_infra(prs)
    slide_mission(prs)
    slide_pourquoi_contexte(prs)
    slide_qui_achete(prs)

    slide_chapitre(prs, "02", "Ce que ça coûte",
                   "Ce que coûte le statu quo, les douleurs mesurables, et les 8 "
                   "familles qui les rendent traitables.",
                   # seed=5 : index Openverse vérifié sans filigrane (cf. _REQUETES_PHOTO).
                   ENCRE, "riverdelta", seed=5)
    # v2.42 : chapitre ramené à 3 slides (retour utilisateur) — enjeux, RUN et
    # infra transverse fusionnés ; Opportunités retirée, sa charnière (« c'est
    # traitable ») devient le bandeau de clôture des 8 familles.
    slide_cout_si_rien_ne_change(prs)
    slide_douleurs(prs)
    slide_familles(prs)

    slide_chapitre(prs, "03", "Nos convictions",
                   "Sept convictions, une conviction sur l'agentic, et un exemple "
                   "avant/après de ce qu'elle change.",
                   ENCRE, "wheatfield", seed=0)
    slide_convictions(prs)
    slide_convictions_2(prs)
    slide_infra_as_product_exemple(prs)

    slide_chapitre(prs, "04", "L'offre",
                   "La thèse, la problématique traitée à deux, et la cible Platform Team.",
                   ENCRE, "forest", seed=0)
    # v2.42 : 3 slides (retour utilisateur) — les trois temps et le « à deux »
    # fusionnés dans slide_offre_mecanique.
    slide_why_iap(prs)
    slide_offre_mecanique(prs)
    slide_team_topologies(prs)

    # v2.41 : La démarche resserrée sur ses deux slides de fond (doublons avec
    # L'offre retirés, retour utilisateur) ; les deux fils en sont le centre.
    slide_chapitre(prs, "05", "La démarche",
                   "Trois temps et une boucle, et les deux fils — les personnes et la "
                   "technique — qui courent dans chaque phase.",
                   ENCRE, "canyon", seed=0)
    slide_trajectoire(prs)
    slide_deux_fils(prs)

    # v2.41 : l'agentic devient une expertise OCTO qui COMPLÈTE la démarche
    # (retour utilisateur) — placé après elle, remplace « l'IA » de la v2.40.
    slide_chapitre(prs, "06", "L'expertise agentic d'OCTO",
                   "Un complément à notre démarche, jamais un prérequis : ce qu'il "
                   "apporte, les agents candidats, les garde-fous et les niveaux d'ambition.",
                   ENCRE, "ocean", seed=0)
    slide_intro_agentic(prs)
    slide_activites_humaines(prs)
    slide_agents_candidats(prs)
    slide_ia_sous_controle(prs)
    slide_ambition_si(prs)

    slide_chapitre(prs, "07", "Réussir et démarrer",
                   "Les conditions de réussite, ce que la démarche refuse, et la décision "
                   "de lancer l'Assessment flash.",
                   ENCRE, "meadow", seed=1)
    slide_conditions_reussite(prs)
    slide_next_steps(prs)

    # v2.42 : un vrai chapitre « Annexes » (retour utilisateur), intercalaire
    # compris. « dunes » : photo réelle déjà vérifiée (ex-chapitre Opportunités).
    slide_chapitre(prs, "08", "Annexes",
                   "Le schéma d'accompagnement de référence et l'export markdown.",
                   ENCRE, "dunes", seed=0)
    slide_offre_iap(prs)   # v2.41 : schéma d'accompagnement de référence
    slide_export_markdown(prs)
    _CHAPITRE_COURANT[0] = None

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
