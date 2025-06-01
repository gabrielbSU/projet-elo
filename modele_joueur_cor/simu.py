import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import random
import math
import seaborn as sns


from constantes import K, RATING_INIT, RD_INIT, Q


class Joueur:
    _id_counter = 0

    def __init__(self, force, histo_partie, histo_elo):
        self.id = Joueur._id_counter
        Joueur._id_counter += 1
        self.force = force
        self._histo_partie = histo_partie
        self._histo_elo = histo_elo
        self.histo_glicko = []

    def __str__(self):
        return (f"ID : {self.id}\n"
                f"force : {self.force}\n"
                f"Historique des Elos : {self._histo_elo}\n"
                f"Historique des parties : {self._histo_partie}\n")

    @property
    def histo_elo(self):
        return self._histo_elo

    @histo_elo.setter
    def histo_elo(self, nouveau_elo):
        self._histo_elo.append(nouveau_elo)

    @property
    def histo_partie(self):
        return self._histo_partie

    @histo_partie.setter
    def histo_partie(self, score):
        self._histo_partie.append(score)


def generer_joueur():
    force = np.random.lognormal(mean=1.0, sigma=0.5)
    force = max(0, min(force, 10))
    histo_partie = []
    histo_elo = [1500]
    return Joueur(force, histo_partie, histo_elo)


def modifie_hasard(f1, taux, impact):
    if impact == 0:
        return taux
    a = (2 * taux - 2) / ((2 / (1 + np.exp(-10 * impact)) - 1) + 1e-10)
    b = 1 - a / 2
    return a / (1 + np.exp(-impact * 10 * f1)) + b


def get_proba_simu(f1, f2, jeu):
    diff = f1 - f2
    mf = max(f1, f2)
    k_hasard = np.log(modifie_hasard(mf, jeu.taux_de_hasard, jeu.impact_hasard))
    return sigmoid(diff, k=k_hasard)


def sigmoid(x, k=10):
    return 1 / (1 + np.exp(-k * x))


def tirage_bernoulli(p):
    return np.random.binomial(1, p)


def rencontre_simu(joueur1, joueur2, jeu):
    P1 = get_proba_simu(joueur1.force, joueur2.force, jeu)
    S1 = tirage_bernoulli(P1)
    S2 = 1 - S1
    return S1, S2


def mettre_a_jour_elo_simu(joueur1, joueur2, jeu, S1, S2):
    P1 = get_proba_simu(joueur1.force, joueur2.force, jeu)
    P2 = 1 - P1
    elo1 = joueur1.histo_elo[-1] + K * (S1 - P1)
    elo2 = joueur2.histo_elo[-1] + K * (S2 - P2)
    joueur1.histo_partie = S1
    joueur2.histo_partie = S2
    joueur1.histo_elo = elo1
    joueur2.histo_elo = elo2


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


def g(rating):
    return 1 / math.sqrt(1 + (3 * Q**2 * rating**2) / math.pi**2)


def E(r, ri, rdi):
    return 1 / (1 + 10 ** (g(rdi) * (ri - r) / 400))


def rencontre_simu_glicko(joueur1, joueur2, jeu):
    P1 = get_proba_simu(joueur1.force, joueur2.force, jeu)
    S1 = tirage_bernoulli(P1)
    S2 = 1 - S1
    joueur1.histo_partie = S1
    joueur2.histo_partie = S2
    return joueur1, joueur2, S1, S2


def mettre_a_jour_glicko(joueur, adversaires_info, date):
    if joueur.histo_glicko:
        r, rd = joueur.histo_glicko[-1][:2]
    else:
        r, rd = RATING_INIT, RD_INIT

    if not adversaires_info:
        rd = min(math.sqrt(rd**2 + 50**2), RD_INIT)
        joueur.histo_glicko.append((r, rd, date))
        return

    d2_inv = sum((Q**2) * g(rdi)**2 * E(r, ri, rdi) * (1 - E(r, ri, rdi)) for ri, rdi, score in adversaires_info)
    d2 = 1 / d2_inv
    delta = d2 * sum(Q * g(rdi) * (score - E(r, ri, rdi)) for ri, rdi, score in adversaires_info)
    rd_new = 1 / math.sqrt((1 / rd**2) + (1 / d2))
    r_new = r + Q / ((1 / rd**2) + (1 / d2)) * sum(g(rdi) * (score - E(r, ri, rdi)) for ri, rdi, score in adversaires_info)
    joueur.histo_glicko.append((r_new, rd_new, date))


def update_glicko_all_players(joueurs, matchs, date):
    infos = {j.id: [] for j in joueurs}
    for j1, j2, s1, s2 in matchs:
        r2, rd2 = j2.histo_glicko[-1][:2] if j2.histo_glicko else (RATING_INIT, RD_INIT)
        r1, rd1 = j1.histo_glicko[-1][:2] if j1.histo_glicko else (RATING_INIT, RD_INIT)
        infos[j1.id].append((r2, rd2, s1))
        infos[j2.id].append((r1, rd1, s2))
    for j in joueurs:
        mettre_a_jour_glicko(j, infos[j.id], date)
