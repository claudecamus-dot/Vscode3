"""pptx_deck — petite bibliotheque d'aide pour construire des slides python-pptx
"de qualite" : echelle typographique coherente, formes (barres, jauge, cartes),
couleurs, et surtout quatre filets de controle automatique :

  - `verifier_geometrie` — toute forme qui sort de la slide (le defaut classique
    des decks generes a la main) ;
  - `verifier_debordements_texte` — le texte qui deborde de SA PROPRE boite,
    que le controle des bords ne peut pas voir ;
  - `verifier_chrome_gabarit` — la forme de contenu qui recouvre le badge de
    pagination herite du gabarit (il vient du master : ce n'est pas une forme
    de la slide, donc `verifier_geometrie` l'ignore) ;
  - `verifier_plancher_de_dessin` — le bas de bande que le generateur s'impose,
    confronte au gabarit reellement charge.

Les trois derniers sont portes des homologues de la flotte (VSCode4
scripts/pptx_deck.py, VSCode2 app/services/pptx_deck.py) le 2026-09-09, sur
finding robustesse de l'audit VScode5 du meme jour, et adaptes aux constantes de
ce gabarit (voir `_ZONE_NUMERO_PAGE_IN` et `verifier_plancher_de_dessin`).

Reutilisable hors de ce projet : aucune dependance au domaine metier ici.
Les coordonnees des helpers sont exprimees en POUCES (float) pour la lisibilite.
"""
from pptx.dml.color import RGBColor
from pptx.enum.dml import MSO_LINE_DASH_STYLE
from pptx.enum.shapes import MSO_SHAPE, MSO_SHAPE_TYPE
from pptx.enum.text import MSO_ANCHOR, MSO_AUTO_SIZE, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Emu, Inches, Pt

# --- Echelle typographique (pt) — une seule source de verite ---
TYPE = {
    "title": 26, "h2": 18, "h3": 14, "body": 12, "small": 10.5, "tiny": 9,
    "kpi": 44, "kpi_unit": 16,
}

# Palette des piliers : IDENTIQUE au radar web (radar-svg.js) pour que les
# barres et le radar parlent le meme langage couleur.
PALETTE = ["#2c5cc5", "#1e6b34", "#b3261e", "#b8860b", "#6a3d9a", "#138086"]

INK = "#1c2330"
MUTED = "#6b7280"
LINE = "#e6e8ee"
TRACK = "#eef1f7"
OK = "#1e6b34"
WARN = "#b3261e"
GOLD = "#b8860b"


def rgb(hexa):
    return RGBColor.from_string(hexa.lstrip("#"))


def couleur_pilier(i):
    return PALETTE[i % len(PALETTE)]


def _no_shadow(shape):
    # Les autoshapes heritent parfois d'une ombre du theme : on la coupe.
    try:
        shape.shadow.inherit = False
    except Exception:
        pass


def add_text(slide, l, t, w, h, lignes, anchor=MSO_ANCHOR.TOP, align=PP_ALIGN.LEFT,
             wrap=True):
    """Ajoute une zone de texte. `lignes` = liste de (texte, opts) ; chaque
    element devient un paragraphe. opts: size,bold,italic,color,align,
    space_before,space_after,line_spacing."""
    box = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = wrap
    tf.auto_size = MSO_AUTO_SIZE.NONE
    tf.vertical_anchor = anchor
    for m in ("margin_left", "margin_right", "margin_top", "margin_bottom"):
        setattr(tf, m, 0)
    for i, (texte, opts) in enumerate(lignes):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = opts.get("align", align)
        if "space_before" in opts:
            p.space_before = Pt(opts["space_before"])
        if "space_after" in opts:
            p.space_after = Pt(opts["space_after"])
        if "line_spacing" in opts:
            p.line_spacing = opts["line_spacing"]
        run = p.add_run()
        run.text = texte
        f = run.font
        f.size = Pt(opts.get("size", TYPE["body"]))
        f.bold = opts.get("bold", False)
        f.italic = opts.get("italic", False)
        f.color.rgb = rgb(opts.get("color", INK))
    return box


def add_rect(slide, l, t, w, h, fill=None, line=None, line_w=1.0, rounded=False,
             radius=0.12):
    shp = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE,
        Inches(l), Inches(t), Inches(w), Inches(h))
    _no_shadow(shp)
    if rounded:
        try:
            shp.adjustments[0] = radius
        except Exception:
            pass
    if fill is None:
        shp.fill.background()
    else:
        shp.fill.solid()
        shp.fill.fore_color.rgb = rgb(fill)
    if line is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = rgb(line)
        shp.line.width = Pt(line_w)
    shp.text_frame.paragraphs[0].text = ""
    return shp


def add_hbar(slide, l, t, w, h, frac, fill, track=TRACK):
    """Barre de progression horizontale (piste + remplissage), coins arrondis."""
    frac = max(0.0, min(1.0, float(frac)))
    add_rect(slide, l, t, w, h, fill=track, rounded=True, radius=0.5)
    if frac > 0:
        wv = max(h, w * frac)  # largeur minimale visible = hauteur (pastille)
        add_rect(slide, l, t, wv, h, fill=fill, rounded=True, radius=0.5)


def add_gauge(slide, l, t, size, frac, fill, track=TRACK, hole=62):
    """Jauge circulaire (anneau) via un graphique doughnut a 2 segments.
    Renvoie le GraphicFrame. Le libelle central est a poser separement."""
    from pptx.chart.data import CategoryChartData
    from pptx.enum.chart import XL_CHART_TYPE
    frac = max(0.0, min(1.0, float(frac)))
    data = CategoryChartData()
    data.categories = ["v", "r"]
    data.add_series("g", (frac, 1 - frac))
    gf = slide.shapes.add_chart(XL_CHART_TYPE.DOUGHNUT, Inches(l), Inches(t),
                                Inches(size), Inches(size), data)
    chart = gf.chart
    chart.has_legend = False
    chart.has_title = False
    plot = chart.plots[0]
    plot.has_data_labels = False
    # Taille du trou
    dough = plot._element  # <c:doughnutChart>
    hs = dough.find(qn("c:holeSize"))
    if hs is None:
        hs = dough.makeelement(qn("c:holeSize"), {"val": str(hole)})
        dough.append(hs)
    else:
        hs.set("val", str(hole))
    # Couleurs des 2 segments
    pts = plot.series[0].points
    for pt_, col in ((pts[0], fill), (pts[1], track)):
        pt_.format.fill.solid()
        pt_.format.fill.fore_color.rgb = rgb(col)
        pt_.format.line.color.rgb = rgb("#ffffff")
        pt_.format.line.width = Pt(1)
    return gf


def add_card(slide, l, t, w, h, accent):
    """Carte blanche a coins arrondis + liseré couleur a gauche (style infographie)."""
    add_rect(slide, l, t, w, h, fill="#ffffff", line=LINE, line_w=0.75,
             rounded=True, radius=0.06)
    add_rect(slide, l, t, 0.07, h, fill=accent, rounded=True, radius=0.5)


def add_dot(slide, x, y, d, color):
    """Petite pastille ronde pleine (puce de legende / marqueur de chip)."""
    return add_rect(slide, x, y, d, d, fill=color, rounded=True, radius=0.5)


def add_range_bar(slide, l, t, w, h, mn, mx, scale_max, fill, marker=None,
                  track=TRACK):
    """Barre d'amplitude min..max sur une echelle 0..scale_max (piste complete +
    segment colore couvrant la plage). `marker` (ex. moyenne) pose un repere
    vertical. Sert a montrer une dispersion sur l'echelle reelle, pas en relatif."""
    add_rect(slide, l, t, w, h, fill=track, rounded=True, radius=0.5)
    fa = max(0.0, min(1.0, mn / scale_max))
    fb = max(0.0, min(1.0, mx / scale_max))
    seg_w = max(h, w * (fb - fa))  # largeur minimale = hauteur (pastille)
    add_rect(slide, l + w * fa, t, seg_w, h, fill=fill, rounded=True, radius=0.5)
    if marker is not None:
        fm = max(0.0, min(1.0, marker / scale_max))
        mx_x = l + w * fm - 0.015
        add_rect(slide, mx_x, t - 0.05, 0.03, h + 0.10, fill=INK, rounded=True,
                 radius=0.5)


def add_chip(slide, x, y, w, h, label, color, text_color="#ffffff", size=TYPE["tiny"]):
    """Pastille rectangulaire pleine avec libelle centre (etiquette de code,
    de duree, de famille...). Portee ici depuis generate_deck.py le 2026-09-11
    (finding audit VScode5 : reste utilisee telle quelle par 8+ types de slide,
    donc genuinement reutilisable, contrairement aux helpers de schema
    a usage unique qui restent locaux au generateur)."""
    add_rect(slide, x, y, w, h, fill=color, rounded=True, radius=0.5)
    add_text(slide, x, y, w, h, [(label, dict(size=size, bold=True, color=text_color,
              align=PP_ALIGN.CENTER))], anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)


def add_badge(slide, cx, cy, d, color, symbol, filled=True, dashed=False, fill=None,
              text_color=None, size=12, bold=True):
    """Pastille ronde centree en (cx, cy) — `filled` pour une etape « en dur »
    (fond plein), sinon contour seul (etape optionnelle, `dashed=True`). Portee
    ici depuis generate_deck.py le 2026-09-11 (meme finding que `add_chip`).

    Repli de couleur de texte volontairement en litteral ('#ffffff'), pas via
    une constante de theme : ce module reste sans dependance au domaine metier
    (docstring du fichier) — c'est a l'appelant de passer `text_color` si son
    theme n'est pas blanc sur fond plein."""
    x, y = cx - d / 2, cy - d / 2
    if filled:
        add_rect(slide, x, y, d, d, fill=color, rounded=True, radius=0.5)
        tc = text_color or "#ffffff"
    else:
        shp = add_rect(slide, x, y, d, d, fill=(fill or "#ffffff"), line=color,
                        line_w=1.2, rounded=True, radius=0.5)
        if dashed:
            shp.line.dash_style = MSO_LINE_DASH_STYLE.DASH
        tc = text_color or color
    add_text(slide, x, y, d, d, [
        (symbol, dict(size=size, bold=bold, color=tc, align=PP_ALIGN.CENTER)),
    ], anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)


def add_encart(slide, l, t, w, h, texte, accent=None, label=None, size=None,
               align=PP_ALIGN.CENTER):
    """Encart « a retenir / so-what » — boite fond TRACK (gris clair), coins
    arrondis, sans ombre, texte INK. Un encart est QUIET (gris neutre), pas une
    bande de couleur criarde : `accent`, si fourni, pose un fin lisere gauche
    colore (repere sans crier) ; `label` un prefixe en gras au-dessus de
    `texte`. Le tout est centre verticalement dans la boite.

    Porte ici depuis les homologues de la flotte (VSCode2 app/services/
    pptx_deck.py, VSCode4 scripts/pptx_deck.py) le 2026-09-12, sur le meme
    finding reutilisabilite de l'audit VScode5 qui avait deja fait porter
    `add_chip`/`add_badge`/`appliquer_police` le 2026-09-11 : ces trois-la
    existaient donc deja dans ce fichier au moment du constat, seul
    `add_encart` manquait reellement. Motif deja present a la main dans
    `generate_deck.py` (ex. le bloc « TRANCHE ENSEMBLE » : rectangle TRACK +
    lisere colore + libelle + texte, pptx_deck.py n'etant pas cense connaitre
    ce nom de variable) — cette fonction generalise ce couple rect+texte pour
    eviter la resaisie a chaque nouvel encart, sans forcer les 3 sites
    existants a migrer.

    Fond en TRACK, la piste neutre DEJA definie dans ce module (pas une
    nouvelle constante ENCART_BG comme chez les homologues) : ce fichier n'a
    qu'un seul gris de fond, les deux homologues en avaient une variante
    quasi identique (#eceef2 contre #eef1f7 ici) qui aurait fait deux
    constantes pour la meme intention."""
    size = TYPE["h3"] if size is None else size
    add_rect(slide, l, t, w, h, fill=TRACK, rounded=True, radius=0.12)
    pad = 0.24
    if accent:
        add_rect(slide, l, t, 0.06, h, fill=accent, rounded=True, radius=0.5)
        pad = 0.28
    lignes = []
    if label:
        lignes.append((label, dict(size=size, bold=True, color=INK, align=align)))
    lignes.append((texte, dict(size=size, bold=(label is None), color=INK, align=align)))
    add_text(slide, l + pad, t, w - 2 * pad, h, lignes, anchor=MSO_ANCHOR.MIDDLE,
             align=align)


def appliquer_police(prs, police, secours, glyphes_hors_police=frozenset()):
    """Applique `police` a tous les runs de texte du document, sauf les glyphes
    de `glyphes_hors_police` qui restent en `secours` (couverture Unicode absente
    de la police de marque). Portee ici depuis generate_deck.py le 2026-09-11 —
    seule la logique est generique ; le CHOIX de police reste au projet appelant
    (aucun defaut ici : imposer une police de marque par defaut couplerait ce
    module reutilisable a l'identite visuelle d'un seul projet)."""
    n_police, n_secours = 0, 0
    for slide in prs.slides:
        for shape in slide.shapes:
            if not shape.has_text_frame:
                continue
            for p in shape.text_frame.paragraphs:
                for r in p.runs:
                    if r.text.strip() in glyphes_hors_police:
                        r.font.name = secours
                        n_secours += 1
                    else:
                        r.font.name = police
                        n_police += 1
    print(f"Police {police} appliquee sur {n_police} runs "
          f"({n_secours} run(s) laisse(s) en {secours} — glyphe hors couverture).")
    return n_police, n_secours


def _compte_lignes(texte, cpl):
    """Nombre de lignes apres un repli mot-a-mot pour une largeur de `cpl`
    caracteres. Estimateur volontairement simple (pas de mesure de police reelle) :
    calibre empiriquement via `cpl`, pas cense etre pixel-parfait."""
    total = 0
    for para in str(texte).split("\n"):
        cur = 0
        n = 1
        for mot in para.split():
            ajout = (1 if cur else 0) + len(mot)
            if cur + ajout > cpl and cur:
                n += 1
                cur = len(mot)
            else:
                cur += ajout
        total += n
    return total


def estimer_lignes(texte, largeur_in, taille_pt, cpi_ref=11.0, taille_ref=10.5):
    """Estime le nombre de lignes qu'occupera `texte` une fois reparti mot-a-mot
    sur `largeur_in` pouces a la taille de police `taille_pt`. Les caracteres par
    pouce sont derives de `cpi_ref` (calibre a `taille_ref` pt) par une regle de
    trois : une police 2x plus petite loge environ 2x plus de caracteres/pouce."""
    if not texte:
        return 1
    cpi = cpi_ref * (taille_ref / taille_pt)
    cpl = max(6, int(largeur_in * cpi))
    return _compte_lignes(texte, cpl)


def ajuster_police(textes, largeur_in, taille_max, taille_min, budget_ok, pas=0.5,
                   cpi_ref=11.0, taille_ref=10.5):
    """Adapte la taille de police a la longueur des phrases a restituer : cherche,
    par pas de `pas` pt entre `taille_max` et `taille_min`, la plus GRANDE taille
    telle que `budget_ok(taille, lignes_max)` soit vrai — ou `lignes_max` est le
    nombre de lignes necessaires au plus long de `textes` une fois reparti sur
    `largeur_in` pouces a cette taille (voir `estimer_lignes`).

    `budget_ok` encapsule la contrainte geometrique propre a l'appelant (ex. :
    n cartes empilees doivent tenir dans la bande disponible) — cette fonction
    reste agnostique du domaine. Objectif : ne JAMAIS tronquer/faire deborder une
    phrase — si aucune taille ne satisfait `budget_ok`, on degrade sur
    `taille_min` (texte tres dense) plutot que de laisser un texte coupe.

    Renvoie (taille, lignes_max)."""
    taille = taille_max
    while True:
        lignes_max = max((estimer_lignes(t, largeur_in, taille, cpi_ref, taille_ref)
                          for t in textes), default=1)
        if budget_ok(taille, lignes_max) or taille <= taille_min:
            return (max(taille, taille_min), lignes_max)
        taille = max(taille_min, round(taille - pas, 2))


def tronquer_a_lignes(texte, largeur_in, taille_pt, max_lignes, cpi_ref=11.0,
                      taille_ref=10.5):
    """Tronque `texte` (avec une ellipse finale) pour qu'il tienne dans
    `max_lignes` lignes une fois reparti sur `largeur_in` pouces a `taille_pt`.
    Dernier recours quand meme `ajuster_police` a sa taille plancher ne suffit
    plus a eviter un debordement geometrique — mieux vaut un texte coupe
    proprement qu'une forme qui deborde de la slide. Ne fait rien si le texte
    tient deja dans `max_lignes`."""
    if estimer_lignes(texte, largeur_in, taille_pt, cpi_ref, taille_ref) <= max_lignes:
        return texte
    cpi = cpi_ref * (taille_ref / taille_pt)
    cpl = max(6, int(largeur_in * cpi))
    limite = max(1, cpl * max_lignes - 1)
    tronque = str(texte)[:limite].rstrip()
    dernier_espace = tronque.rfind(" ")
    if dernier_espace > limite * 0.6:
        tronque = tronque[:dernier_espace]
    return tronque.rstrip(" ,;:.") + "…"


def _noter(compte, cle):
    """Incremente `compte[cle]` quand un compteur est fourni. Le dict est cree
    par l'APPELANT : un filet appele sans compteur garde exactement son
    comportement d'avant."""
    if compte is not None:
        compte[cle] = compte.get(cle, 0) + 1


def verifier_debordements_texte(prs, cpi_pessimiste=10.7, tolerance_in=0.15,
                                compte=None):
    """Filet « le texte tient dans sa boite » — complementaire de
    `verifier_geometrie`, qui ne voit que les BORDS des formes et jamais le
    rendu du texte a l'interieur. Pour chaque zone de texte dessinee (repli de
    mots actif, auto-size desactive, ancrage haut), estime la hauteur du
    contenu avec une calibration PESSIMISTE (`cpi_pessimiste` < la calibration
    nominale de `estimer_lignes`) et signale les boites dont le contenu estime
    depasse la hauteur declaree + `tolerance_in`. Renvoie une liste de constats
    (vide = OK) ; l'appelant decide (defaut dur, ou simple log).

    Porte depuis les homologues de la flotte (VSCode4 scripts/pptx_deck.py,
    VSCode2 app/services/pptx_deck.py) le 2026-09-09, sur finding robustesse de
    l'audit VScode5 : c'est exactement le defaut qui a mordu ce deck deux fois
    (4e puce masquee par le chip de pied, slide 4 ; texte estime plus haut que
    sa carte) et que le controle geometrique seul ne peut pas voir.

    CE QUE CE FILET NE REGARDE PAS, ET POURQUOI. Sont ecartees : les boites
    AUTO-AGRANDISSANTES (`SHAPE_TO_FIT_TEXT` — PowerPoint recalcule leur
    hauteur, la valeur declaree n'est qu'une amorce), les boites en
    `TEXT_TO_FIT_SHAPE` (PowerPoint y REDUIT la police, une estimation a taille
    nominale n'y dit rien), les placeholders (le gabarit les gere), les formes
    tournees (geometrie non comparable) et les ancrages MIDDLE/BOTTOM (contenu
    deja borne par l'appelant). Sur VSCode4, inclure les auto-agrandissantes a
    ete essaye puis retire sur mesure : 17 constats sur un deck qui se rend
    correctement — un filet qui crie sur des zones correctes finit debranche.

    La plus grosse exclusion n'est aucune de celles-la : c'est `word_wrap`
    (503 des 904 zones ecartees du deck reel, mesure du 2026-09-09). Attention,
    `not tf.word_wrap` traite `None` — repli HERITE, que PowerPoint replie bel
    et bien — comme un repli desactive : une zone de texte qui laisse le repli
    herite echappe au filet. Sans consequence sur ce deck (ces 503 zones sont
    toutes a texte vide, et `add_text` pose `word_wrap` explicitement), mais
    tout texte pose hors de `add_text` tombe dans ce trou en silence.
    Les formes GROUPEES sont hors filet elles aussi : on n'y descend pas.

    `compte` : dict optionnel rempli avec le nombre de zones `examinees` et
    `ignorees`. Un filet qui ne dit pas combien de zones il a REGARDEES laisse
    croire que son vert couvre tout le deck.

    A LIRE AVANT DE LE BRANCHER EN DEFAUT DUR. Mesure du 2026-09-09 sur
    bmad-iap-cadrage-synthese.pptx (49 slides, lecture seule) : 302 zones
    examinees, 904 hors filet, et 58 constats a la tolerance par defaut — dont
    l'ecart median n'est que de 0.22in (max 0.52in). A 0.40in de tolerance il
    en reste 3, a 0.60in aucun. Le meme filet a ete essaye puis restreint chez
    VSCode4 pour cette raison exacte. La calibration est un ESTIMATEUR, pas une
    mesure de rendu : brancher ce filet en anomalie de build sans avoir d'abord
    trie ces constats contre un rendu PowerPoint reel bloquerait un deck qui se
    rend correctement — et un filet qui bloque a tort finit debranche.

    Une part de ces 58 vient de l'ESTIMATEUR, pas du deck : le modele de hauteur
    de ligne est une constante (`taille * 0.017 + 4/72`) qui ignore le
    `line_spacing` et les `space_before`/`space_after` que `add_text` pose
    pourtant. Mesure de la revue du 2026-09-09 : en honorant ces valeurs, les
    constats tombent a 22. Regler la tolerance avant de corriger le modele, ce
    serait fixer un seuil sur du bruit."""
    if compte is not None:
        compte.setdefault("examinees", 0)
        compte.setdefault("ignorees", 0)

    def _ignorer():
        if compte is not None:
            compte["ignorees"] += 1

    problemes = []
    for num, slide in enumerate(prs.slides, start=1):
        for sh in slide.shapes:
            if not getattr(sh, "has_text_frame", False):
                continue
            if getattr(sh, "is_placeholder", False):
                _ignorer()
                continue
            tf = sh.text_frame
            try:
                if not tf.word_wrap or tf.auto_size != MSO_AUTO_SIZE.NONE:
                    _ignorer()
                    continue
                if tf.vertical_anchor not in (None, MSO_ANCHOR.TOP):
                    _ignorer()
                    continue
                if getattr(sh, "rotation", 0):
                    _ignorer()
                    continue
                w_in = Emu(sh.width).inches
                h_in = Emu(sh.height).inches
            except Exception:
                _ignorer()
                continue
            if w_in <= 0 or h_in <= 0:
                _ignorer()
                continue
            if compte is not None:
                compte["examinees"] += 1
            est = 0.0
            texte_court = ""
            for p in tf.paragraphs:
                t = "".join(r.text for r in p.runs)
                if not t.strip():
                    continue
                # max des runs styles, pas le premier : un prefixe en petit
                # devant un corps plus grand sous-estimerait toute la hauteur.
                tailles = [r.font.size.pt for r in p.runs if r.font.size]
                taille = max(tailles) if tailles else TYPE["body"]
                lignes = estimer_lignes(t, w_in, taille, cpi_ref=cpi_pessimiste)
                # meme modele de hauteur de ligne que le layout (le +4/72 couvre
                # deja le space_after usuel — pas de double comptage)
                est += lignes * (taille * 0.017 + 4 / 72)
                texte_court = texte_court or t[:40]
            if est > h_in + tolerance_in:
                problemes.append(
                    f"slide {num}: texte ~{est:.2f}in > boite {h_in:.2f}in "
                    f"(« {texte_court}… »)")
    return problemes


def verifier_geometrie(prs, marge_in=0.02):
    """Retourne la liste des problemes : toute forme dont les bords depassent la
    slide (au-dela d'une petite marge de tolerance). Liste vide = OK."""
    W, H = prs.slide_width, prs.slide_height
    tol = Inches(marge_in)
    problemes = []
    for si, slide in enumerate(prs.slides, start=1):
        for shp in slide.shapes:
            try:
                l, t, w, h = shp.left, shp.top, shp.width, shp.height
            except Exception:
                continue
            if None in (l, t, w, h):
                continue
            nom = shp.name or "shape"
            if l < -tol or t < -tol or (l + w) > W + tol or (t + h) > H + tol:
                problemes.append(
                    f"slide {si}: '{nom}' hors cadre "
                    f"(l={Emu(l).inches:.2f} t={Emu(t).inches:.2f} "
                    f"r={Emu(l + w).inches:.2f} b={Emu(t + h).inches:.2f} ; "
                    f"slide {Emu(W).inches:.2f}x{Emu(H).inches:.2f})")
    return problemes


# Zone du badge de pagination heritee du gabarit OCTO. Ce numero n'est PAS un
# placeholder pose sur chaque slide : PowerPoint le rend depuis le master/layout,
# donc `verifier_geometrie` (qui ne regarde que les formes DE LA SLIDE) ne peut
# pas le proteger — une forme de contenu peut le recouvrir sans jamais depasser
# la slide.
#
# La zone est LUE SUR LE GABARIT (`zones_numero_page`), pas codee en dur. La
# valeur ci-dessous n'est qu'un REPLI, pour un gabarit qui ne declarerait aucun
# champ de numero de page. Elle est mesuree sur template-octo.pptx (master
# « Google Shape;10;p1 » : 9.2512 / 5.0874 / 9.7974 / 5.3374 in) et arrondie
# VERS L'EXTERIEUR pour ne pas sous-declarer la zone a proteger.
_ZONE_NUMERO_PAGE_IN = (9.25, 5.08, 9.80, 5.34)  # left, top, right, bottom


def _xfrm_de_groupe_non_transforme(shp):
    """True si `shp` est un groupe dont l'espace ENFANT coincide avec l'espace
    slide (chOff == off, chExt == ext, ni rotation ni miroir) : les coordonnees
    de ses enfants sont alors directement lisibles en coordonnees de slide.
    Sinon False — l'appelant retombe sur la boite englobante du groupe plutot
    que de rendre une position fausse."""
    try:
        grp = shp._element.find(qn("p:grpSpPr"))
        xfrm = grp.find(qn("a:xfrm")) if grp is not None else None
        if xfrm is None:
            return False
        if xfrm.get("rot") or xfrm.get("flipH") or xfrm.get("flipV"):
            return False
        off, ext = xfrm.find(qn("a:off")), xfrm.find(qn("a:ext"))
        choff, chext = xfrm.find(qn("a:chOff")), xfrm.find(qn("a:chExt"))
        if None in (off, ext, choff, chext):
            return False
        return (off.get("x") == choff.get("x") and off.get("y") == choff.get("y")
                and ext.get("cx") == chext.get("cx")
                and ext.get("cy") == chext.get("cy"))
    except Exception:
        return False


def _porte_un_champ_numero(shp):
    element = getattr(shp, "_element", None)
    if element is None:
        return False
    return any(f.get("type") == "slidenum" for f in element.iter(qn("a:fld")))


def _bornes_in(shp):
    """(l, t, r, b) en POUCES, ou None si la forme n'a pas de geometrie lisible."""
    try:
        l, t, w, h = shp.left, shp.top, shp.width, shp.height
    except Exception:
        return None
    if None in (l, t, w, h):
        return None
    return (Emu(l).inches, Emu(t).inches, Emu(l + w).inches, Emu(t + h).inches)


def _zones_numero_page_de(conteneur):
    """Bornes (l, t, r, b) en POUCES de chaque bloc de numero de page porte par
    `conteneur` (un master ou un layout).

    Reconnu par le CHAMP qu'il contient (`<a:fld type="slidenum">`), jamais par
    son nom ni par sa position : le nom (« Google Shape;10;p1 ») est un artefact
    de l'export Google Slides de CE gabarit, et une heuristique de position
    (« en bas a droite ») designerait la premiere forme qui passe par la.

    ADAPTATION AU GABARIT OCTO DE CE PROJET (mesuree le 2026-09-09, elle n'est
    pas dans l'homologue VSCode4) : sur 10 des layouts de template-octo.pptx, le
    champ n'est pas porte par une forme de premier niveau mais par un ENFANT
    d'un groupe qui couvre presque toute la slide (ex. « 63 - Titre, contenu et
    visuel a droite » : groupe de 0.30/0.32 a 9.80/5.34). S'arreter au premier
    niveau — comme `element.iter()` y invite — rendrait une zone de 9,5 x 5,0 in
    et ferait crier `verifier_chrome_gabarit` sur toute forme de contenu de ces
    slides : un filet vrai partout est un filet qu'on debranche. On descend donc
    dans les groupes dont l'espace enfant n'est pas transforme (verifie sur ce
    gabarit : chOff == off, chExt == ext), et on retombe sur la boite englobante
    pour tout groupe transforme."""
    zones = []
    for shp in conteneur.shapes:
        if not _porte_un_champ_numero(shp):
            continue
        enfants = getattr(shp, "shapes", None)
        if enfants is not None and _xfrm_de_groupe_non_transforme(shp):
            sous_zones = _zones_numero_page_de(shp)
            if sous_zones:  # sinon (enfants sans geometrie lisible) on retombe
                zones.extend(sous_zones)  # sur la boite du groupe : une zone
                continue                  # trop large vaut mieux qu'aucune
        bornes = _bornes_in(shp)
        if bornes is not None:
            zones.append(bornes)
    return zones


def zones_numero_page(slide, defaut=_ZONE_NUMERO_PAGE_IN):
    """Les zones de numero de page qui s'appliquent a `slide` : celles de son
    LAYOUT et celles de son MASTER (le gabarit OCTO redouble le bloc a
    l'identique sur les deux), dedoublonnees. Repli sur `defaut` si le gabarit
    n'en declare aucune — un deck sans numero de page n'a rien a proteger, mais
    un repli muet vaut mieux qu'un filet qui disparait en silence."""
    layout = slide.slide_layout
    zones = _zones_numero_page_de(layout) + _zones_numero_page_de(layout.slide_master)
    uniques = {tuple(round(v, 4) for v in z) for z in zones}
    return sorted(uniques) or [defaut]


def verifier_plancher_de_dessin(prs, plancher_in, bord_droit_in=None):
    """Retourne un probleme si le bas de bande que les slides s'imposent
    (`plancher_in`) descend AU NIVEAU du numero de page reellement declare par
    le gabarit charge.

    Les slides derivent ce plancher d'une constante (`CONTENT_BOTTOM` cote
    generateur). Un gabarit qui remonterait son numero de page rendrait cette
    constante fausse EN SILENCE : les slides continueraient de dessiner jusqu'a
    l'ancien plancher, et rien ne dirait pourquoi.

    ADAPTATION AU CANAL DE CE PROJET : le generateur ne dessine pas pleine
    largeur — il s'arrete a `BORD_DROIT` (9.15 in), a GAUCHE du badge de
    pagination (qui commence a 9.25 in), alors que son `CONTENT_BOTTOM` (5.45
    in) passe SOUS le haut de ce badge (5.09 in). Une comparaison purement
    verticale, comme chez l'homologue VSCode4 qui dessine pleine largeur,
    crierait donc a tort sur chaque build. `bord_droit_in`, quand il est fourni,
    exige EN PLUS un recouvrement horizontal : le constat ne tombe que si la
    bande dessinee atteint reellement le badge. Sans lui, comportement identique
    a l'homologue.

    CE QUE `bord_droit_in` COUTE, ET IL FAUT LE SAVOIR (revue bmad-code-review
    du 2026-09-09). Avec les valeurs reelles de ce projet (bande a gauche du
    badge), le filet est vert QUEL QUE SOIT `plancher_in` — meme absurde : ce
    n'est pas un filet inerte, c'est un verdict « pas de recouvrement », mais
    les deux se ressemblent de l'exterieur. Ce qui le fait tomber, c'est donc
    une derive qui ramene le badge DANS la bande (gabarit qui deplace le bloc
    vers la gauche, ou generateur qui elargit `BORD_DROIT`) — le cas verrouille
    par `test_badge_qui_derive_dans_la_bande_est_signale`. Une derive purement
    verticale d'un badge qui reste a droite de la bande ne le fait pas tomber,
    et c'est correct : rien ne se recouvre."""
    zones = [zone for slide in prs.slides for zone in zones_numero_page(slide)]
    if not zones:
        return []
    if bord_droit_in is not None:
        zones = [z for z in zones if bord_droit_in > z[0]]
        if not zones:
            return []
    plus_haut = min(z[1] for z in zones)
    if plancher_in <= plus_haut:
        return []
    return [f"plancher de dessin ({plancher_in:.2f}in) sous le haut de la zone "
            f"du numero de page declaree par le gabarit ({plus_haut:.2f}in) : "
            f"la constante de repli _ZONE_NUMERO_PAGE_IN a decroche du gabarit"]


def verifier_chrome_gabarit(prs, zone_in=None, marge_in=0.02, compte=None):
    """Retourne la liste des problemes : toute forme DE CONTENU (posee sur une
    slide, pas sur le layout/master) dont les bords chevauchent la zone du
    numero de page heritee du gabarit. Liste vide = OK.

    `zone_in` force une zone unique pour toutes les slides (tests) ; par defaut
    la zone est LUE sur le layout/master de CHAQUE slide.

    Meme forme de resultat que `verifier_geometrie` (chaine « slide N: … »),
    pour rester agregeable telle quelle dans le self-check de `build()`.

    `compte` : dict optionnel (`examinees`, `ignorees`, `groupes`), pour la meme
    raison que sur `verifier_debordements_texte`. Les formes groupees sont
    examinees sur leur boite ENGLOBANTE : un enfant fautif se signale alors au
    nom du groupe, jamais au sien."""
    if compte is not None:
        # Les trois clefs sont posees d'avance : le docstring les promet, et
        # « 0 groupe » doit se lire 0, pas se deviner d'une clef absente (revue
        # bmad-code-review du 2026-09-09 — un KeyError chez l'appelant).
        for cle in ("examinees", "ignorees", "groupes"):
            compte.setdefault(cle, 0)
    tol_in = marge_in
    problemes = []
    for si, slide in enumerate(prs.slides, start=1):
        zones = [zone_in] if zone_in is not None else zones_numero_page(slide)
        for shp in slide.shapes:
            bornes = _bornes_in(shp)
            if bornes is None:
                _noter(compte, "ignorees")
                continue
            _noter(compte, "examinees")
            if getattr(shp, "shape_type", None) == MSO_SHAPE_TYPE.GROUP:
                _noter(compte, "groupes")
            l, t, r, b = bornes
            for zone in zones:
                zl, zt, zr, zb = zone
                chevauche = (l < zr - tol_in and r > zl + tol_in
                             and t < zb - tol_in and b > zt + tol_in)
                if not chevauche:
                    continue
                nom = shp.name or "shape"
                problemes.append(
                    f"slide {si}: '{nom}' recouvre la zone du numero de page "
                    f"(l={l:.2f} t={t:.2f} r={r:.2f} b={b:.2f} ; "
                    f"zone {zone[0]:.2f}-{zone[2]:.2f} x "
                    f"{zone[1]:.2f}-{zone[3]:.2f})")
                break
    return problemes


def theme_colors(prs):
    """Lit le nuancier du theme (dk1/lt1/dk2/lt2/accent1..6) du 1er master et le
    renvoie en dict {nom: '#RRGGBB'}. Sert a adapter le deck a la charte du
    template fourni (couleur d'accent de marque) sans rien coder en dur.
    Renvoie {} si le theme est introuvable (l'appelant prevoit un repli)."""
    import re
    try:
        part = prs.slide_masters[0].part
        theme_part = next((r.target_part for r in part.rels.values()
                           if "theme" in r.reltype), None)
        if theme_part is None:
            return {}
        xml = theme_part.blob.decode("utf-8", "ignore")
    except Exception:
        return {}
    m = re.search(r"<a:clrScheme.*?</a:clrScheme>", xml, re.S)
    if not m:
        return {}
    seg = m.group(0)
    out = {}
    for name in ("dk1", "lt1", "dk2", "lt2", "accent1", "accent2",
                 "accent3", "accent4", "accent5", "accent6"):
        mm = re.search(
            r"<a:" + name + r">.*?(?:srgbClr val=\"([0-9A-Fa-f]{6})\"|"
            r"sysClr[^>]*lastClr=\"([0-9A-Fa-f]{6})\")", seg, re.S)
        if mm:
            out[name] = "#" + (mm.group(1) or mm.group(2)).upper()
    return out
