import math
from vpython import canvas, box, vector, color, rate
from Source import Simulation, RoboCar
from Source import AdaptateurSimule
from Source import creer_strategie
import math

LARGEUR = 800
HAUTEUR = 600

def conv_y(y):
    """Convertit le y du monde 2D vers le z de VPython"""
    return HAUTEUR - y #on inverse cet axe pour que l'affichage reste coherent car en 2d l'axe y descend vers le bad et nous on veut un repere plus naturel

def main():
    scene = canvas(title="Robocar en 3D",width=1000,height=700,background=vector(0.1, 0.1, 0.15) ) #creation de la scene 3d VPython
    scene.center = vector(LARGEUR / 2, 0, HAUTEUR / 2) #centre de la zone qu'on regarde
    scene.forward = vector(-1, -0.7, -1) #direction de la camera
    scene.up = vector(0, 1, 0) #direction du haut
    scene.range = 500 #niveau de zoom global

    robot = RoboCar("Flash", (100, 300), 0)
    zone_robot = (
        robot.x - robot.longueur / 2,
        robot.y - robot.largeur / 2,
        robot.longueur,
        robot.largeur,
    )
    sim = Simulation(LARGEUR, HAUTEUR, zone_interdite=zone_robot)
    robot.simulation = sim
    adp = AdaptateurSimule(robot)
    strat = creer_strategie(adp) #creation de la strategie globale
    strat.start()
    sol = box(pos=vector(LARGEUR / 2, -5, HAUTEUR / 2),size=vector(LARGEUR, 10, HAUTEUR),color=color.green) #creation du sol en 3d et on le place en dessous de y=0 pour qu'on le voie bien

    obstacles_3d = []
    for obs in sim.obstacles: #on transforme chaque obstacle 2d en boite 3d
        x, y = obs.pos
        l, w = obs.dim
        obj = box(
            pos=vector(x + l / 2, 30, conv_y(y + w / 2)), #x + l/2 et y + w/2 car VPython place une boite par son centre et 30 ici correspond a la hauteur du centre de la boite
            size=vector(l, 60, w),
            color=color.red
        )
        obstacles_3d.append(obj)
    robot_3d = box(pos=vector(robot.x, 15, conv_y(robot.y)),size=vector(robot.longueur, 30, robot.largeur),color=color.blue) #creation du robot 3d
    while True:
        rate(60) #rate(60) limite la boucle a environ 60 iterations par seconde
        strat.step()
        if not robot.step():
            adp.arreter()
        robot_3d.pos = vector(robot.x, 15, conv_y(robot.y)) #on prend la position logique du robot et on l'affiche en 3d

        #axis represente la direction de la boite donc on oriente la boite 3d dans la bonne direction
        robot_3d.axis = vector(robot.longueur * math.cos(robot.angle), 0, -robot.longueur * math.sin(robot.angle)) #on met -sin pour qu'elle devient la composante en z du monde 3d

if __name__ == "__main__":
    main()
