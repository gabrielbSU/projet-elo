from itertools import combinations
from simu import (
    rencontre_simu,
    mettre_a_jour_elo,
    mettre_a_jour_glicko,
    mettre_a_jour_glicko2
)

def tournoi_round_robin(joueurs, jeu, mode="simu", systeme="elo"):
    matchs = []
    for j1, j2 in combinations(joueurs, 2):
        S1, S2 = rencontre_simu(j1.force, j2.force, jeu)
        if systeme == "elo":
            mettre_a_jour_elo(j1, j2, S1, S2, mode)
        elif systeme == "glicko":
            mettre_a_jour_glicko(j1, j2, S1, S2, mode)
        elif systeme == "glicko2":
            mettre_a_jour_glicko2(j1, j2, S1, S2, mode)
        matchs.append((j1, j2, S1, S2))
    return matchs

def tournoi_suisse(joueurs, jeu, nb_rounds=5, mode="simu", systeme="elo"):
    scores = {j: 0 for j in joueurs}
    adversaires = {j: [] for j in joueurs}
    
    for _ in range(nb_rounds):
        if systeme == "elo":
            joueurs_tries = sorted(joueurs, key=lambda j: (-scores[j], -j.elo_simu.rating if mode == "simu" else -j.elo_estime.rating))
        elif systeme == "glicko":
            joueurs_tries = sorted(joueurs, key=lambda j: (-scores[j], -j.glicko_simu.get_rating()[0] if mode == "simu" else -j.glicko_estime.get_rating()[0]))
        elif systeme == "glicko2":
            joueurs_tries = sorted(joueurs, key=lambda j: (-scores[j], -j.glicko2_simu.get_rating()[0] if mode == "simu" else -j.glicko2_estime.get_rating()[0]))

        deja_apparies = set()
        for i, j1 in enumerate(joueurs_tries):
            if j1 in deja_apparies:
                continue
            for j2 in joueurs_tries[i+1:]:
                if j2 in deja_apparies or j2 in adversaires[j1]:
                    continue

                S1, S2 = rencontre_simu(j1.force, j2.force, jeu)

                if systeme == "elo":
                    mettre_a_jour_elo(j1, j2, S1, S2, mode)
                elif systeme == "glicko":
                    mettre_a_jour_glicko(j1, j2, S1, S2, mode)
                elif systeme == "glicko2":
                    mettre_a_jour_glicko2(j1, j2, S1, S2, mode)

                scores[j1] += S1
                scores[j2] += S2
                adversaires[j1].append(j2)
                adversaires[j2].append(j1)
                deja_apparies.update([j1, j2])
                break

    if systeme == "elo":
        classement = sorted(joueurs, key=lambda j: (-scores[j], -j.elo_simu.rating if mode == "simu" else -j.elo_estime.rating))
    elif systeme == "glicko":
        classement = sorted(joueurs, key=lambda j: (-scores[j], -j.glicko_simu.get_rating()[0] if mode == "simu" else -j.glicko_estime.get_rating()[0]))
    elif systeme == "glicko2":
        classement = sorted(joueurs, key=lambda j: (-scores[j], -j.glicko2_simu.get_rating()[0] if mode == "simu" else -j.glicko2_estime.get_rating()[0]))

    return classement
