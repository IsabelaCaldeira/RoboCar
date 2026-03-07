import unittest
import math

from robocar import RoboCar
from simulation import Simulation
from strategies import Deplacement


class TestRoboCar(unittest.TestCase):

    def setUp(self):
        self.robot = RoboCar("Flash", (100, 200), 0)

    def test_initialisation(self):
        self.assertEqual(self.robot.x, 100)
        self.assertEqual(self.robot.y, 200)
        self.assertEqual(self.robot.vG, 0)
        self.assertEqual(self.robot.vR, 0)

    def test_calculer_vitesse(self):
        self.robot.set_vitesse_gauche(50)
        self.robot.set_vitesse_droite(50)
        v, w = self.robot.calculer_vitesse()
        self.assertEqual(v, 50)
        self.assertEqual(w, 0)

    def test_update(self):
        self.robot.set_vitesse_gauche(10)
        self.robot.set_vitesse_droite(10)
        self.robot.update(1)
        self.assertAlmostEqual(self.robot.x, 110)



if __name__ == "__main__":
    unittest.main()