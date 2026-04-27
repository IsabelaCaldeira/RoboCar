from Source import Simulation, Affichage, RoboCar
from Source import AdaptateurSimule
from Source import creer_strategie
import time

LARGEUR = 800
HAUTEUR = 600


def main():
    robot = RoboCar("Flash", (400, 300), 0) #creation du robot
    zone_robot = (
        robot.x - robot.longueur / 2,
        robot.y - robot.largeur / 2,
        robot.longueur,
        robot.largeur,
    )
    sim = Simulation(LARGEUR, HAUTEUR, zone_interdite=zone_robot) #creation du monde
    robot.simulation = sim
    adp = AdaptateurSimule(robot) #adaptateur de pilotage
    view = Affichage(LARGEUR, HAUTEUR) #affichage
    strat = creer_strategie(adp) #creation de la strategie globale
    strat.start()
    running = True
    while running:
        strat.step() #execution d'un pas de strategie
        #mise a jour physique du robot
        if not robot.step():
            adp.arreter()
        #affichage
        running = view.update(robot, sim.obstacles)

        time.sleep(0.01)

    view.stop()

if __name__ == "__main__":
    main()
