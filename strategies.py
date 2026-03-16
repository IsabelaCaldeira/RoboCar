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
        self.terminee = False      # indique si la strategie est terminee

    def update(self, dt):
        """
        Fonction appelee a chaque frame qui fait avancer le robot et verifie si la distance demandee a ete parcourue
        """

        if self.terminee:
            return True
        distance_pixels = self.distance * 100  # conversion de metres en pixels 
        if self.depart is None:
            self.depart = (self.sim.robot.x, self.sim.robot.y) # on memorise la position de depart la premiere fois

        if self.sim.distance_mur(max_range=60) < self.marge_mur: #si on est trop proche d'un mur on arrete
            self.sim.freiner(dt)
            self.terminee = True
            return True

        self.sim.avancer(self.vitesse) # on fait avancer le robot

        # calcul de la distance parcourue depuis le depart
        dx = self.sim.robot.x - self.depart[0]
        dy = self.sim.robot.y - self.depart[1]
        distance_parcourue = math.sqrt(dx**2 + dy**2)

        # si on a atteint la distance voulue
        if distance_parcourue >= distance_pixels:
            self.sim.freiner(dt)
            self.terminee = True
            return True

        return False
class FreinageProgressif:
    """
    Strategie qui ralentit progressivement le robot jusqu'a ce qu'il soit completement arrete
    """

    def __init__(self, simulation):
        self.sim = simulation

    def update(self, dt):
        self.sim.freiner(dt)  # on applique le freinage progressif
        vG, vR = self.sim.robot.get_wheel_speeds() # on recupere la vitesse des deux roues
        return abs(vG) < 1 and abs(vR) < 1 # si les vitesses sont presque nulles alors le robot est arrete

class Reculer:
    """
    Strategie qui fait reculer le robot sur une distance donnee qui est utilisee quand le robot est bloque
    """

    def __init__(self, simulation, vitesse=50, distance=0.4):

        self.sim = simulation
        self.vitesse = vitesse # vitesse a laquelle le robot va reculer
        self.distance = distance #distance que le robot doit reculer
        self.depart = None #position de depart du robot quand la strategie commence
        self.actif = False #booleen qui indique si la strategie est active

    def declencher(self):
        """
        Lance la strategie de recule
        """
        self.depart = None
        self.actif = True

    def update(self, dt):

        # si la strategie n'est pas active
        if not self.actif:
            return True
        distance_pixels = self.distance * 100
        if self.depart is None: 
            self.depart = (self.sim.robot.x, self.sim.robot.y)  # memorisation de la position de départ

        self.sim.reculer(self.vitesse)  # on fait reculer le robot

        # calcul distance parcourue
        dx = self.sim.robot.x - self.depart[0]
        dy = self.sim.robot.y - self.depart[1]
        distance_parcourue = math.sqrt(dx**2 + dy**2)

        if distance_parcourue >= distance_pixels: # si la distance est atteinte
            self.sim.freiner(dt)
            self.actif = False
            return True

        return False


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

    def distance_securite(self,dt):
        """Calcule la distance minimale à garder avant d'agir"""
        #un seuil fixe; une marge liée à la vitesse et au temps de réaction; la demi-longueur du robot pour éviter le contact
        return max(self.seuil, self.vitesse_avance * dt * 2.5 + self.sim.robot.longueur/2) 
    
    def choisir_direction(self, dist_gauche, dist_droite):
        """Choisit la direction avec le plus d'espace"""
        if self.direction is None:
            self.direction = "gauche" if dist_gauche > dist_droite else "droite"

    def update(self, dt):
        dist_obs = self.sim.distance_obstacle(max_range=140)  # distance a l'obstacle devant
        dist_mur = self.sim.distance_mur(max_range=70) # distance au mur devant
        # distances sur les cotes
        dist_gauche = self.sim.distance_cote_gauche(max_range=60)
        dist_droite = self.sim.distance_cote_droite(max_range=60)
        # on prend la distance la plus dangereuse
        distance = min(dist_obs, dist_mur)
    
        if distance < self.seuil:  # obstacle detecte devant

          
            if self.direction is None:  # on choisit une direction si ce n'est pas deja fait
                if dist_gauche > dist_droite:  # on choisit le cote avec le plus d'espace
                    self.direction = "gauche"
                else:
                    self.direction = "droite"

            # rotation selon la direction choisie
            if self.direction == "gauche":
                self.sim.tourner_gauche(self.vitesse_tourne)
            else:
                self.sim.tourner_droite(self.vitesse_tourne)

        else:
            # si aucun obstacle alors on avance
            self.direction = None
            self.sim.avancer(self.vitesse_avance)

        return False


class GestionStrategies:
    """
    Classe qui gere toutes les strategies du robot
    """

    def __init__(self, simulation):

        self.sim = simulation
        # differentes strategies disponibles
        self.avance_depart = AvancerXMetres(simulation, distance=1, vitesse=80)
        self.freinage = FreinageProgressif(simulation)
        self.recul = Reculer(simulation, vitesse=50, distance=0.4)
        self.evitement = EviterObstacles(simulation, vitesse_avance=80, vitesse_tourne=60, seuil=50)

        self.phase = "DEPART" # etat actuel du robot

    def update(self, dt):
        """
        Fonction appelee a chaque frame qui choisit quelle strategie appliquer
        """
        if self.phase == "DEPART": # phase de depart

            fini = self.avance_depart.update(dt)

            if fini:
                self.phase = "EVITEMENT"
        elif self.phase == "RECUL":  # phase de recul

            fini = self.recul.update(dt)

            if fini:
                self.phase = "EVITEMENT"
        elif self.phase == "FREINAGE":  # phase de freinage

            fini = self.freinage.update(dt)

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
