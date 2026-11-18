"""Delta V42a (base V41) : passe de charte transversale, alignée sur « Slides préformatées OCTO (1).pptx ».

Demande utilisateur du 2026-11-05 : « corrige tout » sur la revue de charte de V41
(docs/imports/references/slides-preformatees-octo/REVUE-CHARTE-V41.md). Cette étape ne corrige que
ce qui se règle SANS recomposer une slide : italiques, trait de cadre, texte noir/gris pâle, 7 pt.
Les reprises de composition (coins asymétriques, tableaux, colonnes) sont des deltas suivants.
Change par slide (toutes les formes `p:sp`, groupes compris ; connecteurs et images intacts) :
  - italique -> romain (réf. sl. 7 : citations entre guillemets, pas d'italique) ;
  - texte en 000000 ou CFD3DD -> navy 0E2356 (réf. : texte navy, jamais noir ni gris pâle) ;
  - trait de cadre > 0,75 pt -> 9525 EMU, trait gris CFD3DD -> navy (réf. : signature = 9525 navy) ;
  - texte à 7 pt -> 8 pt (le fil de chapitres du haut ; réf. : ~4 % des runs sous 8 pt).
Usage (depuis docs/cadrage-ppt/) : py deck_delta/deck.py delta_V42a --base V41 --sortie C:/tmp/deck-v42-a/V42a.pptx --sans-rendu
"""
from pptx.oxml.ns import qn

BASE = "V41"
NOTE = "V42a : charte transversale (italiques, trait 0,75 pt navy, texte navy, 7 pt -> 8 pt)"
OPS = []

NAVY = "0E2356"
TRAIT = 9525
TEXTE_A_REMPLACER = {"000000", "CFD3DD"}
COMPTES = {"italique": 0, "texte": 0, "trait": 0, "trait_couleur": 0, "taille": 0}


def _run_props(el):
    for e in el.iter(qn("a:rPr"), qn("a:defRPr"), qn("a:endParaRPr")):
        if e.get("i") == "1":
            e.set("i", "0")
            COMPTES["italique"] += 1
        if e.get("sz") == "700":
            e.set("sz", "800")
            COMPTES["taille"] += 1
        fill = e.find(qn("a:solidFill"))
        if fill is not None:
            c = fill.find(qn("a:srgbClr"))
            if c is not None and (c.get("val") or "").upper() in TEXTE_A_REMPLACER:
                c.set("val", NAVY)
                COMPTES["texte"] += 1


def _traits(sp):
    """Trait des formes (p:sp) ; les connecteurs (p:cxnSp) gardent leur épaisseur : une flèche n'est pas un cadre."""
    sppr = sp.find(qn("p:spPr"))
    ln = sppr.find(qn("a:ln")) if sppr is not None else None
    if ln is None:
        return
    w = ln.get("w")
    if w and int(w) > TRAIT:
        ln.set("w", str(TRAIT))
        COMPTES["trait"] += 1
    fill = ln.find(qn("a:solidFill"))
    c = fill.find(qn("a:srgbClr")) if fill is not None else None
    if c is not None and (c.get("val") or "").upper() == "CFD3DD":
        c.set("val", NAVY)
        COMPTES["trait_couleur"] += 1


def charte(prs):
    for s in prs.slides:
        racine = s._element
        _run_props(racine)
        for sp in racine.iter(qn("p:sp")):
            _traits(sp)
    print("V42a charte :", COMPTES)


def _tous_les_rangs():
    """Sélecteurs de rang de toutes les slides de la base (l'étape les déclare : elle les touche toutes)."""
    from pptx import Presentation

    import deck_base
    return [f"id:{s.slide_id}" for s in Presentation(deck_base.resoudre_base(BASE)).slides]


ETAPES = [{"declarer": _tous_les_rangs(), "f": charte, "nouvelles_max": 0,
           "nom": "charte : italiques, trait 0,75 pt navy, texte navy, 7 pt -> 8 pt"}]
