"""Delta V35t (base V34) : « T0 » et « T1 » ne sont expliques que sur la slide de mesure ; partout ailleurs ils deviennent des mots simples.

Demande : « dans les autres slides sauf la slide ou on explique T0 et T1, sinon supprimer car on ne comprend pas ».
- la slide « Nous mesurons la valeur client… » garde T0 et T1 (colonnes « Reference T0 », « Resultat T1 ») et les DEFINIT dans sa phrase d'accroche ;
- 14 autres slides : T0 -> « reference de depart » / « situation de depart » / « avant », T1 -> « resultats mesures » / « apres » (remplacement au niveau du run : la mise en forme est conservee) ;
- les slides « Votre demande… » et « Conviction 1… » sont traitees par le lot sA (refonte).
Chaque remplacement doit s'appliquer exactement une fois : sinon l'etape echoue (pas de remplacement silencieux manque).
Usage (depuis docs/cadrage-ppt/) : py deck_delta/deck.py delta_V35t --base V34 --sortie C:/tmp/deck-v35/V35t.pptx --sans-rendu
"""
import re

import deck_base
from pptx import Presentation

BASE = "V34"
NOTE = "V35t : T0 et T1 retires hors de la slide de mesure (qui les definit)"
NB = "\u00a0"

# prefixe du titre -> [(ancien, nouveau)] ; ancien est cherche dans les runs de toutes les formes de la slide
REMPLACEMENTS = {
    "Conviction 11 : piloter": [
        ("Ce que nous suivons, T0 → T1", "Ce que nous suivons, avant → après"),
        ("mesuré au T0 puis au T1", "mesuré avant, puis après"),
    ],
    "L'IA apporte au coach": [(" gains à mesurer au T0 puis au T1", " gains à mesurer avant, puis après")],
    "Un planning hypothétique": [("indicateurs T0 → T1", "indicateurs avant → après")],
    "Calendrier du pilote": [
        ("baseline au T0", "situation de départ"),
        ("Mesure au T1 et décision", "Mesure des résultats et décision"),
    ],
    "De la douleur au produit": [
        ("T0 et T1 à mesurer", "référence et résultat à mesurer"),
        ("fixe la référence au T0", "fixe la référence de départ"),
        ("T0" + NB + ": À MESURER", "AVANT"),  # pastilles trop etroites pour « AVANT : A MESURER » ; « a mesurer » reste dit par la legende de l'encart
        ("T1" + NB + ": À MESURER", "APRÈS"),
        ("mesurés au T1, jamais présumés", "mesurés après le pilote, jamais présumés"),
    ],
    "Exemples de livrables (1/2)": [("l'état de départ (T0) pour", "l'état de départ pour")],
    "Exemples de livrables (2/2)": [("du T0 au T1.", "avant puis après.")],
    # la slide de mesure DEFINIT T0 et T1 : sa phrase d'accroche porte la definition
    "Nous mesurons la valeur client": [("Référence documentée au T0, résultats et écarts évalués au T1" + NB + "; la contribution de l'IA est ",
                                        "État de départ (T0) documenté, résultat (T1) mesuré en fin de pilote" + NB + "; la contribution de l'IA est ")],
    "Risques et objections": [
        ("référence au T0, résultats au T1", "référence de départ, résultats mesurés"),
        ("Écart entre T0 et T1", "Écart entre avant et après"),
    ],
    "Problèmes 1 à 5": [("suivis au T0 et au T1", "suivis avant, puis après")],
    "Problèmes 6 à 10": [("suivis au T0 et au T1", "suivis avant, puis après")],
    "Chaque enjeu cité": [("Référence au T0, résultats au T1, valeur mesurée", "Référence de départ, résultats, valeur mesurée")],
    "Fiche de phase : l'Assessment flash": [
        ("la référence au T0 et choisir", "la référence de départ et choisir"),
        ("baseline au T0, pilote", "situation de départ, pilote"),
    ],
    "Fiche de phase type": [
        ("une référence au T0", "une référence de départ"),
        ("Mesure au T1 et recommandation", "Mesure et recommandation"),  # « Mesure des resultats… » passait sur une ligne de plus que la boite
    ],
    "Le scénario déroule six étapes": [
        ("Problème et T0", "Problème et référence"),
        ("Mesure au T1", "Mesure des résultats"),
    ],
}


def _titre(s):
    return s.shapes.title.text_frame.text if s.shapes.title is not None else ""


def _slide(prs, prefixe):
    trouvees = [s for s in prs.slides if _titre(s).startswith(prefixe)]
    if len(trouvees) != 1:
        raise ValueError(f"titre commençant par « {prefixe} » : {len(trouvees)} slides, 1 attendue")
    return trouvees[0]


def _ids():
    prs = Presentation(deck_base.resoudre_base(BASE))
    return [f"id:{_slide(prs, p).slide_id}" for p in REMPLACEMENTS]


def _runs(s):
    for sh in s.shapes:
        if sh.has_text_frame:
            for p in sh.text_frame.paragraphs:
                yield from p.runs


def retirer_t0_t1(prs):
    for prefixe, paires in REMPLACEMENTS.items():
        s = _slide(prs, prefixe)
        for ancien, nouveau in paires:
            faits = 0
            for r in _runs(s):
                if ancien in r.text:
                    r.text = r.text.replace(ancien, nouveau)
                    faits += 1
            if faits != 1:
                raise ValueError(f"« {prefixe} » : « {ancien} » trouve {faits} fois (1 attendue)")
    # garde : T0 / T1 ne subsistent que sur la slide de mesure (et sur les slides refaites par sA : 2 et 10)
    for s in prs.slides:
        t = _titre(s)
        if t.startswith(("Nous mesurons la valeur client", "Votre demande", "Conviction 1 :")):
            continue
        restes = [r.text for r in _runs(s) if re.search(r"\bT[01]\b", r.text)]
        if restes:
            raise ValueError(f"T0/T1 restant sur « {t} » : {restes}")


ETAPES = [{"declarer": _ids(), "f": retirer_t0_t1, "nouvelles_max": 0, "nom": "T0 et T1 retires hors de la slide de mesure, definis sur celle-ci"}]
OPS = []
