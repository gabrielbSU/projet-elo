import random
from modele_joueur_cor.simu import rencontre_simu, mettre_a_jour_elo_simu
from modele_joueur_cor.estimation import rencontre_elo_estime, mettre_a_jour_elo_estime

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
        if mode == "simu":
            S1, S2 = rencontre_simu(joueur1, joueur2, jeu)
            mettre_a_jour_elo_simu(joueur1, joueur2, jeu, S1, S2)

        elif mode == "estimation":
            S1, S2 = rencontre_elo_estime(joueur1, joueur2)
            mettre_a_jour_elo_estime(joueur1, joueur2)

        else:
            raise ValueError("Mode inconnu. Utilisez 'simu' ou 'estimation'.")

        matchs.append((joueur1, joueur2, S1, S2))
    
    return matchs


def tournoi_suisse(joueurs, jeu, nb_rounds=5, modele=1):
    """
    Organise un tournoi selon le système suisse.
    """
    
    # Initialisation des scores et des historiques
    scores = {joueur: 0 for joueur in joueurs}
    appariements = {joueur: [] for joueur in joueurs}  # Historique des adversaires
    
    for round_num in range(1, nb_rounds + 1):
        # Tri des joueurs par score (puis par Elo si égalité)
        joueurs_tries = sorted(joueurs, 
                             key=lambda j: (-scores[j], -j.histo_elo[-1]))
        
        # Appariement des joueurs
        apparies = set()
        for i in range(len(joueurs_tries)):
            joueur1 = joueurs_tries[i]
            if joueur1 in apparies:
                continue
                
            # Trouver le meilleur adversaire disponible
            for j in range(i + 1, len(joueurs_tries)):
                joueur2 = joueurs_tries[j]
                if (joueur2 not in apparies and 
                    joueur2 not in appariements[joueur1]):
                    # Faire jouer la partie
                    if modele == 1:
                        S1, S2 = rencontre_simu(joueur1, joueur2, jeu)
                        mettre_a_jour_elo_simu(joueur1, joueur2, jeu, S1, S2)
                    else:
                        S1, S2 = rencontre_elo_estime(joueur1, joueur2)
                        mettre_a_jour_elo_estime(joueur1, joueur2)
                    
                    # Mettre à jour les scores
                    scores[joueur1] += S1
                    scores[joueur2] += S2
                    
                    # Enregistrer l'appariement
                    appariements[joueur1].append(joueur2)
                    appariements[joueur2].append(joueur1)
                    
                    apparies.update([joueur1, joueur2])
                    break
    
    # Classement final
    classement = sorted(joueurs, key=lambda j: (-scores[j], -j.histo_elo[-1]))
    
    return classement

