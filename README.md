# Projet LU2IN013  
## Exploration du comportement des systèmes de rating (Elo, Glicko, Glicko-2)

---

## Description

Ce projet étudie le comportement comparé de trois systèmes de rating largement utilisés dans les environnements compétitifs :

- **Elo**
- **Glicko**
- **Glicko-2**

L’objectif est d’analyser leur capacité à estimer fidèlement le niveau réel des joueurs à partir de simulations contrôlées.

Le rapport complet disponible dans ce dépôt présente en détail :
- Les fondements théoriques des systèmes
- La modélisation probabiliste des rencontres
- Les protocoles expérimentaux
- Les résultats et analyses statistiques

---

## Contexte

Les systèmes de rating jouent un rôle central dans de nombreux contextes compétitifs (échecs, e-sport, jeux en ligne, compétitions sportives).  
Ils attribuent à chaque joueur une valeur numérique censée refléter son niveau réel à partir de ses performances passées.

Dans ce projet, nous cherchons à comprendre :

- À quelle vitesse chaque système converge vers le niveau réel ?
- Comment réagissent-ils face à des joueurs instables ou intermittents ?
- Quelle est leur robustesse face au hasard ?
- Comment évoluent les distributions des ratings au cours du temps ?

---

## Méthodologie

Notre approche repose sur deux axes principaux :

### Implémentation des systèmes

Chaque système (Elo, Glicko, Glicko-2) est implémenté conformément à sa définition théorique.

### Simulation probabiliste de tournois

Nous générons :

- Des joueurs avec une **compétence réelle aléatoire**
- Des **ratings initiaux**
- Un modèle de confrontation intégrant :
  - Une part de hasard contrôlable
  - Une probabilité de victoire dépendant du différentiel de niveau

Des tournois simulés sont ensuite exécutés afin d’observer :

- La vitesse de convergence
- La stabilité des classements
- L’écart entre compétence réelle et rating estimé
- L’évolution statistique des distributions

---

## 📊 Analyses réalisées

Les expérimentations mesurent notamment :

- L’erreur moyenne entre compétence réelle et rating
- Le temps nécessaire pour obtenir un classement fidèle
- La stabilité du système face aux fluctuations
- La dispersion des ratings
- La robustesse face au bruit aléatoire

---

## Contenu du dépôt

- Implémentation des systèmes de rating
- Génération de joueurs et de tournois simulés
- Scripts d’expérimentations
- Visualisations statistiques
- Rapport complet (analyse théorique et résultats détaillés)

---

## Cadre académique

Projet réalisé dans le cadre de l’UE **LU2IN013**.

Le code permet de reproduire les simulations.  
Le rapport fournit une analyse complète et détaillée des résultats expérimentaux.

---
