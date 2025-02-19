import math

class Elo:
    """
    Implémentation simplifiée du système de classement Elo.
    
    Attributs:
    score: Current Elo rating
    parties_jouees: Number of games played
    historique: List of Elo ratings over times
    """
    
    def __init__(self, score_initial=1200):
        """
        Initialise le classement.
            score_initial (float): Score de départ (1200 par défaut)
        """
        self.score = score_initial
        self.parties_jouees = 0
        self.historique = [score_initial]

    def score_attendu(self, score_adversaire):
        """
        Calcule le score attendu contre un adversaire.
        
        Returns:
            float: Score attendu entre 0 et 1
        """
        return 1 / (1 + 10 ** ((score_adversaire - self.score) / 400))

    def maj_score(self, score_adversaire, resultat):
        """
        Met à jour le score après une partie.
        
        Args:
            score_adversaire (float): Score de l'adversaire
            resultat (float): Résultat (0 pour défaite, 1 pour victoire)
            
        Returns:
            float: Nouveau score
        """
        attendu = self.score_attendu(score_adversaire)
        changement = 32 * (resultat - attendu)
        self.score += changement
        self.parties_jouees += 1
        self.historique.append(self.score)
        return self.score

    def categorie(self):
    
        if self.score < 1200:
            return "Débutant"
        elif self.score < 1600:
            return "Intermédiaire"
        elif self.score < 2000:
            return "Avancé"
        elif self.score < 2400:
            return "Expert"
        else:
            return "Maître"

    def score_actuel(self):

        return self.score
    

if __name__ == "__main__":
    # Création de deux joueurs
    joueur1 = Elo(1200)
    joueur2 = Elo(1400)

    # Affichage des scores initiaux
    print("=== Scores initiaux ===")
    print(f"Joueur 1: {joueur1.score_actuel()} ({joueur1.categorie()})")
    print(f"Joueur 2: {joueur2.score_actuel()} ({joueur2.categorie()})")

    # Joueur1 gagne contre joueur2
    print("\n=== Résultat de la partie ===")
    print("Joueur1 gagne contre Joueur2")
    joueur1.maj_score(joueur2.score_actuel(), 1)
    joueur2.maj_score(joueur1.score_actuel(), 0)

    # Affichage des nouveaux scores
    print("\n=== Scores après la partie ===")
    print(f"Joueur 1: {joueur1.score_actuel()} ({joueur1.categorie()})")
    print(f"Joueur 2: {joueur2.score_actuel()} ({joueur2.categorie()})")

#=== Scores initiaux ===
#Joueur 1: 1200 (Intermédiaire)
#Joueur 2: 1400 (Intermédiaire)

#=== Résultat de la partie ===
#Joueur1 gagne contre Joueur2

#=== Scores après la partie ===
#Joueur 1: 1224.3119016527346 (Intermédiaire)
#Joueur 2: 1376.5349537013067 (Intermédiaire)
