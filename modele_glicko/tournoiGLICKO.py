import random
from .glicko_utils import rencontre_glicko

def tournoi_round_robin_glicko(joueurs):
    """
    Tournoi round robin où chaque joueur affronte tous les autres une fois.
    """
    n = len(joueurs)
    for i in range(n):
        for j in range(i + 1, n):
            S1, S2 = rencontre_glicko(joueurs[i], joueurs[j])
            joueurs[i].ajouter_match_temp(joueurs[j], S1)
            joueurs[j].ajouter_match_temp(joueurs[i], S2)
    
    # Mettre à jour tous les joueurs
    for joueur in joueurs:
        joueur.mettre_a_jour_batch()
    
    return sorted(joueurs, key=lambda j: j.rating, reverse=True)

def tournoi_suisse_glicko(joueurs, nb_rounds=5):
    """
    Tournoi système suisse Glicko.
    """
    scores = {joueur: 0 for joueur in joueurs}
    appariements = {joueur: [] for joueur in joueurs}

    for _ in range(nb_rounds):
        joueurs_tries = sorted(joueurs, key=lambda j: (-scores[j], -j.rating))
        apparies = set()

        for i, joueur1 in enumerate(joueurs_tries):
            if joueur1 in apparies:
                continue
            for j in range(i + 1, len(joueurs_tries)):
                joueur2 = joueurs_tries[j]
                if joueur2 not in apparies and joueur2 not in appariements[joueur1]:
                    S1, S2 = rencontre_glicko(joueur1, joueur2)
                    scores[joueur1] += S1
                    scores[joueur2] += S2
                    joueur1.ajouter_match_temp(joueur2, S1)
                    joueur2.ajouter_match_temp(joueur1, S2)
                    appariements[joueur1].append(joueur2)
                    appariements[joueur2].append(joueur1)
                    apparies.update([joueur1, joueur2])
                    break

    # Mettre à jour tous les joueurs
    for joueur in joueurs:
        joueur.mettre_a_jour_batch()

    return sorted(joueurs, key=lambda j: j.rating, reverse=True)
