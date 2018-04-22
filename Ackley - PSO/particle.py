from random import random
from math import exp, sqrt, cos, pi
class Particle:
    def __init__(self, xmin, xmax, ymin, ymax):
        self.__x = random() * (xmax - xmin) + xmin
        self.__y = random() * (ymax - ymin) + ymin
        self.__velocity = [0, 0]
        self.__fitness = self.__best = self.__calcFitness()
        self.__bestPos = [self.__x, self.__y]

    @property
    def fitness(self):
        return self.__fitness

    @property
    def velocity(self):
        return self.__velocity
    
    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    def updatePosition(self):
        #print("updating from (%.2f, %.2f) to (%.2f, %.2f)" % (self.x, self.y, self.x + self.velocity[0], self.y + self.velocity[1]))
        self.__x = self.__x + self.__velocity[0]
        self.__y = self.__y + self.__velocity[1]

    @property
    def bestPosition(self):
        return self.__bestPos

    @property
    def bestState(self):
        return self.__best

    def __calcFitness(self):
        first = -20 * exp(-0.2 * sqrt(0.5 * (self.x ** 2 + self.y ** 2)))
        second = exp(0.5 * (cos(2 * pi * self.y) + cos(2 * pi * self.y)))
        return first - second + exp(1) + 20

    def changePosition(self, newPosition):
        self.__x = newPosition[0]
        self.__y = newPosition[1]
        self.__fitness = self.__calcFitness()
        if self.fitness < self.bestState:
            self.__best = self.fitness
            self.__bestPos = [self.x, self.y]

    def relativeDistance(self, particle):
        return abs(particle.x - self.x) + abs(particle.y - self.y)

    def __str__(self) -> str:
        return "x: " + str(self.__x) + ", y: " + str(self.y) + ", fitness: " + str(self.fitness)




