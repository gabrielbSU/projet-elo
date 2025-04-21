from .joueur import get_proba_modele1, get_proba_modele2 
from .jeu import Jeu
from .outils import sigmoid
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import MaxNLocator


def tracer_competences(joueurs):
    """
    Trace l'histogramme des compétences des joueurs.
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
    plt.title("Distribution des compétences des joueurs")
    plt.xlabel("Compétences")
    plt.ylabel("Fréquence")
    plt.legend()
    plt.grid(True)
    plt.show()

def tracer_elo(joueurs):
    """
    Trace l'histogramme des derniers Elo des joueurs.
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
    
    plt.title("Distribution des derniers Elo des joueurs")
    plt.xlabel("Elo")
    plt.ylabel("Fréquence")
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

    plt.xlabel("Force du joueur")
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


def tracer_isocontours_force(jeu, impact_hasard=None, modele=1):
    """
    Trace les isocontours de la probabilité de victoire du joueur 1
    en fonction des forces f1 et f2 pour un jeu donné.
    """
    
    # Création d'un grid de valeurs pour f1 et f2
    f = np.linspace(0, 1, 100)
    f1, f2 = np.meshgrid(f, f)
    
    # Calcul des probabilités selon le modèle choisi
    if modele == 1:
        probas = np.zeros_like(f1)
        for i in range(f1.shape[0]):
            for j in range(f1.shape[1]):
                probas[i,j] = get_proba_modele1(f1[i,j], f2[i,j], jeu)
        title = f"Isocontours - Modèle 1\nTaux hasard: {jeu.taux_de_hasard}, Impact: {impact_hasard}"
    else:
        # Pour le modèle 2 on convertit les forces en Elo (linéairement entre 1000 et 2000)
        elo1 = 1000 + 1000 * f1
        elo2 = 1000 + 1000 * f2
        probas = 1 / (1 + 10**((elo2 - elo1)/400))
        title = f"Isocontours - Modèle 2 (basé sur Elo)"
    
    # Création de la figure
    plt.figure(figsize=(12, 8))
    
    # Tracé des isocontours
    levels = np.linspace(0, 1, 11)
    cs = plt.contourf(f1, f2, probas, levels=levels, cmap=cm.coolwarm)
    plt.colorbar(cs, label='Probabilité victoire Joueur 1')
    
    # Contour de la ligne d'équiprobabilité
    plt.contour(f1, f2, probas, levels=[0.5], colors='black', linewidths=2)
    
    # Configuration du graphique
    plt.title(title)
    plt.xlabel('Force Joueur 1 (f1)')
    plt.ylabel('Force Joueur 2 (f2)')
    plt.grid(True)
    
    # Ligne d'égalité
    plt.plot([0, 1], [0, 1], 'k--', alpha=0.5, label='f1 = f2')
    plt.legend()
    
    plt.show()

def visualiser_3d_force(jeu, impact_hasard=None, modele=1):
    """
    Visualisation 3D de la surface de probabilité en fonction de f1 et f2.
    """
    
    # Création du grid
    f = np.linspace(0, 1, 50)
    f1, f2 = np.meshgrid(f, f)
    
    # Calcul des probabilités
    if modele == 1:
        probas = np.zeros_like(f1)
        for i in range(f1.shape[0]):
            for j in range(f1.shape[1]):
                probas[i,j] = get_proba_modele1(f1[i,j], f2[i,j], jeu)
        title = f"Surface Probabilité - Modèle 1\nTaux hasard: {jeu.taux_de_hasard}, Impact: {impact_hasard}"
    else:
        elo1 = 1000 + 1000 * f1
        elo2 = 1000 + 1000 * f2
        probas = 1 / (1 + 10**((elo2 - elo1)/400))
        title = f"Surface Probabilité - Modèle 2 (basé sur Elo)"
    
    # Création de la figure 3D
    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # Tracé de la surface
    surf = ax.plot_surface(f1, f2, probas, cmap=cm.coolwarm,
                         linewidth=0, antialiased=True, alpha=0.8)
    
    # Configuration
    ax.set_title(title)
    ax.set_xlabel('Force Joueur 1 (f1)')
    ax.set_ylabel('Force Joueur 2 (f2)')
    ax.set_zlabel('P(victoire J1)')
    fig.colorbar(surf, shrink=0.5, aspect=5)
    
    plt.show()


def tracer_isocontours_impact_variable(taux_de_hasard, impacts=[0.1, 0.5, 1.0, 2.0], n_levels=11):
    """
    Trace plusieurs graphiques d'isocontours pour un même taux de hasard 
    mais avec différents impacts.
    """
    
    # Création du grid de valeurs
    f = np.linspace(0, 1, 100)
    f1, f2 = np.meshgrid(f, f)
    
    # Configuration de la figure
    n_impacts = len(impacts)
    fig, axes = plt.subplots(1, n_impacts, figsize=(6*n_impacts, 5), 
                            sharey=True, squeeze=False)
    axes = axes.flatten()
    
    # Niveaux communs pour tous les plots
    levels = np.linspace(0, 1, n_levels)
    
    for ax, impact in zip(axes, impacts):
        # Création d'un jeu temporaire avec l'impact courant
        jeu_temp = Jeu("Temp", taux_de_hasard, impact)
        
        # Calcul des probabilités
        probas = np.zeros_like(f1)
        for i in range(f1.shape[0]):
            for j in range(f1.shape[1]):
                probas[i,j] = get_proba_modele1(f1[i,j], f2[i,j], jeu_temp)
        
        # Tracé des isocontours
        cs = ax.contourf(f1, f2, probas, levels=levels, cmap=cm.coolwarm)
        ax.contour(f1, f2, probas, levels=[0.5], colors='black', linewidths=2)
        ax.plot([0, 1], [0, 1], 'k--', alpha=0.5)
        
        # Configuration
        ax.set_title(f"Impact = {impact}")
        ax.set_xlabel('Force Joueur 1 (f1)')
        if ax == axes[0]:
            ax.set_ylabel('Force Joueur 2 (f2)')
        ax.grid(True)
    
    # Barre de couleur commune
    fig.colorbar(cs, ax=axes.tolist(), label='Probabilité victoire Joueur 1', 
                fraction=0.02, pad=0.04)
    
    plt.suptitle(f"Évolution des isocontours pour taux de hasard = {taux_de_hasard}", y=1.05)
    plt.tight_layout()
    plt.show()


def tracer_isocontours_hasard(taux_de_hasard, impacts=None, n_points=100):
    """
    Trace les isocontours en gérant spécifiquement les forts taux de hasard.
    """
    if impacts is None:
        if taux_de_hasard < 0.3:
            impacts = [0.5, 1.0, 2.0, 5.0]  # Impacts forts pour jeux stratégiques
        elif taux_de_hasard < 0.7:
            impacts = [0.2, 0.5, 1.0, 2.0]  # Plage standard
        else:
            impacts = [0.1, 0.3, 0.7, 1.0]  # Impacts faibles pour jeux aléatoires
    
    f = np.linspace(0, 1, n_points)
    f1, f2 = np.meshgrid(f, f)
    
    fig, axes = plt.subplots(1, len(impacts), figsize=(len(impacts)*4, 4.5),
                         sharey=True)
    if len(impacts) == 1:
        axes = [axes]
    
    # Niveaux dynamiques selon le taux de hasard
    if taux_de_hasard > 0.8:
        levels = np.linspace(0.4, 0.6, 11)  # Zoom autour de 0.5
    elif taux_de_hasard > 0.5:
        levels = np.linspace(0.3, 0.7, 11)
    else:
        levels = np.linspace(0, 1, 11)
    
    for ax, impact in zip(axes, impacts):
        jeu_temp = Jeu("Temp", taux_de_hasard, impact)
        
        # Version vectorisée pour la performance
        probas = np.vectorize(lambda x,y: get_proba_modele1(x,y,jeu_temp))(f1,f2)
        
        # Contrôle dynamique de la plage de couleurs
        if taux_de_hasard > 0.7:
            vmin, vmax = 0.4, 0.6
        elif taux_de_hasard > 0.4:
            vmin, vmax = 0.2, 0.8
        else:
            vmin, vmax = 0, 1
        
        cs = ax.contourf(f1, f2, probas, levels=levels, cmap=cm.coolwarm,
                        vmin=vmin, vmax=vmax)
        
        # Ligne d'équiprobabilité en gras
        ax.contour(f1, f2, probas, levels=[0.5], colors='black', linewidths=2)
        ax.plot([0,1], [0,1], 'k--', alpha=0.5)
        
        ax.set_title(f"Impact = {impact}")
        ax.set_xlabel('Force Joueur 1')
        ax.xaxis.set_major_locator(MaxNLocator(5))
        ax.yaxis.set_major_locator(MaxNLocator(5))
    
    axes[0].set_ylabel('Force Joueur 2')
    
    # Barre de couleur commune avec format adaptatif
    cb = fig.colorbar(cs, ax=axes, shrink=0.8)
    if taux_de_hasard > 0.7:
        cb.set_ticks(np.linspace(0.4, 0.6, 5))
    cb.set_label('Probabilité victoire J1')
    
    plt.suptitle(f"Taux de hasard = {taux_de_hasard:.2f}", y=1.05)
    plt.tight_layout()
    plt.show()