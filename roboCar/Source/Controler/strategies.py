import math


class AvancerXMetres:
    """Strategie qui fait avancer ou reculer le robot"""
    def __init__(self, adaptateur, distance, vitesse):
        self.adaptateur = adaptateur #l'adaptateur qui permet d'envoyer des commandes au robot
        self.distance = distance #distance cible a atteindre
        self.vitesse = vitesse #vitesse de deplacement
        self.distance_parcourue = 0 #distance parcourue depuis le debut de la strategie

    #il faut calculer les positions sans self.depart , on a besoin de quelque chose comme get_distance_parcorue 
    def start(self):
        self.distance_parcourue = 0 #on reset la distance au debut de la strategie

    def step(self):
        if self.stop(): #si la distance cible est atteinte on arrete
            self.adaptateur.arreter()
            return
        if self.vitesse >= 0:
            self.adaptateur.avancer(self.vitesse)
        else:
            self.adaptateur.reculer(-self.vitesse)
        self.distance_parcourue += self.adaptateur.get_distance_parcourue()

    #On a pas access aux coord du robot reel, donc il faut trouver une autre façon calculer la distance
    def stop(self):
        distance_pixels = self.distance * 100 #conversion metres en pixels
        if self.depart is None:
            return False
        #difference entre la position actuelle et la position de depart
        dx = self.sim.robot.x - self.depart[0]
        dy = self.sim.robot.y - self.depart[1]
        distance_parcourue = math.sqrt(dx**2 + dy**2)
        return distance_parcourue >= distance_pixels #si la distance voulue es atteinte alors la strategies s'arrete
    
#Meme principe que les problemes d'AvancerXMetres
class TournerXDegrees:
    """Strategie qui fait tourner le robot jusqu'a atteindre un angle donne"""

    def __init__(self, adaptateur, angle, vitesse):
        self.adaptateur = adaptateur
        self.angle = math.radians(angle) #angle cible converti en radians
        self.vitesse = vitesse #vitesse de rotation
        self.angle_parcouru = 0 #angle deja parcouru

    def start(self):
        self.angle_parcouru = 0

    def step(self):
        if self.stop(): #si on a deja tourne assez on arrete
            self.adaptateur.arreter()
            return
        self.adaptateur.tourner_sur_place(self.vitesse)
        self.angle_parcouru += abs(self.adaptateur.get_angle_parcouru())

    def stop(self):
        return self.angle_parcouru >= self.angle
class Sequence:
    """Strategie sequentielle qui execute une liste de strategies dans l'ordre"""
    def __init__(self, strategies):
        self.strategies = strategies #liste des strategies a executer
        self.i = 0 #index de la strategie actuelle

    def start(self):
        self.i = 0 #on initialise la sequence
        #on demarre la premiere strategie si elle existe
        if self.strategies:
            self.strategies[0].start()
    def step(self):
        if self.stop(): #si toutes les strategies sont finies on ne fait rien
            return
        strat = self.strategies[self.i] #strategie actuelle
        strat.step() #execution d'un pas
        if strat.stop(): #si la strategie est terminee on passe a la suivante
            self.i += 1
            if not self.stop(): #si il reste des strategies on start la suivante
                self.strategies[self.i].start()

    def stop(self):
        return self.i >= len(self.strategies) #True si toutes les strategies ont ete executees

class Condition:
    """Strategie conditionnelle qui choisit dynamiquement entre 2 strategies"""
    def __init__(self, s1, s2, adaptateur, distance):
        self.s1 = s1  #strategie si obstacle proche
        self.s2 = s2  #strategie sinon
        self.adaptateur = adaptateur
        self.distance = distance #distance seuil pour detecter un obstacle
        self.current = None #strategie actuellement active

    def start(self):
        self.current = None #aucune strategie active au debut

    def step(self):
        d = self.adaptateur.get_distance() #lecture de la distance devant le robot
        if d<self.distance: #si obstacle proche donc strategie 1
            new =self.s1
        else:
            new=self.s2
        if self.current is not new: #si la strategie change on reset
            self.current = new
            self.current.start()
        elif self.current.stop(): #si la strategie est la meme mais terminee on la relance
            self.current.start()
        self.current.step() #execution d'un pas

    def stop(self):
        return False #une strategie conditionnelle ne s'arrete jamais seule
class Boucle:
    """Strategie qui repete une autre strategie a l'infini"""
    def __init__(self, strat):
        self.strat = strat  #strategie interne a repeter

    def start(self):
        self.strat.start() #on demarre la strategie

    def step(self):
        if self.strat.stop(): #si la strategie est finie -> on la relance
            self.strat.start()

        self.strat.step() #sinon on continue

    def stop(self):
        return False #une boucle ne s'arrete jamais