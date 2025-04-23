import math
import numpy as np

def glicko_g(RD):
    """ Fonction g(RD) du Glicko """
    return 1 / math.sqrt(1 + (3 * RD**2) / (math.pi**2 * 400**2))

def glicko_E(rating_joueur, rating_adversaire, RD_adversaire):
    """Probabilité de victoire selon Glicko."""
    return 1 / (1 + 10 ** (-glicko_g(RD_adversaire) * (rating_joueur - rating_adversaire) / 400))

def mettre_a_jour_glicko(joueur, adversaires, resultats):
    """Mise à jour du rating et RD d'un joueur après ses matchs."""
    if not adversaires:
        # Aucun match → incertitude augmente
        joueur.RD = min(math.sqrt(joueur.RD**2 + 50**2), 350)
        joueur.historique_RD.append(joueur.RD)
        joueur.historique_rating.append(joueur.rating)
        return

    d2_inv = 0
    somme = 0
    for adv, res in zip(adversaires, resultats):
        E_ = glicko_E(joueur.rating, adv.rating, adv.RD)
        g_ = glicko_g(adv.RD)
        d2_inv += (g_ ** 2) * E_ * (1 - E_)
        somme += g_ * (res - E_)

    d2 = 1 / (d2_inv + 1e-10)
    nouveau_rating = joueur.rating + (400 / math.log(10)) * d2 * somme
    nouveau_RD = math.sqrt(1 / d2)

    joueur.rating = nouveau_rating
    joueur.RD = max(min(nouveau_RD, 350), 30)
    joueur.historique_rating.append(joueur.rating)
    joueur.historique_RD.append(joueur.RD)

def rencontre_glicko(joueur1, joueur2):
    """Simule un match entre deux joueurs selon le modèle Glicko."""
    P1 = glicko_E(joueur1.rating, joueur2.rating, joueur2.RD)
    S1 = np.random.binomial(1, P1)
    S2 = 1 - S1
    return S1, S2

def tirer_bernoulli(p):
    """Tirage aléatoire Bernoulli."""
    return np.random.binomial(1, p)
