# Analyse de 7 cas limites du cadrage BMAD IAP (2026-09-23)

Source des findings : revue bmad-review edge-case du 2026-09-23. Chaque cas a été vérifié ici dans le texte réel de `docs/bmad-iap-cadrage.md` (numéros de ligne relevés le 2026-09-23 ; le fichier est en cours d'édition, relocaliser par le nom de section). Analyse seulement : rien n'est appliqué. Aucun nouveau chiffre n'est introduit ; les seuils éventuels restent **INCERTAIN — non mesurés**, à fixer par l'humain.

Numérotation 7-13 reprise de la revue.

---

## Cas 7 — Client qui cumule plusieurs scénarios

**(a) Confirmé.** §Routage des scénarios, l.737-749 : table à une ligne par scénario (« RUN massif », « Pression IA sponsor », « Données sensibles »…), aucune règle de cumul. Or des cumuls sont probables par construction (« Pression IA sponsor » + « Maturité IA faible » + « Données sensibles »).

**(b) Options**

| Option | Ce qu'on écrit | Coût | Ce qu'on saura | Risque |
|---|---|---|---|---|
| A. Ordre de préséance | Une règle : les scénarios-contraintes (données, maturité IA) s'appliquent toujours ; un seul scénario-moteur mène le chemin, choisi par le sponsor à l'intake | Un paragraphe + une colonne « nature » | Quel chemin a été retenu, et pourquoi (ADR) | Préséance mal choisie sur un cas réel |
| B. Union des chemins | « Enchaîner les chemins de tous les scénarios détectés » | Une ligne | Rien de plus | Mission surdimensionnée, contraire à « 3 hypothèses max par pilote » |
| C. Laisser au coach | « Arbitrage au cas par cas » | Nul | Rien | Chaque coach invente sa règle, pas de comparabilité entre pilotes |

**(c) Recommandation : A.** Distingue ce qui *plafonne* (même logique que « la mesure d'état plafonne le palier atteignable », §Cross-walk des échelles) de ce qui *oriente* ; garde un seul moteur, cohérent avec le plan de preuve.

**(d) Texte proposé** — sous la table de §Routage des scénarios :

> **Cumul de scénarios.** Les scénarios se répartissent en deux natures. Les **contraintes** (« Données sensibles », « Maturité IA faible ») ne choisissent pas le chemin : elles le plafonnent et s'appliquent toujours, cumulées. Les **moteurs** (les autres lignes) choisissent le chemin : un seul est retenu comme moteur de la mission, les autres sont notés comme scénarios secondaires traités par le chemin du moteur ou reportés à la réévaluation. Le choix du moteur est une décision ADR prise à l'intake avec le sponsor, alternatives rejetées obligatoires. Aucun ordre de préséance n'est fixé entre moteurs à ce stade — `INCERTAIN`, à instruire sur les missions pilotes.

**(e) Humain :** valider la partition contrainte/moteur (« Pression IA sponsor » est-il moteur ou contrainte ?) ; décider si un ordre par défaut entre moteurs est souhaité.

---

## Cas 8 — Gate DevOps [0] + D3/D4 sans LLM local : que vend la mission ?

**(a) Confirmé.** §Cross-walk des échelles, l.312 : « Usine DevOps niveau [0] → interdit le pattern « Automatiser » » ; l.314 : « D3–D4 sans LLM local qualifié → mode M0 / documentation-first ». Rien ne décrit le cumul. Éléments de réponse épars : l.222 « M0 n'est pas un mode dégradé au rabais » ; l.1019 chemin documentation `runbook-<processus>.md` ; dérogation ADR au gate DevOps (décision l.1206).

**(b) Options**

| Option | Ce qu'on écrit | Coût | Ce qu'on saura | Risque |
|---|---|---|---|---|
| A. Nommer le cumul comme une offre à part entière | Un paragraphe : la mission vend Transformer + Assainir hors automatisation et hors IA (simplifier/supprimer, runbooks, fiabilisation de la chaîne), avec la sortie du gate comme livrable | Un paragraphe | Si ce périmètre se vend (1ʳᵉ proposition) | Perçu comme « l'offre sans ce qui la distingue » |
| B. Déclasser en mission flash / pré-mission | « Ce client relève d'un assessment puis d'une remédiation DevOps hors IAP » | Une ligne | Rien sur la valeur IAP en contexte contraint | Perte du client ; contradiction avec « M0 pas au rabais » |
| C. Dérogation ADR par défaut | Pousser la dérogation au gate DevOps | Nul | — | Vide le gate de son sens |

**(c) Recommandation : A.** Tout le matériau existe déjà ; seul le cumul n'est pas écrit. La fiabilisation de la chaîne devient l'objectif mesurable qui lève le gate à la réévaluation.

**(d) Texte proposé** — dans §Cross-walk des échelles, après la liste des règles dures :

> **Cumul des plafonds (DevOps [0] et D3–D4 sans LLM local).** Les deux règles se cumulent : ni pattern « Automatiser », ni IA sur les données réelles. La mission ne change pas de nature, elle change de livrables : (1) Transformer en entier (cible produit, roadmap, gouvernance) ; (2) Assainir par les seuls patterns hors automatisation (supprimer, simplifier, standardiser) ; (3) les `runbook-<processus>.md` du chemin documentation (§Export markdown) ; (4) un plan de fiabilisation de la chaîne DevOps dont l'atteinte du niveau [1] est le critère de levée du gate à la réévaluation. Ce que la mission ne vend pas est écrit dans la proposition, pas découvert en cours de route. Viabilité commerciale de ce périmètre : `INCERTAIN` — non testée.

**(e) Humain :** accepter de vendre ce périmètre sous le même nom d'offre (lien avec B1) ; valider que « niveau [1] » est le bon critère de levée.

---

## Cas 9 — Financement croisé réfuté : pas de branche

**(a) Confirmé.** §Mission & vision, l.35 : « hypothèse à valider sur les premières missions pilotes, pas un invariant démontré ». §Plan de preuve, l.856 : critère de réfutation écrit avant la mission, hypothèse n°1 du pilote 1. Nulle part : ce que devient l'offre si elle est réfutée. Le brief (l.7) porte la même hypothèse sans branche.

**(b) Options**

| Option | Ce qu'on écrit | Coût | Ce qu'on saura | Risque |
|---|---|---|---|---|
| A. Branche pré-écrite à deux niveaux | Réfuté sur 1 pilote → requalifier et rejouer ; réfuté sur N → l'offre se repositionne (les deux piliers vendus comme conjoints mais non autofinancés) | Un paragraphe | Quel signal déclenche quoi | Seuil N arbitraire (INCERTAIN) |
| B. Renvoyer au scénario « delta plat » | Une ligne de renvoi | Nul | Le deck de bilan du pilote, pas le devenir de l'offre | Confond l'échec d'une mission et celui de la thèse |
| C. Retirer « finance » du discours dès maintenant | Réécrire l.30-31 | Refonte du positionnement | — | Abandonne le différenciateur avant preuve |

**(c) Recommandation : A.** Cohérent avec « la narrative d'échec fait partie du dispositif de preuve » (l.858), appliqué à l'offre et non plus à la mission.

**(d) Texte proposé** — ajout en point 4 de §Plan de preuve des missions pilotes :

> 4. **Branche « financement croisé réfuté »** — écrite avant le pilote 1. Réfutation sur **un** pilote : on distingue « capacité non récupérée » (échec d'Assainir) de « capacité récupérée mais absorbée ailleurs » (échec du réinvestissement) — seul le second touche la thèse ; l'hypothèse est maintenue et rejouée au pilote suivant. Réfutation répétée (nombre de pilotes : `INCERTAIN`, à fixer par la direction de cabinet) : la colonne « Ce qu'il finance » de §Mission & vision est réécrite — les deux piliers restent vendus comme conjoints, le discours sponsor retire « la capacité récupérée finance la trajectoire » et le brief est mis à jour dans le même mouvement.

**(e) Humain :** fixer le nombre de réfutations qui déclenche le repositionnement ; accepter d'écrire à l'avance que la thèse centrale peut tomber.

---

## Cas 10 — B2 : compte déjà client d'« Agentic Product Run »

**(a) Confirmé.** §Points échus, l.1140 : risque « Un même compte peut recevoir les deux discours séparément », échéance « Avant la première proposition commerciale ». Le cas d'un compte déjà engagé avec l'offre sœur n'est pas traité ; le brief (l.127) nomme la cohabitation sans la traiter. Nature de l'offre sœur et recouvrement réel : **Information insuffisante** dans ces deux documents.

**(b) Options**

| Option | Ce qu'on écrit | Coût | Ce qu'on saura | Risque |
|---|---|---|---|---|
| A. Règle de compte : l'offre en place mène | Critère ajouté à B2 : sur un compte déjà client, IAP ne se propose qu'en accord avec le porteur de l'offre sœur, et l'intake reprend ses constats existants | Une ligne de table + un signal d'intake | Si des comptes sont concernés | Dépend d'un porteur externe au projet |
| B. Question d'intake seule | « Le client a-t-il une mission Agentic Product Run ? » à l'intake | Une question | L'occurrence réelle | Détecte sans dire quoi faire |
| C. Hors périmètre du cadrage | Laisser à la direction | Nul | Rien | Le cas surgit en mission |

**(c) Recommandation : A + la question de B.** B2 est déjà porté par la direction de cabinet ; il suffit d'élargir son périmètre et d'ajouter un signal détectable.

**(d) Texte proposé** — remplacer la cellule « Pourquoi ça casse en mission » de la ligne B2 dans §Points échus :

> Un même compte peut recevoir les deux discours séparément — **et un compte déjà client d'« Agentic Product Run » peut se voir proposer IAP par-dessus une mission en cours**. Règle attendue de l'arbitrage : quelle offre mène sur un compte déjà engagé, et comment l'intake IAP reprend les constats existants plutôt que de ré-interviewer. Signal d'intake : « une mission Agentic Product Run est-elle en cours ou passée sur ce compte ? »

**(e) Humain :** tout l'arbitrage (direction de cabinet) ; échéance « avant la première proposition » à maintenir ou avancer.

---

## Cas 11 — ExternalEvidence toujours CONFIRMÉ, sans fraîcheur

**(a) Confirmé.** §Import de données outils, l.535 : « tag de confiance : toujours CONFIRMÉ (donnée système, pas une opinion) » ; l.539 : « tag CONFIRMÉ automatique ». Règle d'or IA & données, l.190 : « Vérifier provenance, qualité, fraîcheur des données. » L'entité porte un champ `date` (l.534) mais aucune règle ne l'utilise. Décision l.1185 répète « toujours CONFIRMÉ ». Nuance : §KPIs l.833 exige déjà une preuve externe pour CONFIRMÉ — cohérent, mais n'aborde pas la fraîcheur.

**(b) Options**

| Option | Ce qu'on écrit | Coût | Ce qu'on saura | Risque |
|---|---|---|---|---|
| A. CONFIRMÉ conditionnel | CONFIRMÉ si extraction datée, source identifiée et fenêtre couvrant la période mesurée ; sinon DÉDUIT avec motif | Réécrire 2 lignes + décision | L'âge des preuves dans chaque livrable | Seuil de fraîcheur arbitraire (INCERTAIN) |
| B. CONFIRMÉ + mention d'âge | Garder CONFIRMÉ, afficher toujours la date d'extraction | Une ligne | L'âge, sans conséquence | Un export périmé reste « confirmé » |
| C. Statu quo | — | Nul | — | Contradiction interne avec la règle d'or 8 |

**(c) Recommandation : A.** « Toujours » est la faille ; le tag doit dire qu'un fait est confirmé *pour la période mesurée*. La fenêtre se définit par rapport à la période du diagnostic, ce qui évite d'inventer une durée.

**(d) Texte proposé** — remplace l.535-536 dans §Import de données outils, puis aligner la décision « Import manuel de données outils » :

> tag de confiance : `CONFIRMÉ` si source identifiée, date d'extraction connue et période couverte incluant la période diagnostiquée ; sinon `DÉDUIT`, motif écrit (« export antérieur à la réorganisation », « période non couverte »). Application de la règle d'or « Vérifier provenance, qualité, fraîcheur des données » (§Règles d'or) — une donnée système n'est pas une opinion, mais elle peut être périmée.

**(e) Humain :** accepter de retirer « toujours » (décision v0.8 revisitée) ; dire s'il faut une durée plafond en plus de la fenêtre.

---

## Cas 12 — Corpus mixte D0-D4

**(a) Confirmé.** §Gate IA & confidentialité, l.204-210 : un usage par niveau, aucune règle pour un corpus qui mêle plusieurs niveaux (ex. notes d'interview D2 citant des tickets D3). §Export markdown l.1012-1013 raisonne aussi par niveau unique.

**(b) Options**

| Option | Ce qu'on écrit | Coût | Ce qu'on saura | Risque |
|---|---|---|---|---|
| A. Niveau le plus haut l'emporte, sauf séparation prouvée | Ligne « Corpus mixte » : le corpus prend le niveau maximal ; on ne traite un sous-ensemble à un niveau inférieur que s'il est physiquement séparé et que la séparation est tracée | Une ligne de table | Où la séparation a été faite | Bascule fréquente en M0 |
| B. Découpage systématique | Chaque document classé et traité à son niveau | Charge de classification par pièce | Granularité fine | Fuite par un document mal classé |
| C. Statu quo | — | — | — | Traitement IA d'un D3 noyé dans un D2 |

**(c) Recommandation : A.** Règle conservatrice cohérente avec la doctrine ; le découpage reste possible mais comme exception tracée.

**(d) Texte proposé** — ligne ajoutée sous la table de §Gate IA & confidentialité (classification des données) :

> | Mixte | Notes D2 citant des tickets D3, export mêlant coûts et IAM | **Niveau le plus élevé présent**. Un sous-ensemble ne se traite à un niveau inférieur que s'il est extrait dans un corpus séparé, la séparation tracée par `iap-ai-data-confidentiality-gate` ; en cas de doute, le niveau supérieur |

**(e) Humain :** valider que la règle ne rend pas M0 quasi systématique (fréquence réelle : non mesurée).

---

## Cas 13 — Delta mission vs bruit organisationnel : pas de méthode

**(a) Confirmé.** §Plan de preuve des missions pilotes, l.858 : « comment on distingue le delta de mission du bruit organisationnel sur 6-12 mois (réorgs, coupes budgétaires, départs) » — l'exigence est posée, aucune méthode.

**(b) Options**

| Option | Ce qu'on écrit | Coût | Ce qu'on saura | Risque |
|---|---|---|---|---|
| A. Journal d'événements + attribution par périmètre | Tenir dès l'intake un journal daté des événements exogènes ; comparer les périmètres traités vs non traités par la mission ; conclusion taguée DÉDUIT, jamais CONFIRMÉ | Un paragraphe + un template de journal | Un faisceau d'indices, pas une preuve causale | Périmètre témoin souvent absent |
| B. Groupe témoin formel | Exiger un périmètre non traité comparable | Contrainte forte sur le scoping | Attribution plus solide | Rarement acceptable par le sponsor |
| C. Déclarer l'attribution non établissable | Écrire que le delta reste DÉDUIT/INCERTAIN | Nul | Honnêteté | Affaiblit tout le plan de preuve |

**(c) Recommandation : A, avec B « si disponible ».** Méthode faisable en mission réelle, honnête sur son niveau de preuve.

**(d) Texte proposé** — compléter le point 3 de §Plan de preuve des missions pilotes :

> Méthode minimale : (i) un **journal des événements exogènes** tenu dès l'intake (réorganisations, coupes, départs, changements d'outil), daté et rattaché aux périmètres touchés ; (ii) chaque KPI est lu **par périmètre**, traité vs non traité par la mission quand un périmètre non traité comparable existe ; (iii) un delta n'est attribué à la mission que si le journal n'explique pas l'écart, et il reste tagué `DÉDUIT` — jamais `CONFIRMÉ` : l'attribution causale n'est pas établie par cette méthode.

**(e) Humain :** accepter qu'aucune conclusion d'impact ne soit CONFIRMÉ ; dire si un périmètre témoin est négocié à l'intake.

---

## Synthèse des décisions humaines

- Cas 7 : partition contrainte/moteur des scénarios.
- Cas 8 : vendre le périmètre « sans automatisation ni IA » sous le même nom.
- Cas 9 : seuil de réfutations avant repositionnement.
- Cas 10 : quelle offre mène sur un compte déjà engagé (direction de cabinet).
- Cas 11 : lever le « toujours CONFIRMÉ » de la décision v0.8.
- Cas 12 : règle du niveau maximal pour les corpus mixtes.
- Cas 13 : impact de mission jamais au-delà de DÉDUIT ; périmètre témoin ou non.
