import pygame
import math
from pygame.locals import *

clock = pygame.time.Clock()
pygame.init()
screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Flash Run - Conduite lente")
clock = pygame.time.Clock()

# -------------------- DESSIN DU JOUEUR --------------------
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
    flash = [(200, 200)]     # position du joueur
    angle = math.pi          # direction initiale
    rotation_speed = 0.03    # rotation lente, comme une voiture
    move_speed = 4        # déplacement rapide

    running = True
    while running:
        clock.tick(60)  # 60 images par seconde

        # Quitter le jeu
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        keys = pygame.key.get_pressed()

        # Sauvegarde de l'ancienne position
        old_x, old_y = flash[0]

        # Rotation lente (comme une voiture)
        if keys[K_LEFT]:
            angle -= rotation_speed
        if keys[K_RIGHT]:
            angle += rotation_speed

        # Avancer / reculer
        if keys[K_UP]:
            flash[0] = (
                flash[0][0] + math.cos(angle) * move_speed,
                flash[0][1] + math.sin(angle) * move_speed
            )
        if keys[K_DOWN]:
            flash[0] = (
                flash[0][0] - math.cos(angle) * move_speed,
                flash[0][1] - math.sin(angle) * move_speed
            )

        # Collision avec les murs (blocage)
        if (flash[0][0] < 0 or
            flash[0][1] < 0 or
            flash[0][0] + 50 > 500 or
            flash[0][1] + 50 > 500):
            flash[0] = (old_x, old_y)

        # Dessin
        screen.fill((0, 0, 0))
        draw_flash(flash[0], angle)
        pygame.display.update()

    pygame.quit()

# -------------------- LANCEMENT --------------------
start_game()
