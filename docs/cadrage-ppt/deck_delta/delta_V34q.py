"""Delta V34q (base V33) : quatre slides de « Démarche détaillée » refaites avec des illustrations en encarts (lot q).

- « De la douleur au produit… » : trois cartes compactes + un encart ILLUSTRATION (extrait de la bibliotheque de slides OCTO, « La démarche de réalisation d'un produit ») ;
- « Exemples de livrables (1/2) » et « (2/2) » : quatre cartes allegees (pictogramme a cheval sur le bord, nom, but, trois pilules Format / Qui / Quand) a gauche,
  un encart ILLUSTRATION a droite (grille de priorisation gains/effort ; roadmap multi-streams), images OCTO generiques sans nom de client ;
- « Nous mesurons la valeur client… » : tableau reecrit nativement (pas d'encart : un tableau de mesure ne supporte pas d'etre rogne en largeur), rangees sans zebre, niveaux en colonne,
  legende a pastilles ; les 6 indicateurs, leurs garde-fous et les etats des pastilles sont conserves a l'identique.
Images : crops PNG sous C:/tmp/deck-v34-q/ (source et recadrage : provenance_V34q.json). Aucune slide creee, aucun surtitre ni bouton de navigation touche.
Usage (depuis docs/cadrage-ppt/) : py deck_delta/deck.py delta_V34q --base V33 --sortie C:/tmp/deck-v34-q/V34q.pptx --sans-rendu
"""
import os
import sys

import deck_base
from forme_v9 import (
    BLANC,
    CYAN,
    LINE,
    NAVY,
    PANEL,
    SLATE,
    S,
    carre_num_cyan,
    carte_diag,
    forme,
    pilule_entete,
    tx,
)
from forme_v26 import disque_picto, vider
from PIL import Image
from pptx import Presentation
from pptx.enum.text import MSO_ANCHOR as A
from pptx.enum.text import PP_ALIGN as P
from pptx.util import Emu

sys.path.insert(0, os.path.join(deck_base.RACINE, ".claude", "skills", "pptx-framed-image", "scripts"))
from framed_image import place_image_in_frame, round2diag_geom  # noqa: E402

BASE = "V33"
NOTE = "V34q : mission pilote, deux slides de livrables et mesure de la valeur refaites ; encarts ILLUSTRATION (bibliotheque OCTO generique) sur trois d'entre elles"
OPS = []

NB = "\u00a0"
IMG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "illustrations_V34")
T1 = "De la douleur au produit : une mission pilote de bout en bout"
T2 = "Exemples de livrables (1/2) : comprendre et décider"
T3 = "Exemples de livrables (2/2) : piloter et ancrer"
T4 = "Nous mesurons la valeur client et l'apport du coaching augmenté"
LEGENDE_IMG = "Illustration" + NB + ": extrait d'un support de méthode OCTO, anonymisé — à valider avant diffusion."


# ---------------------------------------------------------------- encart ILLUSTRATION
def _encart(s, x, y, w, h, titre, png, bx, by, bw, bh):
    """Panneau gris + pilule ILLUSTRATION + titre, image rognee a la forme (round2DiagRect) centree dans la boite (bx, by, bw, bh), legende en pied."""
    forme(s, S.ROUNDED_RECTANGLE, x, y, w, h, PANEL, None, adj=0.05)
    pilule_entete(s, x + 8, y + 6, 88, 16, "ILLUSTRATION", NAVY, sz=9)
    tx(s, x + 104, y + 6, w - 112, 16, [[(titre, 10.5, True, NAVY)]], A.MIDDLE)
    iw, ih = Image.open(png).size
    k = min(bw / iw, bh / ih)
    pw, ph = iw * k, ih * k
    px, py = bx + (bw - pw) / 2, by + (bh - ph) / 2
    pic = place_image_in_frame(s, png, Emu(int(px * 12700)), Emu(int(py * 12700)), Emu(int(pw * 12700)), Emu(int(ph * 12700)), geom=round2diag_geom(9000, 0))
    pic.line.color.rgb = LINE
    pic.line.width = 9525
    pic.name = "illustration"
    tx(s, x + 8, y + h - 30, w - 16, 26, [[(LEGENDE_IMG, 9, False, SLATE)]], A.MIDDLE)
    return pic


def _notes(s, texte):
    s.notes_slide.notes_text_frame.text = texte


def _pilule_texte(s, x, y, w, h, runs, fill=BLANC, bord=NAVY, sz=9.5):
    forme(s, S.ROUNDED_RECTANGLE, x, y, w, h, fill, bord, adj=0.5, lw=0.75)
    tx(s, x, y, w, h, [[(t, sz, b, c) for t, b, c in runs]], A.MIDDLE, P.CENTER)


# ---------------------------------------------------------------- slide 1 : mission pilote
CARTE1 = ("Des équipes de développement attendent leurs environnements" + NB + "; le guichet Infra est saturé.")
MISSION = [
    "Le coach qualifie le périmètre et fixe la référence au T0.",
    "Il conduit les interviews" + NB + "; les agents repèrent les motifs récurrents.",
    "Il facilite le cadrage du produit" + NB + "; l'équipe client expérimente.",
    "Aucune action des agents en production.",
]


def _carte_num(s, x, y, w, h, num, titre):
    carte_diag(s, x, y, w, h, adj=0.1)
    carre_num_cyan(s, x + 6, y + 4, 17, num, sz=10)
    tx(s, x + 30, y + 3, w - 40, 19, [[(titre, 11.5, True, NAVY)]], A.MIDDLE)


def mission(prs):
    s = _slide(prs, T1)
    vider(s)
    forme(s, S.ROUNDED_RECTANGLE, 45, 96, 340, 18, NAVY, None, adj=0.5)
    tx(s, 45, 96, 340, 18, [[("SCÉNARIO PÉDAGOGIQUE — ILLUSTRATIF, NON CLIENT", 10, True, BLANC)]], A.MIDDLE, P.CENTER)
    tx(s, 393, 92, 266, 28, [[("Connectivité applicative sécurisée — T0 et T1 à mesurer, aucune valeur réelle", 10, False, SLATE)]], A.MIDDLE)
    y1, h1, y2, h2, y3, h3 = 122, 56, 183, 88, 276, 82
    _carte_num(s, 45, y1, 340, h1, 1, "Contexte, enjeux et demande")
    tx(s, 53, y1 + 25, 324, 22, [[(CARTE1, 10, False, NAVY)]], A.TOP)
    _carte_num(s, 45, y2, 340, h2, 2, "Mission OCTO")
    tx(s, 53, y2 + 25, 324, h2 - 28, [[("– " + t, 10, False, NAVY)] for t in MISSION], A.TOP, espace=1.5)
    carte_diag(s, 45, y3, 340, h3, adj=0.1)
    carre_num_cyan(s, 51, y3 + 4, 17, 3, sz=10)
    tx(s, 75, y3 + 3, 120, 19, [[("Résultats et décision", 11.5, True, NAVY)]], A.MIDDLE)
    _pilule_texte(s, 205, y3 + 4, 84, 16, [("T0" + NB + ": À MESURER", True, NAVY)], bord=LINE)
    forme(s, S.CHEVRON, 293, y3 + 5, 7, 14, CYAN, None, adj=0.35)
    _pilule_texte(s, 304, y3 + 4, 76, 16, [("T1" + NB + ": À MESURER", True, BLANC)], fill=NAVY, bord=None)
    tx(s, 53, y3 + 26, 324, h3 - 28, [
        [("Résultats mesurés au T1, jamais présumés" + NB + "; les agents consolident les faits et capitalisent la décision validée.", 10, False, NAVY)],
        [("Le client décide" + NB + ": généraliser, adapter ou arrêter.", 10, True, NAVY)]], A.TOP, espace=2)
    _encart(s, 393, 122, 266, 236, "Discovery, puis Delivery", f"{IMG}/c1_demarche.png", 401, 150, 250, 176)
    _notes(s, "Phrases retirees de la slide (rien n'est perdu)" + NB + ": « Aucun client réel, aucune valeur réelle" + NB + ": un scénario pour montrer le déroulé. » "
              "(portee par le bandeau « ILLUSTRATIF, NON CLIENT » et la ligne « aucune valeur réelle »). "
              "Encart ILLUSTRATION" + NB + ": extrait « La démarche de réalisation d'un produit en 3 grandes phases » de la bibliotheque de slides OCTO (Discovery, Delivery), "
              "recadre sur les deux premieres phases ; generique, aucun nom de client. À valider avant diffusion.")


# ---------------------------------------------------------------- slides 2 et 3 : livrables
LIVRABLES_1 = [
    ("grille", "Cartographie des capacités", "Voir capacités, consommateurs et propriétaires.", "tableau", "ensemble", "début",
     "Voir les capacités, leurs consommateurs et leurs propriétaires."),
    ("jauge", "Baseline des indicateurs", "Fixer l'état de départ (T0) pour mesurer l'apport.", "tableau", "OCTO", "début",
     "Fixer l'état de départ (T0) pour mesurer ensuite l'apport."),
    ("document", "Fiche produit Infra", "Décrire offre, valeur, engagements, propriétaire.", "fiche", "ensemble", "pilote",
     "Décrire l'offre, la valeur, les engagements et le propriétaire."),
    ("cible", "Grille de priorisation", "Arbitrer sur valeur, faisabilité et charge.", "grille", "ensemble", "pilote",
     "Arbitrer les demandes sur la valeur, la faisabilité et la charge."),
]
LIVRABLES_2 = [
    ("calendrier", "Roadmap produit", "Planifier les évolutions et l'arrêt des capacités.", "frise", "client", "pilote",
     "Planifier les évolutions et l'arrêt des capacités."),
    ("barres", "Tableau de bord", "Suivre l'usage, la qualité et le coût, du T0 au T1.", "écran", "client", "continu",
     "Suivre l'usage, la qualité et le coût, du T0 au T1."),
    ("personnes", "Charte IA et RACI", "Cadrer qui prépare, valide et décide quand l'IA aide.", "charte", "ensemble", "pilote",
     "Cadrer qui prépare, qui valide et qui décide quand l'IA aide."),
    ("fleche", "Plan de passage de main", "Transférer l'animation aux relais formés du client.", "plan", "OCTO", "fin",
     "Transférer l'animation aux relais formés du client."),
]


def _cartes_livrables(s, liste):
    for k, (glyphe, nom, but, fmt, qui, quand, _orig) in enumerate(liste):
        y = 98 + k * 66
        carte_diag(s, 62, y, 299, 60, adj=0.12)
        disque_picto(s, 62, y + 30, glyphe, d=34)
        tx(s, 86, y + 6, 270, 15, [[(nom, 11.5, True, NAVY)]], A.MIDDLE)
        tx(s, 86, y + 22, 270, 14, [[(but, 10, False, NAVY)]], A.MIDDLE)
        x = 86
        for lab, val in (("Format", fmt), ("Qui", qui), ("Quand", quand)):
            w = 11 + 5.0 * (len(lab) + 3 + len(val))
            _pilule_texte(s, x, y + 40, w, 15, [(lab + NB + ": ", False, SLATE), (val, True, NAVY)], bord=LINE)
            x += w + 5


def _pied_livrables(s):
    tx(s, 45, 364, 520, 12, [[("Exemples illustratifs" + NB + ": formats et contenus à adapter en atelier avec vous.", 9.5, False, SLATE)]], A.TOP)


def _notes_livrables(liste, extra):
    lignes = "Buts complets avant allegement" + NB + ": " + " ; ".join(f"{n}" + NB + ": {o}" for _g, n, _b, _f, _q, _w, o in liste) + ". "
    return lignes + extra


def livrables1(prs):
    s = _slide(prs, T2)
    vider(s)
    _cartes_livrables(s, LIVRABLES_1)
    _encart(s, 369, 98, 290, 258, "Grille de priorisation", f"{IMG}/c2_priorisation.png", 377, 126, 274, 194)
    _pied_livrables(s)
    _notes(s, _notes_livrables(LIVRABLES_1, "Encart ILLUSTRATION" + NB + ": « Priorisation » (matrice gains / effort-confiance) de la bibliotheque de slides OCTO, generique, "
                                              "aucun nom de client ; il illustre la grille de priorisation. Pas d'illustration pour les trois autres livrables. À valider avant diffusion."))


def livrables2(prs):
    s = _slide(prs, T3)
    vider(s)
    _cartes_livrables(s, LIVRABLES_2)
    _encart(s, 369, 98, 290, 258, "Roadmap multi-streams", f"{IMG}/c3_roadmap.png", 377, 126, 274, 194)
    _pied_livrables(s)
    _notes(s, _notes_livrables(LIVRABLES_2, "Encart ILLUSTRATION" + NB + ": « Roadmap multi-stream » de la bibliotheque de slides OCTO, recadre sans l'axe des trimestres "
                                              "(aucune date), generique, aucun nom de client ; il illustre la roadmap produit. Pas d'illustration pour le tableau de bord, la charte et le RACI, le plan de passage de main. À valider avant diffusion."))


# ---------------------------------------------------------------- slide 4 : mesure
INTRO = ("Référence documentée au T0, résultats et écarts évalués au T1" + NB + "; la contribution de l'IA est ", "vérifiée, jamais présumée", ".")
COLS = [("Référence|T0", 383), ("Résultat|T1", 433), ("IA|vérifiée", 483)]
# (indicateur, ce qu'on mesure, (T0, T1, IA) : 2 plein / 1 demi / 0 vide, garde-fou)
NIVEAU1 = [
    ("Efficacité opérationnelle", "Délai de mise à disposition, demandes complètes", (2, 1, 0), "Ne pas compter un simple déplacement de charge"),
    ("Expérience utilisateur", "Effort perçu, succès du self-service", (2, 0, 0), "Échantillon représentatif, clients captifs"),
    ("Robustesse et risque", "SLO, incidents liés aux changements", (1, 0, 0), "Ne jamais sacrifier la fiabilité à la vitesse"),
    ("Coûts et valeur", "Coût unitaire par capacité utile, prévisibilité", (2, 1, 1), "Distinguer économies, coûts évités, temps libéré"),
    ("Anticipation de l'IA", "Délai d'accès à une capacité IA gouvernée", (1, 0, 0), "Pas de métrique IA hors périmètre concerné"),
]
NIVEAU2 = [("Efficacité du coaching augmenté", "Temps de préparation, preuves sourcées, délai signal → arbitrage, autonomie transférée", (2, 1, 1), "Vérifier la contribution de l'IA")]


def _pastille(s, cx, cy, etat, d=15):
    forme(s, S.OVAL, cx - d / 2, cy - d / 2, d, d, NAVY if etat == 2 else BLANC, NAVY, lw=1.25)
    if etat == 1:
        c = forme(s, S.CHORD, cx - d / 2, cy - d / 2, d, d, NAVY, None)
        from lxml import etree
        ns = "http://schemas.openxmlformats.org/drawingml/2006/main"
        av = c._element.spPr.find(f"{{{ns}}}prstGeom").find(f"{{{ns}}}avLst")
        for g in list(av):
            av.remove(g)
        for nom, val in (("adj1", 5400000), ("adj2", 16200000)):
            gd = etree.SubElement(av, f"{{{ns}}}gd")
            gd.set("name", nom)
            gd.set("fmla", f"val {val}")


def _rangee(s, y, h, nom, mesure, etats, garde):
    tx(s, 113, y, 252, h, [[(nom, 11, True, NAVY)], [(mesure, 10, False, SLATE)]], A.MIDDLE)
    for (_lab, cx), etat in zip(COLS, etats, strict=True):
        _pastille(s, cx, y + h / 2, etat)
    tx(s, 520, y, 139, h, [[(garde, 10, False, NAVY)]], A.MIDDLE)


def mesure(prs):
    s = _slide(prs, T4)
    vider(s)
    forme(s, S.ROUNDED_RECTANGLE, 45, 98, 4, 22, CYAN, None, adj=0.5)
    tx(s, 58, 98, 601, 22, [[(INTRO[0], 11, False, NAVY), (INTRO[1], 11, True, NAVY), (INTRO[2], 11, False, NAVY)]], A.MIDDLE)
    tx(s, 113, 126, 252, 20, [[("Indicateurs possibles (T0 → T1)", 9.5, True, SLATE)]], A.BOTTOM)
    for lab, cx in COLS:
        tx(s, cx - 24, 120, 48, 26, [[(m, 9.5, True, SLATE)] for m in lab.split("|")], A.BOTTOM, P.CENTER)
    tx(s, 520, 126, 139, 20, [[("Garde-fou", 9.5, True, SLATE)]], A.BOTTOM)
    forme(s, S.RECTANGLE, 45, 148, 614, 1, NAVY, None)
    y0, pas = 150, 31
    forme(s, S.ROUNDED_RECTANGLE, 45, y0, 60, pas * 5 - 3, NAVY, None, adj=0.1)
    tx(s, 47, y0, 56, pas * 5 - 3, [[("NIVEAU 1", 10, True, BLANC)], [("CLIENT", 10, True, BLANC)]], A.MIDDLE, P.CENTER)
    for k, (nom, mesure_, etats, garde) in enumerate(NIVEAU1):
        _rangee(s, y0 + k * pas, pas - 2, nom, mesure_, etats, garde)
        if k:
            forme(s, S.RECTANGLE, 113, y0 + k * pas - 1, 546, 0.75, LINE, None)
    y2, h2 = y0 + 5 * pas + 3, 40
    forme(s, S.ROUNDED_RECTANGLE, 45, y2, 60, h2, CYAN, None, adj=0.1)
    tx(s, 46, y2, 58, h2, [[(m, 9.5, True, NAVY)] for m in ("NIVEAU 2", "COACHING", "AUGMENTÉ")], A.MIDDLE, P.CENTER)
    nom, mesure_, etats, garde = NIVEAU2[0]
    _rangee(s, y2, h2, nom, mesure_, etats, garde)
    forme(s, S.RECTANGLE, 45, y2 + h2 + 3, 614, 0.75, LINE, None)
    # legende : pastilles + mots ; puis la reserve
    x = 45
    for etat, mot in ((2, "plein" + NB + ": mesuré et vérifié"), (1, "demi" + NB + ": mesuré, à vérifier"), (0, "vide" + NB + ": pas encore mesuré")):
        _pastille(s, x + 5, 361, etat, d=10)
        tx(s, x + 14, 355, 140, 12, [[(mot, 9.5, False, SLATE)]], A.MIDDLE)
        x += 14 + 4.0 * len(mot) + 14
    tx(s, 419, 355, 240, 12, [[("Niveaux de démonstration, aucune mesure réelle.", 9.5, True, SLATE)]], A.MIDDLE, P.RIGHT)
    _notes(s, "Mise en page" + NB + ": tableau reecrit en formes natives (memes 6 indicateurs, memes garde-fous, memes etats de pastilles que la version precedente) ; "
              "les niveaux passent en colonne a gauche. Aucune illustration importee : un tableau de mesure ne supporte pas d'etre reduit pour faire place a un encart.")


# ---------------------------------------------------------------- assemblage
def _slide(prs, titre):
    for sl in prs.slides:
        t = sl.shapes.title
        if t is not None and t.text_frame.text == titre:
            return sl
    raise ValueError(f"slide introuvable : {titre!r}")


def _tout(prs):
    mission(prs)
    livrables1(prs)
    livrables2(prs)
    mesure(prs)


def _ids():
    prs = Presentation(deck_base.resoudre_base(BASE))
    return [f"id:{_slide(prs, t).slide_id}" for t in (T1, T2, T3, T4)]


ETAPES = [{"declarer": _ids(), "f": _tout, "nouvelles_max": 0, "nom": "mission pilote, livrables 1/2 et 2/2, mesure : encarts ILLUSTRATION et tableau natif"}]
