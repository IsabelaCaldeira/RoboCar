import math
from robocar import RoboCar
from obstacle import Obstacle


class Simulation:
    """
    Cette classe represente le monde simule
    Elle contient le robot , les obstacles et les dimensions de la fenêtre
    """

    def __init__(self, largeur, hauteur):
        self.robot = RoboCar("Flash", (400, 300), 0) # creation du robot au centre de la fenetre
        # liste des obstacles presents dans l'environnement
        self.obstacles = [
            Obstacle("rectangle", (100, 100), (80, 100)),
            Obstacle("rectangle", (500, 200), (100, 50)),
            Obstacle("rectangle", (300, 450), (50, 50)),
        ]
        # dimensions du monde
        self.largeur = largeur
        self.hauteur = hauteur
        self.a_collision = False # booleen indiquant si le robot a rencontre un obstacle

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
            
    def distance_obstacle(self, max_range=140): #max_range c'est la portee maximale du capteur (en pixels)
        """
        Calcule la distance au plus proche obstacle devant le robot
        """
        min_dist = max_range
        # vecteur direction du robot
        dir_x = math.cos(self.robot.angle)
        dir_y = math.sin(self.robot.angle)

        for obs in self.obstacles:
            # centre de l'obstacle
            cx = obs.pos[0] + obs.dim[0] / 2
            cy = obs.pos[1] + obs.dim[1] / 2
            # vecteur robot en  centre obstacle
            dx = cx - self.robot.x
            dy = cy - self.robot.y
            # projection du vecteur obstacle sur la direction du robot pour  savoir si l'obstacle est devant
            projection = dx * dir_x + dy * dir_y

            if 0 < projection < max_range:
                # distance robot en centre de l'obstacle
                dist_au_centre = math.sqrt(dx**2 + dy**2)
                rayon_obs = max(obs.dim) / 2 # approximation du "rayon" de l'obstacle

                dist_au_bord = dist_au_centre - rayon_obs # distance robot en bord de l'obstacle

                if dist_au_bord < min_dist:
                    min_dist = max(0, dist_au_bord)

        return min_dist
    def distance_cote_gauche(self, max_range=60):
        """Calcule la distance libre sur le cote gauche du robot
        Cette fonction sert a savoir si le robot peut tourner a gauche
        """
        angle_gauche = self.robot.angle - math.pi / 2 # angle correspondant au cote gauche du robot
        dir_x = math.cos(angle_gauche)
        dir_y = math.sin(angle_gauche)
        # point de test sur le côté gauche
        side_x = self.robot.x + dir_x * max_range
        side_y = self.robot.y + dir_y * max_range
        # distance au mur le plus proche
        dist_x = min(side_x, self.largeur - side_x)
        dist_y = min(side_y, self.hauteur - side_y)
        min_dist = min(dist_x, dist_y)

        for obs in self.obstacles:  # on teste aussi les obstacles
            cx = obs.pos[0] + obs.dim[0] / 2
            cy = obs.pos[1] + obs.dim[1] / 2

            dx = cx - self.robot.x
            dy = cy - self.robot.y

            projection = dx * dir_x + dy * dir_y

            if 0 < projection < max_range:
                dist = math.sqrt(dx**2 + dy**2) - max(obs.dim) / 2
                min_dist = min(min_dist, max(0, dist))

        return min_dist
    def distance_cote_droite(self, max_range=60):
        """
        Calcule la distance libre sur le cote droit du robot
        Cette fonction sert a savoir si le robot peut tourner a droite
        """

        angle_droite = self.robot.angle + math.pi / 2
        dir_x = math.cos(angle_droite)
        dir_y = math.sin(angle_droite)

        side_x = self.robot.x + dir_x * max_range
        side_y = self.robot.y + dir_y * max_range

        dist_x = min(side_x, self.largeur - side_x)
        dist_y = min(side_y, self.hauteur - side_y)
        min_dist = min(dist_x, dist_y)

        for obs in self.obstacles:
            cx = obs.pos[0] + obs.dim[0] / 2
            cy = obs.pos[1] + obs.dim[1] / 2

            dx = cx - self.robot.x
            dy = cy - self.robot.y

            projection = dx * dir_x + dy * dir_y

            if 0 < projection < max_range:
                dist = math.sqrt(dx**2 + dy**2) - max(obs.dim) / 2
                min_dist = min(min_dist, max(0, dist))

        return min_dist
    
    def distance_mur(self, max_range=120):
        """
        Calcule la distance au mur devant le robot 
        On regarde un point situe devant le robot a max_range pixels, puis on calcule a quelle distance il est du bord de la fenetre
        """
        # point situe devant le robot
        front_x = self.robot.x + math.cos(self.robot.angle) * max_range
        front_y = self.robot.y + math.sin(self.robot.angle) * max_range

        dist_x = min(front_x, self.largeur - front_x) # distance au bord gauche/droit
        dist_y = min(front_y, self.hauteur - front_y) # distance au bord haut/bas
        return min(dist_x, dist_y)

    def obtenir_rectangle(self):
        """
        Construit un rectangle simplifie autour du robot
        Cela sert a faire les collisions
        """
        half_L = self.robot.longueur / 2
        half_W = self.robot.largeur / 2
        return (
            self.robot.x - half_L,
            self.robot.y - half_W,
            self.robot.longueur,
            self.robot.largeur
        )

    def collision(self, obstacle):
        """
        Verifie si le robot entre en collision avec un obstacle
        On compare le rectangle du robot avec le rectangle de l'obstacle
        """
        x1, y1, w1, h1 = self.obtenir_rectangle()
        x2, y2 = obstacle.pos
        w2, h2 = obstacle.dim
        return (
            x1 < x2 + w2 and
            x1 + w1 > x2 and
            y1 < y2 + h2 and
            y1 + h1 > y2
        )

    def appliquer_murs(self):
        """Empeche le robot de sortir de la fenetre"""
        half_L = self.robot.longueur / 2.0
        half_W = self.robot.largeur / 2.0
        self.robot.x = max(half_L, min(self.robot.x, self.largeur - half_L))
        self.robot.y = max(half_W, min(self.robot.y, self.hauteur - half_W))

    def resoudre_collisions(self, old_state):
        """Empeche le robot de traverser un obstacle"""
        for obs in self.obstacles:
            if self.collision(obs):
                self.robot.x, self.robot.y = old_state
                return True
        return False

    def update(self, dt):
        """Met a jour la simulation"""
        old_state = (self.robot.x, self.robot.y)
        self.robot.update(dt) # mise a jour physique du robot
        self.appliquer_murs() # on verifie les bords de la fenetre
        self.a_collision = self.resoudre_collisions(old_state)  # on verifie collisions avec obstacles
        return self.a_collision