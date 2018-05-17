'''
Created on Apr 29, 2018

@author: Gergely
'''
LEARN_RATE = 0.01
import numpy as np
import matplotlib.pyplot as plt
from random import *
from math import *


class Neuron:
    def __init__(self, n=0):
        self._noInputs = n
        self._weights = [random() * 2 - 1 for k in range(n)]
        self._output = 0
        self._error = 0

    def linearActivate(self, info):
        net = 0.0
        for i in range(self._noInputs):
            net += info[i] * self._weights[i]
        self._output = net

    def sigmoidalActivate(self, info):
        net = 0.0
        for i in range(self._noInputs):
            net += info[i] * self._weights[i]
        try:
            net = np.clip(net, -500, 500)
            self._output = 1 / (1.0 + exp(-net))
        except OverflowError:

            print(net, "*****************************there was an overflow")
            if net > 10 ** 8:
                self._output = 0.0000001
            if net < -(10 ** 8):
                self._output = 0.9999999

    def setLinearError(self, val):
        self._error = val

    def setWeight(self, idx, val):
        self._weights[idx] = val

    def setSigmoidalError(self, val):
        self._error = val * (1 - self._output) * self._output

    def __len__(self):
        return len(self._weights)

    def getWeights(self):
        return self._weights

    def getError(self):
        return self._error

    def getOutput(self):
        return self._output

    def setOutput(self, out):
        self._output = out

    def __str__(self):
        w = [round(x, 4) for x in self._weights]
        return str(w) + '-' + str(round(self._output, 4)) + "-" + str(self._error)


class Layer:
    def __init__(self, noN, noI):
        self._noNeurons = noN
        self._neurons = [Neuron(noI) for _ in range(noN)]

    def __len__(self):
        return len(self._neurons)

    def __getitem__(self, idx):
        return self._neurons[idx]

    def getNeurons(self):
        return self._neurons


class Network:
    def __init__(self, noIn, noOut, noHidden, noNH):
        self._noInputs = noIn
        self._noOutputs = noOut
        self._noHiddenLayers = noHidden
        self._neuronsPerHiddenLayer = noNH
        self._layers = [Layer(self._noInputs, 1)]
        self._layers += [Layer(noNH, noIn)]
        self._layers += [Layer(noNH, noNH) for _ in range(noHidden - 1)]
        self._layers += [Layer(noOut, noNH)]

    def activate(self, inputs):
        # self.iterateNetwork()
        for i in range(len(self._layers[0])):
            self._layers[0][i].setOutput(inputs[i])
        for i in range(1, self._noHiddenLayers + 2):
            layers = self._layers
            '''
            for j in range(len(layers[i])):
                info=[]
                for k in range(len(layers[i][j])):
                    info.append(layers[i-1][k].getOutput())
                layers[i][j].sigmoidalActivate(info)'''
            for neuron in self._layers[i].getNeurons():
                info = []
                for k in range(len(neuron)):
                    info.append(self._layers[i - 1][k].getOutput())
                # print("before",str(neuron.getOutput()))
                neuron.sigmoidalActivate(info)
                # print("after activation",str(neuron.getOutput()))

    def errorsBackPropagate(self, err):
        for l in range(self._noHiddenLayers + 1, 0, -1):
            # print("backpropagating layer",l)
            i = 0
            for n1 in self._layers[l].getNeurons():
                if l == self._noHiddenLayers + 1:
                    n1.setLinearError(-n1.getOutput() + err[i])
                    # n1.setSigmoidalError(n1.getOutput()-err[i])
                else:
                    sumError = 0.0
                    for n2 in self._layers[l + 1].getNeurons():
                        sumError += n2.getWeights()[i] * n2.getError()
                    n1.setSigmoidalError(sumError)
                for j in range(len(n1)):
                    netWeight = n1.getWeights()[j] + LEARN_RATE * n1.getError() * self._layers[l - 1][j].getOutput()
                    # print("difference is ",n1.getWeights()[j]-netWeight)
                    n1.setWeight(j, netWeight)
                i += 1
        # print("\n")

    def errorComputationRegression(self, target, error):
        globalError = 0.0
        for i in range(len(self._layers[self._noHiddenLayers + 1])):
            error.append(target[i] - self._layers[self._noHiddenLayers + 1][i].getOutput())
            globalError += error[i] ** 2
        return globalError

    def errorComputationClassification(self, target, noLabels, error):
        # aux = [n.getOutput() for n in self._layers[self._noHiddenLayers + 1].getNeurons()]
        # m = max(aux)
        # aux = [exp(x - m) for x in aux]
        # s = sum(aux)
        # transfOutput = [x/s for x in aux]
        # m = transfOutput[0]
        # computeLabel = 1
        # for i in range(noLabels):
        #     if transfOutput[i] > m:
        #         m = transfOutput[i]
        #         computeLabel = i
        # if target == computeLabel - 1:
        #     return 0
        # else:
        #     return 1
        maxx = -1
        idx = 1
        transfOut = []
        for n in range(len(self._layers[self._noHiddenLayers + 1])):
            if self._layers[self._noHiddenLayers + 1][n].getOutput() > maxx:
                maxx = self._layers[self._noHiddenLayers + 1][n].getOutput()
                idx = n + 1
        sumExp = 0
        for i in range(noLabels):
            sumExp += exp(self._layers[self._noHiddenLayers + 1][i].getOutput() - maxx)
        for i in range(noLabels):
            transfOut.append(exp(self._layers[self._noHiddenLayers + 1][i].getOutput() - maxx) / sumExp)
        # print(transfOut,"is the transfout")
        maxx = transfOut[0]
        label = 0
        for i in range(noLabels):
            if transfOut[i] > maxx:
                maxx = transfOut[i]
                label = i
        # error=[transfOut[i]-error[i]for i in range(noLabels)]
        if target == label:
            return 0
        else:
            return 1

        # print("computed label is",label,target)
        return error[0]

    def checkGlobalError(self, error):
        correct = sum(error)
        error = correct / len(error)
        if error > 0.95:
            return True
        return False

    def normalizeData(self, noExamples, noFeatures, trainData):
        for j in range(noFeatures):
            summ = 0.0
            for i in range(noExamples):
                summ += trainData[i][j]
            mean = summ / noExamples
            squareSum = 0.0
            for i in range(noExamples):
                squareSum += (trainData[i][j] - mean) ** 2
            deviation = sqrt(squareSum / noExamples)
            for i in range(noExamples):
                trainData[i][j] = (trainData[i][j] - mean) / deviation

    def iterateNetwork(self, s=''):
        print("there are ", len(self._layers), "layers")
        for layer in self._layers:
            l = 'layer:' + str(len(layer)) + ":"
            for neuron in layer.getNeurons():
                l += str(neuron) + "  " + s
            print(l)
        print("\n")

    def learning(self, inData, outData):
        epoch = 0
        idx = [i for i in range(len(inData))]
        # shuffle(idx)
        stop = False
        errorList = []
        # self.iterateNetwork()
        while (not stop and epoch < 10):
            globalError = []
            for d in range(len(inData)):
                # self.iterateNetwork()

                self.activate(inData[d])
                err = [0 for _ in range(3)]
                err[outData[d] - 1] = 1
                globalError += [self.errorComputationClassification(outData[d] - 1, 3, err)]
                self.errorsBackPropagate(err)
            errorList.append(sum(globalError))
            # print(sum(globalError),"is the error vector")
            # res=[self._layers[self._noHiddenLayers+1][i].getOutput()for i in range(3)]
            # print(res,"res are the outputs")

            epoch += 1
        # self.iterateNetwork('\n')
        return errorList

    def readData(self, fin, fout):

        f = open(fin, 'r')
        f2 = open(fout, 'r')
        line = f.readline().strip()
        line2 = f2.readline().strip()
        X = []
        y = []
        while line != '' and line2 != '':
            # print(line)
            dataRow = line.split(' ')
            xRow = []
            for i in range(len(dataRow)):
                xRow.append(float(dataRow[i]))
            yRow = int(line2)
            X.append(xRow)
            y.append(yRow)
            line2 = f2.readline().strip()
            line = f.readline().strip()
        f.close()
        f2.close()
        return X, y

    def readData2(self, fname):
        # semantic={'NO':1,'SL':2,'DH':3,'AB':4}#for spinal column dataset
        semantic = {"Slight-Right-Turn": 1, "Sharp-Right-Turn": 2, "Move-Forward": 3, "Slight-Left-Turn": 4,
                    "Sharp-Left-Turn": 5}  # for robot dataset
        f = open(fname, 'r')
        line = f.readline().strip()
        X = []
        y = []
        while line != '':
            dataRow = line.split(' ')
            y.append(semantic[dataRow[len(dataRow) - 1]])
            dataRow = dataRow[:len(dataRow) - 1]
            xRow = []
            for i in range(len(dataRow)):
                xRow.append(float(dataRow[i]))
            X.append(xRow)
            line = f.readline().strip()
        return X, y


    def main(self):
        # choose between the three possible datasets to learn from
        # uncomment the line line which containt the data ou want the network to learn and also, the corresponding architecture from lines 294-296
        # and also from lines245-246 the corresponding semantics of the output labels, in case of spinal column or robot dataset
        X, y = self.readData("inputData.txt", "outputData.txt")  # fetal cardiograph
        # X,y=self.readData2("column_3C.txt")#column data
        # X,y=self.readData2("sensor_readings_24.data")#robot sensor readings
        noExamples = len(X)
        noFeatures = len(X[1])
        self.normalizeData(noExamples, noFeatures, X)
        print(X[-10:-1])
        print(len(X))
        print(y[-10:-1])
        print(len(y))
        #
        # # print(y)
        #
        #
        # el = self.learning(X, y)
        # # el=y
        # d = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        # for e in y:
        #     d[e] += 1
        # print("statistics is", d)
        # i = 0
        # for row in X:
        #     # row=[float(x)for x in example.split(' ')]
        #     self.activate(row)
        #     res = [self._layers[self._noHiddenLayers + 1][i].getOutput() for i in range(3)]
        #     res = [round(x, 3) for x in res]
        #     # print(res,"is the res",y[i])
        #     i += 1
        # x = [x for x in range(len(el))]
        # plt.plot(x, el, 'k')
        # plt.show()


# network = Network(21, 3, 1, 6)  # cardiograph
# # network=Network(6,3,1,6)#spinal column data
# # network=Network(24,4,1,6)#robot sensor readings
# network.main()
#
# print("asdfasd")





















































