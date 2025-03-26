from modele_joueur.joueur import generer_joueur, tracer_competences, tracer_evolution_proba_victoire
from modele_joueur.jeu import Jeu
from modele_joueur.tournoi import tournoi_round_robin, afficher_classement

jeu = Jeu("Poker", 0.5)

joueurs = [generer_joueur(f"nom {i+1}", f"prenom {i+1}") for i in range(50)]

tracer_competences(joueurs)

tournoi_round_robin(joueurs, jeu)

afficher_classement(joueurs)

for i in range(50) : 
    tracer_evolution_proba_victoire(jeu, joueurs[i], joueurs[i+1])

