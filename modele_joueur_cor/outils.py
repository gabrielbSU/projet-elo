import numpy as np
K = 32  # Facteur K commun dans les systèmes Elo

def sigmoid(x, k=10):
    """Fonction sigmoïde.
        param: k: pente de la fonction sigmoïde
    """
    return 1 / (1 + np.exp(-k * x))

def tirage_bernoulli(p):
    """
    Tire un 1 avec probabilité p,
    0 sinon.
    """
    return np.random.binomial(1, p)

#Fonction qui met à jour l'elo des joueurs après une partie (modéle 1)
def mettre_a_jour_elo(joueur1, joueur2, S1, S2, P1, P2):
    """
    Met à jour l'elo des deux joueurs après une partie.
    """
    elo1 = joueur1.histo_elo[-1] + K * (S1 - P1)
    elo2 = joueur2.histo_elo[-1] + K * (S2 - P2)

    # Mise à jour de l'historique des parties
    joueur1.histo_partie.append(S1)
    joueur2.histo_partie.append(S2)

    joueur1.histo_elo.append(elo1)
    joueur2.histo_elo.append(elo2)