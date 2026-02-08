from robocar import *
import pygame
import math
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Flash Run")
clock = pygame.time.Clock()


def draw_flash(voiture):
    """Cette fonction dessine la voiture sur l'écran"""
    x, y = voiture.coo
    center = (int(x + 25), int(y + 25))

    pygame.draw.circle(screen, (34, 139, 34), center, 25)

    angle_rad = math.radians(voiture.a)
    tip = (center[0] + math.cos(angle_rad) * 15,center[1] + math.sin(angle_rad) * 15)

    pygame.draw.line(screen, (255, 255, 255), center, tip, 3)

def main():
    flash = RoboCar("Flash", (200, 200), 4, 0)

    v_rotation= 3
    running = True

    