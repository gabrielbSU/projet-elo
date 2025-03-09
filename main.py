import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from outils import Outils

# Définir la plage de différences de forces (Delta f)
delta_f = np.linspace(-10, 10, 1000)  # De -10 à 10 pour couvrir un large éventail de différences

# Calculer la fonction de répartition (CDF) pour chaque Delta f
proba_victoire = norm.cdf(delta_f, loc=0, scale=1)  # sigma = 1

# Tracer la courbe
plt.figure(figsize=(8, 6))
plt.plot(delta_f, proba_victoire, label="Fonction de répartition (CDF)", color="blue")
plt.title("Fonction de répartition de la probabilité de victoire du joueur 1")
plt.xlabel("Différence de forces (Δf = f1 - f2)")
plt.ylabel("Probabilité que le joueur 1 gagne")
plt.grid(True)
plt.axvline(0, color="red", linestyle="--", label="Δf = 0")  # Ligne verticale à Δf = 0
plt.axhline(0.5, color="green", linestyle="--", label="Probabilité = 0.5")  # Ligne horizontale à proba = 0.5
plt.legend()
plt.show()

# Exemple d'utilisation
f1 = 0.7  # Force du joueur 1 (doit être dans [0, 1])
f2 = 0.5  # Force du joueur 2 (doit être dans [0, 1])
sigma = 1  # Écart-type de la gaussienne
sigma_hasard = 0.2  # Écart-type du facteur de hasard (doit être dans [0, 0.5])

# Calcul de la probabilité de victoire avec facteur de hasard
proba_victoire = Outils.probabilite_victoire_avec_hasard(f1, f2, sigma, sigma_hasard)
print(f"Probabilité que le joueur 1 gagne avec facteur de hasard : {proba_victoire:.2f}")

# Exécuter la fonction plusieurs fois pour observer la variabilité
print("\nVariabilité des résultats avec le facteur de hasard :")
for _ in range(10):
    proba = Outils.probabilite_victoire_avec_hasard(f1, f2, sigma, sigma_hasard)
    print(f"Probabilité de victoire : {proba:.2f}")