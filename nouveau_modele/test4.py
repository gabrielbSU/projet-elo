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

    return hist1, hist2


def simuler_duel_glicko_batch(p_win, n_batches=1000, batch_size=10):
    j1 = SystemeGlicko()
    j2 = SystemeGlicko()
    hist1, hist2 = [], []

    for _ in range(n_batches):
        scores = np.random.binomial(1, p_win, size=batch_size)
        opp_scores = 1 - scores
        r2, rd2 = j2.get_rating()
        r1, rd1 = j1.get_rating()
        j1.update([(r2, rd2)] * batch_size, scores.tolist())
        j2.update([(r1, rd1)] * batch_size, opp_scores.tolist())
        hist1.append(j1.get_rating()[0])
        hist2.append(j2.get_rating()[0])

    return hist1, hist2


def simuler_duel_glicko2_batch(p_win, n_batches=1000, batch_size=10):
    j1 = SystemeGlicko2()
    j2 = SystemeGlicko2()
    hist1, hist2 = [], []

    for _ in range(n_batches):
        scores = np.random.binomial(1, p_win, size=batch_size)
        opp_scores = 1 - scores
        r2, rd2 = j2.get_rating()
        r1, rd1 = j1.get_rating()
        j1.update([(r2, rd2)] * batch_size, scores.tolist())
        j2.update([(r1, rd1)] * batch_size, opp_scores.tolist())
        hist1.append(j1.get_rating()[0])
        hist2.append(j2.get_rating()[0])

    return hist1, hist2


def tracer_convergence(hist1, hist2, titre, ylabel):
    plt.figure(figsize=(10, 6))
    plt.plot(hist1, label="Joueur 1")
    plt.plot(hist2, label="Joueur 2")
    plt.title(titre)
    plt.xlabel("Batchs")
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    probas = [0.5, 0.7, 0.8, 0.9]

    for p in probas:
        h1, h2 = simuler_duel_elo(p_win=p, n_parties=10000)
        tracer_convergence(h1, h2, f"Évolution Elo (P(J1 gagne) = {p})", "Elo")

    for p in probas:
        h1, h2 = simuler_duel_glicko_batch(p_win=p)
        tracer_convergence(h1, h2, f"Évolution Glicko (batch) — P(J1 gagne) = {p}", "Rating Glicko")

    for p in probas:
        h1, h2 = simuler_duel_glicko2_batch(p_win=p)
        tracer_convergence(h1, h2, f"Évolution Glicko-2 (batch) — P(J1 gagne) = {p}", "Rating Glicko-2")
