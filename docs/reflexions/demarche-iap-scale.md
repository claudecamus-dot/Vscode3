# Analyse de la démarche IAP à la lumière de l'offre SCALE (2026-07-23)

**Objet.** Relecture critique de la démarche BMAD IAP (schéma de fonctionnement
COLLECTE→DIAGNOSTIC→CONCEPTION→RESTITUTION, trajectoire ①②③⟲, démarche
d'accompagnement agent en 5 phases, comitologie) à la lumière des trois decks de
l'offre OCTO SCALE (transformation agile, 2019-2020 — notes d'extraction sourcées :
`docs/Import/notes-extraction-scale.md`). Cette analyse vient **après** l'intégration
v2.4 du cadrage (`docs/bmad-iap-cadrage.md`, §Accompagnement de l'humain dans la
trajectoire) : elle ne redit pas ce qui y est déjà acté, elle relève ce que la
comparaison révèle **en plus** — convergences qui valident, manques restants,
tensions à assumer. Rien de ce qui suit n'est intégré au cadrage : l'humain arbitre.

**Précaution de méthode.** SCALE et IAP ne sont pas le même objet : SCALE vend une
*présence* de transformation (1-3 mois pour engager, 1-3 trimestres pour
expérimenter, 1-3 ans pour passer à l'échelle) ; IAP vend un *delta instrumenté*
(mission de quelques semaines + boucle T+6-12 mois). Une comparaison naïve
conclurait « IAP doit faire tout ce que fait SCALE » — faux : la moitié des
dispositifs SCALE ne survivent pas au format court. Le filtre appliqué ici :
un mécanisme SCALE n'est retenu que s'il traite un risque que la démarche IAP
porte *aussi*, à son échelle.

---

## 1. Ce que SCALE valide dans la démarche IAP (convergences)

La comparaison est d'abord rassurante — plusieurs choix structurants d'IAP sont
exactement ceux que SCALE a éprouvés en mission :

- **Pilotes volontaires puis généralisation progressive, bascule par l'usage** :
  la trajectoire ①②③⟲ et son Coach → Délégué recoupent le lancement en vagues
  SCALE avec « accompagnement à présence dégressive » et un coach qui « cherche à
  se rendre progressivement dispensable ». Même anti-décret : chez SCALE non plus,
  aucune bascule ne se déclenche par une date.
- **Le pilotage par la mesure avec l'avant/après comme discipline** : SCALE mesure
  l'adoption « avant accompagnement puis tous les 6-12 mois » — c'est la boucle ⟲
  d'IAP, en moins instrumenté (pas d'équivalent des tags CONFIRMÉ/DÉDUIT ni du
  scénario « delta plat » pré-écrit). Sur ce terrain IAP est *plus* rigoureux que
  la référence.
- **L'écoute multi-parties prenantes comme entrée** : la « prise de contexte »
  SCALE (interviews des décideurs, écoute des tensions, « faire prendre
  conscience ») est la Collecte d'IAP — avec la même intuition, désormais
  explicite en v2.4, que l'interview est déjà un acte d'accompagnement.
- **Le refus du framework plaqué** : le tableau SCALE© vs SAFe® (« les processus
  et les outils prennent le dessus sur les individus ») est l'argument jumeau de
  la bibliothèque de patterns de comitologie par scénario « expérimentée, pas
  décrétée » et de la règle « jamais l'IA sur un problème d'abord organisationnel ».
- **La gouvernance à deux étages** : gouvernance opérationnelle fréquente vs
  stratégique d'évaluation chez SCALE ≈ la matrice instance × fréquence × décision
  de la comitologie IAP.

## 2. Ce que la comparaison révèle — constats restants (au-delà du v2.4)

### S1 · La démarche IAP n'a pas de temps d'engagement avant la collecte — majeur

SCALE « commence par le QUI » : Leader identifié, intention écrite, ambition
présentée par le sponsor lui-même *avant* tout travail d'analyse — parce qu'un
diagnostic lancé dans une organisation qui n'en connaît pas l'intention est vécu
comme un audit subi. IAP enchaîne intake → Collecte : le test d'engagement du
sponsor (v2.4) vérifie que le sponsor *portera*, mais rien ne prévoit que les
équipes interviewées aient entendu l'intention *de sa bouche* avant les
interviews. Transposition réaliste au format flash : un **micro-lancement**
(≤ 1 h, dans la semaine 1 de ①) où le sponsor présente lui-même pourquoi il
ouvre cette mission, ce qu'il fera du résultat, et ce que ça ne décidera pas —
coût marginal, améliore à la fois la qualité des interviews (on parle plus vrai
quand on sait à quoi ça sert) et l'adhésion à la restitution. **Proposition :**
l'ajouter comme dispositif de ① dans §Accompagnement de l'humain (owner
`iap-intake` + sponsor), à valider en mission pilote.

### S2 · La formation n'existe nulle part dans le corpus IAP — majeur

Le target operating model crée des rôles nouveaux (owner produit d'infra, rôles
Team Topologies, postures Coach/Délégué) — et aucun template, workflow ou
livrable du module ne formalise la montée en compétence associée. SCALE produit
une « V0 du plan de formation » dès son premier volet et pose « la formation
comme un bootstrap des équipes ». Le v2.4 a intégré le *principe* (« pas de
formation sans coaching », formation expérientielle sur cas réels) mais aucun
livrable ne le porte. **Proposition :** un gabarit léger `competence-plan.md`
(ou une section du `transformation-backlog.md` existant — préférable, pas de
document de plus) listant par rôle du TOM cible : compétence attendue, geste
concret travaillé, modalité (pairing/mentorat/formation ciblée — les 3 pistes
déjà cadrées au §Focus management). Owner : `iap-adoption-plan`.

### S3 · La RH est absente de la cible operating model — majeur

Le cadrage documente lui-même le risque (`management-posture-risk` : coacher une
posture que les grilles d'évaluation récompensent à l'inverse) mais la cible TOM
ne touche jamais fiches de poste, évaluation, parcours — les structures qui
décident si le nouveau modèle tient après le départ du consultant. SCALE est
frontal : « les fonctions RH peuvent être un frein ou le principal accélérateur ;
plus tôt le changement commence en RH, plus rapide sera la transformation ».
Transposé au format IAP (pas de stream RH — hors de portée d'une mission courte) :
**la cible TOM signale explicitement les rôles dont la fiche de poste ou la grille
d'évaluation contredit le modèle cible** — une colonne du `team-topology-map.md`
existant, remplie en ②/③, remise au sponsor comme *sa* liste de chantiers RH, pas
comme un engagement du consultant. Renforce le point ouvert existant
« `iap-change-coach` doit-il refuser une mission sans engagement RH minimal ? » —
la réponse SCALE serait oui au moins pour l'accès : sans interlocuteur RH
identifié, la partie ③ du fil humain perd son levier principal.

### S4 · La mesure du système social est mono-instrument — moyen

Le v2.4 ajoute le sondage collaborateurs avant/après ; SCALE mesure à deux
niveaux (équipe : posture managériale, entraide, acceptation du changement /
entreprise : sponsorship, gouvernance) plus un Team Health Check trimestriel
historisé. Sur mission courte, un instrument unique est un choix défendable —
mais il faut alors que la **Grille V3.2 dise ce qu'elle couvre du champ
posture/culture** (vs pratiques techniques seulement). Rejoint exactement le
point ouvert v2.3 « validation de domaine de la Grille V3.2 » (finding M2) :
ajouter la question « couvre-t-elle le système social ? » à cette passe de
validation déjà planifiée, plutôt qu'un nouveau chantier.

### S5 · Le delta humain à T+6-12 mois est optimiste par rapport aux ordres de grandeur SCALE — moyen

SCALE annonce 1-3 *trimestres* rien que pour « expérimenter des changements
significatifs » et 1-3 *ans* pour l'échelle. La boucle ⟲ d'IAP mesure à T+6-12
mois — dans la fourchette basse pour des changements de posture (les KPIs
techniques bougent plus vite que les humains). Le scénario « delta plat »
pré-écrit (v2.3, §Plan de preuve) devrait distinguer explicitement **« delta
humain lent mais sain »** (adhésion en progression, relais actifs, mais
satisfaction stable) d'un vrai échec — sinon la première réévaluation risque de
conclure à tort que le volet humain n'a servi à rien. Owner naturel :
`iap-metrics-sre-finops-lead`, dans la même passe que le scénario delta plat.

### S6 · Le mandat du consultant n'est pas cadré — mineur

SCALE vérifie avant de s'engager : « nous nous assurons d'avoir le mandat — en
lead plutôt qu'en sous-traitance » et « nous testons la propension de
l'environnement à se mettre en mouvement ». IAP cadre finement qui fait quoi
entre *agents*, jamais la posture contractuelle de la mission chez le client
(lead de la transformation ? conseil auprès d'un porteur interne ? audit
ponctuel ?). Trois postures qui changent le fil humain du tout au tout.
Probablement une sous-section de §Positionnement & achat (owner
`iap-strategy-lead`) — une page, pas un chantier.

### S7 · La grammaire QUI → POURQUOI → QUOI → COMMENT → RÉSULTAT — mineur, opportuniste

Les trois decks SCALE utilisent cette séquence comme structure narrative de
l'argumentaire sponsor. Le deck exécutif IAP (profil ①) a son contenu
(GlobalSynthesis, RecommendationAxis, radar) mais pas d'ordre narratif imposé.
Piste pour `iap-deck-builder` au moment de définir les 4 profils de deck :
ouvrir le deck de restitution par le QUI/POURQUOI (sponsor, intention,
déclencheurs — contenu déjà cadré au §Positionnement & achat) avant le QUOI
(diagnostic). Coût nul, à tester sur le premier deck de mission réel.

## 3. Tensions structurelles — à assumer, pas à corriger

- **T1 · Ne pas importer la promesse de présence.** Transposer les *mécanismes*
  SCALE sans importer sa *promesse commerciale* (une présence longue). Le risque
  symétrique du double discours fermé en v2.3 : sur-promettre l'accompagnement
  humain dans le deck alors que le format vendu est court. Le garde-fou existe
  (« promesse instrumentée ») — l'appliquer aussi au volet humain : promettre le
  *dispositif* (test d'engagement, restitution-embarquement, relais) et le
  *delta mesuré*, jamais « nous conduirons votre changement ».
- **T2 · L'humain reste subordonné à la double mission.** Le bloc « ce que ça ne
  crée pas » (v2.4) le dit : pas de 3ᵉ mission « conduite du changement ». SCALE
  est une offre *de* transformation ; IAP est une offre d'assessment-transformation
  *outillée* où l'humain est un fil, pas le produit.
- **T3 · La charge d'`iap-change-coach` s'accumule.** Manager (§Focus management),
  adoption d'agents (v1.8), et maintenant le fil humain de la trajectoire (v2.4) —
  trois casquettes sur le même agent, cohérent avec le refus d'un agent par sujet
  transverse mais à surveiller côté **staffing humain** de la mission (qui joue ce
  rôle, avec quelle séniorité ?). Rejoint le point ouvert v2.3 « carte staffing
  junior/senior par étape » (finding M5) — y ajouter explicitement le rôle
  change-coach.

## 4. Synthèse des recommandations

| # | Recommandation | Où ça irait | Owner proposé | Statut |
|---|---|---|---|---|
| — | Test d'engagement sponsor, restitution-embarquement, communauté de managers, relais internes, KPI humain, déontologie | §Accompagnement de l'humain (v2.4) | — | **Déjà intégré** (v2.4) |
| S1 | Micro-lancement sponsor (≤ 1 h) avant les interviews de ① | §Accompagnement de l'humain, ligne ① | `iap-intake` + sponsor | À arbitrer |
| S2 | Plan de montée en compétence par rôle du TOM cible (section du `transformation-backlog.md`, pas un doc de plus) | §Workflows / livrables ② | `iap-adoption-plan` | À arbitrer |
| S3 | Colonne « fiche de poste / évaluation en contradiction avec la cible » dans `team-topology-map.md`, remise au sponsor | §Modèles d'équipe + §Accompagnement ③ | `iap-operating-model-architect` + `iap-change-coach` | À arbitrer |
| S4 | Ajouter « la grille couvre-t-elle le système social ? » à la validation de domaine V3.2 déjà planifiée | Point ouvert M2 existant | `iap-strategy-lead` | À arbitrer (extension d'un point ouvert) |
| S5 | Distinguer « delta humain lent mais sain » dans le scénario delta plat | §Plan de preuve (v2.3) | `iap-metrics-sre-finops-lead` | À arbitrer |
| S6 | Cadrer le mandat de mission (lead / appui d'un porteur interne / audit) | §Positionnement & achat | `iap-strategy-lead` | À arbitrer |
| S7 | Trame QUI→POURQUOI→QUOI pour l'ouverture du deck de restitution | Définition des 4 profils de deck | `iap-deck-builder` | **Partiellement arbitré** (2026-07-23) : l'utilisateur a demandé cette grammaire comme fil rouge du deck de *synthèse du cadrage* (restructuration v2.5) ; reste ouvert pour les 4 profils de deck de mission |
| T1-T3 | Tensions à garder nommées (promesse, subordination, charge change-coach) | — | — | À surveiller, pas à corriger |

---

*Analyse produite le 2026-07-23 sur demande, après l'intégration v2.4. Sources :
`docs/Import/notes-extraction-scale.md` (extraction des 3 decks SCALE) +
`docs/bmad-iap-cadrage.md` (v2.4). Aucune recommandation S1-S7 n'est intégrée au
cadrage à ce stade — arbitrage humain attendu, même mécanique que la revue
produit/marché v2.3 (`docs/reflexions/revue-produit-marche.md`).*
