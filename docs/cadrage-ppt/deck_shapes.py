"""Primitives graphiques du deck (extraites mécaniquement de generate_deck.py) :
chips, badges, chevrons, bandeaux, texte riche, cellules d'en-tête.
"""

import pptx_deck_vscode3 as D
from deck_theme import (  # noqa: E402,F401 — extraction mécanique v2.46
    ACCENT,
    ACCENT1,
    ACCENT2,
    ACCENT_PLEIN,
    BORD_DROIT,
    CONTENT_BOTTOM,
    CONTENT_H,
    CONTENT_TOP,
    CONTENT_W,
    DK2,
    ENCRE,
    GAP,
    HERE,
    LAYOUT_CHAPITRE,
    LAYOUT_COUVERTURE,
    LAYOUT_TITRE_SEUL,
    LAYOUT_VIDE,
    LAYOUT_VISUEL_DROITE,
    LINE,
    MARGIN,
    MUTED,
    NAVY,
    RAYON_COIN_IN,
    SEVERITE,
    SUPPORT,
    SUPPORT_LIGNE,
    TEMPLATE,
    TH,
    TRACK,
    WHITE,
    _add_rect_arrondi,
    _add_rect_brut,
    _exiger_template,
    _rgb,
    encre_de,
    new_prs,
)
from pptx.enum.dml import MSO_LINE_DASH_STYLE
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt


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
    """Wrapper de `D.add_chip` (extrait vers pptx_deck.py le 2026-09-11 ; garde
    ce nom pour ne pas toucher les ~12 sites d'appel du generateur, grep
    \\bchip\\( generate_deck.py hors ce commentaire).

    Garde D1 (arbitrage du 2026-09-10, ~1,9:1 sur blanc) : le cyan (ACCENT /
    ACCENT_PLEIN) ne porte JAMAIS de texte. Beaucoup d'appelants passent une
    `color` de palette (« un sur N en accent ») sans se soucier du texte par
    defaut blanc du chip — quand cette couleur vaut le cyan ET que l'appelant
    n'a pas deja choisi un texte lisible, l'aplat retombe sur NAVY : l'element
    distingue garde un aplat PLEIN (navy, pas cyan), le texte blanc reste
    lisible dessus. Un appelant qui a deja pose un `text_color` explicite
    (ex. NAVY sur un chip cyan sur panneau navy, slide gate) n'est pas
    touche : ce n'est pas le defaut corrige ici."""
    if str(color).lower() == str(ACCENT).lower() and str(text_color).lower() == "#ffffff":
        color = NAVY
    return D.add_chip(slide, x, y, w, h, label, color, text_color=text_color, size=size)


# --- Helpers du schéma « parcours de mission » (slide_offre_iap, v2.8) : pas de
# CONNECTOR/oval réutilisable ailleurs dans le générateur avant ce schéma, donc
# petits helpers dédiés plutôt qu'un détour par pptx_deck (déjà surchargé de
# add_rect/add_card génériques — ceux-ci sont spécifiques à ce diagramme).
def _oval(slide, x, y, w, h, fill=None, line=None, line_w=1.0):
    """Ellipse simple (nœuds « entrée/sortie » du schéma de parcours)."""
    shp = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x), Inches(y), Inches(w), Inches(h))
    try:
        shp.shadow.inherit = False
    except Exception:
        pass
    if fill is None:
        shp.fill.background()
    else:
        shp.fill.solid()
        shp.fill.fore_color.rgb = _rgb(fill)
    if line is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = _rgb(line)
        shp.line.width = Pt(line_w)
    shp.text_frame.paragraphs[0].text = ""
    return shp


def _pale(hexcolor, factor=0.1):
    """Teinte pâle d'une couleur PALETTE (mélange à `factor` avec du blanc) —
    fond de carte discret qui garde l'accent de couleur lisible sans l'écraser."""
    r, g, b = (int(hexcolor[i:i + 2], 16) for i in (1, 3, 5))
    mix = lambda c: round(c * factor + 255 * (1 - factor))
    return f"#{mix(r):02x}{mix(g):02x}{mix(b):02x}"


def _dashed_rect(slide, x, y, w, h, fill, line, line_w=1.0, radius=0.12):
    """Rectangle à bordure pointillée (« mécanisme additif » du schéma de parcours) —
    python-pptx n'expose le style de trait qu'en LineFormat.dash_style, pas via
    D.add_rect (qui ne prend pas ce paramètre)."""
    shp = D.add_rect(slide, x, y, w, h, fill=fill, line=line, line_w=line_w,
                      rounded=True, radius=radius)
    shp.line.dash_style = MSO_LINE_DASH_STYLE.DASH
    return shp


# ---- Helpers « refonte graphique v3 » (2026-09-04, exercice d'idéation sur 2
# decks OCTO réels — cf. gen_check_slide_synthese_v3_refonte.py pour la trace
# complète du système de design). Système : conteneur = contour seul, jamais
# un aplat plein ; étiquette courte = pilule pleine ; chevron = marqueur de
# séquence ; badge à cheval sur un bord plutôt que relié par une flèche ;
# emphase en ligne (mot-clé gras dans une phrase normale) plutôt qu'une
# phrase entière en gras/italique ; barre d'accent verticale ; bandeau de
# clôture citation (guillemet blanc + filet cyan en aplat, v2.39).
QUOTE = "“"   # guillemet ouvrant décoratif (confirmé dans le cmap Outfit)
DOT = "•"     # point isolé de clôture (confirmé dans le cmap Outfit)


def _rich(slide, x, y, w, h, paragraphs, anchor=MSO_ANCHOR.TOP, wrap=True):
    """Zone de texte MULTI-RUNS par paragraphe : `paragraphs` = liste de
    (runs, para_opts) où runs = liste de (texte, run_opts). Nécessaire pour
    l'emphase EN LIGNE (mot-clé gras/coloré au milieu d'une phrase normale) —
    `D.add_text` ne pose qu'un seul run par paragraphe."""
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = wrap
    tf.vertical_anchor = anchor
    for m in ("margin_left", "margin_right", "margin_top", "margin_bottom"):
        setattr(tf, m, 0)
    for i, (runs, popts) in enumerate(paragraphs):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = popts.get("align", PP_ALIGN.LEFT)
        if "space_before" in popts:
            p.space_before = Pt(popts["space_before"])
        if "space_after" in popts:
            p.space_after = Pt(popts["space_after"])
        if "line_spacing" in popts:
            p.line_spacing = popts["line_spacing"]
        for texte, ropts in runs:
            r = p.add_run()
            r.text = texte
            r.font.size = Pt(ropts.get("size", 10))
            r.font.bold = ropts.get("bold", False)
            r.font.italic = ropts.get("italic", False)
            r.font.color.rgb = _rgb(ropts.get("color", NAVY))
    return box


def _split_emph(texte, emph):
    """Coupe `texte` en (avant, emph, après) — la sous-phrase `emph` doit
    exister MOT POUR MOT dans `texte` (lève si absente : garde-fou contre une
    emphase qui déviendrait du texte source)."""
    i = texte.index(emph)
    return texte[:i], emph, texte[i + len(emph):]


def _chevron_shape(slide, x, y, w, h, fill=WHITE, line=MUTED, line_w=1.25):
    """Silhouette « pilule + pointe » (encoche gauche, pointe droite) — le
    seul preset natif python-pptx qui rend cette silhouette SANS rotation
    (une rotation fausserait `verifier_geometrie`, qui mesure le cadre non
    pivoté — piège déjà documenté dans ce dépôt pour un groupe pivoté 180°)."""
    shp = slide.shapes.add_shape(MSO_SHAPE.CHEVRON, Inches(x), Inches(y), Inches(w), Inches(h))
    try:
        shp.shadow.inherit = False
    except Exception:
        pass
    if fill is None:
        shp.fill.background()
    else:
        shp.fill.solid()
        shp.fill.fore_color.rgb = _rgb(fill)
    if line is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = _rgb(line)
        shp.line.width = Pt(line_w)
    shp.text_frame.paragraphs[0].text = ""
    return shp


def _chevron_arrow(slide, x, y, w, h, color=MUTED, frac_w=0.72, frac_h=0.5):
    """Petite flèche de flux (chevron fin) centrée dans la cellule (x,y,w,h) —
    remplace le glyphe texte '→' entre 2 pilules constat/réponse."""
    cw, ch = w * frac_w, h * frac_h
    _chevron_shape(slide, x + (w - cw) / 2, y + (h - ch) / 2, cw, ch,
                   fill=WHITE, line=color, line_w=1.4)


def _badge(slide, cx, cy, d, color, symbol, filled=True, dashed=False, fill=None,
           text_color=None, size=12, bold=True):
    """Wrapper de `D.add_badge` (extrait vers pptx_deck.py le 2026-09-11 ; garde
    ce nom pour ne pas toucher les ~6 sites d'appel du generateur). WHITE
    (theme lt1 de CE gabarit) mesure a #FFFFFF, identique au litteral '#ffffff'
    dont add_badge se sert par defaut — repli confirme, pas suppose.

    Garde D1 (meme regle que `chip` ci-dessus) : un badge REMPLI (`filled`)
    dont la couleur vaut le cyan ET dont l'appelant n'a pas deja choisi un
    `text_color` retombe sur un aplat NAVY — pas de texte blanc sur cyan a
    ~1,9:1. Le badge CONTOUR (`filled=False`) n'est pas concerne : il n'a
    jamais de fond cyan plein, juste un trait."""
    if filled and str(color).lower() == str(ACCENT).lower() and text_color is None:
        color = NAVY
    return D.add_badge(slide, cx, cy, d, color, symbol, filled=filled, dashed=dashed,
                        fill=fill, text_color=text_color, size=size, bold=bold)


def _bandeau_cloture(slide, texte, bas_contenu, nom_slide, size=12):
    """Bandeau de clôture dimensionné par SON TEXTE et posé en bas de slide.

    Deux règles de dimensionnement coexistaient, dont une fausse. La variante
    « étirée » (`h = CONTENT_BOTTOM - y`) remplit tout le vide restant : quand
    le contenu est court, elle produit un pavé navy de plus d'un pouce de haut
    pour une phrase — constaté au rendu du 2026-09-10, et deux slides du même
    chapitre l'utilisaient encore juste à côté de deux slides corrigées.
    Ici la hauteur vient du texte, le blanc restant respire, et le
    chevauchement échoue AU BUILD plutôt qu'à la relecture.
    """
    h = _lignes(texte, CONTENT_W - 0.76, size) * (size * 1.2 / 72.0) + 0.34
    top = CONTENT_BOTTOM - h
    if top < bas_contenu:
        raise SystemExit(
            f"{nom_slide} : le bandeau de clôture chevauche le contenu "
            f"({bas_contenu - top:.3f}in de trop) — resserrer avant de régénérer."
        )
    _quote_banner(slide, MARGIN, top, CONTENT_W, h, texte, size=size)


def _quote_banner(slide, x, y, w, h, text, size=15.5):
    """Bandeau de clôture : fond navy plein (la phrase qu'on retient reste le
    SEUL aplat plein d'une slide en système « contour ») + guillemet décoratif
    blanc en coin + filet cyan en aplat sur le bord gauche.

    v2.39 (revue design 2026-09-23) : le guillemet et le point final étaient
    des RUNS de texte cyan — la charte (arbitrage 2026-09-10) interdit le cyan
    sur tout texte ou glyphe. Le cyan survit en aplat (filet), le point final
    décoratif disparaît (la phrase a déjà sa ponctuation)."""
    D.add_rect(slide, x, y, w, h, fill=NAVY, rounded=True, radius=0.10)
    D.add_rect(slide, x + 0.07, y + 0.10, 0.05, max(0.05, h - 0.20), fill=ACCENT)
    D.add_text(slide, x + 0.18, y + 0.02, 0.4, min(0.4, h - 0.04), [
        (QUOTE, dict(size=24, bold=True, color=WHITE)),
    ], anchor=MSO_ANCHOR.TOP)
    _rich(slide, x + 0.56, y, w - 0.76, h, [
        ([(text, dict(size=size, bold=True, color=WHITE))],
         dict(align=PP_ALIGN.CENTER)),
    ], anchor=MSO_ANCHOR.MIDDLE)


def _noeud_socle(slide, x, y, w, h, titre, sous_titre=None, oval=False):
    """Nœud « mouvement du socle » (toujours présent) du schéma de parcours —
    fill bleu-gris clair, bordure navy ; ellipse pour les nœuds d'entrée/sortie."""
    fill = "#dce6f5"
    if oval:
        _oval(slide, x, y, w, h, fill=fill, line=NAVY, line_w=1.0)
    else:
        D.add_rect(slide, x, y, w, h, fill=fill, line=NAVY, line_w=1.0, rounded=True, radius=0.14)
    lignes = [(titre, dict(size=8, bold=True, color=NAVY, align=PP_ALIGN.CENTER, line_spacing=1.0))]
    if sous_titre:
        lignes.append((sous_titre, dict(size=8, color=MUTED, align=PP_ALIGN.CENTER,
                                         italic=True, space_before=1, line_spacing=1.0)))
    D.add_text(slide, x + 0.04, y, w - 0.08, h, lignes, anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)


def _pilule_variante(slide, x, y, w, h, texte, size=8):
    """Pilule « variante conditionnée au contexte » (sable/or) du schéma de parcours.
    Si `h` est None, la hauteur est calculée à partir du texte (pilules « si contexte
    politique », plus longues que les pilules courtes « Contexte léger/politique ») —
    retourne toujours la hauteur effectivement utilisée."""
    pad = 0.03
    if h is None:
        lignes = _lignes(texte, w - 2 * pad, size)
        h = 2 * pad + lignes * (size * 1.15 / 72.0)
    D.add_rect(slide, x, y, w, h, fill="#E7E9EE", line=ENCRE, line_w=1.0,
               rounded=True, radius=0.35)
    D.add_text(slide, x + 0.05, y, w - 0.10, h, [
        (texte, dict(size=size, bold=True, color=ENCRE, align=PP_ALIGN.CENTER, line_spacing=1.05)),
    ], anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
    return h


def _note_mecanisme(slide, x, y, w, titre, corps, title_size=8, body_size=8, pad=0.04):
    """Encadré pointillé pâle = « mécanisme additif » (extension, checklist transverse)
    du schéma de parcours — hauteur calculée à partir du corps, jamais fixe (cf. défaut
    « panneau sur-étiré » du dépôt) ; retourne la hauteur effectivement utilisée."""
    lignes = _lignes(corps, w - 2 * pad, body_size)
    # v2.43 : +0.06 — à 8 pt, l'estimation laissait le corps déborder au rendu.
    h = 2 * pad + (title_size * 1.1 / 72.0) + 0.05 + lignes * (body_size * 1.2 / 72.0)
    _dashed_rect(slide, x, y, w, h, fill="#F2F4F8", line=ENCRE, line_w=0.9, radius=0.10)
    # v2.45 : +0.10 en x — le coin plus arrondi mordait sur la 1re lettre.
    D.add_text(slide, x + pad + 0.10, y + pad * 0.6, w - 2 * pad - 0.20, h - pad * 1.2, [
        (titre, dict(size=title_size, bold=True, color=ENCRE, line_spacing=1.05)),
        (corps, dict(size=body_size, color=MUTED, italic=True, space_before=2, line_spacing=1.15)),
    ])
    return h


def _fleche_h(slide, x, y, w, h, color=MUTED, size=10):
    """Flèche « → » centrée dans une cellule (vocabulaire de flux du schéma de
    parcours — même simplification texte que slide_iap_contexte_client)."""
    D.add_text(slide, x, y, w, h, [
        ("→", dict(size=size, bold=True, color=encre_de(color), align=PP_ALIGN.CENTER)),
    ], anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)


# --- Badge de série (v2.6, point ④) : les 4 slides « proposition de déploiement
# agentic chez le client » du chapitre IA (3 agents candidats + export
# markdown) portent le MÊME petit badge — signal visuel récurrent et discret qui
# les relie à la zone « déploiement agentic » du schéma d'architecture
# (slide_iap_contexte_client, chapitre 08). Renvoi par CHAPITRE, jamais par
# numéro de page (les numéros bougent). ENCRE = encre navy, la couleur du
# chapitre IA, la même que la zone du schéma.
BADGE_AGENTIC_W = 2.3


def badge_deploiement_agentic(slide):
    x = BORD_DROIT - BADGE_AGENTIC_W
    h = 0.42
    D.add_rect(slide, x, CONTENT_TOP, BADGE_AGENTIC_W, h, fill="#ffffff",
               line=ENCRE, line_w=1.0, rounded=True, radius=0.18)
    D.add_text(slide, x + 0.12, CONTENT_TOP, BADGE_AGENTIC_W - 0.24, h, [
        ("DÉPLOIEMENT AGENTIC",
         dict(size=8, bold=True, color=ENCRE, line_spacing=1.1)),
        ("cf. les trois niveaux d'ambition",
         dict(size=8, italic=True, color=MUTED, space_before=1)),
    ], anchor=MSO_ANCHOR.MIDDLE)


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
