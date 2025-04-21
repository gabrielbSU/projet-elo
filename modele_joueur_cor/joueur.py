from.outils import sigmoid, tirage_bernoulli, mettre_a_jour_elo
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import random
import math
import seaborn as sns

class Joueur:
    """
    Cette classe permet de modéliser un joueur. 
    On supposera que le jeu est un jeu individuel donc un joueur est un objet unique de la classe Joueur.
    """

    def __init__(self, nom, prenom, age, comp, histo_partie, histo_elo):
        self.nom = nom
        self.prenom = prenom
        self.age = age
        self.comp = comp  # comp est une liste de 5 compétences dont le coeff est la position dans la liste. Chaque compétence prend une valeur entre 0 et 10
        self.histo_partie = histo_partie  # Liste des résultats des parties (0 défaite, 1: victoire)
        self.histo_elo = histo_elo  # Historique des Elo 
        
    def __str__(self):
        return (f"Nom : {self.nom}\n"
                f"Prénom : {self.prenom}\n"
                f"Age : {self.age}\n"
                f"Compétences : {self.comp}\n"
                f"Historique des Elos : {self.histo_elo}\n"
                f"Historique des parties : {self.histo_partie}\n")


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



    # Historique des parties (initialement vides)
    histo_partie = []
    histo_elo = [1500]  # on initialise l'elo à 1500, valeur moyenne entre 0 et 3000

    return Joueur(nom, prenom, age, comp, histo_partie, histo_elo)


def modifie_hasard(f1,taux,impact):
    if impact==0:
        return taux
    a = (2*taux-2)/((2/(1+np.exp(-10*impact))-1)+1e-10)
    b = 1-a/2
    return a/(1+np.exp(-impact*10*f1))+b
    #return np.exp((1-impact)*np.log2(f1))

def get_proba_modele1(f1,f2,jeu):

    #k_hasard = np.log(jeu.taux_de_hasard+1e-10)
    diff = f1-f2
    mf = max(f1,f2)
    k_hasard = np.log(modifie_hasard(mf,jeu.taux_de_hasard,jeu.impact_hasard))
    return sigmoid(diff, k=k_hasard)

def get_proba_modele2(elo1,elo2) :
    diff = elo2-elo1
    return 1/(1+10**(diff/400))

#Dans la fonction de rencontre suivante, on a choisit de modéliser la probabilité de victoire par une loi sigmoide.
def rencontre_modele1(joueur1, joueur2, jeu):
    """
    Simule une partie entre deux joueurs et met à jour :
    - leurs elos respectifs.
    - leurs historiques de parties. 
    
    Le taux de hasard du jeu influence la fonction sigmoïde pour ajuster l'impact de la différence de forces.
    """
    # Ajustement du taux de hasard basé sur les joueurs
    
    # Calcul de la probabilité de victoire pour le joueur 1
    P1 = get_proba_modele1(joueur1.force_joueur(), joueur2.force_joueur(), jeu)  # Probabilité de victoire pour le joueur 1
    P2 = 1 - P1  # Probabilité de victoire pour le joueur 2

    S1 = tirage_bernoulli(P1)  # Tirage aléatoire selon la probabilité de victoire du joueur 1
    S2 = 1 - S1

    # Mise à jour des Elo des joueurs et de leur historique de parties
    mettre_a_jour_elo(joueur1, joueur2, S1, S2, P1, P2)

    return S1, S2

def rencontre_modele2(joueur1, joueur2):
    """
    Simule une partie entre deux joueurs en se basant uniquement sur leur Elo
    """
    # Récupération des Elos actuels
    elo1 = joueur1.histo_elo[-1]  # Dernier Elo du joueur 1
    elo2 = joueur2.histo_elo[-1]  # Dernier Elo du joueur 2

    # Calcul des probabilités selon la formule de l'Elo
    P1 = get_proba_modele2(elo1,elo2)  # Probabilité de victoire du joueur 1
    P2 = 1 - P1  # Probabilité de victoire du joueur 2 (complémentaire)

    # Détermination du vainqueur selon les probabilités lissées
    S1 = tirage_bernoulli(P1)  # Tirage aléatoire pour le joueur 1 basé sur PP1
    S2 = 1 - S1  # Le vainqueur inverse

    # Mise à jour des Elos des joueurs
    mettre_a_jour_elo(joueur1, joueur2, S1, S2, P1, P2)

    return S1, S2