import random
from modele_joueur_cor.simu import rencontre_simu, mettre_a_jour_elo_simu
from modele_joueur_cor.estimation import rencontre_elo_estime, mettre_a_jour_elo_estime, update_glicko_all_players

from itertools import combinations

def tournoi_round_robin(joueurs, jeu, mode="simu"):
    """
    Organise un tournoi round-robin selon le mode choisi : simulation ou estimation.
    
    Args:
        joueurs (list): Liste des objets Joueur.
        jeu (object): Contient taux_de_hasard et impact_hasard.
        mode (str): "simu" ou "estimation".
    
    Returns:
        list of tuple: Liste des matchs (joueur1, joueur2, score1, score2)
    """
    matchs = []

    for joueur1, joueur2 in combinations(joueurs, 2):
        f1, f2 = joueur1.force, joueur2.force
        S1, S2 = rencontre_simu(f1, f2, jeu)
        if mode == "simu":
            mettre_a_jour_elo_simu(joueur1, joueur2, jeu, S1, S2)

        elif mode == "estimation":
            mettre_a_jour_elo_estime(joueur1, joueur2, S1, S2)

        else:
            raise ValueError("Mode inconnu. Utilisez 'simu' ou 'estimation'.")

        matchs.append((joueur1, joueur2, S1, S2))
    
    return matchs


def tournoi_suisse(joueurs, jeu, nb_rounds=5, mode="simu"):
    """
    """
    scores = {joueur: 0 for joueur in joueurs}
    appariements = {joueur: [] for joueur in joueurs}

    for round_num in range(1, nb_rounds + 1):
        joueurs_tries = sorted(
            joueurs,
            key=lambda j: (-scores[j], -(
                j.histo_elo_simu[-1] if mode == "simu" else j.histo_elo_estimation[-1])
            )
        )

        apparies = set()
        for i in range(len(joueurs_tries)):
            joueur1 = joueurs_tries[i]
            if joueur1 in apparies:
                continue

            for j in range(i + 1, len(joueurs_tries)):
                joueur2 = joueurs_tries[j]
                if joueur2 not in apparies and joueur2 not in appariements[joueur1]:
                    S1, S2 = rencontre_simu(joueur1.force, joueur2.force, jeu)
                    if mode == "simu":
                        mettre_a_jour_elo_simu(joueur1, joueur2, jeu, S1, S2)
                    elif mode == "estimation":
                        mettre_a_jour_elo_estime(joueur1, joueur2, S1, S2)
                    else:
                        raise ValueError("Mode inconnu. Utilisez 'simu' ou 'estimation'.")

                    scores[joueur1] += S1
                    scores[joueur2] += S2
                    appariements[joueur1].append(joueur2)
                    appariements[joueur2].append(joueur1)
                    apparies.update([joueur1, joueur2])
                    break

    classement = sorted(
        joueurs,
        key=lambda j: (-scores[j], -(
            j.histo_elo_simu[-1] if mode == "simu" else j.histo_elo_estimation[-1])
        )
    )
    return classement



def tournoi_round_robin_glicko(joueurs, jeu, date, mode="simu"):
    """
    """
    matchs = []

    for joueur1, joueur2 in combinations(joueurs, 2):
        f1, f2 = joueur1.force, joueur2.force
        S1, S2 = rencontre_simu(f1, f2, jeu)
        if mode == "simu":
            mettre_a_jour_elo_simu(joueur1, joueur2, jeu, S1, S2)

        elif mode == "estimation":
            mettre_a_jour_elo_estime(joueur1, joueur2, S1, S2)

        else:
            raise ValueError("Mode inconnu. Utilisez 'simu' ou 'estimation'.")

        matchs.append((joueur1, joueur2, S1, S2))

    update_glicko_all_players(joueurs, matchs, date)
    return matchs

    
def tournoi_suisse_glicko(joueurs, jeu, date, nb_rounds=5, mode="simu"):
    """
    """
    scores = {joueur: 0 for joueur in joueurs}
    appariements = {joueur: [] for joueur in joueurs}
    matchs_total = []

    for round_num in range(nb_rounds):
        joueurs_tries = sorted(
            joueurs,
            key=lambda j: (-scores[j], -(
                j.histo_elo_simu[-1] if mode == "simu" else j.histo_elo_estimation[-1])
            )
        )

        apparies = set()
        for i in range(len(joueurs_tries)):
            joueur1 = joueurs_tries[i]
            if joueur1 in apparies:
                continue

            for j in range(i + 1, len(joueurs_tries)):
                joueur2 = joueurs_tries[j]
                if joueur2 not in apparies and joueur2 not in appariements[joueur1]:
                    S1, S2 = rencontre_simu(joueur1.force, joueur2.force, jeu)
                    if mode == "simu":
                        mettre_a_jour_elo_simu(joueur1, joueur2, jeu, S1, S2)
                    elif mode == "estimation":
                        mettre_a_jour_elo_estime(joueur1, joueur2, S1, S2)
                    else:
                        raise ValueError("Mode inconnu. Utilisez 'simu' ou 'estimation'.")

                    scores[joueur1] += S1
                    scores[joueur2] += S2
                    appariements[joueur1].append(joueur2)
                    appariements[joueur2].append(joueur1)
                    apparies.update([joueur1, joueur2])
                    matchs_total.append((joueur1, joueur2, S1, S2))
                    break

    update_glicko_all_players(joueurs, matchs_total, date)

    classement = sorted(
        joueurs,
        key=lambda j: (-scores[j], -(
            j.histo_elo_simu[-1] if mode == "simu" else j.histo_elo_estimation[-1])
        )
    )
    return classement
