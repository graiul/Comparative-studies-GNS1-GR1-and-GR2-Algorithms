# # EXERCITIUL 3 de la Exercitii_Dask_Distributed, aici adaptat la lucrul cu grafuri - un producator si mai multi consumatori,
# iar fiecare consumator este producator la randul lui si lucreaza cu material doar de la consumatorul precedent lyui.

# # https://stonesoupprogramming.com/2017/09/11/python-multiprocessing-producer-consumer-pattern/
# # https://docs.dask.org/en/latest/futures.html?highlight=queue#queues


############################ Din GNS1_Backtracking_STwig_Matching_with_txt_file_printing ##########################################################
import copy


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
############################ Din GNS1_Backtracking_STwig_Matching_with_txt_file_printing ##########################################################


from dask.distributed import Client, LocalCluster, Queue, Variable
import os
# Producer function that places data on the Queue
# Va produce noduri data cu label-ul radacinii din graful query STwig.
def producer(queue_of_the_producer, query_stwig_1_dict, data_graph_edges, node_attributes_dictionary):
    query_stwig = list(query_stwig_1_dict.items())
    # print(query_stwig)
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

############################ Din GNS1_Backtracking_STwig_Matching_with_txt_file_printing ##########################################################
    for node in list(dataGraph.nodes()):
        if query_stwig_root_node_label == dataGraph.nodes[node]['label']:
            # print(type([node]))

            queue_of_the_producer.put([node])
############################ Din GNS1_Backtracking_STwig_Matching_with_txt_file_printing ##########################################################

    queue_of_the_producer.put(['STOP'])
    # print(list(queue_of_the_producer.get()))


    # print("\nQueue of producer results: ")
    # aux = copy.deepcopy(queue_of_the_producer)
    # print(aux.get(batch=True)) # docs.dask.org/en/latest/futures.html?highlight=queue#distributed.Queue.get
                                 # batch=True ia toate elementele din queue, lasand queue goala.

# The consumer function takes data off of the Queue
def consumer(input_queue, output_queue, query_stwig_leaf_node_label, query_stwig_length, data_graph_edges, node_attributes_dictionary, queue_for_printing):
    print("\nStarting consumer " + str(os.getpid()))

    dataGraph = nx.Graph()
    dataGraph.add_edges_from(data_graph_edges)
    nx.set_node_attributes(dataGraph, node_attributes_dictionary, 'label')

    partial_solution = list(input_queue.get())
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
                        print("Consumer " + str(os.getpid()) + ": Partial solution: " + str(partial_solution))
                        queue_for_printing.put(partial_solution)

                        if partial_solution == [3842, 9997, 9670]:
                            print("!!!")
                            root_node = 'STOP'

                        # VARIANTA 1:
                        # Verificator de iteratii sau contor al gasirilor. Daca o solutie partiala se gaseste o data in lista
                        # si e construita inca o data alg se incheie.

                        # VARIANTA 2:
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

    # if len(query_stwig) == query_stwig_length:
        # f = open("file_Parallel_Backtracking_Algorithm_with_STwig_query_graphs_OUTPUT.txt", "w+")
        # while queue_for_printing.qsize() > 0:
        #     p = queue_for_printing.get()
        #     f.write(str(p) + "\n")
        # f.close()


# Pentru ca un consumator sa preia nume noi de la consumatorul precedent treb folosita o bucla infinita care sa
# caute intr-o coada si sa prelucreze in continuare. Acea coada va trebui sa fie:
# - IMPLEMENTAT: coada consumatorului precedent in care se pun nume produse de cons respectiv
# - NU A FOST NEVOIE: SAU o coada comuna in care se pun nume finalizate, ia prin finalizate ma refer ca au fost prelucrate l rand de consumatorii precedenti
# - IMPLEMENTAT: cazul primului consumator care preia nume proaspat produse de producator.
# - IMPLEMENTAT crearea unei bucle infinite care preia material pana la intalnirea unui semnal de oprire.
# - NU A FOST NEVOIE: Pentru acest lucru e nevoie de mult mai mult material in coada initiala de nume.
if __name__ == '__main__': # https://github.com/dask/distributed/issues/2422
                           # https://github.com/dask/distributed/pull/2462
    # Client() foloseste un LocalCluster format din procese.
    # client = Client() # ASA E PARALEL, PT CA LUCREAZA CU PROCESE, NU CU THREADURI.
                           # Daca ar fi fost nbconverted, nu ar fi fost nevoie de "if name==main".
                           # Acest lucru nu e mentionat in documentatia dask pentru LocalCluster, care e generat de Client().

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
    partial_solutions = Queue()
    queue_for_printing = Queue()

############################ Din GNS1_Backtracking_STwig_Matching_with_txt_file_printing ##########################################################
    # Aici cream un obiect graf query:
    query_graph_gen = Query_Graph_Generator()
    query_graph = query_graph_gen.gen_RI_query_graph()
    query_stwig_1 = list(query_graph.nodes())
    # print("Query STwig: " + str(query_stwig_1))
    # Label-ul radacinii
    # root_label = dataGraph.node[query_stwig_1[0]]['label']
    root_label = query_graph.nodes[query_stwig_1[0]]['label']
    # Label-urile vecinilor din lista
    neighbor_labels = []
    for n in query_stwig_1[1:]:
       # neighbor_labels.append(dataGraph.node[n]['label'])
       neighbor_labels.append(query_graph.nodes[n]['label'])

    query_stwig_1_as_labels = []
    query_stwig_1_as_labels.append(root_label)
    for nl in neighbor_labels:
       query_stwig_1_as_labels.append(nl)
    # print("query_stwig_1_as_labels: " + str(query_stwig_1_as_labels))
    # print()
    query_stwig_1_as_labels_source = copy.deepcopy(query_stwig_1_as_labels)

    query_stwig_1_dict = OrderedDict(zip(query_stwig_1, query_stwig_1_as_labels_source))
############################ Din GNS1_Backtracking_STwig_Matching_with_txt_file_printing ##########################################################

############################ Din GNS1_Backtracking_STwig_Matching_with_txt_file_printing ##########################################################
    # GRAFUL DATA DIN NEO4J
    # neograph_data = Graph("bolt://127.0.0.1:7690", auth=("neo4j", "changeme")) # Data Graph RI - Cluster Neo4J
    neograph_data = Graph("bolt://127.0.0.1:7687",
                         auth=(
                         "neo4j", "password"))  # Data Graph RI - O singura instanta de Neo4J

    cqlQuery = "MATCH p=(n)-[r:PPI]->(m) return n.node_id, m.node_id"
    result = neograph_data.run(cqlQuery).to_ndarray()
    edge_list = result.tolist()
    # # print("edge_list: ")
    # # print(edge_list)
    edge_list_integer_ids = []
    for string_edge in edge_list:
       edge_list_integer_ids.append([int(i) for i in string_edge])
    # # print("edge_list_integer_ids: ")
    # # print(edge_list_integer_ids)

    dataGraph = nx.Graph()
    dataGraph.add_edges_from(sorted(edge_list_integer_ids))
    cqlQuery2 = "MATCH (n) return n.node_id, n.node_label"
    result2 = neograph_data.run(cqlQuery2).to_ndarray()
    # # print("result2: ")
    # # print(result2)
    node_ids_as_integers_with_string_labels = []
    for node in result2:
       # # print(node[0])
       node_ids_as_integers_with_string_labels.append([int(node[0]), node[1]])
    # # print("node_ids_as_integers_with_string_labels: ")
    # # print(node_ids_as_integers_with_string_labels)

    node_attr_dict = OrderedDict(sorted(node_ids_as_integers_with_string_labels))
    nx.set_node_attributes(dataGraph, node_attr_dict, 'label')
############################ Din GNS1_Backtracking_STwig_Matching_with_txt_file_printing ##########################################################

    query_stwig = list(query_stwig_1_dict.items())
    print(query_stwig)
    data_graph_edges = copy.deepcopy(sorted(edge_list_integer_ids))
    node_attributes_dictionary = OrderedDict(sorted(node_ids_as_integers_with_string_labels))

    query_stwig_root_node = query_stwig[0]
    query_stwig_root_node_label = query_stwig[0][1]
    query_stwig_length = len(query_stwig) # Pentru grafuri STwig, e nr nodurilor. Pentru grafuri care nu au forma STwig, va fi nr muchiilor, adica al perechilor de noduri,
                                          # datorita faptului ca am pus o muchie pe cate o pozitie al solutiei partiale in cazul respectiv.

    start_time = timer()
    # Prin metoda submit() se da de lucru Pool-ului de procese create de LocalCluster, iar numarul de procese este cel dat prin metoda scale() dupa instantierea LocalCluster-ului.
    a = client.submit(producer, queue_of_the_producer, query_stwig_1_dict, data_graph_edges, node_attributes_dictionary) # Producer-ul creaza coada cu nume.
    # print(a.result())
    # print(queue_of_the_producer.get(batch=True))

    query_stwig_leaf_node1 = query_stwig[1]
    query_stwig_leaf_node_label1 = query_stwig[1][1]
    b = client.submit(consumer, queue_of_the_producer, queue_of_finished_products_1, query_stwig_leaf_node_label1, query_stwig_length, data_graph_edges, node_attributes_dictionary, queue_for_printing)
    # print(b.result())

    query_stwig_leaf_node2 = query_stwig[2]
    query_stwig_leaf_node_label2 = query_stwig[2][1]
    c = client.submit(consumer, queue_of_finished_products_1, queue_of_finished_products_2, query_stwig_leaf_node_label2, query_stwig_length, data_graph_edges, node_attributes_dictionary, queue_for_printing)
    print(c.result())

    # query_stwig_leaf_node3 = query_stwig[3]
    # query_stwig_leaf_node_label3 = query_stwig[3][1]
    # d = client.submit(consumer, queue_of_finished_products_2, queue_of_finished_products_3, query_stwig_leaf_node_label3, data_graph_edges, node_attributes_dictionary)
    # print(d.result())

    # e = client.submit(consumer, queue_of_finished_products_3, queue_of_finished_products_4, queue_of_futures)
    # print(e)
    # print(e.result())
    # queue_of_futures.put(e)

    # f = client.submit(consumer, queue_of_finished_products_4, queue_of_finished_products_5, queue_of_futures)
    # print(f.result())

    total_time = timer() - start_time
    print("Total execution time: " + str(total_time))
    f = open("file_Parallel_Backtracking_Algorithm_with_STwig_query_graphs_OUTPUT.txt", "w+")
    while queue_for_printing.qsize() > 0:
        p = queue_for_printing.get()
        for p_elem in p:
            f.write(str(p_elem) + " ")
        f.write("\n")
    f.close()
