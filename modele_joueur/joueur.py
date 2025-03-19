import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import random
import math
import seaborn as sns
from .outils import tirage_victoire_log_normal, tirage_victoire_sigmoide

K = 30 #Facteur de dévellopement (il nous permet de moduler l'impact d'un match sur l'elo d'un joueur)

class Joueur:
    """
    Cette classe permet de modéliser un joueur. 
    On supposera que le jeu est un jeu individuel donc un joueur est un objet unique de la classe Joueur.
    """

    def __init__(self, nom, prenom, age, comp, histo_partie, histo_tournoi, elo):
        self.nom = nom
        self.prenom = prenom
        self.age = age
        self.comp = comp  # comp est une liste de 5 compétences dont le coeff est la position dans la liste. Chaque compétence prend une valeur entre 0 et 10
        self.histo_partie = histo_partie  # Liste des résultats des parties (0 défaite, 1: victoire)
        self.histo_tournoi = histo_tournoi  # Liste des résultats des tournois
        self.elo = elo  # ELO du joueur compris entre 0 et 3000

    def categorie(self):
        """
        Retourne la catégorie du joueur en fonction de son elo.
        """
        if self.elo < 1200:
            return "Débutant"
        elif self.elo < 1600:
            return "Intermédiaire"
        elif self.elo < 2000:
            return "Avancé"
        elif self.elo < 2400:
            return "Expert"
        else:
            return "Maître"

    def __str__(self):
        """
        Affiche les informations du joueur.
        """
        print(f"Nom : {self.nom}")
        print(f"Prénom : {self.prenom}")
        print(f"Age : {self.age}")
        print(f"Compétences : {self.comp}")
        print(f"Elo : {self.elo}")
        print(f"Historique des parties : {self.histo_partie}")
        print(f"Historique des tournois : {self.histo_tournoi}")

    def force_joueur(self):
        """
        Retourne la force d'un joueur entre 0 et 1.
        """
        tot = 0
        for i in range(len(self.comp)):
            tot += self.comp[i] * (i + 1)
        return float(tot) / 150
    
    
def generer_joueur(nom, prenom):
    """
    Génère un joueur avec des caractéristiques aléatoires selon différentes distributions :
    Compétences : log-normale (plus adapté qu'une gaussienne car on a plus de joueurs faibles et moyens que fort).
    Age : gaussienne
    elo : log-normale (plus adapté qu'une gaussienne car on a plus de joueurs faibles et moyens que fort).
    Il est important de noter que la génération des compétences et indépendante de celle de l'elo.
    """
    # Génération de l'âge (entre 15 et 40 ans)
    age = int(np.random.normal(loc=25, scale=5))  # Moyenne = 25, écart-type = 5
    age = max(15, min(age, 40))  # On s'assure que l'âge reste dans [15, 40]

    # Génération des compétences (5 compétences entre 0 et 10)
    comp = []
    for _ in range(5):
        competence = np.random.lognormal(mean=1.0, sigma=0.5)
        # Normalisation pour avoir une valeur entre 0 et 10
        competence = max(0, min(competence, 10))
        comp.append(round(competence, 1))



    # Historique des parties et tournois (initialement vides)
    histo_partie = []
    histo_tournoi = []
    elo = 1500 # on initialise l'elo à 1500, valeur moyenne entre 0 et 3000

    return Joueur(nom, prenom, age, comp, histo_partie, histo_tournoi, elo)


def tracer_competences(joueurs):
    """
    Trace l'histogramme et la densité des compétences des joueurs.
    """
    # On récupére les compétences de tous les joueurs
    competences = []
    for joueur in joueurs:
        competences.extend(joueur.comp)  # On ajoute toutes les compétences de chaque joueur

    # Création du graphique
    plt.figure(figsize=(10, 6))
    
    # Histogramme des compétences
    sns.histplot(competences, bins=20, color='blue', alpha=0.5, label='Histogramme', kde=True)
    
    # Courbe de densité des compétences
    sns.kdeplot(competences, color='red', label='Densité', linewidth=2)
    
    # Ajout des labels et de la légende
    plt.title("Distribution des compétences des joueurs")
    plt.xlabel("Compétences")
    plt.ylabel("Fréquence / Densité")
    plt.legend()
    plt.grid(True)
    plt.show()

def tracer_elo(joueurs):
    """
    Trace l'histogramme et la densité des elo des joueurs.
    """
    # On récupére les elos de tous les joueurs
    elo = [joueur.elo for joueur in joueurs]

    # Création du graphique
    plt.figure(figsize=(10, 6))
    
    # Histogramme des elo
    sns.histplot(elo, bins=20, color='green', alpha=0.5, label='Histogramme', kde=True)
    
    # Courbe de densité des elo
    sns.kdeplot(elo, color='orange', label='Densité', linewidth=2)
    
    # Ajout des labels et de la légende
    plt.title("Distribution des elo des joueurs")
    plt.xlabel("Elo")
    plt.ylabel("Fréquence / Densité")
    plt.legend()
    plt.grid(True)
    plt.show()

def tracer_competences_et_elo(joueurs):
    """
    Trace les densités des compétences et des elo sur le même graphique.
    """
    # On récupére les compétences et des elo
    competences = []
    elo = []
    for joueur in joueurs:
        competences.extend(joueur.comp)
        elo.append(joueur.elo)

    # Création du graphique
    plt.figure(figsize=(10, 6))
    
    # Densité des compétences
    sns.kdeplot(competences, color='blue', label='Compétences', linewidth=2)
    
    # Densité des elo
    sns.kdeplot(elo, color='green', label='Elo', linewidth=2)
    
    # Ajout des labels et de la légende
    plt.title("Comparaison des densités des compétences et des elo")
    plt.xlabel("Valeur")
    plt.ylabel("Densité")
    plt.legend()
    plt.grid(True)
    plt.show()

#Dans la fonction de rencontre suivante, on a choisit de modéliser la probabilité de victoire par une loi sigmoide.
#Cette loi est plus adaptée pour une répartition homogène du hasard
def rencontre_sigmoide(joueur1, joueur2):
    """
    Simule une partie entre deux joueurs et met à jour :
    - leurs elos respectifs.
    - leurs historiques de parties. 
    """
    f1, f2 = joueur1.force_joueur(), joueur2.force_joueur()

    # Calcul du gagnant de la partie et du perdant de la partie
    (P1,P2) = tirage_victoire_sigmoide(f1, f2)

    # Tirage final selon les probabilités calculées avec un facteur de hasard
    tirage = np.random.rand()  # Tirage aléatoire entre 0 et 1
    if tirage < P1:
        S1 = 1  # Joueur 1 gagne
        S2 = 0  # Joueur 2 perd
    else:
        S1 = 0  # Joueur 1 perd
        S2 = 1  # Joueur 2 gagne

    # Mise à jour de l'elo
    joueur1.elo = joueur1.elo + K * (S1 - P1)
    joueur2.elo = joueur2.elo + K * (S2 - P2)

    # Mise à jour de l'historique des parties
    joueur1.histo_partie.append(S1)
    joueur2.histo_partie.append(S2)



#Dans la fonction de rencontre suivante, on a choisit de modéliser la probabilité de victoire par une loi log-normale.
#Cette loi est plus adaptée pour modéliser la probabilité de victoire d'un joueur en fonction de sa force.
def rencontre_log_normale(joueur1, joueur2):
    """
    Simule une partie entre deux joueurs et met à jour :
    - leurs elos respectifs.
    - leurs historiques de parties. 
    """
    f1, f2 = joueur1.force_joueur(), joueur2.force_joueur()

    # Calcul du gagnant de la partie et du perdant de la partie
    (P1,P2) = tirage_victoire_log_normale(f1, f2)

    # Tirage final selon les probabilités calculées avec un facteur de hasard
    tirage = np.random.rand()  # Tirage aléatoire entre 0 et 1
    if tirage < P1:
        S1 = 1  # Joueur 1 gagne
        S2 = 0  # Joueur 2 perd
    else:
        S1 = 0  # Joueur 1 perd
        S2 = 1  # Joueur 2 gagne

    # Mise à jour de l'elo
    joueur1.elo = joueur1.elo + K * (S1 - P1)
    joueur2.elo = joueur2.elo + K * (S2 - P2)

    # Mise à jour de l'historique des parties
    joueur1.histo_partie.append(S1)
    joueur2.histo_partie.append(S2)


