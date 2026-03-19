import unittest
import math
from roboCar import (
    RoboCar,
    Simulation,
    AvancerXMetres,
    Reculer,
    FreinageProgressif,
    EviterObstacles,
    GestionStrategies,
)


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
        self.assertAlmostEqual(self.robot.y, 200)

    def test_avancer(self):
        self.robot.avancer(40)
        self.assertEqual(self.robot.vG, 40)
        self.assertEqual(self.robot.vR, 40)

    def test_reculer(self):
        self.robot.reculer(30)
        self.assertEqual(self.robot.vG, -30)
        self.assertEqual(self.robot.vR, -30)

    def test_tourner_gauche(self):
        self.robot.tourner_gauche(50)
        self.assertEqual(self.robot.vG, 50)
        self.assertEqual(self.robot.vR, 0)

    def test_tourner_droite(self):
        self.robot.tourner_droite(50)
        self.assertEqual(self.robot.vG, 0)
        self.assertEqual(self.robot.vR, 50)

    def test_arreter(self):
        self.robot.vG = 100
        self.robot.vR = 100

        self.robot.arreter()

        self.assertEqual(self.robot.vG, 0)
        self.assertEqual(self.robot.vR, 0)


class TestSimulation(unittest.TestCase):

    def setUp(self):
        self.sim = Simulation(800, 600)

    def test_initialisation(self):
        self.assertEqual(self.sim.largeur, 800)
        self.assertEqual(self.sim.hauteur, 600)
        self.assertIsNotNone(self.sim.robot)
        self.assertEqual(len(self.sim.obstacles), 3)

    def test_distance_obstacle_positive(self):
        dist = self.sim.distance_obstacle()
        self.assertGreaterEqual(dist, 0)

    def test_distance_mur_positive(self):
        dist = self.sim.distance_mur()
        self.assertGreaterEqual(dist, 0)

    def test_distance_cote_gauche_positive(self):
        dist = self.sim.distance_cote_gauche()
        self.assertGreaterEqual(dist, 0)

    def test_distance_cote_droite_positive(self):
        dist = self.sim.distance_cote_droite()
        self.assertGreaterEqual(dist, 0)

    def test_obtenir_rectangle(self):
        rect = self.sim.obtenir_rectangle()
        self.assertEqual(len(rect), 4)

    def test_collision_type(self):
        obs = self.sim.obstacles[0]
        resultat = self.sim.collision(obs)
        self.assertIsInstance(resultat, bool)

    def test_appliquer_murs(self):
        self.sim.robot.x = -100
        self.sim.robot.y = -100

        self.sim.appliquer_murs()

        self.assertGreaterEqual(self.sim.robot.x, self.sim.robot.longueur / 2)
        self.assertGreaterEqual(self.sim.robot.y, self.sim.robot.largeur / 2)

    def test_update_retourne_bool(self):
        resultat = self.sim.update(0.1)
        self.assertIsInstance(resultat, bool)


class TestStrategies(unittest.TestCase):

    def setUp(self):
        self.sim = Simulation(800, 600)

        # on enlève les obstacles pour certains tests simples
        self.sim.obstacles = []

    def test_avancer_x_metres_pas_termine_au_premier_appel(self):
        strat = AvancerXMetres(self.sim, distance=1, vitesse=80)

        fini = strat.update(0.1)

        self.assertFalse(fini)

    def test_avancer_x_metres_termine_si_distance_deja_parcourue(self):
        strat = AvancerXMetres(self.sim, distance=1, vitesse=80)

        # premier appel : mémorise le départ
        strat.update(0.1)

        # on simule un déplacement déjà effectué
        self.sim.robot.x += 120

        fini = strat.update(0.1)

        self.assertTrue(fini)

    def test_freinage_progressif(self):
        self.sim.robot.vG = 50
        self.sim.robot.vR = 50

        strat = FreinageProgressif(self.sim)
        fini = strat.update(1)

        self.assertTrue(fini)
        self.assertEqual(self.sim.robot.vG, 0)
        self.assertEqual(self.sim.robot.vR, 0)

    def test_reculer_declenche(self):
        strat = Reculer(self.sim, vitesse=50, distance=0.4)

        strat.declencher()

        self.assertTrue(strat.actif)

    def test_reculer_update(self):
        strat = Reculer(self.sim, vitesse=50, distance=0.4)

        strat.declencher()
        fini = strat.update(0.1)

        self.assertFalse(fini)
        self.assertEqual(self.sim.robot.vG, -50)
        self.assertEqual(self.sim.robot.vR, -50)

    def test_eviter_obstacles_avance_si_rien_devant(self):
        strat = EviterObstacles(self.sim, vitesse_avance=80, vitesse_tourne=60, seuil=50)

        strat.update(0.1)

        self.assertEqual(self.sim.robot.vG, 80)
        self.assertEqual(self.sim.robot.vR, 80)

    def test_distance_securite(self):
        strat = EviterObstacles(self.sim, vitesse_avance=80, vitesse_tourne=60, seuil=50)

        d_sec = strat.distance_securite(0.1)

        self.assertGreaterEqual(d_sec, 50)

    def test_choisir_direction(self):
        strat = EviterObstacles(self.sim, vitesse_avance=80, vitesse_tourne=60, seuil=50)

        strat.choisir_direction(100, 50)
        self.assertEqual(strat.direction, "gauche")

    def test_gestion_strategies_initialisation(self):
        strat = GestionStrategies(self.sim)

        self.assertEqual(strat.phase, "DEPART")

    def test_gestion_strategies_update(self):
        strat = GestionStrategies(self.sim)

        strat.update(0.1)

        self.assertIn(strat.phase, ["DEPART", "EVITEMENT", "RECUL", "FREINAGE"])


if __name__ == "__main__":
    unittest.main()