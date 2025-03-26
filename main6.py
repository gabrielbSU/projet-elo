from modele_joueur import sigmoid, np, plt, sns

#Ce main permet de voir l'évolution de notre sigmoide selon le jeu choisi (hasard plus ou moins présent)
# On retrouve ici la courbe de la fonction sigmoïde pour différents taux de hasard ainsi que la heatmap de la probabilité de victoire en fonction de la différence de force et du taux de hasard.



# Différence de forces entre les joueurs (de -1 à 1)
x = np.linspace(-1, 1, 200)  # Augmenter le nombre de points de 100 à 200

# Taux de hasard pour plusieurs scénarios
taux_de_hasard_values = [0.1, 0.5, 0.8, 0.9, 1]  # Taux de hasard faible, moyen et élevé
k_values = [9, 6, 2, 1, 0]  # Facteur k ajusté en fonction du taux de hasard (faible k = plus de hasard)

plt.figure(figsize=(10, 6))

for taux, k in zip(taux_de_hasard_values, k_values):
    # Tracé de la courbe sigmoïde pour chaque taux de hasard
    plt.plot(x, sigmoid(x, k), label=f"Taux de hasard = {taux}")

plt.title("Impact du taux de hasard sur la probabilité de victoire")
plt.xlabel("Différence de forces (f1 - f2)")
plt.ylabel("Probabilité de victoire du joueur 1")
plt.legend()
plt.grid(True)
plt.show()

# Heatmap de la probabilité de victoire en fonction du taux de hasard et de la différence de force
# Valeurs de la différence de force (f1 - f2) entre -1 et 1
x = np.linspace(-1, 1, 200)  # Augmenter le nombre de points de 100 à 200

# Liste des taux de hasard à tester (ajuste k selon le taux de hasard)
taux_de_hasard_values = np.linspace(0.1, 1.0, 20)  # Augmenter le nombre de taux de hasard testés de 10 à 20
k_values = [10 * (1 - taux) for taux in taux_de_hasard_values]  # k devient plus faible avec plus de hasard

# Créer une matrice pour les probabilités de victoire
heatmap_data = np.zeros((len(taux_de_hasard_values), len(x)))

# Calculer la probabilité de victoire du joueur 1 pour chaque combinaison de taux de hasard et différence de force
for i, taux in enumerate(taux_de_hasard_values):
    for j, diff in enumerate(x):
        k = k_values[i]
        heatmap_data[i, j] = sigmoid(diff, k)

# Création de la heatmap
plt.figure(figsize=(10, 6))
sns.heatmap(heatmap_data, cmap="YlGnBu", xticklabels=10, yticklabels=np.round(taux_de_hasard_values, 2), cbar_kws={'label': 'Probabilité de victoire du joueur 1'})

# Ajout des labels et du titre
plt.title("Heatmap de la probabilité de victoire du joueur 1 en fonction du taux de hasard et de la différence de force")
plt.xlabel("Différence de forces (f1 - f2)")
plt.ylabel("Taux de hasard")

# Affichage
plt.show()
