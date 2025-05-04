import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import random
import math
import seaborn as sns

K = 32  # Facteur K commun dans les systèmes Elo

class Joueur:
    """
    Cette classe permet de modéliser un joueur. 
    On supposera que le jeu est un jeu individuel donc un joueur est un objet unique de la classe Joueur.
    """
    _id_counter = 0  # Compteur d'ID pour les joueurs
    
    def __init__(self, force, histo_partie, histo_elo):
        self.id = Joueur._id_counter
        Joueur._id_counter += 1
    
        self.force = force 
        self.histo_partie = histo_partie  # Liste des résultats des parties (0 défaite, 1: victoire)
        self.histo_elo = histo_elo  # Historique des Elo 
        
    def __str__(self):
        return (f"ID : {self.id}\n"
                f"force : {self.force}\n"
                f"Historique des Elos : {self.histo_elo}\n"
                f"Historique des parties : {self.histo_partie}\n")

    @property
    def histo_elo(self):
        return self.histo_elo

    @histo_elo.setter
    def histo_elo(self, nouveau_elo):
        self.histo_elo.append(nouveau_elo)


    @property
    def histo_partie(self):
        return self.histo_partie

    @histo_partie.setter
    def histo_partie(self, score):
        self.histo_partie.append(score)
    

def generer_joueur():
    """
    Génère un joueur avec des caractéristiques aléatoires selon différentes distributions :
    Compétences : log-normale (plus adapté qu'une gaussienne car on a plus de joueurs faibles et moyens que fort).
    Age : gaussienne
    elo : log-normale (plus adapté qu'une gaussienne car on a plus de joueurs faibles et moyens que fort).
    Il est important de noter que la génération des compétences et indépendante de celle de l'elo.
    """
    force = np.random.lognormal(mean=1.0, sigma=0.5)
    # Normalisation pour avoir une valeur entre 0 et 10
    force = max(0, min(force, 10))

    # Historique des parties (initialement vides)
    histo_partie = []
    histo_elo = [1500]  # on initialise l'elo à 1500, valeur moyenne entre 0 et 3000

    return Joueur(force, histo_partie, histo_elo)


def modifie_hasard(f1,taux,impact):
    if impact==0:
        return taux
    a = (2*taux-2)/((2/(1+np.exp(-10*impact))-1)+1e-10)
    b = 1-a/2
    return a/(1+np.exp(-impact*10*f1))+b
    #return np.exp((1-impact)*np.log2(f1))


def get_proba_simu(f1,f2,jeu):

    #k_hasard = np.log(jeu.taux_de_hasard+1e-10)
    diff = f1-f2
    mf = max(f1,f2)
    k_hasard = np.log(modifie_hasard(mf,jeu.taux_de_hasard,jeu.impact_hasard))
    return sigmoid(diff, k=k_hasard)


#Dans la fonction de rencontre suivante, on a choisit de modéliser la probabilité de victoire par une loi sigmoide.
def rencontre_simu(joueur1, joueur2, jeu):
    """
    Simule une partie entre deux joueurs et met à jour :
    - leurs elos respectifs.
    - leurs historiques de parties. 
    
    Le taux de hasard du jeu influence la fonction sigmoïde pour ajuster l'impact de la différence de forces.
    """
    # Ajustement du taux de hasard basé sur les joueurs
    
    # Calcul de la probabilité de victoire pour le joueur 1
    P1 = get_proba_simu(joueur1.force, joueur2.force, jeu)  # Probabilité de victoire pour le joueur 1
    P2 = 1 - P1  # Probabilité de victoire pour le joueur 2

    S1 = tirage_bernoulli(P1)  # Tirage aléatoire selon la probabilité de victoire du joueur 1
    S2 = 1 - S1

    # Mise à jour des Elo des joueurs et de leur historique de parties
    # mettre_a_jour_elo(joueur1, joueur2, S1, S2, P1, P2)

    return S1, S2

def sigmoid(x, k=10):
    """Fonction sigmoïde.
        param: k: pente de la fonction sigmoïde
    """
    return 1 / (1 + np.exp(-k * x))

def tirage_bernoulli(p):
    """
    Tire un 1 avec probabilité p,
    0 sinon.
    """
    return np.random.binomial(1, p)

#Fonction qui met à jour l'elo des joueurs après une partie (modéle 1)
def mettre_a_jour_elo_simu(joueur1, joueur2, jeu, S1, S2) :
    """
    Met à jour l'elo des deux joueurs après une partie.
    """
    P1,P2 = get_proba_simu(joueur1.force, joueur2.force, jeu), 1 - get_proba_simu(joueur1.force, joueur2.force, jeu)

    elo1 = joueur1.histo_elo[-1] + K * (S1 - P1)
    elo2 = joueur2.histo_elo[-1] + K * (S2 - P2)

    # Mise à jour de l'historique des parties et des elos
    joueur1.histo_partie = S1
    joueur2.histo_partie = S2

    joueur1.histo_elo = elo1
    joueur2.histo_elo = elo2


def vraisemblance_simu(joueurs, jeu, n_parties):
    vraisemblance_totale = 1.0  # Initialisation à 1 

    for _ in range(n_parties):
        joueur1, joueur2 = random.sample(joueurs, 2)
        
        # Calcul de la probabilité de victoire selon le modèle des forces
        P1 = get_proba_simu(joueur1.force, joueur2.force, jeu)
        P2 = 1 - P1
        
        # Tirage du résultat réel de la rencontre
        S1 = tirage_bernoulli(P1)
        S2 = 1 - S1
        
        # Vraisemblance pour cette rencontre
        vraisemblance_totale *= P1**S1 * P2**S2

        # Mise à jour des historiques
        mettre_a_jour_elo_simu(joueur1, joueur2, jeu, S1, S2)

    return vraisemblance_totale