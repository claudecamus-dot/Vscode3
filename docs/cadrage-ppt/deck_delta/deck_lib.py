"""Utilitaires minimaux partages (reduction de Vscode8 `scripts/deck_lib.py`, gele la-bas).

Ne sont portes que `plat` et `titre`, requis par deck_rapport et deck_draw. Non portes : `clone_slide` (depend de `copie_rels_slide`, absent ici ;
le core fournit `copier_slide`), `snapshot`/`run_delta` a triplets (remplaces par le core), `delete_slide`/`move_slide`/`garder_rangs` (idem, via les ops du core).
"""
import re

plat = lambda t: re.sub(r"\s+", " ", t.replace("\xa0", " ").replace("\x0b", " ")).strip()  # noqa: E731


def titre(slide):
    """Texte du placeholder titre, aplati ; « » s'il n'y en a pas."""
    return plat(slide.shapes.title.text_frame.text) if slide.shapes.title is not None else ""
