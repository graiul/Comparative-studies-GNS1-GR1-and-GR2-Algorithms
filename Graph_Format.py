import random

import networkx as nx

# Avem doua tipuri de fisiere:
#   1) fisier care contine un singur graf mare,
#   2) fisier care contine mai multe grafuri(de asemenea numit graph database).

class Graph_Format:
    lines = []
    graph = nx.Graph()
    subgraph_database = []
    # ID_gen = 0
    filename = None

    def __init__(self, filename=None): # Simulare polimorfism pentru constructor.
        if filename is None:
            # print("No filename constructor")
            pass
        else:
            self.filename = filename
            # print(self.filename)
            with open(self.filename) as f:
                self.lines = f.readlines()


        # # Atribuire numere de identificare unice pentru noduri si muchii.
        # nodeLabelsDict = {}
        # random_num_list = [0, 1, 2, 3, 4, 5]
        # for node in self.graph.nodes():
        # #     nodeLabelsDict[node] = str(node)
        #     nodeLabelsDict[node] = random.sample(random_num_list, 1)
        # # nx.set_node_attributes(self.graph, nodeLabelsDict, 'label')
        # nx.set_node_attributes(self.graph, nodeLabelsDict, 'type')
        # # print(self.graph.nodes(data=True))
        #
        #
        # edgeLabelsDict={}
        # for edge in self.graph.edges():
        #     edgeLabelsDict[edge] = str(edge[0])+str(edge[1])
        # nx.set_edge_attributes(self.graph, edgeLabelsDict, 'uniqueID')
        #
        # for edge in self.graph.edges(data=True):
        #     print(edge)


    def display_file(self):
        for line in self.lines:
            print(line)

    # def read_file_hossam(self, filename):
        # for line in self.lines:
        #     newLine = line.rsplit(sep=" ")
        #     # print(newLine)
        #     # if "*Arcs" in newLine:
        #     #     print("ARCS")
        #     firstElem = newLine[0]
        #     secondElem = newLine[1]
        #     # print(secondElem)
        #     trimmedSecondElem = secondElem.rsplit(sep="\n")
        #     # if "Vertices" in firstElem:
        #     #     if "Arcs" not in firstElem:
        #     #         print("yes")
        #     # else:
        #     self.graph.add_edge(firstElem, trimmedSecondElem[0], uniqueID=None)  # Eticheta compusa; pentru fiecare muchie, are tipul "list".
        #     # self.ID_gen = self.ID_gen + 1
        #     # print(self.ID_gen)


    # def write_new_file_hossam(self):
    #     f = open("reformated_graf.txt", "w+")
    #     nr_nodes = len(self.graph.nodes())
    #     nr_edges = len(self.graph.edges())
    #     f.write("Vertices %d " % nr_nodes)
    #     f.write("Edges %d\n" % nr_edges)
    #     for node in self.graph.nodes(data=True):
    #         f.write(str(node) + "\n")
    #     for edge in self.graph.edges(data=True):
    #         f.write(str(edge) + "\n")
    #         # print(edge)

    def write_new_file_for_gSpan(self, subgraph_database):
        graph_counter = 0
        random_num_list = [0, 1, 2, 3, 4, 5]
        f = open("gSpan-master by betterenvi/gSpan-master/graphdata/input_for_gSpan.txt", "w+")

        for subgraph in subgraph_database:
            # f = open("reformated_graf_for_gSpan_number_%d.txt" % graph_counter, "w+")
            f.write("t # %d\n" % graph_counter)
            for node in sorted(subgraph.nodes(data=True)):
                # print(node[1]["type"][0]) # Selectam dictionarul nodului, cheia, si valoarea. Aici valoarea reprezinta tipul nodului. Necesar un numar mic de tipuri ale nodurilor si muchiilor pentru gSpan.
                # print(subgraph.node[node]['type'])
                f.write('{0} {1} {2}\n'.format("v", node[0], node[1]["label"][0])) # Aici trebuie generalizat: se trece nodul si eticheta trebuie luata din proprietatea nodului.

            for edge in sorted(subgraph.edges(data=True)):
                f.write('{0} {1} {2} {3}\n'.format("e", edge[0], edge[1], random.sample(random_num_list, 1)[0]))
            graph_counter = graph_counter + 1
        f.write("t # -1")
            # f.close()

    # Folosit pentru date de tipul RI. Era nevoie de un counter pana la valoarea 10 ?!
    # Aceasta metoda interpreteaza output gSpan din setul RI query sau data, care nu au etichete la muchii.
    def get_graph_db_from_gSpan_output_file(self): # Se ruleaza dupa gSpan.
                                                                      # Exista un singur tip de output gSpan, deci metoda poate fi folosita
                                                                      # in cazul oricarui format de graf dat ca si input pt gSpan.

        new_subgraph_database = []
        # count_graph = 0 # !!! De ce sa numar doar 10 pattern-uri???
        new_graph = nx.Graph(gSpan_graph_ID=None, support=None, where=None)
        # print("Output gSpan:")
        for line in self.lines:
            # print(line)
            # if count_graph <= 9: # !!! De ce sa numar doar 10 pattern-uri???
            if "t #" in line:
                # print("YES")
                new_graph.graph['gSpan_graph_ID'] = line
                # print(list(new_graph.graph.values())[0])
            if "e " in line:
                sep_line = line.split(" ")
                # print(sep_line[0])
                new_graph.add_edge(sep_line[1], sep_line[2], uniqueID=str(str(sep_line[1]+str(sep_line[2]))), label=sep_line[3]) #
            if "Support:" in line:
                # count_graph = count_graph + 1
                sep_line = line.split(" ")
                new_graph.graph['support'] = sep_line[1]
                # print(new_graph.edges(data=True))
                # new_subgraph_database.append(new_graph)
                # new_graph = nx.Graph(gSpan_graph_ID=None, support=None)
            if "where: [" in line:
                sep_line = line.split(", ")
                # print("where line:")
                sep_line[0]= sep_line[0].split("where: [")[1]
                sep_line[len(sep_line)-1] = sep_line[len(sep_line)-1].split("]\n")[0]
                int_sep_line = []
                for elem in sep_line:
                    int_sep_line.append(int(elem))
                # print(int_sep_line)
                new_graph.graph['where'] = int_sep_line
                new_subgraph_database.append(new_graph)
                new_graph = nx.Graph(gSpan_graph_ID=None, support=None, where=None)

        for graph in new_subgraph_database:
            print(graph.graph)
            print(graph.edges(data=True))
        return new_subgraph_database

    # Aceasta metoda interpreteaza output gSpan din setul p133han query sau data, care au etichete la muchii.
    def get_graph_db_from_gSpan_output_file_from_p133han(self):
        # print("Executie get_graph_db_from_gSpan_output_file_from_p133han")
        # print(self.filename)
        new_subgraph_database = []
        new_graph = nx.Graph(gSpan_graph_ID=None, support=None, where=None)
        # print("Output gSpan:")
        for line in self.lines:
            # print(line)
            if "t # " in line:
                # print("YES")
                new_graph.graph['gSpan_graph_ID'] = line.split("\n")[0]
                # print(line.split("\n")[0])
                # print(list(new_graph.graph.values())[0])
            if "e " in line:
                sep_line = line.split(" ")
                # print(sep_line[0])
                new_graph.add_edge(sep_line[1], sep_line[2], uniqueID=str(str(sep_line[1]+str(sep_line[2]))), label="0") #sep_line[3].split("\n")[0])
                # print(new_graph.graph)
            if "Support: " in line:
                # count_graph = count_graph + 1
                sep_line = line.split(" ")
                new_graph.graph['support'] = sep_line[1].split("\n")[0]
                # print(new_graph.edges(data=True))
                # new_subgraph_database.append(new_graph)
                # new_graph = nx.Graph(gSpan_graph_ID=None, support=None)
            if "where: [" in line:
                sep_line = line.split(", ")
                # print("where line:")
                sep_line[0]= sep_line[0].split("where: [")[1]
                sep_line[len(sep_line)-1] = sep_line[len(sep_line)-1].split("]\n")[0]
                int_sep_line = []
                for elem in sep_line:
                    int_sep_line.append(int(elem))
                # print(int_sep_line)
                new_graph.graph['where'] = int_sep_line
                # print("new_graph")
                # print(new_graph.edges)
                new_subgraph_database.append(new_graph)
                new_graph = nx.Graph(gSpan_graph_ID=None, support=None, where=None)

        # print()
        # for graph in new_subgraph_database:
        #     print(graph.graph)
            # print(graph.edges(data=True))
        number=0
        for graph_to_renumber in new_subgraph_database:
            graph_to_renumber.graph['gSpan_graph_ID'] = "t # " + str(number)
            number = number + 1
        # print()
        # for graph in new_subgraph_database:
        #     print(graph.graph)
        return new_subgraph_database

    # RI db inseamna RI database, si reprezinta toate grafurile RI, care au un format aparte.
    # Nu are a face cu subgra[h_database, cele 100 de intersectii din GADDI.
    def create_graph_from_RI_file(self):
        # DETALII FORMAT din RI-Datasets.tar\RI-Datasets\PPI\DESCRIPTION.txt
        # Undirect graphs
        #
        # Format:
        #
        # # GraphName
        # NumberOfNodes
        # NodesAttributesList
        # ...
        # NumerOfEdges
        # Source
        # Target
        #--------------------------------------------------------------------
        # nx pastreaza ordinea nodurilor din fisierul text, chiar daca acestea sunt exprimate doar prin muchii.
        # Fiind graf neorientat, nx injumatateste automat numarul de muchii stocat in obiectul de tipul Graph.
        # Lista de etichete are numarul de elemente egal cu numarul de noduri, dar aceasta este lista care poate fi atribuita direct nodurilor, numarul de etichete unice fiind in realitate mult mai mic, si anume 32,
        # avand o distribuire uniforma asupra nodurilor.
        input_graph = nx.Graph()
        # print("Input graph name: " + str(self.lines[0]))
        num_nodes = int(self.lines[1])
        # print("Number of nodes: " + str(num_nodes))
        nodes_attr_list = []
        # for line in self.lines:
        #     if "ENSP" in line:
        #         spl = line.split(sep="\n")
        #         nodes_attr_list.append(spl[0])
        for i in range(2,num_nodes+2):
            spl = self.lines[i].split(sep="\n")[0]
            nodes_attr_list.append(spl)
        # print("Nodes attributes number: " + str(len(nodes_attr_list)))
        num_edges = int(self.lines[num_nodes+2])
        # print("Number of edges: " + str(num_edges))
        # print("Input graph edges: ")
        edge_list = []
        for i in range(num_nodes+3, len(self.lines)):
            line = [self.lines[i].split(sep="\n")[0], self.lines[i].split(sep="\n")[1]]
            new_edge = tuple(line[0].split(sep=" "), )
            edge_list.append(new_edge)
        # print(edge_list)
        # print(len(edge_list))
        input_graph.add_edges_from(edge_list)
        # Pentru graf neorientat, nx creeaza graful cu doar jumatate din muchiile din edge_list, adica daca avem muchia (a,b), nu are rost sa adauge in graf si (b,a).
        # print(input_graph.edges())
        # print("Input graph number of edges: ")
        # print(len(input_graph.edges()))
        # print("Input graph nodes: ")
        # print(input_graph.nodes())
        # print("Input graph number of nodes: ")
        # print(len(input_graph.nodes()))
        # print("Node attributes list: ")
        # print(nodes_attr_list)
        node_attr_dict = dict(zip(input_graph.nodes(), nodes_attr_list))
        # print(node_attr_dict)
        nx.set_node_attributes(input_graph, node_attr_dict,'label')
        # print(sorted(input_graph.nodes(data=True)))
        # print(len(input_graph.nodes()))
        # print(len(input_graph.edges()))
        self.graph = input_graph

    # def create_RI_file_from_graph(self, graph): # L-am folosit ca sa creez un graf query din graful RI numit Homo_sapiens_udistr_32.gfd
    #     f = open("gSpan-master by betterenvi/gSpan-master/graphdata/graph_to_RI_db.txt", "w+")
    #     f.write("#Homo_sapiens_query_graph\n")
    #     f.write(str(len(graph.nodes)) + "\n")
    #     for n in graph.nodes():
    #         f.write(graph.node[n]['label'] + "\n")
    #     f.write(str(len(graph.edges)) + "\n")
    #     for e in graph.edges:
    #         f.write(e[0] + " " + e[1] + "\n")

    def write_new_file_for_gSpan_from_RI_subgraph_db(self, subgraph_database):
        # Grafurile din RI nu au etichete pentru muchii, doar pentru noduri. Dar pentru ca gSpan by betterenvi are nevoie de etichete si pentru muchii, vom atribui eticheta "0" pentru fiecare muchie.
        graph_counter = 0
        # f = open("gSpan-master by betterenvi/gSpan-master/graphdata/input_for_gSpan.txt", "w+")
        f = open('dataset_RI\gSpan_input\input_for_gSpan.txt', "w+")

        for subgraph in subgraph_database:
            # f = open("reformated_graf_for_gSpan_number_%d.txt" % graph_counter, "w+")
            f.write("t # %d\n" % graph_counter)
            for node in sorted(subgraph.nodes(data=True)):
                # print(node[1]["type"][0]) # Selectam dictionarul nodului, cheia, si valoarea. Aici valoarea reprezinta tipul nodului. Necesar un numar mic de tipuri ale nodurilor si muchiilor pentru gSpan.
                # print(subgraph.node[node]['type'])
                f.write('{0} {1} {2}\n'.format("v", node[0], node[1]["label"][0]))  # Aici trebuie generalizat: se trece nodul si eticheta trebuie luata din proprietatea nodului.

            for edge in sorted(subgraph.edges(data=True)):
                f.write('{0} {1} {2} {3}\n'.format("e", edge[0], edge[1], "0"))
            graph_counter = graph_counter + 1
        f.write("t # -1")
        # f.close()

    def create_graph_from_p133han_file(self): # Asemanator cu formatul RI, dar cu etichete pentru muchii.
        # DETALII FORMAT din RI-Datasets.tar\RI-Datasets\PPI\DESCRIPTION.txt
        # Undirect graphs
        #
        # Format:
        #
        # # GraphName
        # NumberOfNodes
        # NodesAttributesList
        # ...
        # NumerOfEdges
        # Source
        # Target
        # --------------------------------------------------------------------
        # nx pastreaza ordinea nodurilor din fisierul text, chiar daca acestea sunt exprimate doar prin muchii.
        # Fiind graf neorientat, nx injumatateste automat numarul de muchii stocat in obiectul de tipul Graph.
        # Lista de etichete are numarul de elemente egal cu numarul de noduri, dar aceasta este lista care poate fi atribuita direct nodurilor, numarul de etichete unice fiind in realitate mult mai mic, si anume 32,
        # avand o distribuire uniforma asupra nodurilor.
        input_graph = nx.Graph()
        # print("Input graph name: " + str(self.lines[0]))
        num_nodes = int(self.lines[1])
        # print("Number of nodes: " + str(num_nodes))
        nodes_attr_list = []
        # for line in self.lines:
        #     if "ENSP" in line:
        #         spl = line.split(sep="\n")
        #         nodes_attr_list.append(spl[0])
        for i in range(2, num_nodes + 2):
            spl = self.lines[i].split(sep="\n")[0]
            nodes_attr_list.append(spl)
        # print("Nodes attributes number: " + str(len(nodes_attr_list)))
        num_edges = int(self.lines[num_nodes + 2])
        # print("Number of edges: " + str(num_edges))
        # print("Input graph edges: ")
        edge_list = []
        edges_attr_list = []
        for i in range(num_nodes + 3, len(self.lines)):
            # print("self.lines[i].split(sep=n)")
            # print(self.lines[i].split(sep="\n"))
            # print("self.lines[i].split(sep=n)[1]")
            # print(self.lines[i].split(sep="\n")[1])
            line = [self.lines[i].split(sep="\n")[0]]
            # print(line)
            line_split = tuple(line[0].split(sep=" "))
            # print(line_split)
            new_edge = (line_split[0], line_split[1])
            edges_attr_list.append(line_split[2])
            # print(new_edge)
            edge_list.append(new_edge)
        # print(edge_list)
        # print(len(edge_list))
        input_graph.add_edges_from(edge_list)
        edge_attr_dict = dict(zip(edge_list, edges_attr_list))
        nx.set_edge_attributes(input_graph, edge_attr_dict, 'type')
        # print(input_graph.edges(data=True))

        # Pentru graf neorientat, nx creeaza graful cu doar jumatate din muchiile din edge_list, adica daca avem muchia (a,b), nu are rost sa adauge in graf si (b,a).
        # print(input_graph.edges())
        # print("Input graph number of edges: ")
        # print(len(input_graph.edges()))
        # print("Input graph nodes: ")
        # print(input_graph.nodes())
        # print("Input graph number of nodes: ")
        # print(len(input_graph.nodes()))
        # print("Node attributes list: ")
        # print(nodes_attr_list)
        node_attr_dict = dict(zip(input_graph.nodes(), nodes_attr_list))
        # print(node_attr_dict)
        nx.set_node_attributes(input_graph, node_attr_dict, 'label')
        # print(sorted(input_graph.nodes(data=True)))
        # print(len(input_graph.nodes()))
        # print(len(input_graph.edges()))
        self.graph = input_graph

    def write_new_file_for_gSpan_from_p133han_subgraph_db(self, subgraph_database):
        graph_counter = 0
        # f = open("gSpan-master by betterenvi/gSpan-master/graphdata/input_for_gSpan.txt", "w+")
        f = open('dataset_p133-han\gSpan_input\input_for_gSpan.txt', "w+")

        for subgraph in subgraph_database:
            # f = open("reformated_graf_for_gSpan_number_%d.txt" % graph_counter, "w+")
            f.write("t # %d\n" % graph_counter)
            for node in sorted(subgraph.nodes(data=True)):
                # print(node[1]["type"][0]) # Selectam dictionarul nodului, cheia, si valoarea. Aici valoarea reprezinta tipul nodului. Necesar un numar mic de tipuri ale nodurilor si muchiilor pentru gSpan.
                # print(subgraph.node[node]['type'])
                # Conform ZhangY09, fara etichete la noduri si nici la muchii.
                # gspan are nevoie de etichete pt noduri si muchii,
                # astfel, un workaround este ca atat nodurile cat si muchiile sa aiba aceeasi eticheta.
                f.write('{0} {1} {2}\n'.format("v", node[0], "0")) #node[1]["label"][0]))

            for edge in sorted(subgraph.edges(data=True)):
                # print(edge)
                f.write('{0} {1} {2} {3}\n'.format("e", edge[0], edge[1], "0")) #subgraph[edge[0]][edge[1]]['type']))
            graph_counter = graph_counter + 1
        f.write("t # -1")

    def get_graph(self):
        return self.graph

    def create_RI_data_graph_nodes_csv_file(self, nx_RI_data_graph):
        f = open('RI_data_graph_nodes.csv', "w+")
        f.write("RI_node_label,RI_node_id\n")
        node_list = list(nx_RI_data_graph.nodes(data=True))
        node_list_without_last_element = node_list[:-1]
        # print(node_list[1][0])
        # print(str(node_list[0][1]).split(": ")[1])
        for node in node_list_without_last_element:
            RI_node_label_aux = str(node[1]).split(": '")[1]
            RI_node_label = RI_node_label_aux.split("'}")[0]
            f.write(RI_node_label + "," + str(node[0]) + "\n")

        last_node = node_list[len(node_list)-1]
        RI_node_label_aux = str(last_node[1]).split(": '")[1]
        RI_node_label = RI_node_label_aux.split("'}")[0]
        f.write(RI_node_label + "," + str(last_node[0]))

    def create_RI_data_graph_edges_csv_file(self, nx_RI_data_graph):
        f = open('RI_data_graph_edges.csv', "w+")
        f.write("RI_from,RI_to\n")
        edge_list = list(nx_RI_data_graph.edges())
        edge_list_without_last_elem = edge_list[:-1]
        # print(edge_list)
        for edge in edge_list_without_last_elem:
            f.write(str(edge[0]) + "," + str(edge[1]) + "\n")
        # Adaugarea ultimei muchii, dar fara un "\n" dupa ea.
        f.write(str(edge_list[len(edge_list)-1][0]) + "," + str(edge_list[len(edge_list)-1][1]))

# # Date mari
# # Prelucrez fisierul text:
# print()
# print("Massive graph: ")
# with open('0.edges') as f:
#     lines = f.readlines()
# print(type(lines))
# print(lines)
# print()
# graph = nx.Graph()
#
# for line in lines:
#     newLine = line.rsplit(sep=" ")
#     firstElem = newLine[0]
#     secondElem = newLine[1]
#     trimmedSecondElem = secondElem.rsplit(sep="\n")
#     auxTuple = (firstElem, trimmedSecondElem[0])
#     graph.add_edge(firstElem, trimmedSecondElem[0], label=[firstElem, trimmedSecondElem[0]]) # Eticheta compusa; pentru fiecare muchie, are tipul "list".
#
# nodeLabelsDict = {}
# for node in graph.nodes():
#     nodeLabelsDict[node] = str(node)
# nx.set_node_attributes(graph, nodeLabelsDict, 'label')
#
#
# print()
# print("Numar de laturi: ")
# print(len(graph.edges()))
# print("Lista de laturi:")
# print(graph.edges(data=True))
# print()
# print("Numar de noduri: ")
# print(len(graph.nodes()))
# print("Lista de noduri: ")
# print(graph.nodes(data=True))

gf = Graph_Format("Homo_sapiens_udistr_32.gfd")
gf.create_graph_from_RI_file()
nx_RI_data_graph = gf.get_graph()
# print(nx_RI_data_graph.nodes(data=True))
gf.create_RI_data_graph_nodes_csv_file(nx_RI_data_graph)
# gf.create_RI_data_graph_edges_csv_file(nx_RI_data_graph)