import pygame
import math

from robocar import RoboCar
from obstacle import Obstacle
from simulation import Simulation
from strategies import Deplacement

LARGEUR = 800
HAUTEUR = 600
FPS = 60

def draw_robot(screen, robot):
    """Cette fonction dessine le robot"""
    x, y, angle = robot.get_state()

    L = robot.longueur
    W = robot.largeur

    half_L = L / 2
    half_W = W / 2
    corners = [
        (-half_L, -half_W),
        (-half_L,  half_W),
        ( half_L,  half_W),
        ( half_L, -half_W),
    ]

    rotated = []
    for cx, cy in corners:
        rx = x + cx * math.cos(angle) - cy * math.sin(angle)
        ry = y + cx * math.sin(angle) + cy * math.cos(angle)
        rotated.append((rx, ry))

    pygame.draw.polygon(screen, (0, 200, 0), rotated)

    # ligne direction (avant)
    front_x = x + math.cos(angle) * half_L
    front_y = y + math.sin(angle) * half_L
    pygame.draw.line(screen, (255, 255, 255), (x, y), (front_x, front_y), 3)

def draw_obstacles(screen, obstacles):
    """Cette fonction dessine l'obstacle"""
    for obs in obstacles:
        pygame.draw.rect(screen, (200, 0, 0), (*obs.pos, *obs.dim))


def main():
    pygame.init()
    screen = pygame.display.set_mode((LARGEUR, HAUTEUR))
    pygame.display.set_caption("Flash car")
    clock = pygame.time.Clock()

    robot = RoboCar("Flash", (400, 300), 0)
    obstacles = [
        Obstacle("rectangle", (100, 100), (80, 100)),
        Obstacle("rectangle", (500, 200), (100, 50)),
        Obstacle("rectangle", (300, 450), (50, 50)),
    ]
    sim = Simulation(robot, obstacles, LARGEUR, HAUTEUR) #on cree la simulation qui contient le robot,les obstacles
    strat = Deplacement(sim) #on cree la stratégie qui reçoit la simulation
    
    mouvement_lineaire= False
    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        if not mouvement_lineaire:
            mouvement_lineaire=strat.avancer_x_metres(-3, 80)
        else:
            strat.eviter_obstacles(80, 60, 30) #on decide quoi faire (avancer,tourner) le robot ne bouge pas la mais on regle sa vitesse seulement
        
        a_collision = sim.update(dt) #c'est la que le robot bouge réellement
        if a_collision:
            strat.tourner_sur_place(60)

        screen.fill((0, 0, 0))
        draw_robot(screen, robot)
        draw_obstacles(screen, obstacles)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
