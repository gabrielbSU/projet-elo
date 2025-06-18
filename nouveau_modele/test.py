from simu import Joueur
from tournoi import tournoi_round_robin, tournoi_suisse
from jeu import Jeu
from visu import *

joueurs = [Joueur() for _ in range(100)]

jeu = Jeu(nom=".", taux_de_hasard=0.3, impact_force_hasard=1)


for i in range(10) : 
    tournoi_suisse(joueurs, jeu, mode="elo")
 
    tournoi_suisse(joueurs, jeu, mode="glicko")

    tournoi_suisse(joueurs, jeu, mode="glicko2")

afficher_spearman(joueurs, systeme="elo")
afficher_spearman(joueurs, systeme="glicko")
afficher_spearman(joueurs, systeme="glicko2")

# comparer_groupes_mannwhitney(joueurs, seuil_force=0.6, systeme=mode)

tester_diff_elo_glicko(joueurs)
tester_diff_elo_glicko2(joueurs)
tester_diff_glicko_glicko2(joueurs)



# tracer_correlation_force_elo(joueurs)

# tracer_correlation_force_glicko(joueurs)

# tracer_correlation_force_glicko2(joueurs)

# tracer_evolution_elo(joueurs[0])
# tracer_evolution_glicko(joueurs[0])
# tracer_evolution_glicko2(joueurs[0])

tracer_comparaison_boxplot(joueurs)
tracer_comparaisons_scatter(joueurs)
