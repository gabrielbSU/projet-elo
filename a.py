import numpy as np
import matplotlib.pyplot as plt

# Fonctions
def modifie_hasard(taux, impact_force, f1):
    a = (2 * taux * (1 + np.exp(-impact_force))) / (1 - np.exp(-impact_force))
    b = -a / 2
    return a / (1 + np.exp(-impact_force * f1)) + b

def sigmoid(x, k=10):
    return 1 / (1 + np.exp(-k * x))

def get_proba_simu(f1, f2, jeu):
    diff = np.abs(f1 - f2)
    mf = np.maximum(f1, f2)
    k_hasard = np.log(modifie_hasard(jeu['taux'], jeu['impact'], mf))
    return sigmoid(diff, k=k_hasard * 10 *  diff)

# Grille f1/f2
f1_vals = np.linspace(0, 1, 200)
f2_vals = np.linspace(0, 1, 200)
F1, F2 = np.meshgrid(f1_vals, f2_vals)

# Paramètres à tester
taux_values = [0.0, 0.2, 0.5, 0.8]
impact_values = [0.1, 0.5, 1.0, 2.0]

# Affichage
fig, axes = plt.subplots(len(taux_values), len(impact_values), figsize=(16, 14), sharex=True, sharey=True)
fig.suptitle("Isocontours de probabilité pour différents taux / impact", fontsize=18)

for i, taux in enumerate(taux_values):
    for j, impact in enumerate(impact_values):
        ax = axes[i, j]
        jeu = {'taux': taux, 'impact': impact}
        P = get_proba_simu(F1, F2, jeu)

        contour = ax.contourf(F1, F2, P, levels=20, cmap='viridis')
        ax.contour(F1, F2, P, levels=[0.25, 0.5, 0.75], colors='white', linewidths=0.5)
        ax.set_title(f"taux={taux}, impact={impact}")
        ax.set_aspect('equal')

# Légende couleur
cbar_ax = fig.add_axes([0.92, 0.15, 0.015, 0.7])
fig.colorbar(contour, cax=cbar_ax, label='Probabilité que le plus fort gagne')

plt.subplots_adjust(hspace=0.3, wspace=0.3, right=0.9)
plt.show()
