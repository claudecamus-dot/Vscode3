"""Le livrable principal du deck ne doit jamais disparaitre d'un commit.

Constat du 2026-09-24 : le commit de design 6408bc5 a supprime
docs/cadrage-ppt/bmad-iap-cadrage-synthese.pptx (4 482 428 -> 0 octet), retabli seulement
par b28baea. Un deck vide ou absent fait desormais passer la suite au rouge.

Depuis le 2026-09-26 le livrable est le deck « Offre Infra as a Product »
(generate_offre.py) ; l'ancien bmad-iap-cadrage-synthese.pptx est archive.
"""
import glob
import os
import re
import zipfile

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOSSIER = os.path.join(RACINE, "docs", "exports", "decks")


def _dernier_livrable():
    """Le livrable courant = la version la plus haute du dossier ; les anciennes versions partent en Archives/ (V1 deplace le 2026-10-30)."""
    versions = []
    for chemin in glob.glob(os.path.join(DOSSIER, "offre-infra-as-a-product-V*.pptx")):
        m = re.search(r"-V(\d+)\.pptx$", chemin)
        if m:
            versions.append((int(m.group(1)), chemin))
    return max(versions)[1] if versions else os.path.join(DOSSIER, "offre-infra-as-a-product-V1.pptx")


LIVRABLE = _dernier_livrable()


def test_livrable_present_et_lisible():
    assert os.path.isfile(LIVRABLE), f"livrable absent : {LIVRABLE}"
    assert os.path.getsize(LIVRABLE) > 1_000_000, "livrable anormalement petit"
    with zipfile.ZipFile(LIVRABLE) as z:
        slides = [n for n in z.namelist() if n.startswith("ppt/slides/slide")]
    assert len(slides) >= 10, f"{len(slides)} slide(s) seulement"
