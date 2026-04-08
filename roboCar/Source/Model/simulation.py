from .obstacle import Obstacle


class Simulation:
    """Classe qui represente le monde elle sert uniquement a stocker les dimensions,obstacles et verifier les collision
    """

    def __init__(self, largeur, hauteur):
        self.largeur = largeur #largeur de la fenetre
        self.hauteur = hauteur #hauteur de la fenetre
        centre_x = self.largeur // 2
        self.obstacles = [
            Obstacle("rectangle", (centre_x - 40, 80), (80, 80)),
            Obstacle("rectangle", (centre_x - 50, self.hauteur // 2 - 30), (100, 60)),
            Obstacle("rectangle", (centre_x - 40, self.hauteur - 140), (80, 80)),
        ]


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
