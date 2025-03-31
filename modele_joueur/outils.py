import numpy as np
from .constantes import K

def tirage_victoire_log_normal(f1, f2, mu=0, sigma_base=0.1):
    """
    Calcule les probabilités de victoire en utilisant une loi log-normale
    pour ajuster l'importance du hasard en fonction de la différence de forces
    entre les joueurs. Les forces f1 et f2 sont comprises entre 0 et 1.
    
    f1 : Force du joueur 1 (entre 0 et 1)
    f2 : Force du joueur 2 (entre 0 et 1)
    mu : Moyenne de la loi log-normale (facteur central pour la probabilité de victoire)
    sigma_base : Ecart-type de la loi log-normale, qui détermine l'importance du hasard
    
    Retourne 1 si le joueur 1 gagne, 2 si le joueur 2 gagne.
    """
    # Calcul de la différence de forces
    diff = f1 - f2
    
    # Calcul de la variance de la loi log-normale en fonction de la différence
    # Plus la différence est grande, moins le hasard affecte le tirage
    variance = sigma_base * (1 - np.abs(diff))  # Plus la différence est grande, moins la variance est importante
    
    # Tirage log-normal : plus la différence est grande, moins la variance est importante
    log_normal_draw = np.random.lognormal(mu, variance)
    
    # Probabilité de victoire du joueur 1 selon la loi log-normale
    P1 = log_normal_draw / (1 + log_normal_draw)  # Conversion pour obtenir une probabilité entre 0 et 1
    P2 = 1 - P1
    
    return (P1, P2)

def sigmoid(x, k=10):
    """Fonction sigmoïde qui lisse les probabilités en fonction de la différence des forces."""
    return 1 / (1 + np.exp(-k * x))

def tirage_victoire_sigmoide(f1, f2, k=10):
    """
    Calcule les probabilités de victoire en utilisant une fonction sigmoïde.
    
    f1 : Force du joueur 1 (entre 0 et 1)
    f2 : Force du joueur 2 (entre 0 et 1)
    k : Facteur de lissage pour la fonction sigmoïde
    
    Retourne 1 si le joueur 1 gagne, 2 si le joueur 2 gagne.
    """
    # Calcul de la différence de forces
    diff = f1 - f2
    
    # Calcul de la probabilité de victoire pour le joueur 1
    P1 = sigmoid(diff, k)
    P2 = 1 - P1  # Probabilité de victoire pour le joueur 2

    return (P1,P2)

#Fonction qui met à jour l'elo des joueurs après une partie  #à mettre dans outils
def mettre_a_jour_elo(joueur1, joueur2, S1, S2, P1, P2):
    from .joueur import Joueur  #import dans la fonction pour pas avoir de pb de circular import
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