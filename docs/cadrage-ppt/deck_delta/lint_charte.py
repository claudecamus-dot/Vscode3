"""Lint de charte : couleurs (srgbClr) et polices (a:latin/ea/cs) du deck contre `charte/tokens.json`.

Autorise : couleurs du THEME du deck (theme1.xml), `autorise_hex`, polices `autorise_polices` et references de theme (+mn-, +mj-).
Tolere (avertissement) : `tolere_hex` / `tolere_polices` = valeurs mesurees sur la V8, a arbitrer ([A VALIDER]).
Defaut (exit 1) : toute autre couleur ou police. Les couleurs en schemeClr suivent le theme et ne sont pas controlees.
Usage : py docs/cadrage-ppt/deck_delta/lint_charte.py deck.pptx
Port de Vscode8 `scripts/lint_charte.py` ; seuls le chemin des tokens et le texte des constats changent.
"""
import collections
import json
import os
import re
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
TOKENS = os.path.join(HERE, "..", "..", "..", "charte", "tokens.json")
PARTIES = re.compile(r"ppt/(slides|slideLayouts|slideMasters)/[^/]+\.xml")


def charger_tokens(chemin=TOKENS):
    with open(chemin, encoding="utf8") as f:
        return json.load(f)


def mesurer(chemin):
    """(couleurs hex en majuscules, polices, couleurs du theme) : Counters/ensemble sur slides, mises en page et masques."""
    z = zipfile.ZipFile(chemin)
    hexa, polices, theme = collections.Counter(), collections.Counter(), set()
    for n in z.namelist():
        if re.fullmatch(r"ppt/theme/theme\d+\.xml", n):
            d = z.read(n).decode("utf8")
            theme |= {v.upper() for v in re.findall(r'<a:(?:dk1|lt1|dk2|lt2|accent\d|hlink|folHlink)>\s*<a:(?:srgbClr val|sysClr val="[^"]*" lastClr)="([0-9A-Fa-f]{6})"', d)}
        elif PARTIES.fullmatch(n):
            d = z.read(n).decode("utf8")
            hexa.update(v.upper() for v in re.findall(r'srgbClr val="([0-9A-Fa-f]{6})"', d))
            polices.update(re.findall(r'<a:(?:latin|ea|cs) typeface="([^"]*)"', d))
    return hexa, polices, theme


def controler(chemin, tokens=None):
    """(defauts, avertissements) : listes de str."""
    t = tokens or charger_tokens()
    hexa, polices, theme = mesurer(chemin)
    ok_hex = theme | {h.upper() for h in t["autorise_hex"]}
    tol_hex = {h.upper() for h in t["tolere_hex"]}
    defauts, avert = [], []
    for h, n in sorted(hexa.items()):
        if h in ok_hex:
            continue
        (avert if h in tol_hex else defauts).append(f"couleur {h} x{n}" + ("" if h in tol_hex else " : hors charte"))
    for p, n in sorted(polices.items()):
        if p in t["autorise_polices"] or p.startswith(tuple(t["police_theme_prefixes"])) or p == "":
            continue
        (avert if p in t["tolere_polices"] else defauts).append(f"police '{p}' x{n}" + ("" if p in t["tolere_polices"] else " : hors charte"))
    return defauts, avert


if __name__ == "__main__":
    d, a = controler(sys.argv[1])
    for x in d:
        print("CHARTE DEFAUT", x, file=sys.stderr)
    for x in a:
        print("charte tolere [A VALIDER]", x)
    print(f"lint_charte : {len(d)} defaut(s), {len(a)} valeur(s) tolerees")
    sys.exit(1 if d else 0)
