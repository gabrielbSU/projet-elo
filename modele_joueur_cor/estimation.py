import random
from modele_joueur_cor.simu import tirage_bernoulli

from constantes import K

def get_proba_estime(elo1, elo2):
    """
    Calcule la probabilité de victoire du joueur1 sur joueur2 selon leur Elo.
    """
    diff = elo2 - elo1
    return 1 / (1 + 10 ** (diff / 400))


def rencontre_elo_estime(joueur1, joueur2):
    """
    Simule une partie entre deux joueurs selon leurs Elos uniquement.
    Retourne le score sous forme (S1, S2).
    """
    elo1 = joueur1.histo_elo[-1]
    elo2 = joueur2.histo_elo[-1]

    P1 = get_proba_estime(elo1, elo2)

    if P1 > 0.5:
        return 1, 0
    elif P1 < 0.5:
        return 0, 1
    else:
        # En cas d'égalité parfaite, tirage aléatoire
        return tirage_bernoulli(0.5), tirage_bernoulli(0.5)


def mettre_a_jour_elo_estime(joueur1, joueur2):
    """
    Met à jour l'Elo des deux joueurs après leur rencontre simulée sur base des Elos.
    """
    elo1_last = joueur1.histo_elo[-1]
    elo2_last = joueur2.histo_elo[-1]

    P1 = get_proba_estime(elo1_last, elo2_last)
    P2 = 1 - P1

    S1, S2 = rencontre_elo_estime(joueur1, joueur2)

    new_elo1 = elo1_last + K * (S1 - P1)
    new_elo2 = elo2_last + K * (S2 - P2)

    joueur1.histo_partie = S1
    joueur2.histo_partie = S2

    joueur1.histo_elo = new_elo1
    joueur2.histo_elo = new_elo2


def vraisemblance_estime_elo(joueurs, n_parties):
    """
    Calcule la vraisemblance globale d'un ensemble de rencontres entre joueurs selon leur Elo.
    """
    vraisemblance_totale = 1.0

    for _ in range(n_parties):
        joueur1, joueur2 = random.sample(joueurs, 2)

        P1 = get_proba_estime(joueur1.histo_elo[-1], joueur2.histo_elo[-1])
        P2 = 1 - P1

        S1 = tirage_bernoulli(P1)
        S2 = 1 - S1

        vraisemblance_totale *= P1**S1 * P2**S2

        mettre_a_jour_elo_estime(joueur1, joueur2)

    return vraisemblance_totale
