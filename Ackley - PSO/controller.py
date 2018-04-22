from random import random
class Controller:
    def __init__(self, swarm, w, c1, c2):
        self.__swarm = swarm
        self.__w = w
        self.__c1 = c1
        self.__c2 = c2

    def iterate(self):
        bestNeighbours = []
        neighbourhoods = self.__swarm.getNeighbourhoods(50)
        for i in range(len(self.__swarm)):
            localNeighbours = neighbourhoods[i]
            localNeighbours = sorted(localNeighbours, key=lambda x: x.getFitness())
            bestNeighbours.append(localNeighbours[0])

        for i in range(len(self.__swarm)):
            #apply weight to current velocity
            newVelX = self.__w * self.__swarm.getParticle(i).getVelocity()[0]

            #change velocity based on best neighbour
            newVelX = newVelX + self.__c1 * random() * \
                (bestNeighbours[i].getPos()[0] - self.__swarm.getParticle(i).getPos()[0])

            #change velocity based on best past value
            newVelX = newVelX + self.__c2 * random() * \
                (self.__swarm.getParticle(i).getBestPosition()[0] - self.__swarm.getParticle(i).getPos()[0])

            #apply weight to current velocity
            newVelY = self.__w * self.__swarm.getParticle(i).getVelocity()[1]

            #change velocity based on best neighbour
            newVelY = newVelY + self.__c1 * random() * \
                (bestNeighbours[i].getPos()[1] - self.__swarm.getParticle(i).getPos()[1])
            newVelY = newVelY + self.__c2 * random() * \
                (self.__swarm.getParticle(i).getBestPosition()[1] - self.__swarm.getParticle(i).getPos()[1])

            self.__swarm.getPopulation()[i].setVelocity([newVelX, newVelY])
            self.__swarm.getPopulation()[i].move()






