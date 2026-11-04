"""Delta V37wB (base V36) : convictions 2 a 6 developpees en trois puces, sans les pilules « Boucle » ; deux mots de la grille des convictions.

- slide « Du besoin a la priorite » : enonce de la conviction 2 reecrit (besoins des utilisateurs, satisfaction mesuree), titre qui dit pourquoi les trois vont ensemble,
  pilules « Boucle » retirees, trois puces par conviction (tirees des notes : critere observable et chantier) ;
- slide « Valeur et gain de l'IA » : « progres » devient « valeur », pilules « Boucle » retirees, trois puces par conviction, legende des deux niveaux sous la conviction 5,
  « regle de passage » inchangee (carte navy plus etroite) ;
- grille des convictions : deux libelles (conviction 2 et conviction 5) ; rien d'autre.
Les phrases retirees (anciens enonces, titres) vont dans les notes de chaque slide.
Usage (depuis docs/cadrage-ppt/) : py deck_delta/deck.py delta_V37wB --base V36 --sortie C:/tmp/deck-v37-wB/V37wB.pptx --sans-rendu
"""
import deck_base
import deck_draw
from forme_v9 import CYAN, NAVY, PANEL, S, carre_num_cyan, forme, restyle, tx
from forme_v9 import deplacer as mv
from pptx import Presentation
from pptx.enum.text import MSO_ANCHOR as A
from pptx.enum.text import MSO_AUTO_SIZE
from pptx.enum.text import PP_ALIGN as P
from pptx.util import Pt

BASE = "V36"
NOTE = "V37wB : convictions 2 a 6 en trois puces sans boucle, valeur a la place de progres, legende des niveaux, deux libelles de la grille"
OPS = []

NB = "\u00a0"
T_GRILLE = "Treize convictions couvrent toute la transformation de l'Infra"
T_C234_ANCIEN = "Du besoin à la priorité" + NB + ": douleur mesurée, porteur, faits d'abord"
T_C56_ANCIEN = "Progrès et gain de l'IA" + NB + ": mesurés puis vérifiés, jamais promis"
T_C234 = "Besoins mesurés, porteur nommé, priorités fondées sur des faits"
T_C56 = "Valeur et gain de l'IA" + NB + ": mesurés puis vérifiés, jamais promis"
TITRES_BASE = (T_GRILLE, T_C234_ANCIEN, T_C56_ANCIEN)

ENONCE_2 = "Une plateforme n'est adoptée que si elle répond aux besoins des utilisateurs" + NB + ": on le mesure par leur satisfaction."
ENONCE_5 = "La valeur se mesure de façon régulière et transparente, à chaque niveau."

# geometrie commune (points) : la carte monte de 16 pt, le disque du pictogramme passe de 68 a 60
CARTE_Y, CARTE_H = 118.0, 246.0
CENTRE_PICTO_Y, D_PICTO, D_ANCIEN = 112.0, 60.0, 68.0
PILULE_Y, PILULE_H = 150.0, 20.0
ENONCE_Y = 177.0
PAS_LIGNE = 13.4  # interligne d'une puce a 11 pt


def _d(s):
    return {sh.shape_id: sh for sh in s.shapes}


def _notes_ajout(s, texte):
    tf = s.notes_slide.notes_text_frame
    ancien = tf.text.strip()
    tf.text = (ancien + "\n\n" if ancien else "") + texte


def _suppr(d, ids):
    for i in ids:
        d[i]._element.getparent().remove(d[i]._element)


def _zone(sh, x=None, y=None, w=None, h=None, sz=None, align=None, ancre=None):
    mv(sh, x, y, w, h)
    tf = sh.text_frame
    tf.auto_size = MSO_AUTO_SIZE.SHAPE_TO_FIT_TEXT if ancre == A.TOP else MSO_AUTO_SIZE.NONE  # idiome V36 : texte ancre en haut, la boite epouse le texte
    tf.word_wrap = True
    if ancre is not None:
        tf.vertical_anchor = ancre
    for para in tf.paragraphs:
        if align is not None:
            para.alignment = align
        for r in para.runs:
            if sz is not None:
                r.font.size = Pt(sz)


def _echelle(s, ids, ancien_centre, nouveau_centre, k):
    d = _d(s)
    ox, oy = ancien_centre
    nx, ny = nouveau_centre
    for i in ids:
        sh = d[i]
        x, y, w, h = (v / 12700 for v in (sh.left, sh.top, sh.width, sh.height))
        mv(sh, x=nx + (x - ox) * k, y=ny + (y - oy) * k, w=w * k, h=h * k)


def _puces(s, x, y, w, items, sz=11):
    """items = [(texte, nombre de lignes)] : un point cyan a contour navy, puis le texte ; renvoie l'ordonnee de fin."""
    for texte, lignes in items:
        forme(s, S.OVAL, x, y + 3.2, 7, 7, CYAN, NAVY, lw=0.75)
        h = lignes * PAS_LIGNE
        tx(s, x + 14, y, w - 14, h, [[(texte, sz, False, NAVY)]], A.TOP, P.LEFT)
        y += h + 4
    return y


def _carte(s, d, x, w, carte, picto, disque, pastille, ptxt, enonce, texte_enonce=None, hauteur_enonce=70.0):
    cx = x + w / 2
    mv(d[carte], x=x, y=CARTE_Y, w=w, h=CARTE_H)
    restyle(d[carte], "roundRect", adj=0.11)
    ancien = ((d[disque].left + d[disque].width / 2) / 12700, (d[disque].top + d[disque].height / 2) / 12700)
    _echelle(s, (disque,) + picto, ancien, (cx, CENTRE_PICTO_Y), D_PICTO / D_ANCIEN)
    mv(d[pastille], x=cx - 60, y=PILULE_Y, w=120, h=PILULE_H)
    _zone(d[ptxt], x=cx - 60, y=PILULE_Y, w=120, h=PILULE_H, sz=11, align=P.CENTER, ancre=A.MIDDLE)
    _zone(d[enonce], x=x + 12, y=ENONCE_Y, w=w - 20, h=hauteur_enonce, sz=14, align=P.LEFT, ancre=A.TOP)
    if texte_enonce:
        d[enonce].text_frame.paragraphs[0].runs[0].text = texte_enonce
    # filet fin sous l'enonce
    ys = ENONCE_Y + hauteur_enonce + 3
    forme(s, S.RECTANGLE, x + 12, ys, w - 24, 0.75, NAVY)
    return ys + 6


# ================================================================ 9. Deux libelles de la grille
def grille(prs):
    s = deck_draw.slide_par_titre(prs, T_GRILLE)
    d = _d(s)
    r2 = d[103].text_frame.paragraphs[0].runs[0]
    r5 = d[136].text_frame.paragraphs[0].runs[0]
    a2, a5 = r2.text, r5.text
    r2.text = "Répondre aux besoins des utilisateurs"
    r5.text = "Valeur mesurée, régulière, transparente"
    mv(d[136], w=112)
    _notes_ajout(s, "Libellés modifiés (V37)" + NB + ": conviction 2 « " + a2 + " » devient « " + r2.text + " » ; "
                    "conviction 5 « " + a5 + " » devient « " + r5.text + " ».")


# ================================================================ 11. Convictions 2 a 4
def convictions_234(prs):
    s = deck_draw.slide_par_titre(prs, T_C234_ANCIEN)
    d = _d(s)
    ancien_enonce = d[106].text_frame.text
    ancien_titre = s.shapes.title.text_frame.text
    s.shapes.title.text_frame.paragraphs[0].runs[0].text = T_C234
    for r in s.shapes.title.text_frame.paragraphs[0].runs[1:]:
        r.text = ""
    W = 190.0
    cols = (
        (45.0, 100, (102, 103, 104, 105), 101, 107, 108, 106, ENONCE_2, 82.0,
         [("Besoins de chaque consommateur documentés", 2), ("Satisfaction des utilisateurs mesurée", 2), ("Interviews et situation de référence mesurée", 2)]),
        (257.0, 113, (115, 116, 117, 118, 119, 120), 114, 122, 123, 121, None, 82.0,
         [("Chaque capacité clé a un propriétaire nommé", 2), ("Une roadmap et un indicateur de valeur", 2), ("Désigner, bâtir la roadmap, définir l'indicateur", 2)]),
        (469.0, 128, tuple(range(130, 137)), 129, 138, 139, 137, None, 82.0,
         [("Une grille de priorisation partagée", 2), ("Elle alimente les arbitrages budgétaires", 2), ("Choisir les indicateurs, scorer, ritualiser la décision", 2)]),
    )
    suites = []
    for x, carte, picto, disque, pastille, ptxt, enonce, texte, h_en, puces in cols:
        y = _carte(s, d, x, W, carte, picto, disque, pastille, ptxt, enonce, texte, h_en)
        suites.append((x, y, puces))
    _suppr(d, [157, 158, 159, 160, 161, 162])  # pilules « Boucle »
    for x, y, puces in suites:
        _puces(s, x + 14, y, W - 26, puces)
    _notes_ajout(s, "Modifications V37" + NB + ":\n"
                    "Ancien titre : « " + ancien_titre + " » ; le nouveau dit pourquoi les trois convictions vont ensemble (besoin mesuré, porteur nommé, priorité sur des faits).\n"
                    "Ancien énoncé de la conviction 2 : « " + ancien_enonce + " » ; remplacé à la demande de l'utilisateur (répondre à des besoins utilisateurs, mesurer leur satisfaction).\n"
                    "Pilules « Boucle : Explorer / Ancrer / Prioriser » retirées de la slide (la boucle reste portée par la grille des convictions).\n"
                    "Les trois puces de chaque conviction reprennent, reformulées, le critère observable et le chantier ci-dessus.")


# ================================================================ 12. Convictions 5 et 6
def convictions_56(prs):
    s = deck_draw.slide_par_titre(prs, T_C56_ANCIEN)
    d = _d(s)
    ancien_enonce = d[104].text_frame.text
    ancien_titre = s.shapes.title.text_frame.text
    runs = s.shapes.title.text_frame.paragraphs[0].runs
    runs[0].text = T_C56
    for r in runs[1:]:
        r.text = ""
    w5, w6, wr = 236.0, 206.0, 140.0
    x5, x6, xr = 45.0, 45.0 + w5 + 16, 45.0 + w5 + 16 + w6 + 16
    y5 = _carte(s, d, x5, w5, 99, (101, 102, 103), 100, 105, 106, 104, ENONCE_5, 52.0)
    y6 = _carte(s, d, x6, w6, 111, (113, 114), 112, 116, 117, 115, None, 52.0)
    _suppr(d, [139, 140, 141, 142])  # pilules « Boucle »
    # conviction 5 : legende des deux niveaux (definis sur la slide « Nous mesurons la valeur client... »)
    forme(s, S.ROUNDED_RECTANGLE, x5 + 12, y5, w5 - 24, 50, PANEL, None, adj=0.14)
    tx(s, x5 + 22, y5 + 5, w5 - 44, 12, [[("À chaque niveau", 10, True, NAVY)]], A.TOP, P.LEFT)
    carre_num_cyan(s, x5 + 22, y5 + 19, 13, 1, 9.5)
    tx(s, x5 + 40, y5 + 19, w5 - 62, 13, [[("la valeur rendue au client", 11, False, NAVY)]], A.MIDDLE, P.LEFT)
    carre_num_cyan(s, x5 + 22, y5 + 34, 13, 2, 9.5)
    tx(s, x5 + 40, y5 + 34, w5 - 62, 13, [[("l'apport du coaching augmenté", 11, False, NAVY)]], A.MIDDLE, P.LEFT)
    _puces(s, x5 + 14, y5 + 58, w5 - 26, [("Indicateurs suivis à rythme régulier", 1), ("Succès comme erreurs, tous mesurés", 1), ("Rituel de revue" + NB + ": équipes redevables", 1)])
    _puces(s, x6 + 14, y6, w6 - 26, [("Gisements de temps perdu repérés", 2), ("Données utilisables autorisées", 1), ("Un cas d'usage borné, après contrôle de confidentialité", 3)])
    # regle de passage : meme texte, carte plus etroite
    mv(d[122], x=xr, y=CARTE_Y, w=wr, h=CARTE_H)
    mv(d[123], x=xr + 12, y=PILULE_Y, w=wr - 24, h=PILULE_H)
    _zone(d[124], x=xr + 12, y=PILULE_Y, w=wr - 24, h=PILULE_H, sz=11, align=P.CENTER, ancre=A.MIDDLE)
    _zone(d[125], x=xr + 14, y=ENONCE_Y, w=wr - 26, h=170, sz=12, align=P.LEFT, ancre=A.TOP)
    _notes_ajout(s, "Modifications V37" + NB + ":\n"
                    "Ancien titre : « " + ancien_titre + " » ; « progrès » devient « valeur » (demande de l'utilisateur).\n"
                    "Ancien énoncé de la conviction 5 : « " + ancien_enonce + " » ; « progrès » devient « valeur ».\n"
                    "Pilules « Boucle : Mesurer / Comprendre » retirées de la slide (la boucle reste portée par la grille des convictions).\n"
                    "Légende « À chaque niveau » : les deux niveaux sont ceux de la slide « Nous mesurons la valeur client et l'apport du coaching augmenté » (niveau 1 client, niveau 2 coaching augmenté).\n"
                    "Les trois puces de chaque conviction reprennent, reformulées, le critère observable et le chantier ci-dessus (« indicateurs de progrès » y devient « indicateurs de valeur »).")


def _ids():
    prs = Presentation(deck_base.resoudre_base(BASE))
    return [f"id:{deck_draw.slide_par_titre(prs, t).slide_id}" for t in TITRES_BASE]


_I = dict(zip(TITRES_BASE, _ids(), strict=True))
ETAPES = [
    {"declarer": [_I[T_GRILLE]], "f": grille, "nouvelles_max": 0, "nom": "grille : libelles des convictions 2 et 5"},
    {"declarer": [_I[T_C234_ANCIEN]], "f": convictions_234, "nouvelles_max": 0, "nom": "convictions 2 a 4 : trois puces, sans boucle"},
    {"declarer": [_I[T_C56_ANCIEN]], "f": convictions_56, "nouvelles_max": 0, "nom": "convictions 5 et 6 : valeur, trois puces, legende des niveaux"},
]
