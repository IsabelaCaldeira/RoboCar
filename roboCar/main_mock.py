from Source import Simulation, GestionStrategies, Affichage, Robot2IN013_MOCK, AdaptateurSimule
import time

LARGEUR = 800
HAUTEUR = 600
FPS = 180


def main():
    affichage = Affichage(LARGEUR, HAUTEUR)

    robot_mock = Robot2IN013_MOCK()
    adaptateur = AdaptateurSimule(robot_mock, coordonnees=(400, 300), angle=0)
    adaptateur.initialise()

    sim = Simulation(LARGEUR, HAUTEUR, adaptateur, mode="adaptateur")
    strat = GestionStrategies(sim)

    running = True
    strat.start()

    while running:
        time.sleep(1.0 / FPS)
        strat.step()
        sim.update()
        running = affichage.update(sim.robot, sim.obstacles)

    adaptateur.stop()
    affichage.stop()


if __name__ == "__main__":
    main()