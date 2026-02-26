🎯 Projet LU2IN013
Exploration du comportement des systèmes de rating (Elo, Glicko, Glicko-2)
📌 À propos du projet

Ce projet étudie le comportement comparé de trois systèmes de rating largement utilisés dans les environnements compétitifs :

Elo

Glicko

Glicko-2

L’objectif est d’analyser leur capacité à estimer fidèlement le niveau réel des joueurs à partir de simulations contrôlées de tournois.

Le rapport complet disponible dans le dépôt détaille :

Les fondements théoriques des systèmes

Les choix de modélisation probabiliste

Les protocoles expérimentaux

Les analyses statistiques approfondies

🧠 Contexte

Les systèmes de rating jouent un rôle fondamental dans de nombreux contextes compétitifs : échecs, e-sport, jeux en ligne, compétitions sportives, etc.
Ils cherchent à attribuer à chaque joueur une valeur numérique reflétant son niveau réel à partir de ses performances passées.

Dans ce projet, nous cherchons à répondre aux questions suivantes :

À quelle vitesse chaque système converge-t-il vers le niveau réel ?

Comment réagissent-ils face à des joueurs instables ou intermittents ?

Quel système est le plus robuste face au hasard ?

Comment évoluent les distributions des ratings au cours du temps ?

⚙️ Approche méthodologique

Notre démarche repose sur une double approche :

1️⃣ Implémentation fidèle des systèmes

Chaque système (Elo, Glicko, Glicko-2) est implémenté en respectant strictement sa formalisation théorique.

2️⃣ Simulation probabiliste de tournois

Nous générons :

Des joueurs avec compétences réelles aléatoires

Des ratings initiaux aléatoires

Un modèle probabiliste de confrontation intégrant :

Une part de hasard contrôlable

Une sensibilité au différentiel de niveau

Nous simulons ensuite des tournois répétés afin d’observer :

La vitesse de convergence

La stabilité des classements

L’erreur entre compétence réelle et rating estimé

La dispersion des distributions

🧪 Profils de joueurs étudiés

Les simulations permettent d’analyser différents types de joueurs :

🔁 Joueurs réguliers

🎲 Joueurs imprévisibles

⏳ Joueurs intermittents

📈 Joueurs en progression

🎯 Spécialistes vs généralistes

📊 Analyses réalisées

Les expériences permettent de mesurer :

L’erreur moyenne entre compétence réelle et rating

Le temps nécessaire pour obtenir un classement fidèle

La stabilité du système face aux fluctuations

L’évolution statistique des distributions

📁 Contenu du dépôt

Implémentation des systèmes de rating

Génération de joueurs et de tournois simulés

Scripts d’expérimentations

Visualisations statistiques

📄 Rapport complet (analyse détaillée et résultats)

🎓 Cadre académique

Projet réalisé dans le cadre de l’UE LU2IN013.
Le dépôt contient l’ensemble du travail expérimental ; le rapport fournit une analyse théorique et statistique approfondie.
