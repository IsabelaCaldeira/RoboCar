import random
class Obstacle(object):
    def __init__(self, forme: str, position: tuple, dimensions: tuple):
        self.forme = forme #forme peut etre un cercle, rectangle etc.
        self.pos = position #position (x,y) (represente le centre si c'est un cercle)
        self.dim = dimensions #(largeur,longeur) si c'est un rectangle et rayon seulement si c'est un cercle

    def pos_aleatoire(self):  
        x = self.pos[0] + random.randint(0,500)
        y = self.pos[1] + random.randint(0,500)
        self.pos = (x, y)
        return self.pos