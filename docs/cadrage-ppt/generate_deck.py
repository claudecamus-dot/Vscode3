"""Génère une synthèse PPT (32 slides) des RÉSULTATS du cadrage BMAD IAP
(docs/bmad-iap-cadrage.md) à partir des helpers pptx_deck, dessinée
PAR-DESSUS le vrai template de marque OCTO (template-octo.pptx) —
masters/layouts/thème conservés, pas un deck sur canevas vierge.

Centré sur les résultats du cadrage (mission, doctrine, méthode, maturité,
ambition, KPIs, schéma de fonctionnement) plutôt que sur tout le détail de
mise en œuvre. Le commit 4f0c9b7 avait retiré ce détail d'implémentation ;
l'arbitrage utilisateur du 2026-07-21 rouvre ce périmètre sur DEUX points
précis seulement, désormais dans le deck :
  - l'architecture des 11 agents-workflows (slide_architecture_agents,
    inventaire des composants — complémentaire du schéma de flux, pas un
    doublon) ;
  - l'étude des personas / product discovery (slide_personas, réouverture de
    la discovery fusionnée en MVP1, §Décision de cadrage ligne 236).
Restent hors périmètre (toujours du support interne, pas une synthèse
exécutive) : le schéma des workflows détaillé, la roadmap MVP et les points
ouverts — les trois autres slides retirées au même commit ne sont PAS
réintroduites.

Usage : python generate_deck.py
Sortie : bmad-iap-cadrage-synthese.pptx (à côté de ce script).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import pptx_deck as D
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn

HERE = os.path.dirname(__file__)
TEMPLATE = os.path.join(HERE, "template-octo.pptx")
REPO_ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(REPO_ROOT, ".claude", "skills", "pptx-framed-image", "scripts"))
from framed_image import place_image_in_frame, frame_obstructions  # noqa: E402
import nature_images  # noqa: E402
import stock_images  # noqa: E402

IMG_DIR = os.path.join(HERE, "_img")
os.makedirs(IMG_DIR, exist_ok=True)
IMG_MANIFEST = os.path.join(HERE, "images-manifest.json")

LAYOUT_COUVERTURE = 8   # "40 - Couverture [1]" — idx0 titre, idx1 sous-titre, idx2/idx3 crédit+date
LAYOUT_TITRE_SEUL = 5   # "04 - Titre seul" — idx0 titre, garde logo/pied de page/n° de slide
LAYOUT_VIDE = 0         # "06 - Slide vide" — pas de placeholder, juste logo + badge de pagination
LAYOUT_CHAPITRE = 2     # "50 - Chapitre [1]" — idx0 titre (grand), idx1 numéro ; cadre photo teardrop
LAYOUT_VISUEL_DROITE = 15  # "63 - Titre, contenu et visuel à droite - cadre blanc"

# --- Géométrie du template OCTO réel (10 x 5.625 in, 16:9) — cf.
# docs/vscode1-export/template-octo.md §4-5, vérifiée localement contre
# template-octo.pptx (mêmes dims/layouts/thème). Contenu dessiné dans la
# zone de contenu du layout « Titre seul » (sous le titre, au-dessus du
# pied de page), marge gauche alignée sur le placeholder titre (0.615 in),
# marge droite plafonnée avant le badge de pagination bas-droit.
SLIDE_W, SLIDE_H = 10.0, 5.625
MARGIN = 0.615
BORD_DROIT = 9.15
CONTENT_TOP = 1.15
CONTENT_BOTTOM = 5.45
CONTENT_W = BORD_DROIT - MARGIN
CONTENT_H = CONTENT_BOTTOM - CONTENT_TOP
GAP = 0.2

TH = D.theme_colors(Presentation(TEMPLATE))
NAVY = TH.get("dk1", D.INK)          # #0E2356 — texte principal, titres
WHITE = TH.get("lt1", "#FFFFFF")
ACCENT = TH.get("accent3", D.PALETTE[0])   # #00D2DD — cyan OCTO, identité du deck
MUTED = TH.get("lt2", D.MUTED)       # #586586 — slate 600, texte secondaire
LINE = TH.get("accent5", D.LINE)     # #CFD3DD — slate 200, bordures de cards
TRACK = TH.get("accent6", D.TRACK)   # #E7E9EE — slate 100, fonds d'encarts

SEVERITE = ["#1e6b34", "#5b8a3c", "#b8860b", "#c1651e", "#b3261e"]  # D0..D4, vert -> rouge


def _rgb(hexcolor):
    return RGBColor.from_string(hexcolor.lstrip("#").upper())


def new_prs():
    prs = Presentation(TEMPLATE)
    # Retire les 9 slides d'exemple du template — masters/layouts/thème conservés.
    # Il faut aussi supprimer la relation (drop_rel), sinon les parties
    # ppt/slides/slideN.xml orphelines entrent en collision de nom avec les
    # nouvelles slides ajoutées ensuite (même numérotation réutilisée).
    xml_slides = prs.slides._sldIdLst
    for sld in list(xml_slides):
        rId = sld.get(D.qn("r:id"))
        prs.part.drop_rel(rId)
        xml_slides.remove(sld)
    return prs


# Couleur de chapitre par groupe de slides — signal de navigation plus fort
# que le seul kicker textuel (piste retenue dans analyse-template-alternatif.md).
# Cadrage/Méthode/Trajectoire reprennent les mêmes 3 couleurs déjà utilisées
# sur la slide Executive summary (D.PALETTE[0]/[1]/[3]) — pas une palette de
# plus à mémoriser ; passées explicitement à chaque appel de content_slide().


def content_slide(prs, kicker, title, color=None):
    layout = prs.slide_masters[0].slide_layouts[LAYOUT_TITRE_SEUL]
    s = prs.slides.add_slide(layout)
    ph = s.shapes.placeholders[0]
    box_w = Emu(ph.width).inches
    kicker_color = color or ACCENT
    texte_complet = f"{kicker.upper()}   ·   {title}"
    taille, _ = D.ajuster_police([texte_complet], box_w, 17, 12,
                                  lambda t, lignes_max: lignes_max <= 1)
    tf = ph.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    r1 = p.add_run()
    r1.text = kicker.upper() + "   ·   "
    r1.font.bold = True
    r1.font.size = Pt(taille)
    r1.font.color.rgb = _rgb(kicker_color)
    r2 = p.add_run()
    r2.text = title
    r2.font.bold = True
    r2.font.size = Pt(taille)
    r2.font.color.rgb = _rgb(NAVY)
    return s


def _sans_puce(paragraph):
    """Retire l'indentation de puce héritée (marL/indent) et désactive le
    caractère de puce. Cause réelle du bug "01" qui passe à la ligne dans le
    petit encart numéro du layout Chapitre : son style de liste hérité pose
    marL=0.5in (indentation de puce) dans un encart large de 0.546in — il ne
    reste presque plus de largeur utile, donc chaque caractère wrap. Le REX
    V3 (VSCode1) corrige exactement ça avec un pPr marL=0/indent=0/buNone
    explicite ; python-pptx n'expose pas ces attributs, d'où la manipulation
    XML directe."""
    pPr = paragraph._p.get_or_add_pPr()
    pPr.set("marL", "0")
    pPr.set("indent", "0")
    for tag in ("a:buChar", "a:buAutoNum", "a:buNone"):
        for el in pPr.findall(qn(tag)):
            pPr.remove(el)
    pPr.append(pPr.makeelement(qn("a:buNone"), {}))


def _find_frame_by_geom(shapes, prst):
    """Cadre non groupé (top-level) portant un prstGeom donné — variante de
    pptx-framed-image.frame_geometry pour le cas où le cadre n'est pas niché
    dans un groupe (le layout Chapitre du template, à la différence des
    layouts « cadre blanc », place son cadre teardrop directement)."""
    for sh in shapes:
        spPr = getattr(sh._element, "spPr", None)
        if spPr is None:
            continue
        g = spPr.find(qn("a:prstGeom"))
        if g is not None and g.get("prst") == prst:
            return sh.left, sh.top, sh.width, sh.height, g
    return None


def _find_frame_in_group(shapes, group_name, inner_name):
    from framed_image import frame_geometry
    for sh in shapes:
        if sh.name == group_name:
            return frame_geometry(sh, inner_name)
    return None


# scene -> requête Openverse (photo réelle) ; la génération procédurale
# (nature_images) reste le nom de "scene" utilisé comme repli hors-ligne.
_REQUETES_PHOTO = {
    "mountains": "mountains landscape",
    "forest": "green forest sunlight",
    # Littoral rocheux turquoise (chapitre 03) : « ocean waves aerial » (horizon
    # brumeux délavé en blanc) puis « turquoise sea water aerial » (0 résultat
    # Openverse -> repli procédural à ciel pâle) échouaient tous deux à ancrer le
    # haut du cadre teardrop sur le fond blanc de la slide. « turquoise water »
    # (seed 0) renvoie une vue plongeante roche+eau+écume, texturée et contrastée
    # sur les quatre bords — VÉRIFIÉE au rendu réel le 2026-07-21.
    "ocean": "turquoise water",
    "sunset": "sunset sky",
}


def _remplir_cadre(slide, cadre, scene, seed=0):
    """Pose une vraie photo libre de droit (Openverse, CC0) à l'aspect exact
    du cadre, repli sur la génération procédurale (nature_images) si le
    réseau/l'API n'est pas disponible — cf. pptx-framed-image, greffé depuis
    VSCode1. Une photo réelle lit mieux qu'un aplat vectoriel généré, constat
    fait en comparant au REX "⛱️ L'Été de l'IA" (VSCode1) qui utilise de
    vraies photos sur ces mêmes cadres."""
    if cadre is None:
        print(f"  cadre introuvable pour la scène '{scene}' — image non posée")
        return
    left, top, width, height, geom = cadre
    aspect = Emu(width).inches / Emu(height).inches
    px_w = 960
    px_h = int(round(px_w / aspect))
    path = os.path.join(IMG_DIR, f"{scene}_{seed}_{px_w}x{px_h}.png")
    if not os.path.exists(path):
        requete = _REQUETES_PHOTO.get(scene, scene)
        aspect_ratio = "wide" if aspect > 1.15 else "tall" if aspect < 0.85 else "square"
        try:
            brut = os.path.join(IMG_DIR, f"_brut_{scene}_{seed}.jpg")
            stock_images.fetch_to(brut, requete, seed=seed, aspect_ratio=aspect_ratio,
                                   manifest_path=IMG_MANIFEST)
            from framed_image import cover_crop_to_aspect
            cover_crop_to_aspect(brut, path, aspect)
            print(f"  photo réelle posée pour '{scene}' ({requete!r}, via Openverse CC0)")
        except Exception as e:
            print(f"  Openverse indisponible pour '{scene}' ({e}) — repli sur nature_images")
            nature_images.generate_to(path, scene, px_w, px_h, seed=seed)
    place_image_in_frame(slide, path, left, top, width, height, geom=geom)


def slide_chapitre(prs, numero, titre, couverture, color, scene, seed=0):
    """Slide d'intercalaire de chapitre — vrai layout dédié du template
    (« 50 - Chapitre [1] »), repris tel qu'utilisé dans le REX
    "⛱️ L'Été de l'IA" (VSCode1) : cadre photo teardrop rempli (pas laissé
    vide), numéro à 17pt (pas la taille par défaut d'un texte de titre — un
    premier essai à 28pt débordait du petit encart sur le badge logo voisin,
    trouvé au rendu, cf. mémoire de session). Couleur de chapitre appliquée
    au numéro et au titre — le REX source ne le faisait pas, ajouté ici pour
    rester cohérent avec le code couleur déjà en place sur tout le deck."""
    layout = prs.slide_masters[0].slide_layouts[LAYOUT_CHAPITRE]
    s = prs.slides.add_slide(layout)
    phs = {ph.placeholder_format.idx: ph for ph in s.placeholders}

    phs[0].text_frame.text = titre
    p2 = phs[0].text_frame.add_paragraph()
    p2.text = couverture
    for r in p2.runs:
        r.font.size = Pt(D.TYPE["small"])
        r.font.italic = True
        r.font.color.rgb = _rgb(MUTED)
    for p in phs[0].text_frame.paragraphs[:1]:
        for r in p.runs:
            r.font.color.rgb = _rgb(color)

    tf1 = phs[1].text_frame
    tf1.text = numero
    # Marges par défaut (~0.1in/côté) mangent la largeur du minuscule encart
    # (0.55in) et forcent "01" à passer à la ligne — invisible tant qu'on ne
    # zéroute pas les marges comme le fait l'exemple qui fonctionne (REX V3).
    tf1.margin_left = tf1.margin_right = tf1.margin_top = tf1.margin_bottom = 0
    tf1.vertical_anchor = MSO_ANCHOR.MIDDLE
    for p in tf1.paragraphs:
        p.alignment = PP_ALIGN.CENTER
        _sans_puce(p)
        for r in p.runs:
            r.font.size = Pt(17)
            r.font.color.rgb = _rgb(color)

    cadre = _find_frame_by_geom(s.slide_layout.shapes, "teardrop")
    for pb in frame_obstructions(s, *cadre[:4]) if cadre else []:
        print(f"  [obstruction] chapitre {numero}:", pb["source"], pb["name"], pb["reason"])
    _remplir_cadre(s, cadre, scene, seed)
    return s


def dot_scale(slide, x, y, n, score, color, d=0.14, gap=0.06, empty_color=None):
    """Jauge à points 0..n (score plein en `color`, reste en `empty_color`) —
    pattern repris de la carte de recommandation valeur/complexité observée
    dans l'autre template analysé (analyse-template-alternatif.md §4)."""
    empty_color = empty_color or TRACK
    for i in range(n):
        fill = color if i < score else empty_color
        D.add_dot(slide, x + i * (d + gap), y, d, fill)


def col_x(i, n, w=CONTENT_W, x0=MARGIN, gap=GAP):
    col_w = (w - (n - 1) * gap) / n
    return x0 + i * (col_w + gap), col_w


def chip(slide, x, y, w, h, label, color, text_color="#ffffff", size=D.TYPE["tiny"]):
    D.add_rect(slide, x, y, w, h, fill=color, rounded=True, radius=0.5)
    D.add_text(slide, x, y, w, h, [(label, dict(size=size, bold=True, color=text_color,
                align=PP_ALIGN.CENTER))], anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)


# Le glyphe "⟲" (U+27F2) n'a pas de variante GRASSE dans la police du template
# (rendu LibreOffice = case vide/tofu dans un run bold) alors que sa variante
# normale s'affiche — même correctif que slide_trajectoire/slide_schema_*
# /slide_livrables_ppt : forcer bold=False pour ce SEUL caractère. Voir
# CLAUDE.md §docs/cadrage-ppt.
_GLYPHES_SANS_GRAS = ("⟲",)


def _header_cell(slide, x, y, w, h, label, size=7, color=MUTED, bold=True,
                 anchor=MSO_ANCHOR.TOP):
    """En-tête de colonne en un seul paragraphe multi-runs : chaque caractère de
    `_GLYPHES_SANS_GRAS` est posé en bold=False même si le libellé est en gras,
    pour éviter le tofu du "⟲" en fonte grasse (cf. _GLYPHES_SANS_GRAS)."""
    import re as _re
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    for m in ("margin_left", "margin_right", "margin_top", "margin_bottom"):
        setattr(tf, m, 0)
    p = tf.paragraphs[0]
    motif = "(" + "|".join(_re.escape(g) for g in _GLYPHES_SANS_GRAS) + ")"
    for part in _re.split(motif, label):
        if not part:
            continue
        r = p.add_run()
        r.text = part
        r.font.size = Pt(size)
        r.font.bold = bool(bold) and part not in _GLYPHES_SANS_GRAS
        r.font.color.rgb = _rgb(color)
    return box


def _lignes(texte, largeur_in, taille_pt):
    """Nombre de lignes estimé pour `texte` (helper de dimensionnement des
    panneaux à la hauteur de leur contenu — cf. « panneau sur-étiré »)."""
    return max(1, D.estimer_lignes(texte, largeur_in, taille_pt))


# ---------------------------------------------------------------- slide 1
def slide_cover(prs):
    layout = prs.slide_masters[0].slide_layouts[LAYOUT_COUVERTURE]
    s = prs.slides.add_slide(layout)
    phs = {ph.placeholder_format.idx: ph for ph in s.placeholders}
    phs[0].text_frame.text = "BMAD IAP"
    phs[1].text_frame.text = "Infra as a Product Transformation Pack — synthèse de cadrage"
    phs[2].text_frame.text = "OCTO Technology"
    phs[3].text_frame.text = "v2.0 · 2026-07-15"

    # Bandeau de métadonnées sous la zone de couverture du template, dans la
    # bande basse encore libre (le pied de page/logo du master restent visibles).
    metas = [
        ("STATUT", "Draft consolidé v2.0"),
        ("LANGUE", "FR"),
        ("CONFIDENTIALITÉ", "Client-data-first"),
        ("SOURCES", "Grille Assessment V3.2 · Interview-to-Deck"),
    ]
    n = len(metas)
    y = 4.55
    for i, (k, v) in enumerate(metas):
        x, w = col_x(i, n, w=CONTENT_W, x0=MARGIN)
        D.add_text(s, x, y, w, 0.55, [
            (k, dict(size=D.TYPE["tiny"], bold=True, color=NAVY)),
            (v, dict(size=D.TYPE["tiny"], color=MUTED, space_before=2, line_spacing=1.1)),
        ])
    return s


# ---------------------------------------------------------------- slide 2
def slide_executive_summary(prs):
    s = content_slide(prs, "Executive summary", "Une transformation à deux piliers, cadrée et mesurable")

    headline_h = 0.85
    D.add_text(s, MARGIN, CONTENT_TOP, CONTENT_W, headline_h, [
        ("Transformer l'infrastructure en plateforme opérée comme un produit, ET traiter "
         "structurellement le gaspillage qui l'en empêche — deux piliers non séquentiels, "
         "cadrés par une doctrine non négociable et mesurés par des KPIs dédiés.",
         dict(size=D.TYPE["small"], color=NAVY, italic=True, line_spacing=1.3)),
    ])

    items = [
        ("Doctrine", D.PALETTE[0],
         "Gate IA non négociable : checkpoint humain systématique sur toute donnée client, "
         "quel que soit le mode d'exécution IA retenu."),
        ("Méthode", D.PALETTE[1],
         "Gaspillage traité avec un score explicite (impact × faisabilité − prudence IA) ; "
         "modèles d'équipe Team Topologies étendus aux agents IA, mandat écrit avant délégation."),
        ("Maturité", D.PALETTE[3],
         "Deux échelles jamais confondues : maturité IA client (M0-M4) et grille produit/"
         "plateforme V3.2 — chacune sa lecture, son usage."),
        ("Posture", D.PALETTE[2],
         "Niveau d'ambition A (aide au coach) assumé aujourd'hui — un choix de gouvernance, "
         "pas une limite technique subie, mesuré par 3 familles de KPIs distinctes."),
    ]
    n = len(items)
    pad = 0.18
    _, cw = col_x(0, n)
    usable = cw - 2 * pad
    desc_size = 8
    line_h = desc_size * 1.3 / 72.0
    # Hauteur de carte PLAFONNÉE au contenu (max de descriptions) au lieu de
    # CONTENT_BOTTOM - top0 : sinon la carte s'étire et laisse un grand vide
    # sous le texte (défaut « panneau sur-étiré », cf. brief ppt-designer).
    desc_lines = max(_lignes(desc, usable, desc_size) for _, _, desc in items)
    card_h = 0.65 + desc_lines * line_h + 0.22
    region_top = CONTENT_TOP + headline_h + 0.3
    # bande de cartes plaquée sous le chapeau, gap plafonné pour ne pas creuser
    # un vide sous le chapeau ; le reste tombe en marge basse propre.
    top0 = region_top + min(0.35, max(0.0, (CONTENT_BOTTOM - region_top - card_h) / 2))
    for i, (titre, color, desc) in enumerate(items):
        x, w = col_x(i, n)
        D.add_card(s, x, top0, w, card_h, color)
        D.add_text(s, x + pad, top0 + 0.18, w - 2 * pad, 0.4, [
            (titre, dict(size=D.TYPE["h3"], bold=True, color=color)),
        ])
        D.add_text(s, x + pad, top0 + 0.65, w - 2 * pad, card_h - 0.8, [
            (desc, dict(size=desc_size, color=NAVY, line_spacing=1.28)),
        ])
    return s


# ---------------------------------------------------------------- slide 3
def slide_mission(prs):
    s = content_slide(prs, "Cadrage", "Une double mission : transformer ET assainir", color=D.PALETTE[0])
    cards = [
        ("TRANSFORMER", D.PALETTE[0],
         "Cible produit/plateforme : utilisateurs identifiés, valeur, roadmap, "
         "engagements de qualité, gouvernance lisible.",
         "La vision à moyen terme — ce que le sponsor achète."),
        ("ASSAINIR", D.PALETTE[2],
         "Traitement mesurable des gaspillages : flux, RUN, humain, financier, "
         "cognitif, décisionnel, environnemental, IA.",
         "La capacité récupérée qui finance la trajectoire produit."),
    ]
    card_h = 1.75
    top0 = CONTENT_TOP + 0.5
    for i, (titre, color, vise, finance) in enumerate(cards):
        x, w = col_x(i, 2)
        D.add_card(s, x, top0, w, card_h, color)
        pad = 0.22
        D.add_text(s, x + pad, top0 + 0.15, w - 2 * pad, 0.3, [
            (titre, dict(size=D.TYPE["h3"], bold=True, color=color))
        ])
        D.add_text(s, x + pad, top0 + 0.5, w - 2 * pad, 0.6, [
            ("CE QU'IL VISE", dict(size=D.TYPE["tiny"], bold=True, color=MUTED)),
            (vise, dict(size=D.TYPE["tiny"], color=NAVY, space_before=2, line_spacing=1.2)),
        ])
        D.add_text(s, x + pad, top0 + 1.15, w - 2 * pad, 0.55, [
            ("CE QU'IL FINANCE", dict(size=D.TYPE["tiny"], bold=True, color=MUTED)),
            (finance, dict(size=D.TYPE["tiny"], color=NAVY, space_before=2, line_spacing=1.2)),
        ])

    note_top = top0 + card_h + 0.2
    D.add_text(s, MARGIN, note_top, CONTENT_W, 0.55, [
        ("Les deux piliers ne sont ni séquentiels ni optionnels l'un par rapport à "
         "l'autre : une cible produit sans traitement du gaspillage manque de "
         "capacité pour s'y déployer ; l'inverse reste une réduction de coûts sans vision.",
         dict(size=D.TYPE["tiny"], color=MUTED, italic=True, line_spacing=1.25)),
    ])

    tens_top = note_top + 0.62
    tens_h = 0.62
    tensions = ["Efficacité du delivery", "Robustesse du RUN", "Valeur perçue (utilisateurs internes)"]
    for i, t in enumerate(tensions):
        x, w = col_x(i, 3)
        D.add_rect(s, x, tens_top, w, tens_h, fill=TRACK, rounded=True, radius=0.12)
        D.add_text(s, x + 0.1, tens_top, w - 0.2, tens_h, [
            (t, dict(size=D.TYPE["tiny"], bold=True, color=NAVY, align=PP_ALIGN.CENTER))
        ], anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
    return s


# ---------------------------------------------------------------- slide 4
def slide_gate_ia(prs):
    s = content_slide(prs, "Cadrage", "Les données du client gouvernent le choix du modèle IA", color=D.PALETTE[0])
    D.add_text(s, MARGIN, CONTENT_TOP, CONTENT_W, 0.35, [
        ("Checkpoint toujours humain avant tout usage IA sur données client — "
         "iap-ai-data-confidentiality-gate, quel que soit le mode (ADR-006 OpenHub).",
         dict(size=D.TYPE["tiny"], color=MUTED, line_spacing=1.2)),
    ])
    rows = [
        ("D0", "Public", "Articles publics, docs méthodo", "IA externe possible"),
        ("D1", "Interne", "Organisation macro, catalogue anonymisé", "IA client recommandée"),
        ("D2", "Confidentiel", "Notes d'interview, reporting, portefeuille", "IA client ou LLM privé"),
        ("D3", "Restreint", "Tickets détaillés, logs, CMDB, IAM", "LLM local, contrôles forts"),
        ("D4", "Critique", "Secrets de production, données réglementées", "Local/on-prem, sans IA générative"),
    ]
    row_top = CONTENT_TOP + 0.45
    row_h = 0.62
    row_gap = 0.1
    label_w = 1.35
    desc_w = 4.2
    usage_w = CONTENT_W - label_w - desc_w - 2 * 0.2
    for i, (code, nom, exemples, usage) in enumerate(rows):
        y = row_top + i * (row_h + row_gap)
        chip(s, MARGIN, y, label_w, row_h, f"{code} · {nom}", SEVERITE[i], size=D.TYPE["tiny"])
        D.add_text(s, MARGIN + label_w + 0.2, y, desc_w, row_h, [
            (exemples, dict(size=D.TYPE["tiny"], color=NAVY, line_spacing=1.1)),
        ], anchor=MSO_ANCHOR.MIDDLE)
        D.add_text(s, MARGIN + label_w + 0.2 + desc_w + 0.2, y, usage_w, row_h, [
            (usage, dict(size=D.TYPE["tiny"], color=MUTED, italic=True, line_spacing=1.1)),
        ], anchor=MSO_ANCHOR.MIDDLE)
    return s


# ---------------------------------------------------------------- slide 5
def slide_maturite(prs):
    s = content_slide(prs, "Cadrage", "Deux échelles de maturité, jamais confondues", color=D.PALETTE[0])
    x0, w0 = col_x(0, 2)
    x1, w1 = col_x(1, 2)

    D.add_text(s, x0, CONTENT_TOP, w0, 0.3, [
        ("MATURITÉ IA CLIENT (M0–M4)", dict(size=D.TYPE["tiny"], bold=True, color=NAVY))
    ])
    niveaux = [
        ("M0", "Pas d'IA interne utilisable", "Méthodo générique, données anonymisées"),
        ("M1", "IA interne basique", "Synthèses internes, pas d'analyse critique auto"),
        ("M2", "IA privée avec RAG", "Diagnostic documentaire, consolidation"),
        ("M3", "Plateforme IA gouvernée", "Workflows agentic contrôlés"),
        ("M4", "IA industrielle", "Agents spécialisés à fort volume, contrôle humain"),
    ]
    row_top = CONTENT_TOP + 0.4
    row_h = 0.72
    row_gap = 0.06
    for i, (code, titre, strat) in enumerate(niveaux):
        y = row_top + i * (row_h + row_gap)
        chip(s, x0, y, 0.62, row_h, code, D.PALETTE[0], size=D.TYPE["tiny"])
        D.add_text(s, x0 + 0.62 + 0.15, y, w0 - 0.77 - 0.15, row_h, [
            (titre, dict(size=D.TYPE["tiny"], bold=True, color=NAVY)),
            (strat, dict(size=8, color=MUTED, space_before=1, line_spacing=1.1)),
        ], anchor=MSO_ANCHOR.MIDDLE)

    D.add_text(s, x1, CONTENT_TOP, w1, 0.3, [
        ("MATURITÉ PRODUIT / PLATEFORME (grille V3.2)", dict(size=D.TYPE["tiny"], bold=True, color=NAVY))
    ])
    piliers = [
        ("Équipe Produit", "Adjacent", False),
        ("Excellence Technique", "Cœur du périmètre", True),
        ("Culture de l'Entreprise Agile", "Adjacent", False),
        ("Agilité à l'Échelle", "Cœur du périmètre", True),
        ("IA, Agentic et Organisation Augmentée", "Remplace le M0–M4", True),
    ]
    for i, (nom, badge, coeur) in enumerate(piliers):
        y = row_top + i * (row_h + row_gap)
        color = D.couleur_pilier(i)
        D.add_dot(s, x1, y + row_h / 2 - 0.07, 0.14, color)
        tx = x1 + 0.28
        tw = w1 - 0.28
        D.add_text(s, tx, y, tw, row_h, [
            (nom, dict(size=D.TYPE["tiny"], bold=coeur, color=NAVY, line_spacing=1.1)),
            (badge, dict(size=8, color=(color if coeur else MUTED), space_before=1)),
        ], anchor=MSO_ANCHOR.MIDDLE)
    return s


# --- Nouveau (réouverture de périmètre, arbitrage 2026-07-21) : la Product
# Discovery (personas/parcours/pain points), délibérément fusionnée dans
# iap-product-definition pour MVP1 (§Décision de cadrage, ligne 236), est
# rouverte ici en une slide dédiée. Quatre parties prenantes de la couverture
# d'interview (§Synthesis, "répartition par persona : infra/utilisateur/
# management/sponsor", ligne 457) — chacune sa voix, sa question directrice
# (reprise des questions des §Agents), son irritant, son attente. Placée en
# fin de chapitre Cadrage : on sait qui l'on transforme avant d'attaquer les
# candidats d'automatisation (slides agent IA) et la méthode (chapitre Méthode).
def slide_personas(prs):
    s = content_slide(prs, "Cadrage",
                       "Chaque persona est interrogé séparément, pour ne pas lisser un faux consensus",
                       color=D.PALETTE[0])
    D.add_text(s, MARGIN, CONTENT_TOP, CONTENT_W, 0.55, [
        ("La Product Discovery (personas, parcours, pain points) reste fusionnée dans "
         "iap-product-definition en MVP1 — mais chaque partie prenante répond à la même trame, "
         "pour révéler convergences ET divergences plutôt qu'un diagnostic monolithique.",
         dict(size=8, color=MUTED, italic=True, line_spacing=1.2)),
    ])

    personas = [
        ("Infra & RUN", "« Opérable sans sacrifier le delivery ? »", D.PALETTE[0],
         "Incidents récurrents et astreintes : les experts seniors passent leur temps sur du répétitif.",
         "Récupérer de la capacité et sortir du RUN subi."),
        ("Utilisateur applicatif", "« Pourquoi adopterais-je la plateforme ? »", D.PALETTE[5],
         "Ni self-service ni parcours conçu : tout passe par un guichet, le contournement va plus vite.",
         "Une plateforme adoptée par choix : self-service, onboarding, valeur perçue."),
        ("Management", "« Comment piloter avec un signal fiable ? »", D.PALETTE[3],
         "« Expert devenu manager malgré lui » : reporting miroir et micromanagement, faute de signal fiable.",
         "Un signal de confiance (métriques de flux), pas plus de contrôle."),
        ("Sponsor", "« Quel problème business règle-t-on ? »", D.PALETTE[4],
         "Craint une transformation cosmétique : beaucoup d'activité, peu de valeur démontrée.",
         "Un problème business réglé, une trajectoire lisible, des KPIs de mission."),
    ]
    top0 = CONTENT_TOP + 0.6
    n = len(personas)
    row_gap = 0.12
    row_h = (CONTENT_BOTTOM - top0 - (n - 1) * row_gap) / n
    name_w = 2.05
    col_gap = 0.2
    x_name = MARGIN + 0.2
    x_pain = x_name + name_w + col_gap
    txt_total = (MARGIN + CONTENT_W) - x_pain - 0.15
    colw = (txt_total - col_gap) / 2
    x_attend = x_pain + colw + col_gap
    for i, (nom, question, color, pain, attend) in enumerate(personas):
        y = top0 + i * (row_h + row_gap)
        D.add_rect(s, MARGIN, y, CONTENT_W, row_h, fill="#ffffff", line=LINE, line_w=0.75,
                   rounded=True, radius=0.08)
        D.add_rect(s, MARGIN, y, 0.06, row_h, fill=color, rounded=True, radius=0.5)
        D.add_text(s, x_name, y + 0.1, name_w, row_h - 0.2, [
            (nom, dict(size=D.TYPE["tiny"], bold=True, color=color, line_spacing=1.05)),
            (question, dict(size=7, color=MUTED, italic=True, space_before=3, line_spacing=1.1)),
        ], anchor=MSO_ANCHOR.MIDDLE)
        D.add_text(s, x_pain, y + 0.1, colw, row_h - 0.2, [
            ("IRRITANT", dict(size=7, bold=True, color=MUTED)),
            (pain, dict(size=8, color=NAVY, space_before=3, line_spacing=1.2)),
        ], anchor=MSO_ANCHOR.MIDDLE)
        D.add_text(s, x_attend, y + 0.1, colw, row_h - 0.2, [
            ("ATTENTE", dict(size=7, bold=True, color=MUTED)),
            (attend, dict(size=8, color=NAVY, space_before=3, line_spacing=1.2)),
        ], anchor=MSO_ANCHOR.MIDDLE)
    return s


# --- Nouveau (arbitrage cadrage validé) : corollaire direct de slide_personas.
# Interviewer chaque partie prenante SÉPARÉMENT (§Synthesis) n'a de sens que si
# l'on garde les divergences au lieu de les lisser en consensus — cette slide
# les rend explicites. Réutilise les couleurs d'accent persona de
# slide_personas (Infra=bleu, Utilisateur=teal, Management=or, Sponsor=violet)
# et introduit le RSSI (porteur du gate) en rouge = criticité/blocage. Le
# symbole de tension « ⟂ » du cadrage est rendu par le connecteur texte « en
# tension avec » plutôt que par le glyphe (non garanti dans la fonte du
# template, cf. _GLYPHES_SANS_GRAS) — même prudence que pour « ⟲ ». Rangées
# dimensionnées à leur contenu (pas de panneau sur-étiré).
def slide_personas_divergences(prs):
    s = content_slide(prs, "Cadrage",
                       "Interroger chaque persona séparément révèle des tensions "
                       "qu'un diagnostic fusionné lisserait",
                       color=D.PALETTE[0])
    D.add_text(s, MARGIN, CONTENT_TOP, CONTENT_W, 0.4, [
        ("Interviewer séparément sert précisément à faire ressortir ces divergences, "
         "pas à produire un consensus lissé.",
         dict(size=8, color=MUTED, italic=True, line_spacing=1.2)),
    ])

    c_infra = D.PALETTE[0]   # Infra & RUN — bleu (comme slide_personas)
    c_user = D.PALETTE[5]    # Utilisateur applicatif — teal
    c_mgmt = D.PALETTE[3]    # Management — or
    c_spon = D.PALETTE[4]    # Sponsor — violet
    c_rssi = D.PALETTE[2]    # RSSI — rouge = porteur du gate, criticité/blocage
    rows = [
        (("Management", c_mgmt), ("Infra & RUN", c_infra), None,
         "Le même métrique de flux, lu « signal de pilotage de confiance » d'un côté, "
         "« surveillance » de l'autre."),
        (("Sponsor", c_spon), ("Infra & RUN", c_infra), None,
         "Horizon : valeur business rapide et visible d'un côté, soulagement durable et "
         "structurel du RUN de l'autre."),
        (("Utilisateur applicatif", c_user), ("Infra & RUN", c_infra), None,
         "Self-service adopté par choix face à l'opérabilité sans sacrifier le delivery : "
         "qui absorbe le coût du self-service ?"),
        (("Sponsor", c_spon), ("RSSI", c_rssi), "ANGLE MORT",
         "Vitesse de démonstration face au gate confidentialité, bloquant sur donnée client."),
    ]
    top0 = CONTENT_TOP + 0.55
    n = len(rows)
    note_reserve = 0.55
    row_gap = 0.12
    region_bot = CONTENT_BOTTOM - note_reserve
    row_h = (region_bot - top0 - (n - 1) * row_gap) / n
    name_w = 2.7
    x_name = MARGIN + 0.2
    x_fric = x_name + name_w + 0.25
    fric_w = (MARGIN + CONTENT_W) - x_fric - 0.15
    for i, ((nomA, colA), (nomB, colB), tag, friction) in enumerate(rows):
        y = top0 + i * (row_h + row_gap)
        D.add_rect(s, MARGIN, y, CONTENT_W, row_h, fill="#ffffff", line=LINE, line_w=0.75,
                   rounded=True, radius=0.08)
        # liseré scindé : moitié haute = couleur A, moitié basse = couleur B
        D.add_rect(s, MARGIN, y, 0.06, row_h / 2, fill=colA, rounded=True, radius=0.5)
        D.add_rect(s, MARGIN, y + row_h / 2, 0.06, row_h / 2, fill=colB, rounded=True, radius=0.5)
        lignes = [
            (nomA, dict(size=D.TYPE["tiny"], bold=True, color=colA, line_spacing=1.0)),
            ("en tension avec", dict(size=7, italic=True, color=MUTED, space_before=3, space_after=3)),
            (nomB, dict(size=D.TYPE["tiny"], bold=True, color=colB, line_spacing=1.0)),
        ]
        if tag:
            lignes.append((tag, dict(size=6.5, bold=True, color=c_rssi, space_before=3)))
        D.add_text(s, x_name, y + 0.08, name_w, row_h - 0.16, lignes, anchor=MSO_ANCHOR.MIDDLE)
        D.add_text(s, x_fric, y + 0.08, fric_w, row_h - 0.16, [
            (friction, dict(size=8, color=NAVY, line_spacing=1.2)),
        ], anchor=MSO_ANCHOR.MIDDLE)

    note_top = top0 + n * row_h + (n - 1) * row_gap + 0.15
    D.add_text(s, MARGIN, note_top, CONTENT_W, CONTENT_BOTTOM - note_top, [
        ("Angles morts, non interrogés à ce stade : le client métier consommateur des services, "
         "le RSSI (porteur du gate), le junior / nouvel arrivant.",
         dict(size=8, color=MUTED, italic=True, line_spacing=1.2)),
    ])
    return s


# ---------------------------------------------------------------- slide 6
def slide_gaspillages(prs):
    s = content_slide(prs, "Méthode", "Le gaspillage, traité comme un objet de transformation", color=D.PALETTE[1])
    familles = [
        ("Flux", "Attentes, validations multiples"),
        ("Humain", "Experts seniors sur tâches répétitives"),
        ("RUN", "Incidents récurrents, demandes répétées"),
        ("Financier", "Surdimensionnement, ressources non décommissionnées"),
        ("Cognitif", "Trop d'outils, procédures complexes"),
        ("Décisionnel", "Arbitrages subjectifs, priorisation opaque"),
        ("Environnemental", "Ressources inutilisées, environnements non éteints"),
        ("IA", "Cas d'usage gadget, automatisation sans garde-fous"),
    ]
    fam_colors = ["#2c5cc5", "#1e6b34", "#b3261e", "#b8860b", "#6a3d9a", "#138086", "#c1651e", "#4b5563"]
    row_top = CONTENT_TOP + 0.45
    row_h = 0.52
    row_gap = 0.08
    for i, (nom, ex) in enumerate(familles):
        col = i % 4
        row = i // 4
        x, w = col_x(col, 4)
        y = row_top + row * (row_h + row_gap)
        D.add_rect(s, x, y, w, row_h, fill="#ffffff", line=LINE, line_w=0.75, rounded=True, radius=0.1)
        D.add_rect(s, x, y, 0.06, row_h, fill=fam_colors[i], rounded=True, radius=0.5)
        D.add_text(s, x + 0.16, y + 0.04, w - 0.28, row_h - 0.08, [
            (nom, dict(size=D.TYPE["tiny"], bold=True, color=NAVY)),
            (ex, dict(size=8, color=MUTED, space_before=1, line_spacing=1.05)),
        ])

    chain_top = row_top + 2 * row_h + row_gap + 0.22
    D.add_text(s, MARGIN, chain_top, CONTENT_W, 0.22, [
        ("CHAÎNE DE TRAITEMENT", dict(size=8, bold=True, color=MUTED))
    ])
    etapes = ["Détecter", "Qualifier", "Quantifier", "Cause racine", "Pattern",
              "Prioriser", "Expérimenter", "Mesurer", "Industrialiser", "Prévenir"]
    step_top = chain_top + 0.24
    step_h = 0.34
    n = 5
    for i, et in enumerate(etapes):
        col = i % n
        row = i // n
        x, w = col_x(col, n)
        y = step_top + row * (step_h + 0.08)
        D.add_rect(s, x, y, w, step_h, fill=TRACK, rounded=True, radius=0.5)
        D.add_text(s, x, y, w, step_h, [
            (f"{i+1}. {et}", dict(size=8, bold=True, color=NAVY, align=PP_ALIGN.CENTER))
        ], anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)

    score_top = step_top + 2 * step_h + 0.08 + 0.2
    score_h = 1.05
    D.add_rect(s, MARGIN, score_top, CONTENT_W, score_h, fill=NAVY, rounded=True, radius=0.08)
    text_w = CONTENT_W * 0.5
    D.add_text(s, MARGIN + 0.22, score_top, text_w - 0.3, score_h, [
        ("Priorité = (impact × faisabilité) − prudence IA", dict(size=D.TYPE["small"], bold=True, color="#ffffff", line_spacing=1.15)),
        ("Le score ne remplace pas l'arbitrage humain : il rend la discussion explicite.",
         dict(size=8, color="#c7cbe0", space_before=4, line_spacing=1.2)),
    ], anchor=MSO_ANCHOR.MIDDLE)

    # Jauge à points — pattern repris de l'autre template analysé
    # (analyse-template-alternatif.md §4) pour illustrer un score 1-5.
    gauge_x = MARGIN + text_w
    gauge_w = CONTENT_W - text_w
    D.add_text(s, gauge_x, score_top + 0.1, gauge_w - 0.15, 0.18, [
        ("SCORE ILLUSTRATIF", dict(size=7, bold=True, color="#8891b3")),
    ])
    rows_top = score_top + 0.32
    row_h2 = (score_h - 0.32 - 0.08) / 3
    gauge_rows = [
        ("Impact", 4, "#ffffff"),
        ("Faisabilité", 3, ACCENT),
        ("Prudence IA", 1, SEVERITE[4]),
    ]
    for i, (label, score, color) in enumerate(gauge_rows):
        ry = rows_top + i * row_h2
        D.add_text(s, gauge_x, ry, 1.2, row_h2, [
            (label, dict(size=7, color="#c7cbe0")),
        ], anchor=MSO_ANCHOR.MIDDLE)
        dot_scale(s, gauge_x + 1.25, ry + row_h2 / 2 - 0.07, 5, score, color,
                  empty_color="#3a4568")
    return s


# --- Exemples générés (Méthode) — concrétisent slide_gaspillages avec des
# instanciations chiffrées des concepts déjà cadrés (formule de priorisation,
# tags de confiance, RecommendationAxis valeur/complexité, US Coach/Délégué) —
# aucun nouveau concept, uniquement des exemples fictifs illustratifs.
def slide_exemple_priorisation(prs):
    s = content_slide(prs, "Méthode",
                       "La priorisation en pratique : la faisabilité tempère l'impact brut",
                       color=D.PALETTE[1])
    D.add_text(s, MARGIN, CONTENT_TOP, CONTENT_W, 0.3, [
        ("Exemple illustratif — 3 gaspillages fictifs notés sur la même formule que la slide précédente.",
         dict(size=8, color=MUTED, italic=True)),
    ])

    items = [
        ("#1", "Triage manuel de tickets récurrents", "RUN", 4, 3, 1, 11, D.PALETTE[1]),
        ("#2", "Ressources cloud surdimensionnées, jamais décommissionnées", "Financier", 5, 2, 0, 10, D.PALETTE[3]),
        ("#3", "Chatbot IA gadget sur la FAQ interne", "IA", 2, 4, 3, 5, MUTED),
    ]
    row_top = CONTENT_TOP + 0.4
    row_h = 1.0
    row_gap = 0.12
    badge_d = 0.4
    name_x = MARGIN + badge_d + 0.15
    name_w = 2.2
    metrics_x0 = name_x + name_w + 0.15
    col_w = 1.3
    col_gap = 0.1
    priorite_x = metrics_x0 + 3 * col_w + 2 * col_gap + 0.15
    priorite_w = MARGIN + CONTENT_W - priorite_x
    metriques = [("IMPACT", D.PALETTE[0]), ("FAISABILITÉ", D.PALETTE[1]), ("PRUDENCE IA", SEVERITE[4])]

    for i, (rang, nom, famille, impact, fais, prudence, priorite, rangcolor) in enumerate(items):
        y = row_top + i * (row_h + row_gap)
        D.add_rect(s, MARGIN, y, CONTENT_W, row_h, fill="#ffffff", line=LINE, line_w=0.75, rounded=True, radius=0.08)
        D.add_rect(s, MARGIN + 0.12, y + row_h / 2 - badge_d / 2, badge_d, badge_d, fill=rangcolor, rounded=True, radius=0.5)
        D.add_text(s, MARGIN + 0.12, y + row_h / 2 - badge_d / 2, badge_d, badge_d, [
            (rang, dict(size=8, bold=True, color="#ffffff", align=PP_ALIGN.CENTER)),
        ], anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
        D.add_text(s, name_x, y + 0.12, name_w, row_h - 0.24, [
            (nom, dict(size=8, bold=True, color=NAVY, line_spacing=1.15)),
            (famille, dict(size=7, color=MUTED, space_before=3)),
        ], anchor=MSO_ANCHOR.MIDDLE)
        scores = [impact, fais, prudence]
        for j, (label, color) in enumerate(metriques):
            mx = metrics_x0 + j * (col_w + col_gap)
            D.add_text(s, mx, y + 0.14, col_w, 0.2, [
                (label, dict(size=7, bold=True, color=MUTED)),
            ])
            dot_scale(s, mx, y + 0.44, 5, scores[j], color, d=0.11, gap=0.05)
        D.add_rect(s, priorite_x, y + row_h / 2 - 0.24, priorite_w, 0.48, fill=TRACK, rounded=True, radius=0.5)
        D.add_text(s, priorite_x, y + row_h / 2 - 0.24, priorite_w, 0.48, [
            (str(priorite), dict(size=D.TYPE["h3"], bold=True, color=NAVY, align=PP_ALIGN.CENTER)),
        ], anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)

    note_top = row_top + 3 * row_h + 2 * row_gap + 0.15
    note_h = min(0.65, CONTENT_BOTTOM - note_top)
    D.add_text(s, MARGIN, note_top, CONTENT_W, note_h, [
        ("#1 et #2 quasi ex-aequo malgré un impact brut très différent (la faisabilité rééquilibre) ; "
         "#3 écarté malgré sa facilité — la prudence IA pénalise un gadget à faible valeur réelle. Le "
         "score rend l'arbitrage explicite, il ne le remplace pas.",
         dict(size=8, color=MUTED, italic=True, line_spacing=1.25)),
    ])
    return s


def slide_exemple_diagnostic(prs):
    s = content_slide(prs, "Méthode",
                       "Un exemple de synthèse : des verbatims tagués, pas une intuition",
                       color=D.PALETTE[1])
    D.add_text(s, MARGIN, CONTENT_TOP, CONTENT_W, 0.28, [
        ("THÈME : RUN / SUPPORT", dict(size=8, bold=True, color=NAVY)),
    ])
    verbatims = [
        ("CONFIRMÉ", SEVERITE[0], "Interview #4 · Équipe infra",
         "« On reçoit les mêmes 5 types de tickets depuis 2 ans, personne n'a jamais "
         "formalisé la procédure de triage. »"),
        ("DÉDUIT", SEVERITE[2], "Recoupement de 3 interviews",
         "« Le temps de triage moyen semble avoir doublé depuis le départ de l'expert "
         "référent, mais personne n'a de chiffre exact. »"),
    ]
    top0 = CONTENT_TOP + 0.4
    card_h = 1.05
    gap = 0.12
    for i, (tag, tagcolor, source, quote) in enumerate(verbatims):
        y = top0 + i * (card_h + gap)
        D.add_card(s, MARGIN, y, CONTENT_W, card_h, tagcolor)
        pad = 0.2
        chip(s, MARGIN + pad, y + 0.14, 1.0, 0.26, tag, tagcolor, size=7)
        D.add_text(s, MARGIN + pad + 1.15, y + 0.14, CONTENT_W - 2 * pad - 1.15, 0.26, [
            (source, dict(size=7, italic=True, color=MUTED)),
        ], anchor=MSO_ANCHOR.MIDDLE)
        D.add_text(s, MARGIN + pad, y + 0.5, CONTENT_W - 2 * pad, card_h - 0.62, [
            (quote, dict(size=8, color=NAVY, italic=True, line_spacing=1.25)),
        ])

    note_top = top0 + 2 * card_h + gap + 0.15
    note_h = min(0.85, CONTENT_BOTTOM - note_top)
    D.add_rect(s, MARGIN, note_top, CONTENT_W, note_h, fill=NAVY, rounded=True, radius=0.08)
    D.add_text(s, MARGIN + 0.22, note_top, CONTENT_W - 0.44, note_h, [
        ("Synthèse", dict(size=D.TYPE["tiny"], bold=True, color="#ffffff")),
        ("Gaspillage RUN récurrent, cause racine = process tacite jamais documenté — "
         "candidat prioritaire pour la chaîne de traitement (slide précédente).",
         dict(size=8, color="#c7cbe0", space_before=3, line_spacing=1.2)),
    ], anchor=MSO_ANCHOR.MIDDLE)
    return s


def slide_exemple_recommandation(prs):
    s = content_slide(prs, "Méthode",
                       "Une recommandation type : valeur/complexité chiffrées, backlog actionnable",
                       color=D.PALETTE[1])
    top0 = CONTENT_TOP + 0.2
    reco_h = 1.15
    D.add_card(s, MARGIN, top0, CONTENT_W, reco_h, D.PALETTE[1])
    pad = 0.2
    D.add_text(s, MARGIN + pad, top0 + 0.14, CONTENT_W - 2 * pad, 0.3, [
        ("RECOMMANDATION", dict(size=7, bold=True, color=MUTED)),
        ("Documenter puis outiller le triage de tickets", dict(size=D.TYPE["h3"], bold=True, color=NAVY, space_before=2)),
    ])
    gauge_y = top0 + 0.72
    for i, (label, score, color) in enumerate([("VALEUR", 4, D.PALETTE[1]), ("COMPLEXITÉ", 2, D.PALETTE[3])]):
        gx = MARGIN + pad + i * 3.0
        D.add_text(s, gx, gauge_y, 1.3, 0.2, [(label, dict(size=7, bold=True, color=MUTED))])
        dot_scale(s, gx, gauge_y + 0.24, 5, score, color, d=0.12, gap=0.05)

    # Carte US plafonnée au contenu (chip → titre → owner → critère collés),
    # au lieu du min(2.2, …) qui laissait un vide sous le titre d'action et
    # sous la carte (défaut « panneau sur-étiré », slide 17).
    us_top = top0 + reco_h + 0.2
    us_h = 1.78
    backlog = [
        ("Coach", D.PALETTE[3], "Rédiger le runbook de triage",
         "Consultant BMAD IAP", "Runbook validé par l'équipe RUN en atelier"),
        ("Délégué", D.PALETTE[1], "Appliquer le runbook seule pendant 2 semaines",
         "Équipe infra", "Aucun ticket mal routé sur l'échantillon audité"),
    ]
    for i, (mode, color, titre, owner, critere) in enumerate(backlog):
        x, w = col_x(i, 2)
        D.add_card(s, x, us_top, w, us_h, color)
        p2 = 0.18
        chip(s, x + p2, us_top + 0.14, 1.0, 0.26, mode.upper(), color, size=7)
        D.add_text(s, x + p2, us_top + 0.52, w - 2 * p2, 0.30, [
            (titre, dict(size=8, bold=True, color=NAVY, line_spacing=1.2)),
        ])
        D.add_text(s, x + p2, us_top + 0.84, w - 2 * p2, 0.32, [
            ("OWNER", dict(size=7, bold=True, color=MUTED)),
            (owner, dict(size=8, color=NAVY, space_before=1)),
        ])
        D.add_text(s, x + p2, us_top + 1.26, w - 2 * p2, us_h - 1.36, [
            ("CRITÈRE D'ACCEPTATION", dict(size=7, bold=True, color=MUTED)),
            (critere, dict(size=8, color=NAVY, space_before=1, line_spacing=1.2)),
        ])
    return s


# ---------------------------------------------------------------- slide 9
def slide_team_topologies(prs):
    s = content_slide(prs, "Méthode", "La cible IAP est une Platform Team — agents IA compris", color=D.PALETTE[1])
    types = [
        ("Stream-aligned", D.PALETTE[0], "Flux de valeur métier continu",
         "Équipes applicatives clientes de la plateforme infra"),
        ("Platform", D.PALETTE[1], "Capacités en self-service (X-as-a-Service)",
         "La cible même de la transformation IAP"),
        ("Enabling", D.PALETTE[3], "Montée en compétence temporaire",
         "Posture du coach BMAD IAP — jamais permanente"),
        ("Complicated-subsystem", D.PALETTE[4], "Expertise pointue, compétences rares",
         "Un vrai sous-système complexe, pas un produit plateforme classique"),
    ]
    n = 4
    card_h = 1.55
    top0 = CONTENT_TOP + 0.05
    for i, (titre, color, role, lecture) in enumerate(types):
        x, w = col_x(i, n)
        D.add_card(s, x, top0, w, card_h, color)
        pad = 0.16
        D.add_text(s, x + pad, top0 + 0.14, w - 2 * pad, 0.45, [
            (titre, dict(size=8, bold=True, color=color, line_spacing=1.05)),
        ])
        D.add_text(s, x + pad, top0 + 0.58, w - 2 * pad, 0.4, [
            (role, dict(size=8, color=NAVY, line_spacing=1.15)),
        ])
        D.add_text(s, x + pad, top0 + 1.0, w - 2 * pad, card_h - 1.1, [
            (lecture, dict(size=8, color=MUTED, italic=True, line_spacing=1.15)),
        ])

    note_top = top0 + card_h + 0.18
    note_h = min(1.5, CONTENT_BOTTOM - note_top)
    D.add_rect(s, MARGIN, note_top, CONTENT_W, note_h, fill=TRACK, rounded=True, radius=0.08)
    D.add_text(s, MARGIN + 0.22, note_top, CONTENT_W - 0.44, note_h, [
        ("Extension — les agents IA comme coéquipiers, et leur mise en œuvre (v1.7)",
         dict(size=D.TYPE["tiny"], bold=True, color=NAVY)),
        ("Un agent peut être membre d'une Stream-aligned team ou capacité exposée par la "
         "Platform Team (4ᵉ mode candidat : Supervision). L'adoption suit la trajectoire "
         "Coach → Délégué (assisté → supervisé → délégué) : mandat écrit (ce que l'agent "
         "décide seul / ce qui escalade / qui répond de ses erreurs) avant tout palier "
         "au-delà de l'assisté — jamais un usage qui dérive à l'implicite.",
         dict(size=8, color=NAVY, space_before=3, line_spacing=1.25)),
    ], anchor=MSO_ANCHOR.MIDDLE)
    return s


# ---------------------------------------------------------------- slide 8
# Formes inspirées des slides d'exemple du template lui-même (« Notre
# approche ») : badges circulaires connectés par une ligne, chip de durée,
# description centrée sous chaque étape.
# Nouveau (v2.3) : le schéma de fonctionnement du §Trajectoire de
# bmad-iap-cadrage.md n'avait jusqu'ici qu'un résumé en une ligne dans
# slide_trajectoire (phase ①, "= Schéma de fonctionnement déjà cadré") —
# jamais sa propre slide. Reprend la lecture verticale du schéma ASCII
# source : bandeau Gate IA transversal, 4 colonnes du pipeline, bandeau
# iap-risk-reviewer, bandeau boucle de réévaluation.
def slide_schema_fonctionnement(prs):
    s = content_slide(prs, "Trajectoire",
                       "La Gate IA s'applique à chaque étape, de la collecte à la boucle de réévaluation",
                       color=D.PALETTE[3])
    D.add_text(s, MARGIN, CONTENT_TOP, CONTENT_W, 0.26, [
        ("Deux sources de collecte convergent vers un diagnostic structuré ; une boucle de "
         "réévaluation referme le cycle.", dict(size=8, color=MUTED, italic=True, line_spacing=1.1)),
    ])

    band_top = CONTENT_TOP + 0.3
    band_h = 0.36
    D.add_rect(s, MARGIN, band_top, CONTENT_W, band_h, fill=NAVY, rounded=True, radius=0.12)
    D.add_text(s, MARGIN + 0.2, band_top, CONTENT_W - 0.4, band_h, [
        ("GATE IA & CONFIDENTIALITÉ — checkpoint humain, transversal à chaque étape qui invoque un LLM",
         dict(size=8, bold=True, color="#ffffff", line_spacing=1.1)),
    ], anchor=MSO_ANCHOR.MIDDLE)

    etapes = [
        ("COLLECTE", D.PALETTE[0],
         ["Interviews par persona (Trame/Theme/Question)",
          "Import outils : ServiceNow/Jira/CMDB si accès"]),
        ("DIAGNOSTIC", D.PALETTE[4],
         ["Synthesis par thème + GlobalSynthesis",
          "Waste-register (tags CONFIRMÉ/DÉDUIT/INCERTAIN)"]),
        ("CONCEPTION", D.PALETTE[3],
         ["Product definition (+ mvp-target-model.md)",
          "Operating model + waste-treatment (ADR)"]),
        ("RESTITUTION", D.PALETTE[1],
         ["Deck exécutif : RecommendationAxis",
          "+ radar de maturité"]),
    ]
    n = len(etapes)
    col_top = band_top + band_h + 0.16
    card_h = 1.85
    for i, (titre, color, lignes) in enumerate(etapes):
        x, w = col_x(i, n)
        D.add_rect(s, x, col_top, w, 0.05, fill=color)
        D.add_text(s, x, col_top + 0.1, w, 0.26, [
            (titre, dict(size=8, bold=True, color=color, align=PP_ALIGN.CENTER)),
        ], align=PP_ALIGN.CENTER)
        card_y = col_top + 0.4
        D.add_rect(s, x, card_y, w, card_h - 0.4, fill=TRACK, rounded=True, radius=0.08)
        lignes_fmt = [(f"·  {l}", dict(size=7, color=NAVY, space_after=4, line_spacing=1.2)) for l in lignes]
        D.add_text(s, x + 0.1, card_y + 0.12, w - 0.2, card_h - 0.4 - 0.24, lignes_fmt,
                   anchor=MSO_ANCHOR.MIDDLE)
        if i < n - 1:
            D.add_text(s, x + w, col_top + 0.08, GAP, 0.26, [
                ("→", dict(size=10, bold=True, color=MUTED, align=PP_ALIGN.CENTER)),
            ], anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)

    reviewer_top = col_top + card_h + 0.16
    reviewer_h = 0.4
    D.add_rect(s, MARGIN, reviewer_top, CONTENT_W, reviewer_h, fill="#ffffff", line=LINE,
               rounded=True, radius=0.1)
    D.add_text(s, MARGIN + 0.2, reviewer_top, CONTENT_W - 0.4, reviewer_h, [
        ("iap-risk-reviewer — lecture seule, challenge Product definition / Operating model → Deck exécutif",
         dict(size=7.5, italic=True, color=MUTED, line_spacing=1.1)),
    ], anchor=MSO_ANCHOR.MIDDLE)

    loop_top = reviewer_top + reviewer_h + 0.14
    loop_h = min(0.55, CONTENT_BOTTOM - loop_top)
    D.add_rect(s, MARGIN, loop_top, CONTENT_W, loop_h, fill=D.PALETTE[2], rounded=True, radius=0.1)
    D.add_text(s, MARGIN + 0.2, loop_top, CONTENT_W - 0.4, loop_h, [
        ("⟲ Boucle de réévaluation — iap-re-assessment, T+6-12 mois, alimente rex-library.md, "
         "reboucle vers la Collecte", dict(size=8, bold=False, color="#ffffff", line_spacing=1.15)),
    ], anchor=MSO_ANCHOR.MIDDLE)
    return s


def slide_trajectoire(prs):
    s = content_slide(prs, "Trajectoire", "Mise en œuvre du target operating model — brainstorm", color=D.PALETTE[3])
    phases = [
        ("①", "Assessment flash", "1–2 sem.", D.PALETTE[0],
         "= Schéma de fonctionnement déjà cadré (Collecte → Diagnostic → Conception → Restitution)."),
        ("②", "Premier déploiement", "4–5 sem.", D.PALETTE[3],
         "1-2 équipes pilotes, mode Coach dominant. Piste agent IA (si retenue) : qualifier, cadrer, mandater."),
        ("③", "Implémentation itérative", "→ T+6-12 mois", D.PALETTE[1],
         "Généralisation équipe par équipe, bascule Coach → Délégué. Piste agent IA : supervisé puis délégué."),
        ("⟲", "Boucle de réévaluation", "T+6-12 mois", D.PALETTE[2],
         "iap-re-assessment reboucle vers la Collecte — alimente rex-library.md."),
    ]
    n = len(phases)
    badge_d = 0.55
    top0 = CONTENT_TOP + 0.1
    line_y = top0 + badge_d / 2 - 0.012
    D.add_rect(s, MARGIN + badge_d / 2, line_y, CONTENT_W - badge_d, 0.024, fill=LINE)
    desc_h = 0.95
    for i, (sym, titre, duree, color, desc) in enumerate(phases):
        x, w = col_x(i, n)
        cx = x + w / 2 - badge_d / 2
        D.add_rect(s, cx, top0, badge_d, badge_d, fill=color, rounded=True, radius=0.5)
        D.add_text(s, cx, top0, badge_d, badge_d, [
            # bold=False pour "⟲" : sa variante grasse manque dans la police du
            # template (rendu LibreOffice = case vide) — ①②③ n'ont pas ce problème.
            (sym, dict(size=16, bold=(sym != "⟲"), color="#ffffff", align=PP_ALIGN.CENTER))
        ], anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
        ty = top0 + badge_d + 0.12
        D.add_text(s, x, ty, w, 0.35, [
            (titre, dict(size=8, bold=True, color=NAVY, align=PP_ALIGN.CENTER, line_spacing=1.05)),
        ], align=PP_ALIGN.CENTER)
        chip_y = ty + 0.36
        chip(s, x + w / 2 - 0.55, chip_y, 1.1, 0.24, duree, color, size=7)
        desc_y = chip_y + 0.32
        D.add_text(s, x + 0.05, desc_y, w - 0.1, desc_h, [
            (desc, dict(size=7, color=MUTED, align=PP_ALIGN.CENTER, line_spacing=1.2)),
        ], align=PP_ALIGN.CENTER)

    note_top = top0 + badge_d + 0.12 + 0.36 + 0.32 + desc_h + 0.12
    note_h = min(1.4, CONTENT_BOTTOM - note_top)
    D.add_rect(s, MARGIN, note_top, CONTENT_W, note_h, fill=TRACK, rounded=True, radius=0.08)
    D.add_text(s, MARGIN + 0.2, note_top, CONTENT_W - 0.4, note_h, [
        ("Bifurcation avec/sans agents IA déployés", dict(size=8, bold=True, color=NAVY)),
        ("Le tronc commun ①→②→③→⟲ ne change pas de structure — la piste agent IA (si retenue) "
         "se greffe sur ②/③ via la démarche en 5 phases déjà cadrée (§Modèles d'équipe), plutôt "
         "que d'être un chemin séparé à maintenir. Owner proposé (non tranché) : "
         "iap-operating-model-architect + iap-change-coach sur le volet humain.",
         dict(size=7, color=NAVY, space_before=3, line_spacing=1.25)),
    ], anchor=MSO_ANCHOR.MIDDLE)
    return s


# ---------------------------------------------------------------- slide 9
# Formes inspirées de la slide d'exemple « Une approche contextualisée » du
# template : colonne par étape avec badge + bandeau titre + ligne de
# séparation + bloc LIVRABLES, plutôt qu'un tableau plat.
def slide_livrables_ppt(prs):
    s = content_slide(prs, "Trajectoire", "Livrables PPT par étape — brainstorm", color=D.PALETTE[3])
    D.add_text(s, MARGIN, CONTENT_TOP, CONTENT_W, 0.4, [
        ("iap-deck-builder est cadré comme un seul deck modulaire 16 sections, produit une fois "
         "à la Restitution — la trajectoire ci-avant implique plusieurs publics et moments de "
         "décision distincts. Piste : un profil de sections par étape, pas 4 générateurs séparés.",
         dict(size=8, color=MUTED, italic=True, line_spacing=1.2)),
    ])
    cols = [
        ("①", "Assessment flash", D.PALETTE[0], "Sponsor, comité de lancement",
         "Deck exécutif de restitution", "(déjà cadré) GlobalSynthesis, RecommendationAxis, radar T0"),
        ("②", "Premier déploiement", D.PALETTE[3], "Équipes pilotes + management",
         "Deck de plan de déploiement", "(nouveau) Cible TOM détaillée, backlog Coach/Délégué, mandat agent IA"),
        ("③", "Implémentation itérative", D.PALETTE[1], "Instance de comitologie",
         "Deck de comité de pilotage", "(nouveau, périodique) Avancement backlog, delta KPIs, risques actifs"),
        ("⟲", "Boucle de réévaluation", D.PALETTE[2], "Sponsor",
         "Deck de bilan / ré-évaluation", "(nouveau) Delta maturité T0→T+6-12, REX consolidé"),
    ]
    n = len(cols)
    pad = 0.16
    _, wcol = col_x(0, n)
    usable = wcol - 2 * pad
    # Carte plafonnée au contenu (bloc badge/titre → séparateur → audience →
    # LIVRABLES → contenu) au lieu de CONTENT_BOTTOM - top0 : sinon la colonne
    # s'étirait sur toute la hauteur et laissait ~60 % de vide sous le texte
    # (défaut « colonne timeline sur-étirée », slide 24).
    contenu_lines = max(_lignes(c[5], usable, 7) for c in cols)
    card_h = 1.56 + contenu_lines * (7 * 1.28 / 72.0) + 0.18
    region_top = CONTENT_TOP + 0.5
    top0 = region_top + min(0.45, max(0.0, (CONTENT_BOTTOM - region_top - card_h) / 2))
    badge_d = 0.34
    for i, (sym, titre, color, audience, deck, contenu) in enumerate(cols):
        x, w = col_x(i, n)
        D.add_card(s, x, top0, w, card_h, color)
        pad = 0.16
        D.add_rect(s, x + pad, top0 + 0.14, badge_d, badge_d, fill=color, rounded=True, radius=0.5)
        D.add_text(s, x + pad, top0 + 0.14, badge_d, badge_d, [
            (sym, dict(size=11, bold=(sym != "⟲"), color="#ffffff", align=PP_ALIGN.CENTER)),
        ], anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
        D.add_text(s, x + pad + badge_d + 0.08, top0 + 0.14, w - 2 * pad - badge_d - 0.08, badge_d, [
            (titre, dict(size=8, bold=True, color=color, line_spacing=1.0)),
        ], anchor=MSO_ANCHOR.MIDDLE)
        line_y = top0 + 0.14 + badge_d + 0.1
        D.add_rect(s, x + pad, line_y, w - 2 * pad, 0.012, fill=LINE)
        D.add_text(s, x + pad, line_y + 0.08, w - 2 * pad, 0.22, [
            (audience, dict(size=7, italic=True, color=MUTED)),
        ])
        D.add_text(s, x + pad, line_y + 0.34, w - 2 * pad, 0.55, [
            ("LIVRABLES", dict(size=7, bold=True, color=NAVY)),
            (deck, dict(size=8, bold=True, color=NAVY, space_before=2, line_spacing=1.1)),
        ])
        contenu_top = line_y + 0.98
        D.add_text(s, x + pad, contenu_top, w - 2 * pad, top0 + card_h - contenu_top - 0.12, [
            (contenu, dict(size=7, color=MUTED, line_spacing=1.25)),
        ])
    return s


# Nouveau — brainstorm de design (v2.2) : reprend le pattern « cadre blanc »
# du template (déjà utilisé dans le REX "⛱️ L'Été de l'IA", VSCode1, en
# alternance gauche/droite pour chaque slide de contenu) — claim + puces à
# gauche, illustration encadrée à droite.
# Révisé (v2.3, retour utilisateur) : slide 3 recadrée sur le pourquoi du
# projet, les enjeux, un vrai risque et une difficulté de mise en œuvre —
# plutôt que sur le seul point de doctrine IA (qui reste, mais comme UNE
# puce parmi d'autres, pas tout l'écran). Contenu puisé dans §Mission &
# vision (guichet/centre de coûts, 3 tensions), §Doctrine (dette non
# séquentielle gaspillage/cible) et le callout IA déjà cadré.
def slide_vision_ia(prs):
    layout = prs.slide_masters[0].slide_layouts[LAYOUT_VISUEL_DROITE]
    s = prs.slides.add_slide(layout)
    phs = {ph.placeholder_format.idx: ph for ph in s.placeholders}

    phs[0].text_frame.text = ("Le risque n'est pas de manquer d'outils : "
                               "c'est de traiter le mauvais problème")
    for p in phs[0].text_frame.paragraphs:
        for r in p.runs:
            r.font.color.rgb = _rgb(NAVY)

    bullets = [
        "Pourquoi ce projet : une infrastructure vécue comme un guichet ou un centre de "
        "coûts n'a ni utilisateurs identifiés, ni feuille de route, ni levier d'adoption "
        "— elle subit la demande au lieu de la piloter.",
        "Les enjeux : tenir trois tensions en même temps, jamais une seule — l'efficacité "
        "du delivery, la robustesse du RUN, et la valeur perçue par les utilisateurs internes.",
        "La difficulté : gaspillage et cible produit ne sont pas séquentiels — une cible "
        "sans traitement du gaspillage manque de la capacité pour s'y déployer, l'inverse "
        "reste une réduction de coûts sans vision.",
        "Le risque le plus sous-estimé : l'IA amplifie l'organisation existante, elle n'en "
        "corrige pas les dysfonctionnements — jamais une réponse à un problème d'abord "
        "organisationnel.",
    ]
    tf = phs[1].text_frame
    tf.text = bullets[0]
    for b in bullets[1:]:
        p = tf.add_paragraph()
        p.text = b
    for p in tf.paragraphs:
        for r in p.runs:
            r.font.color.rgb = _rgb(NAVY)

    cadre = _find_frame_in_group(s.slide_layout.shapes, "Google Shape;212;p17", "Google Shape;213;p17")
    for pb in frame_obstructions(s, *cadre[:4]) if cadre else []:
        print("  [obstruction] vision-ia:", pb["source"], pb["name"], pb["reason"])
    _remplir_cadre(s, cadre, "sunset", seed=1)
    return s


# Nouveau : assemble slide_trajectoire (phases) et slide_livrables_ppt/
# slide_export_markdown (contenu détaillé de chaque livrable) en une seule
# vue de synthèse bout-en-bout — sert de pont entre les deux, pas un doublon
# (chaque colonne ne liste QUE le nom des livrables, pas leur contenu).
def slide_schema_bout_en_bout(prs):
    s = content_slide(prs, "Trajectoire",
                       "Comment ça fonctionne, de bout en bout : quels livrables, à quel moment",
                       color=D.PALETTE[3])
    D.add_text(s, MARGIN, CONTENT_TOP, CONTENT_W, 0.3, [
        ("Assemble la trajectoire (slide précédente) et les livrables détaillés (slides suivantes) "
         "en une seule vue d'ensemble.", dict(size=8, color=MUTED, italic=True)),
    ])
    phases = [
        ("①", "Assessment flash", "1-2 sem.", D.PALETTE[0],
         ["Deck exécutif de restitution"]),
        ("②", "Premier déploiement", "4-5 sem.", D.PALETTE[3],
         ["Deck de plan de déploiement", "Export markdown (1re version)"]),
        ("③", "Implémentation itérative", "→ T+6-12 mois", D.PALETTE[1],
         ["Deck de comité de pilotage (périodique)"]),
        ("⟲", "Boucle de réévaluation", "T+6-12 mois", D.PALETTE[2],
         ["Deck de bilan / ré-évaluation", "Export markdown amendé"]),
    ]
    n = 4
    badge_d = 0.45
    top0 = CONTENT_TOP + 0.42
    line_y = top0 + badge_d / 2 - 0.01
    D.add_rect(s, MARGIN + badge_d / 2, line_y, CONTENT_W - badge_d, 0.02, fill=LINE)
    card_h = 1.1
    card_top = None
    for i, (sym, titre, duree, color, livrables) in enumerate(phases):
        x, w = col_x(i, n)
        cx = x + w / 2 - badge_d / 2
        D.add_rect(s, cx, top0, badge_d, badge_d, fill=color, rounded=True, radius=0.5)
        D.add_text(s, cx, top0, badge_d, badge_d, [
            (sym, dict(size=13, bold=(sym != "⟲"), color="#ffffff", align=PP_ALIGN.CENTER)),
        ], anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
        ty = top0 + badge_d + 0.1
        D.add_text(s, x, ty, w, 0.3, [
            (titre, dict(size=8, bold=True, color=NAVY, align=PP_ALIGN.CENTER, line_spacing=1.0)),
        ], align=PP_ALIGN.CENTER)
        chip_y = ty + 0.3
        chip(s, x + w / 2 - 0.5, chip_y, 1.0, 0.22, duree, color, size=7)
        card_top = chip_y + 0.32
        D.add_rect(s, x, card_top, w, card_h, fill=TRACK, rounded=True, radius=0.08)
        D.add_text(s, x + 0.1, card_top + 0.08, w - 0.2, 0.2, [
            ("LIVRABLES", dict(size=7, bold=True, color=MUTED)),
        ])
        lignes = [(f"·  {l}", dict(size=7, color=NAVY, space_after=3, line_spacing=1.15)) for l in livrables]
        D.add_text(s, x + 0.1, card_top + 0.3, w - 0.2, card_h - 0.4, lignes)

    note_top = card_top + card_h + 0.15
    note_h = min(1.3, CONTENT_BOTTOM - note_top)
    D.add_rect(s, MARGIN, note_top, CONTENT_W, note_h, fill=NAVY, rounded=True, radius=0.08)
    D.add_text(s, MARGIN + 0.22, note_top, CONTENT_W - 0.44, note_h, [
        ("Deux flux de livrables, une seule trajectoire", dict(size=D.TYPE["tiny"], bold=True, color="#ffffff")),
        ("Le flux PPT (sponsor, comité de pilotage) et le flux markdown (équipe qui exécute) avancent "
         "en parallèle sur le même calendrier ①→②→③→⟲ — jamais deux trajectoires séparées à maintenir.",
         dict(size=8, color="#c7cbe0", space_before=3, line_spacing=1.25)),
    ], anchor=MSO_ANCHOR.MIDDLE)
    return s


# ---------------------------------------------------------------- slide 10
# Nouveau (v2.0) : la bifurcation "avec/sans agent IA" de slide_trajectoire
# gagne un livrable concret, distinct des 4 decks PPT — un markdown pour
# l'équipe qui exécute, pas pour le sponsor. Deux cartes (mêmes proportions
# que slide_mission) + un bandeau de routage + une note "pas un aller simple".
def slide_export_markdown(prs):
    s = content_slide(prs, "Trajectoire",
                       "Export markdown — agentic ou documentation, selon le contexte client (brainstorm)",
                       color=D.PALETTE[3])
    D.add_text(s, MARGIN, CONTENT_TOP, CONTENT_W, 0.32, [
        ("Pas un 5e deck PPT : un livrable markdown pour l'équipe qui exécute (versionnable, "
         "committable) — les 4 decks ci-dessus restent pour sponsor et comité de pilotage.",
         dict(size=8, color=MUTED, italic=True, line_spacing=1.2)),
    ])

    cards = [
        ("DOCUMENTATION-FIRST", D.PALETTE[2],
         "Agentic Readiness [0]-[1], données D3-D4 sans LLM local, ou score de gaspillage faible.",
         "runbook-<processus>.md", "iap-adoption-plan"),
        ("AGENTIC-IMPLEMENTATION", D.PALETTE[0],
         "Agentic Readiness [2]-[3], données D0-D2 (ou D3-D4 avec LLM local), score positif.",
         "agentic-implementation-plan.md", "iap-agentic-opportunities"),
    ]
    top0 = CONTENT_TOP + 0.42
    card_h = 1.55
    for i, (titre, color, quand, fichier, owner) in enumerate(cards):
        x, w = col_x(i, 2)
        D.add_card(s, x, top0, w, card_h, color)
        pad = 0.2
        D.add_text(s, x + pad, top0 + 0.14, w - 2 * pad, 0.3, [
            (titre, dict(size=D.TYPE["h3"], bold=True, color=color)),
        ])
        D.add_text(s, x + pad, top0 + 0.5, w - 2 * pad, 0.55, [
            ("QUAND", dict(size=D.TYPE["tiny"], bold=True, color=MUTED)),
            (quand, dict(size=8, color=NAVY, space_before=2, line_spacing=1.2)),
        ])
        D.add_text(s, x + pad, top0 + 1.08, w - 2 * pad, 0.4, [
            ("LIVRABLE · OWNER", dict(size=7, bold=True, color=MUTED)),
            (f"{fichier} — {owner}", dict(size=8, bold=True, color=NAVY, space_before=2)),
        ])

    signals_top = top0 + card_h + 0.15
    signals_h = 0.55
    signals = [
        ("PILIER AGENTIC READINESS", "[0-1] → documentation · [2-3] → agentic"),
        ("DONNÉES (GATE IA)", "D3-D4 sans LLM local → doc · D0-D2 → agentic"),
        ("SCORE DE GASPILLAGE", "faible/négatif → doc · positif → agentic"),
    ]
    for i, (label, mapping) in enumerate(signals):
        x, w = col_x(i, 3)
        D.add_rect(s, x, signals_top, w, signals_h, fill=TRACK, rounded=True, radius=0.1)
        D.add_text(s, x + 0.12, signals_top + 0.06, w - 0.24, signals_h - 0.12, [
            (label, dict(size=7, bold=True, color=NAVY)),
            (mapping, dict(size=7, color=MUTED, space_before=2, line_spacing=1.15)),
        ])

    note_top = signals_top + signals_h + 0.15
    note_h = min(1.05, CONTENT_BOTTOM - note_top)
    D.add_rect(s, MARGIN, note_top, CONTENT_W, note_h, fill=NAVY, rounded=True, radius=0.08)
    D.add_text(s, MARGIN + 0.22, note_top, CONTENT_W - 0.44, note_h, [
        ("Pas un aller simple", dict(size=D.TYPE["tiny"], bold=True, color="#ffffff")),
        ("À chaque boucle de réévaluation, le même fichier est amendé — jamais dupliqué — sur le "
         "modèle d'ai-risk-register.md : un client documentation-first peut basculer en agentic si "
         "son Agentic Readiness progresse, et inversement en cas de deskilling-risk avéré.",
         dict(size=8, color="#c7cbe0", space_before=4, line_spacing=1.25)),
    ], anchor=MSO_ANCHOR.MIDDLE)
    return s


# ---------------------------------------------------------------- slide 11
def slide_ambition(prs):
    s = content_slide(prs, "Trajectoire", "Trois niveaux d'ambition, pas un spectre linéaire", color=D.PALETTE[3])
    niveaux = [
        ("A", "Aide au coach", D.PALETTE[0],
         "Génère un livrable à la demande — aucune initiative propre. Le consultant pilote à 100 %.",
         "État actuel du cadrage (MVP0–MVP5)"),
        ("B", "Assistant interactif", D.PALETTE[3],
         "Guide pas à pas, pose des questions de clarification, signale les incohérences.",
         "Palier intermédiaire, entre MVP5 et MVP6"),
        ("C", "Companion connecté", D.PALETTE[2],
         "Connecté en direct à ServiceNow/Jira/Confluence/Datadog/CMDB/FinOps, quasi autonome.",
         "= MVP6, non engagé"),
    ]
    n = 3
    pad = 0.2
    _, wcol = col_x(0, n)
    usable = wcol - 2 * pad
    # Légende roadmap collée SOUS le texte de rôle (au lieu d'un y fixe en bas
    # de carte) et carte plafonnée à son contenu : supprime le « trou mort »
    # entre le rôle et la légende, et le sur-étirement de la carte (slide 26).
    role_lines = max(_lignes(niv[3], usable, 8) for niv in niveaux)
    role_h = role_lines * (8 * 1.25 / 72.0) + 0.06
    roadmap_y = 0.55 + role_h + 0.12
    card_h = roadmap_y + 0.28 + 0.14
    top0 = CONTENT_TOP + 0.45
    for i, (code, titre, color, role, roadmap) in enumerate(niveaux):
        x, w = col_x(i, n)
        D.add_card(s, x, top0, w, card_h, color)
        D.add_text(s, x + pad, top0 + 0.15, w - 2 * pad, 0.35, [
            (f"{code} · {titre}", dict(size=D.TYPE["small"], bold=True, color=color)),
        ])
        D.add_text(s, x + pad, top0 + 0.55, w - 2 * pad, role_h, [
            (role, dict(size=8, color=NAVY, line_spacing=1.25)),
        ])
        D.add_text(s, x + pad, top0 + roadmap_y, w - 2 * pad, 0.3, [
            (roadmap, dict(size=8, bold=True, color=MUTED)),
        ])

    note_top = top0 + card_h + 0.18
    note_h = CONTENT_BOTTOM - note_top
    D.add_text(s, MARGIN, note_top, CONTENT_W, note_h, [
        ("Monter de A à C n'est pas qu'une question de fonctionnalités : le niveau C suppose "
         "un accès direct aux données de production du client — risque sécurité/confidentialité "
         "d'un tout autre ordre. Un cabinet peut durablement rester au niveau A ou B par choix "
         "de gouvernance, pas seulement par contrainte technique transitoire.",
         dict(size=8, color=MUTED, italic=True, line_spacing=1.3)),
    ])
    return s


# ---------------------------------------------------------------- slide 12
def slide_kpis(prs):
    s = content_slide(prs, "Trajectoire", "Trois familles de KPIs, à ne jamais confondre", color=D.PALETTE[3])
    familles = [
        ("KPIs de mission", D.PALETTE[0], "Côté client",
         ["Gaspillage traité (capacité RUN récupérée)", "Adoption produit (self-service)",
          "Fiabilité & coût (MTTR : délai moyen de résolution, coût/capacité)", "Gouvernance IA (supervision, incidents)",
          "Maturité (delta par pilier, T0→réévaluation)"]),
        ("KPIs d'usage du module", D.PALETTE[1], "Côté cabinet",
         ["Accélération (temps pour un cadrage flash)", "Réutilisation (templates vs ad hoc)",
          "Cohérence (écarts détectés par risk-reviewer)", "Capitalisation (REX ajoutés)",
          "Adoption interne (consultants, missions)"]),
        ("Grille de maturité", D.PALETTE[3], "Progression dans le temps",
         ["Delta par pilier (Excellence Tech., Agilité, IA/Agentic)",
          "Re-assessment T+6–12 mois",
          "Score de priorisation ≠ KPI de résultat"]),
    ]
    n = 3
    pad = 0.18
    _, wcol = col_x(0, n)
    usable = wcol - 2 * pad
    # Carte plafonnée au contenu (titre + sous-titre + puces) puis bande de
    # cartes CENTRÉE verticalement — au lieu de card_h = CONTENT_H qui étirait
    # chaque colonne sur toute la hauteur et laissait un grand vide sous les
    # puces (défaut « panneau sur-étiré », slide 28).
    def _bloc_puces(items):
        lignes = sum(_lignes("·  " + it, usable, 8) for it in items)
        return lignes * (8 * 1.15 / 72.0) + len(items) * (4 / 72.0)
    bullets_h = max(_bloc_puces(items) for *_, items in familles)
    card_h = 0.8 + bullets_h + 0.22
    top0 = CONTENT_TOP + max(0.0, (CONTENT_H - card_h) / 2)
    for i, (titre, color, sous, items) in enumerate(familles):
        x, w = col_x(i, n)
        D.add_card(s, x, top0, w, card_h, color)
        D.add_text(s, x + pad, top0 + 0.16, w - 2 * pad, 0.55, [
            (titre, dict(size=D.TYPE["tiny"], bold=True, color=color, line_spacing=1.05)),
            (sous, dict(size=8, color=MUTED, italic=True, space_before=2)),
        ])
        lignes = [(f"·  {it}", dict(size=8, color=NAVY, space_after=4, line_spacing=1.15))
                  for it in items]
        D.add_text(s, x + pad, top0 + 0.8, w - 2 * pad, card_h - 0.95, lignes)
    return s

# --- Brainstorm KPIs relancé (v2.1, docs/bmad-iap-cadrage.md §KPIs) — pourquoi
# chaque famille, quoi mesurer précisément, comment la mettre en place, et un
# exemple chiffré sur le cas nominal déjà posé pour l'export markdown.
def slide_kpis_pourquoi_quoi(prs):
    s = content_slide(prs, "Trajectoire", "KPIs : pourquoi chaque famille, et quoi mesurer précisément", color=D.PALETTE[3])
    familles = [
        ("KPIs de mission", D.PALETTE[0],
         "Sans eux, un deck peut être livré dans les règles sans jamais savoir si le client va "
         "réellement mieux — la « transformation cosmétique » appliquée cette fois au résultat.",
         "Capacité RUN récupérée en heures/mois ; delta de MTTR en minutes ; taux de self-service "
         "sur la capacité livrée — pas un pourcentage vague."),
        ("KPIs d'usage du module", D.PALETTE[1],
         "Le module est réutilisé mission après mission — sans mesure d'usage, impossible de "
         "distinguer une méthode qui s'améliore d'une méthode qui stagne.",
         "Temps en heures consultant pour un cadrage flash ; part des livrables issus d'un template "
         "sans réécriture substantielle — pas juste « utilisé un template »."),
        ("Grille de maturité", D.PALETTE[3],
         "Sans mesure répétée dans le temps, la maturité reste une opinion de consultant, pas un "
         "delta objectivable — ce qui rend la boucle ⟲ vérifiable plutôt que déclarative.",
         "Delta par pilier (pas un score agrégé qui masquerait un recul) ; même instrument (grille "
         "V3.2) à T0 et à chaque re-assessment."),
    ]
    top0 = CONTENT_TOP + 0.05
    row_h = (CONTENT_H - 0.05 - 2 * 0.12) / 3
    for i, (nom, color, pourquoi, quoi) in enumerate(familles):
        y = top0 + i * (row_h + 0.12)
        D.add_card(s, MARGIN, y, CONTENT_W, row_h, color)
        pad = 0.18
        D.add_text(s, MARGIN + pad, y + 0.12, 1.7, row_h - 0.24, [
            (nom, dict(size=8, bold=True, color=color, line_spacing=1.15)),
        ], anchor=MSO_ANCHOR.MIDDLE)
        colw = (CONTENT_W - 2 * pad - 1.7 - 0.2) / 2
        x1 = MARGIN + pad + 1.7 + 0.2
        D.add_text(s, x1, y + 0.12, colw, row_h - 0.24, [
            ("POURQUOI", dict(size=7, bold=True, color=MUTED)),
            (pourquoi, dict(size=8, color=NAVY, space_before=3, line_spacing=1.2)),
        ])
        x2 = x1 + colw + 0.15
        D.add_text(s, x2, y + 0.12, colw, row_h - 0.24, [
            ("QUOI, PRÉCISÉMENT", dict(size=7, bold=True, color=MUTED)),
            (quoi, dict(size=8, color=NAVY, space_before=3, line_spacing=1.2)),
        ])
    return s


def slide_kpis_mise_en_place(prs):
    s = content_slide(prs, "Trajectoire", "KPIs : comment on les met en place, concrètement", color=D.PALETTE[3])
    familles = [
        ("KPIs de mission", D.PALETTE[0], "iap-metrics-sre-finops-lead",
         "ServiceNow/Jira/CMDB si accès (ExternalEvidence), sinon déclaratif — tagué DÉDUIT",
         "Continu, lu à chaque étape ②③⟲"),
        ("KPIs d'usage du module", D.PALETTE[1], "Le consultant, au fil des missions",
         "Journal de mission + rex-library.md",
         "Par mission, consolidé à MVP5"),
        ("Grille de maturité", D.PALETTE[3], "iap-strategy-lead",
         "Grille V3.2 repassée en atelier ou en interview",
         "T0 (① Assessment flash) puis chaque boucle ⟲"),
    ]
    top0 = CONTENT_TOP + 0.05
    row_h = 1.0
    name_w = 2.0
    for i, (nom, color, owner, source, cadence) in enumerate(familles):
        y = top0 + i * (row_h + 0.12)
        D.add_rect(s, MARGIN, y, CONTENT_W, row_h, fill="#ffffff", line=LINE, line_w=0.75, rounded=True, radius=0.08)
        D.add_rect(s, MARGIN, y, 0.06, row_h, fill=color, rounded=True, radius=0.5)
        D.add_text(s, MARGIN + 0.2, y + 0.1, name_w, row_h - 0.2, [
            (nom, dict(size=8, bold=True, color=color, line_spacing=1.15)),
        ], anchor=MSO_ANCHOR.MIDDLE)
        colw = (CONTENT_W - 0.2 - name_w - 3 * 0.15) / 3
        specs = [("OWNER", owner), ("SOURCE DES DONNÉES", source), ("CADENCE", cadence)]
        for j, (label, val) in enumerate(specs):
            xj = MARGIN + 0.2 + name_w + 0.15 + j * (colw + 0.15)
            D.add_text(s, xj, y + 0.1, colw, row_h - 0.2, [
                (label, dict(size=7, bold=True, color=MUTED)),
                (val, dict(size=8, color=NAVY, space_before=3, line_spacing=1.15)),
            ], anchor=MSO_ANCHOR.MIDDLE)

    note_top = top0 + 3 * row_h + 2 * 0.12 + 0.15
    note_h = min(0.85, CONTENT_BOTTOM - note_top)
    D.add_rect(s, MARGIN, note_top, CONTENT_W, note_h, fill=TRACK, rounded=True, radius=0.08)
    D.add_text(s, MARGIN + 0.2, note_top, CONTENT_W - 0.4, note_h, [
        ("Pas d'instrumentation automatique en MVP1", dict(size=8, bold=True, color=NAVY)),
        ("Cohérent avec le Niveau A/B assumé (§Ambition de l'outil) : recueil et rapport à la main "
         "tant qu'aucun tableau de bord temps réel n'est promis avant le Niveau C.",
         dict(size=8, color=MUTED, space_before=3, line_spacing=1.2)),
    ], anchor=MSO_ANCHOR.MIDDLE)
    return s


def slide_kpis_exemple(prs):
    s = content_slide(prs, "Trajectoire", "KPIs en pratique : le cas nominal RUN massif, avant/après", color=D.PALETTE[3])
    D.add_text(s, MARGIN, CONTENT_TOP, CONTENT_W, 0.28, [
        ("Même fixture illustrative que le cas nominal export markdown (chapitre Trajectoire) — pas un client réel.",
         dict(size=8, color=MUTED, italic=True)),
    ])
    col_widths = [2.85, 1.75, 1.85, 1.725]
    headers = ["KPI", "T0 · ① ASSESSMENT FLASH", "T+6-12 MOIS · ⟲ RÉÉVALUATION", "TAG"]
    xs = []
    cx = MARGIN
    for cw in col_widths:
        xs.append(cx)
        cx += cw + 0.12

    header_y = CONTENT_TOP + 0.4
    for x, w, label in zip(xs, col_widths, headers):
        # _header_cell : le "⟲" de « T+6-12 MOIS · ⟲ RÉÉVALUATION » serait un
        # tofu en gras (cf. _GLYPHES_SANS_GRAS) — posé bold=False pour ce seul
        # caractère, le reste du libellé reste en gras.
        _header_cell(s, x, header_y, w, 0.24, label, size=7, color=MUTED, bold=True)

    tagcolor = {"CONFIRMÉ": SEVERITE[0], "DÉDUIT": SEVERITE[2], "—": MUTED}
    rows = [
        ("Pilier Agentic Readiness", "[1] — process pas assez explicite",
         "[2] — process explicite, rôles définis", "CONFIRMÉ"),
        ("Tickets récurrents évités / mois", "0", "≈ 15", "DÉDUIT"),
        ("Temps de triage moyen / ticket", "25 min", "12 min", "DÉDUIT"),
        ("Recommandation associée", "Documentation-first (runbook)",
         "Agentic-implementation (même fichier amendé)", "—"),
    ]
    row_top = header_y + 0.32
    row_h = 0.62
    row_gap = 0.08
    for i, (kpi, t0, t1, tag) in enumerate(rows):
        y = row_top + i * (row_h + row_gap)
        D.add_rect(s, MARGIN, y + row_h, CONTENT_W, 0.012, fill=LINE)
        D.add_text(s, xs[0], y, col_widths[0], row_h, [
            (kpi, dict(size=8, bold=True, color=NAVY, line_spacing=1.15)),
        ], anchor=MSO_ANCHOR.MIDDLE)
        D.add_text(s, xs[1], y, col_widths[1], row_h, [
            (t0, dict(size=8, color=NAVY, line_spacing=1.15)),
        ], anchor=MSO_ANCHOR.MIDDLE)
        D.add_text(s, xs[2], y, col_widths[2], row_h, [
            (t1, dict(size=8, color=NAVY, line_spacing=1.15)),
        ], anchor=MSO_ANCHOR.MIDDLE)
        if tag == "—":
            D.add_text(s, xs[3], y, col_widths[3], row_h, [
                (tag, dict(size=8, color=MUTED, align=PP_ALIGN.CENTER)),
            ], anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
        else:
            chip(s, xs[3], y + row_h / 2 - 0.13, min(1.1, col_widths[3]), 0.26, tag, tagcolor[tag], size=7)

    note_top = row_top + 4 * row_h + 3 * row_gap + 0.15
    note_h = min(0.6, CONTENT_BOTTOM - note_top)
    D.add_text(s, MARGIN, note_top, CONTENT_W, note_h, [
        ("Le point à retenir n'est pas l'ampleur des chiffres (fixture, pas une preuve) mais la "
         "discipline de mesure : même instrument aux deux instants, tag de confiance explicite, et "
         "un KPI de maturité qui déclenche directement le changement de recommandation.",
         dict(size=8, color=MUTED, italic=True, line_spacing=1.25)),
    ])
    return s


# --- Nouveau (brainstorm) : rendre tangible, dès le chapitre Cadrage, ce que
# "piste agentique" veut dire concrètement — 3 candidats illustratifs ancrés
# sur des familles de gaspillage déjà cadrées (§Traitement des gaspillages),
# pas des exemples inventés hors cadre. Même code couleur que les familles de
# gaspillage sur la slide dédiée (Méthode) : RUN=rouge, Financier=or,
# Cognitif=violet — cohérence intentionnelle, pas un hasard de palette.
def slide_agent_ia(prs, titre, nom_agent, famille, why, what, gain, color, note=None):
    s = content_slide(prs, "Cadrage", titre, color=D.PALETTE[0])
    D.add_text(s, MARGIN, CONTENT_TOP, CONTENT_W, 0.45, [
        (nom_agent, dict(size=D.TYPE["h3"], bold=True, color=color)),
        (f"Gaspillage {famille}", dict(size=8, color=MUTED, italic=True, space_before=2)),
    ])
    top0 = CONTENT_TOP + 0.55
    bands = [
        ("POURQUOI", why),
        ("CE QUE FAIT L'AGENT", what),
        ("GAIN", gain),
    ]
    txt_size = 9
    line_h = txt_size * 1.25 / 72.0
    usable = CONTENT_W - 0.44
    # Chaque bandeau plafonné à SON contenu — le bandeau GAIN (souvent 1 ligne)
    # ne garde plus la hauteur fixe d'un bandeau à 2 lignes (défaut « panneau
    # sur-étiré » constaté slides 10/11) — puis les 3 bandeaux sont répartis
    # pour remplir la zone, donc pas de vide résiduel en bas non plus.
    heights = [0.42 + _lignes(t, usable, txt_size) * line_h for _, t in bands]
    n = len(bands)
    region_bot = CONTENT_BOTTOM - (0.5 if note else 0.0)
    total = sum(heights)
    gap = max(0.10, min(0.5, (region_bot - top0 - total) / (n - 1)))
    y = top0
    last_bottom = top0
    for i, (label, texte) in enumerate(bands):
        h = heights[i]
        D.add_rect(s, MARGIN, y, CONTENT_W, h, fill="#ffffff", line=LINE, line_w=0.75, rounded=True, radius=0.08)
        D.add_rect(s, MARGIN, y, 0.06, h, fill=color, rounded=True, radius=0.5)
        D.add_text(s, MARGIN + 0.22, y + 0.12, CONTENT_W - 0.44, h - 0.24, [
            (label, dict(size=7, bold=True, color=color)),
            (texte, dict(size=txt_size, color=NAVY, space_before=4, line_spacing=1.25)),
        ])
        last_bottom = y + h
        y = last_bottom + gap

    if note:
        note_top = last_bottom + 0.16
        note_h = min(0.45, CONTENT_BOTTOM - note_top)
        D.add_text(s, MARGIN, note_top, CONTENT_W, note_h, [
            (note, dict(size=8, color=MUTED, italic=True, line_spacing=1.2)),
        ])
    return s


# --- Nouveau (brainstorm) : la formule de priorisation (slide précédente du
# chapitre Méthode) cite "prudence IA" sans jamais l'expliquer — corrige ça
# avant que l'exemple chiffré (slide suivante) ne s'en serve.
def slide_prudence_ia(prs):
    s = content_slide(prs, "Méthode", "La prudence IA est un frein chiffré, pas un veto", color=D.PALETTE[1])
    D.add_text(s, MARGIN, CONTENT_TOP, CONTENT_W, 0.4, [
        ("Prudence IA = confidentialité + besoin de supervision + criticité de la décision",
         dict(size=D.TYPE["small"], bold=True, color=NAVY, line_spacing=1.2)),
    ])

    facteurs = [
        ("CONFIDENTIALITÉ", D.PALETTE[0],
         "Reprend directement la classification du gate IA (D0-D4, chapitre Cadrage) — "
         "plus la donnée est sensible, plus le score monte."),
        ("BESOIN DE SUPERVISION", D.PALETTE[3],
         "Le palier d'adoption visé (assisté / supervisé / délégué) — un agent encore "
         "au stade assisté pèse plus lourd qu'un agent déjà éprouvé."),
        ("CRITICITÉ DE LA DÉCISION", D.PALETTE[2],
         "L'impact d'une erreur si l'agent se trompe seul — une recommandation "
         "réversible pèse moins qu'une décision irréversible."),
    ]
    top0 = CONTENT_TOP + 0.55
    n = 3
    card_h = 1.55
    for i, (label, color, texte) in enumerate(facteurs):
        x, w = col_x(i, n)
        D.add_card(s, x, top0, w, card_h, color)
        pad = 0.16
        D.add_text(s, x + pad, top0 + 0.14, w - 2 * pad, 0.4, [
            (label, dict(size=8, bold=True, color=color, line_spacing=1.1)),
        ])
        D.add_text(s, x + pad, top0 + 0.55, w - 2 * pad, card_h - 0.65, [
            (texte, dict(size=8, color=NAVY, line_spacing=1.25)),
        ])

    note_top = top0 + card_h + 0.18
    note_h = min(1.15, CONTENT_BOTTOM - note_top)
    D.add_rect(s, MARGIN, note_top, CONTENT_W, note_h, fill=NAVY, rounded=True, radius=0.08)
    D.add_text(s, MARGIN + 0.22, note_top, CONTENT_W - 0.44, note_h, [
        ("Un frein, pas un veto automatique", dict(size=D.TYPE["tiny"], bold=True, color="#ffffff")),
        ("Le score est SOUSTRAIT de impact × faisabilité — un candidat facile et à fort "
         "impact peut quand même être écarté si sa prudence IA est trop haute (cf. l'exemple "
         "chiffré, slide suivante). Le score ne remplace pas l'arbitrage humain : il le rend "
         "explicite. Avancer malgré un score élevé reste possible, mais se documente comme une "
         "décision à part entière (même discipline que la dérogation du gate DevOps).",
         dict(size=8, color="#c7cbe0", space_before=3, line_spacing=1.25)),
    ], anchor=MSO_ANCHOR.MIDDLE)
    return s


# --- Nouveau (brainstorm) : comment le tronc commun se branche concrètement
# sur le SI du client, et ce que ça change selon le niveau d'ambition déjà
# cadré (slide précédente) — synthèse d'éléments déjà posés (§Ambition de
# l'outil, §Solution technique envisagée), pas une nouvelle doctrine.
def slide_architecture_si(prs):
    s = content_slide(prs, "Trajectoire",
                       "Le lien avec le SI du client change avec le niveau d'ambition, pas la méthode",
                       color=D.PALETTE[3])
    headers = ["NIVEAU", "SOURCES", "MODE DE CONNEXION", "LIVRABLES"]
    col_widths = [1.1, 2.55, 2.75, 1.95]
    xs = []
    cx = MARGIN
    for cw in col_widths:
        xs.append(cx)
        cx += cw + 0.1

    header_y = CONTENT_TOP + 0.05
    for x, w, label in zip(xs, col_widths, headers):
        D.add_text(s, x, header_y, w, 0.22, [
            (label, dict(size=7, bold=True, color=MUTED)),
        ])

    rows = [
        ("A", D.PALETTE[0], "Aide au coach",
         "Exports ponctuels (ServiceNow/Jira), interviews",
         "Aucune — tout est apporté par le consultant",
         "Markdown + deck, à la demande"),
        ("B", D.PALETTE[3], "Assistant interactif",
         "Exports + App companion (capture terrain)",
         "Website centralise, orchestration assistée",
         "+ tableau de bord multi-engagements"),
        ("C", D.PALETTE[2], "Companion connecté (non engagé)",
         "ServiceNow/Jira/Confluence/Datadog/CMDB/FinOps",
         "Connecteurs API directs, en continu",
         "Livrables mis à jour en continu"),
    ]
    row_top = header_y + 0.3
    row_h = 1.05
    row_gap = 0.1
    for i, (code, color, niveau, sources, connexion, livrables) in enumerate(rows):
        y = row_top + i * (row_h + row_gap)
        D.add_rect(s, MARGIN, y, CONTENT_W, row_h, fill="#ffffff", line=LINE, line_w=0.75, rounded=True, radius=0.08)
        D.add_rect(s, MARGIN, y, 0.06, row_h, fill=color, rounded=True, radius=0.5)
        D.add_text(s, xs[0] + 0.12, y, col_widths[0] - 0.12, row_h, [
            (code, dict(size=D.TYPE["h3"], bold=True, color=color)),
            (niveau, dict(size=7, color=MUTED, space_before=2, line_spacing=1.1)),
        ], anchor=MSO_ANCHOR.MIDDLE)
        D.add_text(s, xs[1], y, col_widths[1] - 0.1, row_h, [
            (sources, dict(size=8, color=NAVY, line_spacing=1.2)),
        ], anchor=MSO_ANCHOR.MIDDLE)
        D.add_text(s, xs[2], y, col_widths[2] - 0.1, row_h, [
            (connexion, dict(size=8, color=NAVY, line_spacing=1.2)),
        ], anchor=MSO_ANCHOR.MIDDLE)
        D.add_text(s, xs[3], y, col_widths[3] - 0.1, row_h, [
            (livrables, dict(size=8, color=NAVY, line_spacing=1.2)),
        ], anchor=MSO_ANCHOR.MIDDLE)

    note_top = row_top + 3 * row_h + 2 * row_gap + 0.15
    note_h = min(0.5, CONTENT_BOTTOM - note_top)
    D.add_text(s, MARGIN, note_top, CONTENT_W, note_h, [
        ("Le niveau C suppose un accès direct aux données de production du client — un cabinet "
         "peut durablement rester au niveau A ou B par choix de gouvernance (slide précédente).",
         dict(size=8, color=MUTED, italic=True, line_spacing=1.25)),
    ])
    return s


# --- Nouveau (réouverture de périmètre, arbitrage 2026-07-21) : l'architecture
# des 11 agents-workflows (§Workflows, ligne 587+), délibérément retirée du deck
# au commit 4f0c9b7, est rouverte sur ce seul point. COMPLÉMENTAIRE de
# slide_schema_fonctionnement (le FLUX de données Collecte→Diagnostic→Conception
# →Restitution, avec flèches) : ici c'est l'INVENTAIRE des composants — les 11
# agents nommés, regroupés par étape en cartes (pas de flèches), le gate
# confidentialité posé comme un socle transversal et bloquant. Couleurs des
# familles reprises de slide_schema_fonctionnement (Diagnostic=violet,
# Conception=or, etc.) — cohérence inter-slides voulue, pas un hasard. Ouvre le
# chapitre Trajectoire : on présente les composants avant leur mise en œuvre.
def slide_architecture_agents(prs):
    s = content_slide(prs, "Trajectoire",
                       "Onze agents spécialisés, un seul bloquant : le gate confidentialité les traverse tous",
                       color=D.PALETTE[3])
    D.add_text(s, MARGIN, CONTENT_TOP, CONTENT_W, 0.5, [
        ("Un mandat unique par agent, regroupés par étape. Le gate confidentialité est le seul "
         "à pouvoir arrêter la chaîne — transversal, il précède tout usage d'un modèle IA sur "
         "donnée client.", dict(size=8, color=MUTED, italic=True, line_spacing=1.2)),
    ])

    familles = [
        ("INTAKE", D.PALETTE[0], [
            ("iap-intake",
             "Qualifie le contexte client, le positionne sur les deux échelles de maturité, "
             "puis choisit le chemin de mission : diagnostic, pilote, adoption ou gate d'abord."),
        ]),
        ("DIAGNOSTIC", D.PALETTE[4], [
            ("iap-diagnostic-systemique", "Structure, flux, RUN, posture management"),
            ("iap-discovery-gaspillage", "Preuves, causes racines, options de traitement"),
        ]),
        ("CONCEPTION", D.PALETTE[3], [
            ("iap-waste-treatment", "Backlog priorisé et scoré des gaspillages"),
            ("iap-product-definition", "Personas, capacités, valeur, roadmap"),
            ("iap-operating-model", "Rôles, gouvernance, financement (ADR)"),
            ("iap-agentic-opportunities", "Le gaspillage d'abord, l'IA ensuite"),
        ]),
        ("ADOPTION & RESTITUTION", D.PALETTE[1], [
            ("iap-adoption-plan", "Onboarding, documentation, communautés"),
            ("iap-scenario-playbook", "Adapte la démarche au scénario client"),
            ("iap-deck-builder", "Deck modulaire, restitution exécutive"),
        ]),
    ]
    n = len(familles)
    # Cartes de MÊME hauteur (cadence sur la colonne la plus fournie, CONCEPTION
    # à 4 agents) — mais au lieu d'un slot fixe aligné en haut qui laissait un
    # grand vide sous l'agent unique d'INTAKE, chaque colonne RÉPARTIT ses agents
    # sur toute la zone : chaque bloc-agent est dimensionné à SON texte, puis les
    # blocs sont espacés (space-between) pour couvrir la hauteur — colonne à 4 =
    # remplie ; colonne à 2-3 = espacée régulièrement ; colonne à 1 = centrée. La
    # rangée se lit ainsi « équilibrée » (cf. brief ppt-designer, défaut INTAKE).
    top0 = CONTENT_TOP + 0.6
    gate_h = 0.6
    note_h = 0.36
    card_h = CONTENT_BOTTOM - top0 - 0.15 - gate_h - 0.12 - note_h
    _, wcol = col_x(0, n)
    pad = 0.14
    usable_col = wcol - 2 * pad
    region_top = top0 + 0.52
    region_h = card_h - 0.52 - 0.08
    for i, (nom, color, agents) in enumerate(familles):
        x, w = col_x(i, n)
        D.add_card(s, x, top0, w, card_h, color)
        D.add_text(s, x + pad, top0 + 0.12, w - 2 * pad, 0.36, [
            (nom, dict(size=8, bold=True, color=color, line_spacing=1.0)),
            (f"{len(agents)} agent" + ("s" if len(agents) > 1 else ""),
             dict(size=6.5, color=MUTED, space_before=1)),
        ])
        blocs = [0.16 + _lignes(role, usable_col, 6.5) * (6.5 * 1.15 / 72.0)
                 for _, role in agents]
        na = len(agents)
        total = sum(blocs)
        if na == 1:
            gap_a = 0.0
            start = region_top  # top-align le bloc unique (INTAKE) sous l'en-tête : le centrer le faisait flotter (défaut « panneau flottant », cf. revue 2026-07-21)
        else:
            gap_a = min(0.5, (region_h - total) / (na - 1))
            span = total + gap_a * (na - 1)
            start = region_top + max(0.0, (region_h - span) / 2)
        ay = start
        for j, (agent, role) in enumerate(agents):
            D.add_text(s, x + pad, ay, w - 2 * pad, blocs[j], [
                (agent, dict(size=7, bold=True, color=NAVY, line_spacing=1.0)),
                (role, dict(size=6.5, color=MUTED, space_before=2, line_spacing=1.1)),
            ], anchor=MSO_ANCHOR.TOP)
            ay += blocs[j] + gap_a

    gate_top = top0 + card_h + 0.15
    D.add_rect(s, MARGIN, gate_top, CONTENT_W, gate_h, fill=NAVY, rounded=True, radius=0.1)
    chip_w = 1.15
    chip(s, MARGIN + 0.16, gate_top + gate_h / 2 - 0.14, chip_w, 0.28, "BLOQUANT", SEVERITE[4], size=7)
    D.add_text(s, MARGIN + 0.16 + chip_w + 0.2, gate_top + 0.1, CONTENT_W - chip_w - 0.55, gate_h - 0.2, [
        ("iap-ai-data-confidentiality-gate", dict(size=8, bold=True, color="#ffffff")),
        ("Classe les données (D0-D4), décide le mode d'exécution IA et pose les garde-fous — "
         "transversal, avant tout usage d'un modèle IA sur donnée client.",
         dict(size=7.5, color="#c7cbe0", space_before=2, line_spacing=1.15)),
    ], anchor=MSO_ANCHOR.MIDDLE)

    note_top = gate_top + gate_h + 0.12
    note_h_real = min(note_h, CONTENT_BOTTOM - note_top)
    D.add_text(s, MARGIN, note_top, CONTENT_W, note_h_real, [
        ("Onze mandats distincts, un seul peut arrêter la chaîne — tous les autres proposent et "
         "produisent, la décision finale reste humaine.",
         dict(size=8, color=MUTED, italic=True, line_spacing=1.2)),
    ])
    return s


def build():
    prs = new_prs()
    slide_cover(prs)
    slide_executive_summary(prs)
    slide_vision_ia(prs)

    slide_chapitre(prs, "01", "Cadrage", "Mission, doctrine, gate IA, maturité, personas",
                   D.PALETTE[0], "mountains")
    slide_mission(prs)
    slide_gate_ia(prs)
    slide_maturite(prs)
    slide_personas(prs)
    slide_personas_divergences(prs)
    slide_agent_ia(
        prs, "Un agent de triage peut absorber le gaspillage RUN le plus répétitif",
        "Agent de triage de tickets", "RUN",
        "Les mêmes types de tickets reviennent depuis des années et mobilisent des experts "
        "seniors sur un travail répétitif à faible valeur — le gaspillage RUN le plus classique.",
        "Lit chaque ticket entrant, le classe selon un runbook déjà documenté et le route vers "
        "la bonne équipe. Le processus doit être explicite avant l'agent (préalable non "
        "négociable, §Modèles d'équipe) — jamais l'inverse.",
        "Capacité RUN récupérée : dans le cas nominal du cadrage, jusqu'à 15 tickets/mois "
        "traités sans intervention humaine, temps de triage divisé par deux.",
        D.PALETTE[2])
    slide_agent_ia(
        prs, "Un agent de veille FinOps rend le décommissionnement continu, pas ponctuel",
        "Agent de veille FinOps", "Financier",
        "Les ressources cloud surdimensionnées ou orphelines ne sont détectées qu'à l'occasion "
        "d'audits ponctuels — le gaspillage s'accumule entre deux revues manuelles.",
        "Scanne en continu la CMDB et la facturation cloud, détecte les ressources inactives ou "
        "surdimensionnées, et propose une liste de décommissionnement à valider — ne décommissionne "
        "jamais seul.",
        "Coût récupéré et directement mesurable (ressources décommissionnées par mois) — un KPI "
        "de mission déjà cadré, pas à inventer.",
        D.PALETTE[3])
    slide_agent_ia(
        prs, "Un agent documentaire réduit la charge cognitive sans remplacer l'expert",
        "Agent documentaire (RAG)", "Cognitif",
        "Trop d'outils, procédures dispersées : la charge cognitive pour retrouver l'information "
        "ralentit les équipes et sollicite en permanence les mêmes experts.",
        "Indexe la documentation existante (runbooks, wikis, tickets résolus) et répond aux "
        "questions fréquentes avec la source citée — jamais une réponse sans preuve.",
        "Charge cognitive réduite, onboarding plus rapide, moins d'interruptions des experts "
        "seniors pour des questions déjà documentées.",
        D.PALETTE[4],
        note=("Ces 3 candidats restent soumis au même scoring (chapitre Méthode) et au gate IA "
              "(ci-dessus) avant toute décision — des exemples illustratifs, pas une liste actée."))

    slide_chapitre(prs, "02", "Méthode", "Traitement des gaspillages, exemples chiffrés, modèles d'équipe",
                   D.PALETTE[1], "forest")
    slide_gaspillages(prs)
    slide_prudence_ia(prs)
    slide_exemple_priorisation(prs)
    slide_exemple_diagnostic(prs)
    slide_exemple_recommandation(prs)
    slide_team_topologies(prs)

    slide_chapitre(prs, "03", "Trajectoire", "Architecture des agents, mise en œuvre, livrables, ambition, KPIs",
                   D.PALETTE[3], "ocean", seed=0)
    slide_architecture_agents(prs)
    slide_schema_fonctionnement(prs)
    slide_trajectoire(prs)
    slide_schema_bout_en_bout(prs)
    slide_livrables_ppt(prs)
    slide_export_markdown(prs)
    slide_ambition(prs)
    slide_architecture_si(prs)
    slide_kpis(prs)
    slide_kpis_pourquoi_quoi(prs)
    slide_kpis_mise_en_place(prs)
    slide_kpis_exemple(prs)

    problemes = D.verifier_geometrie(prs)
    if problemes:
        print(f"GEOMETRIE: {len(problemes)} probleme(s)")
        for p in problemes:
            print(" -", p)
    else:
        print("GEOMETRIE: OK — aucune forme hors cadre")

    out = os.path.join(os.path.dirname(__file__), "bmad-iap-cadrage-synthese.pptx")
    prs.save(out)
    print("Ecrit:", out)
    return problemes


if __name__ == "__main__":
    problemes = build()
    sys.exit(1 if problemes else 0)
