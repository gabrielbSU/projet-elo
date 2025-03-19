#Test des tournois

from modele_joueur import tournoi_round_robin, generer_joueur, afficher_classement, tournoi_eliminatoire

# Générer 8 joueurs aléatoires
joueurs = [generer_joueur(f"nom{i+1}", f"prenom{i+1}") for i in range(100)]

# Organiser un tournoi round robin
classement = tournoi_eliminatoire(joueurs)
afficher_classement(classement)