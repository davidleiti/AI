from individual import Individual
from population import Population
from problem import Problem
from random import randint, random

class Algorithm:
    def __init__(self, problem):
        self.__problem  = problem
        x = problem.getXBounds()
        y = problem.getYBounds()
        self.__pop = Population(problem.getIndCount(), x[0], x[1], y[0], y[1])
        self.__fitnesses = [x.fitness() for x in self.__pop.getIndividuals()]

    def getPopulation(self):
        return self.__pop

    def iterate(self):
        i1 = randint(0, len(self.__pop) - 1)
        i2 = randint(0, len(self.__pop) - 1)
        if (i1 != i2):
            child = self.__pop.get(i1).crossover(self.__pop.get(i2))
            x = self.__problem.getXBounds()
            y = self.__problem.getYBounds()
            child.mutate(self.__problem.getMutationProbability(), x[0], x[1], y[0], y[1])
            f1 = self.__pop.getIndividuals()[i1].fitness()
            f2 = self.__pop.getIndividuals()[i2].fitness()
            if f1 > f2 and f1 > child.fitness():
                self.__pop.replaceIndividual(i1, child)
                self.__fitnesses += [child.fitness]
            if f2 > f1 and f2 > child.fitness():
                self.__pop.replaceIndividual(i2, child)
                self.__fitnesses += [child.fitness]

    def getIndividuals(self):
        return self.__pop.getIndividuals()
        
    def run(self):
        avg = []
        stddev = []
        for x in range(self.__problem.getItCount()):
            avg += [self.__pop.avgFitness()]
            stddev += [self.__pop.deviationFitness()]
            self.iterate()
        return avg, stddev
        





            
