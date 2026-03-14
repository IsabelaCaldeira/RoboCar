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
