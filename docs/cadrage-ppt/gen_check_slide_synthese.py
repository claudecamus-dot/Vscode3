"""Génération ISOLÉE de slides pour relecture rapide (4 pages), sans passer
par les 48 slides du deck complet — ORDRE de relecture (retour utilisateur,
distinct de l'ordre de `build()`) :
1. `slide_cover` — reprise TELLE QUELLE (même fonction que la slide 1 du deck
   complet, pas une variante) pour que la charte OCTO du check soit garantie
   identique à celle du deck livré, jamais rejouée à la main.
2. `slide_specificites_infra` — câblée dans `build()` depuis la v2.28 (slide
   8 du deck livré, chapitre 02 · Contexte) ; reprise ici pour relecture
   isolée, pas une 2e version distincte.
3. `slide_synthese_pourquoi_quoi_comment` — brouillon, NON câblée dans
   `build()`, cf. generate_deck.py v2.16-v2.33 pour son historique.
4. `slide_infra_as_product_exemple` — câblée dans `build()` depuis la v2.29
   (slide 9 du deck livré, juste après slide_specificites_infra). Repassée en
   dernier (retour utilisateur du 2026-09-03 : elle occupait la position 2).
Écrit check_slide_synthese.pptx à côté de ce script.

Usage : python gen_check_slide_synthese.py
"""
import os

import generate_deck as G

prs = G.new_prs()
G.slide_cover(prs)
G.slide_specificites_infra(prs)
G.slide_synthese_pourquoi_quoi_comment(prs)
G.slide_infra_as_product_exemple(prs)

problemes = G.D.verifier_geometrie(prs)
if problemes:
    print(f"GEOMETRIE: {len(problemes)} probleme(s)")
    for p in problemes:
        print(" -", p)
else:
    print("GEOMETRIE: OK — aucune forme hors cadre")

out = os.path.join(G.HERE, "check_slide_synthese.pptx")
prs.save(out)
print("Ecrit:", out)
