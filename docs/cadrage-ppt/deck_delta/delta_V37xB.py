"""Delta V37xB (base V36) : slide « Deux temps d'engagement » : plus de « Conduit par », plus de pastille jalon ; chaque carte porte une liste a coches des activites principales.

- retire les trois lignes « Conduit par : … » et la pastille cyan « JALON : RESTITUTION DU SPONSOR » (texte mot pour mot dans les notes) ;
- remplace le paragraphe de chaque carte par 4 puces a coche (11 pt) ; les cartes s'allongent un peu, la ligne « Financement : … » reste dessous.
Usage (depuis docs/cadrage-ppt/) : py deck_delta/deck.py delta_V37xB --base V36 --sortie C:/tmp/deck-v37-xB/V37xB.pptx --sans-rendu
"""
import deck_base
import deck_draw
from forme_ground import NAVY, A, P, coche, tx
from pptx import Presentation

BASE = "V36"
NOTE = "V37xB : slide Deux temps d'engagement : Conduit par et jalon retires, puces d'activites"
OPS = []

NB = "\u00a0"
TITRE = "Deux temps d'engagement : diagnostiquer, puis expérimenter et déployer"
EMU_PT = 12700
HAUT_CARTE = 198
SZ = 11
PAS_LIGNE = 13.6
ECART = 5.0

CARTES = (
    ("Assessment flash", [
        ("Diagnostic et cartographie des opportunités", 2),
        ("Interviews, baseline documentée", 2),
        ("Coût du statu quo estimé si calculable", 2),
        ("Choix d'un pilote. Aucun ROI promis.", 2),
    ]),
    ("Pilote Produit + IA", [
        ("Dimensionné à l'issue de l'Assessment flash", 2),
        ("Une boucle complète, de Explorer à Ancrer", 2),
        ("On n'enchaîne que ce que le pilote justifie", 2),
        ("Assainissement déclenché par le diagnostic", 2),
    ]),
    ("Ancrage", [
        ("Relais internes formés", 1),
        ("Indicateurs tenus par le client", 1),
        ("Plan de passage de main", 1),
        ("Extension éventuelle selon les résultats du pilote", 2),
    ]),
)
RETIRES_DEBUT = ("Conduit par", "JALON")


def _ids():
    return [f"id:{deck_draw.slide_par_titre(Presentation(deck_base.resoudre_base(BASE)), TITRE).slide_id}"]


def _retirer(sh):
    sh._element.getparent().remove(sh._element)


def refondre(prs):
    s = deck_draw.slide_par_titre(prs, TITRE)
    retires = []
    # 1) lignes « Conduit par » et pastille jalon (texte + fond de la pastille)
    for tb in [x for x in s.shapes if x.has_text_frame and x.text_frame.text.startswith(RETIRES_DEBUT)]:
        retires.append(tb.text_frame.text)
        if tb.text_frame.text.startswith("JALON"):
            fond = next(x for x in s.shapes if x is not tb and x.shape_type == 1 and not x.text_frame.text
                        and x.top == tb.top and x.height == tb.height and x.left <= tb.left)
            _retirer(fond)
        _retirer(tb)
    if len(retires) != 4:
        raise ValueError(f"{len(retires)} textes retires au lieu de 4 : {retires}")
    # 2) paragraphes des cartes -> puces
    cartes = sorted((x for x in s.shapes if "Diagonal" in x.name and x.height > 150 * EMU_PT), key=lambda x: x.left)
    if len(cartes) != 3:
        raise ValueError(f"{len(cartes)} cartes au lieu de 3")
    for carte, (titre, puces) in zip(cartes, CARTES, strict=True):
        titre_tb = next(x for x in s.shapes if x.has_text_frame and x.text_frame.text == titre)
        para = next(x for x in s.shapes if x.has_text_frame and x.top > titre_tb.top and x.left > carte.left
                    and x.left < carte.left + carte.width and len(x.text_frame.text) > 40 and x is not titre_tb)
        _retirer(para)
        carte.height = HAUT_CARTE * EMU_PT
        x0 = carte.left / EMU_PT
        y = 209.0
        for texte, nl in puces:
            coche(s, x0 + 21, y + 7, 13)
            tx(s, x0 + 35, y, 148, PAS_LIGNE * nl, [[(texte, SZ, False, NAVY)]], A.TOP, P.LEFT)
            y += PAS_LIGNE * nl + ECART
    # 3) ligne Financement sous les cartes
    fin = next(x for x in s.shapes if x.has_text_frame and x.text_frame.text.startswith("Financement"))
    fin.top = int((cartes[0].top + HAUT_CARTE * EMU_PT) + 4 * EMU_PT)
    notes = s.notes_slide.notes_text_frame
    notes.text = (notes.text + "\n\n" if notes.text else "") + (
        "Retire de la slide (demande de supprimer « conduit par OCTO et le client » et le jalon) :\n"
        "- Assessment flash : « Conduit par" + NB + ": OCTO. Décide" + NB + ": le" + NB + "client. »\n"
        "- Pilote Produit + IA : « Conduit par" + NB + ": OCTO et le client ensemble. »\n"
        "- Ancrage : « Conduit par" + NB + ": le client, avec ses" + NB + "relais. » ; pastille « JALON" + NB + ": RESTITUTION DU SPONSOR »\n"
        "Les phrases des cartes sont reprises en puces (activités principales) : le texte intégral d'origine reste dans la première note ci-dessus ; "
        "puces ajoutées tirées de la slide « Fiche de phase : l'Assessment flash fixe la référence et choisit le pilote » (interviews), "
        "de la « Fiche de phase type, appliquée au pilote » (une boucle complète, de Explorer à Ancrer) et du planning (plan de passage de main).")


ETAPES = [{"declarer": _ids(), "f": refondre, "nouvelles_max": 0, "nom": "deux temps : puces d'activites, sans Conduit par ni jalon"}]
