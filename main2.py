from joueur import Joueur

# Génération d'une liste de joueurs
joueurs = [Joueur.generer_joueur(f"Joueur{i}", f"Prénom{i}") for i in range(1000)]

# Tracé des compétences
Joueur.tracer_competences(joueurs)

# Tracé des elo
Joueur.tracer_elo(joueurs)

# Comparaison des densités des compétences et des elo
Joueur.tracer_competences_et_elo(joueurs)