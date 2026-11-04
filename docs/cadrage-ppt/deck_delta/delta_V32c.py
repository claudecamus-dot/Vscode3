"""Delta V32c (base V31) : une treizieme conviction dans « Nos convictions » : l'Infra organisee en equipe plateforme, pas en guichet.

- Nouvelle slide « Conviction 13 » juste apres « Conviction 12 : aucun produit livre sans RUN pret », sur le gabarit d'une conviction a un seul pilier
  (« Conviction 8 ») : meme surtitre, meme etiquette PROPOSITION A VALIDER, meme pastille CONVICTION, memes cartes LE CRITERE OBSERVABLE / LE CHANTIER ;
- le chapitre passe de 12 a 13 : surtitres « n/13 » dans l'ordre reel des slides, reperes de lecture a 13 pastilles (la 13e allumee sur la nouvelle slide) ;
- slide d'introduction (« Douze » -> « Treize convictions ») : titre, bandeau, et une quatrieme ligne « 13 » dans la carte « Culture et organisation ».
Sources (lecture seule) : docs/exports/cadrage/bmad-iap-cadrage.md, § « Modeles d'equipe » (Team Topologies : types d'equipe, modes d'interaction ; « souvent Collaboration ad hoc
— ticket, reunion » comme mode actuel, X-as-a-Service comme mode cible).
Les slides sont designees par TEXTE ou par role (surtitre, forme), jamais par id de forme : ce delta s'applique aussi sur la sortie de V32a (slides 9 et 20 reconstruites).
Usage (depuis docs/cadrage-ppt/) : py deck_delta/deck.py delta_V32c --base V31 --sortie C:/tmp/deck-v32-c/V32c.pptx
"""
import copy
import re

import deck_base
import deck_draw
from forme_v9 import BLANC, CLAIR, CYAN, LINE, NAVY, PANEL, SLATE, S, forme, tx
from pptx import Presentation
from pptx.enum.text import MSO_ANCHOR as A
from pptx.enum.text import PP_ALIGN as P

BASE = "V31"
NOTE = "V32c : conviction 13 (modele d'organisation de l'Infra choisi, pas impose ; dix modeles de reference du benchmark) ; chapitre n/12 -> n/13, reperes a 13 pastilles, introduction « Treize convictions »"
OPS = []

NB = "\u00a0"
NS_A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
KICKER = re.compile(r"^02 · NOS CONVICTIONS · \d+/\d+$")
T_REF = "Conviction 12 : aucun produit livré sans RUN prêt"
T_MODELE = "Conviction 8 : une petite équipe produit qui construit et exploite"
T_9 = "Douze convictions en quatre thèmes, déclinées une à une ensuite"
T_9_NEUF = "Treize convictions en quatre thèmes, déclinées une à une ensuite"
BARRE = "Douze convictions que nous posons, puis que nous vérifions une à une."
BARRE_NEUVE = "Treize convictions que nous posons, puis que nous vérifions une à une."
T_NEUVE = "Conviction 13 : un modèle d'organisation Infra choisi, pas imposé"
LABEL_9 = "Un modèle d'organisation choisi, pas imposé"

# textes de la slide modele (« Conviction 8 ») -> textes de la conviction 13
CHIP_ANCIEN, CHIP_NEUF = "CONVICTION 8", "CONVICTION 13"
CRITERE_ANCIEN = "Temps de construction protégé ; demandes récurrentes passées en self-service."
CRITERE_NEUF = "Chaque produit ou service Infra a un owner identifié et des interactions explicites avec ses consommateurs."
CHANTIER_ANCIEN = "Cadrer la composition de l'équipe, le binôme produit et la répartition entre construire et exploiter."
CHANTIER_NEUF = "Cartographier le modèle réel, nommer les owners de trois à cinq services, puis choisir pour chaque entité un modèle cible, sans réorganisation générale."
# benchmark « modèles d'organisation des entités Infrastructure IT » (3 novembre 2026), § 4.1 : les dix archetypes, noms exacts du tableau
MODELES = (
    "Silos technologiques", "Build / Run séparés", "Centre de services mutualisés", "Organisation orientée services",
    "Décentralisation par BU ou domaine", "Externalisation / SIAM", "Cloud / CCoE", "DevOps / SRE",
    "Platform Engineering / Infra as a Product", "Fédéré / hybride",
)
# § 4.2 : trois combinaisons frequentes (libelles courts)
COMBINAISONS = (
    ("Silos technologiques", "+ Orienté services"),
    ("Services mutualisés", "+ Platform Engineering"),
    ("Fédéré", "+ Orienté services", "+ Platform Engineering"),
)
SOURCE = f"Source{NB}: benchmark des modèles d'organisation Infrastructure IT (3 novembre 2026){NB}: synthèse de référentiels, hypothèses de travail, non représentative."

def _s(prs, t):
    return deck_draw.slide_par_titre(prs, t)


def _pt(v):
    return int(round(v * 12700))


def _par_texte(s, texte):
    trouvees = [sh for sh in s.shapes if sh.has_text_frame and deck_draw.plat(sh.text_frame.text) == deck_draw.plat(texte)] if hasattr(deck_draw, "plat") else []
    if not trouvees:
        trouvees = [sh for sh in s.shapes if sh.has_text_frame and " ".join(sh.text_frame.text.split()) == " ".join(texte.split())]
    if len(trouvees) != 1:
        raise ValueError(f"texte {texte!r} : {len(trouvees)} forme(s) ; 1 exigee")
    return trouvees[0]


def _ecrire(sh, texte):
    """Ne reecrit que si le texte differe (un set_run identique compte comme modification)."""
    if sh.text_frame.text != texte:
        deck_draw.set_run(sh, texte)


def _prst(sh):
    g = sh._element.find(f".//{NS_A}prstGeom")
    return g.get("prst") if g is not None else ""


def _xfrm(el):
    return next(el.iter(f"{NS_A}xfrm"))


def _poser(el, x, y, w=None, h=None):
    xf = _xfrm(el)
    off, ext = xf.find(f"{NS_A}off"), xf.find(f"{NS_A}ext")
    off.set("x", str(_pt(x)))
    off.set("y", str(_pt(y)))
    if w is not None:
        ext.set("cx", str(_pt(w)))
        ext.set("cy", str(_pt(h)))


def _nouvel_id(s):
    return max(sh.shape_id for sh in s.shapes) + 1


def _cloner(s, sh, apres=None):
    """Copie profonde d'une forme, identifiant neuf ; inseree apres `apres` (ou en fin d'arbre)."""
    el = copy.deepcopy(sh._element)
    next(e for e in el.iter() if e.tag.endswith("}cNvPr")).set("id", str(_nouvel_id(s)))
    if apres is None:
        s.shapes._spTree.append(el)
    else:
        apres.addnext(el)
    return el


# ---------------------------------------------------------------- reperes de lecture : 12 -> 13 pastilles
def _pastilles(s):
    return sorted((sh for sh in s.shapes if sh.shape_type == 1 and round(sh.width / 12700) == 8 and round(sh.height / 12700) == 8 and round(sh.top / 12700) == 70),
                  key=lambda sh: sh.left)


def _remplir(sh, rgb):
    sh.fill.solid()
    sh.fill.fore_color.rgb = rgb


def etendre_reperes(s):
    """12 pastilles -> 13 : le rang se decale de 11 pt vers la gauche (l'ecart a l'etiquette PROPOSITION A VALIDER reste le meme) et une pastille claire est ajoutee a droite."""
    ps = _pastilles(s)
    if len(ps) != 12:
        return None
    pas = (ps[1].left - ps[0].left) / 12700
    dernier_x = ps[-1].left / 12700 - pas
    modele = next(p for p in ps if str(p.fill.fore_color.rgb) == str(CLAIR))
    for p in ps:
        p.left = p.left - _pt(pas)
    el = _cloner(s, modele, apres=ps[-1]._element)
    _poser(el, dernier_x + pas, 70)
    return _pastilles(s)


# ---------------------------------------------------------------- la nouvelle slide
def _illustration(s):
    """Zone d'illustration : dix modeles de reference (2 colonnes x 5) et trois combinaisons frequentes. Aucune classification, aucun score."""
    tx(s, 190, 98, 289, 22, [[("DIX MODÈLES DE RÉFÉRENCE", 9.5, True, NAVY)]], A.MIDDLE)
    tx(s, 491, 98, 168, 22, [[("SOUVENT COMBINÉS", 9.5, True, NAVY)]], A.MIDDLE)
    Y0, PAS, H, W, GAP = 126, 27, 24, 211, 12
    for k, nom in enumerate(MODELES):
        col, row = divmod(k, 5)
        x, y = 45 + col * (W + GAP), Y0 + row * PAS
        forme(s, S.ROUNDED_RECTANGLE, x, y, W, H, PANEL, None, adj=0.3)
        forme(s, S.ROUNDED_RECTANGLE, x + 4, y + 3, 26, 18, CYAN, None, adj=0.25)
        tx(s, x + 4, y + 3, 26, 18, [[(f"M{k + 1}", 9, True, NAVY)]], A.MIDDLE, P.CENTER)
        tx(s, x + 36, y, W - 40, H, [[(nom, 9, True, NAVY)]], A.MIDDLE)
    bas = Y0 + 4 * PAS + H
    hs = (36, 36, 48)
    reste = (bas - Y0) - sum(hs)
    g = reste / 2
    y = Y0
    for lignes, h in zip(COMBINAISONS, hs, strict=True):
        forme(s, S.ROUND_2_DIAG_RECTANGLE, 491, y, 168, h, BLANC, LINE, adj=0.15, lw=0.75)
        tx(s, 501, y, 152, h, [[(ligne, 9.5, True, NAVY)] for ligne in lignes], A.MIDDLE)
        y += h + g


def nouvelle_conviction(prs):
    core = deck_base.core()
    modele = _s(prs, T_MODELE)
    ref = _s(prs, T_REF)
    rang = list(prs.slides).index(ref)
    s = core.copier_slide(prs, modele, index=rang + 1)
    ext = deck_draw._sections(prs)  # copier_slide ne met pas a jour les sections p14 : la nouvelle slide rejoint celle de sa reference
    if ext is not None:
        deck_draw._placer_dans_section(ext, deck_draw.id_de(prs, ref), deck_draw.id_de(prs, s))
    deck_draw.set_run(s.shapes.title, T_NEUVE)
    _ecrire(_par_texte(s, CHIP_ANCIEN), CHIP_NEUF)
    _ecrire(_par_texte(s, CRITERE_ANCIEN), CRITERE_NEUF)
    _ecrire(_par_texte(s, CHANTIER_ANCIEN), CHANTIER_NEUF)
    # le corps du gabarit (goutte-pictogramme et trois colonnes, y 95..270) est remplace ; la pastille CONVICTION remonte en tete de zone
    chip = _par_texte(s, CHIP_NEUF)
    chip_fond = next(sh for sh in s.shapes if sh.shape_id != chip.shape_id and _prst(sh) == "roundRect" and sh.left == chip.left - _pt(6) and sh.top == chip.top)
    for sh in list(s.shapes):
        if 95 * 12700 <= sh.top < 270 * 12700 and sh.shape_id not in (chip.shape_id, chip_fond.shape_id):
            sh._element.getparent().remove(sh._element)
    chip.top = chip_fond.top = _pt(98)
    _illustration(s)
    note = tx(s, 45, 364, 614, 12, [[(SOURCE, 9, False, SLATE)]], A.TOP)
    for r in note.text_frame.paragraphs[0].runs:
        r.font.italic = True
    return s

# ---------------------------------------------------------------- slide d'introduction : « Treize convictions »
def introduction(prs):
    s = _s(prs, T_9)
    deck_draw.set_run(s.shapes.title, T_9_NEUF)
    _ecrire(_par_texte(s, BARRE), BARRE_NEUVE)
    # la carte « Culture et organisation » : premiere carte (round2DiagRect) en partant de la gauche
    cartes = sorted((sh for sh in s.shapes if _prst(sh) == "round2DiagRect"), key=lambda sh: sh.left)
    carte = cartes[0]
    assert deck_draw.plat(_par_texte(s, "Culture et organisation").text_frame.text) == "Culture et organisation"
    g, d, b = carte.left, carte.left + carte.width, carte.top + carte.height
    dedans = [sh for sh in s.shapes if sh is not carte and sh.left >= g and sh.left + sh.width <= d and sh.top >= carte.top + 50 * 12700 and sh.top + sh.height <= b]
    chips = sorted((sh for sh in dedans if sh.shape_type == 1 and round(sh.width / 12700) == 18 and round(sh.height / 12700) == 18), key=lambda sh: sh.top)
    assert len(chips) == 3, f"{len(chips)} pastilles numerotees dans la carte (3 attendues)"
    groupes = []
    for c in chips:
        num = next(sh for sh in dedans if sh.has_text_frame and sh.text_frame.text.strip() and abs(sh.top - c.top) < _pt(1) and abs(sh.left - c.left) < _pt(1))
        lab = next(sh for sh in dedans if sh.has_text_frame and abs(sh.left - (c.left + _pt(24))) < _pt(1) and abs(sh.top - c.top) < _pt(2))
        groupes.append((c, num, lab))
    y0 = chips[0].top / 12700
    pas = 35  # quatre lignes dont la derniere sur trois lignes de texte tiennent dans la carte (fin a 339, carte a 344)
    for k, (c, num, lab) in enumerate(groupes):
        dy = (y0 + k * pas) - c.top / 12700
        for sh in (c, num, lab):
            sh.top = sh.top + _pt(dy)
    c, num, lab = groupes[-1]
    y3 = y0 + 3 * pas
    chaine = []
    prec = lab._element
    for sh in (c, num, lab):
        el = _cloner(s, sh, apres=prec)
        _poser(el, sh.left / 12700, y3 - (0.5 if sh is lab else 0) + 0)
        prec = el
        chaine.append(el)
    nouveaux = [sh for sh in s.shapes if sh._element in chaine]
    for sh in nouveaux:
        if sh.has_text_frame and sh.text_frame.text.strip() == num.text_frame.text.strip():
            _ecrire(sh, "13")
        elif sh.has_text_frame and sh.text_frame.text.strip():
            _ecrire(sh, LABEL_9)
    return s


# ---------------------------------------------------------------- surtitres et reperes du chapitre
def renumeroter(prs):
    kickers = [sh for sl in prs.slides for sh in sl.shapes if sh.has_text_frame and KICKER.match(sh.text_frame.text)]
    n = len(kickers)
    for i, sh in enumerate(kickers, 1):
        _ecrire(sh, f"02 · NOS CONVICTIONS · {i}/{n}")


def reperes(prs, nouvelle):
    for sl in prs.slides:
        if not any(sh.has_text_frame and KICKER.match(sh.text_frame.text) for sh in sl.shapes):
            continue
        ps = etendre_reperes(sl)
        if ps and sl is nouvelle:
            for k, p in enumerate(ps, 1):
                _remplir(p, NAVY if k == 13 else CLAIR)


def retouche(prs):
    nouvelle = nouvelle_conviction(prs)
    introduction(prs)
    reperes(prs, nouvelle)
    renumeroter(prs)


def _ids():
    prs = Presentation(deck_base.resoudre_base(BASE))
    ids = [f"id:{s.slide_id}" for s in prs.slides if any(sh.has_text_frame and KICKER.match(sh.text_frame.text) for sh in s.shapes)]
    assert len(ids) == 12, f"{len(ids)} surtitres « NOS CONVICTIONS » trouves, 12 attendus"
    return ids


ETAPES = [{"declarer": _ids(), "f": retouche, "nouvelles_max": 1, "nom": "conviction 13 (equipe plateforme), chapitre n/13, introduction « Treize »"}]







