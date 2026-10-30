# Apprentissages — comité de supervision, refonte de forme du deck « Infra as a Product » (V26–V28)

- **Origine** : VSCode3, session du 2026-10-30, demande « lance un comité de supervision et transmets au hub les apprentissages ». Deux bras en lecture seule : S1 (qualité/coût de 15 rapports de sous-agents), S2 (outillage `deck_delta`). Rapports bruts hors dépôt (scratchpad de session, `comite_sup/S1.md`, `S2.md`).
- **Statut** : constats. Aucune proposition appliquée. Tout est **À arbitrer côté hub**. Aucune propagation à d'autres projets.
- Complète `apprentissage-comite-storytelling-forme-deck-2026-10-30.md` (note n°1, déjà envoyée).

## 1. Cause racine du retour utilisateur « les formes sont toujours similaires »

L'utilisateur a nommé un fichier de référence (OCTO_GROUND) ; je l'ai résumé à l'œil au lieu d'en extraire les formes au niveau des shapes. Les styles A/D/E prototypés (V26) ne venaient donc pas du PDF nommé. Il a fallu une 2e passe (`forme_ground.py`, V28) après un nouveau retour. Seules 17 slides sur 54 ont été reconstruites ; les autres sont seulement restylées (non mesuré : ce que l'utilisateur en pensera).
**À arbitrer** : règle « quand l'utilisateur nomme un document de référence pour la forme, extraire d'abord l'inventaire de formes (type, rayon, trait, remplissage) puis prototyper depuis cet inventaire ».

## 2. Qualité des bras (S1, mesuré sur 15 rapports)

- Le brief annonçait 13 rapports ; 15 fichiers existent (aucun manquant).
- Visuel : couverture complète pour 2 rapports sur 11 où il comptait (P2 27/27, G1 27/27) ; partielle ou nulle pour 9 (82 %). Ex. P1 0/27, P4 10/232, P6 16/172.
- Comparaison à la V25 non vérifiée dans 7 rapports comparatifs sur 8 (P1–P7 : titres ou nombre de formes seulement) ; seul P9 a rendu 11 slides sur 46.
- Ratios durée/budget : G1, G2 0,32 ; P1–P8 0,63–1,07 (P6 1,07, P8 1,05) ; C1 3,87, C3 4,63, C2 5,38, C4 5,73. Durée de P9 non fournie. Budget de 20 min = 1,25× la médiane P (16 min), pas 2×. Série C : aucun plafond de nombre de documents (305 à 444 scannés).
- « FAITS INFIRMÉS » : valeur la plus forte quand le brief faisait des hypothèses sur des noms/formats (P7 5 corrections, P4 960×540 au lieu de 720×405, P6 zéro IA dans 3 sources sur 5, C1 gabarit vide pris pour un pitch). Rituel quand le rapport écrit « aucun » après lecture partielle (P2, C2, G1).
- Limite : FAITS INFIRMÉS et « à re-sourcer » de C3 et C4 non localisés par grep, pas lus en entier : « non localisé », pas « absent ».

**À arbitrer** (propositions S1) :
1. Tableau obligatoire « pages vues / total / non vues » en tête de rapport, vérifié par le nombre de PNG produits.
2. Budget = 2× médiane de classe ET plafond de documents lus ; alerte à > 3×.
3. FAITS INFIRMÉS reformulé en « vérifié / infirmé / non vérifié » par hypothèse du brief ; comparaison à une référence = N slides rendues minimum, sinon mention NON VÉRIFIÉ.

## 3. Outillage `deck_delta` (S2, preuves fichier:ligne)

Confirmés : (a) numéro de version sans mode essai, écrasement refusé (`deck_base.py:63-71`, `deck.py:95-96`) — contournement `--sortie` ; (b) refus « layout modifié » sans nommer l'élément (`deck_garde.py:197`, `:235`) ; (c) baseline qui échoue aussi sur défauts disparus, sans diff au `--figer` (`tests/test_charte_livrable.py:54-55`, `deck_baseline.py:40-45`) ; (g) accès aux formes par index (`delta_V28.py:20-21`, `delta_V26.py:209-211`), casse sans bruit ; (h) I/O à l'import : delta_V9 à V12 et V14 à V19 ne s'importent plus (base V8 absente) ; V26–V28 ne marchent que parce que V19 et V24–V27 existent encore ; e2 : dossier de rendu partagé `deck.py:89`, risque de regarder un PNG périmé.
Partiels ou non rejoués : (d) estimateur de texte hors boîte volontairement pessimiste (`pptx_deck.py:965-992`), faux positifs figés comme dette ; (f) absence de `-I` non rejouée.
Correctifs proposés par S2 : mode essai puis promotion, nommer le diff d'empreinte, cliquet sur les défauts disparus, noms de formes stables, zéro I/O à l'import, sous-dossier de rendu par version.

## 4. Pratique de session

Une même question restée sans réponse a été reposée à chaque notification d'arrière-plan : une notification système n'est pas une réponse de l'utilisateur ; poser la question une fois, poursuivre avec le défaut annoncé.

## À arbitrer côté hub

Les points 1 à 4 ci-dessus : gabarit de brief (hub), règle de référence de forme (skill deck), correctifs `deck_delta` (projet VSCode3, après arbitrage utilisateur).
