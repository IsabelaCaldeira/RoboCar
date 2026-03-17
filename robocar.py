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
        return self.vG, self.vR
        
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
    
    def avancer(self, vitesse):
        """Fait avancer le robot tout droit.
        """
        self.robot.set_vitesse_gauche(vitesse) #les deux roues doivent avoir la memee vitesse pour avancer en ligne droite
        self.robot.set_vitesse_droite(vitesse)

    def reculer(self, vitesse):
        """Fait reculer le robot
        """
        self.robot.set_vitesse_gauche(-vitesse)
        self.robot.set_vitesse_droite(-vitesse)
           
    def tourner_sur_place(self, vitesse):
        """Fait tourner le robot sur lui-même
        """
        self.robot.set_vitesse_gauche(vitesse) #Une roue avance et l'autre recule
        self.robot.set_vitesse_droite(-vitesse)

    def tourner_gauche(self, vitesse):
        """
        Fait tourner le robot vers la gauche 
        """
        self.robot.set_vitesse_gauche(vitesse)
        self.robot.set_vitesse_droite(0)

    def tourner_droite(self, vitesse):
        """
        Fait tourner le robot vers la droite 
        """
        self.robot.set_vitesse_gauche(0)
        self.robot.set_vitesse_droite(vitesse)
        
    def freiner(self, dt, deceleration=120): #deceleration correspond a l'intensite du freinage
        """Reduit progressivement les vitesses des roues vers 0
        """
        pas = deceleration * dt # quantite de vitesse retiree pendant cette frame
        # freinage roue gauche
        if self.robot.vG > 0:
            self.robot.vG = max(0, self.robot.vG - pas)
        elif self.robot.vG < 0:
            self.robot.vG = min(0, self.robot.vG + pas)
        # freinage roue droite
        if self.robot.vR > 0:
            self.robot.vR = max(0, self.robot.vR - pas)
        elif self.robot.vR < 0:
            self.robot.vR = min(0, self.robot.vR + pas)

    def update(self, dt):
        """Mise a jour du robot"""
        v, w = self.calculer_vitesse()
        self.x += v * math.cos(self.angle) * dt
        self.y += v * math.sin(self.angle) * dt
        self.angle += w * dt #si w<0 on tourne a droite et a gauche sinon
    