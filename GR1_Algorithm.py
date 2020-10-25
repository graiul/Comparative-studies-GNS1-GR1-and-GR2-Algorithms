# # EXERCITIUL 3 de la Exercitii_Dask_Distributed, aici adaptat la lucrul cu grafuri - un producator si mai multi consumatori,
# iar fiecare consumator este producator la randul lui si lucreaza cu material doar de la consumatorul precedent lyui.

# # https://stonesoupprogramming.com/2017/09/11/python-multiprocessing-producer-consumer-pattern/
# # https://docs.dask.org/en/latest/futures.html?highlight=queue#queues


############################ Din GNS1_Backtracking_STwig_Matching_with_txt_file_printing ##########################################################
import copy

# import dask
import networkx as nx
from collections import OrderedDict

# https://stackoverflow.com/questions/6537487/changing-shell-text-color-windows
# https://pypi.org/project/colorama/
from colorama import init
from colorama import Fore, Back, Style

from Query_Graph_Generator import Query_Graph_Generator

init()

# https://stackoverflow.com/questions/4564559/get-exception-description-and-stack-trace-which-caused-an-exception-all-as-a-st
import traceback

from py2neo import Graph, Subgraph

from timeit import default_timer as timer
# import time
############################ Din GNS1_Backtracking_STwig_Matching_with_txt_file_printing ##########################################################


from dask.distributed import Client, LocalCluster, Queue, Variable
import os

class GR1_Algorithm(object):
    # Atributele clasei
    execution_time = None

    def __init__(self, query_graph, data_graph, first_query_node_id_into_search=False, logs_directory=''):
        self.query_graph = query_graph
        self.data_graph = data_graph
        self.first_query_node_id_into_search = first_query_node_id_into_search
        self.logs_directory = logs_directory

    # Producer function that places data on the Queue
    # Va produce noduri data cu label-ul radacinii din graful query STwig.
    def producer(self, queue_of_the_producer, query_stwig, data_graph_edges, node_attributes_dictionary):
    # Signatura urmatoare contine ca si input o lista de parti ale grafului query
    # def producer(queue_of_the_producer, query_parts, query_stwig_1_dict, data_graph_edges, node_attributes_dictionary):
        print("\nStarting producer " + str(os.getpid()))

        # query_stwig = list(query_stwig_1_dict.items())
        print("Query STwig received by the producer: ")
        print(query_stwig)
        # print("The STwig query graf split into parts: ")
        # query_stwig_parts = split_list(query_stwig, wanted_parts=2)
        # for part in query_stwig_parts:
        #     print(part)
        # print("Query STwig PARTS received by the producer: ")
        # for part in query_parts:
        #     print(part)
        query_stwig_root_node = query_stwig[0]
        # print(query_stwig_root_node)
        query_stwig_root_node_id = query_stwig_root_node[0]
        query_stwig_root_node_label = query_stwig_root_node[1]
        # print(query_stwig_root_node_id)
        # print(query_stwig_root_node_label)
        # print()
        dataGraph = nx.Graph()
        dataGraph.add_edges_from(data_graph_edges)
        nx.set_node_attributes(dataGraph, node_attributes_dictionary, 'label')

        if self.first_query_node_id_into_search == False:
        ############################ Din GNS1_Backtracking_STwig_Matching_with_txt_file_printing ##########################################################
            for node in list(dataGraph.nodes()):
                if query_stwig_root_node_label == dataGraph.nodes[node]['label']:
                    # print(node)

                    queue_of_the_producer.put([node])
        ############################ Din GNS1_Backtracking_STwig_Matching_with_txt_file_printing ##########################################################

        # Aici am incercat o filtrare pentru a evita aparitia rezultatelor pentru parti query STwig care
        # nu pot fi cuplate. Am decis sa nu mai folosesc aceasta filtrare.
        else:
            if self.first_query_node_id_into_search == True:
                for node in list(dataGraph.nodes()):
                    if query_stwig_root_node_label == dataGraph.nodes[node]['label'] and query_stwig_root_node_id == node:
                        print(node)

                        queue_of_the_producer.put([node])


        queue_of_the_producer.put(['STOP'])
        # print(list(queue_of_the_producer.get()))


        # print("\nQueue of producer results: ")
        # aux = copy.deepcopy(queue_of_the_producer)
        # print(aux.get(batch=True)) # docs.dask.org/en/latest/futures.html?highlight=queue#distributed.Queue.get
                                     # batch=True ia toate elementele din queue, lasand queue goala.

    # The consumer function takes data off of the Queue
    # @dask.delayed
    def consumer(self, input_queue, output_queue, query_stwig_leaf_node_label, query_stwig_length, data_graph_edges, node_attributes_dictionary, queue_for_printing):
        print("\nStarting consumer " + str(os.getpid()))

        dataGraph = nx.Graph()
        dataGraph.add_edges_from(data_graph_edges)
        nx.set_node_attributes(dataGraph, node_attributes_dictionary, 'label')

        partial_solution = copy.deepcopy(list(input_queue.get()))
        # print(partial_solution)
        root_node = partial_solution[0]

        aux_partial_solutions_list = []

        # # Run indefinitely
        while root_node != 'STOP': # DACA LA WHILE AICI CEILALTI CONSUMATORI NU VOR MAI AVEA MATERIAL, ATUNCI NU VOR FI PUSE IN FOLOSIRE SI CELELALTE PROCESE.
            # Se poate folosi acest procedeu daca lista data de producator este mult mai mare, pentru ca lucreaza foarte repede consumatorii,
            # iar consumatorul care ia din coada nu lasa timp pentru ceilalti.

            # If the queue is empty, queue.get() will block until the queue has data
            # print("Consumer " + str(os.getpid()) + ": Root node: " + str(root_node))
            # print("Consumer " + str(os.getpid()) + ": partial_solution[-1]: " + str(partial_solution[-1]))

            # print("Consumer " + str(os.getpid()) + " got: " + str(partial_solution) + " from the queue of producer products.")
            for data_node in dataGraph.nodes():
                if query_stwig_leaf_node_label == dataGraph.nodes[data_node]['label']:
                    if dataGraph.has_edge(root_node, data_node):

                        # print("Consumer " + str(os.getpid()) + ": Root node: " + str(root_node))

                        partial_solution.append(data_node)

                        if len(partial_solution) == query_stwig_length:
                            # La acest nivel, consumatorul va mai crea o solutie partiala validata care a mai fost creata deja.
                            # Cand acest lucru se intampla, mai jos algoritmul isi va opri executia.
                            # print("Consumer " + str(os.getpid()) + ": Partial solution: " + str(partial_solution))

                            if partial_solution not in aux_partial_solutions_list:
                                queue_for_printing.put(partial_solution)
                                # print("Consumer " + str(os.getpid()) + ": Partial solution: " + str(partial_solution))

                                aux_ps = copy.deepcopy(partial_solution)
                                aux_partial_solutions_list.append(aux_ps)
                                # print(aux_partial_solutions_list)
                            # elif partial_solution in aux_partial_solutions_list:
                                # print("!!!")
                                # root_node = 'STOP'


                            # if partial_solution == [3842, 9997, 9670]:
                            #     print("!!!")
                            #     root_node = 'STOP'

                            # NU A FOST NEVOIE: VARIANTA 1:
                            # Verificator de iteratii sau contor al gasirilor. Daca o solutie partiala se gaseste o data in lista
                            # si e construita inca o data alg se incheie.

                            # NU A FOST NEVOIE: VARIANTA 2:
                            # In loc sa verific daca o solutie se afla deja, mai bine numar de cate ori apare solutia resp inainte de a o adauga in lista.
                            # Nu se poate sa adaug in lista si sa verific existenta sol resp in lista in aceeasi iteratie. Nu are sens.
                            # Fie verific existenta, dar in iteratii diferite, fie numar existenta, da in aceeasi iteratie.

                            # if partial_solution not in aux_partial_solutions_list:
                            #     aux_partial_solutions_list.append(partial_solution)
                            #     queue_for_printing.put(partial_solution)
                            # else:
                            #     if partial_solution in aux_partial_solutions_list:
                            #         print("!!!")
                            #         root_node = 'STOP'
                            #         break

                        output_queue.put(partial_solution)
                        partial_solution.remove(partial_solution[-1])

            # if len(partial_solution) == query_stwig_length:
            #     queue_for_printing.put(partial_solution)
            #     partial_solution = list(input_queue.get())
            # if partial_solution[0] == 'STOP':
            #     # print('STOP')
            #     root_node = 'STOP'
            #     print(root_node)
            #     # break

            # docs.dask.org/en/latest/futures.html?highlight=queue#distributed.Queue.qsize
            if input_queue.qsize() > 0:
                partial_solution = list(input_queue.get())
                root_node = partial_solution[0]
            # print(partial_solution[-1])
            # if len(partial_solution) > 1 and partial_solution[-1] != 'STOP':
            # if len(partial_solution) == 1 and partial_solution[-1] == 'STOP':
            if partial_solution[0] == 'STOP':
                # output_queue.put(['STOP'])
                root_node = 'STOP'
        output_queue.put(['STOP'])

    # FOARTE IMPORTANT! TOATE COMPARARILE CU M SE FAC CU ULTIMA INTRARE, ADICA ULTIMA ASOCIERE. ASTFEL< PE RAND TOATA LISTA VA FI VERIFICATA O SINGURA DATA. DACA REIAU VERIFICAREA CU FIECARE ASOCIERE DIN LISTA
    # DUPA SELECAREA FIECARUI CANDIDAT, VA REZULTA O LISTA GOALA A CANDIDATILOR RAFINATI.
    # DAR, cateodata este nevoie doar de ultima intrare. Pentru o posibila rezolvare, am notat in comentarii deasupra metodei subgraphSearch.
    # def refineCandidates(self, M, query_node, query_node_candidates):
    #     Mq = []  # Set of matched query vertices
    #     Mg = []  # Set of matched data vertices
    #     Cq = []  # Set of adjacent and not-yet-matched query vertices connected from Mq
    #     Cg = []  # Set of adjacent and not-yet-matched data vertices connected from Mg
    #
    #     # Conditia (1): Prune out v belonging to c(u) such that a vertex v is not connected from already matched data vertices.
    #     # query_node = self.nextQueryVertex(query_graph)
    #     # query_node_candidates = self.filterCandidates(query_node, query_graph, data_graph)
    #     # print("------------INCEPUT EXECUTIE RAFINARE CANDIDATI-----------")
    #     # print("QUERY NODE: " + str(query_node))
    #     # print("CANDIDATES: " + str(query_node_candidates))
    #
    #     # print()
    #     # print(M)
    #     if len(M) == 0:
    #         # print("\nNu avem valori pt Mq si Mg pentru ca nu avem o prima asociere inca.")
    #         # print("Astfel, Cq si Cg vor avea toate nodurile din grafurile query, respectiv cel data.")
    #         Cq = list(self.queryGraph.nodes())
    #         Cg = list(self.dataGraph.nodes())
    #
    #     if len(M) > 0:
    #         Mq.append(M[-1][0]) # Ce are a face cu ultima asociere?
    #         Mg.append(M[-1][1]) # Folosesc -1 pentru a returna ultimul element din lista (https://stackoverflow.com/questions/930397/getting-the-last-element-of-a-list-in-python).
    #         # Este necesar ca lista sa nu fie niciodata goala, ceea ce se rezolva foarte bine prin faptul ca lista va fi tot
    #         # timpul initializata cu o asociere.
    #         Cq.append(list(self.adj(M[-1][0], self.queryGraph)))
    #         Cg.append(list(self.adj(M[-1][1], self.dataGraph)))
    #         # print("Mq = " + str(Mq))
    #         # print("Mg = " + str(Mg))
    #         # print("Cq = " + str(Cq))
    #         # print("Cg = " + str(Cg))
    #         # Pentru fiecare candidat verificam conditia (1)
    #
    #     query_nodes_candidates_for_deletion = copy.deepcopy(query_node_candidates)
    #     self.respectare_conditie_1 = False
    #     self.respectare_conditie_2 = False
    #     self.respectare_conditie_3 = False
    #
    #     # Conditia (1): Prune out candidate such that candidate is not connected from already matched data vertices.
    #                     # Prune out candidate such that candidate is connected
    #     # from not matched data vertices.
    #
    #     # print("\n     Conditia(1): ")
    #     for candidate in query_node_candidates:
    #         # print("\nCandidatul selectat: " + str(candidate))
    #         # print("     Conditia(1):")
    #         # for matching in M:
    #         # last_matching = M[-1]
    #         # print("     Matching (trebuie verificat pentru fiecare matching / asociere): " + str(matching))
    #         # print("M: " + str(M))
    #         # print(candidate)
    #
    #         delete_indicator = False
    #         occurence_list = []
    #
    #         if len(M) == 0:
    #             # Cateva detalii despre prima iteratie a rularii:
    #             # print("Inca nu avem nici un matching, deci nu putem verifica 'such that candidate is not connected from already matched data vertices' ")
    #             # print("Dar verificam daca exista muchie intre nodul candidat si celelalte noduri data. Facem acest lucru pentru a verifica si urmatoarele doua conditii.")
    #             # print(
    #             #     "Pentru ca nu avem inca asocieri in lista M, nu avem Mq si Mg. De aceea nu putem verifica Conditia(2) sau Conditia(3) pentru ca are nevoie de aceleasi doua liste Mq si Mg.")
    #             # print(
    #             #     "Conform p133han pentru rularea algoritmului este nevoie deja de o asociere existenta in lista M.")
    #             # print(
    #             #     "Din articolul p133han, http://www.vldb.org/pvldb/vol6/p133-han.pdf, sectiunea 3.3 VF2 Algorithm, explicatii pentru metoda NextQueryVertex: ")
    #             # print(
    #             #     "NextQueryVertex: Unlike Ullmann, VF2 starts with the first vertex and selects a vertex connected from the already matched query vertices. Note that the original VF2 algorithm does not define any order in which query vertices are selected.")
    #             # print("'already matched query vertices.'")
    #             # print("Deci avem nevoie de un matching la inceputul executarii algoritmului.")
    #             # print(
    #             #     "Astfel returnam candidatii cu care putem face asocierea primului nod al grafului query. Cu alte cuvinte, radacinile-candidat.")
    #
    #             return query_node_candidates
    #
    #         if len(M) > 0:
    #
    #             for data_node in self.dataGraph.nodes():
    #                 # print("Nod data selectat pentru verificare: " + str(data_node))
    #                 # Daca nodul data selectat a mai fost folosit
    #                 if self.dataGraph.nodes[data_node]['matched'] == True:
    #                     # print("Nodul " + str(data_node) + " este deja marcat ca fiind 'matched' ")
    #                     # Atunci verificam sa nu fie adiacent lui
    #                     # print("Lipseste in graful data muchia " + str([candidate, data_node]) + " ?")
    #                     if self.dataGraph.has_edge(data_node, candidate) == False:
    #                         if candidate in query_nodes_candidates_for_deletion:
    #                             delete_indicator = True
    #                             # print("Lipseste.")
    #                             occurence_list.append("Lipseste")
    #
    #                     else:
    #                         delete_indicator = False
    #                         # print("Exista.")
    #                         # print("Edge " + str([data_node, candidate]) + " exists.")
    #                         occurence_list.append("Exista")
    #                             # print("Nu exista muchie. Eliminam candidatul conform Conditiei 1.")
    #                             # print("Muchia care nu exista: " + str([candidate, data_node]))
    #                             # query_nodes_candidates_for_deletion.remove(candidate)
    #                             # self.respectare_conditie_1 = False
    #                             # break
    #             # # A DOUA VARIANTA VECHE: foloseste lista M inversata.
    #             # for matching in reversed(M):
    #             #     print("Candidate: " + str(candidate))
    #             #     print("Refinement: " + str(matching))
    #             #     # # PRIMA VARIANTA VECHE: cautarea in lista M care contine elementele in ordinea inserarii.
    #             #     # if self.data_graph.has_edge(candidate, matching[1]) is False:
    #             #     #     # print("         Conditia(1) intra in vigoare, astfel avem:")
    #             #     #     # print("         *Nu exista muchie intre " + str(candidate) + " si " + str(matching[1]) + ". Se va sterge candidatul " + str(candidate) + ".")
    #             #     #     # print("         *Nu se mai verifica pentru Conditia(2), ci verificam Conditia(2) pentru candidatii care au trecut.")
    #             #     #     for neighbor in self.data_graph.neighbors(matching[1]):
    #             #     #         if neighbor is matching[1]:
    #             #     #             if self.data_graph.has_edge(candidate, neighbor) is True:
    #             #     #                 print("Has edge. Trece regula 1.\n")
    #             #     #                 self.respectare_conditie_1 = True
    #             #     #                 break
    #             #     # else:
    #             #     #     break
    #             #
    #             #     if self.data_graph.has_edge(candidate, matching[1]) is False:
    #             #         if candidate in query_nodes_candidates_for_deletion:
    #             #             query_nodes_candidates_for_deletion.remove(candidate) # Am putut sa fac remove unui element din lista direct in bucla foreach. NU SE FAC STERGERI DIN LISTA IN ACELASI TIMP CU ITERAREA!
    #             #             self.respectare_conditie_1 = False
    #
    #         # print(occurence_list)
    #         # exit(0)
    #
    #         if len(occurence_list) == 0:
    #             return query_node_candidates
    #
    #         if len(occurence_list) == 1:
    #             if occurence_list[0] == "Lipseste":
    #                 # print("Nu exista muchie. Eliminam candidatul conform Conditiei 1.")
    #                 # print("Muchia care nu exista: " + str([candidate, data_node]))
    #                 query_nodes_candidates_for_deletion.remove(candidate)
    #                 self.respectare_conditie_1 = False
    #
    #         if len(occurence_list) == 1:
    #             if occurence_list[0] == "Exista":
    #                 # print("Exista muchia. Trece Conditia (1).")
    #                 # print()
    #                 self.respectare_conditie_1 = True
    #
    #
    #         if len(occurence_list) > 1:
    #             if occurence_list[-1] == "Lipseste":
    #                 if occurence_list[-2] == "Lipseste":
    #                     # print("Nu exista muchie. Eliminam candidatul conform Conditiei 1.")
    #                     # print("Muchia care nu exista: " + str([candidate, data_node]))
    #                     query_nodes_candidates_for_deletion.remove(candidate)
    #                     self.respectare_conditie_1 = False
    #
    #                 if occurence_list[-2] == "Exista":
    #                     # print("Exista muchia. Trece Conditia (1).")
    #                     # print()
    #                     self.respectare_conditie_1 = True
    #
    #             if occurence_list[-1] == "Exista":
    #                 # print("Exista muchia. Trece Conditia (1).")
    #                 # print()
    #                 self.respectare_conditie_1 = True
    #             # if occurence_list.count("Exista") > occurence_list.count("Lipseste"):
    #             #     print("Exista muchia. Trece Conditia (1).")
    #             #     print()
    #             #     self.respectare_conditie_1 = True
    #             # if occurence_list.count("Exista") < occurence_list.count("Lipseste"):
    #             #     if candidate in query_nodes_candidates_for_deletion:
    #             #
    #             #         print("Nu exista muchie. Eliminam candidatul conform Conditiei 1.")
    #             #         print("Muchia care nu exista: " + str([candidate, data_node]))
    #             #         query_nodes_candidates_for_deletion.remove(candidate)
    #             #         self.respectare_conditie_1 = False
    #
    #         # print("         Candidatii lui " + str(query_node) + " dupa Conditia(1)")# + " actualizati in functie de conditia (1) al VF2: ")
    #         # print("         " + str(query_nodes_candidates_for_deletion))
    #         # print()
    #
    #         # Pentru fiecare candidat trebuie verificata si Conditia (2): Prune out any vertex v in c(u) such that |Cq intersected with adj(u)| > |Cg intersected with adj(v)|
    #         if self.respectare_conditie_1:
    #             # print("     Conditia(2):")
    #
    #             first_intersection = []
    #             adjQueryNode = list(self.adj(query_node, self.queryGraph)) # Retin candidatii in ordine lexicografic crescatoare.
    #             for xx in adjQueryNode:
    #                 for yy in Cq[-1]: # Aici e lista in lista.
    #                     if xx == yy:
    #                         first_intersection.append(xx)
    #             second_intersection = []
    #             adjCandidate = list(self.adj(candidate, self.dataGraph))
    #             for xx in adjCandidate:
    #                 for yy in Cg[-1]:
    #                     if xx == yy:
    #                         second_intersection.append(xx)
    #             # print("         Facut intersectiile de la Conditia (2)")
    #             # print("         " + str(len(first_intersection)))
    #             # print("         " + str(len(second_intersection)))
    #             # print("For breakpoint.")
    #             # print("Cardinalul primei intersectii > decat celei de a doua?")
    #             if len(first_intersection) > len(second_intersection):
    #                 # print("         Conditia(2) intra in vigoare, astfel avem:")
    #                 # print("         Cardinalul primei intersectii este mai mare decat cea de-a doua. Se va sterge candidatul " + str(candidate) + ".")
    #                 if candidate in query_nodes_candidates_for_deletion:
    #                     query_nodes_candidates_for_deletion.remove(candidate)
    #                     # print("         Candidatii lui " + str(query_node))
    #                     # print("         " + str(query_nodes_candidates_for_deletion))
    #                     # print()
    #                     self.respectare_conditie_2 = False
    #             else:
    #                 # print("         Nu. Trece Conditia (2).")
    #                 # print()
    #                 self.respectare_conditie_2 = True
    #
    #             # print("         Candidatii lui " + str(query_node) + " dupa Conditia (2):")
    #             # print("         " + str(query_nodes_candidates_for_deletion))
    #             # print()
    #             if self.respectare_conditie_2 is True:
    #                 # print("     Conditia(3):")
    #
    #                 for cq_elem in Cq:
    #                     for cq_elem_node in cq_elem:
    #                         if cq_elem_node in adjQueryNode:
    #                             adjQueryNode.remove(cq_elem_node)
    #                 for mq_elem_node in Mq:
    #                     if mq_elem_node in adjQueryNode:
    #                         adjQueryNode.remove(mq_elem_node)
    #
    #                 for cg_elem in Cg:
    #                     for cg_elem_node in cg_elem:
    #                         if cg_elem_node in adjCandidate:
    #                             adjCandidate.remove(cg_elem_node)
    #                 for mg_elem_node in Mg:
    #                     if mg_elem_node in adjCandidate:
    #                         adjCandidate.remove(mg_elem_node)
    #
    #                 # print("Este primul cardinal mai mare decat al doilea?")
    #                 if len(adjQueryNode) > len(adjCandidate):
    #                     # print("         Facut intersectiile si scaderile de la c3")
    #                     # print("         " + str(len(adjQueryNode)))
    #                     # print("         " + str(len(adjCandidate)))
    #                     # print("         Conditia(3) intra in vigoare, astfel avem:")
    #                     # print("         *Cardinalul primei intersectii cu scaderi este mai mare decat cea de-a doua. Se va sterge candidatul " + str(candidate) + ".")
    #                     if candidate in query_nodes_candidates_for_deletion:
    #                         query_nodes_candidates_for_deletion.remove(candidate)
    #                         self.respectare_conditie_3 = False
    #                         # print("         Candidatii lui " + str(query_node))
    #                         # print("         " + str(query_nodes_candidates_for_deletion))
    #                         # print()
    #                         # self.respectare_conditie_2 = False
    #                 else:
    #                     self.respectare_conditie_3 = True
    #                     # print("         Nu. Candidatul " + str(candidate) + " a trecut de toate cele 3 filtre / conditii.")
    #                 # print("         Candidatii finali ai lui " + str(query_node))
    #                 # print("         " + str(query_nodes_candidates_for_deletion))
    #                 # print()
    #     if len(query_nodes_candidates_for_deletion) == 0:
    #         return None
    #     # VECHI: Conditia 1 am adaptat-o pe loc mai sus.
    #     # Mai jos se afla si Conditia 2 si 3 functionale, dar fara blocari(trecerea la candidatul urmator) daca un candidat nu a trecut de o conditie, si fara verificari daca exista candidatul care trebuie eliminat.
    #     # De asemenea, nu folosesc o copie din care voi fi facut eliminarea de candidati, avand astfel un rezultat eronat.
    #     # print()
    #     # # for candidate in query_node_candidates:
    #     # # |Cq intersected with adj(u)| > |Cg intersected with adj(v)|
    #     # # print("Prima intersectie din conditia (2): ")
    #     # first_intersection = []
    #     # # print("adj(queryNode):")
    #     # adjQueryNode = sorted(list(self.adj(query_node, self.query_graph))) # Retin candidatii in ordine lexicografic crescatoare.
    #     # # print(adjQueryNode)
    #     # # print("Cq: ")
    #     # # print(Cq)
    #     # for xx in adjQueryNode:
    #     #     for yy in Cq[-1]:
    #     #         if xx == yy:
    #     #             first_intersection.append(xx)
    #     #
    #     # # print("A doua intersectie din conditia (2): ")
    #     # second_intersection = []
    #     # # print("adj(candidate):")
    #     # adjCandidate = sorted(list(self.adj(candidate, self.data_graph)))
    #     # # print(adjCandidate)
    #     # # print("Cg: ")
    #     # # print(Cg)
    #     #
    #     # for xx in adjCandidate:
    #     #     for yy in Cg[-1]:
    #     #         if xx == yy:
    #     #             second_intersection.append(xx)
    #     # # print("|Cq intersected with adj(u)| > |Cg intersected with adj(v)| ?")
    #     # # print(str(len(first_intersection)) + " > " + str(len(second_intersection)) + " ?")
    #     # if len(first_intersection) > len(second_intersection):
    #     #     print("     Se va sterge candidatul " + str(candidate) + ".")
    #     #     if candidate in query_node_candidates:
    #     #         query_node_candidates.remove(candidate)
    #     # print()
    #     #
    #     # print("Candidatii lui u2 actualizati in functie de conditia (1) si (2) al VF2: ")
    #     # print(query_node_candidates)
    #
    #     # # Pentru fiecare candidat verificam si Conditia(3): prune out any vertex v in C(u) such that |adj(u) \ Cq \Mq| > |adj(v) \ Cg \Mg|
    #     # print()
    #     # print("Conditia(3): ")
    #     # # for candidate in query_node_candidates:
    #     # # print("|adj(u) \ Cq \Mq|:")
    #     # # print("adjQueryNode = " + str(adjQueryNode))
    #     # # print("Cq = " + str(Cq))
    #     # # print("Mq = " + str(Mq))
    #     # # print(type(adjQueryNode))
    #     # for cq_elem in Cq:
    #     #     for cq_elem_node in cq_elem:
    #     #         if cq_elem_node in adjQueryNode:
    #     #             adjQueryNode.remove(cq_elem_node)
    #     # for mq_elem_node in Mq:
    #     #     if mq_elem_node in adjQueryNode:
    #     #         adjQueryNode.remove(mq_elem_node)
    #     # # print("adjQueryNode = " + str(adjQueryNode))
    #     # # print("len(adjQueryNode) = " + str(len(adjQueryNode)))
    #     #
    #     # # print()
    #     # # print("|adj(v) \ Cg \Mg|:")
    #     # # print("adjCandidate = " + str(adjCandidate))
    #     # # print("Cg = " + str(Cg))
    #     # # print("Mg = " + str(Mg))
    #     # # print(type(adjCandidate))
    #     # for cg_elem in Cg:
    #     #     for cg_elem_node in cg_elem:
    #     #         if cg_elem_node in adjCandidate:
    #     #             adjCandidate.remove(cg_elem_node)
    #     # for mg_elem_node in Mg:
    #     #     if mg_elem_node in adjCandidate:
    #     #         adjCandidate.remove(mg_elem_node)
    #     # # print("adjCandidate = " + str(adjCandidate))
    #     # # print("len(adjCandidate) = " + str(len(adjCandidate)))
    #     # # print("|adj(u) \ Cq \Mq| > |adj(v) \ Cg \Mg| ?")
    #     # if len(adjQueryNode) > len(adjCandidate):
    #     #     if candidate in query_node_candidates:
    #     #         query_node_candidates.remove(candidate) # De pus si conditii in cazul in care nodul respectiv nu mai exista, daca a fost eliminat deja de una din primele doua conditii.
    #     # # print("Candidatii lui u2 actualizati in functie de conditia (1) si (2) al VF2: ")
    #     # # print(query_node_candidates)
    #     # print("---------------------\n")
    #     # print("------------SFARSIT EXECUTIE RAFINARE CANDIDATI-----------")
    #     return query_nodes_candidates_for_deletion
    #
    #     # Adaug in M o noua asociere. Voi alege doar primul candidat din lista de candidati care au ramas dupa regulile de refinement.
    #     # self.M.append([query_node, query_node_candidates[0]])


    # Pentru ca un consumator sa preia nume noi de la consumatorul precedent treb folosita o bucla infinita care sa
    # caute intr-o coada si sa prelucreze in continuare. Acea coada va trebui sa fie:
    # - IMPLEMENTAT: coada consumatorului precedent in care se pun nume produse de cons respectiv
    # - NU A FOST NEVOIE: SAU o coada comuna in care se pun nume finalizate, ia prin finalizate ma refer ca au fost prelucrate l rand de consumatorii precedenti
    # - IMPLEMENTAT: cazul primului consumator care preia nume proaspat produse de producator.
    # - IMPLEMENTAT crearea unei bucle infinite care preia material pana la intalnirea unui semnal de oprire.
    # - NU A FOST NEVOIE: Pentru acest lucru e nevoie de mult mai mult material in coada initiala de nume.
    # if __name__ == '__main__': # https://github.com/dask/distributed/issues/2422
                               # https://github.com/dask/distributed/pull/2462
        # Client() foloseste un LocalCluster format din procese.
        # client = Client() # ASA E PARALEL, PT CA LUCREAZA CU PROCESE, NU CU THREADURI.
                               # Daca ar fi fost nbconverted, nu ar fi fost nevoie de "if name==main".
                               # Acest lucru nu e mentionat in documentatia dask pentru LocalCluster, care e generat de Client().
    def execute_gr1_algorithm(self):
        # Am creat un LocalCluster cu 5 workers, adica 5 procese, acesta avand rolul de Pool din  pachetul py multiprocessing.
        lc = LocalCluster()
        lc.scale(10)
        client = Client(lc)
        # https://docs.dask.org/en/latest/futures.html#distributed.Client.scheduler_info
        # Am ales sa afisez pe cate o linie fiecare informatie din dictionarl returnat de Client.scheduler_info().
        # La item-ul 'workers se afla un subdictionar cu informatii despre procesele din LocalCluster/Pool, la campul 'id'.
        # for item in client.scheduler_info().items():
        #     print(item)

        q1 = Queue()
        q2 = Queue()
        queue_of_futures = Queue()
        # docs.dask.org/en/latest/futures.html?highlight=queue#distributed.Queue.qsize
        dataGraph_node_list_with_labels = Variable()
        dataGraph_distrib_var = Variable()

        # Lucrul cu cozi in loc de stive simplifica lucrul cand vine vorba de preluarea de catre consumatori al materialelor.
        # Acest lucru deoarece ei preiau de la primul element pus in coada, ceea ce inseamna ca noile elemente produse vor fi adaugate la
        # sfarsitul cozii. Astfel nu mai apar probleme ca si la stive , unde ar fi fost preluat tot timpul ultimele elemente adaugate.
        # Pe scurt, e mai usoara crearea unui model tip banda rulanta folosind cozi.
        queue_of_the_producer = Queue()
        queue_of_finished_products_1 = Queue()
        queue_of_finished_products_2 = Queue()
        queue_of_finished_products_3 = Queue()
        queue_of_finished_products_4 = Queue()
        queue_of_finished_products_5 = Queue()
        queue_of_finished_products_6 = Queue()
        queue_of_finished_products_7 = Queue()
        partial_solutions = Queue()
        queue_for_printing = Queue()

    # ############################ Din GNS1_Backtracking_STwig_Matching_with_txt_file_printing ##########################################################
    #     # Aici cream un obiect graf query:
    #     query_graph_gen = Query_Graph_Generator()
    #     query_graph = query_graph_gen.gen_RI_query_graph()
    #     query_stwig_1 = list(query_graph.nodes())
    #     # print("Query STwig: " + str(query_stwig_1))
    #     # Label-ul radacinii
    #     # root_label = dataGraph.node[query_stwig_1[0]]['label']
    #     root_label = query_graph.nodes[query_stwig_1[0]]['label']
    #     # Label-urile vecinilor din lista
    #     neighbor_labels = []
    #     for n in query_stwig_1[1:]:
    #        # neighbor_labels.append(dataGraph.node[n]['label'])
    #        neighbor_labels.append(query_graph.nodes[n]['label'])
    #
    #     query_stwig_1_as_labels = []
    #     query_stwig_1_as_labels.append(root_label)
    #     for nl in neighbor_labels:
    #        query_stwig_1_as_labels.append(nl)
    #     # print("query_stwig_1_as_labels: " + str(query_stwig_1_as_labels))
    #     # print()
    #     query_stwig_1_as_labels_source = copy.deepcopy(query_stwig_1_as_labels)
    #
    #     query_stwig_1_dict = OrderedDict(zip(query_stwig_1, query_stwig_1_as_labels_source))
    # ############################ Din GNS1_Backtracking_STwig_Matching_with_txt_file_printing ##########################################################
    #
    # ############################ Din GNS1_Backtracking_STwig_Matching_with_txt_file_printing ##########################################################
    #     # GRAFUL DATA DIN NEO4J
    #     # neograph_data = Graph("bolt://127.0.0.1:7690", auth=("neo4j", "changeme")) # Data Graph RI - Cluster Neo4J
    #     neograph_data = Graph("bolt://127.0.0.1:7687",
    #                          auth=(
    #                          "neo4j", "password"))  # Data Graph RI - O singura instanta de Neo4J
    #
    #     cqlQuery = "MATCH p=(n)-[r:PPI]->(m) return n.node_id, m.node_id"
    #     result = neograph_data.run(cqlQuery).to_ndarray()
    #     edge_list = result.tolist()
    #     # # print("edge_list: ")
    #     # # print(edge_list)
    #     edge_list_integer_ids = []
    #     for string_edge in edge_list:
    #        edge_list_integer_ids.append([int(i) for i in string_edge])
    #     # # print("edge_list_integer_ids: ")
    #     # # print(edge_list_integer_ids)
    #
    #     dataGraph = nx.Graph()
    #     dataGraph.add_edges_from(sorted(edge_list_integer_ids))
    #     cqlQuery2 = "MATCH (n) return n.node_id, n.node_label"
    #     result2 = neograph_data.run(cqlQuery2).to_ndarray()
    #     # # print("result2: ")
    #     # # print(result2)
    #     node_ids_as_integers_with_string_labels = []
    #     for node in result2:
    #        # # print(node[0])
    #        node_ids_as_integers_with_string_labels.append([int(node[0]), node[1]])
    #     # # print("node_ids_as_integers_with_string_labels: ")
    #     # # print(node_ids_as_integers_with_string_labels)
    #
    #     node_attr_dict = OrderedDict(sorted(node_ids_as_integers_with_string_labels))
    #     nx.set_node_attributes(dataGraph, node_attr_dict, 'label')
    # ############################ Din GNS1_Backtracking_STwig_Matching_with_txt_file_printing ##########################################################

        # query_stwig = list(query_stwig_1_dict.items())
        # print(query_stwig)
        # data_graph_edges = copy.deepcopy(sorted(edge_list_integer_ids))
        # node_attributes_dictionary = OrderedDict(sorted(node_ids_as_integers_with_string_labels))

        query_stwig_root_node = self.query_graph[0]
        query_stwig_root_node_label = self.query_graph[0][1]
        query_stwig_length = len(self.query_graph) # Pentru grafuri STwig, e nr nodurilor. Pentru grafuri care nu au forma STwig, va fi nr muchiilor, adica al perechilor de noduri,
                                              # datorita faptului ca am pus o muchie pe cate o pozitie al solutiei partiale in cazul respectiv.

        # parts = split_list(query_stwig, wanted_parts=2)
        # print("Query graph parts: ")
        # for part in parts:
        #     print(part)
        # # print(query_stwig_1_as_labels)
        # l_parts = split_list(query_stwig_1_as_labels, wanted_parts=2)
        # print("\nQuery graph edges with labels, having ID's inserted at the beginning of each edge:")
        # print(l_parts)
        # aux = (None, l_parts[0][0])
        # del l_parts[0][0]
        # del l_parts[1][0]
        # l_parts[0].insert(0, aux)
        # l_parts[1].insert(0, parts[1][0])
        # print(l_parts)

        start_time = timer()
        # start_time = time.clock()
        # print()
        # print("A INCEPUT CRONOMETRAREA")
        # print()

        # distributed.dask.org/en/latest/locality.html
        # futures = client.scatter(data_graph_edges, workers=None, broadcast=False)
        futures = client.scatter(self.data_graph[0], workers=None, broadcast=False)


        # Prin metoda submit() se da de lucru Pool-ului de procese create de LocalCluster, iar numarul de procese este cel dat prin metoda scale() dupa instantierea LocalCluster-ului.
        # big_producer = client.scatter(data_graph_edges)

        # a = client.submit(self.producer, queue_of_the_producer, query_stwig_1_dict, data_graph_edges, node_attributes_dictionary)  # Producer-ul creaza coada cu nume.
        a = client.submit(self.producer, queue_of_the_producer, self.query_graph, self.data_graph[0], self.data_graph[1])  # Producer-ul creaza coada cu nume.

        # Urmatorul rand contine crearea unui producer folosind signatura ce contine o lista de parti ale grafului query
        # a = client.submit(producer, queue_of_the_producer, l_parts, query_stwig_1_dict, data_graph_edges, node_attributes_dictionary) # Producer-ul creaza coada cu nume.

        # print(a.result())
        # print(queue_of_the_producer.get(batch=True))
        # exit(0)

        number_of_consumers = len(self.query_graph) - 1
        # simplifiedpython.net/python-switch-case-statement/
        if number_of_consumers == 1:
            query_stwig_leaf_node1 = self.query_graph[1]
            query_stwig_leaf_node_label1 = self.query_graph[1][1]
            # big_consumer_1 = client.scatter(data_graph_edges)
            # b = client.submit(consumer, big_consumer_1, queue_of_the_producer, queue_of_finished_products_1, query_stwig_leaf_node_label1, query_stwig_length, data_graph_edges, node_attributes_dictionary, queue_for_printing)

            # b = client.submit(consumer, queue_of_the_producer, queue_of_finished_products_1, query_stwig_leaf_node_label1, query_stwig_length, data_graph_edges, node_attributes_dictionary, queue_for_printing)
            b = client.submit(self.consumer, queue_of_the_producer, queue_of_finished_products_1,
                              query_stwig_leaf_node_label1, query_stwig_length, self.data_graph[0], self.data_graph[1],
                              queue_for_printing)

            print(b.result())
        elif number_of_consumers == 2:
            query_stwig_leaf_node1 = self.query_graph[1]
            query_stwig_leaf_node_label1 = self.query_graph[1][1]
            # big_consumer_1 = client.scatter(data_graph_edges)
            # b = client.submit(consumer, big_consumer_1, queue_of_the_producer, queue_of_finished_products_1, query_stwig_leaf_node_label1, query_stwig_length, data_graph_edges, node_attributes_dictionary, queue_for_printing)

            # b = client.submit(consumer, queue_of_the_producer, queue_of_finished_products_1, query_stwig_leaf_node_label1, query_stwig_length, data_graph_edges, node_attributes_dictionary, queue_for_printing)
            b = client.submit(self.consumer, queue_of_the_producer, queue_of_finished_products_1,
                              query_stwig_leaf_node_label1, query_stwig_length, self.data_graph[0], self.data_graph[1],
                              queue_for_printing)

            query_stwig_leaf_node2 = self.query_graph[2]
            query_stwig_leaf_node_label2 = self.query_graph[2][1]
            # big_consumer_2 = client.scatter(data_graph_edges)
            # c = client.submit(consumer, big_consumer_2, queue_of_finished_products_1, queue_of_finished_products_2, query_stwig_leaf_node_label2, query_stwig_length, data_graph_edges, node_attributes_dictionary, queue_for_printing)

            # c = client.submit(consumer, queue_of_finished_products_1, queue_of_finished_products_2, query_stwig_leaf_node_label2, query_stwig_length, data_graph_edges, node_attributes_dictionary, queue_for_printing)
            c = client.submit(self.consumer, queue_of_finished_products_1, queue_of_finished_products_2,
                              query_stwig_leaf_node_label2, query_stwig_length, self.data_graph[0], self.data_graph[1],
                              queue_for_printing)
            c.result()

        elif number_of_consumers == 3:
            query_stwig_leaf_node1 = self.query_graph[1]
            query_stwig_leaf_node_label1 = self.query_graph[1][1]
            # big_consumer_1 = client.scatter(data_graph_edges)
            # b = client.submit(consumer, big_consumer_1, queue_of_the_producer, queue_of_finished_products_1, query_stwig_leaf_node_label1, query_stwig_length, data_graph_edges, node_attributes_dictionary, queue_for_printing)

            # b = client.submit(consumer, queue_of_the_producer, queue_of_finished_products_1, query_stwig_leaf_node_label1, query_stwig_length, data_graph_edges, node_attributes_dictionary, queue_for_printing)
            b = client.submit(self.consumer, queue_of_the_producer, queue_of_finished_products_1,
                              query_stwig_leaf_node_label1, query_stwig_length, self.data_graph[0], self.data_graph[1],
                              queue_for_printing)

            query_stwig_leaf_node2 = self.query_graph[2]
            query_stwig_leaf_node_label2 = self.query_graph[2][1]
            # big_consumer_2 = client.scatter(data_graph_edges)
            # c = client.submit(consumer, big_consumer_2, queue_of_finished_products_1, queue_of_finished_products_2, query_stwig_leaf_node_label2, query_stwig_length, data_graph_edges, node_attributes_dictionary, queue_for_printing)

            # c = client.submit(consumer, queue_of_finished_products_1, queue_of_finished_products_2, query_stwig_leaf_node_label2, query_stwig_length, data_graph_edges, node_attributes_dictionary, queue_for_printing)
            c = client.submit(self.consumer, queue_of_finished_products_1, queue_of_finished_products_2,
                              query_stwig_leaf_node_label2, query_stwig_length, self.data_graph[0], self.data_graph[1],
                              queue_for_printing)

            query_stwig_leaf_node3 = self.query_graph[3]
            query_stwig_leaf_node_label3 = self.query_graph[3][1]
            # big_consumer_3 = client.scatter(data_graph_edges)
            # d = client.submit(consumer, big_consumer_3, queue_of_finished_products_2, queue_of_finished_products_3, query_stwig_leaf_node_label3, query_stwig_length, data_graph_edges, node_attributes_dictionary, queue_for_printing)
            d = client.submit(self.consumer, queue_of_finished_products_2, queue_of_finished_products_3, query_stwig_leaf_node_label3, query_stwig_length, self.data_graph[0], self.data_graph[1], queue_for_printing)
            d.result()

        elif number_of_consumers == 4:
            query_stwig_leaf_node1 = self.query_graph[1]
            query_stwig_leaf_node_label1 = self.query_graph[1][1]
            # big_consumer_1 = client.scatter(data_graph_edges)
            # b = client.submit(consumer, big_consumer_1, queue_of_the_producer, queue_of_finished_products_1, query_stwig_leaf_node_label1, query_stwig_length, data_graph_edges, node_attributes_dictionary, queue_for_printing)

            # b = client.submit(consumer, queue_of_the_producer, queue_of_finished_products_1, query_stwig_leaf_node_label1, query_stwig_length, data_graph_edges, node_attributes_dictionary, queue_for_printing)
            b = client.submit(self.consumer, queue_of_the_producer, queue_of_finished_products_1,
                              query_stwig_leaf_node_label1, query_stwig_length, self.data_graph[0], self.data_graph[1],
                              queue_for_printing)

            query_stwig_leaf_node2 = self.query_graph[2]
            query_stwig_leaf_node_label2 = self.query_graph[2][1]
            # big_consumer_2 = client.scatter(data_graph_edges)
            # c = client.submit(consumer, big_consumer_2, queue_of_finished_products_1, queue_of_finished_products_2, query_stwig_leaf_node_label2, query_stwig_length, data_graph_edges, node_attributes_dictionary, queue_for_printing)

            # c = client.submit(consumer, queue_of_finished_products_1, queue_of_finished_products_2, query_stwig_leaf_node_label2, query_stwig_length, data_graph_edges, node_attributes_dictionary, queue_for_printing)
            c = client.submit(self.consumer, queue_of_finished_products_1, queue_of_finished_products_2,
                              query_stwig_leaf_node_label2, query_stwig_length, self.data_graph[0], self.data_graph[1],
                              queue_for_printing)

            query_stwig_leaf_node3 = self.query_graph[3]
            query_stwig_leaf_node_label3 = self.query_graph[3][1]
            # big_consumer_3 = client.scatter(data_graph_edges)
            # d = client.submit(consumer, big_consumer_3, queue_of_finished_products_2, queue_of_finished_products_3, query_stwig_leaf_node_label3, query_stwig_length, data_graph_edges, node_attributes_dictionary, queue_for_printing)
            d = client.submit(self.consumer, queue_of_finished_products_2, queue_of_finished_products_3, query_stwig_leaf_node_label3, query_stwig_length, self.data_graph[0], self.data_graph[1], queue_for_printing)

            query_stwig_leaf_node4 = self.query_graph[4]
            query_stwig_leaf_node_label4 = self.query_graph[4][1]
            # big_consumer_4 = client.scatter(data_graph_edges)
            # e = client.submit(consumer, big_consumer_4, queue_of_finished_products_3, queue_of_finished_products_4, query_stwig_leaf_node_label4, query_stwig_length, data_graph_edges, node_attributes_dictionary, queue_for_printing)
            e = client.submit(self.consumer, queue_of_finished_products_3, queue_of_finished_products_4, query_stwig_leaf_node_label4, query_stwig_length, self.data_graph[0], self.data_graph[1], queue_for_printing)
            # print(e)
            # print(e.result())
            # queue_of_futures.put(e)
            e.result()

        elif number_of_consumers == 5:
            query_stwig_leaf_node1 = self.query_graph[1]
            query_stwig_leaf_node_label1 = self.query_graph[1][1]
            # big_consumer_1 = client.scatter(data_graph_edges)
            # b = client.submit(consumer, big_consumer_1, queue_of_the_producer, queue_of_finished_products_1, query_stwig_leaf_node_label1, query_stwig_length, data_graph_edges, node_attributes_dictionary, queue_for_printing)

            # b = client.submit(consumer, queue_of_the_producer, queue_of_finished_products_1, query_stwig_leaf_node_label1, query_stwig_length, data_graph_edges, node_attributes_dictionary, queue_for_printing)
            b = client.submit(self.consumer, queue_of_the_producer, queue_of_finished_products_1,
                              query_stwig_leaf_node_label1, query_stwig_length, self.data_graph[0], self.data_graph[1],
                              queue_for_printing)

            query_stwig_leaf_node2 = self.query_graph[2]
            query_stwig_leaf_node_label2 = self.query_graph[2][1]
            # big_consumer_2 = client.scatter(data_graph_edges)
            # c = client.submit(consumer, big_consumer_2, queue_of_finished_products_1, queue_of_finished_products_2, query_stwig_leaf_node_label2, query_stwig_length, data_graph_edges, node_attributes_dictionary, queue_for_printing)

            # c = client.submit(consumer, queue_of_finished_products_1, queue_of_finished_products_2, query_stwig_leaf_node_label2, query_stwig_length, data_graph_edges, node_attributes_dictionary, queue_for_printing)
            c = client.submit(self.consumer, queue_of_finished_products_1, queue_of_finished_products_2,
                              query_stwig_leaf_node_label2, query_stwig_length, self.data_graph[0], self.data_graph[1],
                              queue_for_printing)

            query_stwig_leaf_node3 = self.query_graph[3]
            query_stwig_leaf_node_label3 = self.query_graph[3][1]
            # big_consumer_3 = client.scatter(data_graph_edges)
            # d = client.submit(consumer, big_consumer_3, queue_of_finished_products_2, queue_of_finished_products_3, query_stwig_leaf_node_label3, query_stwig_length, data_graph_edges, node_attributes_dictionary, queue_for_printing)
            d = client.submit(self.consumer, queue_of_finished_products_2, queue_of_finished_products_3, query_stwig_leaf_node_label3, query_stwig_length, self.data_graph[0], self.data_graph[1], queue_for_printing)

            query_stwig_leaf_node4 = self.query_graph[4]
            query_stwig_leaf_node_label4 = self.query_graph[4][1]
            # big_consumer_4 = client.scatter(data_graph_edges)
            # e = client.submit(consumer, big_consumer_4, queue_of_finished_products_3, queue_of_finished_products_4, query_stwig_leaf_node_label4, query_stwig_length, data_graph_edges, node_attributes_dictionary, queue_for_printing)
            e = client.submit(self.consumer, queue_of_finished_products_3, queue_of_finished_products_4, query_stwig_leaf_node_label4, query_stwig_length, self.data_graph[0], self.data_graph[1], queue_for_printing)
            # print(e)
            # print(e.result())
            # queue_of_futures.put(e)

            query_stwig_leaf_node5 = self.query_graph[5]
            query_stwig_leaf_node_label5 = self.query_graph[5][1]
            f = client.submit(self.consumer, queue_of_finished_products_4, queue_of_finished_products_5, query_stwig_leaf_node_label5, query_stwig_length, self.data_graph[0], self.data_graph[1], queue_for_printing)
            f.result()

        else:
            print("Not enough consumer processes.")


        # query_stwig_leaf_node1 = self.query_graph[1]
        # query_stwig_leaf_node_label1 = self.query_graph[1][1]
        # # big_consumer_1 = client.scatter(data_graph_edges)
        # # b = client.submit(consumer, big_consumer_1, queue_of_the_producer, queue_of_finished_products_1, query_stwig_leaf_node_label1, query_stwig_length, data_graph_edges, node_attributes_dictionary, queue_for_printing)
        #
        # # b = client.submit(consumer, queue_of_the_producer, queue_of_finished_products_1, query_stwig_leaf_node_label1, query_stwig_length, data_graph_edges, node_attributes_dictionary, queue_for_printing)
        # b = client.submit(self.consumer, queue_of_the_producer, queue_of_finished_products_1, query_stwig_leaf_node_label1, query_stwig_length, self.data_graph[0], self.data_graph[1], queue_for_printing)
        #
        # # print(b.result())
        #
        # query_stwig_leaf_node2 = self.query_graph[2]
        # query_stwig_leaf_node_label2 = self.query_graph[2][1]
        # # big_consumer_2 = client.scatter(data_graph_edges)
        # # c = client.submit(consumer, big_consumer_2, queue_of_finished_products_1, queue_of_finished_products_2, query_stwig_leaf_node_label2, query_stwig_length, data_graph_edges, node_attributes_dictionary, queue_for_printing)
        #
        # # c = client.submit(consumer, queue_of_finished_products_1, queue_of_finished_products_2, query_stwig_leaf_node_label2, query_stwig_length, data_graph_edges, node_attributes_dictionary, queue_for_printing)
        # c = client.submit(self.consumer, queue_of_finished_products_1, queue_of_finished_products_2, query_stwig_leaf_node_label2, query_stwig_length, self.data_graph[0], self.data_graph[1], queue_for_printing)
        #
        # c.result()
        #
        # query_stwig_leaf_node3 = self.query_graph[3]
        # query_stwig_leaf_node_label3 = self.query_graph[3][1]
        # # big_consumer_3 = client.scatter(data_graph_edges)
        # # d = client.submit(consumer, big_consumer_3, queue_of_finished_products_2, queue_of_finished_products_3, query_stwig_leaf_node_label3, query_stwig_length, data_graph_edges, node_attributes_dictionary, queue_for_printing)
        # d = client.submit(self.consumer, queue_of_finished_products_2, queue_of_finished_products_3, query_stwig_leaf_node_label3, query_stwig_length, self.data_graph[0], self.data_graph[1], queue_for_printing)
        # d.result()

        # query_stwig_leaf_node4 = query_stwig[4]
        # query_stwig_leaf_node_label4 = query_stwig[4][1]
        # # big_consumer_4 = client.scatter(data_graph_edges)
        # # e = client.submit(consumer, big_consumer_4, queue_of_finished_products_3, queue_of_finished_products_4, query_stwig_leaf_node_label4, query_stwig_length, data_graph_edges, node_attributes_dictionary, queue_for_printing)
        # e = client.submit(consumer, queue_of_finished_products_3, queue_of_finished_products_4, query_stwig_leaf_node_label4, query_stwig_length, data_graph_edges, node_attributes_dictionary, queue_for_printing)
        # # print(e)
        # # print(e.result())
        # # queue_of_futures.put(e)
        # e.result()
        #
        #
        # query_stwig_leaf_node5 = query_stwig[5]
        # query_stwig_leaf_node_label5 = query_stwig[5][1]
        # f = client.submit(consumer, queue_of_finished_products_4, queue_of_finished_products_5, query_stwig_leaf_node_label5, query_stwig_length, data_graph_edges, node_attributes_dictionary, queue_for_printing)
        # # f.result()
        #
        # query_stwig_leaf_node6 = query_stwig[6]
        # query_stwig_leaf_node_label6 = query_stwig[6][1]
        # g = client.submit(consumer, queue_of_finished_products_5, queue_of_finished_products_6, query_stwig_leaf_node_label6, query_stwig_length, data_graph_edges, node_attributes_dictionary, queue_for_printing)
        # # g.result()
        #
        # query_stwig_leaf_node7 = query_stwig[7]
        # query_stwig_leaf_node_label7 = query_stwig[7][1]
        # h = client.submit(consumer, queue_of_finished_products_6, queue_of_finished_products_7, query_stwig_leaf_node_label7, query_stwig_length, data_graph_edges, node_attributes_dictionary, queue_for_printing)
        # # h.result()

        total_time = timer() - start_time
        # total_time = time.clock() - start_time
        print("Total execution time: " + str(total_time) + " seconds.")

        # stackoverflow.com/questions/11700593/creating-files-and-directories-via-python
        import os
        if not os.path.exists(self.logs_directory):
            os.makedirs(self.logs_directory)

        # stackoverflow.com/questions/8024248/telling-python-to-save-a-txt-file-to-a-certain-directory-on-windows-and-mac
        save_path = self.logs_directory
        name_of_file = "file_GR1_Algorithm_execution_times"
        completeName = os.path.join(save_path, name_of_file+".txt")

        # f_time = open(self.logs_directory + "\\file_GR1_Algorithm_with_STwig_query_graphs_execution_times.txt", "a")
        f_time = open(completeName, "a")
        f_time.write(str(total_time) + " ")
        f_time.write("\n")
        f_time.close()
        self.execution_time = total_time

        # f = open(self.logs_directory + "\\file_GR1_Algorithm_with_STwig_query_graphs_OUTPUT.txt", "w+")
        name_of_file_2 = "file_GR1_Algorithm_output"
        complete_name_2 = os.path.join(save_path, name_of_file_2+".txt")
        f_output = open(complete_name_2, "w+")
        while queue_for_printing.qsize() > 0:
            p = queue_for_printing.get()
            for p_elem in p:
                f_output.write(str(p_elem) + " ")
            f_output.write("\n")
        f_output.close()

        name_of_file_3 = "query_graph"
        complete_name_3 = os.path.join(save_path, name_of_file_3+".txt")
        f_query_graph_used = open(complete_name_3, "w+")
        f_query_graph_used.write(str(self.query_graph))
        f_query_graph_used.close()

    def get_execution_time_gr1_algorithm(self):
        return self.execution_time