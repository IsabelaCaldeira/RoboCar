import math
from .robocar import RoboCar
from .obstacle import Obstacle, Polygone
from .vecteur import Vecteur


class Simulation:
    """
    Cette classe represente le monde simule
    Elle contient le robot les obstacles et les dimensions de la fenetre
    """

    def __init__(self, largeur, hauteur,robot,mode):
        self.robot = robot # creation du robot 
        # liste des obstacles presents dans l'environnement
        self.obstacles = [
            Obstacle("rectangle", (100, 100), (80, 100)),
            Obstacle("rectangle", (500, 200), (100, 50)),
            Obstacle("rectangle", (300, 450), (50, 50)),
        ]
        #self.obstacles = [Polygone([Vecteur(220, -300), Vecteur(240, 320), Vecteur(160, -300)]),]

        # dimensions du monde
        self.largeur = largeur
        self.hauteur = hauteur
        self.a_collision = False # booleen indiquant si le robot a rencontre un obstacle
        self._last_update = None #garde le moment de la dernière mise à jour de la simulation
        self._last_distance = 0
        self._last_angle_parcouru = 0
        self.mode = mode  # "robocar" ou "adaptateur"

    def collision_segments(A: Vecteur, B: Vecteur, C: Vecteur, D: Vecteur)->bool:
        """ detecte une collision entre les segments AB et CD"""
        AB = A.point_vers_vecteur(B); AC = A.point_vers_vecteur(C); AD = A.point_vers_vecteur(D)
        CD = C.point_vers_vecteur(D); CA = C.point_vers_vecteur(A); CB = C.point_vers_vecteur(B)
        return AB.produit_vectoriel(AC) * AB.produit_vectoriel(AD) < 0 and CD.produit_vectoriel(CA) * CD.produit_vectoriel(CB) < 0

    def raycast_obstacle(self, ray_size:float=5, portee_capteur=120):
        """ renvoie la distance entre le robot et l'obstacle le plus proche dans la direction du capteur """
        ray = Vecteur(ray_size, 0).rotation(self.robot.get_angle()) # vecteur du raycast dans la direction du capteur
        tete_x, tete_y = self.robot.get_position_tete()
        ray_x = Vecteur(tete_x, tete_y) # depart du segment rayon
        ray_y = Vecteur(tete_x + ray.x, tete_y + ray.y) # arrivee du segment rayon

        for ray_i in range(int(portee_capteur/ray_size)): # couper la portee en rayons de taille ray_size
            for obs in self.obstacles:
                points = obs.get_points()
                for j in range(len(points)):
                    if self.collision_segments(ray_x, ray_y, points[j], points[(j+1) % len(points)]):
                        return ray_i * ray_size # nombre de rayons avant collision * taille du rayon
            # ajout d'un epsilon pour eviter de rater la collision
            ray_x.x += ray.x - 0.01; ray_x.y += ray.y - 0.01
            ray_y.x += ray.x - 0.01; ray_y.y += ray.y - 0.01
        return portee_capteur # pas de collision après max rayons

    def distance_obstacle(self, max_range=140): #max_range c'est la portee maximale du capteur (en pixels)
        """
        Calcule la distance au plus proche obstacle devant le robot
        """
        min_dist = max_range
        # vecteur direction du robot
        dir_x = math.cos(self.robot.get_angle())
        dir_y = math.sin(self.robot.get_angle())

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
        angle_gauche = self.robot.get_angle() - math.pi / 2 # angle correspondant au cote gauche du robot
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

        angle_droite = self.robot.get_angle() + math.pi / 2
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
        angle = self.robot.get_angle() #orientation du robot
        front_x = self.robot.x + math.cos(angle) * max_range
        front_y = self.robot.y + math.sin(angle) * max_range

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

    def update(self):
        """Met a jour la simulation"""
        old_state = self.robot.get_position() # on sauvergarde la position actuel du robot

        if self.mode == "adaptateur": #si on utilise un adaptateur
            distance_totale = self.robot.get_distance_parcourue() #distance totale parcourue depuis le debut de la simulation
            angle_total = self.robot.get_angle_parcouru() #angle total parcouru depuis le debut de la simulation

            delta_distance = distance_totale - self._last_distance #distance parcourue depuis la dernière mise à jour
            delta_angle = angle_total - self._last_angle_parcouru #angle parcouru depuis la dernière mise à jour

            self._last_distance = distance_totale #on met a jour la distance totale parcourue
            self._last_angle_parcouru = angle_total #on met a jour l'angle total parcouru

            self.robot.x += delta_distance * math.cos(self.robot.angle) #on met a jour la position du robot en fonction de la distance parcourue et de l'angle actuel
            self.robot.y += delta_distance * math.sin(self.robot.angle)
            self.robot.angle += delta_angle  #mise a jour de l'angle en fonction de l'angle parcouru

        else:  #robocar
            now = time.time()  #on calcule le temps ecoule depuis la derniere mise a jour
            if self._last_update is None:
                dt = 0.0
            else:
                dt = now - self._last_update
            self._last_update = now

            v, w = self.robot.calculer_vitesse() #on recupere la vitesse lineaire et angulaire

            self.robot.x += v * math.cos(self.robot.angle) * dt #mise a jour de la position avec la vitesse
            self.robot.y += v * math.sin(self.robot.angle) * dt
            self.robot.angle += w * dt #mise a jour de l angle

        self.appliquer_murs()  #on verifie les bords de la fenetre
        self.a_collision = self.resoudre_collisions(old_state)  # on verifie collisions avec obstacles

        return self.a_collision