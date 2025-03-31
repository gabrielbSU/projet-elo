from modele_joueur import tracer_competences, tracer_elo, generer_joueur, tournoi_round_robin, plt, Jeu, tracer_force_elo, tracer_comparaison_evolution_elo, tracer_evolution_elo

# Génération de joueurs aléatoires
nombres_joueurs = 20  # Nombre de joueurs à générer
joueurs = [generer_joueur(f"Joueur{i+1}", f"Prenom{i+1}") for i in range(nombres_joueurs)]

# Affichage initial des courbes
print("Test des fonctions de visualisation...\n")

# Tracer la distribution des compétences et des Elo au début
print("Affichage initial des distributions des compétences et Elo...")
tracer_competences(joueurs)
tracer_elo(joueurs)


# Simulation de plusieurs tournois avec la fonction round robin
n_tournois = 100  # Nombre de tournois à simuler
jeu = Jeu('Poker',0.1)  # Assurez-vous de définir ce paramètre en fonction du jeu

for t in range(1, n_tournois + 1):
    #print(f"\nTournoi {t}...\n")
    
    # Effectuer un tournoi round-robin
    classement = tournoi_round_robin(joueurs, jeu)
    
    
    # Réaffichage des courbes après le tournoi
    #print(f"Affichage de l'elo après le tournoi {t}...\n")
    #tracer_elo(joueurs)

#tracer_force_elo(joueurs)

print("force joueur 0 : ", joueurs[0].force_joueur())
tracer_evolution_elo(joueurs[0])

