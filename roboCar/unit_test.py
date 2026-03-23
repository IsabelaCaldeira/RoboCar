import unittest
import math
import time
from Source import (
    RoboCar,
    Simulation,
    AvancerXMetres,
    TournerXDegrees,
    Reculer,
    EviterObstacles,
    GestionStrategies,
)


class TestRoboCar(unittest.TestCase):

    def setUp(self): #setUp sert a preparer ce dont les tests ont besoin avant chaque test
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
        """Verifie que le robot se deplace correctement avec update()"""
        self.robot.set_vitesse_gauche(10)
        self.robot.set_vitesse_droite(10)

        # on simule un delta temps d'une seconde
        self.robot._last_update = time.time() - 1
        ancien_x = self.robot.x
        ancien_y = self.robot.y

        self.robot.update()

        self.assertAlmostEqual(self.robot.x, ancien_x + 10, delta=1.0)
        self.assertAlmostEqual(self.robot.y, ancien_y, delta=1.0)

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


class TestSimulation(unittest.TestCase):

    def setUp(self):
        self.sim = Simulation(800, 600)

    def test_initialisation(self):
        """Verifie les dimensions et la creation du robot"""
        self.assertEqual(self.sim.largeur, 800)
        self.assertEqual(self.sim.hauteur, 600)
        self.assertIsNotNone(self.sim.robot)
        self.assertEqual(len(self.sim.obstacles), 3)

    def test_distance_obstacle_positive(self):
        """La distance a un obstacle doit etre positive"""
        dist = self.sim.distance_obstacle()
        self.assertGreaterEqual(dist, 0)

    def test_distance_mur_positive(self):
        """La distance au mur doit être positive"""
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
        """"Le rectangle du robot doit contenir 4 points"""
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

    def test_update_retourne_bool(self):
        """update() doit retourner un booleen"""
        self.sim.robot._last_update = time.time()
        resultat = self.sim.update()
        self.assertIsInstance(resultat, bool)


class TestStrategies(unittest.TestCase):

    def setUp(self):
        self.sim = Simulation(800, 600)
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

        # on simule un déplacement du robot
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