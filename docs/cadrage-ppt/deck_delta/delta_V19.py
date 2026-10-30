"""Delta V19 (base V18) : suite des demandes (« ok continue » apres le comite, 2026-10-29).

- convictions : nouvelle slide « Trois principes de conduite » au format « X plutot que Y » (releve dans un support OCTO/AG2R, slide 16) qui porte les trois convictions
  absentes que le comite a relevees dans le plus de decks : premier service puis extension, adoption plutot que livraison, binome plateforme-consommateurs. Formulations
  nouvelles, aucune donnee ni nom de client, marquees « proposition a valider ».
- « Prochain pas » : le gradin cyan / gris / navy (la couleur y portait le sens) est remplace par trois cartes a en-tete (modele AGIMA 35, delta_V14).
- convictions 4 et 5 : la boite de texte du panneau « regle de passage » depassait du panneau.
Non fait : chapitres « Equipe et modalites » et « References » (le sommaire n'a que 7 pastilles numerotees fixes et l'equipe est deja dans « Dispositif et prix » : arbitrage a prendre).
"""
import re

import deck_base
import deck_draw
from delta_V9 import EMU
from delta_V10 import sections
from delta_V11 import navigation_8
from delta_V16 import carte
from pptx import Presentation
from pptx.enum.text import PP_ALIGN

BASE = "V18"
NOTE = "V19 : trois principes de conduite, Prochain pas en cartes a en-tete"
OPS = []

T_MODELE = "Une conviction, un critère, un chantier : 4 et 5"
T_PRINCIPES = "Trois principes de conduite : le service, l'adoption, le binôme"
T_PROCHAIN = "Prochain pas : choisir un périmètre, mesurer, tester, puis nous contacter"

PRINCIPES = [
    ("Un premier service plutôt qu'un grand programme",
     "Une ambition de plateforme, un premier service livré vite à une équipe réelle, puis l'extension selon les résultats.",
     "Un programme long dont la valeur n'apparaît qu'à la fin.",
     "Le premier service est utilisé par une équipe consommatrice."),
    ("L'adoption mesurée plutôt que la livraison annoncée",
     "Nous suivons l'usage de chaque capacité, pas seulement sa mise en production.",
     "Une plateforme livrée que personne n'utilise.",
     "Taux d'adoption et usages hors plateforme."),
    ("Un binôme plateforme et consommateurs plutôt qu'un guichet",
     "Le consommateur est légitime sur le besoin, l'équipe plateforme sur le comment ; chacun conseille l'autre.",
     "Un guichet qui reçoit des demandes sans comprendre l'usage.",
     "Un propriétaire nommé de chaque côté."),
]
ETAPES_PROCHAIN = [
    ("1  Choisir", "Un sponsor et des objectifs clairs pour un périmètre utile."),
    ("2  Diagnostiquer", "Accès aux personnes et aux données autorisées ; référence mesurée au T0."),
    ("3  Tester", "Une capacité dédiée aux décisions et à l'expérimentation."),
]
A_RETIRER = {"corps-carte", "entete-carte", "pastille-rubrique", "texte-carte", "panneau-regle"}


def _gauche(s):
    for sh in s.shapes:
        if sh.name in ("texte-carte", "entete-carte") and sh.has_text_frame:
            for p in sh.text_frame.paragraphs:
                p.alignment = PP_ALIGN.LEFT


def principes(prs):
    modele = deck_draw.slide_par_titre(prs, T_MODELE)
    rang = list(prs.slides).index(modele)
    s = deck_base.core().copier_slide(prs, modele, index=rang + 1)
    for sh in list(s.shapes):
        texte = sh.text_frame.text if sh.has_text_frame else ""
        if sh.name in A_RETIRER or texte.startswith(("RÈGLE", "Une capacité entre")):
            sh._element.getparent().remove(sh._element)
    deck_draw.set_run(next(sh for sh in s.shapes if sh.is_placeholder), T_PRINCIPES)
    w, gap = 195, 14.5
    for k, (titre, fait, evite, verifie) in enumerate(PRINCIPES):
        carte(s, 45 + k * (w + gap), 112, w, 235, 52, titre,
              [("CE QUE NOUS FAISONS", fait), ("CE QUE NOUS ÉVITONS", evite), ("COMMENT NOUS LE VÉRIFIONS", verifie)], tag=f"PRINCIPE {k + 1}")
    _gauche(s)


def prochain_pas(prs):
    s = deck_draw.slide_par_titre(prs, T_PROCHAIN)
    formes = list(s.shapes)
    for j in range(1, 10):  # gradin (3 aplats + 6 textes)
        formes[j]._element.getparent().remove(formes[j]._element)
    w, gap = 195, 14.5
    for k, (titre, texte) in enumerate(ETAPES_PROCHAIN):
        carte(s, 45 + k * (w + gap), 104, w, 112, 30, titre, [("CE QU'IL FAUT RÉUNIR", texte)])
    _gauche(s)


def panneau(prs):
    s = deck_draw.slide_par_titre(prs, T_MODELE)
    for sh in s.shapes:
        if sh.has_text_frame and sh.text_frame.text.startswith("Une capacité entre"):
            sh.height = 116 * EMU


def retouche(prs):
    principes(prs)
    prochain_pas(prs)
    panneau(prs)
    navigation_8(prs)
    sections(prs)


def _ids():
    return [f"id:{s.slide_id}" for s in Presentation(deck_base.resoudre_base(BASE)).slides]


ETAPES = [{"declarer": _ids(), "f": retouche, "nouvelles_max": 1, "nom": "principes de conduite, Prochain pas en cartes"}]
