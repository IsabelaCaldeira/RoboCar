import math


class RoboCar:
    """Classe du robot simule
    """
    WHEEL_BASE = 50
    PAS = 0.5  #taille du pas de deplacement (controle la vitesse globale)

    def __init__(self, nom, coordonnees, angle, simulation=None):
        self.nom = nom
        self.x, self.y = coordonnees
        self.angle = math.radians(angle)

        # vitesses roues
        self.vG = 0
        self.vR = 0

        self.largeur = 40
        self.longueur = 50

        self.simulation = simulation #reference vers le monde

        self.draw = True
        self.draw_color = (0, 0, 200)

    def get_position(self):
        """Retourne (x, y)"""
        return self.x, self.y

    def get_angle(self):
        """Retourne l'angle du robot"""
        return self.angle

    def set_vitesse(self):
        """On calcule la vitesse lineaire et angulaire
        """
        v = (self.vR + self.vG) / 2
        w = (self.vR - self.vG) / self.WHEEL_BASE
        return v, w

    def update(self, v, w):
        """On retourne les prochaines valeurs de x,y,angle
        """
        next_x = self.x + v * math.cos(self.angle) * self.PAS
        next_y = self.y + v * math.sin(self.angle) * self.PAS
        next_angle = self.angle + w * self.PAS

        return next_x, next_y, next_angle

    def appliquer(self, x, y, angle):
        """Applique le nouvel etat calcule
        """
        self.x = x
        self.y = y
        self.angle = angle

    def step(self):
        """On fait une mise a jour complete 
        """
        v, w = self.set_vitesse()
        next_x, next_y, next_angle = self.update(v, w)

        if not self.simulation.collision(next_x, next_y, self.longueur, self.largeur):
            self.appliquer(next_x, next_y, next_angle)
            return True

        return False

    def get_distance(self, max_range=120, pas=5):
        """
        Mesure la distance devant le robot jusqu'au premier obstacle
        """
        for d in range(0, max_range, pas):
            x = self.x + math.cos(self.angle) * d
            y = self.y + math.sin(self.angle) * d

            if self.simulation.collision(x, y, self.longueur, self.largeur):
                return d

        return max_range
    
    def dessiner(self, b):
        self.dessin = b

    def changer_couleur(self, couleur):
        self.line_color = couleur