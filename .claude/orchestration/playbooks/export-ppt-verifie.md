# Playbook `export-ppt-verifie` — travaux sur le deck de restitution, vérifiés au rendu réel

La chaîne PPT complète de ce dépôt, rendue structurelle : produire ou faire évoluer le deck
`docs/cadrage-ppt/bmad-iap-cadrage-synthese.pptx` (via `generate_deck.py`/`pptx_deck.py`),
enrichir si pertinent (cadres photo du template OCTO, qualité rédactionnelle, passe design),
puis **toujours** vérifier au rendu réel — python-pptx est un parseur tolérant, un fichier
qui parse peut ne pas s'ouvrir correctement dans PowerPoint (cf. l'exigence déjà actée dans
CLAUDE.md : « le test ne remplace pas l'œil sur la qualité d'une photo, juste sur son
cadrage géométrique »).

Précédent réel sur ce dépôt (statut `eprouve` pour la colonne vertébrale) : la paire
génération → `test_generate_deck.py` → rendu réel a déjà été jouée pour rebâtir le deck sur
le vrai template OCTO (commit `1cb15fc`, cadres photo réels via `pptx-framed-image`). Les
étapes conditionnelles `slide-text-polish` et `restitution-deck-design` restent, elles,
`jamais-jouees` sur ce dépôt à ce jour — à proposer avec prudence explicite.

Routage de l'étape `generation` (arbitrage 2026-07-21) : elle s'instancie désormais via le
**sous-agent `ppt-designer`** (outil `Agent`), pas en génération inline dans la session —
le constat superviseur avait relevé que le deck avait été rebâti (`1cb15fc`) sans jamais
passer par cet agent pourtant désigné pilote. Modèle hérité du thread principal (pas de
bascule : jugement visuel, cf. CLAUDE.md). C'est la voie deck unique — `bmad-agent-ux-designer`
ne double pas ce rôle.

Frontière avec `dev-verifie` : si la demande est un changement de code générique (un hook,
un script de supervision/orchestration), c'est `dev-verifie` qui s'applique — ce
playbook-ci est la version spécialisée quand le **livrable est le deck lui-même** (layout,
contenu, visuel). Les deux partagent l'obligation de rendu réel et la terminaison
`revue-increment`.

```json
{
  "nom": "export-ppt-verifie",
  "description": "Production ou évolution du deck PPT de restitution : génération, enrichissements conditionnels (cadres photo, polish rédactionnel, passe design), vérification au rendu réel obligatoire, revue-increment avant commit.",
  "statut": "eprouve",
  "source": "manuel",
  "declencheurs": [
    "génère/améliore/corrige le deck PPT de cadrage BMAD IAP (docs/cadrage-ppt/)",
    "changement de layout, de contenu ou de slide dans generate_deck.py / pptx_deck.py",
    "remplir les cadres photo (« ici mettre une Photo ») du template OCTO",
    "qualité rédactionnelle / design des slides du deck"
  ],
  "etapes": [
    {
      "id": "cadrage",
      "agent": "session principale",
      "mode": "cascade",
      "modele": "(session)",
      "contrat": {
        "type": "deterministe",
        "critere": "contenu de cadrage/synthèse identifié, template OCTO ou deck existant relu, wiki/mémoires consultés avant de re-dériver un contexte déjà écrit (discipline tokens du CLAUDE.md)"
      },
      "checkpoint": false
    },
    {
      "id": "generation",
      "agent": "ppt-designer",
      "mode": "cascade",
      "modele": "(session)",
      "contrat": {
        "type": "deterministe",
        "critere": "instancié via le sous-agent ppt-designer (outil Agent), pas inline ; export .pptx produit sans exception, self-check géométrique de pptx_deck.py passé, test_generate_deck.py vert (structure, cadres photo alignés, régression numéro de chapitre)"
      },
      "checkpoint": false
    },
    {
      "id": "cadres-photo",
      "agent": "pptx-framed-image",
      "mode": "cascade",
      "modele": "(session)",
      "contrat": {
        "type": "deterministe",
        "critere": "SI un cadre photo (prstGeom round2DiagRect, « ici mettre une Photo ») est touché : image insérée épousant la forme exacte du cadre, provenance journalisée dans images-manifest.json, chaque photo vérifiée par rendu réel avant d'être gardée (la recherche par mot-clé n'a aucun jugement)"
      },
      "checkpoint": false
    },
    {
      "id": "polish-texte",
      "agent": "slide-text-polish",
      "mode": "cascade",
      "modele": "(session)",
      "contrat": {
        "type": "deterministe",
        "critere": "SI le contenu textuel des slides a été produit ou retouché : slide_lint passé sur {title, bullets}, findings bloquants corrigés (skill jamais utilisée à ce jour sur ce dépôt — prudence, contrôler à l'étape verification-rendu)"
      },
      "checkpoint": false
    },
    {
      "id": "verification-rendu",
      "agent": "pptx-verify",
      "mode": "cascade",
      "modele": "(session)",
      "contrat": {
        "type": "reel",
        "critere": "export réel rendu en images (LibreOffice/COM) et inspecté visuellement, avec un rendu ZOOMÉ sur chaque NOUVEAU type de slide (valeurs alignées, panneaux ni vides ni sur-étirés, ni contenu centré par slot laissant un grand vide sous l'en-tête — défaut « panneau flottant/étiré » récurrent, invisible au self-check géométrique, cf. constat superviseur 2026-07-21 / commit a8b264a, pas de collision avec le chrome du template) — jamais retirée à l'instanciation, quelle que soit la taille du changement"
      },
      "checkpoint": false
    },
    {
      "id": "design-review",
      "agent": "restitution-deck-design",
      "mode": "cascade",
      "modele": "(session)",
      "contrat": {
        "type": "reel",
        "critere": "SI le rendu passe la géométrie mais reste visuellement pauvre (mur de boîtes, hiérarchie absente) : passe design appliquée puis retour à verification-rendu (skill jamais utilisée à ce jour sur ce dépôt — prudence)"
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
        "critere": "SI du code produit a été modifié (generate_deck.py, pptx_deck.py) : boucle revue + correctifs + re-vérification exécutée en entier"
      },
      "checkpoint": "avant tout commit — action difficilement réversible, proposer, ne pas exécuter unilatéralement"
    }
  ],
  "regle_reprise": "une relance ciblée par étape en échec de contrat, puis escalade utilisateur avec l'état réel"
}
```
