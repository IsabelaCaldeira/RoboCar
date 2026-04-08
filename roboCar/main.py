from Source import Simulation, Affichage, RoboCar,Ballon
from Source import AdaptateurSimule
from Source import creer_strategie,creer_strategie_2
import time

LARGEUR = 800
HAUTEUR = 600


def main():
    sim = Simulation(LARGEUR, HAUTEUR) #creation du monde
    sim.obstacles=[]
    robot1 = RoboCar("Flash1", (600, 300), 0, simulation=sim) #creation du robot1
    robot2= RoboCar("Flash1", (400, 300), -90, simulation=sim) #creation du robot2
    adp1 = AdaptateurSimule(robot1) #adaptateur de pilotage
    adp2 = AdaptateurSimule(robot2) #adaptateur de pilotage
    #ballon=Ballon(300,200,3,2,20)
    view = Affichage(LARGEUR, HAUTEUR) #affichage
    #strat1 = creer_strategie(adp1) #creation de la strategie globale de adp1
    #strat1.start()
    #strat2 = creer_strategie_2(adp2) #creation de la strategie globale de adp2
    #strat2.start()
    running = True
    while running:
        #strat1.step() #execution d'un pas de strategie 1
        #strat2.step()  #execution d'un pas de strategie 2
        #mise a jour physique du robot
        if not robot1.step():
            adp1.arreter()
        if not robot2.step():
            adp2.arreter()
        #affichage
        sim.update_ballon()
        running = view.update(robot1,robot2, sim.obstacles,sim.ballon)

        time.sleep(0.01)

    view.stop()

if __name__ == "__main__":
    main()