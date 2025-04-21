import random
from .joueur import rencontre_modele1, rencontre_modele2
def tournoi_round_robin(joueurs, jeu,  modele) :
    """
    Organise un tournoi round robin où chaque joueur rencontre tous les autres joueurs une fois.
    Met à jour les elos et les historiques des parties des joueurs après chaque rencontre.
    """
    victoires = {joueur: 0 for joueur in joueurs}

    n = len(joueurs)
    for i in range(n):
        for j in range(i + 1, n):
            if modele == 1:
                S1, S2 = rencontre_modele1(joueurs[i], joueurs[j], jeu)
            else:
                S1, S2 = rencontre_modele2(joueurs[i], joueurs[j])
                
            if S1 == 1:
                victoires[joueurs[i]] += 1
            else:
                victoires[joueurs[j]] += 1

    return sorted(joueurs, key=lambda joueur: victoires[joueur], reverse=True)

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
                        S1, S2 = rencontre_modele1(joueur1, joueur2, jeu)
                    else:
                        S1, S2 = rencontre_modele2(joueur1, joueur2)
                    
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