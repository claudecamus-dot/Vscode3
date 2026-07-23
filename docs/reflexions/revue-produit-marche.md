# Revue produit + research + market-research — BMAD IAP (2026-07-23)

> Regard critique **externe** sur le projet global, demandé le 2026-07-23 — trois passes
> parallèles : revue produit adversariale (méthode Cynical Review, angle offre/achat),
> research domaine/technique (état de l'art 2025-2026, sourcé web), market research
> (concurrence + demande, marché conseil FR/EU). Complète — sans la répéter — la revue de
> COHÉRENCE INTERNE du 2026-07-22 (`revue-cadrage.md`, corrigée en v2.2 du cadrage).
> Les trois rapports bruts sont en annexes ; la synthèse croisée est la valeur ajoutée.
>
> Statut : **constats à arbitrer** — rien n'a été appliqué au cadrage ni au deck.

## Synthèse croisée — ce que les trois regards disent ensemble

### 1. Le joint de financement croisé est LA faiblesse centrale — les trois passes convergent dessus

- **Produit (C1, critique)** : la v2.2 tague « hypothèse à prouver » en interne mais décide
  de le présenter comme un fait au sponsor — la discipline des tags (le différenciateur
  épistémique de l'offre) s'arrête à la porte du pitch. Double discours institutionnalisé.
- **Research (Q4)** : aucun cadre publié (FinOps 2026, DORA, SPACE) n'outille le lien
  « capacité récupérée → réinvestie » ; le proxy le plus proche (toil ≤50 % de Google SRE)
  mesure du temps, pas de la valeur, et n'est repris par aucun standard. IAP porterait
  **seul** la charge de la preuve sur son affirmation la plus commercialement centrale.
- **Marché (faiblesse 2)** : c'est exactement le point qu'attaquent les concurrents
  outillés (FinOps SaaS, Itential et ses « -90 % OPEX ») avec du ROI chiffré immédiat,
  quand IAP promet un mécanisme de réallocation non instrumenté.

**À trancher** : KPI de réinvestissement en chantier propriétaire assumé (l'industrie n'a
rien à offrir — c'est un angle mort du marché, pas seulement du cadrage), ET alignement du
discours sponsor sur le statut réel (« hypothèse que la mission pilote instrumente, ce qui
suppose X de votre part ») — l'honnêteté conditionnelle est plus vendable que l'écart
interne/externe ne le sera le jour où un DSI lit le corpus.

### 2. « Infra as a product » n'est plus différenciant — le COUPLAGE l'est, mais personne ne le vend

- **Research (Q1)** : 80 % des grandes orgs auront des platform teams en 2026 (Gartner),
  « Platform as a Product » est mainstream ; l'écart réel du marché est adoption vs valeur
  mesurée (80 % vs <30 %) — précisément ce que le pilier Assainir prétend adresser.
- **Marché (§1, §4)** : **collision de nom quasi littérale** — Thoughtworks a un e-book
  « Infrastructure as a Product », Itential une plateforme du même nom. L'étiquette est
  prise ; le contenu (produit + gaspillage + doctrine IA couplés) est, lui, dans l'angle
  mort commun de Thoughtworks (pas de financement croisé), du FinOps (pas de cible
  produit) et de Capgemini (pas de doctrine IA).
- **Produit (C2, critique)** : 1035 lignes sans acheteur qualifié, sans déclencheur d'achat,
  sans concurrent nommé — chaque état du routage a un concurrent naturel moins cher
  (RUN massif → AIOps ; surdimensionnement → FinOps ; plateforme peu adoptée → platform
  engineering) et l'offre n'explique jamais pourquoi la double mission bat chacun de ces
  achats partiels. L'anti-pattern déclaré (« réduction de coûts sans vision ») est
  exactement ce que le marché demande.

**À trancher** : une page « qui achète, contre quoi, pourquoi nous » dans le cadrage (les
3-4 achats concurrents + la réponse au sponsor qui ne veut que la baisse de coûts), et la
décision d'assumer le couplage comme LE différenciateur — pas l'étiquette, pas la prudence.

### 3. La prudence IA est validée par le marché… et commercialement désarmée

- **Research (Q2-Q3)** : la ligne de crête IAP (collecte déléguable, arbitrage jamais
  automatisé, checkpoint non-automatisable) est littéralement confirmée par l'état de
  l'art (40 % d'abandon des projets agentic prédit d'ici 2027, écart démo/prod documenté
  sur le triage, plafond de débit HITL et rubber-stamping nommés dans la littérature,
  convergence EU AI Act/NIST/ISO sur la supervision humaine).
- **Marché (force 1, faiblesse 3)** : le timing de la désillusion (Gartner + Forrester
  2026 : « la discipline compte plus que l'expérimentation ») transforme la prudence en
  anticipation documentée, plus en posture frileuse. MAIS le terrain « gouvernance IA »
  est déjà occupé par les Big4 et ServiceNow (AI Control Tower) — un cabinet intermédiaire
  ne gagne pas en étant « le plus prudent », risque me-too.
- **Produit (M6, majeur)** : composition toxique de trois choix sains — règle 3.2.1 +
  diagnostic qui trouve toujours de l'organisationnel + boucle ⟲ sans véhicule commercial
  = le sponsor venu pour l'IA repart avec un runbook et une promesse d'IA dans un avenant
  jamais cadré. La contre-narrative (« pourquoi notre déception structurée vaut plus que
  leur sur-promesse ») n'est écrite nulle part.

**À trancher** : écrire l'argumentaire de vente de la prudence (avec les chiffres Gartner/
Forrester ci-dessus, désormais sourcés) + packager un « quick win IA légitime » détectable
dès l'intake (cas D0/D1 à readiness [2]+) pour les sponsors sous pression IA.

### 4. Le dispositif de preuve a des incitations inversées et aucun standard sur lequel s'appuyer

- **Produit (C3, critique)** : si le delta T0→réévaluation est faible, personne n'a intérêt
  à remesurer (ni le cabinet ni le sponsor) — biais de survivance intégré au dispositif de
  preuve ; aucun scénario « delta plat » n'est écrit ; l'attribution du delta au milieu du
  bruit organisationnel (réorgs, coupes, départs sur 6-12 mois) n'est pas traitée.
- **Produit (M4)** : 8+ hypothèses structurantes renvoyées « aux premières missions
  pilotes » qu'une mission de 6-8 semaines ne peut pas trancher — plusieurs exigent
  T+6-12 mois, au-delà de la mission.
- **Research (Q4)** : pas de standard externe à invoquer pour la remesure — la charge est
  propriétaire.

**À trancher** : matrice hypothèse × mission (3 hypothèses max par pilote, critère de
réfutation écrit AVANT la mission — le format ADR que l'offre impose partout, appliqué à
son propre plan de preuve) + engagement de réévaluation contracté à froid dès l'intake +
scénario « delta plat » pré-écrit.

### 5. Timing marché 2026 : le narratif d'entrée doit être la douleur RUN, pas la transformation ni l'IA

- **Marché (§3)** : budgets DSI FR 2026 « back to basics » — la modernisation infra
  RECULE face à la cyber ; mais l'IA capte le budget sans plafond (87 % des DSI ont des
  agents en prod, seuls 25 % ont une visibilité temps réel — la fatigue de gouvernance
  est un point de douleur concret) ; pénurie SRE/cloud persistante.
- **Recommandation convergente des trois passes** : entrer par le gaspillage RUN mesuré
  (« récupérer de la capacité humaine rare »), positionner IAP en AVAL des outils FinOps/
  AIOps (« vous avez le chiffre, nous avons la méthode pour le transformer en capacité
  produit gouvernée »), amener l'IA en garde-fou et non en promesse — ce qui est déjà
  la structure narrative du deck (IA en avant-dernier chapitre) : le deck a raison,
  le cadrage doit le rattraper (finding produit m2 : les « 3 déclencheurs » vivent dans
  le deck sans section source dans le cadrage).

### Findings produit restants (non croisés, à traiter en propre)

- **M1** : le sort des tags CONFIRMÉ/DÉDUIT dans le deck sponsor n'est réglé nulle part —
  or les chiffres de bilan seront structurellement DÉDUIT (accès outils = exception).
- **M2** : la Grille V3.2 est « éprouvée » comme outillage, pas comme instrument valide en
  domaine infra (transfert agile→infra jamais validé ; c'est l'unique instrument de toute
  la vérifiabilité).
- **M3** : le seul moat accumulable (REX/scénarios) est affamé par la doctrine d'isolation
  multi-client — tension jamais traitée comme problème de produit.
- **M5** : aucune économie de staffing (junior/senior) — offre opérable par son auteur
  seulement ; le test d'apprenabilité (faire dérouler l'intake par un consultant qui n'a
  pas écrit le cadrage) n'est jamais programmé.
- **m1** : la règle d'or 3.2.1 (« jamais l'IA sur un problème organisationnel ») est la
  seule règle d'or non-outillée — ni critère observable, ni dérogation ADR.
- **m3** : la mission flash (premier produit vendu) est le moins spécifié de tout le
  corpus, quand le MVP6 à 3 ans a sa vision détaillée.

---

## Annexe A — Revue produit adversariale (rapport brut)

*(Sous-agent modèle de session, lecture intégrale du cadrage v2.2 + revue-cadrage.md +
wiki business ; consigne : ne pas répéter la revue de cohérence du 22/07.)*

### CRITIQUE

**C1. Le cadrage institutionnalise un double discours : vendre au sponsor ce qu'on tague en interne « hypothèse non validée »** — Preuve : §Vue d'ensemble, callout v2.2 : « La proposition de valeur peut rester présentée comme telle au sponsor (elle l'est dans le deck de restitution) ; c'est en interne qu'elle doit porter ce statut d'hypothèse. » L'offre a bâti sa crédibilité sur la discipline CONFIRMÉ/DÉDUIT/INCERTAIN ; appliquée à son propre argumentaire, elle classerait la promesse centrale en INCERTAIN. Le jour où un sponsor découvre l'écart, c'est le différenciateur épistémique entier qui devient une posture marketing. À trancher : assumer la promesse avec sa condition, ou porter la même honnêteté dans le deck sponsor.

**C2. 1035 lignes, zéro acheteur, zéro déclencheur, zéro concurrent** — « Sponsor » n'apparaît que comme persona interviewée, jamais comme acheteur qualifié (qui signe, quelle ligne budgétaire, déclenché par quoi). Aucune mention des alternatives (ne rien faire, FinOps, platform engineering pur, AIOps). Chaque état du routage a un concurrent naturel moins cher ; l'anti-pattern déclaré est exactement ce que le marché demande ; le sponsor qui ne veut que l'assainissement n'a aucune réponse. À trancher : une page « qui achète, contre quoi, pourquoi nous ».

**C3. Le KPI phare (delta T0→réévaluation) crée un désalignement d'incitations que personne n'a nommé** — (1) Attribution : rien ne distingue le delta de mission du bruit organisationnel sur 6-12 mois. (2) Incitation inversée : si les gains sont faibles, ni le cabinet ni le sponsor n'ont intérêt à remesurer — biais de survivance intégré. (3) Aucune narrative d'échec commercial (que dit-on quand le delta est nul ?). À trancher : scénario « delta plat » pré-écrit + réévaluation contractée à froid dès l'intake.

### MAJEUR

**M1. La discipline des tags sabotera la vitrine commerciale — ou sera silencieusement abandonnée** — Les résultats phares du cas chiffré sont tagués DÉDUIT ; en mission réelle l'accès aux exports outils est l'exception. Soit le deck de bilan affiche DÉDUIT sur ses chiffres de succès, soit les tags disparaissent du deck sponsor — et aucune règle du iap-deck-builder ne tranche. Recommandation : trancher la présence des tags dans le deck sponsor (légende consolidée + argumentaire « pourquoi nos chiffres prudents valent plus ») et faire de l'accès outils une condition d'engagement, pas un repli.

**M2. La Grille V3.2, « référentiel déjà éprouvé » — éprouvé pour mesurer de l'agilité, pas de l'infra** — « Éprouvé » porte sur l'outillage de passation, pas sur la validité de l'instrument en domaine infra (astreintes, obsolescence, TMA, CMDB). C'est l'unique instrument de toute la vérifiabilité de l'offre. À trancher : passe de validation de contenu des ~50 questions avant la première mission, sinon requalifier en « grille adaptée de ».

**M3. Le moat de l'offre est en guerre structurelle avec son différenciateur** — Le seul actif qui s'accumule (rex-library, scenario-library) est freiné par la doctrine confidentialité-first (tension notée en passant au §Qualité & test, jamais traitée comme problème de produit). Le reste est emprunté ou public. À trancher : capitalisation systématique outillée (redaction reproductible en fin de mission, objectif chiffré de REX/an) ou assumer que la défendabilité est ailleurs.

**M4. Les « premières missions pilotes » sont un véhicule de validation surchargé à l'impossible** — 8+ hypothèses structurantes renvoyées aux pilotes, dont plusieurs exigent T+6-12 mois. Sans plan de validation priorisé, la sortie sera « tout a plus ou moins marché » — zéro hypothèse tranchée. Recommandation : matrice hypothèse × mission, 3 hypothèses max par pilote, critère de réfutation écrit avant.

**M5. L'économie de staffing n'existe pas : une offre opérable uniquement par son auteur** — Chaque garde-fou route vers du jugement senior ; rien ne distingue ce qu'un junior peut faire seul. Le KPI « nombre de consultants utilisant le module » restera à 1. À trancher : carte junior/junior+revue/senior par étape + test d'apprenabilité réel chronométré par un consultant qui n'a pas écrit le cadrage.

**M6. Le pari IA prudent renvoie la valeur IA dans la phase que le modèle commercial ne couvre pas** — (règle 3.2.1) + (le diagnostic trouve toujours de l'organisationnel) + (la boucle ⟲ sans véhicule commercial) = le sponsor venu pour l'IA repart avec un runbook. Face à un vendeur AIOps qui promet un dashboard en 3 semaines, l'offre perd à la qualification faute de contre-narrative écrite. Recommandation : argumentaire d'attaque contre la sur-promesse IA + quick win IA légitime packagé dès l'intake (cas D0/D1 readiness [2]+).

### MINEUR

**m1. La règle d'or n°1 IA n'a ni test ni arbitre** — « Jamais l'IA sur un problème d'abord organisationnel » : aucun critère, aucune checklist, aucun owner. Comparer avec le gate DevOps [0] qui a règle dure + dérogation ADR. Recommandation : critère observable adossé au pilier Agentic Readiness + dérogation ADR.

**m2. Le « pourquoi maintenant » vit dans le deck, pas dans le cadrage** — Les « 3 déclencheurs » de la slide Contexte n'ont pas de section source dans le cadrage ; la propagation s'est faite deck→cadrage, sens interdit par la règle. Recommandation : rapatrier les 3 déclencheurs en sous-section de §Vue d'ensemble, sourcés et tagués.

**m3. L'effort de cadrage est inversement proportionnel à la proximité du revenu** — La mission flash (premier produit vendu) tient en une parenthèse quand le MVP6 a vision + composants + analyse de risque. Recommandation : scoper la mission flash au niveau du cas nominal (durée, livrables, sous-ensemble des 11 agents mobilisé).

**Fil rouge** : un document de méthode d'une rigueur rare qui se prend pour un cadrage
d'offre — le « comment faire la mission » est au-dessus du standard du marché, le
« pourquoi un client l'achète, qui la vend, ce qui se passe quand ça rate » est absent,
hors périmètre, ou délégué à des pilotes qui ne peuvent pas tout porter.

---

## Annexe B — Research domaine/technique (rapport brut, sourcé web)

**Q1 Platform engineering / « as a product »** — Gartner : 80 % des grandes orgs avec platform teams en 2026 (45 % en 2022) mais <30 % de gains mesurables ; REX d'échec publiés (IDP abandonnée par 80 % des devs en 3 mois ; goulot = staffing du profil hybride infra/API/UX ; time-to-value 6-18 mois). « Platform as a Product » (Team Topologies) est mainstream. **Verdict : nuance** — la thèse n'est plus différenciante, la valeur est dans l'exécution du pilier Assainir ; risque de reproduire l'écart 80/30 si le gaspillage reste un audit déconnecté. Sources : gartner.com (topic platform engineering), devx.com, hackernoon.com, platformengineering.com, topconsultingfirms.net, teamtopologies.com.

**Q2 Agentic AI ops** — Gartner (25/06/2025) : >40 % des projets agentic abandonnés d'ici fin 2027 (coûts, ROI flou, gouvernance) ; « agent washing » (~130 vendeurs réellement agentic sur des milliers) ; 19 % seulement d'investissements significatifs (n=3412). Production réelle : corrélation d'alertes et knowledge retrieval validés, remédiation autonome aspirationnelle — écho littéral au triptyque COLLECTE (validé) / DIAGNOSTIC (partiel) / arbitrage (non délégué). Deloitte 2026 : 1 entreprise sur 5 a une gouvernance mature des agents. **Verdict : conforte fortement** — mais le gate IA couvre confidentialité/supervision, pas le risque de ROI (celui qui tue 40 % des projets). Sources : gartner.com/newsroom, augmentcode.com, digitalapplied.com.

**Q3 Supervision humaine & gates** — Plafond de débit du reviewer documenté et nommé ; dérive rubber-stamping au-delà de quelques centaines de décisions/jour ; EU AI Act art. 14 (supervision humaine, application 08/2026), convergence NIST AI RMF / ISO 42001 sur 4 contrôles dont la supervision ; « governance-in-the-loop » émergent = reformulation du checkpoint non-automatisable. **Verdict : conforte fortement, mais souligne le trou** — aucune source ne résout la dérive rubber-stamping à l'échelle ; le cadrage nomme le plafond sans mécanisme anti-fatigue. Sources : synvestable.com, digitalapplied.com, eccouncil.org, ishir.com.

**Q4 Mesure gaspillage → réinvestissement** — FinOps Framework 2026 : réduction du gaspillage priorité n°1, « Executive Strategy Alignment » qualitatif, pas de KPI de réinvestissement standardisé ; DORA/SPACE : rien ; proxy le plus proche = toil ≤50 % (Google SRE), mesure de temps jamais reprise en standard transverse ; FinOps for AI = coût consommé, pas capacité libérée. **Verdict : conforte l'aveu du cadrage** — vrai angle mort de l'industrie ; chantier propriétaire justifié mais charge de la preuve portée seul. Sources : finops.org, waydev.co, sre.google, n-ix.com.

**5 signaux clés** : (1) « as a product » plus différenciant ; (2) l'écart adoption/valeur 80/30 est le test de vérité de la double mission ; (3) la prudence agentique validée par les données mais aveugle au risque ROI ; (4) plafond HITL réel et documenté, mécanisme anti-fatigue absent d'IAP — point le plus exposé si le Niveau C est engagé ; (5) le KPI de réinvestissement manque partout — IAP porterait seul la charge de la preuve de son affirmation la plus centrale.

---

## Annexe C — Market research (rapport brut, sourcé web)

**Paysage concurrentiel** — Accenture (AATA, Frontier Alliances OpenAI avec McKinsey/BCG X/Capgemini) : fort IA ops, pas de narratif gaspillage-finance-transformation. Capgemini : concurrent le plus proche sur le TOM plateforme banque/assurance. **Thoughtworks : e-book « Infrastructure as a Product »** — collision de nom, sans pilier gaspillage ni doctrine IA. **Itential : plateforme « Infrastructure as a Product for AI-Driven Operations »** (SaaS, -90 % OPEX promis) — même nom, promesse outillage pur. Wavestone/Devoteam/Theodo : briques cloud/cyber/IA vendues séparément, aucun ne couple les trois. Big4 : PwC FR (04/2026) occupe déjà le terrain gouvernance IA agentique. Sources : tensure.io, cio.com, argano.com, thoughtworks.com, itential.com, cfnews.net, wavestone.com, theodo.com, pwc.fr.

**Alternatives outillées** — Backstage ~89 % de part IDP ; 75 % des grandes orgs avec portail dev fin 2026 ; Datadog Bits AI (100+ features DASH 06/2026), Dynatrace Davis, PagerDuty agents sur escalation policies ; ServiceNow « Autonomous Workforce » + AI Control Tower (l'offre la plus agressive, à l'opposé de la doctrine IAP) ; FinOps outillé : marché 15,7 Md$ (2026), gaspillage cloud ~29 % et en hausse (Flexera). **Conclusion : l'outillage mange la mécanique, pas le liant organisationnel** (cible, gouvernance, compétences, réallocation du gain) — c'est la zone de survie d'IAP. Sources : cycloid.io, roadie.io, siliconangle.com, augmentcode.com, newsroom.servicenow.com, diginomica.com, axis-intelligence.com, mordorintelligence.com.

**Demande** — Baromètre Abraxio DSI FR (12/2025) : « back to basics », cyber en tête, modernisation infra et optimisation coûts RECULENT. Mais l'IA capte le budget sans plafond : 87 % des DSI avec agents en prod, 25 % seulement avec visibilité temps réel (fatigue de gouvernance = douleur concrète). Gartner CIO Agenda 2026 : +35 % de dépense IA, 64 % des DSI en agentic sous 24 mois, 2026 = année de l'exigence de ROI ; >40 % d'abandons prédits d'ici 2027 ; Hype Cycle : agentic au pic des attentes exagérées (17 % déployés). Forrester : « la discipline compte plus que l'expérimentation », autonomie complète « à des années », <15 % activeront les features agentiques. Souveraineté FR/EU : 2026-2027 « année du basculement ». Pénurie SRE/cloud persistante. Sources : cio-online.com, abraxio.com, alliancy.fr, gartner.com, forrester.com, journaldunet.com, pwc.fr, cadreho-portage.fr, free-work.com.

**Menaces de substitution** — (1) le SaaS bat le conseil en time-to-value sur « automatiser le run » ; (2) l'étiquette « Infrastructure as a Product » est déjà prise (Thoughtworks, Itential) ; (3) la gouvernance IA est un terrain Big4/hyperscalers — me-too si la prudence est l'angle principal ; (4) cycle budgétaire 2026 défavorable au narratif transformation pluriannuelle.

**3 forces** : timing de la désillusion agentique (la prudence devient anticipation documentée) ; couplage produit+gaspillage dans l'angle mort commun de la concurrence ; alignement avec la fatigue de gouvernance IA (87 % vs 25 %) avec promesse vérifiable (delta T0→réévaluation).
**3 faiblesses** : cycle budgétaire 2026 contre la transformation pluriannuelle ; financement croisé non prouvé attaquable par le ROI immédiat des outillés ; taille/marque face aux Big4 sur l'axe prudence seule.
**Angle d'attaque recommandé** : entrer par la douleur RUN mesurée (capacité humaine rare récupérée), se positionner en aval des outils FinOps/AIOps, amener l'IA en garde-fou — cohérent avec le narratif du deck (IA en avant-dernier). Souveraineté/conformité = accélérateur de deuxième vague (banque, secteur public), pas point d'entrée.
