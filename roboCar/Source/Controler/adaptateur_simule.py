import math
import time
from .adaptateur import Adaptateur


class AdaptateurSimule(Adaptateur):
    """
    Adaptateur entre les strategies et le Robot2IN013_MOCK
    cet adaptateur garde une position simulee pour que la simulation pygame fonctionne
    """

    def __init__(self, robot, nom="Flash", coordonnees=(400, 300), angle=0):
        self.robot = robot
        self.nom = nom
        self.x, self.y = coordonnees
        self.angle = math.radians(angle)

        self.vG = 0
        self.vR = 0

        self.largeur = 40
        self.longueur = 50

        self._last_update = None

    def initialise(self):
        pos_g, pos_d = self.robot.get_motor_position()
        self.robot.offset_motor_encoder(self.robot.MOTOR_LEFT, pos_g)
        self.robot.offset_motor_encoder(self.robot.MOTOR_RIGHT, pos_d)
        self._last_update = None

    def get_position(self):
        return self.x, self.y

    def get_angle(self):
        return self.angle

    def get_wheel_speeds(self):
        return self.vG, self.vR

    def set_vitesse_gauche(self, vitesse):
        self.vG = vitesse
        self.robot.set_motor_dps(self.robot.MOTOR_LEFT, vitesse)

    def set_vitesse_droite(self, vitesse):
        self.vR = vitesse
        self.robot.set_motor_dps(self.robot.MOTOR_RIGHT, vitesse)

    def calculer_vitesse(self):
        """
        On garde la meme logique que RoboCar :
        v = vitesse linéaire moyenne
        w = vitesse angulaire
        """
        v = (self.vR + self.vG) / 2
        w = (self.vR - self.vG) / self.robot.WHEEL_BASE_WIDTH
        return v, w

    def avancer(self, vitesse):
        self.set_vitesse_gauche(vitesse)
        self.set_vitesse_droite(vitesse)

    def reculer(self, vitesse):
        self.set_vitesse_gauche(-vitesse)
        self.set_vitesse_droite(-vitesse)

    def arreter(self):
        self.set_vitesse_gauche(0)
        self.set_vitesse_droite(0)

    def tourner_sur_place(self, vitesse):
        self.set_vitesse_gauche(vitesse)
        self.set_vitesse_droite(-vitesse)

    def tourner_gauche(self, vitesse):
        self.set_vitesse_gauche(vitesse)
        self.set_vitesse_droite(0)

    def tourner_droite(self, vitesse):
        self.set_vitesse_gauche(0)
        self.set_vitesse_droite(vitesse)

    def update(self):
        now = time.time()
        if self._last_update is None:
            dt = 0.0
        else:
            dt = now - self._last_update
        self._last_update = now

        v, w = self.calculer_vitesse()
        self.x += v * math.cos(self.angle) * dt
        self.y += v * math.sin(self.angle) * dt
        self.angle += w * dt

    def stop(self):
        self.robot.stop()