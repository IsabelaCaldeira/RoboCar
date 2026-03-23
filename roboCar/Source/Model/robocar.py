import math
import time 

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
        self.longueur = 50  # longueur (avant/arriere)
        self._last_update = None #memoire du dernier moment ou le robot a ete mis a jour
    
    def get_position(self):
        """Recuperer les coord du robot"""
        return self.x, self.y
    
    def get_position_tete(self):
        """Recuperer les coord de la tete du robot (avant du robot)"""
        tete_x = self.x + math.cos(self.angle) * self.longueur / 2
        tete_y = self.y + math.sin(self.angle) * self.longueur / 2
        return tete_x, tete_y
    
    def get_angle(self):
        """Recuperer l'etat du robot"""
        return self.angle
    
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
        self.set_vitesse_gauche(vitesse) #les deux roues doivent avoir la memee vitesse pour avancer en ligne droite
        self.set_vitesse_droite(vitesse)

    def reculer(self, vitesse):
        """Fait reculer le robot
        """
        self.set_vitesse_gauche(-vitesse)
        self.set_vitesse_droite(-vitesse)
        
    def arreter(self): #deceleration correspond a l'intensite du freinage
        """Reduit la vitesse du robot à 0
        """
        self.set_vitesse_droite(0)
        self.set_vitesse_gauche(0)
           
    def tourner_sur_place(self, vitesse):
        """Fait tourner le robot sur lui-même
        """
        self.set_vitesse_gauche(vitesse) #Une roue avance et l'autre recule
        self.set_vitesse_droite(-vitesse)

    def tourner_gauche(self, vitesse):
        """
        Fait tourner le robot vers la gauche 
        """
        self.set_vitesse_gauche(vitesse)
        self.set_vitesse_droite(0)

    def tourner_droite(self, vitesse):
        """
        Fait tourner le robot vers la droite 
        """
        self.set_vitesse_gauche(0)
        self.set_vitesse_droite(vitesse)  

    def update(self):
        """Mise a jour du robot"""
        now = time.time() #le temps actuel en secondes
        if self._last_update is None:
            dt = 0.0
        else:
            dt = now - self._last_update #le temps ecoule depuis la derniere mise a jour
        self._last_update = now #on sauvegarde le moment actuel

        v, w = self.calculer_vitesse()
        self.x += v * math.cos(self.angle) * dt #on multiplie par dt pour prendre en compte le temps ecoule
        self.y += v * math.sin(self.angle) * dt
        self.angle += w * dt #plus dt est grand plus il tourne longtemps
        #si w<0 on tourne a droite et a gauche sinon
    