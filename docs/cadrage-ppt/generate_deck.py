"""Génère une synthèse PPT (44 slides) des RÉSULTATS du cadrage BMAD IAP
(docs/bmad-iap-cadrage.md) à partir des helpers pptx_deck, dessinée
PAR-DESSUS le vrai template de marque OCTO (template-octo.pptx) —
masters/layouts/thème conservés, pas un deck sur canevas vierge.

Structure v2.5 en 8 chapitres, sur le fil rouge narratif des decks SCALE
(docs/Import/notes-extraction-scale.md : POURQUOI → QUI → QUOI → COMMENT →
RÉSULTAT) : 01 Contexte (pourquoi) · 02 Personas (qui) · 03 Besoins & douleurs
(le pourquoi, mesuré) · 04 Proposition (quoi — thèse `why_iap` en ouverture,
méthode scorée, sous-chapitre « Exemples » introduit par `slide_sous_chapitre`)
· 05 IA (le quoi, côté IA — sous gate) · 06 Démarche (comment — trajectoire
fusionnée avec la vue bout-en-bout, fil humain, schéma de fonctionnement,
inventaire des agents, livrables, conditions de réussite) · 07 Outillage IAP
(avec quoi — ce que le module met dans les mains du consultant, ambition A/B/C,
lien SI) · 08 KPI (la preuve — 3 familles → mise en place → grille de maturité
→ cas chiffré, clôture). L'IA reste tirée APRÈS la proposition (doctrine :
« l'IA amplifie l'organisation, elle n'est jamais la réponse à un problème
d'abord organisationnel ») ; la Démarche vient APRÈS l'IA pour que le
« comment » enchaîne directement sur l'outillage puis la preuve.
L'executive summary (slide 2) reprend le même fil en 4 blocs
POURQUOI/QUOI/COMMENT/RÉSULTAT avec renvoi aux chapitres.

Séparateurs : chapitres = intercalaire teardrop (photo + numéro, layout dédié) ;
sous-chapitres = `slide_sous_chapitre` (bloc-titre léger, sans photo ni numéro).

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
# Un code couleur par chapitre, passé explicitement à chaque appel de
# content_slide() ET repris sur l'intercalaire du chapitre (v2.5, 8 chapitres) :
#   01 Contexte           = D.PALETTE[0]  (bleu)
#   02 Personas           = D.PALETTE[5]  (teal)
#   03 Besoins & douleurs = D.PALETTE[2]  (rouge)
#   04 Proposition        = D.PALETTE[1]  (vert)
#   05 IA                 = D.PALETTE[4]  (violet)
#   06 Démarche           = D.PALETTE[3]  (or)
#   07 Outillage IAP      = D.PALETTE[5]  (teal — réutilisé, comme KPI réutilise le bleu)
#   08 KPI                = D.PALETTE[0]  (bleu)


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


def slide_sous_chapitre(prs, kicker, titre, sous_titre, color):
    """Séparateur de SOUS-chapitre (léger) : PAS l'intercalaire teardrop des
    chapitres (layout dédié + photo), juste un bloc-titre de section sur le layout
    « titre seul ». Introduit un groupe logique DANS un chapitre — ici « Exemples »
    dans la Proposition (points ②/③ : l'arbitrage « kicker seul, pas d'intercalaire »
    est levé pour ce groupe, à la demande). Reste plus léger qu'un chapitre : pas de
    numéro, pas de photo, garde le pied de page du master."""
    layout = prs.slide_masters[0].slide_layouts[LAYOUT_TITRE_SEUL]
    s = prs.slides.add_slide(layout)
    # Vider le placeholder titre (sinon prompt résiduel) — on pose notre propre bloc.
    s.shapes.placeholders[0].text_frame.text = ""
    bar_top, bar_h = 2.05, 1.55
    D.add_rect(s, MARGIN, bar_top, 0.14, bar_h, fill=color, rounded=True, radius=0.5)
    tx = MARGIN + 0.45
    tw = CONTENT_W - 0.45
    D.add_text(s, tx, bar_top, tw, bar_h, [
        (kicker.upper() + "  ·  SOUS-CHAPITRE",
         dict(size=D.TYPE["tiny"], bold=True, color=color, line_spacing=1.0)),
        (titre, dict(size=34, bold=True, color=NAVY, space_before=8, line_spacing=1.0)),
        (sous_titre, dict(size=D.TYPE["small"], color=MUTED, italic=True, space_before=12, line_spacing=1.2)),
    ], anchor=MSO_ANCHOR.MIDDLE)
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
    # Chapitres à photo (restructuration 7 chapitres) : scènes réelles distinctes,
    # VÉRIFIÉES au rendu réel — une requête mot-clé n'a aucun jugement (cf. « plage
    # bondée », « desert dune » seed 0 → fossile de musée, « winding river » →
    # cloître de monastère), donc chaque photo est validée à l'œil (fetch du _brut
    # puis lecture image avant câblage). Le repli nature_images (procédural) ne se
    # déclenche que si Openverse est indisponible (SSL/0-résultat) ET que le nom de
    # scène est connu du fallback (forest/meadow/mountains/ocean/sunset/tropical) —
    # sinon le générateur PLANTE (ValueError unknown scene). Préférer une vraie photo
    # à du procédural ; cf. mémoire reference-deck-image-fetcher.
    #   dunes  (Proposition) = vue aérienne NASA ; nightsky (IA) = astrophoto ;
    #   canyon (Démarche)    = strates de roche (nom NEUF → repli qui PLANTE, comme
    #                          dunes/nightsky : dépend d'un vrai fetch) ;
    #   meadow (KPI, seed 1) = asters/verges d'or (nom CONNU du fallback → sûr).
    "dunes": "sand dunes",
    "nightsky": "starry night sky",
    "canyon": "canyon landscape",
    "meadow": "meadow wildflowers",
    # tropical (Outillage IAP, chapitre 07 — v2.5) : nom CONNU du fallback
    # procédural (forest/meadow/mountains/ocean/sunset/tropical), donc sûr même
    # hors ligne. Photo à VÉRIFIER au rendu réel comme les autres.
    "tropical": "tropical palm leaves",
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
    # v2.5 (2026-07-23) : restructuration 8 chapitres sur le fil rouge SCALE
    # (POURQUOI→QUI→QUOI→COMMENT→RÉSULTAT) — fusion trajectoire/bout-en-bout,
    # executive summary réancré sur le fil, nouveau chapitre Outillage IAP,
    # slide Conditions de réussite. (v2.4 : fil humain de la trajectoire.)
    phs[3].text_frame.text = "v2.5 · 2026-07-23"
    # Bandeau de métadonnées (statut/langue/confidentialité/sources) retiré sur
    # demande — la couverture ne garde que titre, sous-titre, entité et version.
    return s


# ---------------------------------------------------------------- slide 2
# Réancré (v2.5, chantier ②) sur le fil rouge narratif SCALE
# (docs/Import/notes-extraction-scale.md) : 4 blocs POURQUOI → QUOI → COMMENT →
# RÉSULTAT, chacun une claim d'une ligne + le renvoi aux chapitres — pattern 7
# du catalogue deck-design-library (« rangée de cartes sur bandeau, une en
# accent ») : le RÉSULTAT (la preuve, ce que le sponsor achète in fine) est la
# seule carte en fill navy plein.
def slide_executive_summary(prs):
    s = content_slide(prs, "Executive summary",
                       "Du pourquoi à la preuve : une transformation cadrée de bout en bout")

    headline_h = 0.62
    D.add_text(s, MARGIN, CONTENT_TOP, CONTENT_W, headline_h, [
        ("Transformer l'infrastructure en plateforme opérée comme un produit, ET traiter "
         "structurellement le gaspillage qui l'en empêche — le deck suit le fil : pourquoi, "
         "qui, quoi, comment, avec quoi, la preuve.",
         dict(size=D.TYPE["small"], color=NAVY, italic=True, line_spacing=1.3)),
    ])

    items = [
        ("POURQUOI", D.PALETTE[0], "L'infra subie coûte de plus en plus cher.",
         "Trois déclencheurs, quatre personas interrogés séparément, des douleurs "
         "mesurables plutôt que des plaintes.",
         "Chapitres 01–03"),
        ("QUOI", D.PALETTE[1], "Traiter l'infra comme un produit — et assainir.",
         "Double mission, méthode scorée (impact × faisabilité − prudence IA), IA sous "
         "gate : jamais la réponse à un problème d'abord organisationnel.",
         "Chapitres 04–05"),
        ("COMMENT", D.PALETTE[3], "Trois temps et une boucle, personnes comprises.",
         "Démarche ①②③⟲ avec son fil humain de bout en bout ; l'outillage IAP au "
         "service de la démarche — jamais l'inverse.",
         "Chapitres 06–07"),
        ("RÉSULTAT", NAVY, "Le delta instrumenté T0 → réévaluation.",
         "Trois familles de KPIs, même instrument aux deux instants — la preuve, "
         "pas une opinion.",
         "Chapitre 08"),
    ]
    n = len(items)
    pad = 0.16
    _, cw = col_x(0, n)
    usable = cw - 2 * pad
    desc_size = 8
    line_h = desc_size * 1.3 / 72.0
    claim_h = max(_lignes(c, usable, 9) for _, _, c, _, _ in items) * (9 * 1.2 / 72.0) + 0.06
    desc_h = max(_lignes(d, usable, desc_size) for _, _, _, d, _ in items) * line_h + 0.06
    # étages : label (0.24) + claim + desc + renvoi chapitres (0.26) + respirations
    card_h = 0.14 + 0.24 + claim_h + 0.10 + desc_h + 0.14 + 0.26 + 0.14
    top0 = CONTENT_TOP + headline_h + 0.30
    # bandeau de fond commun (pattern 7) : regroupe les 4 blocs en un seul
    # « bloc de lecture » — le fil se lit d'un trait, flèches dans les inter-colonnes.
    D.add_rect(s, MARGIN - 0.08, top0 - 0.16, CONTENT_W + 0.16, card_h + 0.32,
               fill=TRACK, rounded=True, radius=0.06)
    for i, (etape, color, claim, desc, renvoi) in enumerate(items):
        x, w = col_x(i, n)
        accent = (etape == "RÉSULTAT")   # « un sur N » : la preuve
        if accent:
            D.add_rect(s, x, top0, w, card_h, fill=NAVY, rounded=True, radius=0.08)
        else:
            D.add_rect(s, x, top0, w, card_h, fill="#ffffff", line=LINE, line_w=0.75,
                       rounded=True, radius=0.08)
        D.add_text(s, x + pad, top0 + 0.14, w - 2 * pad, 0.24, [
            (etape, dict(size=8, bold=True, color="#8fd6db" if accent else color)),
        ])
        D.add_text(s, x + pad, top0 + 0.38, w - 2 * pad, claim_h, [
            (claim, dict(size=9, bold=True, color="#ffffff" if accent else NAVY,
                         line_spacing=1.2)),
        ])
        D.add_text(s, x + pad, top0 + 0.38 + claim_h + 0.10, w - 2 * pad, desc_h, [
            (desc, dict(size=desc_size, color="#c7cbe0" if accent else MUTED,
                        line_spacing=1.3)),
        ])
        D.add_text(s, x + pad, top0 + card_h - 0.38, w - 2 * pad, 0.26, [
            (renvoi, dict(size=7.5, bold=True, color="#8fd6db" if accent else
                          (D.PALETTE[0] if etape == "RÉSULTAT" else color))),
        ], anchor=MSO_ANCHOR.BOTTOM)
        if i < n - 1:   # le fil : flèche dans l'inter-colonne
            D.add_text(s, x + w - 0.02, top0 + card_h / 2 - 0.12, GAP + 0.04, 0.24, [
                ("→", dict(size=11, bold=True, color=MUTED, align=PP_ALIGN.CENTER)),
            ], anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
    return s


# ---------------------------------------------------------------- slide 3
def slide_mission(prs):
    s = content_slide(prs, "Contexte", "Une double mission : transformer ET assainir", color=D.PALETTE[0])
    cards = [
        ("TRANSFORMER", D.PALETTE[0],
         "Cible produit/plateforme : utilisateurs identifiés, valeur, roadmap, "
         "engagements de qualité, gouvernance lisible.",
         "La vision à moyen terme — ce que le sponsor achète."),
        ("ASSAINIR", D.PALETTE[2],
         "Traitement mesurable des gaspillages : flux, RUN, humain, financier, "
         "cognitif, décisionnel, environnemental, IA.",
         # v2.3 : promesse instrumentée, pas un acquis — même honnêteté que le
         # statut interne du cadrage (fin du double discours, finding C1).
         "La capacité récupérée finance la trajectoire produit — mécanisme "
         "instrumenté dès la première mission (KPI de réinvestissement)."),
    ]
    # v2.5 (chantier ③) : les cartes flottaient à CONTENT_TOP+0.5 sans rien
    # au-dessus (~0.5in de blanc sous le titre). La note « ni séquentiels ni
    # optionnels » devient le CHAPEAU (à CONTENT_TOP), les cartes suivent, et
    # la rangée de tensions gagne son étiquette — l'espace se redistribue dans
    # le contenu, pas en vide.
    chapeau_h = 0.5
    D.add_text(s, MARGIN, CONTENT_TOP, CONTENT_W, chapeau_h, [
        ("Deux piliers ni séquentiels ni optionnels : une cible produit sans traitement du "
         "gaspillage manque de capacité pour s'y déployer ; l'inverse reste une réduction "
         "de coûts sans vision.",
         dict(size=D.TYPE["small"], color=NAVY, italic=True, line_spacing=1.25)),
    ])
    card_h = 1.95
    top0 = CONTENT_TOP + chapeau_h + 0.12
    for i, (titre, color, vise, finance) in enumerate(cards):
        x, w = col_x(i, 2)
        D.add_card(s, x, top0, w, card_h, color)
        pad = 0.22
        D.add_text(s, x + pad, top0 + 0.18, w - 2 * pad, 0.3, [
            (titre, dict(size=D.TYPE["h3"], bold=True, color=color))
        ])
        D.add_text(s, x + pad, top0 + 0.58, w - 2 * pad, 0.62, [
            ("CE QU'IL VISE", dict(size=D.TYPE["tiny"], bold=True, color=MUTED)),
            (vise, dict(size=D.TYPE["tiny"], color=NAVY, space_before=2, line_spacing=1.25)),
        ])
        D.add_text(s, x + pad, top0 + 1.28, w - 2 * pad, 0.58, [
            ("CE QU'IL FINANCE", dict(size=D.TYPE["tiny"], bold=True, color=MUTED)),
            (finance, dict(size=D.TYPE["tiny"], color=NAVY, space_before=2, line_spacing=1.25)),
        ])

    label_top = top0 + card_h + 0.22
    D.add_text(s, MARGIN, label_top, CONTENT_W, 0.22, [
        ("L'ÉQUILIBRE QUE LA DOUBLE MISSION TIENT EN PERMANENCE",
         dict(size=7.5, bold=True, color=MUTED)),
    ])
    tens_top = label_top + 0.26
    tens_h = 0.62
    tensions = ["Efficacité du delivery", "Robustesse du RUN", "Valeur perçue (utilisateurs internes)"]
    for i, t in enumerate(tensions):
        x, w = col_x(i, 3)
        D.add_rect(s, x, tens_top, w, tens_h, fill=TRACK, rounded=True, radius=0.12)
        D.add_text(s, x + 0.1, tens_top, w - 0.2, tens_h, [
            (t, dict(size=D.TYPE["tiny"], bold=True, color=NAVY, align=PP_ALIGN.CENTER))
        ], anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
    return s


def slide_pourquoi_contexte(prs):
    """Nouveau (point ②) : dans le chapitre Contexte, le POURQUOI — pourquoi
    proposer cette transformation à un client infra, et maintenant. Trois
    déclencheurs + un pont trait-pour-trait vers la double mission (slide_mission)."""
    s = content_slide(prs, "Contexte",
                       "Pourquoi cette transformation, pour un client infra — et maintenant",
                       color=D.PALETTE[0])
    D.add_text(s, MARGIN, CONTENT_TOP, CONTENT_W, 0.5, [
        ("Trois bascules rendent l'Infra-as-a-Product pertinente — et urgente — pour un client "
         "dont l'infrastructure est encore vécue comme un centre de coûts et un guichet.",
         dict(size=D.TYPE["small"], color=NAVY, italic=True, line_spacing=1.25)),
    ])
    triggers = [
        (D.PALETTE[2], "L'infra subie n'est plus tenable",
         "RUN subi, experts seniors drainés sur du répétitif, gaspillage cloud non maîtrisé, "
         "plateforme contournée : le coût du statu quo ne cesse de monter."),
        (D.PALETTE[1], "Le modèle produit/plateforme est prouvé",
         "Platform engineering et product operating model ne sont plus un pari mais un "
         "standard : la cible est connue, outillée, reproductible."),
        (D.PALETTE[4], "L'IA rebat les cartes — l'organisation d'abord",
         "L'IA amplifie une organisation mûre, jamais l'inverse. S'y préparer maintenant "
         "(doctrine confidentialité-first) évite de la subir plus tard."),
    ]
    lead_h, bridge_h = 0.55, 0.72
    top0 = CONTENT_TOP + lead_h + 0.1
    card_h = (CONTENT_BOTTOM - bridge_h - 0.18) - top0
    pad = 0.22
    for i, (color, titre, corps) in enumerate(triggers):
        x, w = col_x(i, 3)
        D.add_card(s, x, top0, w, card_h, color)
        tx = x + 0.08 + pad
        tw = w - 0.08 - 2 * pad
        D.add_text(s, tx, top0 + 0.22, tw, card_h - 0.44, [
            (f"DÉCLENCHEUR {i + 1}", dict(size=6.5, bold=True, color=MUTED)),
            (titre, dict(size=D.TYPE["small"], bold=True, color=color, space_before=3, line_spacing=1.05)),
            (corps, dict(size=9, color=NAVY, space_before=8, line_spacing=1.25)),
        ])
    bridge_top = CONTENT_BOTTOM - bridge_h
    D.add_rect(s, MARGIN, bridge_top, CONTENT_W, bridge_h, fill=TRACK, rounded=True, radius=0.1)
    D.add_rect(s, MARGIN, bridge_top, 0.08, bridge_h, fill=D.PALETTE[0], rounded=True, radius=0.5)
    D.add_text(s, MARGIN + 0.28, bridge_top, CONTENT_W - 0.46, bridge_h, [
        ("Et surtout — nos deux missions répondent trait pour trait aux deux douleurs du client.",
         dict(size=8.5, bold=True, color=NAVY, line_spacing=1.05)),
        ("Subir le RUN → TRANSFORMER (cible produit/plateforme) ; le gaspillage → ASSAINIR "
         "(capacité récupérée réinvestie dans la trajectoire — mesuré par KPI).",
         dict(size=8, color=MUTED, space_before=2, line_spacing=1.15)),
    ], anchor=MSO_ANCHOR.MIDDLE)
    return s


# ---------------------------------------------------------------- slide 4
def slide_gate_ia(prs):
    s = content_slide(prs, "IA", "Les données du client gouvernent le choix du modèle IA", color=D.PALETTE[4])
    D.add_text(s, MARGIN, CONTENT_TOP, CONTENT_W, 0.35, [
        ("Checkpoint toujours humain avant tout usage IA sur données client — "
         "iap-ai-data-confidentiality-gate, quel que soit le mode d'exécution retenu.",
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
def slide_why_iap(prs):
    """Nouveau (point ⑤) : OUVRE le chapitre Proposition (la thèse). Le POURQUOI de
    l'Infra-as-a-Product — trois bascules produit, chacune ancrée sur un persona/une
    douleur déjà posés. (2e passe : la maturité est partie au chapitre KPI, le
    sous-chapitre « Technique IAP » a donc disparu — why_iap ouvre la Proposition.)"""
    s = content_slide(prs, "Proposition",
                       "Pourquoi « Infrastructure as a Product » — le socle de la proposition",
                       color=D.PALETTE[1])
    claim_h = 0.95
    D.add_rect(s, MARGIN, CONTENT_TOP, CONTENT_W, claim_h, fill=TRACK, rounded=True, radius=0.1)
    D.add_rect(s, MARGIN, CONTENT_TOP, 0.08, claim_h, fill=D.PALETTE[1], rounded=True, radius=0.5)
    D.add_text(s, MARGIN + 0.3, CONTENT_TOP, CONTENT_W - 0.5, claim_h, [
        ("Traiter l'infrastructure comme un produit, pas comme un guichet de tickets.",
         dict(size=14, bold=True, color=NAVY, line_spacing=1.05)),
        ("Un produit a des utilisateurs, un cycle de vie et une valeur mesurée — trois bascules "
         "qui répondent directement aux personas et à leurs douleurs.",
         dict(size=9, color=MUTED, space_before=4, line_spacing=1.15)),
    ], anchor=MSO_ANCHOR.MIDDLE)

    piliers = [
        (D.PALETTE[5], "Des utilisateurs, pas des tickets",
         "On conçoit l'adoption — self-service, onboarding, parcours — au lieu de subir un "
         "guichet que le contournement rend inutile.",
         "l'Utilisateur applicatif"),
        (D.PALETTE[0], "Un cycle de vie, une équipe qui en répond",
         "Le produit a un propriétaire, une roadmap et une dette gérée : on sort du RUN subi "
         "et on récupère de la capacité.",
         "Infra & RUN"),
        (D.PALETTE[3], "Un pilotage par la valeur",
         "On mesure l'usage et la valeur produite, pas l'activité : un signal de flux fiable, "
         "des KPIs de mission — pas du reporting-miroir.",
         "Management & Sponsor"),
    ]
    top = CONTENT_TOP + claim_h + 0.25
    card_h = CONTENT_BOTTOM - top
    pad = 0.22
    for i, (color, titre, corps, ancre) in enumerate(piliers):
        cx, cw = col_x(i, 3)
        D.add_card(s, cx, top, cw, card_h, color)
        tx = cx + 0.08 + pad
        tw = cw - 0.08 - 2 * pad
        D.add_text(s, tx, top + 0.22, tw, card_h - 0.44, [
            (titre, dict(size=D.TYPE["small"], bold=True, color=color, line_spacing=1.05)),
            (corps, dict(size=9, color=NAVY, space_before=8, line_spacing=1.25)),
            ("RÉPOND À", dict(size=6.5, bold=True, color=MUTED, space_before=12)),
            (ancre, dict(size=9, bold=True, color=color, space_before=2)),
        ])
    return s


def slide_maturite(prs):
    s = content_slide(prs, "KPI",
                       "La grille de maturité : deux échelles distinctes, mesurées dans le temps",
                       color=D.PALETTE[0])
    # Placée en fin de chapitre KPI (juste avant le cas chiffré) et CLARIFIÉE
    # (point ①) : c'est la 3e famille de KPIs (grille de maturité). Message resserré :
    # deux échelles ne mesurant PAS la même chose, chacune gouvernant une décision
    # différente ; le KPI = le DELTA dans le temps, pas le niveau absolu. Ambiguïté
    # « Remplace le M0–M4 » toujours levée (badge « Où se lit l'axe IA »).
    D.add_text(s, MARGIN, CONTENT_TOP, CONTENT_W, 0.42, [
        ("La 3ᵉ famille de KPIs. Deux lectures qui ne mesurent pas la même chose et se lisent "
         "séparément ; le KPI de progression, c'est le DELTA par pilier entre T0 et chaque "
         "réévaluation — pas le niveau absolu.",
         dict(size=8, color=MUTED, italic=True, line_spacing=1.2)),
    ])
    x0, w0 = col_x(0, 2)
    x1, w1 = col_x(1, 2)

    head_top = CONTENT_TOP + 0.5
    D.add_text(s, x0, head_top, w0, 0.5, [
        ("CAPACITÉ IA DU CLIENT (M0–M4)", dict(size=D.TYPE["tiny"], bold=True, color=NAVY)),
        ("→ gouverne le choix du modèle IA et le gate",
         dict(size=7.5, color=D.PALETTE[0], space_before=2, line_spacing=1.05)),
    ])
    niveaux = [
        ("M0", "Pas d'IA interne utilisable", "Méthodo générique, données anonymisées"),
        ("M1", "IA interne basique", "Synthèses internes, pas d'analyse critique auto"),
        ("M2", "IA privée avec RAG", "Diagnostic documentaire, consolidation"),
        ("M3", "Plateforme IA gouvernée", "Workflows agentic contrôlés"),
        ("M4", "IA industrielle", "Agents spécialisés à fort volume, contrôle humain"),
    ]
    row_top = head_top + 0.52
    row_h = 0.58
    row_gap = 0.06
    for i, (code, titre, strat) in enumerate(niveaux):
        y = row_top + i * (row_h + row_gap)
        chip(s, x0, y, 0.62, row_h, code, D.PALETTE[0], size=D.TYPE["tiny"])
        D.add_text(s, x0 + 0.62 + 0.15, y, w0 - 0.77 - 0.15, row_h, [
            (titre, dict(size=D.TYPE["tiny"], bold=True, color=NAVY)),
            (strat, dict(size=8, color=MUTED, space_before=1, line_spacing=1.1)),
        ], anchor=MSO_ANCHOR.MIDDLE)

    D.add_text(s, x1, head_top, w1, 0.5, [
        ("MATURITÉ PRODUIT / PLATEFORME (grille V3.2)", dict(size=D.TYPE["tiny"], bold=True, color=NAVY)),
        ("→ gouverne la trajectoire de transformation",
         dict(size=7.5, color=D.PALETTE[1], space_before=2, line_spacing=1.05)),
    ])
    piliers = [
        ("Équipe Produit", "Adjacent", False),
        ("Excellence Technique", "Cœur du périmètre", True),
        ("Culture de l'Entreprise Agile", "Adjacent", False),
        ("Agilité à l'Échelle", "Cœur du périmètre", True),
        ("IA, Agentic et Organisation Augmentée", "Où se lit l'axe IA (M0–M4)", True),
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
# (reprise des questions des §Agents), son irritant, son attente. Ouvre le
# chapitre Personas (acte 2) : on sait QUI l'on transforme avant d'exposer ses
# douleurs (chapitre Besoins & douleurs) puis notre réponse (Proposition).
def slide_personas(prs):
    s = content_slide(prs, "Personas",
                       "Quatre parties prenantes interrogées séparément — leur voix, leur posture",
                       color=D.PALETTE[5])
    D.add_text(s, MARGIN, CONTENT_TOP, CONTENT_W, 0.5, [
        ("Product Discovery fusionnée dans iap-product-definition en MVP1 — mais chaque partie "
         "prenante répond à la même trame, pour révéler convergences ET divergences plutôt qu'un "
         "diagnostic monolithique.",
         dict(size=8, color=MUTED, italic=True, line_spacing=1.2)),
    ])

    P = D.PALETTE
    # 2×2 cartes persona. Tuple : nom, accent, rôle (1 ligne), verbatim, ce qu'il
    # SUBIT, ce qu'il VISE, posture face à la transformation + sa couleur (feu
    # tricolore sémantique : allié=vert, sceptique=rouge, vigilant=or). La posture
    # est l'ajout du brainstorm — le comité lit le paysage politique, pas 4 listes.
    personas = [
        ("Infra & RUN", P[0], "Tient l'exploitation, subit les astreintes.",
         "« Opérable sans sacrifier le delivery ? »",
         "Experts seniors mobilisés sur du répétitif.",
         "Capacité récupérée, RUN maîtrisé.",
         "Vigilant", P[3]),
        ("Utilisateur applicatif", P[5], "Consomme la plateforme — ou la contourne.",
         "« Pourquoi adopterais-je la plateforme ? »",
         "Guichet unique, contournement plus rapide.",
         "Un self-service adopté par choix.",
         "Sceptique", P[2]),
        ("Management", P[3], "Expert devenu manager, pilote à vue.",
         "« Comment piloter avec un signal fiable ? »",
         "Reporting-miroir et micromanagement.",
         "Un signal de flux de confiance.",
         "Allié", P[1]),
        ("Sponsor", P[4], "Porte le budget et la promesse business.",
         "« Quel problème business règle-t-on ? »",
         "Craint une transformation cosmétique.",
         "Problème business réglé, KPIs de mission.",
         "Allié exigeant", P[1]),
    ]
    top0 = CONTENT_TOP + 0.62
    row_gap = 0.18
    card_h = (CONTENT_BOTTOM - top0 - row_gap) / 2
    pad = 0.2
    chip_w, chip_h = 1.2, 0.24
    for i, (nom, accent, role, verbatim, subit, vise, posture, cposture) in enumerate(personas):
        r, c = divmod(i, 2)
        cx, cw = col_x(c, 2)
        cy = top0 + r * (card_h + row_gap)
        D.add_card(s, cx, cy, cw, card_h, accent)
        tx = cx + 0.07 + pad
        tw = cw - 0.07 - 2 * pad
        D.add_text(s, tx, cy + 0.15, tw, card_h - 0.15 - chip_h - 0.18, [
            (nom, dict(size=D.TYPE["tiny"], bold=True, color=accent, line_spacing=1.0)),
            (role, dict(size=8, color=MUTED, space_before=1, line_spacing=1.1)),
            (verbatim, dict(size=8, italic=True, color=NAVY, space_before=5, line_spacing=1.1)),
            ("Subit — " + subit, dict(size=8, color=MUTED, space_before=6, line_spacing=1.1)),
            ("Vise — " + vise, dict(size=8, color=accent, space_before=3, line_spacing=1.1)),
        ])
        chip(s, cx + cw - pad - chip_w, cy + card_h - 0.14 - chip_h, chip_w, chip_h,
             posture.upper(), cposture, size=6.5)
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
    s = content_slide(prs, "Personas",
                       "Interroger chaque persona séparément révèle des tensions "
                       "qu'un diagnostic fusionné lisserait",
                       color=D.PALETTE[5])
    # Note d'intro retirée (redondante avec le sous-titre) : les rangées démarrent
    # plus haut pour laisser place, en bas, à la synthèse « pont » vers la Proposition.
    # Passe de design 2026-07-23 — pattern 7 du catalogue deck-design-library
    # (« rangée de cartes, une en accent ») : la rangée ANGLE MORT (Sponsor ⟂ RSSI)
    # est la seule teintée (fond rouge très pâle + contour rouge) — rouge =
    # sémantique d'alerte, pas décoration ; les 3 tensions instruites restent
    # des cartes blanches identiques.
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
    top0 = CONTENT_TOP + 0.1
    n = len(rows)
    synth_h, note_h = 0.56, 0.34
    bottom_reserve = synth_h + 0.14 + note_h + 0.10
    row_gap = 0.12
    region_bot = CONTENT_BOTTOM - bottom_reserve
    row_h = (region_bot - top0 - (n - 1) * row_gap) / n
    name_w = 2.7
    x_name = MARGIN + 0.2
    x_fric = x_name + name_w + 0.25
    fric_w = (MARGIN + CONTENT_W) - x_fric - 0.15
    for i, ((nomA, colA), (nomB, colB), tag, friction) in enumerate(rows):
        y = top0 + i * (row_h + row_gap)
        accent = tag is not None   # « un sur N » : l'angle mort, seul non instruit
        D.add_rect(s, MARGIN, y, CONTENT_W, row_h,
                   fill="#fbeeed" if accent else "#ffffff",
                   line=c_rssi if accent else LINE,
                   line_w=1.0 if accent else 0.75,
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

    # Ligne de synthèse « pont » (issue du brainstorm) : les divergences ne se
    # tranchent pas, la méthode (ch. Proposition) les tient des deux bouts —
    # transforme la slide de « voici des conflits » en « voici pourquoi on n'a pas
    # à choisir un camp », et donne l'élan vers la suite.
    synth_top = top0 + n * row_h + (n - 1) * row_gap + 0.14
    D.add_rect(s, MARGIN, synth_top, CONTENT_W, synth_h, fill=TRACK, rounded=True, radius=0.12)
    D.add_rect(s, MARGIN, synth_top, 0.07, synth_h, fill=c_user, rounded=True, radius=0.5)
    D.add_text(s, MARGIN + 0.26, synth_top, CONTENT_W - 0.42, synth_h, [
        ("Ces tensions ne se tranchent pas — on les tient des deux bouts.",
         dict(size=8.5, bold=True, color=c_user, line_spacing=1.05)),
        ("La méthode (ch. Proposition) : la métrique de flux = signal partagé, le gate "
         "confidentialité = non négociable.",
         dict(size=8, color=NAVY, space_before=2, line_spacing=1.1)),
    ], anchor=MSO_ANCHOR.MIDDLE)

    note_top = synth_top + synth_h + 0.10
    D.add_text(s, MARGIN, note_top, CONTENT_W, note_h, [
        ("Angles morts, non interrogés à ce stade : le client métier consommateur des services, "
         "le RSSI (porteur du gate), le junior / nouvel arrivant.",
         dict(size=7.5, color=MUTED, italic=True, line_spacing=1.15)),
    ])
    return s


# ---------------------------------------------------------------- Besoins & douleurs
# Nouveau (restructuration 5 actes) : la grille des 8 familles de gaspillage,
# jusqu'ici empaquetée dans slide_gaspillages avec la chaîne de traitement et le
# score, est isolée ici — elle appartient au chapitre « Besoins & douleurs » (le
# langage commun qui rend une douleur nommable, donc détectable et traitable),
# tandis que la MÉTHODE de traitement (chaîne + score) reste au chapitre
# Proposition. Accent unifié sur la couleur du chapitre Douleurs (PALETTE[2]) :
# les 8 familles se distinguent par leur libellé, pas par 8 teintes sans clé.
# Passe de design 2026-07-23 — règle « un sur N en accent » (principes
# transversaux + pattern 3 du catalogue deck-design-library) : la famille IA,
# seule famille que cette méthode NOMME comme gaspillage (cas gadget,
# automatisation sans garde-fous — la doctrine du deck), reçoit un fill navy
# plein ; les 7 autres restent des cartes blanches identiques.
def slide_familles(prs):
    s = content_slide(prs, "Besoins & douleurs",
                       "Les 8 familles de gaspillage — le langage commun qui rend les douleurs traitables",
                       color=D.PALETTE[2])
    D.add_text(s, MARGIN, CONTENT_TOP, CONTENT_W, 0.42, [
        ("Nommer la famille, c'est déjà pouvoir la détecter, la quantifier et la prioriser "
         "(méthode de traitement → chapitre Proposition).",
         dict(size=D.TYPE["small"], color=NAVY, italic=True, line_spacing=1.25)),
    ])
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
    # 2 colonnes x 4 rangées : remplit la hauteur de la slide dédiée sans étirer
    # chaque carte (défaut « panneau sur-étiré »). Lecture gauche->droite par
    # paire (col = i % 2, row = i // 2).
    n_rows = 4
    region_top = CONTENT_TOP + 0.55
    row_gap = 0.14
    row_h = (CONTENT_BOTTOM - region_top - (n_rows - 1) * row_gap) / n_rows
    for i, (nom, ex) in enumerate(familles):
        col = i % 2
        row = i // 2
        x, w = col_x(col, 2)
        y = region_top + row * (row_h + row_gap)
        accent = (nom == "IA")   # « un sur N » : la famille portée par la doctrine
        if accent:
            D.add_rect(s, x, y, w, row_h, fill=NAVY, rounded=True, radius=0.1)
        else:
            D.add_rect(s, x, y, w, row_h, fill="#ffffff", line=LINE, line_w=0.75,
                       rounded=True, radius=0.1)
        D.add_rect(s, x, y, 0.06, row_h, fill=D.PALETTE[2], rounded=True, radius=0.5)
        D.add_text(s, x + 0.2, y + 0.06, w - 0.34, row_h - 0.12, [
            (f"{i + 1}. {nom}", dict(size=D.TYPE["small"], bold=True,
                                     color="#ffffff" if accent else NAVY)),
            (ex, dict(size=8, color="#c7cbe0" if accent else MUTED,
                      space_before=2, line_spacing=1.1)),
        ], anchor=MSO_ANCHOR.MIDDLE)
    return s


# ---------------------------------------------------------------- Proposition
# Reframe (restructuration 5 actes) : la grille des 8 familles est partie au
# chapitre « Besoins & douleurs » (slide_familles). Ne reste ici que la MÉTHODE
# de traitement — la chaîne Détecter->Prévenir et le score de priorisation — ré-
# ancrée vers le haut pour combler l'espace libéré par la grille retirée, avec
# une accroche en tête pour éviter un vide sous le titre.
# Passe de design 2026-07-23 : la chaîne, jusqu'ici 10 pilules grises identiques
# en grille 2×5 (effet « tableau de chips »), est redessinée selon le pattern 4
# du catalogue deck-design-library (« flux numéroté en quinconce, badges +
# connecteur, sans cadres ») : badges numérotés reliés par un fil, 2e rangée
# décalée d'un demi-slot, et « un sur N en accent » — seule l'étape 6 (Prioriser)
# est remplie en couleur pleine, car c'est elle qui produit le score détaillé
# dans le panneau navy juste en dessous.
def slide_gaspillages(prs):
    s = content_slide(prs, "Proposition",
                       "Du gaspillage au backlog priorisé : chaîne de traitement + score",
                       color=D.PALETTE[1])
    D.add_text(s, MARGIN, CONTENT_TOP, CONTENT_W, 0.5, [
        ("Chaque famille de gaspillage (chapitre précédent) passe par la même chaîne de "
         "traitement, puis reçoit un score explicite qui la classe dans un backlog priorisé "
         "— jamais un tri à l'intuition.",
         dict(size=D.TYPE["small"], color=NAVY, italic=True, line_spacing=1.25)),
    ])

    chain_top = CONTENT_TOP + 0.65
    D.add_text(s, MARGIN, chain_top, CONTENT_W, 0.24, [
        ("CHAÎNE DE TRAITEMENT — de la détection à la prévention",
         dict(size=8, bold=True, color=MUTED))
    ])
    etapes = ["Détecter", "Qualifier", "Quantifier", "Cause racine", "Pattern",
              "Prioriser", "Expérimenter", "Mesurer", "Industrialiser", "Prévenir"]
    step_top = chain_top + 0.34
    n = 5
    slot = CONTENT_W / (n + 0.5)   # 2e rangée décalée d'un demi-slot (quinconce)
    badge_d = 0.32
    unit_h = 0.62                  # badge + libellé
    row_gap2 = 0.10
    accent_idx = 5                 # « Prioriser » — l'étape qui produit le score
    for row in range(2):
        x0 = MARGIN + (slot / 2 if row == 1 else 0.0)
        y = step_top + row * (unit_h + row_gap2)
        cy = y + badge_d / 2
        # fil du flux : connecteur horizontal reliant les badges de la rangée
        D.add_rect(s, x0 + slot / 2, cy - 0.01, (n - 1) * slot, 0.02, fill=LINE)
        for col in range(n):
            i = row * n + col
            accent = (i == accent_idx)
            bx = x0 + col * slot + slot / 2 - badge_d / 2
            D.add_rect(s, bx, y, badge_d, badge_d,
                       fill=D.PALETTE[1] if accent else "#ffffff",
                       line=None if accent else D.PALETTE[1], line_w=1.0,
                       rounded=True, radius=0.5)
            D.add_text(s, bx, y, badge_d, badge_d, [
                (str(i + 1), dict(size=8, bold=True,
                                  color="#ffffff" if accent else D.PALETTE[1],
                                  align=PP_ALIGN.CENTER)),
            ], anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
            D.add_text(s, x0 + col * slot, y + badge_d + 0.04, slot, 0.22, [
                (etapes[i], dict(size=8, bold=True,
                                 color=D.PALETTE[1] if accent else NAVY,
                                 align=PP_ALIGN.CENTER)),
            ], align=PP_ALIGN.CENTER)

    score_top = step_top + 2 * unit_h + row_gap2 + 0.30
    score_h = CONTENT_BOTTOM - score_top - 0.12
    D.add_rect(s, MARGIN, score_top, CONTENT_W, score_h, fill=NAVY, rounded=True, radius=0.08)
    text_w = CONTENT_W * 0.5
    D.add_text(s, MARGIN + 0.22, score_top, text_w - 0.3, score_h, [
        ("Priorité = (impact × faisabilité) − prudence IA",
         dict(size=D.TYPE["small"], bold=True, color="#ffffff", line_spacing=1.15)),
        ("Le score ne remplace pas l'arbitrage humain : il rend la discussion explicite, "
         "et classe les candidats dans un backlog priorisé.",
         dict(size=8, color="#c7cbe0", space_before=4, line_spacing=1.2)),
    ], anchor=MSO_ANCHOR.MIDDLE)

    # Jauge à points — pattern repris de l'autre template analysé
    # (analyse-template-alternatif.md §4) pour illustrer un score 1-5.
    gauge_x = MARGIN + text_w
    gauge_w = CONTENT_W - text_w
    D.add_text(s, gauge_x, score_top + 0.12, gauge_w - 0.15, 0.18, [
        ("SCORE ILLUSTRATIF", dict(size=7, bold=True, color="#8891b3")),
    ])
    rows_top = score_top + 0.38
    row_h2 = (score_h - 0.38 - 0.1) / 3
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


# ---------------------------------------------------------------- Besoins & douleurs
# Nouveau (restructuration 5 actes) : va PLUS LOIN que slide_personas (qui porte
# un irritant + une attente d'une ligne par persona). Ici chaque douleur est
# approfondie, dotée d'un signal/mesure qui la rend objectivable, et rattachée à
# une ou plusieurs familles de gaspillage — le pont direct vers slide_familles.
# Réutilise les couleurs d'accent persona (Infra=bleu, Utilisateur=teal,
# Management=or, Sponsor=violet). Rangées dimensionnées à leur contenu.
def slide_douleurs(prs):
    s = content_slide(prs, "Besoins & douleurs",
                       "Les douleurs des clients infra : mesurables, pas des plaintes",
                       color=D.PALETTE[2])
    D.add_text(s, MARGIN, CONTENT_TOP, CONTENT_W, 0.4, [
        ("Chaque douleur appartient à un persona et se range dans une famille de gaspillage "
         "— c'est ce qui la rend traitable plutôt que subie.",
         dict(size=8, color=MUTED, italic=True, line_spacing=1.2)),
    ])

    rows = [
        ("Infra & RUN", D.PALETTE[0],
         "RUN subi : les mêmes incidents reviennent et mobilisent les experts seniors, le BUILD "
         "est sacrifié à l'astreinte.",
         "Tickets récurrents/mois, part du temps en RUN non maîtrisé.",
         "RUN · Humain"),
        ("Utilisateur applicatif", D.PALETTE[5],
         "Aucun self-service ni parcours conçu : tout passe par un guichet, le contournement "
         "(shadow IT) va plus vite que la demande officielle.",
         "Taux de contournement, délai de mise à disposition.",
         "Flux · Cognitif"),
        ("Management", D.PALETTE[3],
         "« Expert devenu manager malgré lui » : reporting miroir et micromanagement "
         "compensatoire, faute de signal fiable sur le flux.",
         "Ratio temps reporting / temps résolution d'obstacles.",
         "Décisionnel · Humain"),
        ("Sponsor", D.PALETTE[4],
         "Pression à « mettre de l'IA » sans cas d'usage, peur d'une transformation cosmétique : "
         "beaucoup d'activité, peu de valeur démontrée.",
         "Valeur / capacité récupérée démontrée vs promise.",
         "Décisionnel · IA (gadget)"),
    ]

    # Colonnes (comme slide_architecture_si) : en-têtes une seule fois, puis 4
    # rangées à liseré = couleur persona, anchor MIDDLE. Hauteur de rangée
    # calée sur le contenu le plus long (colonne douleur), pas d'étirement.
    headers = ["PERSONA", "LA DOULEUR, APPROFONDIE", "SIGNAL / MESURE", "FAMILLE(S)"]
    col_widths = [1.3, 3.6, 1.85, 1.425]
    col_gap = 0.12
    xs = []
    cx = MARGIN
    for cw in col_widths:
        xs.append(cx)
        cx += cw + col_gap

    header_y = CONTENT_TOP + 0.45
    for x, w, label in zip(xs, col_widths, headers):
        D.add_text(s, x + (0.12 if x == xs[0] else 0), header_y, w, 0.2, [
            (label, dict(size=7, bold=True, color=MUTED)),
        ])

    # Hauteur de rangée calée sur le contenu, MAIS bornée pour toujours réserver
    # la ligne-pont du bas (« → slide suivante ») — sans ce plafond, 4 rangées de
    # 4 lignes remplissaient jusqu'au bas et escamotaient la ligne-pont.
    n = len(rows)
    row_gap = 0.12
    note_reserve = 0.5
    row_top = header_y + 0.26
    region_bot = CONTENT_BOTTOM - note_reserve
    size = 8
    lh = size * 1.2 / 72.0
    row_lines = max(
        max(_lignes(r[2], col_widths[1] - 0.2, size), _lignes(r[3], col_widths[2] - 0.15, size))
        for r in rows)
    row_h = min(row_lines * lh + 0.26, (region_bot - row_top - (n - 1) * row_gap) / n)
    for i, (nom, color, douleur, signal, famille) in enumerate(rows):
        y = row_top + i * (row_h + row_gap)
        D.add_rect(s, MARGIN, y, CONTENT_W, row_h, fill="#ffffff", line=LINE, line_w=0.75,
                   rounded=True, radius=0.08)
        D.add_rect(s, MARGIN, y, 0.06, row_h, fill=color, rounded=True, radius=0.5)
        D.add_text(s, xs[0] + 0.12, y + 0.08, col_widths[0] - 0.12, row_h - 0.16, [
            (nom, dict(size=D.TYPE["tiny"], bold=True, color=color, line_spacing=1.1)),
        ], anchor=MSO_ANCHOR.MIDDLE)
        D.add_text(s, xs[1], y + 0.08, col_widths[1] - 0.15, row_h - 0.16, [
            (douleur, dict(size=size, color=NAVY, line_spacing=1.2)),
        ], anchor=MSO_ANCHOR.MIDDLE)
        D.add_text(s, xs[2], y + 0.08, col_widths[2] - 0.12, row_h - 0.16, [
            (signal, dict(size=size, color=MUTED, italic=True, line_spacing=1.2)),
        ], anchor=MSO_ANCHOR.MIDDLE)
        D.add_text(s, xs[3], y + 0.08, col_widths[3], row_h - 0.16, [
            (famille, dict(size=size, bold=True, color=color, line_spacing=1.2)),
        ], anchor=MSO_ANCHOR.MIDDLE)

    note_top = row_top + len(rows) * row_h + (len(rows) - 1) * row_gap + 0.14
    note_h = min(0.4, CONTENT_BOTTOM - note_top)
    if note_h > 0.12:
        D.add_text(s, MARGIN, note_top, CONTENT_W, note_h, [
            ("Ces douleurs se rangent en 8 familles de gaspillage → slide suivante.",
             dict(size=8, bold=True, color=D.PALETTE[2], line_spacing=1.15)),
        ])
    return s


# --- Exemples générés (Méthode) — concrétisent slide_gaspillages avec des
# instanciations chiffrées des concepts déjà cadrés (formule de priorisation,
# tags de confiance, RecommendationAxis valeur/complexité, US Coach/Délégué) —
# aucun nouveau concept, uniquement des exemples fictifs illustratifs.
def slide_exemple_priorisation(prs):
    s = content_slide(prs, "Exemples",
                       "La priorisation en pratique : la faisabilité tempère l'impact brut",
                       color=D.PALETTE[1])
    D.add_text(s, MARGIN, CONTENT_TOP, CONTENT_W, 0.3, [
        ("Exemple illustratif — 3 gaspillages fictifs notés sur la formule de la chaîne de traitement (plus haut dans la Proposition).",
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
    s = content_slide(prs, "Exemples",
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
         "candidat prioritaire pour la chaîne de traitement (chapitre Proposition).",
         dict(size=8, color="#c7cbe0", space_before=3, line_spacing=1.2)),
    ], anchor=MSO_ANCHOR.MIDDLE)
    return s


def slide_exemple_recommandation(prs):
    s = content_slide(prs, "Exemples",
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
    s = content_slide(prs, "Proposition", "La cible IAP est une Platform Team — agents IA compris", color=D.PALETTE[1])
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
         "Platform Team. Aux 3 modes d'interaction Team Topologies — Collaboration, "
         "X-as-a-Service, Facilitating — s'ajoute un 4ᵉ candidat : Supervision. "
         "L'adoption suit la trajectoire "
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
    # v2.5 (chantier ④) : déplacée de la Proposition vers la Démarche — c'est
    # « comment la mission tourne », pas ce qu'on propose.
    s = content_slide(prs, "Démarche",
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
         ["Interviews par persona (trame / thème / question)",
          "Import outils : ServiceNow/Jira/CMDB si accès"]),
        ("DIAGNOSTIC", D.PALETTE[4],
         ["Synthèse par thème puis synthèse globale",
          "Registre de gaspillage (tags CONFIRMÉ/DÉDUIT/INCERTAIN)"]),
        ("CONCEPTION", D.PALETTE[3],
         ["Définition produit (+ cible MVP)",
          "Operating model + traitement du gaspillage (décisions actées)"]),
        ("RESTITUTION", D.PALETTE[1],
         ["Deck exécutif : axes valeur/complexité",
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
        ("⟲ Boucle de réévaluation — iap-re-assessment, T+6-12 mois, alimente la bibliothèque de REX, "
         "reboucle vers la Collecte", dict(size=8, bold=False, color="#ffffff", line_spacing=1.15)),
    ], anchor=MSO_ANCHOR.MIDDLE)
    return s


# Fusion v2.5 (chantier ①) : slide_trajectoire et slide_schema_bout_en_bout
# déroulaient la même trame ①②③⟲ sur deux slides — fusionnées ici. La ligne de
# badges + durées + actions clés (de l'ancienne trajectoire) est enrichie du
# LIVRABLE-CLÉ par phase en une ligne (l'apport de la vue bout-en-bout — les
# NOMS seulement ; le détail des 4 profils de deck reste à slide_livrables_ppt).
def slide_trajectoire(prs):
    s = content_slide(prs, "Démarche",
                       "Trois temps et une boucle — chaque phase produit son livrable de décision",
                       color=D.PALETTE[3])
    phases = [
        ("①", "Assessment flash", "1–2 sem.", D.PALETTE[0],
         "= Schéma de fonctionnement déjà cadré (Collecte → Diagnostic → Conception → Restitution).",
         "Deck exécutif de restitution"),
        ("②", "Premier déploiement", "4–5 sem.", D.PALETTE[3],
         "1-2 équipes pilotes, mode Coach dominant. Piste agent IA (si retenue) : qualifier, cadrer, mandater.",
         "Deck de plan de déploiement · export markdown (1re version)"),
        ("③", "Implémentation itérative", "→ T+6-12 mois", D.PALETTE[1],
         "Généralisation équipe par équipe, bascule Coach → Délégué. Piste agent IA : supervisé puis délégué.",
         "Deck de comité de pilotage (périodique)"),
        ("⟲", "Boucle de réévaluation", "T+6-12 mois", D.PALETTE[2],
         "iap-re-assessment reboucle vers la Collecte — alimente la bibliothèque de REX.",
         "Deck de bilan / ré-évaluation · markdown amendé"),
    ]
    n = len(phases)
    badge_d = 0.55
    top0 = CONTENT_TOP + 0.1
    line_y = top0 + badge_d / 2 - 0.012
    D.add_rect(s, MARGIN + badge_d / 2, line_y, CONTENT_W - badge_d, 0.024, fill=LINE)
    _, wcol = col_x(0, n)
    desc_h = max(_lignes(p[4], wcol - 0.1, 7) for p in phases) * (7 * 1.2 / 72.0) + 0.05
    livr_h = max(_lignes(p[5], wcol - 0.2, 7.5) for p in phases) * (7.5 * 1.2 / 72.0) + 0.24
    for i, (sym, titre, duree, color, desc, livrable) in enumerate(phases):
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
        desc_y = chip_y + 0.34
        D.add_text(s, x + 0.05, desc_y, w - 0.1, desc_h, [
            (desc, dict(size=7, color=MUTED, align=PP_ALIGN.CENTER, line_spacing=1.2)),
        ], align=PP_ALIGN.CENTER)
        # Livrable-clé (fusion bout-en-bout) : le NOM du livrable, encadré,
        # au pied de chaque colonne — le détail vit dans slide_livrables_ppt.
        livr_y = desc_y + desc_h + 0.10
        D.add_rect(s, x, livr_y, w, livr_h, fill=TRACK, rounded=True, radius=0.1)
        D.add_text(s, x + 0.1, livr_y, w - 0.2, livr_h, [
            ("LIVRABLE-CLÉ", dict(size=6.5, bold=True, color=MUTED, align=PP_ALIGN.CENTER)),
            (livrable, dict(size=7.5, bold=True, color=color, space_before=2,
                            align=PP_ALIGN.CENTER, line_spacing=1.15)),
        ], anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)

    note_top = top0 + badge_d + 0.12 + 0.36 + 0.34 + desc_h + 0.10 + livr_h + 0.18
    note_h = min(1.05, CONTENT_BOTTOM - note_top)
    D.add_rect(s, MARGIN, note_top, CONTENT_W, note_h, fill=TRACK, rounded=True, radius=0.08)
    D.add_text(s, MARGIN + 0.2, note_top, CONTENT_W - 0.4, note_h, [
        ("Bifurcation avec/sans agents IA déployés", dict(size=8, bold=True, color=NAVY)),
        ("Le tronc commun ①→②→③→⟲ ne change pas de structure — la piste agent IA (si retenue) "
         "se greffe sur ②/③ via la démarche d'accompagnement en 5 phases déjà cadrée, plutôt "
         "que d'être un chemin séparé à maintenir. Owner proposé (non tranché) : "
         "iap-operating-model-architect + iap-change-coach sur le volet humain.",
         dict(size=7, color=NAVY, space_before=3, line_spacing=1.25)),
    ], anchor=MSO_ANCHOR.MIDDLE)
    return s


# Nouveau (v2.4) : le fil humain de la trajectoire (§Accompagnement de
# l'humain dans la trajectoire, transposé de l'offre SCALE). Décline la même
# trame ①②③⟲ que slide_trajectoire côté personnes — pattern 14 du catalogue
# deck-design-library (« processus en 4 étapes numérotées, colonnes de détail
# dans UNE carte », fil rouge transversal repérable en diagonale : ici
# iap-change-coach répété en pied de chaque colonne) + badge chevauchant le
# bord haut de la carte (pattern 10). L'accroche Kotter (70 %) est LE seul
# élément en aplat plein de la slide (« un sur N en accent »).
def slide_fil_humain(prs):
    s = content_slide(prs, "Démarche",
                       "La trajectoire accompagne aussi les personnes, de bout en bout",
                       color=D.PALETTE[3])

    # --- Accroche argumentaire : le chiffre Kotter en bloc accent + intro.
    stat_w, stat_h = 1.05, 0.62
    strip_top = CONTENT_TOP + 0.02
    D.add_rect(s, MARGIN, strip_top, stat_w, stat_h, fill=NAVY, rounded=True, radius=0.12)
    D.add_text(s, MARGIN, strip_top, stat_w, stat_h, [
        ("70 %", dict(size=18, bold=True, color="#ffffff", align=PP_ALIGN.CENTER)),
    ], anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
    tx = MARGIN + stat_w + 0.18
    tw = CONTENT_W - stat_w - 0.18
    D.add_text(s, tx, strip_top, tw, stat_h, [
        ("des transformations sont inachevées ou échouent parce que les facteurs humains "
         "et culturels sont mal pris en compte (Kotter, Harvard Business Review).",
         dict(size=8, bold=True, color=NAVY, line_spacing=1.15)),
        # ⟲ en run NON gras (paragraphe italic non-bold) — cf. _GLYPHES_SANS_GRAS.
        ("Le fil humain suit la même trame ①②③⟲ que la trajectoire — un fil dans les "
         "phases, pas un stream séparé, porté par iap-change-coach de bout en bout.",
         dict(size=7.5, italic=True, color=MUTED, space_before=3, line_spacing=1.15)),
    ], anchor=MSO_ANCHOR.MIDDLE)

    phases = [
        ("①", "ASSESSMENT FLASH", "Engager", D.PALETTE[0],
         "L'engagement personnel du sponsor est testé dès l'intake, avant signature ; "
         "les interviews écoutent les tensions ; la restitution revient aux interviewés, "
         "pas au seul sponsor.",
         "iap-change-coach · iap-intake"),
        ("②", "PREMIER DÉPLOIEMENT", "Expérimenter", D.PALETTE[3],
         "Équipes pilotes volontaires, jamais désignées d'office ; formation sur les cas "
         "réels de l'équipe — « pas de formation sans coaching ».",
         "iap-change-coach · équipe pilote"),
        ("③", "IMPLÉMENTATION ITÉRATIVE", "Outiller & relayer", D.PALETTE[1],
         "Les résistances sont un signal à écouter ; communauté de managers (N+1/N+2 "
         "embarqués) ; relais internes formés — le consultant se rend dispensable.",
         "iap-change-coach · operating-model-architect"),
        ("⟲", "BOUCLE DE RÉÉVALUATION", "Mesurer", D.PALETTE[2],
         "Satisfaction et adhésion mesurées au même instrument à T0 et à la réévaluation — "
         "le delta humain se lit à côté du delta de maturité.",
         "iap-change-coach · metrics-sre-finops-lead"),
    ]
    n = len(phases)
    badge_d = 0.45
    pad = 0.16
    _, col_w = col_x(0, n, gap=0)
    usable = col_w - 2 * pad

    # Hauteurs dérivées du CONTENU (jamais « jusqu'à CONTENT_BOTTOM ») —
    # défaut récurrent « panneau étiré vide », cf. slide_livrables_ppt.
    body_lines = max(_lignes(p[4], usable, 7.5) for p in phases)
    body_h = body_lines * (7.5 * 1.25 / 72.0) + 0.04
    owner_lines = max(_lignes(p[5], usable, 6.5) for p in phases)
    owner_h = owner_lines * (6.5 * 1.2 / 72.0) + 0.03
    # card_h relatif au bord haut de la carte : demi-badge + en-têtes + corps
    # + séparateur + owner + respiration basse.
    card_h = badge_d / 2 + 0.10 + 0.44 + body_h + 0.14 + owner_h + 0.14
    band_h = 0.60
    group_h = badge_d / 2 + card_h + 0.18 + band_h
    region_top = strip_top + stat_h + 0.16
    top1 = region_top + min(0.30, max(0.0, (CONTENT_BOTTOM - region_top - group_h) / 2))
    card_top = top1 + badge_d / 2

    D.add_rect(s, MARGIN, card_top, CONTENT_W, card_h, fill="#ffffff",
               line=LINE, line_w=0.75, rounded=True, radius=0.06)
    for i, (sym, phase, verbe, color, desc, owner) in enumerate(phases):
        x, w = col_x(i, n, gap=0)
        if i > 0:  # séparateurs fins internes — UNE carte, pas 4 (pattern 14)
            D.add_rect(s, x, card_top + 0.14, 0.012, card_h - 0.28, fill=LINE)
        cx = x + w / 2 - badge_d / 2
        D.add_rect(s, cx, top1, badge_d, badge_d, fill=color, rounded=True, radius=0.5)
        D.add_text(s, cx, top1, badge_d, badge_d, [
            # bold=False pour "⟲" : variante grasse absente de la police du
            # template (tofu au rendu) — même correctif que slide_trajectoire.
            (sym, dict(size=13, bold=(sym != "⟲"), color="#ffffff", align=PP_ALIGN.CENTER)),
        ], anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
        head_y = top1 + badge_d + 0.10
        D.add_text(s, x + pad, head_y, usable, 0.22, [
            (verbe, dict(size=9, bold=True, color=color, align=PP_ALIGN.CENTER)),
        ], align=PP_ALIGN.CENTER)
        D.add_text(s, x + pad, head_y + 0.22, usable, 0.16, [
            (phase, dict(size=6, bold=True, color=MUTED, align=PP_ALIGN.CENTER)),
        ], align=PP_ALIGN.CENTER)
        body_y = head_y + 0.44
        D.add_text(s, x + pad, body_y, usable, body_h, [
            (desc, dict(size=7.5, color=NAVY, line_spacing=1.25)),
        ])
        sep_y = body_y + body_h + 0.06
        D.add_rect(s, x + pad, sep_y, usable, 0.012, fill=LINE)
        D.add_text(s, x + pad, sep_y + 0.06, usable, owner_h, [
            (owner, dict(size=6.5, bold=True, color=color, line_spacing=1.2)),
        ])

    band_top = card_top + card_h + 0.18
    D.add_rect(s, MARGIN, band_top, CONTENT_W, band_h, fill=TRACK, rounded=True, radius=0.08)
    D.add_text(s, MARGIN + 0.2, band_top, CONTENT_W - 0.4, band_h, [
        ("Ce que ça ne crée pas", dict(size=8, bold=True, color=NAVY)),
        ("Pas de nouvel agent (iap-change-coach porte le fil de bout en bout), pas de phase "
         "en plus — et jamais d'évaluation individuelle des personnes (déontologie du "
         "consultant, transposée telle quelle).",
         dict(size=7, color=NAVY, space_before=3, line_spacing=1.25)),
    ], anchor=MSO_ANCHOR.MIDDLE)
    return s


# ---------------------------------------------------------------- slide 9
# Formes inspirées de la slide d'exemple « Une approche contextualisée » du
# template : colonne par étape avec badge + bandeau titre + ligne de
# séparation + bloc LIVRABLES, plutôt qu'un tableau plat.
def slide_livrables_ppt(prs):
    # v2.5 (chantier ④) : déplacée de la Proposition vers la Démarche, avec la
    # trajectoire fusionnée qui ne porte que les NOMS de livrables — ici le
    # détail des 4 profils (audience, contenu).
    s = content_slide(prs, "Démarche", "Livrables PPT par étape — piste à valider", color=D.PALETTE[3])
    D.add_text(s, MARGIN, CONTENT_TOP, CONTENT_W, 0.4, [
        ("iap-deck-builder est cadré comme un seul deck modulaire 16 sections, produit une fois "
         "à la Restitution — la trajectoire ci-avant implique plusieurs publics et moments de "
         "décision distincts. Piste : un profil de sections par étape, pas 4 générateurs séparés.",
         dict(size=8, color=MUTED, italic=True, line_spacing=1.2)),
    ])
    cols = [
        ("①", "Assessment flash", D.PALETTE[0], "Sponsor, comité de lancement",
         "Deck exécutif de restitution", "(déjà cadré) synthèse globale, axes valeur/complexité, radar T0"),
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
# Révisé (restructuration 5 actes) : slide 3 est l'énoncé de problème qui ouvre
# le deck — 3 puces d'une seule colonne vertébrale ancrées dans l'utilisateur
# (le constat → ce que ça coûte → ce qu'un bon diagnostic exige). La puce
# « l'IA amplifie l'organisation » a été RETIRÉE : elle est implicite dans la
# puce 2 et son point de doctrine est développé au chapitre IA. Le
# titre et l'image encadrée (sunset, cadre round2DiagRect) sont conservés.
def slide_vision(prs):
    layout = prs.slide_masters[0].slide_layouts[LAYOUT_VISUEL_DROITE]
    s = prs.slides.add_slide(layout)
    phs = {ph.placeholder_format.idx: ph for ph in s.placeholders}

    phs[0].text_frame.text = ("Le risque n'est pas de manquer d'outils : "
                               "c'est de traiter le mauvais problème")
    for p in phs[0].text_frame.paragraphs:
        for r in p.runs:
            r.font.color.rgb = _rgb(NAVY)

    # (amorce en gras, corps normal) — une seule colonne vertébrale utilisateur.
    bullets = [
        ("Le constat",
         "Une infrastructure vécue comme un guichet ou un centre de coûts subit la demande "
         "au lieu de la piloter : ni utilisateurs identifiés, ni feuille de route, ni levier "
         "d'adoption."),
        ("Ce que ça coûte",
         "La capacité disponible part en gaspillage (RUN subi, ressources orphelines, experts "
         "seniors sur des tâches répétitives) — et le réflexe « plus d'outils » ou « mettons de "
         "l'IA » l'aggrave au lieu de le traiter."),
        ("Ce qu'un bon diagnostic exige",
         "Partir des utilisateurs réels et de leurs douleurs, pas d'une réponse toute faite : "
         "c'est ce que déroulent les chapitres suivants."),
    ]
    tf = phs[1].text_frame
    tf.word_wrap = True
    for i, (lead, body) in enumerate(bullets):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        r1 = p.add_run()
        r1.text = lead
        r1.font.bold = True
        r1.font.color.rgb = _rgb(NAVY)
        r2 = p.add_run()
        r2.text = " — " + body
        r2.font.color.rgb = _rgb(NAVY)

    cadre = _find_frame_in_group(s.slide_layout.shapes, "Google Shape;212;p17", "Google Shape;213;p17")
    for pb in frame_obstructions(s, *cadre[:4]) if cadre else []:
        print("  [obstruction] vision:", pb["source"], pb["name"], pb["reason"])
    _remplir_cadre(s, cadre, "sunset", seed=1)
    return s


# (v2.5 — slide_schema_bout_en_bout supprimée, chantier ① : sa trame ①②③⟲
# doublonnait slide_trajectoire ; son apport — le livrable-clé par phase — est
# fusionné dans slide_trajectoire ci-dessus.)


# ---------------------------------------------------------------- slide 10
# Nouveau (v2.0) : la bifurcation "avec/sans agent IA" de slide_trajectoire
# gagne un livrable concret, distinct des 4 decks PPT — un markdown pour
# l'équipe qui exécute, pas pour le sponsor. Deux cartes (mêmes proportions
# que slide_mission) + un bandeau de routage + une note "pas un aller simple".
def slide_export_markdown(prs):
    s = content_slide(prs, "IA",
                       "Export markdown — agentic ou documentation, selon le contexte client (piste à valider)",
                       color=D.PALETTE[4])
    D.add_text(s, MARGIN, CONTENT_TOP, CONTENT_W, 0.32, [
        ("Pas un 5e deck PPT : un livrable markdown pour l'équipe qui exécute (versionnable, "
         "committable) — les 4 decks du chapitre Proposition restent pour sponsor et comité de pilotage.",
         dict(size=8, color=MUTED, italic=True, line_spacing=1.2)),
    ])

    cards = [
        ("DOCUMENTATION-FIRST", D.PALETTE[2],
         "Agentic Readiness [0]-[1], données D3-D4 sans LLM local, ou score de gaspillage faible.",
         "Runbook du processus", "iap-adoption-plan"),
        ("AGENTIC-IMPLEMENTATION", D.PALETTE[0],
         "Agentic Readiness [2]-[3], données D0-D2 (ou D3-D4 avec LLM local), score positif.",
         "Plan d'implémentation agentic", "iap-agentic-opportunities"),
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
         "modèle du registre de risques IA : un client documentation-first peut basculer en agentic si "
         "son Agentic Readiness progresse, et inversement en cas de perte de compétence avérée.",
         dict(size=8, color="#c7cbe0", space_before=4, line_spacing=1.25)),
    ], anchor=MSO_ANCHOR.MIDDLE)
    return s


# ---------------------------------------------------------------- slide 11
def slide_ambition(prs):
    s = content_slide(prs, "Proposition", "Trois niveaux d'ambition, pas un spectre linéaire", color=D.PALETTE[1])
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
    # Passe de design 2026-07-23 — pattern 7 du catalogue deck-design-library
    # (« un sur N en accent ») : le niveau A, ÉTAT ACTUEL assumé du cadrage
    # (cf. executive summary, posture de gouvernance), est la seule carte en
    # fill navy plein — B et C restent des cartes blanches identiques.
    role_lines = max(_lignes(niv[3], usable, 8) for niv in niveaux)
    role_h = role_lines * (8 * 1.25 / 72.0) + 0.06
    roadmap_y = 0.55 + role_h + 0.12
    card_h = roadmap_y + 0.28 + 0.14
    top0 = CONTENT_TOP + 0.45
    accent_idx = 0   # A · Aide au coach — l'état actuel
    for i, (code, titre, color, role, roadmap) in enumerate(niveaux):
        x, w = col_x(i, n)
        accent = (i == accent_idx)
        if accent:
            D.add_rect(s, x, top0, w, card_h, fill=NAVY, rounded=True, radius=0.06)
            D.add_rect(s, x, top0, 0.07, card_h, fill=color, rounded=True, radius=0.5)
        else:
            D.add_card(s, x, top0, w, card_h, color)
        D.add_text(s, x + pad, top0 + 0.15, w - 2 * pad, 0.35, [
            (f"{code} · {titre}", dict(size=D.TYPE["small"], bold=True,
                                       color="#ffffff" if accent else color)),
        ])
        D.add_text(s, x + pad, top0 + 0.55, w - 2 * pad, role_h, [
            (role, dict(size=8, color="#e8ebf5" if accent else NAVY, line_spacing=1.25)),
        ])
        D.add_text(s, x + pad, top0 + roadmap_y, w - 2 * pad, 0.3, [
            (roadmap, dict(size=8, bold=True, color="#ffffff" if accent else MUTED)),
        ])

    note_top = top0 + card_h + 0.18
    note_h = CONTENT_BOTTOM - note_top
    D.add_text(s, MARGIN, note_top, CONTENT_W, note_h, [
        ("Monter de A à C n'est pas qu'une question de fonctionnalités : le niveau C suppose "
         "un accès direct aux données de production du client — risque sécurité/confidentialité "
         "d'un tout autre ordre. Un cabinet peut durablement rester au niveau A ou B par choix "
         "de gouvernance, pas seulement par contrainte technique transitoire. "
         "MVP0–6 = jalons de la roadmap de mise en œuvre ; MVP6, le « companion connecté », n'est pas engagé.",
         dict(size=8, color=MUTED, italic=True, line_spacing=1.3)),
    ])
    return s


# ---------------------------------------------------------------- slide 12
def slide_kpis(prs):
    s = content_slide(prs, "KPI", "Trois familles de KPIs, à ne jamais confondre", color=D.PALETTE[0])
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
    # Passe de design 2026-07-23 — pattern 3 du catalogue deck-design-library
    # (« grille de cartes stat, une en accent ») : la Grille de maturité est la
    # seule carte en fill navy plein — c'est la famille que le chapitre détaille
    # ensuite (slide_maturite + message « le KPI = le delta T0→réévaluation ») ;
    # corps monté à 8.5pt (la densité s'absorbe par la police, pas par le vide).
    accent_idx = 2   # « Grille de maturité »
    def _bloc_puces(items):
        lignes = sum(_lignes("·  " + it, usable, 8.5) for it in items)
        return lignes * (8.5 * 1.15 / 72.0) + len(items) * (4 / 72.0)
    bullets_h = max(_bloc_puces(items) for *_, items in familles)
    card_h = 0.8 + bullets_h + 0.22
    top0 = CONTENT_TOP + max(0.0, (CONTENT_H - card_h) / 2)
    for i, (titre, color, sous, items) in enumerate(familles):
        x, w = col_x(i, n)
        accent = (i == accent_idx)
        if accent:
            D.add_rect(s, x, top0, w, card_h, fill=NAVY, rounded=True, radius=0.06)
            D.add_rect(s, x, top0, 0.07, card_h, fill=color, rounded=True, radius=0.5)
        else:
            D.add_card(s, x, top0, w, card_h, color)
        D.add_text(s, x + pad, top0 + 0.16, w - 2 * pad, 0.55, [
            (titre, dict(size=D.TYPE["small"], bold=True,
                         color="#ffffff" if accent else color, line_spacing=1.05)),
            (sous, dict(size=8.5, color="#aeb6d4" if accent else MUTED,
                        italic=True, space_before=2)),
        ])
        lignes = [(f"·  {it}", dict(size=8.5, color="#e8ebf5" if accent else NAVY,
                                    space_after=4, line_spacing=1.15))
                  for it in items]
        D.add_text(s, x + pad, top0 + 0.8, w - 2 * pad, card_h - 0.95, lignes)
    return s

# --- Brainstorm KPIs relancé (v2.1, docs/bmad-iap-cadrage.md §KPIs) — pourquoi
# chaque famille, quoi mesurer précisément, comment la mettre en place, et un
# exemple chiffré sur le cas nominal déjà posé pour l'export markdown.
def slide_kpis_pourquoi_quoi(prs):
    s = content_slide(prs, "KPI", "KPIs : pourquoi chaque famille, et quoi mesurer précisément", color=D.PALETTE[0])
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
    s = content_slide(prs, "KPI", "KPIs : comment on les met en place, concrètement", color=D.PALETTE[0])
    familles = [
        ("KPIs de mission", D.PALETTE[0], "iap-metrics-sre-finops-lead",
         "ServiceNow/Jira/CMDB si accès (preuves externes), sinon déclaratif — tagué DÉDUIT",
         "Continu, lu à chaque étape ②③⟲"),
        ("KPIs d'usage du module", D.PALETTE[1], "Le consultant, au fil des missions",
         "Journal de mission + bibliothèque de REX",
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
    s = content_slide(prs, "KPI", "KPIs en pratique : le cas nominal RUN massif, avant/après", color=D.PALETTE[0])
    D.add_text(s, MARGIN, CONTENT_TOP, CONTENT_W, 0.28, [
        ("Même fixture illustrative que le cas nominal de l'export markdown (chapitre IA) — pas un client réel.",
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


# --- Nouveau (brainstorm) : rendre tangible, dans le chapitre IA (acte 5,
# APRÈS la proposition), ce que "piste agentique" veut dire concrètement — 3
# candidats illustratifs ancrés sur des familles de gaspillage déjà cadrées
# (§Traitement des gaspillages), pas des exemples inventés hors cadre. Chaque
# carte reprend la couleur de sa famille de gaspillage (RUN=rouge, Financier=or,
# Cognitif=violet) via l'argument `color` — cohérence intentionnelle avec
# slide_familles, pas un hasard de palette.
def slide_agent_ia(prs, titre, nom_agent, famille, why, what, gain, color, note=None):
    s = content_slide(prs, "IA", titre, color=D.PALETTE[4])
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


# --- Nouveau (brainstorm) : la formule de priorisation (chapitre Proposition)
# cite "prudence IA" sans jamais l'expliquer — cette slide la décompose. Dans le
# chapitre IA, juste après le gate IA (qui l'a rejoint) et avant les 3 candidats
# d'agent : on pose d'abord le frein, ensuite seulement les cas d'usage.
def slide_prudence_ia(prs):
    s = content_slide(prs, "IA", "La prudence IA est un frein chiffré, pas un veto", color=D.PALETTE[4])
    D.add_text(s, MARGIN, CONTENT_TOP, CONTENT_W, 0.4, [
        ("Prudence IA = confidentialité + besoin de supervision + criticité de la décision",
         dict(size=D.TYPE["small"], bold=True, color=NAVY, line_spacing=1.2)),
    ])

    facteurs = [
        ("CONFIDENTIALITÉ", D.PALETTE[0],
         "Reprend directement la classification du gate IA (D0-D4, slide précédente) — "
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
         "chiffré du chapitre Proposition). Le score ne remplace pas l'arbitrage humain : il le rend "
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
    s = content_slide(prs, "Proposition",
                       "Le lien avec le SI du client change avec le niveau d'ambition, pas la méthode",
                       color=D.PALETTE[1])
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
         "Site web centralisé, orchestration assistée",
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
# Conception=or, etc.) — cohérence inter-slides voulue, pas un hasard. Clôt le
# chapitre IA : l'inventaire complet des agents, gate en socle.
def slide_architecture_agents(prs):
    s = content_slide(prs, "IA",
                       "Onze agents spécialisés, un seul bloquant : le gate confidentialité les traverse tous",
                       color=D.PALETTE[4])
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
            ("iap-operating-model", "Rôles, gouvernance, financement (décisions actées)"),
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
    slide_vision(prs)

    # === Chapitre 01 — CONTEXTE : le problème ===
    slide_chapitre(prs, "01", "Contexte",
                   "La double mission, et pourquoi cette transformation a du sens pour un client infra maintenant.",
                   D.PALETTE[0], "mountains", seed=0)
    slide_mission(prs)
    slide_pourquoi_contexte(prs)

    # === Chapitre 02 — PERSONAS : qui l'on transforme ===
    slide_chapitre(prs, "02", "Personas",
                   "Quatre parties prenantes interrogées séparément — leurs voix, leurs postures, les tensions.",
                   D.PALETTE[5], "forest", seed=0)
    slide_personas(prs)
    slide_personas_divergences(prs)

    # === Chapitre 03 — BESOINS & DOULEURS : ce qui fait mal ===
    slide_chapitre(prs, "03", "Besoins & douleurs",
                   "Les douleurs approfondies et mesurables, et les 8 familles de gaspillage qui les rangent.",
                   D.PALETTE[2], "ocean", seed=0)
    slide_douleurs(prs)
    slide_familles(prs)

    # === Chapitre 04 — PROPOSITION : notre réponse ===
    # Fil rouge : la THÈSE (why_iap) ouvre, puis la MÉTHODE scorée (gaspillages),
    # puis le sous-chapitre « Exemples » — désormais introduit par un VRAI
    # séparateur léger (slide_sous_chapitre, points ②/③ : l'arbitrage « kicker seul »
    # est levé pour ce groupe à la demande) — puis la cible, le fonctionnement, les
    # livrables, l'ambition et le lien SI. gate IA → IA ; trajectoire + bout-en-bout
    # → Démarche ; maturité + KPIs → KPI.
    slide_chapitre(prs, "04", "Proposition",
                   "Traiter l'infra comme un produit : la thèse, la méthode scorée, des exemples, la cible et les livrables.",
                   D.PALETTE[1], "dunes", seed=0)
    slide_why_iap(prs)
    slide_gaspillages(prs)
    # -- sous-chapitre « Exemples » (séparateur léger + 3 cas, kicker « Exemples ») --
    slide_sous_chapitre(prs, "Proposition", "Exemples",
                        "La méthode en pratique — trois cas illustratifs : priorisation chiffrée, "
                        "diagnostic tagué, recommandation actionnable.",
                        D.PALETTE[1])
    slide_exemple_priorisation(prs)
    slide_exemple_diagnostic(prs)
    slide_exemple_recommandation(prs)
    # -- suite Proposition : cible, fonctionnement, livrables, ambition, SI --
    slide_team_topologies(prs)
    slide_schema_fonctionnement(prs)
    slide_livrables_ppt(prs)
    slide_ambition(prs)
    slide_architecture_si(prs)

    # === Chapitre 05 — DÉMARCHE : comment on la mène (placée plutôt vers la fin) ===
    slide_chapitre(prs, "05", "Démarche",
                   "La trajectoire de mise en œuvre, son fil humain, et la vue bout-en-bout des livrables.",
                   D.PALETTE[3], "canyon", seed=0)
    slide_trajectoire(prs)
    # v2.4 : le fil humain décline la trame ①②③⟲ de slide_trajectoire côté
    # personnes — placé juste après elle, avant la vue bout-en-bout.
    slide_fil_humain(prs)
    slide_schema_bout_en_bout(prs)

    # === Chapitre 06 — IA : tirée APRÈS la proposition (l'IA amplifie, n'est jamais la réponse) ===
    slide_chapitre(prs, "06", "IA",
                   "L'IA au service de la réponse : le gate confidentialité, la prudence, les agents candidats, l'export.",
                   D.PALETTE[4], "nightsky", seed=0)
    slide_gate_ia(prs)
    slide_prudence_ia(prs)
    slide_agent_ia(
        prs, "Un agent de triage peut absorber le gaspillage RUN le plus répétitif",
        "Agent de triage de tickets", "RUN",
        "Les mêmes types de tickets reviennent depuis des années et mobilisent des experts "
        "seniors sur un travail répétitif à faible valeur — le gaspillage RUN le plus classique.",
        "Lit chaque ticket entrant, le classe selon un runbook déjà documenté et le route vers "
        "la bonne équipe. Le processus doit être explicite avant l'agent (préalable non "
        "négociable) — jamais l'inverse.",
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
        note=("Ces 3 candidats restent soumis au scoring (chapitre Proposition) et au gate IA (ouverture de ce chapitre) "
              "avant toute décision — des exemples illustratifs, pas une liste actée."))
    slide_export_markdown(prs)
    slide_architecture_agents(prs)

    # === Chapitre 07 — KPI : comment on mesure (clôture du deck) ===
    # Les 3 familles ouvrent, puis leur pourquoi/quoi et leur mise en place ; la
    # grille de maturité (slide_maturite, la 3e famille détaillée) vient ensuite
    # (déplacée après kpis_mise_en_place, point ①), et le cas nominal chiffré
    # ferme le deck.
    slide_chapitre(prs, "07", "KPI",
                   "Trois familles de KPIs à ne jamais confondre, leur mise en place, la grille de maturité, et le cas chiffré.",
                   D.PALETTE[0], "meadow", seed=1)
    slide_kpis(prs)
    slide_kpis_pourquoi_quoi(prs)
    slide_kpis_mise_en_place(prs)
    slide_maturite(prs)
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
