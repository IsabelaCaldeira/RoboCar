import pygame

from robocar import RoboCar
from obstacle import Obstacle
from simulation import Simulation
from strategies import Deplacement
from affichage import Affichage

LARGEUR = 800
HAUTEUR = 600
FPS = 60

affichage = Affichage(LARGEUR, HAUTEUR)
sim = Simulation(LARGEUR, HAUTEUR)#on cree la simulation qui contient le robot,les obstacles
strat = Deplacement(sim) #on cree la stratégie qui reçoit la simulation

def main():
    running = True
    mouvement_lineaire= False
    while running:
        dt = affichage.clock.tick(FPS) / 1000.0
        for event in affichage.events():
            if event.type == pygame.QUIT:
                running = False
        if not mouvement_lineaire:
            mouvement_lineaire=strat.avancer_x_metres(1, 80)
        else:
            strat.eviter_obstacles(80, 60, 30) #on decide quoi faire (avancer,tourner) le robot ne bouge pas la mais on regle sa vitesse seulement
        a_collision = sim.update(dt) #c'est a que le robot bouge réellement
        if a_collision:
            strat.tourner_sur_place(60)

        affichage.update(sim.robot, sim.obstacles)

    affichage.stop()

if __name__ == "__main__":
    main()