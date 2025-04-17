import random
from .joueur import rencontre_sigmoide, generer_joueur

def tournoi_round_robin(joueurs, jeu):
    """
    Organise un tournoi round robin où chaque joueur rencontre tous les autres joueurs une fois.
    Met à jour les elos et les historiques des parties des joueurs après chaque rencontre.
    """
    # Initialiser le dictionnaire des victoires
    victoires = {joueur: 0 for joueur in joueurs}

    n = len(joueurs)
    for i in range(n):
        for j in range(i + 1, n):
            S1, S2 = rencontre_sigmoide(joueurs[i], joueurs[j], jeu)
            if S1 == 1:
                victoires[joueurs[i]] += 1
            else:  # forcément S2 == 1
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


def tournoi_suisse(joueurs, nb_rounds):
    """
    Simule un tournoi suisse avec une liste de joueurs.
    
    :param joueurs: Liste d'objets Joueur
    :param nb_rounds: Nombre de rondes du tournoi
    :return: Classement des joueurs après le tournoi
    """
    for ronde in range(nb_rounds):
        # Trie les joueurs par Elo et les appaire par paires proches
        joueurs_triees = sorted(joueurs, key=lambda x: x.histo_elo[-1], reverse=True)
        
        # Partie par partie
        for i in range(0, len(joueurs_triees), 2):
            joueur1 = joueurs_triees[i]
            joueur2 = joueurs_triees[i + 1]
            # Rencontre entre les joueurs
            rencontre_sigmoide(joueur1, joueur2, jeu)
        
    # Classement final des joueurs
    classement = sorted(joueurs, key=lambda x: sum(x.histo_partie), reverse=True)
    return classement



def tournoi_suisse_modele2(joueurs, nb_rounds, jeu):
    """
    Simule un tournoi suisse avec une liste de joueurs en utilisant la fonction rencontre_modele2.
    
    :param joueurs: Liste d'objets Joueur
    :param nb_rounds: Nombre de rondes du tournoi
    :param jeu: L'objet du jeu qui contient les paramètres d'impact du hasard
    :return: Classement des joueurs après le tournoi
    """
    for ronde in range(nb_rounds):
        print(f"--- Ronde {ronde + 1} ---")
        
        # Trie les joueurs par Elo et les appaire par paires proches
        joueurs_triees = sorted(joueurs, key=lambda x: x.histo_elo[-1], reverse=True)
        
        # Partie par partie
        for i in range(0, len(joueurs_triees), 2):
            joueur1 = joueurs_triees[i]
            joueur2 = joueurs_triees[i + 1]
            
            # Affiche les informations des joueurs
            print(f"Rencontre entre {joueur1.nom} {joueur1.prenom} (Elo: {joueur1.histo_elo[-1]}) "
                  f"et {joueur2.nom} {joueur2.prenom} (Elo: {joueur2.histo_elo[-1]})")
            
            # Simulation de la rencontre entre les joueurs en utilisant rencontre_modele2
            S1, S2 = rencontre_modele2(joueur1, joueur2, jeu)
            
            # Affiche les résultats de la rencontre
            if S1 == 1:
                print(f"{joueur1.nom} {joueur1.prenom} gagne contre {joueur2.nom} {joueur2.prenom}")
            else:
                print(f"{joueur2.nom} {joueur2.prenom} gagne contre {joueur1.nom} {joueur1.prenom}")
        
        print("\n")

    # Classement final des joueurs : tri par le nombre de victoires ou points cumulés
    classement = sorted(joueurs, key=lambda x: sum(x.histo_partie), reverse=True)
    
    print("--- Classement Final ---")
    for i, joueur in enumerate(classement, 1):
        print(f"{i}. {joueur.nom} {joueur.prenom} - Victoires: {sum(joueur.histo_partie)} - Elo: {joueur.histo_elo[-1]}")
    
    return classement
