class RoboCar(object):
    def __init__(self, nom, coordonnees, vitesse, sens):
        self.n = nom    # nom:string
        self.coo = coordonnees  # coordonnees:tuple(int, int)
        self.v = vitesse    # vitesse:int
        self.s = sens  # orientation (nord:0, est:1, sud:2, ouest:3)
    