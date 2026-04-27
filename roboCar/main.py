from Source import Simulation, Affichage, RoboCar
from Source import AdaptateurSimule
from Source import creer_strategie
import time

LARGEUR = 800
HAUTEUR = 600


def main():
    robot = RoboCar("Flash", (400, 300), 0) #creation du robot
    zone_carre = (
        robot.x - 40,
        robot.y - 40,
        200,
        200,
    )
    sim = Simulation(LARGEUR, HAUTEUR, zone_interdite=zone_carre) #creation du monde
    robot.simulation = sim
    adp = AdaptateurSimule(robot) #adaptateur de pilotage
    view = Affichage(LARGEUR, HAUTEUR) #affichage
    strat = creer_strategie(adp, sim) #creation de la strategie globale
    strat.start()
    phase_3_preparee = False
    position_phase_3 = (LARGEUR / 2, HAUTEUR / 2)
    running = True
    while running:
        if strat.i >= 2 and not phase_3_preparee:
            sim.obstacles = []
            robot.appliquer(position_phase_3[0], position_phase_3[1], 0)
            adp.arreter()
            adp.synchroniser()
            sim.initialiser_souris(vitesse=1)
            phase_3_preparee = True

        if strat.i >= 2:
            sim.deplacer_souris()

        strat.step() #execution d'un pas de strategie
        #mise a jour physique du robot
        if not robot.step():
            adp.arreter()
        #affichage
        souris = sim.souris if strat.i >= 2 else None
        running = view.update(robot, sim.obstacles, souris=souris)

        time.sleep(0.01)

    view.stop()

if __name__ == "__main__":
    main()
