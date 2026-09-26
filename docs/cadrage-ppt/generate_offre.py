"""Deck « Offre Infra as a Product » — nouvelle version (2026-09-26).

La SOURCE est le PPT déposé par l'utilisateur (`source/offre-iap-source.pptx`,
sur le vrai template OCTO) : sa structure de chapitres fait foi. Ce script le
transforme de façon rejouable — doublons supprimés, textes reformulés, slides
vides remplies, chapitres renumérotés et illustrés — puis passe les filets
géométriques.

Charte (CLAUDE.md) : navy encre, cyan en aplat seulement, jamais sur du texte ;
« un sur N en accent ». Pas de « gaspillage » (arbitrage du commit 94b04ff).
Vocabulaire de composants (skill deck-design-library, catalogue proposition
commerciale) : conteneur = contour blanc, jamais aplat gris ; étiquette courte =
pilule pleine ; chevron = séquence ; badge à cheval sur un bord ; bandeau de
clôture navy à guillemet.

Usage : python generate_offre.py  (depuis docs/cadrage-ppt/)
"""
import os
import sys

import pptx_deck_vscode3 as D
from PIL import Image, ImageDraw
from pptx import Presentation
from pptx.enum.dml import MSO_LINE_DASH_STYLE
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, MSO_AUTO_SIZE, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "source", "offre-iap-source.pptx")
SORTIE = os.path.join(HERE, "offre-infra-as-a-product-V1.pptx")
IMG_DIR = os.path.join(HERE, "_img")

NAVY, ACCENT, MUTED = "#0E2356", "#00D2DD", "#586586"
TRACK, LINE, WHITE = "#E7E9EE", "#CFD3DD", "#FFFFFF"

X0, XR, YB = 0.62, 9.15, 4.98   # zone de contenu (badge de page à 5.08)
W = XR - X0

CHAPITRES = ["Contexte et enjeux", "Les choix possibles",
             "Infra as a product, pourquoi ce choix ?", "Démarche globale",
             "Démarche détaillée", "Le dispositif", "Le prix"]
# photos CC0 déjà en cache (_img/_brut_*, source et licence : images-manifest.json)
PHOTOS = ["mountains_0", "canyon_0", "forest_0", "riverdelta_5", "wheatfield_0", "ocean_0",
          "dunes_0"]
PHASES = ["Explorer et diagnostiquer", "Cadrer l'offre", "Assainir", "Transformer"]


# ---------------------------------------------------------------- primitives
def forme(s, kind, x, y, w, h, fill=None, line=None, lw=1.25, adj=None):
    shp = s.shapes.add_shape(kind, Inches(x), Inches(y), Inches(w), Inches(h))
    style = shp._element.find(qn("p:style"))
    if style is not None:              # sinon l'effectRef du thème pose une ombre
        shp._element.remove(style)
    if adj is not None:
        shp.adjustments[0] = adj
    if fill is None:
        shp.fill.background()
    else:
        shp.fill.solid()
        shp.fill.fore_color.rgb = D.rgb(fill)
    if line is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = D.rgb(line)
        shp.line.width = Pt(lw)
    return shp


def carte(s, x, y, w, h, line=LINE, fill=WHITE, lw=1.25):
    """Conteneur multi-lignes : contour sur fond blanc, coins arrondis."""
    return forme(s, MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h, fill, line, lw,
                 adj=min(0.5, 0.12 / min(w, h)))


def rich(s, x, y, w, h, paras, anchor=MSO_ANCHOR.TOP, align=PP_ALIGN.LEFT):
    """paras : liste de paragraphes ; paragraphe = liste de runs (texte, opts)
    ou tuple (texte, opts). opts : size, bold, italic, color, space_after."""
    box = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = True
    tf.auto_size = MSO_AUTO_SIZE.NONE
    tf.vertical_anchor = anchor
    for m in ("margin_left", "margin_right", "margin_top", "margin_bottom"):
        setattr(tf, m, 0)
    for i, para in enumerate(paras):
        runs = [para] if isinstance(para, tuple) else para
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        sa = max(o.get("space_after", 0) for _, o in runs)
        if sa:
            p.space_after = Pt(sa)
        for texte, o in runs:
            r = p.add_run()
            # espaces insécables : jamais de « » ni de « : » orphelin en début de ligne
            r.text = (texte.replace("« ", "« ").replace(" »", " »")
                      .replace(" :", " :").replace(" ;", " ;"))
            f = r.font
            f.name = "Outfit"                  # police des textes du gabarit
            f.size = Pt(o.get("size", 10.5))
            f.bold = o.get("bold", False)
            f.italic = o.get("italic", False)
            f.color.rgb = D.rgb(o.get("color", NAVY))
    return box


def pilule(s, x, y, w, h, texte, fill=NAVY, color=WHITE, size=9, bold=True):
    forme(s, MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h, fill, adj=0.5)
    rich(s, x + 0.04, y, w - 0.08, h, [(texte, {"size": size, "bold": bold, "color": color})],
         anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)


def badge(s, cx, cy, d, texte, accent=False, size=11):
    forme(s, MSO_SHAPE.OVAL, cx - d / 2, cy - d / 2, d, d, ACCENT if accent else NAVY,
          WHITE, lw=1.5)
    rich(s, cx - d / 2, cy - d / 2, d, d,
         [(texte, {"size": size, "bold": True, "color": NAVY if accent else WHITE})],
         anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)


def chevron(s, x, y, w, h, texte, accent=False, size=10.5):
    forme(s, MSO_SHAPE.CHEVRON, x, y, w, h, ACCENT if accent else NAVY, adj=0.35)
    retrait = 0.35 * min(w, h) + 0.04
    rich(s, x + retrait, y, w - 2 * retrait, h,
         [(texte, {"size": size, "bold": True, "color": NAVY if accent else WHITE})],
         anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)


def fleche(s, x, y, w=0.2, h=0.26):
    forme(s, MSO_SHAPE.CHEVRON, x, y, w, h, NAVY, adj=0.5)


def etiquette(s, x, y, w, texte):
    rich(s, x, y, w, 0.2, [(texte.upper(), {"size": 8, "bold": True, "color": MUTED})])


def chapo(s, y, paras, h=0.5):
    """Chapeau à barre verticale d'accent (pas d'italique nu)."""
    forme(s, MSO_SHAPE.ROUNDED_RECTANGLE, X0, y + 0.02, 0.05, h - 0.04, ACCENT, adj=0.5)
    rich(s, X0 + 0.18, y, W - 0.18, h, paras, anchor=MSO_ANCHOR.MIDDLE)


def cloture(s, y, h, texte, size=11.5):
    """Bandeau de clôture signature : navy plein, guillemet décoratif."""
    forme(s, MSO_SHAPE.ROUNDED_RECTANGLE, X0, y, W, h, NAVY, adj=min(0.5, 0.1 / h))
    rich(s, X0 + 0.15, y - 0.06, 0.45, 0.5, [("“", {"size": 30, "bold": True,
         "color": ACCENT})])
    rich(s, X0 + 0.65, y, W - 0.85, h, [(texte, {"size": size, "bold": True,
         "color": WHITE})], anchor=MSO_ANCHOR.MIDDLE)


def gras(texte, cle, size=10.5, color=NAVY, italic=False):
    """Emphase en ligne : `cle` en gras dans une phrase de poids normal."""
    o = {"size": size, "color": color, "italic": italic}
    if not cle or cle not in texte:
        return [(texte, o)]
    a, b = texte.split(cle, 1)
    return [(a, o), (cle, {**o, "bold": True}), (b, o)]


def tete_queue(texte, size=10, color=NAVY):
    """« Tête — suite » : la tête en gras."""
    tete, _, queue = texte.partition(" — ")
    return [(tete, {"size": size, "bold": True, "color": color}),
            (f" — {queue}" if queue else "", {"size": size, "color": color})]


def cols(n, gap=0.18, x0=X0, w=W):
    cw = (w - gap * (n - 1)) / n
    return [(x0 + i * (cw + gap), cw) for i in range(n)]


def ph(slide, idx):
    for s in slide.placeholders:
        if s.placeholder_format.idx == idx:
            return s
    return None


def set_ph(slide, idx, texte):
    p = ph(slide, idx)
    if p is not None:
        p.text_frame.text = texte


def retirer(shape):
    el = shape._element
    el.getparent().remove(el)


def retirer_ph(slide, *idxs):
    for idx in idxs:
        p = ph(slide, idx)
        if p is not None:
            retirer(p)


def vider(slide):
    """Retire tout sauf le titre (placeholder 0) — pour les slides redessinées."""
    for sh in list(slide.shapes):
        if not (sh.is_placeholder and sh.placeholder_format.idx == 0):
            retirer(sh)


def iter_shapes(shapes):
    for s in shapes:
        yield s
        if s.shape_type == 6:  # groupe
            yield from iter_shapes(s.shapes)


def remplacer_partout(prs, table):
    for slide in prs.slides:
        for s in iter_shapes(slide.shapes):
            if not s.has_text_frame:
                continue
            for p in s.text_frame.paragraphs:
                for r in p.runs:
                    for a, b in table:
                        if a in r.text:
                            r.text = r.text.replace(a, b)


def texte_deck(prs):
    out = []
    for i, slide in enumerate(prs.slides, 1):
        for s in iter_shapes(slide.shapes):
            if s.has_text_frame:
                out.append((i, s.text_frame.text))
    return out


# ---------------------------------------------------------------- slides
def couverture(s):
    rich(s, 1.81, 2.8, 3.4, 0.3, [("Faire de l'infrastructure un produit que ses "
         "utilisateurs choisissent", {"size": 9.5, "color": WHITE})])


def sommaire(prs):
    """Sommaire sur le gabarit natif « Table des matières [7] »."""
    layout = next(lay for lay in prs.slide_layouts if lay.name.startswith("95 - "))
    s = prs.slides.add_slide(layout)
    s.shapes.title.text = "Sommaire"
    for k, nom in enumerate(CHAPITRES, 1):
        ph(s, k).text_frame.text = nom
    return s


def photo_chapitre(slide, scene):
    """Remplace l'image du cadre du chapitre par une photo CC0 recadrée à son
    aspect : le cadre (forme, position) du gabarit est conservé."""
    pic = next(sh for sh in slide.shapes if sh.shape_type == 13)
    aspect = pic.width / pic.height
    brut = os.path.join(IMG_DIR, f"_brut_{scene}.jpg")
    im = Image.open(brut).convert("RGB")
    w, h = im.size
    if w / h > aspect:
        nw = int(h * aspect)
        im = im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    else:
        nh = int(w / aspect)
        im = im.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
    im = im.resize((900, int(900 / aspect)))
    chemin = os.path.join(IMG_DIR, f"chap_{scene}_{im.size[0]}x{im.size[1]}.jpg")
    im.save(chemin, quality=88, optimize=True)
    _, rid = slide.part.get_or_add_image_part(chemin)
    blip_fill = pic._element.blipFill
    blip_fill.find(qn("a:blip")).set(qn("r:embed"), rid)
    src_rect = blip_fill.find(qn("a:srcRect"))
    if src_rect is not None:
        blip_fill.remove(src_rect)


def executive_summary(s):
    set_ph(s, 2, "L'offre en cinq points")
    retirer_ph(s, 1)
    rows = [
        ("Le constat", "L'infra est devenue un guichet saturé : RUN subi, experts drainés "
         "sur du répétitif, offre illisible, plateformes contournées.", "guichet saturé"),
        ("La cible", "Infra as a product : des utilisateurs identifiés, un catalogue de "
         "capacités, un propriétaire, une roadmap et une valeur mesurée.", "Infra as a product"),
        ("Pourquoi maintenant", "80 % des grandes organisations ont une platform team en "
         "2026, moins de 30 % en tirent des gains mesurables (Gartner) ; l'IA amplifie "
         "une organisation mûre, jamais l'inverse.", "moins de 30 %"),
        ("La démarche", "Un Assessment flash d'entrée qui chiffre le statu quo, puis une "
         "trajectoire : cadrer l'offre, assainir, transformer.", "Assessment flash"),
        ("Ce que vous obtenez", "De la capacité humaine récupérée et réinvestie, mesurée "
         "dès le T0 — et des équipes qui portent le modèle sans nous.",
         "capacité humaine récupérée"),
    ]
    h, gap, y0 = 0.62, 0.1, 1.38
    for i, (lab, corps, cle) in enumerate(rows):
        y = y0 + i * (h + gap)
        carte(s, X0 + 1.0, y, W - 1.0, h)
        pilule(s, X0, y + 0.13, 2.0, h - 0.26, lab, fill=ACCENT if i == 0 else NAVY,
               color=NAVY if i == 0 else WHITE, size=10)
        rich(s, X0 + 2.2, y, W - 2.35, h, [gras(corps, cle, size=10.5)],
             anchor=MSO_ANCHOR.MIDDLE)


def problematiques(s):
    set_ph(s, 2, "Quatre symptômes, une même cause : une infra pensée comme un guichet")
    retirer_ph(s, 1)
    items = [
        ("Des délais qui s'allongent",
         "Trois semaines pour un environnement ; l'équipe infra devient le goulot."),
        ("Une offre que personne ne lit",
         "Plusieurs plateformes, aucune vision d'ensemble ; on ne sait pas à qui s'adresser."),
        ("Des outils contournés",
         "Une plateforme existe, les équipes applicatives passent à côté."),
        ("Des coûts sans valeur visible",
         "Les coûts cloud explosent sans qu'on sache ce qu'ils apportent."),
    ]
    y, h = 1.75, 2.05
    for i, ((x, w), (t, c)) in enumerate(zip(cols(4), items, strict=True)):
        carte(s, x, y, w, h, line=NAVY)
        badge(s, x + w / 2, y, 0.5, f"{i + 1}", accent=i == 0, size=13)
        rich(s, x + 0.15, y + 0.4, w - 0.3, h - 0.5, [
            (t, {"size": 12, "bold": True, "space_after": 6}),
            (c, {"size": 10.5, "color": MUTED})], align=PP_ALIGN.CENTER)
    cloture(s, 4.1, 0.85, "La réponse n'est pas un outil de plus, c'est une posture "
            "produit : voici les situations vécues, puis ce que l'approche apporte.", size=11)


def situations(s):
    set_ph(s, 0, "Des situations que toute DSI reconnaît")
    retirer_ph(s, 1)
    vs = [  # (famille, verbatim, mot-clé)
        ("Délais", "Nos développeurs attendent trois semaines pour obtenir leur "
         "environnement.", "trois semaines"),
        ("Délais", "Notre équipe infra est devenue un goulot d'étranglement.",
         "goulot d'étranglement"),
        ("Délais", "Nous voulons réduire les tickets.", "réduire les tickets"),
        ("Coûts", "Nos coûts cloud explosent.", "explosent"),
        ("Offre illisible", "Nous avons une plateforme, mais personne ne l'utilise.",
         "personne ne l'utilise"),
        ("Offre illisible", "Nous avons plusieurs plateformes qui font plus ou moins la "
         "même chose.", "plusieurs plateformes"),
        ("Offre illisible", "Pour développer un produit, il faut solliciter plusieurs "
         "équipes — sans savoir à qui s'adresser, ni pour quoi.", "à qui s'adresser"),
        ("Offre illisible", "Nous n'avons pas de vision globale : pas d'outils intégrés et "
         "simples au service des applications.", "pas de vision globale"),
    ]
    xs = cols(4, gap=0.22)
    h = 1.55
    for k, (fam, v, cle) in enumerate(vs):
        x, w = xs[k % 4]
        y = 1.3 + (k // 4) * 1.85                     # grille stricte, bulles alignées
        forme(s, MSO_SHAPE.ROUND_2_DIAG_RECTANGLE, x, y, w, h, WHITE, NAVY, 1.25, adj=0.18)
        rich(s, x + 0.12, y - 0.02, 0.4, 0.45, [("“", {"size": 28, "bold": True})])
        pw = 0.075 * len(fam) + 0.3
        pilule(s, x + w - pw - 0.12, y - 0.13, pw, 0.26, fam,
               fill=ACCENT if fam == "Coûts" else NAVY,
               color=NAVY if fam == "Coûts" else WHITE, size=8)
        rich(s, x + 0.18, y + 0.42, w - 0.32, h - 0.5, [gras(v, cle, size=10, italic=True)])


def apports(s):
    set_ph(s, 0, "Ce que l'approche produit apporte, problème par problème")
    retirer_ph(s, 1)
    for g in [x for x in s.shapes if getattr(x, "has_table", False)]:
        retirer(g)
    lignes = [
        ("L'infra est perçue comme un centre de coûts", "Clarifier la proposition de valeur",
         "Valeur délivrée par capacité"),
        ("Les utilisateurs ne comprennent pas l'offre", "Formaliser un catalogue de capacités",
         "Demandes couvertes par le catalogue"),
        ("Les demandes sont trop spécifiques", "Identifier les besoins récurrents",
         "Part de demandes standardisées"),
        ("Les outils sont peu adoptés", "Travailler l'UX et l'adoption", "Taux d'adoption"),
        ("Les équipes applicatives contournent l'infra",
         "Rendre l'offre simple et désirable", "Usages hors plateforme"),
        ("Les priorités sont politiques", "Prioriser par valeur, usage, risque, adoption",
         "Backlog priorisé sur critères partagés"),
        ("Les capacités livrées ne sont pas utilisées", "Mesurer l'usage réel",
         "Usage par capacité livrée"),
        ("L'automatisation manque de financement", "Construire un business case produit",
         "Capacité RUN récupérée"),
        ("L'obsolescence est subie", "Piloter le cycle de vie des capacités",
         "Décommissionnements tenus"),
        ("La plateforme est trop technique", "Définir des parcours compréhensibles",
         "Délai de mise à disposition"),
    ]
    wp, wa, wi = 2.9, 2.85, 2.28
    xa = X0 + wp + 0.25
    xi = XR - wi
    etiquette(s, X0, 1.02, wp, "Le problème")
    etiquette(s, xa, 1.02, wa, "L'apport de l'approche produit")
    etiquette(s, xi, 1.02, wi, "L'indicateur à suivre")
    h, gap, y0 = 0.31, 0.056, 1.3
    for i, (p, a, ind) in enumerate(lignes):
        y = y0 + i * (h + gap)
        carte(s, X0, y, wp, h)
        rich(s, X0 + 0.12, y, wp - 0.2, h, [(p, {"size": 9})], anchor=MSO_ANCHOR.MIDDLE)
        fleche(s, X0 + wp + 0.05, y + 0.07, 0.14, 0.17)
        carte(s, xa, y, wa, h, line=NAVY)
        rich(s, xa + 0.12, y, wa - 0.2, h, [(a, {"size": 9, "bold": True})],
             anchor=MSO_ANCHOR.MIDDLE)
        pilule(s, xi, y + 0.02, wi, h - 0.04, ind, fill=ACCENT if i == 7 else TRACK,
               color=NAVY, size=8.5, bold=False)


def guichet_vers_produit(s):
    """Source S8 : réintègre le bloc IA du deck précédent (perdu dans la source)
    et explicite le « pourquoi » demandé en commentaire."""
    for sh in list(s.shapes):
        if sh.has_text_frame and ("L'objectif" in sh.text_frame.text
                                  or sh.text_frame.text.strip() == "“"):
            retirer(sh)
        elif (sh.shape_type == 1 and Inches(0.6) < sh.left < Inches(0.75)
              and sh.top > Inches(4.9)):
            retirer(sh)                       # barre d'accent orpheline
    rich(s, 0.81, 3.7, 0.5, 0.5, [("IA", {"size": 12, "bold": True, "color": WHITE})],
         anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
    rich(s, 1.51, 3.55, 7.43, 0.8, [
        ("AVEC L'ARRIVÉE DE L'IA — UNE SURSOLLICITATION EXACERBÉE",
         {"size": 8, "bold": True, "color": MUTED, "space_after": 2}),
        gras("Trop de demandes, des équipes engorgées : la même pression que le guichet "
             "d'hier, amplifiée par l'IA plutôt que résolue par elle.", "amplifiée par l'IA",
             size=10)], anchor=MSO_ANCHOR.MIDDLE)
    cloture(s, 4.45, 0.53, "L'objectif : infra as a product — pour absorber la demande "
            "au lieu de la subir.", size=11.5)
    # le commentaire « expliciter pourquoi » est traité (bloc IA + bandeau) : on le retire
    for rid, rel in list(s.part.rels.items()):
        if rel.reltype.endswith("/comments"):
            s.part.drop_rel(rid)


def enjeux(s):
    set_ph(s, 2, "Cinq enjeux qui justifient le passage en mode produit")
    retirer_ph(s, 1)
    items = [
        ("Efficacité opérationnelle", "Moins de dépendances grâce à l'autonomie ; les "
         "experts aux bons endroits ; une livraison rapide."),
        ("Expérience utilisateur", "Une expérience fluide et sans couture pour les équipes "
         "qui consomment l'infra."),
        ("Robustesse", "Un monitoring qui accélère la prise de décision."),
        ("Maîtrise des coûts", "Inventaire du parc, licences inutilisées, décommissionnement "
         "des actifs « zombies »."),
        ("Anticiper l'IA", "Plus de mises en production à absorber ; un usage interne qui "
         "exige gouvernance et coordination."),
    ]
    h, gap, y0 = 0.6, 0.13, 1.4
    for i, (t, c) in enumerate(items):
        y = y0 + i * (h + gap)
        carte(s, X0 + 0.28, y, W - 0.28, h, line=NAVY if i == 0 else LINE)
        badge(s, X0 + 0.28, y + h / 2, 0.46, f"{i + 1}", accent=i == 0, size=12)
        rich(s, X0 + 0.7, y, 2.4, h, [(t, {"size": 12, "bold": True})],
             anchor=MSO_ANCHOR.MIDDLE)
        rich(s, X0 + 3.2, y, W - 3.35, h, [(c, {"size": 10.5, "color": MUTED})],
             anchor=MSO_ANCHOR.MIDDLE)


def alternatives(s):
    """Source S15 redessinée : plus lisible, texte surligné réécrit."""
    set_ph(s, 0, "Quatre alternatives, aucune ne finance la cible")
    vider(s)
    chapo(s, 1.0, [
        gras("Sponsor qualifié : DSI ou direction infrastructure, sur une ligne budgétaire "
             "transformation — jamais le budget RUN.", "jamais le budget RUN", size=9.5),
        gras("La modernisation de l'infra recule face à la cyber dans les priorités 2026 "
             "(baromètre Abraxio) : l'argument qui porte est « récupérer une capacité humaine "
             "rare », pas « moderniser l'infra ».", "récupérer une capacité humaine rare",
             size=9.5)], h=0.62)
    rows = [
        ("Ne rien faire", "Zéro coût apparent.", "Le coût du statu quo monte",
         "C'est lui que l'Assessment flash chiffre."),
        ("FinOps outillé seul", "Mesure les dépenses inutiles : marché mature, 29 % de la "
         "dépense cloud (Flexera).", "Ni cible produit, ni réallocation",
         "Le chiffre devient une capacité produit gouvernée, pas une simple économie."),
        ("Platform engineering pur", "La cible produit/plateforme, un modèle devenu standard.",
         "La cible sans le financement", "80 % de platform teams en 2026, moins de 30 % de "
         "gains mesurables (Gartner)."),
        ("AIOps / agentic outillé", "Time-to-value court (ServiceNow, Datadog).",
         "Automatise le RUN sans transformer", "Plus de 40 % des projets agentic abandonnés "
         "d'ici 2027 (Gartner, juin 2025)."),
    ]
    wl, xr = 3.45, X0 + 3.45 + 0.35
    wr = XR - xr
    etiquette(s, X0, 1.72, wl, "L'alternative")
    etiquette(s, xr, 1.72, wr, "Ce qui lui manque — la réponse IAP")
    h, gap, y0 = 0.5, 0.08, 1.95
    for a, apport, manque, rep in rows:
        y = y0 + rows.index((a, apport, manque, rep)) * (h + gap)
        carte(s, X0, y, wl, h)
        rich(s, X0 + 0.12, y, wl - 0.2, h, [[(a, {"size": 9.5, "bold": True}),
             (f" — {apport}", {"size": 9, "color": MUTED})]], anchor=MSO_ANCHOR.MIDDLE)
        fleche(s, X0 + wl + 0.1, y + 0.13, 0.17, 0.24)
        carte(s, xr, y, wr, h, line=NAVY)
        rich(s, xr + 0.12, y, wr - 0.2, h, [[(manque, {"size": 9.5, "bold": True}),
             (f" — {rep}", {"size": 9})]], anchor=MSO_ANCHOR.MIDDLE)
    yb = y0 + 4 * (h + gap) + 0.02
    for (x, w), (titre, corps) in zip(cols(2, gap=0.2), [
        ("Ce que les quatre alternatives n'ont pas", "« Infrastructure as a Product » existe "
         "ailleurs (Thoughtworks, Itential). Notre différenciateur : produit + assainissement "
         "+ doctrine IA."),
        ("Réponse au « je ne veux que la baisse des coûts »", "Un Assessment flash d'entrée, "
         "puis la trajectoire — jamais l'assainissement seul. Sous pression IA : un cas "
         "d'usage public, tout de suite, sous gate.")], strict=True):
        carte(s, x, yb, w, YB - yb, line=NAVY, fill=NAVY)
        rich(s, x + 0.15, yb, w - 0.3, YB - yb, [
            (titre.upper(), {"size": 7.5, "bold": True, "color": WHITE, "space_after": 2}),
            (corps, {"size": 8.5, "color": WHITE})], anchor=MSO_ANCHOR.MIDDLE)


def typologies(s):
    set_ph(s, 0, "Six typologies de transformation")
    retirer_ph(s, 1, 2)
    items = [
        ("Expérience", "Nos utilisateurs trouvent l'infra trop compliquée.",
         ["Expérience développeur", "Self-service", "Golden paths", "Portail",
          "Documentation"]),
        ("Delivery", "Nous sommes trop lents.",
         ["Automatisation", "IaC", "CI/CD", "Provisioning", "Standardisation"]),
        ("Organisation", "Tout remonte à l'équipe infra centrale.",
         ["Team Topologies", "Ownership", "Plateforme", "Équipes produit"]),
        ("Valeur", "Nous dépensons beaucoup sans savoir ce que cela apporte.",
         ["Product management", "FinOps", "Métriques de valeur", "Priorisation"]),
        ("Fiabilité", "Nos systèmes sont trop fragiles.",
         ["SRE", "Observabilité", "SLO", "Error budgets", "Automatisation"]),
        ("Stratégie", "Nous voulons que l'infra devienne un levier stratégique.",
         ["Operating model", "Architecture", "Gouvernance", "Portefeuille produit"]),
    ]
    xs = cols(3, gap=0.2)
    h = 1.42
    for k, (t, v, levs) in enumerate(items):
        x, w = xs[k % 3]
        y = 1.2 + (k // 3) * (h + 0.3)
        carte(s, x, y, w, h, line=NAVY)
        pilule(s, x + 0.15, y - 0.14, 0.12 * len(t) + 0.55, 0.28, f"{k + 1:02d}  ·  {t}",
               fill=ACCENT if k == 0 else NAVY, color=NAVY if k == 0 else WHITE, size=8.5)
        rich(s, x + 0.15, y + 0.22, w - 0.3, 0.42, [(f"« {v} »", {"size": 9.5,
             "italic": True})])
        px, py = x + 0.15, y + 0.7
        for lev in levs:
            pw = 0.062 * len(lev) + 0.32
            if px + pw > x + w - 0.12:
                px, py = x + 0.15, py + 0.25
            pilule(s, px, py, pw, 0.21, lev, fill=TRACK, color=NAVY, size=7.5, bold=False)
            px += pw + 0.06
    cloture(s, 4.5, 0.48, "Un même client peut mener plusieurs transformations en "
            "parallèle : c'est au coach de choisir le point d'entrée.", size=10.5)


def definition(s):
    set_ph(s, 2, "Une définition, quatre piliers")
    retirer_ph(s, 1)
    carte(s, X0, 1.35, W, 0.9, line=NAVY, fill=NAVY)
    rich(s, X0 + 0.2, 1.35, 0.5, 0.6, [("“", {"size": 34, "bold": True, "color": ACCENT})])
    rich(s, X0 + 0.75, 1.35, W - 0.95, 0.9, [
        [("Traiter l'infrastructure comme un produit ", {"size": 12, "bold": True,
          "color": WHITE}),
         ("— des utilisateurs identifiés, une proposition de valeur, un catalogue de "
          "capacités, un propriétaire et une roadmap, et une valeur mesurée par l'usage.",
          {"size": 11, "color": WHITE})]], anchor=MSO_ANCHOR.MIDDLE)
    piliers = [
        ("Utilisateurs", "Partir des équipes qui consomment l'infra et de leurs douleurs "
         "mesurées."),
        ("Catalogue", "Des capacités lisibles, en self-service, avec un niveau de service "
         "explicite."),
        ("Ownership", "Un propriétaire produit par capacité, une roadmap priorisée sur des "
         "critères partagés."),
        ("Mesure", "L'adoption et l'usage réel pilotent les décisions, jusqu'au "
         "décommissionnement."),
    ]
    y, h = 2.75, 2.1
    for i, ((x, w), (t, c)) in enumerate(zip(cols(4), piliers, strict=True)):
        carte(s, x, y, w, h, line=NAVY if i == 0 else LINE)
        badge(s, x + w / 2, y, 0.5, f"{i + 1}", accent=i == 0, size=13)
        rich(s, x + 0.15, y + 0.42, w - 0.3, h - 0.5, [
            (t, {"size": 13, "bold": True, "space_after": 6}),
            (c, {"size": 10.5, "color": MUTED})], align=PP_ALIGN.CENTER)


def promesse(s):
    """Source S19 (avant/après) redessinée en paires reliées par chevron."""
    vider(s)
    s.shapes.title.text_frame.text = "Notre promesse"
    rich(s, X0, 0.85, W, 0.41, [("Ce que change l'infra as a product, concrètement",
         {"size": 14})], anchor=MSO_ANCHOR.MIDDLE)
    paires = [
        ("Guichet de tickets — personne n'est propriétaire du service.",
         "Un propriétaire produit — une roadmap, des indicateurs de pilotage."),
        ("Triage du RUN trop long — traité au fil de l'eau.",
         "Temps de triage du RUN réduit — capacité RUN récupérée."),
        ("Backlog invisible — aucun indicateur de pilotage.",
         "Backlog visible — priorisé, mesuré dans le temps."),
        ("Beaucoup de projets, peu d'indicateurs — du contrôle et du reporting partout.",
         "Process explicite, rôles définis — l'agent n'arrive qu'une fois le process écrit."),
        ("Un pilotage dans la douleur — trop de sujets pour trop peu de capacité.",
         "Des évolutions tech atteignables — un pilotage serein, des priorités tenues."),
    ]
    wl = 3.95
    xr = XR - wl
    pilule(s, X0, 1.33, 1.1, 0.27, "AVANT", fill=TRACK, color=NAVY, size=9)
    pilule(s, xr, 1.33, 2.4, 0.27, "APRÈS — infra as a product", size=9)
    h, gap, y0 = 0.47, 0.07, 1.7
    for i, (av, ap) in enumerate(paires):
        y = y0 + i * (h + gap)
        carte(s, X0, y, wl, h)
        rich(s, X0 + 0.14, y, wl - 0.24, h, [tete_queue(av, size=9.5, color=MUTED)],
             anchor=MSO_ANCHOR.MIDDLE)
        fleche(s, X0 + wl + 0.12, y + 0.1, 0.2, 0.27)
        carte(s, xr, y, wl, h, line=NAVY)
        rich(s, xr + 0.14, y, wl - 0.24, h, [[("✓  ", {"size": 9.5, "bold": True})]
             + tete_queue(ap, size=9.5)], anchor=MSO_ANCHOR.MIDDLE)
    cloture(s, 4.45, 0.53, "Faire les bonnes choses au bon moment, un backlog piloté, des "
            "résultats concrets — l'agentique accélère la démarche, il ne la remplace pas.",
            size=10)


def bascules(s):
    """Source S20 redessinée."""
    set_ph(s, 0, "Pourquoi cette transformation — et pourquoi maintenant")
    vider(s)
    chapo(s, 1.0, [gras("Trois bascules rendent l'infra as a product pertinente — et "
                        "urgente — maintenant.", "pertinente — et urgente —", size=11.5)],
          h=0.38)
    cartes = [
        ("L'infra subie n'est plus tenable", "RUN subi, experts seniors drainés sur du "
         "répétitif, dépenses cloud non maîtrisées, plateforme contournée : le coût du statu "
         "quo ne cesse de monter."),
        ("Le modèle produit/plateforme est prouvé", "Devenu un standard — mais 80 % des "
         "grandes organisations ont une platform team en 2026, moins de 30 % en tirent des "
         "gains mesurables (Gartner). Nous adressons cet écart."),
        ("L'IA rebat les cartes — l'organisation d'abord", "L'IA amplifie une organisation "
         "mûre, jamais l'inverse. S'y préparer maintenant (doctrine confidentialité-first) "
         "évite de la subir plus tard."),
    ]
    y, h = 1.75, 1.75
    for i, ((x, w), (t, c)) in enumerate(zip(cols(3, gap=0.22), cartes, strict=True)):
        fill = NAVY if i == 0 else WHITE
        coul = WHITE if i == 0 else NAVY
        carte(s, x, y, w, h, line=NAVY, fill=fill)
        badge(s, x + 0.4, y, 0.46, f"{i + 1}", accent=i == 0, size=12)
        rich(s, x + 0.18, y + 0.33, w - 0.36, h - 0.4, [
            (t, {"size": 11, "bold": True, "color": coul, "space_after": 5}),
            (c, {"size": 9.5, "color": WHITE if i == 0 else MUTED})])
    etiquette(s, X0, 3.72, W, "Et surtout — nos deux missions répondent trait pour trait "
              "aux deux douleurs du client")
    for (x, w), (douleur, mission, detail) in zip(cols(2, gap=0.3), [
        ("Subir le RUN", "TRANSFORMER", "cible produit/plateforme"),
        ("Les dépenses subies", "ASSAINIR", "capacité récupérée à réinvestir — sous réserve "
         "d'une réallocation côté client")], strict=True):
        yy = 4.05
        pilule(s, x, yy + 0.14, 1.45, 0.5, douleur, fill=TRACK, color=NAVY, size=9.5)
        fleche(s, x + 1.53, yy + 0.25, 0.18, 0.28)
        carte(s, x + 1.8, yy, w - 1.8, 0.78, line=NAVY)
        rich(s, x + 1.95, yy, w - 2.05, 0.78, [
            (mission, {"size": 10.5, "bold": True, "space_after": 1}),
            (detail, {"size": 9, "color": MUTED})], anchor=MSO_ANCHOR.MIDDLE)


def demarche_globale(s):
    set_ph(s, 2, "Quatre phases, des livrables à chaque étape")
    retirer_ph(s, 1)
    corps = [
        ("Assessment flash : entretiens, inventaire du parc et des demandes, coût du "
         "statu quo chiffré.", "Diagnostic et coût du statu quo"),
        ("Utilisateurs et parcours, catalogue de capacités cible, critères de "
         "priorisation partagés.", "Catalogue cible et roadmap"),
        ("Traiter les douleurs prioritaires : décommissionnement, licences, triage du RUN.",
         "Capacité récupérée, mesurée"),
        ("Premiers périmètres en mode produit : propriétaire, backlog, indicateurs d'usage.",
         "Premiers produits d'infra en service"),
    ]
    xs = cols(4, gap=0.08)
    for i, ((x, w), nom, (act, liv)) in enumerate(zip(xs, PHASES, corps, strict=True)):
        chevron(s, x, 1.38, w + (0.12 if i < 3 else 0), 0.6, f"{i + 1}. {nom}",
                accent=i == 0, size=10)
        cx, cw = x + 0.05, w - 0.1
        carte(s, cx, 2.15, cw, 2.8, line=NAVY if i == 0 else LINE)
        etiquette(s, cx + 0.14, 2.3, cw - 0.28, "Activités clés")
        rich(s, cx + 0.14, 2.55, cw - 0.28, 1.3, [(act, {"size": 10})])
        forme(s, MSO_SHAPE.RECTANGLE, cx + 0.14, 3.85, cw - 0.28, 0.012, LINE)
        etiquette(s, cx + 0.14, 3.97, cw - 0.28, "Livrable")
        rich(s, cx + 0.14, 4.2, cw - 0.28, 0.65, [(liv, {"size": 10.5, "bold": True})])


def ia_demarche(s):
    set_ph(s, 2, "L'IA accélère la démarche, elle ne la remplace pas — toujours après "
           "le gate de confidentialité")
    retirer_ph(s, 1)
    usages = [
        ("Explorer le parc et catégoriser l'historique des demandes plus vite.",
         "catégoriser l'historique"),
        ("Accélérer la mise en place du catalogue de services.", "catalogue de services"),
        ("Trier et qualifier les demandes entrantes : le temps de triage du RUN est "
         "rendu aux équipes.", "rendu aux équipes"),
        ("Documenter rapidement les capacités et les parcours utilisateurs.",
         "Documenter rapidement"),
    ]
    h, gap, y0 = 0.6, 0.13, 1.4
    for i, (nom, (u, cle)) in enumerate(zip(PHASES, usages, strict=True)):
        y = y0 + i * (h + gap)
        chevron(s, X0, y, 2.6, h, nom, accent=i == 2, size=10)
        carte(s, X0 + 2.75, y, W - 2.75, h, line=NAVY if i == 2 else LINE)
        badge(s, X0 + 2.75, y + h / 2, 0.36, "IA", accent=i == 2, size=8)
        rich(s, X0 + 3.1, y, W - 3.25, h, [gras(u, cle, size=10.5)],
             anchor=MSO_ANCHOR.MIDDLE)
    cloture(s, 4.4, 0.55, "Un gain mesuré dès le T0, pas promis.", size=12)


def planning(s):
    set_ph(s, 2, "Planning indicatif — durées à confirmer avec le client")
    retirer_ph(s, 1)
    xg, wg = X0 + 2.5, W - 2.5
    # frise de points : la cadence, sans échelle de dates inventée
    n = 16
    for k in range(n):
        cx = xg + 0.06 + k * (wg - 0.12) / (n - 1)
        forme(s, MSO_SHAPE.OVAL, cx - 0.05, 1.45, 0.1, 0.1, ACCENT if k in (3, 15) else LINE)
    rich(s, xg, 1.18, 1.5, 0.22, [("Démarrage", {"size": 8.5, "bold": True,
         "color": MUTED})])
    rich(s, xg + wg - 2.0, 1.18, 2.0, 0.22, [("Autonomie des équipes", {"size": 8.5,
         "bold": True, "color": MUTED})], align=PP_ALIGN.RIGHT)
    barres = [(0.0, 0.25), (0.2, 0.47), (0.4, 0.8), (0.55, 1.0)]
    h, gap, y0 = 0.46, 0.2, 1.8
    for i, (nom, (a, b)) in enumerate(zip(PHASES, barres, strict=True)):
        y = y0 + i * (h + gap)
        pilule(s, X0, y, 2.3, h, f"{i + 1}. {nom}", fill=ACCENT if i == 0 else NAVY,
               color=NAVY if i == 0 else WHITE, size=9.5)
        forme(s, MSO_SHAPE.RECTANGLE, xg, y + h / 2 - 0.006, wg, 0.012, LINE)
        forme(s, MSO_SHAPE.ROUNDED_RECTANGLE, xg + a * wg, y + 0.1, (b - a) * wg, h - 0.2,
              ACCENT if i == 0 else NAVY, adj=0.5)
    # jalon : restitution de l'Assessment flash
    jx = xg + 0.25 * wg
    forme(s, MSO_SHAPE.DIAMOND, jx - 0.11, y0 + 0.12, 0.22, 0.22, WHITE, NAVY, 1.5)
    rich(s, jx + 0.18, y0 + 0.05, 2.6, 0.36, [("Jalon : restitution de l'Assessment flash",
         {"size": 8.5, "bold": True})], anchor=MSO_ANCHOR.MIDDLE)
    chapo(s, 4.52, [("Durées à compléter : elles dépendent du périmètre retenu à l'issue "
                     "de l'Assessment flash.", {"size": 10, "color": MUTED})], h=0.4)


def demarche_detaillee(s):
    set_ph(s, 0, "Démarche détaillée")
    set_ph(s, 2, "Activités, livrables et prérequis par phase")
    retirer_ph(s, 1)
    contenu = [
        ("Entretiens utilisateurs et équipe infra ; inventaire du parc, des licences et des "
         "demandes ; chiffrage du statu quo", "Diagnostic ; coût du statu quo ; périmètres "
         "candidats", "Sponsor nommé ; accès aux données de tickets et d'inventaire"),
        ("Parcours utilisateurs ; catalogue de capacités cible ; critères de priorisation ; "
         "rôles produit", "Catalogue cible ; roadmap priorisée ; rôles définis",
         "Arbitrage du sponsor sur les premiers périmètres"),
        ("Décommissionnement ; licences inutilisées ; triage du RUN outillé par l'IA, "
         "après le gate de confidentialité", "Capacité récupérée et mesurée ; plan de "
         "réallocation", "Réallocation de la capacité décidée côté client"),
        ("Premiers périmètres en mode produit ; backlog et indicateurs d'usage ; "
         "accompagnement des profils clés", "Produits d'infra en service ; rituels de "
         "pilotage ; transfert aux équipes", "Propriétaires produit désignés ; ligne "
         "budgétaire transformation"),
    ]
    wl = 1.05
    xs = cols(4, gap=0.12, x0=X0 + wl + 0.1, w=W - wl - 0.1)
    rangs = [("Activités", 1.95, 1.25), ("Livrables", 3.28, 0.8), ("Prérequis", 4.16, 0.8)]
    for nom, y, _ in rangs:
        forme(s, MSO_SHAPE.RECTANGLE, X0, y - 0.05, W, 0.012,
              NAVY if nom == "Activités" else LINE)
        etiquette(s, X0, y + 0.02, wl, nom)
    for i, ((x, w), nom) in enumerate(zip(xs, PHASES, strict=True)):
        pilule(s, x, 1.38, w, 0.42, f"{i + 1}. {nom}", fill=ACCENT if i == 0 else NAVY,
               color=NAVY if i == 0 else WHITE, size=9.5)
        for (_, y, h), texte in zip(rangs, contenu[i], strict=True):
            rich(s, x + 0.04, y + 0.02, w - 0.08, h - 0.08, [(texte, {"size": 9})])


def accompagnement(s):
    """Détail de l'accompagnement — repris du deck précédent (v2.47, slides 22-23)."""
    set_ph(s, 0, "Le détail de l'accompagnement")
    set_ph(s, 2, "Les personnes d'abord, des livrables à chaque phase — la technique en "
           "option, dans une approche globale")
    retirer_ph(s, 1)
    fils = [
        ("Les personnes", [
            ("Engager", "L'engagement du sponsor se construit dès le cadrage ; la restitution "
             "revient aux interviewés."),
            ("Expérimenter", "Équipes pilotes volontaires, jamais désignées ; formation sur "
             "les cas réels — pas de formation sans coaching."),
            ("Outiller et relayer", "Les résistances sont un signal ; des relais internes "
             "formés prennent le relais."),
            ("Mesurer", "Satisfaction et adhésion au même instrument qu'au T0 : le delta "
             "humain à côté du delta de maturité.")]),
        ("La technique", [
            ("Cartographier", "Dette, plateformes vieillissantes, dépendances : une base "
             "factuelle partagée."),
            ("Décommissionner et observer", "Sur les pilotes, ce qui peut être "
             "décommissionné l'est ; l'observabilité du reste est posée."),
            ("Standardiser et outiller", "CI/CD et infra as code deviennent le mode par "
             "défaut."),
            ("Mesurer et réengager", "Dette et indicateurs infra rejoués au même instrument "
             "qu'au T0.")]),
    ]
    # exemples de livrables : repris de la trajectoire d'accompagnement de la
    # soutenance SGRF (Documents/SG, p. 24), transposés aux quatre phases
    livrables = [
        ["Rapport de diagnostic flash, découpé en thèmes", "Backlog priorisé et plan de "
         "déploiement"],
        ["Référentiel product management V0 adapté", "Dispositif et rituels de pilotage"],
        ["Premiers enseignements terrain", "Board des dépendances, health checks d'équipe"],
        ["Tableau de bord de suivi de la transformation", "Bilan, plan de pérennisation et "
         "de passation"],
    ]
    wl = 1.05
    xs = cols(4, gap=0.1, x0=X0 + wl + 0.1, w=W - wl - 0.1)
    for i, ((x, w), nom) in enumerate(zip(xs, PHASES, strict=True)):
        pilule(s, x, 1.3, w, 0.4, f"{i + 1}. {nom}", fill=ACCENT if i == 0 else NAVY,
               color=NAVY if i == 0 else WHITE, size=9.5)
    rangs = [(fils[0], 1.8, 1.04, False), (fils[1], 3.9, 1.06, True)]
    for (fil, cellules), y, h, option in rangs:
        etiquette(s, X0, y + 0.05, wl, fil)
        if option:                                 # la technique : option d'approche globale
            pilule(s, X0, y + 0.3, 0.95, 0.22, "EN OPTION", fill=TRACK, color=NAVY, size=7)
            rich(s, X0, y + 0.56, wl, 0.5, [("dans une approche globale",
                 {"size": 7.5, "italic": True, "color": MUTED})])
        for (x, w), (verbe, texte) in zip(xs, cellules, strict=True):
            c = carte(s, x, y, w, h, line=LINE if option else NAVY)
            if option:
                c.line.dash_style = MSO_LINE_DASH_STYLE.DASH
            rich(s, x + 0.1, y + 0.07, w - 0.2, h - 0.1, [
                (verbe, {"size": 9.5 if option else 10, "bold": True, "space_after": 2,
                         "color": MUTED if option else NAVY}),
                (texte, {"size": 8.5, "color": MUTED})])
    y, h = 2.94, 0.86
    etiquette(s, X0, y + 0.05, wl, "Exemples de livrables")
    for (x, w), items in zip(xs, livrables, strict=True):
        forme(s, MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h, TRACK, adj=0.08)
        rich(s, x + 0.1, y + 0.08, w - 0.2, h - 0.12,
             [[("■  ", {"size": 6, "color": NAVY}), (it, {"size": 8.5, "bold": True})]
              for it in items])


def photo_equipe(s):
    """Photo de Claude CAMUS au-dessus de son nom (source : Documents/SG, soutenance
    SGRF p. 2), recadrée en rond comme les autres portraits de la slide."""
    nom = next(sh for sh in s.shapes if sh.has_text_frame and "CAMUS" in sh.text_frame.text)
    brut = os.path.join(IMG_DIR, "_equipe_claude_camus_brut.png")
    im = Image.open(brut).convert("RGB").resize((600, 600))
    masque = Image.new("L", im.size, 0)
    ImageDraw.Draw(masque).ellipse((0, 0, 599, 599), fill=255)
    im.putalpha(masque)
    chemin = os.path.join(IMG_DIR, "equipe_claude_camus_rond.png")
    im.save(chemin)
    d = 1.2
    cx = (nom.left + nom.width / 2) / 914400
    y = nom.top / 914400 - d - 0.1
    s.shapes.add_picture(chemin, Inches(cx - d / 2), Inches(y), Inches(d), Inches(d))
    forme(s, MSO_SHAPE.OVAL, cx - d / 2, y, d, d, None, NAVY, lw=1.25)


def exemple_methode(s):
    """Exemple de réalisation (1/2) — repris du deck précédent (v2.47, slide 19)."""
    set_ph(s, 0, "Exemple de réalisation : repérer, prioriser, tenir")
    set_ph(s, 2, "Résultat : un backlog de problématiques priorisé, un porteur par ligne et "
           "un delta mesuré avant de généraliser")
    retirer_ph(s, 1)
    etapes = [
        ("Repérer et chiffrer", "On détecte chaque problématique et on la quantifie, preuves "
         "à l'appui.",
         ["Ouvre ses données — CMDB, facturation, tickets — et nomme ce qui le gêne vraiment.",
          "Apporte la grille des 8 familles de douleur et la méthode de quantification.",
          "Le périmètre mesuré, et ce qu'on accepte d'appeler problématique."]),
        ("Prioriser dans un backlog", "Chaque problématique reçoit un score et prend sa place "
         "dans le backlog.",
         ["Arbitre ce qu'aucune équipe ne tranche seule : fermer, standardiser, "
          "décommissionner.",
          "Instruit les causes racines et propose le score — une proposition, jamais un "
          "verdict.",
          "Le backlog priorisé et, pour chaque ligne, le porteur nommé."]),
        ("Tenir dans la durée", "On expérimente, on mesure le delta réel, puis on "
         "industrialise.",
         ["Porte les expérimentations et libère le temps qu'elles demandent.",
          "Outille, mesure le delta réel et industrialise ce qui a marché.",
          "Le seuil au-delà duquel on généralise — ou on arrête."]),
    ]
    roles = [("CÔTÉ CLIENT", TRACK, NAVY), ("CÔTÉ OCTO", NAVY, WHITE),
             ("TRANCHÉ ENSEMBLE", ACCENT, NAVY)]
    for i, ((x, w), (nom, desc, lignes)) in enumerate(zip(cols(3, gap=0.1), etapes,
                                                          strict=True)):
        chevron(s, x, 1.35, w + (0.12 if i < 2 else 0), 0.48, f"{i + 1}. {nom}",
                accent=i == 0, size=10)
        cx, cw = x + 0.05, w - 0.1
        carte(s, cx, 1.95, cw, YB - 1.95, line=NAVY if i == 0 else LINE)
        rich(s, cx + 0.14, 2.05, cw - 0.28, 0.42, [(desc, {"size": 9.5, "bold": True})])
        for k, ((lab, fill, coul), texte) in enumerate(zip(roles, lignes, strict=True)):
            y = 2.55 + k * 0.8
            pilule(s, cx + 0.14, y, 0.07 * len(lab) + 0.3, 0.22, lab, fill=fill,
                   color=coul, size=7.5)
            rich(s, cx + 0.14, y + 0.27, cw - 0.28, 0.5, [(texte, {"size": 9})])


def exemple_agents(s):
    """Exemple de réalisation (2/2) — repris du deck précédent (v2.47, slide 27)."""
    set_ph(s, 0, "Exemples de réalisation : trois agents, un par problématique")
    set_ph(s, 2, "La problématique d'abord, l'IA ensuite — exemples illustratifs, soumis au "
           "scoring et au gate de confidentialité")
    retirer_ph(s, 1)
    agents = [
        ("RUN", "Agent de triage de tickets",
         "Les mêmes tickets reviennent depuis des années et mobilisent des seniors sur du "
         "répétitif à faible valeur.",
         "Lit chaque ticket, le classe selon un runbook déjà documenté, le route vers la "
         "bonne équipe. Le processus est écrit AVANT l'agent.",
         "Jusqu'à 15 tickets/mois sans intervention humaine, temps de triage divisé par deux "
         "(cas nominal du cadrage)."),
        ("Financier", "Agent de veille FinOps",
         "Les ressources cloud surdimensionnées ou orphelines n'apparaissent qu'aux audits "
         "ponctuels.",
         "Scanne en continu la CMDB et la facturation, repère l'inactif et le surdimensionné, "
         "propose une liste à valider — ne décommissionne jamais seul.",
         "Coût récupéré directement mesurable — un indicateur de mission déjà cadré."),
        ("Cognitif", "Agent documentaire",
         "Trop d'outils, des procédures dispersées : retrouver l'information sollicite "
         "toujours les mêmes experts.",
         "Indexe runbooks, wikis et tickets résolus, répond aux questions fréquentes avec la "
         "source citée — jamais de réponse sans preuve.",
         "Charge cognitive réduite, onboarding plus rapide, moins d'interruptions des "
         "experts."),
    ]
    y0 = 1.45
    for i, ((x, w), (fam, nom, pq, fait, gain)) in enumerate(zip(cols(3, gap=0.22), agents,
                                                                 strict=True)):
        carte(s, x, y0, w, YB - y0, line=NAVY if i == 0 else LINE)
        pilule(s, x + 0.15, y0 - 0.13, 0.08 * len(fam) + 0.7, 0.26,
               f"Famille {fam}", fill=ACCENT if i == 0 else NAVY,
               color=NAVY if i == 0 else WHITE, size=8)
        rich(s, x + 0.15, y0 + 0.22, w - 0.3, 0.3, [(nom, {"size": 11.5, "bold": True})])
        blocs = [("Pourquoi", pq, 0.62), ("Ce que fait l'agent", fait, 0.92),
                 ("Gain", gain, 0.6)]
        y = y0 + 0.6
        for lab, texte, h in blocs:
            etiquette(s, x + 0.15, y, w - 0.3, lab)
            rich(s, x + 0.15, y + 0.2, w - 0.3, h, [(texte, {"size": 9,
                 "bold": lab == "Gain"})])
            y += h + 0.28


def dispositif(s):
    s.shapes.title.text = "Le dispositif"
    wl = 3.0
    forme(s, MSO_SHAPE.ROUND_2_DIAG_RECTANGLE, X0, 1.25, wl, YB - 1.25, NAVY, adj=0.12)
    rich(s, X0 + 0.25, 1.45, wl - 0.5, YB - 1.65, [
        ("NOTRE APPROCHE", {"size": 8, "bold": True, "color": WHITE, "space_after": 6}),
        ("Un dispositif resserré, qui se rend dispensable.", {"size": 14, "bold": True,
         "color": WHITE, "space_after": 10}),
        ("Un noyau OCTO, des experts mobilisés au bon moment et un transfert continu : la "
         "réussite se mesure au jour où vos équipes tiennent le modèle sans nous.",
         {"size": 10, "color": WHITE, "space_after": 10}),
        ("Dimensionnement à compléter selon le périmètre retenu.",
         {"size": 9, "italic": True, "color": WHITE})])
    xr = X0 + wl + 0.35
    wr = XR - xr
    roles = [
        ("CP", "Coach produit / plateforme", "Porte la démarche, anime les rituels, "
         "accompagne les propriétaires produit."),
        ("EP", "Expert plateforme et infrastructure", "Diagnostic du parc, catalogue de "
         "capacités, automatisation."),
        ("IA", "Expert IA", "Outille le triage et l'exploration, toujours après le gate de "
         "confidentialité."),
    ]
    h, gap, y0 = 0.72, 0.12, 1.25
    for i, (ini, t, c) in enumerate(roles):
        y = y0 + i * (h + gap)
        carte(s, xr + 0.3, y, wr - 0.3, h, line=NAVY if i == 0 else LINE)
        badge(s, xr + 0.3, y + h / 2, 0.56, ini, accent=i == 0, size=10)
        rich(s, xr + 0.72, y, wr - 0.85, h, [(t, {"size": 11, "bold": True,
             "space_after": 2}), (c, {"size": 9.5, "color": MUTED})],
             anchor=MSO_ANCHOR.MIDDLE)
    yc = y0 + 3 * (h + gap) + 0.12
    carte(s, xr, yc, wr, YB - yc, line=NAVY)
    pilule(s, xr + 0.2, yc - 0.13, 1.2, 0.26, "CÔTÉ CLIENT", fill=TRACK, color=NAVY,
           size=8)
    rich(s, xr + 0.2, yc + 0.1, wr - 0.4, YB - yc - 0.15, [gras(
        "Un sponsor (DSI ou direction infrastructure), des propriétaires produit désignés, "
        "les équipes infra et applicatives.", "des propriétaires produit désignés", size=10)],
        anchor=MSO_ANCHOR.MIDDLE)


def prix(s):
    s.shapes.title.text = "Le prix"
    x, y, w, h = X0 + 0.2, 1.35, W - 0.4, 3.3
    xs = x + 3.3                                      # perforation du ticket
    carte(s, x, y, w, h, line=NAVY, lw=1.5)
    for cy, haut in ((y, True), (y + h, False)):      # encoches du ticket
        forme(s, MSO_SHAPE.OVAL, xs - 0.16, cy - 0.16, 0.32, 0.32, WHITE, NAVY, 1.5)
        forme(s, MSO_SHAPE.RECTANGLE, xs - 0.2, cy - 0.2 if haut else cy, 0.4, 0.2, WHITE)
    for k in range(12):
        forme(s, MSO_SHAPE.RECTANGLE, xs - 0.006, y + 0.3 + k * 0.23, 0.012, 0.12, LINE)
    rich(s, x + 0.3, y + 0.3, 2.75, h - 0.6, [
        ("UN PRIX EN DEUX TEMPS", {"size": 8, "bold": True, "color": MUTED,
         "space_after": 6}),
        ("On chiffre d'abord, on s'engage ensuite.", {"size": 15, "bold": True,
         "space_after": 12}),
        gras("Financé sur une ligne budgétaire transformation, jamais sur le budget RUN.",
             "jamais sur le budget RUN", size=10)])
    offres = [
        ("Assessment flash", "Forfait d'entrée : diagnostic et coût du statu quo chiffré."),
        ("Trajectoire", "Cadrer l'offre, assainir, transformer — dimensionnée à l'issue de "
         "l'Assessment flash."),
    ]
    for i, (t, c) in enumerate(offres):
        yy = y + 0.35 + i * 1.45
        badge(s, xs + 0.6, yy + 0.3, 0.5, f"{i + 1}", accent=i == 0, size=13)
        rich(s, xs + 1.0, yy, x + w - xs - 1.3, 0.62, [
            (t, {"size": 13, "bold": True, "space_after": 2}),
            (c, {"size": 9.5, "color": MUTED})])
        pilule(s, xs + 1.0, yy + 0.8, 2.3, 0.32, "Montant : à compléter", fill=TRACK,
               color=NAVY, size=9.5)


REMPLACEMENTS = [  # pas de « gaspillage » dans le deck (commit 94b04ff)
    ("Assainir et travailler le gaspillage", "Assainir et traiter les problématiques"),
    ("Traiter le gaspillage avant de construire", "Traiter les douleurs avant de construire"),
]


# ---------------------------------------------------------------- assemblage
def construire():
    prs = Presentation(SOURCE)
    sld = prs.slides._sldIdLst
    S = list(prs.slides)                      # index = n° de slide SOURCE - 1
    ids = list(sld)
    src = lambda n: S[n - 1]  # noqa: E731

    couverture(src(1))
    executive_summary(src(3))
    problematiques(src(5))
    situations(src(6))
    apports(src(7))
    guichet_vers_produit(src(8))
    enjeux(src(9))
    alternatives(src(15))
    typologies(src(16))
    definition(src(18))
    promesse(src(19))
    bascules(src(20))
    demarche_globale(src(23))
    ia_demarche(src(24))                      # reprend le contenu de la source S21
    planning(src(25))
    demarche_detaillee(src(27))

    # chapitres renumérotés 01..07 (la source portait « 01 » partout) + photos CC0
    for num, (n, scene) in enumerate(zip((4, 14, 17, 22, 26, 28, 29), PHOTOS,
                                         strict=True), 1):
        for s in list(src(n).shapes):
            if s.has_text_frame and s.text_frame.text.strip() in ("01", "02"):
                s.text_frame.paragraphs[0].runs[0].text = f"{num:02d}"
            elif s.has_text_frame and s.text_frame.text.strip() == "Chapitre.":
                retirer(s)                    # reliquat du gabarit
        photo_chapitre(src(n), scene)

    # contenus neufs derrière « Le dispositif » et « Le prix »
    layout = next(lay for lay in prs.slide_layouts if lay.name.startswith("04 - Titre seul"))
    for apres, remplir in ((28, dispositif), (29, prix)):
        s = prs.slides.add_slide(layout)
        remplir(s)
        el = sld[-1]
        sld.remove(el)
        ids[apres - 1].addnext(el)

    # deux exemples de réalisation derrière « Démarche détaillée » (source S27)
    layout_st = next(lay for lay in prs.slide_layouts
                     if lay.name.startswith("01 - Titre, sous-titre"))
    for remplir in (exemple_agents, exemple_methode, accompagnement):   # insérés en ordre inverse
        s = prs.slides.add_slide(layout_st)
        remplir(s)
        el = sld[-1]
        sld.remove(el)
        ids[26].addnext(el)

    sommaire(prs)                             # remplace la source S2
    el = sld[-1]
    sld.remove(el)
    ids[1].addnext(el)

    # notes internes (source S30) : dans les notes du présentateur de « L'équipe »
    notes = src(30).shapes.placeholders[1].text_frame.text
    photo_equipe(src(31))
    src(31).notes_slide.notes_text_frame.text = "Personnes à contacter :\n" + notes

    # S2 sommaire vide ; S10 « Nos convictions » (demande du 2026-09-26) ;
    # doublons : S13 = S19, S21 fusionnée dans « L'IA dans la démarche » ;
    # S30 notes internes
    for n in (2, 10, 13, 21, 30):
        prs.part.drop_rel(ids[n - 1].rId)
        sld.remove(ids[n - 1])

    remplacer_partout(prs, REMPLACEMENTS)
    return prs


def main():
    prs = construire()
    defauts = []
    restes = [(i, t) for i, t in texte_deck(prs) if "gaspill" in t.lower()]
    defauts += [f"slide {i}: « gaspillage » subsiste" for i, _ in restes]
    defauts += D.verifier_geometrie(prs)
    debord = D.verifier_debordements_texte(prs, tolerance_in=0.4)
    prs.save(SORTIE)
    print(f"{len(prs.slides)} slides -> {SORTIE}")
    for d in debord:
        print("  debordement estime :", d)
    if defauts:
        print("DEFAUTS :\n  " + "\n  ".join(defauts))
        sys.exit(1)
    print("CONTROLE: OK")


if __name__ == "__main__":
    main()
