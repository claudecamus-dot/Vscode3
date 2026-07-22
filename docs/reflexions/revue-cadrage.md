# Revue de fond — cadrage BMAD IAP

> Revue critique de pair du cadrage source [`docs/bmad-iap-cadrage.md`](../bmad-iap-cadrage.md),
> menée le **2026-07-22** sur la version **v2.1** (avant les corrections v2.2 qui en
> découlent — recomptage d'inventaire, requalification de la thèse de financement,
> cross-walk des échelles). Ce document est le **journal de la revue**, pas la doctrine :
> il ne fait pas autorité sur le cadrage, il le challenge.

## Verdict

Cadrage d'une **rigueur inhabituelle** : il se relit lui-même (anti-patterns nommés,
points marqués « non tranché », points ouverts avec owner + échéance, décisions au format
ADR). La doctrine confidentialité-first est un vrai différenciateur. Mais trois maux
structurels, pas des détails :

1. une **complexité qui contredit sa propre doctrine anti-gaspillage** (famille « Cognitif ») ;
2. la **thèse centrale du financement croisé posée comme acquise** alors qu'elle n'est jamais prouvée ;
3. une **keystone (la boucle ⟲) sans modèle commercial** qui la rende réelle.

Mûr sur la méthode, fragile sur la preuve et sur l'usage.

## Ce qui tient vraiment (à ne pas casser en corrigeant le reste)

- **Auto-conscience méthodologique** — nommer « le comité qui valide mais n'arbitre
  jamais », « la QA cosmétique côté outillage », « teaching to the test ». Le document
  anticipe ses propres échecs.
- **Discipline épistémique des tags** — CONFIRMÉ/DÉDUIT/INCERTAIN posé *par constat*,
  rétrogradation automatique DÉDUIT→INCERTAIN sous seuil de couverture (§Moteur
  d'assessment). Plus sérieux que 95 % des restitutions de conseil.
- **Cohérence du fil « expérimentée, pas décrétée »** — appliqué au même endroit à
  l'operating model, à la comitologie ET à l'adoption d'agents. Un invariant tenu bout en bout.
- **Retenue anti-sprawl** — refus répété d'un 12ᵉ agent / d'un template par sujet
  transverse. Bonne discipline (même si la surface totale reste énorme, cf. point 2).

## Points porteurs (par ordre d'enjeu)

### 1. La thèse du financement croisé est le pivot de tout, et c'est le joint le moins étayé

§Vue d'ensemble pose comme **acquis** que « la capacité récupérée finance la trajectoire
produit » et que les deux piliers « ne sont ni séquentiels ni optionnels ». Or rien ne
décrit le **mécanisme de conversion** : capacité RUN récupérée (heures/mois) →
réallocation budgétaire effective vers le produit. Le `garde-fou anti-déplacement` vérifie
qu'un gain n'est pas *faux*, mais **rien ne vérifie qu'un gain réel est réinvesti** dans la
cible produit plutôt qu'absorbé ailleurs (réduction d'effectif, autre incendie). C'est la
promesse de valeur centrale vendue au sponsor, et elle repose sur un saut de foi.
→ À requalifier d'« invariant acté » en **hypothèse à prouver**, avec un KPI de
réinvestissement, pas seulement de récupération. **[traité en v2.2 — callout ajouté à §Vue d'ensemble]**

### 2. Le cadrage embarque le gaspillage cognitif qu'il prétend traiter

11 agents, 11 workflows, ~14+ templates, ~9+ checklists, ~9 knowledge, une formule de
scoring, et **plusieurs échelles laddered partiellement recouvrantes** (M0–M4 IA · grille
V3.2 niveaux 0–3 · ambition A/B/C · Coach/Délégué · assisté/supervisé/délégué ·
manuel/semi-auto/auto · Team Topologies Collaboration/Supervision/X-as-a-Service). Le
lecteur doit tenir ~6 vocabulaires en tête — exactement la famille « Cognitif » (« trop
d'outils, procédures complexes, doc dispersée ») appliquée à la méthode elle-même. Le doc
traite la complexité localement (« pas de 12ᵉ agent ») mais ne prend jamais le recul
global : ce corpus est-il apprenable et utilisable au Niveau A par un vrai consultant sur
une vraie mission ?
→ Manque un **cross-walk canonique unique** des échelles. **[traité en v2.2 — nouvelle section §Cross-walk des échelles]**

### 3. La boucle ⟲ est la keystone — et elle n'a pas de modèle commercial

Toute la narration vedette de la v2.1 (« la recommandation s'améliore » :
documentation-first → agentic) repose sur remesurer la grille à T+6–12 mois. Deux trous :

- Une mission de conseil s'arrête généralement à la Restitution. **Qui paie et exécute la
  ré-évaluation** 6–12 mois plus tard ? L'owner est affecté (`iap-strategy-lead`) mais
  jamais le **modèle de relation/contrat** qui rend la boucle réelle. Sans ça, ⟲ est un
  vœu, pas un dispositif.
- Le doc est honnête (« fixture, pas un REX réel »), mais la feature phare a **zéro
  validation terrain** et dépend d'un modèle de récurrence commerciale nulle part décrit.

**[traité en v2.2 — callout « modalité de retour » à §Mise en œuvre ; la mécanique de
continuité est en point ouvert, la tarification/packaging reste hors périmètre décidé]**

### 4. Tension autonomie ↔ checkpoint humain au Niveau C

Presque chaque garde-fou route vers un humain (gate IA non-automatisable, `iap-risk-reviewer`
lecture seule, jugement « irréductiblement humain », checklists `[JUGEMENT]`). Sain contre
l'automatisation cosmétique — mais ça fait du **consultant senior l'unique goulot de
scaling**. Au Niveau C (« quasi autonome sur la collecte »), la promesse de débit et la
doctrine du checkpoint humain entrent en collision : le doc reconnaît le changement de
*nature de risque* mais n'adresse pas la question du **débit**. À trancher, pas à laisser
en « non linéaire ».
→ **[traité en v2.2 — callout à §Ambition ; puis intégré structurellement dans la table
Niveau C : outil « quasi autonome sur la collecte/préparation, jamais l'arbitrage »,
checkpoints batchés par risque (ADR-006). Mise à l'échelle en point ouvert]**

### 5. La vérifiabilité (« vérifiable plutôt que déclarative ») est encore aspirationnelle

L'argument est fait deux fois (grille de maturité, boucle ⟲). Or l'instrument qui la rend
vérifiable — la Grille V3.2 — est « importé tel quel » mais **son vecteur d'import est
encore un point ouvert** (Excel vendored vs JSON/Markdown, MVP0). Tant que l'instrument
n'est pas intégré, la vérifiabilité est promise, pas acquise. À ne pas présenter au présent.
*(Non traité — candidat restant.)*

### 6. Phasage QA vs exposition client réelle

La discipline QA/fixtures/pré-check structurel est rattachée à **MVP5**. Or l'isolation
multi-client sert « dès les premiers engagements réels » en **MVP3**. Donc MVP1–4 = vrais
clients **sans le filet** (fixtures rejouées, pré-check anti-livrable-creux) que la propre
doctrine qualité désigne comme le risque principal. Le filet arrive après la première
exposition. Contradiction phasage ↔ doctrine à assumer ou à réordonner.
→ **[traité en v2.2 — callout à §Qualité & test ; puis intégré structurellement : la couche
`[STRUCTUREL]` du pré-check est câblée dans la Roadmap MVP3, fixtures/REX/industrialisation
restant à MVP5]**

### 7. Le risque confidentialité concret n'est pas le modèle IA — c'est le PDF source et le téléphone

La doctrine IA-données est excellente. Mais les deux expositions **matérielles** restent en creux :

- La redaction est faite sur *ce* wiki, mais **le PDF brut avec les vrais noms reste la
  source de vérité des REX**, et le process de redaction reproductible est encore un point
  ouvert (owner `iap-ai-governance-lead`, avant clôture MVP0). C'est le risque live.
- L'App mobile capture de l'audio **D2+ hors connexion** puis synchronise. Un téléphone
  perdu avec de l'audio D2+ non synchronisé est une surface que « le choix du modèle » ne
  couvre pas. Le gate gouverne la *transcription*, pas l'audio brut au repos sur l'appareil.

**[audio D2+ au repos traité en v2.2 — callout à §Moteur d'assessment + exigences App en
point ouvert. Le volet PDF/redaction reste sur son point ouvert MVP0 préexistant.]**

## Incohérences concrètes (vérifiables)

- **Compteurs d'inventaire périmés.** La Vue globale (v1.1) affiche « 14 templates / 9
  checklists », mais `automation-action-plan.md` est déjà le « 14ᵉ template » et
  `automation-readiness-checklist.md` la « 9ᵉ checklist » — donc les additions
  postérieures (`comitologie-coherence.md` = 10ᵉ checklist ; `governance-instance-map.md`,
  `team-topology-map.md`, `manual-synthesis-guide.md`, `mvp-target-model.md`,
  `runbook-<processus>.md`, `agentic-implementation-plan.md`) débordent les compteurs.
  Figés en v1.1, jamais réconciliés. **[traité en v2.2 — note de cohérence + recompte en point ouvert]**
- **La formule de priorité invite la fausse précision que le doc combat ailleurs.**
  `Priorité = Impact × Faisabilité − Prudence IA` : trois sommes de termes non pondérés,
  sans échelle définie, dont un produit moins une somme (dimensionnellement bancal).
  Le présenter comme une formule contredit la vigilance du doc sur la « fausse confiance ».
  → Soit l'assumer comme support de discussion (et le montrer comme tel), soit définir
  échelles et pondérations. **[traité en v2.2 — callout « support ordinal, pas métrique » à §Scoring]**
- **Double scoring sciemment conservé puis mesuré comme incohérence.** Deux systèmes
  (`Impact×Faisabilité−Prudence` vs `valeur/complexité 1–5`), et « les écarts détectés
  entre double scoring » est listé comme KPI de cohérence du module. Le design ship une
  source d'incohérence puis mesure l'incohérence. Défendable, mais à nommer comme **dette
  assumée**, pas comme un simple garde-fou. *(Non traité — candidat restant.)*

## Packaging (transverse)

986 lignes avec l'archéologie de version en ligne (v0.5 « remplacé par… », raisonnements
barrés) : ça se lit comme un **journal de brainstorm accrété**, pas comme une référence
finie. Séparer **(a)** une couche référence canonique (doctrine actuelle, sans historique)
de **(b)** un journal de décisions (le §Décisions v0.5 en fait déjà la moitié) rendrait la
propagation vers le deck **vérifiable**. Gap connexe : pour un cadrage d'**offre** de
conseil, l'enveloppe commerciale (durée d'engagement, coût client, périmètre du « mission
flash » évoqué mais jamais scopé) est quasi absente.

## Suites données (v2.2, 2026-07-22)

Points de la revue traités dans la source, **sauf l'enveloppe commerciale** (durée
d'engagement, coût client, périmètre du « mission flash » — laissée hors périmètre sur
décision explicite) et deux candidats restants (porteur 5 vérifiabilité, double scoring).
Chaque traitement est un callout/note additif, non une réécriture — l'affirmation d'origine
est préservée quand elle sert de proposition de valeur. Pour les points 4 et 6, le callout
a ensuite été **intégré dans les sections structurelles** (table §Ambition, Roadmap) pour
que le doc ne se contredise pas.

| Point de la revue | Traitement dans `bmad-iap-cadrage.md` v2.2 |
|---|---|
| Thèse de financement croisé (porteur 1) | Callout « hypothèse à prouver » à §Vue d'ensemble, value prop préservée (deck inchangé, [`generate_deck.py`](../cadrage-ppt/generate_deck.py) ligne 415) ; KPI de réinvestissement en point ouvert |
| Complexité / 6 vocabulaires (porteur 2) | Nouvelle section §Cross-walk des échelles (3 natures, 1 gradient unifié) |
| Boucle ⟲ sans continuité (porteur 3) | Callout « modalité de retour à T+6–12 mois » à §Mise en œuvre — mécanique de continuité en point ouvert, tarification/packaging hors périmètre |
| Débit vs checkpoint humain au Niveau C (porteur 4) | Callout à §Ambition **+ table Niveau C mise à jour** : outil « quasi autonome sur collecte/préparation, jamais l'arbitrage », checkpoints batchés par risque (ADR-006) ; mise à l'échelle en point ouvert |
| Phasage QA-MVP5 vs client MVP3 (porteur 6) | Callout à §Qualité & test **+ Roadmap MVP3/MVP5 mise à jour** : couche `[STRUCTUREL]` du pré-check câblée à MVP3, fixtures/REX/industrialisation restant à MVP5 |
| Audio D2+ au repos sur mobile (porteur 7) | Callout à §Moteur d'assessment : chiffrement + purge post-sync + pas de backup cloud tiers ; exigences App en point ouvert |
| Formule de priorité pseudo-quantitative | Callout à §Scoring : score = support de discussion **ordinal** (tiers), pas une métrique calculée |
| Compteurs d'inventaire périmés | Note de cohérence à §Structure + recompte faisant autorité en point ouvert |

**Non traités :** l'enveloppe commerciale de l'offre (hors périmètre décidé) ; le porteur 5
(vérifiabilité tributaire de l'import de la grille V3.2) ; le double scoring waste vs
recommandation (à nommer « dette assumée »).
