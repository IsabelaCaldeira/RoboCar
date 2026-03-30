import unittest
import time

from Source.Model import RoboCar


class TestRoboCar(unittest.TestCase):

    def setUp(self):
        self.robot = RoboCar("Flash", (100, 200), 0)

    def test_initialisation(self):
        """Verifie que le robot est correctement initialise"""
        self.assertEqual(self.robot.x, 100)
        self.assertEqual(self.robot.y, 200)
        self.assertEqual(self.robot.vG, 0)
        self.assertEqual(self.robot.vR, 0)

    def test_calculer_vitesse(self):
        """Verifie le calcul des vitesses lineaire et angulaire"""
        self.robot.set_vitesse_gauche(50)
        self.robot.set_vitesse_droite(50)
        v, w = self.robot.calculer_vitesse()
        self.assertEqual(v, 50)
        self.assertEqual(w, 0)

    def test_update(self):
        """Verifie que le robot se deplace correctement"""
        self.robot.set_vitesse_gauche(10)
        self.robot.set_vitesse_droite(10)
        self.robot._last_update = time.time() - 1

        ancien_x = self.robot.x
        self.robot.update()

        self.assertAlmostEqual(self.robot.x, ancien_x + 10, delta=1.0)

if __name__ == "__main__":
    unittest.main()