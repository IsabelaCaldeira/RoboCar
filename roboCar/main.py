from Source import Simulation, GestionStrategies, Affichage,RoboCar
import time

LARGEUR = 800
HAUTEUR = 600
#dimensions de la fenetre (en pixels)
FPS = 180

def main():
    affichage = Affichage(LARGEUR, HAUTEUR)
    robot = RoboCar("Flash", (400, 300), 0)
    sim = Simulation(LARGEUR, HAUTEUR, robot, mode="robocar") #creation de la simulation
    strat = GestionStrategies(sim) #creation du gestionnaire de strategies

    running = True #variable pour savoir si le programme doit continuer
    strat.start() #on initialise les strategies

    while running:
        time.sleep(1.0 / FPS) #limite la vitesse de la boucle(attendre juste assez pour faire une boucle toutes les 1/FPS secondes)
        strat.step() #on decide quoi faire 
        sim.update() #on met a jour la position du robot
        running = affichage.update(sim.robot, sim.obstacles[1::]) #on met a jour l'affichage (le premier obstacle est le bord de la fenetre, on ne le dessine pas)

    affichage.stop()


if __name__ == "__main__":
    main()