import numpy as np
import multiprocessing
import random
import math

class NodeCreationThreadObject(object):
    threadCount = None
    threadIndex = None
    def __init__(self, threadCount, threadIndex):
        self.threadCount = threadCount
        self.threadIndex = threadIndex

class EdgeCreationThreadObject(object):
    threadCount = None
    threadIndex = None
    def __init__(self, threadCount, threadIndex):
        self.threadCount = threadCount
        self.threadIndex = threadIndex

class CellCleaningThreadObject(object):
    threadCount = None
    threadIndex = None
    nodeNum = None
    def __init__(self, threadCount, threadIndex, nodeNum):
        self.threadCount = threadCount
        self.threadIndex = threadIndex
        self.nodeNum = nodeNum

class GraphGen_ZhaoSun(object):

    labelSet = []
    randomArray = np.random.rand(1,multiprocessing.cpu_count())
    print(randomArray)
    usedAlphabet = []

    nodeCount = None
    avgDegree = None
    edgeCount = None

    p1 = 0.4
    p2 = 0.15
    p3 = 0.2
    p4 = 0.25

    def __init__(self, nodeCount, avgDegree, labelCount):
        self.nodeCount = nodeCount
        self.avgDegree = avgDegree
        self.edgeCount = nodeCount * avgDegree
        for i in range(0, labelCount):
            self.labelSet.append(str(i))
        self.BuildRandomNumber()

    def BuildRandomNumber(self):
        rd = random.randint(4, multiprocessing.cpu_count() + 4)
        return rd

    def CreateEdgeThreadProc(self, par):
        p = EdgeCreationThreadObject(par.threadCount, par.threadIndex)
        start = None
        end = None
        if (multiprocessing.cpu_count() - 1 == p.threadIndex):
            start = 0
            end = self.edgeCount / (p.threadCount) + self.edgeCount % (p.threadCount)
        else:
            start = 0
            end = self.edgeCount / p.threadCount
        times = math.log(self.nodeCount, 2)
        for i in range(start, end):
            x1 = 0
            x2 = 0
            y1 = self.nodeCount
            y2 = self.nodeCount
            probability = None
            for timesIndex in range(0, times):
                probability =

gg = GraphGen_ZhaoSun(5,5,5)
print(gg.BuildRandomNumber())