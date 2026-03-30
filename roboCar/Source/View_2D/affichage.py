import pygame
import math


class Affichage:
    def __init__(self, largeur, hauteur):
        pygame.init()
        self.screen = pygame.display.set_mode((largeur, hauteur))
        pygame.display.set_caption("Flash car")
        self.clock = pygame.time.Clock()

    def draw_robot(self, robot):
        """Dessine le robot (rectangle oriente)"""
        x, y  = robot.get_position()
        angle = robot.get_angle()
        L = robot.longueur

        #corps du robot
        self.draw_polygone([robot.get_forme_robot()], color=(0, 255, 0))

        # ligne indiquant l'avant
        front_x = x + math.cos(angle) * L/2
        front_y = y + math.sin(angle) * L/2
        pygame.draw.line(self.screen, (255, 255, 255), (x, y), (front_x, front_y), 3)

    def draw_polygone(self, obstacles:list, color=(255, 0, 0)):
        """ Fonction pour dessiner des polygones quelconques sur l'écran """
        for obs in obstacles:
            points = [(p.x, p.y) for p in obs.get_points()]
            pygame.draw.polygon(self.screen, color, points)

    def update(self, robot, obstacles):
        """Met a jour l'affichage et gere les evenements"""

        running = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        self.screen.fill((0, 0, 0))

        self.draw_robot(robot)
        self.draw_polygone(obstacles)

        pygame.display.update()

        return running

    def stop(self):
        pygame.quit()