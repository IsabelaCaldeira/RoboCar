import math


class AvancerXMetres:
    """Strategie qui fait avancer ou reculer le robot"""
    def __init__(self, adaptateur, distance, vitesse):
        self.adaptateur = adaptateur #l'adaptateur qui permet d'envoyer des commandes au robot
        self.distance = distance #distance cible a atteindre
        self.vitesse = vitesse #vitesse de deplacement
        self.distance_parcourue = 0 #distance parcourue depuis le debut de la strategie

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

    def stop(self):
        return self.distance_parcourue >= self.distance

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

