from joueur import Joueur

# Générer des joueurs
joueur1 = Joueur.generer_joueur("Nom1", "Prenom1")
joueur2 = Joueur.generer_joueur("Nom2", "Prenom2")
joueur3 = Joueur.generer_joueur("Nom3", "Prenom3")
joueur4 = Joueur.generer_joueur("Nom4", "Prenom4")
joueur5 = Joueur("Nom5", "Prenom5", 13, [1, 1, 1, 1, 1], [], [], 1000)

# Afficher les informations des joueurs
joueur1.afficher_joueur()
joueur2.afficher_joueur()
joueur3.afficher_joueur()
joueur4.afficher_joueur()
joueur5.afficher_joueur()

# Simuler des rencontres entre les joueurs
resultat1 = joueur1.rencontre(joueur2)
resultat2 = joueur1.rencontre(joueur3)
resultat3 = joueur1.rencontre(joueur4)
resultat4 = joueur2.rencontre(joueur3)
resultat5 = joueur2.rencontre(joueur4)
resultat6 = joueur3.rencontre(joueur4)
resultat7 = joueur3.rencontre(joueur5)

# Afficher les résultats des rencontres
print(f"Résultat de la rencontre entre {joueur1.nom} et {joueur2.nom} : {resultat1}")
print(f"Résultat de la rencontre entre {joueur1.nom} et {joueur3.nom} : {resultat2}")
print(f"Résultat de la rencontre entre {joueur1.nom} et {joueur4.nom} : {resultat3}")
print(f"Résultat de la rencontre entre {joueur2.nom} et {joueur3.nom} : {resultat4}")
print(f"Résultat de la rencontre entre {joueur2.nom} et {joueur4.nom} : {resultat5}")
print(f"Résultat de la rencontre entre {joueur3.nom} et {joueur4.nom} : {resultat6}")
print(f"Résultat de la rencontre entre {joueur3.nom} et {joueur5.nom} : {resultat7}")

# Afficher les informations des joueurs après les rencontres
print("\nInformations des joueurs après les rencontres :")
joueur1.afficher_joueur()
joueur2.afficher_joueur()
joueur3.afficher_joueur()
joueur4.afficher_joueur()
joueur5.afficher_joueur()