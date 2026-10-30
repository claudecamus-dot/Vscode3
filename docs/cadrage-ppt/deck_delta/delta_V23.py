"""Delta V23 (base V22) : lot D du comite « forme » (F2_2.md, 2026-10-30) : intercalaires enrichis + trois slides les plus faibles.

- les huit intercalaires de chapitre : grand numero fantome (E7E9EE, decor), titre remonte, regle navy, question du chapitre [proposee], huit reperes de progression (un navy) ;
  la photo, le badge et le point cyan du gabarit ne bougent pas ;
- « Nous mesurons la valeur client... » (indicateurs T0 -> T1) : le tableau nu devient une carte : en-tete capsule navy, zebrure claire, filets supprimes, un seul cyan (le lisere d'intro) ;
- « Du pilote a l'autonomie : trois modes... » : trois cartes de meme famille (en-tetes tous navy, numeros en disques cernes, filet, pastilles de pied dans la carte) ;
- « Les alternatives sont des complements... » : en-tete capsule navy, quatre lignes en cartes, pastilles navy en premiere colonne.
Le texte des slides ne change pas ; seules les cinq phrases de question des intercalaires sont nouvelles (marquees [proposees] dans la note de livraison).
Usage (depuis docs/cadrage-ppt/) : py deck_delta/deck.py delta_V23 --base V22
"""
import deck_base
import deck_draw
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Pt

BASE = "V22"
NOTE = "V23 : intercalaires enrichis, trois slides les plus faibles en cartes (lot D)"
OPS = []

N = RGBColor(0x0E, 0x23, 0x56)
L = RGBColor(0xE7, 0xE9, 0xEE)
M = RGBColor(0x58, 0x65, 0x86)
W = RGBColor(0xFF, 0xFF, 0xFF)
EMU = 12700
POLICE = "Outfit"

T_INDIC = "Nous mesurons la valeur client et l'apport du coaching augmenté"
T_MODES = "Du pilote à l'autonomie : trois modes d'interaction entre OCTO et le client"
T_ALTERN = "Les alternatives sont des compléments que l'offre intègre"
CHAPITRES = ["Contexte et enjeux", "Nos convictions", "Notre approche", "Démarche générale", "Démarche détaillée", "Dispositif et prix", "Prochain pas", "Annexes"]
QUESTIONS = {  # [proposees] sauf « Mon cas est-il couvert ? » (comite T3)
    "Contexte et enjeux": "Pourquoi changer ?",
    "Nos convictions": "Que croyons-nous ?",
    "Notre approche": "Comment, avec quel moteur ?",
    "Démarche générale": "Quel cycle suivons-nous ?",
    "Démarche détaillée": "Que se passe-t-il concrètement ?",
    "Dispositif et prix": "Qui fait quoi, et pour combien ?",
    "Prochain pas": "Par où commencer ?",
    "Annexes": "Mon cas est-il couvert ?",
}


def _ids():
    return [f"id:{s.slide_id}" for s in Presentation(deck_base.resoudre_base(BASE)).slides]


def _arriere(s, sh):
    """Envoie la forme juste apres le groupe de proprietes de l'arbre (sous tout le reste de la slide)."""
    arbre = s.shapes._spTree
    arbre.remove(sh._element)
    arbre.insert(2, sh._element)


def _rect(s, x, y, w, h, fill, forme=MSO_SHAPE.ROUNDED_RECTANGLE, ligne=None, adj=None, nom=None, trait=0.75):
    sh = deck_draw.rect(s, x, y, w, h, fill, forme, ligne=ligne)
    if ligne is not None:
        sh.line.width = Pt(trait)
    if adj is not None:
        sh.adjustments[0] = adj
    if nom:
        sh.name = nom
    return sh


def _place(sh, x=None, y=None, w=None, h=None):
    if x is not None:
        sh.left = int(x * EMU)
    if y is not None:
        sh.top = int(y * EMU)
    if w is not None:
        sh.width = int(w * EMU)
    if h is not None:
        sh.height = int(h * EMU)


def _style(sh, taille=None, couleur=None, gras=None, ancre=None, align=None):
    tf = sh.text_frame
    if ancre is not None:
        tf.vertical_anchor = ancre
    for p in tf.paragraphs:
        if align is not None:
            p.alignment = align
        for r in p.runs:
            if taille is not None:
                r.font.size = Pt(taille)
            if couleur is not None:
                r.font.color.rgb = couleur
            if gras is not None:
                r.font.bold = gras


def _fond(sh, couleur):
    sh.fill.solid()
    sh.fill.fore_color.rgb = couleur


def _filets(s):
    """Filets horizontaux fins (Rectangle de 1 pt sur toute la largeur du tableau) : supprimes."""
    for sh in list(s.shapes):
        if sh.name.startswith("Rectangle") and sh.height <= 2 * EMU and sh.width >= 600 * EMU:
            sh._element.getparent().remove(sh._element)


def _par_texte(s, debut):
    return next(sh for sh in s.shapes if sh.has_text_frame and sh.text_frame.text.startswith(debut))


def intercalaires(prs):
    for s in prs.slides:
        if not s.slide_layout.name.startswith(("50 -", "51 -")):
            continue
        titre = next(sh for sh in s.shapes if sh.is_placeholder and sh.has_text_frame and sh.top > 100 * EMU and sh.text_frame.text in CHAPITRES)
        badge = next(sh for sh in s.shapes if sh.is_placeholder and sh.has_text_frame and sh.text_frame.text not in CHAPITRES and len(sh.text_frame.text) <= 2)
        chapitre = titre.text_frame.text
        _place(titre, 338, 168, 321, 48)
        titre.text_frame.vertical_anchor = MSO_ANCHOR.TOP
        fantome = s.shapes.add_textbox(int(420 * EMU), int(50 * EMU), int(239 * EMU), int(122 * EMU))
        fantome.name = "num-fantome"
        tf = fantome.text_frame
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        tf.vertical_anchor = MSO_ANCHOR.TOP
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.RIGHT
        r = p.add_run()
        r.text = badge.text_frame.text
        r.font.size, r.font.bold, r.font.name = Pt(110), True, POLICE
        r.font.color.rgb = L
        _arriere(s, fantome)
        _rect(s, 338, 224, 48, 3, N, MSO_SHAPE.RECTANGLE, nom="regle")
        question = s.shapes.add_textbox(int(338 * EMU), int(234 * EMU), int(300 * EMU), int(48 * EMU))
        question.name = "question"
        qt = question.text_frame
        qt.word_wrap = True
        qt.margin_left = qt.margin_right = qt.margin_top = qt.margin_bottom = 0
        r = qt.paragraphs[0].add_run()
        r.text = QUESTIONS[chapitre]
        r.font.size, r.font.name = Pt(16), POLICE
        r.font.color.rgb = M
        courant = CHAPITRES.index(chapitre)
        for i in range(8):
            _rect(s, 338 + 18 * i, 300, 10, 10, N if i == courant else L, MSO_SHAPE.OVAL, nom=f"repere-{i + 1}")


def indicateurs(prs):
    s = deck_draw.slide_par_titre(prs, T_INDIC)
    capsule = _rect(s, 45, 133, 614, 29, N, adj=0.45, nom="entete-tab")
    _arriere(s, capsule)
    for debut in ("Indicateurs possibles", "Référence T0", "Résultat T1", "IA vérifiée", "Garde-fou"):
        sh = _par_texte(s, debut)
        _place(sh, y=133, h=29)
        _style(sh, taille=9.5, couleur=W, gras=True, ancre=MSO_ANCHOR.MIDDLE)
    pastille1 = _par_texte(s, "NIVEAU 1")
    fond1 = next(sh for sh in s.shapes if sh.name.startswith("Rounded Rectangle") and abs(sh.left - 45 * EMU) < 2 * EMU and abs(sh.top - pastille1.top) < 2 * EMU)
    _fond(fond1, L)
    _place(fond1, y=138)
    _place(pastille1, y=138)
    _style(pastille1, couleur=N)
    _filets(s)
    for y, h in ((188, 25), (238, 26), (309, 36)):
        bande = _rect(s, 49, y, 606, h, L, adj=0.3, nom="zebre")
        _arriere(s, bande)
    n2 = _par_texte(s, "NIVEAU 2")
    fond2 = next(sh for sh in s.shapes if sh.name.startswith("Rounded Rectangle") and abs(sh.top - n2.top) < 2 * EMU and abs(sh.left - 45 * EMU) < 2 * EMU)
    _fond(fond2, N)
    _style(n2, couleur=W)
    _place(_par_texte(s, "Plein"), y=349)


def modes(prs):
    s = deck_draw.slide_par_titre(prs, T_MODES)
    formes = list(s.shapes)
    cartes = [sh for sh in formes if sh.name.startswith("Rounded Rectangle") and abs(sh.height - 140 * EMU) < 2 * EMU and abs(sh.width - 195 * EMU) < 2 * EMU]
    assert len(cartes) == 3, len(cartes)
    for carte in cartes:
        x = carte.left / EMU
        dedans = [sh for sh in formes if sh is not carte and x <= sh.left / EMU <= x + 195 and 120 <= sh.top / EMU <= 330]
        carte.height = int(172 * EMU)
        entete = next(sh for sh in dedans if sh.name.startswith("Round Diagonal"))
        _fond(entete, N)
        titre_e = next(sh for sh in dedans if sh.has_text_frame and abs(sh.top - entete.top) < 2 * EMU and sh is not entete and sh.width > 100 * EMU)
        _style(titre_e, taille=12, couleur=W, gras=True)
        ovale = next(sh for sh in dedans if sh.name.startswith("Oval"))
        _fond(ovale, W)
        ovale.line.color.rgb = N
        ovale.line.width = Pt(1.5)
        numero = next(sh for sh in dedans if sh.has_text_frame and abs(sh.left - ovale.left) < 2 * EMU and abs(sh.top - ovale.top) < 2 * EMU and sh is not ovale)
        _style(numero, couleur=N)
        corps = next(sh for sh in dedans if sh.has_text_frame and abs(sh.top / EMU - 171) < 2)
        _place(corps, y=171, h=96)
        _style(corps, taille=10)
        conduit = next(sh for sh in dedans if sh.has_text_frame and sh.text_frame.text.startswith("Conduit par"))
        _place(conduit, y=270, h=26)
        _style(conduit, taille=10)
        filet = _rect(s, x + 10, 268, 175, 1, L, MSO_SHAPE.RECTANGLE, nom="filet-carte")
        pied = [sh for sh in dedans if abs(sh.top / EMU - 302) < 2]
        for sh in pied:
            _place(sh, y=299)
            if sh.name.startswith("Rounded Rectangle"):
                _fond(sh, L)
        for sh in pied:
            if sh.has_text_frame and sh.text_frame.text:
                _style(sh, taille=9.5, couleur=N)
        chevron = next((sh for sh in formes if sh.name.startswith("Chevron") and abs(sh.left / EMU - (x + 193)) < 4), None)
        if chevron is not None:
            _place(chevron, y=231)
    _place(next(sh for sh in formes if sh.has_text_frame and sh.text_frame.text.startswith("Modes de Team Topologies")), y=334)


def alternatives(prs):
    s = deck_draw.slide_par_titre(prs, T_ALTERN)
    capsule = _rect(s, 45, 91, 614, 20, N, adj=0.5, nom="entete-alt")
    _arriere(s, capsule)
    for debut, x in (("ALTERNATIVE", 63), ("CE QU'ELLE APPORTE", 203), ("CE QUE L'OFFRE AJOUTE", 405)):
        sh = _par_texte(s, debut)
        _place(sh, x=x, y=91, h=20)
        _style(sh, taille=9.5, couleur=W, gras=True, ancre=MSO_ANCHOR.MIDDLE)
    _filets(s)
    lignes = sorted([sh for sh in s.shapes if sh.has_text_frame and abs(sh.left - 45 * EMU) < 2 * EMU and 110 * EMU <= sh.top < 315 * EMU and sh.height >= 40 * EMU],
                    key=lambda sh: sh.top)
    assert len(lignes) == 4, len(lignes)
    for k, c1 in enumerate(lignes):
        y = 117 + 51 * k
        ligne = _rect(s, 45, y, 614, 46, W, adj=0.22, ligne=L, nom=f"ligne-{k + 1}", trait=1.25)
        pastille = _rect(s, 53, y + 6, 136, 34, N, adj=0.5, nom=f"pastille-{k + 1}")
        _arriere(s, pastille)
        _arriere(s, ligne)  # la carte passe SOUS la pastille
        _place(c1, x=53, y=y + 6, w=136, h=34)
        _style(c1, taille=10 if len(c1.text_frame.text) > 22 else 10.5, couleur=W, gras=True, ancre=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
        for sh in s.shapes:
            if sh.has_text_frame and abs(sh.top - c1.top) < 1 and False:
                pass
    # colonnes 2 et 3 : relevees par leur rang vertical d'origine (115, 166, 216, 266 pt)
    origine = [115, 166, 216, 266]
    for k, y0 in enumerate(origine):
        for sh in s.shapes:
            if sh.has_text_frame and abs(sh.top / EMU - y0) < 1.5 and sh.left > 190 * EMU and abs(sh.height - 50 * EMU) < 2 * EMU:
                _place(sh, y=119 + 51 * k, h=42)
                _style(sh, taille=10, ancre=MSO_ANCHOR.MIDDLE)
    for sh in s.shapes:
        if sh.name.startswith("Rounded Rectangle") and abs(sh.top / EMU - 331) < 1.5:
            _place(sh, y=326, h=30)
        elif sh.has_text_frame and abs(sh.top / EMU - 331) < 1.5 and sh.name.startswith("TextBox"):
            _place(sh, y=326, h=30)


def retouche(prs):
    intercalaires(prs)
    indicateurs(prs)
    modes(prs)
    alternatives(prs)


ETAPES = [{"declarer": _ids(), "f": retouche, "nouvelles_max": 0, "nom": "lot D : intercalaires, indicateurs, modes, alternatives"}]
