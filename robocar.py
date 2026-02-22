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