from robocar import *
import tkinter as tk
import sys
sys.stdout.reconfigure(encoding='utf-8')

# FONCTIONS

def affichage(matrice:list, voiture:RoboCar)->None:
    """
    Affiche la matrice en plaçant la voiture à ses coordonnees et montrant ça direction
    """
    chaine = ""
    for j in range(len(matrice)):
        for i in range(len(matrice[j])-1):
            if (i, j) == voiture.coo:
                chaine += orientation(voiture) + " "
            else:
                chaine += matrice[j][i] + " "
        if (i+1, j) == voiture.coo:
            chaine += orientation(voiture) + "\n"
        else:
            chaine += matrice[j][i+1] + "\n"
    print(chaine)
    print(f"Coordoonées de la voiture: {voiture.coo}")
    print(f"Orientation de la voiture: {orientation(voiture)}")
    print("----------------------------------------------------\n")

def orientation(voiture:RoboCar)->str:
    """
    Renvoie une chaîne de caractère donnant la direction de la voiture
    """
    if voiture.s%8 == 0:
        return "↑"
    elif voiture.s%8 == 1:
        return "↗"
    elif voiture.s%8 == 2:
        return "→"
    elif voiture.s%8 == 3:
        return "↘"
    elif voiture.s%8 == 4:
        return "↓"
    elif voiture.s%8 == 5:
        return "↙"
    elif voiture.s%8 == 6:
        return "←"
    elif voiture.s%8 == 7:
        return "↖"

def avancer(matrice:list, voiture:RoboCar)->None:
    """
    Fait avancer la voiture dans matrice, affiche "MUR !" si elle est au bout
    """
    sens = voiture.s%8
    coo = voiture.coo
    if sens == 0 and coo[1]-1>=0:
        voiture.coo = (coo[0], coo[1]-1)
    elif sens == 1 and coo[1]-1>=0 and coo[0]+1<len(matrice[coo[1]]):
        voiture.coo = (coo[0]+1, coo[1]-1)
    elif sens == 2 and coo[0]+1<len(matrice[coo[1]]):
        voiture.coo = (coo[0]+1, coo[1])
    elif sens == 3 and coo[0]+1<len(matrice[coo[1]]) and coo[1]+1<len(matrice):
        voiture.coo = (coo[0]+1, coo[1]+1)
    elif sens == 4 and coo[1]+1<len(matrice): # mauvais sens
        voiture.coo = (coo[0], coo[1]+1)
    elif sens == 5 and coo[1]+1<len(matrice) and coo[0]-1>=0:
        voiture.coo = (coo[0]-1, coo[1]+1)
    elif sens == 6 and coo[0]-1>=0:
        voiture.coo = (coo[0]-1, coo[1])
    elif sens == 7 and coo[0]-1>=0 and coo[1]-1>=0:
        voiture.coo = (coo[0]-1, coo[1]-1)
    else:
        print("MUR !")

def reculer(matrice:list, voiture:RoboCar)->None:
    """
    Fait reuler la voiture dans matrice, affiche "MUR !" si elle est au bout
    """
    sens = voiture.s%8
    coo = voiture.coo
    if sens == 0 and coo[1]+1<len(matrice):
        voiture.coo = (coo[0], coo[1]+1)
    elif sens == 1 and coo[1]+1<len(matrice) and coo[0]-1>=0:
        voiture.coo = (coo[0]-1, coo[1]+1)
    elif sens == 2 and coo[0]-1>=0:
        voiture.coo = (coo[0]-1, coo[1])
    elif sens== 3 and coo[0]-1>=0 and coo[1]-1>=0:
        voiture.coo = (coo[0]-1, coo[1]-1)
    elif sens == 4 and coo[1]-1>=0: # mauvais sens
        voiture.coo = (coo[0], coo[1]-1)
    elif sens == 5 and coo[1]-1>=0 and coo[0]+1<len(matrice[coo[1]]):
        voiture.coo = (coo[0]+1, coo[1]-1)
    elif sens == 6 and coo[0]+1<len(matrice[coo[1]]):
        voiture.coo = (coo[0]+1, coo[1])
    elif sens == 7 and coo[0]+1<len(matrice[coo[1]]) and coo[1]+1<len(matrice):
        voiture.coo = (coo[0]+1, coo[1]+1)
    else:
        print("MUR !")

def lancement():
    """
    Lance une interface terminal pour contrôler la voiture
    """
    def keypressed(k):
        """
        Appel une fonction pour chaque touche pressé dans le terminale
        """
        if k.keysym == "Left":
            flash.s += -1
        if k.keysym == "Right":
            flash.s += 1
        if k.keysym == "Up":
            avancer(matrice, flash)
        if k.keysym == "Down":
            reculer(matrice, flash)
        affichage(matrice, flash)

    root = tk.Tk()
    root.bind('<KeyPress>', keypressed)

    flash = RoboCar("Flash", (1,1), 0, 0)
    matrice = [["O" for _ in range(3)] for _ in range(3)]

    affichage(matrice, flash)
    root.mainloop()

if __name__ == "__main__":
    lancement()