from robocar import *
import pygame
import math
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Flash Run")
clock = pygame.time.Clock()

rayon = 25

def draw_flash(voiture):
    """Cette fonction dessine la voiture sur l'écran"""
    x, y = voiture.coo
    center = (int(x + rayon), int(y + rayon))

    pygame.draw.circle(screen, (34, 139, 34), center, rayon)

    angle_rad = math.radians(voiture.a)
    tip = (center[0] + math.cos(angle_rad) * 15,center[1] + math.sin(angle_rad) * 15)

    pygame.draw.line(screen, (255, 255, 255), center, tip, 3)

def draw_obstacles(obstacles):
    """Cette fonction dessine les obstacles sur l'écran"""
    for obs in obstacles:
        x, y = obs.pos
        w, h = obs.dim
        pygame.draw.rect(screen, (200, 0, 0), (x, y, w, h))


def main():
    """Cette fonction represente le main qui lance la boucle principale du programme"""
    flash = RoboCar("Flash", (200, 200), 4, 0, rayon)

    v_rotation= 3
    running = True
    obstacles = [
    Obstacle("rectangle", (100, 150), (80, 50)),
    Obstacle("rectangle", (300, 200), (50, 50))
]

    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        keys = pygame.key.get_pressed()
        old_x, old_y = flash.coo #on sauvegarde les anciennes coordonnees pour le cas de collision
        if keys[K_LEFT]:
            flash.tourner_gauche(v_rotation)

        if keys[K_RIGHT]:
            flash.tourner_droite(v_rotation)

        if keys[K_UP]:
            flash.avancer()

        if keys[K_DOWN]:
            flash.reculer()

        for obs in obstacles:
            if flash.collision(obs):
                flash.Contourne(flash.coo, flash.a, obstacles)
                return

        # collision avec le mur
        if (flash.coo[0] < 0 or flash.coo[1] < 0 or
            flash.coo[0] + 50 > 500 or flash.coo[1] + 50 > 500):
            flash.coo = (old_x, old_y)
        if event.type == KEYDOWN and event.key == K_SPACE:
            trajet_carre = flash.trajectoire_carree(50)

        screen.fill((0, 0, 0))
        draw_flash(flash)
        draw_obstacles(obstacles)
        pygame.display.update()


    pygame.quit()


main()
