import math
from .adaptateur import Adaptateur


class AdaptateurReel(Adaptateur):
    """Adaptateur utilise pour piloter le vrai robot
    """
    WHEEL_BASE_WIDTH = 117
    WHEEL_DIAMETER = 66.5
    WHEEL_CIRCUMFERENCE = WHEEL_DIAMETER * math.pi
    def __init__(self, robot):
        self.robot = robot #instance du vrai robot Robot2IN013
        pos_g, pos_d = self.robot.get_motor_position()  #On lit les positions initiales des encodeurs
        #Anciennes valeurs pour la distance
        self.old_pos_g_dist = pos_g
        self.old_pos_d_dist = pos_d
        #Anciennes valeurs pour l'angle
        self.old_pos_g_angle = pos_g
        self.old_pos_d_angle = pos_d

    def set_vitesse(self, v, w):
        """Convertit la vitesse lineaire v et la vitesse angulaire w
        en vitesse de roue gauche et de roue droite"""
        vG = v - (w * self.WHEEL_BASE_WIDTH / 2)
        vR = v + (w * self.WHEEL_BASE_WIDTH / 2)

        self.robot.set_motor_dps(self.robot.MOTOR_LEFT, vG)
        self.robot.set_motor_dps(self.robot.MOTOR_RIGHT, vR)

    def get_distance(self):
        """Lit directement la distance sur le capteur du robot reel
        """
        return self.robot.get_distance()

    def get_distance_parcourue(self):
        """Calcule la distance parcourue depuis le dernier appel
        a partir de la variation des encodeurs
        """
        pos_g, pos_d = self.robot.get_motor_position()

        delta_g = pos_g - self.old_pos_g_dist
        delta_d = pos_d - self.old_pos_d_dist

        dist_g = (delta_g / 360) * self.WHEEL_CIRCUMFERENCE
        dist_d = (delta_d / 360) * self.WHEEL_CIRCUMFERENCE

        # Mise a jour des anciennes valeurs
        self.old_pos_g_dist = pos_g
        self.old_pos_d_dist = pos_d

        return (dist_g + dist_d) / 2

    def get_angle_parcouru(self):
        """Calcule l'angle parcouru depuis le dernier appel
        a partir de la difference de deplacement entre les deux roues
        """
        pos_g, pos_d = self.robot.get_motor_position()

        delta_g = pos_g - self.old_pos_g_angle
        delta_d = pos_d - self.old_pos_d_angle

        dist_g = (delta_g / 360) * self.WHEEL_CIRCUMFERENCE
        dist_d = (delta_d / 360) * self.WHEEL_CIRCUMFERENCE

        # Mise a jour des anciennes valeurs
        self.old_pos_g_angle = pos_g
        self.old_pos_d_angle = pos_d

        return (dist_d - dist_g) / self.WHEEL_BASE_WIDTH

    def arreter(self):
        """Arrete completement le robot reel"""
        self.robot.set_motor_dps(self.robot.MOTOR_LEFT, 0)
        self.robot.set_motor_dps(self.robot.MOTOR_RIGHT, 0)
