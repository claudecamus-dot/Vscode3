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


def main():
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
    check(len(prs.slides) == 49, f"49 slides — reçu {len(prs.slides)}")
    check(bool(_vu), "build() consulte bien _controler (tous les filets), "
                     "et pas un sous-ensemble câblé en dur")
    check(not problemes,
          "contrôle propre — geometrie + chrome du gabarit + plancher de dessin"
          f" + anomalies de build : {len(problemes or [])} problème(s)")
    check(os.path.exists(out) and os.path.getsize(out) > 500_000,
          f"fichier .pptx écrit, taille plausible ({os.path.getsize(out) if os.path.exists(out) else 0} octets)")

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
    # 9 chapitres (v2.9) : Exec summary(3) · Contexte(7) · Personas(11) ·
    # Besoins & douleurs(14) · Proposition(17) · IA(21) · Démarche(28) ·
    # Outillage IAP(37) · KPI(41)
    # (v2.6 : le sous-chapitre « Exemples » — séparateur + 3 slides — est
    # supprimé, d'où IA/Démarche qui remontent de 4 ; la Démarche gagne les
    # activités humaines avec/sans l'outil, et l'Outillage IAP ouvre sur le
    # schéma d'architecture en contexte client — 3 slides de contenu.
    # v2.7 : +1 dans le Contexte (« qui achète, contre quoi ») et +1 dans la
    # Démarche (« conditions de réussite ») — tout ce qui suit décale d'autant.
    # v2.8 : nouveau chapitre 01 « Exec summary » en OUVERTURE du deck (juste
    # après le sommaire, avant slide_vision) — 3 slides de plus (2 de contenu +
    # 1 intercalaire), tous les chapitres suivants glissent de +1.
    # v2.9 : le chapitre 01 garde 2 slides de contenu (le pitch en 3 faces et la
    # démarche avec/sans agentic remplacent l'offre et sa synthèse) mais le grand
    # schéma du parcours de mission déménage dans la Démarche — +1 slide au total
    # (45 -> 46), donc Outillage IAP et KPI glissent seuls de +1.
    # v2.13 : slide_executive_summary déménage d'AVANT l'intercalaire à APRÈS
    # (arbitrage utilisateur) — l'intercalaire du chapitre 01 recule de 3 à 2,
    # tout le reste (positions 4+, inchangées) ne bouge pas.
    # v2.14/v2.15 avaient câblé slide_synthese_pourquoi_quoi_comment ici (+1
    # slide, 46 -> 47) ; v2.16 la retire de build() (2 tours rejetée) — 46
    # slides à nouveau, indices ci-dessous redevenus ceux de v2.13.)
    # v2.28 : slide_specificites_infra CÂBLÉE juste après l'intercalaire du
    # chapitre 02 (qui reste en 7, l'ajout vient APRÈS lui) — 46 -> 47, tout
    # ce qui suit le chapitre 02 glisse de +1 (Personas 11->12, Besoins &
    # douleurs 14->15, Proposition 17->18, IA 21->22, Démarche 28->29,
    # Outillage IAP 37->38, KPI 41->42).
    # v2.29 : slide_infra_as_product_exemple CÂBLÉE juste après elle (l'exemple
    # avant/après qui rend tangible sa conclusion) — 47 -> 48, encore +1 sur
    # tout ce qui suit le chapitre 02 (Personas 12->13, Besoins & douleurs
    # 15->16, Proposition 18->19, IA 22->23, Démarche 29->30, Outillage IAP
    # 38->39, KPI 42->43).
    # v2.30 : `slide_specificites_infra` et `slide_infra_as_product_exemple`
    # DÉMÉNAGENT du chapitre 02 vers le chapitre 01 (juste après
    # slide_executive_summary) ; `slide_synthese_pourquoi_quoi_comment` est
    # AJOUTÉE entre les deux — net +1 slide au total (48 -> 49). Le chapitre 02
    # commence directement par slide_mission après son intercalaire, qui
    # glisse de +3 (7 -> 10), et tout ce qui suit avec lui (13->14, 16->17,
    # 19->20, 23->24, 30->31, 39->40, 43->44).
    chapitres = [2, 10, 14, 17, 20, 24, 31, 40, 44]
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
    # v2.8 : slide_vision décale de 3 -> 6 (chapitre 01 Exec summary inséré avant elle).
    # v2.30 : +3 slides insérées avant elle dans le chapitre 01 (specificites_infra,
    # synthese_pourquoi_quoi_comment, infra_as_product_exemple) — 6 -> 9.
    slide_vision = prs.slides[8]
    cadre_vision = gen._find_frame_in_group(
        slide_vision.slide_layout.shapes, "Google Shape;212;p17", "Google Shape;213;p17")
    images_vision = _images(slide_vision)
    check(len(images_vision) == 1, f"slide 9 (vision) : exactement 1 image posée (reçu {len(images_vision)})")
    check(cadre_vision is not None, "slide 9 (vision) : cadre 'cadre blanc' trouvé sur le layout")
    if images_vision and cadre_vision:
        pic = images_vision[0]
        l, t, w, h, _ = cadre_vision
        check((pic.left, pic.top, pic.width, pic.height) == (l, t, w, h),
              f"slide 9 (vision) : image alignée exactement sur le cadre "
              f"(image=({pic.left},{pic.top},{pic.width},{pic.height}) vs cadre=({l},{t},{w},{h}))")
        g = pic._element.spPr.find(qn("a:prstGeom"))
        check(g is not None and g.get("prst") == "round2DiagRect",
              "slide 9 (vision) : image clippée au bon preset (round2DiagRect)")

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
