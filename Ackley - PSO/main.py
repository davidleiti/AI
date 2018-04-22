from particle import Particle
from swarm import Swarm
from controller import Controller
from matplotlib import pyplot, pylab

swarm = Swarm(100, -5, 5, -5, 5)
c = Controller(swarm, 0.5, 1.0, 2.5)
for x in range(1000):
    c.iterate()
best = 20
bestPos = [0, 0]
for p in swarm.getPopulation():
    if p.getFitness() < best:
        best = p.getFitness()
        bestPos = p.getPos()

print('Minimum value: %3.3f found at point (%3.3f, %3.3f)' % (best, bestPos[0], bestPos[1]))
# x = [i.x for i in swarm.population]
# y = [i.y for i in swarm.population]
# pyplot.scatter(x,y)
# pylab.show()
# x[0] = []
# avg = []
#x in range(100):
#    avg += [swarm.avgFitness()]
#    c.iterate()
#pyplot.plot(avg)
#pylab.show()
#pop = [[x.fitness, x] for x in swarm.population]
#pop = sorted(pop, key=lambda x: x[0])
#pop = [x[1] for x in pop]
#print(pop[0])
