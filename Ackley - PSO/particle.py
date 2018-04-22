from random import random
from math import exp, sqrt, cos, pi

class Particle:
    def __init__(self, xmin, xmax, ymin, ymax):
        self.__pos = [random() * (xmax - xmin) + xmin, random() * (ymax - ymin) + ymin]
        self.__velocity = [0, 0]
        self.__fitness = self.__calculateFitness()
        self.__bestVal = self.__fitness
        self.__bestPos = [self.__pos[0], self.__pos[1]]

    def setPos(self, x, y):
        self.__pos = [x, y]

    def getFitness(self):
        return self.__fitness

    def getVelocity(self):
        return self.__velocity

    def getPos(self):
        return self.__pos

    def getBestPosition(self):
        return self.__bestPos

    def getBestValue(self):
        return self.__bestVal

    def setVelocity(self, newVel):
        self.__velocity = newVel

    def __calculateFitness(self):
        first = -20 * exp(-0.2 * sqrt(0.5 * (self.__pos[0] ** 2 + self.__pos[1] ** 2)))
        second = exp(0.5 * (cos(2 * pi * self.__pos[0]) + cos(2 * pi * self.__pos[1])))
        return first - second + exp(1) + 20

    def move(self):
        x = self.__pos[0] + self.__velocity[0]
        y = self.__pos[1] + self.__velocity[1]
        self.__pos = [x, y]
        self.__fitness = self.__calculateFitness()
        if self.__fitness < self.__bestVal:
            self.__bestVal = self.__fitness
            self.__bestPos = self.__pos

    def __str__(self):
        return "x: " + str(self.__pos[0]) + ", y: " + str(self.__pos[1]) + ", fitness: " + str(self.__fitness)

    # def changePosition(self, newPosition):
    #     self.__x = newPosition[0]
    #     self.__y = newPosition[1]
    #     self.__fitness = self.__calcFitness()
    #     if self.fitness < self.bestState:
    #         self.__best = self.fitness
    #         self.__bestPos = [self.x, self.y]

    def relativeDistance(self, particle):
        deltaX = (particle.getPos()[0] - self.__pos[0]) ** 2
        deltaY = (particle.getPos()[1] - self.__pos[1]) ** 2
        return sqrt(deltaX + deltaY)
