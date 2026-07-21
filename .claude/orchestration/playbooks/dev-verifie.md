# Playbook `dev-verifie` — implémentation vérifiée de bout en bout

Workflow générique pour tout changement de code produit sur ce dépôt (scripts de génération
PPT, hooks `.claude/`, scripts de supervision/orchestration) : implémenter, tester,
**vérifier en réel** (pas seulement un run vert), puis boucle de definition-of-done avant
tout commit. Adapté du playbook du même nom porté depuis VSCode2 : ce dépôt n'est pas une
app web (pas de serveur de dev, pas de template Jinja/CSS/JS) — l'étape de vérification UI a
été retirée ; l'étape PPT reste, elle correspond à la pratique déjà réelle de ce projet.

Frontière avec `export-ppt-verifie` : un changement de code qui *touche* la génération PPT
au passage reste ici (l'étape `verification-pptx` couvre) ; quand le **livrable est le deck
lui-même** (layout, contenu, visuel), préférer `export-ppt-verifie`.

```json
{
  "nom": "dev-verifie",
  "description": "Implémentation d'une feature/correction avec tests, vérification réelle adaptée aux fichiers touchés, et revue-increment avant commit.",
  "statut": "jamais-joue",
  "source": "manuel",
  "declencheurs": [
    "implémente/corrige un script Python (génération PPT, hooks, supervision/orchestration)",
    "changement dans docs/cadrage-ppt/generate_deck.py ou pptx_deck.py",
    "fin d'incrément, préparation d'un commit de code produit"
  ],
  "etapes": [
    {
      "id": "cadrage",
      "agent": "session principale",
      "mode": "cascade",
      "modele": "(session)",
      "contrat": {
        "type": "deterministe",
        "critere": "fichiers concernés lus, appelants des fonctions/champs partagés grep-és avant modification"
      },
      "checkpoint": false
    },
    {
      "id": "implementation",
      "agent": "session principale",
      "mode": "cascade",
      "modele": "(session)",
      "contrat": {
        "type": "deterministe",
        "critere": "chaque exigence EXPLICITE de la demande (points numérotés, contraintes) cochée une à une contre le diff — pas seulement « ça compile/passe » ; toute exigence réinterprétée ou écartée signalée, jamais silencieuse ; style du fichier environnant respecté (pas de linter configuré)"
      },
      "checkpoint": false
    },
    {
      "id": "tests",
      "agent": "session principale",
      "mode": "cascade",
      "modele": "(session)",
      "contrat": {
        "type": "deterministe",
        "critere": "verdict lu sur la ligne de synthèse RÉELLE de pytest (N passed / 0 failed / 0 error) quand une suite existe (ex. test_generate_deck.py) — jamais sur un résumé filtré ou tronqué ; en cas de doute, rediriger toute la sortie dans un fichier",
        "commande": "pytest -q"
      },
      "checkpoint": false
    },
    {
      "id": "verification-pptx",
      "agent": "pptx-verify",
      "mode": "cascade",
      "modele": "(session)",
      "contrat": {
        "type": "reel",
        "critere": "SI generate_deck.py/pptx_deck.py touché : export réel rendu en images et inspecté (python-pptx est un parseur tolérant)"
      },
      "checkpoint": false
    },
    {
      "id": "revue-increment",
      "agent": "revue-increment",
      "mode": "cascade",
      "modele": "(session)",
      "contrat": {
        "type": "reel",
        "critere": "boucle revue + application des correctifs + re-vérification réelle exécutée en entier"
      },
      "checkpoint": "avant tout commit — action difficilement réversible, proposer, ne pas exécuter unilatéralement"
    }
  ],
  "regle_reprise": "une relance ciblée par étape en échec de contrat, puis escalade utilisateur avec l'état réel"
}
```
