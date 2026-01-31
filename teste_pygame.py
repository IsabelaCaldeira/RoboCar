import pygame
import math
from pygame.locals import *

clock = pygame.time.Clock()
pygame.init()
screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Flash Run - Conduite lente")
clock = pygame.time.Clock()


def draw_flash(position, angle):
    x, y = position
    center = (int(x + 25), int(y + 25))

    pygame.draw.circle(screen, (34, 139, 34), center, 25)

    tip = (
        center[0] + math.cos(angle) * 15,
        center[1] + math.sin(angle) * 15
    )
    left = (
        center[0] + math.cos(angle + 2.5) * 12,
        center[1] + math.sin(angle + 2.5) * 12
    )
    right = (
        center[0] + math.cos(angle - 2.5) * 12,
        center[1] + math.sin(angle - 2.5) * 12
    )

    pygame.draw.polygon(screen, (255, 255, 255), [tip, left, right])

def start_game():
    flash = [(200, 200)]    
    angle = math.pi          
    rotation_speed = 0.03   
    move_speed = 4        

    running = True
    while running:
        clock.tick(60) 

       
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        keys = pygame.key.get_pressed()

        old_x, old_y = flash[0]
        if keys[K_LEFT]:
            angle -= rotation_speed
        if keys[K_RIGHT]:
            angle += rotation_speed

        if keys[K_UP]: #on avance
            flash[0] = (
                flash[0][0] + math.cos(angle) * move_speed,
                flash[0][1] + math.sin(angle) * move_speed
            )
        if keys[K_DOWN]: #on recule
            flash[0] = (
                flash[0][0] - math.cos(angle) * move_speed,
                flash[0][1] - math.sin(angle) * move_speed
            )
        if (flash[0][0] < 0 or flash[0][1] < 0 or flash[0][0] + 50 > 500 or flash[0][1] + 50 > 500):  #si on est bloqué
            flash[0] = (old_x, old_y)

        screen.fill((0, 0, 0))
        draw_flash(flash[0], angle)
        pygame.display.update()

    pygame.quit()


start_game()
