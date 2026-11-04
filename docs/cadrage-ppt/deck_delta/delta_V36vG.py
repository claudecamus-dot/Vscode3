"""Delta V36vG (base V35) : encarts « ILLUSTRATION » plus sobres, legendes d'origine retirees.

Demande : « pour tous les encarts illustration voir pour un affichage plus sobre comme dans le PPT vscode8 » puis
« modifie toutes les legendes d'illustrations dans le PPT ».
Lecture de la 2e demande (ambigue, a corriger si besoin) : la REFERENCE D'ORIGINE de chaque legende (« extrait d'un support de methode OCTO, anonymise ... »,
« Source : Grille d'evaluation OCTO ... ») quitte la slide et va mot pour mot dans les notes (« Reference des illustrations (retiree de la slide) ») ;
ce qui n'est pas une origine reste (« Exemple illustratif, aucune donnee client. »). Lecture alternative : reformuler chaque legende au lieu de la retirer.

Restylage GENERIQUE (aucune position absolue) : on trouve la pastille par son texte « ILLUSTRATION », son panneau = le rectangle arrondi gris qui la contient.
- panneau : fond blanc, filet fin LINE (plus d'aplat gris) ;
- pastille : contour navy fin, fond blanc, texte navy 9,5 pt (plus d'aplat navy) ;
- titre de l'encart : graisse normale ;
- legende d'origine : retiree (notes) ; l'image, clipee a son cadre, est recentree dans la hauteur libre du panneau si une bande est apparue.
Usage (depuis docs/cadrage-ppt/) : py deck_delta/deck.py delta_V36vG --base V35 --sortie C:/tmp/deck-v36-vG/V36vG.pptx --sans-rendu
"""
import re

import deck_base
import deck_draw
from forme_v9 import BLANC, LINE, NAVY, PANEL, deplacer, restyle, supprimer, texte_couleur
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE as MST
from pptx.util import Pt

BASE = "V35"
NOTE = "V36vG : encarts ILLUSTRATION sobres (panneau blanc a filet, pastille en contour), references d'origine des legendes dans les notes"
OPS = []

NB = "\u00a0"
MOT = "ILLUSTRATION"
T_ENCART_RETIRE = "Un planning hypothétique en trois phases, avant tout chiffrage"  # encart supprime par un autre lot : on n'y touche pas
ORIGINE_LEGENDE = re.compile(r"^Illustration\s*:.*(extrait|anonymis|valider avant diffusion)", re.S)
ORIGINE_SOURCE = re.compile(r"^(Source\s*:\s*Grille d'évaluation OCTO.*?\.)\s+(Exemple illustratif.*)$", re.S)
E = 12700


def _pt(sh):
    return sh.left / E, sh.top / E, sh.width / E, sh.height / E


def _contient(g, p, tol=1.0):
    gx, gy, gw, gh = g
    px, py, pw, ph = p
    return gx - tol <= px and gy - tol <= py and gx + gw + tol >= px + pw and gy + gh + tol >= py + ph


def _rgb(sh):
    try:
        return str(sh.fill.fore_color.rgb) if sh.fill.type == 1 else None
    except (AttributeError, TypeError):
        return None


def _notes_ajout(s, texte):
    tf = s.notes_slide.notes_text_frame
    ancien = tf.text.strip()
    tf.text = (ancien + "\n\n" if ancien else "") + texte


def _encarts(s):
    """[(texte_pastille, forme_pastille, panneau)] : pastille = texte exact ILLUSTRATION ; panneau = plus petit rectangle arrondi gris qui la contient."""
    trouves = []
    for t in s.shapes:
        if t.has_text_frame and t.text_frame.text.strip() == MOT:
            bb = _pt(t)
            pastille = next((f for f in s.shapes if f is not t and f.shape_type == MST.AUTO_SHAPE and _pt(f) == bb), None)
            panneaux = [f for f in s.shapes if f.shape_type == MST.AUTO_SHAPE and f is not pastille and _rgb(f) == str(PANEL) and _contient(_pt(f), bb)]
            if pastille is not None and panneaux:
                trouves.append((t, pastille, min(panneaux, key=lambda f: _pt(f)[2] * _pt(f)[3])))
    return trouves


def _sobre(s, texte, pastille, panneau):
    px, py, pw, ph = _pt(panneau)
    # panneau : plus de fond gris, un filet fin
    restyle(panneau, fill=BLANC, ligne=LINE, lw=0.75)
    # pastille : contour navy, fond blanc, texte navy 9,5 pt
    restyle(pastille, fill=BLANC, ligne=NAVY, lw=0.75)
    texte_couleur(texte, NAVY)
    for r in (r for p in texte.text_frame.paragraphs for r in p.runs):
        r.font.size = Pt(9.5)
        r.font.bold = True
    # titre de l'encart : meme ligne que la pastille, a sa droite -> graisse normale
    tx0, ty0, tw0, th0 = _pt(texte)
    for sh in s.shapes:
        if sh is texte or not sh.has_text_frame or not sh.text_frame.text.strip():
            continue
        x, y, w, h = _pt(sh)
        if x >= tx0 + tw0 - 1 and abs((y + h / 2) - (ty0 + th0 / 2)) <= 3 and _contient((px, py, pw, ph), (x, y, w, h)):
            for r in (r for p in sh.text_frame.paragraphs for r in p.runs):
                r.font.bold = False
                r.font.size = Pt(11)
    return panneau


def _legendes(s, panneau, notes):
    """Retire les legendes d'origine DANS le panneau (texte verbatim vers `notes`). Rend True si au moins une a ete retiree."""
    retire = False
    for sh in list(s.shapes):
        if sh.has_text_frame and _contient(_pt(panneau), _pt(sh)) and ORIGINE_LEGENDE.match(sh.text_frame.text.strip()):
            notes.append(sh.text_frame.text.strip())
            supprimer(sh)
            retire = True
    return retire


def _recentrer(s, texte, panneau):
    """Une bande vide sous l'image (legende retiree) : l'image, clipee a son cadre, est recentree dans la hauteur libre sous l'en-tete du panneau."""
    px, py, pw, ph = _pt(panneau)
    entete_bas = _pt(texte)[1] + _pt(texte)[3]
    for sh in s.shapes:
        if sh.shape_type == MST.PICTURE and _contient(_pt(panneau), _pt(sh)):
            x, y, w, h = _pt(sh)
            haut, bas = y - entete_bas, py + ph - (y + h)
            if bas - haut > 8:
                deplacer(sh, y=y + (bas - haut) / 2)


def encarts_sobres(prs, s):
    notes = []
    for texte, pastille, panneau in _encarts(s):
        _sobre(s, texte, pastille, panneau)
        if _legendes(s, panneau, notes):
            _recentrer(s, texte, panneau)
    for sh in list(s.shapes):  # ligne « Source : <grille OCTO>. Exemple illustratif ... » hors panneau : l'origine part, la mention de protection reste
        if sh.has_text_frame:
            m = ORIGINE_SOURCE.match(sh.text_frame.text.strip())
            if m and m.group(2):
                notes.append(m.group(1))
                deck_draw.set_run(sh, m.group(2))
    if notes:
        _notes_ajout(s, "Référence des illustrations (retirée de la slide)" + NB + ":\n" + "\n".join(f"« {n} »" for n in notes))


def _slides_a_traiter(prs):
    """Slides ayant au moins un encart ILLUSTRATION (hors celle dont l'encart est supprime par un autre lot)."""
    return [s for s in prs.slides if _encarts(s) and deck_draw.titre_slide(s) != T_ENCART_RETIRE]


def sobre(prs):
    """Toutes les slides declarees portent un encart ILLUSTRATION ; une slide sans encart (retire entre-temps) est ignoree."""
    for s in _slides_a_traiter(prs):
        encarts_sobres(prs, s)


def _ids():
    prs = Presentation(deck_base.resoudre_base(BASE))
    return [f"id:{s.slide_id}" for s in _slides_a_traiter(prs)]


ETAPES = [{"declarer": _ids(), "f": sobre, "nouvelles_max": 0, "nom": "encarts ILLUSTRATION sobres + references d'origine des legendes vers les notes"}]
