import math
from .adaptateur import Adaptateur


class AdaptateurSimule(Adaptateur):
    """Adaptateur pour le robot simule
    ll traduit les vitesses lineaire et angulaire en vitesses des roues"""

    def __init__(self, robot):
        self.robot = robot
        # anciennes valeurs pour calcul distance
        x, y = robot.get_position()
        self.old_x = x
        self.old_y = y

        self.old_angle = robot.get_angle()

    #Problem avec les noms des foncctions 
    def set_vitesse(self, v, w): 
        """Convertit v et w en vitesses des roues
        """
        vG = v - (w * self.robot.WHEEL_BASE / 2)
        vR = v + (w * self.robot.WHEEL_BASE / 2)

        self.robot.vG = vG
        self.robot.vR = vR

    def get_distance(self):
        """Distance devant le robot"""
        return self.robot.get_distance()

    #On calcule pas la vrai distance parcourue, plutot le parcours ici (probleme avec la façon qu'on calcule et le temps)
    def get_distance_parcourue(self):
        """Distance euclidienne parcourue depuis dernier appel.
        """
        x, y = self.robot.get_position()

        dx = x - self.old_x
        dy = y - self.old_y

        dist = math.sqrt(dx**2 + dy**2)

        self.old_x = x
        self.old_y = y

        return dist

    def get_angle_parcouru(self):
        """Angle parcouru depuis dernier appel.
        """
        angle = self.robot.get_angle()
        d = abs(angle - self.old_angle)

        self.old_angle = angle

        return d

    def avancer(self, vitesse):
        """Avancer tout droit"""
        self.set_vitesse(vitesse, 0)

    def reculer(self, vitesse):
        """Reculer"""
        self.set_vitesse(-vitesse, 0)

    def arreter(self):
        """Stop"""
        self.robot.vG = 0
        self.robot.vR = 0

    def tourner_sur_place(self, vitesse):
        """Rotation sur place"""
        self.set_vitesse(0, vitesse)