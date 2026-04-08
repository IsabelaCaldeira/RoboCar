from abc import ABC, abstractmethod


class Adaptateur(ABC):
    """Classe abstraite commune aux adaptateurs
    """

    @abstractmethod
    def set_vitesse(self, v, w):
        """Convertit une vitesse lineaire v et une vitesse angulaire w
        en vitesse de roue gauche et de roue droite"""
        pass

    @abstractmethod
    def get_distance(self):
        """Retourne la distance jusqu'a l'obstacle le plus proche"""
        pass

    @abstractmethod
    def get_distance_parcourue(self):
        """Retourne la distance parcourue depuis le dernier appel"""
        pass

    @abstractmethod
    def get_angle_parcouru(self):
        """ Retourne l'angle parcouru depuis le dernier appel"""
        pass

    @abstractmethod
    def arreter(self):
        """Arrete le robot"""
        pass

    @abstractmethod
    def dessine(self, b):
        """Active ou desactive le trace du robot"""
        pass

    @abstractmethod
    def change_couleur(self, couleur):
        """Change la couleur de la trace du robot"""
        pass
