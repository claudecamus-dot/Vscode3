"""Delta V39i (base V38) : convictions 10 a 13 (rangs 16-19), « goutte reduite, pleine largeur ».

Arbitrage utilisateur du 2026-11-03 : le bloc goutte + pictogramme du rail passe a 56 x 56 pt en (45, 94) ;
le corps occupe la bande haute x 113 -> 659.25, y 92 -> 150, puis toute la largeur x 45 -> 659.25, y 158 -> 366.
Meme texte, un seul accent navy par slide. Points de progression, filet, navigation, titre, source : non touches.
Usage (depuis docs/cadrage-ppt/) : py deck_delta/deck.py delta_V39i --base V38 --sortie C:/tmp/deck-v39-i/V39i.pptx --sans-rendu
"""
import deck_base
import deck_draw
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

BASE = "V38"
NOTE = "V39i : convictions 10-13, goutte reduite 56 pt et corps pleine largeur (meme texte)"
OPS = []

NB = "\u00a0"
EMU = 12700


def goutte_reduite(slide):
    """Goutte du rail (+ pictogramme) ramenee a une boite 56 x 56 pt en (45, 94), proportions gardees."""
    bloc = [sh for sh in slide.shapes
            if not sh.is_placeholder and not sh.name.startswith("nav-")
            and sh.left / EMU < 189 and 95 <= sh.top / EMU < 300]
    tear = [sh for sh in bloc if sh.name.startswith("Teardrop")]
    if not tear:
        return
    t = tear[0]
    x0, y0, k = t.left, t.top, 56 * EMU / t.width
    for sh in bloc:
        sh.left = int(45 * EMU + (sh.left - x0) * k)
        sh.top = int(94 * EMU + (sh.top - y0) * k)
        sh.width = int(sh.width * k)
        sh.height = int(sh.height * k)


XB, XG, XD = 113.0, 45.0, 659.25   # bande haute, gauche pleine largeur, droite
YB0, YB1, YC0, YC1 = 92.0, 150.0, 158.0, 366.0
LW = XD - XG


def _retirer_corps(s):
    for sh in list(s.shapes):
        if sh.is_placeholder or sh.name.startswith("nav-"):
            continue
        if sh.left / EMU >= 189 and sh.top / EMU >= 88:
            sh._element.getparent().remove(sh._element)


def _navy(sh):
    sh.fill.solid()
    sh.fill.fore_color.rgb = NAVY
    sh.line.fill.background()


def _cols(n, gap):
    w = (LW - (n - 1) * gap) / n
    return [XG + i * (w + gap) for i in range(n)], w


# ---------------------------------------------------------------- conviction 10
T_C10 = "Conviction 10" + NB + ": un flux d'entrée unique qui qualifie avant de servir"
ETAPES10 = [("DoR", "definition of ready"), ("Qualifier", "valeur, faisabilité, charge"), ("Automatiser", "demandes récurrentes")]
SANS = ["Un seul point d'entrée" + NB + "; critères d'entrée" + NB + ": problème, valeur, indicateur.",
        "Une grille explicite" + NB + "; au-delà d'un seuil de charge, un ROI est demandé.",
        "Statut visible" + NB + "; demandes récurrentes en self-service."]
AVEC = ["L'IA contrôle la complétude de la demande au regard de la DoR.",
        "Qualification par l'IA" + NB + ": elle classe et oriente" + NB + "; l'équipe décide.",
        "L'IA propose d'automatiser les demandes récurrentes."]


def conviction10(prs):
    s = deck_draw.slide_par_titre(prs, T_C10)
    goutte_reduite(s)
    _retirer_corps(s)
    gap = 16.0
    xs, cw = _cols(3, gap)
    # bande haute : les 3 etapes, colonnes 2 et 3 alignees sur les cartes
    starts = [XB, xs[1], xs[2]]
    ends = [xs[0] + cw, xs[1] + cw, xs[2] + cw]
    for k, (nom, sous) in enumerate(ETAPES10):
        x = starts[k]
        carre_num_cyan(s, x, 103, 30, k + 1, sz=14)
        tx(s, x + 38, 96, ends[k] - x - 38, 46, [[(nom, 16, True, NAVY)], [(sous, 12, False, NAVY)]], A.MIDDLE)
        if k:
            chevron_sep(s, x - gap / 2 - 4, 110, 8, 16)
    rangs = [("SANS IA", SANS, 160.0), ("AVEC IA", AVEC, 266.0)]
    for nom, textes, y in rangs:
        pilule_entete(s, XG, y, 84, 22, nom, CYAN, sz=12)
        if nom == "AVEC IA":
            forme(s, S.ROUNDED_RECTANGLE, XG + 94, y, 290, 22, PANEL, None, adj=0.5)
            tx(s, XG + 94, y, 290, 22, [[("Option selon la maturité · IA gouvernée", 12, False, NAVY)]], A.MIDDLE, P.CENTER)
        yc = y + 28
        for k, t in enumerate(textes):
            accent = nom == "AVEC IA" and k == 1
            c = carte_diag(s, xs[k], yc, cw, 70, adj=0.12)
            if accent:
                _navy(c)
            tx(s, xs[k] + 12, yc, cw - 24, 70, [[(t, 13, False, BLANC if accent else NAVY)]], A.MIDDLE)
            if k:
                chevron_sep(s, xs[k] - gap / 2 - 4, yc + 27, 8, 16)


# ---------------------------------------------------------------- conviction 11
T_C11 = "Conviction 11" + NB + ": évaluer en continu le service vécu, le mesurer et le montrer"
ETAPES11 = [
    ("Mesurer", ["L'écart entre le SLA et le service vécu", "Satisfaction et effort perçu", "Part de RUN subi et maîtrisé"]),
    ("Montrer", ["À rythme régulier", "Aux consommateurs, au COMOP et au COPIL (à" + NB + "valider)", "Écarts et charge de RUN"]),
    ("Agir", ["Un objectif de service par capacité", "Revue trimestrielle des écarts", "Écarts au backlog (à" + NB + "valider)"]),
]
EN_TETE = ("Ce que dit le SLA", "Ce que vit le consommateur")
PAIRES = [
    ("Disponibilité du service", "Une demande qui attend, même quand le service est « vert »"),
    ("Incidents clos dans le délai", "Le même incident qui revient"),
]
LIGNES11 = [[2, 1, 1], [1, 3, 1], [2, 1, 1]]


def conviction11(prs):
    s = deck_draw.slide_par_titre(prs, T_C11)
    goutte_reduite(s)
    _retirer_corps(s)
    gap = 16.0
    xs, cw = _cols(3, gap)
    starts = [XB, xs[1], xs[2]]
    for k, (nom, _) in enumerate(ETAPES11):
        x = starts[k]
        carre_num_cyan(s, x, 106, 30, k + 1, sz=15)
        tx(s, x + 40, 106, 140, 30, [[(nom, 18, True, NAVY)]], A.MIDDLE)
        if k:
            chevron_sep(s, x - gap / 2 - 4, 113, 8, 16)
    y0, h = 158.0, 114.0
    lh = 15.0
    for k, (_, points) in enumerate(ETAPES11):
        accent = k == 2
        col = BLANC if accent else NAVY
        c = carte_diag(s, xs[k], y0, cw, h, adj=0.12)
        if accent:
            _navy(c)
        y = y0 + 10
        for p, n in zip(points, LIGNES11[k], strict=True):
            forme(s, S.OVAL, xs[k] + 12, y + 5, 5, 5, CYAN, None)
            tx(s, xs[k] + 22, y, cw - 30, n * lh, [[(p, 12, False, col)]], A.TOP)
            y += n * lh + 5
    yc, ht, hl, g = 278.0, 22.0, 30.0, 3.0
    c2 = LW / 2
    forme(s, S.ROUNDED_RECTANGLE, XG, yc, LW, ht, CYAN, None, adj=0.5)
    tx(s, XG + 16, yc, c2 - 20, ht, [[(EN_TETE[0], 13, True, NAVY)]], A.MIDDLE)
    tx(s, XG + c2 + 12, yc, c2 - 24, ht, [[(EN_TETE[1], 13, True, NAVY)]], A.MIDDLE)
    for k, (a, b) in enumerate(PAIRES):
        y = yc + ht + g + k * (hl + g)
        forme(s, S.RECTANGLE, XG, y, LW, hl, PANEL, None)
        tx(s, XG + 16, y, c2 - 20, hl, [[(a, 12, False, NAVY)]], A.MIDDLE)
        tx(s, XG + c2 + 12, y, c2 - 24, hl, [[(b, 12, True, NAVY)]], A.MIDDLE)


# ---------------------------------------------------------------- conviction 12
T_C12 = "Conviction 12" + NB + ": aucun produit livré sans RUN prêt"
FLUX = ["Construire", "Porte" + NB + "«" + NB + "RUN" + NB + "prêt" + NB + "»", "Exploiter", "Apprendre"]
CRITERES = [("Équipe" + NB + ": ", "un propriétaire nommé, deux personnes capables par module."),
            ("Supervision" + NB + ": ", "alertes et astreinte définies."),
            ("Connaissance" + NB + ": ", "procédure d'incident documentée."),
            ("Budget" + NB + ": ", "RUN inscrit dans le business case.")]
APPRENDRE = "Chaque incident majeur" + NB + ": un post\u2011mortem, puis une action au backlog."
AVEC12 = "L'IA aide à diagnostiquer et trier les incidents" + NB + "; l'humain décide, chaque sortie est relue et tracée."


def conviction12(prs):
    s = deck_draw.slide_par_titre(prs, T_C12)
    goutte_reduite(s)
    _retirer_corps(s)
    # bande haute : flux en 4 pilules
    larg = [100.0, 170.0, 100.0, 110.0]
    gap = (XD - XB - sum(larg)) / 3
    x = XB
    for k, (t, w) in enumerate(zip(FLUX, larg, strict=True)):
        accent = k == 1
        forme(s, S.ROUNDED_RECTANGLE, x, 106, w, 30, NAVY if accent else PANEL, None, adj=0.5)
        tx(s, x, 106, w, 30, [[(t, 14, True, BLANC if accent else NAVY)]], A.MIDDLE, P.CENTER)
        if k < 3:
            chevron_sep(s, x + w + gap / 2 - 4, 113, 8, 16)
        x += w + gap
    # criteres : panneau pleine largeur, grille 2 x 2
    yp = 168.0
    carte_diag(s, XG, yp, LW, 96, adj=0.12)
    pilule_entete(s, XG + 14, 158, 300, 20, "4 CRITÈRES AVANT LA MISE EN SERVICE", CYAN, sz=12)
    cw = (LW - 28 - 16) / 2
    for i, (b, t) in enumerate(CRITERES):
        cx = XG + 14 + (i % 2) * (cw + 16)
        cy = yp + 20 + (i // 2) * 36
        carre_num_cyan(s, cx, cy + 4, 24, i + 1, sz=13)
        tx(s, cx + 32, cy, cw - 32, 32, [[(b, 13, True, NAVY), (t, 13, False, NAVY)]], A.MIDDLE)
    # deux encarts du bas
    yb, hb = 290.0, 74.0
    wb = (LW - 16) / 2
    forme(s, S.ROUNDED_RECTANGLE, XG, yb, wb, hb, PANEL, None, adj=0.12)
    pilule_entete(s, XG + 14, yb - 10, 110, 20, "APPRENDRE", CYAN, sz=12)
    tx(s, XG + 14, yb + 14, wb - 28, hb - 18, [[(APPRENDRE, 13, False, NAVY)]], A.MIDDLE)
    x2 = XG + wb + 16
    carte_diag(s, x2, yb, wb, hb, adj=0.12)
    pilule_entete(s, x2 + 14, yb - 10, 230, 20, "AVEC IA · SELON LA MATURITÉ", CYAN, sz=12)
    tx(s, x2 + 14, yb + 14, wb - 28, hb - 18, [[(AVEC12, 13, False, NAVY)]], A.MIDDLE)


# ---------------------------------------------------------------- conviction 13
T_C13 = "Conviction 13" + NB + ": un modèle d'organisation Infra choisi, pas imposé"
MODELES = [("Silos technologiques", "Une équipe par spécialité technique."),
           ("Services mutualisés", "Un centre commun livre des services sur catalogue."),
           ("Orienté services", "Un responsable garantit le service de bout en bout."),
           ("Plateforme produit", "Des plateformes internes gérées comme des produits."),
           ("Fédéré / hybride", "Un noyau commun et des équipes autonomes.")]
CONCLU = "Chaque entité choisit sa forme selon sa maturité, sa criticité et sa taille" + NB + ": aucune n'est imposée."


def conviction13(prs):
    s = deck_draw.slide_par_titre(prs, T_C13)
    goutte_reduite(s)
    _retirer_corps(s)
    # bande haute : le message (accent navy unique)
    forme(s, S.ROUND_2_DIAG_RECTANGLE, XB, 98, XD - XB, 46, NAVY, None, adj=0.2)
    tx(s, XB + 16, 98, XD - XB - 32, 46, [[(CONCLU, 14, True, BLANC)]], A.MIDDLE)
    # echelle des 5 modeles, pleine largeur
    xr = XG + 26
    wr = XD - xr
    tx(s, xr, 158, wr, 16, [[("Par spécialité technique", 13, True, NAVY)]], A.MIDDLE)
    y0, hr, g = 178.0, 28.0, 4.0
    forme(s, S.DOWN_ARROW, XG, y0, 16, 5 * hr + 4 * g, PANEL, None)
    for i, (nom, desc) in enumerate(MODELES):
        y = y0 + i * (hr + g)
        carte_diag(s, xr, y, wr, hr, adj=0.2)
        carre_num_cyan(s, xr + 8, y + 4, 22, i + 1, sz=13)
        tx(s, xr + 40, y, 180, hr, [[(nom, 14, True, NAVY)]], A.MIDDLE)
        forme(s, S.RECTANGLE, xr + 226, y + 6, 0.8, hr - 12, LINE, None)
        tx(s, xr + 238, y, wr - 250, hr, [[(desc, 13, False, NAVY)]], A.MIDDLE)
    tx(s, xr, y0 + 5 * hr + 4 * g + 2, wr, 16, [[("Par produit et par service rendu", 13, True, NAVY)]], A.MIDDLE)


TITRES = (T_C10, T_C11, T_C12, T_C13)


def _ids():
    prs = Presentation(deck_base.resoudre_base(BASE))
    return [f"id:{deck_draw.slide_par_titre(prs, t).slide_id}" for t in TITRES]


_I = dict(zip(TITRES, _ids(), strict=True))
ETAPES = [
    {"declarer": [_I[T_C10]], "f": conviction10, "nouvelles_max": 0, "nom": "conviction 10 : goutte reduite, etapes + 2 rangs pleine largeur"},
    {"declarer": [_I[T_C11]], "f": conviction11, "nouvelles_max": 0, "nom": "conviction 11 : goutte reduite, cartes + tableau pleine largeur"},
    {"declarer": [_I[T_C12]], "f": conviction12, "nouvelles_max": 0, "nom": "conviction 12 : goutte reduite, flux + criteres 2x2 + encarts"},
    {"declarer": [_I[T_C13]], "f": conviction13, "nouvelles_max": 0, "nom": "conviction 13 : goutte reduite, message en tete + echelle pleine largeur"},
]
