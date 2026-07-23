> Miroir local de l'artifact claude.ai : <https://claude.ai/code/artifact/aea2c16d-101d-475d-afc6-f2f54771872b> — extrait le 2026-07-07.

# BMAD IAP — Infra as a Product Transformation Pack

**Statut :** draft consolidé v2.3 (v2.1, revue localement le 2026-07-15 : brainstorm sur un export markdown de recommandation d'implémentation — agentic ou documentation, selon le contexte client — en complément des 4 profils de livrables PPT déjà cadrés, plus un cas nominal illustratif traçant une intervention de l'intake à l'amélioration de la recommandation à la boucle de réévaluation ; puis un second brainstorm relancé sur les KPIs — pourquoi, quoi mesurer précisément, comment les mettre en place, exemple chiffré sur le même cas nominal, §Trajectoire. v2.2, revue de fond le 2026-07-22 — cf. `docs/reflexions/revue-cadrage.md` : recomptage de l'inventaire des artefacts, requalification de la thèse de financement croisé en hypothèse à prouver, et cross-walk des échelles pour réduire la charge cognitive ; puis traitement des points porteurs restants de la revue — continuité de la boucle ⟲, plafond de débit du checkpoint humain au Niveau C, phasage QA/MVP, audio D2+ au repos sur mobile, statut ordinal du score de priorisation, l'enveloppe commerciale restant seule hors périmètre. v2.3, revue produit + research + market-research du 2026-07-23 — cf. `docs/reflexions/revue-produit-marche.md` : ajout de la section [Vue d'ensemble] Positionnement & achat, alignement du discours sponsor sur le statut d'hypothèse du financement croisé, plan de preuve des missions pilotes, et 8 nouveaux points ouverts produit)
**Langue :** FR (vocabulaire technique conservé)
**Confidentialité :** client-data-first
**Sources croisées :** VSCode1 (grille de maturité) · VSCode2 (moteur d'assessment + OpenHub)

---

## [Vue d'ensemble] Mission & vision

Un module BMAD à **double mission**, pas une méthode de transformation avec un traitement du gaspillage en option : transformer une organisation infrastructure — guichet, centre de coûts ou fonction support — en **plateforme interne opérée comme un produit**, ET traiter structurellement le gaspillage qui l'en empêche.

| Pilier | Ce qu'il vise | Ce qu'il finance |
|---|---|---|
| **Transformer** | Cible produit/plateforme : utilisateurs identifiés, proposition de valeur, roadmap, engagements de qualité, gouvernance lisible | La vision à moyen terme — ce que le sponsor achète |
| **Assainir** | Traitement mesurable des gaspillages (flux, RUN, humain, financier, cognitif, décisionnel, environnemental, IA) | La capacité récupérée qui finance la trajectoire produit — pas un audit de coûts isolé |

Les deux piliers ne sont pas séquentiels ni optionnels l'un par rapport à l'autre : une cible produit sans traitement du gaspillage manque de capacité pour s'y déployer ; un traitement du gaspillage sans cible produit reste un exercice de réduction de coûts sans vision — c'est explicitement l'anti-pattern à éviter (voir doctrine, « ne jamais confondre... »).

> **Hypothèse porteuse à prouver, pas un invariant acquis (v2.2) :** Le lien « la capacité récupérée finance la trajectoire produit » (colonne « Ce qu'il finance » ci-dessus) est le **joint qui tient toute la double mission** — et il n'est aujourd'hui **pas outillé**. Le garde-fou anti-déplacement (§Traitement des gaspillages) vérifie qu'un gain n'est pas *faux* ; rien ne vérifie qu'un gain réel est effectivement **réinvesti** dans la cible produit plutôt qu'absorbé ailleurs (réduction d'effectif, autre incendie, dette repayée). Tant que la mission ne mesure que la capacité *récupérée* (heures/mois, §KPIs) sans **KPI de réinvestissement** ni mécanisme de réallocation budgétaire décrit, cette affirmation reste une **hypothèse à valider sur les premières missions pilotes**, pas un invariant démontré. **(v2.3)** Le discours sponsor porte la **même honnêteté** que le statut interne — pas de double discours (finding critique C1 de la revue produit du 2026-07-23, `docs/reflexions/revue-produit-marche.md`) : la proposition de valeur se formule au sponsor comme une **promesse instrumentée** — « mécanisme instrumenté dès la première mission — KPI de réinvestissement — et qui suppose un mécanisme de réallocation budgétaire côté client ». Le KPI de réinvestissement passe de « point à trancher » à **chantier propriétaire assumé** : la research du 23/07 a établi qu'aucun standard publié (FinOps Framework 2026, DORA, SPACE) n'outille le lien « capacité récupérée → réinvestie » — c'est un angle mort de l'industrie entière, donc un actif différenciant si IAP l'outille en premier (proxy le plus proche : le toil ≤ 50 % de Google SRE, une mesure de temps jamais reprise en standard transverse). Chantier porté à la famille « KPIs de mission » (owner `iap-metrics-sre-finops-lead`, voir §Points ouverts).

La démarche équilibre trois tensions permanentes :

| Efficacité du delivery | Robustesse du RUN | Valeur perçue par les utilisateurs internes |
|---|---|---|

Elle relie systématiquement : organisation, delivery, technologie, RUN, TMA/fournisseurs, financement, UX/adoption, données, IA/automatisation, compétences, gouvernance.

> **Risque cadre — issu du brainstorm source :** « L'IA amplifie le système organisationnel existant : elle aide davantage les organisations déjà bien structurées qu'elle ne corrige les dysfonctionnements profonds. » Cette phrase ancre la règle d'or 3.2.1 (ne jamais proposer l'IA comme réponse à un problème d'abord organisationnel) — elle en est l'argument, pas un doublon.

## [Vue d'ensemble] Positionnement & achat (v2.3)

> **Origine (v2.3) :** section issue de la revue produit + research + market-research du 2026-07-23 (`docs/reflexions/revue-produit-marche.md`, findings C2, M6, m2) — le cadrage décrivait le « comment faire la mission » sans jamais dire qui achète, contre quoi, ni pourquoi maintenant. Les « 3 déclencheurs » de la slide Contexte vivaient dans le deck sans section source ici : ils sont rapatriés ci-dessous, et le sens de propagation deck→cadrage est régularisé — c'est désormais cette section qui fait foi, le deck qui la reprend.

### Les trois déclencheurs d'achat — pourquoi proposer ça à un client infra maintenant

| Déclencheur | Contenu | Source & tag |
|---|---|---|
| ① **« L'infra subie n'est plus tenable »** | RUN subi, seniors drainés sur du répétitif, gaspillage cloud non maîtrisé, plateforme contournée — le coût du statu quo monte | `CONFIRMÉ` — gaspillage cloud ~29 % et en hausse (Flexera) ; pénurie SRE/cloud persistante (baromètres FR 2025-2026) |
| ② **« Le modèle produit/plateforme est prouvé »** | Le platform engineering est devenu le standard — MAIS l'écart adoption/valeur est le vrai sujet, et c'est exactement l'écart que le pilier Assainir adresse | `CONFIRMÉ` — Gartner : 80 % des grandes orgs avec platform teams en 2026, mais < 30 % de gains mesurables |
| ③ **« L'IA rebat les cartes — l'organisation d'abord »** | L'IA amplifie une organisation mûre (règle d'or 3.2.1, risque cadre ci-dessus) ; doctrine confidentialité-first (§Gate IA) | `CONFIRMÉ` sur le retour de balancier (Gartner/Forrester, voir argumentaire de la prudence ci-dessous) ; la formulation « l'organisation d'abord » reste la thèse propre de l'offre — `DÉDUIT` |

### Qui achète

Sponsor qualifié : **DSI / direction infrastructure**, sur une ligne budgétaire **transformation** — pas le budget RUN. Tension 2026 à connaître avant de qualifier : le baromètre Abraxio DSI FR (déc. 2025) documente un « back to basics » — la modernisation infra **recule** face à la cyber dans les priorités budgétaires (`CONFIRMÉ`). Mais deux contre-courants jouent pour l'offre : l'IA capte le budget sans plafond, et la pénurie SRE/cloud persiste — le langage de vente est donc « **récupérer de la capacité humaine rare** », pas « moderniser l'infra ».

### Les 4 achats alternatifs — et pourquoi la double mission bat chaque achat partiel

| Alternative | Ce qu'elle apporte | Ce qui lui manque — la réponse IAP |
|---|---|---|
| **Ne rien faire** | Zéro coût apparent | Le coût du statu quo monte (déclencheur ①) — c'est lui que l'Assessment flash chiffre |
| **FinOps outillé seul** | Mesure le gaspillage — gaspillage cloud ~29 % (Flexera), marché outillé mature | Sans cible produit ni réallocation. IAP se positionne **en aval** : « vous avez le chiffre, nous transformons le gain en capacité produit gouvernée » |
| **Platform engineering pur** | La cible produit/plateforme | La cible sans le financement — reproduit l'écart 80/30 (adoption sans valeur mesurée) |
| **AIOps / agentic outillé** | Time-to-value court (ServiceNow « Autonomous Workforce », Datadog Bits AI) | Automatise le RUN sans transformation ; > 40 % d'abandons de projets agentic prédits d'ici 2027 (Gartner, 06/2025) |

> **Réponse au sponsor « je ne veux que la baisse de coûts » :** c'est l'anti-pattern documenté du cadrage — « un traitement du gaspillage sans cible produit reste un exercice de réduction de coûts sans vision » (§Mission & vision) — et la réponse est assumée, pas esquivée : une **mission flash d'entrée** (intake + gate IA + pilote court — scoping à trancher, §Points ouverts) puis la trajectoire ; jamais l'assainissement seul en régime permanent.

### Collision de nom — « Infrastructure as a Product » est déjà pris

L'étiquette est déjà portée par **Thoughtworks** (e-book « Infrastructure as a Product » — conseil technique, sans pilier gaspillage) et **Itential** (plateforme SaaS « Infrastructure as a Product for AI-Driven Operations », promesse −90 % OPEX) — `CONFIRMÉ` (market research, annexe C de la revue). Le différenciateur IAP n'est donc **pas l'étiquette mais le couplage** produit + gaspillage + doctrine IA — angle mort commun des concurrents identifiés (Thoughtworks sans financement croisé, FinOps sans cible produit, Capgemini sans doctrine IA, Big4 sur la gouvernance seule). Le **nom public de l'offre** est un point à trancher (§Points ouverts).

### Argumentaire de la prudence IA — la contre-narrative face à la sur-promesse

Face au vendeur AIOps qui promet un dashboard en 3 semaines, l'offre perdait à la qualification faute de contre-narrative écrite (finding M6). La voici, chiffrée (`CONFIRMÉ`, sources web en annexes B/C de la revue) :

- **> 40 % des projets agentic abandonnés d'ici 2027** (Gartner, 06/2025) — coûts, ROI flou, gouvernance ;
- **« agent washing »** : ~130 vendeurs réellement agentic sur des milliers revendiqués (Gartner) ;
- Forrester : « **la discipline compte plus que l'expérimentation** » ;
- **87 % des DSI ont des agents en production, mais 25 % seulement une visibilité temps réel** — la fatigue de gouvernance est une douleur concrète, exactement celle que le gate IA et la doctrine adressent.

La prudence IAP n'est pas une frilosité : c'est l'**anticipation du retour de balancier**, documentée par les deux analystes majeurs — et elle se vend comme telle (« pourquoi notre déception structurée vaut plus que leur sur-promesse »).

### Quick win IA légitime — pour le sponsor sous pression IA

Le scénario « Pression IA sponsor » (§Routage des scénarios) route vers le gate + la discovery gaspillage — nécessaire, mais commercialement sec si l'offre ne sait répondre que « pas tout de suite ». Complément v2.3 : **packager dès l'intake un cas D0/D1 à readiness [2]+** — le matériau existe déjà dans le routage (classification des données §Gate IA, seuil de readiness §Export markdown) ; l'offre répond désormais « **celui-ci, tout de suite, sous gate** », sans rien céder à la règle d'or 3.2.1.

## [Vue d'ensemble] Structure & emplacement du corpus

Décision de cadrage : pas de fichier pivot `iap-module-context.md`. Le corpus source (doc d'intégration + brainstorm PDF) se décompose directement dans `bmad-iap/knowledge/`, chaque fichier ayant un propriétaire de contenu unique.

### Vue globale du module (v1.1)

- 11 — Agents
- 11 — Workflows
- 14 — Templates *(baseline v1.1 — périmé, voir note de cohérence ci-dessous)*
- 9 — Checklists *(baseline v1.1 — périmé, voir note de cohérence ci-dessous)*
- 9+ — Knowledge (dont 2 nouveaux v0.6–0.7)
- 1 — Gate IA transversal non-automatisable

> **Note de cohérence de l'inventaire (v2.2) :** Les compteurs ci-dessus sont le **snapshot v1.1** et n'ont pas été réconciliés avec les artefacts ajoutés depuis. `automation-action-plan.md` est explicitement le « 14ᵉ template » (v1.3) et `automation-readiness-checklist.md` la « 9ᵉ checklist » — or des templates introduits **après** débordent « 14 » (`manual-synthesis-guide.md` v0.9, `governance-instance-map.md` v1.0, `team-topology-map.md` v1.2, `mvp-target-model.md`, les gabarits `runbook-<processus>.md` et `agentic-implementation-plan.md` v2.0) et `comitologie-coherence.md` est une **10ᵉ** checklist (v1.0). Le total exact n'est pas reconstituable ici faute d'énumération de la base des 13 premiers templates / 8 premières checklists ; le **recompte faisant autorité se fait au scaffolding `bmb`** (énumérer les fichiers réellement générés dans `templates/` et `checklists/`) — porté comme point ouvert (voir §Points ouverts).

```
bmad-iap/
  module.yaml ← résolu (v1.6) : scaffoldé via bmb, voir §Structure "Résolution module.yaml"
  agents/            11 agents — voir §Agents
  workflows/         11 workflows — voir §Workflows
  templates/         14 templates
  checklists/        9 checklists
  knowledge/
    infra-product-definition.md   ← mission/vision + invariants organisationnels + ITIL4/Platform Eng.
    doctrine-and-golden-rules.md  ← règles d'or IAP + IA/données (renforcées)
    anti-patterns.md
    ai-confidentiality-doctrine.md  ← nouveau, sorti de la doctrine générale (trop dense)
    platform-maturity-model.md      ← nouveau, maturité produit/plateforme (≠ maturité IA)
    scenario-library.md           ← routage + spécificités clients anonymisées
    waste-library.md              ← familles + patterns de traitement fusionnés
    metrics-library.md
    rex-library.md                ← REX clients, après redaction (voir callout ci-dessous)
  engagements/<client-slug>/  ← nouveau, isolation multi-client — voir section dédiée
```

> **Confidentialité amont — redaction appliquée :** La source brute contenait des noms de clients réels (secteurs télécom/plateformes numériques, banque de détail, GIE informatique bancaire) et une donnée chiffrée identifiante (pyramide des âges). Conformément aux règles de redaction déjà fixées en doctrine, ce wiki de cadrage ne cite plus que des alias sectoriels génériques (« Client Télécom/Diffusion A », « Client Bancaire B », « Client GIE Informatique Bancaire C ») et des chiffres généralisés par tranche large — c'était le premier test réel de cette règle, pas un cas théorique. Le process de redaction reste néanmoins à formaliser en étape de workflow reproductible pour les prochains REX (voir §Points ouverts) ; l'intégration effective dans `rex-library.md` devra repartir des mêmes alias, jamais des noms bruts de la source PDF.

### Résolution module.yaml (v1.6)

Point bloquant levé. L'installation BMAD locale (`_bmad/`, BMAD v6.8.0, cf. `_bmad/_config/manifest.yaml`) distingue deux objets différents qu'il ne fallait pas confondre :

- **`config.yaml`** (un par module déjà installé — `core/config.yaml`, `bmm/config.yaml`…) : configuration d'exécution locale (langue, dossiers de sortie, nom du projet) — ne concerne pas la définition d'un nouveau module.
- **`module.yaml`** : l'asset de **définition/enregistrement** d'un module (nom, agents, workflows, templates exposés) — fourni comme gabarit par le module **`bmb` (bmad-builder, v1.8.1)**, déjà installé localement. Le manifeste de fichiers de l'installation (`_bmad/_config/files-manifest.csv`) référence explicitement deux gabarits `module.yaml` fournis par `bmb` : `bmb/bmad-bmb-setup/assets/module.yaml` et `bmb/bmad-module-builder/assets/setup-skill-template/assets/module.yaml`.

> **Décision de cadrage :** `bmad-iap/module.yaml` ne sera pas rédigé à la main contre un schéma supposé. Il sera **scaffoldé via l'outillage `bmb` (Module Builder) déjà installé** dans `_bmad/`, en MVP1, au même moment que `iap-intake` — cohérent avec le rôle même de `bmb` (construire de nouveaux modules BMAD). Propriétaire : première itération MVP1, à valider par relecture humaine avant d'être considéré final (même discipline que le reste : outillage propose, humain valide).

## [Vue d'ensemble] Isolation multi-client

Trou identifié dans le corpus source : rien ne prévoyait qu'une même installation du module serve plusieurs missions sans mélange de contexte. Ajout d'un niveau dans l'arborescence :

```
bmad-iap/engagements/<client-slug>/
  iap-context.md
  diagnostic/
  product-definition/
  operating-model/
  ai-data-gate/
  waste-treatment/
  adoption/
  deck/
```

La racine du module (`agents/`, `workflows/`, `templates/`, `knowledge/`) reste la méthode générique, sans donnée client. Tout output de mission vit sous `engagements/<client-slug>/` — c'est le premier garde-fou de confidentialité, avant même la question du modèle IA utilisé.

## [Doctrine] Règles d'or

### Infra as a Product

1. Ne jamais confondre actif technique et produit infra.
2. Toujours expliciter utilisateurs, proposition de valeur, engagements et roadmap.
3. Distinguer produit plateforme, service, capacité, composant, leviers d'automatisation/gouvernance/expérience.
4. Distinguer RUN subi, RUN maîtrisé, BUILD, dette, sécurité, obsolescence, innovation.
5. Relier organisation, delivery, technologie, financement, UX et adoption.
6. Traiter dépendances et règles de gouvernance.
7. Intégrer la TMA/fournisseurs dans le modèle cible si le RUN est externalisé.
8. Toujours produire une option diagnostic-first *et* une option pilot-first en contexte incertain.
9. Transformer les recommandations en livrables actionnables et réutilisables.
10. Toujours prévoir des métriques de succès.

### IA & données

1. Ne jamais proposer l'IA si le problème est d'abord organisationnel *— l'IA amplifie le système existant, elle ne corrige pas les dysfonctionnements profonds.*
2. Ne jamais envoyer de données client confidentielles à une IA externe sans autorisation explicite.
3. Toujours qualifier la classification des données avant d'utiliser un LLM.
4. Toujours évaluer en priorité l'IA interne du client.
5. Toujours évaluer si un LLM local/privé peut suffire.
6. Documenter les limites du modèle choisi : qualité, contexte, latence, coût, sécurité, auditabilité.
7. Prévoir supervision humaine, intervention, contournement, audit, désactivation.
8. Vérifier provenance, qualité, fraîcheur des données.
9. Distinguer automatisation classique, IA générative, RAG, agentic workflow, décision automatisée.
10. Prévoir un mode dégradé si l'IA n'est pas autorisée sur les données réelles.

Anti-patterns à détecter : appeler « produit » un composant technique isolé ; PO sans changer la gestion de la demande ; agilité sans traiter les dépendances ; priorisation par bruit/statut ; chatbot IA sans cadrer flux/rôles/données ; automatiser un processus mal conçu ; externaliser des données sensibles sans cadre ; ignorer le RUN dans la roadmap ; plateforme techniquement bonne mais peu adoptée ; séparer transformation organisationnelle et technique.

## [Doctrine] Gate IA & confidentialité

Workflow obligatoire avant tout usage IA sur données client : `iap-ai-data-confidentiality-gate`. Principe directeur : **les données client gouvernent le choix du modèle IA, pas l'inverse.**

### Classification des données

Tags : `D0 · Public` — `D1 · Interne non sensible` — `D2 · Confidentiel` — `D3 · Restreint` — `D4 · Critique / réglementé`

| Niveau | Exemples | Usage IA par défaut |
|---|---|---|
| D0 | Articles publics, docs méthodo | IA externe possible |
| D1 | Organisation macro, catalogue anonymisé | IA client recommandée ; externe sur accord |
| D2 | Notes d'interview, reporting, portefeuille projets | IA client ou LLM privé/local |
| D3 | Tickets détaillés, logs, CMDB, IAM | LLM local/client, contrôles forts |
| D4 | Secrets de production, données réglementées | Local/on-prem, éventuellement sans IA générative |

### Modes d'exécution

- **IA client / tenant privé** — cas par défaut pour données internes.
- **LLM local / on-premise** — données sensibles, souveraineté, audit fort.
- **LLM privé cloud dédié** — clients à maturité cloud/IA établie.
- **IA externe SaaS** — données non sensibles ou anonymisées uniquement.
- **Mode hybride** — externe pour la méthode générique, client/local pour les données réelles.

### Fonctionner sans IA externe (v0.9)

Le mode « pas d'IA sur les données réelles » (M0, voir §Modèles de maturité) n'est pas un mode dégradé au rabais — la méthode doit rester intégralement exécutable à la main. Deux volets : des pistes encore ouvertes, et une approche déjà assez concrète pour être appliquée.

#### Brainstorm — pistes non tranchées

- Consultant senior en doublure sur la synthèse manuelle — la paire de relecture croisée remplace la vérification qu'apporterait normalement un second passage IA.
- Utiliser la grille de maturité (VSCode1) comme trame de facilitation d'atelier humain plutôt que comme seul support de scoring — un animateur peut dérouler pilier/objectif/question en atelier collectif, sans LLM de synthèse.
- Budget-temps volontairement allongé et annoncé au sponsor dès l'intake, plutôt que de dégrader silencieusement la profondeur du livrable pour tenir un délai calé sur le mode assisté par IA.
- Tableau croisé manuel thème × interviewé sur un mur ou un tableur partagé, pour repérer convergences/divergences sans passer par une GlobalSynthesis générée.
- **Question ouverte :** au-delà de M0 (pas d'IA du tout), existe-t-il un palier intermédiaire réaliste — IA locale très limitée en contexte — qui mérite sa propre approche plutôt que d'être traité comme un M0 dégradé de plus ?

#### Approche UX/UI recommandée

- **Badge visible et jamais silencieux** — tout livrable produit en mode sans IA externe porte la mention « Synthèse manuelle — mode M0 » de façon aussi visible qu'un tag de confiance, cohérent avec la règle OpenHub de ne jamais basculer de mode sans le signaler (voir §Agents).
- **Méthode de pré-synthèse manuelle outillée, pas un simple principe** — reprendre l'algorithme du mode démo de VSCode2 (`synthese_ai.py` : fréquence de mots-clés, cooccurrence entre répondants) et le formaliser en template `manual-synthesis-guide.md`, exécutable à la main par un consultant sans dépendre d'un LLM.
- **Tags de confiance renforcés en mode M0** — un constat `DÉDUIT` sans IA doit citer sa méthode manuelle (comptage, croisement de tableau) en plus de sa source, pas seulement la source.
- **Le scoring reste intact** — le score de priorisation des gaspillages et le score valeur/complexité (voir §Traitement des gaspillages et §Moteur d'assessment) sont des formules, pas des capacités IA : à rappeler explicitement pour éviter qu'un consultant pense devoir renoncer au scoring faute d'IA disponible.

## [Doctrine] Modèles de maturité

Deux échelles indépendantes — ne pas les mélanger dans un seul diagnostic.

### Maturité IA client (M0–M4)

| Niveau | Description | Stratégie BMAD |
|---|---|---|
| M0 | Pas d'IA interne utilisable | Méthodo générique, données anonymisées/synthétiques |
| M1 | IA interne basique | Synthèses internes, pas d'analyse critique automatisée |
| M2 | IA privée avec RAG | Diagnostic documentaire, consolidation |
| M3 | Plateforme IA gouvernée | Workflows agentic contrôlés |
| M4 | IA industrielle | Agents spécialisés à fort volume, contrôle humain |

### Maturité produit / plateforme (v0.6 — remplacé par la grille VSCode1)

Le raisonnement en 3 dimensions imaginé en v0.5 (état de l'art / marches à franchir / mode d'accompagnement) reste valable comme *lecture* de la grille, mais n'est plus l'instrument de mesure : on réutilise telle quelle la **Grille d'Assessment Agile V3.2 (variante IA-Agentic-Complet)** du projet VSCode1 — un référentiel déjà éprouvé (outil web de passation, résultats agrégés en radar, export de restitution PPT), plutôt que d'inventer une échelle qualitative à 5 crans.

Format du référentiel : **5 Piliers → Objectifs → Questions → 4 Niveaux (0–3)**, chaque niveau portant un texte descriptif complet (pas un simple chiffre).

| Pilier | Objectifs | Pertinence pour BMAD IAP |
|---|---|---|
| Équipe Produit | Gestion du backlog · fonctionnement en équipe produit · orientation client & pilotage par la valeur | Adjacent — utile en périphérie de `iap-product-definition` |
| **Excellence Technique** | Ingénierie logicielle & testing · usine DevOps existante et évolutive · indicateurs de performance/qualité (TTM) | **Cœur du périmètre infra** — réutilisé directement comme grille de maturité plateforme |
| Culture de l'Entreprise Agile | Rôles & collaboration · leadership & culture agile · Ressources Humaines | Adjacent — recoupe `iap-change-coach` |
| **Agilité à l'Échelle** | Vision de la transformation · fonctionnement à l'échelle · gouvernance & management des produits | **Cœur du périmètre** — recoupe `iap-operating-model` |
| **IA, Agentic et Organisation Augmentée** | Acculturation/adoption · gouvernance & IA responsable · produit/métier/excellence technique · agentic readiness · AgentOps & industrialisation · organisation multi-agent | **Remplace le M0–M4 générique ci-dessus** — plus opérationnel, question par question |

### Extrait — pilier « Excellence Technique », objectif « Usine DevOps »

> **Question :** « Comment est réalisée la chaîne de construction des livrables ? »
> **[0]** Chaîne manuelle. **[1]** Chaîne automatisée et fiabilisée. **[2]** Pipeline d'intégration continue déclenché automatiquement, exécute build/tests, livrable versionné dans un dépôt. **[3]** Livrable packagé/versionné (snapshot/RC/final), portable, équipe produit autonome sur build et configuration des tests.

### Extrait — pilier « IA, Agentic », objectif « Agentic Readiness »

> **Questions (niveaux 0–3 rédigés dans le référentiel source) :** « Les processus sont-ils suffisamment explicites, documentés et mesurables pour être exécutés par des agents ? » · « Les rôles respectifs des humains et des agents sont-ils clairement définis ? » · « Les équipes savent-elles concevoir, utiliser et piloter des agents IA ? »

> **Décision de cadrage :** Importer directement `Grille-Assessment-Agile-V3.2-IA-Agentic-Complet.xlsx` comme source de `platform-maturity-model.md`, plutôt que de ré-écrire une échelle à la main. `iap-intake` positionne chaque client sur les piliers **Excellence Technique** et **Agilité à l'Échelle** (maturité produit/plateforme) et sur le pilier **IA, Agentic et Organisation Augmentée** (maturité IA, en lieu et place du M0–M4 générique).

### Dépendances externes — versionnage (v1.6)

BMAD IAP réutilise des artefacts vivants issus de deux projets frères qui continuent d'évoluer indépendamment. Sans pin explicite, une évolution de VSCode1 ou VSCode2 pourrait faire dériver silencieusement le cadrage sans que personne ne le remarque avant un engagement client.

| Dépendance | Version pinnée | Fichier local de référence | Déclencheur de resynchronisation |
|---|---|---|---|
| Grille d'Assessment Agile (VSCode1) | **V3.2**, variante IA-Agentic-Complet | `knowledge/platform-maturity-model.md` (§Modèles de maturité) | Revue obligatoire avant tout nouvel engagement si VSCode1 publie une V3.3+ ; `iap-strategy-lead` évalue l'écart avant d'importer |
| Contrats de handoff & checkpoint OpenHub — ADR-006 / ADR-009 (VSCode2) | Version des ADR au moment de l'emprunt, à consigner dans `knowledge/doctrine-and-golden-rules.md` | Contrats de handoff (§Agents) et checkpoint non-automatisable (§Gate IA) | Revue si OpenHub republie ADR-006 ou ADR-009 sous un numéro/contenu modifié |
| Moteur d'assessment / Interview-to-Deck (VSCode2) | Structure de données seule (Mission/Trame/Theme/Question…), pas le code applicatif | `platform-maturity-model.md`-adjacent — voir §Moteur d'assessment | Revue si VSCode2 change son schéma de données source |

Règle de cadrage : chaque dépendance externe versionnée est revue systématiquement à deux moments — à chaque boucle de réévaluation `iap-re-assessment` (T+6–12 mois, voir §Schéma de fonctionnement) et à chaque passage de MVP gate (voir §Roadmap) — plutôt que laissée sans point de contrôle jusqu'à ce qu'une incohérence soit détectée en mission. Propriétaire de cette revue : `iap-strategy-lead`, consigné dans le même fichier que les décisions ADR de l'operating model.

## [Doctrine] Cross-walk des échelles & vocabulaires (v2.2 — réduction de charge cognitive)

Le cadrage manipule plusieurs échelles à paliers qui se recoupent partiellement — source réelle de charge cognitive, la famille « Gaspillage cognitif » (§Traitement des gaspillages) appliquée à la méthode elle-même. Cette section les remet à plat **une fois**, pour éviter qu'un lecteur les confonde ou croie devoir toutes les tenir en tête séparément. Règle de lecture : ce n'est **pas** un décret d'équivalence — le doc refuse déjà de traiter le spectre A/B/C comme strictement linéaire (§Ambition de l'outil) — mais une aide de lecture des correspondances approximatives.

**Il n'y a pas 6 échelles parallèles, mais 3 natures distinctes :**

| Nature | Échelle(s) | Rôle |
|---|---|---|
| **Mesure d'état (input)** | Maturité IA client **M0–M4** · Grille V3.2 **niveaux 0–3** par pilier/objectif (§Modèles de maturité) | Mesure l'état réel du client. **Plafonne** jusqu'où on a le droit de monter dans le gradient de délégation — ne s'y superpose pas. |
| **Choix d'ambition (cabinet)** | Ambition de l'outil **A / B / C** (§Ambition de l'outil) | Combien d'autonomie on donne à **l'outillage BMAD IAP** lui-même. Indépendant de la maturité client. |
| **Gradient de délégation (exécution)** | Coach/Délégué · assisté/supervisé/délégué · manuel/semi-auto/auto · Team Topologies Collaboration/Supervision/X-as-a-Service | **Un seul et même gradient** (« l'humain fait / supervise / laisse faire »), décliné selon l'objet gouverné. |

**Le gradient de délégation, unifié — le même mouvement, 4 déclinaisons :**

| Palier | US / posture consultant (§Traitement des gaspillages, §Focus management) | Agent IA dans une équipe (§Modèles d'équipe, v1.8) | Mode de workflow (OpenHub, §Agents) | Mode d'interaction Team Topologies augmenté (§Modèles d'équipe) |
|---|---|---|---|---|
| **Bas** — l'humain fait ou valide tout | **Coach** (le consultant fait) | **assisté** (l'humain valide chaque sortie) | **manuel** | **Collaboration** (ad hoc, haute bande passante) |
| **Milieu** — l'humain supervise / audite | *(transition Coach → Délégué)* | **supervisé** (audit a posteriori par échantillon) | **semi-auto** | **Supervision** (4ᵉ mode candidat) |
| **Haut** — l'exécutant agit seul dans son mandat | **Délégué** (le client ou un agent fait) | **délégué** (l'agent décide seul dans son mandat) | **auto** | **X-as-a-Service** (self-service sans collaboration continue) |

**La mesure d'état plafonne le palier atteignable** — c'est ce qui relie les deux premières natures au gradient, et c'est déjà le mécanisme des règles dures du cadrage :

- Grille **Excellence Technique / Usine DevOps niveau [0]** → interdit le pattern « Automatiser » (§Traitement des gaspillages) : on ne dépasse pas le palier bas tant que la chaîne n'est pas fiabilisée.
- Grille **Agentic Readiness [0]–[1]** → force la branche **documentation-first**, interdit le palier « délégué » d'un agent (§Export markdown) : le process doit être explicite *avant* l'agent, pas après.
- Classification **D3–D4 sans LLM local qualifié** → mode M0 / documentation-first (§Gate IA).

> **Ce que ce cross-walk ne fait pas :** il n'aplatit pas les échelles en une seule. Coach/Délégué reste **binaire** (une US est Coach *ou* Délégué), le gradient agent est à **3 paliers**, l'ambition A/B/C est un **choix de gouvernance non nécessairement linéaire** — les correspondances par ligne sont des repères de lecture, pas des synonymes interchangeables. L'intérêt : un consultant qui a intégré « bas / milieu / haut = qui fait, qui supervise, qui laisse faire » n'a plus qu'**un** mouvement mental à tenir, décliné selon l'objet, au lieu de six vocabulaires à mémoriser séparément.

## [Méthode] Définition produit infra

Un produit d'infrastructure : ensemble cohérent de capacités techniques, fourni comme service à des clients internes/externes, avec responsable, cycle de vie, roadmap, engagements de qualité.

> **Test de qualification :** « Puis-je décrire ce que j'offre à un utilisateur, la valeur apportée, les engagements de service, les règles d'usage, les évolutions prévues, les métriques de succès ? » Si oui → produit. Si non → actif ou composant technique. Vision cohérente avec ITIL 4 et le Platform Engineering : on ne livre plus des technologies, mais des produits de plateforme consommés comme des services.

### Niveaux de granularité

| Niveau | Exemple | Usage BMAD |
|---|---|---|
| Produit plateforme | Cloud interne, Kubernetes, CI/CD, observabilité | Objet principal de product definition |
| Service | Sauvegarde, base managée, digital workplace | Partie du catalogue de capacités |
| Capacité | Provisioning VM, secret management | Brique consommable |
| Automatisation | Script, template, API, workflow self-service | Réduit le RUN / simplifie les parcours |
| Gouvernance | Standard sécurité, politique FinOps | Cadre d'usage et de décision |
| Expérience | Créer une app, diagnostiquer un incident | Parcours à designer et mesurer |
| Composant | Serveur, VM, switch, firewall | Ressource technique, pas produit par défaut |

> **Décision de cadrage — Product Discovery :** Le framework source distingue Product Discovery (personas, parcours, pain points) de Product Definition. Dans ce cadrage, la discovery reste **fusionnée** dans l'étape 1 de `iap-product-definition` — plus simple pour MVP1, à rouvrir en MVP4 si un client demande une discovery approfondie découplée.

## [Méthode] Traitement des gaspillages

Le focus le plus développé du corpus — traité comme un objet de transformation à part entière, au même niveau que le produit, l'operating model, l'adoption et l'IA.

### Familles

| Famille | Exemples |
|---|---|
| Flux | Attentes, validations multiples, dépendances |
| Humain | Experts seniors sur tâches répétitives, management subi |
| RUN | Incidents récurrents, demandes répétitives, escalades |
| Financier | Surdimensionnement, ressources non décommissionnées |
| Cognitif | Trop d'outils, procédures complexes, doc dispersée |
| Décisionnel | Arbitrages subjectifs, priorisation opaque |
| Environnemental | Ressources inutilisées, environnements non éteints |
| IA | Cas d'usage gadget, données non fiables, automatisation sans garde-fous |

### Chaîne de traitement

Détecter → Qualifier → Quantifier → Comprendre la cause racine → Choisir un pattern → Prioriser → Expérimenter → Mesurer → Industrialiser → Prévenir la réapparition.

### Scoring de priorisation

```
Score impact     = capacité + utilisateur + delivery + RUN + financier + risque + environnement
Score faisabilité = faisabilité + maturité données/outillage + confiance preuves
Score prudence IA = confidentialité + besoin supervision + criticité décision

Priorité = Score impact × Score faisabilité − Score prudence IA
```

Le score ne remplace pas l'arbitrage humain : il rend la discussion explicite.

> **Ce « score » est un support de discussion ordinal, pas une métrique calculée (v2.2) :** La forme `Impact × Faisabilité − Prudence IA` peut faire croire à une mesure — or ses trois termes sont des **sommes ordinales non pondérées**, sans échelle définie, et « produit moins somme » n'a pas de sens dimensionnel strict. Le présenter comme une équation contredirait la vigilance du reste du cadrage contre la **fausse confiance** (KPI sans méthode §KPIs, badge cosmétique §Qualité & test). À lire donc comme un **classement par paliers** (fort / moyen / faible), pas un nombre exact : c'est déjà ce que fait le deck, qui traite la Prudence IA comme **recoloration d'alerte** au-delà d'un seuil plutôt que comme un vrai 3ᵉ axe (§Workflows, `iap-deck-builder`). Deux voies acceptables, à trancher à l'usage : soit assumer le support ordinal tel quel (et le montrer en tiers, jamais en score à la décimale), soit définir explicitement échelles et pondérations avant d'en faire un chiffre communiqué.

> **Garde-fou anti-déplacement :** Avant de déclarer un gain : vérifier qu'il ne crée pas plus de charge utilisateur/support, plus de complexité cognitive, plus de risque sécurité, plus de coûts cachés, plus de dette technique ou de dépendance fournisseur.

### Automatisation concrète (v1.3 — le pattern « Automatiser » restait un mot dans une case)

Deux artefacts nouveaux pour transformer le pattern « Automatiser » de la bibliothèque de traitements en plan exécutable, plutôt que de le laisser au niveau du principe.

| Artefact | Déclenchement | Contenu |
|---|---|---|
| `automation-readiness-checklist.md` (9ᵉ checklist) | Avant de choisir le pattern « Automatiser » (étape « Choisir un pattern » de la chaîne de traitement) | Processus déjà simplifié/standardisé ? Encore utile aujourd'hui ? Réellement stable et déterministe ? Qui a intérêt à ce qu'il reste manuel ? — propriétaire : `iap-waste-treatment-lead` |
| `automation-action-plan.md` (14ᵉ template) | Après scoring, une fois le pattern « Automatiser » retenu | Portée exacte, prérequis techniques, effort, définition du « fait », mode Coach/Délégué, plan de retrait du geste manuel — **deux branches distinctes** : Test & Qualité (confiance, risque de faux sentiment de sécurité) vs Tâche RUN (capacité récupérée, provisioning/nettoyage) |

> **Gate de maturité DevOps — tranché (v1.6) : dur par défaut, dérogation tracée :** Recommander « automatiser les tests » quand le pilier **Excellence Technique / Usine DevOps** (grille VSCode1) est mesuré au niveau [0] (chaîne manuelle) est un anti-pattern quasi certain — la recommandation pertinente à ce niveau est « fiabiliser la chaîne de construction », pas automatiser par-dessus. Décision : **règle dure par défaut** — `iap-waste-treatment-lead` ne peut pas retenir le pattern « Automatiser » tant que le niveau mesuré est [0], sauf **dérogation explicite** consignée comme une décision ADR à part entière dans `operating-model/decisions/` (Statut / Contexte / Décision / Conséquences / **Alternatives rejetées obligatoire**) et contre-signée par `iap-risk-reviewer` avant d'être appliquée. Ce compromis protège contre l'anti-pattern par défaut (la règle dure) tout en préservant l'arbitrage humain pour le cas réel où le consultant a une raison documentée de déroger (la règle souple, mais jamais silencieuse) — cohérent avec le principe déjà acté « le score ne remplace pas l'arbitrage humain, il le rend explicite ».

**Coach/Délégué appliqué à l'automatisation** : toute US liée à l'automatisation doit porter une date ou un critère de bascule Coach → Délégué explicite — sans quoi le consultant risque de s'installer en exécutant technique permanent, à l'exact opposé de la posture Enabling « jamais permanente » (voir §Modèles d'équipe). Métrique de sortie de mission : proportion d'US automatisation encore taguées Coach à T+3 mois — un chiffre élevé signale une dépendance non résorbée.

**Métriques de capacité réellement libérée**, portées par `iap-metrics-sre-finops-lead`, exprimées avec tag de confiance comme le reste (une baisse de MTTR sans ExternalEvidence à l'appui reste `DÉDUIT`, pas `CONFIRMÉ`) : temps de cycle build→déploiement, interventions manuelles/semaine sur la tâche ciblée, MTTR et régressions en prod, tickets de demande manuelle, et un **taux d'override manuel** — un taux élevé signale que l'automatisation ne couvre pas le cas réel et que le geste manuel perdure en doublon.

## [Méthode] Comitologie (v1.0 — jusqu'ici diluée entre operating-model, waste-treatment et diagnostic)

Instances de décision, rituels, cadences : jusqu'à présent répartis sans point de convergence entre `iap-operating-model` (cadences/décisions clés), `iap-waste-treatment` (cadences de revue du backlog) et `iap-diagnostic-systemique` (`governance-friction-map.md`). Cette section les rassemble sans créer de 12ᵉ agent.

### Anti-patterns à nommer explicitement

- **Le comité qui valide mais n'arbitre jamais** — tout le monde dit « OK » en réunion, le vrai arbitrage se fait après, en couloir ou par défaut.
- **Cadence calée sur le calendrier plutôt que sur le flux** — un comité mensuel traite un sujet urgent trois semaines trop tard, ou se réunit sans rien à décider.
- **Empilement d'instances redondantes** — le même sujet remonte à trois niveaux sans qu'aucun n'ait un mandat de décision distinct.
- **Comitologie muette sur le RUN** — la gouvernance suit le BUILD/projets, aucune instance n'a mandat sur les incidents récurrents ou la dette RUN.
- **Comité fantoche post-gate IA** — une instance créée pour superviser l'IA qui ne challenge jamais vraiment un cas d'usage, contredisant l'esprit du checkpoint non-automatisable.
- **Comitologie qui survit à sa raison d'être** — une instance créée pour un projet ponctuel continue de se réunir des années après, sans clause de fin de vie.

### Pivots recommandés

- Remplacer un **comité de suivi de projet** (statuts, jalons) par une **revue de flux** centrée sur ce qui bloque réellement.
- **Fusionner les instances redondantes** autour d'un mandat de décision unique par sujet plutôt que plusieurs comités qui discutent la même chose à des granularités différentes.
- Instances d'arbitrage à **deux issues obligatoires** — « on fait » ou « on ne fait pas / pas maintenant » — bannir l'issue implicite « on en reparle ».
- **Time-boxer les comités eux-mêmes** — toute nouvelle instance porte une date de revue de pertinence (6-12 mois), avec option de suppression.
- Séparer explicitement **pilotage opérationnel** (flux, incidents, décisions courtes) et **pilotage stratégique** (trajectoire produit, arbitrages budgétaires) en deux cadences distinctes.

### Bibliothèque de patterns par scénario, pas une cible générique unique

Une comitologie cible unique reproduirait l'anti-pattern « agilité sans traiter le contexte » : elle doit suivre la même logique de bibliothèque que `scenario-library.md`, pas un design générique.

| Scénario | Pattern de comitologie |
|---|---|
| RUN massif | Comitologie resserrée sur le flux incidents/dette, cadence courte, peu de participants — pas de grand comité stratégique tant que le RUN n'est pas stabilisé |
| TMA dominante | Le fournisseur doit être partie prenante formelle, pas seulement en reporting, sinon les décisions client n'ont pas de prise sur le RUN externalisé |
| Priorités politiques | Instance de priorisation transparente (score visible) pour désamorcer le jeu de pouvoir plutôt qu'une liste de règles |
| Organisation sceptique | Ne pas ajouter de comité du tout — rendre la décision visible dans un rituel existant, pour ne pas nourrir le scepticisme (« encore une usine à gaz ») |

Liste illustrative, pas exhaustive des 9+ scénarios déjà routés (voir §Routage des scénarios).

### Checkpoint conditionnel selon le risque — hybride, pas 100 % automatisable

Le principe ADR-006 (checkpoint IA toujours manuel mais pas systématique en mode semi-auto/auto, voir §Agents) se transpose partiellement : une instance humaine ne se réunirait qu'au franchissement d'un seuil de risque/désaccord/impact plutôt qu'à date fixe. Mais contrairement au gate IA (seuil assez objectif : classification de données), un désaccord humain reste qualitatif — risque de sur-outiller un jugement qui ne s'y prête pas complètement. Compromis retenu : une **cadence plancher basse** (ex. trimestrielle) comme filet de sécurité, plus des convocations hors cycle dès qu'un seuil est franchi — cohérent avec le refus déjà acté de traiter le spectre d'ambition A/B/C comme strictement linéaire (voir §Ambition de l'outil).

> **Portage — pas un agent dédié :** Onzième agent déjà nombreux : plutôt qu'un 12ᵉ, une **checklist** `comitologie-coherence.md` invoquée par `iap-risk-reviewer` (croise les cadences proposées par les différents workflows pour détecter des doublons ou contradictions), et un **template transverse** `governance-instance-map.md` — propriété canonique de `iap-operating-model-architect`, amendé (jamais réécrit) par `iap-waste-treatment-lead` et `iap-diagnostic-systemique`, même principe que `ai-risk-register.md`.

### Livrable : matrice instance × fréquence × décision × participants × source de vérité

Colonnes : instance, fréquence/déclencheur (date fixe ou seuil de risque), décision portée, participants, source de vérité, **instance remplacée/fusionnée** (pour tracer le pivot, pas seulement l'état cible). Vit comme sous-section de `governance-friction-map.md` (diagnostic) qui bascule en cible dans `operating-model/` — pas un fichier entièrement nouveau. À ne pas confondre avec un RACI classique : centré sur la décision et sa cadence, pas sur qui-fait-quoi au quotidien.

### Expérimentée, pas décrétée — sauf le gate IA

Cohérent avec la chaîne de traitement des gaspillages (Prioriser → **Expérimenter** → Mesurer → Industrialiser, voir §Traitement des gaspillages) et avec les expérimentations pilotes qui nourrissent l'operating model (voir `iap-operating-model` en §Workflows) : une nouvelle cadence de comitologie est elle-même un candidat à une expérimentation courte (« tester une revue de flux hebdomadaire pendant 6 semaines ») plutôt qu'un décret descendant — portée directement par une US du `transformation-backlog.md`, taguée Coach ou Délégué. Exception explicite : le **gate IA reste non négociable**, jamais sujet à une pré-expérimentation légère.

## [Méthode] Modèles d'équipe (v1.2 — Team Topologies, étendu aux agents IA)

Déjà cité en une ligne dans le brainstorm source (« framework d'agilité à l'échelle, team topologie et structure d'équipe »), jamais développé. Le rattacher explicitement à `iap-operating-model-architect` : la cible « plateforme opérée comme un produit » de toute la mission BMAD IAP **est**, au sens de ce framework, une *Platform Team*.

### 4 types d'équipe (Team Topologies)

| Type | Rôle | Lecture BMAD IAP |
|---|---|---|
| **Stream-aligned** | Alignée sur un flux de valeur métier continu | Les équipes applicatives clientes de la plateforme infra |
| **Platform** | Fournit des capacités en self-service (X-as-a-Service) pour réduire la charge cognitive des stream-aligned | **La cible même de la transformation IAP** — pas un type parmi d'autres, l'objet du module |
| **Enabling** | Aide temporairement une équipe à monter en compétence sur un domaine, puis se retire | Posture du coach BMAD IAP pendant la mission — jamais permanente |
| **Complicated-subsystem** | Expertise pointue sur un composant à compétences rares | Distingue un vrai sous-système complexe (ex. moteur ML) d'un produit plateforme classique — voir §Définition produit infra |

### 3 modes d'interaction — et un 4ᵉ à envisager

- **Collaboration** — travail conjoint étroit et temporaire, haute bande passante de communication.
- **X-as-a-Service** — une équipe consomme une capacité en self-service sans collaboration continue : le mode cible d'une Platform Team mature, cohérent avec toute la doctrine produit déjà cadrée.
- **Facilitating** — une équipe aide une autre à progresser sans faire le travail à sa place.

`iap-operating-model-architect` doit qualifier explicitement le mode actuel (souvent Collaboration ad hoc — ticket, réunion) et le mode cible (X-as-a-Service) pour la relation infra/équipes applicatives. Lecture directe du backlog de transformation déjà cadré : une US taguée **Coach** relève typiquement d'un mode Facilitating/Enabling ; une US taguée **Délégué** marque le passage effectif vers l'autonomie X-as-a-Service de l'équipe cliente.

> **Extension — les agents IA comme membres d'équipe :** Team Topologies a été conçu pour des équipes 100 % humaines. Extension nécessaire pour BMAD IAP, cohérente avec le pilier **IA, Agentic et Organisation Augmentée** de la grille de maturité (§Modèles de maturité) :
> - Un agent IA peut être **membre à part entière d'une Stream-aligned team** (ex. triage de tickets, préparation de PR) — réduit la charge cognitive humaine, mais exige un mandat clair de ce que l'agent décide seul vs escalade (rejoint le gate IA et son checkpoint non-automatisable).
> - Une **Platform Team peut exposer un agent IA comme capacité en self-service** — un agent conversationnel de triage devient une brique du catalogue de capacités, au même titre qu'un pipeline CI/CD.
> - **Mode d'interaction candidat, absent du modèle original : Supervision** — une équipe humaine supervise un agent IA opérant à un niveau d'autonomie donné, sur le même principe que les 3 modes manuel/semi-auto/auto déjà empruntés à OpenHub (§Agents) — proposé comme 4ᵉ mode plutôt que forcé dans Collaboration ou X-as-a-Service.
> - La question « les rôles respectifs des humains et des agents sont-ils clairement définis ? » (pilier Agentic Readiness de la grille VSCode1) est, de fait, une question de team topology augmentée — les deux référentiels se recoupent et devraient être lus ensemble par `iap-operating-model-architect`.

Nouveau template à prévoir : `team-topology-map.md` — équipes existantes (type, mode d'interaction actuel), équipes cibles, et localisation des agents IA (membre d'équipe vs capacité exposée) — rattaché à `iap-operating-model`, alimenté comme le reste par les expérimentations pilotes (voir §Workflows) plutôt que décrété d'emblée.

### Mise en œuvre des agents IA dans les équipes — réflexion (v1.7)

La section précédente classe l'agent dans le framework (type d'équipe, mode d'interaction) ; elle ne dit rien de **comment une équipe passe de zéro agent à un agent réellement utilisé**. Question distincte, et probablement plus déterminante pour le succès d'une mission IAP que la taxonomie elle-même — brainstorm non tranché, à confronter aux premières expérimentations pilotes plutôt qu'à décréter en cadrage pur.

> **Trajectoire d'adoption, pas un interrupteur :** le mécanisme **Coach → Délégué** déjà retenu pour l'automatisation des gaspillages (§Traitement des gaspillages) et pour la posture managériale (§Focus management) se transpose ici tel quel plutôt que de réinventer un troisième vocabulaire pour le même phénomène : une équipe ne bascule pas d'un jour à l'autre au tout-agent. Trois paliers observables, alignés sur les 3 modes d'exécution IA déjà cadrés (§Gate IA) : **assisté** (l'agent propose, un humain valide chaque sortie avant usage — la charge cognitive baisse peu, mais la confiance se construit), **supervisé** (l'agent agit dans un périmètre déclaré, l'humain audite un échantillon a posteriori plutôt que de tout relire), **délégué** (l'agent décide seul dans son mandat, l'humain n'intervient que sur escalade). La bascule d'un palier au suivant se déclenche par l'usage constaté, pas par une date de mission arrêtée à l'avance — même logique anti-décret que le reste de la doctrine d'automatisation.

> **Préalable non négociable — le process doit être explicite avant l'agent, pas après :** la grille V3.2 pose déjà la question (« les processus sont-ils suffisamment explicites, documentés et mesurables pour être exécutés par des agents ? », §Modèles de maturité, pilier Agentic Readiness). Introduire un agent sur un processus tacite ou disputé revient à figer une pratique mal définie dans du code — et rend l'écart entre ce que l'agent fait réellement et ce que l'équipe croit qu'il fait plus difficile à détecter qu'un désaccord entre deux humains. Ordre de mission recommandé : documenter/stabiliser le processus cible (souvent déjà le travail d'`iap-operating-model-architect`) **avant** de qualifier une opportunité agentique dessus, jamais en parallèle pour gagner du temps.

> **Mandat écrit, pas un usage qui dérive à l'implicite :** pour chaque agent introduit dans une équipe, trois questions doivent avoir une réponse écrite avant le palier « supervisé » — Qu'est-ce que l'agent décide seul ? Qu'est-ce qui doit remonter à un humain (rejoint le checkpoint non-automatisable du gate IA, §Gate IA) ? Qui répond quand l'agent se trompe — le manager de l'équipe, ou `iap-ai-governance-lead` en tant que propriétaire transverse de la gouvernance IA ? Sans ce mandat écrit, le mode d'interaction « Supervision » proposé plus haut se réduit en pratique à une Collaboration ad hoc non assumée, l'exact anti-pattern que la doctrine essaie d'éviter ailleurs (§Comitologie, anti-patterns).

> **Résistance et deskilling — deux risques symétriques, tous deux du ressort d'`iap-change-coach` :** un agent introduit trop vite déclenche la même dynamique de résistance qu'un changement d'outillage classique (rejoint la persona « expert devenu manager malgré lui », §Focus management, pour le cas où c'est justement le manager qui pousse l'agent sans porter le sujet auprès de son équipe) — traiter comme un changement organisationnel, pas comme un déploiement technique. Risque inverse, moins souvent nommé : une équipe qui bascule trop vite en mode délégué perd la capacité tacite de faire le travail sans l'agent — un `deskilling-risk` à consigner sur le modèle d'`ai-risk-register.md`, avec un signal de sortie de mission simple (« l'équipe saurait-elle reprendre la main une semaine sans l'agent ? ») plutôt qu'un jugement qualitatif non vérifiable.

> **Ce que ça change à la roadmap :** ce sujet relève de MVP4 (« agentic opportunities », §Roadmap) pour l'outillage — mais la question du **mandat par équipe** peut et doit être posée dès qu'un agent existant (BMAD ou tiers) touche une équipe cliente, y compris avant MVP4, au même titre que le gate IA n'a jamais été conditionné à un MVP donné. Position provisoire : pas de nouveau template dédié — le mandat par agent vient enrichir `team-topology-map.md` (déjà prévu ci-dessus) d'une colonne mandat/escalade/owner plutôt que de créer un document séparé, à confirmer ou infirmer à l'usage sur les premières missions pilotes.

### Démarche d'accompagnement — mise en place d'un agent dans une équipe (v1.8)

La réflexion ci-dessus pose le cadre (paliers, préalable, mandat, risques) ; elle ne donne pas de séquence actionnable pour une équipe cliente donnée. Démarche en 5 phases, conçue pour être **portée par les agents et gabarits déjà cadrés** — aucun nouvel agent, cohérent avec le refus déjà acté d'un agent dédié par sujet transverse (§Comitologie, §Recommandations niveau équipe).

| Phase | Objectif | Owner | Sortie de phase (critère de passage) |
|---|---|---|---|
| 0 · Qualifier | Vérifier que le candidat est un vrai gaspillage récurrent, pas un gadget IA — réutilise le scoring impact × faisabilité − prudence IA (§Traitement des gaspillages), pas une grille séparée | `iap-waste-treatment-lead` | Candidat scoré, priorité justifiée |
| 1 · Cadrer le process | Documenter/stabiliser le processus cible **avant** l'agent (préalable non négociable ci-dessus) | `iap-operating-model-architect` | Processus explicite et validé par l'équipe — pas de version tacite/disputée |
| 2 · Mandater | Rédiger le mandat écrit : décide seul / escalade / owner des erreurs (checklist ci-dessus) | `iap-ai-governance-lead` + manager de l'équipe cliente | Mandat signé des deux côtés, versionné dans `team-topology-map.md` |
| 3 · Piloter en assisté | 1 à 2 cas réels, l'humain valide chaque sortie ; accompagnement humain en parallèle sur le volet résistance/compétences — mêmes 3 pistes que la persona « expert devenu manager malgré lui » (mentorat par un pair externe, pairing sur des situations réelles, formation ciblée sur un seul geste), §Focus management | `iap-change-coach` (accompagnement) + équipe pilote | Taux d'adhésion mesuré, aucun incident non détecté |
| 4 · Élargir en supervisé, puis délégué | Périmètre élargi, audit a posteriori par échantillon ; bascule en délégué seulement si le signal `deskilling-risk` est négatif (« l'équipe saurait-elle reprendre la main une semaine sans l'agent ? ») | `iap-metrics-sre-finops-lead` (mesure) + `iap-risk-reviewer` (challenge avant généralisation) | Cadence de revue périodique actée, alignée sur la boucle `iap-re-assessment` (§Schéma de fonctionnement) |

> **Ce que cette démarche n'est pas :** un plan de déploiement technique séquencé par des dates. Chaque passage de phase se déclenche par un critère observé (adhésion, incidents, signal deskilling), pas par un calendrier — même principe anti-décret que le reste de la doctrine d'automatisation (§Traitement des gaspillages) et qu'une nouvelle cadence de comitologie (§Comitologie, « Expérimentée, pas décrétée »). Une équipe peut rester durablement en phase 3 (assisté) par choix, au même titre qu'un cabinet peut rester au niveau d'ambition A (§Ambition de l'outil) — la démarche n'a pas de palier « final » obligatoire.

## [Méthode] Moteur d'assessment (v0.6 — emprunté à VSCode2 / Interview-to-Deck)

Le diagnostic BMAD IAP restait, jusqu'ici, décrit comme une prose libre issue d'« axes d'analyse ». Le projet Interview-to-Deck (outil de capture d'entretiens qualitatifs pour audits) fournit un pipeline déjà éprouvé pour exactement ce besoin — on en reprend la structure de données, pas le code.

### Hiérarchie de capture

```
Mission (= engagement IAP)
  └─ Trame
       └─ Theme          ← les axes de diagnostic déjà identifiés
            └─ Question   ← reprend §8.4 : flux/priorisation, RUN/support,
                             humain/compétences, financier/environnemental,
                             cognitif/UX, décisionnel/gouvernance, IA/données

Interview (une par partie prenante : équipe infra, utilisateur, management, sponsor)
  ├─ Answer            (par Question, statut pending/answered/skipped/revisit)
  ├─ Verbatim           (citation rattachée à une Question — alimente le deck)
  └─ audio_backup_path  (v1.5 — sauvegarde audio complète, filet de sécurité uniquement)

CoachNote (v1.5 — réflexion libre hors trame formelle : trajet, debrief à chaud, intuition)
  └─ audio_backup_path  (même mécanisme, jamais transcrit sans passage par le gate IA)
```

> **Enregistrement audio (v1.5 — repris de VSCode2 / Interview-to-Deck) :** VSCode2 conserve, par Interview, un `audio_backup_path` (chemin relatif à `data/recordings/`) : la sauvegarde audio complète de l'entretien, jamais transcrite automatiquement — un **filet de sécurité** en cas de souci d'extraction/transcription, l'audio brut n'étant sinon jamais conservé. Repris tel quel pour les Interviews BMAD IAP, et étendu à une nouvelle entité légère **CoachNote** : réflexion vocale libre hors trame formelle (un debrief à chaud dans la voiture entre deux sites, une intuition à noter avant de l'oublier) — capture rapide, pas structurée en Thème/Question.

> **Confidentialité de l'audio — jamais un contournement du gate :** Un enregistrement audio d'interview est par défaut **D2+** (voix identifiable, propos non filtrés) — même règle de classification que le reste (§Gate IA). La transcription automatique d'un audio suit exactement le mode d'exécution IA déjà décidé pour la mission (IA client/LLM local/pas d'IA) ; l'audio brut ne part jamais vers une IA externe au prétexte que « ce n'est qu'une sauvegarde ». En mode M0, l'audio reste un filet de sécurité non exploité activement — pas de transcription du tout, le consultant retranscrit à la main s'il en a besoin.

> **L'audio D2+ au repos sur le mobile est une surface à part entière (v2.2) :** La règle ci-dessus gouverne la *transcription* de l'audio (quel modèle IA), mais l'App de capture terrain (§Solution technique) enregistre de l'audio **D2+ hors connexion puis synchronise en différé** — un téléphone perdu avec de l'audio non synchronisé est une exposition que « le choix du modèle » ne couvre pas. Exigences à cadrer pour l'App, au même rang que le gate lui-même : chiffrement au repos sur l'appareil, **purge automatique après confirmation de synchronisation** (l'audio brut n'est pas conservé sur le mobile au-delà du transfert, cohérent avec « l'audio brut n'étant sinon jamais conservé »), pas de sauvegarde cloud tierce automatique (iCloud/Google Drive), et l'App traitée comme un maillon de confidentialité, pas un simple périphérique de capture. À cadrer avant tout build de l'App (owner `iap-ai-governance-lead`, §Points ouverts).

> **Ce que ça résout :** La doctrine identifie la « multiplicité des utilisateurs internes » comme point d'attention permanent (§2.2 du corpus source), mais rien n'obligeait à interviewer chaque persona séparément. Une `Interview` par partie prenante rend ce principe opérationnel : RUN/infra, utilisateurs applicatifs et management répondent à la même Trame, ce qui permet ensuite de repérer les convergences et divergences entre points de vue plutôt que de produire un diagnostic monolithique.

### Import de données outils (v0.8 — repli sans connecteur live)

Le MVP6 (« Transformation Companion », voir §Roadmap) reste hors périmètre — mais rien n'empêche d'**importer manuellement des exports** de ServiceNow, Jira, Confluence, CMDB ou outils FinOps quand un accès direct n'est pas possible : extraits CSV de tickets, backlog exporté, inventaire CMDB, rapport de coûts cloud. Ces imports alimentent le **même diagnostic** que les interviews, mais par une entité distincte :

```
Interview → Answer / Verbatim   ← déclaratif, sujet au biais de l'interviewé
ExternalEvidence → source, type, date, référence   ← factuel, extrait d'un système
                                                       tag de confiance : toujours CONFIRMÉ
                                                       (donnée système, pas une opinion)
```

> **Pourquoi une entité séparée plutôt que fondre les deux :** Un ticket ServiceNow n'a pas le même statut épistémique qu'un verbatim d'interview : c'est une preuve factuelle (tag `CONFIRMÉ` automatique, voir §Agents), pas une déclaration à recouper. Séparer `ExternalEvidence` d'`Interview` permet à `iap-incident-postmortem-miner` (voir décisions ci-dessous) de croiser les deux sans confondre un fait et une perception — utile en particulier pour objectiver l'écart entre RUN perçu et RUN réel (voir §KPIs).

Format d'import minimal attendu : un CSV/export brut par outil source, mappé à la Trame via un fichier `import-mapping.md` par engagement (quelles colonnes source correspondent à quels Thèmes/Questions) — pas de connecteur API, juste un import de fichier déposé par le client ou le consultant.

### Synthèse (v1.1 — revue et approfondie)

Une **Synthesis** par Thème (convergences/divergences entre interviewés), puis une **GlobalSynthesis** à 5 catégories fixes, transverse à la mission — remplace la prose libre de `diagnostic-systemique.md` par une structure éprouvée :

Catégories : `Contexte` · `Culture & ADN` · `Forces / succès` · `Points d'amélioration` · `Aspirations (ou leur absence)`

> **Revue de structure — 3 clarifications (v1.4) :**
> - **Aspirations autorise explicitement un contenu négatif** — résignation, épuisement, aspiration absente sont des constats de plein droit, pas un échec à remplir la case. Les scénarios « organisation sceptique », « RUN massif » ou « absence de sponsor mandaté » (§Routage des scénarios) produisent rarement une vision positive spontanée ; forcer une formulation positive de façade ment sur l'état réel.
> - **Non-duplication explicite avec le waste-register** : « Forces/succès » et « Points d'amélioration » sont la couche *exécutive* (5-10 lignes qu'un sponsor lit en premier), le waste-register reste l'outil de travail scoré du consultant — les deux publics et les deux granularités sont différents, ça doit être dit dans le livrable (« voir waste-treatment-backlog.md pour le détail scoré »), pas seulement supposé.
> - **Distribution des tags visible par catégorie** — chaque paragraphe de GlobalSynthesis liste en fin de texte la distribution des tags de ses constats sources (ex. « 3 CONFIRMÉ, 2 DÉDUIT, 1 INCERTAIN »), pour ne pas aplatir en un seul bloc lisse des constats de fiabilité très inégale. Ferme le point ouvert v1.1 sur les tags hétérogènes.
>
> RUN/BUILD, comitologie, Team Topologies et gouvernance IA n'ont pas de foyer naturel dans les 5 catégories — décision : enrichir d'abord la Trame (Thèmes/Questions guides propres à chaque catégorie) plutôt que d'ajouter une 6ᵉ catégorie d'emblée, une 6ᵉ catégorie restant en réserve si l'enrichissement s'avère insuffisant à l'usage.

Jusqu'ici cadrée en une seule phrase alors qu'elle est le maillon qui transforme des réponses brutes en matière exploitable. Champs minimaux désormais explicites :

```
theme_id, mission_id
statut            ← empty / draft-generated / edited / validated (cycle de vie)
méthode_génération ← llm / manuel-outillé / atelier-collectif (INDÉPENDANT du statut :
                     un M0 sans IA a bien un "generated", produit par manual-synthesis-guide.md)
couverture         ← répondants / total prévu + répartition par persona (infra/utilisateur/
                     management/sponsor) — condition nécessaire pour détecter un faux consensus
constats[]         ← texte + tag CONFIRMÉ/DÉDUIT/INCERTAIN + sources (Verbatim.id et/ou
                     ExternalEvidence.id) + type dominant (déclaratif/factuel/mixte)
divergences[]      ← distinctes des convergences, voir structure ci-dessous
alerte_couverture  ← posée automatiquement si 0 réponse ou déséquilibre fort par persona
```

> **Triage des tags de confiance — le lien manquant avec §Agents :** Les tags CONFIRMÉ/DÉDUIT/INCERTAIN (empruntés à OpenHub) et l'entité Synthesis étaient cadrés dans deux sections qui ne se citaient jamais, alors que l'exemple donné pour DÉDUIT (« constat déduit de plusieurs entretiens ») est littéralement une Synthesis. Règle désormais explicite : convergence forte (≥4 interviews alignées) → `DÉDUIT` ; convergence avec preuve factuelle à l'appui (ExternalEvidence, pas seulement des opinions répétées) → `CONFIRMÉ` ; divergence non résolue en fin de mission → `INCERTAIN`. Le tag se pose **par constat**, jamais globalement sur toute la Synthesis — une même Synthesis mélange typiquement les trois.

> **Garde-fou anti-faux-consensus, porté par la donnée :** Une Synthesis reste **provisoire** tant que la couverture est incomplète, affichée avec un bandeau explicite « provisoire — X/Y interviews reçues » (pas un simple label « draft » muet sur le manque). Sous un seuil de couverture (ex. <50 % des interviews prévues sur ce Thème), tout constat `DÉDUIT` est automatiquement rétrogradé en `INCERTAIN` — le tag suit la maturité réelle de l'échantillon, pas seulement le jugement de l'agent qui rédige. Un Thème à 0 réponse déclenche `alerte_couverture` plutôt que de disparaître silencieusement du diagnostic.

**Divergences structurées**, pas juste « les avis divergent » : chaque entrée porte la question source, les positions résumées par groupe d'interviewés avec `verbatim_id` précis, un `axe_de_divergence` (périmètre différent / fait vs perception / enjeu politique / information datée) et un statut de `résolution` (non résolu / tranché par ExternalEvidence / tranché par l'agent / divergence légitime acceptée). Une divergence non résolue en fin de mission remonte automatiquement dans `ai-risk-register.md` plutôt que de rester enterrée dans un fichier que peu de monde relit après le deck.

**Synthesis → waste-register** : jamais de génération automatique d'un gaspillage depuis une Synthesis — un constat de convergence n'est qu'un signal, un gaspillage qualifié suppose le passage Qualifier → Quantifier → Cause racine déjà cadré (voir §Traitement des gaspillages). Le pont reste *assisté* : un constat fortement négatif (mots-clés récurrents détectés par l'algorithme fréquence/cooccurrence du mode M0) peut pré-remplir un brouillon d'entrée dans le `waste-register` — le registre brut des signaux, distinct du `waste-treatment-backlog.md` qualifié et scoré qui n'accueille que ce qui a franchi ce passage — avec lien retour vers la Synthesis d'origine, jamais une entrée générée directement dans le backlog priorisé.

Correction apportée à la hiérarchie de capture : un `Verbatim` ne doit plus alimenter le deck-builder directement en court-circuitant la Synthesis — il doit d'abord être cité comme source d'un constat tagué, pour ne pas ouvrir un chemin parallèle non gouverné par les tags de confiance.

### Recommandations

**RecommendationAxis** (3–4 axes transverses, pas un axe par thème) → **Recommendation** (Objectif / Acteurs / Proposition de valeur / Plan d'actions / Résultats attendus), notée sur deux axes simples **valeur / complexité (1–5)**.

> **Ne remplace pas le scoring du waste-treatment :** Le scoring `Impact × Faisabilité − Prudence IA` du backlog de gaspillages (voir section précédente) reste en place — il est plus granulaire et propre au traitement des gaspillages. Le couple valeur/complexité (1–5) est réservé aux **recommandations de transformation transverses** (issues du diagnostic global, alimentant la roadmap et le deck), un usage plus léger et plus proche d'une matrice effort/valeur classique.

### Recommandations niveau équipe (v1.4)

Ce que BMAD IAP recommande à **une équipe précise** sur son fonctionnement, distinct du diagnostic transverse de mission — pas un nouveau palier d'entité, un simple champ `scope: mission | équipe` (+ `team_id`) ajouté à `Recommendation`, et une section optionnelle « Profil équipe » dans `recommendation-card.md` plutôt qu'un template dédié en plus des 14 déjà prévus.

| Axe | Exemples de recommandations propres à une équipe | Propriétaire |
|---|---|---|
| Delivery | Swimlanes RUN/BUILD séparées avec WIP propre ; Definition of Done infra (alerting, runbook, rollback testé) ; dépendances externes visibles sur le kanban avec SLA | `iap-platform-product-pm` (flux/DoD) + `iap-run-tma-specialist` (patterns RUN) |
| Gaspillage | Bus factor, canal de contournement du manager, ping-pong de tickets à l'interface de cette équipe, backlog fantôme hors outil officiel — une maille plus fine du même `waste-register`, pas un nouvel objet | `iap-waste-treatment-lead` |
| Efficacité | Rotation « bouclier » anti-interruption, allocation RUN explicite avec alerte de dérive, contrat écrit « ce qui justifie une interruption », plafond de toil déclenchant l'automation-readiness-checklist | `iap-run-tma-specialist` + `iap-metrics-sre-finops-lead` (handoff conjoint, pas un propriétaire unique) |
| Interaction | Mode d'interaction déclaré par dépendance (actuel/cible, §Modèles d'équipe), mini-catalogue de service propre à l'équipe, règle « une seule voix en comitologie », menu d'escalade explicite du manager | `iap-operating-model-architect`, alimenté par `iap-diagnostic-systemique` |

Position générale : **pas de nouvel agent** (pas de `iap-team-coach`) — chaque agent existant applique sa lecture à une maille plus fine, cohérent avec le refus déjà acté d'un 12ᵉ agent pour la comitologie. Extension du garde-fou anti-déplacement : toute fiche de recommandation niveau équipe porte un champ « Qui d'autre est affecté ? » (équipes voisines/management/comitologie) — un gain d'équipe peut être un optimum local qui déplace la file d'attente vers une équipe amont/aval.

### Mapping vers les workflows IAP

| Entité du moteur | Porté par |
|---|---|
| Mission, Trame | Créées par `iap-intake` |
| Interview, Answer, Verbatim | Capturées par `iap-diagnostic-systemique` et `iap-discovery-gaspillage`, une par persona |
| Synthesis, GlobalSynthesis | Output structuré de `iap-diagnostic-systemique`, remplace le markdown libre — alimente *assisté* (jamais automatique) le waste-register et, via `iap-waste-treatment-lead`, les RecommendationAxis |
| RecommendationAxis, Recommendation | Output transverse consommé par `iap-deck-builder` (slides recommandations/roadmap) |

## [Exécution] Agents BMAD

Contrat commun à chaque agent : synthèse, hypothèses, questions ouvertes, recommandations, risques, métriques, handoffs, livrable Markdown.

> **Clause d'allègement — décision de cadrage :** En mode brouillon/itération rapide, un agent peut ne produire que synthèse + hypothèses + questions + recommandations, et compléter risques/métriques/handoffs seulement au passage en version « prête à partager ».

### Mécanismes empruntés à OpenHub (v0.7 — framework multi-agents trouvé dans VSCode2/external/openhub)

VSCode2 invoque déjà en interne un framework multi-agents complet et documenté par ADR. Quatre de ses mécanismes se transposent directement à BMAD IAP, sans reprendre son code — seulement ses contrats.

#### Contrats de handoff formalisés (cf. ADR-009)

Chaque paire agent producteur→consommateur (ex. `iap-waste-treatment-lead` → `iap-deck-builder`) reçoit un contrat partagé : un bloc `## Retour vers <consommateur>` normalisé, produit en fin de mission d'un agent, contenant la sortie complète (jamais résumée) et des champs de métadonnées actionnables (statut, routing recommandé, verdict). Règle stricte héritée d'OpenHub : **le consommateur ne construit jamais un output à partir d'une entrée non structurée** — un bloc absent ou incomplet déclenche une demande explicite à l'agent producteur plutôt qu'une reconstruction approximative.

#### Checkpoint non-automatisable, quel que soit le mode (cf. ADR-006)

OpenHub propose 3 modes de workflow (manuel / semi-auto / auto) choisis une fois pour la session, mais un checkpoint reste **toujours manuel dans tous les modes** (chez OpenHub : la décision de merger du code). Transposé à BMAD IAP : quel que soit le mode d'autonomie choisi à l'intake, **la décision du gate IA/confidentialité reste toujours un checkpoint humain**, jamais automatisable — « absence de risque apparent » n'équivaut pas à « autorisé ».

#### Tags de confiance CONFIRMÉ / DÉDUIT / INCERTAIN (cf. wiki vivant OpenHub)

Chaque constat produit par un agent BMAD IAP (diagnostic, gaspillage, recommandation) porte désormais un tag de confiance explicite et sa source :

```
- Constat : ...
  — `CONFIRMÉ` · <agent> · <date> · <verbatim/document:référence>

- Constat déduit de plusieurs entretiens : ...
  — `DÉDUIT` · <agent> · <date> · <sources croisées>

- Hypothèse non encore validée par le client : ...
  — `INCERTAIN` · <agent> · <date>
```

Rend opérationnelles deux règles déjà présentes dans la doctrine (« expliciter ses hypothèses », « signaler les informations manquantes ») en leur donnant un format portable plutôt qu'une intention en prose.

#### Agent strictement lecture-seule (cf. agents auditor/onboarder OpenHub)

`iap-risk-reviewer` adopte la règle stricte des agents d'audit OpenHub : **« ne réalise jamais d'action hors lecture »**. Il challenge, verdict, recommande — mais ne modifie jamais directement un livrable produit par un autre agent. Une correction proposée par `iap-risk-reviewer` reste une recommandation à valider par l'agent propriétaire du fichier, jamais une réécriture directe.

### Les 11 agents

- **iap-strategy-lead** — Cadre la transformation, sponsors, scénarios, trajectoire. *« Quel problème business règle-t-on vraiment ? »*
- **iap-platform-product-pm** — Définit produits infra, personas, valeur, catalogue, roadmap. *« Est-ce un produit ou juste un composant technique ? »*
- **iap-operating-model-architect** — Conçoit rôles, gouvernance, financement, dépendances. *« Comment ça fonctionne réellement demain ? »*
- **iap-run-tma-specialist** — RUN, SLA/SLO, TMA, incidents récurrents, astreintes. *« Le modèle est-il opérable sans sacrifier le BUILD ? »*
- **iap-waste-treatment-lead** — Cartographie, score et backlog de traitement des gaspillages.
- **iap-platform-architect** — Relie cible produit et réalité technique. *« La cible produit est-elle techniquement cohérente ? »*
- **iap-ux-adoption-lead** — Parcours, onboarding, self-service, documentation, feedback. *« Pourquoi les équipes applicatives adopteraient-elles la plateforme ? »*
- **iap-metrics-sre-finops-lead** — Métriques de flux, fiabilité, coût, usage, satisfaction. *« Comment saura-t-on que ça marche ? »*
- **iap-ai-governance-lead** — Cas d'usage IA/agentic, garde-fous, supervision, audit. *« L'IA est-elle sûre, utile et gouvernable ? »*
- **iap-change-coach** — Middle management, compétences, RH, communautés. *« Comment évite-t-on une transformation cosmétique ? »*
- **iap-risk-reviewer** — Revue critique des livrables, angles morts. *« Qu'est-ce qui va échouer chez ce client ? »*

### Vue globale — graphe des handoffs (v1.1)

Simplifié en 3 chaînes séquentielles plutôt qu'un graphe complet (trop d'arêtes croisées pour rester lisible). Les agents en accent (`platform-product-pm`, `operating-model-architect`, `metrics-sre-finops-lead`) apparaissent sur plusieurs chaînes — même agent, pas une copie.

```
STRATÉGIE  : iap-strategy-lead → platform-product-pm → operating-model-architect → ai-governance-lead

PRODUIT    : platform-product-pm → ux-adoption-lead → metrics-sre-finops-lead → platform-architect

RUN/TMA    : run-tma-specialist → operating-model-architect → metrics-sre-finops-lead

GASPILLAGE : iap-waste-treatment-lead → operating-model-architect (capacité)
                                       & metrics-sre-finops-lead (métriques du backlog scoré)

--- (lecture seule, transverse) ---
iap-risk-reviewer — lecture seule, challenge tous les agents ci-dessus avant le deck final
iap-change-coach accompagne l'adoption humaine en parallèle de ux-adoption-lead
```

### Focus management (v1.4 — approfondit iap-change-coach)

Le management était traité en une ligne (« middle management, compétences, RH, communautés »). Trois clarifications, sans créer de nouvel agent ni de 9ᵉ famille de gaspillage :

> **Persona à nommer explicitement :** **« L'expert devenu manager malgré lui »** — parcours technique récompensé par une promotion managériale non choisie ou non préparée, sans retrait progressif du dossier technique. Accompagnement en 3 pistes : mentorat par un pair externe (un manager d'une autre organisation ayant vécu la même transition, plus crédible qu'un consultant qui n'a jamais tenu le rôle), pairing structuré sur des situations réelles (un comité, un arbitrage RUN) plutôt qu'une formation générique, formation ciblée sur un seul geste à la fois (animer une rétro sans redonner les réponses, déléguer et tenir une semaine). Mécanisme **Coach → Délégué en miroir** de celui de l'automatisation (§Traitement des gaspillages) : le consultant accompagne directement 2-3 situations réelles, bascule vers Délégué quand le manager anime seul le même rituel sans supervision.

**Gaspillage managérial — angle transverse, pas une famille de plus** : plutôt que d'ajouter une 9ᵉ famille à `waste-library.md` (recouperait déjà « Humain » et « Décisionnel »), un angle de lecture « vu depuis le manager » s'applique aux familles existantes. Patterns à nommer : réunions de statut organisées *par* le manager (pas seulement subies), reporting redondant recopié à chaque niveau hiérarchique, « reporting miroir » (un manager maintient un reporting détaillé parallèle au reporting simplifié transmis), micromanagement compensatoire — la cause racine est un déficit d'information fiable, pas un trait de personnalité ; la vraie remédiation redonne un signal de confiance (métriques de flux), pas plus de contrôle.

**Indicateurs de posture, jamais un score RH déguisé** : ratio temps réunion de statut / temps résolution d'obstacles, taux de décisions déléguées effectivement tenues, fréquence d'escalade déclenchée par l'équipe elle-même plutôt que par le manager. Tag de confiance applicable ici aussi (une amélioration rapportée par le manager seul reste `DÉDUIT`, confirmée par l'équipe en interview croisée peut monter en confiance) — ces indicateurs restent des signaux de coaching, jamais un livrable communicable à la hiérarchie du manager sans son accord.

> **Risque documenté — dépendance non maîtrisable aux structures RH :** Coacher une posture que les grilles de promotion/évaluation continuent de récompenser à l'inverse (contrôle, expertise technique visible) revient à ramer contre le système d'incitation — la même règle d'or que « l'IA amplifie le système existant » (§Doctrine) s'applique ici à une méthode humaine. Traitement : un `management-posture-risk` consigné sur le modèle d'`ai-risk-register.md`, avec une question de sortie de mission systématique côté sponsor (« qu'est-ce qui, dans vos grilles d'évaluation actuelles, récompense encore le comportement qu'on vient de décourager ? ») — sans obligation de la résoudre, avec obligation de la poser et de tracer la réponse.

## [Exécution] Workflows

Un seul est bloquant avant tout usage IA sur données client : `iap-ai-data-confidentiality-gate`.

**iap-intake** — *Démarrage de mission.* Qualifie le contexte client, positionne sur les deux échelles de maturité, choisit le chemin (diagnostic-first / pilot-first / adoption-first / operating-model-first / AI-gate-first). Outputs : `iap-context.md` · `client-scenario.md` · `recommended-path.md`

**iap-ai-data-confidentiality-gate** — *Bloquant avant tout usage IA.* Classifie les données, évalue IA client/LLM local/anonymisation, décide le mode d'exécution, définit garde-fous. Outputs — propriété canonique de ce workflow : `ai-data-confidentiality-assessment.md` · `llm-execution-mode-decision.md` · `human-oversight-model.md` · `ai-risk-register.md` (amendé, jamais réécrit, par les autres workflows IA)

**iap-diagnostic-systemique** — *Comprendre le système.* Structure, gouvernance, flux, dépendances, RUN/BUILD, posture management, relation infra/produits applicatifs.

**iap-discovery-gaspillage** — *Carte exploitable, pas une liste.* Preuves, causes racines, impact, options de traitement, owner, métriques par gaspillage détecté.

**iap-waste-treatment** — *Pont diagnostic → operating model → adoption.* Transforme les gaspillages en backlog priorisé (scoring, patterns, cadences de revue, garde-fou anti-déplacement).

**iap-product-definition** — *Discovery fusionnée — voir décision de cadrage.* Personas → capacités → distinction produit/service/composant → proposition de valeur → SLA/SLO → roadmap. Output optionnel — nouveau : `mvp-target-model.md` : core target model minimal pour expérimentation/témoignage rapide, distinct du product canvas complet.

**iap-operating-model** — *Opérer durablement la plateforme.* Rôles, gouvernance, financement par capacité, RUN/BUILD, TMA, cadences, décisions clés.
- *Format ADR pour les décisions structurantes — nouveau (v0.7, cf. OpenHub) :* Chaque décision de modèle-cible (ex. « financement par capacité plutôt que par projet ») devient un fichier séparé `decisions/NNN-titre.md` — Statut / Contexte / Décision / Conséquences (positives, négatives-compromis) / Alternatives rejetées — plutôt qu'un unique `operating-model.md` monolithique. Une décision peut être amendée plus tard en ajoutant une section « Amendement » en fin de fichier, sans réécrire l'historique.
- *Le modèle cible n'est pas décrété d'emblée — nouveau (v0.9) :* Le target operating model n'est pas figé au moment où il est rédigé : chaque décision structurante peut être testée par une **expérimentation pilote** (ex. une nouvelle cadence de priorisation essayée 6 semaines sur une seule équipe) avant généralisation. Les résultats de l'expérimentation — mesurés, pas supposés — amendent la décision ADR correspondante plutôt que de la valider a priori. C'est le même principe que le pilot-first déjà en doctrine (règle d'or #8), appliqué spécifiquement à l'operating model plutôt qu'au diagnostic initial.

**iap-operating-model → transformation-backlog.md** (nouveau, v0.9) — *Un artefact transverse, pas un output de plus parmi d'autres.* Reprend le pattern Epic → User Story déjà repéré dans le projet frère VSCode1 (`cadrage/epics-us.md`) pour transformer les décisions d'operating model, le backlog de gaspillages et la roadmap produit en actions exécutables. Chaque US porte un **mode d'exécution explicite** : `Coach` · `Délégué`. **Coach** : réalisée directement par le consultant en mission (ex. animer un atelier de priorisation, rédiger une fiche produit). **Délégué** : confiée à l'équipe client elle-même ou à un autre agent BMAD (ex. l'équipe RUN documente ses tickets récurrents, `iap-metrics-sre-finops-lead` instrumente un tableau de bord). Cette distinction évite l'anti-pattern où le consultant fait tout à la place du client — contraire à l'objectif d'autonomisation de l'operating model cible. Champs par US : Titre · Epic parent · critères d'acceptation · mode (Coach/Délégué) · owner · effort estimé · dépendances · lien vers la décision ADR ou le gaspillage d'origine.

**iap-agentic-opportunities** — *Chercher le gaspillage avant de chercher l'IA.* Consulte (ne régénère pas) `llm-execution-mode-decision.md` et `human-oversight-model.md` produits par le gate.

**iap-adoption-plan** — *Faire adopter la plateforme.* Personas, onboarding, documentation, communautés, feedback loops, migration.

**iap-scenario-playbook** — *Adapter la démarche au scénario client.*

**iap-deck-builder** — *Deck modulaire, 16 sections par défaut.* Slide 02 (« ce qui est différent d'une transfo agile classique ») récupère les tables problème→méthode du brainstorm source.
- *Exigence explicite — niveau professionnel (v1.3) :* Le deck exporté doit atteindre un niveau **professionnel**, pas seulement fonctionnel — en design (typographie, palette, composants visuels) **et** en UX (hiérarchie de lecture, navigabilité, clarté du message pour un sponsor qui le feuillette en 10 secondes). Un deck qui « passe » le garde-fou géométrique n'est pas encore un deck de ce niveau.
- *Visuels infra à construire :* Radar 5 piliers (couleur par pilier constante entre radar T0, T0/T1 superposé et légende — jamais deux mappings couleur différents dans le même deck) ; frise RUN/BUILD (rubans proportionnels RUN subi/maîtrisé/BUILD, pas un simple donut) ; matrice de dépendances inter-équipes (teinte d'intensité, pas un graphe nœud-lien dense — même principe de simplification que le graphe des handoffs d'agents ci-dessus) ; diagramme en couches concentriques pour la granularité produit/service/capacité/composant. Le scoring de gaspillage à 3 dimensions (Impact × Faisabilité − Prudence IA) perd sa 3ᵉ dimension en 2D — traiter la Prudence IA comme **recoloration d'alerte** (teinte gate) au-delà d'un seuil plutôt que comme un vrai 3ᵉ axe, ou préférer un classement en barres horizontales (plus lisible qu'un scatter au-delà d'une dizaine d'items, limite connue de la légende native PowerPoint).
- *Palette — décision non tranchée :* Réserver l'ambre strictement au gate IA/alertes (déjà son usage dans ce wiki) ; l'utiliser aussi pour les sections « gaspillage » risquerait de sur-connoter tout le pilier Assainir comme un problème de sécurité. Piste retenue à confirmer : une teinte neutre pour les sections gaspillage plutôt qu'une couleur dédiée, en réservant le teal à la vision produit.
- > **Garde-fous manquants — plus dangereux qu'un débordement de forme, car invisibles en relecture rapide :** **Texte débordant sa propre boîte** (le garde-fou géométrique actuel ne détecte que les formes hors cadre, pas un overflow interne à une zone de texte) et **cohérence d'échelle entre radars** (un même `scale_max`/graduation obligatoire entre radar T0 et T0/T1, sinon un delta visuel peut ne représenter aucun delta réel).
- *Discipline de rendu — brouillon vs final :* Rendu réel (LibreOffice/PowerPoint → PDF, vérification du nombre de pages) **non-bloquant en mode brouillon** (log un avertissement, n'arrête pas le workflow) mais **obligatoire avant remise en comité** (`mode: final`) — jamais de dégradation silencieuse si l'outil de rendu est indisponible sur le poste (échec visible, cohérent avec la règle OpenHub déjà actée). Un flag `mode: brouillon` réduit aussi le nombre de sections (6 slides clés plutôt que 16) sans dupliquer le générateur — même mécanique que la clause d'allègement des agents, transposée au deck.
- *Confidentialité de l'export lui-même :* Checklist de relecture explicite avant export (verbatims, captures d'écran, noms d'équipes) plutôt qu'un filtre automatique — les captures d'écran sont un angle mort spécifique (données visibles à l'œil, non détectables par un filtre texte). Verbatims cités dans le deck anonymisés par défaut (« un manager RUN » plutôt qu'un nom) ; bandeau de classification D0–D4 visible sur toute slide contenant des données D2+. En mode M0, cette relecture reste entièrement manuelle — pas de filtre automatique, cohérent avec le badge « Synthèse manuelle » déjà acté.
- *Template dédié — nice-to-have, pas un prérequis :* Un template PowerPoint OCTO propre à BMAD IAP coûterait cher à maintenir pour un seul module ; la mécanique déjà template-agnostique (accepte un template client uploadé ou construit un deck 16:9 depuis zéro) suffit avec un thème de couleurs/pictogrammes appliqué par-dessus, plutôt qu'un fichier figé séparé.
- > **Réflexion — retour d'expérience VSCode3, à nuancer plutôt qu'à renverser la décision ci-dessus (v1.8) :** la synthèse PPT de ce cadrage (`docs/cadrage-ppt/`) a d'abord été construite sur un canevas vierge avec un thème de couleurs recopié à la main — exactement le mode « sans template » validé ci-dessus — avant d'être reconstruite pour dessiner directement par-dessus le vrai template de marque OCTO (masters/layouts/thème natifs), sur le modèle déjà éprouvé côté VSCode1 (`ppt-toolkit.md`, `template-<nom>.md`). Le second résultat est net­tement supérieur à coût comparable : logo, pied de page et badge de pagination hérités gratuitement du template au lieu d'être redessinés à la main (et donc jamais tout à fait fidèles), couleurs lues depuis le thème réel plutôt que recopiées en dur, police de marque appliquée par défaut sur les placeholders. La distinction utile n'est donc pas « avec ou sans template » mais **« un template de marque fixe est-il disponible pour cette mission ? »** — si le client fournit un template (ou que le cabinet en a un, comme OCTO ici), le rouvrir et dessiner sur ses layouts natifs (pattern `template-<nom>.md` : identité, palette du thème, police par placeholder, layouts nommés, chrome conservé) plutôt que de le décorativement imiter ; si aucun template n'est fourni, le mode actuel (thème appliqué sur un deck construit depuis zéro) reste la bonne dégradation. Deux pièges opérationnels à documenter pour `iap-deck-builder` si ce pattern est repris : (1) supprimer les slides d'exemple d'un template nécessite de retirer la relation (`drop_rel`), pas seulement la référence dans la liste des slides, sous peine de collision de nom de fichier interne au `.pptx` généré ; (2) un deck géométriquement propre peut rester mal centré dans sa zone de contenu (vide vertical) — seul un rendu réel (PowerPoint/LibreOffice, cf. garde-fous ci-dessus) le révèle, jamais le seul contrôle géométrique.

## [Exécution] Routage des scénarios

| Scénario | Signaux | Chemin recommandé |
|---|---|---|
| Organisation sceptique | « Chez nous le produit ne marche pas » | Pilot-first + vocabulaire commun + preuves terrain |
| RUN massif | Tickets récurrents, BUILD sacrifié | Diagnostic RUN + discovery gaspillage + waste treatment |
| Gaspillages diffus | Irritants nombreux, peu de preuves consolidées | Discovery gaspillage + scoring + expérimentations courtes |
| TMA dominante | RUN externalisé, SLA contractuels | Workflow RUN/TMA + operating model |
| Plateforme peu adoptée | Shadow IT, faible usage | Product discovery + UX/adoption |
| Priorités politiques | Premier arrivé, plus bruyant | Flux entrants + gouvernance de priorisation |
| Pression IA sponsor | « Mettre de l'IA » sans cas d'usage | AI/Data Gate + discovery gaspillage |
| Données sensibles | Tickets, logs, coûts, PII | IA client ou LLM local + anonymisation |
| Maturité IA faible | Pas de plateforme IA gouvernée | Méthodo + données synthétiques |

## [Trajectoire] Ambition de l'outil (v0.8 — cadrage initial, affiné par 2 agents en cours)

BMAD IAP n'est pas figé sur un seul niveau d'ambition technique. Trois niveaux distincts, du plus simple au plus connecté :

| Niveau | Rôle de l'outil | Rôle du consultant | Corrélation roadmap |
|---|---|---|---|
| **A · Aide au coach** | Génère un livrable à la demande (template rempli, score calculé, deck assemblé) — aucune initiative propre | Pilote à 100 % : lit, décide, ajuste chaque livrable | Correspond à l'état actuel du cadrage (MVP0–MVP5) : agents invoqués un par un, sorties Markdown |
| **B · Assistant interactif** | Guide pas à pas, pose des questions de clarification, signale les incohérences entre livrables (ex. double scoring waste/recommandation) | Reste décisionnaire, mais délègue l'orchestration entre agents à l'outil | Palier intermédiaire non numéroté dans la roadmap actuelle — à situer entre MVP5 et MVP6 |
| **C · Companion connecté** | Vision « Transformation Companion » déjà actée : connecté en direct à ServiceNow/Jira/Confluence/Datadog/CMDB/FinOps, quasi autonome sur la collecte **et la préparation — jamais sur l'arbitrage** | Supervise ; arbitre les checkpoints non-automatisables **batchés par risque** (faible risque groupé, revue unitaire au franchissement de seuil, ADR-006) — son jugement reste le plafond de débit (voir §Agents) | = MVP6, toujours non engagé |

> **Pas nécessairement un spectre linéaire :** Monter de A à C n'est pas qu'une question de fonctionnalités en plus : le niveau C suppose un accès direct aux données de production du client (risque sécurité/confidentialité d'un tout autre ordre que A/B, voir le gate IA). Un cabinet peut très bien vouloir rester durablement au niveau A ou B par choix de gouvernance, pas seulement par contrainte technique transitoire.

> **Le checkpoint humain est le plafond de débit du Niveau C — à assumer, pas à masquer (v2.2) :** Le Niveau C promet « quasi autonome sur la collecte », mais le gate IA reste un **checkpoint humain non-automatisable** (ADR-006, §Agents) — donc le consultant reste le goulot sur *le jugement*, quel que soit le degré d'automatisation de la collecte. Conséquence à énoncer clairement pour ne pas survendre C comme une autonomie décisionnelle : ce que C accélère, c'est la **collecte et la préparation** (import continu ServiceNow/Jira/CMDB, pré-synthèse), jamais l'arbitrage. La piste de mise à l'échelle du checkpoint sans violer la règle existe déjà dans le cadrage — le **checkpoint conditionnel au risque** (ADR-006 : « toujours manuel mais pas systématique en mode semi-auto/auto » ; cadence plancher + convocation hors cycle, §Comitologie) : batcher les cas à faible risque, réserver la revue humaine unitaire aux franchissements de seuil (classification de données, désaccord, impact). À valider avant tout engagement Niveau C (owner `iap-ai-governance-lead`, §Points ouverts).

### Solution technique envisagée (v1.5 — Website en primaire, App en complément)

| Composant | Rôle | Ancrage |
|---|---|---|
| **Website** (web app) | Outil principal — moteur d'assessment, deck-builder, wiki de cadrage, grille de maturité, tableau de bord multi-engagements | Même pattern que les deux projets frères déjà éprouvés : VSCode1 (Express/Node.js) et VSCode2 (FastAPI/Jinja2/HTMX) — aucun build step lourd, déploiement simple, pas de friction de store |
| **App** (companion mobile, léger) | Capture terrain uniquement : enregistrement audio (Interview/CoachNote, voir ci-dessus), prise de note rapide hors connexion, synchronisation différée vers le Website | Répond au cas d'usage où le consultant n'a pas son ordinateur ouvert pendant l'entretien ou entre deux sites — pas une réplique du Website sur mobile, un outil de capture minimal qui se synchronise |

Le Website reste l'unique source de vérité (missions, engagements, livrables) ; l'App ne fait que déposer des captures brutes (audio, notes) qui remontent au même modèle de données (Interview/CoachNote) — pas deux systèmes à maintenir en parallèle. Correspond au Niveau B de l'ambition ci-dessus ; le Niveau A (aide au coach, état actuel du cadrage) n'a besoin d'aucun des deux, juste des agents invoqués à la demande.

## [Trajectoire] Utilisation simple par le coach (v1.1 — Niveau A, aide au coach)

Avant toute ambition Niveau B/C, voici littéralement ce qu'un consultant fait avec BMAD IAP aujourd'hui — un agent invoqué à la fois, aucune autonomie, un livrable Markdown à chaque étape.

| # | Ce que fait le coach | Ce qu'il obtient |
|---|---|---|
| 1 | Décrit le contexte client à `iap-intake` | Positionnement sur les 2 échelles de maturité + chemin recommandé (diagnostic-first, pilot-first…) |
| 2 | Prend le gabarit de guide d'entretien du scénario détecté dans `scenario-library.md` | Une Trame prête à l'emploi (Thèmes/Questions déjà écrits) |
| 3 | Mène les interviews une par une, note verbatims — importe si possible des exports ServiceNow/Jira | Une Interview par persona + ExternalEvidence en complément |
| 4 | Lance `iap-diagnostic-systemique` et `iap-discovery-gaspillage` | Synthesis par Thème + GlobalSynthesis + waste-register scoré |
| 5 | Lance `iap-product-definition` et `iap-operating-model` | Product canvas, mvp-target-model.md, décisions ADR, transformation-backlog.md (US Coach/Délégué) |
| 6 | Relit avec `iap-risk-reviewer` avant de finaliser | Une liste de challenges/incohérences à corriger — jamais une réécriture automatique |
| 7 | Lance `iap-deck-builder` | Le deck exécutif modulaire, prêt à présenter |

Pas d'orchestration automatique entre ces étapes, pas de tableau de bord : le coach garde la main d'un bout à l'autre, exactement comme décrit au Niveau A du spectre d'ambition ci-dessus. Rien n'empêche de sauter une étape (ex. mission flash : intake + gate IA + un pilote d'une semaine, cf. §Points ouverts) — la séquence complète n'est qu'un plafond, pas un plancher.

## [Trajectoire] KPIs

Trois familles de KPIs, à ne pas confondre : ceux de la **mission chez le client** (est-ce que la transformation marche ?), ceux de **l'usage du module BMAD IAP lui-même** (est-ce que la méthode est efficace pour le cabinet ?), et ceux de la **grille de maturité** (progression mesurée dans le temps).

### KPIs de mission (côté client)

| Catégorie | Indicateurs |
|---|---|
| Gaspillage traité | Tickets récurrents évités, ressources décommissionnées, interruptions d'experts réduites, capacité RUN récupérée |
| Adoption produit | Usage réel des capacités livrées, taux de self-service, taux de contribution retour, recommandation spontanée inter-équipes |
| Fiabilité & coût | MTTR, incidents par cause racine, coût par capacité, ressources orphelines |
| Gouvernance IA | Cas IA avec supervision/audit/critère d'arrêt documentés, incidents IA, mode d'exécution respecté (pas de bascule silencieuse) |
| Maturité | Delta de score par pilier de la grille (Excellence Technique, Agilité à l'Échelle, IA/Agentic) entre T0 et re-assessment |

### KPIs d'usage du module (côté cabinet)

| Catégorie | Indicateurs |
|---|---|
| Accélération | Temps pour produire un cadrage flash, un diagnostic, un deck sponsor |
| Réutilisation | Part des livrables issus de templates BMAD IAP plutôt que rédigés ad hoc |
| Cohérence | Écarts détectés par `iap-risk-reviewer` entre diagnostic, recommandations, roadmap et deck |
| Capitalisation | Scénarios, REX et anti-patterns ajoutés à `rex-library.md` / `scenario-library.md` par mission |
| Adoption interne | Nombre de consultants utilisant le module, nombre de missions traitées |

Le score de priorisation des gaspillages et le score valeur/complexité des recommandations (voir §Traitement des gaspillages et §Moteur d'assessment) restent des scores de *priorisation*, pas des KPIs de résultat — ne pas les confondre dans un tableau de bord de suivi de mission.

### Pourquoi et quoi mesurer précisément, par famille (brainstorm v2.1)

Les trois familles ci-dessus listent déjà des indicateurs, mais jamais la raison d'être de chaque famille ni une définition assez précise pour être mesurée sans ambiguïté — un KPI énoncé en label reste aussi flou qu'une recommandation en label (même défaut que celui déjà corrigé pour les slides, §slide-text-polish côté outillage PPT). Complété ci-dessous.

| Famille | Pourquoi (sans elle, quel angle mort) | Ce qu'on mesure précisément (une définition, pas une liste) |
|---|---|---|
| KPIs de mission | Sans eux, un cabinet peut livrer un deck exécutif dans les règles sans jamais savoir si le client va réellement mieux — le risque nommé en doctrine de « transformation cosmétique » (§Focus management) appliqué cette fois au résultat, pas à la posture managériale | Capacité RUN récupérée en **heures/mois** sur le processus ciblé (pas un pourcentage vague) ; delta de MTTR en **minutes**, mesuré sur le même périmètre d'incidents avant/après ; taux de self-service = part des demandes traitées sans ticket humain sur la capacité livrée |
| KPIs d'usage du module | Le module BMAD IAP est réutilisé mission après mission — sans mesure d'usage, impossible de distinguer une méthode qui s'améliore d'une méthode qui stagne, ni de justifier l'investissement de capitalisation (`rex-library.md`, MVP5) | Temps en **heures consultant** pour produire un cadrage flash (intake → deck sponsor) ; part des livrables provenant d'un template BMAD IAP sans réécriture substantielle (pas juste « utilisé un template ») |
| Grille de maturité | Sans mesure répétée dans le temps, la maturité reste une opinion de consultant plutôt qu'un delta objectivable — c'est ce qui rend la boucle de réévaluation (⟲) vérifiable plutôt que déclarative | Delta de score **par pilier** (pas un score agrégé unique qui masquerait un pilier qui recule pendant qu'un autre progresse), mesuré au même instrument (grille V3.2) à T0 et à chaque `iap-re-assessment` |

### Mise en place — owners, source des données, cadence (brainstorm v2.1)

Aucun de ces KPIs ne s'instrumente seul : ce qui manquait jusqu'ici n'est pas la liste des indicateurs mais qui les recueille, avec quoi, et à quel rythme.

| Famille | Owner | Source des données | Cadence |
|---|---|---|---|
| KPIs de mission | `iap-metrics-sre-finops-lead` (déjà owner des métriques de flux/fiabilité/coût, §Agents) | Import ServiceNow/Jira/CMDB si accès (`ExternalEvidence`), sinon déclaratif client — tagué `DÉDUIT`, jamais `CONFIRMÉ` sans preuve externe | En continu, lu à chaque étape de la trajectoire (②, ③, ⟲) — pas seulement à la Restitution |
| KPIs d'usage du module | Le consultant lui-même, au fil des missions — pas d'outillage dédié tant que le Niveau A/B (§Ambition de l'outil) reste la posture | Journal de mission + `rex-library.md` | Par mission ; consolidé en revue explicite à MVP5 (Industrialisation) |
| Grille de maturité | `iap-strategy-lead` (déjà owner de la revue de dépendance versionnée sur la grille, §Modèles de maturité) | Grille d'Assessment Agile V3.2, repassée en atelier ou en interview — jamais recalculée sans repasser l'instrument | T0 (Assessment flash, ①) puis à chaque boucle ⟲ (T+6-12 mois) |

> **Pas d'instrumentation automatique en MVP1 — cohérent avec l'ambition assumée :** tant que l'outil reste au Niveau A (aide au coach) ou B (assistant interactif), ces KPIs sont recueillis et rapportés à la main — aucun tableau de bord temps réel promis avant le Niveau C (Companion connecté, MVP6, non engagé, §Ambition de l'outil). Documenter cette limite évite l'anti-pattern « la QA cosmétique côté outillage » déjà nommé pour les livrables (§Qualité & test du module) transposé cette fois aux KPIs eux-mêmes : un KPI affiché sans préciser sa méthode de collecte crée une fausse confiance.

### Exemple chiffré — cas nominal RUN massif, avant/après (brainstorm v2.1)

> Reprend le cas nominal déjà posé en §Export markdown — recommandation d'implémentation agentic ou documentation (même fixture fictive « RUN massif », pas un client réel) pour montrer ce que ces KPIs donnent concrètement plutôt que d'inventer un second exemple.

| KPI | T0 (① Assessment flash) | T+6-12 mois (⟲ Boucle de réévaluation) | Tag de confiance |
|---|---|---|---|
| Pilier Agentic Readiness (grille V3.2) | [1] — process pas assez explicite | [2] — process explicite, rôles humains/agents définis | `CONFIRMÉ` (mesuré par la grille aux deux instants) |
| Tickets récurrents évités / mois (triage) | 0 | ≈ 15 | `DÉDUIT` — pas encore d'`ExternalEvidence` ServiceNow sur ce périmètre |
| Temps de triage moyen par ticket | 25 min | 12 min | `DÉDUIT` — déclaratif équipe, pas encore confirmé par export d'outil |
| Recommandation associée (export markdown) | Documentation-first (`runbook-triage-tickets.md`) | Agentic-implementation (même fichier amendé) | — |

Le point à retenir n'est pas l'ampleur des chiffres (fixture, pas une preuve) mais la **discipline de mesure** : même instrument aux deux instants, tag de confiance explicite plutôt qu'un chiffre présenté comme acquis, et un KPI de maturité qui déclenche directement le changement de recommandation plutôt que de rester un indicateur décoratif à côté.

### Plan de preuve des missions pilotes (v2.3)

> **Origine (v2.3) :** findings C3 + M4 de la revue produit du 2026-07-23 (`docs/reflexions/revue-produit-marche.md`) — le cadrage renvoyait 8+ hypothèses structurantes « aux premières missions pilotes » qu'une mission de 6-8 semaines ne peut pas toutes trancher (plusieurs exigent T+6-12 mois), et le dispositif de preuve portait une incitation inversée jamais nommée : si le delta T0→réévaluation est faible, ni le cabinet ni le sponsor n'ont intérêt à remesurer — biais de survivance intégré. Trois garde-fous, actés :

1. **Matrice hypothèse × mission** — 3 hypothèses maximum par pilote, chacune avec un **critère de réfutation écrit AVANT la mission**, au format ADR (celui que l'offre impose partout — appliqué ici à son propre plan de preuve). Hypothèse n°1 du pilote 1 : le **financement croisé** (§Vue d'ensemble, hypothèse porteuse).
2. **Réévaluation contractée à froid** — l'engagement de remesure T+6-12 mois (boucle ⟲) se contracte **dès l'intake**, pas en fin de mission : à chaud, personne n'a intérêt à remesurer si le delta s'annonce faible.
3. **Scénario « delta plat » pré-écrit** — avant la mission : que mesure-t-on exactement, que dit le deck de bilan si le delta est nul, et comment on distingue le delta de mission du bruit organisationnel sur 6-12 mois (réorgs, coupes budgétaires, départs). La narrative d'échec fait partie du dispositif de preuve, pas une éventualité qu'on improvisera le moment venu.

## [Trajectoire] Qualité & test du module (v1.3 — rattaché à MVP5, Industrialisation)

Pas le testing chez le client — comment on sait que ce que **produit BMAD IAP lui-même** (livrables Markdown, decks, scores) est réellement bon, pas seulement présent. Fil conducteur : séparer strictement une couche **structurelle automatisable** et une couche **qualitative irréductiblement humaine**, ne jamais confondre les deux sous un même badge.

### Ce qui se transpose du test logiciel, et ce qui ne se transpose pas

| Technique | Transposition à BMAD IAP |
|---|---|
| Tests de structure/complétude | Aucune section vide ou placeholder (« TODO ») dans un livrable — se transpose bien |
| Property-based testing | Propriétés toujours vraies : aucun tag CONFIRMÉ sans source citée, aucune Recommendation sans couple valeur/complexité |
| Contract testing | Un bloc « Retour vers <consommateur> » (ADR-009) est présent et complet avant que l'agent consommateur ne s'exécute |
| Tests de mutation | Injecter un livrable corrompu (score incohérent, tag mal posé) et vérifier qu'`iap-risk-reviewer` le détecte |
| Linting | « Linting doctrinal » — scanner les formulations-signal des anti-patterns déjà nommés |
| Non-régression exacte (input→output stable) | **Ne se transpose pas** — un LLM ne produit jamais deux fois le même texte |
| Tests de charge/performance | **Ne se transpose pas** — pas d'enjeu de scalabilité technique ici |
| Jugement de pertinence contextuelle | **Irréductiblement humain** — aucun test ne mesure si un diagnostic reflète vraiment CE client |

### Détecter le livrable structurellement complet mais qualitativement creux

Un `product-canvas-infra.md` avec les 6 champs remplis peut rester une généralité interchangeable d'un client à l'autre. Signaux proxy, jamais des preuves : ratio verbatim/assertion (un constat sans `verbatim_id` ni `ExternalEvidence.id` est suspect — déjà mesurable via le schéma de Synthesis, voir §Moteur d'assessment) ; couverture insuffisante comme témoin indirect (déjà cadré : `alerte_couverture`, rétrogradation DÉDUIT→INCERTAIN) ; détection de texte générique recyclé entre missions (nécessite un corpus anonymisé, en tension avec l'isolation multi-client — à traiter avec précaution). Le jugement qualitatif pur (proposition de valeur convaincante ? roadmap réaliste ?) reste le rôle assumé d'`iap-risk-reviewer` et du consultant — aucun mécanisme structurel ne le remplace.

### Missions fixtures rejouées de bout en bout

3 à 5 scénarios clients fictifs calqués sur le tableau de §Routage des scénarios (jamais de vraies données), rejoués intake→diagnostic→product-definition→waste-treatment→deck à chaque changement de version d'un agent ou d'un template — pas à chaque commit. Objectif : pas vérifier qu'un LLM produit le même texte, mais que les invariants structurels et la cohérence avec le scénario tiennent (le scénario « RUN massif » doit toujours produire un chemin orienté RUN). L'assertion finale reste une checklist de relecture humaine courte, jamais un simple diff vert/rouge. Risque à surveiller : des fixtures trop stables sur-adaptent les prompts des agents à ces scénarios précis (« teaching to the test » méthodologique) — à faire varier dans le temps.

> **Pré-check structurel avant iap-risk-reviewer :** Séparer une couche structurelle/mécanique (champs manquants, double-scoring waste/recommandation déjà repéré comme incohérence possible, tag DÉDUIT posé sous le seuil de couverture, décision ADR sans Alternatives rejetées) qui peut devenir un script ou sous-agent déterministe passé **avant** la revue humaine — et une couche jugement pur qui reste le rôle de l'agent. Règle non négociable : ce pré-check ne corrige jamais silencieusement, il liste des anomalies à trancher par l'agent producteur — même règle « lecture seule » que `iap-risk-reviewer` lui-même.

**9 checklists de readiness, deux couches par item** : chaque item tagué `[STRUCTUREL]` (case à cocher, automatisable) ou `[JUGEMENT]` (question ouverte, irréductiblement humaine) dès la rédaction — prépare une automatisation future sans l'exiger dès MVP1. `ai-confidentiality-readiness` est la plus structurelle des 8 par nature (classification D0-D4, mode d'exécution documentés) mais son checkpoint final reste, par doctrine, toujours un jugement humain (ADR-006). `no-waste-shift-checklist` est presque entièrement jugement par construction.

> **Anti-pattern : la QA cosmétique côté outillage :** Un badge « validé » qui ne précise pas explicitement ce qui a été vérifié (structurel seul, ou structurel + relecture humaine) crée une fausse confiance — même écart que « transformation cosmétique » déjà nommé côté client, reproduit cette fois côté outillage QA. Un badge `QA structurelle uniquement — relecture qualitative non faite` rend visible le niveau de contrôle réellement appliqué, sur le même principe que le badge « Synthèse manuelle — mode M0 ».

Rattachement roadmap : un sous-dossier `bmad-iap/qa/` (fixtures, pré-check structurel, script de rendu réel du deck-builder — voir §Workflows, `iap-deck-builder`) traité comme un investissement d'industrialisation de MVP5, pas une case cochée en fin de sprint. KPI de qualité candidat : taux de livrables ayant déclenché une correction lors de la revue `iap-risk-reviewer` avant présentation, à suivre dans le temps.

> **Décalage phasage ↔ doctrine qualité, corrigé (v2.2) :** Rattacher toute la QA à MVP5 alors que les premiers **engagements réels** arrivent dès MVP3 (isolation multi-client, §Roadmap) expose des clients avant le filet que cette section désigne pourtant comme le risque principal (livrable structurellement complet mais qualitativement creux). Correction, en s'appuyant sur la séparation structurel/jugement déjà cadrée : la couche **`[STRUCTUREL]`** du pré-check (champs manquants, double-scoring waste/recommandation, tag `DÉDUIT` sous seuil de couverture, décision ADR sans « Alternatives rejetées ») — peu coûteuse et automatisable — est **avancée à MVP3**, en même temps que les premiers diagnostics réels ; seules les **fixtures rejouées de bout en bout, le REX et l'industrialisation** restent à MVP5. Le filet minimal arrive donc avec la première exposition client, pas après (owner `iap-risk-reviewer`, §Points ouverts).

## [Trajectoire] Schéma de fonctionnement

Vue d'ensemble du mode opératoire : deux sources de collecte convergent vers un diagnostic structuré, le gate IA s'applique transversalement à toute étape qui invoque un LLM, et une boucle de réévaluation referme le cycle.

```
┌──────────────────────────────────────────────────────────────────────────────────────┐
│ Gate IA & confidentialité — checkpoint humain non-automatisable,                       │
│ transversal à toutes les étapes ci-dessous                                             │
└──────────────────────────────────────────────────────────────────────────────────────┘

  COLLECTE                        DIAGNOSTIC                    CONCEPTION                          RESTITUTION

  Interviews par persona   ┐                                ┌ Product definition
  (Trame/Theme/Question)   ├──▶ Synthesis par Thème +       ┤   (+ mvp-target-model.md)     ──▶  Deck exécutif
                            │    GlobalSynthesis             │                                    (RecommendationAxis
  Import de données outils ┘    + waste-register             └ Operating model                     + radar maturité)
  (ServiceNow/Jira/CMDB          (tags CONFIRMÉ/DÉDUIT/          + waste-treatment
   si accès → ExternalEvidence)  INCERTAIN)                      (décisions ADR · nourri par
                                                                   des expérimentations pilotes)

  ─────────────────────────────────────────────────────────────────────────────────
  iap-risk-reviewer — lecture seule, challenge les livrables ci-dessus
  (Product definition / Operating model → Deck exécutif)
  ─────────────────────────────────────────────────────────────────────────────────

  ⟲ Boucle de réévaluation : iap-re-assessment · boucle T+6–12 mois · alimente rex-library.md
     (repart du bandeau de revue et reboucle vers la Collecte)

  Chaque flèche traverse implicitement le bandeau Gate IA dès qu'une étape invoque un LLM sur des données client.
```

## [Trajectoire] Mise en œuvre du target operating model — brainstorm (v1.9)

**Le trou identifié :** le schéma ci-dessus s'arrête à RESTITUTION (le deck exécutif livré) puis saute directement à la boucle de réévaluation T+6–12 mois — rien ne décrit ce qui se passe **entre les deux**, c'est-à-dire la période où le client déploie réellement la cible operating model définie pendant la mission. Le cadrage a jusqu'ici entièrement porté sur le diagnostic et la conception, jamais sur le déploiement lui-même. Brainstorm ci-dessous, non tranché — à confronter aux premières missions pilotes.

> **Le trou dans le trou : la modalité de retour à T+6–12 mois (v2.2) :** Le brainstorm ci-dessous décrit ce que le client *déploie* entre Restitution et boucle ⟲, mais suppose implicitement que quelqu'un **repasse mesurer la grille** 6–12 mois plus tard — alors qu'une mission de conseil s'arrête normalement à la Restitution. Toute la narration « la recommandation s'améliore » (§Export markdown, §Cas nominal : documentation-first → agentic) **dépend d'une continuité de la relation** qui n'est nulle part décrite : ré-assessment inclus dès le contrat initial, option de suivi contractée séparément, ou relais interne côté client outillé par le module (mode Délégué). Sans cette modalité, la boucle ⟲ — keystone de la vérifiabilité (§KPIs, §Modèles de maturité) — reste un vœu, pas un dispositif. À trancher (owner `iap-strategy-lead`, §Points ouverts) — **la tarification et le packaging de ce retour restent hors périmètre de ce cadrage** ; seule la *mécanique de continuité* (qui repasse l'instrument, sous quel mandat) est à cadrer ici.

### Trajectoire en 3 temps + boucle, inspirée du gabarit OCTO lui-même

Le template `template-octo.pptx` porte déjà, dans ses slides d'exemple (« Notre approche », « Une approche contextualisée »), un pattern de trajectoire en 3 temps utilisé ailleurs dans le cabinet — signal fort qu'il ne s'agit pas d'inventer un vocabulaire de plus mais de brancher BMAD IAP sur une trame déjà partagée :

```
① ASSESSMENT FLASH          ② PREMIER DÉPLOIEMENT           ③ IMPLÉMENTATION ITÉRATIVE        ⟲ BOUCLE
  1–2 semaines                 4–5 semaines                    en continu, jusqu'à T+6–12 mois     T+6–12 mois

  = le Schéma de              1-2 équipes pilotes,             Généralisation progressive         iap-re-assessment
  fonctionnement déjà         mode Coach dominant               aux équipes restantes,              (déjà cadré)
  cadré ci-dessus             (US taguées Coach)                bascule Coach → Délégué            reboucle vers
  (Collecte→Diagnostic→                                         équipe par équipe                  la Collecte
  Conception→Restitution)     Piste agent IA (optionnelle,
                               si retenue) démarre ici :        Piste agent IA (si retenue) :
                               phases 0-2 de la démarche         phases 3-4 de la démarche
                               d'accompagnement (§Modèles        d'accompagnement — supervisé
                               d'équipe) — qualifier,             puis délégué, jamais forcé
                               cadrer, mandater
```

> **Bifurcation explicite — avec ou sans agents IA déployés :** le tronc commun (①→②→③→⟲) ne change pas de structure que la cible operating model inclue des agents IA ou non — c'est une variable de contenu à l'intérieur des phases ②/③, pas un chemin séparé. Si aucun agent n'est retenu, ②/③ restent un déploiement humain classique (Coach→Délégué sur le `transformation-backlog.md` déjà cadré, §Workflows). Si un agent est retenu, la démarche en 5 phases déjà cadrée (§Modèles d'équipe, v1.8 : Qualifier → Cadrer le process → Mandater → Piloter en assisté → Élargir) se greffe sur ②/③ plutôt que d'être une trajectoire séparée à maintenir — un seul calendrier, une piste de contenu en plus.

> **Ce que ça ne tranche pas :** durée exacte de ③ (dépend du nombre d'équipes et du scénario, §Routage des scénarios), et qui porte la trajectoire au global — probablement `iap-operating-model-architect` en propriétaire, avec `iap-change-coach` co-portant le volet humain (cohérent avec son rôle déjà cadré en ②/③ agent), mais non tranché à ce stade.

### Livrables PPT par étape — brainstorm (v1.9)

`iap-deck-builder` est aujourd'hui cadré comme **un seul** deck modulaire à 16 sections (§Workflows), produit une fois à la Restitution. La trajectoire ci-dessus implique plusieurs publics et plusieurs moments de décision — un seul deck monolithique ne les sert pas tous. Brainstorm : décliner le même moteur modulaire en **plusieurs instanciations**, chacune un sous-ensemble de sections pertinent pour son étape et son public — pas un générateur séparé par deck, cohérent avec le flag `mode: brouillon` déjà cadré qui allège déjà le nombre de sections.

| Étape | Livrable PPT | Audience | Contenu clé |
|---|---|---|---|
| ① Assessment flash | Deck exécutif de restitution (déjà cadré, §Schéma de fonctionnement) | Sponsor, comité de lancement | GlobalSynthesis, RecommendationAxis, radar de maturité T0 |
| ② Premier déploiement | **Deck de plan de déploiement** (nouveau, non cadré avant ce brainstorm) | Équipes pilotes + management direct | Cible operating model détaillée, backlog Coach/Délégué priorisé, mandat agent IA si la piste est retenue (§Modèles d'équipe) |
| ③ Implémentation itérative | **Deck de comité de pilotage**, périodique (nouveau) | Instance de comitologie (§Comitologie) | Avancement du backlog, delta de KPIs de mission, risques actifs (`ai-risk-register.md`, `deskilling-risk`) |
| ⟲ Boucle de réévaluation | **Deck de bilan / ré-évaluation** (nouveau) | Sponsor | Delta de maturité T0 → T+6–12 mois, REX consolidé (`rex-library.md`) |

> **Position provisoire :** pas de 4 générateurs séparés — un unique contrat de payload `iap-deck-builder`, avec un paramètre de **profil de sections** par type de deck (même mécanique que `mode: brouillon`/`mode: final` déjà cadré, juste un axe de variation de plus). Owner de la définition des 4 profils : `iap-deck-builder` en portage technique, `iap-strategy-lead` en validation du contenu attendu par profil — à confirmer sur les premières missions pilotes plutôt qu'à figer ici.

### Export markdown — recommandation d'implémentation agentic ou documentation, selon le contexte client (brainstorm v2.0)

**Le trou identifié :** la bifurcation « avec ou sans agents IA déployés » est déjà cadrée comme variable de contenu à l'intérieur de ②/③ (voir ci-dessus), et les 4 profils de deck PPT ci-dessus s'adressent au sponsor et aux pilotes — mais rien ne matérialise **la décision elle-même**, ni ce qui est concrètement livré à l'équipe d'implémentation quand la piste agent **n'est pas** retenue. Le « sans agent » reste un non-dit en creux plutôt qu'un livrable — alors que le préalable « le process doit être explicite avant l'agent, pas après » (§Modèles d'équipe, v1.8) implique déjà qu'un travail concret existe dans ce cas, juste jamais nommé comme livrable.

> **Position — pas un 12ᵉ agent, pas un template de plus pour la décision elle-même :** s'appuie sur deux workflows déjà cadrés plutôt que d'en créer un nouveau — `iap-agentic-opportunities` (« chercher le gaspillage avant l'IA », §Workflows) pour la branche agentic, `iap-adoption-plan` (« documentation, onboarding, feedback loops », §Workflows) pour la branche documentation. Le fichier produit **est** soit le plan agentic soit le runbook documentaire — le routage vit comme une courte section en tête du fichier (contexte client → branche choisie → pourquoi), pas comme un artefact de décision séparé.

**Pourquoi markdown et pas un 5ᵉ profil PPT :** audience différente — pas le sponsor ni le comité de pilotage, mais l'équipe qui exécute (tech lead, manager d'équipe, ou l'équipe cliente elle-même en mode Délégué). Cohérent avec le Niveau A déjà cadré (§Utilisation simple par le coach : « un livrable Markdown à chaque étape ») : versionnable, diffable, committable dans le dépôt de l'équipe cliente — un PPT ne l'est pas.

**Routage — aucun nouveau scoring, on réutilise ce qui existe déjà :**

| Signal (déjà cadré ailleurs) | Seuil observé | Branche |
|---|---|---|
| Pilier **Agentic Readiness** (grille V3.2, §Modèles de maturité) | [0]–[1] : process pas assez explicite/documenté/mesurable | **Documentation-first** |
| idem | [2]–[3] : rôles humains/agents définis, process mesurable | **Agentic-implementation** possible |
| Classification des données (Gate IA, §Doctrine) | D3–D4 sans LLM local qualifié | **Documentation-first** (ou mode M0, §Fonctionner sans IA externe) |
| idem | D0–D2, ou D3–D4 avec LLM local qualifié | **Agentic-implementation** possible |
| Score de traitement du gaspillage (Priorité = impact × faisabilité − prudence IA) | Négatif ou faible | **Documentation-first** |
| Signal `deskilling-risk` (§Modèles d'équipe) sur un processus voisin déjà agentifié | Risque déjà élevé | **Documentation-first**, prudence |

**Deux gabarits, pas trois :**

- **Chemin documentation** — `runbook-<processus>.md` : documente le processus stabilisé tel qu'il doit être exécuté aujourd'hui, à la main. Ce n'est pas un pis-aller : cohérent avec « le mode M0 n'est pas un mode dégradé au rabais » (§Fonctionner sans IA externe). Il satisfait de fait le préalable non négociable du process explicite — et devient la base mesurée de la prochaine ré-évaluation. Owner : `iap-adoption-plan`.
- **Chemin agentic** — `agentic-implementation-plan.md` : reprend directement la démarche en 5 phases déjà cadrée (§Modèles d'équipe v1.8 : Qualifier → Cadrer le process → Mandater → Piloter en assisté → Élargir), avec le **mandat écrit** (décide seul / escalade / owner des erreurs) comme section obligatoire dès la rédaction — pas une recommandation en l'air. Owner : `iap-agentic-opportunities`.

Communs aux deux : tag de confiance CONFIRMÉ/DÉDUIT/INCERTAIN (même doctrine que le reste des constats) et un bloc « Retour vers `iap-deck-builder` » (ADR-009) qui résume la recommandation en une ligne pour le deck PPT de l'étape courante — le markdown porte le détail actionnable, le PPT porte la synthèse, jamais l'inverse.

> **Pas un aller simple :** à chaque boucle de réévaluation (⟲, T+6–12 mois), le **même fichier est amendé, jamais dupliqué** (même discipline que `ai-risk-register.md`) — un client en documentation-first peut basculer en agentic-implementation si son Agentic Readiness progresse ; l'inverse reste possible aussi (un incident ou un `deskilling-risk` avéré peut faire revenir en documentation-first). Un historique en fin de fichier (append) tient lieu de mini-REX local et alimente `rex-library.md` au global.

**Anti-pattern à nommer explicitement :** une recommandation agentic générique, recyclée d'une mission à l'autre sans repasser par le scoring réel du client — même défaut que la « détection de texte générique recyclé entre missions » déjà nommée en §Qualité & test du module.

### Cas nominal — d'une intervention qui démarre à une recommandation qui s'améliore (exemple illustratif, v2.0)

> **Fixture, pas un REX client réel** — au même titre que les « 3 à 5 scénarios clients fictifs » du §Qualité & test du module : aucune donnée réelle, un scénario déjà routé (« RUN massif », §Comitologie) rejoué de bout en bout pour valider que le mécanisme de recommandation ci-dessus tient sur tout le cycle, de l'intake à la boucle de réévaluation.

| # | Étape | Ce qui se passe | Ce que ça produit |
|---|---|---|---|
| 1 | Intake | `iap-intake` qualifie un client fictif « scénario RUN massif » (§Comitologie) : beaucoup d'incidents récurrents sur une même chaîne de triage de tickets. Positionné M1 (IA interne basique) sur la maturité IA, chemin pilot-first. | `iap-context.md` · `client-scenario.md` · `recommended-path.md` |
| 2 | Diagnostic | Interviews + `iap-diagnostic-systemique` + `iap-discovery-gaspillage` identifient le triage manuel de tickets comme gaspillage RUN majeur — le même exemple déjà cité en §Modèles d'équipe (« agent IA membre d'une Stream-aligned team, ex. triage de tickets »). | Synthesis, waste-register scoré |
| 3 | Scoring | Impact élevé, mais la grille V3.2 mesure le pilier **Agentic Readiness à [1]** : le processus de triage n'est pas encore assez explicite/documenté pour être exécuté par un agent (§Modèles de maturité). | Score de gaspillage, niveau de pilier mesuré |
| 4 | **Export markdown (nouveau)** | `iap-agentic-opportunities` route sur **Documentation-first** (readiness [1] < seuil [2]) → produit `runbook-triage-tickets.md`, tag `DÉDUIT` (pas encore de preuve terrain), owner `iap-adoption-plan`. Pas de plan d'agent à ce stade. | `runbook-triage-tickets.md` |
| 5 | ② Premier déploiement | L'équipe pilote exécute le runbook à la main, mode Coach dominant, US taguées `Coach` sur `transformation-backlog.md`. Le deck de plan de déploiement (livrable PPT ② déjà cadré) résume en une ligne : « Triage documenté, agent non recommandé — readiness [1] ». | Deck de plan de déploiement, `transformation-backlog.md` |
| 6 | ③ Implémentation itérative | Le runbook s'affine à l'usage, le processus se stabilise ; bascule Coach → Délégué mesurée dans le temps (§Traitement des gaspillages). | Delta de KPIs, cadence de revue |
| 7 | ⟲ Boucle de réévaluation (T+6–12 mois) | `iap-re-assessment` remesure la grille : **Agentic Readiness passe à [2]** — le processus est désormais explicite, mesurable, et le runbook documente déjà les rôles humains. | Delta de maturité T0 → T+6-12 |
| 8 | **« J'améliore ce qui a été proposé »** | Le **même fichier** est ré-évalué, jamais dupliqué : la branche bascule de Documentation-first à Agentic-implementation. `iap-agentic-opportunities` amende `runbook-triage-tickets.md` (historique conservé en append) vers un contenu `agentic-implementation-plan.md` — mandat écrit désormais rédigeable puisque le préalable « process explicite » est rempli. La démarche en 5 phases (§Modèles d'équipe v1.8) démarre à la phase 0 (Qualifier) sur un candidat qui a cette fois un runbook mesuré à l'appui, pas un score à l'aveugle. | `agentic-implementation-plan.md` (même fichier amendé) |
| 9 | Deck de bilan | Le deck de bilan/ré-évaluation (livrable PPT ⟲ déjà cadré) montre le delta readiness [1]→[2] **et** la recommandation qui bascule de documentation à agentic — preuve visible que la boucle sert à quelque chose, pas un re-scoring administratif de plus. | Deck de bilan / ré-évaluation |

À rejouer avec les scénarios réellement routés (§Routage des scénarios) dès les premières missions pilotes — ce cas n'en préjuge pas l'issue, il vérifie seulement que le mécanisme (routage → gabarit → amendement au lieu de duplication) tient sur un cycle complet.

## [Trajectoire] Roadmap de mise en œuvre

### MVP 0 · Corpus — Décomposer le corpus dans knowledge/

Inclut la redaction du REX source, la doctrine renforcée, les invariants organisationnels et le nouveau modèle de maturité produit/plateforme.

### MVP 1 · Cœur — iap-intake, iap-product-definition, iap-deck-builder

Product-definition gagne l'output optionnel `mvp-target-model.md` ; le deck-builder récupère le matériel argumentaire du brainstorm.

### MVP 2 · Gate IA — iap-ai-data-confidentiality-gate + templates IA

### MVP 3 · Diagnostic & gaspillages — Diagnostic systémique, discovery gaspillage, waste treatment, operating model

Bénéficie de l'isolation multi-client dès les premiers engagements réels. Emporte aussi la couche **`[STRUCTUREL]`** du pré-check qualité (champs manquants, double-scoring waste/recommandation, tag `DÉDUIT` sous seuil de couverture, décision ADR sans « Alternatives rejetées ») — peu coûteuse, automatisable, et livrée ici pour que le filet minimal arrive **avec** la première exposition client, pas seulement à MVP5 (voir §Qualité & test du module).

### MVP 4 · Spécialisation — Scénario playbook, adoption plan, agentic opportunities, agents restants

Point de réouverture prévu pour la Product Discovery découplée.

### MVP 5 · Industrialisation — QA, REX, templates slides, connecteurs éventuels

La QA ici = **fixtures rejouées de bout en bout, REX consolidé, industrialisation** du pré-check et du rendu réel du deck-builder. La couche `[STRUCTUREL]` du pré-check a déjà été livrée à MVP3 (voir ci-dessus et §Qualité & test du module) — MVP5 ajoute la couche fixtures/jugement outillé, pas le filet minimal.

### MVP 6 · Connecteurs — non engagé — « Transformation Companion »

Vision d'un assistant connecté en direct à ServiceNow, Jira, Confluence, Datadog, CMDB, FinOps tooling. Changement d'échelle en termes de sécurité/confidentialité — acté comme horizon hors périmètre explicite plutôt que laissé en non-dit.

## [Trajectoire] Décisions de cadrage v0.5

Consolidation des arbitrages tranchés au fil de l'analyse du corpus (doc d'intégration + brainstorm source).

- **[Structure] Pas de fichier pivot** — Décomposition directe du corpus dans knowledge/, avec un nouveau fichier ai-confidentiality-doctrine.md.
- **[Ownership] Fichiers partagés entre workflows** — Un propriétaire canonique par fichier (gate IA pour les décisions de mode, agent AI Governance pour le risk register) ; les autres l'amendent.
- **[Confidentialité] Isolation multi-client** — Nouveau niveau engagements/<client-slug>/ — méthode générique et données client physiquement séparées.
- **[Langue] Français, vocabulaire technique conservé** — RUN/BUILD, TMA, FinOps, SLA/SLO, golden path non traduits. Pas de bilingue avant MVP5.
- **[Agents] Contrat allégé en mode brouillon** — Contrat complet conservé pour le livrable final ; version compacte autorisée en itération rapide.
- **[Confidentialité] Redaction du REX source** — Noms de clients et données chiffrées identifiantes de la source PDF anonymisés avant intégration à rex-library.md.
- **[Doctrine] Règle 3.2.1 renforcée** — Ajout de la citation source sur l'amplification du système existant par l'IA, comme argument de la règle.
- **[Scope] Product Discovery fusionnée** — Reste dans iap-product-definition pour MVP1 ; réouverture actée pour MVP4.
- **[Doctrine] Maturité produit/plateforme** — Nouvelle échelle indépendante du M0-M4 IA (état de l'art / marches / accompagnement).
- **[Méthode] Incrément pilote minimal** — mvp-target-model.md ajouté comme output optionnel de iap-product-definition.
- **[Scope] Transformation Companion hors périmètre** — Acté explicitement comme MVP 6 non engagé plutôt que laissé en non-dit.
- **[Contenu] Matériel argumentaire récupéré** — Tables problème→méthode du brainstorm rattachées au deck-builder, slide 02.
- **[Maturité] Grille VSCode1 importée telle quelle** — Le modèle 3 dimensions inventé en v0.5 est remplacé par la Grille d'Assessment Agile V3.2 (5 piliers, 17 objectifs, ~50 questions, 4 niveaux rédigés) — Excellence Technique et Agilité à l'Échelle pour la maturité produit/plateforme, IA/Agentic/Organisation Augmentée en lieu et place du M0-M4 générique.
- **[Assessment] Moteur d'assessment emprunté à VSCode2** — Structure Mission/Trame/Theme/Question + Interview/Verbatim par persona + Synthesis/GlobalSynthesis (5 catégories) + RecommendationAxis/Recommendation (valeur/complexité) reprise d'Interview-to-Deck pour structurer iap-intake, iap-diagnostic-systemique et iap-discovery-gaspillage.
- **[Agents] Contrats de handoff formalisés** — Chaque paire agent producteur→consommateur reçoit un bloc « Retour vers <consommateur> » normalisé avec champs actionnables — le consommateur ne construit jamais un output depuis une sortie non structurée (ADR-009 OpenHub).
- **[Gouvernance] Checkpoint gate IA non-automatisable** — Quel que soit le mode d'autonomie choisi à l'intake (manuel/semi-auto/auto), la décision du gate IA/confidentialité reste toujours un checkpoint humain (ADR-006 OpenHub).
- **[Agents] Tags de confiance CONFIRMÉ/DÉDUIT/INCERTAIN** — Chaque constat produit par un agent porte un tag de confiance et sa source, sur le modèle du wiki vivant OpenHub — rend opérationnelles les règles doctrinales existantes sur les hypothèses et informations manquantes.
- **[Agents] iap-risk-reviewer strictement lecture-seule** — Ne modifie jamais directement un livrable d'un autre agent — challenge, verdict, recommande uniquement (règle des agents auditor/onboarder OpenHub).
- **[Documentation] Décisions de modèle-cible au format ADR** — iap-operating-model produit un fichier de décision par choix structurant (Statut/Contexte/Décision/Conséquences/Alternatives rejetées), amendable sans réécrire l'historique, plutôt qu'un operating-model.md monolithique.
- **[Mission] Double mission Transformer/Assainir** — Le traitement des gaspillages devient un pilier de mission à part entière, pas une méthode annexe — la capacité récupérée finance la trajectoire produit. Affiné par l'agent de réflexion en cours.
- **[Positionnement] Spectre d'ambition A/B/C non tranché comme linéaire** — Aide au coach / assistant interactif / companion connecté ne sont pas nécessairement empilables — le niveau C change la nature du risque (accès direct aux données de prod). Cadrage initial, en cours d'affinage par 2 agents.
- **[Données] Import manuel de données outils (ExternalEvidence)** — Repli sans connecteur live : import CSV/export de ServiceNow/Jira/CMDB/FinOps, entité distincte de l'Interview (tag de confiance toujours CONFIRMÉ), mappée à la Trame via import-mapping.md par engagement.
- **[Méthode] Expérimentations pilotes nourrissent l'operating model** — Le target operating model n'est pas décrété a priori — des expérimentations mesurées (nouvelle cadence testée 6 semaines, etc.) amendent les décisions ADR correspondantes, sur le même principe que le pilot-first déjà en doctrine.
- **[Artefact] Backlog de transformation — US Coach/Délégué** — transformation-backlog.md reprend le pattern Epic/US de VSCode1, chaque US taguée Coach (réalisée par le consultant) ou Délégué (confiée au client ou à un autre agent) — évite que le consultant fasse tout à la place du client.
- **[Gate IA] Fonctionnement sans IA externe outillé** — Le mode M0 (pas d'IA) reste intégralement exécutable à la main : badge jamais silencieux, manual-synthesis-guide.md formalisant la méthode fréquence/cooccurrence de VSCode2, scoring de priorisation rappelé comme indépendant de l'IA.
- **[Gouvernance] Comitologie consolidée, pas un 12ᵉ agent** — Anti-patterns et pivots nommés explicitement, bibliothèque de patterns par scénario plutôt qu'une cible générique, checkpoint hybride (cadence plancher + convocation hors cycle si seuil de risque). Portage par une checklist (comitologie-coherence.md) et un template transverse (governance-instance-map.md), pas un agent dédié.
- **[Assessment] Synthesis par Thème — schéma de champs explicite** — Statut de cycle de vie séparé de la méthode de génération, couverture/répartition par persona pour détecter le faux consensus, divergences structurées avec verbatims liés et statut de résolution, tag de confiance posé par constat et rétrogradé automatiquement sous un seuil de couverture.
- **[Assessment] Pont Synthesis→waste-register assisté, jamais automatique** — Un constat négatif peut pré-remplir un brouillon dans le waste-register (registre brut des signaux), jamais directement dans le waste-treatment-backlog.md qualifié — le passage Qualifier→Quantifier→Cause racine reste obligatoire.
- **[Opérating model] Team Topologies comme grille de lecture de l'operating model** — La cible IAP est explicitement une Platform Team ; iap-operating-model-architect qualifie mode d'interaction actuel/cible (Collaboration ad hoc → X-as-a-Service). US Coach/Délégué relues comme Facilitating/Enabling → autonomie.
- **[Agents IA] Agents IA comme coéquipiers, pas seulement outils** — Un agent IA peut être membre d'une Stream-aligned team ou capacité exposée par la Platform Team. Nouveau mode d'interaction candidat « Supervision » (autonomie manuel/semi-auto/auto), à recouper avec le pilier Agentic Readiness de la grille de maturité.
- **[Gaspillage] Automatisation concrète — 2 nouveaux artefacts** — automation-readiness-checklist.md (avant de choisir le pattern) et automation-action-plan.md, 14ᵉ template, à deux branches Test/RUN — évite qu'« Automatiser » reste un mot dans une case du backlog.
- **[QA module] Structurel automatisable vs qualitatif humain, jamais confondu** — Pré-check structurel avant iap-risk-reviewer (lecture seule, ne corrige jamais), missions fixtures rejouées à chaque changement d'agent/template, checklists taguées [STRUCTUREL]/[JUGEMENT] — tout badge de conformité dit explicitement ce qu'il a vérifié.
- **[Deck PPT] Niveau professionnel exigé, garde-fous et discipline de rendu** — Rendu réel non-bloquant en brouillon / obligatoire en mode final ; garde-fous texte débordant + cohérence d'échelle inter-radars ; confidentialité de l'export par checklist de relecture humaine ; template dédié jugé nice-to-have.
- **[Assessment] GlobalSynthesis — 3 clarifications** — Aspirations autorise un contenu négatif ; non-duplication explicite avec le waste-register (couche exécutive vs backlog opérationnel) ; distribution des tags visible par catégorie. 6ᵉ catégorie en réserve, enrichissement de la Trame testé d'abord.
- **[Assessment] Recommandations niveau équipe — champ scope, pas de nouveau palier** — Recommendation gagne scope: mission|équipe + team_id. Patterns par axe (delivery/gaspillage/efficacité/interaction) distribués sur les agents existants, pas de iap-team-coach. Garde-fou anti-déplacement étendu aux équipes voisines.
- **[Management] Focus management sans 9ᵉ famille ni nouvel agent** — Persona "expert devenu manager malgré lui" nommé avec mécanisme Coach→Délégué miroir de l'automatisation ; angle de lecture transverse plutôt qu'une famille de gaspillage dédiée ; dépendance RH traitée comme management-posture-risk documenté.
- **[Données] Enregistrement audio — filet de sécurité, pas un contournement** — audio_backup_path repris de VSCode2 pour Interview + nouvelle entité CoachNote (réflexion libre hors trame). Classification D2+ par défaut, transcription soumise au même mode d'exécution IA que le reste — jamais un raccourci vers une IA externe.
- **[Outillage] Website en primaire, App en complément de capture** — Le Website (pattern VSCode1/VSCode2 déjà éprouvé) reste l'unique source de vérité ; une App mobile légère ne sert qu'à la capture terrain (audio, notes hors connexion) qui se synchronise vers le même modèle de données — pas deux systèmes parallèles.
- **[Confidentialité] Redaction du REX appliquée au cadrage lui-même** — Les noms de clients réels et la donnée démographique identifiante de la source brute ont été remplacés par des alias sectoriels génériques directement dans ce wiki (voir §Structure) ; le process de redaction reproductible pour les prochains REX reste un point ouvert distinct.
- **[Gouvernance] Dépendances externes versionnées et revues** — Grille VSCode1 (pin V3.2), contrats OpenHub ADR-006/ADR-009 et schéma de données Interview-to-Deck (VSCode2) sont désormais des dépendances explicitement pinnées, revues à chaque boucle `iap-re-assessment` et à chaque MVP gate, propriété de `iap-strategy-lead` (voir §Modèles de maturité).
- **[Rigueur] Points ouverts avec owner et échéance** — Chaque point ouvert du cadrage porte désormais un owner (agent/rôle) et une échéance cible (jalon MVP), sur le même principe de traçabilité que le format ADR déjà imposé aux décisions produit (voir §Points ouverts).
- **[Outillage] Résolution du schéma module.yaml** — Levé via l'installation BMAD locale (`_bmad/`) : `module.yaml` est un asset de définition de module fourni en gabarit par le module `bmb` (bmad-builder) déjà installé, distinct des `config.yaml` d'exécution par module. Scaffoldé via `bmb` en MVP1 plutôt que rédigé à la main (voir §Structure).
- **[Méthode] Gate de maturité DevOps — règle dure par défaut, dérogation ADR tracée** — Le pattern « Automatiser » est bloqué par défaut sous le niveau [0] du pilier Excellence Technique/Usine DevOps (grille VSCode1) ; toute dérogation doit être consignée comme décision ADR avec Alternatives rejetées obligatoires et contre-signature `iap-risk-reviewer` (voir §Traitement des gaspillages).

## [Trajectoire] Points ouverts

> **Discipline de suivi (v1.6) :** Le cadrage impose un format ADR strict (Statut/Contexte/Décision/Conséquences/Alternatives rejetées) aux décisions produit, mais n'appliquait jusqu'ici aucune rigueur équivalente à ses propres points ouverts — aucun n'avait d'owner ni d'échéance. Corrigé ci-dessous : chaque point porte désormais un owner (agent ou rôle responsable de le trancher) et une échéance cible (jalon MVP ou repère temporel). Deux points précédemment listés ici sont retirés parce que déjà tranchés ailleurs dans ce document et non par oubli de mise à jour : le schéma `module.yaml` (voir §Structure, "Résolution module.yaml") et la règle dure/souple du gate de maturité DevOps (voir §Traitement des gaspillages). Un troisième — les tags hétérogènes de GlobalSynthesis — était déjà fermé par la clarification v1.4 sur la distribution des tags (§Moteur d'assessment) mais était resté listé ici par erreur ; retiré pour la même raison.

| Point ouvert | Owner | Échéance cible |
|---|---|---|
| Convention de nommage des `<client-slug>` sous `engagements/` (slug libre vs registre contrôlé) | `iap-intake` | Avant MVP1 |
| Recompte faisant autorité de l'inventaire du module (templates/checklists réels vs snapshot v1.1, voir §Structure) — et un KPI de réinvestissement de la capacité récupérée (§Vue d'ensemble, hypothèse de financement croisé) | scaffolding `bmb` / `iap-strategy-lead` (inventaire) · `iap-metrics-sre-finops-lead` (KPI) | MVP1 (inventaire, au scaffolding `module.yaml`) · MVP3 (KPI) |
| Modalité de continuité de la boucle ⟲ à T+6–12 mois — qui repasse l'instrument, sous quel mandat (hors tarification/packaging, laissés hors périmètre du cadrage) | `iap-strategy-lead` | MVP4 |
| Mise à l'échelle du checkpoint humain au Niveau C sans violer ADR-006 (batch faible risque / revue unitaire au franchissement de seuil) | `iap-ai-governance-lead` | Avant tout engagement Niveau C (MVP6) |
| Confirmer à l'usage l'avancement à MVP3 de la couche `[STRUCTUREL]` du pré-check — désormais **câblé dans la Roadmap** (§Roadmap MVP3), fixtures/REX/industrialisation restant à MVP5 | `iap-risk-reviewer` | MVP3 (câblé) — validation sur mission pilote |
| Exigences de sécurité de l'App pour l'audio D2+ au repos (chiffrement, purge post-synchronisation, pas de backup cloud tiers) | `iap-ai-governance-lead` | Avant build de l'App |
| Process de redaction du REX formalisé en étape de workflow reproductible (au-delà du principe déjà acté) | `iap-ai-governance-lead` | Avant clôture MVP0 |
| Product Discovery découplée — nouveau workflow vs sous-étape enrichie | `iap-platform-product-pm` | MVP4 |
| Vecteur d'import de la grille — Excel vendored vs JSON/Markdown portable | `iap-strategy-lead` | MVP0 (avant intégration à `platform-maturity-model.md`) |
| Réutilisation du code vs du seul modèle de données (VSCode1/VSCode2) | `iap-platform-architect` | Revisite à MVP5 (industrialisation) |
| Granularité des contrats de handoff — par paire réelle vs format générique paramétré | `iap-risk-reviewer` | MVP1 |
| Versionnement d'une Synthesis dans le temps (brouillon vs re-synthèse déclenchée) | `iap-diagnostic-systemique` | MVP3 |
| Teinte des sections gaspillage dans le deck — neutre vs 3ᵉ couleur dédiée | `iap-deck-builder` | MVP1 |
| Gate dur ou soft sur la relecture qualitative avant livraison (attestation obligatoire vs jugement professionnel) | Direction de cabinet (choix de gouvernance, pas un agent) | MVP5 |
| `iap-change-coach` doit-il refuser une mission sans engagement RH minimal ? | `iap-change-coach` | MVP4 |
| Owner de la trajectoire de mise en œuvre du target operating model (①→②→③→⟲) et des 4 profils de deck associés — à confirmer sur missions pilotes | `iap-operating-model-architect` (proposé) | MVP4 (spécialisation) |
| Gabarits `runbook-<processus>.md` / `agentic-implementation-plan.md` (export markdown agentic-ou-documentation) — routage sur seuils déjà cadrés à valider sur mission pilote réelle, pas seulement sur le cas nominal fictif | `iap-agentic-opportunities` (technique) + `iap-ai-governance-lead` (validation doctrinale) | MVP4 (spécialisation) |
| Définitions précises + mécanique de mise en place des KPIs (owners, sources, cadence) — posées en brainstorm v2.1, jamais essayées sur une mission réelle ; le "pas d'instrumentation automatique avant le Niveau C" reste à confirmer dans la durée | `iap-metrics-sre-finops-lead` | MVP5 (Industrialisation) |
| Sort des tags CONFIRMÉ/DÉDUIT dans le deck sponsor (v2.3, finding M1) — recommandation : légende consolidée + argumentaire « pourquoi nos chiffres prudents valent plus », et accès aux exports outils posé comme condition d'engagement, pas comme repli | `iap-deck-builder` | MVP1 |
| Validation de domaine de la Grille V3.2 (v2.3, finding M2) — passe de contenu des ~50 questions vs spécificités infra (astreinte, obsolescence, TMA, CMDB) ; d'ici là, la qualifier « adaptée de », pas « éprouvée » en domaine infra | `iap-strategy-lead` | Avant la première mission pilote |
| Capitalisation REX outillée (v2.3, finding M3) — redaction reproductible en fin de chaque mission + objectif chiffré de REX/an ; le moat (rex-library/scenario-library) est en tension avec l'isolation multi-client — tension de produit, pas d'hygiène | `iap-ai-governance-lead` (redaction) · `iap-strategy-lead` (objectif) | MVP5 (Industrialisation) |
| Carte staffing junior / junior+revue / senior par étape du parcours coach + test d'apprenabilité réel (intake + diagnostic déroulés par un consultant qui n'a pas écrit le cadrage, chronométré) (v2.3, finding M5) | `iap-strategy-lead` + Direction de cabinet (staffing) | MVP5 — test d'apprenabilité dès qu'un consultant hors-auteur est disponible |
| Critère observable + dérogation ADR pour la règle d'or 3.2.1 « jamais l'IA sur un problème d'abord organisationnel » — adosser au pilier Agentic Readiness de la grille, même mécanique que le gate de maturité DevOps [0] (v2.3, finding m1) | `iap-ai-governance-lead` | MVP2 (Gate IA) |
| Scoper la mission flash au niveau du cas nominal : durée, livrables, ce qu'elle ne promet pas, sous-ensemble des 11 agents mobilisé (v2.3, finding m3 — le premier produit vendu était le moins spécifié du corpus) | `iap-intake` + `iap-strategy-lead` | MVP1 |
| Mécanisme anti-rubber-stamping du checkpoint humain — le plafond de débit est documenté (littérature HITL 2026) mais IAP n'a que le batching par risque, pas de mécanisme anti-fatigue (v2.3, research Q3) | `iap-ai-governance-lead` | Avant tout engagement Niveau C (MVP6) |
| Nom public de l'offre — collision « Infrastructure as a Product » avec Thoughtworks et Itential (v2.3, §Positionnement & achat) | Direction de cabinet (choix commercial, pas un agent) | Avant la première proposition commerciale |

---

*BMAD IAP · Wiki de cadrage consolidé (v0.4 doc d'intégration + brainstorm source + décisions v0.5 + v0.6 croisées VSCode1/VSCode2 + v0.7 mécanismes OpenHub + v0.8 mission double/ambition outil/KPIs/import données/schéma + v0.9 expérimentations/backlog US/mode sans IA externe + v1.0 comitologie + v1.1 Synthesis par Thème/schéma corrigé/vue globale/usage coach + v1.2 Team Topologies/agents IA coéquipiers + v1.3 automatisation/QA du module/qualité PPT professionnelle + v1.4 GlobalSynthesis/recommandations équipe/focus management + v1.5 enregistrement audio/solution technique App+Website + v1.6 dépendances externes versionnées/redaction/owners des points ouverts + v1.7 mise en œuvre des agents IA dans les équipes + v1.8 démarche d'accompagnement en 5 phases/réflexion production de livrables PPT + v1.9 trajectoire de mise en œuvre du target operating model/4 profils de livrables PPT + v2.0 export markdown de recommandation agentic-ou-documentation/cas nominal illustratif + v2.1 brainstorm KPIs pourquoi/quoi/mise en place/exemple chiffré) · document de travail, aucune donnée client réelle*
