"""Delta V6 (base V5) : retours utilisateur traitables par operations ciblees (R1, R4, R5, R7, R10).

Non traites ici (refonte de forme, pas des retouches) : slides 7, 8, 11, 13-15, 17, 18, typographie globale, formes arrondies et pictos.
Usage (depuis docs/cadrage-ppt/) : py deck_delta/deck.py delta_V6 --base V5 --dry-run   puis sans --dry-run.
"""
import re

import deck_draw

BASE = "V5"
NOTE = "V6 : interlocuteurs retires (R1), 2 slides de conviction (R4), intercalaire Notre approche aligne (R5), Demarche generale / detaillee (R7, R10)"

T2_ANCIEN = "Notre engagement : quatre atouts et des interlocuteurs identifiés"
T2 = "Notre engagement : quatre atouts pour passer du guichet au produit"
T_CONV = "Cinq convictions : une cible à construire et une démarche pour y conduire"
T_REUSSIR = "Réussir : cinq conditions que nous posons avant de commencer"
T_IA = "L'IA apporte au coach du temps et de la matière, pas la décision"
T_ATTENTES = "Ce que nous attendons de vous, et comment nous passons la main"
T_CALENDRIER = "Calendrier du pilote : étapes et jalons, durées à valider"
T_COMITES = "Deux comités en parallèle : l'un suit l'exécution, l'autre décide"
T_GOUV_IA = "L'IA est gouvernée : données, droits, validations et traçabilité"
EMU = 12700

OPS = []  # tout passe par ETAPES : les titres de `declarer` sont resolus AVANT les ops (un titre renomme par op serait introuvable)

# slide « modele » de chaque nouvelle conviction : 6 cartes (libelle | titre | lien avec la boucle) + carte « proposition »
CARTES_REUSSIR = [
    ("LA CONDITION", "Un sponsor qui arbitre", "dans la démarche : Prioriser"),
    ("LA CONDITION", "Un périmètre utile", "dans la démarche : Explorer"),
    ("LA CONDITION", "Une référence avant d'agir", "dans la démarche : Mesurer"),
    ("LA CONDITION", "Un relais côté client", "dans la démarche : Ancrer"),
    ("LA CONDITION", "Une IA cadrée d'abord", "dans la démarche : Comprendre"),
]
CARTES_IA = [
    ("L'APPORT", "Un diagnostic plus rapide", "dans la démarche : Comprendre"),
    ("L'APPORT", "Un tri assisté des demandes", "dans la démarche : Prioriser"),
    ("L'APPORT", "Une capitalisation continue", "dans la démarche : Ancrer"),
    ("L'APPORT", "Des mesures consolidées", "dans la démarche : Mesurer"),
    ("L'APPORT", "Des cas d'usage bornés", "dans la démarche : Explorer"),
]
# formes-cartes de la slide modele (rang dans spTree) : le texte porte 3 paragraphes
RANGS_CARTES = [6, 9, 12, 15, 18]


def _paragraphes(forme, textes):
    """Remplace le texte de chaque paragraphe (style du premier run conserve) ; refuse un nombre de paragraphes different."""
    paras = forme.text_frame.paragraphs
    if len(paras) != len(textes):
        raise ValueError(f"{len(paras)} paragraphes, {len(textes)} textes")
    for para, texte in zip(paras, textes, strict=True):
        runs = para.runs
        runs[0].text = texte
        for extra in runs[1:]:
            extra._r.getparent().remove(extra._r)


def _nouvelle_conviction(core, prs, apres_titre, titre, sous_titre, cartes, texte_prop, kicker):
    modele = deck_draw.slide_par_titre(prs, T_CONV)
    reference = deck_draw.slide_par_titre(prs, apres_titre)
    rang = list(prs.slides).index(reference)
    neuve = core.copier_slide(prs, modele, index=rang + 1)
    formes = list(neuve.shapes)
    deck_draw.set_run(formes[0], titre)
    deck_draw.set_run(formes[2], sous_titre)
    for idx, carte in zip(RANGS_CARTES, cartes, strict=True):
        _paragraphes(formes[idx], list(carte))
    deck_draw.set_run(formes[22], texte_prop)
    deck_draw.set_run(formes[23], kicker)
    return neuve


def conventions_nouvelles(prs):
    import deck_base
    core = deck_base.core()
    _nouvelle_conviction(core, prs, "Chaque conviction fonde un principe, un critère observable et un chantier", T_REUSSIR,
                         "Ce sont des choix de conduite, pas des promesses de résultat : à valider avec vous.", CARTES_REUSSIR,
                         "Ces conditions sont notre proposition, à valider avec vous.", "NOS CONVICTIONS · 3/4")
    _nouvelle_conviction(core, prs, T_REUSSIR, T_IA,
                         "L'IA prépare, nos coachs challengent, le client décide : chaque apport est borné et relu.", CARTES_IA,
                         "Gains à mesurer au T0 puis au T1 : aucun chiffre n'est promis.", "NOS CONVICTIONS · 4/4")
    # les deux kickers existants passent de x/2 a x/4
    for titre, valeur in ((T_CONV, "1/4"), ("Chaque conviction fonde un principe, un critère observable et un chantier", "2/4")):
        s = deck_draw.slide_par_titre(prs, titre)
        for sh in s.shapes:
            if sh.has_text_frame and sh.text_frame.text.startswith("NOS CONVICTIONS ·"):
                deck_draw.set_run(sh, f"NOS CONVICTIONS · {valeur}")


def interlocuteurs_et_intercalaire(prs):
    """R1 : retire la zone « VOS INTERLOCUTEURS » ; R5 : l'intercalaire Notre approche reprend le gabarit des autres intercalaires."""
    s2 = deck_draw.slide_par_titre(prs, T2_ANCIEN)
    deck_draw.set_run(s2.shapes.title, T2)
    a_retirer = [sh for sh in s2.shapes if sh.top >= 298 * EMU and sh.height < 60 * EMU and sh.name != "Title 1" and not (sh.has_text_frame and sh.text_frame.text.startswith("OUVERTURE"))]
    for sh in a_retirer:
        sh._element.getparent().remove(sh._element)
    modele = deck_draw.slide_par_titre(prs, "Nos convictions")
    s12 = deck_draw.slide_par_titre(prs, "Notre approche")
    rel = next(r for r in s12.part.rels.values() if r.reltype.endswith("/slideLayout"))
    rel._target = modele.slide_layout.part
    ph = {sh.placeholder_format.idx: sh for sh in s12.placeholders}
    for sh in list(s12.shapes):
        if sh.shape_type == 17:  # TEXT_BOX : le « 03 » decoratif de l'ancien gabarit
            sh._element.getparent().remove(sh._element)
    for sh in s12.shapes:
        for ref in modele.shapes:
            if ref.shape_type == sh.shape_type and (sh.is_placeholder == ref.is_placeholder):
                if sh.is_placeholder and sh.placeholder_format.type != ref.placeholder_format.type:
                    continue
                if sh.shape_type == 13:
                    sh.left, sh.top, sh.width, sh.height = ref.left, ref.top, ref.width, ref.height
                    import copy
                    ancienne = sh._element.spPr.find("{http://schemas.openxmlformats.org/drawingml/2006/main}prstGeom")
                    nouvelle = ref._element.spPr.find("{http://schemas.openxmlformats.org/drawingml/2006/main}prstGeom")
                    if ancienne is not None and nouvelle is not None:
                        ancienne.getparent().replace(ancienne, copy.deepcopy(nouvelle))
                else:
                    sh.left, sh.top, sh.width, sh.height = ref.left, ref.top, ref.width, ref.height
                break
    return ph


def demarche_generale_et_detaillee(prs):
    """R7, R10 : chapitre « Démarche générale » puis « Démarche détaillée » (calendrier, attentes et relais, comités, gouvernance IA)."""
    import deck_base
    core = deck_base.core()
    interc = deck_draw.slide_par_titre(prs, "Démarche")
    for sh in interc.shapes:
        if sh.has_text_frame and sh.text_frame.text == "Démarche":
            deck_draw.set_run(sh, "Démarche générale")
    agents = deck_draw.slide_par_titre(prs, "Des agents augmentent le coach ; d'autres améliorent l'Infra du client")
    rang = list(prs.slides).index(agents)
    neuve = core.copier_slide(prs, interc, index=rang + 1)
    for sh in neuve.shapes:
        if sh.has_text_frame and sh.text_frame.text == "Démarche générale":
            deck_draw.set_run(sh, "Démarche détaillée")
    ordre = [T_CALENDRIER, T_COMITES, T_ATTENTES, T_GOUV_IA]
    ref = neuve
    for titre in ordre:
        s = deck_draw.slide_par_titre(prs, titre)
        deck_draw.deplacer_apres(prs, s, ref)
        ref = s
    _renumeroter(prs)


def _renumeroter(prs):
    """Numero des intercalaires numerotes, puis x/n des bandeaux de chapitre pour les chapitres touches."""
    chapitre, contenu = None, {}
    ordre = []
    for s in prs.slides:
        if s.slide_layout.name.startswith(("50 -", "51 -")):
            chapitre = next((sh.text_frame.text for sh in s.shapes if sh.has_text_frame and sh.text_frame.text and not re.fullmatch(r"\d{2}|[A-Z]", sh.text_frame.text) and sh.is_placeholder and sh.top > 100 * EMU), None)
            ordre.append((chapitre, s))
            contenu[chapitre] = []
        elif chapitre:
            contenu[chapitre].append(s)
    numero = 0
    for nom, s in ordre:
        for sh in s.shapes:
            if sh.is_placeholder and sh.has_text_frame and re.fullmatch(r"\d{2}", sh.text_frame.text):
                if nom == "Annexes":
                    continue
                if nom != "Démarche détaillée":  # partage la pastille du chapitre general (7 pastilles dans le sommaire)
                    numero += 1
                if sh.text_frame.text != f"{numero:02d}":
                    deck_draw.set_run(sh, f"{numero:02d}")
    for nom in ("Démarche détaillée", "Dispositif et prix", "Démarche générale"):
        slides = contenu.get(nom, [])
        for i, s in enumerate(slides, 1):
            for sh in s.shapes:
                if sh.has_text_frame and re.match(r"^(DISPOSITIF ET PRIX|DÉMARCHE[A-ZÉ ]*) · \d+/\d+$", sh.text_frame.text):
                    voulu = f"{nom.upper()} · {i}/{len(slides)}"
                    if sh.text_frame.text != voulu:
                        deck_draw.set_run(sh, voulu)


def sommaire(prs):
    """Le gabarit n'a que 7 pastilles numerotees : « Démarche générale » et « Démarche détaillée » partagent la pastille 04."""
    s = deck_draw.slide_par_titre(prs, "Sommaire")
    cible = next(sh for sh in s.shapes if sh.has_text_frame and sh.text_frame.text == "Démarche")
    deck_draw.set_run(cible, "Démarche générale et détaillée")


ETAPES = [
    {"declarer": [T2_ANCIEN, "Notre approche"], "f": interlocuteurs_et_intercalaire, "nouvelles_max": 0, "nom": "R1 interlocuteurs, R5 intercalaire"},
    {"declarer": ["Chaque conviction fonde un principe, un critère observable et un chantier", T_CONV], "f": conventions_nouvelles, "nouvelles_max": 2, "nom": "R4 deux slides de conviction"},
    {"declarer": ["Une boucle continue pour décider sur des faits, expérimenter et ancrer", "Des agents augmentent le coach ; d'autres améliorent l'Infra du client", T_CALENDRIER, T_COMITES, T_ATTENTES, T_GOUV_IA, "Démarche", "Preuve", "Dispositif et prix", "Prochain pas",
                 "Un dispositif OCTO + client qui construit son propre relais", "Deux temps d'engagement : diagnostiquer, puis expérimenter et déployer",
                 "Chiffrage : la forme du tableau jours × rôles, toutes valeurs à valider", "Risques et objections : ce que nous répondons, ce que nous mesurons"], "f": demarche_generale_et_detaillee, "nouvelles_max": 1, "nom": "R7 R10 demarche generale et detaillee"},
    {"declarer": ["Sommaire"], "f": sommaire, "nouvelles_max": 0, "nom": "sommaire"},
]
