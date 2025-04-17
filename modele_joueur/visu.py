import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from .joueur import Joueur, rencontre_sigmoide, ajuster_impact_hasard
from .outils import sigmoid

def tracer_competences(joueurs):
    """
    Trace l'histogramme et la densité des compétences des joueurs.
    """
    if not joueurs:
        print("Aucun joueur à afficher.")
        return

    competences = [comp for joueur in joueurs for comp in joueur.comp if isinstance(comp, (int, float))]

    if not competences:
        print("Aucune compétence valide à afficher.")
        return

    plt.figure(figsize=(10, 6))
    sns.histplot(competences, bins=20, color='blue', alpha=0.5, label='Histogramme', kde=True)
    sns.kdeplot(competences, color='red', label='Densité', linewidth=2)
    
    plt.title("Distribution des compétences des joueurs")
    plt.xlabel("Compétences")
    plt.ylabel("Fréquence / Densité")
    plt.legend()
    plt.grid(True)
    plt.show()

def tracer_elo(joueurs):
    """
    Trace l'histogramme et la densité des derniers Elo des joueurs.
    """
    if not joueurs:
        print("Aucun joueur à afficher.")
        return

    elo = [joueur.histo_elo[-1] for joueur in joueurs if joueur.histo_elo]

    if not elo:
        print("Aucun Elo valide à afficher.")
        return

    plt.figure(figsize=(10, 6))
    sns.histplot(elo, bins=20, color='green', alpha=0.5, label='Histogramme', kde=True)
    sns.kdeplot(elo, color='orange', label='Densité', linewidth=2)
    
    plt.title("Distribution des derniers Elo des joueurs")
    plt.xlabel("Elo")
    plt.ylabel("Fréquence / Densité")
    plt.legend()
    plt.grid(True)
    plt.show()

def tracer_force_elo(joueurs):
    """
    Trace un graphique montrant la relation entre la force des joueurs et leur dernier Elo.
    
    Paramètres :
    - joueurs : liste d'objets Joueur
    """
    forces = [joueur.force_joueur() for joueur in joueurs]
    elos = [joueur.histo_elo[-1] for joueur in joueurs if joueur.histo_elo]

    if not elos:
        print("Aucun Elo valide à afficher.")
        return

    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=forces, y=elos, alpha=0.7)

    plt.xlabel("Force du joueur (entre 0 et 1)")
    plt.ylabel("Dernier Elo du joueur")
    plt.title("Relation entre la force et le dernier Elo des joueurs")
    plt.grid(True)

    plt.show()

def tracer_evolution_elo(joueur):
    """
    Trace l'évolution de l'Elo d'un joueur au fil du temps.
    
    Paramètres :
    - joueur : objet de la classe Joueur
    """
    if not joueur.histo_elo:
        print(f"Aucun historique Elo pour {joueur.nom} {joueur.prenom}.")
        return

    plt.figure(figsize=(10, 6))
    plt.plot(joueur.histo_elo, marker='o', linestyle='-', color='b', label="Évolution de l'Elo")
    
    plt.xlabel("Nombre de parties")
    plt.ylabel("Elo")
    plt.title(f"Évolution de l'Elo de {joueur.nom} {joueur.prenom}")
    plt.legend()
    plt.grid(True)
    
    plt.show()

def tracer_comparaison_evolution_elo(joueurs):
    """
    Trace l'évolution de l'Elo de plusieurs joueurs sur le même graphique.

    Paramètres :
    - joueurs : liste d'objets Joueur
    """
    if not joueurs:
        print("Aucun joueur à afficher.")
        return

    plt.figure(figsize=(12, 7))

    for joueur in joueurs:
        if joueur.histo_elo:  # Vérifie que l'historique n'est pas vide
            plt.plot(joueur.histo_elo, marker='o', linestyle='-', label=f"{joueur.nom} {joueur.prenom}")

    plt.xlabel("Nombre de parties")
    plt.ylabel("Elo")
    plt.title("Évolution de l'Elo des joueurs")
    plt.legend()
    plt.grid(True)

    plt.show()

def visualiser_plusieurs_sigmoides(k_list=[5, 10, 20, 50]):
    """
    Trace plusieurs fonctions sigmoïdes pour différentes valeurs de k.
    
    :param k_list: Liste des coefficients k à tracer.
    """
    x = np.linspace(-1, 1, 500)  # Différence de force de -1 à 1

    plt.figure(figsize=(10, 6))
    
    for k in k_list:
        y = sigmoid(x, k)
        plt.plot(x, y, label=f'k = {k}')
    
    plt.title("Comparaison de plusieurs sigmoïdes (effet du paramètre k)")
    plt.xlabel("Différence de force (force joueur 1 - force joueur 2)")
    plt.ylabel("Probabilité de victoire pour Joueur 1")
    plt.legend()
    plt.grid(True)
    plt.show()

def visualiser_sigmoide_rencontre(joueur1, joueur2, jeu):
    """
    Visualise la courbe sigmoïde utilisée pour déterminer la probabilité de victoire
    entre joueur1 et joueur2, en tenant compte du lissage par l'impact du hasard.
    """
    # 1. Calcul du facteur de hasard k comme dans rencontre_sigmoide
    f1 = joueur1.force_joueur()
    f2 = joueur2.force_joueur()
    
    # Calcule du k_hasard utilisé
    k_hasard = ajuster_impact_hasard(joueur1, joueur2, jeu) * (1 + abs(f1 - f2))

    # 2. Génération de la courbe
    x = np.linspace(-1, 1, 500)  # Différence de force : f1 - f2
    y = sigmoid(x, k=k_hasard)

    # 3. Affichage
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, label=f'Sigmoïde lissée avec k = {k_hasard:.2f}')
    plt.title("Sigmoïde réelle utilisée dans 'rencontre_sigmoide'")
    plt.xlabel("Différence de forces (Joueur 1 - Joueur 2)")
    plt.ylabel("Probabilité de victoire du Joueur 1")
    plt.grid(True)
    plt.legend()
    plt.show()

def visualiser_sigmoides_multiples(liste_paires_joueurs, jeu):
    """
    Visualise plusieurs courbes sigmoïdes correspondant à plusieurs paires de joueurs,
    tenant compte du lissage par l'impact du hasard.

    liste_paires_joueurs : liste de tuples (joueur1, joueur2)
    jeu : instance du jeu
    """
    x = np.linspace(-1, 1, 500)  # Intervalle des différences de forces

    plt.figure(figsize=(12, 8))
    
    for idx, (joueur1, joueur2) in enumerate(liste_paires_joueurs):
        # Calcul du k_hasard propre à la paire
        f1 = joueur1.force_joueur()
        f2 = joueur2.force_joueur()
        k_hasard = ajuster_impact_hasard(joueur1, joueur2, jeu) * (1 + abs(f1 - f2))

        # Calcul de la courbe
        y = sigmoid(x, k=k_hasard)
        
        # Nom pour la légende
        label = f"{joueur1.nom} vs {joueur2.nom} (k={k_hasard:.2f})"
        plt.plot(x, y, label=label)

    plt.title("Comparaison des sigmoïdes lissées pour plusieurs paires de joueurs")
    plt.xlabel("Différence de forces (Joueur 1 - Joueur 2)")
    plt.ylabel("Probabilité de victoire du Joueur 1")
    plt.grid(True)
    plt.legend()
    plt.show()