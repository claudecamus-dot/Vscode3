"""Sous-système image/cadre (extrait mécaniquement de generate_deck.py) :
recherche des cadres du gabarit, photos Openverse en cache, repli procédural,
_remplir_cadre et _photo_libre.
"""
import os
import sys

import pptx_deck as D
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.dml import MSO_LINE_DASH_STYLE
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Emu, Inches, Pt

from deck_theme import (  # noqa: E402,F401 — extraction mécanique v2.46
    HERE,
    TEMPLATE,
    LAYOUT_COUVERTURE,
    LAYOUT_TITRE_SEUL,
    LAYOUT_VIDE,
    LAYOUT_CHAPITRE,
    LAYOUT_VISUEL_DROITE,
    MARGIN,
    BORD_DROIT,
    CONTENT_TOP,
    CONTENT_BOTTOM,
    CONTENT_W,
    CONTENT_H,
    GAP,
    _exiger_template,
    TH,
    NAVY,
    DK2,
    WHITE,
    ACCENT,
    MUTED,
    ACCENT1,
    ACCENT2,
    LINE,
    TRACK,
    RAYON_COIN_IN,
    _add_rect_brut,
    _add_rect_arrondi,
    SEVERITE,
    _rgb,
    new_prs,
    ENCRE,
    ACCENT_PLEIN,
    SUPPORT,
    SUPPORT_LIGNE,
    encre_de,
)

REPO_ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.append(os.path.join(REPO_ROOT, ".claude", "skills", "pptx-framed-image", "scripts"))
import nature_images  # noqa: E402
import stock_images  # noqa: E402
from framed_image import cover_crop_to_aspect, frame_obstructions, place_image_in_frame  # noqa: E402
from PIL import Image as _PILImage  # noqa: E402

IMG_DIR = os.path.join(HERE, "_img")
os.makedirs(IMG_DIR, exist_ok=True)
IMG_MANIFEST = os.path.join(HERE, "images-manifest.json")


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
    # Littoral rocheux turquoise (chapitre Besoins & douleurs) : « ocean waves aerial » (horizon
    # brumeux délavé en blanc) puis « turquoise sea water aerial » (0 résultat
    # Openverse -> repli procédural à ciel pâle) échouaient tous deux à ancrer le
    # haut du cadre teardrop sur le fond blanc de la slide. « turquoise water »
    # (seed 0) renvoie une vue plongeante roche+eau+écume, texturée et contrastée
    # sur les quatre bords — VÉRIFIÉE au rendu réel le 2026-07-21.
    "ocean": "turquoise water",
    "sunset": "sunset sky",
    # Chapitres à photo (restructurations 7 puis 8 puis 9 chapitres) : scènes réelles
    # distinctes, VÉRIFIÉES au rendu réel — une requête mot-clé n'a aucun jugement (cf. « plage
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
    # tropical (Outillage IAP, chapitre 08 — nommé chapitre 07 en v2.5) : nom CONNU
    # du fallback procédural (forest/meadow/mountains/ocean/sunset/tropical), donc
    # sûr même hors ligne. Photo à VÉRIFIER au rendu réel comme les autres.
    "tropical": "tropical palm leaves",
    # wheatfield (Exec summary, chapitre 01, nouveau v2.8) : épis de blé doré, gros
    # plan texturé — la récolte/le résultat, en écho au thème du chapitre (l'offre
    # ET sa synthèse, « ce que la mission produit »). « golden wheat field sunset »/
    # « wheat field golden hour » (0 résultat Openverse en aspect carré, le cadre
    # teardrop de ce layout est carré — pas « tall » comme les autres chapitres)
    # échouaient ; « wheat field » simple RENVOIE un résultat, gros plan contrasté
    # sur les 4 bords — VÉRIFIÉE au rendu réel le 2026-09-02. Nom NEUF → repli
    # procédural qui PLANTE sauf mapping _SCENE_REPLI (ci-dessous).
    "wheatfield": "wheat field",
    # riverdelta (Specificites de l'infra, chapitre 03, neuf en v2.33) : un delta
    # — un seul cours d'eau qui alimente toutes les branches — dit litteralement
    # le sujet du chapitre (une infra transverse sous plusieurs equipes). « canyon »
    # etait deja pris par la Demarche : deux chapitres a la meme photo se lisent
    # comme une erreur de montage. Nom NEUF -> repli obligatoire ci-dessous.
    # Photo A VERIFIER AU RENDU comme toutes les autres : une requete mot-cle
    # n'a aucun jugement (cf. « desert dune » -> fossile de musee, trouve puis
    # ecarte le 2026-09-01, jamais expose car hors des scenes REELLEMENT
    # appelees par le deck — seul « river delta aerial » l'etait).
    # « river delta aerial » (seed=0, requete d'origine) rendait le resultat
    # Openverse #0 : une image satellite en fausses couleurs arc-en-ciel
    # PORTANT UN FILIGRANE « rawpixel » tuile visible sur toute la photo —
    # trouve au rendu reel zoome du 2026-09-11, jamais vu au rendu non-zoome
    # (la vignette de slide le masque). Reciblee sur la requete plus large
    # « river delta » (7 resultats CC0) : l'index 5 (NASA, credit Openverse,
    # delta du Gange/Brahmapoutre) est SANS filigrane sur toute sa surface
    # (verifie par crop plein-cadre des 3 coins) et sa palette (chenaux
    # sombres/creme) est plus proche de la charte navy+cyan que l'original.
    # Ordre Openverse reverifie stable entre deux appels le 2026-09-11 (meme
    # URL) — meme fragilite structurelle que le reste de ce mapping mot-cle
    # (aucun jugement de contenu cote API), a re-verifier si jamais le
    # resultat change de nature au rendu.
    "riverdelta": "river delta",
}


# Repli procedural : nature_images ne connait que 6 scenes
# (forest/meadow/mountains/ocean/sunset/tropical). Les noms NEUFS choisis pour
# les chapitres (dunes, nightsky, canyon) n'y sont pas — hors reseau ou sur
# 0-resultat Openverse, generate_to levait ValueError HORS du try, ce qui tuait
# build() en entier : 0 slide produite alors que 37 des 40 n'ont pas de photo
# (mesure du 2026-09-01). On mappe donc chaque nom neuf sur la scene connue la
# plus proche visuellement. Ce n'est PAS la meme image — c'est un repli assume,
# dont le but est que le deck sorte, pas qu'il soit identique.
_SCENE_REPLI = {
    "dunes": "sunset",       # tons chauds sable/orange
    "nightsky": "sunset",    # composition de ciel (clair au lieu de sombre)
    "canyon": "mountains",   # relief rocheux
    "wheatfield": "meadow",  # champ ouvert, tons chauds proches
    # « ocean » aurait ete le repli visuellement le plus proche, mais c'est la
    # scene REELLE du chapitre 05 : hors ligne, les chapitres 03 et 05 auraient
    # rendu la meme image. « sunset » n'est la scene reelle d'aucun chapitre —
    # un repli doit degrader, pas dupliquer un voisin. (« canyon » -> mountains
    # porte le meme defaut, anterieur a ce chantier : mountains est la scene du
    # chapitre 02.)
    "riverdelta": "sunset",
}

# Anomalies relevees pendant le build (pas seulement d'image, malgre le nom
# historique), fusionnees dans `problemes` par build(). Sans cela, un defaut
# ne sortait qu'en print : le build annoncait « GEOMETRIE: OK » avec des
# photos manquantes (cadre introuvable/repli impossible) OU, depuis v2.11,
# avec un contenu qui deborde silencieusement sous un element de pied de
# carte (cf. slide_pitch_iap, supprimee en v2.34 -- voir archives/ : le
# self-check geometrique de pptx_deck.py ne
# mesure QUE les formes que NOUS dessinons hors-cadre — pas un debordement de
# texte dans son propre panneau).
_ANOMALIES_BUILD = []


def _image_cache_valide(path):
    """True si `path` est une image utilisable : fichier non vide, décodable
    par PIL, et de dimensions plausibles pour un cadre du deck (>= 32 px sur
    chaque côté, <= 8000 px). Un fichier de 0 octet laissé par un build
    interrompu (Ctrl-C pendant `fetch_to`/`save`) — ou, pour le contenu
    Openverse fraîchement téléchargé, une image corrompue/hors format —
    ne doit jamais être réputé valide (audit VSCode3 2026-09-23, constats
    R2/S1 : `os.path.exists()` seul ne prouve rien sur le contenu)."""
    try:
        if not os.path.exists(path) or os.path.getsize(path) <= 0:
            return False
        with _PILImage.open(path) as im:
            im.verify()
        with _PILImage.open(path) as im:
            largeur, hauteur = im.size
            if largeur < 32 or hauteur < 32 or largeur > 8000 or hauteur > 8000:
                return False
        return True
    except Exception:
        return False


def _remplir_cadre(slide, cadre, scene, seed=0):
    """Pose une vraie photo libre de droit (Openverse, CC0) à l'aspect exact
    du cadre, repli sur la génération procédurale (nature_images) si le
    réseau/l'API n'est pas disponible — cf. pptx-framed-image, greffé depuis
    VSCode1. Une photo réelle lit mieux qu'un aplat vectoriel généré, constat
    fait en comparant au REX "⛱️ L'Été de l'IA" (VSCode1) qui utilise de
    vraies photos sur ces mêmes cadres.

    Contrat du cache disque (``_img/``) : le nom de fichier ``path`` ci-dessous
    ne doit exister QUE pour une vraie photo Openverse — jamais pour un repli
    procédural. Avant ce correctif, le repli s'écrivait SOUS LE MÊME NOM que la
    photo réelle ; `os.path.exists(path)` passait alors à True pour de bon, et
    plus aucun build suivant ne retentait Openverse pour cette scène — même
    après le retour du réseau, un incident réseau transitoire dégradait le
    deck en PERMANENCE (repro : appel avec `fetch_to` en échec puis en succès,
    le 2e appel ne rappelait jamais `fetch_to`). Le repli est donc désormais
    écrit sous un nom distinct (`_repli`) : il ne bloque plus la case
    `os.path.exists(path)` qui protège la vraie photo, et chaque build retente
    Openverse tant qu'aucune vraie photo n'a été mise en cache."""
    if cadre is None:
        msg = f"cadre introuvable pour la scène '{scene}' — image non posée"
        print(f"  {msg}")
        _ANOMALIES_BUILD.append(msg)
        return
    left, top, width, height, geom = cadre
    aspect = Emu(width).inches / Emu(height).inches
    px_w = 960
    px_h = int(round(px_w / aspect))
    # Cache en .jpg, pas .png : le contenu est une PHOTO (network ou repli
    # procedural), et cover_crop_to_aspect()/generate_to() infèrent l'encodage
    # du seul suffixe du chemin passé. Une photo cachée en PNG (lossless) sur
    # ~1000px pèse 5 à 10× plus qu'un JPEG visuellement identique — c'était
    # la quasi-totalité des 26 Mo mesurés dans le .pptx exporté (2026-09-11).
    path = os.path.join(IMG_DIR, f"{scene}_{seed}_{px_w}x{px_h}.jpg")
    # Nom DISTINCT pour le repli procedural : il ne doit jamais faire passer
    # `os.path.exists(path)` (ci-dessus) a True a la place d'une vraie photo —
    # cf. docstring de la fonction pour le defaut que ce nom distinct ferme.
    path_repli = os.path.join(IMG_DIR, f"{scene}_{seed}_{px_w}x{px_h}_repli.jpg")
    path_a_poser = path
    if not _image_cache_valide(path):
        requete = _REQUETES_PHOTO.get(scene, scene)
        aspect_ratio = "wide" if aspect > 1.15 else "tall" if aspect < 0.85 else "square"
        brut = os.path.join(IMG_DIR, f"_brut_{scene}_{seed}.jpg")
        # Try restreint au seul appel réseau (constat R1, audit VSCode3
        # 2026-09-23) : une erreur d'import ou d'encodage ne doit plus être
        # rapportée « Openverse indisponible » — imports sortis en tête de
        # module, ré-encodage traité dans un second try au message distinct.
        try:
            stock_images.fetch_to(brut, requete, seed=seed, aspect_ratio=aspect_ratio,
                                   manifest_path=IMG_MANIFEST)
        except Exception as e:
            repli = _SCENE_REPLI.get(scene, scene)
            note = f" (scène '{scene}' inconnue du repli -> '{repli}')" if repli != scene else ""
            print(f"  Openverse indisponible pour '{scene}' ({e}) — repli sur nature_images{note}")
            try:
                nature_images.generate_to(path_repli, repli, px_w, px_h, seed=seed)
                path_a_poser = path_repli
            except Exception as e2:
                # Degrader, jamais planter : la slide sort sans photo et le
                # defaut remonte dans `problemes`, il ne disparait pas.
                msg = f"aucune image pour '{scene}' : Openverse KO ({e}) et repli KO ({e2})"
                print(f"  {msg}")
                _ANOMALIES_BUILD.append(msg)
                return
        else:
            try:
                cover_crop_to_aspect(brut, path, aspect)
                # cover_crop_to_aspect() sauve avec les défauts PIL (JPEG
                # qualité 75) : ré-encodage local à qualité 90 pour un rendu
                # plein cadre sur un deck client — le gain de poids vient de
                # PNG->JPEG, pas d'une compression agressive en plus.
                _PILImage.open(path).convert("RGB").save(path, quality=90, optimize=True)
                # Constat S1 : contenu tiers Openverse non validé avant usage
                # dans un livrable client — valider le fichier téléchargé
                # (format image décodable, dimensions bornées) avant de le
                # poser. Un fichier retenu invalide ne doit pas rester en
                # cache pour le build suivant (constat R2).
                if not _image_cache_valide(path):
                    raise ValueError(f"image Openverse invalide pour '{scene}' ({path})")
                print(f"  photo réelle posée pour '{scene}' ({requete!r}, via Openverse CC0)")
                path_a_poser = path
            except Exception as e:
                if os.path.exists(path):
                    os.remove(path)
                repli = _SCENE_REPLI.get(scene, scene)
                note = f" (scène '{scene}' inconnue du repli -> '{repli}')" if repli != scene else ""
                print(f"  image Openverse illisible pour '{scene}' ({e}) — repli sur nature_images{note}")
                try:
                    nature_images.generate_to(path_repli, repli, px_w, px_h, seed=seed)
                    path_a_poser = path_repli
                except Exception as e2:
                    msg = f"aucune image pour '{scene}' : encodage/validation KO ({e}) et repli KO ({e2})"
                    print(f"  {msg}")
                    _ANOMALIES_BUILD.append(msg)
                    return
    place_image_in_frame(slide, path_a_poser, left, top, width, height, geom=geom)



# v2.45 : photo « pour aérer » (demande utilisateur), et UNIQUEMENT une photo
# réelle libre de droit (« pas d'image générée ») : on recadre un brut Openverse
# CC0 DÉJÀ en cache (source et licence dans images-manifest.json), sans appel
# réseau ni repli procédural. Brut absent = pas d'image, jamais un substitut.
# Cadre : le prstGeom round2DiagRect CLONÉ du layout « cadre blanc » du
# gabarit (méthode pptx-framed-image), pas d'arrondi fait dans PIL.
def _photo_libre(slide, scene, seed, x, y, w, h):
    brut = os.path.join(IMG_DIR, f"_brut_{scene}_{seed}.jpg")
    if not _image_cache_valide(brut):
        print(f"  pas de photo réelle en cache pour '{scene}' — slide laissée sans image")
        return None
    layout = slide.slide_layout.slide_master.slide_layouts[LAYOUT_VISUEL_DROITE]
    cadre = _find_frame_in_group(layout.shapes, "Google Shape;212;p17", "Google Shape;213;p17")
    geom = cadre[4] if cadre else None
    aspect = w / h
    px_w = 960
    out = os.path.join(IMG_DIR, f"{scene}_{seed}_libre_{px_w}x{int(round(px_w / aspect))}.jpg")
    if not _image_cache_valide(out):
        cover_crop_to_aspect(brut, out, aspect)
        _PILImage.open(out).convert("RGB").save(out, quality=90, optimize=True)
    return place_image_in_frame(slide, out, Inches(x), Inches(y), Inches(w), Inches(h), geom=geom)
