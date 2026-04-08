from .strategies import AvancerXMetres, TournerXDegrees, Sequence, Condition, Boucle
from .adaptateur import Adaptateur
def obstacle_proche(adaptateur):
    """Retourne True si un obstacle est detecte a une distance proche"""
    return adaptateur.get_distance() < 60


def creer_strategie(adaptateur1,adaptateur2):
    """Cree la strategie globale du robot"""
    #phase de depart
    depart = Sequence([
        AvancerXMetres(adaptateur1, 30, 2),
    ])
    #comportement reactif,si obs proche on tourne et on avance un peu sinon
    reaction = Condition(
        TournerXDegrees(adaptateur1, 45, 0.08, 0),
        AvancerXMetres(adaptateur1, 2, 2),
        adaptateur1,
        obstacle_proche
    )
    #strategie globale
    strat = Sequence([
        depart,
        AvancerXMetres(adaptateur2, 30, 2),
        Boucle(reaction)
    ])
    return strat