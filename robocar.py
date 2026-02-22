import math
class RoboCar:
    WHEEL_BASE = 50  # distance entre roues 

    def __init__(self, nom, coordonnees, angle):
        self.nom = nom
        self.x, self.y = coordonnees #coordonne du centre du robot
        self.angle = math.radians(angle) #orientation

        # vitesses roues
        self.v_l = 0 #vitesse roue gauche
        self.v_r = 0 #vitesse roue droite
        self.largeur = 40   # largeur (cote roues)
        self.longueur = 60  # longueur (avant/arriere)
    def get_state(self):
        """Recuperer l'etat du robot"""
        return self.x, self.y, self.angle

    def get_wheel_speeds(self):
        """Recuperer la vitesse des roues"""
        return self.v_l, self.v_r
    def set_vitesse_gauche(self, v):
        """Modifier la vitesse du roue gauche"""
        self.v_l = v

    def set_vitesse_droite(self, v):
        """Modifier la vitesse du roue droite"""
        self.v_r = v
    def calculer_vitesse(self):
        """Cette fonction calcule la vitesse lineaire et angulaire"""
        v = (self.v_r + self.v_l) / 2
        w = (self.v_r - self.v_l) / self.WHEEL_BASE #c'est le theoreme de Thales applique au cercle de rotation
        return v, w
    def update(self, dt):
        """Mise a jour du robot"""
        v, w = self.calculer_vitesse()
        self.x += v * math.cos(self.angle) * dt
        self.y += v * math.sin(self.angle) * dt
        self.angle += w * dt #si w<0 on tourne a droite et a gauche sinon
    def distance_obstacle(self, obstacles, max_range=120):
        """Cette fonction regarde l'obstacle le plus proche"""
        min_dist = max_range #distance minimale

        # vecteur direction du robot
        dir_x = math.cos(self.angle)
        dir_y = math.sin(self.angle)

        for obs in obstacles:

            ox, oy = obs.pos
            dx = ox - self.x #on cree un vecteur du robot vers l’obstacle
            dy = oy - self.y

            # projection dans la direction du robot
            projection = dx * dir_x + dy * dir_y #produit scalaire

