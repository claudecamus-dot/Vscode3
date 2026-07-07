---
updated: 2026-07-07
confidence: confirmed
agents: [onboarder]
---

# Domaine métier — BMAD IAP (Infra as a Product)

## Vue d'ensemble

Module de transformation consulting à double mission : transformer une organisation infrastructure (guichet, centre de coûts ou fonction support) en plateforme interne opérée comme un produit, ET traiter structurellement le gaspillage qui l'en empêche. Les deux piliers ne sont pas séquentiels ni optionnels l'un par rapport à l'autre.
— `CONFIRMÉ` · onboarder · 2026-07-07 · `docs/bmad-iap-cadrage.md` §Mission & vision

## Domaines documentés

| Domaine | Fichier | Concepts clés |
|---------|---------|----------------|
| Cadrage BMAD IAP | *(page unique — [docs/bmad-iap-cadrage.md](../../bmad-iap-cadrage.md))* | Produit infra, traitement des gaspillages, gate IA, modèles de maturité, agents/workflows |

## Concepts transversaux

- **Gate IA & confidentialité** — workflow bloquant (`iap-ai-data-confidentiality-gate`), checkpoint humain non-automatisable avant tout usage IA sur données client, classification D0–D4
  — `CONFIRMÉ` · onboarder · 2026-07-07 · `docs/bmad-iap-cadrage.md` §Gate IA & confidentialité
- **Traitement des gaspillages** — 8 familles (flux, humain, RUN, financier, cognitif, décisionnel, environnemental, IA), chaîne Détecter→Qualifier→Quantifier→…→Prévenir, scoring Impact × Faisabilité − Prudence IA
  — `CONFIRMÉ` · onboarder · 2026-07-07 · `docs/bmad-iap-cadrage.md` §Traitement des gaspillages
- **Modèles de maturité** — deux échelles indépendantes : maturité produit/plateforme (grille VSCode1, pilotée par pilier Excellence Technique / Agilité à l'Échelle) et maturité IA client (pilier IA/Agentic/Organisation Augmentée, remplace l'ancien M0–M4 générique)
  — `CONFIRMÉ` · onboarder · 2026-07-07 · `docs/bmad-iap-cadrage.md` §Modèles de maturité

## Utilisateurs cibles

- Consultant BMAD IAP (« le coach ») — pilote la mission de bout en bout, un agent invoqué à la fois, aucune orchestration automatique (Niveau A de l'ambition de l'outil, état actuel du cadrage)
  — `CONFIRMÉ` · onboarder · 2026-07-07 · `docs/bmad-iap-cadrage.md` §Utilisation simple par le coach
- Sponsor client — achète la trajectoire produit/plateforme à moyen terme, lit le deck exécutif final (16 sections, radar de maturité, roadmap)
  — `DÉDUIT` · onboarder · 2026-07-07 · `docs/bmad-iap-cadrage.md` §Mission & vision, §Workflows (`iap-deck-builder`)
- Parties prenantes interviewées — équipe infra, utilisateurs applicatifs, management, sponsor — une `Interview` par persona pour objectiver convergences/divergences
  — `CONFIRMÉ` · onboarder · 2026-07-07 · `docs/bmad-iap-cadrage.md` §Moteur d'assessment
