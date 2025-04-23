#Affichage des probas

from modele_joueur import np, plt, tirage_victoire_sigmoide

# Paramètres du graphique
num_matches = 500  # Nombre de matchs à simuler
f1_values = np.linspace(0, 1, num_matches)  # Valeurs des forces du joueur 1
f2_values = np.random.uniform(0, 1, num_matches)  # Valeurs des forces du joueur 2 tirées aléatoirement

P1_values = []  # Liste pour stocker les probabilités de victoire du joueur 1
diff_values = []  # Liste pour stocker la différence de forces (f1 - f2)

# Simulation des matchs et calcul des probabilités
for i in range(num_matches):
    P1, P2 = tirage_victoire_sigmoide(f1_values[i], f2_values[i])
    P1_values.append(P1)  # Stocker la probabilité de victoire du joueur 1
    diff_values.append(f1_values[i] - f2_values[i])  # Stocker la différence de forces

# Tracer la courbe des probabilités de victoire du joueur 1 (P1)
plt.figure(figsize=(8, 6))
plt.scatter(diff_values, P1_values, label="Probabilité de victoire du joueur 1", color="blue")
plt.xlabel("Différence de forces (f1 - f2)")
plt.ylabel("Probabilité de victoire du joueur 1")
plt.title("Probabilité de victoire du joueur 1 en fonction de la différence de forces")
plt.grid(True)
plt.legend()
plt.show()
