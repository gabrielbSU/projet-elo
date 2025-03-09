# projet-LU2IN013
Exploration du comportement des systèmes de rating (Elo, Glicko, Glicko-2) en fonction des capacités des joueurs

## Description
Ce projet explore le comportement des systèmes de rating tels que Elo, Glicko et Glicko-2 en fonction des capacités des joueurs. Il permet de générer des joueurs avec des compétences et des elo aléatoires, de simuler des rencontres entre eux et de visualiser les distributions des compétences et des elo.

## Installation
Pour exécuter ce projet, vous aurez besoin de Python 3 et des bibliothèques suivantes :
- numpy
- matplotlib
- seaborn
- scipy

## Description des classes et des fonctions

## Classe Joueur
__init__(self, nom, prenom, age, comp, histo_partie, histo_tournoi, elo):
Initialise un joueur avec son nom, prénom, âge, compétences, historique des parties, historique des tournois et elo.

categorie(self): Retourne la catégorie du joueur en fonction de son elo.

afficher_joueur(self): Affiche les informations du joueur.

get_elo(self): Retourne l'elo du joueur.

force_joueur(self): Retourne la force d'un joueur entre 0 et 1.

force_relative(self, joueur_adverse): Renvoie le couple (f1, f2) des forces relatives entre 2 joueurs.

rencontre(self, joueur_adverse): Simule une partie entre deux joueurs et renvoie le résultat.

comparaison_rencontre_elo(self, joueur_adverse): Renvoie True si le résultat de la rencontre est conforme aux prédictions de l'elo, False sinon.

generer_joueur(nom, prenom): Génère un joueur avec des caractéristiques aléatoires.

tracer_competences(joueurs): Trace l'histogramme et la densité des compétences des joueurs.

tracer_elo(joueurs): Trace l'histogramme et la densité des elo des joueurs.

tracer_competences_et_elo(joueurs): Trace les densités des compétences et des elo sur le même graphique.

## Classe Outils
probabilite_victoire(f1, f2, sigma=1): Calcule la probabilité que le joueur 1 gagne en fonction des forces relatives f1 et f2.

probabilite_victoire_avec_hasard(f1, f2, sigma=1, sigma_hasard=0.2): Calcule la probabilité que le joueur 1 gagne en ajoutant un facteur de hasard.



