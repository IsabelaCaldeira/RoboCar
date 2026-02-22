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
        """Recuperer la vitesse des roues"""
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
    def update(self, dt):
        """Mise a jour du robot"""
        v, w = self.calculer_vitesse()
        self.x += v * math.cos(self.angle) * dt
        self.y += v * math.sin(self.angle) * dt
        self.angle += w * dt #si w<0 on tourne a droite et a gauche sinon
    def distance_obstacle(self, obstacles, max_range=120):
        """Cette fonction regarde l'obstacle le plus proche"""
        min_dist = max_range #distance minimale

        # vecteur direction du robot
        dir_x = math.cos(self.angle)
        dir_y = math.sin(self.angle)

        for obs in obstacles:

            ox, oy = obs.pos
            dx = ox - self.x #on cree un vecteur du robot vers l’obstacle
            dy = oy - self.y

            # projection dans la direction du robot
            projection = dx * dir_x + dy * dir_y #produit scalaire
            if 0 < projection < max_range: #on regard si l'obstacle est proche
                dist = math.sqrt(dx**2 + dy**2)
                if dist < min_dist:
                    min_dist = dist #on garde l'obstacle le plus proche devant

        return min_dist
    def distance_mur(self, largeur, hauteur, max_range=120):
        """Cette fonction renvoie la distance au mur le plus proche dans la direction du robot"""
        # point devant le robot
        front_x = self.x + math.cos(self.angle) * max_range #on avance de 120 pixels dans la direction du robot
        front_y = self.y + math.sin(self.angle) * max_range

        # distance au mur le plus proche
        dist_x = min(front_x, largeur - front_x)
        dist_y = min(front_y, hauteur - front_y)

        return min(dist_x, dist_y)
    def obtenir_rectangle(self):
        """cette fonction cree un rectangle simplifie autour du robot pour faire les collisions"""
        half_L = self.longueur / 2 #le robot est centre donc on calcule le centre pour le retrancher apres a x et y
        half_W = self.largeur / 2

        return (
            self.x - half_L, #on va du centre vers la gauche
            self.y - half_W, #on va du centre vers le haut
            self.longueur,
            self.largeur
        )
    def collision(self, obstacle):
        """Cette fonction detetcte la collision"""
        x1, y1, w1, h1 = self.obtenir_rectangle()
        x2, y2 = obstacle.pos
        w2, h2 = obstacle.dim

        return (
        x1 < x2 + w2 and
        x1 + w1 > x2 and
        y1 < y2 + h2 and
        y1 + h1 > y2
    )