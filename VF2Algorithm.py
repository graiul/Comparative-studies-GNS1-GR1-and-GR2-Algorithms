import copy
from collections import OrderedDict

import networkx as nx
from networkx.algorithms import isomorphism
from py2neo import Graph, Subgraph

from GenericQueryProc import GenericQueryProc
from Query_Graph_Generator import Query_Graph_Generator
from Graph_Format import Graph_Format
from timeit import default_timer as timer

# https://stackoverflow.com/questions/6537487/changing-shell-text-color-windows
# https://pypi.org/project/colorama/
from colorama import init
from colorama import Fore, Back, Style
init()

# print("\nVF2 algorithm:")


class VF2Algorithm(GenericQueryProc):

    # M = [] # Lista de asocieri intre noduri query si data / Matchings.
             # Cum decurge procedura de asociere, dupa procedura de refinement?

    # Solutie partiala curenta (prima corespondenta functioneaza tot timpul):
    # M.append(["u1", "v4"]) # Voi alege pentru prima asociere in mod aleator un nod data. Acesta va fi inceputul asocieriilor.

    queryGraphFile = None
    dataGraphFile = None
    queryGraph = None
    dataGraph = None

    start_time = None
    total_time = None

    respectare_conditie_1 = False
    respectare_conditie_2 = False
    respectare_conditie_3 = False

    results_dict = OrderedDict()

    M_list = []


    # def __init__(self, M, graph_choice): #, queryGraphFile, dataGraphFile, graph_format_type):
    def __init__(self, M): #, queryGraphFile, dataGraphFile):

        # self.queryGraph = query_graph
        # self.dataGraph = data_graph
        self.start_time = timer()


        # self.queryGraphFile = queryGraphFile
        # self.dataGraphFile = dataGraphFile
        # if graph_format_type is 'p133han':
        #     gfq = Graph_Format(self.queryGraphFile)
        #     # gfq.display_file()
        #     gfq.create_graph_from_p133han_file()
        #     self.queryGraph = gfq.get_graph()
        #     # print(self.queryGraph.edges)
        #     gfd = Graph_Format(self.dataGraphFile)
        #     gfd.create_graph_from_p133han_file()
        #     self.dataGraph = gfd.get_graph()
        #     # print(self.dataGraph.edges())
        #
        # if graph_format_type is 'RI':
        #     gfq = Graph_Format(self.queryGraphFile)
        #     # gfq.display_file()
        #     gfq.create_graph_from_RI_file()
        #     self.queryGraph = gfq.get_graph()
        #     gfd = Graph_Format(self.dataGraphFile)
        #     gfd.create_graph_from_RI_file()
        #     self.dataGraph = gfd.get_graph()


        # # Pentru metoda nextQueryVertex, fiecare nod al celor doua grafuri
        # # va avea adaugat o proprietate de tip bool numita 'matched'

        # GRAFUL QUERY - FOLOSESTE NODURI CU ID DE TIPUL INT
        query_graph_gen = Query_Graph_Generator()
        # if graph_choice == "sm":
        #     self.queryGraph = query_graph_gen.gen_small_graph_query_graph()
        #     nx.set_node_attributes(self.queryGraph, False, 'matched')

        # if graph_choice == "ri":
        graph_choice = "ri"
        self.queryGraph = query_graph_gen.gen_RI_query_graph()
        nx.set_node_attributes(self.queryGraph, False, 'matched')
        # print("Query graph nodes: " + str(self.queryGraph.nodes(data=True)))
        # print("Query graph edges: " + str(self.queryGraph.edges()))

        # GRAFUL DATA DIN NEO4J
        # neograph_data = Graph("bolt://127.0.0.1:7690", auth=("neo4j", "changeme"))  # Data Graph RI din READ_REPLICA
                                                                                    # din cluster Neo4J cu cinci instante.
                                                                                    # Patru 'core' si una 'read replica'.

        neograph_data = Graph("bolt://127.0.0.1:7687", auth=("neo4j", "password")) # Data Graph RI - O singura instanta de Neo4J

        cqlQuery = "MATCH p=(n)-[r:PPI]->(m) return n.node_id, m.node_id"
        result = neograph_data.run(cqlQuery).to_ndarray()
        edge_list = result.tolist()
        # print("edge_list: ")
        # print(edge_list)
        edge_list_integer_ids = []
        for string_edge in edge_list:
            edge_list_integer_ids.append([int(i) for i in string_edge])
        # print("edge_list_integer_ids: ")
        # print(edge_list_integer_ids)


        self.dataGraph = nx.Graph()
        self.dataGraph.add_edges_from(sorted(edge_list_integer_ids))
        cqlQuery2 = "MATCH (n) return n.node_id, n.node_label"
        result2 = neograph_data.run(cqlQuery2).to_ndarray()
        # print("result2: ")
        # print(result2)
        node_ids_as_integers_with_string_labels = []
        for node in result2:
            # print(node[0])
            node_ids_as_integers_with_string_labels.append([int(node[0]), node[1]])
        # print("node_ids_as_integers_with_string_labels: ")
        # print(node_ids_as_integers_with_string_labels)

        node_attr_dict = OrderedDict(sorted(node_ids_as_integers_with_string_labels))
        nx.set_node_attributes(self.dataGraph, node_attr_dict, 'label')
        nx.set_node_attributes(self.dataGraph, False, 'matched')

        if len(M) > 0:
            # Matching-ul trebuie sa fie fara id-uri, doar label-uri.
            # print("M: ")
            # for m_item in M:
            #     print(m_item)
            self.queryGraph.nodes[M[0][0]]['matched'] = True
            self.dataGraph.nodes[M[0][1]]['matched'] = True

        # GM = isomorphism.GraphMatcher(self.queryGraph, self.dataGraph)
        # print(GM.is_isomorphic())
        # exit(0)

        # print("\nQuery graph: ")
        # print(self.queryGraph.nodes(data=True))
        # print(self.queryGraph.edges())
        # print()

        # print("Data graph: ")
        # print(self.dataGraph.nodes(data=True))
        # print(self.dataGraph.edges())
        # print()

    # Varianta in care lucram cu lista M in vederea verificarii daca un nod a fost asociat deja sau nu este dificil de implementat datorita contradictiei care apare:
    # in anumite cazuri, adica pentru unele noduri query sau data este nevoie doar de ultima asociere din lista, iar daca aceasta nu corespunde cerintelor, trebuie verificata toata lista.
    # Din pacate, acest lucru face ca prima regula de pruning sa nu functioneze corect in toate cazurile.
    # Aceasta varianta este mai buna pentru grafurile cu zeci de mii de noduri, deoarece lista M este mult mai mica, si astfel este mai usor de verificat care dintre noduri au fost asociate,
    # in loc de a verifica acest lucru iterand toate nodurile grafului respectiv.

    # CA SI IDEE: de aplicat indicativul matched si la graful data. Astfel, as putea evita verificarea listei M, sau al ultimei intrari din M, in functie de caz, evitand contradictiile de calcul.
    # Valabil pentru
    #   GATA - nextQueryVertex
    #   refineCandidates.
    # GATA - Pentru isJoinable: folosind un astfel de indicativ si pentru nodurile grafului data, as putea verifica daca este joinable si fara a utiliza lista M, sau ultima asociere din M.
    # De asemenea pentru isJoinable, in cazul nodurilor query, ar putea fi mai indicata verificarea vecinilor nodului query selectat, conform p133-han.pdf, pagina 4/12 partea stanga,
    # la sectiunea algoritmului lui Ullmann, unde se descrie metoda isJoinable.

    # Trebuie sa vad ce folos are restoreState in context
    # Trebuie sa returnez toate instantele lui M, adica de fiecare data cand graful query a fost gasit in totalitate in graful data.

    def subGraphSearch(self, M):
        if M == None: # Termina executia programului.
            return
        if len(M) == len(self.queryGraph.nodes()): # Termina cautarea dupa rezultate
            # print(Fore.LIGHTRED_EX + "Reported M: ")
            # print(M)
            # print(Style.RESET_ALL)
            return M
        else:
            # print()
            # print(Back.WHITE + Fore.LIGHTBLUE_EX + Style.BRIGHT + "Subgraph search:")
            # print(Style.RESET_ALL)

            u = self.nextQueryVertex(M)
            if u is None:
                # print("Nu mai sunt noduri query!")
                self.total_time = timer() - self.start_time
                # print("Timp total de executare algoritm VF2: " + str(self.total_time) + " secunde.")
                return
            # print(str(u) + " Selectat de nextQueryVertex.")

            candidates_u = self.filterCandidates(u)
            # print("Candidatii lui " + str(u) + ": " + str(candidates_u))

            candidates_refined = self.refineCandidates(M, u, candidates_u)
            # print("\nCandidatii rafinati ai nodului " + str(u) + ": " + str(candidates_refined))
            # print("candidates_refined:")
            # print(candidates_refined)
            # print(len(list(candidates_refined)))

            if candidates_refined == None:
                # print("No refined candidates for node: " + str(u))
                # print()
                # print(self.results_dict.items())
                # self.results_dict = {}
                return 0

            if len(M) == 0:
                self.results_dict[u] = candidates_refined
                return list(self.results_dict.items())[0]
            if len(M) > 0:
                # if candidates_refined != None:
                # print("Query leaf node: " + str(u))
                # print("Query root node: " + str(M[0][1]))
                # print("Results dict before putting results: " + str(list(self.results_dict.items())))
                # print("Refined candidates for leaf " + str(u) + ": " + str(candidates_refined))
                self.results_dict[u] = candidates_refined
                # print("Results dict after putting results: " + str(list(self.results_dict.items())))

            # print("Asocieri / Matchings: " + str(M))

            for v in candidates_refined:
                # print("Candidat rafinat selectat: " + str(v))
                # print("Asocieri existente: ")
                # print(M)
                # for m_elem in M:

                # last_matching = M[-1]
                # print("Subgraph search last_matching:")
                # print(last_matching)
                # print(str(v) + " not in " + str(last_matching) + " ?")
                # if v not in last_matching: # such that v is not yet matched. Am verificat deja acest lucru pentru nodul query u in metoda nextQueryVertex().
                    # print("v not in last_matching! Continuing...")
                    # print("Is joinable?")
                if self.isJoinable(M, u, v):
                    # print("Joinable!")
                    updated_M = self.updateState(M, u, v)
                    # print("updated_M: " + str(updated_M))
                    self.subGraphSearch(updated_M)
                    # if updated_M != None:
                    #     self.restoreState(updated_M, u, v)
                    # else:
                    #     print("Not joinable!")


    def filterCandidates(self, query_node):
        candidates = []
        # if query_node is None:
        #     exit(0)
        for data_node in self.dataGraph.nodes():
            if self.queryGraph.nodes[query_node]['label'] == self.dataGraph.nodes[data_node]['label']:
                candidates.append(data_node)
        return candidates

        # Eticheta unui nod query SE AFLA IN eticheta unui nod data.
        # candidates = []
        # # for x in VF2QueryGraphDict.keys():
        # # print("Candidates for node: " + u.getVertexLabel())
        # for y in dataGraphDict.keys():
        #     if u.getVertexLabel() in dataGraphDict.get(y).getVertexLabel():
        #         # print("Is candidate")
        #         # print(dataGraphDict.get(y))
        #         candidates.append(dataGraphDict.get(y).getVertexID())
        #
        # return candidates

    # def filterCandidates(self, q, g, u): # Poate avea si denumirea de c().
    #     self.q = q #Aici se folosesc variabilele din clasa abstracta atunci cand folosim "self"
    #     self.g = g
    #     filteredDataGraphVertices = {} #Cheile sunt etichetele nodurilor, iar valorile sunt obiecte de tip Vertex.
    #     return filteredDataGraphVertices

    def nextQueryVertex(self, M): # Neoptimizat, adica se vor parcurge nodurile query in ordine lexicografic crescatoare. In aceeasi ordine vor fi inserate perechile [nod query, ..] in M.
        # print("next query vertex exec:")
        # print("queryNodes:")
        queryNodes = list(self.queryGraph.nodes())
        # print(queryNodes)
        # print("matchings:")
        # print(M)
        # last_matching = M[-1]
        # # SAU:
        # for matching in reversed(M):
        #     print("matching from reversed matching list: " + str(matching))
        for node in queryNodes:
            if self.queryGraph.nodes[node]['matched'] is False:
                # print("Returnam nodul query: " + str(node))
                return node  # Returneaza primul nod query care nu se afla

        # VARIANTA VECHE in care folosesc lista M de asocieri.
        # for queryNode in queryNodes:
        #     for m_elem in M:
        #         if queryNode in m_elem: # Daca folosesc operatorul !=, nu face diferenta intre doua siruri string, ci returneaza u1, chiar daca sunt egale. Trebuie sa returneze de la u2 in jos,
        #                                 # adica generalizand, primul nod care este diferit.

    # FOARTE IMPORTANT! TOATE COMPARARILE CU M SE FAC CU ULTIMA INTRARE, ADICA ULTIMA ASOCIERE. ASTFEL< PE RAND TOATA LISTA VA FI VERIFICATA O SINGURA DATA. DACA REIAU VERIFICAREA CU FIECARE ASOCIERE DIN LISTA
    # DUPA SELECAREA FIECARUI CANDIDAT, VA REZULTA O LISTA GOALA A CANDIDATILOR RAFINATI.
    # DAR, cateodata este nevoie doar de ultima intrare. Pentru o posibila rezolvare, am notat in comentarii deasupra metodei subgraphSearch.
    def refineCandidates(self, M, query_node, query_node_candidates):
        Mq = []  # Set of matched query vertices
        Mg = []  # Set of matched data vertices
        Cq = []  # Set of adjacent and not-yet-matched query vertices connected from Mq
        Cg = []  # Set of adjacent and not-yet-matched data vertices connected from Mg

        # Conditia (1): Prune out v belonging to c(u) such that a vertex v is not connected from already matched data vertices.
        # query_node = self.nextQueryVertex(query_graph)
        # query_node_candidates = self.filterCandidates(query_node, query_graph, data_graph)
        # print("------------INCEPUT EXECUTIE RAFINARE CANDIDATI-----------")
        # print("QUERY NODE: " + str(query_node))
        # print("CANDIDATES: " + str(query_node_candidates))

        # print()
        # print(M)
        if len(M) == 0:
            # print("\nNu avem valori pt Mq si Mg pentru ca nu avem o prima asociere inca.")
            # print("Astfel, Cq si Cg vor avea toate nodurile din grafurile query, respectiv cel data.")
            Cq = list(self.queryGraph.nodes())
            Cg = list(self.dataGraph.nodes())

        if len(M) > 0:
            Mq.append(M[-1][0]) # Ce are a face cu ultima asociere?
            Mg.append(M[-1][1]) # Folosesc -1 pentru a returna ultimul element din lista (https://stackoverflow.com/questions/930397/getting-the-last-element-of-a-list-in-python).
            # Este necesar ca lista sa nu fie niciodata goala, ceea ce se rezolva foarte bine prin faptul ca lista va fi tot
            # timpul initializata cu o asociere.
            Cq.append(list(self.adj(M[-1][0], self.queryGraph)))
            Cg.append(list(self.adj(M[-1][1], self.dataGraph)))
            # print("Mq = " + str(Mq))
            # print("Mg = " + str(Mg))
            # print("Cq = " + str(Cq))
            # print("Cg = " + str(Cg))
            # Pentru fiecare candidat verificam conditia (1)

        query_nodes_candidates_for_deletion = copy.deepcopy(query_node_candidates)
        self.respectare_conditie_1 = False
        self.respectare_conditie_2 = False
        self.respectare_conditie_3 = False

        # Conditia (1): Prune out candidate such that candidate is not connected from already matched data vertices.
                        # Prune out candidate such that candidate is connected
        # from not matched data vertices.

        # print("\n     Conditia(1): ")
        for candidate in query_node_candidates:
            # print("\nCandidatul selectat: " + str(candidate))
            # print("     Conditia(1):")
            # for matching in M:
            # last_matching = M[-1]
            # print("     Matching (trebuie verificat pentru fiecare matching / asociere): " + str(matching))
            # print("M: " + str(M))
            # print(candidate)

            delete_indicator = False
            occurence_list = []

            if len(M) == 0:
                # Cateva detalii despre prima iteratie a rularii:
                # print("Inca nu avem nici un matching, deci nu putem verifica 'such that candidate is not connected from already matched data vertices' ")
                # print("Dar verificam daca exista muchie intre nodul candidat si celelalte noduri data. Facem acest lucru pentru a verifica si urmatoarele doua conditii.")
                # print(
                #     "Pentru ca nu avem inca asocieri in lista M, nu avem Mq si Mg. De aceea nu putem verifica Conditia(2) sau Conditia(3) pentru ca are nevoie de aceleasi doua liste Mq si Mg.")
                # print(
                #     "Conform p133han pentru rularea algoritmului este nevoie deja de o asociere existenta in lista M.")
                # print(
                #     "Din articolul p133han, http://www.vldb.org/pvldb/vol6/p133-han.pdf, sectiunea 3.3 VF2 Algorithm, explicatii pentru metoda NextQueryVertex: ")
                # print(
                #     "NextQueryVertex: Unlike Ullmann, VF2 starts with the first vertex and selects a vertex connected from the already matched query vertices. Note that the original VF2 algorithm does not define any order in which query vertices are selected.")
                # print("'already matched query vertices.'")
                # print("Deci avem nevoie de un matching la inceputul executarii algoritmului.")
                # print(
                #     "Astfel returnam candidatii cu care putem face asocierea primului nod al grafului query. Cu alte cuvinte, radacinile-candidat.")

                return query_node_candidates

            if len(M) > 0:

                for data_node in self.dataGraph.nodes():
                    # print("Nod data selectat pentru verificare: " + str(data_node))
                    # Daca nodul data selectat a mai fost folosit
                    if self.dataGraph.nodes[data_node]['matched'] == True:
                        # print("Nodul " + str(data_node) + " este deja marcat ca fiind 'matched' ")
                        # Atunci verificam sa nu fie adiacent lui
                        # print("Lipseste in graful data muchia " + str([candidate, data_node]) + " ?")
                        if self.dataGraph.has_edge(data_node, candidate) == False:
                            if candidate in query_nodes_candidates_for_deletion:
                                delete_indicator = True
                                # print("Lipseste.")
                                occurence_list.append("Lipseste")

                        else:
                            delete_indicator = False
                            # print("Exista.")
                            # print("Edge " + str([data_node, candidate]) + " exists.")
                            occurence_list.append("Exista")
                                # print("Nu exista muchie. Eliminam candidatul conform Conditiei 1.")
                                # print("Muchia care nu exista: " + str([candidate, data_node]))
                                # query_nodes_candidates_for_deletion.remove(candidate)
                                # self.respectare_conditie_1 = False
                                # break
                # # A DOUA VARIANTA VECHE: foloseste lista M inversata.
                # for matching in reversed(M):
                #     print("Candidate: " + str(candidate))
                #     print("Refinement: " + str(matching))
                #     # # PRIMA VARIANTA VECHE: cautarea in lista M care contine elementele in ordinea inserarii.
                #     # if self.data_graph.has_edge(candidate, matching[1]) is False:
                #     #     # print("         Conditia(1) intra in vigoare, astfel avem:")
                #     #     # print("         *Nu exista muchie intre " + str(candidate) + " si " + str(matching[1]) + ". Se va sterge candidatul " + str(candidate) + ".")
                #     #     # print("         *Nu se mai verifica pentru Conditia(2), ci verificam Conditia(2) pentru candidatii care au trecut.")
                #     #     for neighbor in self.data_graph.neighbors(matching[1]):
                #     #         if neighbor is matching[1]:
                #     #             if self.data_graph.has_edge(candidate, neighbor) is True:
                #     #                 print("Has edge. Trece regula 1.\n")
                #     #                 self.respectare_conditie_1 = True
                #     #                 break
                #     # else:
                #     #     break
                #
                #     if self.data_graph.has_edge(candidate, matching[1]) is False:
                #         if candidate in query_nodes_candidates_for_deletion:
                #             query_nodes_candidates_for_deletion.remove(candidate) # Am putut sa fac remove unui element din lista direct in bucla foreach. NU SE FAC STERGERI DIN LISTA IN ACELASI TIMP CU ITERAREA!
                #             self.respectare_conditie_1 = False

            # print(occurence_list)
            # exit(0)

            if len(occurence_list) == 0:
                return query_node_candidates

            if len(occurence_list) == 1:
                if occurence_list[0] == "Lipseste":
                    # print("Nu exista muchie. Eliminam candidatul conform Conditiei 1.")
                    # print("Muchia care nu exista: " + str([candidate, data_node]))
                    query_nodes_candidates_for_deletion.remove(candidate)
                    self.respectare_conditie_1 = False

            if len(occurence_list) == 1:
                if occurence_list[0] == "Exista":
                    # print("Exista muchia. Trece Conditia (1).")
                    # print()
                    self.respectare_conditie_1 = True


            if len(occurence_list) > 1:
                if occurence_list[-1] == "Lipseste":
                    if occurence_list[-2] == "Lipseste":
                        # print("Nu exista muchie. Eliminam candidatul conform Conditiei 1.")
                        # print("Muchia care nu exista: " + str([candidate, data_node]))
                        query_nodes_candidates_for_deletion.remove(candidate)
                        self.respectare_conditie_1 = False

                    if occurence_list[-2] == "Exista":
                        # print("Exista muchia. Trece Conditia (1).")
                        # print()
                        self.respectare_conditie_1 = True

                if occurence_list[-1] == "Exista":
                    # print("Exista muchia. Trece Conditia (1).")
                    # print()
                    self.respectare_conditie_1 = True
                # if occurence_list.count("Exista") > occurence_list.count("Lipseste"):
                #     print("Exista muchia. Trece Conditia (1).")
                #     print()
                #     self.respectare_conditie_1 = True
                # if occurence_list.count("Exista") < occurence_list.count("Lipseste"):
                #     if candidate in query_nodes_candidates_for_deletion:
                #
                #         print("Nu exista muchie. Eliminam candidatul conform Conditiei 1.")
                #         print("Muchia care nu exista: " + str([candidate, data_node]))
                #         query_nodes_candidates_for_deletion.remove(candidate)
                #         self.respectare_conditie_1 = False

            # print("         Candidatii lui " + str(query_node) + " dupa Conditia(1)")# + " actualizati in functie de conditia (1) al VF2: ")
            # print("         " + str(query_nodes_candidates_for_deletion))
            # print()

            # Pentru fiecare candidat trebuie verificata si Conditia (2): Prune out any vertex v in c(u) such that |Cq intersected with adj(u)| > |Cg intersected with adj(v)|
            if self.respectare_conditie_1:
                # print("     Conditia(2):")

                first_intersection = []
                adjQueryNode = list(self.adj(query_node, self.queryGraph)) # Retin candidatii in ordine lexicografic crescatoare.
                for xx in adjQueryNode:
                    for yy in Cq[-1]: # Aici e lista in lista.
                        if xx == yy:
                            first_intersection.append(xx)
                second_intersection = []
                adjCandidate = list(self.adj(candidate, self.dataGraph))
                for xx in adjCandidate:
                    for yy in Cg[-1]:
                        if xx == yy:
                            second_intersection.append(xx)
                # print("         Facut intersectiile de la Conditia (2)")
                # print("         " + str(len(first_intersection)))
                # print("         " + str(len(second_intersection)))
                # print("For breakpoint.")
                # print("Cardinalul primei intersectii > decat celei de a doua?")
                if len(first_intersection) > len(second_intersection):
                    # print("         Conditia(2) intra in vigoare, astfel avem:")
                    # print("         Cardinalul primei intersectii este mai mare decat cea de-a doua. Se va sterge candidatul " + str(candidate) + ".")
                    if candidate in query_nodes_candidates_for_deletion:
                        query_nodes_candidates_for_deletion.remove(candidate)
                        # print("         Candidatii lui " + str(query_node))
                        # print("         " + str(query_nodes_candidates_for_deletion))
                        # print()
                        self.respectare_conditie_2 = False
                else:
                    # print("         Nu. Trece Conditia (2).")
                    # print()
                    self.respectare_conditie_2 = True

                # print("         Candidatii lui " + str(query_node) + " dupa Conditia (2):")
                # print("         " + str(query_nodes_candidates_for_deletion))
                # print()
                if self.respectare_conditie_2 is True:
                    # print("     Conditia(3):")

                    for cq_elem in Cq:
                        for cq_elem_node in cq_elem:
                            if cq_elem_node in adjQueryNode:
                                adjQueryNode.remove(cq_elem_node)
                    for mq_elem_node in Mq:
                        if mq_elem_node in adjQueryNode:
                            adjQueryNode.remove(mq_elem_node)

                    for cg_elem in Cg:
                        for cg_elem_node in cg_elem:
                            if cg_elem_node in adjCandidate:
                                adjCandidate.remove(cg_elem_node)
                    for mg_elem_node in Mg:
                        if mg_elem_node in adjCandidate:
                            adjCandidate.remove(mg_elem_node)

                    # print("Este primul cardinal mai mare decat al doilea?")
                    if len(adjQueryNode) > len(adjCandidate):
                        # print("         Facut intersectiile si scaderile de la c3")
                        # print("         " + str(len(adjQueryNode)))
                        # print("         " + str(len(adjCandidate)))
                        # print("         Conditia(3) intra in vigoare, astfel avem:")
                        # print("         *Cardinalul primei intersectii cu scaderi este mai mare decat cea de-a doua. Se va sterge candidatul " + str(candidate) + ".")
                        if candidate in query_nodes_candidates_for_deletion:
                            query_nodes_candidates_for_deletion.remove(candidate)
                            self.respectare_conditie_3 = False
                            # print("         Candidatii lui " + str(query_node))
                            # print("         " + str(query_nodes_candidates_for_deletion))
                            # print()
                            # self.respectare_conditie_2 = False
                    else:
                        self.respectare_conditie_3 = True
                        # print("         Nu. Candidatul " + str(candidate) + " a trecut de toate cele 3 filtre / conditii.")
                    # print("         Candidatii finali ai lui " + str(query_node))
                    # print("         " + str(query_nodes_candidates_for_deletion))
                    # print()
        if len(query_nodes_candidates_for_deletion) == 0:
            return None
        # VECHI: Conditia 1 am adaptat-o pe loc mai sus.
        # Mai jos se afla si Conditia 2 si 3 functionale, dar fara blocari(trecerea la candidatul urmator) daca un candidat nu a trecut de o conditie, si fara verificari daca exista candidatul care trebuie eliminat.
        # De asemenea, nu folosesc o copie din care voi fi facut eliminarea de candidati, avand astfel un rezultat eronat.
        # print()
        # # for candidate in query_node_candidates:
        # # |Cq intersected with adj(u)| > |Cg intersected with adj(v)|
        # # print("Prima intersectie din conditia (2): ")
        # first_intersection = []
        # # print("adj(queryNode):")
        # adjQueryNode = sorted(list(self.adj(query_node, self.query_graph))) # Retin candidatii in ordine lexicografic crescatoare.
        # # print(adjQueryNode)
        # # print("Cq: ")
        # # print(Cq)
        # for xx in adjQueryNode:
        #     for yy in Cq[-1]:
        #         if xx == yy:
        #             first_intersection.append(xx)
        #
        # # print("A doua intersectie din conditia (2): ")
        # second_intersection = []
        # # print("adj(candidate):")
        # adjCandidate = sorted(list(self.adj(candidate, self.data_graph)))
        # # print(adjCandidate)
        # # print("Cg: ")
        # # print(Cg)
        #
        # for xx in adjCandidate:
        #     for yy in Cg[-1]:
        #         if xx == yy:
        #             second_intersection.append(xx)
        # # print("|Cq intersected with adj(u)| > |Cg intersected with adj(v)| ?")
        # # print(str(len(first_intersection)) + " > " + str(len(second_intersection)) + " ?")
        # if len(first_intersection) > len(second_intersection):
        #     print("     Se va sterge candidatul " + str(candidate) + ".")
        #     if candidate in query_node_candidates:
        #         query_node_candidates.remove(candidate)
        # print()
        #
        # print("Candidatii lui u2 actualizati in functie de conditia (1) si (2) al VF2: ")
        # print(query_node_candidates)

        # # Pentru fiecare candidat verificam si Conditia(3): prune out any vertex v in C(u) such that |adj(u) \ Cq \Mq| > |adj(v) \ Cg \Mg|
        # print()
        # print("Conditia(3): ")
        # # for candidate in query_node_candidates:
        # # print("|adj(u) \ Cq \Mq|:")
        # # print("adjQueryNode = " + str(adjQueryNode))
        # # print("Cq = " + str(Cq))
        # # print("Mq = " + str(Mq))
        # # print(type(adjQueryNode))
        # for cq_elem in Cq:
        #     for cq_elem_node in cq_elem:
        #         if cq_elem_node in adjQueryNode:
        #             adjQueryNode.remove(cq_elem_node)
        # for mq_elem_node in Mq:
        #     if mq_elem_node in adjQueryNode:
        #         adjQueryNode.remove(mq_elem_node)
        # # print("adjQueryNode = " + str(adjQueryNode))
        # # print("len(adjQueryNode) = " + str(len(adjQueryNode)))
        #
        # # print()
        # # print("|adj(v) \ Cg \Mg|:")
        # # print("adjCandidate = " + str(adjCandidate))
        # # print("Cg = " + str(Cg))
        # # print("Mg = " + str(Mg))
        # # print(type(adjCandidate))
        # for cg_elem in Cg:
        #     for cg_elem_node in cg_elem:
        #         if cg_elem_node in adjCandidate:
        #             adjCandidate.remove(cg_elem_node)
        # for mg_elem_node in Mg:
        #     if mg_elem_node in adjCandidate:
        #         adjCandidate.remove(mg_elem_node)
        # # print("adjCandidate = " + str(adjCandidate))
        # # print("len(adjCandidate) = " + str(len(adjCandidate)))
        # # print("|adj(u) \ Cq \Mq| > |adj(v) \ Cg \Mg| ?")
        # if len(adjQueryNode) > len(adjCandidate):
        #     if candidate in query_node_candidates:
        #         query_node_candidates.remove(candidate) # De pus si conditii in cazul in care nodul respectiv nu mai exista, daca a fost eliminat deja de una din primele doua conditii.
        # # print("Candidatii lui u2 actualizati in functie de conditia (1) si (2) al VF2: ")
        # # print(query_node_candidates)
        # print("---------------------\n")
        # print("------------SFARSIT EXECUTIE RAFINARE CANDIDATI-----------")
        return query_nodes_candidates_for_deletion

        # Adaug in M o noua asociere. Voi alege doar primul candidat din lista de candidati care au ramas dupa regulile de refinement.
        # self.M.append([query_node, query_node_candidates[0]])

    def getMatchList(self):
        return self.M

    def isJoinable(self, M, u, v):
        # VARIANTA PROPRIE care lucreaza cu proprietatea 'matched' adaugata nodurilor grafurilor atat query, cat si data.
        # print("IS JOINABLE EXEC:")
        # v5 trebuie sa fie cu matched = True pentru ca se afla deja in M
        # print(self.dataGraph.nodes(data=True))
        # print("u = " + str(u))
        # IsJoinable iterates through all adjacent query vertices of u.
        for query_neighbor in self.queryGraph.neighbors(u):
            # If the adjacent query vertex u' is already matched
            if self.queryGraph.nodes[query_neighbor]['matched'] is True:
                # print("ALREADY MATCHED query_neighbor = " + str(query_neighbor))
                # then it checks whether there is a corresponding edge (v, v') in the data graph.
                for data_node in self.dataGraph.nodes():
                    if self.dataGraph.nodes[data_node]['matched'] is True:
                        # print("NEW DATA NODE v = " + str(v))
                        # print("ALREADY MATCHED data_node = " + str(data_node))
                        if self.dataGraph.has_edge(v, data_node):
                            return True # !!! Aici se termina executia inainte devreme. Nu trebuie terminata la prima necorespondenta.
                        else:
                            continue

        # # VARIANTA VECHE care lucreaza cu lista M:
        # # print("Is joinable exec:")
        # # print("u: " + str(u))
        # # print("v: " + str(v))
        # # # for m_elem in M:
        # last_matching = M[-1]
        #
        # # print("Last matching: " + str(last_matching))
        # if query_graph.has_edge(u, last_matching[0]):
        #     # print("Has edge: " + str([u, last_matching[0]]))
        #     # print([v, last_matching[1]])
        #     # # for e in query_graph.edges.data():
        #     #     # print(e)
        #     # print(query_graph[u][last_matching[0]])
        #     # print(data_graph[v][last_matching[1]])
        #     if data_graph.has_edge(v, last_matching[1]) and query_graph[u][last_matching[0]]['label'] in data_graph[v][last_matching[1]]['label']:
        #         # print("Same labels!")
        #         return True

    def updateState(self, M, u, v): # Adaug o asociere / match la sfarsitul lui M.
        # print("updateState exec: ")
        self.queryGraph.nodes[u]['matched'] = True
        # self.dataGraph.node[v]['matched'] = True # Am declarat si nodul data ca fiind MATCHED. In p133-han se lucreaza cu lista M, exista nextQueryVertex, dar prea putin se ocupa de nodurile data din acest pct de vedere.
        # print(Fore.BLUE + str([u,v]))
        M.append([u, v])
        # print(Fore.LIGHTMAGENTA_EX + "Updated M: " + str(M))
        # print(Style.RESET_ALL)
        # print(str(self.queryGraph.nodes(data=True)))
        # print("updateState exec finish")
        end_program = True
        for query_node in self.queryGraph.nodes():
            if self.queryGraph.nodes[query_node]['matched'] == False:
                end_program = False
        if end_program == False:
            return M
        else:
            # print(Fore.GREEN + Style.BRIGHT + "VF2 results: ")
            # for r in self.results_dict.items():
            #     print(r)
            # print(Style.RESET_ALL)
            return

    def restoreState(self, M, u, v): # Inlatur o asociere / match din M, care in acest caz, cautand perechea [u, v], ar trebui sa o elimine, si in acelasi timp, perechea eliminata sa fie cea adaugata de
                                     # updateState, adica ultima pereche.
        M.remove([u, v])
        # SAU pentru a elimina ultimul element:
        # M.remove(M[-1])

     #SAU restoreState: Trebuie sa dau si valoarea False indicativului 'matched' nodurilor u si v.

    def adj(self, u, graph):
        return graph.neighbors(u)
    # def adj(self, u, dataGraphDict):
    #     adjacentVertices = []
    #     # print("----------")
    #     # print("Inceput apel metoda adj(): ")
    #     # print("Parametrul de intrare u:")
    #     # print(u)
    #     # print("Tipul parametrului: ")
    #     # print(type(u))
    #     # print(u.getNeighbors())
    #     adjacentVertices.append(u.getNeighbors())
    #     # print("adjacentVertices variable from adj() method: ")
    #     # print(adjacentVertices)
    #     # print("Sfarsit apel metoda adj().")
    #     # print("----------")
    #     return adjacentVertices

# # Afisam muchiile grafurilor query si data.
# print("Muchiile grafului query:")
# for edge in queryGraph.edges():
#     print(edge)
# print()
# print("Muchiile grafului data:")
# for edge in dataGraph.edges():
#     print(edge)
# print()
#
# # Initializam o instanta a algoritmului.
# vf2 = VF2Algorithm(queryGraph, dataGraph)
# # Afisam candidatii fiecarui nod query
# for x in queryGraph.nodes():
#     print("Candidati pentru nodul: " + x)
#     print(vf2.filterCandidates(x, queryGraph, dataGraph))
# print()
# # Rulam metoda de rafinare a candidatilor
# # print("Valoare returnata de refineCandidates(): " + str(vf2.refineCandidates(queryGraph, dataGraph))) # Nu trece la alt nod query pana nu facem o asociere si o adaugam in M
# vf2.refineCandidates(queryGraph, dataGraph)
# print()
# print("Lista de asocieri:")
# M = []
# # M.append(vf2.getMatchList())
# M = vf2.getMatchList()
# for m_elem in M:
#     print(m_elem)


# De cuprins in metoda refineCandidates:
# Mq = [] # Set of matched query vertices
# Mg = [] # Set of matched data vertices
# Cq = [] # Set of adjacent and not-yet-matched query vertices connected from Mq
# Cg = [] # Set of adjacent and not-yet-matched data vertices connected from Mg
# M = [] # Partial solution of matchings

# Aici va fi etapa de backtracking in care se aleg cuplari intre cele doua grafuri si vor fi cuprinse in solutia partiala M, care la sfarsit va deveni solutia completa.
# for x in VF2QueryGraphDict.keys():
#     print("Candidates for node: " + VF2QueryGraphDict.get(x).getVertexID())
#     for y in VF2DataGraphDict.keys():
#         if VF2QueryGraphDict.get(x).getVertexLabel() in VF2DataGraphDict.get(y).getVertexLabel():
#             # print("Is candidate")
#             # print(VF2DataGraphDict.get(y))
#             print("Current partial solution: ")
#             M.append([VF2QueryGraphDict.get(x).getVertexID(), VF2DataGraphDict.get(y).getVertexID()])
#             # (1)
#             # (2)
#             # (3)
#             print(M)

# # Exemplu lucrat si HARDCODED din articolul p133-han care de asemenea l-am derulat pe hartie:
# print("Exemplu lucrat: ")
# print("Conditia (1): Prune out v belonging to c(u) such that a vertex v is not connected from already matched data vertices. \n AICI: Prune out v7 because it is not connected to any vertex in Mg.")
# print("Solutie partiala curenta (prima corespondenta functioneaza tot timpul):")
# M.append(["u1", "v4"])
# print(M)
# print("Urmatorul nod query (va fi metoda): u2")
# candidates_u2 = vf2.c("u2", queryGraph, dataGraph)
# print("Candidati pentru nodul u2: ")
# print(candidates_u2)
# Mq.append(M[0][0])
# Mg.append(M[0][1])
# Cq.append(list(vf2.adj("u1", queryGraph))) # Aici ar fi bine sa se apeleze adj() de nodul u1 din multimea Mq, nu direct din dictionar.
# Cg.append(list(vf2.adj("v4", dataGraph)))
# print("Mq = " + str(Mq))
# print("Mg = " + str(Mg))
# print("Cq = " + str(Cq))
# print("Cg = " + str(Cg))
#
# # Prune out v belonging to c(u) such that a vertex v is not connected from already matched data vertices
# for candidate in candidates_u2:
#     for matching in M:
#         if dataGraph.has_edge(candidate, matching[1]) is False:
#             print("Nu exista muchie intre " + str(candidate) + " " + str(matching[1]) + ". Se va sterge candidatul " + str(candidate) + ".")
#             candidates_u2.remove(candidate)
#
# # AICI AM INTELES GRESIT PRIMA CONDITIE, ASTFEL FACEAM PRUNING DUPA PRIMA REGULA CARE ERA GRESITA.
# # for x in Mg:
# #     print("Elemente enumerate din Mg:")
# #     print(x)
# #     print("Afisare noduri adiacente (vecini) pentru elementul din Mg: ")
# #     print(list(vf2.adj(x, dataGraph))[0])
# #     # (1) Daca v7 nu se afla in multimea vecinilor elementului din Mg, eliminam v7 din candidati
# #     for y in candidates_u2:
# #         print("Candidat al lui u2: ")
# #         print(y)
# #         print("Se afla acest candidat in vecinii elementului din Mg?")
# #         if y not in list(vf2.adj(x, dataGraph))[0]: # Vector. Accesam valoarea de pe pozitia [0] care este la randul ei un sir de elemente. Tablou multidimensional.
# #             candidates_u2.remove(y)
# #             print("YES. Removed from candidates of u2.") #???!!! Nu verifica v8 care este ultimul candidat!
# #         else:
# #             print("NO")
# print("Candidatii lui u2 actualizati in functie de conditia (1) al VF2: ")
# print(candidates_u2)
#
# print()
# print("Conditia(2): Prune out any vertex v in c(u) such that |Cq intersected with adj(u)| > |Cg intersected with adj(v)|")
# print("adj(u2):")
# adjU2 = list(vf2.adj("u2", queryGraph))
# print(adjU2)
# print("Cq: ")
# print(Cq)
#
# # |Cq intersected with adj(u)| > |Cg intersected with adj(v)| !!! Va trebui sa adaug compararea rezultatelor celor doua intersectii: daca rezultatul primei are elemente mai multe decat rezultatul celei de a doua.
#
# print("Prima intersectie din conditia (2): ")
# first_intersection = []
# for x in adjU2:
#     # print("x in adj(u2): ")
#     # print(x)
#     # for y in cq_Mg_u1:
#     for y in Cq[0]:
#         if x == y:
#             first_intersection.append(x)
#
# print("A doua intersectie din conditia (2): ")
# second_intersection = []
# print("adj(v8):")
# adjV8 = list(vf2.adj("v8", dataGraph))
# print(adjV8)
# print("Cg: ")
# print(Cg)
#
# for x in adjV8:
#     for y in Cg[0]:
#         if x == y:
#             second_intersection.append(x)
# print()
# print("|Cq intersected with adj(u)| > |Cg intersected with adj(v)| ?")
# if len(first_intersection) > len(second_intersection):
#     candidates_u2.remove("v8")
# print("Candidatii lui u2 actualizati in functie de conditia (1) si (2) al VF2: ")
# print(candidates_u2)
#
# print()
# print("Conditia(3): prune out any vertex v in C(u) such that |adj(u) \ Cq \Mq| > |adj(v) \ Cg \Mg|")
# print("|adj(u) \ Cq \Mq|:")
# print("adjU2 = " + str(adjU2))
# print("Cq = " + str(Cq))
# print("Mq = " + str(Mq))
# print(type(adjU2))
# for cq_elem in Cq:
#     for cq_elem_node in cq_elem:
#         # print(cq_elem_node)
#         if cq_elem_node in adjU2:
#             adjU2.remove(cq_elem_node)
# for mq_elem_node in Mq:
#     if mq_elem_node in adjU2:
#             adjU2.remove(mq_elem_node)
# print("adjU2 = " + str(adjU2))
# print("len(adjU2) = " + str(len(adjU2)))
#
# print()
# print("|adj(v) \ Cg \Mg|:")
# print("adjV8 = " + str(adjV8))
# print("Cg = " + str(Cg))
# print("Mg = " + str(Mg))
# print(type(adjV8))
# for cg_elem in Cg:
#     for cg_elem_node in cg_elem:
#         if cg_elem_node in adjV8:
#             adjV8.remove(cg_elem_node)
# for mg_elem_node in Mg:
#     if mg_elem_node in adjV8:
#         adjV8.remove(mg_elem_node)
# print("adjV8 = " + str(adjV8))
# print("len(adjV8) = " + str(len(adjV8)))
# print("|adj(u) \ Cq \Mq| > |adj(v) \ Cg \Mg| ?")
# if len(adjU2) > len(adjV8):
#     candidates_u2.remove()


# VECHI: initializarea grafului cu clasa Vertex scrisa de mine.
# Graful query
# u1 = Vertex("A", "u1")
# u2 = Vertex("B", "u2")
# u3 = Vertex("C", "u3")
# u4 = Vertex("A", "u4")
#
# u1.setEdgeUndirected("AB", "u2")
# u1.setEdgeUndirected("AA", "u4")
# u2.setEdgeUndirected("BA", "u1")
# u2.setEdgeUndirected("BA", "u4")
# u2.setEdgeUndirected("BC", "u3")
# u3.setEdgeUndirected("CB", "u2")
# u4.setEdgeUndirected("AB", "u2")
# u4.setEdgeUndirected("AA", "u1")

# Graful data
# v1 = Vertex("A", "v1") # ID-ul este de tipul str
# v2 = Vertex("B", "v2")
# v3 = Vertex("A", "v3")
# v4 = Vertex("A", "v4")
# v5 = Vertex("B,D", "v5")
# v6 = Vertex("A", "v6")
# v7 = Vertex("B,C", "v7")
# v8 = Vertex("B", "v8")
# v9 = Vertex("C", "v9")
#
# v1.setEdgeUndirected("b", "v4")
# v2.setEdgeUndirected("a", "v4")
# v2.setEdgeUndirected("b", "v5")
# v3.setEdgeUndirected("a", "v5")
# v3.setEdgeUndirected("b", "v6")
# v4.setEdgeUndirected("b", "v1")
# v4.setEdgeUndirected("a", "v2")
# v4.setEdgeUndirected("a", "v5")
# v4.setEdgeUndirected("a", "v8")
# v5.setEdgeUndirected("a", "v4")
# v5.setEdgeUndirected("b", "v2")
# v5.setEdgeUndirected("a", "v3")
# v5.setEdgeUndirected("a", "v6")
# v5.setEdgeUndirected("b", "v9")
# v6.setEdgeUndirected("a", "v5")
# v6.setEdgeUndirected("b", "v3")
# v7.setEdgeUndirected("b", "v8")
# v8.setEdgeUndirected("a", "v4")
# v8.setEdgeUndirected("b", "v7")
# v9.setEdgeUndirected("b", "v5")

# VF2QueryGraphDict = {}
# VF2QueryGraphDict = {"u1": u1,
#                      "u2": u2,
#                      "u3": u3,
#                      "u4": u4}
#
# # VF2DataGraphDict = {v1.getVertexLabel():v1,
# #                     v2.getVertexLabel():v2,
# #                     v3.getVertexLabel():v3,
# #                     v4.getVertexLabel():v4,
# #                     v5.getVertexLabel():v5,
# #                     v6.getVertexLabel():v6,
# #                     v7.getVertexLabel():v7,
# #                     v8.getVertexLabel():v8,
# #                     v9.getVertexLabel():v9}
#
# VF2DataGraphDict = {"v1":v1,
#                     "v2":v2,
#                     "v3":v3,
#                     "v4":v4,
#                     "v5":v5,
#                     "v6":v6,
#                     "v7":v7,
#                     "v8":v8,
#                     "v9":v9}

# # Afisam etichetele nodurilor grafului query si celui data.
# for x in VF2QueryGraphDict.keys():
#     print(VF2QueryGraphDict.get(x).getVertexLabel())
# print()
# for x in VF2DataGraphDict.keys():
#     print(VF2DataGraphDict.get(x).getVertexLabel())
# print()

# for x in VF2QueryGraphDict.keys():
#     print("Candidates for node: " + VF2QueryGraphDict.get(x).getVertexID())
#     for y in VF2DataGraphDict.keys():
#         if VF2QueryGraphDict.get(x).getVertexLabel() in VF2DataGraphDict.get(y).getVertexLabel():
#             # print("Is candidate")
#             print(VF2DataGraphDict.get(y).getVertexID())
#
# # Urmatorul nod query

# # Rafinarea candidatilor
# Mq = []
# Mg = []
# Cq = []
# Cg = []
#
# print()
# # print("Folosind metoda c(u) pentru obtinerea candidatilor unui nod din graful query: ")
# vf2 = VF2Algorithm()
# # print(vf2.c(VF2QueryGraphDict.get(4), VF2DataGraphDict))
#
# M = []
#
# # Aici va fi etapa de backtracking in care se aleg cuplari intre cele doua grafuri si vor fi cuprinse in solutia partiala M, care la sfarsit va deveni solutia completa.
# # for x in VF2QueryGraphDict.keys():
# #     print("Candidates for node: " + VF2QueryGraphDict.get(x).getVertexID())
# #     for y in VF2DataGraphDict.keys():
# #         if VF2QueryGraphDict.get(x).getVertexLabel() in VF2DataGraphDict.get(y).getVertexLabel():
# #             # print("Is candidate")
# #             # print(VF2DataGraphDict.get(y))
# #             print("Current partial solution: ")
# #             M.append([VF2QueryGraphDict.get(x).getVertexID(), VF2DataGraphDict.get(y).getVertexID()])
# #             # (1)
# #             # (2)
# #             # (3)
# #             print(M)
#
# # Hardcode exemplu din articolul p133-han care de asemenea l-am derulat pe hartie:
# print("Exemplu lucrat: ")
# print("Conditia (1): Prune out v belonging to c(u) such that a vertex v is not connected from already matched data vertices. \n AICI: Prune out v7 because it is not connected to any vertex in Mg.")
# print("Current partial solution (first match always works): ")
# M.append([VF2QueryGraphDict.get("u1").getVertexID(), VF2DataGraphDict.get("v4").getVertexID()]) # Ce tip are VertexID? str?
# print(M)
# print("Next query vertex (will be a method): " + VF2QueryGraphDict.get("u2").getVertexID())
# print("Candidates for " + str(VF2QueryGraphDict.get("u2").getVertexID()) + ": " + str(vf2.c(VF2QueryGraphDict.get("u2"), VF2DataGraphDict)))
# Mq.append(M[0][0])
# Mg.append(M[0][1])
# Cq.append(vf2.adj(VF2QueryGraphDict.get("u1"), VF2QueryGraphDict)) # Aici ar fi bine sa se apeleze adj() de nodul u1 din multimea Mq, nu direct din dictionar.
# Cg.append(vf2.adj(VF2DataGraphDict.get("v4"), VF2DataGraphDict))
# print("Mq = " + str(Mq))
# print("Mg = " + str(Mg))
# print("Cq = " + str(Cq))
# print("Cg = " + str(Cg))
#
# # print("------------------------------------------------------")
# # for x in vf2.c(VF2QueryGraphDict.get("u2"), VF2DataGraphDict): # Aici apelez cu tipul de valoare Vertex
# #     print(x)
# # print("Valoare Mg[0]: ")
# # print(Mg[0])
# # print("Tipul Mg[0]: ")
# # print(type(Mg[0]))# De tipul str
# # print()
# # print("Apelare adj() folosind primul element din multimea Mg.") # Dupa apelul metodei adj() in care au loc printuri, va avea loc si printul de mai jos:
# # print(vf2.adj(VF2DataGraphDict.get(Mg[0]), VF2DataGraphDict)) # Trebuie furnizat tipul Vertex, nu str care este Mg[0]. Asa ca am folosit Mg[0] ca si cheie pentru cautarea in dictionar.
# # print("------------------------------------------------------")
#
# candidatesU2 = vf2.c(VF2QueryGraphDict.get("u2"), VF2DataGraphDict)
#
# for x in Mg:
#     print("Elemente enumerate din Mg:")
#     print(x)
#     print("Afisare noduri adiacente (vecini) pentru elementul din Mg: ")
#     print(vf2.adj(VF2DataGraphDict.get(x), VF2DataGraphDict)[0])
#     # (1) Daca v7 nu se afla in multimea vecinilor elementului din Mg, eliminam v7 din candidati
#     for y in candidatesU2:
#         print("Candidat al lui u2: ")
#         print(y)
#         print("Se afla acest candidat in vecinii elementului din Mg?")
#         if y not in vf2.adj(VF2DataGraphDict.get(x), VF2DataGraphDict)[0]: # Vector. Accesam valoarea de pe pozitia [0] care este la randul ei un sir de elemente. Tablou multidimensional.
#             # Mg.remove(vf2.c(VF2QueryGraphDict.get("u2"), VF2DataGraphDict))
#             candidatesU2.remove(y)
#             print("YES. Removed from candidates of u2.") #!!! Nu verifica v8 care este ultimul candidat!
#         else:
#             print("NO")
# print("Candidatii lui u2 actualizati in functie de conditia (1) al VF2: ")
# print(candidatesU2)
#
# print()
# print("Conditia(2): Prune out any vertex v in c(u) such that |Cq intersected with adj(u)| > |Cg intersected with adj(v)|")
# print("adj(u2): ")
# adjU2 = vf2.adj(VF2QueryGraphDict.get("u2"), VF2QueryGraphDict)[0]
# print(adjU2)
# print("Cq: ")
# cq_Mg_u1 = Cq[0][0] # !!! In tabloul Cq, elementul de pe pozitia [0][0] este lista dorita, si anume nodurile adiacente elementului u1 din Mq. Un element cu doua coordonate este o lista. De rectificat tabloul multidimesnional la unul unidimensional, daca este nevoie.
# print(cq_Mg_u1)
#
# # |Cq intersected with adj(u)| > |Cg intersected with adj(v)| !!! Va trebui sa adaug compararea rezultatelor celor doua intersectii: daca rezultatul primei are elemente mai multe decat rezultatul celei de a doua.
#
# print("Prima intersectie din conditia (2): ")
# for x in adjU2:
#     # print("x in adj(u2): ")
#     # print(x)
#     for y in cq_Mg_u1:
#         if x == y:
#             print(x)
#         # print("y in cq_Mg_u1")
#         # print(y)
# print("A doua intersectie din conditia (2): ")
# print("adj(v8)")
# adjV8 = vf2.adj(VF2DataGraphDict.get("v8"), VF2DataGraphDict)[0]
# print(adjV8) # !!! Afiseaza doar v7. Ar trebui sa afiseze v4 si v7
# print("Cg: ")
# cg_Mg_v4 = Cg[0][0]
# print(cg_Mg_v4)
# indice_de_intersectie = 0 # Daca acesta va fi egal cu valoarea 1, atunci inseamna ca intersectia celor doua multimi are cel putin un element comun. Alfel avem rezultatul nul.
#                           # Conform acestui indice vom decide daca vom inlatura elementul v8 in acest caz din lista de candidati al nodului u2 din graful query.
# element_eliminat = None
# for x in adjV8:
#     for y in cg_Mg_v4:
#         if x == y:
#             print(x)
#             indice_de_intersectie = 1
#         else:
#             print("Intersectia returneaza null")
# #             candidatesU2.remove() # !!! Se va inlatura v8. Vreau sa fac acest lucru in mod dinamic. Trebuie selectat v8 fara a fi hardcodat.
#
# print("---------------------------------------")
# print("VF2DataGraphDict.get(v8): ")
# print(VF2DataGraphDict.get("v8").getVertexID())
# print("indice_de_intersectie: ")
# print(indice_de_intersectie)
# print("candidatesU2: ")
# print(candidatesU2[2])
# print("type(candidatesU2): ")
# print(type(candidatesU2[2]))
# print("---------------------------------------")
#
# if indice_de_intersectie == 0:
#     candidatesU2.remove(VF2DataGraphDict.get("v8").getVertexID())
#
# print("Lista de candidati al nodului u2 actualizata dupa conditiile (1) si (2)")
# print(candidatesU2)
#
# print()
# print("Conditia (3): Prune out any vertex v in c(u) such that |adj(u) \ Cq \ Mq| > |adj(v) \ Cg \ Mg|")
# print("adj(u2):")
# print(adjU2)
# print("Cq: ")
# print(Cq[0][0])
# print("Mq: ")
# print(Mq)
# for x in adjU2:
#     for y in Cq[0][0]:
#         if x == y:
#             adjU2.remove(x)
# print("adj(u2) dupa prima eliminare adj(u) \ Cq:")
# print(adjU2)
# for x in adjU2:
#     for y in Mq:
#         if x == y:
#             adjU2.remove(x)
# print("adj(u2) dupa a doua eliminare adj(u) \ Cq \ Mq:")
# print(adjU2)
#
# print()
# print("adj(v2): ")
# adjV2 = vf2.adj(VF2DataGraphDict.get("v2"), VF2DataGraphDict)[0]
# print(adjV2)
# print("Cg: ")
# print(Cg[0][0])
# print("Mg: ")
# print(Mg)
#
# for x in adjV2:
#     for y in Cg[0][0]:
#         if x == y:
#             adjV2.remove(x)
# print("adj(v2) dupa prima eliminare adj(v) \ Cg:")
# print(adjV2)
# for x in adjV2:
#     for y in Mg:
#         if x == y:
#             adjV2.remove(x)
# print("adj(v2) dupa prima eliminare adj(v) \ Cg \ Mg:")
# print(adjV2)
#
# if len(adjU2) > len(adjV2):
#     candidatesU2.remove(VF2DataGraphDict.get("v2").getVertexID())
#
# print()
# print(candidatesU2)