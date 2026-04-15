from Source import Robot2IN013
from Source import AdaptateurReel
from Source import creer_strategie
import time

def main():
    robot = Robot2IN013()
    adp = AdaptateurReel(robot) #adaptateur de pilotage
    strat = creer_strategie(adp) #creation de la strategie globale
    strat.start()

    try:
        while True:
            strat.step()
            time.sleep(0.01)
    except KeyboardInterrupt:
        print("arret")
    finally:
        adp.arreter()
        robot.stop()

if __name__ == "__main__":
    main()

# ------------------- Commandes utiles ---------------------
# copier les fichier sur le robot:  scp -r roboCar pi@192.168.13.1:roboCar
# update les fichier du robot:      rsync -r roboCar/ pi@192.168.13.1:roboCar/
# se connecter sur le robot:        ssh pi@192.168.13.1