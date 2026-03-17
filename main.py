from roboCar import Simulation, GestionStrategies, Affichage


LARGEUR = 800
HAUTEUR = 600
FPS = 60

affichage = Affichage(LARGEUR, HAUTEUR)
sim = Simulation(LARGEUR, HAUTEUR)
strat = GestionStrategies(sim)

def main():
    running = True

    while running:
        dt = affichage.clock.tick(FPS) / 1000.0 #le temps ecoule entre deux mises a jour
        #clock.tick(FPS) sert a controler la vitesse du programme (alors pygame va essayer de faire 60 images par seconde) et renvoie le temps ecoule depuis la derniere frame en millisecondes et on le divise par 10000 pour que ca soit en secondes
        strat.update(dt) #le robot decide quoi faire
        sim.update(dt) # on applique le mouvement reel du robot
        running = affichage.update(sim.robot, sim.obstacles, dt) #on dessine le robot et les obstacles et on recupere l'etat de la fenetre

    affichage.stop()


if __name__ == "__main__":
    main()