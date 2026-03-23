from Source import Simulation, GestionStrategies, Affichage

LARGEUR = 800
HAUTEUR = 600
#dimensions de la fenetre (en pixels)
FPS = 180

def main():
    affichage = Affichage(LARGEUR, HAUTEUR)
    sim = Simulation(LARGEUR, HAUTEUR) #creation de la simulation
    strat = GestionStrategies(sim) #creation du gestionnaire de strategies

    running = True #variable pour savoir si le programme doit continuer
    strat.start() #on initialise les strategies

    while running:
        affichage.clock.tick(FPS) #limite la vitesse de la boucle
        strat.step() #on decide quoi faire 
        sim.update() #on met a jour la position du robot
        running = affichage.update(sim.robot, sim.obstacles) #on met a jour l'affichage

    affichage.stop()


if __name__ == "__main__":
    main()