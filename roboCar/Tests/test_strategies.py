import unittest
import math

from Source.Model import RoboCar, Simulation
from Source.Controler import (
    AvancerXMetres,
    TournerXDegrees,
    Reculer,
    EviterObstacles,
    GestionStrategies,
)


class TestStrategies(unittest.TestCase):

    def setUp(self):
        self.robot = RoboCar("Flash", (400, 300), 0)
        self.sim = Simulation(800, 600, self.robot, mode="robocar")
        self.sim.obstacles = []

    def test_avancer_x_metres_pas_termine_au_premier_appel(self):
        """AvancerXMetres ne doit pas etre termine juste apres le premier step"""
        strat = AvancerXMetres(self.sim, distance=1, vitesse=80)
        strat.start()
        strat.step()

        self.assertFalse(strat.stop())

    def test_avancer_x_metres_termine_si_distance_deja_parcourue(self):
        """AvancerXMetres se termine si la distance est atteinte"""
        strat = AvancerXMetres(self.sim, distance=1, vitesse=80)
        strat.start()
        strat.step()

        # on simule un deplacement du robot
        self.sim.robot.x += 120

        self.assertTrue(strat.stop())

    def test_avancer_x_metres_commande_avancer(self):
        """AvancerXMetres doit donner la meme vitesse aux deux roues"""
        strat = AvancerXMetres(self.sim, distance=1, vitesse=80)
        strat.start()
        strat.step()

        self.assertEqual(self.sim.robot.vG, 80)
        self.assertEqual(self.sim.robot.vR, 80)

    def test_tourner_x_degrees_pas_termine_au_premier_appel(self):
        """TournerXDegrees ne doit pas etre termine immediatement apres le debut"""
        strat = TournerXDegrees(self.sim, angle=90, vitesse=80)
        strat.start()
        strat.step()

        self.assertFalse(strat.stop())

    def test_tourner_x_degrees_commande_rotation(self):
        """TournerXDegrees doit faire tourner les roues en sens oppose"""
        strat = TournerXDegrees(self.sim, angle=90, vitesse=80)
        strat.start()
        strat.step()

        self.assertEqual(self.sim.robot.vG, 80)
        self.assertEqual(self.sim.robot.vR, -80)

    def test_tourner_x_degrees_termine_si_angle_atteint(self):
        """TournerXDegrees doit s'arreter quand l'angle cible est atteint"""
        strat = TournerXDegrees(self.sim, angle=90, vitesse=80)
        strat.start()
        strat.step()

        # on simule une rotation de 90 degres
        self.sim.robot.angle = strat.depart + math.radians(90)

        self.assertTrue(strat.stop())

    def test_tourner_x_degrees_pas_termine_si_angle_insuffisant(self):
        """TournerXDegrees ne doit pas s'arreter si l'angle est insuffisant"""
        strat = TournerXDegrees(self.sim, angle=90, vitesse=80)
        strat.start()
        strat.step()

        # on simule une rotation plus petite que 90 degres
        self.sim.robot.angle = strat.depart + math.radians(45)

        self.assertFalse(strat.stop())

    def test_reculer_pas_termine_au_premier_appel(self):
        """Reculer ne doit pas etre termine immediatement"""
        strat = Reculer(self.sim, vitesse=50, distance=0.4)
        strat.start()
        strat.step()

        self.assertFalse(strat.stop())

    def test_reculer_commande_recul(self):
        """Reculer doit appliquer des vitesses negatives aux roues"""
        strat = Reculer(self.sim, vitesse=50, distance=0.4)
        strat.start()
        strat.step()

        self.assertEqual(self.sim.robot.vG, -50)
        self.assertEqual(self.sim.robot.vR, -50)

    def test_reculer_termine_si_distance_deja_parcourue(self):
        """Reculer doit s'arreter quand la distance de recul est atteinte"""
        strat = Reculer(self.sim, vitesse=50, distance=0.4)
        strat.start()
        strat.step()

        self.sim.robot.x -= 50

        self.assertTrue(strat.stop())

    def test_eviter_obstacles_avance_si_rien_devant(self):
        """EviterObstacles doit avancer si aucun obstacle est detecte"""
        strat = EviterObstacles(self.sim, vitesse_avance=80, vitesse_tourne=60, seuil=50)
        strat.start()
        strat.step()

        self.assertEqual(self.sim.robot.vG, 80)
        self.assertEqual(self.sim.robot.vR, 80)

    def test_choisir_direction_gauche(self):
        """EviterObstacles doit choisir gauche si plus d'espace a gauche"""
        strat = EviterObstacles(self.sim, vitesse_avance=80, vitesse_tourne=60, seuil=50)
        strat.choisir_direction(100, 50)

        self.assertEqual(strat.direction, "gauche")

    def test_choisir_direction_droite(self):
        """EviterObstacles doit choisir droite si plus d'espace a droite"""
        strat = EviterObstacles(self.sim, vitesse_avance=80, vitesse_tourne=60, seuil=50)
        strat.choisir_direction(20, 80)

        self.assertEqual(strat.direction, "droite")

    def test_gestion_strategies_initialisation(self):
        """GestionStrategies doit etre correctement initialise (etat de depart)"""
        strat = GestionStrategies(self.sim)
        strat.start()

        self.assertEqual(strat.cur, -1)
        self.assertFalse(strat.mode_collision)

    def test_gestion_strategies_step(self):
        """GestionStrategies.step() doit avancer dans les strategies"""
        strat = GestionStrategies(self.sim)
        strat.start()
        strat.step()

        self.assertIn(strat.cur, [-1, 0, 1])

    def test_gestion_strategies_stop_retourne_bool(self):
        """GestionStrategies.stop() doit toujours retourner un booleen"""
        strat = GestionStrategies(self.sim)
        strat.start()

        self.assertIsInstance(strat.stop(), bool)


if __name__ == "__main__":
    unittest.main()