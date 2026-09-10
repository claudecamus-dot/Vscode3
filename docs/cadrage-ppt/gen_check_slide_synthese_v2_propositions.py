"""Proposition graphique v2 du check isolé — même contenu et même mise en page
que `gen_check_slide_synthese.py` (v2.38, archivé dans
`archives/check_slide_synthese-v2.38.pptx`), SEULE variable changée : la
typographie, remplacée par « Outfit » (Google Font, licence OFL, gratuite),
repérée dans 2 documents OCTO récents fournis en référence par l'utilisateur
(`OCTO_GROUND - Proposition accompagnement...pptx.pdf`,
`FDXIA - Fondamentaux de l'IA Générative...pdf` — polices embarquées
identiques dans les deux : Outfit Light/Regular/Medium/SemiBold/Bold).

Le template `template-octo.pptx` ne définit qu'Arial dans son thème — Outfit
n'y est câblée nulle part. Cette police n'était PAS installée sur ce poste ;
elle a été récupérée depuis le dépôt officiel Google Fonts
(github.com/google/fonts, OFL) et installée pour l'utilisateur courant, PUIS
vérifiée par un rendu réel sur LES DEUX moteurs (LibreOffice ET PowerPoint
COM — police à variation, instances nommées Light..Black, le gras "Bold" a
été confirmé correct sur les deux) avant d'être retenue ici — jamais une
police non installée forcée sans vérification (gotcha connue du projet).

Comme `generate_deck.py`/`pptx_deck.py` ne posent PAS explicitement de nom de
police (ils héritent d'Arial via le thème), le changement se fait par une
passe de POST-TRAITEMENT sur la présentation déjà construite plutôt que par
un patch des helpers — plus sûr : aucune ligne de generate_deck.py n'est
modifiée, le deck de production n'est pas affecté.

2 tailles reprises telles que calculées manuellement pour v1 (17pt/12.5pt) —
volontairement PAS retouchées ici pour isoler la typographie comme unique
variable de cette proposition. Voir le rapport remis à l'utilisateur pour un
2e passage éventuel sur les tailles/couleurs si celui-ci est validé.

Usage : python gen_check_slide_synthese_v2_propositions.py
"""
import os

import generate_deck as G

FONT = "Outfit"
FONT_SECOURS = "Arial"
# Vérifié via fonttools (cmap d'Outfit[wght].ttf, police à variation
# téléchargée depuis github.com/google/fonts) : ces 4 caractères sont ABSENTS
# de la police, quelle que soit la variante de graisse — pas seulement "en
# gras" comme le glyphe ⟲ historique sur le thème OCTO (gotcha connue de
# deck-design-library). Rendu réel confirmé : LibreOffice trouve un repli
# correct pour les 4, PowerPoint n'en trouve un correct QUE pour ①②③ (pas
# ⟲, rendu en tofu ⊠) — défaut trouvé au rendu PowerPoint COM, absent du
# rendu LibreOffice seul. Les 4 restent donc forcés sur Arial (police du
# thème, connue pour les couvrir tous) plutôt que de dépendre d'un repli
# système qui diffère d'un moteur à l'autre.
GLYPHES_HORS_OUTFIT = {"①", "②", "③", "⟲"}


def _appliquer_police(prs, font_name=FONT, secours=FONT_SECOURS):
    """Post-traitement : force le nom de police sur CHAQUE run de CHAQUE
    zone de texte, quelle que soit la façon dont il a été créé (D.add_text,
    content_slide, chip, placeholders de la couverture...). Robuste par
    construction — pas besoin de patcher chaque point d'entrée. Exception :
    les runs qui sont EXACTEMENT un glyphe hors couverture d'Outfit restent
    sur la police de secours."""
    n_runs = 0
    n_secours = 0
    for slide in prs.slides:
        for shape in slide.shapes:
            if not shape.has_text_frame:
                continue
            for p in shape.text_frame.paragraphs:
                for r in p.runs:
                    if r.text.strip() in GLYPHES_HORS_OUTFIT:
                        r.font.name = secours
                        n_secours += 1
                    else:
                        r.font.name = font_name
                        n_runs += 1
    print(f"({n_secours} run(s) laissé(s) en {secours} — glyphe hors couverture Outfit)")
    return n_runs


prs = G.new_prs()
G.slide_cover(prs)
G.slide_specificites_infra(prs)
G.slide_synthese_pourquoi_quoi_comment(prs)
G.slide_infra_as_product_exemple(prs)

n = _appliquer_police(prs)
print(f"Police {FONT} appliquée sur {n} runs de texte.")

problemes = G.D.verifier_geometrie(prs)
if problemes:
    print(f"GEOMETRIE: {len(problemes)} probleme(s)")
    for p in problemes:
        print(" -", p)
else:
    print("GEOMETRIE: OK — aucune forme hors cadre")

out = os.path.join(G.HERE, "check_slide_synthese-v2-propositions.pptx")
prs.save(out)
print("Ecrit:", out)
