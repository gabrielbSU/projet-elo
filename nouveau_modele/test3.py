import numpy as np
import matplotlib.pyplot as plt
from classement import SystemeElo, SystemeGlicko, SystemeGlicko2


def simuler_duel_elo(p_win, n_parties=10000, k=32):
    j1 = SystemeElo(k=k)
    j2 = SystemeElo(k=k)
    hist1, hist2 = [], []

    for _ in range(n_parties):
        score = np.random.binomial(1, p_win)
        r1 = j1.rating
        r2 = j2.rating
        j1.update(r2, score)
        j2.update(r1, 1 - score)
        hist1.append(j1.rating)
        hist2.append(j2.rating)

    plt.figure(figsize=(10, 6))
    plt.plot(hist1, label="Joueur 1")
    plt.plot(hist2, label="Joueur 2")
    plt.title(f"\u00c9volution des Elos (P(J1 gagne) = {p_win})")
    plt.xlabel("Nombre de parties")
    plt.ylabel("Elo")
    plt.legend()
    plt.grid(True)
    plt.show()


def simuler_duel_glicko(p_win, n_parties=10000):
    j1 = SystemeGlicko()
    j2 = SystemeGlicko()
    hist1, hist2 = [], []

    for _ in range(n_parties):
        score = np.random.binomial(1, p_win)
        r2, rd2 = j2.get_rating()
        r1, rd1 = j1.get_rating()
        j1.update([(r2, rd2)], [score])
        j2.update([(r1, rd1)], [1 - score])
        hist1.append(j1.get_rating()[0])
        hist2.append(j2.get_rating()[0])

    plt.figure(figsize=(10, 6))
    plt.plot(hist1, label="Joueur 1")
    plt.plot(hist2, label="Joueur 2")
    plt.title(f"\u00c9volution Glicko (P(J1 gagne) = {p_win})")
    plt.xlabel("Nombre de parties")
    plt.ylabel("Rating Glicko")
    plt.legend()
    plt.grid(True)
    plt.show()


def simuler_duel_glicko2(p_win, n_parties=10000):
    j1 = SystemeGlicko2()
    j2 = SystemeGlicko2()
    hist1, hist2 = [], []

    for _ in range(n_parties):
        score = np.random.binomial(1, p_win)
        r2, rd2 = j2.get_rating()
        r1, rd1 = j1.get_rating()
        j1.update([(r2, rd2)], [score])
        j2.update([(r1, rd1)], [1 - score])
        hist1.append(j1.get_rating()[0])
        hist2.append(j2.get_rating()[0])

    plt.figure(figsize=(10, 6))
    plt.plot(hist1, label="Joueur 1")
    plt.plot(hist2, label="Joueur 2")
    plt.title(f"\u00c9volution Glicko-2 (P(J1 gagne) = {p_win})")
    plt.xlabel("Nombre de parties")
    plt.ylabel("Rating Glicko-2")
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    for p in [0.5, 0.7, 0.8, 0.9]:
        simuler_duel_elo(p_win=p)
        simuler_duel_glicko(p_win=p)
        simuler_duel_glicko2(p_win=p)
 