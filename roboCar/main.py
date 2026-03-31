from Source import Simulation, Affichage, RoboCar
from Source import AdaptateurSimule
from Source import AvancerXMetres, TournerXDegrees, Sequence, Condition, Boucle
import pygame
import time


LARGEUR = 800
HAUTEUR = 600


def main():
    sim = Simulation(LARGEUR, HAUTEUR)  # creation du monde
    robot = RoboCar("Flash", (400, 300), 0, simulation=sim)  # creation du robot
    adaptateur = AdaptateurSimule(robot)  # adaptateur pour piloter le robot
    view = Affichage(LARGEUR, HAUTEUR)  # affichage pygame
    # petite sequence de depart executee une seule fois
    depart = Sequence([
        AvancerXMetres(adaptateur, 40, 2),
        TournerXDegrees(adaptateur, 30, 0.08),
        AvancerXMetres(adaptateur, 25, 2),])
    #premiere reaction
    reaction1 = Condition(
        TournerXDegrees(adaptateur, 17, 0.08), #si obstacle proche
        AvancerXMetres(adaptateur, 2, 2),#sinon
        adaptateur, 28)
    #deuxieme reaction un peu differente
    reaction2 = Condition(
        TournerXDegrees(adaptateur, 23, 0.08),  #si obstacle proche
        AvancerXMetres(adaptateur, 3, 2),       #sinon
        adaptateur,35)
    #on alterne entre deux comportements
    comportement = Boucle(Sequence([
        reaction1,
        reaction2
    ]))
    #depart une seule fois puis comportement en boucle
    strat = Sequence([
        depart,
        comportement])
    strat.start()
    running = True
    while running:
        #execution d'un pas de strategie
        strat.step()
        #mise a jour physique du robot
        if not robot.step():
            adaptateur.arreter()
        view.update(robot, sim.obstacles) #affichage

        for event in pygame.event.get(): #fermeture fenetre
            if event.type == pygame.QUIT:
                running = False

        time.sleep(0.01)

    view.stop()

if __name__ == "__main__":
    main()