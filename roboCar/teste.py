from roboCar.robocar import *
from roboCar.strategies import Deplacement
import pygame
from pygame.locals import *
from roboCar.obstacle import Obstacle

HAUTEUR=500
LARGEUR=500
RAYON=25
pygame.init()
screen = pygame.display.set_mode((LARGEUR,HAUTEUR))
pygame.display.set_caption("Flash Run")
clock = pygame.time.Clock()


def draw_flash(voiture):
    """Cette fonction dessine la voiture sur l'écran"""
    x, y = voiture.x, voiture.y

    pygame.draw.rect(screen, (34, 139, 34), (x,y, 50,30))

def draw_obstacles(obstacles):
    """Cette fonction dessine les obstacles sur l'écran"""
    for obs in obstacles:
        x, y = obs.pos
        w, h = obs.dim
        pygame.draw.rect(screen, (200, 0, 0), (x, y, w, h))

def main():
    """Cette fonction represente le main qui lance la boucle principale du programme"""
    flash = RoboCar("Flash", (200, 200), 90)

    v_rotation= 3
    running = True
    obstacles = [
        Obstacle("rectangle", (20, 0), (80, 50)),
        Obstacle("rectangle", (50, 0), (50, 50))
    ]
    for obs in obstacles : 
        obs.pos_aleatoire()

    strategie = Deplacement(flash, obstacles)

    while running:
        dt = clock.tick(60) / 1000.0  # convertir millisecondes en secondes
        dx = 50
        
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        #strategie.avance()
        #flash.update(dt)
        
        """for obs in obstacles:
            if flash.collision(obs):
                flash.contourne(obs)
                break"""
            
        old_x, old_y = flash.x, flash.y
        expected_x, expected_y = flash.x + dx, flash.y + dx
        while(old_x != expected_x or old_y != expected_y):
            strategie.avance()    
            flash.update(dt)  # appliquer les vitesses pour mettre à jour position"""
        
        strategie.arreter()
        
        #Fonction n'existe plus -> Recreer?
        #flash.mur_collision(LARGEUR,HAUTEUR, (old_x, old_y))

        screen.fill((0, 0, 0))
        draw_flash(flash)
        draw_obstacles(obstacles)
        pygame.display.update()

    pygame.quit()

main()