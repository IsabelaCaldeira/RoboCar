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

    def suivre_trajectoire(self, instructions):
        """Faire flash suivre une trajectoire"""
        action, valeur = instructions[0]
        if action == "avancer":
            self.avancer()
            valeur -= 1
        elif action == "reculer":
            self.reculer()
            valeur -= 1
        elif action == "tourner_gauche":
            self.tourner_gauche(valeur)
            valeur = 0
        elif action == "tourner_droite":
            self.tourner_droite(valeur)
            valeur = 0
        if valeur <= 0:
            instructions.pop(0)
        else:
            instructions[0] = (action, valeur)

    