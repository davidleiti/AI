from particle import Particle
from numpy import mean
class Swarm:
    def __init__(self, count, xmin, xmax, ymin, ymax):
        self.__population = [Particle(xmin, xmax, ymin, ymax) for _ in range(count)]

    def getPopulation(self):
        return self.__population

    def getParticle(self, pos):
        return self.__population[pos]

    def __len__(self):
        return len(self.__population)

    def getNeighbourhoods(self, noOfNeighbours):
        neighbourhoods = []
        if noOfNeighbours + 1 > len(self.__population):
           noOfNeighbours = len(self.__population) - 1

        for x in self.__population:
            candidates = [(x.relativeDistance(y), y) for y in self.__population]
            candidates = sorted(candidates, key=lambda n:n[0])
            candidates = [x[1] for x in candidates]
            local = candidates[1:noOfNeighbours + 1]
            neighbourhoods.append(local[:])
        return neighbourhoods

    def avgFitness(self):
        f = [i.getFitness() for i in self.__population]
        return mean(f)


