"""Delta V36vD (base V35, lot vD du chantier V36) : convictions 12 (RUN pret) et 13 (modele d'organisation Infra) sans les zones « Le critere observable » / « Le chantier ».

Demande : « supprimer dans les slides de convictions les 2 zones "criteres observables" et "le chantier" et revoir la forme de chacune des slides ».
- les deux bandeaux du bas sont retires ; leurs textes partent TELS QUELS dans les notes (« Critere observable (retire de la slide) » / « Chantier (retire de la slide) »), a la suite des notes existantes ;
- zone du corps recomposee sur x 258..659, y 92..366 ; rail gauche (goutte + pilule CONVICTION) conserve ;
- conviction 12 : frise Construire > Porte « RUN pret » (seul aplat navy) > Exploiter > Apprendre, carte des quatre criteres numerotes, puis deux blocs « Apprendre » et « Avec IA, selon la maturite » ;
- conviction 13 : fleche verticale « par specialite technique -> par produit et par service rendu », cinq formes en lignes (numero, nom, definition), bandeau navy « Chaque entite choisit sa forme... » ;
  les cinq « Pour ... » (contextes) et les elements deja en notes partent dans les notes. La slide n'avait PAS de goutte-pictogramme a gauche : elle est ajoutee (meme gabarit que la conviction 12) et la pilule
  CONVICTION 13 passe de y 98 a y 226 pour rejoindre la position des autres convictions (famille). Ligne de source conservee en bas.
Chrome intact : pilules « nav-* », titre, pastilles de progression (y 70), filet (y 86), numero de page.
Usage (depuis docs/cadrage-ppt/) : py deck_delta/deck.py delta_V36vD --base V35 --sortie C:/tmp/deck-v36-vD/V36vD.pptx --sans-rendu
"""
import deck_base
import deck_draw
from forme_ground import goutte_contour, trait
from forme_v9 import (
    BLANC,
    CYAN,
    LINE,
    NAVY,
    PANEL,
    S,
    carre_num_cyan,
    carte_diag,
    chevron_sep,
    forme,
    pilule_entete,
    tx,
)
from pptx import Presentation
from pptx.enum.text import MSO_ANCHOR as A
from pptx.enum.text import PP_ALIGN as P

BASE = "V35"
NOTE = "V36vD : convictions 12 et 13 sans criteres observables ni chantiers ; recomposition du corps (x 258..659, y 92..366), textes retires copies dans les notes"
OPS = []

NB = "\u00a0"
NBH = "\u2011"  # trait d'union insecable : « post-mortem » ne se coupe plus en fin de ligne
EMU = 12700
ZX, ZW = 258, 401  # zone du corps : x 258..659
PILL_CRIT, PILL_CHANT = "LE CRITÈRE OBSERVABLE", "LE CHANTIER"

# ---------------------------------------------------------------- conviction 12
FRISE = [("Construire", 76, False), ("Porte" + NB + "«" + NB + "RUN" + NB + "prêt" + NB + "»", 133, True), ("Exploiter", 76, False), ("Apprendre", 80, False)]
CRITERES = [
    ("Équipe" + NB + ": ", "un propriétaire nommé, deux personnes capables par module."),
    ("Supervision" + NB + ": ", "alertes et astreinte définies."),
    ("Connaissance" + NB + ": ", "procédure d'incident documentée."),
    ("Budget" + NB + ": ", "RUN inscrit dans le business case."),
]
APPRENDRE = "Chaque incident majeur" + NB + ": un post" + NBH + "mortem, puis une action au backlog."
AVEC_IA = "L'IA aide à diagnostiquer et trier les incidents" + NB + "; l'humain décide, chaque sortie est relue et tracée."

# ---------------------------------------------------------------- conviction 13
FORMES = [
    ("Silos technologiques", "Une équipe par spécialité technique."),
    ("Services mutualisés", "Un centre commun livre des services sur catalogue."),
    ("Orienté services", "Un responsable garantit le service de bout en bout."),
    ("Plateforme produit", "Des plateformes internes gérées comme des produits."),
    ("Fédéré / hybride", "Un noyau commun et des équipes autonomes."),
]
POUR = [
    "Pour parcs historiques et expertises rares",
    "Pour plusieurs entités aux besoins répétables",
    "Pour des services traversant plusieurs équipes",
    "Pour demandes répétées, nombreux clients internes",
    "Pour grands groupes aux entités multiples",
]
MESSAGE = "Chaque entité choisit sa forme selon sa maturité, sa criticité et sa taille" + NB + ": aucune n'est imposée."
HAUT, BAS = "Par spécialité technique", "Par produit et par service rendu"


def _titre(debut):
    prs = Presentation(deck_base.resoudre_base(BASE))
    t = [s.shapes.title.text_frame.text for s in prs.slides if s.shapes.title is not None and s.shapes.title.text_frame.text.startswith(debut)]
    if len(t) != 1:
        raise ValueError(f"{debut} : {len(t)} slide(s) ; 1 exigee")
    return t[0]


T12, T13 = _titre("Conviction 12"), _titre("Conviction 13")


def _retirer(sh):
    sh._element.getparent().remove(sh._element)


def _textes_retires(s, y_min):
    """Textes des deux bandeaux (critere, chantier) lus sur la slide, tels quels, de gauche a droite."""
    out = []
    for sh in s.shapes:
        if not sh.has_text_frame or sh.is_placeholder or sh.name.startswith("nav-"):
            continue
        t = sh.text_frame.text
        if sh.top >= y_min * EMU and sh.left >= 85 * EMU and sh.top + sh.height <= 370 * EMU and t.strip() and t not in (PILL_CRIT, PILL_CHANT) and not t.startswith("Source"):
            out.append((sh.left, t))
    out.sort()
    if len(out) != 2:
        raise ValueError(f"bandeaux : {len(out)} texte(s) ; 2 exigés")
    return out[0][1], out[1][1]


def _notes(s, ajout):
    ancien = s.notes_slide.notes_text_frame.text if s.has_notes_slide else ""
    s.notes_slide.notes_text_frame.text = (ancien + "\n" if ancien else "") + ajout


def _bloc_retire(critere, chantier):
    return ("V36 : zones « Le critère observable » et « Le chantier » retirées de la slide (demande utilisateur), textes conservés ici." + "\n"
            "Critère observable (retiré de la slide)" + NB + ": " + critere + "\n"
            "Chantier (retiré de la slide)" + NB + ": " + chantier)


def run_pret(prs):
    s = deck_draw.slide_par_titre(prs, T12)
    critere, chantier = _textes_retires(s, 270)
    for sh in list(s.shapes):
        if sh.is_placeholder or sh.name.startswith("nav-"):
            continue
        bas = sh.top + sh.height
        if sh.top >= 270 * EMU or (sh.left >= 185 * EMU and sh.top >= 92 * EMU and bas <= 270 * EMU):
            _retirer(sh)
    # frise : Construire > Porte « RUN pret » (accent navy) > Exploiter > Apprendre
    x = ZX
    for k, (nom, w, porte) in enumerate(FRISE):
        forme(s, S.ROUNDED_RECTANGLE, x, 94, w, 22, NAVY if porte else PANEL, None, adj=0.5)
        tx(s, x, 94, w, 22, [[(nom, 11.5, True, BLANC if porte else NAVY)]], A.MIDDLE, P.CENTER)
        x += w
        if k < len(FRISE) - 1:
            chevron_sep(s, x + 2.5, 99, 7, 12)
            x += 12
    # la porte : quatre criteres numerotes
    gx, gy, gw, gh = ZX, 130, ZW, 135
    carte_diag(s, gx, gy, gw, gh, adj=0.07)
    pilule_entete(s, gx + 14, gy - 9, 262, 18, "4 CRITÈRES AVANT LA MISE EN SERVICE", NAVY, sz=11)
    y = gy + 12
    for k, (label, texte) in enumerate(CRITERES):
        h = 31 if k == 0 else 25
        carre_num_cyan(s, gx + 12, y + (h - 22) / 2, 22, k + 1, sz=12)
        tx(s, gx + 44, y, gw - 56, h, [[(label, 12, True, NAVY), (texte, 12, False, NAVY)]], A.MIDDLE)
        y += h + 3
    # deux blocs : Apprendre (gris), Avec IA selon la maturite (carte a bord fin)
    by, bh = 282, 80
    aw = 180
    forme(s, S.ROUNDED_RECTANGLE, ZX, by, aw, bh, PANEL, None, adj=0.1)
    pilule_entete(s, ZX + 12, by - 8, 92, 18, "APPRENDRE", NAVY, sz=11)
    tx(s, ZX + 12, by + 12, aw - 24, bh - 16, [[(APPRENDRE, 12, False, NAVY)]], A.MIDDLE)
    ix = ZX + aw + 10
    iw = ZX + ZW - ix
    carte_diag(s, ix, by, iw, bh, adj=0.1)
    pilule_entete(s, ix + 12, by - 8, 188, 18, "AVEC IA · SELON LA MATURITÉ", CYAN, sz=11)
    tx(s, ix + 12, by + 12, iw - 24, bh - 16, [[(AVEC_IA, 12, False, NAVY)]], A.MIDDLE)
    _notes(s, _bloc_retire(critere, chantier) + "\n"
           "Mise en page V36 : « post‑mortem » écrit avec un trait d'union insécable pour ne plus être coupé en fin de ligne.")


def organisation(prs):
    s = deck_draw.slide_par_titre(prs, T13)
    critere, chantier = _textes_retires(s, 285)
    garde_pilule = []
    for sh in list(s.shapes):
        if sh.is_placeholder or sh.name.startswith("nav-"):
            continue
        if sh.top < 92 * EMU:  # pastilles de progression (y 70) et filet cyan (y 86)
            continue
        if sh.has_text_frame and sh.text_frame.text.startswith("Source"):
            continue
        if abs(sh.top - 98 * EMU) < EMU and abs(sh.left - 45 * EMU) < EMU and abs(sh.width - 130 * EMU) < EMU and abs(sh.height - 22 * EMU) < EMU or (
                sh.has_text_frame and sh.text_frame.text.startswith("CONVICTION")):
            garde_pilule.append(sh)
            continue
        _retirer(sh)
    # rail : goutte + pictogramme « organisation » (trois noeuds relies), pilule CONVICTION 13 a la position des autres convictions
    for sh in garde_pilule:
        sh.top = sh.top + 128 * EMU
    goutte_contour(s, 54, 102, 112)
    forme(s, S.OVAL, 83, 131, 55, 55, CYAN, NAVY, lw=2)
    cx, cy = 110.5, 158.5
    for (ax, ay), (bx, by_) in (((cx, cy - 11), (cx - 12, cy + 9)), ((cx, cy - 11), (cx + 12, cy + 9))):
        trait(s, ax, ay, bx, by_, 2)
    for nx, ny in ((cx, cy - 11), (cx - 12, cy + 9), (cx + 12, cy + 9)):
        forme(s, S.OVAL, nx - 5, ny - 5, 10, 10, NAVY, None)
    # fleche de lecture verticale + deux legendes
    top, rh, gap = 114, 32, 4
    fin = top + 5 * rh + 4 * gap
    tx(s, ZX + 22, 93, ZW - 22, 18, [[(HAUT, 12, True, NAVY)]], A.MIDDLE)
    forme(s, S.DOWN_ARROW, ZX, top, 16, fin - top, PANEL, None, adj=0.5)
    # cinq formes en lignes : numero, nom, definition
    rx, rw = ZX + 22, ZW - 22
    for k, (nom, defin) in enumerate(FORMES):
        y = top + k * (rh + gap)
        carte_diag(s, rx, y, rw, rh, adj=0.14)
        carre_num_cyan(s, rx + 9, y + (rh - 22) / 2, 22, k + 1, sz=12)
        tx(s, rx + 39, y, 112, rh, [[(nom, 12, True, NAVY)]], A.MIDDLE)
        forme(s, S.RECTANGLE, rx + 156, y + 6, 0.75, rh - 12, LINE, None)
        tx(s, rx + 164, y, rw - 172, rh, [[(defin, 11.5, False, NAVY)]], A.MIDDLE)
    tx(s, ZX + 22, fin + 3, ZW - 22, 18, [[(BAS, 12, True, NAVY)]], A.MIDDLE)
    # bandeau navy : l'unique accent de la slide
    forme(s, S.ROUND_2_DIAG_RECTANGLE, ZX, 316, ZW, 36, NAVY, None, adj=0.2)
    tx(s, ZX + 14, 316, ZW - 28, 36, [[(MESSAGE, 12, True, BLANC)]], A.MIDDLE, P.CENTER)
    _notes(s, _bloc_retire(critere, chantier) + "\n"
           "Contextes « Pour… » de chaque forme (retirés de la slide V36 pour l'alléger, à reprendre à l'oral) : "
           + " ; ".join(f"{n}" + NB + ": " + p for (n, _), p in zip(FORMES, POUR, strict=True)) + ".")


def _ids():
    prs = Presentation(deck_base.resoudre_base(BASE))
    return [f"id:{deck_draw.slide_par_titre(prs, t).slide_id}" for t in (T12, T13)]


_I12, _I13 = _ids()
ETAPES = [
    {"declarer": [_I12], "f": run_pret, "nouvelles_max": 0, "nom": "conviction 12 : sans bandeaux critere/chantier, frise + porte + apprendre + IA recomposes"},
    {"declarer": [_I13], "f": organisation, "nouvelles_max": 0, "nom": "conviction 13 : sans bandeaux critere/chantier, cinq formes en lignes, rail goutte ajoute"},
]
