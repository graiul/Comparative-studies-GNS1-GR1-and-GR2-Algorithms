import threading
from concurrent.futures.thread import ThreadPoolExecutor
from multiprocessing.dummy import Pool as ThreadPool

from py2neo import Graph, Node, Relationship
import networkx as nx
import copy
import numpy
import operator
import itertools
from timeit import default_timer as timer

class neo4j_test_2(object):

    # neograph_data = Graph(port="7687", user="neo4j", password="graph") # Data Graph Zhaosun
    neograph_data = Graph("bolt://127.0.0.1:7693", auth=("neo4j", "changeme")) # Data Graph Zhaosun din READ_REPLICA
    # neograph_query = Graph("bolt://127.0.0.1:7693", auth=("neo4j", "changeme")) # Query Graph Zhaosun din READ_REPLICA


    def Cloud_Load(self, node_id):  # Pot rula inca o metoda?
        # print("Cloud_Load:")
        # Pentru Zhaosun Data Graph din cluster neo4j:
        biglist = []
        # print("     id=" + str(node_id))
        cqlQuery = "MATCH (n) WHERE n.zhaosun_id = '" + str(node_id) + "' RETURN n"
        # print(cqlQuery)
        result = self.neograph_data.run(cqlQuery).to_ndarray()
        # print(result)
        nodes_loaded = []
        nodes_loaded.append(result)
        cqlQuery2 = "MATCH(n{zhaosun_id: '" + str(node_id) + "'})--(m) return m"
        # MATCH(n{zhaosun_id: 'a1'})--(m) return m
        # print(cqlQuery2)
        result2 = list(self.neograph_data.run(cqlQuery2).to_ndarray())
        # print(result2)
        nodes_loaded.append(result2)
        biglist.append(nodes_loaded)

        # VARIANTA CORECTA VECINATATE DE ORDINUL 1 AL UNUI NOD: MATCH(n{RI_id: 1})--(m) return m
        # print("Vecinatate, primul elem root=")
        # for b in biglist:
        #     for bb in b:
        #         print(bb)
        #     print("---")
        # print("End Cloud_Load")
        return biglist

    def Index_getID(self, label):
        # tx = self.neograph_data.begin()
        # cqlQuery = "MATCH (n:`" + str(label) + "`) RETURN n.RI_id"
        cqlQuery = "MATCH (n) WHERE n.zhaosun_label='" + str(label) + "' RETURN n.zhaosun_id" # IF a IN a1! Graf Zhaosun
        # result = tx.run(cqlQuery).to_ndarray()
        result = self.neograph_data.run(cqlQuery).to_ndarray()
        nodes_loaded = []
        for r in result:
            nodes_loaded.append(r[0])
        return nodes_loaded

    # def Index_hasLabel(self, RI_id, label):
    def Index_hasLabel(self, node_id, label):
        # print("Index_hasLabel:")
        # print("Node ID: " + str(node_id))
        # print("Label: " + str(label))
        cqlQuery = "MATCH (n) WHERE n.zhaosun_label='" + str(label) + "' AND n.zhaosun_id='" + str(node_id) + "' RETURN n"
        # MATCH (n) WHERE n.zhaosun_label='a' AND n.zhaosun_id='a1' RETURN n
        # print(cqlQuery)
        result = self.neograph_data.run(cqlQuery).to_ndarray()
        # print("Index_hasLabel query result= ")
        # print(list(result))
        if len(list(result)) > 0:
            # print("End Index_hasLabel")
            return True
        else:
            # print("End Index_hasLabel")
            return False

    def MatchSTwig(self, q): # q 1 = (a,{b,c}) din articol, [a, [b,c]] in py. Acest q1 (STwig din query graph)si altele vor fi date de STwigOrderSelection care lucreaza cu graful query.
        print("IF QUERY STWIG IS UNDIRECTED, THEN MULTIPLE RESULTS ARE GIVEN "
              "\nBECAUSE WE USE LABELS NOT NODE ID's WHICH ENCOMPASS MULTIPLE NODES")
        print("IF QUERY STWIG WOULD BE DIRECTED, THEN THE RESULTS "
              "\n- THE DATA GRAPH STWIGS - SHOULD BE AT MOST EXACTLY THE ONES FROM THE QUERY")
        print("SO, IT WOULD BE SIMPLY A MATTER OF SEARCHING A QUERY STWIG IN DATA GRAPH, BEING RETURNED A SINGLE DATA STWIG."
              "\nTHE PROBLEM WOULD SIMPLY BE IF THE QUERY STWIG GIVEN IS FOUND IN THE DATA GRAPH."
              "\nBUT FOR THE EXAMPLE IN THE ARTICLE THEY HAD A SINGLE UNDIRECTED QUERY STWIG BE SEARCHED IN AN UNDIRECTED GRAPH."
              "\nTHIS MEANS THAT EACH UNDIRECTED QUERY HAS *MULTIPLE* CORRESPONDING DATA GRAPH STWIGS."
              "\nTHUS, WE WOULD NEED TO CHOOSE EACH DATA STWIG AS TO BE ADJACENT TO SOME OTHER DATA GRAPH STWIGS "
              "\nIN ORDER TO OBTAIN AS A RESULT THE WHOLE QUERY GRAPH."
              "\nTHIS IS MASSIVELY SIMPLIFIED IF THE GRAPHS ARE DIRECTED, SINCE ONE "
              "\nQUERY GRAPH STWIG SHOULD ONLY HAVE RETURNED FROM MatchSTwig ONLY ONE DATA GRAPH STWIG!")
        print("STwig from zhaosun undirected query graph, STwig is undirected (Figure 4b from original article): " + str(q))
        start_time = timer()
        # print("MatchSTwig: ")
        # print("STwig query: " + str(q))
        r = str(q[0]) # Root node label
        L = [q[1][0], q[1][1]] # Root children labels
        # print("Root node label: " + str(r))
        # print("Root children labels: " + str(L))

        #  (1) Find the set of root nodes by calling Index.getID(r);
        Sr = self.Index_getID(r)
        print("Set of root nodes for label " + str(r) + ": " + str(Sr))
        R = []
        Sli = []

        # (2) Foreach root node, find its child nodes using Cloud.Load();
        for root_node in Sr:
            # print("---Root node: " + str(root_node))
            c = self.Cloud_Load(root_node)
            # print("     Children for selected root, first elem is selected root: " + str(c))
            # root = c[0][0]
            children = c[0][1]
            # print("root=" + str(root))
            # print("children=" + str(children))

            # (3) Find its child nodes that match the labels in L by calling Index.hasLabel()
            S = []
            S_child_lists = []
            for root_child_label in L:
                # print("     Root_child_label: " + str(root_child_label))
                # print("     " + str(type(root_child_label)))
                for child in children:
                    if child not in S_child_lists:
                        # print("     child= " + str(child)) # Child, sau vecinii de ordinul 1.
                        aux = str(child).split("id: '")[1]
                        child_id = str(aux).split("',")[0]
                        # print("     child_id= " + str(child_id))
                        # aux2 = str(child).split(" {")[0]
                        # child_label = str(aux2.split(":")[1])
                        # print("     child_label= " + child_label)
                        has_label = self.Index_hasLabel(child_id, root_child_label)
                        # print(has_label)
                        if has_label:
                            # S[S.index(li)] = child
                            S_child_lists.append(child_id)
                # print("S[li]= " + str(S[S.index(li)]))
                # print("     S_child_lists= " + str(S_child_lists))
                S.append(S_child_lists) # Sli, lista de children, pentru fiecare li care respecta conditia, adaugam in S
                S_child_lists = []
            # print("     Sets of children(for selected root " + str(root_node) + ") with labels  " + str(L) + ": ")
            S_one_elems = []
            for s in S:
                # print("     " + str(s))
                for s_temp in s:
                    S_one_elems.append(s_temp)
            S_one_elems.insert(0, root_node)
            # print("Cartesian product: ")
            combinations = list(itertools.combinations(S_one_elems, 3))
            elem_labels = []
            elem_labels_total = []
            for elem in combinations:
                for el in elem:
                    elem_labels.append(el[0])
                elem_labels_total.append(elem_labels)
                elem_labels = []
            combinations_dict = dict(zip(combinations, elem_labels_total))
            combinations_dict_final = copy.deepcopy(combinations_dict)
            # vals = list(combinations_dict.values())[0]
            for val in combinations_dict.items():
                # print(val[1])
                for lb in val[1]:
                    # print(lb)
                    if val[1].count(lb) > 1:
                        # print("More than once ^")
                        combinations_dict_final.pop(val[0])
                        break
            for stwig in combinations_dict_final.keys():
                # print(stwig)
                R.append(stwig)
        # print("STWIGS: ")
        STwigs = sorted(R)
        # for stwig in STwigs:
        #     print(stwig)
        # Am schimbat graful astfel: am inlaturat muchia a3,b3: MATCH (n:a)-[r:RELTYPE]-(m:b) WHERE n.id = 'a3' AND m.id = 'b3' DELETE r
        #                            am adaugat muchia a3,c3: # MATCH (n:a),(m:c) WHERE n.id = 'a3' AND m.id = 'c3' CREATE (n)-[r:RELTYPE]->(m)
        # Astfel am obtinur rezultatele din p788_Zhaosun, pag 5, G(q1) = ...
        # print("End MatchSTwig")
        total_time_sec = timer() - start_time
        total_time_millis = total_time_sec * 1000

        print("\nMatchSTwig exec time -> sec: " + str(total_time_sec))
        print("\nMatchSTwig exec time -> millis: " + str(total_time_millis))

        return STwigs

    def Query_Graph_Split(self, query_graph):

        splits = []
        for node in query_graph.nodes():
            print("Selected node: " + str(node))
            edges = list(query_graph.edges(node))

            # if len(edges) == 2:
            #     splits.append([node, edges])

            # for stop in range(2, len(edges)+1):
            #     splits.append([node, edges[0:stop]])

            print(edges)
            splits.append([edges[0][0], edges])
        print()
        return splits
        # print(splits)

    # def Query_Graph_Split_Parallel(self, nodes_chunk):
    #
    #     splits = []
    #     for node in nodes_chunk:
    #         print("Selected node: " + str(node))
    #         edges = list(query_graph.edges(node))
    #         # if len(edges) == 2:
    #         #     splits.append([node, edges])
    #         print(edges)
    #         for stop in range(2, len(edges)+1):
    #             splits.append([node, edges[0:stop]])
    #     print("Splits: ")
    #     print(splits)

    def f_value(self, v_id, query_graph):
        deg = len(list(query_graph.neighbors(v_id)))
        # print("deg: " + str(deg))
        # print("neighbors: " + str(list(query_graph.neighbors(v))))
        # print(query_graph.node[v_id]['label'])
        return deg / self.freq(query_graph.node[v_id]['label'])

    def freq(self, v_label):
        # tx = self.neograph_data.begin() # Pentru graful data Zhaosun!

        # cqlQuery = "MATCH (n:`" + str(v_label) + "`) RETURN n"
        cqlQuery = "MATCH (n) WHERE n.zhaosun_label='" + str(v_label) + "' return n"
        # result = tx.run(cqlQuery).to_ndarray()
        result = self.neograph_data.run(cqlQuery)
        return len(list(result))

    def get_neo4j_stwig_root(self, Cloud_Load_Resulting_STIWGS):
        # print("get_neo4j_stwig_root: ")
        # print("STwig: " + str(Cloud_Load_Resulting_STIWGS))
        aux = str(Cloud_Load_Resulting_STIWGS).split("id: '")[1]
        root_trimmed = str(aux).split("',")[0]
        # print("root_trimmed: " + str(root_trimmed))
        # print("End get_neo4j_stwig_root")
        return root_trimmed

    def get_neo4j_stwig_node_trim(self, stwig_node_to_trim):
        # print("STwig node to trim: " + str(stwig_node_to_trim))
        aux = str(stwig_node_to_trim).split("id: '")[1]
        node_trimmed = str(aux).split("',")[0]
        return node_trimmed

    def get_neo4j_STwig_with_root(self, root, stwig): # Transforma un STwig din modul de reprezentare Neo4j in lista: [a, [b,c]]
        # print("get_neo4j_STwig_with_root: ")
        # print("root: " + str(root))
        # print("stwig: " + str(stwig[0][1]))
        trimmed_nodes = []
        for node_to_trim in stwig[0][1]:
            trimmed_nodes.append(self.get_neo4j_stwig_node_trim(node_to_trim))
        # print("Root: " + str(root))
        # trimmed_root = self.get_neo4j_stwig_node_trim(root)
        # print("Trimmed root: " + trimmed_root)
        trimmed_nodes.insert(0, root)
        # print("End get_neo4j_STwig_with_root")
        return trimmed_nodes

    def neighbors_of_node(self, node):
        # print("neighbors_of_node execution:")
        Cloud_Load_Resulting_STIWG = self.Cloud_Load(node)[0][1]
        # print(Cloud_Load_Resulting_STIWG)
        return Cloud_Load_Resulting_STIWG

    def degree_of_node(self, node):
        neighbors = self.neighbors_of_node(node)
        deg = len(neighbors)
        return deg

    def STwig_Order_Selection(self, query_graph):
        S = []
        T = []
        dict_f_values_query_graph = {}
        picked_edge = None
        while len(query_graph.edges()) > 0:
            sum_start_time = timer()

            for edge in query_graph.edges():
                sum = self.f_value(edge[0], query_graph) + self.f_value(edge[1], query_graph)
                print("Sum: " + str(sum))
                dict_f_values_query_graph[edge] = sum

            sum_total_time_sec = timer() - sum_start_time
            sum_total_time_millis = sum_total_time_sec * 1000

            print("\nSum exec time -> sec: " + str(sum_total_time_sec))
            print("Sum exec time -> millis: " + str(sum_total_time_millis))
            print()

            if len(S) == 0:
                # print(dict_f_values_query_graph.items())
                index, value = max(enumerate(list(dict_f_values_query_graph.values())), key=operator.itemgetter(1))
                # print("Max val: " + str(value))
                # print("Max val index: " + str(index))
                picked_edge = list(dict_f_values_query_graph.keys())[index]
                print("Picked edge: " + str(picked_edge))



            # TREBUIE SA SCADA DEGREE, TREBUIE INLATURATI VECINII PUSI IN S DIN VECINII NODULUI SELECTAT.
            # else:
            #     index2, value2 = max(enumerate(list(dict_f_values_query_graph.values())), key=operator.itemgetter(1))
            #     for edge in query_graph.edges():
            #         sum2 = self.f_value(edge[0], query_graph) + self.f_value(edge[1], query_graph)
            #         if edge[0] in S and sum2 == value2:
            #             picked_edge = edge
            #             print("Picked edge on 'else' branch: " + str(picked_edge))
            #             break


            print("Working on picked_edge[0] = " + str(picked_edge[0]))
            Cloud_Load_Resulting_STIWG = self.Cloud_Load(picked_edge[0])
            # print("Cloud_Load_Resulting_STIWG: " + str(Cloud_Load_Resulting_STIWG))
            q_root = self.get_neo4j_stwig_root(Cloud_Load_Resulting_STIWG) # DE FACUT TRIM SI LA SF!
            Tv = self.get_neo4j_STwig_with_root(q_root, Cloud_Load_Resulting_STIWG)
            print("     STWIG formatted also having the root at first elem; Tv = " + str(Tv))
            T.append(Tv)
            # Neighbors of v
            neighbors = self.Cloud_Load(picked_edge[0])
            print("     Neighbors of picked_edge[0] = " + str(picked_edge[0]) + ": ")
            for n in neighbors[0][1]:
                print("     " + str(self.get_neo4j_stwig_node_trim(n)))
                S.append(self.get_neo4j_stwig_node_trim(n))
                # Acum, vecinul adaugat in S ar trebui eliminat din multimea vecinilor nodului ales.
                # Astfel, degree-ul scade, iar algoritmul se incheie.


            print("     S: " + str(S))
            Tv_edges = []
            root = Tv[0]
            # print("Root: " + root)
            Tv.remove(root)
            for tv_elem in Tv:
                Tv_edges.append([root, tv_elem])
            print("     Edges in Tv: " + str(Tv_edges))
            print("     Query graph edges: " + str(query_graph.edges()))
            print("     Comparing of edges and removal: ")
            print("     Nr of edges to be removed: " + str(len(Tv_edges)))
            print("     Nr of edges total: " + str(len(query_graph.edges())))
            query_graph_edges = list(query_graph.edges())
            print("     Edges found that will be removed: ")
            for tv_edge in Tv_edges:
                for query_edge in query_graph.edges():
                    # print(set(tv_edge))
                    # print(set(query_edge))
                    # print("-----------")
                    if set(tv_edge) == set(query_edge):
                        print("     tv_edge == query_edge: " + str(tv_edge))
                        try:
                            query_graph_edges.remove(tuple(tv_edge))
                        except:
                            try:
                                query_graph_edges.remove(tuple(tv_edge[::-1]))
                            except:
                                continue
            print("     List of edges after removal: " + str(query_graph_edges))
            print("     Nr of edges total after removal: " + str(len(query_graph_edges)))

            print("\nWorking on picked_edge[1] = " + str(picked_edge[1]))
            print("     Deg of node u, picked_edge[1]: " + str(self.degree_of_node(picked_edge[1])))
            if self.degree_of_node(picked_edge[1]) > 0:
                Cloud_Load_Resulting_STIWG = self.Cloud_Load(picked_edge[1])
                q_root = self.get_neo4j_stwig_root(Cloud_Load_Resulting_STIWG)
                Tu = self.get_neo4j_STwig_with_root(q_root, Cloud_Load_Resulting_STIWG)
                print("     STWIG formatted also having the root at first elem; Tu: " + str(Tu))
                T.append(Tu)

                Tu_edges = []
                root = Tu[0]
                Tu.remove(root)
                for tu_elem in Tu:
                    Tu_edges.append([root, tu_elem])
                print("     Edges in Tu: " + str(Tu_edges))
                print("     Query graph edges: " + str(query_graph.edges()))
                print("     Comparing of edges and removal: ")
                print("     Nr of edges to be removed: " + str(len(Tu_edges)))
                print("     Nr of edges total: " + str(len(query_graph.edges())))
                for tu_edge in Tu_edges:
                    for query_edge in query_graph.edges():
                        # print(set(tu_edge))
                        # print(set(query_edge))
                        # print("-----------")
                        if set(tu_edge) == set(query_edge):
                            print(tu_edge)
                            try:
                                query_graph_edges.remove(tu_edge)
                            except:
                                try:
                                    query_graph_edges.remove(tu_edge[::-1])
                                except:
                                    continue
                neighbors = self.Cloud_Load(picked_edge[1])
                print("     Neighbors of " + str(picked_edge[1]) + ": ")
                for n in neighbors[0][1]:
                    print(self.get_neo4j_stwig_node_trim(n))
                    S.append(self.get_neo4j_stwig_node_trim(n))
                print("     S: " + str(S))
            for s in S:
                print("     Degree of node " + str(s) + " from S:" + str(self.degree_of_node(s)))


# #BIG DATA GRAPH FROM RI DB############################################
# with open('Homo_sapiens_udistr_32.gfd') as f:
#     lines = f.readlines()
# # for line in lines:
# #     print(line)
# # print(lines[0])
# input_graph = nx.Graph()
# num_nodes = int(lines[1])
# # print(num_nodes)
# nodes_attr_list = []
# for i in range(2, num_nodes + 2):
#     spl = lines[i].split(sep="\n")[0]
#     nodes_attr_list.append(spl)
# # for attr in nodes_attr_list:
# #     print(attr)
# num_edges = int(lines[num_nodes + 2])
# # print(num_edges)
# edge_list = []
# for i in range(num_nodes+3, len(lines)):
#     line = [lines[i].split(sep="\n")[0], lines[i].split(sep="\n")[1]]
#     new_edge = tuple(line[0].split(sep=" "), )
#     edge_list.append(new_edge)
# # print(edge_list)
# # Graf neorientat
# graph = nx.Graph()
# graph.add_edges_from(edge_list)
# # print(graph.edges())
# node_attr_dict = dict(zip(graph.nodes(), nodes_attr_list))
# nx.set_node_attributes(graph, node_attr_dict, 'label')
# # print(list(list(graph.nodes(data=True))[0][1].values()))
# # print(list(graph.nodes(data=True))[0][0])

# tx = neograph.begin()
# neonodes = []
# for node in list(graph.nodes(data=True)):
#     cqlQuery = "CREATE (a:`" + str(list(list(node[1].values()))[0]) + "` {RI_id: " + str(node[0]) + "})"
#     neograph.run(cqlQuery)

# edges_without_warning_edge = copy.deepcopy(graph.edges())
# l = list(edges_without_warning_edge)
# l.remove(('12036', '12174'))
# l.remove(('11868', '11915'))
# l.remove(('11680', '11841'))
# l.remove(('11023', '11706'))
#
# for edge in l:
#     cqlQuery = "MATCH(a:`" + str(graph.node[edge[0]]['label']) + "`), (b:`" + str(graph.node[edge[1]]['label']) \
#                + "`) WHERE a.RI_id=" + str(edge[0]) + " AND b.RI_id=" + str(edge[1]) + " CREATE(a)-[:PPI]->(b)"
#     print(cqlQuery)
#     neograph.run(cqlQuery)
#     print(edge)
# #BIG DATA GRAPH FROM RI DB############################################


# SMALL DATA GRAPH FROM ZHAOSUN############################################
# Comenzi Cypher
# CREATE (n:c { id: 'c3' })
# match (n:a) where n.id='a1' return n
# MATCH (n:a),(m:b) WHERE n.id = 'a1' AND m.id = 'b1' CREATE (n)-[r:RELTYPE]->(m)
# Mai ramane de adaugat M2 si M3 din graful de la fig 5
# SMALL DATA GRAPH FROM ZHAOSUN############################################

# test2 = neo4j_test_2()
# print(test2.Cloud_Load(1)) # VECINATATE DE GRADUL 1, toate nodurile indeg/outdeg?
# print(test2.Index_getID(1))
# print(test2.Index_hasLabel(1, 3322))



# query_graph = nx.Graph()
# query_graph_edges = [["a1", "b1"], ["a1", "c1"], ["c1", "d1"], ["c1", "f1"], ["f1", "d1"], ["d1", "b1"], ["d1", "e1"], ["e1", "b1"]]
# query_graph.add_edges_from(query_graph_edges)
# node_attr = ["a", "b", "c", "d", "e", "f"]
# node_attr_dict = dict(zip(sorted(query_graph.nodes()), node_attr))
# nx.set_node_attributes(query_graph, node_attr_dict, 'label')
# print(query_graph.nodes(data=True))

# Caching technique pentru accesul la baza de date?

# q = ['a', ['b','c']] # De facut din fisier, nu hardcoded
# test2.MatchSTwig(q)

# for split in test2.Query_Graph_Split(query_graph):
#     print(split)

# test2.Query_Graph_Split(query_graph)

# query_graph_nodes = list(query_graph.nodes())
# print(query_graph_nodes)

# start = 0
# nodes_chunk = 2
# chunks = []
# # for node in query_graph_nodes:
# while start<len(query_graph_nodes):
#     chunks.append(query_graph_nodes[start:nodes_chunk])
#     start = start + 2
#     nodes_chunk = nodes_chunk + 2
# print(chunks)
# threads = []
# for i in range(len(chunks)):
#     thread = threading.Thread(target=test2.Query_Graph_Split_Parallel, args=[chunks[i]], name="Thread " + str(i))
#     threads.append(thread)
#
# for thread in threads:
#     print()
#     print(thread.name)
#     thread.start()
#     thread.join()

# number_of_threads = int(input("Scrieti numarul de thread-uri: "))
# nodes_chunk2 = len(query_graph_nodes) / number_of_threads
# print(nodes_chunk2)

# print("Freq: ")
# print(test2.freq("a"))
# print("f_value: ")
# print(test2.f_value("a1", query_graph))
# print("STwig_Order_Selection: ")
# print(test2.STwig_Order_Selection(query_graph))