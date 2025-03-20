from modele_joueur import Joueur, tournoi_eliminatoire, afficher_classement, generer_joueur, __str__

# Générer des joueurs
joueur1 = generer_joueur("Nom1", "Prenom1")
joueur2 = generer_joueur("Nom2", "Prenom2")
joueur3 = generer_joueur("Nom3", "Prenom3")
joueur4 = generer_joueur("Nom4", "Prenom4")
joueur5 = Joueur("Nom5", "Prenom5", 13, [1, 1, 1, 1, 1], [], [], 1500)
joueur6 = generer_joueur("Nom6", "Prenom6")
joueur7 = generer_joueur("Nom7", "Prenom7")
joueur8 = generer_joueur("Nom8", "Prenom8")

# Liste des joueurs
joueurs = [joueur1, joueur2, joueur3, joueur4, joueur5, joueur6, joueur7, joueur8]

# Afficher les informations des joueurs
for joueur in joueurs:
    joueur.__str__()

# Organiser un tournoi à élimination directe
for i in range():
    classement = tournoi_eliminatoire(joueurs)

# Afficher le classement du tournoi
afficher_classement(classement)

# Afficher les informations des joueurs après le tournoi
print("\nInformations des joueurs après le tournoi :")
for joueur in classement:
    joueur.__str__()