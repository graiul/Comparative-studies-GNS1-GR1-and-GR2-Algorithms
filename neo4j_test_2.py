import threading
from concurrent.futures.thread import ThreadPoolExecutor
from multiprocessing.dummy import Pool as ThreadPool

from networkx import neighbors
from py2neo import Graph, Node, Relationship
import networkx as nx
import copy
import numpy
import operator
import itertools
from timeit import default_timer as timer

class neo4j_test_2(object):

    query_graph = None
    matches = []


    STwig_query_root = None
    STwig_query_neighbor_labels = None


    matches_dict = {}
    used_stwig_list = []
    def __init__(self, query_graph):
        self.query_graph = query_graph

    # neograph_data = Graph(port="7687", user="neo4j", password="graph") # Data Graph Zhaosun
    neograph_data = Graph("bolt://127.0.0.1:7690", auth=("neo4j", "changeme")) # Data Graph Zhaosun din READ_REPLICA
    # neograph_query = Graph("bolt://127.0.0.1:7693", auth=("neo4j", "changeme")) # Query Graph Zhaosun din READ_REPLICA


    def Cloud_Load(self, node_id):  # Pot rula inca o metoda?
        # print("Cloud_Load:")
        # Pentru Zhaosun Data Graph din db neo4j:
        biglist = []
        # print("     id=" + str(node_id))
        cqlQuery = "MATCH (n) WHERE n.zhaosun_id = '" + str(node_id) + "' RETURN n"
        # print(cqlQuery)
        result = self.neograph_data.run(cqlQuery).to_ndarray()
        # print(result)
        nodes_loaded = []
        nodes_loaded.append(result)
        # Returnarea vecinilor nodului cautat.
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

    def Cloud_Load_NX(self, node_ID, query_graph_nx):
        result_node = None
        for node in query_graph_nx.nodes():
            if node is node_ID:
                result_node = node
        nodes_loaded = []
        nodes_loaded.append(result_node)
        result_neighbors = list(query_graph_nx.neighbors(node_ID))
        nodes_loaded.append(result_neighbors)
        return nodes_loaded

    # Return the IDs of nodes with a
    # given label.
    def Index_getID(self, label, iteration_number, matches, stwig_query):
        if iteration_number == 0:
            print("***Index_getID output for Iteration 0")
            print("STwig query: " + str(stwig_query))
            print("Initial matches list - must be empty at the beginning of the Iteration 0: " + str(matches))
            # tx = self.neograph_data.begin()
            # cqlQuery = "MATCH (n:`" + str(label) + "`) RETURN n.RI_id"
            cqlQuery = "MATCH (n) WHERE n.zhaosun_label='" + str(label) + "' RETURN n.zhaosun_id" # IF a IN a1! Graf Zhaosun
            # result = tx.run(cqlQuery).to_ndarray()
            result = self.neograph_data.run(cqlQuery).to_ndarray()
            # print("result:" + str(list(result)))
            nodes_loaded = []
            for r in result:
                nodes_loaded.append(r[0])
            # print("nodes loaded: " + str(nodes_loaded))

            # # Label-urile primului stwig!
            # print("Index_getID stwig query: " + str(stwig_query))
            # q_labels_start = [self.query_graph.node[stwig_query[0]]['label'], []]
            # # print(q_labels_start)
            # for leaf_id in stwig_query[1]:
            #     q_labels_start[1].append(self.query_graph.node[leaf_id]['label'])
            # print("Index_getID, q_labels_start - first: " + str(q_labels_start))

            self.used_stwig_list.append(stwig_query)
            print("***End of Index_getID output for Iteration 0")
            return nodes_loaded

        elif iteration_number > 0:
            # print("Matches for previous iteration: ")
            # print(matches)
            print("***Index_getID output for Iteration " + str(iteration_number))

            print("STwig query: " + str(stwig_query))

            print("Matches dictionary - key,value pair: ")
            # print(list(self.matches_dict.keys())[iteration_number])
            # print(list(self.matches_dict.values())[iteration_number])
            for item in self.matches_dict.items():
                print(item)

            # Aici trebuie modificat.
            # Frunzele unei radacini dintr-o iteratie
            # devin radacini pentru noua iteratie.
            # Pentru noile radacini verificam in graful data daca
            # sunt frunze de acelasi tip precum in twig-ul noii iteratii.
            # OBS: De schimbat formatul pentru matches.
            # De exemplu: in loc de ('b1', 'a1', 'd1', 'e1'), ar fi ['b1', ['a1', 'd1', 'e1']]
            leafs_to_be_roots = []



            # Daca stwig-ul selectat, nu exista in dictionar,
            # deci nu are nici un match in graful data
            # if self.matches_dict.get(repr(stwig_query), []) == []:

            # Daca stwig-ul selectat, nu exista in lista de stwig-uri folosite,
            # deci nu are nici un match in graful data
            if stwig_query not in self.used_stwig_list:
                # Atunci preluam din matches pentru stwig-ul precedent,
                # in dict fiind doar stwig-uri care au avut matches.

                # Modificam astfel:
                # Verificam daca stwig-ul curent are vreo legatura cu unul din
                # stwigurile care au fost deja folosite.
                # Pentru primul cu care are legatura initiem matches,
                # adica pentru fiecare radacina, atasam o lista.
                # Pentru fiecare astfel de lista vom cauta in graful data.

                print("Used stwigs: ")
                print(self.used_stwig_list)
                for used_stwig in self.used_stwig_list:
                    # Daca radacina stwig-ului actual selectat
                    # este de tipul unei frunze al unui stwig deja prelucrat
                    # atunci cautam in graful data id-ul fiecarui nod care
                    # are tipul vreunei frunze al stwig-ului actual.
                    # Trebuie sa gasim pentru fiecare match inceput cate
                    # un nod care sa corespunda fiecarui tip de frunza.

                    if stwig_query[0] in used_stwig[1]: # Daca tipul/labelul radacinii coincide cu una din frunze:
                        # Atunci stwig-ul actual selectat este legat de unul din stwig-urile deja prelucrate

                # print("Last key in matches dict: ")
                # print(list(self.matches_dict.keys())[-1])
                # last_dict_key = list(self.matches_dict.keys())[-1]

                        print("Current stwig: ")
                        print(stwig_query)

                        print("Selected 'used stwig': ")
                        print(used_stwig)


                        if self.matches_dict.get(repr(stwig_query), []) == []:
                            # print("YES")
                            # print(self.matches_dict.get(repr(used_stwig)))
                            # print(len(self.matches_dict.get(repr(used_stwig))))
                            # if len(list(self.matches_dict.values())) == 1:
                            #     for item in list(self.matches_dict[repr(used_stwig)])[1]:
                            #         if item not in leafs_to_be_roots:
                            #             leafs_to_be_roots.append(item)
                            #     print("leafs_to_be_roots on first if: " + str(leafs_to_be_roots))
                            #
                            # elif len(list(self.matches_dict.values())) > 1:
                            for mm in self.matches_dict.get(repr(used_stwig)):
                                # print("mm: " + str(mm))
                                for item in mm[1]:
                                    if item not in leafs_to_be_roots:
                                        leafs_to_be_roots.append(item)


            sorted_leafs_to_be_roots = sorted(leafs_to_be_roots)
            print("Leafs to be roots - taken from selected 'used stwig' matches dict values: ")
            print(sorted_leafs_to_be_roots)

            # #Trebuie returnate toate frunzele de tipul:
            # # Label-ul radacinii stwig-ului dat ca si parametru pentru Index.getID!
            stwig_query_root_type = self.query_graph.node[stwig_query[0]]['label']

            print("Current iteration STwig query root type: " + str(stwig_query_root_type))
            new_roots = []
            for leaf in sorted_leafs_to_be_roots:
                # print("Leaf: " + str(leaf))
                # If the leafs of the prev stwig/current 'used stwig'
                # have the same type as the current stwig root type:

                # Leaf types must be taken from the data graph
                cqlQuery = "MATCH (n) WHERE n.zhaosun_id='" + str(leaf) + "' RETURN n.zhaosun_label"
                result_label = self.neograph_data.run(cqlQuery).to_ndarray()[0][0]
                # print("leaf type: " + str(result_label))

                if stwig_query_root_type == result_label:
                    new_roots.append(leaf)

            print("New roots: " + str(new_roots))

            current_stwig_childred_node_labels = []
            for child in stwig_query[1]:
                # print(child)
                # print(self.query_graph.node[child]['label'])
                child_node_label = self.query_graph.node[child]['label']
                current_stwig_childred_node_labels.append(child_node_label)
            print("current_stwig_childred_node_labels: " + str(current_stwig_childred_node_labels))

            started_matches = []
            not_match = 0
            for nr in new_roots:
                st = [nr, []]
                started_matches.append(st)
            if len(started_matches) == 0:
                print("Started matches: " + str(started_matches))
            if len(started_matches) > 0:
                print("Matches: ")
                finished_matches = []

                for started_match in started_matches:
                    # print(started_match)
                    # Vecinii trebuie sa fie de tipul indicat in STwig-ul query al iteratiei curente.
                    for neighbor_label in current_stwig_childred_node_labels:
                        # print("Neighbor label selected: " + str(neighbor_label))

                        # AICI DE MODIFICAT IN CAZUL GRAFURILOR ORIENTATE?
                        cqlQuery2 = "MATCH(n{zhaosun_id: '" + str(started_match[0]) + "'})--(m) WHERE m.zhaosun_label='" + str(neighbor_label) + "' return m"
                        # print(cqlQuery2)
                        result2 = list(self.neograph_data.run(cqlQuery2).to_ndarray())
                        # if len(result2) > 0:
                        #     print(result2)
                        #     print(self.get_neo4j_stwig_node_trim(result2))
                        #     started_match[1].append(self.get_neo4j_stwig_node_trim(result2))
                        if len(result2) > 0:
                            started_match[1].append(self.get_neo4j_stwig_node_trim(result2))
                    if len(self.STwig_query_neighbor_labels) == len(started_match[1]):
                        print('\x1b[0;30;45m' + "Finished match: " + str(started_match) + '\x1b[0m')
                        # Trebuie ca sa facem o lista de finished matches care
                        # sa o adaugam cheii, altfel se inregistreaza in dict
                        # doar ultimul finished match pentru o cheie.
                        finished_matches.append(started_match)

                    else:
                        print("A complete match was not found: " + str(started_match))
                        not_match = not_match + 1

                if not_match == len(started_matches):
                    print("No matches found for current query STwig!")
                    option = str(input('Stop execution? (y/n)'))
                    if option == "y":
                        exit(code=0)

                self.matches_dict[repr(stwig_query)] = finished_matches
                if stwig_query not in self.used_stwig_list:
                    self.used_stwig_list.append(stwig_query)

                # print("Finished matches: ")
                # for finished_match in started_matches:
                #     print(finished_match)
                #     # if len(finished_match[1][0]) > 0:
                #     for neighbor in finished_match[1][0]:
                #         # print(neighbor)
                #         print(self.get_neo4j_stwig_node_trim(neighbor))
            print("----------------------------------")

            cqlQuery = "MATCH (n) WHERE n.zhaosun_label='" + str(label) + "' RETURN n.zhaosun_id" # IF a IN a1! Graf Zhaosun
            result = self.neograph_data.run(cqlQuery).to_ndarray()
            nodes_loaded = []
            for r in result:
                nodes_loaded.append(r[0])
            print("***End of Index_getID output for Iteration 0")
            return nodes_loaded

    def Index_getID_NX(self, label, query_graph_nx):
        result = []
        for query_node in query_graph_nx.nodes():
            if query_graph_nx.node[query_node]['label'] is label:
                result.append(query_node)
            return result

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

    def Index_hasLabel_NX(self, node_id, label, query_graph_nx):
        for query_node in query_graph_nx.nodes():
            if query_node is node_id:
                if query_graph_nx.node[query_node]['label'] is label:
                    return True
                else:
                    return False

    def MatchSTwig(self, q, iteration_number): # q 1 = (a,{b,c}) din articol, [a, [b,c]] in py. Acest q1 (STwig din query graph)si altele vor fi date de STwigOrderSelection care lucreaza cu graful query.
        # print("IF QUERY STWIG IS UNDIRECTED, THEN MULTIPLE RESULTS ARE GIVEN "
        #       "\nBECAUSE WE USE LABELS NOT NODE ID's WHICH ENCOMPASS MULTIPLE NODES")
        # print("IF QUERY STWIG WOULD BE DIRECTED, THEN THE RESULTS "
        #       "\n- THE DATA GRAPH STWIGS - SHOULD BE AT MOST EXACTLY THE ONES FROM THE QUERY")
        # print("SO, IT WOULD BE SIMPLY A MATTER OF SEARCHING A QUERY STWIG IN DATA GRAPH, BEING RETURNED A SINGLE DATA STWIG."
        #       "\nTHE PROBLEM WOULD SIMPLY BE IF THE QUERY STWIG GIVEN IS FOUND IN THE DATA GRAPH."
        #       "\nBUT FOR THE EXAMPLE IN THE ARTICLE THEY HAD A SINGLE UNDIRECTED QUERY STWIG BE SEARCHED IN AN UNDIRECTED GRAPH."
        #       "\nTHIS MEANS THAT EACH UNDIRECTED QUERY HAS *MULTIPLE* CORRESPONDING DATA GRAPH STWIGS."
        #       "\nTHUS, WE WOULD NEED TO CHOOSE EACH DATA STWIG AS TO BE ADJACENT TO SOME OTHER DATA GRAPH STWIGS "
        #       "\nIN ORDER TO OBTAIN AS A RESULT THE WHOLE QUERY GRAPH."
        #       "\nTHIS IS MASSIVELY SIMPLIFIED IF THE GRAPHS ARE DIRECTED, SINCE ONE "
        #       "\nQUERY GRAPH STWIG SHOULD ONLY HAVE RETURNED FROM MatchSTwig ONLY ONE DATA GRAPH STWIG!")
        # print("STwig from zhaosun undirected query graph, STwig is undirected (Figure 4b from original article): " + str(q))
        # start_time = timer()
        # print("MatchSTwig: ")


        # Pentru q1 cauta in tot graful
        # Pentru q2 cauta doar in nodurile frunza corespunzatoare din G(q1)
        # Pentru twig-ul q3 cauta doar in nodurile frunza corespunzatoare din G(q1) si G(q2)
        # Se adauga filtrare in plus pentru Sr <- Index.getID(r), linia 1 din alg 1 - MatchSTwig.
        # print("###MatchSTwig output:")
        # print("STwig query node id's: " + str(q))
        # print(q[0])
        #---HARDCODED
        # r = str(q[0]) # Root node label
        # L = [q[1][0], q[1][1]] # Root children labels
        # print("Root node label: " + str(r))
        # print("Root children labels: " + str(L))
        #---HARDCODED

        # Aici transformam un stwig query ([b1, [a1, d1, e1]]) intr-unul generic,
        # lasand doar label-urile: [b, [a, d, e]], in Sr intra doar cu label-uri, indiferent de nr iteratiei.
        q_labels_start = [self.query_graph.node[q[0]]['label'], []]
        # print(q_labels_start)
        for leaf_id in q[1]:
            q_labels_start[1].append(self.query_graph.node[leaf_id]['label'])
        # print("Query STwig labels: " + str(q_labels_start))
        # print("STwig query labels - must be only the labels: " + str(q_labels_start))
        # print("Number of leaf labels: " + str(len(q[1])))


        r = str(self.query_graph.node[q[0]]['label'])
        # print("STwig root label: " + str(r))
        L = q_labels_start[1]
        # print("Children labels: " + str(L))
        # for l in children_labels:
        #     L.append(str(self.query_graph.node[]))

        #  (1) Find the set of root nodes by calling Index.getID(r);
        Sr = self.Index_getID(r, iteration_number, self.matches, q) # AICI q ESTE FORMAT DIN LABEL-URI
        # print("Sr, Set of root nodes for label " + str(r) + ": " + str(Sr))
        R = []
        Sli = []

        # (2) Foreach root node, find its child nodes using Cloud.Load();
        for root_node in Sr:
            # print("---Root node: " + str(root_node))
            c = self.Cloud_Load(root_node)
            # print("     Children for selected root, first elem is selected root: " + str(c))
            root = c[0][0]
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
            # Aici len(q[1]) + 1) inseamna numarul etichetelor vecinilor + 1 care este radacina.
            # Astfel pt [a, [b,c]] avem toate gasirile de forma asta, analog pt [b, [a,d,e]].
            combinations = list(itertools.combinations(S_one_elems, len(q[1]) + 1))
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
        # print("STWIG MATCHES: ")
        STwig_matches = sorted(R)
        # for stwig in STwigs:
        #     print(stwig)
        # Am schimbat graful astfel: am inlaturat muchia a3,b3: MATCH (n:a)-[r:RELTYPE]-(m:b) WHERE n.id = 'a3' AND m.id = 'b3' DELETE r
        #                            am adaugat muchia a3,c3: # MATCH (n:a),(m:c) WHERE n.id = 'a3' AND m.id = 'c3' CREATE (n)-[r:RELTYPE]->(m)
        # Astfel am obtinur rezultatele din p788_Zhaosun, pag 5, G(q1) = ...
        # print("End MatchSTwig")
        # total_time_sec = timer() - start_time
        # total_time_millis = total_time_sec * 1000

        # print("\nMatchSTwig exec time -> sec: " + str(total_time_sec))
        # print("\nMatchSTwig exec time -> millis: " + str(total_time_millis))
        STwig_matches_formatted = []
        for match in STwig_matches:
            formatted_match = [match[0], []]
            for child in match[1:]:
                formatted_match[1].append(child)
            STwig_matches_formatted.append(formatted_match)


        self.matches = STwig_matches
        # self.stwig_list.append(q)
        # print("###End of MatchSTwig output")
        return STwig_matches_formatted

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

    def f_value(self, v_id):
        deg = len(list(self.query_graph.neighbors(v_id)))
        # print("deg: " + str(deg))
        # print("neighbors: " + str(list(query_graph.neighbors(v))))
        # print(query_graph.node[v_id]['label'])
        return deg / self.freq_NX(self.query_graph.node[v_id]['label'], self.query_graph)

    def freq(self, v_label):
        # tx = self.neograph_data.begin() # Pentru graful data Zhaosun!

        # cqlQuery = "MATCH (n:`" + str(v_label) + "`) RETURN n"
        cqlQuery = "MATCH (n) WHERE n.zhaosun_label='" + str(v_label) + "' return n"
        # result = tx.run(cqlQuery).to_ndarray()
        result = self.neograph_data.run(cqlQuery)
        return len(list(result))

    def freq_NX(self, label, query_graph_nx):
        counter = 0
        for node in query_graph_nx.nodes():
            if query_graph_nx.node[node]['label'] is label:
                counter += 1
        return counter


    def get_neo4j_stwig_root(self, Cloud_Load_Resulting_STIWGS):
        # print("get_neo4j_stwig_root: ")
        # print("STwig: " + str(Cloud_Load_Resulting_STIWGS))
        print("Cloud_Load_Resulting_STIWGS: " + str(Cloud_Load_Resulting_STIWGS))
        # aux = str(Cloud_Load_Resulting_STIWGS).split("id: '")[1]
        # root_trimmed = str(aux).split("',")[0]
        # print("root_trimmed: " + str(root_trimmed))
        # print("End get_neo4j_stwig_root")
        # return root_trimmed
        root = Cloud_Load_Resulting_STIWGS[0]
        return root

    def get_neo4j_stwig_node_trim(self, stwig_node_to_trim):
        # print("STwig node to trim: " + str(stwig_node_to_trim))
        aux = str(stwig_node_to_trim).split("id: '")[1]
        # print("Aux: " + str(aux))
        node_trimmed = str(aux).split("',")[0]
        # print("Node trimmed: " + str(node_trimmed))
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

    def neighbors_of_node(self, node, query_graph_nx):
        # print("neighbors_of_node execution:")
        # Cloud_Load_Resulting_STIWG = self.Cloud_Load(node)[0][1]
        Cloud_Load_Resulting_STIWG = self.Cloud_Load_NX(node, query_graph_nx)
        # print(Cloud_Load_Resulting_STIWG)
        return Cloud_Load_Resulting_STIWG

    def degree_of_node(self, node, query_graph_nx):
        neighbors = self.neighbors_of_node(node, query_graph_nx)
        # print("Degree of node exec:----------------------------")
        # print("Neighbors for degree of node:")
        deg = len(neighbors[1])
        # print(neighbors[1])
        # print("Deg: " + str(len(neighbors[1])))
        # print("End degree of node exec:----------------------------")
        return deg

    def STwig_Order_Selection(self):
        S = []
        S_no_dup = []
        S_no_dup2 = []

        T = []
        dict_f_values_query_graph = {}
        dict_f_values_query_graph_2 = {}
        dict_f_values_query_graph_in_S = {}

        picked_edge = None
        # query_graph_edges = list(self.query_graph.edges())
        while len(list(self.query_graph.edges())) > 0:
            # sum_start_time = timer()
            # sum_total_time_sec = timer() - sum_start_time
            # sum_total_time_millis = sum_total_time_sec * 1000
            # print("\nSum exec time -> sec: " + str(sum_total_time_sec))
            # print("Sum exec time -> millis: " + str(sum_total_time_millis))
            # print()
            # print("----------------")

            if len(S) == 0:
                # pick an edge (v, u) such that f(u) + f(v) is the largest
                # print("Exec len(s) == 0")
                for edge in list(self.query_graph.edges()):
                    sum = self.f_value(edge[0]) + self.f_value(edge[1])
                    # print("Sum: " + str(sum))
                    dict_f_values_query_graph[edge] = sum

                # print("Dict of edges and f_value sum of nodes of each edge: ")
                # for item in dict_f_values_query_graph.items():
                #     print("     " + str(item))

                index, value = max(enumerate(list(dict_f_values_query_graph.values())), key=operator.itemgetter(1))
                # print("Max sum val for edge: " + str(value))
                # In articol la liniile 5 si 7 din Alg 2 zice "pick AN edge", adica muchia cu val f cea mai
                # mare, iar daca exista doua valori maxime egale aleg prima muchie cu val f maxima.
                # print("Max sum val, index of edge: " + str(index))
                picked_edge = list(dict_f_values_query_graph.keys())[index]

                # print("Picked edge: " + str(picked_edge))
                # # del dict_f_values_query_graph[picked_edge]
                # print("End exec len(s) == 0")



            # TREBUIE SA SCADA DEGREE, TREBUIE INLATURATI VECINII PUSI IN S DIN VECINII NODULUI SELECTAT.
            elif len(S) > 0:
                # pick an edge (v, u) such that v ∈ S and f(u) + f(v) is
                # the largest
                # print("Exec of elif: ")
                # print("S elif: " + str(S))
                # print("Query graph edges; must shrink: ")
                # Trebuie resetat dictionarul:
                dict_f_values_query_graph_2.clear()
                for edge in list(self.query_graph.edges()):
                    # print(str(edge))
                    sum2 = self.f_value(edge[0]) + self.f_value(edge[1])
                    # print("     Sum2: " + str(sum2))
                    dict_f_values_query_graph_2[edge] = sum2

                # print("Dict of edges and f_value sum of nodes of each edge: ")
                # for item in dict_f_values_query_graph_2.items():
                #     print("     " + str(item))

                # Trebuie resetat dictionarul care in care se afla muchiile care au primul nod in S:
                dict_f_values_query_graph_in_S.clear()

                for edge in list(self.query_graph.edges()):
                    # print("Edge selected from total remaining query graph edges: " + str(edge))

                    for elem in S:
                        # pick an edge (v, u) such that v ∈ S
                        # print("     Elem in S: " + str(elem))
                        if edge[0] in elem:


                            # print("     edge[0] = " + str(edge[0]) + str(" in S"))
                            for key_for_S_dict, value_for_S_dict in dict_f_values_query_graph_2.items():
                                if key_for_S_dict[0] == edge[0]:
                                    dict_f_values_query_graph_in_S[edge] = self.f_value(edge[0]) + self.f_value(edge[1])
                            break
                        # else:
                        #     print("     edge[0] = " + str(edge[0]) + str(" not in S elem"))
                        #     continue
                # print("dict_f_values_query_graph_in_S: ")
                # for item in dict_f_values_query_graph_in_S.items():
                #     print("     " + str(item))
                # print("S end elif: " + str(S))
                # # and f(u) + f(v) is the largest
                index_S, value_S = max(enumerate(list(dict_f_values_query_graph_in_S.values())),
                                     key=operator.itemgetter(1))
                # print("     Max val: " + str(value_S))
                # print("     Max val index: " + str(index_S))

                picked_edge_S = list(dict_f_values_query_graph_in_S.keys())[index_S]

                # print("     Picked edge_S: " + str(picked_edge_S))
                picked_edge = picked_edge_S
                # print("Picked edge: " + str(picked_edge))
                # print("End exec elif.")

            # print("Working on picked_edge[0] (v) = " + str(picked_edge[0]))
            # Tv ←the STwig rooted at v
            Tv = self.Cloud_Load_NX(picked_edge[0], self.query_graph)
            # # print("Cloud_Load_Resulting_STIWG: " + str(Cloud_Load_Resulting_STIWG))
            # # q_root = self.get_neo4j_stwig_root(Cloud_Load_Resulting_STIWG)
            # q_root = Cloud_Load_Resulting_STIWG[0]
            # # Tv = self.get_neo4j_STwig_with_root(q_root, Cloud_Load_Resulting_STIWG)
            # print("     STWIG formatted also having the root at first elem; Tv = " + str(Tv))
            # add Tv to T
            T.append(Tv)
            # S ← S∪ neighbor(v), v este picked_edge[0]
            neighbors = self.Cloud_Load_NX(picked_edge[0], self.query_graph)[1]
            if len(neighbors) == 0:
                # print("No neighbors left.")
                break
            S.append(neighbors)
            # print("S: " + str(S))
            # Scoaterea duplicatelor din S:
            for elem in S:
                for el in elem:
                    if el not in S_no_dup:
                        S_no_dup.append(el)
            # print("S, no duplicates: ")
            # print(S_no_dup)
            # print("Length of query graph edge list: " + str(len(list(self.query_graph.edges()))))
            # print("T: ")
            # for tv in T:
            #     print(tv)
            # # remove edges in Tv from q
            edges_to_remove = []
            for n in neighbors:
                edges_to_remove.append([Tv[0], n])
            # print("Edges to remove: " + str(edges_to_remove))
            for edge_to_rem in edges_to_remove:
                self.query_graph.remove_edge(edge_to_rem[0], edge_to_rem[1])
            # print("Length of query graph edge list after removal: " + str(len(list(self.query_graph.edges()))))


            # Trebuie sa elimin si nodurile singulare ramase? RASPUNS: Nu.
            # # Neighbors of v
            # neighbors = self.Cloud_Load_NX(picked_edge[0], self.query_graph)
            # print("     neighbors: " + str(neighbors[1]))
            # neighbors_copy_to_remove_from = copy.deepcopy(neighbors[1])
            # print("     neighbors_copy_to_remove_from = " + str(neighbors_copy_to_remove_from))
            # print("     Neighbors of picked_edge[0] = " + str(picked_edge[0]) + ": ")
            # # for n in neighbors[0][1]:
            # for n in neighbors[1]:
            #     # print("     " + str(self.get_neo4j_stwig_node_trim(n)))
            #     print("     " + str(n))
            #     # S.append(self.get_neo4j_stwig_node_trim(n))
            #     S.append(n)
            #     # Acum, vecinul adaugat in S ar trebui eliminat din multimea vecinilor nodului ales.
            #     # Astfel, degree-ul scade, iar algoritmul se incheie.
            #     neighbors_copy_to_remove_from.remove(n)
            # print("     neighbors_copy_to_remove_from = " + str(neighbors_copy_to_remove_from))
            # print("     S: " + str(S))
            # Tv_edges = []
            # root = Tv[0]
            # # print("Root: " + root)
            # Tv.remove(root)
            # for tv_elem in Tv[0]:
            #     Tv_edges.append([root, tv_elem])
            # print("     Edges in Tv: " + str(Tv_edges))
            # print("     Query graph edges: " + str(self.query_graph.edges()))
            # print("     Comparing of edges and removal: ")
            # print("         Nr of edges to be removed: " + str(len(Tv_edges)))
            # print("         Nr of edges total: " + str(len(query_graph_edges)))
            # # query_graph_edges = list(query_graph.edges())
            # print("         Edges found that will be removed: ")
            # for tv_edge in Tv_edges:
            #     for query_edge in query_graph_edges:
            #         # print(set(tv_edge))
            #         # print(set(query_edge))
            #         # print("-----------")
            #         if set(tv_edge) == set(query_edge):
            #             print("         tv_edge == query_edge: " + str(tv_edge))
            #             try:
            #                 query_graph_edges.remove(tuple(tv_edge))
            #             except:
            #                 try:
            #                     query_graph_edges.remove(tuple(tv_edge[::-1]))
            #                 except:
            #                     continue
            # print("     List of edges after removal: " + str(query_graph_edges))
            # print("     Nr of edges total after removal: " + str(len(query_graph_edges)))

            # print("\nTu-------------------------------------------------------")
            # print("Working on picked_edge[1] = " + str(picked_edge[1]))
            # print("     Deg of node u, picked_edge[1]: " + str(self.degree_of_node(picked_edge[1], self.query_graph)))
            if self.degree_of_node(picked_edge[1], self.query_graph) > 0:
                Tu = self.Cloud_Load_NX(picked_edge[1], self.query_graph)
                # print("     STWIG formatted also having the root at first elem; Tu: " + str(Tu))
                T.append(Tu)
                # remove edges in Tu from q
                edges_to_remove2 = []
                # Vecinii nodului u
                neighbors2 = self.Cloud_Load_NX(picked_edge[1], self.query_graph)[1]
                for n2 in neighbors2:
                    edges_to_remove2.append([Tu[0], n2])
                    # if self.query_graph.has_edge(Tu[0], n2):
                        # print("     Edge " + str([Tu[0], n2]) + " exists in query graph and must be rem.")
                # print("     Edges to remove: " + str(edges_to_remove2))
                for edge_to_rem2 in edges_to_remove2:
                    self.query_graph.remove_edge(edge_to_rem2[0], edge_to_rem2[1])
                # print("     Length of query graph edge list after removal: " + str(len(list(self.query_graph.edges()))))
                # print("     Deg of node u, picked_edge[1]: " + str(self.degree_of_node(picked_edge[1], self.query_graph)))

                S.append(neighbors2)
                # print("S: " + str(S))
                for elem2 in S:
                    for el2 in elem2:
                        if el2 not in S_no_dup2:
                            S_no_dup2.append(el2)
                # print("S, no duplicates: ")
                # print(S_no_dup2)
                # print("T: ")
                # for t2 in T:
                #     print(t2)
            # print("Degrees of each element in S: ")
            S_no_dup2_for_removal = copy.deepcopy(S_no_dup2)
            for s2 in S_no_dup2:
                # print("Element of S : " + str(s2) + " has degree value of: " + str(self.degree_of_node(s2, self.query_graph)))
                if self.degree_of_node(s2, self.query_graph) == 0:
                    S_no_dup2_for_removal.remove(s2)
            # print("Remaining elements in S: ")
            # print(S_no_dup2_for_removal)
            # print("End exec Tu-------------------------------------------------------\n")
        # print("Final result T: ")
        # for tt in T:
        #     print(tt)
        return T

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


# Testare metode access graf query graf data RI
# test2 = neo4j_test_2()
# print(test2.Cloud_Load(1)) # VECINATATE DE GRADUL 1, toate nodurile indeg/outdeg?
# print(test2.Index_getID(1))
# print(test2.Index_hasLabel(1, 3322))


# Testare metode access graf query graf data RI
# query_graph = nx.Graph()
# query_graph_edges = [["a1", "b1"], ["a1", "c1"], ["c1", "d1"], ["c1", "f1"], ["f1", "d1"], ["d1", "b1"], ["d1", "e1"], ["e1", "b1"]]
# query_graph.add_edges_from(query_graph_edges)
# node_attr = ["a", "b", "c", "d", "e", "f"]
# node_attr_dict = dict(zip(sorted(query_graph.nodes()), node_attr))
# nx.set_node_attributes(query_graph, node_attr_dict, 'label')
# print(query_graph.nodes())
# test2 = neo4j_test_2()
# print(test2.Cloud_Load_NX("a1", query_graph))
# print(test2.Index_getID_NX("a", query_graph))
# print(test2.Index_hasLabel_NX("a1", "a", query_graph))

# Propuneri BP
# Caching technique pentru accesul la baza de date?
# De citit din fisier, nu hardcoded

# q = ['a', ['b','c']]# STwig. Denumit in codul meu de asemenea ca si un "split".
                      # Mai multe dintre acestea vor fi returnate intr-o ordine eficienta de STwig_Order_Selection.
                      # NUMAI PT GRAFUL QUERY.
# test2.MatchSTwig(q)

# Aici am scris eu o metoda pentru a desparti graful query in mai multe bucati.
# Nu sunt formatate precum [root,[root_neighbors]]
# for split in test2.Query_Graph_Split(query_graph):
#     print(split)
# test2.Query_Graph_Split(query_graph)

# Afisare noduri graf query.
# query_graph_nodes = list(query_graph.nodes())
# print(query_graph_nodes)

# Aici am scris eu o metoda pentru a desparti PARALELIZAT graful query in mai multe bucati.
# Nu sunt formatate precum [root,[root_neighbors]]
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
# for thread in threads:
#     print()
#     print(thread.name)
#     thread.start()
#     thread.join()
# number_of_threads = int(input("Scrieti numarul de thread-uri: "))
# nodes_chunk2 = len(query_graph_nodes) / number_of_threads
# print(nodes_chunk2)

# Aici testez frecventa si f_value descrise in articolul ZhaoSun et.al.
# print("Freq: ")
# print(test2.freq("a"))
# print("f_value: ")
# print(test2.f_value("a1", query_graph))
# print("STwig_Order_Selection: ")
# print(test2.STwig_Order_Selection(query_graph))