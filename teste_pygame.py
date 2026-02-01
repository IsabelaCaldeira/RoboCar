import pygame
from pygame.locals import *

# INITIALISATION
pygame.init()
screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Flash Run")
clock = pygame.time.Clock()

# DESSIN DU JOUEUR
def draw_flash(position):
    x, y = position
    pygame.draw.rect(screen, (34, 139, 34), (int(x), int(y), 50, 50))

# JEU PRINCIPAL 
def start_game():
    flash = [(200, 200)] # Position initiale
    move_speed = 4  # Vitesse de déplacement

    running = True 
    while running:
        clock.tick(60)

        # Permet de fermer la fenêtre
        for event in pygame.event.get():  
            if event.type == QUIT:
                running = False

        # Récupération des touches pressées
        keys = pygame.key.get_pressed()

        # Sauvegarde de l'ancienne position
        old_x, old_y = flash[0]

        x, y = flash[0]

        # Déplacement selon les flèches du clavier
        if keys[K_UP]:
            y -= move_speed
        if keys[K_DOWN]:
            y += move_speed
        if keys[K_LEFT]:
            x -= move_speed
        if keys[K_RIGHT]:
            x += move_speed

        # Mise à jour de la nouvelle position
        flash[0] = (x, y)

        # COLLISION AVEC LES MURS
        # on remet l'ancienne position si on sort de l'écran
        if (flash[0][0] < 0 or
            flash[0][1] < 0 or
            flash[0][0] + 50 > 500 or
            flash[0][1] + 50 > 500):
            flash[0] = (old_x, old_y)

        # AFFICHAGE
        screen.fill((0, 0, 0))
        draw_flash(flash[0])
        pygame.display.update()

    pygame.quit()

# LANCEMENT
start_game()
