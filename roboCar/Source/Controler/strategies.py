import math
import time


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
        delta = self.adaptateur.get_distance_parcourue()
        if self.stop(): #si la distance cible est atteinte on arrete
            self.adaptateur.arreter()
            return
        self.adaptateur.set_vitesse(self.vitesse, 0) #si vitesse negative on recule
        self.distance_parcourue += delta

    def stop(self):
        return self.distance_parcourue >= self.distance #True si distance cible est atteinte

class TournerXDegrees:
    """Strategie qui fait tourner le robot jusqu'a atteindre un angle donne"""

    def __init__(self, adaptateur, angle, vitesse_angulaire,vitesse_lineaire=0):
        self.adaptateur = adaptateur
        self.angle = math.radians(angle) #angle cible converti en radians
        self.vitesse_angulaire = vitesse_angulaire 
        self.vitesse_lineaire = vitesse_lineaire
        self.angle_parcouru = 0 #angle deja parcouru

    def start(self):
        self.angle_parcouru = 0

    def step(self):
        self.adaptateur.get_distance_parcourue()
        if self.stop(): #si on a deja tourne assez on arrete
            self.adaptateur.arreter()
            return
        self.adaptateur.set_vitesse(self.vitesse_lineaire, self.vitesse_angulaire) #si vitesse_lineaire=0 on tourne sur place et sinon on tourne en avancant
        self.angle_parcouru += abs(self.adaptateur.get_angle_parcouru())

    def stop(self):
        return self.angle_parcouru >= self.angle #True si l'angle cible est atteint
    
    
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
    def __init__(self, s1, s2, adaptateur, condition):
        self.s1 = s1  #strategie si obstacle proche
        self.s2 = s2  #strategie sinon
        self.adaptateur = adaptateur
        self.condition = condition #distance seuil pour detecter un obstacle
        self.current = None #strategie actuellement active

    def start(self):
        self.current = None #aucune strategie active au debut

    def step(self):
        if self.condition(self.adaptateur): #si obstacle proche alors s1
            new = self.s1
        else:
            new = self.s2
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


class LimiterTemps:
    """Execute une strategie pendant une duree fixe en secondes"""
    def __init__(self, strat, duree_secondes):
        self.strat = strat
        self.duree_secondes = duree_secondes
        self.temps_depart = None

    def start(self):
        #Cette enveloppe sert a donner une duree reelle a la phase 2
        self.temps_depart = time.monotonic()
        self.strat.start()

    def step(self):
        if self.stop():
            return

        if self.strat.stop():
            self.strat.start()

        self.strat.step()

    def stop(self):
        if self.temps_depart is None:
            return False
        return (time.monotonic() - self.temps_depart) >= self.duree_secondes


class SuivreSouris:
    """Strategie reactive qui poursuit une souris mobile"""
    def __init__(self, adaptateur, simulation, vitesse_lineaire=2.8, gain_rotation=0.08):
        self.adaptateur = adaptateur
        self.simulation = simulation
        self.vitesse_lineaire = vitesse_lineaire
        self.gain_rotation = gain_rotation

    def start(self):
        pass

    def step(self):
        souris = self.simulation.souris
        robot = self.adaptateur.robot

        if souris is None:
            self.adaptateur.arreter()
            return

        cible_x = souris["x"] + souris["taille"] / 2
        cible_y = souris["y"] + souris["taille"] / 2

        dx = cible_x - robot.x
        dy = cible_y - robot.y
        distance = math.hypot(dx, dy)

        #Quand le robot est assez proche on considere la souris attrapee
        if distance < max(robot.longueur, robot.largeur):
            self.simulation.attraper_souris()
            self.adaptateur.arreter()
            return

        angle_cible = math.atan2(dy, dx)
        erreur_angle = math.atan2(
            math.sin(angle_cible - robot.angle),
            math.cos(angle_cible - robot.angle)
        )

        #On ralentit dans les virages serres pour garder une trajectoire stable
        vitesse = self.vitesse_lineaire
        if abs(erreur_angle) > 0.6:
            vitesse = self.vitesse_lineaire * 0.55

        self.adaptateur.set_vitesse(vitesse, erreur_angle * self.gain_rotation)

    def stop(self):
        return False
