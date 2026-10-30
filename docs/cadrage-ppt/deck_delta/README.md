# deck_delta : une nouvelle version du deck = un petit fichier d'operations

Port de la generation par delta de Vscode8 (`scripts/deck.py`). Au lieu de regenerer toutes les slides depuis un script, on applique des operations
(`OPS`) sur la derniere version `docs/exports/decks/offre-infra-as-a-product-V<N>.pptx`. Le moteur est `pptx_deck_core` du hub
(`.claude/skills/pptx-deck/scripts/`, canon, jamais modifie ici).

## Usage (depuis `docs/cadrage-ppt/`)

    py deck_delta/deck.py delta_exemple --dry-run                  # simulation : rien n'est ecrit
    py deck_delta/deck.py delta_V6 --base V4                       # ecrit la version suivante (dernier V<N> + 1)
    py deck_delta/deck.py delta_V6 --sortie C:/chemin/essai.pptx   # sortie hors docs/exports/decks
    py deck_delta/deck.py delta_V6 --sans-rendu                    # sans PNG des slides modifiees

Un delta est un `.py` exposant `OPS` (liste d'ops du core), et optionnellement `NOTE`, `BASE`, `ETAPES` : copier `delta_exemple.py`.
Tests : `py -m pytest tests/test_deck_delta.py --basetemp <dossier neuf court>`.

## Rendu des slides modifiees

PowerPoint COM d'abord (`rendu_com.py`, lecture seule, un nouvel essai si le premier appel echoue a froid), puis LibreOffice (skill pptx-verify) ;
PNG `slide_<rang>.png` dans `--dossier-rendu`. Sans rendu possible : statut « NON REGARDÉ ». Le rendu des slides modifiees prend 10 a 70 s.

## Delta type : `delta_V6.py` (base V5 -> V7, 45 slides)

Specimen d'un delta reel : retirer une zone, renommer un titre, ajouter 2 slides sur le gabarit d'une slide existante, aligner un intercalaire, creer un chapitre,
deplacer 4 slides, renumeroter. Pieges rencontres (a connaitre avant d'ecrire un delta) :
- `declarer` est resolu AVANT toute operation : un titre renomme par une op est introuvable (renommer DANS l'etape, declarer l'ancien titre) ;
- toute slide dont un bandeau ou un numero change doit etre declaree, y compris les intercalaires et les slides d'un chapitre renumerote ;
- ne reecrire un texte que s'il differe (un `set_run` identique compte comme modification) ;
- le garde geometrique refuse un texte qui deborde sa boite (cartes de 3 paragraphes : titres courts) ;
- un livrable existant n'est jamais ecrase : une correction apres un premier essai sort en V<N+1>.

## Convention de version

`offre-infra-as-a-product-V<N>.pptx` ; la version suivante est le plus grand N **numerique** plus 1 (V10 > V9), jamais « base + 1 ».
Les fichiers `~$...` et hors convention sont ignores. `--base V4` (ou `4`, ou un chemin) choisit la base ; sans `--base` : la derniere version.

## Garde-fous

- Un livrable existant n'est jamais ecrase (refus avant tout calcul, puis a nouveau juste avant le remplacement) ; ecriture en `.tmp`, controle, puis `os.replace`.
- Slides designees par **titre exact et complet** (placeholder titre, sinon premiere forme texte), `id:N` ou rang ; jamais par prefixe ; titre ambigu ou absent = refus.
- Une slide non declaree qui change, ou qui disparait, est refusee (garde du core + simulation complete en memoire avant ecriture).
- Balises `[À ...]` : une balise retiree sans `source` est refusee. Slides finies : registre optionnel `deck_delta/slides_finies.json` (cles de titre) ; forcage
  seulement avec `--forcer-finie "<titre>" --demande "<mots de l'utilisateur>"`.
- Integrite OPC (skill) + integrite projet + geometrie (nombre de defauts non superieur a celui de la base).
- Statut final : jamais « valide ». `RENDU PRODUIT — À REGARDER : <png>` si le rendu est produit, sinon `NON REGARDÉ`. Les slides modifiees se **regardent** avant livraison.

## Non porte (et pourquoi)

`motifs.py`, `densite.py` (non importes par `deck.py` ; equivalents du hub : `pptx-verify/motifs_deck.py`, `densite_deck.py`), `lint_charte` (aucune charte `tokens.json`
dans ce projet ; signale « non evalue »), `feedbacks_reprise` (registre des slides finies : remplace par le JSON optionnel), `copie_rels_slide` / `clone_slide`
(remplaces par `copier_slide` du core), palette et `cadre_chapitre` Accenture de `deck_draw`. `garde_rendu` et `integrite_projet` sont renommes `deck_garde_rendu` /
`deck_integrite` pour ne pas masquer des modules du hub. Sections p14 : `copier_slide` ne les met pas a jour (V4 n'en a pas).

## Charte, baseline et paliers (portes de Vscode8, 2026-10-29)

- **Charte** : `charte/tokens.json` (racine du depot) + `lint_charte.py` (port de Vscode8). Couleurs du theme et `autorise_*` passent ; `tolere_*` = valeurs mesurees sur la V8,
  signalees `[A VALIDER]` ; tout le reste est un defaut bloquant. Police attendue : Outfit (le theme dit Arial : sans nom explicite, le texte retombe sur Arial).
  Usage : `py lint_charte.py <deck.pptx>`. Seuil de 8 pt de Vscode8 NON repris (la navigation V9 est a 6 pt, a arbitrer).
- **Baseline** : `charte/baseline_defauts.json` fige les defauts geometriques du dernier livrable (cle = constat sans numero de slide). Le test echoue sur un defaut en plus
  ET sur un defaut disparu (dette payee). Apres un delta qui en retire : `py deck_baseline.py --figer`, puis relire le diff du JSON.
- **Paliers** (`tests/conftest.py`, verrouilles par `tests/test_paliers.py`) : `-m livrable` = tests du deck (rapide) ; `-m "not dispositif"` = avant de livrer un deck ; sans `-m` = complet,
  exige des que `.claude/**` change. Les tests du deck (`test_deck_delta`, `test_charte_livrable`) lisent le dernier livrable reel, ou sautent s'il n'y en a aucun.
- Ces gardes ne voient pas un texte rogne ni une forme laide : le rendu regarde reste obligatoire.

## Regle de brief pour tout agent qui reproduit une forme (arbitree le 2026-10-29)

Le brief liste les PNG a OUVRIR (chemins complets), et le rapport rend le **nombre de slides regardees** sur le nombre de slides sources.
Un rapport sans ce compte est refuse : 3 agents sur 3 avaient reproduit des formes « d'apres la description » sans les avoir regardees.
Ce projet ne porte pas les gabarits de brief du hub (`.claude/orchestration/prompts/`, canon du hub) : la regle est consignee ici, la correction du gabarit se fait au hub.
