from classement import SystemeElo, SystemeGlicko, SystemeGlicko2
import numpy as np
import math

K = 32

class Joueur:
    _id_counter = 0

    def __init__(self, force=None):
        self.id = Joueur._id_counter
        Joueur._id_counter += 1
        self.force = force if force is not None else self.generer_force()
        self.historique_scores = []
        self.elo = SystemeElo()
        self.glicko = SystemeGlicko()
        self.glicko2 = SystemeGlicko2()

    @staticmethod
    def generer_force():
        x = np.random.lognormal(mean=-0.5, sigma=0.5)
        return 1 / (1 + np.exp(-np.log(x)))

    def enregistrer_score(self, score):
        self.historique_scores.append(score)


def sigmoid(x, k=10):
    return 1 / (1 + np.exp(-k * x))


def modifie_hasard(taux, impact_force_hasard, fmax):
    eps = 1e-8
    denom = 1 / np.exp(-impact_force_hasard + eps) - 0.5
    denom = np.clip(denom, eps, None)
    a = (taux - 1) / denom
    b = 1 - a / 2
    result = a / (1 + np.exp(-impact_force_hasard * fmax)) + b
    return np.clip(result, 0, 1)


def get_proba_simu(f1, f2, taux, impact):
    diff = abs(f1 - f2)
    mf = max(f1, f2)
    k_hasard = -np.log(modifie_hasard(taux, impact, mf))
    return sigmoid(diff, k=k_hasard * 300 * diff)


def tirage_bernoulli(p):
    return np.random.binomial(1, p)


def rencontre_simu(f1, f2, jeu):
    p = get_proba_simu(f1, f2, jeu.taux_de_hasard, jeu.impact_force_hasard)
    gagnant_est_plus_fort = tirage_bernoulli(p)
    if f1 > f2:
        return (1, 0) if gagnant_est_plus_fort else (0, 1)
    else:
        return (0, 1) if gagnant_est_plus_fort else (1, 0)


def mettre_a_jour_elo_simu(j1, j2, jeu, S1, S2):
    j1.elo.update(j2.elo.rating, S1)
    j2.elo.update(j1.elo.rating, S2)
    j1.enregistrer_score(S1)
    j2.enregistrer_score(S2)


def mettre_a_jour_glicko_simu(j1, j2, S1, S2):
    r2, rd2 = j2.glicko.get_rating()
    r1, rd1 = j1.glicko.get_rating()
    j1.glicko.update([(r2, rd2)], [S1])
    j2.glicko.update([(r1, rd1)], [S2])
    j1.enregistrer_score(S1)
    j2.enregistrer_score(S2)


def mettre_a_jour_glicko2(j1, j2, S1, S2):
    r2, rd2 = j2.glicko2.get_rating()
    r1, rd1 = j1.glicko2.get_rating()
    j1.glicko2.update([(r2, rd2)], [S1])
    j2.glicko2.update([(r1, rd1)], [S2])
    j1.enregistrer_score(S1)
    j2.enregistrer_score(S2)
