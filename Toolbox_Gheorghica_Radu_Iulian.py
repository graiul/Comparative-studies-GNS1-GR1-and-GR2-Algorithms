import copy
import os
from collections import OrderedDict

import networkx as nx
from py2neo import Graph

from Query_Graph_Generator import Query_Graph_Generator


class Toolbox_Gheorghica_Radu_Iulian(object):

    # https://stackoverflow.com/questions/743806/how-to-split-a-string-into-a-list
    # https://stackoverflow.com/questions/7368789/convert-all-strings-in-a-list-to-int
    # https://stackoverflow.com/questions/743806/how-to-split-a-string-into-a-list
    # https://stackoverflow.com/questions/7368789/convert-all-strings-in-a-list-to-int
    # https://stackoverflow.com/questions/1720421/how-do-i-concatenate-two-lists-in-python

    def reunion_of_query_STwig_parts_results(self, list_of_paths): # De generalizat.
        intermediary_results = []
        reunited_results = []
        for path in list_of_paths:
            print(path)
            f = open(path, "r+")
            # https://www.techbeamers.com/python-read-file-line-by-line/
            # https://www.techbeamers.com/python-read-file-line-by-line/#reading-file-using-python-context-manager
            f_string_lines = []
            with open(path, "r") as rd:
                # Read lines in loop
                for read_line in rd:
                    # All lines (besides the last) will include  newline, so strip it
                    f_string_lines.append(read_line.strip())

            f_int_lines = []
            int_line = []
            for str_line in f_string_lines:
                string_vf2_line = str_line.split(" ")
                for str_line_element in string_vf2_line:
                    int_line.append(int(str_line_element))
                f_int_lines.append(int_line)
                int_line = []

            if len(intermediary_results) == 0:
                for res1 in f_int_lines:
                    intermediary_results.append(res1)
            else:
                for res2 in f_int_lines:
                    for rr in intermediary_results:
                        if res2[0] == rr[0]:
                            possible_reunion = copy.deepcopy(rr)
                            for node_id in res2[1:]:
                                possible_reunion.append(node_id)
                            reunited_results.append(possible_reunion)
        return reunited_results

    # stackoverflow.com/questions/752308/split-list-into-smaller-lists-split-in-half
    def split_list(self, alist, wanted_parts=1):
        # print("Splitter work:")
        print(alist)
        root = copy.deepcopy(alist[0])
        no_root_alist = copy.deepcopy(alist[1:])
        # print(no_root_alist)
        length = len(no_root_alist)

        rez_list = []
        # for i in range(wanted_parts):
        #     aux = []
        #     if i == 0:
        #         rez_list.append(alist[i * length // wanted_parts: (i + 1) * length // wanted_parts])
        #     else:
        #         aux = copy.deepcopy(alist[i*length // wanted_parts: (i+1)*length // wanted_parts])
        #         aux.insert(0, root)
        #         rez_list.append(aux)
        # return rez_list

        rez_list.append([no_root_alist[i * length // wanted_parts: (i + 1) * length // wanted_parts]
                for i in range(wanted_parts)])

        for r in rez_list[0]:
            r.insert(0, root)

        return rez_list

        # return [alist[i*length // wanted_parts: (i+1)*length // wanted_parts]
        #         for i in range(wanted_parts)]

    def create_txt_file_reunited_results_at_dir_path(self, reunitedResults, save_path, name_of_file):
        # name_of_file = "file_GR1_Algorithm_execution_times_and_average"
        complete_name = os.path.join(save_path, name_of_file + ".txt")
        f_reunited_results = open(complete_name, "w+")
        for result in reunitedResults:
            for r_element in result:
                f_reunited_results.write(str(r_element) + " ")
            f_reunited_results.write("\n")

    def create_execution_times_and_avg_txt_file_at_dir_path(self, algorithm_name, execution_times_path_and_filename, save_path):
        # avg = 0
        # sum = 0
        # for ex in execution_times:
        #     sum = sum + ex
        # avg = sum / len(execution_times)
        # name_of_file = "file_GR1_Algorithm_execution_times_and_average"
        # complete_name = os.path.join(save_path, name_of_file + ".txt")
        # f_exec_times_and_avg = open(complete_name, "w+")
        # f_exec_times_and_avg.write(str(execution_times))
        # f_exec_times_and_avg.write("\nAverage time: " +str(avg))
        # f_exec_times_and_avg.close()

        list_of_execution_times = []
        times_sum = 0
        result = 0
        f1_string_lines = []

        with open(execution_times_path_and_filename, "r") as rd:
            # Read lines in loop
            for line in rd:
                # All lines (besides the last) will include  newline, so strip it
                f1_string_lines.append(line.strip())

        f1_int_lines = []
        float_val_lines = []
        for string_line in f1_string_lines:
            # https://www.geeksforgeeks.org/python-string-split/
            split_string_line = string_line.split(" ")
            for string_backtracking_line_element in split_string_line:
                float_val_lines.append(float(string_backtracking_line_element))

        print(float_val_lines)
        times_sum = float(0)
        result = float(0)
        length = len(float_val_lines)
        for t in float_val_lines:
            times_sum = times_sum + t
        result = times_sum / length
        name_of_file = "file_" + algorithm_name + "_execution_times_and_average"
        complete_name = os.path.join(save_path, name_of_file + ".txt")
        f_exec_times_and_avg = open(complete_name, "w+")
        for time in float_val_lines:
            f_exec_times_and_avg.write(str(time) + "\n")
        # f_exec_times_and_avg.write(str(result))
        f_exec_times_and_avg.write("\nAverage time: " +str(result))
        f_exec_times_and_avg.close()


    def obtain_query_graph_stwig(self, wanted_parts=1): # Foloseste si data graful din Neo4J pentru label-urile nodurilor
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


        query_stwig = list(query_stwig_1_dict.items())
        if wanted_parts == 1:
            return query_stwig
        elif wanted_parts > 1:
            return self.split_list(query_stwig, wanted_parts=wanted_parts)



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

    # Returneaza graful query non STwig ca si dictionar cu
    # muchii si labelurile nodurilor muchiilor, necesare pentru
    # GR2 Algorithm, si anume pentru metodele next_data_edge si is_joinable
    # care au fost luate din GNS2v1_Backtracking_Graph_Search_Imbunatatiri_Originale_Non-Recursiv 

    # !!! Trebuie sa il fac sa ruleze si cu wanted_parts ca in metoda de mai sus.
    # Aceasta metoda returneaza doar dictionarul muchiilor grafului query
    # impreuna cu labelurile nodurilor fiecarei muchii.
    def obtain_query_graph_non_stwig(self):
        ############################ Din GNS2v1_Backtracking_Graph_Search_Imbunatatiri_Originale_Non-Recursiv ##########################################################
        # ??? MAI TREBUIE CONVERTIT LA GRAFURI QUERY Non STwig daca e din GNS2v1 ???
        # Trebuie sa returneze dictionarul cu muchii si label-urile nodurilor.
        query_graph_gen = Query_Graph_Generator()
        query_graph = query_graph_gen.gen_RI_query_graph()
        query_graph_edges = list(query_graph.edges())
        # print("Query graph edges: " + str(query_graph_edges))
        # Pentru conditiile VF2:
        # nx.set_node_attributes(query_graph, False, 'matched')

        query_nodes = list(query_graph.nodes())
        # print("Query node id's: " + str(query_nodes))
        # query_matched_attributes = []
        # for n1 in list(query_graph.nodes()):
        #     query_matched_attributes.append(query_graph.nodes[n1]['matched'])
        # print("Query node 'matched' attributes: " + str(query_matched_attributes))

        # Label-ul radacinii
        # root_label = dataGraph.node[query_nodes[0]]['label']
        root_label = query_graph.nodes[query_nodes[0]]['label']
        # Label-urile vecinilor din lista
        neighbor_labels = []
        for n2 in query_nodes[1:]:
            # neighbor_labels.append(dataGraph.node[n]['label'])
            neighbor_labels.append(query_graph.nodes[n2]['label'])

        query_node_labels = []
        query_node_labels.append(root_label)
        for nl in neighbor_labels:
            query_node_labels.append(nl)
        # print("Query nodes labels: " + str(query_node_labels))
        query_nodes_dict = OrderedDict(zip(query_nodes, query_node_labels))
        # query_stwig1_dict_matched_attribute = OrderedDict(zip(query_nodes, query_node_matched_attribute_source))
        # print("Query nodes dict: " + str(list(query_nodes_dict.items())))
        query_edge_labels = []
        for q_edge in query_graph_edges:
            query_edge_labels.append([query_nodes_dict[q_edge[0]], query_nodes_dict[q_edge[1]]])

        # print("query_edge_labels: " + str(query_edge_labels))
        # query_node_labels_source = copy.deepcopy(query_node_labels)
        # query_node_matched_attribute_source = copy.deepcopy(query_matched_attributes)

        query_edges_dict = OrderedDict(zip(query_graph_edges, query_edge_labels))
        # query_stwig1_dict_matched_attribute = OrderedDict(zip(query_nodes, query_node_matched_attribute_source))

        # NU E DENUMIT BINE, NU ARE TIPUL DICTIONAR CI TIPUL LISTA
        # query_graph_edges_dictionary = list(query_edges_dict.items())
        # print("Query graph edges dictionary: " + str(query_graph_edges_dictionary))
        # print()

        # adj_mat_query = nx.to_pandas_adjacency(query_graph, dtype=int)
        # print("query_stwig1_dict_matched_attribute: ")
        # print(list(query_stwig1_dict_matched_attribute.items()))
        # print()

        # print(type(query_edges_dict))
        return query_edges_dict
    ############################ Din GNS2v1_Backtracking_Graph_Search_Imbunatatiri_Originale_Non-Recursiv ##########################################################

    def get_query_graph_as_nx_object_non_stwig(self):
        pass

    def get_query_graph_as_dict_with_edges_as_keys_and_node_label_values_non_stwig(self):
        pass

    def obtain_data_graph(self):
        ############################ Din GNS1_Backtracking_STwig_Matching_with_txt_file_printing ##########################################################
        # GRAFUL DATA DIN NEO4J
        # neograph_data = Graph("bolt://127.0.0.1:7690", auth=("neo4j", "changeme")) # Data Graph RI - Cluster Neo4J
        neograph_data = Graph("bolt://127.0.0.1:7687",
                              auth=("neo4j", "password"))  # Data Graph RI - O singura instanta de Neo4J

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

        data_graph_edges = copy.deepcopy(sorted(edge_list_integer_ids))
        node_attributes_dictionary = OrderedDict(sorted(node_ids_as_integers_with_string_labels))
        return [data_graph_edges, node_attributes_dictionary]


