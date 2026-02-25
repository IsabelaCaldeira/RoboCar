import math
class RoboCar:
    WHEEL_BASE = 50  # distance entre roues 

    def __init__(self, nom, coordonnees, angle):
        self.nom = nom
        self.x, self.y = coordonnees #coordonne du centre du robot
        self.angle = math.radians(angle) #orientation

        # vitesses roues
        self.vG = 0 #vitesse roue gauche
        self.vR = 0 #vitesse roue droite
        self.largeur = 40   # largeur (cote roues)
        self.longueur = 60  # longueur (avant/arriere)
        
    def get_state(self):
        """Recuperer l'etat du robot"""
        return self.x, self.y, self.angle
    
    def get_wheel_speeds(self):
        return self.robot.vG, self.robot.vR
        
    def set_vitesse_gauche(self, v):
        """Modifier la vitesse du roue gauche"""
        self.vG = v
        
    def set_vitesse_droite(self, v):
        """Modifier la vitesse du roue droite"""
        self.vR = v
        
    def calculer_vitesse(self):
        """Cette fonction calcule la vitesse lineaire et angulaire"""
        v = (self.vR + self.vG) / 2
        w = (self.vR - self.vG) / self.WHEEL_BASE #c'est le theoreme de Thales applique au cercle de rotation
        return v, w

    def update(self, dt):
        """Mise a jour du robot"""
        v, w = self.calculer_vitesse()
        self.x += v * math.cos(self.angle) * dt
        self.y += v * math.sin(self.angle) * dt
        self.angle += w * dt #si w<0 on tourne a droite et a gauche sinon
    