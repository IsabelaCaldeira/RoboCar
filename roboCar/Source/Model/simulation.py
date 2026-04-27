import random

from .obstacle import Obstacle


class Simulation:
    """Classe qui represente le monde elle sert uniquement a stocker les dimensions,obstacles et verifier les collision
    """

    def __init__(self, largeur, hauteur, zone_interdite=None, obstacle_dimensions=None):
        self.largeur = largeur #largeur de la fenetre
        self.hauteur = hauteur #hauteur de la fenetre
        self.zone_interdite = zone_interdite
        self.obstacles = []
        self.souris = None
        self.vitesse_souris = (0, 0)
        self.souris_attrapees = 0

        if obstacle_dimensions is None:
            obstacle_dimensions = [(80, 100), (100, 50), (50, 50)]

        for dimensions in obstacle_dimensions:
            self.ajouter_obstacle_aleatoire(*dimensions)

    def est_valide(self, x, y, l, h):
        """Renvoie True si l'obstacle est valide"""
        if x < 0 or y < 0 or x + l > self.largeur or y + h > self.hauteur:
            return False

        for obs in self.obstacles:
            ox, oy = obs.pos
            ol, oh = obs.dim

            if self.rectangles_chevauchent(x, y, l, h, ox, oy, ol, oh):
                return False

        if self.zone_interdite is not None:
            rx, ry, rl, rh = self.zone_interdite

            if self.rectangles_chevauchent(x, y, l, h, rx, ry, rl, rh):
                return False

        return True

    def rectangles_chevauchent(self, x1, y1, l1, h1, x2, y2, l2, h2):
        """Retourne True si deux rectangles se chevauchent."""
        return (
            x1 < x2 + l2 and x1 + l1 > x2 and
            y1 < y2 + h2 and y1 + h1 > y2
        )

    def ajouter_obstacle_aleatoire(self, l, h, max_essais=100):
        """Ajoute un obstacle aleatoire sans chevauchement."""
        for _ in range(max_essais):
            x = random.randint(0, self.largeur - l)
            y = random.randint(0, self.hauteur - h)

            if self.est_valide(x, y, l, h):
                self.obstacles.append(Obstacle("rectangle", (x, y), (l, h)))
                return True

        return False

 

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

            if self.rectangles_chevauchent(x1, y1, w1, h1, x2, y2, w2, h2):
                return True

        return False
