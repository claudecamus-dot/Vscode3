"""Delta V21 (base V19) : retour utilisateur sur la V20 (2026-10-30) : « remets les intercalaires de chapitre + ameliore la forme des slides pour que ce soit plus joli ».

- reprend de la V20 l'ouverture en une slide et le bandeau numerote (« 03 · NOTRE APPROCHE · 2/3 »), mais GARDE les sept intercalaires de chapitre (la base est la V19, pas la V20) ;
- sections PowerPoint : une par chapitre, chaque intercalaire ouvre la sienne ;
- forme (relevee sur le rendu complet de la V20, planches de 12 slides) : les cartes a en-tete des convictions, des principes et du prochain pas laissaient la moitie basse vide
  avec un texte a 9,5 pt -> corps de carte grossi (x1,2) ; les deux slides « dix problemes » (cartes de 114 pt, mot long a ne pas couper) gardent leur corps mais les cartes sont
  raccourcies et surmontees d'une bande de lecture navy ; la colonne « votre demande » de l'ouverture (quart de carte vide) passe en texte plus grand.
Usage (depuis docs/cadrage-ppt/) : py deck_delta/deck.py delta_V21 --base V19
"""
import deck_base
import deck_draw
from delta_V20 import NUMEROS, P, _est_intercalaire, _nom_chapitre, bandeau, chapitre_de, ouverture  # noqa: F401
from lxml import etree
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR
from pptx.util import Pt
import uuid

BASE = "V19"
NOTE = "V21 : intercalaires conserves, ouverture en une slide, bandeau numerote, cartes grossies et bandes de lecture"
OPS = []

NAVY = RGBColor(0x0E, 0x23, 0x56)
T_CONV13 = "Une conviction, un critère, un chantier : 1 à 3"
T_CONV45 = "Une conviction, un critère, un chantier : 4 et 5"
T_PRINCIPES = "Trois principes de conduite : le service, l'adoption, le binôme"
T_PROCHAIN = "Prochain pas : choisir un périmètre, mesurer, tester, puis nous contacter"
T_PB1 = "Dix problèmes, dix apports, dix indicateurs : 1 à 5"
T_PB2 = "Dix problèmes, dix apports, dix indicateurs : 6 à 10"
T_OUVERTURE = "Votre demande, notre réponse en trois temps, nos engagements"
ANCIENNES_OUVERTURES = ("Notre engagement : quatre atouts pour passer du guichet au produit",
                        "Cinq points pour passer d'un guichet saturé à une Infra créatrice de valeur")


def _ids():
    prs = Presentation(deck_base.resoudre_base(BASE))
    sorties = [s.slide_id for s in prs.slides if s.shapes.title is not None and s.shapes.title.text_frame.text in ANCIENNES_OUVERTURES]
    return [f"id:{s.slide_id}" for s in prs.slides if s.slide_id not in sorties], sorties


_RESTANTES, _SUPPRIMEES = _ids()
OPS = [{"slide": f"id:{i}", "op": "supprimer"} for i in _SUPPRIMEES]


def _grossir(forme, facteur):
    for p in forme.text_frame.paragraphs:
        for r in p.runs:
            if r.font.size is not None:
                r.font.size = Pt(round(r.font.size.pt * facteur * 2) / 2)


def cartes_grossies(prs):
    for titre in (T_CONV13, T_CONV45, T_PRINCIPES, T_PROCHAIN):
        s = deck_draw.slide_par_titre(prs, titre)
        conviction = titre in (T_CONV13, T_CONV45)
        for sh in s.shapes:
            if sh.name == "texte-carte":
                _grossir(sh, 1.1 if conviction else 1.2)
            elif sh.name == "entete-carte" and conviction:
                _grossir(sh, 1.1)
            if conviction and sh.name in ("corps-carte", "texte-carte", "panneau-regle"):
                sh.height = int(sh.height + 18 * 12700)


def ouverture_texte(prs):
    s = deck_draw.slide_par_titre(prs, "En trois temps et trois engagements, votre Infra passe du guichet au produit")
    colonne = next(sh for sh in s.shapes if sh.has_text_frame and sh.text_frame.text.startswith("Sortir d'un guichet saturé"))
    _grossir(colonne, 1.25)


def problemes(prs):
    for titre in (T_PB1, T_PB2):
        s = deck_draw.slide_par_titre(prs, titre)
        for sh in s.shapes:
            if sh.name in ("corps-carte", "texte-carte"):
                sh.height = int(sh.height - 28 * 12700)
        bande = deck_draw.rect(s, 45, 322, 614, 34, NAVY, MSO_SHAPE.ROUNDED_RECTANGLE)
        bande.name = "bande-lecture"
        bande.adjustments[0] = 0.5
        tf = bande.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf.margin_left = tf.margin_right = Pt(16)
        r = tf.paragraphs[0].add_run()
        r.text = "Chaque problème est relié à un apport et à un indicateur, suivis au T0 et au T1."
        r.font.size, r.font.bold, r.font.name = Pt(11), True, "Outfit"
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)


def sections(prs):
    """Une section par chapitre : ouverture (jusqu'au sommaire), puis une section a chaque intercalaire (les slides du chapitre suivent)."""
    groupes = []
    for s in prs.slides:
        if _est_intercalaire(s):
            nom = _nom_chapitre(s) or "Chapitre"
        else:
            nom = chapitre_de(s) or (groupes[-1][0] if groupes else "Ouverture")
        if groupes and groupes[-1][0] == nom and not _est_intercalaire(s):
            groupes[-1][1].append(deck_draw.id_de(prs, s))
        else:
            groupes.append((nom, [deck_draw.id_de(prs, s)]))
    pres = prs.part._element
    ext_lst = pres.find(f"{P}extLst")
    if ext_lst is None:
        ext_lst = etree.SubElement(pres, f"{P}extLst")
    for ext in ext_lst.findall(f"{P}ext"):
        if ext.get("uri") == "{521415D9-36F7-43E2-AB2F-B90AF26B5E84}":
            ext_lst.remove(ext)
    ext = etree.SubElement(ext_lst, f"{P}ext", uri="{521415D9-36F7-43E2-AB2F-B90AF26B5E84}")
    liste = etree.SubElement(ext, f"{{{deck_draw.P14}}}sectionLst", nsmap={"p14": deck_draw.P14})
    for nom, ids in groupes:
        sec = etree.SubElement(liste, f"{{{deck_draw.P14}}}section", name=nom, id="{" + str(uuid.uuid4()).upper() + "}")
        sl = etree.SubElement(sec, f"{{{deck_draw.P14}}}sldIdLst")
        for i in ids:
            etree.SubElement(sl, f"{{{deck_draw.P14}}}sldId", id=i)


def retouche(prs):
    ouverture(prs)
    ouverture_texte(prs)
    cartes_grossies(prs)
    problemes(prs)
    bandeau(prs)
    sections(prs)


ETAPES = [{"declarer": _RESTANTES, "f": retouche, "nouvelles_max": 0, "nom": "ouverture, cartes grossies, bandes de lecture, bandeau, sections"}]
