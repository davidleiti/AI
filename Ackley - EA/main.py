from problem import Problem
from algorithm import Algorithm
import functools
from matplotlib import pyplot
import pylab

def main():
    problem = Problem("in.txt")
    algorithm = Algorithm(problem)
    stats, stddev = algorithm.run()
    survivors = [ x.fitness() for x in algorithm.getIndividuals() ]
    x = [x for x in range(0, problem.getItCount())]
    pyplot.plot(stats)
    pyplot.plot(stddev)
    pylab.show()

main()

# problem = Problem("in.txt")
# algorithm = Algorithm(problem)
# algorithm.run()
# survivors = [ (x.fitness(), x) for x in algorithm.getIndividuals() ]
# survivors = sorted(survivors, key = lambda x: x[0])
# minHeight = survivors[0][0]
# minPoint = [survivors[0][1].getX(), survivors[0][1].getY()]
# print("The minimum value for the function after %d iterations is f(%.3f, %.3f) = %.3f" % \
# (problem.getItCount(), minPoint[0], minPoint[1], minHeight))
