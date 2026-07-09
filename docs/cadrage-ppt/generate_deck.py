"""Génère une synthèse PPT (11 slides) des RÉSULTATS du cadrage BMAD IAP
(docs/bmad-iap-cadrage.md) à partir des helpers pptx_deck, dessinée
PAR-DESSUS le vrai template de marque OCTO (template-octo.pptx) —
masters/layouts/thème conservés, pas un deck sur canevas vierge.

Volontairement limité aux résultats du cadrage (mission, doctrine,
méthode, maturité, ambition, KPIs) — pas au travail de mise en œuvre de
ce cadrage (architecture des 11 agents BMAD, schéma de fonctionnement,
roadmap MVP, points ouverts), qui relève d'un support interne, pas
d'une synthèse exécutive.

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

HERE = os.path.dirname(__file__)
TEMPLATE = os.path.join(HERE, "template-octo.pptx")

LAYOUT_COUVERTURE = 8   # "40 - Couverture [1]" — idx0 titre, idx1 sous-titre, idx2/idx3 crédit+date
LAYOUT_TITRE_SEUL = 5   # "04 - Titre seul" — idx0 titre, garde logo/pied de page/n° de slide

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


def content_slide(prs, kicker, title):
    layout = prs.slide_masters[0].slide_layouts[LAYOUT_TITRE_SEUL]
    s = prs.slides.add_slide(layout)
    ph = s.shapes.placeholders[0]
    box_w = Emu(ph.width).inches
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
    r1.font.color.rgb = _rgb(ACCENT)
    r2 = p.add_run()
    r2.text = title
    r2.font.bold = True
    r2.font.size = Pt(taille)
    r2.font.color.rgb = _rgb(NAVY)
    return s


def col_x(i, n, w=CONTENT_W, x0=MARGIN, gap=GAP):
    col_w = (w - (n - 1) * gap) / n
    return x0 + i * (col_w + gap), col_w


def chip(slide, x, y, w, h, label, color, text_color="#ffffff", size=D.TYPE["tiny"]):
    D.add_rect(slide, x, y, w, h, fill=color, rounded=True, radius=0.5)
    D.add_text(slide, x, y, w, h, [(label, dict(size=size, bold=True, color=text_color,
                align=PP_ALIGN.CENTER))], anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)


# ---------------------------------------------------------------- slide 1
def slide_cover(prs):
    layout = prs.slide_masters[0].slide_layouts[LAYOUT_COUVERTURE]
    s = prs.slides.add_slide(layout)
    phs = {ph.placeholder_format.idx: ph for ph in s.placeholders}
    phs[0].text_frame.text = "BMAD IAP"
    phs[1].text_frame.text = "Infra as a Product Transformation Pack — synthèse de cadrage"
    phs[2].text_frame.text = "OCTO Technology"
    phs[3].text_frame.text = "v1.9 · 2026-07-09"

    # Bandeau de métadonnées sous la zone de couverture du template, dans la
    # bande basse encore libre (le pied de page/logo du master restent visibles).
    metas = [
        ("STATUT", "Draft consolidé v1.9"),
        ("LANGUE", "FR"),
        ("CONFIDENTIALITÉ", "Client-data-first"),
        ("SOURCES", "VSCode1 · VSCode2"),
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
         "plateforme VSCode1 V3.2 — chacune sa lecture, son usage."),
        ("Posture", D.PALETTE[2],
         "Niveau d'ambition A (aide au coach) assumé aujourd'hui — un choix de gouvernance, "
         "pas une limite technique subie, mesuré par 3 familles de KPIs distinctes."),
    ]
    n = len(items)
    top0 = CONTENT_TOP + headline_h + 0.3
    card_h = CONTENT_BOTTOM - top0
    for i, (titre, color, desc) in enumerate(items):
        x, w = col_x(i, n)
        D.add_card(s, x, top0, w, card_h, color)
        pad = 0.18
        D.add_text(s, x + pad, top0 + 0.18, w - 2 * pad, 0.4, [
            (titre, dict(size=D.TYPE["h3"], bold=True, color=color)),
        ])
        D.add_text(s, x + pad, top0 + 0.65, w - 2 * pad, card_h - 0.85, [
            (desc, dict(size=8, color=NAVY, line_spacing=1.28)),
        ])
    return s


# ---------------------------------------------------------------- slide 3
def slide_mission(prs):
    s = content_slide(prs, "Cadrage", "Une double mission : transformer ET assainir")
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
    s = content_slide(prs, "Cadrage", "Les données du client gouvernent le choix du modèle IA")
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
    s = content_slide(prs, "Cadrage", "Deux échelles de maturité, jamais confondues")
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
        ("MATURITÉ PRODUIT / PLATEFORME (grille VSCode1 V3.2)", dict(size=D.TYPE["tiny"], bold=True, color=NAVY))
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


# ---------------------------------------------------------------- slide 6
def slide_gaspillages(prs):
    s = content_slide(prs, "Méthode", "Le gaspillage, traité comme un objet de transformation")
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
    score_h = 0.72
    D.add_rect(s, MARGIN, score_top, CONTENT_W, score_h, fill=NAVY, rounded=True, radius=0.08)
    D.add_text(s, MARGIN + 0.22, score_top, CONTENT_W - 0.44, score_h, [
        ("Priorité = (impact × faisabilité) − prudence IA", dict(size=D.TYPE["small"], bold=True, color="#ffffff")),
        ("Le score ne remplace pas l'arbitrage humain : il rend la discussion explicite.",
         dict(size=8, color="#c7cbe0", space_before=2)),
    ], anchor=MSO_ANCHOR.MIDDLE)
    return s


# ---------------------------------------------------------------- slide 9
def slide_team_topologies(prs):
    s = content_slide(prs, "Méthode", "La cible IAP est une Platform Team — agents IA compris")
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
    note_h = CONTENT_BOTTOM - note_top
    D.add_rect(s, MARGIN, note_top, CONTENT_W, note_h, fill=TRACK, rounded=True, radius=0.08)
    D.add_text(s, MARGIN + 0.22, note_top + 0.1, CONTENT_W - 0.44, note_h - 0.2, [
        ("Extension — les agents IA comme coéquipiers, et leur mise en œuvre (v1.7)",
         dict(size=D.TYPE["tiny"], bold=True, color=NAVY)),
        ("Un agent peut être membre d'une Stream-aligned team ou capacité exposée par la "
         "Platform Team (4ᵉ mode candidat : Supervision). L'adoption suit la trajectoire "
         "Coach → Délégué (assisté → supervisé → délégué) : mandat écrit (ce que l'agent "
         "décide seul / ce qui escalade / qui répond de ses erreurs) avant tout palier "
         "au-delà de l'assisté — jamais un usage qui dérive à l'implicite.",
         dict(size=8, color=NAVY, space_before=3, line_spacing=1.25)),
    ])
    return s


# ---------------------------------------------------------------- slide 8
# Formes inspirées des slides d'exemple du template lui-même (« Notre
# approche ») : badges circulaires connectés par une ligne, chip de durée,
# description centrée sous chaque étape.
def slide_trajectoire(prs):
    s = content_slide(prs, "Trajectoire", "Mise en œuvre du target operating model — brainstorm")
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
            (sym, dict(size=16, bold=True, color="#ffffff", align=PP_ALIGN.CENTER))
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
    note_h = CONTENT_BOTTOM - note_top
    D.add_rect(s, MARGIN, note_top, CONTENT_W, note_h, fill=TRACK, rounded=True, radius=0.08)
    D.add_text(s, MARGIN + 0.2, note_top + 0.08, CONTENT_W - 0.4, note_h - 0.16, [
        ("Bifurcation avec/sans agents IA déployés", dict(size=8, bold=True, color=NAVY)),
        ("Le tronc commun ①→②→③→⟲ ne change pas de structure — la piste agent IA (si retenue) "
         "se greffe sur ②/③ via la démarche en 5 phases déjà cadrée (§Modèles d'équipe), plutôt "
         "que d'être un chemin séparé à maintenir. Owner proposé (non tranché) : "
         "iap-operating-model-architect + iap-change-coach sur le volet humain.",
         dict(size=7, color=NAVY, space_before=3, line_spacing=1.25)),
    ])
    return s


# ---------------------------------------------------------------- slide 9
# Formes inspirées de la slide d'exemple « Une approche contextualisée » du
# template : colonne par étape avec badge + bandeau titre + ligne de
# séparation + bloc LIVRABLES, plutôt qu'un tableau plat.
def slide_livrables_ppt(prs):
    s = content_slide(prs, "Trajectoire", "Livrables PPT par étape — brainstorm")
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
    top0 = CONTENT_TOP + 0.5
    card_h = CONTENT_BOTTOM - top0
    badge_d = 0.34
    for i, (sym, titre, color, audience, deck, contenu) in enumerate(cols):
        x, w = col_x(i, n)
        D.add_card(s, x, top0, w, card_h, color)
        pad = 0.16
        D.add_rect(s, x + pad, top0 + 0.14, badge_d, badge_d, fill=color, rounded=True, radius=0.5)
        D.add_text(s, x + pad, top0 + 0.14, badge_d, badge_d, [
            (sym, dict(size=11, bold=True, color="#ffffff", align=PP_ALIGN.CENTER)),
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


# ---------------------------------------------------------------- slide 10
def slide_ambition(prs):
    s = content_slide(prs, "Trajectoire", "Trois niveaux d'ambition, pas un spectre linéaire")
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
    card_h = 1.85
    top0 = CONTENT_TOP + 0.45
    for i, (code, titre, color, role, roadmap) in enumerate(niveaux):
        x, w = col_x(i, n)
        D.add_card(s, x, top0, w, card_h, color)
        pad = 0.2
        D.add_text(s, x + pad, top0 + 0.15, w - 2 * pad, 0.35, [
            (f"{code} · {titre}", dict(size=D.TYPE["small"], bold=True, color=color)),
        ])
        D.add_text(s, x + pad, top0 + 0.55, w - 2 * pad, 0.9, [
            (role, dict(size=8, color=NAVY, line_spacing=1.25)),
        ])
        D.add_text(s, x + pad, top0 + 1.5, w - 2 * pad, 0.3, [
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


# ---------------------------------------------------------------- slide 11
def slide_kpis(prs):
    s = content_slide(prs, "Trajectoire", "Trois familles de KPIs, à ne jamais confondre")
    familles = [
        ("KPIs de mission", D.PALETTE[0], "Côté client",
         ["Gaspillage traité (capacité RUN récupérée)", "Adoption produit (self-service)",
          "Fiabilité & coût (MTTR, coût/capacité)", "Gouvernance IA (supervision, incidents)",
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
    card_h = CONTENT_H
    top0 = CONTENT_TOP
    for i, (titre, color, sous, items) in enumerate(familles):
        x, w = col_x(i, n)
        D.add_card(s, x, top0, w, card_h, color)
        pad = 0.18
        D.add_text(s, x + pad, top0 + 0.16, w - 2 * pad, 0.55, [
            (titre, dict(size=D.TYPE["tiny"], bold=True, color=color, line_spacing=1.05)),
            (sous, dict(size=8, color=MUTED, italic=True, space_before=2)),
        ])
        lignes = [(f"·  {it}", dict(size=8, color=NAVY, space_after=4, line_spacing=1.15))
                  for it in items]
        D.add_text(s, x + pad, top0 + 0.8, w - 2 * pad, card_h - 0.95, lignes)
    return s



def build():
    prs = new_prs()
    slide_cover(prs)
    slide_executive_summary(prs)
    slide_mission(prs)
    slide_gate_ia(prs)
    slide_maturite(prs)
    slide_gaspillages(prs)
    slide_team_topologies(prs)
    slide_trajectoire(prs)
    slide_livrables_ppt(prs)
    slide_ambition(prs)
    slide_kpis(prs)

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
