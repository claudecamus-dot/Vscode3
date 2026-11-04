"""Delta V36vE (base V35) : slide « Un planning hypothetique en trois phases » sans l'illustration, recomposee autour du planning et des livrables.

- l'encart ILLUSTRATION (cadre, pilule, titre, image, legende) disparait ; le fichier image du depot n'est pas touche ;
- le planning devient le heros : quatre colonnes de trimestre, trois jalons en losange, trois barres de phase (« duree a valider » reste sur chaque barre) ;
- les livrables cles passent en trois cartes numerotees, dans l'ordre des phases ; les hypotheses de calendrier tiennent dans un bandeau mince ;
- la pastille d'etat « HYPOTHESE · SANS CHIFFRAGE », le trait d'accent, le titre et la navigation ne bougent pas.
Le texte de l'encart retire (titre, pilule, legende, provenance) va dans les notes de la slide, mot pour mot.
Usage (depuis docs/cadrage-ppt/) : py deck_delta/deck.py delta_V36vE --base V35 --sortie C:/tmp/deck-v36-vE/V36vE.pptx --sans-rendu
"""
import deck_base
import deck_draw
from forme_v9 import BLANC, CYAN, LINE, NAVY, PANEL, SLATE, S, carre_num_cyan, carte_diag, forme, tx
from pptx import Presentation
from pptx.enum.text import MSO_ANCHOR as A
from pptx.enum.text import PP_ALIGN as P

BASE = "V35"
NOTE = "V36vE : planning hypothetique sans illustration, planning et livrables en deux foyers"
OPS = []

NB = "\u00a0"
TITRE = "Un planning hypothétique en trois phases, avant tout chiffrage"
EMU = 12700

X0, X1 = 45.0, 659.0          # bords de la grille
QW = (X1 - X0) / 4            # largeur d'un trimestre
Y_Q, H_Q = 86.0, 20.0         # en-tetes de trimestre
Y_J = 112.0                   # losanges des jalons
Y_B, H_B, PAS_B = 130.0, 30.0, 33.0   # barres de phase
Y_L = 232.0                   # etiquette « livrables cles »
Y_C, H_C = 252.0, 68.0        # cartes livrables
Y_H, H_H = 328.0, 38.0        # bandeau hypotheses


def _notes_ajout(s, texte):
    tf = s.notes_slide.notes_text_frame
    ancien = tf.text.strip()
    tf.text = (ancien + "\n\n" if ancien else "") + texte


def _retirer_corps(s):
    """Supprime tout sauf placeholders, navigation et bande d'entete (trait d'accent + pastille d'etat, y < 80 pt)."""
    textes = []
    for sh in list(s.shapes):
        if sh.is_placeholder or sh.name.startswith("nav-") or sh.top < 80 * EMU:
            continue
        if sh.has_text_frame and sh.text_frame.text.strip():
            textes.append(sh.text_frame.text.strip())
        sh._element.getparent().remove(sh._element)
    return textes


def planning(prs):
    s = deck_draw.slide_par_titre(prs, TITRE)
    retires = _retirer_corps(s)
    legende = next(t for t in retires if t.startswith("Illustration"))
    titre_encart = next(t for t in retires if t.startswith("Un rétroplanning"))

    # -------- foyer 1 : le planning
    jalons = [(0.81, "choix du pilote", 1.0, 160.0), (2.19, "comité de décision", 1.0, 193.0), (4.0, "passage de main", 4.0, 226.0)]
    barres = [("Assessment flash", 0.0, 0.81, NAVY), ("Pilote Produit + IA", 0.88, 2.19, CYAN), ("Ancrage", 2.24, 4.0, NAVY)]
    for t in range(1, 4):   # cloisons entre trimestres
        forme(s, S.RECTANGLE, X0 + t * QW - 0.5, Y_B - 3, 1, 226 - (Y_B - 3), LINE, None)
    for t in range(4):
        x = X0 + t * QW
        wq = QW - 4 if t < 3 else QW
        forme(s, S.ROUNDED_RECTANGLE, x, Y_Q, wq, H_Q, PANEL, None, adj=0.5)
        tx(s, x, Y_Q, wq, H_Q, [[(f"Trimestre {t + 1}", 11.5, True, NAVY)]], A.MIDDLE, P.CENTER)
    for f, libelle, _, bas in jalons:   # fil du jalon jusqu'a la fin de sa phase, losange en tete
        cx = X0 + f * QW - (6 if f == 4.0 else 0)
        forme(s, S.RECTANGLE, cx - 0.5, Y_J + 12, 1, bas - (Y_J + 12), NAVY, None)
        forme(s, S.DIAMOND, cx - 6, Y_J, 12, 12, NAVY, None)
        tx(s, cx - 8 - 130, Y_J - 2, 130, 16, [[(libelle, 11, False, SLATE)]], A.MIDDLE, P.RIGHT)
    for k, (nom, a, z, couleur) in enumerate(barres):
        y = Y_B + k * PAS_B
        x0, x1 = X0 + a * QW, X0 + z * QW - (6 if z == 4.0 else 0)
        forme(s, S.ROUNDED_RECTANGLE, x0, y, x1 - x0, H_B, couleur, None, adj=0.5)
        encre = BLANC if couleur == NAVY else NAVY
        tx(s, x0 + 4, y, x1 - x0 - 8, H_B, [[(nom, 11, True, encre)], [("durée à valider", 11, False, encre)]], A.MIDDLE, P.CENTER)

    # -------- foyer 2 : les livrables cles, trois cartes dans l'ordre des phases
    tx(s, X0, Y_L, 130, 16, [[("LIVRABLES CLÉS", 11, True, SLATE)]], A.MIDDLE)
    forme(s, S.RECTANGLE, X0 + 112, Y_L + 8, X1 - X0 - 112, 1, LINE, None)
    cartes = [("Assessment flash", ["baseline", "pilote choisi"]),
              ("Pilote", ["produit Infra livré", "indicateurs avant → après"]),
              ("Ancrage", ["relais formés", "passage de main"])]
    G = 12.0
    W = (X1 - X0 - 2 * G) / 3
    for k, (nom, lignes) in enumerate(cartes):
        x = X0 + k * (W + G)
        carte_diag(s, x, Y_C, W, H_C, adj=0.1)
        carre_num_cyan(s, x + 10, Y_C + 8, 20, k + 1, sz=11)
        tx(s, x + 38, Y_C + 8, W - 46, 20, [[(nom, 12.5, True, NAVY)]], A.MIDDLE)
        for j, t in enumerate(lignes):
            forme(s, S.OVAL, x + 14, Y_C + 35 + j * 15 + 4.5, 5, 5, CYAN, None)
            tx(s, x + 26, Y_C + 33 + j * 15, W - 32, 14, [[(t, 11.5, False, NAVY)]], A.MIDDLE)

    # -------- bandeau mince : hypotheses de calendrier
    forme(s, S.ROUNDED_RECTANGLE, X0, Y_H, X1 - X0, H_H, PANEL, None, adj=0.2)
    tx(s, X0 + 12, Y_H + 4, 250, 14, [[("HYPOTHÈSES DE CALENDRIER", 11, True, SLATE)]], A.MIDDLE)
    hyp = [("Démarrage après le choix du périmètre", X0 + 12, 215), ("Durées à caler avec vous", X0 + 247, 160), ("Le chiffrage est traité à part", X0 + 430, 170)]
    for t, x, w in hyp:
        forme(s, S.OVAL, x, Y_H + 24.5, 5, 5, CYAN, None)
        tx(s, x + 11, Y_H + 20, w, 14, [[(t, 11, False, NAVY)]], A.MIDDLE)

    _notes_ajout(s, "Illustration retirée à la demande" + NB + ": extrait de la bibliothèque de slides OCTO (extrait recadré, phases Cadrage et Conception, "
                    "d'un rétroplanning ; source « Slides préformatées OCTO.pptx », slide 133).\n"
                    "Texte de l'encart retiré" + NB + ": pilule « ILLUSTRATION », titre « " + titre_encart + " », légende « " + legende + " »")


def _ids():
    prs = Presentation(deck_base.resoudre_base(BASE))
    return [f"id:{deck_draw.slide_par_titre(prs, TITRE).slide_id}"]


ETAPES = [{"declarer": _ids(), "f": planning, "nouvelles_max": 0, "nom": "planning : illustration retiree, planning et livrables recomposes"}]
