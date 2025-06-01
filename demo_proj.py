from modele_joueur_cor import *

liste_joueurs = [generer_joueur() for _ in range(100)]

tracer_forces(liste_joueurs)
tracer_elo(liste_joueurs)

poker = Jeu('Poker', taux_de_hasard=0.1, impact_hasard=0.5)

tournoi1 = tournoi_round_robin(liste_joueurs, poker, modele=1)

for _ in range(10) :
    tournoi1 = tournoi_round_robin(tournoi1, poker, modele=1)

tracer_elo(liste_joueurs)


## Les 2 tracés suivants sont incohérents ##

tracer_force_elo(liste_joueurs)
tracer_evolution_elo(liste_joueurs[0])
tracer_comparaison_evolution_elo(liste_joueurs[0:3])

tracer_isocontours_force(poker, impact_hasard=1)
visualiser_3d_force(poker)

tracer_isocontours_impact_variable(0.5)

tracer_isocontours_hasard(0.2)