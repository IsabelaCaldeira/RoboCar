from .strategies import (
    AvancerXMetres,
    TournerXDegrees,
    Sequence,
    Condition,
    Boucle,
    LimiterTemps,
    SuivreSouris,
)
def obstacle_proche(adaptateur):
    """Retourne True si un obstacle est detecte a une distance proche"""
    return adaptateur.get_distance() < 60




def creer_strategie(adaptateur, simulation):
    """Cree une demo: carre, evitement d'obstacles, puis chat et souris."""
    carre = Sequence([
        AvancerXMetres(adaptateur, 120, 2.4),
        TournerXDegrees(adaptateur, 90, 0.12),
        AvancerXMetres(adaptateur, 120, 2.4),
        TournerXDegrees(adaptateur, 90, 0.12),
        AvancerXMetres(adaptateur, 120, 2.4),
        TournerXDegrees(adaptateur, 90, 0.12),
        AvancerXMetres(adaptateur, 120, 2.4),
        TournerXDegrees(adaptateur, 90, 0.12),
    ])

    reaction = Condition(
        TournerXDegrees(adaptateur, 45, 0.08, 0),
        AvancerXMetres(adaptateur, 2, 2),
        adaptateur,
        obstacle_proche
    )

    return Sequence([
        carre,
        LimiterTemps(Boucle(reaction), 30.0),
        Boucle(SuivreSouris(adaptateur, simulation)),
    ])
