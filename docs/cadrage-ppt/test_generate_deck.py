"""Tests fonctionnels du générateur de synthèse PPT (cadrage BMAD IAP).

Complète la vérification manuelle (rendu PowerPoint COM + relecture, cf.
`pptx-verify`) par des assertions rejouables sur le `.pptx` réellement généré
— même esprit que `test-export-ppt.py`/`test-ppt-charte.py` (VSCode1) et
`test_export_pptx_renders_cleanly_in_a_real_engine` (VSCode2), adapté à un
générateur script (pas une app web) :

  - structure : nombre de slides, géométrie (`D.verifier_geometrie`, déjà
    appelé par `build()`) ;
  - **cadres photo bien calés** : pour chaque chapitre + la slide vision,
    l'image posée doit avoir EXACTEMENT les bornes du cadre du template et
    porter le bon `prstGeom` cloné — pas juste "une image est présente
    quelque part". Trouvé la raison d'être de ce test : une image sur la
    slide 8 avait été jugée "pas bien calée" à l'œil (en fait une photo trop
    pâle qui se fondait dans le fond, cf. mémoire de session) ; ce test ne
    remplace pas l'œil (il ne juge pas la qualité de la photo) mais aurait
    immédiatement confirmé que le cadrage géométrique, lui, était correct —
    et détecterait un vrai décalage si l'un survenait.
  - aucun cadre laissé vide (« ici mettre une Photo » résiduel) ;
  - régression : l'encart numéro de chapitre ne doit jamais réhériter le
    retrait de puce du master (cf. `_sans_puce`, bug trouvé et corrigé) ;
  - obstructions de cadre limitées aux deux formes décoratives connues
    (badge logo/numéro) — une nouvelle obstruction serait un vrai défaut ;
  - aucune police générique (Arial/Calibri/...) explicitement posée, hors le
    repli Arial documenté sur les glyphes ①②③⟲ (hors couverture Outfit) ;
  - rendu réel via LibreOffice : le fichier s'ouvre et produit bien une page
    par slide (pas un fichier que python-pptx parse mais qu'aucun moteur
    n'ouvre proprement).

Usage : python test_generate_deck.py
"""
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import generate_deck as gen
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE
from pptx.oxml.ns import qn

echecs = 0


def check(cond, msg):
    global echecs
    if cond:
        print(f"  ok   {msg}")
    else:
        echecs += 1
        print(f"  FAIL {msg}")


def _images(slide):
    return [s for s in slide.shapes if s.shape_type == MSO_SHAPE_TYPE.PICTURE]


def _soffice_path():
    defaut = r"C:\Program Files\LibreOffice\program\soffice.exe"
    return defaut if os.path.exists(defaut) else "soffice"


def _verifier_rendu_reel(pptx_path, n_slides_attendu, tmp_dir):
    """Convertit en PDF via LibreOffice et compte les pages — même principe
    que le test VSCode2 éponyme : un .pptx qui parse avec python-pptx peut
    quand même être refusé/tronqué par un vrai moteur de rendu."""
    try:
        result = subprocess.run(
            [_soffice_path(), "--headless", "--convert-to", "pdf", "--outdir", tmp_dir, pptx_path],
            capture_output=True, timeout=120,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        return None, f"LibreOffice indisponible ({e}) — vérification réelle non faite"
    if result.returncode != 0:
        return False, f"LibreOffice a échoué : {result.stderr.decode(errors='replace')[:300]}"
    pdf_path = os.path.join(tmp_dir, os.path.splitext(os.path.basename(pptx_path))[0] + ".pdf")
    if not os.path.exists(pdf_path):
        return False, "LibreOffice n'a produit aucun PDF"
    pdf_bytes = open(pdf_path, "rb").read()
    if len(pdf_bytes) < 2000:
        return False, "PDF quasi vide — rendu suspect"
    page_count = len(re.findall(rb"/Type\s*/Page[^s]", pdf_bytes))
    if page_count != n_slides_attendu:
        return False, f"{page_count} page(s) rendue(s) pour {n_slides_attendu} slide(s) exportée(s)"
    return True, f"{page_count} page(s) rendues, conforme aux {n_slides_attendu} slides"


def _verifier_contrat_cache_image():
    """Contrat du cache disque `_img/` de `_remplir_cadre` : le nom de fichier
    réservé à une vraie photo Openverse ne doit jamais être occupé par un repli
    procédural (`nature_images`), sinon un incident réseau TRANSITOIRE dégrade
    le deck en PERMANENCE — plus aucun build suivant ne retente Openverse pour
    cette scène, même après le retour du réseau (défaut trouvé lors de la
    lecture du contrat de cache, salle atelier-dev, corrigé le 2026-09-16).

    Isolé dans un dossier `_img` temporaire (jamais celui du dépôt) et sans
    accès réseau réel : `stock_images.fetch_to` est simulé en échec puis en
    succès, sans passer par un vrai appel HTTP."""
    import tempfile
    from unittest import mock

    from pptx.util import Emu

    tmp_img = tempfile.mkdtemp(prefix="test-imgcache-")
    img_dir_reel, manifest_reel = gen.deck_images.IMG_DIR, gen.deck_images.IMG_MANIFEST
    gen.deck_images.IMG_DIR = tmp_img
    gen.deck_images.IMG_MANIFEST = os.path.join(tmp_img, "manifest.json")
    try:
        prs = Presentation(gen.TEMPLATE)
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        cadre = (Emu(0), Emu(0), Emu(1_000_000), Emu(1_000_000), None)

        with mock.patch.object(gen.stock_images, "fetch_to",
                                side_effect=RuntimeError("panne réseau simulée")):
            gen._remplir_cadre(slide, cadre, "forest", seed=0)

        appelee = {"n": 0}

        def _fetch_to_retabli(path, query, seed=0, aspect_ratio=None, manifest_path=None):
            appelee["n"] += 1
            from PIL import Image as _Image
            _Image.new("RGB", (200, 200), color=(10, 80, 30)).save(path, "JPEG")
            return path

        with mock.patch.object(gen.stock_images, "fetch_to", side_effect=_fetch_to_retabli):
            gen._remplir_cadre(slide, cadre, "forest", seed=0)

        check(appelee["n"] > 0,
              "réseau revenu après une panne : Openverse est retenté "
              "(le repli ne squatte plus le nom de cache de la vraie photo)")
    finally:
        gen.deck_images.IMG_DIR, gen.deck_images.IMG_MANIFEST = img_dir_reel, manifest_reel
        import shutil
        shutil.rmtree(tmp_img, ignore_errors=True)


def main():
    print("Contrat du cache image (_remplir_cadre) :")
    _verifier_contrat_cache_image()

    # `build()` consulte-t-il ENCORE _controler ? Les tests pytest appellent
    # _controler en direct : aucun n'observe le site d'appel, donc le remettre à
    # `verifier_geometrie(prs) + _ANOMALIES_BUILD` — l'état exact que le câblage
    # des filets corrige — laissait la suite entièrement verte (mesuré le
    # 2026-09-10 : 196 passed sur le mutant). Ce script est le seul exécutant
    # réel de `build()` : la sentinelle se pose donc ici.
    _controler_reel = gen._controler
    _vu = []

    def _controler_sentinelle(prs):
        _vu.append(True)
        return _controler_reel(prs)

    gen._controler = _controler_sentinelle
    try:
        problemes = gen.build()
    finally:
        gen._controler = _controler_reel

    out = os.path.join(gen.HERE, "bmad-iap-cadrage-synthese.pptx")
    prs = Presentation(out)

    print("Structure :")
    # Chiffre volontairement EN DUR : c'est un fil-piege contre une slide
    # ajoutee ou perdue sans intention. Il se met a jour quand on change le
    # deck exprès. Le 2026-09-10 : 49 -> 52 (chapitre « Specificites de
    # l'infra » : intercalaire + 2 slides neuves), puis 52 -> 53 (le
    # traitement partage du gaspillage, au chapitre Proposition). Le
    # 2026-09-11 : 53 -> 54 (slide_fil_technique, chapitre Démarche — comble
    # un manque relevé en revue face à une demande client réelle : CI/CD et
    # plateformes standard n'existaient qu'en notes "TECH :" éparpillées),
    # puis 54 -> 52 (chapitre 01 « Exec summary » jugé trop lourd : ramené à
    # 3 slides de contenu, slide_pitch_iap et slide_demarche_avec_sans_agentic
    # supprimées, leur matière utile absorbée par
    # slide_synthese_pourquoi_quoi_comment refondue). 52 -> 53 (v2.35,
    # restructuration en 9 chapitres dont Annexes). 53 -> 45 (v2.36, chapitre
    # Annexes retiré à la demande utilisateur : 7 fonctions de slide
    # supprimées avec lui, plus l'intercalaire de chapitre). 45 -> 41 (v2.37,
    # arbitrage du 2026-09-20 : fils humain + technique fusionnés en
    # slide_deux_fils, 3 slides d'agent regroupées en slide_agents_candidats,
    # slide_livrables_ppt supprimée).
    # v2.40 (trame arbitrée du 2026-09-23) : 41 -> 41 — 8 intercalaires
    # deviennent 7 (-1 : Executive summary, Enjeux, Douleur, Opportunités, Next
    # steps retirés ; Ce que ça coûte, Nos convictions, L'IA sous contrôle,
    # Réussir et démarrer ajoutés), slide_convictions neuve (+1), annexe sans
    # intercalaire. Même total par coïncidence, pas par constance du contenu.
    # v2.41 (restructuration validée du 2026-09-23) : 41 -> 37 — schéma de
    # fonctionnement et workflows supprimés (-2), gate+prudence fusionnées
    # (-1), ambition+SI+contexte client fusionnées (-2), slide_intro_agentic
    # neuve (+1), intercalaire « L'IA sous contrôle » remplacé par « L'expertise
    # agentic d'OCTO » (0), schéma d'accompagnement passé en annexe (0).
    # v2.42 (six retours utilisateur) : 37 -> 34 — « Ce que ça coûte » 6 -> 3
    # slides (-3), « L'offre » 4 -> 3 (-1), intercalaire « Annexes » (+1).
    # v2.44 : 34 -> 35 — convictions sur deux slides (fusion avec l'exemple client).
    check(len(prs.slides) == 35, f"35 slides — reçu {len(prs.slides)}")
    check(bool(_vu), "build() consulte bien _controler (tous les filets), "
                     "et pas un sous-ensemble câblé en dur")
    check(not problemes,
          "contrôle propre — geometrie + chrome du gabarit + plancher de dessin"
          f" + anomalies de build : {len(problemes or [])} problème(s)")
    check(os.path.exists(out) and os.path.getsize(out) > 500_000,
          f"fichier .pptx écrit, taille plausible ({os.path.getsize(out) if os.path.exists(out) else 0} octets)")

    # --- Renvois vers un autre chapitre : le couplage est SUPPRIMÉ, pas surveillé.
    # Des slides citaient d'autres chapitres par leur NUMÉRO (« Détaillé aux
    # chapitres 03 et 04 »). Insérer un chapitre décalait tous les suivants et
    # rendait ces phrases fausses en silence — géométrie verte, rendu vert, et
    # c'est le lecteur du deck qui tombe sur le mauvais chapitre.
    #
    # Une première version de ce test gardait le couplage : elle vérifiait que
    # le numéro cité existe, et que le nom accolé corresponde. Le mutant l'a
    # traversée (2026-09-10) — « chapitres 03 et 04 » laissé tel quel après
    # renumérotation pointe deux chapitres qui EXISTENT, simplement plus les
    # bons, et ne porte aucun nom à confronter. Un renvoi nu est indétectable
    # par construction : rien dans le deck ne dit où il DEVRAIT pointer.
    #
    # D'où la règle, plus forte que le test qu'elle remplace : on cite un
    # chapitre par son NOM, jamais par son numéro. Une renumérotation ne peut
    # alors plus rien casser, et le lecteur n'a pas à compter les intercalaires.
    print("Renvois de chapitre — par nom, jamais par numéro :")

    def _formes(conteneur):
        """Descend dans les groupes — un renvoi peut y être enfermé."""
        for shp in conteneur:
            if shp.shape_type == MSO_SHAPE_TYPE.GROUP:
                yield from _formes(shp.shapes)
            else:
                yield shp

    chapitres = {}
    for sl in prs.slides:
        if sl.slide_layout.name.startswith("50 - Chapitre"):
            phs = {ph.placeholder_format.idx: ph for ph in sl.placeholders}
            numero = phs[1].text_frame.text.strip()
            chapitres[numero] = phs[0].text_frame.paragraphs[0].text.strip()
    check(bool(chapitres), f"intercalaires détectés — {len(chapitres)} chapitre(s)")

    # La séquence, pas seulement la présence : `chapitres` est indexé par le
    # numéro imprimé, donc un doublon écraserait silencieusement son jumeau. Ce
    # chantier vient de renuméroter sept intercalaires à la main (2026-09-10) —
    # c'est exactement le geste qui produit un trou ou un doublon.
    attendu = [f"{i:02d}" for i in range(1, len(chapitres) + 1)]
    check(sorted(chapitres) == attendu,
          f"numéros de chapitre = suite continue depuis 01 — reçu {sorted(chapitres)}")

    # Renvois RELATIFS : immunisés par nature à une renumérotation, rien à
    # vérifier. La 1re version les reconnaissait à leur minuscule initiale, ce
    # qui refusait « chapitre Précédent » en début de phrase et acceptait
    # n'importe quel mot capitalisé. Liste explicite désormais.
    RELATIFS = ("précédent", "precedent", "suivant", "suivante", "suivants",
                "suivantes", "qui suit", "qui suivent", "ci-avant", "ci-après",
                "ci-apres", "en cours", "courant", "de ce deck")

    numerotes, nommes = [], []
    for i, sl in enumerate(prs.slides, start=1):
        for shp in _formes(sl.shapes):
            if not shp.has_text_frame:
                continue
            texte = shp.text_frame.text
            # `re.I` et `\d{1,2}` ne sont PAS des raffinements : sans eux la
            # garde ne voyait RIEN. Le deck écrit « Chapitres 02 », « CHAPITRE
            # 06 » — majuscules — et la 1re version cherchait « chapitres » en
            # minuscules avec exactement deux chiffres. Six renvois numérotés
            # ont vécu dans le livrable pendant que le test annonçait « aucun »,
            # et le mutant qui l'a « validée » était écrit en minuscules,
            # c'est-à-dire à la forme de la regex qu'il devait éprouver
            # (2026-09-10). Un mutant doit reproduire la DONNÉE réelle, pas la
            # forme du contrôle.
            for m in re.finditer(r"chapitres?\s+(\d{1,2})", texte, re.I):
                numerotes.append(f"slide {i} : « {m.group(0)} »")
            for m in re.finditer(r"chapitres?\s+([^\n,;.)»]+)", texte, re.I):
                frag = m.group(1).strip()
                if not frag or frag[0].isdigit():
                    continue
                if any(r in frag.lower() for r in RELATIFS):
                    continue
                nommes.append((i, frag))

    check(not numerotes,
          f"aucun renvoi par NUMÉRO — un décalage de chapitre les rendrait faux "
          f"silencieusement : {numerotes or 'aucun'}")

    # Ce qui suit « chapitre » doit COMMENCER par un titre connu. Deux pièges
    # écartés par cette formulation :
    #  - la sous-chaîne : `"ia" in "différenciation"` est vrai, donc « le
    #    chapitre Différenciation » passait pour un renvoi valide vers IA ;
    #  - le découpage sur « et » : il tronçonne une PHRASE, pas une liste de
    #    noms. « les decks du chapitre Démarche restent pour sponsor et comité
    #    de pilotage » produisait « comité de pilotage » en faux positif.
    # LIMITE ASSUMÉE, à dire plutôt qu'à masquer : dans « chapitres Personas et
    # Foobar », seul le premier nom est vérifié — le second passerait. Le
    # couvrir demanderait de savoir où finit l'énumération et où reprend la
    # phrase, ce que rien dans le texte ne dit.
    titres = sorted((t.lower() for t in chapitres.values()), key=len, reverse=True)
    # v2.40 : guillemets et apostrophe typographique neutralisés — « chapitre
    # « L'IA sous contrôle » » ou « L’offre » ne doivent pas passer pour inconnus.
    def _norm(t):
        return t.lower().replace("’", "'").lstrip("«“\"  ")
    inconnus = sorted(
        f"slide {i} : « {frag} »" for i, frag in nommes
        if not any(_norm(frag).startswith(_norm(t)) for t in titres)
    )
    check(not inconnus,
          f"(c) tout renvoi nommé désigne un chapitre existant — inconnus : {inconnus or 'aucun'}")

    # (b) v2.40 : AUCUN renvoi positionnel. La garde ci-dessus les laissait
    # passer (« immunisés à une renumérotation ») — mais « slide précédente »
    # devient faux dès qu'on déplace une slide, ce que la trame v2.40 a fait
    # à la moitié du deck : le renvoi de la prudence IA pointait sur une slide
    # qui n'était plus la précédente. Nommer, ou supprimer.
    POSITIONNEL = re.compile(
        r"\b(slides?|chapitres?|pages?)\s+(suivante?s?|précédente?s?|precedente?s?"
        r"|ci-dessus|ci-dessous|ci-avant|ci-après|qui suit|qui suivent)\b", re.I)
    positionnels = [f"slide {i} : « {m.group(0)} »"
                    for i, sl in enumerate(prs.slides, start=1)
                    for shp in _formes(sl.shapes) if shp.has_text_frame
                    for m in POSITIONNEL.finditer(shp.text_frame.text)]
    check(not positionnels,
          f"(b) aucun renvoi positionnel (slide/chapitre suivant·e/précédent·e) : "
          f"{positionnels or 'aucun'}")

    # (a) v2.40 : le kicker de chaque slide de contenu EST le nom de son
    # chapitre — celui de l'intercalaire qui la précède, EXECUTIVE SUMMARY avant
    # le premier, ANNEXE admis seulement après le dernier chapitre. Cinq
    # kickers citaient des chapitres disparus au rendu v2.39 (« IA »,
    # « PROPOSITION », « BESOINS & DOULEURS », « OUTILLAGE IAP », « DÉMARCHE »).
    print("Kickers = nom du chapitre porteur :")
    SEP = "   ·   "
    courant, faux = "EXECUTIVE SUMMARY", []
    n_chap_vus, n_chap = 0, len(chapitres)
    for i, sl in enumerate(prs.slides, start=1):
        nom_layout = sl.slide_layout.name
        if nom_layout.startswith("50 - Chapitre"):
            ph0 = next(p for p in sl.placeholders if p.placeholder_format.idx == 0)
            courant = ph0.text_frame.paragraphs[0].text.strip().upper()
            n_chap_vus += 1
            continue
        if i == 1:
            continue   # couverture
        ph0 = next((p for p in sl.placeholders if p.placeholder_format.idx == 0), None)
        texte = ph0.text_frame.text if ph0 is not None else ""
        kicker = texte.split(SEP)[0].strip() if SEP in texte else None
        attendu = {courant}
        if n_chap_vus == n_chap:
            attendu.add("ANNEXE")
        if kicker not in attendu:
            faux.append(f"slide {i} : {kicker!r} (attendu {sorted(attendu)})")
    check(not faux, f"(a) kicker de chaque slide de contenu = son chapitre : {faux or 'tous conformes'}")

    # Charte (arbitrage 2026-09-10) : aucun texte cyan, aucun texte blanc posé
    # sur un aplat cyan (1,86:1). Relevé au rendu v2.39 sur deux pastilles.
    print("Charte — aucun texte cyan, aucun blanc sur cyan :")
    CYAN = str(gen.ACCENT).lstrip("#").upper()

    def _fill(shp):
        try:
            return str(shp.fill.fore_color.rgb) if shp.fill.type == 1 else None
        except Exception:
            return None

    def _couleur(run):
        try:
            return str(run.font.color.rgb) if run.font.color and run.font.color.type is not None else None
        except Exception:
            return None

    viol = []
    for i, sl in enumerate(prs.slides, start=1):
        formes = list(_formes(sl.shapes))
        aplats = [(f.left, f.top, f.left + f.width, f.top + f.height) for f in formes
                  if _fill(f) == CYAN and f.width and f.height]
        for shp in formes:
            if not shp.has_text_frame or shp.left is None:
                continue
            cx, cy = shp.left + shp.width // 2, shp.top + shp.height // 2
            sur_cyan = _fill(shp) == CYAN or any(
                a <= cx <= c and b <= cy <= d for a, b, c, d in aplats)
            for p in shp.text_frame.paragraphs:
                for r in p.runs:
                    if not r.text.strip():
                        continue
                    c = _couleur(r)
                    if c == CYAN:
                        viol.append(f"slide {i} : texte cyan « {r.text[:25]} »")
                    elif c == "FFFFFF" and sur_cyan:
                        viol.append(f"slide {i} : blanc sur cyan « {r.text[:25]} »")
    check(not viol, f"charte : {viol or 'aucune violation'}")

    print("Version affichée en couverture à jour (v2.8 y est restée gelée 4 bumps de suite) :")
    versions_docstring = [tuple(int(p) for p in v.split("."))
                           for v in re.findall(r"(?m)^v(\d+\.\d+)", gen.__doc__ or "")]
    version_courante = tuple(int(p) for p in gen.VERSION_DECK.lstrip("v").split("."))
    check(bool(versions_docstring) and max(versions_docstring) == version_courante,
          f"VERSION_DECK ({gen.VERSION_DECK}) == dernière entrée de version du docstring "
          f"({'v' + '.'.join(map(str, max(versions_docstring))) if versions_docstring else 'aucune trouvée'})")
    couverture = prs.slides[0]
    texte_version = next((ph.text_frame.text for ph in couverture.placeholders
                           if ph.placeholder_format.idx == 3), None)
    check(texte_version == f"{gen.VERSION_DECK} · {gen.DATE_VERSION_DECK}",
          f"placeholder version de la couverture == VERSION_DECK/DATE_VERSION_DECK (reçu {texte_version!r})")

    print("Cadres photo bien calés (chapitres — layout '50 - Chapitre', teardrop) :")
    # Index DERIVES du deck, plus jamais ecrits a la main. Ce bloc portait
    # 40 lignes d'historique de renumerotation (« Personas 11->12, Besoins &
    # douleurs 14->15... ») recalculees a chaque insertion de slide : ajouter
    # le chapitre 03 « Specificites de l'infra » (2026-09-10) a fait tomber 21
    # verifications d'un coup, toutes pour cette seule raison. L'historique
    # vit dans `git log docs/cadrage-ppt/`, sa place.
    chapitres = [i for i, sl in enumerate(prs.slides, start=1)
                 if sl.slide_layout.name.startswith('50 - Chapitre')]
    for idx in chapitres:
        slide = prs.slides[idx - 1]
        cadre = gen._find_frame_by_geom(slide.slide_layout.shapes, "teardrop")
        images = _images(slide)
        check(len(images) == 1, f"slide {idx} : exactement 1 image posée (reçu {len(images)})")
        check(cadre is not None, f"slide {idx} : cadre teardrop trouvé sur le layout")
        if images and cadre:
            pic = images[0]
            l, t, w, h, _ = cadre
            check((pic.left, pic.top, pic.width, pic.height) == (l, t, w, h),
                  f"slide {idx} : image alignée exactement sur le cadre "
                  f"(image=({pic.left},{pic.top},{pic.width},{pic.height}) vs cadre=({l},{t},{w},{h}))")
            g = pic._element.spPr.find(qn("a:prstGeom"))
            check(g is not None and g.get("prst") == "teardrop",
                  f"slide {idx} : image clippée au bon preset (teardrop)")

    print("Cadre photo bien calé (slide vision — layout 'cadre blanc', round2DiagRect) :")
    # Index DERIVE, meme raison que pour les chapitres : c'est la SEULE slide du
    # deck posee sur le layout « cadre blanc ». La chercher par son layout est
    # plus vrai que compter les slides qui la precedent.
    _sur_cadre_blanc = [sl for sl in prs.slides if "cadre blanc" in sl.slide_layout.name]
    check(len(_sur_cadre_blanc) == 1,
          f"une seule slide sur le layout « cadre blanc » — trouve {len(_sur_cadre_blanc)}")
    slide_vision = _sur_cadre_blanc[0]
    cadre_vision = gen._find_frame_in_group(
        slide_vision.slide_layout.shapes, "Google Shape;212;p17", "Google Shape;213;p17")
    images_vision = _images(slide_vision)
    check(len(images_vision) == 1, f"slide vision : exactement 1 image posée (reçu {len(images_vision)})")
    check(cadre_vision is not None, "slide vision : cadre 'cadre blanc' trouvé sur le layout")
    if images_vision and cadre_vision:
        pic = images_vision[0]
        l, t, w, h, _ = cadre_vision
        check((pic.left, pic.top, pic.width, pic.height) == (l, t, w, h),
              f"slide vision : image alignée exactement sur le cadre "
              f"(image=({pic.left},{pic.top},{pic.width},{pic.height}) vs cadre=({l},{t},{w},{h}))")
        g = pic._element.spPr.find(qn("a:prstGeom"))
        check(g is not None and g.get("prst") == "round2DiagRect",
              "slide vision : image clippée au bon preset (round2DiagRect)")

    print("Aucun cadre laissé vide (texte gabarit « ici mettre une Photo » résiduel) :")
    texte_complet = "\n".join(
        shp.text_frame.text for slide in prs.slides for shp in slide.shapes if shp.has_text_frame)
    check("ici mettre une Photo" not in texte_complet, "aucun texte gabarit de cadre photo résiduel")

    print("Régression — encart numéro de chapitre sans retrait de puce hérité (bug trouvé/corrigé) :")
    for idx in chapitres:
        slide = prs.slides[idx - 1]
        ph = next((p for p in slide.placeholders if p.placeholder_format.idx == 1), None)
        check(ph is not None, f"slide {idx} : placeholder numéro (idx=1) présent")
        if ph is not None:
            p_el = ph.text_frame.paragraphs[0]._p
            pPr = p_el.find(qn("a:pPr"))
            marL = pPr.get("marL") if pPr is not None else None
            indent = pPr.get("indent") if pPr is not None else None
            bu_none = pPr.find(qn("a:buNone")) is not None if pPr is not None else False
            check(marL == "0" and indent == "0" and bu_none,
                  f"slide {idx} : numéro sans retrait de puce hérité (marL={marL}, indent={indent}, buNone={bu_none})")

    print("Obstructions de cadre — limitées aux 2 formes décoratives connues (badge logo/numéro) :")
    attendus = {"Google Shape;37;p4", "Google Shape;54;p4"}
    for idx in chapitres:
        slide = prs.slides[idx - 1]
        cadre = gen._find_frame_by_geom(slide.slide_layout.shapes, "teardrop")
        if cadre:
            obstructions = gen.frame_obstructions(slide, *cadre[:4])
            noms = {o["name"] for o in obstructions}
            check(noms <= attendus, f"slide {idx} : pas d'obstruction inattendue (trouvé {noms - attendus or 'aucune'})")

    print("Police — Outfit partout, sauf repli Arial documenté sur les glyphes hors couverture :")
    # v2.30 : _appliquer_police_deck pose Outfit sur tout le deck, avec un repli
    # volontaire en Arial (POLICE_SECOURS) sur les seuls runs des glyphes
    # ①②③⟲ (GLYPHES_HORS_POLICE_DECK — absents du cmap Outfit, vérifié sur
    # LibreOffice ET PowerPoint COM). Tout AUTRE run en police générique reste
    # un vrai défaut.
    generiques = {"arial", "calibri", "times new roman", "segoe ui"}
    trouve = set()
    for slide in prs.slides:
        for shp in slide.shapes:
            if shp.has_text_frame:
                for p in shp.text_frame.paragraphs:
                    for r in p.runs:
                        if (r.font.name and r.font.name.lower() in generiques
                                and r.text.strip() not in gen.GLYPHES_HORS_POLICE_DECK):
                            trouve.add((r.font.name, r.text))
    check(not trouve, f"aucune police générique posée hors repli documenté{' (trouvé ' + str(sorted(trouve)) + ')' if trouve else ''}")

    print("Rendu réel (LibreOffice — conversion PDF, comptage de pages) :")
    import tempfile
    with tempfile.TemporaryDirectory(prefix="test-ppt-render-") as tmp:
        ok, detail = _verifier_rendu_reel(out, len(prs.slides), tmp)
        if ok is None:
            print(f"  --   {detail}")
        else:
            check(ok, detail)

    print("\nTOUS LES TESTS PASSENT" if echecs == 0 else f"\n{echecs} TEST(S) EN ECHEC")
    sys.exit(0 if echecs == 0 else 1)


if __name__ == "__main__":
    main()
