class Jeu:
    
    """Classe représentant un jeu."""

    def __init__(self, nom, taux_de_hasard):
        self.nom = nom
        self.taux_de_hasard = taux_de_hasard

    def __str__(self):
        print(f"Nom du jeu: {self.nom}")
        print(f"Taux de hasard: {self.taux_de_hasard}")
