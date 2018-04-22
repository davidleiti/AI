from particle import Particle
from swarm import Swarm
from controller import Controller
from matplotlib import pyplot, pylab
p = Particle(-5,5,-5,5)
swarm = Swarm(40,-5,5,-5,5)
c = Controller(swarm, 1.0, 2.0, 0.0)
for x in range(100):
    c.iterate()
x = [i.x for i in swarm.population]
y = [i.y for i in swarm.population]
pyplot.scatter(x,y)
pylab.show()
x[0] = []
avg = []
#x in range(100):
#    avg += [swarm.avgFitness()]
#    c.iterate()
#pyplot.plot(avg)
#pylab.show()
#pop = [[x.fitness, x] for x in swarm.population]
#pop = sorted(pop, key=lambda x: x[0])
#pop = [x[1] for x in pop]
#print(pop[0])
