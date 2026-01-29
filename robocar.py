class RoboCar(object):
    def __init__(self, nom, coordonnees, vitesse, sens):
        self.n = nom    # nom:string
        self.coo = coordonnees  # coordonnees:tuple(int, int)
        self.v = vitesse    # vitesse:int
        self.s = sens  # orientation (nord:0, nord-est:1, est:2, sud-est:3, sud:4, sud-ouest:5,
                    #                   ouest:6, nord-ouest:7)
    
    def orientation(self)->str:
        """
        Renvoie une chaîne de caractère donnant la direction de la voiture
        """
        if self.s%8 == 0:
            return "↑"
        elif self.s%8 == 1:
            return "↗"
        elif self.s%8 == 2:
            return "→"
        elif self.s%8 == 3:
            return "↘"
        elif self.s%8 == 4:
            return "↓"
        elif self.s%8 == 5:
            return "↙"
        elif self.s%8 == 6:
            return "←"
        elif self.s%8 == 7:
            return "↖"