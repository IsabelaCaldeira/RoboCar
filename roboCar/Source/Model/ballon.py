import math 
class Ballon:
    VITESSE_MAX=6
    def __init__(self, x, y, vx, vy, rayon):
        self.x = x
        self.y = y
        self.vx = vx #vecteur x
        self.vy = vy #vecteur y
        self.rayon = rayon

    def step(self, largeur, hauteur):
        """Met a jour la position du ballon """
        #on avance 
        self.x += self.vx
        self.y += self.vy
        if self.x - self.rayon < 0: #rebond mur gauche
            self.x = self.rayon
            self.vx =self.vx* -1
        if self.x + self.rayon > largeur: #rebond sur mur droit
            self.x = largeur - self.rayon
            self.vx =self.vx* -1
        if self.y - self.rayon < 0: #rebond sur mur haut
            self.y = self.rayon
            self.vy = self.vy* -1
        if self.y + self.rayon > hauteur:  #rebond sur mur bas
            self.y = hauteur - self.rayon
            self.vy =self.vy* -1

    def norme_ballon(self):
        norme =math.sqrt(self.vx**2+self.vy**2)
        if norme> self.VITESSE_MAX and norme>0:
            res=self.VITESSE_MAX/norme
            self.vx=self.vx*res
            self.vy=self.vy*res
    def robot_proche(self,robot):
        """Si le robot est proche alors il va taper le ballon"""
        dx=self.vx-robot.x
        dy=self.vy -robot.y
        dist=math.sqrt(dx**2+dy**2)
        if dist<self.rayon:
            vitesse_robot,_=robot.set_vitesse()
            vx_robot=vitesse_robot*math.cos(robot.angle)
            vy_robot=vitesse_robot*math.sin(robot.angle)

            self.vx=self.vx+vx_robot #nouvelle vitesse du ballon
            self.vy=self.vy+vy_robot
        self.norme_ballon() #norme max
