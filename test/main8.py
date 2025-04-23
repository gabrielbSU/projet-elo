from modele_joueur import Joueur, generer_joueur, Jeu, tournoi_round_robin, afficher_classement, tracer_competences

jeu = Jeu("Poker", 0.5)

joueurs = [generer_joueur(f"nom {i+1}", f"prenom {i+1}") for i in range(50)]

tracer_competences(joueurs)

tournoi_round_robin(joueurs, jeu)

afficher_classement(joueurs)

for i in range(50) : 
    tracer_evolution_proba_victoire(jeu, joueurs[i], joueurs[i+1])

