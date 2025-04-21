class Jeu:
    """Classe représentant un jeu."""

    def __init__(self, nom, taux_de_hasard, impact_hasard=1.0):
        """
        :param nom: Nom du jeu
        :param taux_de_hasard: Le taux de hasard (entre 0 et 1)
        :param impact_hasard: Impact maximal du hasard (par défaut 1.0, ajustable)
        """
        self.nom = nom
        self.taux_de_hasard = taux_de_hasard
        self.impact_hasard = impact_hasard

    def __str__(self):
        return f"Nom du jeu: {self.nom}\nTaux de hasard: {self.taux_de_hasard}\nImpact du hasard: {self.impact_hasard}"
