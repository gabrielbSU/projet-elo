import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from .joueur import Joueur

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