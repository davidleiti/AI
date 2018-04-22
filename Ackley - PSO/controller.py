from random import random
class Controller:
    def __init__(self, swarm, w, c1, c2):
        self.__swarm = swarm
        self.__w = w
        self.__c1 = c1
        self.__c2 = c2

    def iterate(self):
        bestNeighbours = []
        for i in range(len(self.__swarm)):
            localNeighbours = self.__swarm.getNeighbourhoods(20)[i]
            localNeighbours = sorted(localNeighbours, key=lambda x: x.fitness)
            bestNeighbours.append(localNeighbours[0])

        for i in range(len(self.__swarm)):
            newVelX = self.__w * self.__swarm.getParticle(i).velocity[0]
            newVelX = newVelX + self.__c1 * random() * (bestNeighbours[i].x - self.__swarm.getParticle(i).x)
            newVelX = newVelX + self.__c2 * random() * (
                    self.__swarm.getParticle(i).bestPosition[0] - self.__swarm.getParticle(i).x)
            self.__swarm.population[i].velocity[0] = newVelX

            newVelY = self.__w * self.__swarm.getParticle(i).velocity[1]
            newVelY = newVelY + self.__c1 * random() * (bestNeighbours[i].y - self.__swarm.getParticle(i).y)
            newVelY = newVelY + self.__c2 * random() * (
                        self.__swarm.getParticle(i).bestPosition[1] - self.__swarm.getParticle(i).y)
            self.__swarm.population[i].velocity[1] = newVelY
            self.__swarm.population[i].updatePosition()






