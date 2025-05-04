def get_proba_estime(elo1,elo2) :
    diff = elo2-elo1
    return 1/(1+10**(diff/400))

def rencontre_elo_estime(joueur1, joueur2):
    """
    Simule une partie entre deux joueurs en se basant uniquement sur leur Elo
    """
    # Récupération des Elos actuels
    elo1 = joueur1.histo_elo[-1]  # Dernier Elo du joueur 1
    elo2 = joueur2.histo_elo[-1]  # Dernier Elo du joueur 2

    # Calcul des probabilités selon la formule de l'Elo
    P1 = get_proba_estime(elo1,elo2)  # Probabilité de victoire du joueur 1
    P2 = 1 - P1  # Probabilité de victoire du joueur 2 (complémentaire)

    if P1 > P2:
        S1 = 1
        S2 = 0
    elif P1 < P2:
        S1 = 0
        S2 = 1
    return S1, S2

    # Mise à jour des Elos des joueurs
    # mettre_a_jour_elo(joueur1, joueur2, S1, S2, P1, P2)

    return S1, S2

#Fonction qui met à jour l'elo des joueurs après une partie (modéle 1)
def mettre_a_jour_elo_estime(joueur1, joueur2) :
    """
    Met à jour l'elo des deux joueurs après une partie.
    """
    P1,P2 = get_proba_estime(joueur1.histo_elo[-1], joueur2.histo_elo[-1]), 1 - get_proba_estime(joueur1.histo_elo[-1], joueur2.histo_elo[-1])
    S1, S2 = rencontre_elo_estime(joueur1, joueur2)

    elo1 = joueur1.histo_elo[-1] + K * (S1 - P1)
    elo2 = joueur2.histo_elo[-1] + K * (S2 - P2)

    # Mise à jour de l'historique des parties et des elos
    joueur1.histo_partie = S1
    joueur2.histo_partie = S2

    joueur1.histo_elo = elo1
    joueur2.histo_elo = elo2

def vraisemblance_estime_elo(joueurs, n_parties):
    vraisemblance_totale = 1.0  # Initialisation à 1 (multiplication des probabilités)

    for _ in range(n_parties):
        joueur1, joueur2 = random.sample(joueurs, 2)
        
        # Calcul des probabilités de victoire selon les Elos
        P1 = get_proba_estime(joueur1.histo_elo[-1], joueur2.histo_elo[-1])
        P2 = 1 - P1
        
        # Tirage du résultat réel de la rencontre
        S1 = tirage_bernoulli(P1)
        S2 = 1 - S1
        
        # Vraisemblance pour cette rencontre
        vraisemblance_totale *= P1**S1 * P2**S2

        # Mise à jour des Elos des joueurs
        mettre_a_jour_elo_estime(joueur1, joueur2)

    return vraisemblance_totale