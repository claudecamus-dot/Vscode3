"""Refonte GRAPHIQUE v3 (exploratoire, hors production) de 3 slides du check
isole — pas un ajustement mineur : la FORME de chaque slide est redessinee en
s'inspirant de 2 vrais decks OCTO fournis en reference et etudies PAGE PAR
PAGE (rendus en PNG via PyMuPDF puis regardes, pas seulement lus en XML) :

  - "OCTO_GROUND - Proposition accompagnement a la transfo mode produit a
    l'echelle.pptx.pdf" (27 pages, meme theme navy/cyan EXACT que notre
    template) ;
  - "FDXIA - Fondamentaux de l'IA Generative...pdf" (235 pages, echantillon
    de 15 pages, meme famille de polices, complementaire pour les motifs de
    sommaire/citation/emphase).

Systeme de design extrait de ces 2 references (pas une liste de motifs isoles
recopies au hasard — un vocabulaire coherent, reutilise a l'identique sur les
3 slides) :
  1. CONTENEUR = rectangle a coins arrondis en CONTOUR SEUL (fill blanc, trait
     de couleur), jamais un aplat gris/couleur plein — vu sur OCTO_GROUND
     p.3 (bloc de constats), p.8 (4 cartes Strategie/Discovery/Delivery/
     Activation), p.10 (3 roles). Remplace les cartes "fond plein" ou "liseré
     gauche" de la version actuelle.
  2. ETIQUETTE COURTE = pilule PLEINE (couleur unie, texte blanc/navy) —
     reservee aux petites metadonnees (duree, label AVANT/APRES, numero) :
     vu p.11/12 (pilules "Strategie"/"Discovery" pleines a cote de bulles de
     description en contour). Un conteneur reste en contour ; une etiquette
     compacte reste pleine — jamais l'inverse.
  3. CHEVRON = marqueur de sequence/flux (etiquette de titre d'etape, fleche
     de connexion) — approx via le preset MSO_SHAPE.CHEVRON (rectangle a
     encoche gauche + pointe droite), le seul preset natif python-pptx qui
     rend cette silhouette SANS rotation (une rotation aurait fausse
     `verifier_geometrie`, qui mesure le cadre non pivote — piege deja
     documente dans ce depot pour un groupe pivote a 180°). Inspire de
     OCTO_GROUND p.7 (etiquettes numerotees "pilule + pointe") et p.13
     (grande fleche de continuite) ; a defaut d'un preset "pilule a gauche +
     pointe a droite" exact, CHEVRON est l'approximation la plus proche sans
     geometrie custom risquee — assume et documente, pas invente en secret.
  4. BADGE QUI CHEVAUCHE UN BORD = pastille (pleine pour une etape numerotee,
     en pointilles pour une etape optionnelle) centree SUR le bord haut d'une
     forme voisine plutot que posee a cote avec une fleche — vu sur FDXIA
     p.6 (pastille pictogramme+numero a cheval sur le bord de l'icone
     teardrop) et OCTO_GROUND p.7 (pastille numerotee a cheval sur le bord
     gauche de la pilule). Adapte ici en chevauchement de bord HAUT plutot
     que gauche : nos colonnes ne laissent que 0.10in d'ecart, un
     chevauchement lateral aurait mordu sur la colonne voisine (risque non
     detecte par `verifier_geometrie`, qui ne verifie QUE les sorties de
     slide, jamais les collisions entre formes — lecon du depot).
  5. EMPHASE EN LIGNE = 1-2 mots-cles en gras/couleur A L'INTERIEUR d'une
     phrase de poids normal, plutot qu'une phrase entiere en gras ou en
     italique monochrome — vu sur OCTO_GROUND p.3/p.4 et FDXIA p.10 (mot-cle
     colore DANS une phrase navy). Remplace les phrases entierement en italique
     MUTED ou entierement en gras NAVY de la version actuelle.
  6. BARRE VERTICALE D'ACCENT = trait fin colore a gauche d'un chapo/d'un
     libelle important — vu sur FDXIA p.10. Remplace l'italique nu en tete de
     slide.
  7. GUILLEMET DECORATIF + POINT ISOLE = chaque bandeau de cloture (la phrase
     qu'on retient) porte un "“" cyan surdimensionne en coin — signature
     "citation" reprise des refs — et se termine par un point cyan ISOLE
     apres le dernier mot (motif de detail de marque signale par l'utilisateur ;
     confirmation faible dans les refs elles-memes — seule la page hors-charte
     "La Conference." p.20 de FDXIA montre un point colore apres un mot de
     titre — donc applique ici de façon deliberement MINIMALE : seulement sur
     les 3 bandeaux de cloture, jamais sur un titre).

Regle absolue : generate_deck.py et pptx_deck.py ne sont PAS touches. Ce
fichier importe `generate_deck` comme une bibliotheque (template, palette,
helpers, `content_slide`) et redefinit ENTIEREMENT le corps des 3 fonctions
cible (copie-adaptee, pas un simple appel : la FORME change, pas seulement
une passe de post-traitement). Le contenu textuel (chiffres, faits, phrases)
reste RIGOUREUSEMENT le meme qu'aujourd'hui, verifie mot a mot contre
generate_deck.py au moment de l'ecriture de ce fichier — seules les phrases
qui devaient etre coupees en (debut gras, reste) pour l'emphase en ligne ont
ete re-segmentees, jamais reformulees.

Police Outfit appliquee en post-traitement, mecanisme IDENTIQUE a
`gen_check_slide_synthese_v2_propositions.py` (memes 4 glyphes ①②③⟲ forces en
Arial, seule variante de la police sans repli correct sur PowerPoint COM).

Usage : python gen_check_slide_synthese_v3_refonte.py
Sortie : check_slide_synthese-v3-refonte.pptx (a cote de ce script).
"""
import os

import generate_deck as G
from pptx.enum.dml import MSO_LINE_DASH_STYLE
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

D = G.D
NAVY, DK2, MUTED = G.NAVY, G.DK2, G.MUTED
ACCENT1, ACCENT2, ACCENT = G.ACCENT1, G.ACCENT2, G.ACCENT
LINE, TRACK, WHITE = G.LINE, G.TRACK, G.WHITE
MARGIN, BORD_DROIT = G.MARGIN, G.BORD_DROIT
CONTENT_TOP, CONTENT_BOTTOM, CONTENT_W = G.CONTENT_TOP, G.CONTENT_BOTTOM, G.CONTENT_W
_lignes = G._lignes
_pale = G._pale
_rgb = G._rgb
col_x = G.col_x
chip = G.chip
content_slide = G.content_slide

QUOTE = "“"   # " — guillemet ouvrant decoratif (confirme dans le cmap Outfit)
DOT = "•"     # • — point isole de cloture (confirme dans le cmap Outfit)


# --------------------------------------------------------------- helpers v3
def _rich(slide, x, y, w, h, paragraphs, anchor=MSO_ANCHOR.TOP, wrap=True):
    """Zone de texte MULTI-RUNS par paragraphe : `paragraphs` = liste de
    (runs, para_opts) ou runs = liste de (texte, run_opts). Necessaire pour
    l'emphase EN LIGNE (mot-cle gras/colore au milieu d'une phrase normale) —
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
    """Coupe `texte` en (avant, emph, apres) — la sous-phrase `emph` doit
    exister MOT POUR MOT dans `texte` (leve si absente : garde-fou contre une
    emphase qui deriverait du texte source)."""
    i = texte.index(emph)
    return texte[:i], emph, texte[i + len(emph):]


def _chevron_shape(slide, x, y, w, h, fill=WHITE, line=MUTED, line_w=1.25):
    """Silhouette 'pilule + pointe' (encoche gauche, pointe droite) — voir
    docstring de module, point 3, pour le choix de ce preset."""
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


def _badge(slide, cx, cy, d, color, symbol, filled=True, dashed=False, fill=None,
           text_color=None, size=12, bold=True):
    """Pastille ronde centree en (cx, cy) — `filled` pour une etape "en dur"
    (fond plein), sinon contour seul (etape optionnelle, `dashed=True`)."""
    x, y = cx - d / 2, cy - d / 2
    if filled:
        D.add_rect(slide, x, y, d, d, fill=color, rounded=True, radius=0.5)
        tc = text_color or WHITE
    else:
        shp = D.add_rect(slide, x, y, d, d, fill=(fill or WHITE), line=color,
                          line_w=1.2, rounded=True, radius=0.5)
        if dashed:
            shp.line.dash_style = MSO_LINE_DASH_STYLE.DASH
        tc = text_color or color
    D.add_text(slide, x, y, d, d, [
        (symbol, dict(size=size, bold=bold, color=tc, align=PP_ALIGN.CENTER)),
    ], anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)


def _quote_banner(slide, x, y, w, h, text, size=15.5):
    """Bandeau de cloture : fond navy plein (la phrase qu'on retient reste le
    SEUL aplat plein de la slide, cf. rapport) + guillemet decoratif cyan en
    coin + point isole cyan apres le dernier mot."""
    D.add_rect(slide, x, y, w, h, fill=NAVY, rounded=True, radius=0.10)
    D.add_text(slide, x + 0.14, y + 0.02, 0.4, min(0.4, h - 0.04), [
        (QUOTE, dict(size=24, bold=True, color=ACCENT)),
    ], anchor=MSO_ANCHOR.TOP)
    _rich(slide, x + 0.20, y, w - 0.40, h, [
        ([(text, dict(size=size, bold=True, color=WHITE)),
          ("  " + DOT, dict(size=size, bold=True, color=ACCENT))],
         dict(align=PP_ALIGN.CENTER)),
    ], anchor=MSO_ANCHOR.MIDDLE)


def _chevron_arrow(slide, x, y, w, h, color=MUTED, frac_w=0.72, frac_h=0.5):
    """Petite fleche de flux (chevron fin) centree dans la cellule (x,y,w,h) —
    remplace le glyphe texte '→' des paires constat/reponse."""
    cw, ch = w * frac_w, h * frac_h
    _chevron_shape(slide, x + (w - cw) / 2, y + (h - ch) / 2, cw, ch,
                   fill=WHITE, line=color, line_w=1.4)


# ============================================================== SLIDE 1
def slide_specificites_infra(prs):
    s = content_slide(prs, "Les spécificités de l'infra",
                       "D'un guichet sursollicité à une infra as a product — l'IA rend ce virage nécessaire.",
                       color=ACCENT)

    COUL_DOULEUR = MUTED
    COUL_REPONSE = ACCENT

    arrow_w = 0.60
    pill_w = (CONTENT_W - arrow_w) / 2
    pill_pad = 0.17

    def _pill_h(texte, taille=11):
        return _lignes(texte, pill_w - 2 * pill_pad, taille) * (taille * 1.2 / 72.0) + 2 * pill_pad

    def _pill(x, y, w, h, texte, accent, taille=11, radius=0.5):
        D.add_rect(s, x, y, w, h, fill=WHITE, line=accent, line_w=1.3, rounded=True, radius=radius)
        D.add_text(s, x + pill_pad, y, w - 2 * pill_pad, h, [
            (texte, dict(size=taille, bold=True, color=NAVY, align=PP_ALIGN.CENTER, line_spacing=1.15)),
        ], anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)

    # --- Paire 1 : douleur (2 lignes -> rectangle a coins arrondis, pas une
    # capsule : cf. regle "conteneur multi-lignes = rectangle, etiquette
    # courte 1 ligne = capsule", point 1/2 de la docstring de module.
    douleur_titre = "Sortir de la sursollicitation et du guichet"
    douleur_sub_plain = ("Des équipiers qui font trop de choses, sont engorgés — "
                          "décommissionnement jamais fait, trop de RUN au quotidien.")
    dw = pill_w - 2 * pill_pad
    titre_h1 = _lignes(douleur_titre, dw, 11) * (11 * 1.2 / 72.0) + 0.03
    sub_h1 = _lignes(douleur_sub_plain, dw, 9) * (9 * 1.25 / 72.0) + 0.03
    h1 = max(2 * pill_pad + titre_h1 + 0.06 + sub_h1, _pill_h("Assainir et travailler le gaspillage"))

    y = CONTENT_TOP + 0.05
    row_gap = 0.13
    D.add_rect(s, MARGIN, y, pill_w, h1, fill=WHITE, line=COUL_DOULEUR, line_w=1.3, rounded=True, radius=0.13)
    inner_y = y + (h1 - (titre_h1 + 0.06 + sub_h1)) / 2
    D.add_text(s, MARGIN + pill_pad, inner_y, dw, titre_h1, [
        (douleur_titre, dict(size=11, bold=True, color=NAVY, align=PP_ALIGN.CENTER, line_spacing=1.15)),
    ], align=PP_ALIGN.CENTER)
    avant_e, emph_e, apres_e = _split_emph(
        douleur_sub_plain, "décommissionnement jamais fait, trop de RUN au quotidien.")
    _rich(s, MARGIN + pill_pad, inner_y + titre_h1 + 0.06, dw, sub_h1, [
        ([(avant_e, dict(size=9, italic=True, color=MUTED)),
          (emph_e, dict(size=9, bold=True, color=NAVY))],
         dict(align=PP_ALIGN.CENTER, line_spacing=1.25)),
    ])
    _chevron_arrow(s, MARGIN + pill_w, y, arrow_w, h1, color=MUTED)
    _pill(MARGIN + pill_w + arrow_w, y, pill_w, h1, "Assainir et travailler le gaspillage",
          COUL_REPONSE, radius=0.13)
    y += h1 + row_gap

    # --- Paire 2 : 2 phrases courtes -> capsules pleine hauteur (etiquette).
    intention_servir = "Mieux servir les utilisateurs, avec une approche as a service"
    reponse_utilisateurs = "Une infra plus recentrée sur ces utilisateurs"
    h2 = max(_pill_h(intention_servir), _pill_h(reponse_utilisateurs))
    _pill(MARGIN, y, pill_w, h2, intention_servir, COUL_DOULEUR)
    _chevron_arrow(s, MARGIN + pill_w, y, arrow_w, h2, color=MUTED)
    _pill(MARGIN + pill_w + arrow_w, y, pill_w, h2, reponse_utilisateurs, COUL_REPONSE)
    y += h2 + row_gap

    # --- Escalade IA : badge a cheval sur le coin haut-gauche de la carte
    # (point 4 de la docstring) au lieu d'un badge separe relie par une
    # fleche — la carte devient un CONTOUR (point 1), plus un aplat DK2.
    label_h = 0.16
    D.add_text(s, MARGIN, y + 0.02, CONTENT_W, label_h, [
        ("AVEC L'ARRIVÉE DE L'IA", dict(size=8, bold=True, color=NAVY)),
    ])
    esc_top = y + 0.02 + label_h + 0.06
    badge_d = 0.46
    card_x = MARGIN + badge_d / 2
    card_top = esc_top + badge_d / 2
    card_w = BORD_DROIT - card_x
    alert_pad = 0.22
    alert_tw = card_w - 2 * alert_pad
    alert_title = "UNE SURSOLLICITATION EXACERBÉE"
    alert_body = ("Trop de demandes, des équipes engorgées — la même pression que le "
                  "guichet d'hier, amplifiée par l'IA plutôt que résolue par elle.")
    title_h = _lignes(alert_title, alert_tw, 9.5) * (9.5 * 1.2 / 72.0) + 0.03
    body_h = _lignes(alert_body, alert_tw, 9) * (9 * 1.25 / 72.0) + 0.03
    text_top = card_top + badge_d / 2 + 0.05
    title_y = text_top
    body_y = title_y + title_h + 0.05
    card_h = (body_y + body_h + 0.13) - card_top

    D.add_rect(s, card_x, card_top, card_w, card_h, fill=WHITE, line=DK2, line_w=1.4, rounded=True, radius=0.09)
    D.add_text(s, card_x + alert_pad, title_y, alert_tw, title_h, [
        (alert_title, dict(size=9.5, bold=True, color=DK2)),
    ])
    av_e, em_e, ap_e = _split_emph(alert_body, "amplifiée par l'IA plutôt que résolue par elle.")
    _rich(s, card_x + alert_pad, body_y, alert_tw, body_h, [
        ([(av_e, dict(size=9, color=NAVY)),
          (em_e, dict(size=9, bold=True, color=DK2))],
         dict(line_spacing=1.25)),
    ])
    _badge(s, card_x, card_top, badge_d, NAVY, "IA", filled=True, size=11)
    y = card_top + card_h + 0.14

    # --- Cloture : bandeau citation (point 7).
    concl_top = y
    concl_h = CONTENT_BOTTOM - concl_top
    if concl_h < 0.30:
        raise SystemExit(
            f"slide_specificites_infra (v3) : plus assez de place pour le bandeau de "
            f"cloture ({concl_h:.3f}in) — resserrer la slide avant de régénérer."
        )
    _quote_banner(s, MARGIN, concl_top, CONTENT_W, concl_h, "L'objectif : infra as a product.")
    return s


# ============================================================== SLIDE 2
def slide_synthese_pourquoi_quoi_comment(prs):
    s = content_slide(prs, "Exec summary",
                       "Comment aller vers l'infra as a product — le volet organisationnel "
                       "d'une mission tech.",
                       color=NAVY)

    marge_g = 0.38
    bord_d = 9.2
    bas_max = 5.58
    largeur = bord_d - marge_g
    bord_d_haut = 10.0 - marge_g
    largeur_haut = bord_d_haut - marge_g
    ecart = 0.10

    # v4 : retour utilisateur — le chapô ("D'où l'on part...") et sa zone
    # SUPPRIMÉS entièrement. L'espace libéré (~0.36in) remonte la rangée de
    # séquences et aère la bande badge/chevron/durée, jugée trop écrasée
    # face au reste de la colonne.
    debut = 0.85

    # Chaque etape porte desormais aussi son ACTIVITE TECHNIQUE en miroir
    # (champ `tech`, avant-dernier de chaque tuple) — retour utilisateur :
    # la punchline affirme que "le volet organisationnel fait reussir le
    # volet tech", ce lien doit se voir etape par etape, pas seulement une
    # fois a la fin. Formulations condensees (substance du retour utilisateur,
    # raccourcies pour tenir sur 2 lignes dans une colonne de ~1.7in) :
    # audit infra / referentiel technique cible / chantiers pilotes /
    # industrialisation CI-CD / reevaluation dette technique+KPI infra.
    phases = [
        ("①", "Assessment flash", "1–2 sem.", NAVY, False,
         "Schéma déjà cadré : Collecte → Diagnostic → Conception → Restitution.",
         "Collecte → Diagnostic → Conception → Restitution.",
         "TECH : dette et risques cartographiés",
         "Partager un diagnostic et argumenter la décision d'engager ou non.",
         "Livrer un deck exécutif de restitution."),
        ("+", "OPTIONNEL — Constitution du TOM", "3–4 sem.", ACCENT2, True,
         "Formalise le Target Operating Model : rôles, gouvernance, adapté à l'organisation "
         "et aux contraintes du client INFRA.",
         "Target Operating Model",
         "TECH : référentiel standards/outillage",
         "Adapter le cadre de référence à l'organisation et aux contraintes du client.",
         "Livrer le TOM et la roadmap de déploiement."),
        # v5 : retour utilisateur (édité dans le .pptx, réintégré ici) —
        # "1-2 équipes... mode Coach dominant" -> "équipes pilotes volontaires"
        # (le volontariat remplace le compte et le mode de pilotage).
        ("②", "Premier déploiement", "4–5 sem.", DK2, False,
         "Des équipes pilotes volontaires ; agent IA si retenu : qualifier, cadrer, "
         "mandater.",
         "équipes pilotes volontaires",
         "TECH : décommissionnement, observabilité",
         "Prouver la valeur sur le pilote et identifier les ajustements avant généralisation.",
         "Livrer l'évaluation du déploiement pilote (deck)."),
        ("③", "Implémentation itérative", "→ T+6-12 mois", DK2, False,
         "Généralisation équipe par équipe, bascule Coach → Délégué ; agent IA supervisé "
         "puis délégué.",
         "Coach → Délégué",
         "TECH : CI/CD, infra as code",
         "Généraliser l'adoption et déléguer l'agent IA si la piste est retenue.",
         "Livrer un deck de comité de pilotage (périodique)."),
        ("⟲", "Boucle de réévaluation", "T+6-12 mois", ACCENT, False,
         "iap-re-assessment reboucle vers la Collecte — alimente la bibliothèque de REX.",
         "bibliothèque de REX",
         "TECH : dette technique et KPI infra",
         "Mesurer le delta T0 → réévaluation et capitaliser le REX pour la mission suivante.",
         "Livrer un deck de bilan / ré-évaluation."),
    ]
    n = len(phases)
    # Le badge ne chevauche que le bord HAUT du chevron sur une petite marge
    # (`overlap`) — pas son centre : un badge_d=0.46 centre-sur-bord (comme un
    # 1er essai) empietait ~0.23in dans un chevron haut de ~0.36in, recouvrant
    # une partie du TITRE (defaut trouve au rendu reel, invisible en
    # `verifier_geometrie` qui ne verifie que les sorties de slide — jamais
    # les collisions entre 2 formes). `overlap` reste petit expres pour rester
    # sous la moitie de la marge naturelle qu'un texte centre (anchor MIDDLE)
    # laisse au-dessus de lui dans sa boite.
    # v4 : retour utilisateur — le chip de durée lisait "écrasé" face au reste
    # de la colonne. badge_d/chev inchangés (cf. note ci-dessus sur le risque
    # de chevauchement du titre), mais le chip lui-même grandit (7.8->9pt,
    # 0.20->0.25in) et les écarts entre sections s'aèrent — budget dégagé par
    # la suppression du chapô ci-dessus.
    badge_d = 0.40
    overlap = 0.05
    chev_w_frac = 0.94
    chev_pad = 0.045
    # v6 : retour utilisateur — polices réduites sur 3 familles de texte de
    # cette rangée (durée, titre de chevron, résultat/livrable), toutes
    # recalculées ici pour que les hauteurs de boîte suivent.
    chip_h = 0.20
    chip_sz = 7.5
    titre_sz = 7.5
    rl_sz = 7

    top0 = debut
    _, wcol = col_x(0, n, w=largeur_haut, x0=marge_g, gap=ecart)
    chev_tw = wcol * chev_w_frac - 2 * chev_pad
    titre_h = max(_lignes(p[1], chev_tw, titre_sz) for p in phases) * (titre_sz * 1.1 / 72.0) + 2 * chev_pad
    desc_h = max(_lignes(p[5], wcol - 0.06, 8) for p in phases) * (8 * 1.2 / 72.0) + 0.03
    tech_sz = 7
    tech_h = max(_lignes(p[7], wcol - 0.06, tech_sz) for p in phases) * (tech_sz * 1.15 / 72.0) + 0.02
    resultat_h = max(_lignes(p[8], wcol - 0.06, rl_sz) for p in phases) * (rl_sz * 1.2 / 72.0) + 0.03
    livr_h = max(_lignes(p[9], wcol - 0.06, rl_sz) for p in phases) * (rl_sz * 1.2 / 72.0) + 0.03

    badge_cy = top0 + badge_d / 2
    chev_top = top0 + badge_d - overlap
    chev_h = titre_h
    chip_y = chev_top + chev_h + 0.06
    desc_y = chip_y + chip_h + 0.08
    tech_y = desc_y + desc_h + 0.05
    sep_y = tech_y + tech_h + 0.06
    resultat_y = sep_y + 0.05
    livr_y = resultat_y + resultat_h + 0.04

    card_top = top0 - 0.02
    card_bottom = livr_y + livr_h + 0.03
    card_h = card_bottom - card_top

    # Passe 1 : conteneurs en CONTOUR (point 1) — plus d'aplat pastel.
    for i, color in enumerate(p[3] for p in phases):
        x, w = col_x(i, n, w=largeur_haut, x0=marge_g, gap=ecart)
        D.add_rect(s, x, card_top, w, card_h, fill=WHITE, line=color, line_w=1.1, rounded=True, radius=0.08)

    # v5 : retour utilisateur (édité dans le .pptx, réintégré ici) — les
    # petites flèches de connexion entre colonnes SUPPRIMÉES. Les chevrons
    # de titre (encoche gauche + pointe droite, Passe 2 ci-dessous) portent
    # déjà seuls l'idée de flux/enchaînement d'une colonne à l'autre.

    # Passe 2 : chevrons de titre + badges a cheval sur leur bord haut (point 4).
    for i, (sym, titre, duree, color, optionnel, desc, emph, tech, resultat, livrable) in enumerate(phases):
        x, w = col_x(i, n, w=largeur_haut, x0=marge_g, gap=ecart)
        cx = x + w / 2
        sur_cyan = (color == ACCENT)
        sur_clair = optionnel and color == ACCENT2
        texte_color = MUTED if sur_clair else color

        chev_x = cx - chev_w_frac * w / 2
        _chevron_shape(s, chev_x, chev_top, chev_w_frac * w, chev_h, fill=WHITE, line=color, line_w=1.1)
        D.add_text(s, chev_x + chev_pad, chev_top, chev_w_frac * w - 2 * chev_pad, chev_h, [
            (titre, dict(size=titre_sz, bold=True, color=texte_color if optionnel else NAVY,
                         align=PP_ALIGN.CENTER, line_spacing=1.05)),
        ], anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)

        _badge(s, cx, badge_cy, badge_d, color, sym,
               filled=not optionnel, dashed=optionnel, fill=(TRACK if optionnel else None),
               text_color=(NAVY if sur_cyan else None),
               bold=(sym not in ("⟲", "+")), size=12)

        chip(s, x + w / 2 - 0.48, chip_y, 0.96, chip_h, duree, color,
             text_color=(NAVY if (sur_cyan or sur_clair) else WHITE), size=chip_sz)

        av_e, em_e, ap_e = _split_emph(desc, emph)
        _rich(s, x + 0.03, desc_y, w - 0.06, desc_h, [
            ([(av_e, dict(size=8, color=MUTED)),
              (em_e, dict(size=8, bold=True, color=NAVY)),
              (ap_e, dict(size=8, color=MUTED))],
             dict(align=PP_ALIGN.CENTER, line_spacing=1.2)),
        ])
        # Activite technique en miroir (retour utilisateur : le lien organisa-
        # tionnel/tech doit se voir a CHAQUE etape, pas juste dans la
        # punchline finale) — meme famille MUTED que le "constat" au-dessus,
        # label "TECH" en tete pour rester un canal reconnaissable a travers
        # les 5 colonnes quelle que soit la couleur propre de chaque phase.
        tech_lbl, tech_reste = tech.split(" : ", 1)
        _rich(s, x + 0.03, tech_y, w - 0.06, tech_h, [
            ([(tech_lbl + " : ", dict(size=tech_sz, bold=True, color=MUTED)),
              (tech_reste, dict(size=tech_sz, italic=True, color=MUTED))],
             dict(align=PP_ALIGN.CENTER, line_spacing=1.15)),
        ])
        D.add_rect(s, x + 0.16, sep_y, w - 0.32, 0.012, fill=LINE)
        D.add_text(s, x + 0.02, resultat_y, w - 0.04, resultat_h, [
            (resultat, dict(size=rl_sz, bold=True, color=NAVY, align=PP_ALIGN.CENTER, line_spacing=1.2)),
        ], align=PP_ALIGN.CENTER)
        D.add_text(s, x + 0.02, livr_y, w - 0.04, livr_h, [
            (livrable, dict(size=rl_sz, bold=True, italic=True,
                             color=(NAVY if sur_cyan else texte_color),
                             align=PP_ALIGN.CENTER, line_spacing=1.2)),
        ], align=PP_ALIGN.CENTER)

    # --- Outillage agentic : conteneurs en contour + barre d'accent (point 6)
    # a la place des aplats TRACK/cyan pale.
    agents_top = livr_y + livr_h + 0.06
    col_gap = 0.18
    col_w = (largeur - col_gap) / 2
    # v5 : retour utilisateur (édité dans le .pptx, réintégré ici) — le 2e
    # pavé (déploiement client) ÉLARGI de 0.42in (texte allongé, "sous gate
    # IA" remplacé par une phrase qui nomme explicitement le lien orga+tech) ;
    # le 1er pavé garde sa largeur et sa position d'origine.
    largeur_extra_p2 = 0.42
    phases_agentic = [
        ("AGENTIQUE — POUR LA PRODUCTIVITÉ DU CONSULTANT", MUTED, col_w,
         "Un fait acquis : des agents outillent déjà chaque étape de la démarche, sans "
         "remplacer le consultant."),
        ("AGENTIQUE — UN DÉPLOIEMENT CHEZ LE CLIENT POUR ACCOMPAGNER LA TRANSFO", ACCENT,
         col_w + largeur_extra_p2,
         "Une piste à l'étude : accompagner la transformation du volet orga et tech en "
         "aidant le client à déployer ses propres agents."),
    ]
    bar_w2 = 0.045
    txt_x_off = 0.12 + bar_w2 + 0.08
    pad_v = 0.09
    label_h = max(_lignes(l, w_i - txt_x_off - 0.10, 7.5) for l, _, w_i, _ in phases_agentic) * (7.5 * 1.15 / 72.0)
    texte_h = max(_lignes(t, w_i - txt_x_off - 0.10, 7.5) for _, _, w_i, t in phases_agentic) * (7.5 * 1.25 / 72.0)
    agents_h = pad_v + label_h + 3 / 72.0 + texte_h + pad_v
    for i, (label, color, w_i, texte) in enumerate(phases_agentic):
        x = marge_g + i * (col_w + col_gap)
        aw = w_i - txt_x_off - 0.10
        D.add_rect(s, x, agents_top, w_i, agents_h, fill=WHITE, line=color, line_w=1.15, rounded=True, radius=0.07)
        D.add_rect(s, x + 0.12, agents_top + pad_v * 0.6, bar_w2, agents_h - pad_v * 1.2,
                   fill=color, rounded=True, radius=0.5)
        D.add_text(s, x + txt_x_off, agents_top + pad_v / 2, aw, agents_h - pad_v, [
            (label, dict(size=7.5, bold=True, color=color, line_spacing=1.1)),
            (texte, dict(size=7.5, color=NAVY, space_before=3, line_spacing=1.2)),
        ], anchor=MSO_ANCHOR.MIDDLE)

    # --- Cloture (point 7).
    punch_top = agents_top + agents_h + 0.035
    punch_txt = "Le volet organisationnel fait réussir le volet tech — pas l'inverse."
    punch_h = _lignes(punch_txt, largeur - 0.40, 12) * (12 * 1.2 / 72.0) + 0.1
    _quote_banner(s, marge_g, punch_top, largeur, punch_h, punch_txt, size=12)

    bas_reel = punch_top + punch_h
    if bas_reel > bas_max:
        raise SystemExit(
            f"slide_synthese_pourquoi_quoi_comment (v3) : contenu déborde de "
            f"{bas_reel - bas_max:.3f}in sous bas_max ({bas_max}in, bas réel "
            f"{bas_reel:.3f}in) — resserrer avant de régénérer."
        )
    return s


# ============================================================== SLIDE 3
def slide_infra_as_product_exemple(prs):
    s = content_slide(prs, "Contexte",
                       "Ce que change l'infra as a product, concrètement — un exemple avant/après.",
                       color=ACCENT)

    col_w = (CONTENT_W - 0.90) / 2
    # v7 : retour utilisateur (édité dans le .pptx, réintégré ici) — tout le
    # contenu remonté de 0.391in (marge sous le titre resserrée) pour plus
    # d'air ; card_h inchangée, l'espace libéré reste en bas (non redistribué
    # dans cette édition, à ajuster si besoin dans un prochain retour).
    card_top = CONTENT_TOP - 0.251
    # v5 : 2.9 -> 3.3 — retour utilisateur (5e puce AVANT ajoutée, puce 1
    # APRÈS étoffée) : calculé pour tenir les 5 lignes AVANT (la plus longue
    # colonne) à 9pt (2.34in de texte nécessaires sur 2.4in disponibles).
    card_h = 3.3
    pad = 0.24
    tag_h = 0.30

    # --- AVANT : conteneur en CONTOUR (avant : aplat TRACK plein, exactement
    # l'anti-motif nomme dans la consigne) + etiquette pleine compacte (point 2).
    avant_x = MARGIN
    D.add_rect(s, avant_x, card_top, col_w, card_h, fill=WHITE, line=MUTED, line_w=1.3, rounded=True, radius=0.09)
    tag1_w = 1.05
    D.add_rect(s, avant_x + pad - 0.06, card_top + 0.16, tag1_w, tag_h, fill=MUTED, rounded=True, radius=0.5)
    D.add_text(s, avant_x + pad - 0.06, card_top + 0.16, tag1_w, tag_h, [
        ("AVANT", dict(size=11, bold=True, color=WHITE, align=PP_ALIGN.CENTER)),
    ], anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)

    # v5 : retour utilisateur (édité dans le .pptx, réintégré ici) — puce 2
    # reformulée (qualitatif plutôt que le chiffre "25 min") ; 5e puce ajoutée
    # sur le pilotage par manque de priorisation.
    avant_items = [
        ("Guichet de tickets", " — personne n'est propriétaire du service."),
        ("Le triage du RUN trop long", ", traité au fil de l'eau."),
        ("Backlog invisible", ", aucun indicateur de pilotage."),
        ("Plein de projets lancés, peu d'indicateurs",
         ", du contrôle et du reporting à tous les niveaux."),
        ("Un pilotage dans la douleur",
         ", on prend tout et l'on ne sait plus comment bien prioriser les bons sujets à "
         "réaliser avec trop peu de capacité à faire."),
    ]
    avant_paragraphs = [
        ([("—  ", dict(size=9, color=MUTED)),
          (lead, dict(size=9, bold=True, color=NAVY)),
          (rest, dict(size=9, color=MUTED))],
         dict(line_spacing=1.2, space_before=(0 if i == 0 else 7)))
        for i, (lead, rest) in enumerate(avant_items)
    ]
    _rich(s, avant_x + pad, card_top + 0.66, col_w - 2 * pad, card_h - 0.9, avant_paragraphs,
          anchor=MSO_ANCHOR.MIDDLE)

    # --- Fleche de transformation : grosse fleche en CONTOUR epais (avant :
    # glyphe texte '→'), motif "grande fleche" d'OCTO_GROUND p.13.
    fleche_x = avant_x + col_w + 0.14
    fleche_w = 0.62
    arrow = s.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(fleche_x),
                                Inches(card_top + card_h * 0.30),
                                Inches(fleche_w), Inches(card_h * 0.40))
    try:
        arrow.shadow.inherit = False
    except Exception:
        pass
    arrow.fill.solid()
    arrow.fill.fore_color.rgb = _rgb(WHITE)
    arrow.line.color.rgb = _rgb(ACCENT)
    arrow.line.width = Pt(2.25)
    arrow.text_frame.paragraphs[0].text = ""

    # --- APRÈS : conteneur en contour PLEIN PERIMETRE (avant : liseré gauche
    # seul) + etiquette pleine cyan (texte navy dessus, comme le reste du
    # deck le fait deja pour rester lisible sur l'accent clair).
    apres_x = fleche_x + fleche_w + 0.14
    D.add_rect(s, apres_x, card_top, col_w, card_h, fill=WHITE, line=ACCENT, line_w=1.6, rounded=True, radius=0.09)
    tag2_w = 2.55
    D.add_rect(s, apres_x + pad - 0.06, card_top + 0.16, tag2_w, tag_h, fill=ACCENT, rounded=True, radius=0.5)
    D.add_text(s, apres_x + pad - 0.06, card_top + 0.16, tag2_w, tag_h, [
        ("APRÈS — démarche + agentique", dict(size=10, bold=True, color=NAVY, align=PP_ALIGN.CENTER)),
    ], anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)

    # v5 : retour utilisateur (édité dans le .pptx, réintégré ici) — puce 1
    # étoffée ("et un pilotage serein") ; puce 5 recentrée sur "tech" seul
    # (même simplification que le sous-titre/la punchline de slide 3).
    apres_items = [
        ("Un propriétaire produit et un pilotage serein",
         ", une roadmap, des indicateurs de pilotage."),
        ("Temps de triage du RUN fortement réduit", " — capacité RUN récupérée."),
        ("Backlog visible", ", priorisé, mesuré dans le temps."),
        ("Process explicite, rôles définis", " — piste retenue : agentique-implementation."),
        ("Des évolutions tech", " qui sont possibles et atteignables."),
    ]
    apres_paragraphs = [
        ([("✓  ", dict(size=9, color=ACCENT, bold=True)),
          (lead, dict(size=9, bold=True, color=NAVY)),
          (rest, dict(size=9, color=NAVY))],
         dict(line_spacing=1.2, space_before=(0 if i == 0 else 6)))
        for i, (lead, rest) in enumerate(apres_items)
    ]
    _rich(s, apres_x + pad, card_top + 0.66, col_w - 2 * pad, card_h - 0.9, apres_paragraphs,
          anchor=MSO_ANCHOR.MIDDLE)

    # --- Cloture (point 7).
    concl_top = card_top + card_h + 0.16
    concl_h = CONTENT_BOTTOM - concl_top
    # v5 : "un résultat visé" -> "des résultats concrets" (retour utilisateur,
    # édité dans le .pptx puis réintégré ici — moins hypothétique).
    concl_txt = ("Infra as a product, concrètement : le retour à une maîtrise de faire les "
                 "bonnes choses au bon moment, un backlog piloté, des résultats concrets — "
                 "dans notre approche l'agentique accélère la démarche, il ne la remplace pas.")
    if concl_h < 0.30:
        raise SystemExit(
            f"slide_infra_as_product_exemple (v3) : plus assez de place pour le bandeau de "
            f"cloture ({concl_h:.3f}in) — resserrer la slide avant de régénérer."
        )
    _quote_banner(s, MARGIN, concl_top, CONTENT_W, concl_h, concl_txt, size=12)
    return s


# --------------------------------------------------------- police + sortie
FONT = "Outfit"
FONT_SECOURS = "Arial"
GLYPHES_HORS_OUTFIT = {"①", "②", "③", "⟲"}


def _appliquer_police(prs, font_name=FONT, secours=FONT_SECOURS):
    """Post-traitement identique a gen_check_slide_synthese_v2_propositions.py
    (memes 4 glyphes sans repli PowerPoint correct, cf. ce fichier pour le
    detail du diagnostic)."""
    n_runs = 0
    n_secours = 0
    for slide in prs.slides:
        for shape in slide.shapes:
            if not shape.has_text_frame:
                continue
            for p in shape.text_frame.paragraphs:
                for r in p.runs:
                    if r.text.strip() in GLYPHES_HORS_OUTFIT:
                        r.font.name = secours
                        n_secours += 1
                    else:
                        r.font.name = font_name
                        n_runs += 1
    print(f"({n_secours} run(s) laissé(s) en {secours} — glyphe hors couverture Outfit)")
    return n_runs


prs = G.new_prs()
G.slide_cover(prs)
slide_specificites_infra(prs)
slide_synthese_pourquoi_quoi_comment(prs)
slide_infra_as_product_exemple(prs)

n = _appliquer_police(prs)
print(f"Police {FONT} appliquée sur {n} runs de texte.")

problemes = G.D.verifier_geometrie(prs)
if problemes:
    print(f"GEOMETRIE: {len(problemes)} probleme(s)")
    for p in problemes:
        print(" -", p)
else:
    print("GEOMETRIE: OK — aucune forme hors cadre")

out = os.path.join(G.HERE, "check_slide_synthese-v3-refonte.pptx")
prs.save(out)
print("Ecrit:", out)
