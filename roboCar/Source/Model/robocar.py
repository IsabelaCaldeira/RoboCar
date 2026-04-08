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
        self.crayon_abaisse = False
        self.trace = [coordonnees]
        self.couleur_trace = (0, 0, 200)

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
        if self.crayon_abaisse:
            self.trace.append((x, y))

    def abaisser_crayon(self): 
        """Active le trace"""
        self.crayon_abaisse = True
        position = self.get_position()
        if not self.trace or self.trace[-1] != position:
            self.trace.append(position)

    def lever_crayon(self):
        """Desactive le trace du robot"""
        self.crayon_abaisse = False

    def get_trace(self):
        """Retourne les points traces par le robot"""
        return self.trace
    
    def dessine(self,b):
        """active ou desactive le trace du robot selon b"""
        if b:
            self.abaisser_crayon()
        else:
            self.lever_crayon()

    def trace_visible(self):
        """Retourne True si le trace est visible (crayon abaisse)"""
        return self.crayon_abaisse
    
    def change_couleur(self, couleur):
        """Change la couleur de la trace"""
        self.couleur_trace = couleur

    def get_couleur_trace(self):
        """Retourne la couleur de la trace"""
        return self.couleur_trace

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
