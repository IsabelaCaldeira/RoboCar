import unittest
import time

from Source.Controler import AdaptateurSimule
from Source.IRL import Robot2IN013_MOCK


class TestAdaptateurSimule(unittest.TestCase):

    def setUp(self): # setUp sert a preparer ce dont les tests ont besoin avant chaque test
        self.robot_mock = Robot2IN013_MOCK()
        self.robot = AdaptateurSimule(self.robot_mock, coordonnees=(100, 200), angle=0)

    def test_initialisation(self):
        """Verifie que l'adaptateur simule est correctement initialise"""
        self.assertEqual(self.robot.x, 100)
        self.assertEqual(self.robot.y, 200)
        self.assertEqual(self.robot.vG, 0)
        self.assertEqual(self.robot.vR, 0)

    def test_initialise_reset_encodeurs(self):
        """Verifie que initialise() remet les encodeurs a zero"""
        self.robot.pos_g = 100
        self.robot.pos_d = 200

        self.robot.initialise()

        self.assertEqual(self.robot.pos_g, 0)
        self.assertEqual(self.robot.pos_d, 0)
        self.assertIsNotNone(self.robot._last_update)

    def test_get_position(self):
        """Verifie que get_position() retourne les bonnes coordonnees"""
        position = self.robot.get_position()
        self.assertEqual(position, (100, 200))

    def test_get_angle(self):
        """Verifie que get_angle() retourne le bon angle"""
        self.assertEqual(self.robot.get_angle(), 0)

    def test_get_wheel_speeds(self):
        """Verifie que get_wheel_speeds() retourne les bonnes vitesses"""
        self.robot.vG = 10
        self.robot.vR = 20

        vitesses = self.robot.get_wheel_speeds()

        self.assertEqual(vitesses, (10, 20))

    def test_avancer(self):
        """Verifie que avancer() met les deux roues a la meme vitesse"""
        self.robot.avancer(40)
        self.assertEqual(self.robot.vG, 40)
        self.assertEqual(self.robot.vR, 40)

    def test_reculer(self):
        """Verifie que reculer() met les vitesses negatives"""
        self.robot.reculer(30)
        self.assertEqual(self.robot.vG, -30)
        self.assertEqual(self.robot.vR, -30)

    def test_tourner_gauche(self):
        """Verifie que tourner_gauche() active seulement la roue gauche"""
        self.robot.tourner_gauche(50)
        self.assertEqual(self.robot.vG, 50)
        self.assertEqual(self.robot.vR, 0)

    def test_tourner_droite(self):
        """Verifie que tourner_droite() active seulement la roue droite"""
        self.robot.tourner_droite(50)
        self.assertEqual(self.robot.vG, 0)
        self.assertEqual(self.robot.vR, 50)

    def test_tourner_sur_place(self):
        """Verifie que tourner_sur_place() fait tourner les roues en sens oppose"""
        self.robot.tourner_sur_place(50)
        self.assertEqual(self.robot.vG, 50)
        self.assertEqual(self.robot.vR, -50)

    def test_arreter(self):
        """Verifie que arreter() remet les vitesses a zero"""
        self.robot.vG = 100
        self.robot.vR = 100

        self.robot.arreter()

        self.assertEqual(self.robot.vG, 0)
        self.assertEqual(self.robot.vR, 0)

    def test_get_motor_position(self):
        """Verifie que get_motor_position() fait evoluer les encodeurs"""
        self.robot.vG = 10
        self.robot.vR = 10

        # on simule un delta temps d'une seconde
        self.robot._last_update = time.time() - 1

        pos_g, pos_d = self.robot.get_motor_position()

        self.assertAlmostEqual(pos_g, 10, delta=1.0)
        self.assertAlmostEqual(pos_d, 10, delta=1.0)

    def test_get_distance_parcourue(self):
        """Verifie que la distance parcourue est positive si les roues avancent"""
        self.robot.vG = 10
        self.robot.vR = 10

        # on simule un delta temps d'une seconde
        self.robot._last_update = time.time() - 1
        distance = self.robot.get_distance_parcourue()

        self.assertGreater(distance, 0)

    def test_get_angle_parcouru(self):
        """Verifie que l'angle parcouru est nul si les deux roues ont la meme vitesse"""
        self.robot.vG = 10
        self.robot.vR = 10

        # on simule un delta temps d'une seconde
        self.robot._last_update = time.time() - 1
        angle = self.robot.get_angle_parcouru()

        self.assertAlmostEqual(angle, 0, delta=0.1)

    def test_get_angle_parcouru_non_nul(self):
        """Verifie que l'angle parcouru change si les roues n'ont pas la meme vitesse"""
        self.robot.vG = 10
        self.robot.vR = 20

        # on simule un delta temps d'une seconde
        self.robot._last_update = time.time() - 1
        angle = self.robot.get_angle_parcouru()

        self.assertNotEqual(angle, 0)


if __name__ == "__main__":
    unittest.main()