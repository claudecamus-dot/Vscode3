"""Delta V32a (base V31) : quatre slides refaites, aucune slide ajoutee ni retiree (l'autre lot, V32b, traite les slides 5 a 7).

- Couverture : les trois pastilles Infra / Produit / IA et la ligne « orchestres par des coachs » sont retirees, la date du jour remplace « 2026 », le titre occupe l'espace libere ;
- Ouverture (titre reformule) : modele « contexte et demande » de Vscode8 (slide 3) : panneau Contexte / Demande a gauche, NOTRE REPONSE EN TROIS TEMPS dominante a droite,
  les engagements ramenes a un bandeau mince ;
- Douze convictions en quatre themes : vraie slide d'introduction : phrase d'enjeu, quatre cartes surmontees d'un pictogramme rond, douze pastilles numerotees, mode de lecture ;
- IA : modele « cognitive acceleration » de Vscode8 (slide 21) : deux leviers qui convergent vers un disque central, socle de controle humain, cinq moments de la boucle, effets pour le client.
Les pictogrammes sont COPIES des slides de conviction existantes (formes natives, meme dessin), jamais inventes.
Usage (depuis docs/cadrage-ppt/) : py deck_delta/deck.py delta_V32a --base V31 --sortie C:/tmp/deck-v32-a/V32a.pptx
"""
import copy

import deck_base
import deck_draw
from forme_v9 import (
    BLANC,
    CYAN,
    LINE,
    NAVY,
    PANEL,
    SLATE,
    S,
    carre_num_cyan,
    chevron_sep,
    forme,
    par_id,
    pilule_entete,
    tx,
)
from pptx import Presentation
from pptx.enum.text import MSO_ANCHOR as A
from pptx.enum.text import PP_ALIGN as P
from pptx.util import Emu

BASE = "V31"
NOTE = "V32a : couverture allegee et datee, ouverture contexte / demande / reponse, introduction des douze convictions, slide IA a deux leviers"
OPS = []

NB = "\u00a0"
T_1 = "Faire de l'Infrastructure un levier de valeur, avec le Produit et l'IA"
T_2 = "En trois temps et trois engagements, votre Infra passe du guichet au produit"
T_2_NEUF = f"Votre demande, notre réponse en trois temps{NB}: du guichet au produit"
T_9 = "Douze convictions en quatre thèmes, déclinées une à une ensuite"
T_20 = "L'IA apporte au coach du temps et de la matière, pas la décision"
T_10 = "Conviction 1 : le mode produit est d'abord une culture, pas un outil"
T_11 = "Trois convictions, chacune vérifiée par un critère et un chantier"
T_12 = "Deux convictions de plus, vérifiées de la même façon"
TITRES = (T_1, T_2, T_9, T_20)

DATE_DU_JOUR = "3 nov. 2026"  # « 3 novembre 2026 » (78 pt a 10 pt) ne tient pas entre la courbe du bandeau et le filet du gabarit (68 pt libres)


def _s(prs, t):
    return deck_draw.slide_par_titre(prs, t)


def _pt(v):
    return int(round(v * 12700))


# ---------------------------------------------------------------- copie de pictogrammes (formes natives des slides de conviction)
def _xfrm(el):
    for x in el.iter("{http://schemas.openxmlformats.org/drawingml/2006/main}xfrm"):
        return x
    return None


def copier_picto(src, ids, dst, cx, cy, scale, centre_src):
    """Copie les formes `ids` de `src` dans `dst` : centre_src (pt, repere de src) -> (cx, cy) (pt) ; dimensions et epaisseurs de trait x scale. Renvoie les nouveaux elements."""
    ns = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
    par = {sh.shape_id: sh for sh in src.shapes}
    neufs = []
    base_id = max(sh.shape_id for sh in dst.shapes) + 1
    for k, i in enumerate(ids):
        el = copy.deepcopy(par[i]._element)
        x = _xfrm(el)
        off, ext = x.find(f"{ns}off"), x.find(f"{ns}ext")
        ox, oy = int(off.get("x")) / 12700, int(off.get("y")) / 12700
        w, h = int(ext.get("cx")) / 12700, int(ext.get("cy")) / 12700
        off.set("x", str(_pt(cx + (ox - centre_src[0]) * scale)))
        off.set("y", str(_pt(cy + (oy - centre_src[1]) * scale)))
        ext.set("cx", str(_pt(w * scale)))
        ext.set("cy", str(_pt(h * scale)))
        for ln in el.iter(f"{ns}ln"):
            if ln.get("w"):
                ln.set("w", str(max(9525, int(int(ln.get("w")) * min(1.0, scale * 1.15)))))
        c = [e for e in el.iter() if e.tag.endswith("}cNvPr")][0]
        c.set("id", str(base_id + k))
        dst.shapes._spTree.append(el)
        neufs.append(el)
    return neufs


def _supprimer_ids(s, ids):
    for sh in list(s.shapes):
        if sh.shape_id in ids:
            sh._element.getparent().remove(sh._element)


# ---------------------------------------------------------------- mesure de texte (estimation du nombre de lignes, repli grossier sans PIL / police)
def _police(gras):
    try:
        import os

        from PIL import ImageFont
        f = ImageFont.truetype(os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Windows\Fonts\Outfit-Variable.ttf"), 100)
        f.set_variation_by_name("Bold" if gras else "Regular")
        return f
    except Exception:
        return None


def nb_lignes(texte, sz, gras, largeur):
    f = _police(gras)
    mots, n, cur = texte.split(), 1, ""
    for m in mots:
        essai = (cur + " " + m).strip()
        w = f.getlength(essai) * sz / 100 if f else len(essai) * sz * 0.52
        if w > largeur and cur:
            n, cur = n + 1, m
        else:
            cur = essai
    return n


# ================================================================ slide 1 : couverture
def couverture(prs):
    s = _s(prs, T_1)
    b = par_id(s)
    for pid in range(1349, 1356):
        if pid in b:
            b[pid]._element.getparent().remove(b[pid]._element)
    date = b[1347]
    deck_draw.set_run(date, DATE_DU_JOUR)
    titre = b[1346]
    # le titre occupe l'espace libere : 3 lignes a 22 pt, centre sur le contour blanc du gabarit (y 105..253)
    titre.left, titre.top, titre.width, titre.height = _pt(130), _pt(128), _pt(300), _pt(103)
    for r in titre.text_frame.paragraphs[0].runs:
        r.font.size = Emu(_pt(22))


# ================================================================ slide 2 : ouverture
def _picto_oval_loupe_cible(prs):
    """Pictogrammes loupe et cible de la slide IA (cercles de 24 pt) : (ids, centre source)."""
    return {"loupe": ((26, 27, 28), (218, 206)), "barres": ((29, 30, 31, 32), (427, 206)), "engrenage": ((33, 34, 35), (637, 206)),
            "cible": ((36, 37, 38), (218, 315)), "eclair": ((39, 40), (427, 315))}


def ouverture(prs):
    s = _s(prs, T_2)
    sl20 = _s(prs, T_20)
    for sh in list(s.shapes):
        if sh.is_placeholder or (sh.has_text_frame and sh.text_frame.text.strip() == "OUVERTURE"):
            continue
        sh._element.getparent().remove(sh._element)
    deck_draw.set_run(s.shapes.title, T_2_NEUF)

    X0, X1, Y0, H = 45, 659, 98, 206
    LW = 240  # panneau gauche
    # ---- gauche : Contexte / Demande
    forme(s, S.ROUND_2_DIAG_RECTANGLE, X0, Y0, LW, H, BLANC, NAVY, adj=0.1, lw=1.25)
    forme(s, S.RECTANGLE, X0 + 14, Y0 + H / 2, LW - 28, 0.75, LINE)
    forme(s, S.RECTANGLE, X0 + 70, Y0 + 14, 0.75, H - 28, LINE)
    pic = _picto_oval_loupe_cible(prs)
    blocs = (
        ("Contexte", "loupe", "Un guichet saturé", "Délais qui s'allongent, parcours illisible, outils contournés, coûts sans valeur visible."),
        ("Demande", "cible", "Faire de l'Infra un levier de valeur, avec le Produit et l'IA.", "Piloter la valeur plutôt que subir la demande."),
    )
    for k, (lab, key, gras, corps) in enumerate(blocs):
        top = Y0 + k * H / 2
        ids, cs = pic[key]
        copier_picto(sl20, ids, s, X0 + 36, top + 40, 1.7, cs)
        tx(s, X0 + 6, top + 66, 60, 16, [[(lab, 11, True, NAVY)]], A.TOP, P.CENTER)
        tx(s, X0 + 82, top + 10, LW - 82 - 12, H / 2 - 20, [[(gras, 11, True, NAVY)], [(corps, 10, False, NAVY)]], A.MIDDLE, P.LEFT, espace=3)
    # ---- droite : notre reponse, la plus lourde
    RX = X0 + LW + 20
    RW = X1 - RX
    chevron_sep(s, X0 + LW + 5, Y0 + H / 2 - 10, 10, 20)
    forme(s, S.ROUND_2_DIAG_RECTANGLE, RX, Y0, RW, H, NAVY, None, adj=0.1)
    tx(s, RX + 18, Y0 + 12, RW - 36, 16, [[("NOTRE RÉPONSE EN TROIS TEMPS", 11, True, BLANC)]])
    forme(s, S.ROUNDED_RECTANGLE, RX + 18, Y0 + 31, 40, 4, CYAN, None, adj=0.5)
    temps = (
        ("Diagnostiquer", f"Assessment flash{NB}: référence au T0, choix d'un pilote."),
        ("Expérimenter", f"Pilote Produit + IA{NB}: mesure au T1 et décision du client."),
        ("Ancrer", f"Relais internes formés{NB}; extension éventuelle."),
    )
    ry0, pas, d = Y0 + 50, 52, 34
    forme(s, S.RECTANGLE, RX + 18 + d / 2 - 0.75, ry0 + d / 2, 1.5, 2 * pas, SLATE)
    for k, (nom, desc) in enumerate(temps):
        y = ry0 + k * pas
        forme(s, S.OVAL, RX + 18, y, d, d, CYAN, None)
        tx(s, RX + 18, y, d, d, [[(str(k + 1), 14, True, NAVY)]], A.MIDDLE, P.CENTER)
        tx(s, RX + 18 + d + 14, y - 1, RW - 36 - d - 14, 46, [[(nom, 14, True, BLANC)], [(desc, 11, False, BLANC)]], A.TOP, P.LEFT, espace=2)
    # ---- bas : les engagements, un bandeau mince
    BY, BH = Y0 + H + 10, 42
    forme(s, S.ROUNDED_RECTANGLE, X0, BY, X1 - X0, BH, PANEL, None, adj=0.3)
    pilule_entete(s, X0 + 8, BY + 8, 104, 26, "NOS ENGAGEMENTS", NAVY, sz=9)
    items = (
        f"Aucun ROI promis{NB}: référence au T0, résultats au T1",
        "L'IA prépare, nos coachs challengent, le client décide",
        "Un dispositif qui construit son propre relais",
    )
    ix0 = X0 + 124
    iw = (X1 - 8 - ix0) / 3
    for k, t in enumerate(items):
        x = ix0 + k * iw
        forme(s, S.ROUNDED_RECTANGLE, x, BY + BH / 2 - 4, 8, 8, CYAN, None, adj=0.22)
        tx(s, x + 14, BY + 3, iw - 22, BH - 6, [[(t, 9.5, True, NAVY)]], A.MIDDLE, P.LEFT)


# ================================================================ slide 9 : introduction des douze convictions
_PICTOS_9 = {
    # theme -> (slide source, ids, centre source, echelle)
    "culture": (T_10, (100, 101, 102, 103, 104), None, 0.42),
    "produit": (T_11, (101, 102, 103, 104, 105), (140, 112), 0.66),
    "pilotage": (T_11, (129, 130, 131, 132, 133, 134, 135, 136), (564, 112), 0.66),
    "run": (T_12, (100, 101, 102, 103), (140, 112), 0.66),
}


def _picto_rond(prs, s, cle, cx, cy, d):
    """Pictogramme rond (disque blanc a bord navy + glyphe) copie d'une slide de conviction."""
    src_t, ids, centre, echelle = _PICTOS_9[cle]
    src = _s(prs, src_t)
    if cle == "culture":
        # l'ampoule de la conviction 1 n'a pas de disque : on emprunte celui de la slide des convictions 5 et 6, et on centre le glyphe sur lui
        disque = _s(prs, T_12)
        copier_picto(disque, (100,), s, cx, cy, d / 56, (140, 112))
        par = {sh.shape_id: sh for sh in src.shapes}
        xs = [par[i].left / 12700 for i in ids] + [(par[i].left + par[i].width) / 12700 for i in ids]
        ys = [par[i].top / 12700 for i in ids] + [(par[i].top + par[i].height) / 12700 for i in ids]
        centre = ((min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2)
        copier_picto(src, ids, s, cx, cy, echelle, centre)
    else:
        copier_picto(src, ids, s, cx, cy, d / 56, centre)


def convictions(prs):
    s = _s(prs, T_9)
    b = par_id(s)
    themes = (
        ("culture", 73, ((77, 78), (80, 81), (83, 84))),
        ("produit", 86, ((90, 91), (93, 94))),
        ("pilotage", 96, ((100, 101), (103, 104), (106, 107))),
        ("run", 109, ((112, 113), (115, 116), (118, 119), (121, 122))),
    )
    data = []
    for cle, hid, items in themes:
        lst = []
        for nid, lid in items:
            paras = [p.text for p in b[lid].text_frame.paragraphs]
            lst.append((b[nid].text_frame.text, paras[0], paras[1] if len(paras) > 1 else None))
        data.append((cle, b[hid].text_frame.text, lst))
    bas = []
    _supprimer_ids(s, set(range(72, 123)))

    # panneau gris, phrase d'enjeu, quatre cartes
    forme(s, S.RECTANGLE, 37, 95, 630, 269, PANEL)
    # le panneau doit passer derriere tout le corps : on le replace juste apres le titre
    panneau = s.shapes[-1]._element
    arbre = panneau.getparent()
    arbre.remove(panneau)
    arbre.insert(2, panneau)
    forme(s, S.ROUNDED_RECTANGLE, 45, 100, 614, 20, NAVY, None, adj=0.5)
    tx(s, 45, 100, 614, 20, [[("Douze convictions que nous posons, puis que nous vérifions une à une.", 11, True, BLANC)]], A.MIDDLE, P.CENTER)

    W, G, TOP, BOT = 146, 10, 143, 344
    D = 34
    TW = W - 8 - 26 - 6
    for i, (cle, titre, items) in enumerate(data):
        x = 45 + i * (W + G)
        forme(s, S.ROUND_2_DIAG_RECTANGLE, x, TOP, W, BOT - TOP, BLANC, LINE, adj=0.08, lw=0.75)
        _picto_rond(prs, s, cle, x + W / 2, TOP, D)
        tx(s, x + 8, TOP + 20, W - 16, 24, [[(titre, 11.5, True, NAVY)]], A.MIDDLE, P.CENTER)
        forme(s, S.RECTANGLE, x + 18, TOP + 47, W - 36, 0.75, LINE)
        y = TOP + 54
        haut = []
        for _num, lab, boucle in items:
            n1 = nb_lignes(lab, 10, True, TW)
            haut.append(n1 * 12.2 + (11.6 if boucle else 0))
        gap = min(20, (BOT - 6 - y - sum(haut)) / max(1, len(items) - 1))
        for (num, lab, boucle), h in zip(items, haut, strict=True):
            carre_num_cyan(s, x + 8, y + 0.5, 18, num, sz=9)
            paras = [[(lab, 10, True, NAVY)]] + ([[(boucle, 9.5, False, SLATE)]] if boucle else [])
            tx(s, x + 32, y, TW, h + 2, paras, A.TOP, P.LEFT)
            y += h + gap
        bas.append(round(y - gap))
    # mode de lecture
    tx(s, 45, 348, 614, 13, [[("Comment lire la suite : ", 10, True, NAVY), ("chaque conviction se présente avec un critère observable et un chantier à mener.", 10, False, NAVY)]], A.MIDDLE, P.LEFT)
    print("slide convictions : bas des listes par carte (pt, limite 332) :", bas)


# ================================================================ slide 20 : l'IA apporte du temps et de la matiere
def ia(prs):
    s = _s(prs, T_20)
    pic = _picto_oval_loupe_cible(prs)
    # 1) copier les pictogrammes de la slide (24 pt) pour la rangee des moments, puis vider le corps
    # (les elements sont copies AVANT la suppression : meme slide)
    avant = {sh.shape_id for sh in s.shapes}
    garde = {sh.shape_id for sh in s.shapes if sh.is_placeholder or sh.name.startswith("nav-") or (sh.has_text_frame and sh.text_frame.text.startswith("02 · NOS CONVICTIONS"))}
    X0, X1 = 45, 659
    # leviers
    PW, PY, PH = 225, 98, 104
    AR = 20
    cxm, cym = (X0 + X1) / 2, PY + PH / 2
    leviers = (
        (X0, "GAGNER DU TEMPS", ((1, "Un diagnostic plus rapide"), (2, "Un tri assisté des demandes"), (3, "Une capitalisation continue"))),
        (X1 - PW, "APPORTER DE LA MATIÈRE", ((4, "Des mesures consolidées"), (5, "Des cas d'usage bornés"))),
    )
    for x, titre, apports in leviers:
        forme(s, S.ROUND_2_DIAG_RECTANGLE, x, PY, PW, PH, BLANC, NAVY, adj=0.1, lw=1.25)
        pilule_entete(s, x + 12, PY + 9, 158, 18, titre, NAVY, sz=9)
        decal = (3 - len(apports)) * 10.5
        for k, (n, t) in enumerate(apports):
            y = PY + 36 + k * 21 + decal
            carre_num_cyan(s, x + 12, y, 17, n, sz=9)
            tx(s, x + 36, y, PW - 46, 17, [[(t, 11, True, NAVY)]], A.MIDDLE, P.LEFT)
    # fleches et disque central
    forme(s, S.RIGHT_ARROW, X0 + PW + 6, cym - 9, AR, 18, CYAN, None)
    forme(s, S.LEFT_ARROW, X1 - PW - 6 - AR, cym - 9, AR, 18, CYAN, None)
    forme(s, S.OVAL, cxm - 52, cym - 52, 104, 104, BLANC, NAVY, lw=1.25)
    forme(s, S.OVAL, cxm - 45, cym - 45, 90, 90, NAVY, None)
    tx(s, cxm - 42, cym - 20, 84, 40, [[("L'IA augmente", 10.5, True, BLANC)], [("le coach", 10.5, True, BLANC)]], A.MIDDLE, P.CENTER)
    # socle commun
    SY = PY + PH + 9
    forme(s, S.ROUNDED_RECTANGLE, X0, SY, X1 - X0, 30, NAVY, None, adj=0.25)
    tx(s, X0 + 14, SY, 120, 30, [[("SOCLE COMMUN", 9.5, True, BLANC)], [("CONTRÔLE HUMAIN", 9.5, True, BLANC)]], A.MIDDLE, P.LEFT)
    forme(s, S.RECTANGLE, X0 + 134, SY + 6, 0.75, 18, SLATE)
    tx(s, X0 + 146, SY, X1 - X0 - 156, 30, [[(f"L'IA prépare, nos coachs challengent, le client décide{NB}: chaque apport est borné et relu.", 10.5, False, BLANC)]], A.MIDDLE, P.LEFT)
    # moments de la boucle
    LY = SY + 30 + 8
    tx(s, X0, LY, 400, 12, [[("OÙ L'IA AIDE DANS LA BOUCLE", 9.5, True, NAVY)]], A.MIDDLE, P.LEFT)
    MY = LY + 15
    moments = (("loupe", "Comprendre", 1), ("barres", "Prioriser", 2), ("engrenage", "Ancrer", 3), ("cible", "Mesurer", 4), ("eclair", "Explorer", 5))
    mg = 8
    mw = (X1 - X0 - 4 * mg) / 5
    for k, (key, nom, _n) in enumerate(moments):
        x = X0 + k * (mw + mg)
        forme(s, S.ROUNDED_RECTANGLE, x, MY, mw, 38, PANEL, None, adj=0.25)
        ids, cs = pic[key]
        copier_picto(s, ids, s, x + 8 + 14, MY + 19, 28 / 24, cs)
        tx(s, x + 8 + 28 + 7, MY, mw - 8 - 28 - 9, 38, [[(nom, 10.5, True, NAVY)]], A.MIDDLE, P.LEFT)
    # ce que cela change pour vous
    CY = MY + 38 + 9
    tx(s, X0, CY, 400, 12, [[("CE QUE CELA CHANGE POUR VOUS", 9.5, True, NAVY)]], A.MIDDLE, P.LEFT)
    effets = (
        (f"Comprendre plus vite{NB}:", " un diagnostic et un tri assistés"),
        (f"Garder la main{NB}:", " chaque apport est relu, le client décide"),
        (f"Rien n'est promis{NB}:", " gains à mesurer au T0 puis au T1"),
    )
    ew = (X1 - X0 - 2 * 14) / 3
    for k, (a, t) in enumerate(effets):
        x = X0 + k * (ew + 14)
        forme(s, S.RECTANGLE, x, CY + 17, 3, 28, CYAN)
        tx(s, x + 10, CY + 17, ew - 12, 28, [[(a, 10, True, NAVY), (t, 10, False, NAVY)]], A.MIDDLE, P.LEFT)
    # 2) retirer l'ancien corps : toutes les formes d'avant qui ne sont ni titre, ni navigation, ni surtitre
    _supprimer_ids(s, avant - garde)


def retouche(prs):
    couverture(prs)
    ouverture(prs)
    convictions(prs)
    ia(prs)


def _ids():
    prs = Presentation(deck_base.resoudre_base(BASE))
    return [f"id:{_s(prs, t).slide_id}" for t in TITRES]


ETAPES = [{"declarer": _ids(), "f": retouche, "nouvelles_max": 0, "nom": "couverture, ouverture, introduction des convictions, slide IA"}]
