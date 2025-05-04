import random
def tournoi_round_robin(joueurs, jeu, modele):
    """
    Organise un tournoi round robin où chaque joueur rencontre tous les autres joueurs une fois.
    Met à jour les elos et les historiques des parties des joueurs après chaque rencontre.
    """
    victoires = [0 for _ in joueurs]

    n = len(joueurs)
    for i in range(n):
        for j in range(i + 1, n):
            j1, j2 = joueurs[i], joueurs[j]

            if modele == 1:
                # Modèle 1: Simulation
                S1, S2 = rencontre_simu(j1, j2, jeu)
                R1_new, R2_new = mettre_a_jour_elo_simu(j1, j2, S1, S2)
            else:
                # Modèle 2: Elo estimé
                S1, S2 = rencontre_elo_estime(j1, j2)
                R1_new, R2_new = mettre_a_jour_elo_estime(j1, j2, S1, S2)

            # Mise à jour des victoires
            if S1 == 1:
                victoires[i] += 1
            else:
                victoires[j] += 1

            # Mise à jour des historiques
            j1.histo_partie = S1
            j2.histo_partie = S2
            j1.histo_elo = R1_new
            j2.histo_elo = R2_new

    # Trie les joueurs selon le nombre de victoires
    joueurs_tries = sorted(joueurs, key=lambda j: victoires[j.id], reverse=True)
    return joueurs_tries


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
                        R1_new, R2_new = mettre_a_jour_elo_simu(j1, j2, S1, S2)
                    else:
                        S1, S2 = rencontre_elo_estime(joueur1, joueur2)
                        R1_new, R2_new = mettre_a_jour_elo_estime(j1, j2, S1, S2)
                    
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