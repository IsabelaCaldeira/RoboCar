import math
from obstacle import *
import obstacle
class RoboCar(object):
    def __init__(self, nom:str, coordonnees:tuple, vitesse:int, angle:int, rayon:int):
        self.n = nom    # nom:string
        self.coo = coordonnees  # coordonnees:tuple(int, int)
        self.v = vitesse    # vitesse:int
        self.a = angle # angle:int [0;360]
        self.r = rayon 
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
    def collision(self, obstacle):
        """Cette fonction verifie si la voiture entre en collision avec un obstacle"""
        x1, y1 = self.coo #coordonnées du robot
        l1 = h1 = 2 * self.r   # taille du robot

        x2, y2 = obstacle.pos #coordonnées de l'obstacle
        l2, h2 = obstacle.dim #taille de l'obstacle
        return (
            x1 < x2 + l2 and 
            x1 + l1 > x2 and
            y1 < y2 + h2 and
            y1 + h1 > y2
        )
    
    def Contourne(self, coord, angle, obstacles):
        "cette fonction fait tourner la voiture jusqu'à ce qu'elle puisse avancer sans collision"
        self.coo = coord
        self.a = angle
        for obs in obstacles:
            if self.collision(obs):
                self.tourner_droite(5)
                self.avancer()
                return
    