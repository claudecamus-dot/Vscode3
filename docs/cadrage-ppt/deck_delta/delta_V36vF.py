"""Delta V36vF (base V35) : (1) slide « De la douleur au produit… » sans la reference d'origine de l'illustration ;
(2) chapitre « Démarche détaillée » regroupe par phase, comme dans le deck Vscode8.

Mecanisme repris de Vscode8 (deck de reference, chapitre « Demarche detaillee ») : aucune slide intercalaire de phase ; les slides sont ORDONNEES phase par phase
(vue d'ensemble d'abord, puis chaque phase avec ses slides les unes derriere les autres) et CHAQUE slide de phase porte un marqueur de phase, un suiveur de
chips « Phase 1 | Phase 2 | Phase 3 | Phase 4 » dont la phase courante est pleine (navy) et les autres pales. Ici : « DIAGNOSTIQUER | EXPÉRIMENTER | ANCRER | TRANSVERSE »,
sous le titre a gauche (x 45, y 59.5), hors de la rangee de navigation (a droite, en haut). Les deux slides d'ensemble (calendrier, mission pilote)
n'ont pas de suiveur : elles presentent toutes les phases (comme les slides « Demarche globale » de Vscode8).
Aucune slide creee ; titres, navigation, numero de page non touches ; sections p14 mises a jour par `deplacer_apres`.
Usage (depuis docs/cadrage-ppt/) : py deck_delta/deck.py delta_V36vF --base V35 --sortie C:/tmp/deck-v36-vF/V36vF.pptx --sans-rendu
"""
import deck_base
import deck_draw
from forme_v9 import BLANC, LINE, NAVY, SLATE, S, forme
from pptx import Presentation
from pptx.enum.text import MSO_ANCHOR as A
from pptx.enum.text import PP_ALIGN as P
from pptx.util import Pt

BASE = "V35"
NOTE = "V36vF : slide mission pilote sans reference d'origine de l'illustration ; Demarche detaillee regroupee par phase (suiveur de phase sur chaque slide)"
OPS = []

NB = "\u00a0"
T_MISSION = "De la douleur au produit : une mission pilote de bout en bout"
T_CALENDRIER = "Calendrier du pilote : étapes et jalons, durées à valider"
T_PILIERS = "Le diagnostic s'appuie sur cinq piliers, du mode produit à l'agentic"
T_LIV1 = "Exemples de livrables (1/2) : comprendre et décider"
T_LIV2 = "Exemples de livrables (2/2) : piloter et ancrer"
T_MESURE = "Nous mesurons la valeur client et l'apport du coaching augmenté"
T_COMITES = "Deux comités en parallèle : l'un suit l'exécution, l'autre décide"
T_ATTENTES = "Ce que nous attendons de vous, et comment nous passons la main"
T_MODES = "Du pilote à l'autonomie : trois modes d'interaction entre OCTO et le client"
T_IA = "L'IA est gouvernée : données, droits, validations et traçabilité"
T_RISQUES = "Risques et objections : ce que nous répondons, ce que nous mesurons"

LEGENDE_RETIREE = "Illustration" + NB + ": extrait d'un support de méthode OCTO, anonymisé — à valider avant diffusion."

PHASES = ("DIAGNOSTIQUER", "EXPÉRIMENTER", "ANCRER", "TRANSVERSE")
LARGEURS = (92, 90, 56, 80)
X_SUIVEUR, Y_SUIVEUR, H_SUIVEUR, ECART = 45, 59.5, 14, 4

# (titre, phases actives) dans l'ordre FINAL ; les deux slides d'ensemble (calendrier, mission) n'ont pas de suiveur.
ORDRE_FINAL = (
    (T_CALENDRIER, ()),
    (T_MISSION, ()),
    (T_PILIERS, (0,)),      # « La grille cadre le diagnostic de l'Assessment flash »
    (T_LIV1, (0,)),         # comprendre et decider : cartographie, baseline, fiche produit, priorisation
    (T_MESURE, (1,)),       # etat de depart documente, resultat mesure en fin de pilote
    (T_LIV2, (1, 2)),       # piloter (roadmap, tableau de bord, charte IA) et ancrer (plan de passage de main)
    (T_MODES, (2,)),        # du pilote a l'autonomie : le client prend la main pas a pas
    (T_COMITES, (3,)),
    (T_ATTENTES, (3,)),
    (T_IA, (3,)),
    (T_RISQUES, (3,)),
)


# ---------------------------------------------------------------- suiveur de phase
def _chip(s, x, w, texte, actif, nom):
    r = forme(s, S.ROUNDED_RECTANGLE, x, Y_SUIVEUR, w, H_SUIVEUR, NAVY if actif else BLANC, None if actif else LINE, adj=0.5, lw=0.75)
    r.name = nom
    tf = r.text_frame
    tf.word_wrap = False
    tf.vertical_anchor = A.MIDDLE
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.alignment = P.CENTER
    run = p.add_run()
    run.text = texte
    run.font.size, run.font.bold, run.font.name = Pt(9.5), True, "Outfit"
    run.font.color.rgb = BLANC if actif else SLATE


def suiveur(s, actives):
    """Quatre chips ; les phases actives sont pleines navy, les autres blanches a bord fin."""
    for sh in [x for x in s.shapes if x.name.startswith("phase-")]:
        sh._element.getparent().remove(sh._element)
    x = X_SUIVEUR
    for i, (texte, w) in enumerate(zip(PHASES, LARGEURS, strict=True)):
        _chip(s, x, w, texte, i in actives, f"phase-{i + 1}-{texte.lower()}")
        x += w + ECART


# ---------------------------------------------------------------- slide mission pilote : retrait de la reference d'origine
def mission(prs):
    s = deck_draw.slide_par_titre(prs, T_MISSION)
    legende = [sh for sh in s.shapes if sh.has_text_frame and sh.text_frame.text == LEGENDE_RETIREE]
    assert len(legende) == 1, "legende d'illustration introuvable ou ambigue"
    legende[0]._element.getparent().remove(legende[0]._element)
    pic = next(sh for sh in s.shapes if sh.name == "illustration")
    panneau = next(sh for sh in s.shapes if sh.shape_type == 1 and abs(sh.left / 12700 - 393) < 1 and sh.height / 12700 > 200)
    # l'image grandit a la largeur utile du panneau (marge 6 pt), proportions gardees, rognee a la meme forme (round2DiagRect)
    ratio = pic.width / pic.height
    w = 266 - 12
    h = w / ratio
    pic.left, pic.top = int((393 + 6) * 12700), int(142 * 12700)
    pic.width, pic.height = int(w * 12700), int(h * 12700)
    panneau.height = int((142 + h + 8 - 111.4) * 12700)
    notes = s.notes_slide.notes_text_frame
    ajout = "Référence de l'illustration (retirée de la slide à la demande)" + NB + ": " + LEGENDE_RETIREE
    notes.text = (notes.text.rstrip() + "\n" + ajout) if notes.text.strip() else ajout


# ---------------------------------------------------------------- regroupement par phase
def regrouper(prs):
    mission(prs)
    titres = [t for t, _ in ORDRE_FINAL]
    # une seule passe : on place chaque slide apres sa predecesseure de l'ordre final (les slides deja bien placees ne bougent pas)
    courant = [sl.shapes.title.text_frame.text for sl in prs.slides]
    debut = courant.index(titres[0])
    for k in range(1, len(titres)):
        actuel = [sl.shapes.title.text_frame.text for sl in prs.slides]
        if actuel[debut + k] != titres[k]:
            deck_draw.deplacer_apres(prs, deck_draw.slide_par_titre(prs, titres[k]), deck_draw.slide_par_titre(prs, titres[k - 1]))
    for titre, actives in ORDRE_FINAL:
        if actives:
            suiveur(deck_draw.slide_par_titre(prs, titre), actives)
        # les slides d'ensemble n'ont pas de suiveur


def _ids():
    prs = Presentation(deck_base.resoudre_base(BASE))
    return [f"id:{deck_draw.slide_par_titre(prs, t).slide_id}" for t, _ in ORDRE_FINAL]


ETAPES = [{"declarer": _ids(), "f": regrouper, "nouvelles_max": 0, "nom": "mission pilote sans reference d'origine ; Demarche detaillee regroupee par phase"}]
