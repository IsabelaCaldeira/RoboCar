from .strategies import AvancerXMetres, TournerXDegrees, Sequence, Condition, Boucle
def obstacle_proche(adaptateur):
    """Retourne True si un obstacle est detecte a une distance proche"""
    return adaptateur.get_distance() < 40


def creer_strategie_2(adaptateur2):
    """Cree la strategie globale du robot"""
    allerRetour = Condition(
        TournerXDegrees(adaptateur2, 180, 0.08, 0),
        AvancerXMetres(adaptateur2, 360, 2),
        adaptateur2,
        obstacle_proche
    )
    return Boucle(allerRetour)