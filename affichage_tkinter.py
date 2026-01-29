from robocar import * 
from tkinter import *
from tkinter import ttk

def creation(matrice:list, voiture:RoboCar, frm):
    """
    Creation de la matrice avec les labels pour l'affichage tkinter
    """
    mat = []
    for i in range(len(matrice)):
        ligne = []
        for j in range (len(matrice[i])):
            if (i,j) == voiture.coo:
                label = ttk.Label(frm, text=voiture.orientation())
                label.grid(column=i, row=j)
                ligne.append(label)
            else:
                label = ttk.Label(frm, text=matrice[i][j])
                label.grid(column=i, row=j)
                ligne.append(label)
        mat.append(ligne)
    ligne = []
    coo = ttk.Label(frm, text=f"Coordoonées de la voiture: {flash.coo}")
    coo.grid(column=len(matrice)+1, row=0)
    ligne.append(coo)
    orientation = ttk.Label(frm, text=f"Orientation de la voiture: {flash.orientation()}")
    orientation.grid(column=len(matrice)+1, row=1)
    ligne.append(orientation)
    mur = ttk.Label(frm, text="")
    mur.grid(column=len(matrice)+1, row=2)
    ligne.append(mur)
    mat.append(ligne)
    return mat

def actualiser(voiture:RoboCar, mat_ttk:list)->None:
    mat_ttk[voiture.coo[0]][voiture.coo[1]].config(text=voiture.orientation())
    mat_ttk[-1][1].config(text=f"Orientation de la voiture: {flash.orientation()}")
    mat_ttk[-1][2].config(text="")

def avancer(matrice:list, voiture:RoboCar, mat_ttk:list)->None:
    """
    Fait avancer la voiture dans matrice, affiche "MUR !" si elle est au bout
    """
    sens = voiture.s%8
    x,y = voiture.coo
    if sens == 0 and y-1>=0:
        mat_ttk[x][y].config(text=matrice[x][y])
        mat_ttk[x][y-1].config(text=voiture.orientation())
        voiture.coo = (x,y-1)
    elif sens == 1 and y-1>=0 and x+1<len(matrice[y]):
        mat_ttk[x][y].config(text=matrice[x][y])
        mat_ttk[x+1][y-1].config(text=voiture.orientation())
        voiture.coo = (x+1, y-1)
    elif sens == 2 and x+1<len(matrice[y]):
        mat_ttk[x][y].config(text=matrice[x][y])
        mat_ttk[x+1][y].config(text=voiture.orientation())
        voiture.coo = (x+1, y)
    elif sens == 3 and x+1<len(matrice[y]) and y+1<len(matrice):
        mat_ttk[x][y].config(text=matrice[x][y])
        mat_ttk[x+1][y+1].config(text=voiture.orientation())
        voiture.coo = (x+1, y+1)
    elif sens == 4 and y+1<len(matrice):
        mat_ttk[x][y].config(text=matrice[x][y])
        mat_ttk[x][y+1].config(text=voiture.orientation())
        voiture.coo = (x, y+1)
    elif sens == 5 and y+1<len(matrice) and x-1>=0:
        mat_ttk[x][y].config(text=matrice[x][y])
        mat_ttk[x-1][y+1].config(text=voiture.orientation())
        voiture.coo = (x-1, y+1)
    elif sens == 6 and x-1>=0:
        mat_ttk[x][y].config(text=matrice[x][y])
        mat_ttk[x-1][y].config(text=voiture.orientation())
        voiture.coo = (x-1, y)
    elif sens == 7 and x-1>=0 and y-1>=0:
        mat_ttk[x][y].config(text=matrice[x][y])
        mat_ttk[x-1][y-1].config(text=voiture.orientation())
        voiture.coo = (x-1, y-1)
    if (x,y) == voiture.coo:
        mat_ttk[-1][2].config(text="MUR !")
    else:
        mat_ttk[-1][2].config(text="")
        mat_ttk[-1][0].config(text=f"Coordoonées de la voiture: {voiture.coo}")

def reculer(matrice:list, voiture:RoboCar, mat_ttk:list)->None:
    """
    Fait reuler la voiture dans matrice, affiche "MUR !" si elle est au bout
    """
    sens = voiture.s%8
    x,y = voiture.coo
    if sens == 0 and y+1<len(matrice):
        mat_ttk[x][y].config(text=matrice[x][y])
        mat_ttk[x][y+1].config(text=voiture.orientation())
        voiture.coo = (x, y+1)
    elif sens == 1 and y+1<len(matrice) and x-1>=0:
        mat_ttk[x][y].config(text=matrice[x][y])
        mat_ttk[x-1][y+1].config(text=voiture.orientation())
        voiture.coo = (x-1, y+1)
    elif sens == 2 and x-1>=0:
        mat_ttk[x][y].config(text=matrice[x][y])
        mat_ttk[x-1][y].config(text=voiture.orientation())
        voiture.coo = (x-1, y)
    elif sens== 3 and x-1>=0 and y-1>=0:
        mat_ttk[x][y].config(text=matrice[x][y])
        mat_ttk[x-1][y-1].config(text=voiture.orientation())
        voiture.coo = (x-1, y-1)
    elif sens == 4 and y-1>=0:
        mat_ttk[x][y].config(text=matrice[x][y])
        mat_ttk[x][y-1].config(text=voiture.orientation())
        voiture.coo = (x, y-1)
    elif sens == 5 and y-1>=0 and x+1<len(matrice[y]):
        mat_ttk[x][y].config(text=matrice[x][y])
        mat_ttk[x+1][y-1].config(text=voiture.orientation())
        voiture.coo = (x+1, y-1)
    elif sens == 6 and x+1<len(matrice[y]):
        mat_ttk[x][y].config(text=matrice[x][y])
        mat_ttk[x+1][y].config(text=voiture.orientation())
        voiture.coo = (x+1, y)
    elif sens == 7 and x+1<len(matrice[y]) and y+1<len(matrice):
        mat_ttk[x][y].config(text=matrice[x][y])
        mat_ttk[x+1][y+1].config(text=voiture.orientation())
        voiture.coo = (x+1, y+1)
    if (x,y) == voiture.coo:
        mat_ttk[-1][2].config(text="MUR !")
    else:
        mat_ttk[-1][2].config(text="")
        mat_ttk[-1][0].config(text=f"Coordoonées de la voiture: {voiture.coo}")

def keypressed2(k:Event)->None:
    """
    Appel une fonction pour chaque touche pressé dans le terminale
    """
    if k.keysym == "Left":
        flash.s += -1
        actualiser(flash, mat_ttk)
    if k.keysym == "Right":
        flash.s += 1
        actualiser(flash, mat_ttk)
    if k.keysym == "Up":
        avancer(matrice, flash, mat_ttk)
    if k.keysym == "Down":
        reculer(matrice, flash, mat_ttk)

root = Tk()
root.bind('<KeyPress>', keypressed2)


flash = RoboCar("Flash", (1,1), 0, 0)
matrice = [["O" for _ in range(5)] for _ in range(5)]

frm = ttk.Frame(root, padding=10)
frm.grid()

mat_ttk = creation(matrice, flash, frm)

root.mainloop()