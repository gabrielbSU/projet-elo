from modele_joueur_cor import *

# Pour un jeu très stratégique
tracer_isocontours_hasard(taux_de_hasard=0.1)

# Pour un jeu équilibré
tracer_isocontours_hasard(taux_de_hasard=0.5)

# Pour un jeu très aléatoire (affiche correctement malgré le fort hasard)
tracer_isocontours_hasard(taux_de_hasard=0.9)

# Avec des impacts spécifiques
tracer_isocontours_hasard(taux_de_hasard=0.6, impacts=[0.1, 0.5, 1.0])