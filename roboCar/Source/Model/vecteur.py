# vecteur.py : définition de la classe Vecteur
# /!\ IMPORTANT : des objects vecteurs seront aussi utilisés pour représenter des points /!\
import math

class Vecteur:
    def __init__(self, x:float=0, y:float=0):
        """ Initialisation du vecteur"""
        self.x = x
        self.y = y

    def clone(self):
        """ renvoie une copie du vecteur """
        return Vecteur(self.x, self.y)
    
    def egalite(self, vec)->bool:
        """ vérifie si deux vecteurs sont égaux (même composantes) """
        return self.x == vec.x and self.y == vec.y
    
    def addition(self, vec):
        """ addition de deux vecteurs """
        return Vecteur(self.x + vec.x, self.y + vec.y)
    
    def soustraction(self, vec):
        """ soustraction de deux vecteurs """
        return Vecteur(self.x - vec.x, self.y - vec.y)
    
    def multiplication(self, scalar):
        """ multiplication d'un vecteur par un scalaire """
        return Vecteur(self.x * scalar, self.y * scalar)
    
    def norme(self)->float:
        """ norme (longueur) du vecteur """
        return math.sqrt(self.x**2 + self.y**2)
    
    def rotation(self, angle):
        """ rotation du vecteur d'un angle en degrés (sens trigonométrique ou anti-horaire) """
        rad = math.radians(angle)
        cos_a = math.cos(rad)
        sin_a = math.sin(rad)
        x_new = self.x * cos_a - self.y * sin_a
        y_new = self.x * sin_a + self.y * cos_a
        return Vecteur(x_new, y_new)
    
    def produit_scalaire(self, vec)->float:
        """ produit scalaire (u ∙ v) de deux vecteurs """
        return self.x * vec.x + self.y * vec.y
    
    def produit_vectoriel(self, vec)->float:
        """ produit vectoriel (u ∧ v) de deux vecteurs (renvoie un scalaire) """
        return self.x * vec.y - self.y * vec.x

    def point_vers_vecteur(self, point):
        """ convertit deux vecteurs considérés comme points en un vecteur (du point actuel vers l'autre) """
        return Vecteur(point.x - self.x, point.y - self.y)