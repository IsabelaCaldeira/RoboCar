import math
class AvancerXMetres:
    """
    Strategie qui fait avancer le robot d'une distance donnee
    Le robot avance jusqu'a ce que la distance parcourue atteigne la distance demandee (en metres)
    """

    def _init_(self, simulation, distance, vitesse, marge_mur=35):
        self.sim = simulation      # reference vers la simulation 
        self.distance = distance   # distance a parcourir en metres
        self.vitesse = vitesse     # vitesse des roues
        self.marge_mur = marge_mur # distance minimale autorisee avec un mur

        self.depart = None         # position de depart du robot

    def start(self):
        self.depart = None

    def step(self):
        if self.depart is None:
            self.depart = (self.sim.robot.x, self.sim.robot.y)

        if self.stop():
            self.sim.robot.arreter()
            return

        self.sim.robot.avancer(self.vitesse)

    def stop(self):
        distance_pixels = self.distance * 100
        if self.depart is None:
            return False
        dx = self.sim.robot.x - self.depart[0]
        dy = self.sim.robot.y - self.depart[1]
        distance_parcourue = math.sqrt(dx*2 + dy*2)
        return distance_parcourue >= distance_pixels
    
#Il faut creer une nouvelle classe TournerXDegree
class TournerXDegrees:
    """ Strategie qui fait tourner le robot d'un angle donnee
    Le robot tourne jusqu'a ce que la distance parcourue atteigne la distance demandee (en metres)
    """
    
    def __init__(self, simulation):
        pass
class Reculer:
    """
    Strategie qui fait reculer le robot sur une distance donnee qui est utilisee quand le robot est bloque
    """

    def _init_(self, simulation, vitesse=50, distance=0.4):

        self.sim = simulation
        self.vitesse = vitesse # vitesse a laquelle le robot va reculer
        self.distance = distance #distance que le robot doit reculer
        self.depart = None #position de depart du robot quand la strategie commence

    def start(self):
        self.depart = None

    def step(self):
        if self.depart is None:
            self.depart = (self.sim.robot.x, self.sim.robot.y)

        if self.stop():
            self.sim.robot.arreter()
            return

        self.sim.robot.reculer(self.vitesse)

    def stop(self):
        distance_pixels = self.distance * 100
        if self.depart is None:
            return False
        dx = self.sim.robot.x - self.depart[0]
        dy = self.sim.robot.y - self.depart[1]
        distance_parcourue = math.sqrt(dx*2 + dy*2)
        return distance_parcourue >= distance_pixels


class EviterObstacles:
    """
    Strategie principale d'evitement des obstacles le robot detecte les obstacles devant lui choisit la direction avec le plus d'espace
    et tourne dans cette direction
    """

    def __init__(self, simulation, vitesse_avance=80, vitesse_tourne=60, seuil=50):

        self.sim = simulation
        self.vitesse_avance = vitesse_avance
        self.vitesse_tourne = vitesse_tourne
        self.seuil = seuil # distance a partir de laquelle on considere qu'un obstacle est proche
        self.direction = None  # direction choisie pour contourner

    def start(self):
        self.direction = None
        pass

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
        """Agit si un obstacle est détecté à une distance inférieure à la distance de sécurité"""
        self.choisir_direction(dist_gauche, dist_droite) #choisir la direction selon l'espace disponible
        d_sec = max(self.seuil, self.sim.robot.longueur / 2)
        if distance < d_sec * 0.5: # si l'obstacle est très proche
            self.sim.robot.reculer(self.vitesse_avance * 0.6) #flash recule un peu pour se dégager
            return True
        if distance < d_sec : # si l'obstacle est proche mais pas critique
            self.tourner_direction() #flash tourne dans la direction choisie
            return True
        return False #si l'obstacle est suffisamment loin, aucune action n'est nécessaire

    def step(self):
        dist_obs = self.sim.distance_obstacle(max_range=120)  # distance a l'obstacle devant
        dist_mur = self.sim.distance_mur(max_range=120) # distance au mur devant
        dist_gauche = self.sim.distance_cote_gauche(max_range=60)
        dist_droite = self.sim.distance_cote_droite(max_range=60)
        #on prend la distance la plus dangereuse
        distance = min(dist_obs, dist_mur)
    
        if self.agir_si_proche(distance, dist_gauche, dist_droite):
            return False

        #si aucun obstacle alors on avance
        self.direction = None
        self.sim.robot.avancer(self.vitesse_avance)
        return False
    
    def stop(self):
        return False
    




    

    def update(self, dt):
        dist_obs = self.sim.distance_obstacle(max_range=200)  # distance a l'obstacle devant
        dist_mur = self.sim.distance_mur(max_range=120) # distance au mur devant
        # distances sur les cotes
        dist_gauche = self.sim.distance_cote_gauche(max_range=60)
        dist_droite = self.sim.distance_cote_droite(max_range=60)
        # on prend la distance la plus dangereuse
        distance = min(dist_obs, dist_mur)
    
        if self.agir_si_proche(distance, dist_gauche, dist_droite, dt):
            return False

        # si aucun obstacle alors on avance
        self.direction = None
        self.sim.robot.avancer(self.vitesse_avance)
        return False

#Il faut changer ça pour les strategies sequencielles
class GestionStrategies:
    """
    Classe qui gere toutes les strategies du robot
    """

    def __init__(self, simulation):

        self.sim = simulation
        # differentes strategies disponibles
        self.avance_depart = AvancerXMetres(simulation, distance=1, vitesse=80)
        #self.freinage = FreinageProgressif(simulation)
        self.recul = Reculer(simulation, vitesse=50, distance=0.4)
        self.evitement = EviterObstacles(simulation, vitesse_avance=80, vitesse_tourne=60, seuil=80)

        self.phase = "DEPART" # etat actuel du robot

    #C'est mieux de calculer dt ici que l'avoir comme parametre
    def update(self, dt):
        """
        Fonction appelee a chaque frame qui choisit quelle strategie appliquer
        """
        if self.phase == "DEPART": # phase de depart

            fini = self.avance_depart.update()

            if fini:
                self.phase = "EVITEMENT"
        elif self.phase == "RECUL":  # phase de recul

            fini = self.recul.update()

            if fini:
                self.phase = "EVITEMENT"
        elif self.phase == "FREINAGE":  # phase de freinage

            fini = self.arreter.update()

            if fini:
                self.phase = "EVITEMENT"
        elif self.phase == "EVITEMENT": # phase principale : evitement

            dist_obs = self.sim.distance_obstacle(max_range=140)
            dist_mur = self.sim.distance_mur(max_range=70)

            dist_gauche = self.sim.distance_cote_gauche(max_range=60)
            dist_droite = self.sim.distance_cote_droite(max_range=60)
            if min(dist_obs, dist_mur) < 20 and dist_gauche < 25 and dist_droite < 25:  # si on est completement bloque

                self.recul.declencher()
                self.phase = "RECUL"
            elif self.sim.a_collision: # si collision detectee

                self.phase = "FREINAGE"

            else: # sinon on applique l'evitement
                self.evitement.update(dt)
