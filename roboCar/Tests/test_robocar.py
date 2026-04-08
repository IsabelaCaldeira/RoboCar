import unittest
import math

from Source import Simulation, RoboCar, Obstacle


class TestRoboCar(unittest.TestCase):
    def setUp(self):
        """Cree un robot dans un monde simple avant chaque test"""
        self.sim = Simulation(800, 600)
        self.sim.obstacles = []  # on vide les obstacles pour maitriser les tests
        self.robot = RoboCar("Flash", (100, 200), 0, simulation=self.sim)

    def test_initialisation(self):
        """Verifie que le robot est correctement initialise"""
        self.assertEqual(self.robot.x, 100)
        self.assertEqual(self.robot.y, 200)
        self.assertEqual(self.robot.vG, 0)
        self.assertEqual(self.robot.vR, 0)
        self.assertEqual(self.robot.longueur, 50)
        self.assertEqual(self.robot.largeur, 40)
        self.assertFalse(self.robot.crayon_abaisse)
        self.assertEqual(self.robot.get_trace(), [(100, 200)])

    def test_get_position(self):
        """Verifie que get_position() retourne les bonnes coordonnees"""
        self.assertEqual(self.robot.get_position(), (100, 200))

    def test_get_angle(self):
        """Verifie que get_angle() retourne bien l'angle en radians"""
        self.assertEqual(self.robot.get_angle(), 0)

    def test_set_vitesse_ligne_droite(self):
        """Verifie que si les deux roues ont la meme vitesse alors le robot avance en ligne droite"""
        self.robot.vG = 50
        self.robot.vR = 50
        v, w = self.robot.set_vitesse()
        self.assertEqual(v, 50)
        self.assertEqual(w, 0)

    def test_set_vitesse_rotation(self):
        """Verifie que si les roues ont des vitesses differentes alors la vitesse angulaire n'est pas nulle"""
        self.robot.vG = 20
        self.robot.vR = 40
        v, w = self.robot.set_vitesse()
        self.assertEqual(v, 30)
        self.assertNotEqual(w, 0)

    def test_update(self):
        """Verifie que update(v, w) calcule le prochain etat sans modifier directement le robot"""
        next_x, next_y, next_angle = self.robot.update(10, 0)

        #le robot ne doit pas encore avoir bouge
        self.assertEqual(self.robot.x, 100)
        self.assertEqual(self.robot.y, 200)
        self.assertEqual(self.robot.angle, 0)

        #mais la position calculee doit etre correcte
        self.assertAlmostEqual(next_x, 100 + 10 * self.robot.PAS)
        self.assertAlmostEqual(next_y, 200)
        self.assertAlmostEqual(next_angle, 0)

    def test_appliquer(self):
        """Verifie que appliquer() modifie bien la position et l'angle"""
        self.robot.appliquer(120, 210, math.pi / 2)
        self.assertEqual(self.robot.x, 120)
        self.assertEqual(self.robot.y, 210)
        self.assertEqual(self.robot.angle, math.pi / 2)

    def test_step_sans_collision(self):
        """Verifie que step() applique le mouvement si aucune collision n'est detectee"""
        self.robot.abaisser_crayon()
        self.robot.vG = 10
        self.robot.vR = 10
        ancien_x = self.robot.x
        ok = self.robot.step()
        self.assertTrue(ok)
        self.assertGreater(self.robot.x, ancien_x)
        self.assertEqual(len(self.robot.get_trace()), 2)

    def test_step_avec_collision_mur(self):
        """Verifie que step() retourne False si le robot va heurter un mur"""
        #on place le robot tres pres du bord droit
        self.robot.x = 780
        self.robot.y = 200
        self.robot.vG = 10
        self.robot.vR = 10
        ok = self.robot.step()
        self.assertFalse(ok)

    def test_get_distance_sans_obstacle(self):
        """Verifie que get_distance() retourne une distance positive quand il n'y a pas d'obstacle juste devant"""
        distance = self.robot.get_distance()
        self.assertGreater(distance, 0)

    def test_get_distance_avec_obstacle(self):
        """Verifie que get_distance() detecte un obstacle place devant le robot"""
        self.sim.obstacles.append(Obstacle("rectangle", (150, 180), (40, 40)))
        distance = self.robot.get_distance()
        self.assertLess(distance, 120)

    def test_pas_de_trace_quand_crayon_leve(self):
        """Verifie que le robot ne trace rien si le crayon est leve"""
        self.robot.lever_crayon()
        self.robot.appliquer(120, 200, 0)
        self.assertEqual(self.robot.get_trace(), [(100, 200)])

    def test_abaisser_crayon_reprend_trace(self):
        """Verifie que la trace reprend a la position courante quand on rabaisse le crayon"""
        self.robot.lever_crayon()
        self.robot.appliquer(120, 200, 0)
        self.robot.abaisser_crayon()
        self.robot.appliquer(130, 200, 0)
        self.assertEqual(self.robot.get_trace(), [(100, 200), (120, 200), (130, 200)])


if __name__ == "__main__":
    unittest.main()
