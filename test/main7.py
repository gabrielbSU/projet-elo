from modele_joueur import generer_joueur, tracer_competences, tracer_elo, tracer_competences_et_elo, Jeu, rencontre_sigmoide, rencontre_log_normale

K = 30 #Facteur de développement (il nous permet de moduler l'impact d'un match sur l'elo d'un joueur)

# Création de quelques joueurs
joueur1 = generer_joueur("Dupont", "Pierre")
joueur2 = generer_joueur("Martin", "Paul")
joueur3 = generer_joueur("Durand", "Jacques")

# Initialisation des joueurs dans une liste
joueurs = [joueur1, joueur2, joueur3]

# Affichage des joueurs
print("Détails du joueur 1:")
joueur1.__str__()

print("\nDétails du joueur 2:")
joueur2.__str__()

print("\nDétails du joueur 3:")
joueur3.__str__()

# Tracer la distribution des compétences des joueurs
tracer_competences(joueurs)

# Tracer la distribution des Elo des joueurs
tracer_elo(joueurs)

# Tracer les densités des compétences et des Elo sur le même graphique
tracer_competences_et_elo(joueurs)

# Simulation de plusieurs matchs entre les joueurs
print("\nSimulations de matchs (Sigmoïde):")
for i in range(5):
    jeu = Jeu("Poker", 0.5)  # Exemple de jeu avec un taux de hasard de 0.5
    print(f"\nMatch {i+1} entre {joueur1.nom} et {joueur2.nom}:")
    rencontre_sigmoide(joueur1, joueur2, jeu)

    print(f"Élo de {joueur1.nom}: {joueur1.elo}")
    print(f"Élo de {joueur2.nom}: {joueur2.elo}")

# Simulation de matchs avec loi log-normale
print("\nSimulations de matchs (Log-normale):")
for i in range(5):
    print(f"\nMatch {i+1} entre {joueur1.nom} et {joueur2.nom}:")
    rencontre_log_normale(joueur1, joueur2)

    print(f"Élo de {joueur1.nom}: {joueur1.elo}")
    print(f"Élo de {joueur2.nom}: {joueur2.elo}")
