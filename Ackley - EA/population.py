from individual import Individual
import functools
import numpy as np

class Population:
    def __init__(self, n, xmin, xmax, ymin, ymax):
        self.__individuals = [Individual(xmin, xmax, ymin, ymax) for x in range(n)]

    def __len__(self):
        return len(self.__individuals)

    def avgFitness(self):
        f = [i.fitness() for i in self.__individuals]
        return np.mean(f)

    def deviationFitness(self):
        f = [i.fitness() for i in self.__individuals]
        return np.std(f)

    def getIndividuals(self):
        return self.__individuals

    def get(self, pos):
        return self.__individuals[pos]

    def addIndividual(self, individual):
        self.__individuals += individual

    def removeIndividual(self, pos):
        self.__individuals.pop(pos)

    def replaceIndividual(self, pos, new):
        self.__individuals[pos] = new

    def __str__(self):
        s = ""
        for i in self.__individuals:
            s += str(i) + "\n"
        return s