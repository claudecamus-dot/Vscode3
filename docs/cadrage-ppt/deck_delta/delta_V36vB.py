"""Delta V36vB (base V35) : conviction slides 7, 8 and 9 recomposed after removal of the two bottom zones.

- The bands « LE CRITERE OBSERVABLE » / « LE CHANTIER » are removed ; their text is copied verbatim into the slide notes.
- Left rail (teardrop pictogram + pill CONVICTION n), progress dots, filet, nav pills, title : untouched.
- Body area x 258..659, y 92..366 rebuilt larger : 7 = AVANT / APRES stacked rows + product-or-component strip,
  8 = two team rows (sans IA / avec IA) with two columns of ticks, 9 = three full-width instance cards (the highest one is the navy accent).
Usage (from docs/cadrage-ppt/) : py deck_delta/deck.py delta_V36vB --base V35 --sortie C:/tmp/deck-v36-vB/V36vB.pptx --sans-rendu
"""
import deck_base
import deck_draw
from forme_ground import coche, trait
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
from pptx import Presentation
from pptx.enum.text import MSO_ANCHOR as A
from pptx.enum.text import PP_ALIGN as P

BASE = "V35"
NOTE = "V36vB : convictions 7, 8 et 9 recomposees, zones critere observable et chantier retirees (texte conserve dans les notes)"
OPS = []

NB = "\u00a0"
T_FINANCER = "Conviction 7 : financer des produits et des équipes stables"
T_EQUIPE = "Conviction 8 : une petite équipe produit qui construit et exploite"
T_INSTANCES = "Conviction 9 : trois instances, chacune avec sa décision"
TITRES = (T_FINANCER, T_EQUIPE, T_INSTANCES)

ZX, ZW = 258, 401.25
EMU = 12700


def _retirer_bandes(s):
    """Retire les deux bandes du bas (top >= 270 pt) et le corps (x >= 185, y >= 92) ; renvoie (critere, chantier) verbatim."""
    critere = chantier = ""
    for sh in s.shapes:
        if sh.is_placeholder or sh.name.startswith("nav-") or not sh.has_text_frame:
            continue
        t = sh.text_frame.text.strip()
        if sh.top >= 270 * EMU and t and not t.startswith("LE CRIT") and not t.startswith("LE CHANTIER"):
            if sh.left < 200 * EMU:
                critere = t
            else:
                chantier = t
    for sh in list(s.shapes):
        if sh.is_placeholder or sh.name.startswith("nav-"):
            continue
        corps = sh.left >= 185 * EMU and sh.top >= 92 * EMU
        bande = sh.top >= 270 * EMU
        if corps or bande:
            sh._element.getparent().remove(sh._element)
    return critere, chantier


def _notes(s, critere, chantier, ajout=""):
    tf = s.notes_slide.notes_text_frame
    ancien = tf.text.strip()
    parts = [ancien] if ancien else []
    if ajout:
        parts.append(ajout)
    parts.append("Critère observable (retiré de la slide)" + NB + ": " + critere)
    parts.append("Chantier (retiré de la slide)" + NB + ": " + chantier)
    tf.text = "\n".join(parts)


def _chevron_bas(s, cx, cy):
    c = forme(s, S.CHEVRON, cx - 6.5, cy - 12, 13, 24, CYAN, None, adj=0.35)
    c.rotation = 90
    return c


def _pastille(s, x, y, w, h, texte, couleur, sz=10.5):
    forme(s, S.ROUNDED_RECTANGLE, x, y, w, h, couleur, None, adj=0.5)
    tx(s, x, y, w, h, [[(texte, sz, True, BLANC if couleur == NAVY else NAVY)]], A.MIDDLE, P.CENTER)


# ================================================================ conviction 7
def financer(prs):
    s = deck_draw.slide_par_titre(prs, T_FINANCER)
    critere, chantier = _retirer_bandes(s)
    ch = 74
    rows = [
        (104, False, "AVANT", "Un budget par projet", "financé projet par projet",
         "dissoute à la fin du projet.", "transféré à d'autres équipes."),
        (200, True, "APRÈS", "Une capacité par produit", "budget annuel rattaché au produit",
         "stable, elle construit et exploite.", "reste dans l'équipe qui construit."),
    ]
    for y, apres, pastille, titre, sous, equipe, run in rows:
        if apres:
            forme(s, S.ROUND_2_DIAG_RECTANGLE, ZX, y, ZW, ch, NAVY, None, adj=0.1)
            ink, doux = BLANC, BLANC
        else:
            carte_diag(s, ZX, y, ZW, ch, adj=0.1)
            ink, doux = NAVY, SLATE
        _pastille(s, ZX + 14, y - 9, 66, 18, pastille, CYAN if apres else PANEL)
        tx(s, ZX + 16, y + 15, 176, 22, [[(titre, 14, True, ink)]], A.TOP)
        tx(s, ZX + 16, y + 38, 168, 32, [[(sous, 11.5, False, doux)]], A.TOP)
        forme(s, S.RECTANGLE, ZX + 200, y + 12, 0.75, ch - 24, BLANC if apres else LINE, None)
        tx(s, ZX + 212, y + 9, ZW - 224, 31, [[("Équipe" + NB + ": ", 12, True, ink), (equipe, 12, False, ink)]], A.TOP)
        tx(s, ZX + 212, y + 40, ZW - 224, 31, [[("RUN" + NB + ": ", 12, True, ink), (run, 12, False, ink)]], A.TOP)
    _chevron_bas(s, ZX + ZW / 2, 189)
    # produit ou composant : enonce, plus de question
    py_, ph = 302, 64
    forme(s, S.ROUNDED_RECTANGLE, ZX, py_, ZW, ph, PANEL, None, adj=0.15)
    pilule_entete(s, ZX + 14, py_ - 9, 170, 18, "PRODUIT OU COMPOSANT", NAVY, sz=10)
    tx(s, ZX + 16, py_ + 14, ZW - 32, 17, [[("Un produit a une offre, une valeur et des engagements.", 12.5, True, NAVY)]], A.MIDDLE)
    tx(s, ZX + 16, py_ + 38, 190, 17, [[("Produits" + NB + ": ", 12, True, NAVY), ("Kubernetes, CI/CD, IAM", 12, False, NAVY)]], A.MIDDLE)
    tx(s, ZX + 214, py_ + 38, 175, 17, [[("Composants" + NB + ": ", 12, True, NAVY), ("VM, serveur, SAN", 12, False, NAVY)]], A.MIDDLE)
    _notes(s, critere, chantier)


# ================================================================ conviction 8
def equipe(prs):
    s = deck_draw.slide_par_titre(prs, T_EQUIPE)
    critere, chantier = _retirer_bandes(s)
    lignes = [
        (98, 130, 1, "Équipe produit", "SANS IA", PANEL, [
            [("Un binôme" + NB + ": responsable produit et référent technique. Pas un PO posé dans l'Infra.", 3),
             ("Une même équipe conçoit, livre et assure le service.", 2)],
            [("Du temps de construction protégé.", 2),
             ("Demandes récurrentes automatisées, en self-service.", 2)],
        ]),
        (248, 114, 2, "Équipe augmentée", "AVEC IA · OPTION SELON LA MATURITÉ", NAVY, [
            [("Mêmes rôles, plus des agents.", 1),
             ("Les agents préparent le travail récurrent et le diagnostic.", 2)],
            [("L'IA prépare ; l'humain décide et en répond.", 2),
             ("Effets visés, à mesurer ; rien n'est promis.", 2)],
        ]),
    ]
    colw = 182
    for y, h, num, titre, chip, couleur, cols in lignes:
        carte_diag(s, ZX, y, ZW, h, adj=0.08)
        carre_num_cyan(s, ZX + 12, y + 10, 22, num, sz=12)
        tx(s, ZX + 42, y + 10, 120, 22, [[(titre, 13.5, True, NAVY)]], A.MIDDLE)
        cw_ = 90 if num == 1 else 218
        _pastille(s, ZX + ZW - 12 - cw_, y + 12, cw_, 18, chip, couleur, sz=10)
        for k, col in enumerate(cols):
            x = ZX + 14 + k * (colw + 12)
            yy = y + 40
            for t, nl in col:
                coche(s, x + 6.5, yy + 7.5, 13)
                tx(s, x + 18, yy, colw - 18, 14.8 * nl, [[(t, 12, False, NAVY)]], A.TOP)
                yy += 14.8 * nl + 8
    _chevron_bas(s, ZX + ZW / 2, 238)
    _notes(s, critere, chantier)


# ================================================================ conviction 9
INSTANCES = [
    ("COMOP", "comité opérationnel", "ajustements, risques, escalades", "équipe, coach, relais client", "cadence à fixer avec vous"),
    ("COPIL", "comité de pilotage", "backlog et roadmap du produit", "responsable produit, métiers, équipe", "cadence à fixer avec vous"),
    ("Comité d'investissement", "revue trimestrielle des budgets", "arrêter, étendre ou pivoter une capacité", "sponsor, DSI, responsables produit", "cadence trimestrielle, à valider"),
]


def instances(prs):
    s = deck_draw.slide_par_titre(prs, T_INSTANCES)
    critere, chantier = _retirer_bandes(s)
    h, pas, y0 = 82, 92, 98
    for k, (nom, sous, decide, avec, cadence) in enumerate(INSTANCES):
        y = y0 + k * pas
        haut = k == 2
        if haut:
            forme(s, S.ROUND_2_DIAG_RECTANGLE, ZX, y, ZW, h, NAVY, None, adj=0.15)
            ink, doux = BLANC, BLANC
        else:
            carte_diag(s, ZX, y, ZW, h, adj=0.15)
            ink, doux = NAVY, SLATE
        carre_num_cyan(s, ZX + 12, y + 6, 24, k + 1, sz=12.5)
        tx(s, ZX + 46, y + 6, ZW - 58, 24, [[(nom + "  ", 15, True, ink), (sous, 11.5, False, doux)]], A.MIDDLE)
        tx(s, ZX + 46, y + 31, ZW - 58, 17, [[("Décide" + NB + ": ", 12.5, True, ink), (decide, 12.5, True, ink)]], A.MIDDLE)
        tx(s, ZX + 46, y + 49, ZW - 58, 16, [[("Avec" + NB + ": ", 12, True, ink), (avec, 12, False, ink)]], A.MIDDLE)
        tx(s, ZX + 46, y + 65, ZW - 58, 14, [[(cadence, 11, False, doux)]], A.MIDDLE)
    for k in range(2):
        trait(s, ZX + 24, y0 + k * pas + 30, ZX + 24, y0 + (k + 1) * pas + 6, 1.25)
    _notes(s, critere, chantier)


def _ids():
    prs = Presentation(deck_base.resoudre_base(BASE))
    return [f"id:{deck_draw.slide_par_titre(prs, t).slide_id}" for t in TITRES]


_I = dict(zip(TITRES, _ids(), strict=True))
ETAPES = [
    {"declarer": [_I[T_FINANCER]], "f": financer, "nouvelles_max": 0, "nom": "conviction 7 : avant / apres + produit ou composant (recomposee)"},
    {"declarer": [_I[T_EQUIPE]], "f": equipe, "nouvelles_max": 0, "nom": "conviction 8 : sans IA / avec IA (recomposee)"},
    {"declarer": [_I[T_INSTANCES]], "f": instances, "nouvelles_max": 0, "nom": "conviction 9 : COMOP, COPIL, comite d'investissement (recomposee)"},
]
