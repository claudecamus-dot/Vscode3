"""Rendu PNG des slides modifiees par PowerPoint (COM, Windows) : repli quand LibreOffice est muet (WinError 6 en sandbox).

Ouverture en LECTURE SEULE, sans fenetre ; la presentation est fermee, l'application PowerPoint n'est jamais quittee (elle peut servir a l'utilisateur).
"""
import ctypes
import os


def _chemin_long(chemin):
    tampon = ctypes.create_unicode_buffer(1024)
    ctypes.windll.kernel32.GetLongPathNameW(os.path.abspath(chemin), tampon, 1024)
    return os.path.normpath(tampon.value or os.path.abspath(chemin))


def rendre(pptx, rangs, dossier, largeur=1280, hauteur=720):
    """PNG `slide_<rang>.png` (rang 1-base) des slides `rangs` ; renvoie les chemins. Leve si PowerPoint est indisponible (l'appelant se replie)."""
    import win32com.client
    os.makedirs(dossier, exist_ok=True)
    dossier = _chemin_long(dossier)
    app = win32com.client.Dispatch("PowerPoint.Application")
    pres = app.Presentations.Open(_chemin_long(pptx), True, False, False)
    sorties = []
    try:
        for rang in rangs:
            sortie = os.path.join(dossier, f"slide_{rang:02d}.png")
            pres.Slides(rang).Export(sortie, "PNG", largeur, hauteur)
            sorties.append(sortie)
    finally:
        pres.Close()
    return sorties
