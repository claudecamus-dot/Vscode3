# Audits techniques — etage qualitatif de la supervision

Un fichier `<projet>.json` par projet audite, ecrit par la skill `audit-technique`.
Ce repertoire etait reference par la skill mais n'existait pas : cree le 2026-09-01.

Le scanner deterministe (`.claude/supervision/scan_transcripts.py`, 0 token) mesure la
PRESENCE de dispositifs. Ces audits qualifient ce qui exige de LIRE le code —
robustesse, performance, risque technique, securite. Ils sont factures : a lancer sur
demande, pas a chaque scan.

## Format

```json
{
  "projet": "VSCode3",
  "date": "2026-09-01",
  "dimensions": {
    "robustesse":       {"niveau": "moyen",    "synthese": "...", "findings": [{"titre": "...", "localisation": "chemin/fichier.py:42"}]},
    "performance":      {"niveau": "ok",       "synthese": "...", "findings": []},
    "risque_technique": {"niveau": "moyen",    "synthese": "...", "findings": []},
    "securite":         {"niveau": "critique", "synthese": "...", "findings": []}
  }
}
```

`niveau` : `ok` | `moyen` | `critique`. 5 findings max par dimension, chacun localise
(`fichier:ligne` ou fonction nommee) — un ressenti n'est pas un finding.

## Limite connue sur ce depot

La skill annonce que le verdict est rendu dans la section « Pratiques, couverture &
risques » du wiki. **Cette section n'existe pas ici** : elle est produite par le scanner
du hub, pas par `scan_transcripts.py`. Un audit ecrit dans ce repertoire est donc lisible
directement, mais n'apparaitra pas au wiki tant que le rendu n'aura pas ete propage.
