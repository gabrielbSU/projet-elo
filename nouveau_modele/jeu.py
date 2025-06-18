class Jeu:
    """Classe représentant un jeu avec une part de hasard."""

    def __init__(self, nom, taux_de_hasard, impact_force_hasard=1.0):
        """
        :param nom: Nom du jeu.
        :param taux_de_hasard: Le taux de hasard (entre 0 et 1).
        :param impact_force_hasard: Impact du hasard selon la différence de force (>= 0).
        """
        self.nom = nom

        if not (0 <= taux_de_hasard <= 1):
            raise ValueError("taux_de_hasard doit être entre 0 et 1")
        self.taux_de_hasard = taux_de_hasard

        if impact_force_hasard < 0:
            raise ValueError("impact_force_hasard doit être positif")
        self.impact_force_hasard = impact_force_hasard

    def __str__(self):
        return (f"Nom du jeu: {self.nom}\n"
                f"Taux de hasard: {self.taux_de_hasard}\n"
                f"Impact force - hasard: {self.impact_force_hasard}")
