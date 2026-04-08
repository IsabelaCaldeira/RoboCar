from Source import Simulation, Affichage, RoboCar
from Source import AdaptateurSimule
from Source import creer_strategie
import time

LARGEUR = 800
HAUTEUR = 600


def main():
    sim = Simulation(LARGEUR, HAUTEUR) #creation du monde
    robot = RoboCar("Flash", (100, HAUTEUR - 100), 0, simulation=sim) #creation du robot
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