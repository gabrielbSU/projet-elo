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
    elo1 = joueur1.histo_elo_estimation[-1]
    elo2 = joueur2.histo_elo_estimation[-1]

    P1 = get_proba_estime(elo1, elo2)

    if P1 > 0.5:
        return 1, 0
    elif P1 < 0.5:
        return 0, 1
    else:
        # En cas d'égalité parfaite, tirage aléatoire
        return tirage_bernoulli(0.5), tirage_bernoulli(0.5)


def mettre_a_jour_elo_estime(joueur1, joueur2,S1,S2):
    """
    Met à jour l'Elo des deux joueurs après leur rencontre simulée sur base des Elos.
    """
    elo1_last = joueur1.histo_elo_estimation[-1]
    elo2_last = joueur2.histo_elo_estimation[-1]

    P1 = get_proba_estime(elo1_last, elo2_last)
    P2 = 1 - P1
    
    new_elo1 = elo1_last + K * (S1 - P1)
    new_elo2 = elo2_last + K * (S2 - P2)

    joueur1.histo_partie = S1
    joueur2.histo_partie = S2

    joueur1.histo_elo_estimation = new_elo1
    joueur2.histo_elo_estimation = new_elo2


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


def g(rating):
    return 1 / math.sqrt(1 + (3 * Q**2 * rating**2) / math.pi**2)


def E(r, ri, rdi):
    """E est la proba de victoire du joueur avec rating r contre un joueur avec rating ri et RD rdi."""
    return 1 / (1 + 10 ** (g(rdi) * (ri - r) / 400))


def mettre_a_jour_glicko(joueur, adversaires_info, date):
    if joueur.histo_glicko:
        r, rd = joueur.histo_glicko[-1][:2]
    else:
        r, rd = RATING_INIT, RD_INIT

    if not adversaires_info:
        rd = min(math.sqrt(rd**2 + 50**2), RD_INIT)
        joueur.histo_glicko.append((r, rd, date))
        return

    d2_inv = sum((Q**2) * g(rdi)**2 * E(r, ri, rdi) * (1 - E(r, ri, rdi)) for ri, rdi, score in adversaires_info)
    d2 = 1 / d2_inv
    delta = d2 * sum(Q * g(rdi) * (score - E(r, ri, rdi)) for ri, rdi, score in adversaires_info)
    rd_new = 1 / math.sqrt((1 / rd**2) + (1 / d2))
    r_new = r + Q / ((1 / rd**2) + (1 / d2)) * sum(g(rdi) * (score - E(r, ri, rdi)) for ri, rdi, score in adversaires_info)
    joueur.histo_glicko.append((r_new, rd_new, date))


def update_glicko_all_players(joueurs, matchs, date):
    infos = {j.id: [] for j in joueurs}
    for j1, j2, s1, s2 in matchs:
        r2, rd2 = j2.histo_glicko[-1][:2] if j2.histo_glicko else (RATING_INIT, RD_INIT)
        r1, rd1 = j1.histo_glicko[-1][:2] if j1.histo_glicko else (RATING_INIT, RD_INIT)
        infos[j1.id].append((r2, rd2, s1))
        infos[j2.id].append((r1, rd1, s2))
    for j in joueurs:
        mettre_a_jour_glicko(j, infos[j.id], date)
