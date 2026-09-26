"""Le livrable principal du deck ne doit jamais disparaitre d'un commit.

Constat du 2026-09-24 : le commit de design 6408bc5 a supprime
docs/cadrage-ppt/bmad-iap-cadrage-synthese.pptx (4 482 428 -> 0 octet), retabli seulement
par b28baea. Un deck vide ou absent fait desormais passer la suite au rouge.

Depuis le 2026-09-26 le livrable est le deck « Offre Infra as a Product »
(generate_offre.py) ; l'ancien bmad-iap-cadrage-synthese.pptx est archive.
"""
import os
import zipfile

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIVRABLE = os.path.join(RACINE, "docs", "cadrage-ppt", "offre-infra-as-a-product-V1.pptx")


def test_livrable_present_et_lisible():
    assert os.path.isfile(LIVRABLE), f"livrable absent : {LIVRABLE}"
    assert os.path.getsize(LIVRABLE) > 1_000_000, "livrable anormalement petit"
    with zipfile.ZipFile(LIVRABLE) as z:
        slides = [n for n in z.namelist() if n.startswith("ppt/slides/slide")]
    assert len(slides) >= 10, f"{len(slides)} slide(s) seulement"
