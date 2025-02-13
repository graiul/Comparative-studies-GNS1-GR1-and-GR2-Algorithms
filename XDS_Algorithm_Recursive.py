# NUME VECHI:
# GNS2v1_Backtracking_Graph_Search_Imbunatatiri_Originale.py
# from Graph_Format import Graph_Format

# https://stackoverflow.com/questions/6537487/changing-shell-text-color-windows
# https://pypi.org/project/colorama/
# from colorama import init
# from colorama import Fore, Back, Style
# init()

# import pandas as pd

from Query_Graph_Generator import Query_Graph_Generator
from EdgeFinderTool import EdgeFinderTool
import networkx as nx
from collections import OrderedDict
import copy

# https://stackoverflow.com/questions/4564559/get-exception-description-and-stack-trace-which-caused-an-exception-all-as-a-st
import traceback

from py2neo import Graph  #, Subgraph
from timeit import default_timer as timer

# CAUTAREA IN GRAFUL DATA MERGE BINE DAR ERA LIMITATA DE PYTHON
# DATORITA NR MARE DE APELURI RECURSIVE NECESARE, FIIND INTERPRETAT
# GRESIT DE PYTHON CA FIIND BUCLA INFINITA.
# NU E BUCLA INFINITA CI DOAR O CAUTARE RECURSIVA FOARTE ADANCA, IN FUNCTIE DE CAZ.
# DE ACEEA UNELE GRAFURI QUERY DAU REZULTATUL BINE SI ALGORITMUL SE OPRESTE SINGUR,
# IAR IN ALTE CAZURI APAREA EROAREA RESPECTIVA.
# stackoverflow.com/questions/3323001/what-is-the-maximum-recursion-depth-in-python-and-how-to-increase-it
# import sys
# sys.setrecursionlimit(10000000)

# Si mai este problema cu "Process finished with exit code -1073741571 (0xC00000FD)"
# stackoverflow.com/questions/5061582/setting-stacksize-in-a-python-script
# import resource  # trebuie instalat package separat prin instalatorul de pachete al interpretorului.
                 # sau scot recursivitatea
                 # sau folosesc graful data cu 10000 de muchii. ASTA VOI FACE.
# import sys
# resource.setrlimit(resource.RLIMIT_STACK, (2**29, -1))
# sys.setrecursionlimit(10**6)

def update_state(edge, partial_solution):
    # print("update_state exec: ")
    c_edge = copy.deepcopy(edge)
    s = copy.deepcopy(partial_solution)
    s.append(c_edge)
    # print(s)
    return s


def restore_state(partial_solution):
    if len(partial_solution) > 0:
        del partial_solution[-1]
        p_solution = copy.deepcopy(partial_solution)
        # print("Restored state: " + str(p_solution))
        return p_solution
    else:
        return partial_solution


def next_query_vertex(current_node, query_stwig_dict):
    if current_node == []:
        return list(query_stwig_dict.keys())[0]
    current_node_pos = list(query_stwig_dict.keys()).index(current_node)
    next_node_pos = current_node_pos + 1
    try:
        return list(query_stwig_dict.keys())[next_node_pos]
    except IndexError:
        # print("No more elements after this one in dict.")
        pass


def next_data_edge(partial_solution, data_graph):
    for edge in sorted(list(data_graph.edges())):
        if is_joinable(edge, partial_solution, data_graph, query_edges_dict):
            return edge
    return None

def is_joinable(data_edge_to_be_joined, partial_solution, data_graph, query_edges_dict_input):

    found_valid_data_edge = False
    # Nu mai este necesara sortarea: data_edge_to_be_joined = sorted(data_edge_to_be_joined_unsorted)
    data_edge_to_be_joined_node_0_label = data_graph.nodes[data_edge_to_be_joined[0]]['label']
    data_edge_to_be_joined_node_1_label = data_graph.nodes[data_edge_to_be_joined[1]]['label']
    # print("Candidate data edge node 0 label: " + str(data_edge_to_be_joined_node_0_label))
    # print("Candidate data edge node 1 label: " + str(data_edge_to_be_joined_node_1_label))

    ########################################################################

    # print("\nis_joinable exec:")
    # print("input data node id: " + str(data_node_to_be_joined))

    # data_node_label = data_graph.node[data_node_to_be_joined]['label']

    # print("data node label: " + str(data_node_label))
    # print("query_stwig_as_dict: ")
    # print(query_stwig_as_dict.items())
    # print("first query stwig node id: " + str(list(query_stwig_as_dict.items())[0][0]))
    # print("first query stwig node label: " + str(list(query_stwig_as_dict.items())[0][1]))
    ########################################################################
    # Pentru VF2 - obtinere muchii candidate inainte de refinement pentru fiecare pozitie.
    # # Position 0:
    # # Obtain candidates folosind label-ul acestei pozitii
    # position_label = query_edges_dict[query_graph_edges[0]]
    # print("Position [0] nodes label: " + str(position_label))
    # obtained_candidates_pos_0_node_0 = obtainCandidates(position_label[0])
    # obtained_candidates_pos_0_node_1 = obtainCandidates(position_label[1])
    # obtained_candidate_edges = obtainCandidateEdges(position_label[0], position_label[1])
    # print("Candidate edges: " + str(obtained_candidate_edges))
    #
    # initial_match_values_pos_0_candidates = []
    # for im_0 in obtained_candidates_pos_0_node_0:
    #     initial_match_values_pos_0_candidates.append(False)
    # print("Candidate nodes for first node of edge on position[0] and the mentioned labels: " + str(obtained_candidates_pos_0_node_0))
    # print("Candidate nodes for second node of edge on position[0] and the mentioned labels: " + str(obtained_candidates_pos_0_node_1))
    #
    # matched_true_false_data_nodes_pos_0_dict = OrderedDict(zip(obtained_candidates_pos_0_node_0, initial_match_values_pos_0_candidates))
    # # print("matched_true_false_data_nodes_pos_0_dict: " + str(list(matched_true_false_data_nodes_pos_0_dict.items())))
    # print()
    #
    # # Position 1:
    # # Obtain candidates folosind label-ul acestei pozitii
    # position_label = query_edges_dict[query_graph_edges[1]]
    #
    # print("Position [1] nodes label: " + str(position_label))
    # obtained_candidates_pos_1_node_0 = obtainCandidates(position_label[0])
    # obtained_candidates_pos_1_node_1 = obtainCandidates(position_label[1])
    # obtained_candidate_edges = obtainCandidateEdges(position_label[0], position_label[1])
    # print("Candidate edges: " + str(obtained_candidate_edges))
    #
    # initial_match_values_pos_1_candidates = []
    # for im_1 in obtained_candidates_pos_1_node_0:
    #     initial_match_values_pos_1_candidates.append(False)
    #
    # print("Candidate nodes for first node of edge on position [1] and the mentioned label: " + str(obtained_candidates_pos_1_node_0))
    # print("Candidate nodes for first node of edge on position [1] and the mentioned label: " + str(obtained_candidates_pos_1_node_1))
    #
    # matched_true_false_data_nodes_pos_1_dict = OrderedDict(
    #     zip(obtained_candidates_pos_1_node_0, initial_match_values_pos_1_candidates))
    # # print("matched_true_false_data_nodes_pos_1_dict: " + str(list(matched_true_false_data_nodes_pos_1_dict.items())))
    # print()
    #
    # # Position 2:
    # # Obtain candidates folosind label-ul acestei pozitii
    # position_label = query_edges_dict[query_graph_edges[2]]
    #
    # print("Position [2] nodes label: " + str(position_label))
    # obtained_candidates_pos_2 = obtainCandidates(position_label)
    #
    # obtained_candidates_pos_2_node_0 = obtainCandidates(position_label[0])
    # obtained_candidates_pos_2_node_1 = obtainCandidates(position_label[1])
    # obtained_candidate_edges = obtainCandidateEdges(position_label[0], position_label[1])
    # print("Candidate edges: " + str(obtained_candidate_edges))
    #
    # initial_match_values_pos_2_candidates = []
    # for im_2 in obtained_candidates_pos_2:
    #     initial_match_values_pos_2_candidates.append(False)
    #
    # print("Candidate nodes for first node of edge on position [2] and the mentioned label: " + str(obtained_candidates_pos_2_node_0))
    # print("Candidate nodes for first node of edge on position [2] and the mentioned label: " + str(obtained_candidates_pos_2_node_1))
    #
    # matched_true_false_data_nodes_pos_2_dict = OrderedDict(
    #     zip(obtained_candidates_pos_2, initial_match_values_pos_2_candidates))
    # # print("matched_true_false_data_nodes_pos_2_dict: " + str(list(matched_true_false_data_nodes_pos_2_dict.items())))
    # print()
    #
    # # Position 3:
    # # Obtain candidates folosind label-ul acestei pozitii
    # position_label = query_edges_dict[query_graph_edges[3]]
    # print("Position [3] nodes label: " + str(position_label))
    # obtained_candidates_pos_3 = obtainCandidates(position_label)
    #
    # obtained_candidates_pos_3_node_0 = obtainCandidates(position_label[0])
    # obtained_candidates_pos_3_node_1 = obtainCandidates(position_label[1])
    # obtained_candidate_edges = obtainCandidateEdges(position_label[0], position_label[1])
    # print("Candidate edges: " + str(obtained_candidate_edges))
    #
    # initial_match_values_pos_3_candidates = []
    # for im_3 in obtained_candidates_pos_3:
    #     initial_match_values_pos_3_candidates.append(False)
    #
    # print("Candidate nodes for first node of edge on position [3] and the mentioned label: " + str(obtained_candidates_pos_3_node_0))
    # print("Candidate nodes for first node of edge on position [3] and the mentioned label: " + str(obtained_candidates_pos_3_node_1))
    #
    #
    # matched_true_false_data_nodes_pos_3_dict = OrderedDict(
    #     zip(obtained_candidates_pos_3, initial_match_values_pos_3_candidates))
    # # print("matched_true_false_data_nodes_pos_3_dict: " + str(list(matched_true_false_data_nodes_pos_3_dict.items())))
    # print()
    ######################################################################

    # Pentru prima solutie la executie.
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # if len(complete_solutions) == 0: # or len(complete_solutions) > 0:
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # pt primul element(radacina) la prima executie:
    if len(partial_solution) == 0:
        # print("\nWe entered the execution for the first element: ")

        if data_edge_to_be_joined not in partial_solution:
            ########################################################
            # Pentru VF2
            # print(list(query_  _input.items())[0][1])
            # if list(query_   _input.items())[0][1] == False:
            ########################################################
            # print("     Query edge node labels for the first position: ")
            # print("     " + str(list(query_edges_dict.items())[0][1]))
            # print("     Candidate data graph edge (data nodes label): " + str(
            #     [data_graph.nodes[data_edge_to_be_joined[0]]['label'],
            #      data_graph.nodes[data_edge_to_be_joined[1]]['label']]))
            # print("     Candidate data graph edge nodes id: " + str(data_edge_to_be_joined))
            if list(query_edges_dict.items())[0][1][0] == data_edge_to_be_joined_node_0_label or list(query_edges_dict.items())[0][1][0] == data_edge_to_be_joined_node_1_label:
                # print("YES")
                if list(query_edges_dict.items())[0][1][1] == data_edge_to_be_joined_node_1_label or list(query_edges_dict.items())[0][1][1] == data_edge_to_be_joined_node_0_label:
                    # print("YES")
                    # print("     " + Fore.GREEN + Style.BRIGHT +  "Positions log before appending first position data edge: " + str(list(positions.items())) + Style.RESET_ALL)
                    # print()

                    finder = EdgeFinderTool(data_edge_to_be_joined, positions[0])
                    found = finder.edge_found()
                    if found is False:
                    # if data_edge_to_be_joined not in positions[0]:
                        found_valid_data_edge = True
                        aux = copy.deepcopy(partial_solution)
                        aux.append(data_edge_to_be_joined)
                        # print("Appended data edge: ")
                        # print(data_edge_to_be_joined)
                        # print("Reversed data edge to avoid final results duplicates: ")
                        # reversed_data_edge = (data_edge_to_be_joined[1], data_edge_to_be_joined[0])
                        # print(reversed_data_edge)
                        # print()
                        pos = aux.index(aux[-1])
                        positions[pos].append(data_edge_to_be_joined)
                        # positions[pos].append(reversed_data_edge)
                        # print("Log for position 0: ")
                        # print(positions[pos])

                                        #####################################################################
                                        #             matched_true_false_data_nodes_pos_0_dict[data_node_to_be_joined] = True
                                        #             break
                                        #####################################################################
                        # print("     " + Fore.GREEN + Style.BRIGHT + "Positions log after appending first position data edge: " + str(list(positions.items())) + Style.RESET_ALL)
                        # print()
                else:
                    # print("     Data edge is not valid for this.")
                    pass
            else:
                # print("     Data edge is not valid for this.")
                pass

    if len(partial_solution) == 1:
        # print("\nWe entered the execution for the second element: ")
        ########################################################
        # Pentru VF2
        # for data_node_to_be_joined in obtained_candidates_pos_1:
        ########################################################
        if data_edge_to_be_joined not in partial_solution:
            # print("     Query edge for the second element: ")
            # print("     " + str(list(query_edges_dict.items())[1][1]))
            # print("     Candidate data graph edge (data nodes label): " + str(
            #     [data_graph.nodes[data_edge_to_be_joined[0]]['label'],
            #      data_graph.nodes[data_edge_to_be_joined[1]]['label']]))
            if list(query_edges_dict.items())[1][1][0] == data_edge_to_be_joined_node_0_label or list(query_edges_dict.items())[1][1][0] == data_edge_to_be_joined_node_1_label:
                # print("YES")
                if list(query_edges_dict.items())[1][1][1] == data_edge_to_be_joined_node_1_label or list(query_edges_dict.items())[1][1][1] == data_edge_to_be_joined_node_0_label:
                    # print("YES")
                    # print("     " + Fore.GREEN + Style.BRIGHT +  "Positions log before appending second edge: " + str(list(positions.items())) + Style.RESET_ALL)
                    finder = EdgeFinderTool(data_edge_to_be_joined, positions[1])
                    found = finder.edge_found()
                    if found is False:
                    # if data_edge_to_be_joined not in positions[1]:
                        aux = copy.deepcopy(partial_solution)
                        aux.append(data_edge_to_be_joined)

                        pos = aux.index(aux[-1])
                        if aux not in complete_solutions:
                            # Verificam daca label-ul primei frunze al STwig-ului query are aceeasi valoare ca si label-ul nodului data primit ca si parametru
                            # si care sa cauta pentru pozitia primei frunze.

                            # Trebuie sa existe muchie intre nodul de pe prima poz a sol partiale actuale(radacina), deci tot timpul ultimul nod
                            # din log-ul nodurilor care se afla pe prima pozitie
                            for e in partial_solution:
                                # if data_graph.has_edge(positions[0][len(positions[0]) - 1], data_node_to_be_joined):
                                if data_graph.has_edge(e[0], data_edge_to_be_joined[0]) or \
                                        data_graph.has_edge(e[0], data_edge_to_be_joined[1]) or \
                                        data_graph.has_edge(e[1], data_edge_to_be_joined[0]) or \
                                        data_graph.has_edge(e[1], data_edge_to_be_joined[1]):
                                    # print("     Has edge with previous position(s)")

                                    # print("Label of the first leaf of the query STwig: " + str(list(query_stwig_as_dict.items())[1][1]))
                                    # print("Label of data node verified: " + str(data_node_label))
                                    # if list(query_stwig_as_dict.items())[1][1] == data_node_label:

                                    #####################################################################
                                    # if matched_true_false_data_nodes_pos_1_dict[data_node_to_be_joined] == False:
                                    ######################################################################

                                    found_valid_data_edge = True
                                    finder2 = EdgeFinderTool(aux[-1], positions[pos])
                                    found2 = finder2.edge_found()
                                    if found2 is False:
                                    # if aux[-1] not in positions[pos]:
                                        positions[pos].append(aux[-1])  # aux[-1] e data_edge_to_be_joined
                                        # print("Appended data edge: ")
                                        # print(aux[-1])
                                        # print("Reversed data edge to avoid final results duplicates: ")
                                        # reversed_data_edge = (data_edge_to_be_joined[1], data_edge_to_be_joined[0])
                                        # print(reversed_data_edge)
                                        # print()
                                        # positions[pos].append(reversed_data_edge)

                                #####################################################################
                                #     matched_true_false_data_nodes_pos_1_dict[data_node_to_be_joined] = True
                                #     break
                                #####################################################################

                                # print("     " + Fore.GREEN + Style.BRIGHT + "Positions log after appending second edge: " + str(
                                #     list(positions.items())) + Style.RESET_ALL)
                                # print()
                else:
                    # print("     Data edge is not valid for this.")
                    pass
            else:
                # print("     Data edge is not valid for this.")
                pass

        else:
            # print("     Already in partial solution.")
            pass

    if len(partial_solution) == 2:
        # print("\nWe entered the execution for the third element: ")
        #####################################################################
        # for data_node_to_be_joined in obtained_candidates_pos_2:
        #####################################################################
        if data_edge_to_be_joined not in partial_solution:
            # print("     Query edge for the third element: ")
            # print("     " + str(list(query_edges_dict.items())[2][1]))
            # print("     Candidate data graph edge (data nodes label): " + str(
            #     [data_graph.nodes[data_edge_to_be_joined[0]]['label'],
            #      data_graph.nodes[data_edge_to_be_joined[1]]['label']]))
            if list(query_edges_dict.items())[2][1][0] == data_edge_to_be_joined_node_0_label or list(query_edges_dict.items())[2][1][0] == data_edge_to_be_joined_node_1_label:
                # print("YES")
                if list(query_edges_dict.items())[2][1][1] == data_edge_to_be_joined_node_1_label or list(query_edges_dict.items())[2][1][1] == data_edge_to_be_joined_node_0_label:
                    # print("YES")
                    # print("     " + Fore.GREEN + Style.BRIGHT +  "Positions log before appending third edge: " + str(list(positions.items())) + Style.RESET_ALL)
                    aux = copy.deepcopy(partial_solution)
                    aux.append(data_edge_to_be_joined)

                    pos = aux.index(aux[-1])
                    if aux not in complete_solutions:
                        finder = EdgeFinderTool(data_edge_to_be_joined, positions[2])
                        found = finder.edge_found()
                        if found is False:
                        # if data_edge_to_be_joined not in positions[2]:
                            for e in partial_solution:
                                if data_graph.has_edge(e[0], data_edge_to_be_joined[0]) or \
                                        data_graph.has_edge(e[0], data_edge_to_be_joined[1]) or \
                                        data_graph.has_edge(e[1], data_edge_to_be_joined[0]) or \
                                        data_graph.has_edge(e[1], data_edge_to_be_joined[1]):
                                    # print("     Has edge with previous position(s)")
                                    # print("Label of data node verified: " + str(data_node_label))
                                    ###############################################################################
                                    # if matched_true_false_data_nodes_pos_2_dict[data_node_to_be_joined] == False:
                                    ###############################################################################
                                    found_valid_data_edge = True
                                    finder2 = EdgeFinderTool(aux[-1], positions[pos])
                                    found2 = finder2.edge_found()
                                    if found2 is False:
                                    # if aux[-1] not in positions[pos]:
                                        positions[pos].append(aux[-1])
                                        # print("Appended data edge: ")
                                        # print(aux[-1])
                                        # print("Reversed data edge to avoid final results duplicates: ")
                                        # reversed_data_edge = (data_edge_to_be_joined[1], data_edge_to_be_joined[0])
                                        # print(reversed_data_edge)
                                        # print()
                                        # positions[pos].append(reversed_data_edge)
                                    ###############################################################################
                                    # matched_true_false_data_nodes_pos_2_dict[data_node_to_be_joined] = True
                                    # break
                                    ###############################################################################

                                    # print("     " + Fore.GREEN + Style.BRIGHT + "Positions log after appending third edge: " + str(list(positions.items())) + Style.RESET_ALL)
                                    # print()
                else:
                    # print("     Data edge is not valid for this.")
                    pass
            else:
                # print("     Data edge is not valid for this.")
                pass

        else:
            # print("     Already in partial solution.")
            pass

    if len(partial_solution) == 3:
        # print("\nWe entered the execution for the fourth element: ")
        # for data_node_to_be_joined in obtained_candidates_pos_3:
        if data_edge_to_be_joined not in partial_solution:
            # print("     Query edge for the fourth element: ")
            # print("     " + str(list(query_edges_dict.items())[3][1]))
            # print("     Candidate data graph edge (data nodes label): " + str(
            #     [data_graph.nodes[data_edge_to_be_joined[0]]['label'],
            #      data_graph.nodes[data_edge_to_be_joined[1]]['label']]))
            if list(query_edges_dict.items())[3][1][0] == data_edge_to_be_joined_node_0_label or list(query_edges_dict.items())[3][1][0] == data_edge_to_be_joined_node_1_label:
                # print("YES")
                if list(query_edges_dict.items())[3][1][1] == data_edge_to_be_joined_node_1_label or list(query_edges_dict.items())[3][1][1] == data_edge_to_be_joined_node_0_label:
                    # print("YES")
                    # print("     " + Fore.GREEN + Style.BRIGHT +  "Positions log before appending fourth edge: " + str(list(positions.items())) + Style.RESET_ALL)
                    aux = copy.deepcopy(partial_solution)
                    aux.append(data_edge_to_be_joined)
                    pos = aux.index(aux[-1])
                    if aux not in complete_solutions:
                        finder = EdgeFinderTool(data_edge_to_be_joined, positions[3])
                        found = finder.edge_found()
                        if found is False:
                        # if data_edge_to_be_joined not in positions[3]:
                            for e in partial_solution:
                                if data_graph.has_edge(e[0], data_edge_to_be_joined[0]) or \
                                        data_graph.has_edge(e[0], data_edge_to_be_joined[1]) or \
                                        data_graph.has_edge(e[1], data_edge_to_be_joined[0]) or \
                                        data_graph.has_edge(e[1], data_edge_to_be_joined[1]):
                                    # print("     Has edge with previous position(s)")
                                    # if matched_true_false_data_nodes_pos_3_dict[data_node_to_be_joined] == False:
                                    found_valid_data_edge = True
                                    finder2 = EdgeFinderTool(aux[-1], positions[pos])
                                    found2 = finder2.edge_found()
                                    if found2 is False:
                                    # if aux[-1] not in positions[pos]:
                                        positions[pos].append(aux[-1])
                                        # print("Appended data edge: ")
                                        # print(aux[-1])
                                        # print("Reversed data edge to avoid final results duplicates: ")
                                        # reversed_data_edge = (data_edge_to_be_joined[1], data_edge_to_be_joined[0])
                                        # print(reversed_data_edge)
                                        # print()
                                        # positions[pos].append(reversed_data_edge)
                                    # matched_true_false_data_nodes_pos_3_dict[data_node_to_be_joined] = True
                                    # break
                                    # print("     " + Fore.GREEN + Style.BRIGHT + "Positions log after appending fourth edge: " + str(list(positions.items())) + Style.RESET_ALL)
                                    # print()
                else:
                    # print("     Data edge is not valid for this.")
                    pass
            else:
                # print("     Data edge is not valid for this.")
                pass
        else:
            # print("     Already in partial solution.")
            pass

    # if len(complete_solutions) > 0:
    #     if len(partial_solution) == 0:
    #         if data_edge_to_be_joined not in partial_solution:
    #             ########################################################
    #             # Pentru VF2
    #             # print(list(query_  _input.items())[0][1])
    #             # if list(query_   _input.items())[0][1] == False:
    #             ########################################################
    #             print(list(query_edges_dict.items())[0][1])
    #             if list(query_edges_dict.items())[0][1][0] == data_edge_to_be_joined_node_0_label:
    #                 print("YES")
    #                 if list(query_edges_dict.items())[0][1][1] == data_edge_to_be_joined_node_1_label:
    #                     print("YES")
    #                     print("Positions log before appending first edge: " + str(list(positions.items())))
    #                     print()
    #             if data_edge_to_be_joined not in positions[0]:
    #                 found = True
    #                 aux = copy.deepcopy(partial_solution)
    #                 aux.append(data_edge_to_be_joined)
    #                 pos = aux.index(aux[-1])
    #                 positions[pos].append(data_edge_to_be_joined)
    #                 #####################################################################
    #                 #             matched_true_false_data_nodes_pos_0_dict[data_node_to_be_joined] = True
    #                 #             break
    #                 #####################################################################
    #
    #                 print("Positions log after appending first edge: " + str(list(positions.items())))
    #                 print()
    #
    #
    #     if len(partial_solution) == 1:
    #         print("\nWe entered the execution for the second element: ")
    #         ########################################################
    #         # Pentru VF2
    #         # for data_node_to_be_joined in obtained_candidates_pos_1:
    #         ########################################################
    #         if data_edge_to_be_joined not in partial_solution:
    #             print(list(query_edges_dict.items())[1][1])
    #             if list(query_edges_dict.items())[1][1][0] == data_edge_to_be_joined_node_0_label:
    #                 print("YES")
    #                 if list(query_edges_dict.items())[1][1][1] == data_edge_to_be_joined_node_1_label:
    #                     print("YES")
    #                     print("Positions log before appending edge: " + str(list(positions.items())))
    #                     if data_edge_to_be_joined not in positions[1]:
    #                         found = True
    #
    #                         aux = copy.deepcopy(partial_solution)
    #                         aux.append(data_edge_to_be_joined)
    #                         pos = aux.index(aux[-1])
    #                         if aux not in complete_solutions:
    #                             # Verificam daca label-ul primei frunze al STwig-ului query are aceeasi valoare ca si label-ul nodului data primit ca si parametru
    #                             # si care sa cauta pentru pozitia primei frunze.
    #
    #                             # Trebuie sa existe muchie intre nodul de pe prima poz a sol partiale actuale(radacina), deci tot timpul ultimul nod
    #                             # din log-ul nodurilor care se afla pe prima pozitie
    #
    #                             for e in partial_solution:
    #                                 # if data_graph.has_edge(positions[0][len(positions[0]) - 1], data_node_to_be_joined):
    #                                 if data_graph.has_edge(e[0], data_edge_to_be_joined[0]) or \
    #                                         data_graph.has_edge(e[0], data_edge_to_be_joined[1]) or \
    #                                         data_graph.has_edge(e[1], data_edge_to_be_joined[0]) or \
    #                                         data_graph.has_edge(e[1], data_edge_to_be_joined[1]):
    #                                     print("Has edge with previous position(s)")
    #
    #                                     # print("Label of the first leaf of the query STwig: " + str(list(query_stwig_as_dict.items())[1][1]))
    #                                     # print("Label of data node verified: " + str(data_node_label))
    #                                     # if list(query_stwig_as_dict.items())[1][1] == data_node_label:
    #
    #                                     #####################################################################
    #                                     # if matched_true_false_data_nodes_pos_1_dict[data_node_to_be_joined] == False:
    #                                     ######################################################################
    #
    #                                     found = True
    #                                     if aux[-1] not in positions[pos]:
    #                                         positions[pos].append(aux[-1])
    #
    #                                 #####################################################################
    #                                 #     matched_true_false_data_nodes_pos_1_dict[data_node_to_be_joined] = True
    #                                 #     break
    #                                 #####################################################################
    #
    #                                 print("Positions log after appending edge: " + str(list(positions.items())))
    #                                 print()
    #
    #     if len(partial_solution) == 2:
    #         print("\nWe entered the execution for the third element: ")
    #         #####################################################################
    #         # for data_node_to_be_joined in obtained_candidates_pos_2:
    #         #####################################################################
    #         if data_edge_to_be_joined not in partial_solution:
    #             print(list(query_edges_dict.items())[2][1])
    #             if list(query_edges_dict.items())[2][1][0] == data_edge_to_be_joined_node_0_label:
    #                 print("YES")
    #                 if list(query_edges_dict.items())[2][1][1] == data_edge_to_be_joined_node_1_label:
    #                     print("YES")
    #                     aux = copy.deepcopy(partial_solution)
    #                     aux.append(data_edge_to_be_joined)
    #                     pos = aux.index(aux[-1])
    #                     if aux not in complete_solutions:
    #                         if data_edge_to_be_joined not in positions[2]:
    #                             for e in partial_solution:
    #                                 if data_graph.has_edge(e[0], data_edge_to_be_joined[0]) or \
    #                                         data_graph.has_edge(e[0], data_edge_to_be_joined[1]) or \
    #                                         data_graph.has_edge(e[1], data_edge_to_be_joined[0]) or \
    #                                         data_graph.has_edge(e[1], data_edge_to_be_joined[1]):
    #                                     print("Has edge with previous position(s)")
    #                                     # print("Label of data node verified: " + str(data_node_label))
    #                                     ###############################################################################
    #                                     # if matched_true_false_data_nodes_pos_2_dict[data_node_to_be_joined] == False:
    #                                     ###############################################################################
    #                                     found = True
    #                                     if aux[-1] not in positions[pos]:
    #                                         positions[pos].append(aux[-1])
    #                                     ###############################################################################
    #                                     # matched_true_false_data_nodes_pos_2_dict[data_node_to_be_joined] = True
    #                                     # break
    #                                     ###############################################################################
    #
    #                                     print("Positions log after appending edge: " + str(list(positions.items())))
    #                                     print()
    #
    #     if len(partial_solution) == 3:
    #         print("\nWe entered the execution for the fourth element: ")
    #         # for data_node_to_be_joined in obtained_candidates_pos_3:
    #         if data_edge_to_be_joined not in partial_solution:
    #             print(list(query_edges_dict.items())[3][1])
    #             if list(query_edges_dict.items())[3][1][0] == data_edge_to_be_joined_node_0_label:
    #                 print("YES")
    #                 if list(query_edges_dict.items())[3][1][1] == data_edge_to_be_joined_node_1_label:
    #                     print("YES")
    #                     aux = copy.deepcopy(partial_solution)
    #                     aux.append(data_edge_to_be_joined)
    #                     pos = aux.index(aux[-1])
    #                     if aux not in complete_solutions:
    #                         if data_edge_to_be_joined not in positions[3]:
    #                             for e in partial_solution:
    #                                 if data_graph.has_edge(e[0], data_edge_to_be_joined[0]) or \
    #                                         data_graph.has_edge(e[0], data_edge_to_be_joined[1]) or \
    #                                         data_graph.has_edge(e[1], data_edge_to_be_joined[0]) or \
    #                                         data_graph.has_edge(e[1], data_edge_to_be_joined[1]):
    #                                     print("Has edge with previous position(s)")
    #                                     # if matched_true_false_data_nodes_pos_3_dict[data_node_to_be_joined] == False:
    #                                     found = True
    #                                     if aux[-1] not in positions[pos]:
    #                                         positions[pos].append(aux[-1])
    #                                     # matched_true_false_data_nodes_pos_3_dict[data_node_to_be_joined] = True
    #                                     # break
    #                                     print("Positions log after appending edge: " + str(list(positions.items())))
    #                                     print()
    #
    #
    #     # pt primul element, dupa mai multe executii. Trebuie schimbata radacina pentru noul STwig.
    #     if len(partial_solution) == 0:
    #         for data_node_to_be_joined in obtained_candidates_pos_0:
    #             if data_node_to_be_joined not in partial_solution:
    #
    #                 # if node not in sol:
    #
    #                 # aux = copy.deepcopy(partial_solution)
    #                 # aux.append(node)
    #                 # pos = aux.index(aux[-1])
    #                 # if aux not in complete_solutions:
    #
    #                 if data_node_to_be_joined not in positions[0]:
    #                     if matched_true_false_data_nodes_pos_0_dict[data_node_to_be_joined] == False:
    #                         found = True
    #                         positions[0].append(data_node_to_be_joined)
    #                         matched_true_false_data_nodes_pos_0_dict[data_node_to_be_joined] = True
    #                         break
    #                         # print("Positions log: " + str(list(positions.items())))
    #                         # print()
    #
    #     # pt al doilea element(prima frunza):
    #     if len(partial_solution) == 1:
    #         # print("We entered the execution for the second element (the first leaf)")
    #         for data_node_to_be_joined in obtained_candidates_pos_1:
    #             if data_node_to_be_joined not in partial_solution:
    #
    #                 aux = copy.deepcopy(partial_solution)
    #                 aux.append(data_node_to_be_joined)
    #                 pos = aux.index(aux[-1])
    #                 if aux not in complete_solutions:
    #                     if data_node_to_be_joined not in positions[1]:
    #                         # Verificam daca label-ul primei frunze al STwig-ului query are aceeasi valoare ca si label-ul nodului data primit ca si parametru
    #                         # si care sa cauta pentru pozitia primei frunze.
    #
    #                         # Trebuie sa existe muchie intre nodul de pe prima poz a sol partiale actuale(radacina), deci tot timpul ultimul nod
    #                         # din log-ul nodurilor care se afla pe prima pozitie
    #                         if data_graph.has_edge(positions[0][len(positions[0]) - 1], data_node_to_be_joined):
    #                             if matched_true_false_data_nodes_pos_1_dict[data_node_to_be_joined] == False:
    #                                 # print("Label of data node verified: " + str(data_node_label))
    #                                 if matched_true_false_data_nodes_pos_1_dict[data_node_to_be_joined] == False:
    #                                     found = True
    #                                     if aux[-1] not in positions[pos]:
    #                                         positions[pos].append(aux[-1])
    #                                     matched_true_false_data_nodes_pos_1_dict[data_node_to_be_joined] = True
    #                                     break
    #                                     # print("Positions log: " + str(list(positions.items())))
    #                                     # print()
    #
    #         # pt al treilea element(a doua frunza):
    #         if len(partial_solution) == 2:
    #             # print("We entered the execution for the third element (the second leaf)")
    #             for data_node_to_be_joined in obtained_candidates_pos_2:
    #                 if data_node_to_be_joined not in partial_solution:
    #
    #                     aux = copy.deepcopy(partial_solution)
    #                     aux.append(data_node_to_be_joined)
    #                     pos = aux.index(aux[-1])
    #                     if aux not in complete_solutions:
    #
    #                         if data_node_to_be_joined not in positions[2]:
    #                             # print("node: " + str(node))
    #                             # print("positions[2]: " + str(positions[2]))
    #
    #                             # print("Checking if second leaf has edge with root.")
    #                             # print("Root: " + str(positions[0][len(positions[0]) - 1]))
    #                             # print("Potential leaf: " + str(data_node_to_be_joined))
    #                             # print("Potential leaf label: " + str(data_node_label))
    #                             if data_graph.has_edge(positions[0][len(positions[0]) - 1], data_node_to_be_joined):
    #                                 # print("Label of data node verified: " + str(data_node_label))
    #                                 if matched_true_false_data_nodes_pos_2_dict[data_node_to_be_joined] == False:
    #                                     found = True
    #                                     if aux[-1] not in positions[pos]:
    #                                         positions[pos].append(aux[-1])
    #                                     matched_true_false_data_nodes_pos_2_dict[data_node_to_be_joined] = True
    #                                     break
    #                                     # print("Positions log: " + str(list(positions.items())))
    #                                     # print()
    #
    #     # pt al patrulea element:
    #     if len(partial_solution) == 3:
    #         for data_node_to_be_joined in obtained_candidates_pos_3:
    #             if data_node_to_be_joined not in partial_solution:
    #                 aux = copy.deepcopy(partial_solution)
    #                 aux.append(data_node_to_be_joined)
    #                 pos = aux.index(aux[-1])
    #                 if aux not in complete_solutions:
    #                     if data_node_to_be_joined not in positions[2]:
    #                         # print("positions[2]: " + str(positions[2]))
    #                         if data_graph.has_edge(positions[0][len(positions[0]) - 1], data_node_to_be_joined):
    #                             if matched_true_false_data_nodes_pos_3_dict[data_node_to_be_joined] == False:
    #                                 found = True
    #                                 if aux[-1] not in positions[pos]:
    #                                     positions[pos].append(aux[-1])
    #                                 matched_true_false_data_nodes_pos_3_dict[data_node_to_be_joined] = True
    #                                 break
    #                                 # print("Positions log: " + str(list(positions.items())))
    #                                 # print()

    # # Cand trecem la o pozitie precedenta, frunzele de pe pozitia pt care am cautat in data trebuie sa fie marcate ca fiind matched=False.

    if found_valid_data_edge == True:
        return data_edge_to_be_joined

    return None


def subgraph_search(partial_solution, query_graph_dict, current_node, data_graph):
    # print()
    # print("Started subgraph search: ")
    # print(Back.WHITE + Fore.LIGHTBLUE_EX + Style.BRIGHT + "Partial solution given: " + str(partial_solution) + Style.RESET_ALL)
    # print("Partial solution given: " + str(partial_solution))
    i = False
    # print(query_graph_dict)
    if len(partial_solution) == len(list(query_graph_dict.items())):
        if partial_solution not in complete_solutions:
            # https://networkx.github.io/documentation/networkx-1.9/reference/generated/networkx.linalg.graphmatrix.adjacency_matrix.html
            # https://networkx.github.io/documentation/networkx-2.2/reference/generated/networkx.convert_matrix.to_pandas_adjacency.html
            # https://stackoverflow.com/questions/19917545/comparing-two-pandas-dataframes-for-differences
            # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.eq.html#pandas.DataFrame.eq
            # https://stackoverflow.com/questions/38212697/confirming-equality-of-two-pandas-dataframes
            # Obtinerea valorilor dintr-un DataFrame pandas: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_numpy.html#pandas.DataFrame.to_numpy
            # https://stackoverflow.com/questions/10580676/comparing-two-numpy-arrays-for-equality-element-wise

            # Pentru lucrul cu matrice de adiacenta.
            # print("\nQuery adjacency matrix: ")
            # adj_mat_query_elems = adj_mat_query.to_numpy()
            # print(adj_mat_query_elems)
            # partial_solution_data_subgraph = nx.Graph()
            # partial_solution_data_subgraph.add_edges_from(partial_solution)
            # adj_mat_data = nx.to_pandas_adjacency(partial_solution_data_subgraph, dtype=int)
            # print()
            # adj_mat_data_elems = adj_mat_data.to_numpy()
            # print("Data subgraph/partial solution adjacency matrix: ")
            # print(adj_mat_data_elems)
            # print()

            # Problema NetworkX - unele matrice de adiacenta nu corespund cu grafurile aferente.
            # temp = nx.Graph()
            # temp.add_edges_from([(5, 6), (5, 7)])
            # temp_mat = nx.to_pandas_adjacency(temp, dtype=int)

            # Pentru lucrul cu matrice de adiacenta. Problema este descrisa mai sus.
            # mat_equal = False
            # if (adj_mat_query_elems.shape[0] * adj_mat_query_elems.shape[1]) == (adj_mat_data_elems.shape[0] * adj_mat_data_elems.shape[1]):
            #     if (adj_mat_query_elems==adj_mat_data_elems).all():
            #         mat_equal = True

            # print()
            # print(query_graph.edges)
            # print(partial_solution)

            gr_isomorphic = False
            partial_solution_data_subgraph = nx.DiGraph()
            partial_solution_data_subgraph.add_edges_from(partial_solution)
            if nx.is_isomorphic(query_graph, partial_solution_data_subgraph):
                duplicate_occurence_list = []
                duplicate_occurence_indicator = False

                for complete_solution in complete_solutions:
                    duplicate_occurence_list.clear()
                    for partial_solution_edge in partial_solution:
                        finder = EdgeFinderTool(partial_solution_edge, complete_solution)
                        finder_value = finder.edge_found()
                        duplicate_occurence_list.append(finder_value)
                    duplicate_edge_counter = 0
                    for dup in duplicate_occurence_list:
                        if dup == True:
                            duplicate_edge_counter = duplicate_edge_counter + 1
                    if duplicate_edge_counter == len(duplicate_occurence_list):
                        duplicate_occurence_indicator = True
                        duplicate_occurence_list.clear()

                        # duplicate_edge_counter = 0
                        break

                if duplicate_occurence_indicator == False:
                    duplicate_occurence_list.clear()
                    gr_isomorphic = True
                    i = True
                    # if partial_solution not in complete_solutions:
                    c_sol = copy.deepcopy(partial_solution)
                    # print(is_joinable(3, [1,2], data_graph, query_graph_dict))
                    complete_solutions.append(c_sol)
                    print(c_sol)
                    for c_sol_elem in c_sol:
                        f1.write(str(c_sol_elem) + " ")
                    f1.write("\n")
                    # print("\nOne complete solution found!")
                    # print()
                    # print(Fore.GREEN + Style.BRIGHT + "List of complete solutions: ")
                    # print("List of complete solutions: ")
                    # for cs in complete_solutions:
                    #     print(cs)
                    # print()
                    # print(Style.RESET_ALL)
                else:
                    # print("Duplicate found")
                    duplicate_occurence_list.clear()

            else:
                # print("Adjacency matrix sizes do not match.")
                # print("Not isomorphic")
                pass

            partial_solution = copy.deepcopy(restore_state(partial_solution))
            # mat_equal = False # Pentru lucrul cu matrice de adiacenta. Problema este descrisa mai sus.
            gr_isomorphic = False
            # print("\nRestored state: " + str(partial_solution))

            # print()
            # partial_solution = []

            # print("Sliced partial solution: " + str(partial_solution))
            # print("Old current node: " + str(current_node))

            current_node = copy.deepcopy(partial_solution[-1])
            # current_node = []

            # print("New current node: " + str(current_node))
            # print("Next query vertex for new current node: " + str(next_query_vertex(current_node, query_graph_dict)))
            # print("OK")
            # print()

            # next_d = next_data_vertex(partial_solution, data_graph, query_graph_dict)

            # print("Next data vertex: " + str(next_d))
            # print(is_joinable(next_d, partial_solution, data_graph, query_graph_dict))


            # return partial_solution
            # partial_solution = []
            # candidate = []
            # restore_state(partial_solution)

            # PRIMUL APEL RECURSIV
            subgraph_search(partial_solution, query_graph_dict, current_node, data_graph)

        # VECHI
        # if partial_solution in complete_solutions:
        #     print("Already found.")
        #     # HOW MUCH DO WE BACKTRACK?
        #     partial_solution = copy.deepcopy(partial_solution[:1])
        #     print(partial_solution)
        #     current_node = copy.deepcopy(partial_solution[-1])
        #     print(current_node)
        #     subgraph_search(partial_solution, query_graph_dict, current_node, data_graph)
        # VECHI

    else:
        # if len(partial_solution) == 2:

        i = True
        candidate = next_data_edge(partial_solution, data_graph)
        # if candidate is not None:
        #     print("Candidate edge (data node id's): " + str(candidate))
        #     print("Candidate edge (data nodes label): " + str([data_graph.node[candidate[0]]['label'], data_graph.node[candidate[1]]['label']]))
        #     print("Positions log after choosing candidate: " + str(list(positions.items())))

        if candidate is None:  # go back a position with restore position()

            # print("Candidate: " + Fore.LIGHTRED_EX + str(candidate) + Style.RESET_ALL)
            # print()

            if partial_solution == []:
                # i = False



                # print("\n" + Fore.GREEN + Style.BRIGHT + "Backtracking results: ")
                print("Backtracking results: ")
                for cs in complete_solutions:
                    print(cs)
                # print(Style.RESET_ALL)
                # print("Finished. Press 'Enter' to close the window.")
                # input()
                print("Execution time for Backtracking Algorithm (seconds): ")
                total_time = timer() - start_time
                print(total_time)
                f2 = open("file_RI Homo_sapiens_udistr_32 PPI XDS_Algorithm_Recursive execution times.txt", "a")
                f2.write(str(total_time) + " ")
                f2.write("\n")
                f2.close()

                exit(0)

            # go back a position with restore position()
            # print("Going back a position.")
            # input("Continue execution?")
            partial_solution = copy.deepcopy(restore_state(partial_solution))  #partial_solution[:1])
            # print("Restored partial solution: " + str(partial_solution))
            if len(partial_solution) == 0:  # poz 0 = []
                current_node = []
                positions[1] = []  # poz 1 = []
                # positions[2] = []
            # else:
            #     current_node = copy.deepcopy(partial_solution[-1])

            if len(partial_solution) == 1:  # poz 0 = [x]
                current_node = copy.deepcopy(partial_solution[0])
                # positions[1] = []
                positions[2] = []  # poz 1 = []

            if len(partial_solution) == 2:  # poz 0 = [x], poz 1 = [y]
                current_node = copy.deepcopy(partial_solution[-1])
                positions[3] = []

            # print("Current node: " + str(current_node))
            # AL DOILEA APEL RECURSIV
            subgraph_search(partial_solution, query_graph_dict, current_node, data_graph)

        partial_solution = copy.deepcopy(update_state(candidate, partial_solution))
        # print("PARTIAL SOLUTION: " + str(partial_solution))

        # AL TREILEA APEL RECURSIV
        subgraph_search(partial_solution, query_graph_dict, candidate, data_graph)
        # restore_state(partial_solution)

    if i == False:
        print("Finished.")

# https://stackoverflow.com/questions/35964155/checking-if-list-is-a-sublist
def sublist2(lst1, lst2):
    def get_all_in(one, another):
        for element in one:
            if element in another:
                yield element
    for x1, x2 in zip(get_all_in(lst1, lst2), get_all_in(lst2, lst1)):
        if x1 != x2:
            return False
    return True


def remove_used_node_from_node_list(node):
    node_list_aux.remove(node)
    print(node_list_aux)

# def renew_node_list(old_node_list):
#     old_node_list = copy.deepcopy(list(small_graph.nodes()))
#     print(old_node_list)
#     return old_node_list

# Va prelua din graful data nodurile pentru fiecare pozitie al solutiei partiale.
# Astfel cautarea nu se va mai face direct in graful data, ci in multimea de refined candidates.
def obtainCandidates(query_node_label):
    candidates = []
    # if query_node is None:
    #     exit(0)
    for data_node in dataGraph.nodes():
        if query_node_label == dataGraph.nodes[data_node]['label']:
            candidates.append(data_node)
    return candidates

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

def obtainCandidateEdges(edge_node_0_label, edge_node_1_label):
        candidate_edges = []
        for data_edge in dataGraph.edges():
            if edge_node_0_label == dataGraph.nodes[data_edge[0]]['label']:
                if edge_node_1_label == dataGraph.nodes[data_edge[1]]['label']:
                    candidate_edges.append(data_edge)
        return candidate_edges


# # Cream graful de 1000 de muchii.
# # Il inseram in NetworkX
# # Adaugam label-urile nodurilor
#
# # Inseram in graful nx graful RI
# graph_format = Graph_Format("Homo_sapiens_udistr_32.gfd")
# graph_format.create_graph_from_RI_file()
# nx_ri_graph = graph_format.get_graph()
# # print(nx_ri_graph.nodes())
# # print(list(nx_ri_graph.edges())[2])
#
# # Noduri pentru 1000 de muchii, apoi 1000 muchii.
#
# # Cream un graf nou cu 1000 de muchii din graful RI
# nx_ri_graph_1000edges = nx.Graph()
# # nodes_for_1000_edges =
# nx_ri_graph_1000edges.add_edges_from(list(nx_ri_graph.edges())[:1000])
# # nodes_and_labels_dict = {}
# nodes_for_selected_1000_edges = list(nx_ri_graph_1000edges.nodes())
#
# aux_graph = nx.Graph()
# for node in nodes_for_selected_1000_edges:
#     aux_graph.add_node(node, label=nx_ri_graph.node[node]['label'])
# # for n in aux_graph.nodes(data=True):
# #     print(n)
# aux_graph.add_edges_from(list(nx_ri_graph.edges())[:1000])
# print("Number of graph edges: " + str(len(aux_graph.edges())))
# print("Nodes and labels of nodes: " + str(aux_graph.nodes(data=True)))
# print("Number of nodes: " + str(len(aux_graph.nodes(data=True))))
#
# graph_for_bactracking_search = aux_graph
# data_graph = aux_graph
#
#
# query_nodes = ['1773', '1488', '1898', '2285']
# print("Query STwig: " + str(query_nodes))
# # Label-ul radacinii
# root_label = graph_for_bactracking_search.node[query_nodes[0]]['label']
# # Label-urile vecinilor din lista
# neighbor_labels = []
# for n in query_nodes[1:]:
#     neighbor_labels.append(graph_for_bactracking_search.node[n]['label'])
#
# query_node_labels = []
# query_node_labels.append(root_label)
# for nl in neighbor_labels:
#     query_node_labels.append(nl)
# print("query_node_labels: " + str(query_node_labels))

##################################################################
# Graf data foarte mic, 10 noduri, 4 label-uri.
# small_graph = nx.Graph()
# small_graph_nodes = [1,2,3,4,5,6,7,8,9,10]
# # Sortarea ascendenta la string este diferita de cea a de la tipul int
# small_graph_nodes.sort()
# small_graph_edges = [[1, 2], [1, 3], [5, 6], [5, 7], [1, 6], [1, 7], [1, 10], [9, 10], [9, 7], [5, 10], [5, 3], [2, 3], [2, 4], [2, 10], [2, 8], [10, 7], [10, 8], [1, 8], [1, 4], [5, 4], [5, 8], [9, 8]]
# small_graph.add_nodes_from(small_graph_nodes)
# small_graph.add_edges_from(small_graph_edges)
# node_attr = ["a", "b", "c", "d", "a", "b", "c", "d", "a", "b"]
# node_attr_dict = dict(zip(sorted(small_graph.nodes()), node_attr))
# print(node_attr_dict.items())
# nx.set_node_attributes(small_graph, node_attr_dict, 'label')
# print(small_graph.nodes(data=True))
# print(small_graph.edges())
##################################################################
##################################################################
# GRAFUL DATA DIN NEO4J
# neograph_data = Graph("bolt://127.0.0.1:7690", auth=("neo4j", "changeme")) # Data Graph RI - Cluster Neo4J
neograph_data = Graph("bolt://127.0.0.1:7687", auth=("neo4j", "password"))  # Data Graph RI - O singura instanta de Neo4J

cqlQuery = "MATCH p=(n)-[r:PPI]->(m) return n.node_id, m.node_id"
result = neograph_data.run(cqlQuery).to_ndarray()
edge_list = result.tolist()
# print("edge_list: ")
# print(edge_list)
edge_list_integer_ids = []
for string_edge in edge_list:
    node1_int = int(string_edge[0])
    node2_int = int(string_edge[1])
    # edge_list_integer_ids.append([int(i) for i in string_edge]) # Problema
    edge_list_integer_ids.append([node1_int, node2_int])
# print("edge_list_integer_ids: ")
# print(edge_list_integer_ids)

dataGraph = nx.DiGraph()
# Muchiile grafului data sortate dupa id noduri. Nu e ok.
# dataGraph.add_edges_from(sorted(edge_list_integer_ids))
# RASPUNS: Muchiile grafului data nesortate dupa id noduri. Ordinea corecta al nodurilor din muchii, si anume ordinea originala din fisierul CSV si Neo4J.
# dataGraph.add_edges_from(edge_list_integer_ids)
for edge in edge_list_integer_ids:
    dataGraph.add_edge(edge[0], edge[1])

data_edges = dataGraph.edges()

# dataGraph_undirected = nx.Graph() # Problema
# dataGraph_undirected.add_edges_from(dataGraph.edges())

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
nx.set_node_attributes(dataGraph, node_attr_dict, 'label')
# Pentru conditiile VF2:
nx.set_node_attributes(dataGraph, False, 'matched')

#############################################################################
# # FUNCTIONAL:
# query_nodes = [1, 2, 3, 4]
# # query_nodes = [1, 2, 3]
# # query_nodes = [2, 3, 4]
# # query_nodes = [1, 2]
# # query_nodes = [3, 10]
# # query_nodes = [4, 10]
#
#
# print("Query STwig: " + str(query_nodes))
# # Label-ul radacinii
# root_label = small_graph.node[query_nodes[0]]['label']
# # Label-urile vecinilor din lista
# neighbor_labels = []
# for n in query_nodes[1:]:
#     neighbor_labels.append(small_graph.node[n]['label'])
#
# query_node_labels = []
# query_node_labels.append(root_label)
# for nl in neighbor_labels:
#     query_node_labels.append(nl)
# print("query_node_labels: " + str(query_node_labels))
# print()
# query_node_labels_source = copy.deepcopy(query_node_labels)
#
# query_edges_dict = OrderedDict(zip(query_nodes, query_node_labels_source))
# print("query_edges_dict: ")
# print(query_edges_dict.items())
# print()
# p_solution = []
# complete_solutions = []
# positions = OrderedDict().fromkeys([0,1,2,3])
# positions[0] = []
# positions[1] = []
# positions[2] = []
# positions[3] = []
# print(positions.items())
# node_list_aux = copy.deepcopy(list(small_graph.nodes()))
#######################################################################################

print()
# GRAFUL QUERY. Algoritmul va lucra doar cu label-urile acestor noduri.:
query_graph_gen = Query_Graph_Generator()
query_graph = query_graph_gen.gen_RI_query_graph()
query_graph_edges = list(query_graph.edges())
print("Query graph edges: " + str(query_graph_edges))
# Pentru conditiile VF2:
nx.set_node_attributes(query_graph, False, 'matched')

query_nodes = list(query_graph.nodes())
print("Query node id's: " + str(query_nodes))
query_matched_attributes = []
for n1 in list(query_graph.nodes()):
    query_matched_attributes.append(query_graph.nodes[n1]['matched'])
print("Query node 'matched' attributes: " + str(query_matched_attributes))

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
print("Query nodes labels: " + str(query_node_labels))
query_nodes_dict = OrderedDict(zip(query_nodes, query_node_labels))
# query_stwig1_dict_matched_attribute = OrderedDict(zip(query_nodes, query_node_matched_attribute_source))
print("Query nodes dict: " + str(list(query_nodes_dict.items())))
query_edge_labels = []
for q_edge in query_graph_edges:
    query_edge_labels.append([query_nodes_dict[q_edge[0]], query_nodes_dict[q_edge[1]]])

# print("query_edge_labels: " + str(query_edge_labels))
query_node_labels_source = copy.deepcopy(query_node_labels)
query_node_matched_attribute_source = copy.deepcopy(query_matched_attributes)

query_edges_dict = OrderedDict(zip(query_graph_edges, query_edge_labels))
query_stwig1_dict_matched_attribute = OrderedDict(zip(query_nodes, query_node_matched_attribute_source))
print("Query graph edges dictionary: " + str(list(query_edges_dict.items())))
print()
# adj_mat_query = nx.to_pandas_adjacency(query_graph, dtype=int)
print("query_stwig1_dict_matched_attribute: ")
print(list(query_stwig1_dict_matched_attribute.items()))
print()
# print("Data graph edges: ")
# print(list(dataGraph.edges()))
p_solution = []
complete_solutions = []
positions = OrderedDict().fromkeys([0, 1, 2, 3])
positions[0] = []
positions[1] = []
positions[2] = []
positions[3] = []
print("Positions log before first iteration: " + str(list(positions.items())))
node_list_aux = copy.deepcopy(list(dataGraph.nodes()))
####################################################################################

# Fisier text:
f1 = open("file_RI Homo_sapiens_udistr_32 PPI XDS_Algorithm_Recursive output.txt", "w+")

# Executia algoritmului Backtracking:
try:
    # subgraph_search(p_solution, query_edges_dict, [], small_graph)
    start_time = timer()
    subgraph_search(p_solution, query_edges_dict, [], dataGraph)

    # total_time = timer() - start_time
    # print("Timp total de executare algoritm Backtracking: " + str(total_time) + " secunde.")
except IndexError:
    tb = traceback.format_exc()
    print(tb)
# except SystemExit:
#     exit(0)



