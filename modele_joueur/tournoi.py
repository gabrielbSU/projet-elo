import random
from .joueur import rencontre_sigmoide, generer_joueur

def tournoi_round_robin(joueurs,jeu):
    """
    Organise un tournoi round robin où chaque joueur rencontre tous les autres joueurs une fois.
    Met à jour les elos et les historiques des parties des joueurs après chaque rencontre.
    
    joueurs: Liste des joueurs participant au tournoi
    """
    # Initialiser le dictionnaire des victoires
    victoires = {joueur: 0 for joueur in joueurs}

    n = len(joueurs)
    for i in range(n):
        for j in range(i + 1, n):
            rencontre_sigmoide(joueurs[i], joueurs[j], jeu)
            # Mettre à jour le compteur de victoires
            if joueurs[i].histo_partie[-1] == 1:
                victoires[joueurs[i]] += 1
            if joueurs[j].histo_partie[-1] == 1:
                victoires[joueurs[j]] += 1

    # Mise à jour de l'historique des tournois pour chaque joueur
    for joueur in joueurs:
        joueur.histo_tournoi.append("Tournoi Round Robin")

    # Classement des joueurs par leur nombre de victoires
    classement = sorted(joueurs, key=lambda joueur: victoires[joueur], reverse=True)
    
    return classement

def tournoi_eliminatoire(joueurs,jeu):
    """
    Organise un tournoi à élimination directe et renvoie le classement des joueurs.
    Dans ce tournoi, seuls les gagnants passent au tour suivant, et donc il n'y a pas de rencontres des perdants. 
    Attention, le nombre de joueurs doit être multiple de 8.
    
    joueurs: Liste des joueurs participant au tournoi
    """
    classement = []
    num_tour= 1
    while len(joueurs) > 1:
        print(f"tour {num_tour}:")
        random.shuffle(joueurs)
        tour_suiv = []
        for i in range(0, len(joueurs), 2):
            if i + 1 < len(joueurs):
                joueur1 = joueurs[i]
                joueur2 = joueurs[i + 1]
                rencontre_sigmoide(joueur1, joueur2,jeu)
                if joueur1.histo_partie[-1] == 1:
                    tour_suiv.append(joueur1)
                    classement.append(joueur2)
                else:
                    tour_suiv.append(joueur2)
                    classement.append(joueur1)
                print(f"{joueur1.nom} {joueur1.prenom} vs {joueur2.nom} {joueur2.prenom}")
            else:
                tour_suiv.append(joueurs[i])
        joueurs = tour_suiv
        num_tour += 1

    # Le gagnant du tournoi
    gagnant = joueurs[0]
    classement.append(gagnant)
    classement.reverse()  # Le gagnant doit être en tête du classement
    print(f"Le gagnant du tournoi est {gagnant.nom} {gagnant.prenom} avec {gagnant.histo_elo[-1]} Elo")
    return classement

def tournoi_round_robin_modele2(joueurs,jeu):
    """
    Organise un tournoi round robin où chaque joueur rencontre tous les autres joueurs une fois.
    Met à jour les elos et les historiques des parties des joueurs après chaque rencontre.
    
    joueurs: Liste des joueurs participant au tournoi
    """
    # Initialiser le dictionnaire des victoires
    victoires = {joueur: 0 for joueur in joueurs}

    n = len(joueurs)
    for i in range(n):
        for j in range(i + 1, n):
            rencontre_sigmoide(joueurs[i], joueurs[j], jeu)
            # Mettre à jour le compteur de victoires
            if joueurs[i].histo_partie[-1] == 1:
                victoires[joueurs[i]] += 1
            if joueurs[j].histo_partie[-1] == 1:
                victoires[joueurs[j]] += 1

    # Mise à jour de l'historique des tournois pour chaque joueur
    for joueur in joueurs:
        joueur.histo_tournoi.append("Tournoi Round Robin")

    # Classement des joueurs par leur nombre de victoires
    classement = sorted(joueurs, key=lambda joueur: victoires[joueur], reverse=True)
    
    return classement

def tournoi_eliminatoire_modele2(joueurs,jeu):
    """
    Organise un tournoi à élimination directe et renvoie le classement des joueurs.
    Dans ce tournoi, seuls les gagnants passent au tour suivant, et donc il n'y a pas de rencontres des perdants. 
    Attention, le nombre de joueurs doit être multiple de 8.
    
    joueurs: Liste des joueurs participant au tournoi
    """
    classement = []
    num_tour= 1
    while len(joueurs) > 1:
        print(f"tour {num_tour}:")
        random.shuffle(joueurs)
        tour_suiv = []
        for i in range(0, len(joueurs), 2):
            if i + 1 < len(joueurs):
                joueur1 = joueurs[i]
                joueur2 = joueurs[i + 1]
                rencontre_sigmoide(joueur1, joueur2)
                if joueur1.histo_partie[-1] == 1:
                    tour_suiv.append(joueur1)
                    classement.append(joueur2)
                else:
                    tour_suiv.append(joueur2)
                    classement.append(joueur1)
                print(f"{joueur1.nom} {joueur1.prenom} vs {joueur2.nom} {joueur2.prenom}")
            else:
                tour_suiv.append(joueurs[i])
        joueurs = tour_suiv
        num_tour += 1

    # Le gagnant du tournoi
    gagnant = joueurs[0]
    classement.append(gagnant)
    classement.reverse()  # Le gagnant doit être en tête du classement
    print(f"Le gagnant du tournoi est {gagnant.nom} {gagnant.prenom} avec {gagnant.histo_elo[-1]} Elo")
    return classement


def afficher_classement(classement):
    """
    Affiche le classement des joueurs après le tournoi.
    
    classement: Liste des joueurs classés par leur performance dans le tournoi
    """
    print("Classement du tournoi:")
    for i, joueur in enumerate(classement, start=1):
        print(f"{i}. {joueur.nom} {joueur.prenom} - {joueur.histo_elo[-1]} Elo")
