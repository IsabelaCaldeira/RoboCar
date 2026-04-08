from .strategies import AvancerXMetres, TournerXDegrees, Sequence, Condition, Boucle
def obstacle_proche(adaptateur):
    """Retourne True si un obstacle est detecte a une distance proche"""
    return adaptateur.get_distance() < 60


def creer_strategie(adaptateur):
    """Cree la strategie globale du robot"""
    #phase de depart
    depart = Sequence([
        AvancerXMetres(adaptateur, 30, 2),
    ])
    #comportement reactif,si obs proche on tourne et on avance un peu sinon
    reaction = Condition(
        TournerXDegrees(adaptateur, 45, 0.08, 0),
        AvancerXMetres(adaptateur, 2, 2),
        adaptateur,
        obstacle_proche
    )
    #strategie globale
    strat = Sequence([
        depart,
        Boucle(reaction)
    ])
    return strat
def AllerRetour(adaptateur):
      #phase de depart
    depart = Sequence([
        AvancerXMetres(adaptateur, 30, 2),
    ])
    arriver = Sequence([AvancerXMetres(adaptateur, -30, 2)])
    

    #strategie globale
    strat = Sequence([
        depart,
        arriver
    ])
    return strat