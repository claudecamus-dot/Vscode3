# Product-brief — BMAD IAP (« Infra as a Product »)

> **Porte d'entrée produit (1 page).** Synthèse stable du cadrage de fond
> `docs/bmad-iap-cadrage.md` (v2.3, ~1100 lignes) et de la revue produit/marché
> `docs/reflexions/revue-produit-marche.md` — ces deux fichiers restent la **source de
> vérité** ; ce brief n'en est que le résumé d'accroche. **Honnêteté épistémique
> préservée** (finding critique C1 de la revue) : le *financement croisé* (« la capacité
> récupérée finance la trajectoire produit ») est une **promesse instrumentée à prouver
> sur les premières missions pilotes**, jamais un fait acquis — même statut au sponsor
> qu'en interne, pas de double discours.

**En une phrase** — pour une **persona** sponsor (DSI / direction infrastructure) et ses
équipes plateforme, le **pourquoi** est l'infra subie devenue intenable ; les **besoins &
points de douleur** sont la capacité humaine rare drainée par le gaspillage et l'écart
adoption/valeur d'une plateforme peu utilisée ; la **proposition de valeur** est la double
mission couplée *Transformer + Assainir*, dont le différenciateur est le couplage
produit + gaspillage + doctrine IA, pas l'étiquette.

## Persona — qui achète, qui l'opère, pour qui

- **Acheteur / sponsor** : **DSI ou direction infrastructure**, sur une ligne budgétaire
  *transformation* (pas le budget RUN). Langage de vente 2026 = « récupérer de la
  **capacité humaine rare** », pas « moderniser l'infra » (budgets DSI FR en « back to
  basics », modernisation infra en recul face à la cyber — baromètre Abraxio 12/2025).
- **Utilisateurs internes visés** : équipes plateforme/RUN, **SRE seniors drainés** par le
  répétitif, métiers qui contournent une plateforme peu adoptée.
- **Opérateur de l'offre** : consultant senior OCTO outillé par le module BMAD IAP
  (11 agents, 11 workflows, gate IA confidentialité). *Point ouvert assumé (M5) : offre
  aujourd'hui opérable surtout par son auteur — l'économie junior/senior reste à établir.*

## Pourquoi maintenant — les trois déclencheurs d'achat

1. **« L'infra subie n'est plus tenable »** — RUN subi, seniors drainés, gaspillage cloud
   ~29 % et en hausse (Flexera), plateforme contournée : le coût du statu quo monte.
2. **« Le modèle produit/plateforme est prouvé — mais pas la valeur »** — 80 % des grandes
   orgs avec platform teams en 2026, < 30 % de gains mesurables (Gartner) : l'écart
   adoption/valeur (80/30) est précisément ce que le pilier *Assainir* prétend combler.
3. **« L'IA rebat les cartes — l'organisation d'abord »** — > 40 % des projets agentic
   abandonnés d'ici 2027 (Gartner) : la prudence IAP est une **anticipation documentée**,
   pas une frilosité.

## Besoins & points de douleur adressés

- Récupérer la **capacité humaine rare** absorbée par le RUN subi et huit familles de
  gaspillage (flux, humain, RUN, financier, cognitif, décisionnel, environnemental, IA).
- Sortir de l'écart **adoption vs valeur** d'une plateforme techniquement bonne mais peu
  utilisée.
- Traiter la **fatigue de gouvernance IA** (87 % des DSI ont des agents en prod, 25 %
  seulement une visibilité temps réel) sans céder à la sur-promesse AIOps.
- Transformer un chiffre de gaspillage (souvent déjà produit par un outil FinOps) en
  **capacité produit gouvernée** — là où l'outillage seul s'arrête.

## Proposition de valeur — le couplage, pas l'étiquette

Une **double mission couplée, non séquentielle** :

| Pilier | Ce qu'il vise | Ce qu'il finance |
|---|---|---|
| **Transformer** | Cible produit/plateforme : utilisateurs, proposition de valeur, roadmap, engagements de qualité, gouvernance lisible | La vision moyen terme — ce que le sponsor achète |
| **Assainir** | Traitement **mesurable** du gaspillage (8 familles) | La capacité récupérée qui *doit* financer la trajectoire produit — **hypothèse instrumentée**, pas un audit de coûts isolé |

Le différenciateur n'est **pas l'étiquette** — « Infrastructure as a Product » est déjà
prise (Thoughtworks, Itential) — mais le **couplage produit + gaspillage + doctrine IA**,
angle mort commun des concurrents (Thoughtworks sans financement croisé, FinOps sans cible
produit, Big4 sur la gouvernance seule, AIOps sans transformation).

## Pourquoi nous plutôt qu'un achat partiel

| Alternative | Ce qui lui manque — la réponse IAP |
|---|---|
| **Ne rien faire** | Le coût du statu quo monte (déclencheur ①) — chiffré par l'Assessment flash |
| **FinOps outillé seul** | Le chiffre sans cible ni réallocation : IAP se positionne **en aval** |
| **Platform engineering pur** | La cible sans le financement : reproduit l'écart 80/30 |
| **AIOps / agentic** | Automatise le RUN sans transformation (> 40 % d'abandons prédits) |

> **Réponse au sponsor « je ne veux que la baisse de coûts »** : c'est l'anti-pattern
> documenté (« réduction de coûts sans vision ») — assumé, pas esquivé : une **mission
> flash d'entrée** puis la trajectoire, jamais l'assainissement seul en régime permanent.

## Risques produit (lecture Cagan) — honnêtes, non masqués

- **Valeur** : réelle si le pilier *Assainir* évite de redevenir un audit déconnecté (test
  de vérité = fermer l'écart 80/30).
- **Viabilité** : suspendue au **KPI de réinvestissement** — aucun standard publié (FinOps
  2026, DORA, SPACE) n'outille le lien « capacité récupérée → réinvestie » : angle mort de
  l'industrie, donc actif différenciant **si** IAP l'outille en premier, charge de preuve
  portée seul (chantier propriétaire assumé).
- **Faisabilité** : la Grille d'Assessment Agile V3.2 (référentiel déjà éprouvé, réutilisé
  tel quel — cf. §Modèles de maturité) est éprouvée comme *outillage*, pas encore validée
  comme *instrument* en domaine infra (M2).
- **Usabilité** : test d'apprenabilité (dérouler l'intake par un consultant qui n'a pas
  écrit le cadrage) restant à programmer (M5).

## Preuve & indicateurs

- KPI phare : **delta T0 → réévaluation** (T+6-12 mois), avec scénario « delta plat »
  pré-écrit et réévaluation **contractée à froid dès l'intake** (traite le biais de
  survivance, finding C3).
- Discipline de tags **CONFIRMÉ / DÉDUIT / INCERTAIN** en interne — l'honnêteté
  conditionnelle comme argument de vente. *Sa portée jusque dans le deck sponsor reste une
  recommandation à trancher (finding M1, cible MVP1), pas une pratique acquise.*

## Statut & points ouverts

Cadrage v2.3, **draft consolidé** — le « comment faire la mission » est au-dessus du
standard du marché ; les chantiers propriétaires restants (nom public de l'offre, KPI de
réinvestissement, plan de preuve hypothèse × mission, scoping de la mission flash) sont
tracés au §Points ouverts du cadrage de fond. Ce brief est révisé quand l'un d'eux est
tranché.
