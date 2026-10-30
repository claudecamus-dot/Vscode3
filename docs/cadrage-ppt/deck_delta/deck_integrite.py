"""Controle d'integrite d'un .pptx que PowerPoint refuse alors que LibreOffice le tolere (port tel quel de Vscode8 `scripts/integrite_projet.py`).

Verifie dans le zip : cibles de relations internes presentes, rId referencees par une slide mais absentes de ses relations,
relId des diagrammes (SmartArt) resolus, doublons de slides, coherence des sections de navigation (p14:sectionLst).
Renomme `deck_integrite` (Vscode8 : `integrite_projet`).
Usage : py deck_integrite.py deck.pptx   (exit 0 = OK, 1 = probleme)
"""
import posixpath
import re
import sys
import zipfile

from lxml import etree

R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
NS = {"p": "http://schemas.openxmlformats.org/presentationml/2006/main",
      "p14": "http://schemas.microsoft.com/office/powerpoint/2010/main"}


def controler(chemin):
    """Liste de problemes (str) ; vide si le fichier est sain."""
    z = zipfile.ZipFile(chemin)
    noms = set(z.namelist())
    pb = []
    if len(noms) != len(z.namelist()):
        pb.append("parties en doublon dans le zip")
    for n in sorted(noms):
        if not n.endswith(".rels"):
            continue
        base = posixpath.dirname(posixpath.dirname(n))
        for r in etree.fromstring(z.read(n)):
            if r.get("TargetMode") == "External":
                continue
            t = r.get("Target")
            cible = t.lstrip("/") if t.startswith("/") else posixpath.normpath(posixpath.join(base, t))
            if cible not in noms:
                pb.append(f"{n}: cible absente {t}")
    for n in sorted(noms):
        if re.fullmatch(r"ppt/slides/slide\d+\.xml", n):
            rels = etree.fromstring(z.read(posixpath.dirname(n) + "/_rels/" + posixpath.basename(n) + ".rels"))
            ids = {r.get("Id") for r in rels}
            for e in etree.fromstring(z.read(n)).iter():
                for k, v in e.attrib.items():
                    if k.startswith(R) and v not in ids:
                        pb.append(f"{n}: rId orphelin {v}")
    # SmartArt : les relId du modele de donnees doivent exister dans les relations de la slide qui le porte
    for n in sorted(noms):
        if re.fullmatch(r"ppt/slides/slide\d+\.xml", n):
            rels = {r.get("Id") for r in etree.fromstring(z.read(posixpath.dirname(n) + "/_rels/" + posixpath.basename(n) + ".rels"))}
            for m in re.finditer(rb'<dgm:relIds[^>]*>', z.read(n)):
                for v in re.findall(rb'r:(?:dm|lo|qs|cs)="([^"]+)"', m.group(0)):
                    if v.decode() not in rels:
                        pb.append(f"{n}: relation de diagramme absente {v.decode()}")
    pres = etree.fromstring(z.read("ppt/presentation.xml"))
    ids = [e.get("id") for e in pres.findall(".//p:sldId", NS)]
    sec = [e.get("id") for e in pres.findall(".//p14:sldId", NS)]
    if len(ids) != len(set(ids)):
        pb.append("identifiants de slides en doublon")
    if sec:
        if set(sec) - set(ids):
            pb.append(f"sections: slides absentes du plan {sorted(set(sec) - set(ids))}")
        if set(ids) - set(sec):
            pb.append(f"sections: {len(set(ids) - set(sec))} slide(s) sans section")
        if len(sec) != len(set(sec)):
            pb.append("sections: slide(s) dans deux sections")
    return pb


if __name__ == "__main__":
    problemes = controler(sys.argv[1])
    for p in problemes:
        print("INTEGRITE", p, file=sys.stderr)
    print(f"deck_integrite : {len(problemes)} probleme(s)")
    sys.exit(1 if problemes else 0)
