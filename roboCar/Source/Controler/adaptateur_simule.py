import math
from .adaptateur import Adaptateur


class AdaptateurSimule(Adaptateur):
    """
    Adaptateur pour utiliser un robot mock dans la simulation
    Il garde aussi les infos de position pour pygame
    """

    WHEEL_BASE_WIDTH = 117  # distance entre roues
    WHEEL_DIAMETER = 66.5
    WHEEL_CIRCUMFERENCE = WHEEL_DIAMETER * math.pi

    def __init__(self, robot, nom="Flash", coordonnees=(400, 300), angle=0):
        self.robot = robot  # robot mock
        self.nom = nom
        # position du robot dans la simulation
        self.x, self.y = coordonnees
        self.angle = math.radians(angle)
        # vitesses des roues
        self.vG = 0
        self.vR = 0
        self.largeur = 40
        self.longueur = 50

    def initialise(self):
        """reset des encodeurs moteurs"""
        pos_g, pos_d = self.robot.get_motor_position()
        self.robot.offset_motor_encoder(self.robot.MOTOR_LEFT, pos_g)
        self.robot.offset_motor_encoder(self.robot.MOTOR_RIGHT, pos_d)

    def get_position(self):
        return self.x, self.y

    def get_angle(self):
        return self.angle

    def get_wheel_speeds(self):
        return self.vG, self.vR

    def set_vitesse_gauche(self, vitesse):
        """met a jour vitesse interne et envoie au robot"""
        self.vG = vitesse
        self.robot.set_motor_dps(self.robot.MOTOR_LEFT, vitesse)

    def set_vitesse_droite(self, vitesse):
        self.vR = vitesse
        self.robot.set_motor_dps(self.robot.MOTOR_RIGHT, vitesse)

    def avancer(self, vitesse):
        """avance en ligne droite"""
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

    def get_motor_position(self):
        """lit les encodeurs du robot mock"""
        return self.robot.get_motor_position()
    def get_distance_parcourue(self):
        """
        calcule la distance parcourue a partir des encodeurs
        """
        ang_g, ang_d = self.get_motor_position()

        dist_g = (ang_g / 360) * self.robot.WHEEL_CIRCUMFERENCE
        dist_d = (ang_d / 360) * self.robot.WHEEL_CIRCUMFERENCE

        return (dist_g + dist_d) / 2

    def get_angle_parcouru(self):
        """
        calcule la rotation du robot
        """
        ang_g, ang_d = self.get_motor_position()

        dist_g = (ang_g / 360) * self.robot.WHEEL_CIRCUMFERENCE
        dist_d = (ang_d / 360) * self.robot.WHEEL_CIRCUMFERENCE

        angle = (dist_d - dist_g) / self.robot.WHEEL_BASE_WIDTH
        return angle

    def stop(self):
        self.robot.stop()