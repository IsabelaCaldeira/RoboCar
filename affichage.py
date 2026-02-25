import pygame
import math

from robocar import RoboCar
from obstacle import Obstacle
from simulation import Simulation
from strategies import Deplacement

LARGEUR = 800
HAUTEUR = 600

class Affichage():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((LARGEUR, HAUTEUR))
        pygame.display.set_caption("Flash car")
        self.clock = pygame.time.Clock()

    def draw_robot(self,robot):
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

        pygame.draw.polygon(self.screen, (0, 200, 0), rotated)

        # ligne direction (avant)
        front_x = x + math.cos(angle) * half_L
        front_y = y + math.sin(angle) * half_L
        pygame.draw.line(self.screen, (255, 255, 255), (x, y), (front_x, front_y), 3)

    def draw_obstacles(self, obstacles):
        """Cette fonction dessine l'obstacle"""
        for obs in obstacles:
            pygame.draw.rect(self.screen, (200, 0, 0), (*obs.pos, *obs.dim))

    def update(self, robot, obstacles):
        self.screen.fill((0, 0, 0))
        self.draw_robot(robot)
        self.draw_obstacles(obstacles)
        pygame.display.update()

    def events(self):
        return pygame.event.get()

    def stop(self):
        pygame.quit()



