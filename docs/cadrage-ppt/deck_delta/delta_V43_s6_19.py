"""Delta V43 (base V42) : alleger la slide 6 « Infra as a Product » en la scindant en deux slides.

- Slide A (titre inchange) : phrase d'accroche + AVANT / APRES (4 pilules, 4 cartes), re-etalees sur la hauteur utile ;
- Slide B (nouvelle, juste apres) : GAIN SUR LE RUN, RUN et la frise EXEMPLE, textes inchanges, re-etales.
Slide 19 (Conviction 13) : volontairement NON scindee. Elle ferme une serie de 13 convictions numerotee (reperes a 13 pastilles) ;
la scinder casserait la numerotation, et son rendu (5 lignes de 2 phrases courtes) tient sans debordement.
Aucun texte supprime ni reformule ; le titre de B est le seul texte nouveau.
Usage (depuis docs/cadrage-ppt/) : py deck_delta/deck.py delta_V43_s6_19 --base V42 --sortie C:/tmp/deck-v43-s619/V43s619.pptx --sans-rendu
"""
import deck_base
import deck_draw
from forme_v9 import par_id
from pptx import Presentation
from pptx.util import Pt

BASE = "V42"
NOTE = "V43 : slide 6 scindee en deux (AVANT/APRES ; gain sur le run, RUN et exemple)"
OPS = []

T6 = "Infra as a Product : des capacités pensées pour leurs consommateurs"
T6B = "Infra as a Product : le gain sur le run, le RUN et un exemple"
IDS_A_ET_ENTETE = set(range(41, 90))   # accroche, AVANT, APRES (ids de V42)
IDS_B = set(range(90, 112))            # gain, RUN, exemple


def _bloc(s, ids, conteneur, Y, H=None, police=1.0, centre=False):
    """Deplace `ids` comme un bloc rigide : le haut du conteneur va en Y ; si H est donne le conteneur prend la hauteur H (le reste garde sa taille,
    recentre verticalement si `centre`). Les pictos ne sont jamais etires. Polices x police (demi-points)."""
    cont = [sh for sh in s.shapes if sh.shape_id == conteneur][0]
    y0, h0 = cont.top / 12700, cont.height / 12700
    dec = (H - h0) / 2 if (centre and H) else 0
    for sh in s.shapes:
        if sh.shape_id not in ids:
            continue
        sh.top = int((Y + (sh.top / 12700 - y0) + dec) * 12700)
        if police != 1.0 and sh.has_text_frame:
            for p in sh.text_frame.paragraphs:
                for r in p.runs:
                    if r.font.size:
                        r.font.size = Pt(round(r.font.size.pt * police * 2) / 2)
    if H:
        cont.top, cont.height = int(Y * 12700), int(H * 12700)


def _retirer(s, ids):
    for sh in list(s.shapes):
        if sh.shape_id in ids:
            sh._element.getparent().remove(sh._element)


def _id(t):
    prs = Presentation(deck_base.resoudre_base(BASE))
    return [f"id:{deck_draw.slide_par_titre(prs, t).slide_id}"]


def scinder(prs):
    s = deck_draw.slide_par_titre(prs, T6)
    b = deck_draw.ajouter_sur_gabarit(deck_base.core(), prs, T6, {T6: T6B})
    ext = deck_draw._sections(prs)
    if ext is not None:
        deck_draw._placer_dans_section(ext, deck_draw.id_de(prs, s), deck_draw.id_de(prs, b))
    _retirer(b, IDS_A_ET_ENTETE)
    _retirer(s, IDS_B)
    # A : la colonne AVANT (pilules reparties), les 4 cartes APRES en grille 2x2 sur 96..372
    _bloc(s, set(range(47, 58)), 47, 112, 258)
    d = {sh.shape_id: sh for sh in s.shapes}
    for k, (fond, tx) in enumerate(((49, 50), (51, 52), (53, 54), (55, 56))):
        for i in (fond, tx):
            d[i].top, d[i].height = int((160 + 52 * k) * 12700), int(40 * 12700)
    d[57].top = int((112 + 129 - 10) * 12700)
    for cid, ids, Y in ((58, range(58, 66), 112), (66, range(66, 76), 112), (76, range(76, 83), 245), (83, range(83, 90), 245)):
        _bloc(s, set(ids), cid, Y, 128, centre=True)
    # B : gain sur le run + RUN (cartes plus hautes, contenu centre), puis frise exemple (pilules plus hautes)
    _bloc(b, set(range(90, 98)), 90, 100, 90, centre=True)
    _bloc(b, set(range(98, 102)), 98, 100, 90, centre=True)
    _bloc(b, set(range(102, 112)), 102, 215, 140)
    d = {sh.shape_id: sh for sh in b.shapes}
    d[103].top = int(230 * 12700)
    for i in (104, 105, 107, 108, 110, 111):
        d[i].top, d[i].height = int(268 * 12700), int(56 * 12700)
    for i in (106, 109):
        d[i].top = int(288 * 12700)


ETAPES = [{"declarer": _id(T6), "f": scinder, "nouvelles_max": 1, "nom": "6 : scission en deux slides"}]
