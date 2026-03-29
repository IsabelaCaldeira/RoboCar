from abc import ABC, abstractmethod


class Adaptateur(ABC):
    @abstractmethod
    def initialise(self):
        pass

    @abstractmethod
    def get_position(self):
        pass

    @abstractmethod
    def get_angle(self):
        pass

    @abstractmethod
    def get_wheel_speeds(self):
        pass

    @abstractmethod
    def set_vitesse_gauche(self, vitesse):
        pass

    @abstractmethod
    def set_vitesse_droite(self, vitesse):
        pass

    @abstractmethod
    def avancer(self, vitesse):
        pass

    @abstractmethod
    def reculer(self, vitesse):
        pass

    @abstractmethod
    def arreter(self):
        pass

    @abstractmethod
    def tourner_sur_place(self, vitesse):
        pass

    @abstractmethod
    def tourner_gauche(self, vitesse):
        pass

    @abstractmethod
    def tourner_droite(self, vitesse):
        pass

    @abstractmethod
    def calculer_vitesse(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def stop(self):
        pass