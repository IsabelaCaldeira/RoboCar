from Source import Simulation, Affichage, RoboCar
from Source import AdaptateurSimule
from Source.Controler.comportements import (
    creer_strategie_carre,
    creer_strategie_aller_retour,
)
from Source.Controler.comportements import creer_strategie
import time

LARGEUR = 800
HAUTEUR = 600


def main():
    sim = Simulation(LARGEUR, HAUTEUR) #creation du monde
    robot_gauche = RoboCar("Flash gauche", (140, HAUTEUR // 2), 0, simulation=sim)
    robot_droite = RoboCar("Flash droite", (LARGEUR - 140, HAUTEUR // 2), -90, simulation=sim)

    adp_gauche = AdaptateurSimule(robot_gauche)
    adp_droite = AdaptateurSimule(robot_droite)

    view = Affichage(LARGEUR, HAUTEUR) #affichage
    strat_gauche= creer_strategie(adp_gauche)
    strat_droite = creer_strategie(adp_droite)

    #strat_gauche = creer_strategie_carre(adp_gauche)
    #strat_droite = creer_strategie_aller_retour(adp_droite)

    strat_gauche.start()
    strat_droite.start()

    running = True
    while running:
        strat_gauche.step()
        strat_droite.step()

        if not robot_gauche.step():
            adp_gauche.arreter()
        if not robot_droite.step():
            adp_droite.arreter()

        running = view.update([robot_gauche, robot_droite], sim.obstacles)
        time.sleep(0.01)

    view.stop()

if __name__ == "__main__":
    main()
    
