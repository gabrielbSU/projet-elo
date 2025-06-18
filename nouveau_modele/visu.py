import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import spearmanr, mannwhitneyu, wilcoxon
import pandas as pd


def tracer_elo(joueurs, mode="simu"):
    if mode == "simu":
        elos = [j.elo.rating for j in joueurs]
    else:
        print("Mode inconnu pour Elo.")
        return

    plt.figure(figsize=(10, 6))
    sns.histplot(elos, bins=20, kde=True, color='skyblue')
    plt.title(f"Distribution des Elos ({mode})")
    plt.xlabel("Elo")
    plt.ylabel("Fréquence")
    plt.grid(True)
    plt.show()


def tracer_glicko(joueurs, mode="simu"):
    if mode == "simu":
        ratings = [j.glicko.get_rating()[0] for j in joueurs]
    else:
        print("Mode inconnu pour Glicko.")
        return

    plt.figure(figsize=(10, 6))
    sns.histplot(ratings, bins=20, kde=True, color='orange')
    plt.title(f"Distribution des Ratings Glicko ({mode})")
    plt.xlabel("Rating")
    plt.ylabel("Fréquence")
    plt.grid(True)
    plt.show()


def tracer_glicko2(joueurs, mode="simu"):
    if mode == "simu":
        ratings = [j.glicko2.get_rating()[0] for j in joueurs]
    else:
        print("Mode inconnu pour Glicko-2.")
        return

    plt.figure(figsize=(10, 6))
    sns.histplot(ratings, bins=20, kde=True, color='green')
    plt.title(f"Distribution des Ratings Glicko-2 ({mode})")
    plt.xlabel("Rating")
    plt.ylabel("Fréquence")
    plt.grid(True)
    plt.show()


def tracer_evolution_elo(joueur):
    elos = joueur.elo.historique
    plt.figure(figsize=(10, 6))
    plt.plot(elos, marker='o', linestyle='-', color='b', label="Évolution de l'Elo")
    plt.xlabel("Nombre de parties")
    plt.ylabel("Elo")
    plt.title(f"Évolution de l'Elo du joueur {joueur.id}")
    plt.legend()
    plt.grid(True)
    plt.show()


def tracer_evolution_glicko(joueur):
    ratings = [r for r, _ in joueur.glicko.historique]
    plt.figure(figsize=(10, 6))
    plt.plot(ratings, marker='o', linestyle='-', color='orange', label="Glicko")
    plt.xlabel("Nombre de parties")
    plt.ylabel("Rating Glicko")
    plt.title(f"Évolution du rating Glicko du joueur {joueur.id}")
    plt.legend()
    plt.grid(True)
    plt.show()


def tracer_evolution_glicko2(joueur):
    ratings = [r for r, _ in joueur.glicko2.historique]
    plt.figure(figsize=(10, 6))
    plt.plot(ratings, marker='o', linestyle='-', color='green', label="Glicko-2")
    plt.xlabel("Nombre de parties")
    plt.ylabel("Rating Glicko-2")
    plt.title(f"Évolution du rating Glicko-2 du joueur {joueur.id}")
    plt.legend()
    plt.grid(True)
    plt.show()


def tracer_correlation_force_elo(joueurs):
    forces = [j.force for j in joueurs]
    elos = [j.elo.rating for j in joueurs]
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=forces, y=elos)
    sns.regplot(x=forces, y=elos, scatter=False, color='red', label='Régression')
    plt.xlabel("Force réelle")
    plt.ylabel("Elo estimé")
    plt.title("Corrélation entre la force réelle et l'Elo")
    plt.legend()
    plt.grid(True)
    plt.show()


def tracer_correlation_force_glicko(joueurs):
    forces = [j.force for j in joueurs]
    ratings = [j.glicko.get_rating()[0] for j in joueurs]
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=forces, y=ratings)
    sns.regplot(x=forces, y=ratings, scatter=False, color='orange', label='Régression')
    plt.xlabel("Force réelle")
    plt.ylabel("Rating Glicko")
    plt.title("Corrélation entre la force réelle et le rating Glicko")
    plt.legend()
    plt.grid(True)
    plt.show()


def tracer_correlation_force_glicko2(joueurs):
    forces = [j.force for j in joueurs]
    ratings = [j.glicko2.get_rating()[0] for j in joueurs]
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=forces, y=ratings)
    sns.regplot(x=forces, y=ratings, scatter=False, color='green', label='Régression')
    plt.xlabel("Force réelle")
    plt.ylabel("Rating Glicko-2")
    plt.title("Corrélation entre la force réelle et le rating Glicko-2")
    plt.legend()
    plt.grid(True)
    plt.show()


def afficher_spearman(joueurs, systeme="elo"):
    if systeme == "elo":
        notes = [j.elo.rating for j in joueurs]
    elif systeme == "glicko":
        notes = [j.glicko.get_rating()[0] for j in joueurs]
    elif systeme == "glicko2":
        notes = [j.glicko2.get_rating()[0] for j in joueurs]
    else:
        raise ValueError("Système inconnu. Utilisez 'elo', 'glicko' ou 'glicko2'.")

    forces = [j.force for j in joueurs]
    coeff, p_value = spearmanr(forces, notes)

    print(f"Spearman's rank correlation ({systeme}) : {coeff:.4f} (p-value = {p_value:.4g})")



def comparer_groupes_mannwhitney(joueurs, seuil_force=0.5, systeme="elo"):
    """
    Compare les ratings de deux groupes de joueurs (forts vs faibles) via le test de Mann-Whitney.
    """
    if systeme == "elo":
        notes = [j.elo.rating for j in joueurs]
    elif systeme == "glicko":
        notes = [j.glicko.get_rating()[0] for j in joueurs]
    elif systeme == "glicko2":
        notes = [j.glicko2.get_rating()[0] for j in joueurs]
    else:
        raise ValueError("Système inconnu. Utilisez 'elo', 'glicko' ou 'glicko2'.")

    groupes_forts = [note for j, note in zip(joueurs, notes) if j.force > seuil_force]
    groupes_faibles = [note for j, note in zip(joueurs, notes) if j.force <= seuil_force]

    stat, p = mannwhitneyu(groupes_forts, groupes_faibles, alternative='two-sided')

    print(f"Test de Mann–Whitney ({systeme}) : U = {stat:.2f}, p-value = {p:.4f}")
    if p < 0.05:
        print("Différence significative entre les deux groupes.")
    else:
        print("Pas de différence significative entre les groupes.")


def tester_diff_elo_glicko(joueurs):
    from scipy.stats import wilcoxon
    elos = [j.elo.rating for j in joueurs]
    glickos = [j.glicko.get_rating()[0] for j in joueurs]
    try:
        stat, p = wilcoxon(elos, glickos)
        print(f"Wilcoxon test Elo vs Glicko : W = {stat:.2f}, p-value = {p:.4f}")
        if p < 0.05:
            print("Différence significative entre Elo et Glicko.")
        else:
            print("Pas de différence significative entre Elo et Glicko.")
    except ValueError as e:
        print(f"Erreur dans le test Elo vs Glicko : {e}")


def tester_diff_elo_glicko2(joueurs):
    from scipy.stats import wilcoxon
    elos = [j.elo.rating for j in joueurs]
    glicko2s = [j.glicko2.get_rating()[0] for j in joueurs]
    try:
        stat, p = wilcoxon(elos, glicko2s)
        print(f"Wilcoxon test Elo vs Glicko-2 : W = {stat:.2f}, p-value = {p:.4f}")
        if p < 0.05:
            print("Différence significative entre Elo et Glicko-2.")
        else:
            print("Pas de différence significative entre Elo et Glicko-2.")
    except ValueError as e:
        print(f"Erreur dans le test Elo vs Glicko-2 : {e}")


def tester_diff_glicko_glicko2(joueurs):
    from scipy.stats import wilcoxon
    glickos = [j.glicko.get_rating()[0] for j in joueurs]
    glicko2s = [j.glicko2.get_rating()[0] for j in joueurs]
    try:
        stat, p = wilcoxon(glickos, glicko2s)
        print(f"Wilcoxon test Glicko vs Glicko-2 : W = {stat:.2f}, p-value = {p:.4f}")
        if p < 0.05:
            print("Différence significative entre Glicko et Glicko-2.")
        else:
            print("Pas de différence significative entre Glicko et Glicko-2.")
    except ValueError as e:
        print(f"Erreur dans le test Glicko vs Glicko-2 : {e}")


def tracer_comparaison_boxplot(joueurs):
    data = {
        "Elo": [j.elo.rating for j in joueurs],
        "Glicko": [j.glicko.get_rating()[0] for j in joueurs],
        "Glicko-2": [j.glicko2.get_rating()[0] for j in joueurs]
    }
    df = pd.DataFrame(data)
    sns.boxplot(data=df)
    plt.title("Comparaison des distributions : Elo vs Glicko vs Glicko-2")
    plt.ylabel("Rating")
    plt.grid(True)
    plt.show()


def tracer_comparaisons_scatter(joueurs):
    elo = [j.elo.rating for j in joueurs]
    glicko = [j.glicko.get_rating()[0] for j in joueurs]
    glicko2 = [j.glicko2.get_rating()[0] for j in joueurs]

    plt.figure(figsize=(16, 5))

    plt.subplot(1, 3, 1)
    sns.scatterplot(x=elo, y=glicko)
    plt.xlabel("Elo")
    plt.ylabel("Glicko")
    plt.title("Elo vs Glicko")
    plt.grid(True)

    plt.subplot(1, 3, 2)
    sns.scatterplot(x=elo, y=glicko2)
    plt.xlabel("Elo")
    plt.ylabel("Glicko-2")
    plt.title("Elo vs Glicko-2")
    plt.grid(True)

    plt.subplot(1, 3, 3)
    sns.scatterplot(x=glicko, y=glicko2)
    plt.xlabel("Glicko")
    plt.ylabel("Glicko-2")
    plt.title("Glicko vs Glicko-2")
    plt.grid(True)

    plt.tight_layout()
    plt.show()
