from modele_joueur import np, norm, plt, Joueur, probabilite_victoire, probabilite_victoire_avec_hasard

# Génération d'une liste de joueurs
joueurs = [Joueur.generer_joueur(f"Joueur{i}", f"Prénom{i}") for i in range(1000)]
for j in joueurs : 
    print(j.elo)

# Tracé des compétences
Joueur.tracer_competences(joueurs)

# Tracé des elo
Joueur.tracer_elo(joueurs)

# Comparaison des densités des compétences et des elo
Joueur.tracer_competences_et_elo(joueurs)

# Simuler des rencontres
for i in range(len(joueurs) - 1):
    joueurs[i].rencontre(joueurs[i + 1])

# Tracer l'évolution de sigma_hasard
Joueur.tracer_evolution_sigma_hasard()
