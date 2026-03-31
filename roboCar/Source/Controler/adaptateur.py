from abc import ABC, abstractmethod


class Adaptateur(ABC):
    """Classe abstraite commune aux adaptateurs
    """

    @abstractmethod
    def calculer_vitesse(self, v, w):
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
    def avancer(self, vitesse):
        """Fait avancer le robot"""
        pass

    @abstractmethod
    def reculer(self, vitesse):
        """Fait reculer le robot"""
        pass

    @abstractmethod
    def arreter(self):
        """Arrete le robot"""
        pass

    @abstractmethod
    def tourner_sur_place(self, vitesse):
        """Fait tourner le robot sur lui-meme"""
        pass