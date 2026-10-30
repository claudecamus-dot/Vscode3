"""Delta V14 (base V13) : cartes a en-tete et pastille de rubrique, d'apres le deck AGIMA 2026 (slide 35 « Les activites du cadrage 360 »).

Geometrie relevee sur AGIMA 35 (python-pptx, 720 x 405 pt) : corps de carte = rectangle arrondi blanc au trait navy fin ; en-tete = rectangle a deux coins hauts arrondis,
de la LARGEUR du corps, 30 pt de haut, titre 9 pt ; pastille de rubrique = rectangle arrondi blanc cerne de navy, 32 x 18 pt, a cheval sur le bord haut a droite, texte 5,25 pt gras.
Application : les trois slides a cinq cartes numerotees (convictions, conditions de reussite, IA) ; l'etiquette (« LA CIBLE », « LA DEMARCHE », « LA CONDITION ») devient la pastille,
le titre devient l'en-tete, le reste (« dans la demarche : ... ») reste dans le corps. Un seul accent cyan par slide : celui du lisere de la phrase d'intro (le trait cyan de la carte 1 disparait).
Usage (depuis docs/cadrage-ppt/) : py deck_delta/deck.py delta_V14 --base V13
"""
import re

import deck_draw
from delta_V9 import BLANC, EMU, MUTED, NAVY, POLICE
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Pt

BASE = "V13"
NOTE = "V14 : cartes a en-tete et pastille de rubrique (modele AGIMA 35) sur les slides a cinq cartes"
OPS = []

T_CONV = "Cinq convictions : une cible à construire et une démarche pour y conduire"
T_REUSSIR = "Réussir : cinq conditions que nous posons avant de commencer"
T_IA = "L'IA apporte au coach du temps et de la matière, pas la décision"
HAUT_ENTETE = 36 * EMU
A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"


def _texte(sh, texte, taille, couleur, gras=True, align=PP_ALIGN.LEFT, ancre=MSO_ANCHOR.MIDDLE, marges=(8, 3)):
    tf = sh.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Pt(marges[0])
    tf.margin_top = tf.margin_bottom = Pt(marges[1])
    tf.vertical_anchor = ancre
    p = tf.paragraphs[0]
    p.alignment = align
    r = p.add_run()
    r.text = texte
    r.font.size, r.font.bold, r.font.name = Pt(taille), gras, POLICE
    r.font.color.rgb = couleur


def _coins_bas_seuls(forme, rayon):
    geom = forme._element.spPr.find(f"{A}prstGeom")
    geom.set("prst", "round2SameRect")
    for gd in list(geom.find(f"{A}avLst")):
        geom.find(f"{A}avLst").remove(gd)
    forme.adjustments[0] = 0
    forme.adjustments[1] = min(0.5, rayon / min(forme.width, forme.height))


def _cartes(s):
    """Les cartes a cinq numeros : rectangles arrondis blancs de 195 x 97 pt, avec leur numero et leur bloc d'etiquette."""
    formes = list(s.shapes)
    cartes = [c for c in formes if c.name.startswith("Rounded Rectangle") and abs(c.width - 195 * EMU) < 3 * EMU and abs(c.height - 97 * EMU) < 3 * EMU
              and c.fill.type == 1 and str(c.fill.fore_color.rgb) == "FFFFFF"]
    sortie = []
    for c in cartes:
        dedans = [t for t in formes if t.has_text_frame and c.left <= t.left < c.left + c.width and c.top <= t.top < c.top + c.height]
        numero = next(t for t in dedans if re.fullmatch(r"\d", t.text_frame.text))
        texte = next(t for t in dedans if "\n" in t.text_frame.text)
        liseres = [t for t in formes if t.name.startswith("Rectangle") and t.height <= 5 * EMU and t.left > c.left and t.top == c.top]
        sortie.append((c, numero, texte, liseres))
    return sortie


def cartes_entete(prs):
    for titre in (T_CONV, T_REUSSIR, T_IA):
        s = deck_draw.slide_par_titre(prs, titre)
        trouvees = _cartes(s)
        if len(trouvees) != 5:
            raise ValueError(f"{titre!r} : {len(trouvees)} carte(s) numerotee(s), 5 exigees")
        for carte, numero, texte, liseres in trouvees:
            paras = list(texte.text_frame.paragraphs)
            etiquette, titre_carte, reste = paras[0].text, paras[1].text, paras[2:]
            x, y, w = carte.left, carte.top, carte.width
            for lis in liseres:
                lis._element.getparent().remove(lis._element)
            carte.line.color.rgb = NAVY
            carte.line.width = Pt(0.75)
            _coins_bas_seuls(carte, 12 * EMU)
            entete = deck_draw.rect(s, x / EMU, y / EMU, w / EMU, HAUT_ENTETE / EMU, NAVY, MSO_SHAPE.ROUND_2_SAME_RECTANGLE)
            entete.name = "entete-carte"
            entete.adjustments[0] = min(0.5, 12 * EMU / HAUT_ENTETE)
            entete.adjustments[1] = 0
            _texte(entete, titre_carte, 10, BLANC)
            largeur_pastille = 14 + len(etiquette) * 4.4
            pastille = deck_draw.rect(s, (x + w) / EMU - largeur_pastille - 8, y / EMU - 7, largeur_pastille, 14, BLANC, MSO_SHAPE.ROUNDED_RECTANGLE, ligne=NAVY)
            pastille.name = "pastille-rubrique"
            pastille.adjustments[0] = 0.5
            pastille.line.width = Pt(0.75)
            _texte(pastille, etiquette, 6.5, NAVY, align=PP_ALIGN.CENTER, marges=(2, 0))
            numero.left, numero.top, numero.width, numero.height = x + 6 * EMU, y + HAUT_ENTETE + 2 * EMU, 40 * EMU, 40 * EMU
            for r in (r for p in numero.text_frame.paragraphs for r in p.runs):
                r.font.size, r.font.color.rgb = Pt(30), MUTED
            if reste:
                for p in paras[:2]:
                    p._p.getparent().remove(p._p)
                texte.left, texte.top, texte.width, texte.height = x + 50 * EMU, y + HAUT_ENTETE + 4 * EMU, w - 58 * EMU, 52 * EMU
                texte.text_frame.vertical_anchor = MSO_ANCHOR.TOP
            else:
                texte._element.getparent().remove(texte._element)


ETAPES = [{"declarer": [T_CONV, T_REUSSIR, T_IA], "f": cartes_entete, "nouvelles_max": 0, "nom": "cartes a en-tete et pastille de rubrique"}]
