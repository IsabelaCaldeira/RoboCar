from .obstacle import Obstacle
from .ballon import Ballon


class Simulation:
    """Classe qui represente le monde elle sert uniquement a stocker les dimensions,obstacles et verifier les collision
    """

    def __init__(self, largeur, hauteur):
        self.largeur = largeur #largeur de la fenetre
        self.hauteur = hauteur #hauteur de la fenetre
        self.obstacles = [
            Obstacle("rectangle", (0,0), (80, 100)),
            Obstacle("rectangle", (0,0), (100, 50)),
            Obstacle("rectangle", (0,0), (50, 50)),
        ]
        self.obstacles[0].pos_aleatoire()
        self.obstacles[1].pos_aleatoire()
        self.obstacles[2].pos_aleatoire()

        self.ballon=Ballon(300,200,3,2,20)


    def collision(self, x, y, longueur, largeur):
        """Verifie si il y a collision avec un mur ou un obstacle
        avec x, y le centre du robot et longueur, largeur ses dimensions 
        """
        half_L = longueur / 2
        half_W = largeur / 2

        #rectangle du robot
        x1 = x - half_L
        y1 = y - half_W
        w1 = longueur
        h1 = largeur

        #collision avec les murs
        if x1 < 0 or y1 < 0 or x1 + w1 > self.largeur or y1 + h1 > self.hauteur:
            return True

        # collision avec les obstacles
        for obs in self.obstacles:
            x2, y2 = obs.pos
            w2, h2 = obs.dim

            if (
                x1 < x2 + w2 and
                x1 + w1 > x2 and
                y1 < y2 + h2 and
                y1 + h1 > y2
            ):
                return True

        return False
    
    def update_ballon(self):
        """Mise a jour du ballon """
        self.ballon.step(self.largeur,self.hauteur)

    def robot_ballon(self,robot):
        self.ballon.robot_proche(robot)