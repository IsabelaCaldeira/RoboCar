import math
class AvancerXMetres:
    """
    Strategie qui fait avancer le robot d'une distance donnee
    Le robot avance jusqu'a ce que la distance parcourue atteigne la distance demandee (en metres)
    """

    def __init__(self, simulation, distance, vitesse, marge_mur=35):
        self.sim = simulation      # reference vers la simulation 
        self.distance = distance   # distance a parcourir en metres
        self.vitesse = vitesse     # vitesse des roues
        self.marge_mur = marge_mur # distance minimale autorisee avec un mur

        self.depart = None         # position de depart du robot

    def start(self):
        self.depart = None #on reinitialise la position de depart la premiere fois que step() sera appelee

    def step(self):
        if self.depart is None:
            self.depart = (self.sim.robot.x, self.sim.robot.y) # #on enregistre la position actuelle du robot

        if self.stop():
            self.sim.robot.arreter() #on arrete le robot et on quitte la fonction si la distance demandee a deja ete parcourue
            return

        self.sim.robot.avancer(self.vitesse) #sinon le robot continue d'avancer

    def stop(self):
        distance_pixels = self.distance * 100 #conversion metres en pixels
        if self.depart is None:
            return False
        #difference entre la position actuelle et la position de depart
        dx = self.sim.robot.x - self.depart[0]
        dy = self.sim.robot.y - self.depart[1]
        distance_parcourue = math.sqrt(dx**2 + dy**2)
        return distance_parcourue >= distance_pixels #si la distance voulue es atteinte alors la strategies s'arrete
    
class TournerXDegrees:
    """ Strategie qui fait tourner le robot d'un angle X donnee
    Le robot tourne jusqu'a ce que l'angle parcouru atteigne l'angle demande
    """
    
    def __init__(self,simulation,angle,vitesse):
        self.sim = simulation # reference vers la simulation
        self.angle = angle # distance a parcourir en degree
        self.vitesse = vitesse # vitesse des roues

        self.depart = None #angle de depart du robot
        
    def start(self):
        self.depart = None #reinitialisation avant de commencer la strategie
        
    def step(self):
        if self.depart is None:
            self.depart = self.sim.robot.angle #on enregistre l'orientation actuelle du robot
            
        if self.stop(): #si l'angle voulu est atteint on arrete le robot
            self.sim.robot.arreter()
            return
        
        self.sim.robot.tourner_sur_place(self.vitesse)
        
    def stop(self):
        if self.depart is None:
            return False

        angle_voulu = math.radians(self.angle)
        angle_parcouru = abs(self.sim.robot.angle - self.depart) #difference entre angle actuel et angle de depart 
        return angle_parcouru >= angle_voulu
        
        
class Reculer:
    """
    Strategie qui fait reculer le robot sur une distance donnee qui est utilisee quand le robot est bloque
    """

    def __init__(self, simulation, vitesse=50, distance=0.4):
        self.sim = simulation
        self.vitesse = vitesse # vitesse a laquelle le robot va reculer
        self.distance = distance #distance que le robot doit reculer
        self.depart = None #position de depart du robot quand la strategie commence

    def start(self):
        self.depart = None #reinitialisation du point de depart

    def step(self):
        if self.depart is None:
            self.depart = (self.sim.robot.x, self.sim.robot.y) #on memorise la position de depart

        if self.stop():
            self.sim.robot.arreter()
            return

        self.sim.robot.reculer(self.vitesse)

    def stop(self):
        distance_pixels = self.distance * 100 #conversion metres en piexels
        if self.depart is None:
            return False
        #ecart entre position actuelle et position de depart
        dx = self.sim.robot.x - self.depart[0]
        dy = self.sim.robot.y - self.depart[1]
        distance_parcourue = math.sqrt(dx**2 + dy**2) #distance totale parcourue
        return distance_parcourue >= distance_pixels


class EviterObstacles:
    """
    Strategie principale d'evitement des obstacles le robot detecte les obstacles devant lui choisit la direction avec le plus d'espace
    et tourne dans cette direction
    """

    def __init__(self, simulation, vitesse_avance=80, vitesse_tourne=60, seuil=50):

        self.sim = simulation #reference vers sim
        self.vitesse_avance = vitesse_avance #vitesse normale quand le robot avance
        self.vitesse_tourne = vitesse_tourne  #vitesse utilisee quand le robot tourne pour eviter
        self.seuil = seuil #distance a partir de laquelle on considere qu'un obstacle est proche
        self.direction = None  #direction choisie pour contourner

    def start(self):
        self.direction = None #aucune direction est choisie au debut

    def choisir_direction(self, dist_gauche, dist_droite):
        """Choisit la direction avec le plus d'espace"""
        if self.direction is None:
            self.direction = "gauche" if dist_gauche > dist_droite else "droite"
    
    def tourner_direction(self):
        """Applique une rotation selon la direction choisie"""
        if self.direction == "gauche":
            self.sim.robot.tourner_gauche(self.vitesse_tourne)
        else:
            self.sim.robot.tourner_droite(self.vitesse_tourne)
    
    def agir_si_proche(self, distance, dist_gauche, dist_droite):
        """Agit si un obstacle est detecte a une distance inferieure a la distance de securite"""
        self.choisir_direction(dist_gauche, dist_droite) #choisir la direction selon l'espace disponible
        d_sec = max(self.seuil, self.sim.robot.longueur / 2)
        if distance < d_sec * 0.5: #si l'obstacle est tres proche
            self.sim.robot.reculer(self.vitesse_avance * 0.6) #flash recule un peu pour se degager
            return True
        if distance < d_sec : # si l'obstacle est proche mais pas critique
            self.tourner_direction() #flash tourne dans la direction choisie
            return True
        return False #si l'obstacle est suffisamment loin aucune action est necessaire

    def step(self):
        dist_obs = self.sim.distance_obstacle(max_range=120)  # distance a l'obstacle devant
        dist_mur = self.sim.distance_mur(max_range=120) # distance au mur devant
        dist_gauche = self.sim.distance_cote_gauche(max_range=60)
        dist_droite = self.sim.distance_cote_droite(max_range=60)
        #on prend la distance la plus dangereuse
        distance = min(dist_obs, dist_mur)
    
        if self.agir_si_proche(distance, dist_gauche, dist_droite):  #si le robot a deja fait une action d'evitement
            return False

        #si aucun obstacle alors on avance
        self.direction = None
        self.sim.robot.avancer(self.vitesse_avance)
        return False
    
    def stop(self):
        return False

class GestionStrategies:
    """
    Classe qui gere toutes les strategies du robot
    """
    def __init__(self, simulation):
        self.sim = simulation #reference vers sim
        self.strats = [
            AvancerXMetres(simulation, distance=1, vitesse=80),
            TournerXDegrees(simulation, angle=90, vitesse=80),
            EviterObstacles(simulation, vitesse_avance=80, vitesse_tourne=60, seuil=80),
        ] #liste des strategies normales a executer dans l'ordre
        self.recul = Reculer(simulation, vitesse=50, distance=0.4) #strategie speciale utilisee uniquement en cas de collision
        self.cur = -1 #indice de la strategie actuelle
        self.mode_collision = False #indique si on est actuellement en train de gerer une collision

    def start(self):
        self.cur = -1
        self.mode_collision = False

    def step(self):
        if self.stop(): #si tout est termine on fait rien
            return

        if self.mode_collision: #si on est deja en mode collision on continue la strat de recul
            if self.recul.stop():
                self.sim.robot.arreter()
                self.mode_collision = False
                return
            self.recul.step() #on continue a reculer si le recul n'est pas termine
            return

        if self.sim.a_collision: #si une nouvelle collision est detectee
            self.mode_collision = True #on active le mode collision
            self.recul.start()
            self.recul.step()
            return

        if self.cur < 0 or self.strats[self.cur].stop(): #si aucune strategie a encore commence ou si la strategie actuelle est terminee
            self.cur += 1
            if self.cur >= len(self.strats): #si on a depasse la liste des strategies
                return #il n'y a plus rien a executer
            self.strats[self.cur].start()
        self.strats[self.cur].step() #on execute une etape de la strategie actuelle

    def stop(self):
        return (
            not self.mode_collision and #termine si on est pas en mode collision
            self.cur == len(self.strats) - 1 and #si on est sur la derniere strategie
            self.strats[self.cur].stop() #si la derniere strategie est finie
        )