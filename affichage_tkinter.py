from robocar import * 
from tkinter import *
from tkinter import ttk

def affiche(matrice:list, voiture:RoboCar, frm)->None:
    """
    Affiche la matrice et la voiture dans la fenêtre tkinter (initialisation)
    """
    for i in range(len(matrice)):
        for j in range(len(matrice[i])-1):
            if (i, j) == voiture.coo:
                ttk.Label(frm, text=voiture.orientation()).grid(column=i, row=j)
            else:
                ttk.Label(frm, text=matrice[i][j]).grid(column=i, row=j)
        if (i, j+1) == voiture.coo:
            ttk.Label(frm, text=voiture.orientation()).grid(column=i, row=j+1)
        else:
            ttk.Label(frm, text=matrice[i][j+1]).grid(column=i, row=j+1)
    ttk.Label(frm, text=f"Coordoonées de la voiture: {voiture.coo}").grid(column=i+1, row=0)
    ttk.Label(frm, text=f"Orientation de la voiture: {voiture.orientation()}").grid(column=i+1, row=1)

def actualiser(matrice:list, voiture:RoboCar)->None:
    ttk.Label(frm, text=voiture.orientation()).grid(column=voiture.coo[0], row=voiture.coo[1])
    ttk.Label(frm, text="               ").grid(column=len(matrice), row=2)
    ttk.Label(frm, text=f"Orientation de la voiture: {voiture.orientation()}").grid(column=len(matrice), row=1)

def avancer(matrice:list, voiture:RoboCar)->None:
    """
    Fait avancer la voiture dans matrice, affiche "MUR !" si elle est au bout
    """
    sens = voiture.s%8
    coo = voiture.coo
    if sens == 0 and coo[1]-1>=0:
        ttk.Label(frm, text=matrice[coo[0]][coo[1]]).grid(column=coo[0], row=coo[1])
        ttk.Label(frm, text=voiture.orientation()).grid(column=coo[0], row=coo[1]-1)
        voiture.coo = (coo[0], coo[1]-1)
    elif sens == 1 and coo[1]-1>=0 and coo[0]+1<len(matrice[coo[1]]):
        ttk.Label(frm, text=matrice[coo[0]][coo[1]]).grid(column=coo[0], row=coo[1])
        ttk.Label(frm, text=voiture.orientation()).grid(column=coo[0]+1, row=coo[1]-1)
        voiture.coo = (coo[0]+1, coo[1]-1)
    elif sens == 2 and coo[0]+1<len(matrice[coo[1]]):
        ttk.Label(frm, text=matrice[coo[0]][coo[1]]).grid(column=coo[0], row=coo[1])
        ttk.Label(frm, text=voiture.orientation()).grid(column=coo[0]+1, row=coo[1])
        voiture.coo = (coo[0]+1, coo[1])
    elif sens == 3 and coo[0]+1<len(matrice[coo[1]]) and coo[1]+1<len(matrice):
        ttk.Label(frm, text=matrice[coo[0]][coo[1]]).grid(column=coo[0], row=coo[1])
        ttk.Label(frm, text=voiture.orientation()).grid(column=coo[0]+1, row=coo[1]+1)
        voiture.coo = (coo[0]+1, coo[1]+1)
    elif sens == 4 and coo[1]+1<len(matrice):
        ttk.Label(frm, text=matrice[coo[0]][coo[1]]).grid(column=coo[0], row=coo[1])
        ttk.Label(frm, text=voiture.orientation()).grid(column=coo[0], row=coo[1]+1)
        voiture.coo = (coo[0], coo[1]+1)
    elif sens == 5 and coo[1]+1<len(matrice) and coo[0]-1>=0:
        ttk.Label(frm, text=matrice[coo[0]][coo[1]]).grid(column=coo[0], row=coo[1])
        ttk.Label(frm, text=voiture.orientation()).grid(column=coo[0]-1, row=coo[1]+1)
        voiture.coo = (coo[0]-1, coo[1]+1)
    elif sens == 6 and coo[0]-1>=0:
        ttk.Label(frm, text=matrice[coo[0]][coo[1]]).grid(column=coo[0], row=coo[1])
        ttk.Label(frm, text=voiture.orientation()).grid(column=coo[0]-1, row=coo[1])
        voiture.coo = (coo[0]-1, coo[1])
    elif sens == 7 and coo[0]-1>=0 and coo[1]-1>=0:
        ttk.Label(frm, text=matrice[coo[0]][coo[1]]).grid(column=coo[0], row=coo[1])
        ttk.Label(frm, text=voiture.orientation()).grid(column=coo[0]-1, row=coo[1]-1)
        voiture.coo = (coo[0]-1, coo[1]-1)
    if coo == voiture.coo:
        ttk.Label(frm, text="MUR !").grid(column=len(matrice), row=2)
    else:
        ttk.Label(frm, text="               ").grid(column=len(matrice), row=2)
        ttk.Label(frm, text=f"Coordoonées de la voiture: {voiture.coo}").grid(column=len(matrice), row=0)

def reculer(matrice:list, voiture:RoboCar)->None:
    """
    Fait reuler la voiture dans matrice, affiche "MUR !" si elle est au bout
    """
    sens = voiture.s%8
    coo = voiture.coo
    if sens == 0 and coo[1]+1<len(matrice):
        ttk.Label(frm, text=matrice[coo[0]][coo[1]]).grid(column=coo[0], row=coo[1])
        ttk.Label(frm, text=voiture.orientation()).grid(column=coo[0], row=coo[1]+1)
        voiture.coo = (coo[0], coo[1]+1)
    elif sens == 1 and coo[1]+1<len(matrice) and coo[0]-1>=0:
        ttk.Label(frm, text=matrice[coo[0]][coo[1]]).grid(column=coo[0], row=coo[1])
        ttk.Label(frm, text=voiture.orientation()).grid(column=coo[0]-1, row=coo[1]+1)
        voiture.coo = (coo[0]-1, coo[1]+1)
    elif sens == 2 and coo[0]-1>=0:
        ttk.Label(frm, text=matrice[coo[0]][coo[1]]).grid(column=coo[0], row=coo[1])
        ttk.Label(frm, text=voiture.orientation()).grid(column=coo[0]-1, row=coo[1])
        voiture.coo = (coo[0]-1, coo[1])
    elif sens== 3 and coo[0]-1>=0 and coo[1]-1>=0:
        ttk.Label(frm, text=matrice[coo[0]][coo[1]]).grid(column=coo[0], row=coo[1])
        ttk.Label(frm, text=voiture.orientation()).grid(column=coo[0]-1, row=coo[1]-1)
        voiture.coo = (coo[0]-1, coo[1]-1)
    elif sens == 4 and coo[1]-1>=0:
        ttk.Label(frm, text=matrice[coo[0]][coo[1]]).grid(column=coo[0], row=coo[1])
        ttk.Label(frm, text=voiture.orientation()).grid(column=coo[0], row=coo[1]-1)
        voiture.coo = (coo[0], coo[1]-1)
    elif sens == 5 and coo[1]-1>=0 and coo[0]+1<len(matrice[coo[1]]):
        ttk.Label(frm, text=matrice[coo[0]][coo[1]]).grid(column=coo[0], row=coo[1])
        ttk.Label(frm, text=voiture.orientation()).grid(column=coo[0]+1, row=coo[1]-1)
        voiture.coo = (coo[0]+1, coo[1]-1)
    elif sens == 6 and coo[0]+1<len(matrice[coo[1]]):
        ttk.Label(frm, text=matrice[coo[0]][coo[1]]).grid(column=coo[0], row=coo[1])
        ttk.Label(frm, text=voiture.orientation()).grid(column=coo[0]+1, row=coo[1])
        voiture.coo = (coo[0]+1, coo[1])
    elif sens == 7 and coo[0]+1<len(matrice[coo[1]]) and coo[1]+1<len(matrice):
        ttk.Label(frm, text=matrice[coo[0]][coo[1]]).grid(column=coo[0], row=coo[1])
        ttk.Label(frm, text=voiture.orientation()).grid(column=coo[0]+1, row=coo[1]+1)
        voiture.coo = (coo[0]+1, coo[1]+1)
    if coo == voiture.coo:
        ttk.Label(frm, text="MUR !").grid(column=len(matrice), row=2)
    else:
        ttk.Label(frm, text="               ").grid(column=len(matrice), row=2)
        ttk.Label(frm, text=f"Coordoonées de la voiture: {voiture.coo}").grid(column=len(matrice), row=0)

def keypressed2(k:Event)->None:
    """
    Appel une fonction pour chaque touche pressé dans le terminale
    """
    if k.keysym == "Left":
        flash.s += -1
        actualiser(matrice, flash)
    if k.keysym == "Right":
        flash.s += 1
        actualiser(matrice, flash)
    if k.keysym == "Up":
        avancer(matrice, flash)
    if k.keysym == "Down":
        reculer(matrice, flash)

root = Tk()
root.bind('<KeyPress>', keypressed2)


flash = RoboCar("Flash", (1,1), 0, 0)
matrice = [["O" for _ in range(5)] for _ in range(5)]

frm = ttk.Frame(root, padding=10)
frm.grid()

affiche(matrice, flash, frm)

root.mainloop()