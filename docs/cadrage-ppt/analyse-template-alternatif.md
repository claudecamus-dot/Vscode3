# Analyse d'un second template PPT — comparaison avec OCTO

> Objectif : identifier, dans un autre template disponible en local (projet
> frère VSCode2, `data/pptx_templates/1.pptx`), des éléments de design
> réutilisables pour rendre `docs/cadrage-ppt/generate_deck.py` plus
> professionnel — sans copier le template lui-même (voir §Provenance).
> Analyse uniquement — aucune implémentation dans ce document.

## Provenance et redaction

`VSCode2/data/pptx_templates/1.pptx` (7,2 Mo) n'est pas un template vierge :
c'est une **mission de conseil réelle, terminée, réutilisée comme gabarit**
(41 layouts, mais aussi 58 slides d'exemple déjà remplies d'un vrai contenu
de restitution). Les noms de layout (`Insert_SNCF_Connect_Light/Dark`) et le
contenu (streams « DSI TGV », « Factory ») identifient le secteur ferroviaire.
Cette analyse **ne cite aucun contenu client** (verbatims, noms d'équipes,
chiffres) — seulement la structure, les couleurs et la géométrie des formes,
qui sont les éléments transposables. `VSCode2/data/pptx_templates/2.pptx` et
`3.pptx` sont écartés : ce sont les gabarits par défaut de `python-pptx`
(27 Ko, 1 slide, aucune identité de marque), pas des templates de marque.

## 1. Identité

| Élément | `1.pptx` (ce document) | `template-octo.pptx` (déjà utilisé, cf. [`template-octo.md`](../vscode1-export/template-octo.md)) |
|---|---|---|
| Format slide | 13,333 × 7,5 in (16:9 large, standard PowerPoint moderne) | 10 × 5,625 in (16:9 « Google Slides ») |
| Police | **Arial** — police système, aucune famille de marque dédiée | **Outfit** (Light/Regular/Medium/SemiBold) — famille de marque à part entière |
| Nb de layouts | 41 | 34 |
| Nb de slides d'exemple | **58 — un vrai deck de mission rempli**, pas des exemples vides | 9 — exemples vides à vocation de démo |

Premier constat, avant même la couleur : OCTO a une police de marque dédiée,
ce gabarit n'en a pas (Arial = repli système). Sur ce seul critère, le
template déjà utilisé est **plus professionnel** — pas un point à reprendre
de `1.pptx`.

## 2. Palette

```
dk1     #0A131F   navy quasi-noir (texte, fonds sombres)
lt1     #FFFFFF   blanc
dk2     #8DE7FD   cyan clair
lt2     #0088CD   bleu
accent1 #8BFEDC   menthe/teal
accent2 #C099FF   lavande/violet
accent3 #F5DF59   jaune
accent4 #8DE7FC   cyan clair (doublon dk2)
accent5 #0087CC   bleu (doublon lt2)
accent6 #0A121F   navy quasi-noir (doublon dk1)
```

Différence structurelle avec OCTO (`dk1` navy + `accent3` cyan seuls comme
identité, le reste étant des nuances de gris-bleu neutres) : ce gabarit porte
**6 couleurs vives distinctes**, dont 3 en doublon dans le nuancier — signe
que la palette a été pensée pour le **contenu**, pas pour l'identité de
marque au sens strict.

## 3. Ce que la richesse de layouts révèle (le vrai point d'intérêt)

Les 41 layouts se répartissent en familles répétées **une fois par couleur**
(`_BleuClair`, `_BleuPrimaire`, `_Jaune`, `_Pourpre`, `_Vert`) :

- `Intercalaire_1_<couleur>` / `Intercalaire_2_<couleur>` — slides de
  rupture de chapitre, plein cadre coloré.
- `Contenu_<couleur>` — slide de contenu standard.
- `Contenu_XL_<couleur>` — contenu dense (jusqu'à 29 formes observées).
- `Contenu + Photo_<couleur>` — texte + photo plein cadre à droite.
- `Icones` — titre + un badge icône circulaire + légende, pour un concept
  illustré isolé.

**La couleur n'est pas décorative ici : c'est un code de navigation.** Les
58 slides d'exemple confirment l'usage réel : chaque grand chapitre de la
mission (Rapport d'étonnement → jaune, Principes et modèles → vert,
Recommandations → pourpre, Trajectoire → bleu clair) porte sa propre couleur
d'intercalaire ET de contenu, du début à la fin. Un lecteur qui feuillette
sait dans quel chapitre il est sans lire le titre — lisible même en
miniature (mode trieuse de diapositives).

**OCTO n'a pas cet équivalent** : un seul layout « Titre seul » + une
palette de marque à 2 couleurs, la distinction de section se ferait
aujourd'hui uniquement dans notre `kicker` textuel (« CADRAGE » / « MÉTHODE »
/ etc.) — un signal plus faible qu'une couleur de fond de chapitre entière.

## 4. Pattern concret le plus directement réutilisable : la carte de recommandation

Une des slides denses (« NOTRE PROPOSITION DE VALEUR », 29 formes) contient
une **carte de recommandation structurée** : encarts OBJECTIF / ACTEURS /
CRITÈRES DE PRIORISATION empilés à gauche, avec pour ce dernier une
**jauge à points** : 5 points pleins/vides sur deux lignes (« Valeur » /
« Complexité »), chaque ligne représentant un score 1-5.

C'est frappant car **le cadrage BMAD IAP définit déjà exactement cette
donnée** sans jamais avoir défini son traitement visuel :

> §Recommandations (`docs/bmad-iap-cadrage.md`) : *« RecommendationAxis
> (3–4 axes transverses)... noté sur deux axes simples valeur / complexité
> (1–5) »*

Aujourd'hui `slide_ambition`/`slide_kpis` dans `generate_deck.py` n'illustrent
ce genre de score que par du texte. `pptx_deck.py` a déjà l'outillage prêt à
l'emploi pour la jauge à points vue ici — `D.add_dot` (pastille pleine) en
boucle, ou `D.add_gauge` (anneau) pour une variante circulaire — aucun
nouveau helper à écrire.

## 5. Pattern secondaire : roadmap déclinée par équipe/stream

Slides 54-58 (« Roadmap – Stream CODIR / FACTORY / Transverse / DSI TGV /
Autres ») : **une slide de roadmap par équipe** plutôt qu'une roadmap unique
fourre-tout. Précédent concret pour le brainstorm v1.9 déjà posé dans le
cadrage (§Trajectoire, « Deck de plan de déploiement ») : si BMAD IAP
généralise équipe par équipe (§Modèles d'équipe), un deck de déploiement
pourrait décliner sa slide de roadmap une fois par équipe plutôt que
d'empiler toutes les équipes sur une seule frise — cohérent avec le
`team-topology-map.md` déjà prévu comme source de données par équipe.

## 6. Synthèse — à reprendre, à ne pas reprendre

| Élément | Verdict | Pourquoi |
|---|---|---|
| Couleur de chapitre par section du deck | **Repris (2026-07-09)** | Signal de navigation plus fort que le kicker textuel seul ; implémenté comme paramètre de couleur passé à `content_slide()` (pas un nouveau layout — le template OCTO n'a qu'un seul layout « Titre seul »). Cadrage=bleu, Méthode=vert, Trajectoire=or, Executive summary=cyan |
| Jauge à points pour un score 1-5 (valeur/complexité) | **Repris (2026-07-09)** | Implémenté sur `slide_gaspillages` (score « impact × faisabilité − prudence IA ») via un nouveau helper local `dot_scale()` qui compose `D.add_dot` — aucun helper ajouté à `pptx_deck.py` lui-même |
| Roadmap déclinée par équipe/stream | **À envisager** | Précédent concret pour le profil de deck « Plan de déploiement » du brainstorm v1.9 — pas encore fait, suppose d'abord des données réelles par équipe (`team-topology-map.md`) que ce deck de synthèse n'a pas |
| Police Arial | **À ne pas reprendre** | OCTO a une police de marque dédiée (Outfit) — un vrai recul par rapport à ce qui est déjà utilisé |
| 6 couleurs d'accent simultanées | **À ne pas reprendre telles quelles** | Casserait la sobriété de la charte OCTO (2 couleurs d'accent) déjà en place ; seul le *principe* (une couleur par chapitre) a été repris, avec les couleurs déjà en place dans le deck (`D.PALETTE`), pas la palette du gabarit analysé |
| Format 13,333×7,5in | **Sans objet** | Le deck BMAD IAP est contraint par le format natif du template OCTO (10×5,625in) — changer de format reviendrait à abandonner le template de marque |

**Suite donnée (2026-07-09) :** les deux pistes « à reprendre »/« à envisager »
les plus concrètes ont été implémentées dans `generate_deck.py` et vérifiées
(géométrie + rendu réel) — voir le tableau ci-dessus. Restent en attente :
la roadmap déclinée par équipe (bloquée sur des données que ce deck de
synthèse n'a pas encore) et l'application éventuelle de la couleur de
chapitre à d'autres éléments que le kicker (accent des cartes, par exemple),
non faite pour limiter le risque de régression visuelle sur les 11 slides
déjà vérifiées.
