import unittest
import math

from Source.Model import Simulation, RoboCar,Obstacle
from Source.Controler import AdaptateurSimule


class TestAdaptateurSimule(unittest.TestCase):
    def setUp(self):
        """Prepare un monde simple avant chaque test"""
        self.sim = Simulation(800, 600, obstacles=[])
        self.robocar = RoboCar("Flash", (100, 200), 0, simulation=self.sim)
        self.adaptateur = AdaptateurSimule(self.robocar)

    def test_set_vitesse(self):
        """Verifie que set_vitesse(v, w) met bien a jour les vitesses des roues du robot"""
        self.adaptateur.set_vitesse(10, 0)
        self.assertEqual(self.robocar.vG, 10)
        self.assertEqual(self.robocar.vR, 10)

    def test_set_vitesse_rotation(self):
        """Verifie que set_vitesse(v, w) donne des vitesses differentes si le robot tourne"""
        self.adaptateur.set_vitesse(0, 2)
        self.assertNotEqual(self.robocar.vG, self.robocar.vR)

    def test_avancer(self):
        """Verifie que avancer() met les deux roues a la meme vitesse"""
        self.adaptateur.avancer(4)
        self.assertEqual(self.robocar.vG, 4)
        self.assertEqual(self.robocar.vR, 4)

    def test_reculer(self):
        """Verifie que reculer() met les deux roues a une vitesse negative"""
        self.adaptateur.reculer(3)
        self.assertEqual(self.robocar.vG, -3)
        self.assertEqual(self.robocar.vR, -3)

    def test_tourner_sur_place(self):
        """Verifie que tourner_sur_place() met les roues en sens oppose"""
        self.adaptateur.tourner_sur_place(0.5)
        self.assertAlmostEqual(self.robocar.vG, -self.robocar.vR)

    def test_arreter(self):
        """Verifie que arreter() remet les vitesses des roues a zero"""
        self.robocar.vG = 10
        self.robocar.vR = 20
        self.adaptateur.arreter()
        self.assertEqual(self.robocar.vG, 0)
        self.assertEqual(self.robocar.vR, 0)

    def test_get_distance_sans_obstacle(self):
        """Verifie que get_distance() retourne une distance positive quand il n'y a pas d'obstacle juste devant"""
        distance = self.adaptateur.get_distance()
        self.assertGreater(distance, 0)

    def test_get_distance_avec_obstacle_devant(self):
        """Verifie que get_distance() detecte un obstacle place devant le robot"""
        # obstacle devant le robot
        self.sim.obstacles = []
        self.sim.obstacles.append(Obstacle("rectangle", (150, 180), (40, 40)))
        distance = self.adaptateur.get_distance()
        self.assertLess(distance, 120)

    def test_get_distance_parcourue(self):
        """Verifie que get_distance_parcourue() retourne une distance positive si la position du robot a change"""
        # ancienne position memorisee au setUp : (100, 200)
        self.robocar.appliquer(110, 200, self.robocar.angle)
        distance = self.adaptateur.get_distance_parcourue()
        self.assertAlmostEqual(distance, 10)

    def test_get_distance_parcourue_nulle(self):
        """Verifie que la distance parcourue vaut 0 si le robot n'a pas bouge"""
        distance = self.adaptateur.get_distance_parcourue()
        self.assertEqual(distance, 0)

    def test_get_angle_parcouru(self):
        """Verifie que get_angle_parcouru() retourne un angle positif si l'orientation du robot a change"""
        ancien_angle = self.robocar.angle
        nouvel_angle = ancien_angle + math.pi / 4  # 45 degres
        self.robocar.appliquer(self.robocar.x, self.robocar.y, nouvel_angle)
        angle = self.adaptateur.get_angle_parcouru()
        self.assertAlmostEqual(angle, math.pi / 4)

    def test_get_angle_parcouru_nul(self):
        """Verifie que get_angle_parcouru() vaut 0 si l'angle n'a pas change"""
        angle = self.adaptateur.get_angle_parcouru()

        self.assertEqual(angle, 0)


if __name__ == "__main__":
    unittest.main()