"""Delta V35gA (base V34) : l'espace libere par le surtitre sert a aerer 30 slides de contenu (lot gA du chantier V35).

Aucun texte, aucune taille de police, aucune couleur, aucune image ne change : seule la geometrie VERTICALE du corps de chaque slide est refaite.
Le corps (tout sauf titre, pastilles de navigation « nav-* » et placeholders) est remonte vers y = 80 pt (~22 pt sous le titre) ; son bas ne bouge pas.
La hauteur gagnee devient de l'air :
- conteneurs (cartes, panneaux, bandeaux, lignes de tableau, hauteur > 26 pt) : hauteur x s ; centre porte par l'affine f(y) = haut_neuf + (y - haut_ancien) x s ;
- zones de texte, pilules <= 26 pt, chevrons : hauteur gardee, centre porte par f (le decalage dans le parent grandit : plus de marge) ;
- atomes rigides (pictogrammes ronds, pastilles numerotees, points, losanges, images et leur cadre, tout ce qu'ils contiennent) : taille gardee, centre porte par f ;
- traits fins verticaux : etires ; traits et connecteurs : chaque extremite suit la forme qu'elle touche ;
- slides dont la bande sous le titre porte deja une pastille d'etat (« A VALIDER ») : la pastille et le petit trait d'accent remontent a y = 61 et le corps remonte moins.
Usage (depuis docs/cadrage-ppt/) : py deck_delta/deck.py delta_V35gA --base C:/tmp/deck-v35/V35g.pptx --sortie C:/tmp/deck-v35-gA/V35gA.pptx --sans-rendu
"""
import deck_base
import deck_draw
from pptx import Presentation

BASE = "V34"
NOTE = "V35gA : 30 slides aerees, le corps remonte sous le titre (espace du surtitre retire), conteneurs et ecarts agrandis, atomes ronds intacts"
OPS = []

TITRES = [
    "Le guichet Infra atteint ses limites et l'IA accentue la pression",
    "Réussir : cinq conditions que nous posons avant de commencer",
    "Deux temps d'engagement : diagnostiquer, puis expérimenter et déployer",
    "Un planning hypothétique en trois phases, avant tout chiffrage",
    "Une boucle continue pour décider sur des faits, expérimenter et ancrer",
    "Calendrier du pilote : étapes et jalons, durées à valider",
    "De la douleur au produit : une mission pilote de bout en bout",
    "Le diagnostic s'appuie sur cinq piliers, du mode produit à l'agentic",
    "Exemples de livrables (1/2) : comprendre et décider",
    "Exemples de livrables (2/2) : piloter et ancrer",
    "Nous mesurons la valeur client et l'apport du coaching augmenté",
    "Deux comités en parallèle : l'un suit l'exécution, l'autre décide",
    "Ce que nous attendons de vous, et comment nous passons la main",
    "Du pilote à l'autonomie : trois modes d'interaction entre OCTO et le client",
    "L'IA est gouvernée : données, droits, validations et traçabilité",
    "Risques et objections : ce que nous répondons, ce que nous mesurons",
    "Un dispositif OCTO + client qui construit son propre relais",
    "Chiffrage : la forme du tableau jours × rôles, toutes valeurs à valider",
    "Problèmes 1 à 5 : chacun trouve son apport et son indicateur",
    "Problèmes 6 à 10 : chacun trouve son apport et son indicateur",
    "Les alternatives sont des compléments que l'offre intègre",
    "Qui décide quoi, quand entrer, quand passer la main : modèle d'engagement",
    "Infra agent-ready : une option selon la maturité, jamais un prérequis",
    "Chaque enjeu cité trouve sa réponse dans une partie de l'offre",
    "Fiche de phase : l'Assessment flash fixe la référence et choisit le pilote",
    "Fiche de phase type, appliquée au pilote : un gabarit pour chaque phase",
    "Fiche référence : un gabarit prêt à recevoir les références d'OCTO",
    "Le scénario déroule six étapes, du problème au choix du client",
    "Des agents augmentent le coach ; d'autres améliorent l'Infra du client",
    "Trois principes de conduite : le service, l'adoption, le binôme",
]

EMU = 12700
TOP_CIBLE = 80.0        # haut du corps visé (pt)
BAS_BANDE = 61.0        # haut de la pastille d'etat quand la bande en porte une (pt)
ECART_PASTILLE = 8.0    # air sous la pastille (pt)
S_MAX = 1.12            # etirement vertical maximal des conteneurs
H_CONTENEUR = 26.0      # au-dela, une forme qui en contient d'autres s'etire
TOL = 1.6               # tolerance de confinement (pt)
GAIN_MIN = 5.0          # sous ce gain (pt), la slide n'est pas touchee
FORMES_RONDES = {"ellipse", "donut", "blockArc", "pie", "chord", "arc", "circularArrow"}


def _geom(sh):
    g = sh._element.spPr.find("{http://schemas.openxmlformats.org/drawingml/2006/main}prstGeom")
    return g.get("prst") if g is not None else ""


def _boite(sh):
    return (sh.left / EMU, sh.top / EMU, (sh.left + sh.width) / EMU, (sh.top + sh.height) / EMU)


def _est_trait(sh):
    return sh._element.tag.endswith("}cxnSp")


def _contient(p, c, tol=TOL):
    return p[0] - tol <= c[0] and p[1] - tol <= c[1] and c[2] <= p[2] + tol and c[3] <= p[3] + tol


def _aire(b):
    return max(b[2] - b[0], 0.01) * max(b[3] - b[1], 0.01)


def _est_corps(sh):
    return not sh.name.startswith("nav-") and not sh.is_placeholder


def _texte(sh):
    return sh.text_frame.text.strip() if sh.has_text_frame else ""


def _entete(formes):
    """Formes de la bande sous le titre (pastille d'etat + son texte, petit trait d'accent), a part du corps."""
    pastille = [sh for sh in formes if 60 <= sh.top / EMU < 72 and sh.height / EMU <= 22 and not _est_trait(sh)]
    if not pastille:
        return [], []
    traits = [sh for sh in formes if sh not in pastille and abs(sh.left / EMU - 45) < 1 and 84 <= sh.top / EMU <= 92
              and sh.width / EMU <= 50 and sh.height / EMU <= 6]
    return pastille, traits


def plan(slide):
    """Calcule, sans rien ecrire, le plan de la slide : liste d'actions (forme, role, nouvelle boite) + parametres ; None si la slide n'a pas de gain."""
    formes = [sh for sh in slide.shapes if _est_corps(sh)]
    pastille, traits = _entete(formes)
    corps = [sh for sh in formes if sh not in pastille and sh not in traits]
    boites = {id(sh): _boite(sh) for sh in formes}
    haut_ancien = min(boites[id(sh)][1] for sh in corps)
    bas = max(boites[id(sh)][3] for sh in corps)
    if pastille:
        dy_entete = BAS_BANDE - min(boites[id(sh)][1] for sh in pastille)
        haut_vise = max(boites[id(sh)][3] for sh in pastille) + dy_entete + ECART_PASTILLE
    else:
        dy_entete = 0.0
        haut_vise = TOP_CIBLE
    if haut_ancien - haut_vise < GAIN_MIN:
        return None
    s = min((bas - haut_vise) / (bas - haut_ancien), S_MAX)
    haut_neuf = bas - s * (bas - haut_ancien)

    def f(y):
        return haut_neuf + (y - haut_ancien) * s

    # --- arbre de confinement
    idx = {id(sh): i for i, sh in enumerate(corps)}
    images = [boites[id(sh)] for sh in corps if sh._element.tag.endswith("}pic")]
    parent = {}
    for sh in corps:
        if _est_trait(sh):
            continue
        b = boites[id(sh)]
        meilleur = None
        for p in corps:
            if p is sh or _est_trait(p):
                continue
            pb = boites[id(p)]
            if not _contient(pb, b):
                continue
            meme = _contient(b, pb)
            if meme and idx[id(p)] > idx[id(sh)]:
                continue
            if not meme and _aire(pb) <= _aire(b):
                continue
            if meilleur is None or _aire(pb) < _aire(boites[id(meilleur)]) or (meme and _aire(pb) == _aire(boites[id(meilleur)]) and idx[id(p)] > idx[id(meilleur)]):
                meilleur = p
        parent[id(sh)] = meilleur
    enfants = {id(sh): [] for sh in corps}
    for sh in corps:
        p = parent.get(id(sh))
        if p is not None:
            enfants[id(p)].append(sh)

    def descendants(sh):
        for c in enfants[id(sh)]:
            yield c
            yield from descendants(c)

    def atome(sh):
        if _est_trait(sh):
            return False
        b = boites[id(sh)]
        w, h = b[2] - b[0], b[3] - b[1]
        if sh._element.tag.endswith("}pic"):
            return True
        if any(all(abs(b[i] - ib[i]) <= TOL for i in range(4)) for ib in images):   # cadre de l'image : meme boite
            return True
        if sh.has_text_frame and sh.shape_type is not None and "TEXT_BOX" in str(sh.shape_type):
            return False
        if not (0.7 <= w / max(h, 0.01) <= 1.43):
            return False
        if _geom(sh) in FORMES_RONDES and max(w, h) <= 110:
            return True
        longs = [d for d in [sh, *descendants(sh)] if len(_texte(d)) > 6]
        return max(w, h) <= 64 and not longs

    est_atome = {id(sh): atome(sh) for sh in corps}

    def racine_atome(sh):
        """Le plus haut atome parmi les ancetres-ou-soi, sinon None."""
        haut, cur = None, sh
        while cur is not None:
            if est_atome[id(cur)]:
                haut = cur
            cur = parent.get(id(cur))
        return haut

    delta_atome = {}
    for sh in corps:
        if est_atome[id(sh)]:
            b = boites[id(sh)]
            c = (b[1] + b[3]) / 2
            delta_atome[id(sh)] = f(c) - c

    def delta_pour_point(x, y, exclus):
        """Decalage a appliquer a une extremite de trait : celui de l'atome (ou du suiveur d'atome) qui la contient, sinon f(y) - y."""
        meilleur = None
        for p in corps:
            if p in exclus or _est_trait(p):
                continue
            b = boites[id(p)]
            if b[0] - 0.5 <= x <= b[2] + 0.5 and b[1] - 0.5 <= y <= b[3] + 0.5 and racine_atome(p) is not None:
                if meilleur is None or _aire(b) < _aire(boites[id(meilleur)]):
                    meilleur = p
        if meilleur is not None:
            return delta_atome[id(racine_atome(meilleur))]
        return f(y) - y

    actions = []   # (forme, haut_neuf_pt, hauteur_neuve_pt, flipV ou None)
    for sh in corps:
        b = boites[id(sh)]
        h = b[3] - b[1]
        w = b[2] - b[0]
        if _est_trait(sh):
            xf = sh._element.spPr.find("{http://schemas.openxmlformats.org/drawingml/2006/main}xfrm")
            fh = xf is not None and xf.get("flipH") in ("1", "true")
            fv = xf is not None and xf.get("flipV") in ("1", "true")
            x1, x2 = (b[2], b[0]) if fh else (b[0], b[2])
            y1, y2 = (b[3], b[1]) if fv else (b[1], b[3])
            r = None
            for p in corps:
                if not _est_trait(p) and est_atome[id(p)] and _contient(boites[id(p)], b, 0.5) and (r is None or _aire(boites[id(p)]) < _aire(boites[id(r)])):
                    r = p
            if r is not None:   # trait dessine DANS un atome (aiguille d'un pictogramme) : suit l'atome
                d = delta_atome[id(racine_atome(r))]
                actions.append((sh, b[1] + d, h, None))
                continue
            ny1 = y1 + delta_pour_point(x1, y1, (sh,))
            ny2 = y2 + delta_pour_point(x2, y2, (sh,))
            actions.append((sh, min(ny1, ny2), abs(ny2 - ny1), ny1 > ny2 if h >= 0.01 else None))
            continue
        racine = racine_atome(sh)
        if racine is not None:
            actions.append((sh, b[1] + delta_atome[id(racine)], h, None))
            continue
        c = (b[1] + b[3]) / 2
        texte_pur = "TEXT_BOX" in str(sh.shape_type)
        conteneur = bool(enfants[id(sh)]) and h > H_CONTENEUR
        fin_vertical = w <= 2.0 and h > 1.0 and not texte_pur
        vide_grand = (not _texte(sh)) and (not enfants[id(sh)]) and h >= 30 and not texte_pur
        if (conteneur or fin_vertical or vide_grand) and not texte_pur:
            actions.append((sh, f(b[1]), f(b[3]) - f(b[1]), None))
        else:
            actions.append((sh, f(c) - h / 2, h, None))
    entete_actions = [(sh, boites[id(sh)][1] + dy_entete, boites[id(sh)][3] - boites[id(sh)][1], None) for sh in pastille]
    entete_actions += [(sh, BAS_BANDE, boites[id(sh)][3] - boites[id(sh)][1], None) for sh in traits]   # le trait d'accent se cale sur le haut de la pastille
    return {"actions": actions + entete_actions, "s": s, "haut_ancien": haut_ancien, "haut_neuf": haut_neuf, "bas": bas,
            "parent": parent, "boites": boites, "corps": corps, "pastille": bool(pastille)}


def appliquer(slide):
    """Applique le plan ; renvoie (mode, s, haut_ancien, haut_neuf) ou None si la slide est laissee telle quelle."""
    p = plan(slide)
    if p is None:
        return None
    for sh, top, h, flip in p["actions"]:
        sh.top = round(top * EMU)
        sh.height = round(h * EMU)
        if flip is not None:
            xf = sh._element.spPr.find("{http://schemas.openxmlformats.org/drawingml/2006/main}xfrm")
            if flip:
                xf.set("flipV", "1")
            elif "flipV" in xf.attrib:
                del xf.attrib["flipV"]
    return ("stretch", p["s"], p["haut_ancien"], p["haut_neuf"])


def aerer(prs):
    """Etape unique : aere les 30 slides du lot."""
    rapport = {}
    for t in TITRES:
        rapport[t] = appliquer(deck_draw.slide_par_titre(prs, t))
    return rapport


def _ids():
    prs = Presentation(deck_base.resoudre_base(BASE))
    return [f"id:{deck_draw.slide_par_titre(prs, t).slide_id}" for t in TITRES]


ETAPES = [
    {"declarer": _ids(), "f": aerer, "nouvelles_max": 0, "nom": "30 slides aerees : corps remonte sous le titre, conteneurs et ecarts agrandis"},
]
