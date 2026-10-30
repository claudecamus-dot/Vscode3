"""Resolution unique de la base d'un delta et du nom de la version suivante.

Convention VSCode3 : `docs/exports/decks/offre-infra-as-a-product-V<N>.pptx` (V1, V2, ... V10).
Le tri est NUMERIQUE (V10 > V9) ; un tri lexical placerait V9 apres V10. Les fichiers `~$` (ouverts dans PowerPoint) et hors convention sont ignores.
Port adapte de Vscode8 `scripts/deck_base.py` (suffixe `_vN.M` remplace par `-V<N>`). Ce module ne connait ni slides, ni gardes, ni rendu : il resout des chemins.
Aucun chemin de version ni nombre de slides en dur : le dossier se deduit de l'emplacement du module.
"""
import os
import re
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
LIVRABLES = os.path.join(RACINE, "docs", "exports", "decks")
_VERSION = re.compile(r"^(offre-infra-as-a-product-)V(\d+)\.pptx$", re.IGNORECASE)


def cle_version(nom):
    """10 pour « offre-infra-as-a-product-V10.pptx » ; None si le nom ne suit pas la convention (ou commence par `~$`)."""
    m = _VERSION.match(nom)
    return int(m.group(2)) if m else None


def versions(dossier=LIVRABLES):
    """[(N, chemin)] des livrables du dossier, du plus ancien au plus recent (tri numerique)."""
    sortie = []
    for nom in os.listdir(dossier):
        chemin = os.path.join(dossier, nom)
        cle = cle_version(nom)
        if cle is not None and os.path.isfile(chemin):
            sortie.append((cle, chemin))
    return sorted(sortie)


def dernier_livrable(dossier=LIVRABLES):
    """(chemin, N) du livrable de plus grand N ; ValueError s'il n'y en a aucun."""
    v = versions(dossier)
    if not v:
        raise ValueError(f"aucun livrable « offre-infra-as-a-product-V<N>.pptx » dans {dossier}")
    cle, chemin = v[-1]
    return chemin, cle


def resoudre_base(base=None, dossier=LIVRABLES):
    """Chemin de la base : None = dernier livrable ; « V4 », « v4 » ou « 4 » = cette version du dossier ; sinon un fichier .pptx existant."""
    if base is None:
        return dernier_livrable(dossier)[0]
    if os.path.isfile(base):
        return base
    m = re.fullmatch(r"[vV]?(\d+)", str(base))
    if m:
        voulue = int(m.group(1))
        for cle, chemin in versions(dossier):
            if cle == voulue:
                return chemin
    raise ValueError(f"base introuvable : {base!r} (ni fichier, ni version de {dossier})")


def version_suivante(n):
    """9 -> 10."""
    return int(n) + 1


def chemin_sortie(dossier=LIVRABLES):
    """Chemin de la version suivante = DERNIER livrable + 1 (jamais « base + 1 » : une base plus ancienne ne doit pas reprendre un numero existant).
    ValueError si le fichier existe deja : on n'ecrase jamais un livrable."""
    dernier, n = dernier_livrable(dossier)
    prefixe = _VERSION.match(os.path.basename(dernier)).group(1)
    sortie = os.path.join(dossier, f"{prefixe}V{version_suivante(n)}.pptx")
    if os.path.exists(sortie):
        raise ValueError(f"la version suivante existe deja : {sortie} (un livrable n'est jamais ecrase)")
    return sortie


def core():
    """`pptx_deck_core` du hub (canon de .claude/skills/pptx-deck/scripts, JAMAIS modifie ici). `append` : les modules de deck_delta/ gardent la priorite."""
    skill = os.path.join(RACINE, ".claude", "skills", "pptx-deck", "scripts")
    if skill not in sys.path:
        sys.path.append(skill)
    import pptx_deck_core
    return pptx_deck_core
