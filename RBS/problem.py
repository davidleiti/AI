from variable import *
from math import pi

class Problem:
    def __init__(self, problemFile):
        self.__firstVar = None
        self.__secondVar = None
        self.__jointVar = None
        self.__probf = problemFile
        self.__rules = []
        self.__readProblem()

    def solve(self, param1, param2):
        first, second = self.__fuzzify(param1, param2)
        inferences = self.__inference(first, second)
        aggregate = self.__aggregate(inferences)
        centers = [func.center() for func in self.__jointVar.getFunctions()]
        # functions = [i for i in range(len(aggregate)) if aggregate[i] > 0]
        # values = self.__jointVar.getValues()
        # valueMemberships = []
        # for value in values:
        #     memberships = []
        #     for func in functions:
        #         memberships.append(self.__jointVar.getFunctions()[func].compute(value))
        #     valueMemberships.append(max(memberships))
        result = self.__defuzzify(aggregate, centers)
        self.__printProgress([first, second], inferences, aggregate, result)

    def __printProgress(self, fuzzified, inferences, aggregated, result):
        print("Fuzzified values:")
        s = str(self.__firstVar.getName()) + ": ["
        for val in fuzzified[0]:
            s += "{0:.2f}".format(val) + ", "
        print(s[:-2] + "]")
        s = str(self.__secondVar.getName()) + ": ["
        for val in fuzzified[1]:
            s += "{0:.2f}".format(val) + ", "
        print(s[:-2] + "]")
        print("\nInferred values for " + str(self.__jointVar.getName()) + " labels:")
        print(inferences)
        print("\nAggregated values for " + str(self.__jointVar.getName()) + " labels:")
        print(aggregated)
        print("\nDefuzzified result:")
        print(result)
        print("\nRecommended wash cycle")
        p = aggregated.index(max(aggregated))
        a = list(inferences)[p]
        print(a)

    def __defuzzify(self, aggregate, centers):
        s1 = 0.0
        s2 = 0.0
        for i in range(len(aggregate)):
            s1 += aggregate[i] * centers[i]
            s2 += aggregate[i]
        return s1 / s2

    def __aggregate(self, inferences):
        aggregated = [max(inferences[x]) for x in inferences]
        return aggregated

    def __inference(self, firstValues, secondValues):
        inferences = {}
        for i in range(self.__firstVar.noOfLabels()):
            for j in range(self.__secondVar.noOfLabels()):
                label = self.__rules[i][j]
                if label in inferences.keys():
                    inferences[label].append(min(firstValues[i], secondValues[j]))
                else:
                    inferences[label] = [min(firstValues[i], secondValues[j])]
        return inferences

    def __fuzzify(self, param1, param2):
        values1 = []
        for func in self.__firstVar.getFunctions():
            values1.append(func.compute(param1))
        values2 = []
        for func in self.__secondVar.getFunctions():
            values2.append(func.compute(param2))
        return values1, values2

    def __readProblem(self):
        f = open(self.__probf, "r")
        variables = self.__readVars(f)
        self.__firstVar = variables[0]
        self.__secondVar = variables[1]
        self.__jointVar = variables[2]
        self.__rules = self.__readFunctions(f)

    def __readVars(self, f):
        vars = []
        for var in range(3):
            line = f.readline().strip().split(',')
            name = line[0]
            noOfFunctions = int(line[1])
            interval = [float(line[2]), float(line[3])]
            labels = [label for label in line[4:]]
            functions = []
            for func in range(noOfFunctions):
                line = f.readline().strip().split(' ')
                line = [self.__toNr(x) for x in line]
                functions.append(self.__toFunc(line))
            vars.append(FuzzyVariable(name, labels, interval, functions))
        return vars

    def __readFunctions(self, f):
        rules = []
        for i in range(self.__firstVar.noOfLabels()):
            rules.append([])
            line = f.readline().strip().split(',')
            for j in range(self.__secondVar.noOfLabels()):
                rules[i].append(line[j])
        return rules

    def __toNr(self, x):
        if x == 'inf':
            return inf
        return float(x)

    def __toFunc(self, values):
        if len(values) == 1:
            return LinearFunction(values[0])
        if len(values) == 3:
            return TriangularFunction(values[0], values[1], values[2])
        if len(values) == 4:
            return TrapezoidalFunction(values[0], values[1], values[2], values[3])

problem = Problem("problem.in")
problem.solve(0.7, 4)
