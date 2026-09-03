# VSCode3 — cadrage BMAD IAP

Le livrable de ce dépôt est un **deck de synthèse** (`docs/cadrage-ppt/`, v2.11,
9 chapitres, 46 slides) qui restitue les résultats du cadrage BMAD IAP
(`docs/bmad-iap-cadrage.md`), dessiné par-dessus le vrai template de marque
OCTO (`template-octo.pptx`) — masters/layouts/thème conservés.

## Utilisation

Depuis `docs/cadrage-ppt/` :

```bash
# régénérer le deck
python generate_deck.py

# après toute modification du générateur
python test_generate_deck.py
```

`test_generate_deck.py` vérifie la structure, les cadres photo, la régression
du numéro de chapitre, les obstructions en liste blanche et le rendu réel
LibreOffice — **en plus** du rendu PowerPoint et d'une relecture à l'œil (le
test valide le cadrage géométrique, pas la qualité d'une photo).

Scripts superviseur/orchestrateur (`.claude/orchestration/`, `.claude/supervision/`) :

```bash
py -m pytest tests/test_agent_*.py
py -m pytest tests/ --cov=docs/cadrage-ppt   # couverture, première mesure 10 %
py -m ruff check .                            # linter, baseline mesurée
```

Détail complet des commandes : voir [`CLAUDE.md`](CLAUDE.md). Gotchas connus du
deck (cadre teardrop carré, glyphe ⟲ sans variante grasse) : voir
[`.claude/skills/deck-design-review/SKILL.md`](.claude/skills/deck-design-review/SKILL.md)
et les commentaires de `docs/cadrage-ppt/generate_deck.py`.

## Documentation

- Règles et contraintes du dépôt : [`CLAUDE.md`](CLAUDE.md).
- Cadrage produit : [`docs/product-brief.md`](docs/product-brief.md) (synthèse)
  et [`docs/bmad-iap-cadrage.md`](docs/bmad-iap-cadrage.md) (source complète).
- Tableau de bord de supervision (synchronisé depuis le hub) :
  [`docs/wiki/index.md`](docs/wiki/index.md) ou `docs/wiki.html`.
