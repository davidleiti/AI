from particle import Particle
from numpy import mean
class Swarm:
    def __init__(self, count, xmin, xmax, ymin, ymax):
        self.__population = [Particle(xmin, xmax, ymin, ymax) for x in range(count)]

    @property
    def population(self):
        return self.__population

    def getParticle(self, pos):
        return self.__population[pos]

    def __len__(self):
        return len(self.population)

    def getNeighbourhoods(self, noOfNeighbours):
        neighbourhoods = []
        if noOfNeighbours > len(self.population):
           noOfNeighbours = len(self.population)
        for x in self.population:
            candidates = [(x.relativeDistance(y), y) for y in self.population]
            candidates = sorted(candidates, key=lambda n:n[0])
            candidates = [x[1] for x in candidates]
            local = candidates[1:noOfNeighbours]
            neighbourhoods.append(local[:])
        return neighbourhoods

    def avgFitness(self):
        f = [i.fitness for i in self.__population]
        return mean(f)


