from math import *
from numpy import power
from operator import itemgetter
class Problem:
    def __init__(self, k):
        self.values = []
        self.targets = []
        self.test = []
        self.testTargets = []
        self.k = k
        self.loadData()

    def predictTests(self):
        predictions = []
        errors = []
        for i in range(len(self.test)):
            neighbors = []
            for j in range(len(self.values)):
                distance = self.manhattanDistance(
                    self.test[i], self.values[j])
                neighbors.append([distance, self.targets[j]])
            neighbors.sort(key=itemgetter(0))

            s = [0, 0]
            for j in range(self.k):
                s[0] += neighbors[j][1][0]
                s[1] += neighbors[j][1][1]
            s = [s[0] / self.k, s[1] / self.k]
            error = abs(sum(s) - sum(self.testTargets[i]))
            print("Predictions: ", s, ", Actual target: ", self.testTargets[i], ", error: ", error)
            errors.append(error)
        print("Average error: ", sum(errors) / (2 * len(self.test)))
        return predictions

    def euclideanDistance(self, a, b):
        s = 0.0
        for i in range(len(a)):
            s += (a[i] - b[i]) ** 2
        return sqrt(s)

    def minkowskiDistance(self, a, b, p):
        s = 0.0
        for i in range(len(a)):
            s += abs((a[i] - b[i])) ** p
        return power(s, 1/p)

    def manhattanDistance(self, a, b):
        s = 0.0
        for i in range(len(a)):
            s += abs(a[i] - b[i])
        return s

    def loadData(self):
        f = open("input.txt", "r")
        values = []
        targets = []
        test = []
        testTargets = []
        line = f.readline()
        indx = 0
        while line != "":
            temp = line.split(",")
            temp = [float(x) for x in temp]
            val = temp[1:3] + temp[6:]
            target = temp[4:6]
            if indx % 10 == 0:
                test.append(val)
                testTargets.append(target)
            else:
                values.append(val)
                targets.append(target)
            line = f.readline()
            indx += 1
        self.values = values
        self.targets = targets
        self.test = test
        self.testTargets = testTargets

p = Problem(10)
predictions = p.predictTests()