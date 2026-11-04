"""Delta V34p (base V33) : les quatre slides « mecanique » des chapitres Demarche generale et Demarche detaillee, refaites dans le vocabulaire maison.

- « Deux temps d'engagement » : deux bandeaux (forfait d'entree / trajectoire modulaire), trois cartes a pictogramme rond, drapeaux « a valider » en pilules grises ;
- « Un planning hypothetique en trois phases » : Gantt par trimestre (jalons de decision), un encart « ILLUSTRATION » (extrait d'un retroplanning de la bibliotheque
  de slides OCTO, rogne : ni nom de client, ni duree), deux cartes livrables / hypotheses ;
- « Une boucle continue » : boucle a six etapes (la premiere en accent), deux cartes a droite, trois fils transverses a pictogramme ;
- « Calendrier du pilote » : cinq colonnes d'etapes (pas d'axe des temps : les durees sont a valider), losanges COPIL, livrable par echeance, hypotheses, gouvernance.
Les phrases ecourtees passent dans les notes de la slide. Aucune forme de navigation, aucun surtitre, aucun numero de page n'est touche.
Usage (depuis docs/cadrage-ppt/) : py deck_delta/deck.py delta_V34p --base V33 --sortie C:/tmp/deck-v34-p/V34p.pptx --sans-rendu
"""
import os
import re

import deck_base
import deck_draw
from forme_ground import picto
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
    supprimer,
    tx,
)
from lxml import etree
from pptx import Presentation
from pptx.enum.dml import MSO_LINE
from pptx.enum.text import MSO_ANCHOR as A
from pptx.enum.text import PP_ALIGN as P

BASE = "V33"
NOTE = "V34p : Deux temps d'engagement, Planning hypothetique (encart retroplanning), Boucle continue, Calendrier du pilote : formes maison, textes allegés"
OPS = []

NB = "\u00a0"
NS_A = "http://schemas.openxmlformats.org/drawingml/2006/main"
T_26 = "Deux temps d'engagement : diagnostiquer, puis expérimenter et déployer"
T_27 = "Un planning hypothétique en trois phases, avant tout chiffrage"
T_28 = "Une boucle continue pour décider sur des faits, expérimenter et ancrer"
T_30 = "Calendrier du pilote : étapes et jalons, durées à valider"
TITRES = (T_26, T_27, T_28, T_30)
KICKER = re.compile(r"^\d\d · ")

_ICI = os.path.dirname(os.path.abspath(__file__))
IMG_RETRO = next((p for p in (os.path.join(_ICI, "encart_retro_V34p.png"), "C:/tmp/deck-v34-p/encart_retro.png") if os.path.exists(p)),
                 "C:/tmp/deck-v34-p/encart_retro.png")
SOURCE_RETRO = ("Illustration" + NB + ": extrait de la bibliothèque de slides OCTO, anonymisé — à valider avant diffusion.")


# ---------------------------------------------------------------- outils
def _s(prs, t):
    return deck_draw.slide_par_titre(prs, t)


def _nettoyer(s, garder_ids=()):
    """Garde les placeholders (titre, numero), la navigation, le surtitre « NN · ... » et les formes `garder_ids` ; supprime le reste."""
    for sh in list(s.shapes):
        if sh.is_placeholder or sh.name.startswith("nav-") or sh.shape_id in garder_ids:
            continue
        if sh.has_text_frame and KICKER.match(sh.text_frame.text):
            continue
        supprimer(sh)


def _italique(tb):
    for p in tb.text_frame.paragraphs:
        for r in p.runs:
            r.font.italic = True
    return tb


def _sans_ombre(sh):
    sp = sh._element.spPr
    for e in sp.findall(f"{{{NS_A}}}effectLst"):
        sp.remove(e)
    etree.SubElement(sp, f"{{{NS_A}}}effectLst")


def _picto(s, genre, cx, cy, d, ratio=0.58):
    """Disque blanc a bord navy + pictogramme natif de forme_ground (traits proportionnels a la taille)."""
    forme(s, S.OVAL, cx - d / 2, cy - d / 2, d, d, BLANC, NAVY, lw=1.0)
    n0 = len(s.shapes)
    pd = d * ratio
    picto(s, genre, cx, cy, pd)
    f = pd / 64.0
    for sh in list(s.shapes)[n0:]:
        try:
            w = sh.line.width.pt if sh.line.width else 1.5
            sh.line.width = int(max(0.6, w * f * 1.7) * 12700)
        except Exception:
            pass
        _sans_ombre(sh)


def _pilule_drapeau(s, x, y, w, h, texte, sz=9.5, accent=False):
    """Drapeau « a valider » : pilule grise a texte navy ; (accent) cyan a texte navy."""
    forme(s, S.ROUNDED_RECTANGLE, x, y, w, h, CYAN if accent else PANEL, None, adj=0.5)
    return tx(s, x + 4, y, w - 8, h, [[(texte, sz, True, NAVY)]], A.MIDDLE, P.CENTER)


def _notes(s, texte):
    s.notes_slide.notes_text_frame.text = texte


def _txt(sh):
    return sh.text_frame.text


# ================================================================ slide 26 : deux temps d'engagement
CARTES_26 = [
    ("cible", "Assessment flash",
     "Diagnostic et cartographie des opportunités, baseline documentée, coût du statu quo estimé si calculable, choix d'un pilote. Aucun ROI promis.",
     "Conduit par" + NB + ": OCTO. Décide" + NB + ": le" + NB + "client.",
     [("durée" + NB + ": à valider", False), ("MONTANT" + NB + ": 0 — À VALIDER", False)]),
    ("cycle", "Pilote Produit + IA",
     "Dimensionné à l'issue de l'Assessment flash" + NB + ": on n'enchaîne que ce que le pilote justifie. L'assainissement est déclenché par le diagnostic.",
     "Conduit par" + NB + ": OCTO et le client ensemble.",
     [("durée" + NB + ": à valider", False), ("MONTANT" + NB + ": 0 — À VALIDER", False)]),
    ("personnes", "Ancrage",
     "Relais internes formés, indicateurs tenus par le client. Extension éventuelle selon les résultats du pilote.",
     "Conduit par" + NB + ": le client, avec ses" + NB + "relais.",
     [("durée" + NB + ": à valider", False), ("JALON" + NB + ": RESTITUTION DU SPONSOR", True)]),
]


def deux_temps(prs):
    s = _s(prs, T_26)
    b = {sh.shape_id: sh for sh in s.shapes}
    # texte d'origine : conserve tel quel dans les notes (la slide l'allege)
    avant = [_txt(b[i]) for i in (67, 78, 90)]
    financement = _txt(b[96])
    _nettoyer(s)
    forme(s, S.ROUNDED_RECTANGLE, 45, 88, 44, 5, CYAN, None, adj=0.5)  # signature cyan sous le surtitre
    # deux bandeaux
    forme(s, S.ROUNDED_RECTANGLE, 45, 98, 196, 22, NAVY, None, adj=0.5)
    tx(s, 45, 98, 196, 22, [[("TEMPS 1 · FORFAIT D'ENTRÉE", 10.5, True, BLANC)]], A.MIDDLE, P.CENTER)
    forme(s, S.ROUNDED_RECTANGLE, 254, 98, 405, 22, CYAN, None, adj=0.5)
    tx(s, 254, 98, 405, 22, [[("TEMPS 2 · TRAJECTOIRE MODULAIRE", 10.5, True, NAVY)]], A.MIDDLE, P.CENTER)
    W, G, Y, H = 196, 13, 154, 196
    for k, (genre, titre, desc, conduit, pilules) in enumerate(CARTES_26):
        x = 45 + k * (W + G)
        carte_diag(s, x, Y, W, H, adj=0.06)
        _picto(s, genre, x + W / 2, Y, 56)
        tx(s, x + 10, Y + 34, W - 20, 18, [[(titre, 13, True, NAVY)]], A.MIDDLE, P.CENTER)
        tx(s, x + 12, Y + 56, W - 24, 68, [[(desc, 10.5, False, NAVY)]], A.TOP, P.CENTER)
        tx(s, x + 12, Y + 128, W - 24, 28, [[(conduit, 10.5, True, NAVY)]], A.MIDDLE, P.CENTER)
        for j, (t, accent) in enumerate(pilules):
            _pilule_drapeau(s, x + 10, Y + 160 + j * 17, W - 20, 15, t, 9.5, accent)
        if k < 2:  # chevron cyan entre deux cartes
            forme(s, S.CHEVRON, x + W + 2, Y - 9, 9, 18, CYAN, None, adj=0.35)
    tx(s, 45, 360, 614, 14, [[(financement, 10.5, False, SLATE)]], A.TOP)
    _notes(s, "Descriptions complètes d'origine (raccourcies sur la slide, avec « quand il est calculable » devenu « si calculable ») :\n- Assessment flash : "
              + avant[0] + "\n- Pilote Produit + IA : " + avant[1] + "\n- Ancrage : " + avant[2]
              + "\nLes durées et les montants restent à valider avec le client ; aucun ROI n'est promis.")


# ================================================================ slide 27 : planning hypothetique
X_G, L_COL = 170, 122  # origine des trimestres, largeur d'un trimestre


def _insere_image(s, chemin, x, y, w, h, nom, alt):
    import sys
    sys.path.insert(0, os.path.join(deck_base.RACINE, ".claude", "skills", "pptx-framed-image", "scripts"))
    from framed_image import place_image_in_frame, round2diag_geom
    emu = lambda v: int(round(v * 12700))  # noqa: E731
    pic = place_image_in_frame(s, chemin, emu(x), emu(y), emu(w), emu(h), geom=round2diag_geom(8000, 0))
    pic.name = nom
    pic._element.nvPicPr.cNvPr.set("descr", alt)
    return pic


def planning(prs):
    s = _s(prs, T_27)
    _nettoyer(s)
    forme(s, S.ROUNDED_RECTANGLE, 45, 88, 44, 5, CYAN, None, adj=0.5)
    _pilule_drapeau(s, 482, 66, 177, 18, "HYPOTHÈSE · SANS CHIFFRAGE", 10)
    # entetes de trimestre
    for t in range(4):
        x = X_G + t * L_COL
        forme(s, S.ROUNDED_RECTANGLE, x, 92, L_COL - 4, 20, PANEL, None, adj=0.5)
        carre_num_cyan(s, x + 3, 93, 18, t + 1, sz=10)
        tx(s, x + 26, 92, L_COL - 34, 20, [[(f"Trimestre {t + 1}", 10.5, True, NAVY)]], A.MIDDLE)
    # jalons de decision : une ligne fine, trois losanges, libelles dessous
    forme(s, S.RECTANGLE, X_G, 123.5, 4 * L_COL - 4, 0.75, LINE, None)
    jalons = [(0.81, "choix du pilote", "c"), (2.19, "comité de décision", "c"), (4.0, "passage de main", "d")]
    for f, lib, al in jalons:
        cx = X_G + f * L_COL - (4 if al == "d" else 0)
        forme(s, S.DIAMOND, cx - 6, 118, 12, 12, NAVY, None)
        if al == "c":
            tx(s, cx - 55, 132, 110, 13, [[(lib, 10, False, SLATE)]], A.TOP, P.CENTER)
        else:
            tx(s, cx + 6 - 110, 132, 110, 13, [[(lib, 10, False, SLATE)]], A.TOP, P.RIGHT)
    # trois barres : Assessment flash, Pilote Produit + IA (accent), Ancrage
    barres = [("Assessment flash", 0.0, 0.81, False), ("Pilote Produit + IA", 0.88, 2.19, True), ("Ancrage", 2.24, 4.0, False)]
    for k, (nom, a, z, accent) in enumerate(barres):
        y = 152 + k * 25
        tx(s, 45, y, 122, 20, [[(nom, 11, True, NAVY)]], A.MIDDLE)
        x0, x1 = X_G + a * L_COL, X_G + z * L_COL - (4 if z == 4.0 else 0)
        forme(s, S.ROUNDED_RECTANGLE, x0, y, x1 - x0, 20, CYAN if accent else NAVY, None, adj=0.5)
        tx(s, x0 + 4, y, x1 - x0 - 8, 20, [[("durée à valider", 10, True, NAVY if accent else BLANC)]], A.MIDDLE, P.CENTER)
    # encart ILLUSTRATION (gauche)
    forme(s, S.ROUNDED_RECTANGLE, 45, 232, 282, 128, PANEL, None, adj=0.05)
    pilule_entete(s, 53, 237, 88, 16, "ILLUSTRATION", NAVY, sz=9)
    tx(s, 149, 237, 172, 16, [[("Un rétroplanning par phases", 10.5, True, NAVY)]], A.MIDDLE)
    _insere_image(s, IMG_RETRO, 61, 257, 250, 250 * 405 / 1012, "illustration-retroplanning",
                  "Extrait d'un rétroplanning OCTO : phases Cadrage et Conception, jalons en losanges, activités par phase")
    # deux cartes a droite
    cartes = [("LIVRABLES CLÉS", ["Assessment flash" + NB + ": baseline, pilote choisi", "Pilote" + NB + ": produit Infra livré, indicateurs T0 → T1",
                                  "Ancrage" + NB + ": relais formés, passage de main"]),
              ("HYPOTHÈSES DE CALENDRIER", ["Démarrage après le choix du périmètre", "Durées à caler avec vous", "Le chiffrage est traité à part"])]
    for k, (titre, lignes) in enumerate(cartes):
        y = 242 + k * 66
        carte_diag(s, 339, y, 320, 52, adj=0.1)
        pilule_entete(s, 351, y - 8, 150 if k else 110, 16, titre, NAVY if k == 0 else CYAN, sz=9)
        for j, t in enumerate(lignes):
            forme(s, S.OVAL, 353, y + 10 + j * 13.5 + 3.5, 5, 5, CYAN, None)
            tx(s, 365, y + 8 + j * 13.5, 288, 13, [[(t, 10.5, False, NAVY)]], A.MIDDLE)
    _italique(tx(s, 45, 366, 614, 12, [[(SOURCE_RETRO, 9, False, SLATE)]], A.TOP))
    _notes(s, "Hypothèse de planning par trimestre, sans chiffrage ; les durées restent à valider avec le client. "
              "Encart : extrait recadré (phases Cadrage et Conception) d'un rétroplanning de la bibliothèque de slides OCTO ; "
              "les durées et validations de l'original sont écartées, ce n'est pas notre calendrier. Source : « Slides préformatées OCTO.pptx », slide 133.")


# ================================================================ slide 28 : la boucle
BOUCLE = [("Explorer", 216, 131), ("Comprendre", 297, 163), ("Prioriser", 297, 228), ("Expérimenter", 216, 261), ("Mesurer", 135, 228), ("Ancrer", 135, 163)]
CHEVRONS = [(256, 131, 21.79), (303, 187, 90.0), (256, 243, 158.21), (163, 243, 201.79), (116, 187, 270.0), (163, 131, 338.21)]
DX = 8  # decalage de la boucle vers la droite : les libelles de gauche restent dans la marge utile (x >= 45)


def boucle(prs):
    s = _s(prs, T_28)
    b = {sh.shape_id: sh for sh in s.shapes}
    _txt_rep = _txt(b[38])
    _nettoyer(s)
    forme(s, S.ROUNDED_RECTANGLE, 45, 88, 44, 5, CYAN, None, adj=0.5)
    # anneau, chevrons, six etapes (la premiere en accent)
    forme(s, S.OVAL, 122 + DX, 131, 187, 130, None, LINE, lw=3)
    for x, y, rot in CHEVRONS:
        c = forme(s, S.CHEVRON, x + DX, y, 13, 17, NAVY, None, adj=0.35)
        c.rotation = rot
    for k, (nom, cx, cy) in enumerate(BOUCLE):
        cx += DX
        forme(s, S.OVAL, cx - 15, cy - 15, 30, 30, CYAN if k == 0 else NAVY, None)
        tx(s, cx - 15, cy - 15, 30, 30, [[(str(k + 1), 14, True, NAVY if k == 0 else BLANC)]], A.MIDDLE, P.CENTER)
        if k == 0:
            tx(s, cx + 22, cy - 34, 90, 20, [[(nom, 12, True, NAVY)]], A.MIDDLE)
        elif k == 3:
            tx(s, cx + 22, cy + 4, 90, 20, [[(nom, 12, True, NAVY)]], A.MIDDLE)
        elif k in (1, 2):
            tx(s, cx + 22, cy - 10, 90, 20, [[(nom, 12, True, NAVY)]], A.MIDDLE)
        else:
            tx(s, cx - 22 - 90, cy - 10, 90, 20, [[(nom, 12, True, NAVY)]], A.MIDDLE, P.RIGHT)
    _picto(s, "cycle", 215.5 + DX, 184, 40)
    tx(s, 215.5 + DX - 50, 208, 100, 28, [[("puis nouveau cycle", 10.5, False, SLATE)]], A.TOP, P.CENTER)
    # deux cartes a droite
    carte_diag(s, 407, 100, 252, 106, adj=0.08)
    tx(s, 419, 108, 230, 16, [[("Actions possibles dans la boucle", 12, True, NAVY)]], A.MIDDLE)
    tx(s, 419, 127, 230, 30, [[("Des leviers choisis par le diagnostic, pas un préalable" + NB + ":", 10.5, False, NAVY)]], A.TOP)
    xs = 419
    for t, w in (("Assainissement", 74), ("Évolution technique", 92), ("Formation", 52)):
        forme(s, S.ROUNDED_RECTANGLE, xs, 172, w, 22, PANEL, None, adj=0.5)
        tx(s, xs + 2, 172, w - 4, 22, [[(t, 9.5, True, NAVY)]], A.MIDDLE, P.CENTER)
        xs += w + 4
    carte_diag(s, 407, 214, 252, 76, adj=0.08)
    forme(s, S.ROUNDED_RECTANGLE, 417, 224, 4, 56, CYAN, None, adj=0.5)
    tx(s, 431, 220, 220, 66, [[("«" + NB + "Repérer, prioriser, tenir" + NB + "»", 12, True, NAVY)],
                              [("La logique simple d'un pilote, à l'intérieur de la boucle" + NB + ": pas une deuxième méthode.", 10.5, False, NAVY)]], A.MIDDLE)
    # trois fils transverses
    tx(s, 45, 296, 614, 13, [[("TROIS FILS TRANSVERSES", 10, True, SLATE)]], A.MIDDLE)
    fils = [("personnes", "Personnes", "engager, expérimenter, relayer"),
            ("grille", "Technologies et Run", "cartographier, standardiser, décommissionner si pertinent"),
            ("ampoule", "IA", "assister, recommander, déléguer sous contrôle")]
    for k, (genre, titre, ligne) in enumerate(fils):
        x = 45 + k * 209
        carte_diag(s, x, 316, 196, 52, adj=0.1)
        _picto(s, genre, x + 26, 342, 36)
        tx(s, x + 52, 320, 138, 44, [[(titre, 11.5, True, NAVY)], [(ligne, 10, False, NAVY)]], A.MIDDLE)
    _notes(s, "Boucle : explorer, comprendre, prioriser, expérimenter, mesurer, ancrer, puis nouveau cycle. "
              "Les actions possibles (assainissement, évolution technique, formation) sont des leviers choisis par le diagnostic, pas un préalable. "
              + _txt_rep.replace("\n", " ").replace("\u00a0", " "))


# ================================================================ slide 30 : calendrier du pilote
ETAPES_30 = [("Assessment flash", "durée", 1), ("Restitution et arbitrage", "copil", 2), ("Pilote Produit + IA", "durée", 3),
             ("Ancrage", "durée", 4), ("Extension éventuelle", "durée", None)]
LIVRABLES_30 = ["Diagnostic, baseline au T0, pilote choisi", "Décision go / no-go du sponsor",
                "Mesure au T1 et décision de généraliser, adapter ou arrêter", "Relais internes formés, indicateurs tenus par le client"]
INSTANCES = ["Pilotage", "Suivi opérationnel", "Revue de valeur"]


def calendrier(prs):
    s = _s(prs, T_30)
    b = {sh.shape_id: sh for sh in s.shapes}
    legende_avant = _txt(b[5])
    hyp = _txt(b[45]).split("\n")
    _nettoyer(s)
    forme(s, S.ROUNDED_RECTANGLE, 45, 88, 44, 5, CYAN, None, adj=0.5)
    _pilule_drapeau(s, 482, 66, 177, 18, "DURÉES ET CHARGES" + NB + ": À VALIDER", 10)
    # trois phases en bandeau
    for (x, w, txt, prem, accent) in ((45, 244, "Diagnostiquer", True, False), (285, 130, "Expérimenter", False, True), (411, 248, "Ancrer", False, False)):
        forme(s, S.PENTAGON if prem else S.CHEVRON, x, 98, w, 20, CYAN if accent else NAVY, None, adj=0.35)
        tx(s, x + (6 if prem else 12), 98, w - 20, 20, [[(txt, 11, True, NAVY if accent else BLANC)]], A.MIDDLE, P.CENTER)
    # cinq colonnes d'etape
    W, G = 114, 11
    for k, (nom, genre, num) in enumerate(ETAPES_30):
        x = 45 + k * (W + G)
        c = carte_diag(s, x, 124, W, 90, adj=0.1)
        if num is None:
            c.line.dash_style = MSO_LINE.DASH
            c.line.color.rgb = NAVY
        if num:
            carre_num_cyan(s, x + 8, 131, 18, num, sz=10)
        tx(s, x + 8, 154, W - 14, 28, [[(nom, 11, True, NAVY)]], A.TOP)
        if genre == "durée":
            _pilule_drapeau(s, x + 8, 192, W - 16, 17, "durée" + NB + ": à valider", 9.5)
        else:
            tx(s, x + 8, 186, W - 12, 26, [[("COPIL" + NB + ": go / no-go du sponsor", 10, False, SLATE)]], A.TOP)
    # livrables par echeance : losange sur le bord haut de chaque carte, rattache a l'etape
    for k, texte in enumerate(LIVRABLES_30):
        x = 45 + k * (W + G)
        forme(s, S.RECTANGLE, x + W / 2 - 0.5, 214, 1, 12, NAVY, None)
        carte_diag(s, x, 226, W, 76, adj=0.1)
        if k == 0:
            forme(s, S.OVAL, x + W / 2 - 6, 220, 12, 12, CYAN, NAVY, lw=1.0)
        else:
            forme(s, S.DIAMOND, x + W / 2 - 8, 218, 16, 16, NAVY, None)
        tx(s, x + 8, 238, W - 14, 50, [[(texte, 10, True, NAVY)]], A.TOP)
        _italique(tx(s, x + 8, 288, W - 14, 13, [[("date" + NB + ": à valider", 9.5, False, SLATE)]], A.TOP))
    x5 = 45 + 4 * (W + G)
    tx(s, x5, 236, W, 52, [[("LIVRABLE PAR ÉCHÉANCE", 10, True, SLATE)], [("◆ = COPIL", 10, False, SLATE)]], A.TOP)
    # hypotheses et gouvernance
    forme(s, S.ROUNDED_RECTANGLE, 45, 310, 215, 59, PANEL, None, adj=0.1)
    tx(s, 57, 314, 192, 51, [[("HYPOTHÈSES ET CONDITIONS DE TENUE", 9.5, True, SLATE)], [(hyp[1] if len(hyp) > 1 else "", 10.5, False, NAVY)]], A.MIDDLE)
    tx(s, 272, 310, 387, 13, [[("GOUVERNANCE" + NB + ": TROIS INSTANCES", 10, True, SLATE)]], A.MIDDLE)
    for k, nom in enumerate(INSTANCES):
        x = 272 + k * 133
        carte_diag(s, x, 325, 121, 44, adj=0.12, accent=(k == 0))
        tx(s, x + 8, 328, 107, 38, [[(nom, 11, True, NAVY)], [("fréquence" + NB + ": à valider", 10, False, NAVY if k == 0 else SLATE)]], A.MIDDLE)
    _notes(s, "Légende d'origine du calendrier : " + legende_avant.replace("\u00a0", " ")
              + " Les durées, les dates et les fréquences restent à valider avec le client. Le COPIL est le comité de pilotage.")


# ---------------------------------------------------------------- assemblage
def retouche(prs):
    deux_temps(prs)
    planning(prs)
    boucle(prs)
    calendrier(prs)


def _ids():
    prs = Presentation(deck_base.resoudre_base(BASE))
    ids = []
    for t in TITRES:
        ids.append(f"id:{deck_draw.slide_par_titre(prs, t).slide_id}")
    return ids


ETAPES = [{"declarer": _ids(), "f": retouche, "nouvelles_max": 0, "nom": "Deux temps, Planning (encart retroplanning), Boucle, Calendrier du pilote : formes maison"}]
