"""Delta V37z (base V36) : slide « Du pilote à l'autonomie » : les trois lignes « Conduit par : … » disparaissent (trop naives).

- retire les trois lignes « Conduit par : OCTO et le client ensemble. / le client, OCTO en appui. / le client, avec ses relais. » et le filet qui les surmonte ;
- les cartes se raccourcissent (187 -> 170 pt), les pastilles d'etat (pilote / extension eventuelle / autonomie) remontent au bas de leur carte, la note « Modes de Team Topologies… » remonte d'autant ;
- le texte retire est conserve dans les notes de la slide.
Usage (depuis docs/cadrage-ppt/) : py deck_delta/deck.py delta_V37z --base V36 --sortie C:/tmp/deck-v37/V37z.pptx --sans-rendu
"""
import deck_base
from pptx import Presentation

BASE = "V36"
NOTE = "V37z : slide Du pilote a l'autonomie : lignes Conduit par retirees"
PREFIXE = "Du pilote à l'autonomie"
EMU_PT = 12700
HAUT_CARTE = 170 * EMU_PT
HAUT_PASTILLE = 282 * EMU_PT
HAUT_NOTE = 322 * EMU_PT
PASTILLES = ("pilote", "extension éventuelle", "autonomie")


def _texte(sh):
    return sh.text_frame.text if sh.has_text_frame else ""


def _slide(prs):
    s = [x for x in prs.slides if x.shapes.title is not None and _texte(x.shapes.title).startswith(PREFIXE)]
    if len(s) != 1:
        raise ValueError(f"{len(s)} slides « {PREFIXE}… »")
    return s[0]


def _ids():
    return [f"id:{_slide(Presentation(deck_base.resoudre_base(BASE))).slide_id}"]


def _retirer(sh):
    sh._element.getparent().remove(sh._element)


def conduit_par(prs):
    s = _slide(prs)
    lignes = [x for x in s.shapes if _texte(x).startswith("Conduit par")]
    if len(lignes) != 3:
        raise ValueError(f"{len(lignes)} lignes « Conduit par » au lieu de 3")
    retire = []
    for tb in lignes:
        retire.append(_texte(tb))
        for f in [x for x in s.shapes if x.shape_type == 1 and not _texte(x) and x.height <= 2 * EMU_PT and x.left == tb.left and 0 <= tb.top - x.top <= 8 * EMU_PT]:
            _retirer(f)
        _retirer(tb)
    cartes = [x for x in s.shapes if "Diagonal" in x.name and 175 * EMU_PT < x.height < 200 * EMU_PT]
    if len(cartes) != 3:
        raise ValueError(f"{len(cartes)} cartes au lieu de 3")
    for c in cartes:
        c.height = HAUT_CARTE
    nb = 0
    for tb in [x for x in s.shapes if _texte(x) in PASTILLES]:
        fond = next(x for x in s.shapes if x is not tb and x.shape_type == 1 and not _texte(x) and x.top == tb.top and x.left == tb.left and x.height == tb.height)
        tb.top = HAUT_PASTILLE
        fond.top = HAUT_PASTILLE
        nb += 1
    if nb != 3:
        raise ValueError(f"{nb} pastilles au lieu de 3")
    note = next(x for x in s.shapes if _texte(x).startswith("Modes de Team Topologies"))
    note.top = HAUT_NOTE
    ntf = s.notes_slide.notes_text_frame
    ntf.text = (ntf.text + "\n\n" if ntf.text else "") + "Lignes retirées de la slide (demande de supprimer « Conduit par », jugé trop naïf) : " + " | ".join(retire)


ETAPES = [{"declarer": _ids(), "f": conduit_par, "nouvelles_max": 0, "nom": "lignes Conduit par retirees, cartes raccourcies"}]
OPS = []
