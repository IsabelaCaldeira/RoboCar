import unittest
import time

from Source.Model import RoboCar, Simulation


class TestSimulation(unittest.TestCase):

    def setUp(self):
        self.robot = RoboCar("Flash", (400, 300), 0)
        self.sim = Simulation(800, 600, self.robot, mode="robocar")

    def test_initialisation(self):
        """Verifie les dimensions et la creation du robot"""
        self.assertEqual(self.sim.largeur, 800)
        self.assertEqual(self.sim.hauteur, 600)
        self.assertIsNotNone(self.sim.robot)
        self.assertEqual(len(self.sim.obstacles), 3)
        self.assertEqual(self.sim.mode, "robocar")

    def test_distance_obstacle_positive(self):
        """La distance a un obstacle doit etre positive"""
        dist = self.sim.distance_obstacle()
        self.assertGreaterEqual(dist, 0)

    def test_distance_mur_positive(self):
        """La distance au mur doit etre positive"""
        dist = self.sim.distance_mur()
        self.assertGreaterEqual(dist, 0)

    def test_distance_cote_gauche_positive(self):
        """La distance a gauche doit etre positive"""
        dist = self.sim.distance_cote_gauche()
        self.assertGreaterEqual(dist, 0)

    def test_distance_cote_droite_positive(self):
        """La distance a droite doit etre positive"""
        dist = self.sim.distance_cote_droite()
        self.assertGreaterEqual(dist, 0)

    def test_obtenir_rectangle(self):
        """Le rectangle du robot doit contenir 4 valeurs"""
        rect = self.sim.obtenir_rectangle()
        self.assertEqual(len(rect), 4)

    def test_collision_type(self):
        """collision() doit retourner un booleen"""
        obs = self.sim.obstacles[0]
        resultat = self.sim.collision(obs)
        self.assertIsInstance(resultat, bool)

    def test_appliquer_murs(self):
        """Le robot ne doit pas sortir des limites apres appliquer_murs()"""
        self.sim.robot.x = -100
        self.sim.robot.y = -100

        self.sim.appliquer_murs()

        self.assertGreaterEqual(self.sim.robot.x, self.sim.robot.longueur / 2)
        self.assertGreaterEqual(self.sim.robot.y, self.sim.robot.largeur / 2)

    def test_resoudre_collisions_retourne_bool(self):
        """resoudre_collisions() doit retourner un booleen"""
        old_state = self.sim.robot.get_position()
        resultat = self.sim.resoudre_collisions(old_state)
        self.assertIsInstance(resultat, bool)

    def test_update_retourne_bool(self):
        """update() doit retourner un booleen"""
        self.sim._last_update = time.time()
        resultat = self.sim.update()
        self.assertIsInstance(resultat, bool)

    def test_update_fait_bouger_le_robot(self):
        """update() doit faire avancer le robot si une vitesse est definie"""
        self.sim.robot.avancer(20)

        self.sim._last_update = time.time() - 1
        ancien_x = self.sim.robot.x
        ancien_y = self.sim.robot.y

        self.sim.update()

        self.assertGreater(self.sim.robot.x, ancien_x)
        self.assertAlmostEqual(self.sim.robot.y, ancien_y, delta=1.0)


if __name__ == "__main__":
    unittest.main()