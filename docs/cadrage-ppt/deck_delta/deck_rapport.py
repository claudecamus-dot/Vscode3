"""Rapport d'un delta applique : ce que l'utilisateur doit voir (port de Vscode8 `scripts/deck_rapport.py`, inchange hors cette ligne).

Exigences de visibilite : titres COMPLETS (le rapport de deck_lib.run_delta tronquait a 60 caracteres), texte avant/apres par slide modifiee, slides ajoutees / retirees / reordonnees,
duree par etape, et un STATUT qui ne dit jamais « valide » : « 0 defaut » des gardes automatiques n'est pas un rendu regarde (deux defauts de texte rogne n'ont ete vus que par le rendu image).
Ce module ne modifie rien : il formate.
"""
import difflib

from deck_lib import plat

MAX_LIGNES = 6  # lignes avant/apres montrees par slide


def titre_slide(slide):
    """Titre complet : placeholder titre, sinon premiere forme texte non vide."""
    if slide.shapes.title is not None and plat(slide.shapes.title.text_frame.text):
        return plat(slide.shapes.title.text_frame.text)
    return next((plat(sh.text_frame.text) for sh in slide.shapes if sh.has_text_frame and plat(sh.text_frame.text)), "(sans texte)")


def textes(slide):
    return [plat(sh.text_frame.text) for sh in slide.shapes if sh.has_text_frame and plat(sh.text_frame.text)]


def diff_textes(avant, apres):
    """[(« - » ou « + », texte)] des lignes qui different entre deux slides (liste de textes de formes, dans l'ordre)."""
    a, b = textes(avant), textes(apres)
    sortie = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b).get_opcodes():
        if op != "equal":
            sortie += [("-", t) for t in a[i1:i2]] + [("+", t) for t in b[j1:j2]]
    return sortie


def statut(pngs, sans_rendu=False):
    """Jamais « OK » ni « valide » : le delta est produit ; le rendu image des slides modifiees doit etre REGARDE par quelqu'un."""
    if pngs:
        return "RENDU PRODUIT — À REGARDER : " + ", ".join(pngs)
    raison = "rendu demande a etre saute" if sans_rendu else "aucun rendu image produit"
    return f"NON REGARDÉ : {raison} ; ne pas livrer sans avoir regarde les slides modifiees"


def lignes(base, sortie, note, avant_prs, apres_prs, constat, controles, durees, pngs, sans_rendu, simulation=False, extras=()):
    """Le rapport, une chaine par ligne. `constat` vient de deck_garde.simuler ; `controles` : [(nom, resultat)] ; `durees` : {etape: secondes}."""
    avant = {sl.slide_id: sl for sl in avant_prs.slides}
    apres = {sl.slide_id: sl for sl in apres_prs.slides}
    rang = {sl.slide_id: i for i, sl in enumerate(apres_prs.slides, 1)}
    out = [f"Base   : {base}", f"Sortie : {sortie}" + ("  (SIMULATION : rien n'est ecrit)" if simulation else "")]
    if note:
        out.append(f"Note   : {note}")
    touchees = sorted(constat["touchees"], key=lambda i: rang[i])
    out.append(f"Slides modifiees ({len(touchees)}) :")
    for sid in touchees:
        out.append(f"  slide {rang[sid]} — {titre_slide(apres[sid])}")
        diff = diff_textes(avant[sid], apres[sid])
        for signe, t in diff[:MAX_LIGNES]:
            out.append(f"      {signe} {t}")
        if len(diff) > MAX_LIGNES:
            out.append(f"      … (+{len(diff) - MAX_LIGNES} ligne(s))")
        if not diff:
            out.append("      (texte identique : changement de forme, de position ou de style)")
    for sid in sorted(constat["ajoutees"], key=lambda i: rang[i]):
        out.append(f"Slide AJOUTEE  : slide {rang[sid]} — {titre_slide(apres[sid])}")
    for sid in sorted(constat["supprimees"]):
        out.append(f"Slide RETIREE  : {titre_slide(avant[sid])}")
    if constat["ordre_modifie"]:
        out.append("Ordre des slides MODIFIE")
    inchangees = len(constat["apres"]) - len(touchees) - len(constat["ajoutees"])
    out.append(f"Slides non touchees : {inchangees} (empreinte identique)")
    out.extend(extras)
    for nom, resultat in controles:
        out.append(f"Controle {nom} : {resultat}")
    out.append("Durees : " + ", ".join(f"{k} {v:.1f} s" for k, v in durees.items()))
    out.append("STATUT : " + (statut(pngs, sans_rendu) if not simulation else "SIMULATION : rien n'est ecrit, rien n'est a regarder"))
    return out
