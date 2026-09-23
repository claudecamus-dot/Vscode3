# Analyse des points encore ouverts — revues antérieures du cadrage (2026-09-23)

> Analyse, **pas correction** : rien n'est appliqué au cadrage ni au brief (édités en
> parallèle). Sources relues : `revue-cadrage.md` (22/07) et `revue-produit-marche.md`
> (23/07) **en entier, annexes A/B/C comprises** ; `bmad-iap-cadrage.md` par Grep + Read
> ciblé ; `product-brief.md` par Grep. Les numéros de ligne sont ceux du 2026-09-23 et
> **bougent** (le fichier est édité en parallèle) : l'extrait cité fait foi, pas le numéro.
> Les sections sont citées par leur NOM.

## 1. Statut de chaque finding

### Revue de cohérence (revue-cadrage.md, 22/07)

| Finding | Statut | Preuve (cadrage) |
|---|---|---|
| RC-1 Financement croisé posé comme acquis | **Partiel** | L38 « Hypothèse porteuse à prouver, pas un invariant acquis » — corrigé en statut ; le **KPI de réinvestissement** reste non défini (L1233 « KPI … MVP3 ») |
| RC-2 Complexité / 6 vocabulaires | Corrigé | Section « Cross-walk des échelles & vocabulaires » (L290) |
| RC-3 Boucle ⟲ sans modèle commercial | **Ouvert (bloquant)** | B7 L1161 « à la signature, le consultant n'a rien à faire signer » ; L1234 « hors tarification/packaging » |
| RC-4 Débit vs checkpoint humain (Niveau C) | Corrigé en structure, mise à l'échelle ouverte | L763 « batchés par risque … ADR-006 » ; L1235 et L1256 (anti-rubber-stamping) ouverts, échéance MVP6 |
| RC-5 Vérifiabilité aspirationnelle | **Ouvert** | L825 « vérifiable plutôt que déclarative » au présent ; vecteur d'import L1240 ouvert ; validation de domaine B4 ouverte |
| RC-6 Phasage QA MVP5 vs client MVP3 | Corrigé (validation terrain ouverte) | L1236 « désormais câblé dans la Roadmap » |
| RC-7 Audio D2+ au repos / PDF source | Partiel | L527 callout audio ; L1237 exigences App ouvertes ; redaction L1238 ouverte (circularité cassée L1138) |
| Compteurs d'inventaire périmés | **Ouvert** | L113-114 « baseline v1.1 — périmé » ; recompte renvoyé au scaffolding (L118) — or MVP0 non commencé (L12) |
| Formule de priorité pseudo-quantitative | **Partiel — contradiction nouvelle** | L376 « support ordinal » ; mais L1018 route sur « Négatif ou faible » — un seuil **signé** sur un score déclaré ordinal |
| Double scoring conservé puis mesuré | **Ouvert** | Jamais nommé « dette assumée » ; seulement cité en exemple L762 |
| Packaging : doc en journal accrété | Ouvert (non tranché) | L20 : historique en ligne d'un seul paragraphe ; aucune séparation référence/journal |
| Enveloppe commerciale (durée, coût, mission flash) | **Ouvert (bloquant)** | B3 L1157 « trois définitions concurrentes » ; B7 |

### Revue produit/marché (revue-produit-marche.md, 23/07) — synthèse + annexe A

| Finding | Statut | Preuve (cadrage) |
|---|---|---|
| C1 Double discours sponsor | Corrigé | L38 « le discours sponsor porte la même honnêteté … pas de double discours » ; brief L63 « hypothèse instrumentée » |
| C2 Zéro acheteur/concurrent | Corrigé | Section « Positionnement & achat » : « Qui achète » (L63), « Les 4 achats alternatifs » (L69) |
| C3 Incitations inversées du delta | Corrigé sur le papier | « Plan de preuve des missions pilotes » L861 réévaluation contractée ; scénario « delta plat » ; **dépend de B7** |
| M1 Tags dans le deck sponsor | Ouvert | L1250 recommandation posée, non tranchée ; L1166 « échus sans être bloquants » |
| M2 Grille V3.2 non validée en infra | **Partiel — incohérence** | L10 annonce « grille V3.2 plus dite éprouvée » mais L258 dit encore « un référentiel **déjà éprouvé** » ; B4 ouvert |
| M3 Moat vs isolation | Ouvert | L1252, MVP5 |
| M4 Pilotes surchargés | Corrigé sur le papier | L860 « 3 hypothèses maximum par pilote … critère de réfutation écrit AVANT » ; matrice elle-même non rédigée |
| M5 Économie de staffing | Ouvert | L1253, MVP5, porteur mixte |
| M6 Pas de contre-narrative IA | Corrigé | « Argumentaire de la prudence IA » (L88) + « Quick win IA légitime » (L101) |
| m1 Règle 3.2.1 non outillée | Ouvert (B5) — instance de RC-5 | L1159, L1254 |
| m2 Déclencheurs vivent dans le deck | Corrigé | « Les trois déclencheurs d'achat » L53 |
| m3 Mission flash non scopée | **Ouvert (B3)** | L1157 |
| Synthèse §2 nom de l'offre | Ouvert (B1) | L84 « point à trancher » ; L1257 |
| Synthèse §1 KPI de réinvestissement | Ouvert | = RC-1 |
| Annexe B Q3 anti-rubber-stamping | Ouvert | L1256, MVP6 |
| Annexe B Q2 gate aveugle au risque ROI | **Ouvert, jamais repris** | Aucune ligne du cadrage n'en fait un point ; le gate couvre confidentialité/supervision seulement |
| Annexe C souveraineté = 2ᵉ vague | Non repris | Information insuffisante pour dire si c'est un choix ou un oubli |

## 2. Options et recommandations (ouverts / partiels)

Légende : **H** = revient à la décision humaine (souvent commerciale) — cette analyse ne tranche pas.

**RC-3 / B7 — clause de réévaluation (H : Direction de cabinet).**
Options : (a) clause type « réévaluation T+6-12 mois, même instrument, forfait séparé » — coût : une décision de pricing ; on saura à la 1ʳᵉ signature si le client l'accepte ; risque : frein à la vente. (b) réévaluation incluse dans le prix de la mission flash — coût : marge ; risque : engagement non financé si la mission ne se prolonge pas. (c) réévaluation par le client lui-même avec la grille, revue à distance — coût faible ; risque : même instrument non garanti (RC-5).
Reco : (a), la seule qui rende B7 signable sans pré-décider un prix dans le cadrage. Texte pour « Points échus — réattribution humaine », ligne B7 : « Option retenue à arbitrer : clause de réévaluation distincte, forfaitisée hors cadrage ; le cadrage fixe seulement son contenu (même instrument, même périmètre, T+6-12 mois). »

**RC-5 / B5 / m1 — vérifiabilité au présent.**
Options : (a) réécrire au conditionnel les phrases au présent (L825) — coût : quelques lignes ; risque nul. (b) attendre B4 + vecteur d'import. Reco : (a) maintenant, (b) reste le vrai levier. Texte pour « KPIs de mission », ligne Grille : « … c'est ce qui **rendra** la boucle ⟲ vérifiable — une fois la grille validée en domaine infra (B4) et son vecteur d'import tranché. » B5 : critère proposé « pilier Agentic Readiness ≤ [1] ⇒ IA refusée par défaut, dérogation ADR contre-signée » (le choix du seuil est **H**).

**Formule de priorité / seuil signé.**
Options : (a) remplacer « Négatif ou faible » par « palier faible » (L1018) — coût : une cellule ; (b) définir échelles et pondérations — coût : chantier ; on saurait si le signe a un sens. Reco : (a), cohérente avec le callout de « Scoring ». Texte : « Score de traitement du gaspillage (palier ordinal, §Scoring) | Palier faible | Documentation-first ».

**Compteurs d'inventaire.** Options : (a) remplacer les compteurs par « cible, non recomptée (MVP0 non commencé) » ; (b) énumérer à la main. Reco : (a) — un compte d'artefacts inexistants n'a pas d'oracle. Texte pour « Vue globale du module » : « Templates / checklists : compte non figé — à lire au scaffolding `bmb` ».

**Double scoring.** Reco : nommer la dette. Texte pour « Scoring » : « Dette assumée : deux systèmes (Impact×Faisabilité−Prudence ; valeur/complexité 1–5) coexistent ; leurs écarts sont mesurés comme KPI de cohérence, pas éliminés. »

**M2 — « déjà éprouvé » (L258).** Reco : aligner L258 sur L10 et L1251. Texte pour « Modèles de maturité » : « … la Grille V3.2 — éprouvée comme outillage de passation (VSCode1), **adaptée de** pour le domaine infra tant que B4 n'est pas levé ».

**B3 / m3 — mission flash (H : périmètre vendu).** Options : (a) retenir « Assessment flash 1-2 semaines » ; (b) « intake + gate + pilote d'une semaine » ; (c) calque RUN Readiness Check 2-4 semaines (VScode6, `ILLUSTRATIF`). Reco : une seule définition, les deux autres renvoyant à elle ; durée **non mesurée** (aucune source) — l'écrire comme hypothèse.

**B1 nom de l'offre, B2 cohabitation VScode6 (H : Direction).** Pas de reco de fond ; reco de forme : poser une date calendaire (cf. « Limite assumée », L1145).

**M1 tags deck sponsor.** Reco : adopter la recommandation déjà écrite L1250 (légende consolidée). Décision **H** (iap-deck-builder n'existe pas).

**M3 moat, M5 staffing (H : Direction de cabinet).** Reco M5 : avancer le test d'apprenabilité avant la 1ʳᵉ mission (pas MVP5) — c'est le seul moyen de savoir si l'offre est vendable par un autre que l'auteur.

**Annexe B Q2 — risque ROI hors gate.** Reco : ajouter un point ouvert « le gate IA couvre confidentialité/supervision, pas le risque ROI (cause n°1 des abandons, Gartner 06/2025) » — owner **H**.

**Packaging (référence vs journal).** Reco : différer ; le coût (réécriture de ~1 270 lignes, compte `Read` du jour) dépasse le gain tant que le fichier est édité en parallèle.

## 3. Ce qui revient à l'humain
B1, B2, B7 (prix/contrat), périmètre de la mission flash, seuil de la 3.2.1, tags au deck sponsor, staffing, objectif REX/an, owner du risque ROI.
