#Classe Outils
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

class Outils:
    """
    Une classe utilitaire non instanciable.
    """
    def __init__(self):
        raise TypeError("Cette classe ne peut pas être instanciée.")

    @staticmethod
    def probabilite_victoire(f1, f2, sigma=1):
        """
        Calcule la probabilité que le joueur 1 gagne en fonction des forces relatives f1 et f2 (resp des joueurs 1 et 2).
        sigma: Écart-type de la distribution gaussienne (par défaut 1)
        """
        delta_f = f1 - f2
        proba = norm.cdf(delta_f, loc=0, scale=sigma)
        return proba
        
    @staticmethod
    def probabilite_victoire_avec_hasard(f1, f2, sigma=1, sigma_hasard=0.2):
        """
        Calcule la probabilité que le joueur 1 gagne en ajoutant un facteur de hasard.
        sigma_hasard: Écart-type du facteur de hasard (cette valeur doit être choisie dans [0; 0.5]. 
        Si sigma_hasard = 0, il n'y a pas de hasard. 
        Le facteur de hasard epsilon est généré selon une distribution normale centrée en 0 et avec un écart type sigma_hasard.
        """
        if not 0 <= sigma_hasard <= 0.5:
            raise ValueError("sigma_hasard doit être dans l'intervalle [0, 0.5].")
        
        delta_f = f1 - f2
        epsilon = np.random.normal(0, sigma_hasard)
        delta_f_ajuste = delta_f + epsilon
        proba = norm.cdf(delta_f_ajuste, loc=0, scale=sigma)  # sigma = 1 pour la gaussienne
        return proba

