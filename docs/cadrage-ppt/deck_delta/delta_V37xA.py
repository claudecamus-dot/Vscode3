"""Delta V37xA (base V36) : doublons du titre retires (rang 20 et audit des rubriques qui redisent le titre).

Demande : « dans toutes les slides supprimer les doublons de ce qui est ecrit dans le titre comme le mot conviction et dans la slide 20 le mot condition ».
- slide « Reussir : cinq conditions... » : les cinq pastilles « LA CONDITION » (forme + texte, sur le bord haut de chaque carte) sont retirees ; la grille, les cartes, les numeros,
  les pastilles « Boucle : ... » et le bloc cyan « PROPOSITION » (drapeau d'hypothese) restent a leur place ;
- slide « Votre demande, notre reponse en trois temps » : l'en-tete « NOTRE RÉPONSE EN TROIS TEMPS » (redit mot pour mot la fin du titre) et son filet cyan sont retires ;
  les trois etapes sont redistribuees sur la hauteur du panneau navy (meme pas entre elles, trait de liaison recale) ;
- chaque retrait est note dans les notes sous « Doublon du titre retire ».
Les autres doublons candidats (en-tetes utiles qui echo le titre, bandeau de navigation) sont des arbitrages laisses a l'utilisateur : rien d'autre n'est touche.
Usage (depuis docs/cadrage-ppt/) : py deck_delta/deck.py delta_V37xA --base V36 --sortie C:/tmp/deck-v37-xA/V37xA.pptx --sans-rendu
"""
import deck_base
import deck_draw
from pptx import Presentation

BASE = "V36"
NOTE = "V37xA : pastilles « LA CONDITION » retirees (slide cinq conditions) ; en-tete « NOTRE RÉPONSE EN TROIS TEMPS » retire (slide 2), doublons du titre"
OPS = []

NB = "\u00a0"
EMU = 12700
T20 = "Réussir : cinq conditions que nous posons avant de commencer"
T02 = "Votre demande, notre réponse en trois temps : du guichet au produit"


def _slide(titre):
    prs = Presentation(deck_base.resoudre_base(BASE))
    return deck_draw.slide_par_titre(prs, titre)


def _notes(s, ajout):
    ancien = s.notes_slide.notes_text_frame.text if s.has_notes_slide else ""
    s.notes_slide.notes_text_frame.text = (ancien + "\n" if ancien else "") + ajout


def _retirer(sh):
    sh._element.getparent().remove(sh._element)


def conditions(prs):
    s = deck_draw.slide_par_titre(prs, T20)
    pastilles = [sh for sh in s.shapes if sh.name.startswith("pastille-rubrique") and sh.has_text_frame and sh.text_frame.text.strip() == "LA CONDITION"]
    if len(pastilles) != 5:
        raise ValueError(f"pastilles « LA CONDITION » : {len(pastilles)} ; 5 exigees")
    for sh in pastilles:
        _retirer(sh)
    # sans pastille, le haut de carte respire : numeros et textes remontent de 6 pt (la 3e ligne des cartes 4 et 5 se detache de la pastille « Boucle »)
    ids = {7, 8, 10, 11, 13, 14, 16, 17, 19, 20}
    for sh in s.shapes:
        if sh.shape_id in ids:
            sh.top = sh.top - 6 * EMU
    _notes(s, "Doublon du titre retiré" + NB + ": pastille « LA CONDITION » sur chacune des cinq cartes (le titre dit déjà « cinq conditions »). "
              "Le bloc « PROPOSITION » (drapeau d'hypothèse) reste.")


def reponse_en_trois_temps(prs):
    s = deck_draw.slide_par_titre(prs, T02)
    by = {sh.shape_id: sh for sh in s.shapes}
    entete, filet = by[47], by[48]
    if entete.text_frame.text.strip() != "NOTRE RÉPONSE EN TROIS TEMPS":
        raise ValueError("en-tete attendu absent")
    _retirer(entete)
    _retirer(filet)
    # trois etapes (rond, numero, texte) redistribuees : pas 62 pt (au lieu de 56), premiere a y 108
    for k, (rond, num, texte) in enumerate(((50, 51, 52), (53, 54, 55), (56, 57, 58))):
        y = 108 + k * 62
        by[rond].top = int(y * EMU)
        by[num].top = int(y * EMU)
        by[texte].top = int((y - 1) * EMU)
    trait = by[49]  # liaison entre les ronds : du centre du premier au centre du dernier
    trait.top = int((108 + 17) * EMU)
    trait.height = int(124 * EMU)
    _notes(s, "Doublon du titre retiré" + NB + ": en-tête « NOTRE RÉPONSE EN TROIS TEMPS » (et son filet) du panneau navy, mot pour mot dans le titre. "
              "Les trois étapes sont redistribuées sur la hauteur du panneau.")


def _ids():
    prs = Presentation(deck_base.resoudre_base(BASE))
    return [f"id:{deck_draw.slide_par_titre(prs, t).slide_id}" for t in (T20, T02)]


_I20, _I02 = _ids()
ETAPES = [
    {"declarer": [_I20], "f": conditions, "nouvelles_max": 0, "nom": "cinq conditions : pastilles « LA CONDITION » retirees (doublon du titre)"},
    {"declarer": [_I02], "f": reponse_en_trois_temps, "nouvelles_max": 0, "nom": "slide 2 : en-tete « NOTRE RÉPONSE EN TROIS TEMPS » retire (doublon du titre), etapes redistribuees"},
]
