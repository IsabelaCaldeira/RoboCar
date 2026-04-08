from .strategies import (
    AvancerXMetres,
    TournerXDegrees,
    Sequence,
    Condition,
    Boucle,
    Dessiner,
    ChangerCouleur,
)
def obstacle_proche(adaptateur):
    """Retourne True si un obstacle est detecte a une distance proche"""
    return adaptateur.get_distance() < 60

def creer_strategie_carre(adaptateur):
    """Cree une strategie pour faire un carre"""
    return Sequence([
        Dessiner(adaptateur, True), 
        ChangerCouleur(adaptateur, (0, 0, 255)),

        AvancerXMetres(adaptateur, 80, 2), 
        TournerXDegrees(adaptateur, 90, 0.08, 0),

        AvancerXMetres(adaptateur, 80, 2),
        TournerXDegrees(adaptateur, 90, 0.08, 0),

        AvancerXMetres(adaptateur, 80, 2),
        TournerXDegrees(adaptateur, 90, 0.08, 0),

        AvancerXMetres(adaptateur, 80, 2),
        TournerXDegrees(adaptateur, 90, 0.08, 0),
    ])

def creer_strategie_aller_retour(adaptateur):
    aller_retour = Sequence([
        Dessiner(adaptateur, True),
        ChangerCouleur(adaptateur, (255, 255, 0)),

        AvancerXMetres(adaptateur, 100, 2),
        TournerXDegrees(adaptateur, 180, 0.08, 0),
        AvancerXMetres(adaptateur, 100, 2),
        TournerXDegrees(adaptateur, 180, 0.08, 0),
    ])
    return Boucle(aller_retour)



def creer_strategie(adaptateur):
    """Cree la strategie globale du robot"""
    couleurs = [
        (255, 0, 0),
        (255, 140, 0),
        (255, 220, 0),
        (0, 170, 0),
        (0, 120, 255),
        (160, 0, 200),
    ]

    cotes = [Dessiner(adaptateur, True)]
    #for i, couleur in enumerate(couleurs):
        #cotes.append(ChangerCouleur(adaptateur, couleur))
        #cotes.append(AvancerXMetres(adaptateur, 60, 2))
        #if i < len(couleurs) - 1:
            #cotes.append(TournerXDegrees(adaptateur, 60, -0.08, 0))

    #hexagone = Sequence(cotes)

    reaction = Condition(
        TournerXDegrees(adaptateur, 45, 0.08, 0),
        AvancerXMetres(adaptateur, 2, 2),
        adaptateur,
        obstacle_proche
    )

    return Sequence([
        #hexagone,
        Boucle(reaction)
    ])
