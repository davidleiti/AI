class Problem:
    def __init__(self, fileName):
        self.__fileName = fileName
        self.__indCount = 0
        self.__itCount = 0
        self.__xbounds = []
        self.__ybounds = []
        self.__mp = 0.0
        self.loadData()


    def loadData(self):
        file = open(self.__fileName, "r")
        try:
            self.__indCount = int(file.readline())
            self.__itCount = int(file.readline())
            self.__mp = float(file.readline())
            bounds = file.readline().split(";")
            self.__xbounds = [float(bounds[0]), float(bounds[1])]
            self.__ybounds = [float(bounds[2]), float(bounds[3])]
        except TypeError:
            print("Error loading from file")

    def getIndCount(self):
        return self.__indCount

    def getItCount(self):
        return self.__itCount

    def getXBounds(self):
        return self.__xbounds
    
    def getYBounds(self):
        return self.__ybounds

    def getMutationProbability(self):
        return self.__mp
    