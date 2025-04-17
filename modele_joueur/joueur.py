import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import random
import math
import seaborn as sns
from .outils import tirage_victoire_log_normal, tirage_victoire_sigmoide, sigmoid, mettre_a_jour_elo, tirage_bernoulli
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
        return (f"Nom : {self.nom}\n"
                f"Prénom : {self.prenom}\n"
                f"Age : {self.age}\n"
                f"Compétences : {self.comp}\n"
                f"Historique des Elos : {self.histo_elo}\n"
                f"Historique des parties : {self.histo_partie}\n"
                f"Historique des tournois : {self.histo_tournoi}")


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
    """
    # Ajustement du taux de hasard basé sur les joueurs
    k_hasard = 10*ajuster_impact_hasard(joueur1, joueur2,jeu) * (1 + abs(joueur1.force_joueur() - joueur2.force_joueur()))
    
    # Calcul de la probabilité de victoire pour le joueur 1
    diff = joueur1.force_joueur() - joueur2.force_joueur()
    P1 = sigmoid(diff, k=k_hasard)
    P2 = 1 - P1  # Probabilité de victoire pour le joueur 2

    S1 = tirage_bernoulli(P1)  # Tirage aléatoire selon la probabilité de victoire du joueur 1
    S2 = 1 - S1

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
    avec un lissage de la probabilité en fonction de l'impact du hasard ajusté 
    par la fonction 'ajuster_impact_hasard' du jeu.

    Notons que P1_lisse = (1 - impact_hasard) * P1 + impact_hasard * 0.5
    """
    # Récupération des Elos actuels
    elo1 = joueur1.histo_elo[-1]  # Dernier Elo du joueur 1
    elo2 = joueur2.histo_elo[-1]  # Dernier Elo du joueur 2

    # Calcul des probabilités selon la formule de l'Elo
    P1 = 1 / (1 + 10 ** ((elo2 - elo1) / 400))  # Probabilité de victoire du joueur 1
    P2 = 1 - P1  # Probabilité de victoire du joueur 2 (complémentaire)

    # Ajustement du taux de hasard en fonction des forces des joueurs via la méthode ajuster_impact_hasard
    impact_hasard = ajuster_impact_hasard(joueur1, joueur2,jeu)

    # Lissage avec l'impact ajusté du hasard
    P1_lisse = (1 - impact_hasard) * P1 + impact_hasard * 0.5  # Lissage pour P1
    P2_lisse = 1 - P1_lisse  # P2 est forcément l'inverse de P1

    # Détermination du vainqueur selon les probabilités lissées
    S1 = tirage_bernoulli(P1_lisse)  # Tirage aléatoire pour le joueur 1 basé sur P1_lisse
    S2 = 1 - S1  # Le vainqueur inverse

    # Mise à jour des Elos des joueurs
    mettre_a_jour_elo(joueur1, joueur2, S1, S2, P1_lisse, P2_lisse)

    # Mise à jour des historiques
    joueur1.histo_partie.append(S1)  # Ajouter le résultat pour joueur 1
    joueur2.histo_partie.append(S2)  # Ajouter le résultat pour joueur 2

    joueur1.histo_elo.append(joueur1.elo)  # Ajouter le nouvel Elo de joueur 1
    joueur2.histo_elo.append(joueur2.elo)  # Ajouter le nouvel Elo de joueur 2

    return S1, S2



def ajuster_impact_hasard(joueur1, joueur2, jeu):
    """
    Ajuste l'impact du hasard en fonction de la différence de force et des forces individuelles des joueurs.
    
    :param joueur1: Objet représentant le joueur 1
    :param joueur2: Objet représentant le joueur 2
    :return: Le taux de hasard modifié
    """
    
    # Récupérer les forces des joueurs
    f1 = joueur1.force_joueur()
    f2 = joueur2.force_joueur()
    
    # Calcul de la différence de force
    diff_force = abs(f1 - f2)

    # Calcul de l'impact du hasard en fonction des forces des joueurs
    # Si les joueurs sont faibles, le hasard a un plus grand impact
    # Si les joueurs sont forts, le hasard a un impact plus faible
    impact_par_force = max(1 - 0.05 * (f1 + f2), 0.1)  # Plus la somme des forces est élevée, moins le hasard est important
    
    # Ajustement final du taux de hasard en fonction de la différence et de l'impact des forces
    ajustement = max(1 - 0.1 * diff_force, 0.1)  # Moins la différence est grande, plus le hasard est important
    return jeu.taux_de_hasard * impact_par_force * ajustement * jeu.impact_hasard