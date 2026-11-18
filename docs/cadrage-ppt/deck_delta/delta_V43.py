"""Delta V43 (base V42) : reprises de composition + allègement des slides denses, assemblés.

Demande utilisateur du 2026-11-05 : « reprend les compositions + revois les slides trop denses en conservant l'ancienne
version ». La V42 reste intacte ; ce delta produit la V43 en enchaînant les étapes de :
  delta_V43c      : compositions (tableaux 17 et 40, accent navy slide 20, carte 28, roadmap native 32) ;
  delta_V43_s6_19 : slides 6 et 19 allégées ;
  delta_V43_s21   : slide 21 scindée en deux ;
  delta_V43_s29   : slide 29 scindée en deux ;
  delta_V43_s36   : slide 36 scindée en deux.
Chaque étape déclare ses slides par `id:N` (identifiants de la V42, stables au fil des insertions).
Usage (depuis docs/cadrage-ppt/) : py deck_delta/deck.py delta_V43 --base V42 [--sortie ...]
"""
import delta_V43_s6_19 as s619
import delta_V43_s21 as s21
import delta_V43_s29 as s29
import delta_V43_s36 as s36
import delta_V43c as c

BASE = "V42"
NOTE = "V43 : compositions (17, 20, 28, 32, 40) + slides denses scindées ou allégées (6, 19, 21, 29, 36)"
OPS = []
ETAPES = c.ETAPES + s619.ETAPES + s21.ETAPES + s29.ETAPES + s36.ETAPES
