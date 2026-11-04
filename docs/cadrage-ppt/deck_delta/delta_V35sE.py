"""Delta V35sE (base V34 + lot g) : « Conviction 11 » = evaluer en continu le service vecu, le mesurer et le montrer.

Demande : « piloter le service vecu ou evaluer le service mis a disposition en continu en le montrant regulierement ou le mesurant ».
- titre : « Conviction 11 : evaluer en continu le service vecu, le mesurer et le montrer » ;
- une boucle « Mesurer » <-> « Montrer » (pictogramme de cycle + « en continu ») au-dessus du contraste SLA / service vecu ;
- le tableau a trois colonnes (SLA / ce que vit le consommateur / ce que nous suivons) est conserve en compact, les trois lignes d'exemple intactes ;
- critere observable : plus de T0 / T1 (« avant puis apres », « en continu ») ; chantier inchange.
Pictogramme, pastille « CONVICTION 11 », points de progression, filet, navigation et pied de slide ne sont pas touches (seule la zone x >= 189, y 96..268 est redessinee).
Usage (depuis docs/cadrage-ppt/) : py deck_delta/deck.py delta_V35sE --base C:/tmp/deck-v35/V35g.pptx --sortie C:/tmp/deck-v35-sE/V35sE.pptx --sans-rendu
"""
import deck_base
import deck_draw
from forme_v9 import BLANC, CYAN, NAVY, PANEL, S, carte_diag, forme, tx
from pptx import Presentation
from pptx.enum.text import MSO_ANCHOR as A
from pptx.enum.text import PP_ALIGN as P

BASE = "V34"
NOTE = "V35sE : conviction 11 = evaluer en continu le service vecu (mesurer et montrer), contraste SLA / experience conserve en compact"
OPS = []

NB = "\u00a0"
T_ANCIEN = "Conviction 11" + NB + ": piloter le service vécu, pas seulement le SLA"
T_NOUVEAU = "Conviction 11" + NB + ": évaluer en continu le service vécu, le mesurer et le montrer"

CRITERE = "Écart entre SLA et expérience mesuré avant puis après ; part de RUN subi suivie en continu."
MESURER = ("Mesurer", "l'écart entre le SLA et le service vécu")
MONTRER = ("Montrer", "à rythme régulier, les écarts et la charge de RUN")
EN_TETE = ("Ce que mesure le SLA", "Ce que vit le consommateur", "Ce que nous suivons")
LIGNES = [
    ("Disponibilité du service", "Une demande qui attend, même quand le service est « vert »", "Objectif de service publié par capacité"),
    ("Incidents clos dans le délai", "Le même incident qui revient", "Taux d'incidents récurrents"),
    ("Tickets traités", "Du temps passé à subir plutôt qu'à améliorer", "Part de RUN subi et maîtrisé"),
]
COLS = ((200, 118), (328, 172), (512, 143))  # (x, largeur) des trois colonnes


def _slide(prs):
    trouvees = [s for s in prs.slides if s.shapes.title is not None and s.shapes.title.text.startswith("Conviction 11")]
    if len(trouvees) != 1:
        raise ValueError(f"Conviction 11 : {len(trouvees)} slide(s) ; 1 exigee")
    return trouvees[0]


def _run(sh, texte):
    runs = sh.text_frame.paragraphs[0].runs
    runs[0].text = texte
    for r in runs[1:]:
        r._r.getparent().remove(r._r)


def _vider_corps(s):
    """Retire la zone de contenu (x >= 189, 96 <= y < 268) : l'ancien tableau. Pictogramme (x < 189), pied (y >= 268), points (y = 70) et navigation restent."""
    for sh in list(s.shapes):
        if sh.is_placeholder or sh.name.startswith("nav-"):
            continue
        if sh.left >= 189 * 12700 and 96 * 12700 <= sh.top < 268 * 12700:
            sh._element.getparent().remove(sh._element)


def _carte_etape(s, x, y, w, h, nom, sous, accent):
    carte = carte_diag(s, x, y, w, h, adj=0.14)
    if accent:
        carte.fill.solid()
        carte.fill.fore_color.rgb = NAVY
    col = BLANC if accent else NAVY
    tx(s, x + 12, y + 4, w - 24, 17, [[(nom, 13, True, col)]], A.MIDDLE)
    tx(s, x + 12, y + 22, w - 24, 26, [[(sous, 10.5, False, col)]], A.TOP)


def conviction11(prs):
    s = _slide(prs)
    ancien_titre = s.shapes.title.text
    ancien_critere = ""
    for sh in s.shapes:
        if sh.has_text_frame and sh.text_frame.text.startswith("Écart entre SLA"):
            ancien_critere = sh.text_frame.text
            _run(sh, CRITERE)
    if not ancien_critere:
        raise ValueError("critere observable introuvable")
    _run(s.shapes.title, T_NOUVEAU)
    _vider_corps(s)
    # boucle : Mesurer <-> Montrer, en continu
    _carte_etape(s, 190, 96, 200, 52, *MESURER, accent=True)
    _carte_etape(s, 459, 96, 200, 52, *MONTRER, accent=False)
    forme(s, S.OVAL, 404.5, 96, 40, 40, BLANC, NAVY, lw=1.25)
    for rot in (0, 180):  # deux demi-fleches circulaires : le symbole classique de la boucle
        fl = forme(s, S.CIRCULAR_ARROW, 410.5, 102, 28, 28, CYAN, NAVY, lw=1)
        fl.rotation = rot
    tx(s, 390, 137, 69, 13, [[("en continu", 10, True, NAVY)]], A.MIDDLE, P.CENTER)
    # contraste compact SLA / service vecu
    forme(s, S.ROUNDED_RECTANGLE, 190, 155, 469, 20, CYAN, None, adj=0.5)
    for (x, w), titre in zip(COLS, EN_TETE, strict=True):
        tx(s, x, 155, w, 20, [[(titre, 10.5, True, NAVY)]], A.MIDDLE)
    for k, ligne in enumerate(LIGNES):
        y = 178 + k * 28.5
        if k % 2 == 0:
            forme(s, S.RECTANGLE, 190, y, 469, 28.5, PANEL, None)
        for j, ((x, w), texte) in enumerate(zip(COLS, ligne, strict=True)):
            tx(s, x, y, w, 28.5, [[(texte, 10.5, j == 2, NAVY)]], A.MIDDLE)
    s.notes_slide.notes_text_frame.text = (
        "Ancien titre" + NB + ": « " + ancien_titre + " »" + NB + "; le nouveau dit l'idée (évaluer en continu le service réellement vécu, par la mesure et par la restitution régulière). "
        "En-tête retiré de la slide" + NB + ": « Ce que nous suivons, avant → après » (le suivi avant puis après est porté par le critère observable). "
        "Critère observable d'origine" + NB + ": « " + ancien_critere + " »."
    )


def _id():
    prs = Presentation(deck_base.resoudre_base(BASE))
    return f"id:{deck_draw.slide_par_titre(prs, T_ANCIEN).slide_id}"


ETAPES = [
    {"declarer": [_id()], "f": conviction11, "nouvelles_max": 0, "nom": "conviction 11 : evaluer en continu, mesurer et montrer"},
]
