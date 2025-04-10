import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import random
import math
import seaborn as sns
from .outils import tirage_victoire_log_normal, tirage_victoire_sigmoide, sigmoid, mettre_a_jour_elo
from .jeu import Jeu



class Joueur:
    """
    Cette classe permet de modéliser un joueur. 
    On supposera que le jeu est un jeu individuel donc un joueur est un objet unique de la classe Joueur.
    """

    def __init__(self, nom, prenom, age, comp, histo_partie, histo_tournoi, histo_elo):
        self.nom = nom
        self.prenom = prenom
        self.age = age
        self.comp = comp  # comp est une liste de 5 compétences dont le coeff est la position dans la liste. Chaque compétence prend une valeur entre 0 et 10
        self.histo_partie = histo_partie  # Liste des résultats des parties (0 défaite, 1: victoire)
        self.histo_tournoi = histo_tournoi  # Liste des résultats des tournois
        self.histo_elo = histo_elo  # Historique des Elo 
        
    def __str__(self):
        """
        Affiche les informations du joueur.
        """
        print(f"Nom : {self.nom}")
        print(f"Prénom : {self.prenom}")
        print(f"Age : {self.age}")
        print(f"Compétences : {self.comp}")
        print(f"Historique des Elos : {self.histo_elo}")
        print(f"Historique des parties : {self.histo_partie}")
        print(f"Historique des tournois : {self.histo_tournoi}")

    def force_joueur(self):
        """
        Retourne la force d'un joueur entre 0 et 1.
        """
        tot = 0
        for i in range(len(self.comp)):
            tot += self.comp[i] * (i + 1)
        return float(tot) / 150
    
    
def generer_joueur(nom, prenom):
    """
    Génère un joueur avec des caractéristiques aléatoires selon différentes distributions :
    Compétences : log-normale (plus adapté qu'une gaussienne car on a plus de joueurs faibles et moyens que fort).
    Age : gaussienne
    elo : log-normale (plus adapté qu'une gaussienne car on a plus de joueurs faibles et moyens que fort).
    Il est important de noter que la génération des compétences et indépendante de celle de l'elo.
    """
    # Génération de l'âge (entre 15 et 40 ans)
    age = int(np.random.normal(loc=25, scale=5))  # Moyenne = 25, écart-type = 5
    age = max(15, min(age, 40))  # On s'assure que l'âge reste dans [15, 40]

    # Génération des compétences (5 compétences entre 0 et 10)
    comp = []
    for _ in range(5):
        competence = np.random.lognormal(mean=1.0, sigma=0.5)
        # Normalisation pour avoir une valeur entre 0 et 10
        competence = max(0, min(competence, 10))
        comp.append(round(competence, 1))



    # Historique des parties et tournois (initialement vides)
    histo_partie = []
    histo_tournoi = []
    histo_elo = [1500]  # on initialise l'elo à 1500, valeur moyenne entre 0 et 3000

    return Joueur(nom, prenom, age, comp, histo_partie, histo_tournoi, histo_elo)

#Dans la fonction de rencontre suivante, on a choisit de modéliser la probabilité de victoire par une loi sigmoide.
def rencontre_sigmoide(joueur1, joueur2, jeu):
    """
    Simule une partie entre deux joueurs et met à jour :
    - leurs elos respectifs.
    - leurs historiques de parties. 
    
    Le taux de hasard du jeu influence la fonction sigmoïde pour ajuster l'impact de la différence de forces.
    
    jeu: objet de la classe Jeu qui contient le taux de hasard du jeu.
    """
    f1, f2 = joueur1.force_joueur(), joueur2.force_joueur()

    # Calcul de la différence de forces
    diff = f1 - f2
    
    # Ajustement du facteur de lissage 'k' en fonction du taux de hasard du jeu
    # Plus le taux de hasard est élevé, plus le facteur de lissage est faible
    k_hasard = 10 * (1 - jeu.taux_de_hasard) *(1 + abs(diff))  # Ajustement du facteur de lissage en fonction du taux de hasard et de la différence de forces
    
    # Calcul de la probabilité de victoire pour le joueur 1
    P1 = sigmoid(diff, k=k_hasard)
    P2 = 1 - P1  # Probabilité de victoire pour le joueur 2

    if(P1 >= P2):
        S1 = 1
        S2 = 0
    else:
        S1 = 0
        S2 = 1

    # Mise à jour des Elo des joueurs et de leur historique de parties
    mettre_a_jour_elo(joueur1, joueur2, S1, S2, P1, P2)
    
    return S1, S2

#Dans la fonction de rencontre suivante, on a choisit de modéliser la probabilité de victoire par une loi log-normale.
#Cette loi est plus adaptée pour modéliser la probabilité de victoire d'un joueur en fonction de sa force.
def rencontre_log_normale(joueur1, joueur2):
    """
    Simule une partie entre deux joueurs et met à jour :
    - leurs elos respectifs.
    - leurs historiques de parties. 
    """
    f1, f2 = joueur1.force_joueur(), joueur2.force_joueur()

    # Calcul du gagnant de la partie et du perdant de la partie
    (P1, P2) = tirage_victoire_log_normale(f1, f2)

    # Tirage final selon les probabilités calculées avec un facteur de hasard
    tirage = np.random.rand()  # Tirage aléatoire entre 0 et 1
    if tirage < P1:
        S1 = 1  # Joueur 1 gagne
        S2 = 0  # Joueur 2 perd
    else:
        S1 = 0  # Joueur 1 perd
        S2 = 1  # Joueur 2 gagne

    # Mise à jour de l'elo
    mettre_a_jour_elo(joueur1, joueur2, S1, S2, P1, P2)

    # Ajout des nouveaux elos dans l'historique
    joueur1.histo_elo.append(joueur1.elo)
    joueur2.histo_elo.append(joueur2.elo)


def rencontre_modele2(joueur1, joueur2, jeu):
    """
    Simule une partie entre deux joueurs en se basant uniquement sur leur Elo,
    avec un lissage de la probabilité en fonction du taux de hasard du jeu.

    Notons que P1_lisse = (1 - hasard) * P1 + hasard * 0.5
    """
    # Récupération des Elos actuels
    elo1 = joueur1.histo_elo[-1]
    elo2 = joueur2.histo_elo[-1]

    # Calcul des probabilités (selon la formule de l'Elo)
    P1 = 1 / (1 + 10 ** ((elo2 - elo1) / 400))
    P2 = 1 - P1

    # Lissage avec le taux de hasard du jeu
    hasard = jeu.taux_de_hasard
    P1_lisse = (1 - hasard) * P1 + hasard * 0.5
    P2_lisse = 1 - P1_lisse  # Toujours cohérent

    # Détermination du vainqueur selon les probabilités lissées
    if P1_lisse >= P2_lisse:
        S1, S2 = 1, 0  # Joueur 1 gagne
    else:
        S1, S2 = 0, 1  # Joueur 2 gagne

    # Mise à jour des Elos
    mettre_a_jour_elo(joueur1, joueur2, S1, S2, P1_lisse, P2_lisse)

    # Mise à jour des historiques
    joueur1.histo_partie.append(S1)
    joueur2.histo_partie.append(S2)

    joueur1.histo_elo.append(joueur1.elo)
    joueur2.histo_elo.append(joueur2.elo)

    return S1, S2
