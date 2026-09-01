---
updated: 2026-09-01
confidence: mixed
agents: [revue-fonctionnelle-technique]
---

# Critères de pratiques — référentiel d'analyse

Référentiel des **règles d'analyse** appliquées à ce dépôt : ce qu'on vérifie, comment on
le mesure, et d'où la règle vient. Une règle n'entre ici qu'après un arbitrage humain —
la veille *propose*, l'utilisateur *adopte*, l'orchestrateur *applique* (§ 2 quater de
`.claude/skills/agent-orchestrator/SKILL.md`).

> **Pourquoi cette page existe.** Elle était référencée par la skill `veille-agentic`
> (§ 7) et par l'étape « règle d'analyse » de la commande `/orchestre adopte`, sans
> jamais avoir été créée sur ce dépôt — une adoption de trouvaille n'avait donc aucun
> fichier cible où inscrire sa `regle_proposee`. Créée le 2026-09-01 par la revue
> fonctionnelle et technique.

## Portée sur ce dépôt

Le référentiel complet (§ 1 à 6 : critères hérités du hub de supervision) **n'a pas été
propagé ici**. Cette page ne porte donc que le § 7 — les règles nées de la veille et
adoptées pour ce projet. Ne pas la lire comme la copie locale du référentiel du hub :
c'est un fichier local, alimenté par les arbitrages pris ici.

## § 7 — Règles issues de la veille agentic

Chaque règle adoptée s'écrit avec : ce qu'elle exige, comment on la mesure (à froid si
possible), et la trouvaille dont elle vient.

| Règle | Ce qu'elle exige | Mesure | Origine | Adoptée le |
| --- | --- | --- | --- | --- |
| _(aucune)_ | — | — | — | — |

**Aucune règle à ce jour** : la veille n'a jamais tourné sur ce dépôt
(`.claude/veille/veille.json` créé vide le 2026-09-01, `derniere_veille: null`).
Le hook SessionStart le signale à chaque démarrage.

## Comment une règle arrive ici

1. La veille écrit une entrée dans `.claude/veille/veille.json` avec une
   `regle_proposee`, en statut `nouveau`.
2. L'utilisateur arbitre : `adopte <trouvaille>` (ou `écarte`, avec la raison).
3. L'orchestrateur inscrit la règle dans le tableau ci-dessus **et**, si elle est
   mesurable à froid, l'outille dans `.claude/supervision/scan_transcripts.py` avec ses
   tests de non-régression — c'est ce qui fait passer un critère de « déclaré » à
   « mesuré ».
4. L'arbitrage est tracé dans `.claude/supervision/arbitrages.json` à la cible
   `veille:<slug>`, sinon le wiki continue d'afficher la trouvaille comme en attente.

Une règle inscrite ici mais non outillée reste une intention : le dire dans la colonne
« Mesure » plutôt que laisser croire qu'elle est vérifiée.
