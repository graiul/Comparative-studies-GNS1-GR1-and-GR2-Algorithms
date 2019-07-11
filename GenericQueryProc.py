#Clasa abstracta pentru algoritmul lui Ullmann. Contine metoda de backtracking numita subGraphSearch

from abc import ABCMeta, abstractmethod


class GenericQueryProc(object):
#https://docs.python.org/3/library/abc.html

    #Atribute private ale clasei abstracte:
    # M = [] #Multime isomorfism
    queryGraph = [] # Query graph
    dataGraph = [] # Data graph
    C = [] # Multime noduri - candidat
    Cr = [] # Multime noduri - candidat; refined.

#https://www.protechtraining.com/bookshelf/python_fundamentals_tutorial/oop?ncr=1
#oop-5-abc.py.
    __metaclass__ = ABCMeta
    #Metode:
    @abstractmethod
    def __init__(self, query_graph, data_graph):
        pass
        # for u in self.q:
        #     self.C[u].append(self.filterCandidates(self.q, self.g, self.u))
        #     if self.C is None:
        #         return
        # self.subGraphSearch(self.q, self.g, self.M)

    @abstractmethod
    def subGraphSearch(self, q, g, M):
        pass
        # if len(self.M) is len(self.q): #Conditia de oprire pentru backtracking
        #     return self.M
        # else:
        #     u = self.nextQueryVertex()
        #     Cr = self.refineCandidates(self.M, u, self.C)
        #     for v in Cr:
        #         if self.isJoinable(self.q, self.g, self.M, u, v):
        #             self.updateState(self.M, u, v)
        #             self.subGraphSearch(self.q, self.g, self.M)
        #             self.restoreState(self.M, u, v)
    @abstractmethod
    def filterCandidates(self, q, g, u):
        pass

    @abstractmethod
    def nextQueryVertex(self, query_graph, M): #Returneaza PE RAND nodurile asa cum au fost primite la input. Pe rand?!
        pass

    @abstractmethod
    def refineCandidates(self, M, query_node, query_node_candidates):
        pass

    @abstractmethod
    def isJoinable(self, query_graph, data_graph, M, u, v):
        pass

    @abstractmethod
    def updateState(self, M, u, v):
        pass

    @abstractmethod
    def restoreState(self, M, u, v):
        pass

# class UllmannAlgorithm(GenericQueryProc):
#
#     def subGraphSearch(self):
#         super(UllmannAlgorithm, self).subGraphSearch()
#
#     def filterCandidates(self, q, g, u):
#         self.q = q
#         self.g = g
#         filteredDataGraphVertices = {} #Cheile sunt etichetele nodurilor, iar valorile sunt obiecte de tip Vertex.
#         return filteredDataGraphVertices
#
#     def nextQueryVertex(self):
#         pass
#
#     def refineCandidates(self):
#         pass