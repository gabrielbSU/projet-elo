# __init__.py

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm 

from .joueur import Joueur, rencontre_sigmoide, rencontre_log_normale, generer_joueur, tracer_competences, tracer_elo, tracer_competences_et_elo
from .outils import tirage_victoire_log_normal, tirage_victoire_sigmoide
from .tournoi import tournoi_round_robin, afficher_classement, tournoi_eliminatoire