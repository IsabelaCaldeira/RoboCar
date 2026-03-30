import math
import time
from .obstacle import Polygone
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
            Polygone([Vecteur(0, 0), Vecteur(0, hauteur), Vecteur(largeur, hauteur), Vecteur(largeur, 0)]), # bords de la fenetre
            Polygone([Vecteur(500, 200), Vecteur(650, 200), Vecteur(600, 250), Vecteur(450, 250)]),
            Polygone([Vecteur(300, 450), Vecteur(400, 450), Vecteur(350, 500), Vecteur(300, 500)]),  
            Polygone([Vecteur(200, 100), Vecteur(250, 200), Vecteur(300, 150)]),     
        ]

        # dimensions du monde
        self.largeur = largeur
        self.hauteur = hauteur
        self.a_collision = False # booleen indiquant si le robot a rencontre un obstacle
        self._last_update = None #garde le moment de la dernière mise à jour de la simulation
        self._last_distance = 0
        self._last_angle_parcouru = 0
        self.mode = mode  # "robocar" ou "adaptateur"

    @staticmethod # fonction ne depend pas de l'objet simu
    def collision_segments(A: Vecteur, B: Vecteur, C: Vecteur, D: Vecteur)->bool: # rappel: la classe vecteur est aussi utilisée pour représenter des points
        """ detecte une collision entre les segments AB et CD"""
        AB = A.point_vers_vecteur(B); AC = A.point_vers_vecteur(C); AD = A.point_vers_vecteur(D)
        CD = C.point_vers_vecteur(D); CA = C.point_vers_vecteur(A); CB = C.point_vers_vecteur(B)
        return AB.produit_vectoriel(AC) * AB.produit_vectoriel(AD) < 0 and CD.produit_vectoriel(CA) * CD.produit_vectoriel(CB) < 0

    def raycast_robot(self, ray_size=5):
        """ calcule la distance entre le robot et l'obstacle le plus proche devant lui """
        rayon = Vecteur(ray_size, 0).rotation(self.robot.get_angle()) # vecteur du raycast dans la direction de la tete du robot
        tete_x, tete_y = self.robot.get_position_tete()
        ray_x = Vecteur(tete_x, tete_y) # point de depart du segment rayon
        ray_y = Vecteur(tete_x + rayon.x, tete_y + rayon.y) # point d'arrivee du segment rayon

        for ray_i in range(int(self.robot.PORTEE_CAPTEURS/ray_size)): # couper la portee en rayons de taille ray_size
            for obs in self.obstacles:
                points = obs.get_points()
                for j in range(len(points)):
                    if self.collision_segments(ray_x, ray_y, points[j], points[(j+1) % len(points)]):
                        return ray_i * ray_size # nombre de rayons avant collision * taille du rayon   
                       
            ray_x.soustraction(Vecteur(0.01, 0.01)); ray_y.soustraction(Vecteur(0.01, 0.01)) # ajout d'un epsilon pour eviter de rater la collision
        return self.robot.PORTEE_CAPTEURS # pas de collision après max rayons
    
    def distance_cote_robot(self, angle):
        """Calcule la distance libre sur un cote du robot
        Cette fonction sert a savoir si le robot peut tourner dans cette direcrtion
        """
        robot = self.robot
        robot.tourner_tete(angle) # (90 = gauche, -90 = droite) tourner la tete pour mesurer la distance dans cette direction
        distance = self.raycast_robot() # mesurer la distance dans la direction de la tete
        robot.tourner_tete(0) # remettre la tete dans l'alignement du corps
        return distance

    def collision(self, obstacle:Polygone)->bool:
        """
        Verifie si le robot entre en collision avec un obstacle
        On compare le rectangle du robot avec le rectangle de l'obstacle
        """
        robot_forme = self.robot.get_forme_robot()
        robot_points = robot_forme.get_points()
        points = obstacle.get_points()
        for j in range(len(points)):
            if self.collision_segments(robot_points[0], robot_points[2], points[j], points[(j+1) % len(points)]): # on verifie si les diagonales du robot intersectent l'obstacle
                return True
        return False

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

        self.a_collision = self.resoudre_collisions(old_state)  # on verifie collisions avec obstacles

        return self.a_collision