from Source import Simulation, Affichage, RoboCar
from Source import AdaptateurSimule
from Source import creer_strategie
import time

LARGEUR = 800
HAUTEUR = 600


def main():
    sim = Simulation(LARGEUR, HAUTEUR) #creation du monde
    robot1 = RoboCar("Flash1", (600, 300), 0, simulation=sim) #creation du robot1
    robot2= RoboCar("Flash1", (400, 300), -90, simulation=sim) #creation du robot2
    adp1 = AdaptateurSimule(robot1) #adaptateur de pilotage
    adp2 = AdaptateurSimule(robot2) #adaptateur de pilotage
    view = Affichage(LARGEUR, HAUTEUR) #affichage
    strat = creer_strategie(adp1,adp2) #creation de la strategie globale
    strat.start()
    running = True
    while running:
        strat.step() #execution d'un pas de strategie
        #mise a jour physique du robot
        if not robot1.step():
            adp1.arreter()
        if not robot2.step():
            adp2.arreter()
        #affichage
        running = view.update(robot1,robot2, sim.obstacles)

        time.sleep(0.01)

    view.stop()

if __name__ == "__main__":
    main()