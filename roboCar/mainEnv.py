from Source import Simulation, Affichage, RoboCar
from Source import AdaptateurSimule
from Source import creer_strategie

import time
 
LARGEUR = 800
HAUTEUR = 600


def main():
    sim = Simulation(LARGEUR, HAUTEUR) #creation du monde
    robot = RoboCar("Flash", (50, 550), 0, simulation=sim) #creation du robot
    robot2 = RoboCar("Flash", (600, 550), 0, simulation=sim) #creation du robot2
    adp = AdaptateurSimule(robot) #adaptateur de pilotage
    adp2 = AdaptateurSimule(robot2)
    view = Affichage(LARGEUR, HAUTEUR) #affichage
    start2 = creer_strategie(adp2)
    strat = creer_strategie(adp) #creation de la strategie globale
    strat.start()
    start2.start()
    running = True
    while running:
        strat.step() #execution d'un pas de strategie
        #mise a jour physique du robot
        start2.step()

        if not robot.step():
            adp.arreter()
        if not robot2.step() : 
            adp.arreter()
        #affichage
        running = view.update2(robot,robot2, sim.obstacles)

        time.sleep(0.01)

    view.stop()

if __name__ == "__main__":
    main()