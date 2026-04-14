import math
from vpython import canvas, box, vector, color, rate
from Source import Simulation, RoboCar
from Source import AdaptateurSimule
from Source import creer_strategie
import math

LARGEUR = 800
HAUTEUR = 600

def conv_y(y):
    """Convertit le y du monde 2D vers le z de VPython"""
    return HAUTEUR - y #on inverse cet axe pour que l'affichage reste coherent car en 2d l'axe y descend vers le bad et nous on veut un repere plus naturel

