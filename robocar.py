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