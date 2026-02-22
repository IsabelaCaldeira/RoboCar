import random
class Obstacle(object):
    def __init__(self, forme: str, position: tuple, dimensions: tuple):
        self.pos = position #position (x,y) 
        self.dim = dimensions #(largeur,hauteur) 

    def pos_aleatoire(self):  
        x = self.pos[0] + random.randint(0,500)
        y = self.pos[1] + random.randint(0,500)
        self.pos = (x, y)
        return self.pos