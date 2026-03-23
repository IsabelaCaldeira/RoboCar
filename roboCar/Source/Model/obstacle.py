import random
from .vecteur import Vecteur

class Obstacle(object):
    def __init__(self, forme: str, position: tuple, dimensions: tuple):
        self.pos = position #position (x,y) 
        self.dim = dimensions #(largeur,hauteur) 

    def pos_aleatoire(self):  
        x = self.pos[0] + random.randint(0,500)
        y = self.pos[1] + random.randint(0,500)
        self.pos = (x, y)
        return self.pos

class Polygone:
    def __init__(self, points:list[Vecteur]):
        """ Initialisation du polygone, défini par une liste de points (à definir dans l'ordre du perimètre) """
        self.points = points
    
    def get_points(self):
        """ Renvoie les points du polygone dans l'ordre """
        return self.points