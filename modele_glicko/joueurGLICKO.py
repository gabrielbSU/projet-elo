import math

class JoueurGlicko:
    """
    Classe représentant un joueur utilisant le système Glicko.
    """
    def __init__(self, nom, prenom, age, comp, rating=1500, RD=350):
        self.nom = nom
        self.prenom = prenom
        self.age = age
        self.comp = comp  # compétences
        self.rating = rating  # Note Glicko
        self.RD = RD  # Rating Deviation
        self.historique_rating = [rating]
        self.historique_RD = [RD]
        self.adversaires_temp = []  # Adversaires rencontrés sur la période
        self.resultats_temp = []    # Résultats contre ces adversaires
    
    def force_joueur(self):
        """Calcule une force basée sur les compétences."""
        tot = sum(c * (i + 1) for i, c in enumerate(self.comp))
        return float(tot) / 150

    def ajouter_match_temp(self, adversaire, resultat):
        """Ajoute un match temporairement pour le batch update."""
        self.adversaires_temp.append(adversaire)
        self.resultats_temp.append(resultat)

    def mettre_a_jour_batch(self):
        """Met à jour le rating du joueur après un batch de matchs."""
        from .glicko_utils import mettre_a_jour_glicko
        mettre_a_jour_glicko(self, self.adversaires_temp, self.resultats_temp)
        self.adversaires_temp = []
        self.resultats_temp = []

    def __str__(self):
        return (f"Nom : {self.nom}\n"
                f"Prénom : {self.prenom}\n"
                f"Age : {self.age}\n"
                f"Compétences : {self.comp}\n"
                f"Rating actuel : {self.rating:.2f}\n"
                f"RD actuel : {self.RD:.2f}\n")
