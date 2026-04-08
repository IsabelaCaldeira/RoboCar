class Ballon:

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
            self.vx *= -1
        if self.y - self.rayon < 0: #rebond sur mur haut
            self.y = self.rayon
            self.vy *= -1
        if self.y + self.rayon > hauteur:  #rebond sur mur bas
            self.y = hauteur - self.rayon
            self.vy *= -1