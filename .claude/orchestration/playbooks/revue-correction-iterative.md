# Playbook `revue-correction-iterative` — revue, correction, tests, en boucle bornée

Inscrit le 2026-10-24 sur demande de l'utilisateur : « comité augmenté revue puis
correction et tests de façon itérative tant qu'il y a des corrections à mener ». Statut
`jamais-joue` : à confirmer sur le premier lot réel.

**Boucle** : lot écrit par UN rédacteur → comité augmenté de revue → s'il reste un
constat à corriger : comité de correction → UN rédacteur applique la version arbitrée →
tests → NOUVELLE revue en contextes frais → on recommence.

**Comité augmenté de revue** : 3 voix en lecture seule — A régression et mesure sur le
journal réel, B adversariale, C tests / mutants / miroirs-kit — qui écrivent dans un
fichier commun en ajout seul (`C:/tmp/ca-<lot>/commun.md`). Une contre-lecture des voix
uniquement s'il y a désaccord, et c'est l'UTILISATEUR qui arbitre. Les voix n'utilisent
pas Agent (pas de re-fan-out) ; au-delà de 3 voix, validation § 3 de l'orchestrateur.
Coût estimé : ≈6 agents par ronde (3 revue + 3 correction).

**Comité de correction** : voix en lecture seule (comment corriger chaque constat, effets
de bord, tests et mutants, ordre). Un comité n'écrit jamais ; le relecteur n'est jamais
l'auteur du lot ni de la correction.

**Borne : 3 rondes par défaut** (valeur par défaut que l'utilisateur peut changer ; plafond,
jamais critère d'arrêt). On s'arrête dès la première ronde sans constat REPRODUIT. À la
borne, ou si le MÊME constat réapparaît : STOP et escalade à l'utilisateur avec l'état
réel, jamais une ronde de plus. Même constat = même clé (fichier + règle/symbole) présente
dans les rondes N et N-1 du fichier commun ; comparaison faite par la session principale,
sans script (`revue_fonctionnement.py --non-progres` ne lit que `runs.jsonl` : notion seulement).
Escalade : constats ouverts avec sévérité, rondes jouées, commandes de test et comptes,
options (+N rondes, abandon, correction manuelle). Aux voix fraîches de la ronde N+1, on ne
donne du fichier commun de la ronde N qu'une LISTE DE CLÉS de constats, jamais les verdicts.

**Déclenchement** : après un lot commité par un rédacteur et signalé terminé, l'orchestrateur
propose cette boucle (annoncé puis validé). Lot terminé = branche commitée + arbre du worktree
propre pour le périmètre + suites ciblées vertes. Le compteur de rondes est figé tant qu'un
arbitrage utilisateur est en attente ; une ronde sans arbitrage n'est pas rejouée.

**Sortie de boucle** : verdict sans réserve bloquante ET tests verts (rejeu des suites
ciblées exigé même sans constat en ronde 1) ET aucun constat ouvert. Pas de merge avant ce verdict.
Si la boucle s'arrête à la première ronde sans constat reproduit, les hypothèses non reproduites sont listées comme « hypothèses non reproduites » dans le rapport de ronde, ne bloquent PAS la sortie et sont escaladées à l'utilisateur comme points ouverts.

**Réservé à l'utilisateur** : arbitrage des désaccords entre voix, décisions de produit
(ex. l'intention d'une règle), merge, push (jamais sans confirmation explicite).

**Rapport à chaque ronde** : nombre de constats par sévérité, corrigés / ouverts, tests
avec leur commande et leurs comptes.

**Journal** : `log_run.py` uniquement pour une correction ou un bug, résultat
`en-attente-validation` tant que l'utilisateur n'a pas validé (R5).

```json
{
  "nom": "revue-correction-iterative",
  "description": "Boucle bornée revue (comité augmenté, lecture seule) puis correction (comité + un seul rédacteur) puis tests, rejouée avec des relecteurs frais jusqu'à verdict sans réserve bloquante, ou escalade à la borne.",
  "statut": "jamais-joue",
  "source": "manuel",
  "declencheurs": [
    "lot terminé à passer en revue puis corriger puis tester",
    "revue puis correction et tests de façon itérative tant qu'il y a des corrections",
    "comité augmenté de revue sur un lot fini"
  ],
  "etapes": [
    {
      "id": "lot-redacteur",
      "agent": "session principale",
      "mode": "cascade",
      "modele": "(session)",
      "contrat": {
        "type": "deterministe",
        "critere": "lot écrit par un seul rédacteur, commit scopé sur une branche (git diff --cached --name-only relu), compteur de rondes initialisé à 0 avec sa borne (défaut 3, modifiable par l'utilisateur)"
      },
      "checkpoint": false
    },
    {
      "id": "comite-revue",
      "agent": "bmad-revue",
      "mode": "parallele",
      "modele": "sonnet",
      "fan_out_max": 3,
      "contrat": {
        "type": "deterministe",
        "critere": "3 voix en lecture seule (A régression et mesure sur le journal réel, B adversariale, C tests / mutants / miroirs-kit), un rapport par voix dans le fichier commun en ajout seul, contextes frais à chaque ronde, relecteur jamais auteur ; contre-lecture des voix seulement sur désaccord"
      },
      "checkpoint": false
    },
    {
      "id": "consolidation-verdict",
      "agent": "session principale",
      "mode": "cascade",
      "modele": "(session)",
      "contrat": {
        "type": "deterministe",
        "critere": "constats dédoublonnés avec sévérité, verdict écrit ; les désaccords entre voix sont remontés à l'utilisateur, jamais tranchés seul ; sortie de boucle si aucun constat ouvert ET aucune réserve bloquante ET suites ciblées rejouées vertes (même sans constat en ronde 1)"
      },
      "checkpoint": "arbitrage UTILISATEUR de tout désaccord entre voix et de toute décision de produit (intention d'une règle) avant correction"
    },
    {
      "id": "comite-correction",
      "agent": "bmad-revue",
      "mode": "parallele",
      "modele": "sonnet",
      "fan_out_max": 3,
      "contrat": {
        "type": "deterministe",
        "critere": "voix en lecture seule : comment corriger chaque constat, effets de bord, tests et mutants, ordre d'application ; aucune écriture"
      },
      "checkpoint": false
    },
    {
      "id": "correction-redacteur-unique",
      "agent": "session principale",
      "mode": "cascade",
      "modele": "(session)",
      "contrat": {
        "type": "deterministe",
        "critere": "UN seul rédacteur applique la version arbitrée, commit scopé, relecteur différent de lui ; compteur de rondes incrémenté"
      },
      "checkpoint": false
    },
    {
      "id": "tests-et-mutants",
      "agent": "session principale",
      "mode": "cascade",
      "modele": "(session)",
      "contrat": {
        "type": "deterministe",
        "critere": "rejeu de chaque suite trouvée par grep -rl <basename> tests/, un fichier par exécution, comptes cités avec leur commande ; preuve par mutation de chaque nouveau garde-fou (le faire échouer une fois, mutant repéré par un marqueur sur sa ligne, puis restauré)"
      },
      "checkpoint": false
    },
    {
      "id": "decision-boucle",
      "agent": "session principale",
      "mode": "cascade",
      "modele": "(session)",
      "contrat": {
        "type": "deterministe",
        "critere": "rapport de ronde (constats par sévérité, corrigés / ouverts, tests avec commandes). Si sortie atteinte : stop. Si ronde = borne OU même constat réapparu (clé fichier + règle/symbole présente en rondes N et N-1) : STOP et escalade utilisateur (constats ouverts + sévérité, rondes, commandes et comptes, options +N rondes / abandon / correction manuelle). Arrêt aussi dès une ronde sans constat reproduit. Sinon retour à comite-revue avec des contextes frais (liste de clés seulement)"
      },
      "checkpoint": "merge et push : jamais sans verdict sans réserve bloquante, et push seulement sur confirmation explicite de l'utilisateur ; journaliser (log_run.py, correction ou bug seulement) en-attente-validation"
    }
  ],
  "regle_reprise": "une relance ciblée par étape en échec de contrat, puis escalade utilisateur avec l'état réel — jamais de boucle de retry ; la boucle elle-même s'arrête à la borne de rondes (défaut 3) ou dès que le même constat réapparaît"
}
```
