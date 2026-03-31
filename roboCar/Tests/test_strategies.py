import unittest
import math

from Source import (
    Simulation,
    RoboCar,
    AdaptateurSimule,
    AvancerXMetres,
    TournerXDegrees,
    Sequence,
    Condition,
    Boucle,
    Obstacle
)


class TestStrategies(unittest.TestCase):
    def setUp(self):
        """Cree un monde vide un robot et un adaptateur avant chaque test"""
        self.sim = Simulation(800, 600, obstacles=[])
        self.robot = RoboCar("Flash", (400, 300), 0, simulation=self.sim)
        self.adp = AdaptateurSimule(self.robot)

    def test_avancer_x_metres_start_reset(self):
        """Verifie que start() remet la distance parcourue a zero"""
        strat = AvancerXMetres(self.adp, distance=10, vitesse=2)
        strat.distance_parcourue = 99
        strat.start()
        self.assertEqual(strat.distance_parcourue, 0)

    def test_avancer_x_metres_pas_termine_au_debut(self):
        """Verifie que la strategie n'est pas terminee juste apres start()"""
        strat = AvancerXMetres(self.adp, distance=10, vitesse=2)
        strat.start()
        self.assertFalse(strat.stop())

    def test_avancer_x_metres_commande_avancer(self):
        """Verifie que step() donne une commande d'avance si la vitesse est positive"""
        strat = AvancerXMetres(self.adp, distance=10, vitesse=2)
        strat.start()
        strat.step()
        self.assertEqual(self.robot.vG, 2)
        self.assertEqual(self.robot.vR, 2)

    def test_avancer_x_metres_commande_reculer(self):
        """Verifie que step() donne une commande de recul si la vitesse est negative"""
        strat = AvancerXMetres(self.adp, distance=10, vitesse=-3)
        strat.start()
        strat.step()
        self.assertEqual(self.robot.vG, -3)
        self.assertEqual(self.robot.vR, -3)

    def test_avancer_x_metres_termine_si_distance_atteinte(self):
        """Verifie que stop() retourne True si la distance cible est atteinte"""
        strat = AvancerXMetres(self.adp, distance=10, vitesse=2)
        strat.start()
        strat.distance_parcourue = 10
        self.assertTrue(strat.stop())

    def test_avancer_x_metres_arrete_si_termine(self):
        """Verifie que step() arrete le robot si la strategie est deja terminee."""
        strat = AvancerXMetres(self.adp, distance=10, vitesse=2)
        strat.start()
        strat.distance_parcourue = 10
        #on met des vitesses non nulles avant
        self.robot.vG = 5
        self.robot.vR = 5
        strat.step()
        self.assertEqual(self.robot.vG, 0)
        self.assertEqual(self.robot.vR, 0)

    def test_tourner_x_degrees_start_reset(self):
        """Verifie que start() remet l'angle parcouru a zero"""
        strat = TournerXDegrees(self.adp, angle=90, vitesse=0.1)
        strat.angle_parcouru = 99
        strat.start()
        self.assertEqual(strat.angle_parcouru, 0)

    def test_tourner_x_degrees_pas_termine_au_debut(self):
        """Verifie que la strategie n'est pas terminee juste apres start()"""
        strat = TournerXDegrees(self.adp, angle=90, vitesse=0.1)
        strat.start()
        self.assertFalse(strat.stop())

    def test_tourner_x_degrees_commande_rotation(self):
        """Verifie que step() donne une commande de rotation sur place"""
        strat = TournerXDegrees(self.adp, angle=90, vitesse=0.1)
        strat.start()
        strat.step()
        self.assertNotEqual(self.robot.vG, self.robot.vR)
        self.assertAlmostEqual(self.robot.vG, -self.robot.vR)

    def test_tourner_x_degrees_termine_si_angle_atteint(self):
        """Verifie que stop() retourne True si l'angle cible est atteint"""
        strat = TournerXDegrees(self.adp, angle=90, vitesse=0.1)
        strat.start()
        strat.angle_parcouru = math.radians(90)
        self.assertTrue(strat.stop())

    def test_tourner_x_degrees_arrete_si_termine(self):
        """Verifie que step() arrete le robot si la strategie est deja terminee"""
        strat = TournerXDegrees(self.adp, angle=90, vitesse=0.1)
        strat.start()
        strat.angle_parcouru = math.radians(90)
        self.robot.vG = 4
        self.robot.vR = -4
        strat.step()
        self.assertEqual(self.robot.vG, 0)
        self.assertEqual(self.robot.vR, 0)

    def test_sequence_start_initialise_premiere_strategie(self):
        """Verifie que start() place la sequence sur la premiere strategie"""
        s1 = AvancerXMetres(self.adp, 5, 2)
        s2 = TournerXDegrees(self.adp, 45, 0.1)
        seq = Sequence([s1, s2])
        seq.start()
        self.assertEqual(seq.i, 0)
        self.assertEqual(s1.distance_parcourue, 0)

    def test_sequence_passe_a_la_strategie_suivante(self):
        """Verifie que la sequence passe a la strategie suivante si la strategie courante est terminee"""
        s1 = AvancerXMetres(self.adp, 5, 2)
        s2 = TournerXDegrees(self.adp, 45, 0.1)
        seq = Sequence([s1, s2])
        seq.start()
        #on force la premiere strategie a etre terminee
        s1.distance_parcourue = 5
        seq.step()
        self.assertEqual(seq.i, 1)

    def test_sequence_stop_retourne_true_si_tout_est_fini(self):
        """Verifie que stop() retourne True si toutes les strategies sont executees"""
        s1 = AvancerXMetres(self.adp, 5, 2)
        seq = Sequence([s1])
        seq.i = 1
        self.assertTrue(seq.stop())

    def test_sequence_stop_retourne_false_si_pas_fini(self):
        """Verifie que stop() retourne False si toutes les strategies ne sont pas encore executees"""
        s1 = AvancerXMetres(self.adp, 5, 2)
        seq = Sequence([s1])
        seq.i = 0
        self.assertFalse(seq.stop())

    def test_condition_choisit_s1_si_obstacle_proche(self):
        """Verifie que la condition choisit s1 si la distance detectee est inferieure au seuil"""
        #obstacle juste devant le robot
        self.sim.obstacles.append(Obstacle("rectangle", (430, 280), (40, 40)))
        s1 = TournerXDegrees(self.adp, 20, 0.1)
        s2 = AvancerXMetres(self.adp, 5, 2)
        cond = Condition(s1, s2, self.adp, 50)
        cond.start()
        cond.step()
        self.assertIs(cond.current, s1)

    def test_condition_choisit_s2_si_pas_obstacle_proche(self):
        """Verifie que la condition choisit s2 si aucun obstacle proche n'est detecte"""
        s1 = TournerXDegrees(self.adp, 20, 0.1)
        s2 = AvancerXMetres(self.adp, 5, 2)
        cond = Condition(s1, s2, self.adp, 20)
        cond.start()
        cond.step()
        self.assertIs(cond.current, s2)

    def test_condition_stop_retourne_false(self):
        """Verifie qu'une condition ne s'arrete jamais toute seule"""
        s1 = TournerXDegrees(self.adp, 20, 0.1)
        s2 = AvancerXMetres(self.adp, 5, 2)
        cond = Condition(s1, s2, self.adp, 20)
        self.assertFalse(cond.stop())

    def test_boucle_start_demarre_la_strategie(self):
        """Verifie que start() de Boucle demarre la strategie interne"""
        strat = AvancerXMetres(self.adp, 5, 2)
        boucle = Boucle(strat)
        boucle.start()
        self.assertEqual(strat.distance_parcourue, 0)

    def test_boucle_relance_si_strategie_terminee(self):
        """Verifie que Boucle relance la strategie si elle est terminee"""
        strat = AvancerXMetres(self.adp, 5, 2)
        boucle = Boucle(strat)
        boucle.start()
        strat.distance_parcourue = 5  #force stop() a True
        boucle.step()
        #si restart a bien eu lieu, la distance est reinitialisee puis step relance un mouvement
        self.assertLessEqual(strat.distance_parcourue, 5)

    def test_boucle_stop_retourne_false(self):
        """Verifie qu'une boucle ne s'arrete jamais toute seule"""
        strat = AvancerXMetres(self.adp, 5, 2)
        boucle = Boucle(strat)
        self.assertFalse(boucle.stop())


if __name__ == "__main__":
    unittest.main()