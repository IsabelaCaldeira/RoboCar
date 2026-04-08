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

        # ligne indiquant l'avant
        front_x = x + math.cos(angle) * half_L
        front_y = y + math.sin(angle) * half_L

        pygame.draw.line(self.screen, (255, 255, 255), (x, y), (front_x, front_y), 3)

    def draw_obstacles(self, obstacles):
        """Dessine les obstacles"""

        for obs in obstacles:
            pygame.draw.rect(self.screen, (200, 0, 0), (*obs.pos, *obs.dim))
    def update(self, robot1, robot2,obstacles):
        """Met a jour l'affichage et gere les evenements"""

        running = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        self.screen.fill((0, 0, 0))

        self.draw_robot(robot1)
        self.draw_robot(robot2)
        self.draw_obstacles(obstacles)

        pygame.display.update()

        return running

    def stop(self):
        pygame.quit()