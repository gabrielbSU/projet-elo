import random
from itertools import combinations
from simu import (
    rencontre_simu,
    mettre_a_jour_elo_simu,
    mettre_a_jour_glicko_simu,
    mettre_a_jour_glicko2,
)


def tournoi_round_robin(joueurs, jeu, mode="elo"):
    matchs = []
    for j1, j2 in combinations(joueurs, 2):
        S1, S2 = rencontre_simu(j1.force, j2.force, jeu)
        if mode == "elo":
            mettre_a_jour_elo_simu(j1, j2, jeu, S1, S2)
        elif mode == "glicko":
            mettre_a_jour_glicko_simu(j1, j2, S1, S2)
        elif mode == "glicko2":
            mettre_a_jour_glicko2(j1, j2, S1, S2)
        matchs.append((j1, j2, S1, S2))
    return matchs


def tournoi_suisse(joueurs, jeu, nb_rounds=5, mode="elo"):
    scores = {j: 0 for j in joueurs}
    adversaires = {j: [] for j in joueurs}
    for _ in range(nb_rounds):
        joueurs_trie = sorted(joueurs, key=lambda j: (-scores[j], -j.elo.rating))
        deja_apparies = set()
        for i, j1 in enumerate(joueurs_trie):
            if j1 in deja_apparies:
                continue
            for j2 in joueurs_trie[i+1:]:
                if j2 in deja_apparies or j2 in adversaires[j1]:
                    continue
                S1, S2 = rencontre_simu(j1.force, j2.force, jeu)
                if mode == "elo":
                    mettre_a_jour_elo_simu(j1, j2, jeu, S1, S2)
                elif mode == "glicko":
                    mettre_a_jour_glicko_simu(j1, j2, S1, S2)
                elif mode == "glicko2":
                    mettre_a_jour_glicko2(j1, j2, S1, S2)
                scores[j1] += S1
                scores[j2] += S2
                adversaires[j1].append(j2)
                adversaires[j2].append(j1)
                deja_apparies.update([j1, j2])
                break
    classement = sorted(joueurs, key=lambda j: (-scores[j], -j.elo.rating))
    return classement


def tournoi_affrontements_aleatoires(joueurs, jeu, nb_matchs=20, mode="elo"):
    """
    Chaque joueur affronte aléatoirement un autre joueur pendant un nombre de matchs donné.
    """
    matchs = []

    for _ in range(nb_matchs):
        j1, j2 = random.sample(joueurs, 2)
        S1, S2 = rencontre_simu(j1.force, j2.force, jeu)

        if mode == "elo":
            mettre_a_jour_elo_simu(j1, j2, jeu, S1, S2)
        elif mode == "glicko":
            mettre_a_jour_glicko_simu(j1, j2, S1, S2)
        elif mode == "glicko2":
            mettre_a_jour_glicko2(j1, j2, S1, S2)

        matchs.append((j1, j2, S1, S2))

    return matchs
