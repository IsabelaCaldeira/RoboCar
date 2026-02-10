import math
class RoboCar(object):
    def __init__(self, nom:str, coordonnees:tuple, vitesse:int, angle:int):
        self.n = nom    # nom:string
        self.coo = coordonnees  # coordonnees:tuple(int, int)
        self.v = vitesse    # vitesse:int
        self.a = angle  # angle:int [0;360]
    def avancer(self):
        """Avance la voiture selon son angle"""
        angle_rad = math.radians(self.a) 
        x = self.coo[0] + math.cos(angle_rad) * self.v
        y = self.coo[1] + math.sin(angle_rad) * self.v
        self.coo = (x, y)
    def reculer(self):
        """Recule la voiture selon son angle"""
        angle_rad = math.radians(self.a) #on met en radians pour que cos et sin puissent marcher 
        x = self.coo[0] - math.cos(angle_rad) * self.v
        y = self.coo[1] - math.sin(angle_rad) * self.v
        self.coo = (x, y)
    def tourner_gauche(self, vitesse):
        self.a = (self.a - vitesse) % 360 #on veut que l'angle reste entre 0 et 360 donc on fait un modulo 360

    def tourner_droite(self, vitesse):
        self.a = (self.a + vitesse) % 360

    def trajectoire_carree(self, longueur):
        """Fait avancer flash pour faire le trajectoire d'un carré"""
        return [("avancer", longueur), ("tourner_droite", 90),
                ("avancer", longueur), ("tourner_droite", 90),
                ("avancer", longueur), ("tourner_droite", 90),
                ("avancer", longueur), ("tourner_droite", 90),]
