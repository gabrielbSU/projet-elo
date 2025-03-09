import numpy as np
import matplotlib.pyplot as plt
from outils import Outils
from scipy.stats import norm
import random
import math

class Joueur:
    """
    Cette classe permet de modéliser un joueur. 
    On supposera que le jeu est un jeu individuel donc un joueur est un objet unique de la classe Joueur.
    """

    def __init__(self, nom, prenom, age, comp, histo_partie, histo_tournoi, elo):
        self.nom = nom
        self.prenom = prenom
        self.age = age
        self.comp = comp  # comp est une liste de 5 compétences dont le coeff est la position dans la liste.
        self.histo_partie = histo_partie  # Liste des résultats des parties (-1: défaite, 0: nul, 1: victoire)
        self.histo_tournoi = histo_tournoi  # Liste des résultats des tournois
        self.elo = elo  # Niveau de jeu du joueur (elo)

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

    def afficher_joueur(self):
        """
        Affiche les informations du joueur.
        """
        print(f"Nom : {self.nom}")
        print(f"Prénom : {self.prenom}")
        print(f"Age : {self.age}")
        print(f"Compétences : {self.comp}")
        print(f"Elo : {self.elo}")

    def force_joueur(self):
        """
        Retourne la force d'un joueur entre 0 et 1.
        """
        tot = 0
        for i in range(len(self.comp)):
            tot += self.comp[i] * (i + 1)
        return float(tot) / 100

    def force_relative(self, joueur_adverse):
        """
        Renvoie le couple (f1, f2) des forces relatives entre 2 joueurs self et joueur_adverse.
        """
        f1 = self.force_joueur()
        f2 = joueur_adverse.force_joueur()
        return (f1 / (1 - f2), f2 / (1 - f1))

    def rencontre(self, joueur_adverse):
        """
        Simule une partie entre deux joueurs. Renvoie 1 en cas de victoire, -1 en cas de défaite, 0 en cas de nul.
        """
        f1, f2 = self.force_relative(joueur_adverse)
        delta_f = abs(f1 - f2)

        # Calcul du sigma_hasard
        if delta_f >= 0.5:
            # Si la différence entre les 2 forces est trop élevée, le hasard n'a pas d'impact
            sigma_hasard = 0
        else:
            # Sinon, on calcule le sigma_hasard en fonction de l'historique des joueurs
            if len(joueur_adverse.histo_partie) >= 5 and len(self.histo_partie) >= 5:
                tot = 0
                for i in range(len(self.histo_partie) - 6, len(self.histo_partie)):
                    tot += self.histo_partie[i]
                for i in range(len(joueur_adverse.histo_partie) - 6, len(joueur_adverse.histo_partie)):
                    tot += joueur_adverse.histo_partie[i]

                valeur_aleatoire = random.uniform(-tot, tot)
                ancien_min, ancien_max = -tot, tot
                nouvel_min, nouvel_max = 0, 0.5

                # On calcule le sigma_hasard en fonction de la valeur_aleatoire
                sigma_hasard = (valeur_aleatoire - ancien_min) * (nouvel_max - nouvel_min) / (ancien_max - ancien_min) + nouvel_min
            else:
                # Sinon, on fixe que le hasard a peu d'impact
                sigma_hasard = 0.1

        # Calcul du gagnant de la partie
        proba = Outils.probabilite_victoire_avec_hasard(f1, f2, sigma_hasard=sigma_hasard)

        # Mise à jour de l'elo
        self.elo += 400 * math.log10(f1)
        joueur_adverse.elo += 400 * math.log10(f2)

        # Mise à jour de l'historique des parties
        if proba > 0.5:
            self.histo_partie.append(1)
            joueur_adverse.histo_partie.append(-1)
            return 1
        elif proba < 0.5:
            self.histo_partie.append(-1)
            joueur_adverse.histo_partie.append(1)
            return -1
        else:
            self.histo_partie.append(0)
            joueur_adverse.histo_partie.append(0)
            return 0

    def comparaison_rencontre_elo(self, joueur_adverse):
        """
        Renvoie True si la fonction rencontre() renvoie le même résultat que les prédictions de l'elo, False sinon.
        """
        rencontre = self.rencontre(joueur_adverse)
        proba_elo = 1 / (1 + 10 ** (-((self.elo - joueur_adverse.elo) / 400)))
        return ((rencontre == 1 and proba_elo > 0.5) or (rencontre == 0 and proba_elo == 0.5) or (rencontre == -1 and proba_elo < 0.5))