import unittest

from Source import Simulation, Obstacle


class TestSimulation(unittest.TestCase):
    def setUp(self):
        """Cree un monde simple avant chaque test"""
        self.sim = Simulation(800, 600)

    def test_initialisation(self):
        """Verifie que les dimensions et les obstacles sont bien initialises"""
        self.assertEqual(self.sim.largeur, 800)
        self.assertEqual(self.sim.hauteur, 600)
        self.assertEqual(len(self.sim.obstacles), 3)

    def test_collision_retourne_bool(self):
        """Verifie que collision() retourne bien un booleen"""
        resultat = self.sim.collision(400, 300, 50, 40)
        self.assertIsInstance(resultat, bool)

    def test_pas_de_collision_au_centre(self):
        """Verifie qu'un robot place dans une zone libre ne collisionne pas forcement"""
        sim = Simulation(800, 600, obstacles=[])
        resultat = sim.collision(400, 300, 50, 40)
        self.assertFalse(resultat)

    def test_collision_avec_mur_gauche(self):
        """Verifie qu'il y a collision si le robot sort par la gauche"""
        resultat = self.sim.collision(10, 300, 50, 40)
        self.assertTrue(resultat)

    def test_collision_avec_mur_droit(self):
        """Verifie qu'il y a collision si le robot sort par la droite"""
        resultat = self.sim.collision(790, 300, 50, 40)
        self.assertTrue(resultat)

    def test_collision_avec_mur_haut(self):
        """Verifie qu'il y a collision si le robot sort par le haut"""
        resultat = self.sim.collision(400, 10, 50, 40)
        self.assertTrue(resultat)

    def test_collision_avec_mur_bas(self):
        """Verifie qu'il y a collision si le robot sort par le bas"""
        resultat = self.sim.collision(400, 590, 50, 40)
        self.assertTrue(resultat)

    def test_collision_avec_obstacle(self):
        """Verifie qu'il y a collision si le robot recouvre un obstacle"""
        sim = Simulation(
            800,
            600,
            obstacles=[Obstacle("rectangle", (100, 100), (80, 100))]
        )
        #centre du robot place sur l'obstacle
        resultat = sim.collision(140, 150, 50, 40)
        self.assertTrue(resultat)

    def test_pas_de_collision_avec_obstacle_loin(self):
        """Verifie qu'il n'y a pas collision si le robot est loin de l'obstacle"""
        sim = Simulation(
            800,
            600,
            obstacles=[Obstacle("rectangle", (100, 100), (80, 100))]
        )
        resultat = sim.collision(400, 300, 50, 40)
        self.assertFalse(resultat)

    def test_liste_obstacles_personnalisee(self):
        """Verifie qu'on peut fournir une liste d'obstacles personnalisee"""
        obstacles = [
            Obstacle("rectangle", (50, 50), (20, 20)),
            Obstacle("rectangle", (200, 200), (30, 30))
        ]
        sim = Simulation(800, 600, obstacles=obstacles)
        self.assertEqual(len(sim.obstacles), 2)


if __name__ == "__main__":
    unittest.main()