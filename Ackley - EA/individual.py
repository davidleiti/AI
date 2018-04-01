from random import randint, random
from math import exp, sqrt, cos, sin, pi

class Individual:
    def __init__(self, xmin, xmax, ymin, ymax):
        self.__x = random() * (xmax - xmin) + xmin
        self.__y = random() * (ymax - ymin) + ymin

    def getX(self):
        return self.__x

    def getY(self):
        return self.__y

    def fitness(self):
        first = -20 * exp(-0.2 * sqrt(0.5 * (self.getX() ** 2 + self.getY() ** 2)))
        second = exp(0.5 * (cos(2 * pi * self.getX()) + cos(2 * pi * self.getY())))
        return first - second + exp(1) + 20

    def mutate(self, probability, xmax, xmin, ymax, ymin):
        if probability > random():
            self.__x = random() * (xmax - xmin) + xmin
            self.__y = random() * (ymax - ymin) + ymin

    def crossover(self, partner):
        return Individual(self.__x, partner.getX(), self.__y, partner.getY())

    def __str__(self):
        return "{:.3f}".format(self.__x) + ", {:.3f}".format(self.__y) + ", {:.3f}".format(self.fitness())
