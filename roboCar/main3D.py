import math
from vpython import canvas, box, vector, color, rate, sphere, cylinder, cone
from Source import Simulation, RoboCar
from Source import AdaptateurSimule
from Source import creer_strategie

LARGEUR = 800
HAUTEUR = 600

def conv_y(y):
    """Convertit le y du monde 2D vers le z de VPython"""
    return HAUTEUR - y #on inverse cet axe pour que l'affichage reste coherent car en 2d l'axe y descend vers le bad et nous on veut un repere plus naturel


def creer_arbre(x, z, hauteur=90):
    """Ajoute un arbre decoratif."""
    tronc = cylinder(
        pos=vector(x, 0, z),
        axis=vector(0, hauteur, 0),
        radius=8,
        color=vector(0.45, 0.25, 0.1),
    )
    feuillage = sphere(
        pos=vector(x, hauteur + 18, z),
        radius=28,
        color=vector(0.15, 0.55, 0.2),
    )
    return tronc, feuillage


def creer_fleur(x, z, teinte):
    """Ajoute une fleur decorative."""
    tige = cylinder(
        pos=vector(x, 0, z),
        axis=vector(0, 16, 0),
        radius=1.5,
        color=vector(0.15, 0.6, 0.2),
    )
    coeur = sphere(
        pos=vector(x, 18, z),
        radius=3.5,
        color=color.yellow,
    )
    petales = []
    offsets = [(-4, 0), (4, 0), (0, -4), (0, 4)]
    for dx, dz in offsets:
        petales.append(
            sphere(
                pos=vector(x + dx, 18, z + dz),
                radius=3,
                color=teinte,
            )
        )
    return [tige, coeur, *petales]


def creer_nuage(x, y, z):
    """Ajoute un nuage simple."""
    return [
        sphere(pos=vector(x, y, z), radius=18, color=color.white, opacity=0.9),
        sphere(pos=vector(x + 18, y + 4, z + 4), radius=16, color=color.white, opacity=0.9),
        sphere(pos=vector(x - 16, y + 2, z - 2), radius=14, color=color.white, opacity=0.9),
    ]


def creer_decor():
    """Construit un decor de presentation."""
    decor = []
    decor.append(
        sphere(
            pos=vector(690, 220, 90),
            radius=34,
            color=vector(1.0, 0.82, 0.15),
            emissive=True,
        )
    )
    decor.append(
        cone(
            pos=vector(690, 185, 90),
            axis=vector(0, -40, 0),
            radius=18,
            color=vector(1.0, 0.72, 0.2),
            opacity=0.45,
        )
    )

    for x, z, teinte in [
        (260, 120, vector(1.0, 0.45, 0.55)),
        (310, 95, vector(0.95, 0.9, 0.3)),
        (560, 140, vector(0.7, 0.45, 1.0)),
        (640, 420, vector(1.0, 0.55, 0.35)),
        (210, 470, vector(0.95, 0.5, 0.8)),
        (530, 500, vector(0.5, 0.85, 1.0)),
    ]:
        decor.extend(creer_fleur(x, z, teinte))

    for x, y, z in [(180, 230, 140), (420, 250, 90), (560, 220, 170)]:
        decor.extend(creer_nuage(x, y, z))

    return decor


def creer_arbre_obstacle(x, z, largeur, profondeur):
    """Transforme un obstacle en arbre decoratif."""
    # On derive la taille visuelle de l'arbre a partir de l'obstacle 2D.
    rayon_tronc = max(6, min(largeur, profondeur) * 0.12)
    hauteur_tronc = max(45, (largeur + profondeur) * 0.35)
    rayon_feuillage = max(24, max(largeur, profondeur) * 0.4)

    tronc = cylinder(
        pos=vector(x, 0, z),
        axis=vector(0, hauteur_tronc, 0),
        radius=rayon_tronc,
        color=vector(0.45, 0.25, 0.1),
    )
    feuillage_bas = sphere(
        pos=vector(x, hauteur_tronc + rayon_feuillage * 0.35, z),
        radius=rayon_feuillage,
        color=vector(0.16, 0.52, 0.2),
    )
    feuillage_haut = sphere(
        pos=vector(x, hauteur_tronc + rayon_feuillage * 0.95, z),
        radius=rayon_feuillage * 0.72,
        color=vector(0.2, 0.6, 0.24),
    )
    return [tronc, feuillage_bas, feuillage_haut]

def main():
    scene = canvas(title="Robocar en 3D",width=1000,height=700,background=vector(0.58, 0.82, 0.98) ) #creation de la scene 3d VPython
    scene.center = vector(LARGEUR / 2, 0, HAUTEUR / 2) #centre de la zone qu'on regarde
    scene.forward = vector(-1, -0.7, -1) #direction de la camera
    scene.up = vector(0, 1, 0) #direction du haut
    scene.range = 500 #niveau de zoom global
    scene.ambient = vector(0.8, 0.8, 0.8)

    robot = RoboCar("Flash", (100, 300), 0)
    zone_carre = (
        robot.x - 40,
        robot.y - 40,
        200,
        200,
    )
    sim = Simulation(LARGEUR, HAUTEUR, zone_interdite=zone_carre)
    robot.simulation = sim
    adp = AdaptateurSimule(robot)
    strat = creer_strategie(adp, sim) #creation de la strategie globale
    strat.start()
    # La phase 3 repart d'un terrain vide pour laisser la poursuite s'exprimer.
    phase_3_preparee = False
    position_phase_3 = (LARGEUR / 2, HAUTEUR / 2)
    sol = box(
        pos=vector(LARGEUR / 2, -5, HAUTEUR / 2),
        size=vector(LARGEUR, 10, HAUTEUR),
        color=vector(0.3, 0.68, 0.28),
    )
    creer_decor()

    obstacles_3d = []
    # En 3D les obstacles sont affiches comme des arbres plutot que des blocs rouges.
    for obs in sim.obstacles: #on transforme chaque obstacle 2d en arbre 3d
        x, y = obs.pos
        l, w = obs.dim
        obstacles_3d.append(
            creer_arbre_obstacle(x + l / 2, conv_y(y + w / 2), l, w)
        )
    robot_3d = box(
        pos=vector(robot.x, 15, conv_y(robot.y)),
        size=vector(robot.longueur, 30, robot.largeur),
        color=vector(0.1, 0.38, 0.95),
    ) #creation du robot 3d
    souris_3d = sphere(
        pos=vector(0, 12, 0),
        radius=10,
        color=color.yellow,
        emissive=True,
        visible=False,
    )
    while True:
        if strat.i >= 2 and not phase_3_preparee:
            # A l'entree de la phase 3 on vide les obstacles et on recentre le robot.
            sim.obstacles = []
            robot.appliquer(position_phase_3[0], position_phase_3[1], 0)
            adp.arreter()
            adp.synchroniser()
            sim.initialiser_souris(vitesse=1)
            for obstacle_3d in obstacles_3d:
                for partie in obstacle_3d:
                    partie.visible = False
            phase_3_preparee = True

        if strat.i >= 2:
            # La souris n'existe et ne bouge qu'en phase de chat et souris.
            sim.deplacer_souris()
            souris_3d.visible = sim.souris is not None
        else:
            souris_3d.visible = False

        rate(60) #rate(60) limite la boucle a environ 60 iterations par seconde
        strat.step()
        if not robot.step():
            adp.arreter()
        robot_3d.pos = vector(robot.x, 15, conv_y(robot.y)) #on prend la position logique du robot et on l'affiche en 3d
        if sim.souris is not None:
            souris_3d.pos = vector(
                sim.souris["x"] + sim.souris["taille"] / 2,
                12,
                conv_y(sim.souris["y"] + sim.souris["taille"] / 2),
            )

        #axis represente la direction de la boite donc on oriente la boite 3d dans la bonne direction
        robot_3d.axis = vector(robot.longueur * math.cos(robot.angle), 0, -robot.longueur * math.sin(robot.angle)) #on met -sin pour qu'elle devient la composante en z du monde 3d

if __name__ == "__main__":
    main()
