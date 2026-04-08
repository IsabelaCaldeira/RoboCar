from .strategies import AvancerXMetres, TournerXDegrees, Sequence, Condition, Boucle
from .adaptateur import Adaptateur
def obstacle_proche(adaptateur):
    """Retourne True si un obstacle est detecte a une distance proche"""
    return adaptateur.get_distance() < 60


def creer_strategie(adaptateur1,adaptateur2):
    """Cree la strategie globale du robot"""
    #phase de depart
    carre = Sequence([
        AvancerXMetres(adaptateur1, 100, 2),
        TournerXDegrees(adaptateur1,90,0.08),
        AvancerXMetres(adaptateur1, 100, 2),
        TournerXDegrees(adaptateur1,90,0.08),
        AvancerXMetres(adaptateur1, 100, 2),
        TournerXDegrees(adaptateur1,90,0.08),
        AvancerXMetres(adaptateur1, 100, 2),
        TournerXDegrees(adaptateur1,90,0.08)
    ])
    reaction = Condition(
        TournerXDegrees(adaptateur1, 45, 0.08, 0),
        carre,
        adaptateur1,
        obstacle_proche
    )
    return Boucle(reaction)