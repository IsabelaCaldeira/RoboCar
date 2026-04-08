import pygame
import math


class Affichage:
    def __init__(self, largeur, hauteur):
        pygame.init()
        self.screen = pygame.display.set_mode((largeur, hauteur))
        pygame.display.set_caption("Flash car")
        self.clock = pygame.time.Clock()

    def draw_robot(self, robot, adapateur):
        """Dessine le robot (rectangle oriente)"""

        x, y  = robot.get_position()
        angle = robot.get_angle()
        
        pygame.draw.rect(self.screen, (0, 0, 0), ((x-40,y-40), (40,10)))
        
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
    
    #Exercice 1 Question 1.2
    def draw_trajet(self, robot):
        """Affichage du trajet du robot"""
        if(robot.crayon == "abaisee"):
            x, y = robot.get_position()
            #Ou changer_couleur dans la partie (0,0,100) 
            #pygame.draw.rect(self.screen, changer_couleur("r"), ((x-50,y-10), (40,20)))
            #self.trajet.append(robot.get_position())  
        
        #for pos in self.trajet:      
        #J'arrive pas a trouver la logique pour la boucle en train de mettre la position en temps reel ici sans le step
        pygame.draw.rect(self.screen,(0, 0, 100),((x,y), (40,20)))

        
    #Exercice 1 Question 1.4
    def change_couleur(couleur):
        """Change la couleur du trace du robot"""
        if(couleur == "r"):
            return (200,0,0)
        if(couleur == "g"):
            return(0,200,0)
            

    def update(self, robot, obstacles, adapateur):
        """Met a jour l'affichage et gere les evenements"""

        running = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        self.screen.fill((0, 0, 0))

        self.draw_robot(robot, adapateur)
        self.draw_obstacles(obstacles)
        self.draw_trajet(robot)

        pygame.display.update()

        return running

    def stop(self):
        pygame.quit()