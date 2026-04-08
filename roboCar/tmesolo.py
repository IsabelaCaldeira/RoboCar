from Source import Simulation, Affichage, RoboCar
from Source import AdaptateurSimule
from Source import creer_strategie
from Source import faire_hexagone
from Source import Obstacle
import time

LARGEUR = 800
HAUTEUR = 600

def q1_1():
    sim = Simulation(LARGEUR, HAUTEUR, [
            Obstacle("rectangle", (400,250), (50, 50)),
            Obstacle("rectangle", (400,0), (50, 50)),
            Obstacle("rectangle", (400,500), (50, 50)),
        ]) #creation du monde
    robot = RoboCar("Flash", (50, 550), 0, simulation=sim) #creation du robot
    robot.draw(False)
    adp = AdaptateurSimule(robot) #adaptateur de pilotage
    view = Affichage(LARGEUR, HAUTEUR) #affichage
    strat = creer_strategie(adp) #creation de la strategie globale
    strat.start()
    running = True
    while running:
        strat.step() #execution d'un pas de strategie
        #mise a jour physique du robot
        if not robot.step():
            adp.arreter()
        #affichage
        running = view.update(robot, sim.obstacles)

        time.sleep(0.01)

    view.stop()

def q1_2():
    sim = Simulation(LARGEUR, HAUTEUR, [
            Obstacle("rectangle", (400,250), (50, 50)),
            Obstacle("rectangle", (400,0), (50, 50)),
            Obstacle("rectangle", (400,500), (50, 50)),
        ]) #creation du monde
    robot = RoboCar("Flash", (50, 550), 0, simulation=sim) #creation du robot
    adp = AdaptateurSimule(robot) #adaptateur de pilotage
    view = Affichage(LARGEUR, HAUTEUR) #affichage
    strat = creer_strategie(adp) #creation de la strategie globale
    strat.start()
    running = True
    while running:
        strat.step() #execution d'un pas de strategie
        #mise a jour physique du robot
        if not robot.step():
            adp.arreter()
        #affichage
        running = view.update(robot, sim.obstacles)

        time.sleep(0.01)

    view.stop()

def q1_3():
    sim = Simulation(LARGEUR, HAUTEUR, [
            Obstacle("rectangle", (400,250), (50, 50)),
            Obstacle("rectangle", (400,0), (50, 50)),
            Obstacle("rectangle", (400,500), (50, 50)),
        ]) #creation du monde
    robot = RoboCar("Flash", (50, 550), 0, simulation=sim) #creation du robot
    adp = AdaptateurSimule(robot) #adaptateur de pilotage
    view = Affichage(LARGEUR, HAUTEUR) #affichage
    strat = creer_strategie(adp) #creation de la strategie globale
    strat.start()
    running = True
    while running:
        strat.step() #execution d'un pas de strategie
        #mise a jour physique du robot
        if not robot.step():
            adp.arreter()
        #affichage
        running = view.update(robot, sim.obstacles)

        time.sleep(0.01)

    view.stop()

def q1_4():
    sim = Simulation(LARGEUR, HAUTEUR, [
            Obstacle("rectangle", (400,250), (50, 50)),
            Obstacle("rectangle", (400,0), (50, 50)),
            Obstacle("rectangle", (400,500), (50, 50)),
        ]) #creation du monde
    robot = RoboCar("Flash", (50, 550), 0, simulation=sim) #creation du robot
    robot.changer_couleur((200, 0, 0))
    adp = AdaptateurSimule(robot) #adaptateur de pilotage
    view = Affichage(LARGEUR, HAUTEUR) #affichage
    strat = creer_strategie(adp) #creation de la strategie globale
    strat.start()
    running = True
    while running:
        strat.step() #execution d'un pas de strategie
        #mise a jour physique du robot
        if not robot.step():
            adp.arreter()
        #affichage
        running = view.update(robot, sim.obstacles)

        time.sleep(0.01)

    view.stop()

def q1_5():
    sim = Simulation(LARGEUR, HAUTEUR, []) #creation du monde
    robot = RoboCar("Flash", (400, 300), 0, simulation=sim) #creation du robot
    couleur = [(200, 0, 0), (0, 200, 0), (0, 0, 200), (200, 200, 0), (0, 200, 200), (200, 0, 200)]
    adp = AdaptateurSimule(robot) #adaptateur de pilotage
    view = Affichage(LARGEUR, HAUTEUR) #affichage
    strat = faire_hexagone(adp) #creation de la strategie globale
    strat.start()
    running = True
    i = 0
    while running:
        strat.step() #execution d'un pas de strategie
        robot.changer_couleur(couleur[i%6])
        i += 1
        #mise a jour physique du robot
        if not robot.step():
            adp.arreter()
        #affichage
        running = view.update(robot, sim.obstacles)

        time.sleep(0.01)

    view.stop()

def q2_1():
    sim = Simulation(LARGEUR, HAUTEUR, []) #creation du monde
    robot1 = RoboCar("Flash1", (50, 300), 0, simulation=sim) #creation du robot
    robot2 = RoboCar("Falsh2", (750, 300), 180, simulation=sim)
    adp1 = AdaptateurSimule(robot1) #adaptateur de pilotage
    adp2 = AdaptateurSimule(robot2)
    view = Affichage(LARGEUR, HAUTEUR) #affichage
    strat1 = creer_strategie(adp1) #creation de la strategie globale
    strat2 = creer_strategie(adp2)
    strat1.start()
    strat2.start()
    running = True
    while running:
        #mise a jour physique du robot
        if not robot1.step():
            adp1.arreter()
        #affichage
        running = view.update(robot1, sim.obstacles, robot2)

        time.sleep(0.01)

    view.stop()


def q2_1():
    sim = Simulation(LARGEUR, HAUTEUR, []) #creation du monde
    robot1 = RoboCar("Flash1", (50, 300), 0, simulation=sim) #creation du robot
    robot2 = RoboCar("Falsh2", (750, 300), 180, simulation=sim)
    adp1 = AdaptateurSimule(robot1) #adaptateur de pilotage
    adp2 = AdaptateurSimule(robot2)
    view = Affichage(LARGEUR, HAUTEUR) #affichage
    strat1 = creer_strategie(adp1) #creation de la strategie globale
    strat2 = creer_strategie(adp2)
    strat1.start()
    strat2.start()
    running = True
    while running:
        #mise a jour physique du robot
        if not robot1.step():
            adp1.arreter()
        #affichage
        running = view.update(robot1, sim.obstacles, robot2)

        time.sleep(0.01)

    view.stop()

def q2_2():
    sim = Simulation(LARGEUR, HAUTEUR, []) #creation du monde
    robotG = RoboCar("Flash1", (50, 300), 0, simulation=sim) #creation du robot
    robotD = RoboCar("Falsh2", (750, 300), 180, simulation=sim)
    adpG = AdaptateurSimule(robotG) #adaptateur de pilotage
    adpD = AdaptateurSimule(robotD)
    view = Affichage(LARGEUR, HAUTEUR) #affichage
    stratG = creer_strategie(adpG) #creation de la strategie globale
    stratD = creer_strategie(adpD)
    stratG.start()
    stratD.start()
    running = True
    while running:
        stratG.step() #execution d'un pas de strategie
        #mise a jour physique du robot
        if not robotG.step():
            adpG.arreter()
        #affichage
        running = view.update(robotG, sim.obstacles, robotD)

        time.sleep(0.01)

q1_5()