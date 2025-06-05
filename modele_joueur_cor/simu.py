import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import random
import math
import seaborn as sns


from constantes import K, RATING_INIT, RD_INIT, Q


class Joueur:
    _id_counter = 0

    def __init__(self, force, histo_partie, histo_elo_simu, histo_elo_estimation, histo_glicko_simu, histo_glicko_estimation):
        self.id = Joueur._id_counter
        Joueur._id_counter += 1
        self.force = force
        self._histo_partie = histo_partie
        self._histo_elo_simu = histo_elo_simu
        self._histo_elo_estimation = histo_elo_estimation
        self.histo_glicko_simu = histo_glicko_simu
        self.histo_glicko_estimation = histo_glicko_estimation

    def __str__(self):
        return (f"ID : {self.id}\n"
                f"force : {self.force}\n"
                f"Historique des Elos : {self._histo_elo_simu}\n"
                f"Historique des parties : {self._histo_partie}\n")

    @property
    def histo_elo_simu(self):
        return self._histo_elo_simu

    @histo_elo_simu.setter
    def histo_elo_simu(self, nouveau_elo):
        self._histo_elo_simu.append(nouveau_elo)

    @property
    def histo_elo_estimation(self):
        return self._histo_elo_estimation

    @histo_elo_estimation.setter
    def histo_elo_estimation(self, nouveau_elo):
        self._histo_elo_estimation.append(nouveau_elo)

    @property
    def histo_partie(self):
        return self._histo_partie

    @histo_partie.setter
    def histo_partie(self, score):
        self._histo_partie.append(score)


def generer_joueur():
    x = np.random.lognormal(mean=1.0, sigma=0.5)
    force = 1 / (1 + np.exp(-np.log(x)))  # sigmoid(log(x)) == x / (1 + x)
    
    histo_partie = []
    histo_elo_simu = [RATING_INIT]
    histo_elo_estimation = [RATING_INIT]
    histo_glicko_simu = [(RATING_INIT, RD_INIT)]
    histo_glicko_estimation = [(RATING_INIT, RD_INIT)]
    
    return Joueur(force, histo_partie, histo_elo_simu, histo_elo_estimation, histo_glicko_simu, histo_glicko_estimation)


def modifie_hasard(taux, impact_force_hasard, f1):
    """conditions intiales : modifie_hasard(taux, impact_force_hasard, 0) = 0 et modifie_hasard(taux, impact_force_hasard, 1) = taux"""
    a = (2 * taux * (1 + np.exp(-impact_force_hasard))) / (1 - np.exp(-impact_force_hasard))
    b = -a / 2
    return a / (1 + np.exp(-impact_force_hasard * f1)) + b

def get_proba_simu(f1, f2, jeu):
    """passage au log si on veut linéariser la modification du hasard"""

    ## proba inversée !

    diff = abs(f1 - f2)
    mf = np.maximum(f1, f2)
    k_hasard = -np.log(modifie_hasard(jeu.taux_de_hasard, jeu.impact_force_hasard, mf))   #on rajoute un - car log(x) < 0 pour x dans ]0,1]
    return sigmoid(diff, k=k_hasard * 10 * diff)


def sigmoid(x, k=10):
    return 1 / (1 + np.exp(-k * x))


def tirage_bernoulli(p):
    return np.random.binomial(1, p)


def rencontre_simu(f1,f2, jeu):
    P1 = get_proba_simu(f1, f2, jeu)
    S1 = tirage_bernoulli(P1)
    S2 = 1 - S1
    return S1, S2


def mettre_a_jour_elo_simu(joueur1, joueur2, jeu, S1, S2):
    P1 = get_proba_simu(joueur1.force, joueur2.force, jeu)
    P2 = 1 - P1
    elo1 = joueur1.histo_elo_simu[-1] + K * (S1 - P1)
    elo2 = joueur2.histo_elo_simu[-1] + K * (S2 - P2)
    joueur1.histo_partie = S1
    joueur2.histo_partie = S2
    joueur1.histo_elo = elo1
    joueur2.histo_elo = elo2


def mettre_a_jour_glicko_simu(joueur, partie, jeu):
    elo = joueur.histo_elo[-1]
    rd = RD_INIT  # Initialisation du RD, peut être ajusté selon les besoins
    q = Q  # Constante de Glicko

    # Mise à jour du rating et du RD
    elo += q * (partie - get_proba_simu(elo, elo, jeu))
    rd = min(math.sqrt(rd**2 + q**2), 350)  # Limite le RD à 350

    joueur.histo_glicko.append((elo, rd))


def vraisemblance_simu(joueurs, jeu, n_parties):
    vraisemblance_totale = 1.0
    for _ in range(n_parties):
        joueur1, joueur2 = random.sample(joueurs, 2)
        P1 = get_proba_simu(joueur1.force, joueur2.force, jeu)
        P2 = 1 - P1
        S1 = tirage_bernoulli(P1)
        S2 = 1 - S1
        vraisemblance_totale *= P1**S1 * P2**S2
        mettre_a_jour_elo_simu(joueur1, joueur2, jeu, S1, S2)
    return vraisemblance_totale




