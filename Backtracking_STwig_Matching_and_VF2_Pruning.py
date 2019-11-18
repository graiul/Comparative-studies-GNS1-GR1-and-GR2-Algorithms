import copy

# from Graph_Format import Graph_Format
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


# def permute(list, s):
#     if list == 1:
#         return s
#     else:
#         return [ y + x
#                  for y in permute(1, s)
#                  for x in permute(list - 1, s)
#                  ]
#
# print(permute(1, ["a","b","c"]))
# print(permute(2, ["a","b","c"]))

# class Backtracking_STwig_Matching:
#     partial_solution = []
#     query_stwig_dict = {}
#     current_node = None
#     data_graph = None

    # def match_stwig_backtracking(query_stwig, query_stwig_as_labels, data_graph, index, solution):
    # # Cate o lista cu noduri din graf pentru fiecare tip de nod din STwig. Atunci lucram doar cu cateva liste.
    #
    #
    # # Verificam daca exista solutie
    # #   Cum returnam mai multe solutii? Cum facem intoarcerea?
    # # Punem criteriul de validitate
    # # In caz de validitate, apelam din nou si construim astfel solutia
    #
    #
    #     # if solution == [[]] or len(solution[1]) == len(query_stwig[1]):
    #     print("\n------------------------------")
    #     print("Input solution: " + str(solution))
    #     # Verficam daca am gasit o solutie completa.
    #     # if len(solution) > 1:
    #
    #     if is_valid(solution, query_stwig):
    #         cs = copy.deepcopy(solution)
    #         print("Complete solution: " + str(cs))
    #         complete_solutions.append(cs)
    #         print("Intermediary complete list: ")
    #         for c in complete_solutions:
    #             print(c)
    #         solution = back(solution, -1)
    #         print("Solution without last element: " + str(solution))
    #         print("Passing it on...")
    #         index = index - 2
    #         # new_leaf = find_valid_leaf_with_label(query_stwig_as_labels[3], solution, data_graph)
    #         # print("new_leaf: " + str(new_leaf))
    #         match_stwig_backtracking(query_stwig, query_stwig_as_labels, data_graph, index, solution)
    #
    #     else:
    #         if solution in complete_solutions:
    #             print("Already found.")
    #             print(back(solution, -2))
    #             solution = copy.deepcopy(back(solution, -2))
    #             # leaf_labels = copy.deepcopy(query_stwig_as_labels[1:])
    #             query_stwig_as_labels = copy.deepcopy(query_stwig_1_as_labels_source)
    #             match_stwig_backtracking(query_stwig, query_stwig_as_labels, data_graph, 1, solution)
    #
    #         # Pentru radacina STwig-ului:
    #         if len(solution) == 0:
    #             # print(len(solution))
    #             for root in data_graph.nodes():
    #                 # print("root: " + str(root))
    #                 if data_graph.node[root]['label'] == query_stwig_as_labels[0]: # Avem un root al unei solutii
    #                     solution.insert(0,root)
    #                     print("root: " + str(query_stwig[0]))
    #                     print("root label: " + str(query_stwig_as_labels[0]))
    #                     # solution.append([])
    #                     print("-solution start: " + str(solution))
    #                     # match_stwig_backtracking(query_stwig, query_stwig_as_labels, data_graph, index, solution)
    #                     break
    #
    #
    #                     # La urma vom sterge radacina, si vom intra din nou pe ramura aceasta.
    #                     # Trebuie facut ca sa nu ia aceeasi radacina din nou.
    #
    #         # Pentru O FRUNZA STwig-ului:
    #         if len(solution) >= 1:
    #             if len(solution[1:]) < len(query_stwig[1:]):
    #
    #                 print("query_stwig_as_labels: ")
    #                 print(query_stwig_as_labels)
    #                 leaf_labels = copy.deepcopy(query_stwig_as_labels[1:])
    #                 print("leaf_labels: ")
    #                 print(leaf_labels)
    #
    #                 # if len(solution[1:]) > 0:
    #                 if len(leaf_labels) > 0:
    #                     solution_leafs_number = len(solution[1:])
    #                     print("solution_leafs_number: ")
    #                     print(solution_leafs_number)
    #                     print("leaf_labels without already found node labels: ")
    #                     new_list_leaf_labels = leaf_labels[solution_leafs_number:]
    #                     print(new_list_leaf_labels)
    #                     if len(new_list_leaf_labels) > 0:
    #                         leaf_label = new_list_leaf_labels[0]
    #                         print("leaf_label")
    #                         print(leaf_label)
    #
    #                     else:
    #                         leaf_label = leaf_labels[0]
    #
    #                 print("leaf label for next valid leaf: ")
    #                 print(leaf_label)
    #                 print("label list for next iteration: ")
    #                 del leaf_labels[0]
    #                 print(leaf_labels)
    #
    #
    #                 print("query_stwig_as_labels for next iteration: MUST BE EQUAL WITH ABOVE LIST")
    #                 # query_stwig_as_labels.remove(leaf_label)
    #
    #                 position_for_replacement = query_stwig_1_as_labels_source.index(query_stwig_as_labels[0])
    #                 position_for_replacement = position_for_replacement + 1
    #                 print("position_for_replacement: ")
    #                 print(position_for_replacement)
    #                 del query_stwig_as_labels[0]
    #
    #
    #                 print(query_stwig_as_labels[1:])
    #                 valid_leaf = find_valid_leaf_with_label(leaf_label, solution, data_graph, position_for_replacement)
    #
    #                 print("valid_leaf: " + str(valid_leaf))
    #                 solution.append(valid_leaf)
    #                 # print(solution)
    #
    #                 # Trece la urmatoarea frunza
    #                 # solution[1] = solution[1][:3] # .append(valid_root)
    #                 print("Solution before next rec call: " + str(solution))
    #                 if index <= len(query_stwig_as_labels)-1:
    #                     index = index + 1
    #                     print("index: " + str(index))
    #                     match_stwig_backtracking(query_stwig, query_stwig_as_labels, data_graph, index, solution)
    #                 else:
    #                     print("Found first solution. Must pass it on.")
    #                     print("Refreshed query_stwig_1_as_labels: ")
    #                     query_stwig_1_as_labels = copy.deepcopy(query_stwig_1_as_labels_source)
    #                     print(query_stwig_1_as_labels)
    #                     match_stwig_backtracking(query_stwig, query_stwig_1_as_labels, data_graph, index, solution)
    #
    #
    #
    #
    #                 # leaf_label = query_stwig_1_as_labels[1][0]
    #                 # print("leaf_label selectat: " + str(leaf_label))
    #                 #
    #                 # for leaf in data_graph.nodes():
    #                 #     print("--leaf: " + str(leaf))
    #                 #     if data_graph.node[leaf]['label'] == leaf_label: # and leaf not in solution[1]: # Avem un nod te tipul unui leaf
    #                 #         # print("---leaf label: " + str(leaf_label))
    #                 #         # print("Same label")
    #                 #         if data_graph.has_edge(solution[0], leaf): # Verificam daca este vecinatate de ordinul 1
    #                 #         #     # print("----Is neighbor.")
    #                 #
    #                 #             solution[1].append(leaf)
    #                 #             # solution[1].append(leaf_label)
    #                 #             # print("     solution[1]: " + str(solution[1]))
    #                 #             print("     partial solution: " + str(solution))
    #                         #
    #                         #     solution[1] = solution[1][:1] # Cu asta putem face intoarcerea
    #
    #                                 # for i in range(1, len(query_stwig_1[1])):
    #                                 #     print(i)
    #                                 #     solution[1] = solution[1][:i]
    #                                 #     print(solution[1])
    #                                 # index = index + 1
    #                                 # match_stwig_backtracking(query_stwig, query_stwig_as_labels, data_graph, index, solution)
    #                             # else:
    #                             #     break
    #                                 # return solution
    #
    # def find_valid_leaf_with_label(leaf_label, solution, data_graph, position):
    #     valid_leafs_for_position = []
    #
    #     print("find_valid_leaf_with_label execution: ")
    #     # print(len(data_graph.nodes()))
    #     print("     leaf_label: " + leaf_label)
    #     # print(data_graph.has_node('3301'))
    #         # print(leaf)
    #         # print(type(leaf))
    #
    #     if len(complete_solutions) == 0:
    #         for leaf in data_graph.nodes():
    #
    #             # print("FIRST VALIDATION IF")
    #             if data_graph.node[leaf]['label'] == leaf_label:  # and leaf not in solution[1]: # Avem un nod te tipul unui leaf
    #                     print("     " + str(leaf) + " " + str(leaf_label))
    #
    #                     # if data_graph.has_edge(solution[0], leaf):  # Verificam daca este vecinatate de ordinul 1
    #                     if leaf in data_graph.neighbors(solution[0]):
    #                         # print("YES")
    #                         print("find_valid_leaf_with_label execution end on FIRST VALIDATION IF ")
    #
    #                         return leaf
    #
    #
    #     # Aici vine solutia fara ultimul element dupa gasirea primei solutii complete
    #     if len(complete_solutions) != 0:
    #         print("     SECOND VALIDATION IF - USED WHEN WE ALREADY HAD A COMPLETE SOLUTION")
    #         print("         complete_solutions until this iteration: ")
    #         print("         " + str(complete_solutions))
    #         for c_sol in complete_solutions:
    #             print("completed solution selected for comparison: ")
    #             print("     " + str(c_sol))
    #             # print("     " + str(c_sol[-1]))
    #             for leaf in data_graph.nodes():
    #                 # print(leaf)
    #                 # if leaf == c_sol[-1]:
    #                     # print("^---leaf already used")
    #
    #                 if leaf != c_sol[position]:
    #                     print("leaf from completed solution selected for comparison : ")
    #                     print(c_sol[position])
    #                     print(leaf)
    #                     print("^---leaf is different than the one in the complete solutions")
    #                     print("    and its label is: " + str(data_graph.node[leaf]['label']))
    #                     print("    The current selected leaf label is: " + str(leaf_label))
    #
    #                     if data_graph.node[leaf]['label'] == leaf_label:  # and leaf not in solution[1]: # Avem un nod te tipul unui leaf
    #                         if leaf in data_graph.neighbors(solution[0]):
    #                             print("     RETURNED VALID LEAF: " + str(leaf))
    #                             return leaf
    #                             # if leaf not in valid_leafs_for_position:
    #                             #     valid_leafs_for_position.append(leaf)
    #                             #     print("    APPENDED LEAF TO VALID LEAFS FOR POSITION: " + str(leaf))
    #
    #         # valid_leafs_for_position.sort()
    #         # print("valid_leafs_for_position: ")
    #         # print(valid_leafs_for_position)
    #         # leaf_to_return = valid_leafs_for_position[-1]
    #         # del valid_leafs_for_position[-1]
    #         # print("find_valid_leaf_with_label execution end on SECOND VALIDATION IF ")
    #         # return leaf_to_return
    #
    #
    # def back(solution, pos):
    #     to_del = copy.deepcopy(solution)
    #     to_del = to_del[:pos]
    #     # del to_del[pos]
    #     # print("sol_aux: ")
    #     # print(solution)
    #     return to_del
    #
    # def is_valid(solution, query_stwig):
    #     if len(solution[1:]) == len(query_stwig[1:]):
    #         # print(solution[1][:2])
    #         if solution not in complete_solutions:
    #             return True

    #---------------------------------------------------

    # def __init__(self, partial_solution, query_stwig_dict, current_node, data_graph):
    #     self.partial_solution = partial_solution
    #     self.query_stwig_dict = query_stwig_dict
    #     self.current_node = current_node
    #     self.data_graph = data_graph

# data_node_to_be_joined trebuie luat din filter_candidates.
def is_joinable(data_node_to_be_joined, partial_solution, data_graph, query_stwig_as_dict):

    found = False

    # print("\nis_joinable exec:")
    # print("input data node id: " + str(data_node_to_be_joined))
    data_node_label = data_graph.node[data_node_to_be_joined]['label']
    # print("data node label: " + str(data_node_label))
    # print("query_stwig_as_dict: ")
    # print(query_stwig_as_dict.items())
    # print("first query stwig node id: " + str(list(query_stwig_as_dict.items())[0][0]))
    # print("first query stwig node label: " + str(list(query_stwig_as_dict.items())[0][1]))


    if len(complete_solutions) > 0:
        # for sol in complete_solutions:
        sol = complete_solutions[-1]
            # print("complete solution selected for comparison: " + str(sol))
            # print(node)

        # pt al patrulea element:
        if len(partial_solution) <= len(list(query_stwig_as_dict.items())):
            if len(partial_solution) == 3:
                if data_node_to_be_joined not in partial_solution:

                    # if node != sol[2]:

                    aux = copy.deepcopy(partial_solution)
                    aux.append(data_node_to_be_joined)
                    pos = aux.index(aux[-1])
                    if aux not in complete_solutions:

                        if data_node_to_be_joined not in positions[2]:
                        # print("node: " + str(node))
                        # print("positions[2]: " + str(positions[2]))

                            # if data_node_to_be_joined in list(nx.ego_graph(data_graph, partial_solution[0], radius=1, center=True, undirected=True, distance=None).nodes()):

                            if data_graph.has_edge(positions[0][len(positions[0]) - 1], data_node_to_be_joined):

                                # if data_graph.node[data_node_to_be_joined]['label'] == query_stwig_as_dict[list(query_stwig_as_dict.keys())[3]]:

                                if list(query_stwig_as_dict.items())[3][1] == data_node_label:
                                    found = True

                                    # remove_used_node_from_node_list(node)

                                    if aux[-1] not in positions[pos]:
                                        positions[pos].append(aux[-1])
                                    # print("Positions log: " + str(list(positions.items())))
                                    # print()

        # pt al treilea element(a doua frunza):
        if len(partial_solution) <= len(list(query_stwig_as_dict.items())):
            if len(partial_solution) == 2:
                # print("We entered the execution for the third element (the second leaf)")

                if data_node_to_be_joined not in partial_solution:

                    # if node != sol[2]:

                    # print("positions[1], first leaf elements already used for data STwigs: " + str(positions[1]))

                    aux = copy.deepcopy(partial_solution)
                    aux.append(data_node_to_be_joined)
                    pos = aux.index(aux[-1])
                    if aux not in complete_solutions:

                        if data_node_to_be_joined not in positions[2]:
                        # print("node: " + str(node))
                        # print("positions[2]: " + str(positions[2]))

                            # if data_node_to_be_joined in list(nx.ego_graph(data_graph, partial_solution[0], radius=1, center=True, undirected=True, distance=None).nodes()):

                            # print("Checking if second leaf has edge with root.")
                            # print("Root: " + str(positions[0][len(positions[0]) - 1]))
                            # print("Potential leaf: " + str(data_node_to_be_joined))
                            # print("Potential leaf label: " + str(data_node_label))
                            if data_graph.has_edge(positions[0][len(positions[0]) - 1], data_node_to_be_joined):

                                # if data_graph.node[data_node_to_be_joined]['label'] == query_stwig_as_dict[list(query_stwig_as_dict.keys())[2]]:

                                # print("Label of the second leaf of the query STwig: " + str(list(query_stwig_as_dict.items())[2][1]))
                                # print("Label of data node verified: " + str(data_node_label))
                                if list(query_stwig_as_dict.items())[2][1] == data_node_label:
                                    found = True

                                    # remove_used_node_from_node_list(node)

                                    if aux[-1] not in positions[pos]:
                                        positions[pos].append(aux[-1])
                                    # print("Positions log: " + str(list(positions.items())))
                                    # print()

        # pt al doilea element(prima frunza):
        if len(partial_solution) <= len(list(query_stwig_as_dict.items())):
            if len(partial_solution) == 1:
                # print("We entered the execution for the second element (the first leaf)")

                if data_node_to_be_joined not in partial_solution:

                    # if node != sol[1]:

                    # print("positions[0], root elements already used for data STwigs: " + str(positions[0]))


                    aux = copy.deepcopy(partial_solution)
                    if list(query_stwig_as_dict.items())[1][1] == data_node_label:

                        aux.append(data_node_to_be_joined)
                        pos = aux.index(aux[-1])
                        if aux not in complete_solutions:

                            if data_node_to_be_joined not in positions[1]:
                                # root_label = query_stwig_as_dict[1]
                                # if data_graph.node[node]['label'] == root_label:

                                # if data_node_to_be_joined in list(nx.ego_graph(data_graph, partial_solution[0], radius=1, center=True, undirected=True, distance=None).nodes()):

                                # Verificam daca label-ul primei frunze al STwig-ului query are aceeasi valoare ca si label-ul nodului data primit ca si parametru
                                # si care sa cauta pentru pozitia primei frunze.

                                # Trebuie sa existe muchie intre nodul de pe prima poz a sol partiale actuale(radacina), deci tot timpul ultimul nod
                                # din log-ul nodurilor care se afla pe prima pozitie
                                if data_graph.has_edge(positions[0][len(positions[0])-1], data_node_to_be_joined):

                                    # if data_graph.node[data_node_to_be_joined]['label'] == query_stwig_as_dict[list(query_stwig_as_dict.keys())[1]]:

                                    # print("Label of the first leaf of the query STwig: " + str(list(query_stwig_as_dict.items())[1][1]))
                                    # print("Label of data node verified: " + str(data_node_label))
                                    if list(query_stwig_as_dict.items())[1][1] == data_node_label:
                                        found = True
                                        if aux[-1] not in positions[pos]:
                                            positions[pos].append(aux[-1])
                                        # print("Positions log: " + str(list(positions.items())))
                                        # print()

        # pt primul element, dupa mai multe executii. Trebuie schimbata radacina pentru noul STwig.
        if len(partial_solution) <= len(list(query_stwig_as_dict.items())):
            if len(partial_solution) == 0:
                if data_node_to_be_joined not in partial_solution:

                    # if node not in sol:

                        # aux = copy.deepcopy(partial_solution)
                        # aux.append(node)
                        # pos = aux.index(aux[-1])
                        # if aux not in complete_solutions:

                    if data_node_to_be_joined not in positions[0]:

                        # if node in list(nx.ego_graph(data_graph, list(query_stwig_as_dict.keys())[0], radius=1, center=True, undirected=True, distance=None).nodes()):

                        # if data_graph.node[data_node_to_be_joined]['label'] == query_stwig_as_dict[list(query_stwig_as_dict.keys())[len(partial_solution)]]:
                        if list(query_stwig_as_dict.items())[0][1] == data_node_label:
                            found = True
                            if data_node_to_be_joined not in positions[0]:
                                positions[0].append(data_node_to_be_joined)
                                # print("Positions log: " + str(list(positions.items())))
                                # print()

    # Pentru prima solutie la executie.

    # Problema pt moment este faptul ca urmatorul nod care ar trebui sa fie pe aceasta prima pozitie este inregistrat pe urmatoarea.
    # Acest lucru nu este corect, deoarece nu exista muchie intre ele, amandoua avand rolul de radacina pt STwig-ul data partial.
    if len(complete_solutions) == 0:

        # pt al primul element(radacina) la prima executie:
        # if len(partial_solution) <= len(list(query_stwig_as_dict.items())):
        if len(partial_solution) == 0:

            if data_node_to_be_joined not in partial_solution:

                # Aici facem verificarea dupa id-ul nodurilor. Trebuie modificat pentru a verifica dupa label, fara noduri.
                # if node in list(nx.ego_graph(data_graph, list(query_stwig_as_dict.keys())[0], radius=1, center=True, undirected=True, distance=None).nodes()):

                # Pentru primul element din STwig-ul data inceput nu trebuie verificat daca exista vreo muchie.
                # Si pentru cazurile pt care trebuie, nu trebuie sa mai iteram inca o data prin lista nodurilor grafului data.
                # for data_node in list(dataGraph.nodes()):
                #     if dataGraph.has_edge(node, data_node):

                # if query_graph.node[data_node_to_be_joined]['label'] == query_stwig_as_dict[list(query_stwig_as_dict.keys())[len(partial_solution)]]:

                # Daca label-ul radacinii STwig-ului query are aceeasi valoare ca si label-ul nodului data primit ca si parametru

                if list(query_stwig_as_dict.items())[0][1] == data_node_label:

                    print("Positions log before appending first node: " + str(list(positions.items())))
                    # print("Positions log for position[0] before appending first node: " + str(positions[0]))
                    print()

                    if data_node_to_be_joined not in positions[0]:
                        found = True

                        aux = copy.deepcopy(partial_solution)
                        aux.append(data_node_to_be_joined)
                        pos = aux.index(aux[-1])

                        positions[pos].append(data_node_to_be_joined)
                        # print("Positions log after appending first node: " + str(list(positions.items())))
                        # print()

        # pt al doilea element(prima frunza) la prima executie:
        # if len(partial_solution) <= len(list(query_stwig_as_dict.items())):
        if len(partial_solution) == 1:
                # print("We entered the execution for the second element (the first leaf)")

                if data_node_to_be_joined not in partial_solution:

                    # if node != sol[1]:

                    # print("positions[0], root elements already used for data STwigs: " + str(positions[0]))


                    aux = copy.deepcopy(partial_solution)
                    aux.append(data_node_to_be_joined)
                    pos = aux.index(aux[-1])
                    if aux not in complete_solutions:

                        if data_node_to_be_joined not in positions[1]:
                            # root_label = query_stwig_as_dict[1]
                            # if data_graph.node[node]['label'] == root_label:

                            # if data_node_to_be_joined in list(nx.ego_graph(data_graph, partial_solution[0], radius=1, center=True, undirected=True, distance=None).nodes()):

                            # Verificam daca label-ul primei frunze al STwig-ului query are aceeasi valoare ca si label-ul nodului data primit ca si parametru
                            # si care sa cauta pentru pozitia primei frunze.

                            # Trebuie sa existe muchie intre nodul de pe prima poz a sol partiale actuale(radacina), deci tot timpul ultimul nod
                            # din log-ul nodurilor care se afla pe prima pozitie
                            if data_graph.has_edge(positions[0][len(positions[0])-1], data_node_to_be_joined):

                                # if data_graph.node[data_node_to_be_joined]['label'] == query_stwig_as_dict[list(query_stwig_as_dict.keys())[1]]:

                                # print("Label of the first leaf of the query STwig: " + str(list(query_stwig_as_dict.items())[1][1]))
                                # print("Label of data node verified: " + str(data_node_label))
                                if list(query_stwig_as_dict.items())[1][1] == data_node_label:
                                    found = True
                                    if aux[-1] not in positions[pos]:
                                        positions[pos].append(aux[-1])
                                    # print("Positions log: " + str(list(positions.items())))
                                    # print()

        # pt al treilea element(a doua frunza) la prima executie:
        # if len(partial_solution) <= len(list(query_stwig_as_dict.items())):
        if len(partial_solution) == 2:
                # print("We entered the execution for the third element (the second leaf)")

                if data_node_to_be_joined not in partial_solution:

                    # if node != sol[2]:

                    # print("positions[1], first leaf elements already used for data STwigs: " + str(positions[1]))

                    aux = copy.deepcopy(partial_solution)
                    aux.append(data_node_to_be_joined)
                    pos = aux.index(aux[-1])
                    if aux not in complete_solutions:

                        if data_node_to_be_joined not in positions[2]:
                        # print("node: " + str(node))
                        # print("positions[2]: " + str(positions[2]))

                            # if data_node_to_be_joined in list(nx.ego_graph(data_graph, partial_solution[0], radius=1, center=True, undirected=True, distance=None).nodes()):

                            # print("Checking if second leaf has edge with root.")
                            # print("Root: " + str(positions[0][len(positions[0]) - 1]))
                            # print("Potential leaf: " + str(data_node_to_be_joined))
                            # print("Potential leaf label: " + str(data_node_label))
                            if data_graph.has_edge(positions[0][len(positions[0]) - 1], data_node_to_be_joined):

                                # if data_graph.node[data_node_to_be_joined]['label'] == query_stwig_as_dict[list(query_stwig_as_dict.keys())[2]]:

                                # print("Label of the second leaf of the query STwig: " + str(list(query_stwig_as_dict.items())[2][1]))
                                # print("Label of data node verified: " + str(data_node_label))
                                if list(query_stwig_as_dict.items())[2][1] == data_node_label:
                                    found = True

                                    # remove_used_node_from_node_list(node)

                                    if aux[-1] not in positions[pos]:
                                        positions[pos].append(aux[-1])
                                    # print("Positions log: " + str(list(positions.items())))
                                    # print()

        # pt al patrulea element la prima executie:
        # if len(partial_solution) <= len(list(query_stwig_as_dict.items())):
        if len(partial_solution) == 3:
                if data_node_to_be_joined not in partial_solution:

                    # if node != sol[2]:

                    aux = copy.deepcopy(partial_solution)
                    aux.append(data_node_to_be_joined)
                    pos = aux.index(aux[-1])
                    if aux not in complete_solutions:

                        if data_node_to_be_joined not in positions[2]:
                        # print("node: " + str(node))
                        # print("positions[2]: " + str(positions[2]))

                            # if data_node_to_be_joined in list(nx.ego_graph(data_graph, partial_solution[0], radius=1, center=True, undirected=True, distance=None).nodes()):

                            if data_graph.has_edge(positions[0][len(positions[0]) - 1], data_node_to_be_joined):

                                # if data_graph.node[data_node_to_be_joined]['label'] == query_stwig_as_dict[list(query_stwig_as_dict.keys())[3]]:

                                if list(query_stwig_as_dict.items())[3][1] == data_node_label:
                                    found = True

                                    # remove_used_node_from_node_list(node)

                                    if aux[-1] not in positions[pos]:
                                        positions[pos].append(aux[-1])
                                    # print("Positions log: " + str(list(positions.items())))
                                    # print()


    if found == True:
        return True

    return False

def update_state(node, partial_solution):
    print("update_state exec: ")
    c_node = copy.deepcopy(node)
    s = copy.deepcopy(partial_solution)
    s.append(c_node)
    print(s)
    return s
    # print("p_solution: " + str(p_solution))
    # p_solution = copy.deepcopy(partial_solution)
    # p_solution.append(c_node)
    # return p_solution

def restore_state(partial_solution):
    if len(partial_solution) > 0:
        del partial_solution[-1]
        # partial_solution = []
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
        # if is_joinable(list(query_stwig_dict.keys())[next_node_pos], partial_solution, data_graph, query_stwig_dict):
        return list(query_stwig_dict.keys())[next_node_pos]
        # else:
        #     next_query_vertex(list(query_stwig_dict.keys())[next_node_pos], query_stwig_dict)
    except IndexError:
        print("No more elements after this one in dict.")

def next_data_vertex(partial_solution, data_graph):
    # print()
    # print("next_data_vertex exec : ")
    # print("complete_solutions: " + str(complete_solutions))
    # print("partial_solution: " + str(partial_solution))

    found = False

    # print("\nis_joinable exec:")
    # print("input data node id: " + str(data_node_to_be_joined))

    # data_node_label = data_graph.node[data_node_to_be_joined]['label']

    # print("data node label: " + str(data_node_label))
    # print("query_stwig_as_dict: ")
    # print(query_stwig_as_dict.items())
    # print("first query stwig node id: " + str(list(query_stwig_as_dict.items())[0][0]))
    # print("first query stwig node label: " + str(list(query_stwig_as_dict.items())[0][1]))

    # Position 0:
    # Filter candidates folosind label-ul acestei pozitii
    position_label = query_stwig_1_as_labels_source[0]
    print("Position [0] label: " + str(position_label))
    filtered_candidates_pos_0 = filterCandidates(position_label)
    initial_match_values_pos_0_candidates = []
    for im_0 in filtered_candidates_pos_0:
        initial_match_values_pos_0_candidates.append(False)
    print("Candidates for position [0] and the mentioned label: " + str(filtered_candidates_pos_0))
    matched_true_false_data_nodes_pos_0_dict = OrderedDict(
        zip(filtered_candidates_pos_0, initial_match_values_pos_0_candidates))
    print("matched_true_false_data_nodes_pos_0_dict: " + str(list(matched_true_false_data_nodes_pos_0_dict.items())))

    # Position 1:
    # Filter candidates folosind label-ul acestei pozitii
    position_label = query_stwig_1_as_labels_source[1]
    print("Position [1] label: " + str(position_label))
    filtered_candidates_pos_1 = filterCandidates(position_label)
    initial_match_values_pos_1_candidates = []
    for im_1 in filtered_candidates_pos_1:
        initial_match_values_pos_1_candidates.append(False)
    print("Candidates for position [1] and the mentioned label: " + str(filtered_candidates_pos_1))
    matched_true_false_data_nodes_pos_1_dict = OrderedDict(
        zip(filtered_candidates_pos_1, initial_match_values_pos_1_candidates))
    print("matched_true_false_data_nodes_pos_1_dict: " + str(list(matched_true_false_data_nodes_pos_1_dict.items())))

    # Position 2:
    # Filter candidates folosind label-ul acestei pozitii
    position_label = query_stwig_1_as_labels_source[2]
    print("Position [2] label: " + str(position_label))
    filtered_candidates_pos_2 = filterCandidates(position_label)
    initial_match_values_pos_2_candidates = []
    for im_2 in filtered_candidates_pos_2:
        initial_match_values_pos_2_candidates.append(False)
    print("Candidates for position [2] and the mentioned label: " + str(filtered_candidates_pos_2))
    matched_true_false_data_nodes_pos_2_dict = OrderedDict(
        zip(filtered_candidates_pos_2, initial_match_values_pos_2_candidates))
    print("matched_true_false_data_nodes_pos_2_dict: " + str(list(matched_true_false_data_nodes_pos_2_dict.items())))

    # Position 3:
    # Filter candidates folosind label-ul acestei pozitii
    position_label = query_stwig_1_as_labels_source[3]
    print("Position [3] label: " + str(position_label))
    filtered_candidates_pos_3 = filterCandidates(position_label)
    initial_match_values_pos_3_candidates = []
    for im_3 in filtered_candidates_pos_3:
        initial_match_values_pos_3_candidates.append(False)
    print("Candidates for position [3] and the mentioned label: " + str(filtered_candidates_pos_3))
    matched_true_false_data_nodes_pos_3_dict = OrderedDict(
        zip(filtered_candidates_pos_3, initial_match_values_pos_3_candidates))
    print("matched_true_false_data_nodes_pos_3_dict: " + str(list(matched_true_false_data_nodes_pos_3_dict.items())))




    # Pentru prima solutie la executie.

    # Problema pt moment este faptul ca urmatorul nod care ar trebui sa fie pe aceasta prima pozitie este inregistrat pe urmatoarea.
    # Acest lucru nu este corect, deoarece nu exista muchie intre ele, amandoua avand rolul de radacina pt STwig-ul data partial.
    if len(complete_solutions) == 0:

        # pt primul element(radacina) la prima executie:
        if len(partial_solution) == 0:

            for data_node_to_be_joined in filtered_candidates_pos_0:
                if data_node_to_be_joined not in partial_solution:

                    # Aici facem verificarea dupa id-ul nodurilor. Trebuie modificat pentru a verifica dupa label, fara noduri.
                    # if node in list(nx.ego_graph(data_graph, list(query_stwig_as_dict.keys())[0], radius=1, center=True, undirected=True, distance=None).nodes()):

                    # Pentru primul element din STwig-ul data inceput nu trebuie verificat daca exista vreo muchie.
                    # Si pentru cazurile pt care trebuie, nu trebuie sa mai iteram inca o data prin lista nodurilor grafului data.
                    # for data_node in list(dataGraph.nodes()):
                    #     if dataGraph.has_edge(node, data_node):

                    # if query_graph.node[data_node_to_be_joined]['label'] == query_stwig_as_dict[list(query_stwig_as_dict.keys())[len(partial_solution)]]:

                    # Daca label-ul radacinii STwig-ului query are aceeasi valoare ca si label-ul nodului data primit ca si parametru

                    # if list(query_stwig_dict.items())[0][1] == data_node_label:

                    print("Positions log before appending first node: " + str(list(positions.items())))
                    # print("Positions log for position[0] before appending first node: " + str(positions[0]))
                    print()

                    if data_node_to_be_joined not in positions[0]:
                        if matched_true_false_data_nodes_pos_0_dict[data_node_to_be_joined] == False:

                            found = True

                            aux = copy.deepcopy(partial_solution)
                            aux.append(data_node_to_be_joined)
                            pos = aux.index(aux[-1])

                            positions[pos].append(data_node_to_be_joined)
                            matched_true_false_data_nodes_pos_0_dict[data_node_to_be_joined] = True
                            break
                            # print("Positions log after appending first node: " + str(list(positions.items())))
                            # print()

        # pt al doilea element(prima frunza) la prima executie:
        if len(partial_solution) == 1:
            # print("We entered the execution for the second element (the first leaf)")
            for data_node_to_be_joined in filtered_candidates_pos_1:
                if data_node_to_be_joined not in partial_solution:

                    aux = copy.deepcopy(partial_solution)
                    aux.append(data_node_to_be_joined)
                    pos = aux.index(aux[-1])
                    if aux not in complete_solutions:

                        if data_node_to_be_joined not in positions[1]:

                            # Verificam daca label-ul primei frunze al STwig-ului query are aceeasi valoare ca si label-ul nodului data primit ca si parametru
                            # si care sa cauta pentru pozitia primei frunze.

                            # Trebuie sa existe muchie intre nodul de pe prima poz a sol partiale actuale(radacina), deci tot timpul ultimul nod
                            # din log-ul nodurilor care se afla pe prima pozitie
                            if data_graph.has_edge(positions[0][len(positions[0]) - 1], data_node_to_be_joined):

                                # print("Label of the first leaf of the query STwig: " + str(list(query_stwig_as_dict.items())[1][1]))
                                # print("Label of data node verified: " + str(data_node_label))
                                # if list(query_stwig_as_dict.items())[1][1] == data_node_label:

                                if matched_true_false_data_nodes_pos_1_dict[data_node_to_be_joined] == False:
                                    found = True
                                    if aux[-1] not in positions[pos]:
                                        positions[pos].append(aux[-1])
                                    matched_true_false_data_nodes_pos_1_dict[data_node_to_be_joined] = True
                                    break
                                    # print("Positions log: " + str(list(positions.items())))
                                    # print()

        # pt al treilea element(a doua frunza) la prima executie:
        # if len(partial_solution) <= len(list(query_stwig_as_dict.items())):
        if len(partial_solution) == 2:
            # print("We entered the execution for the third element (the second leaf)")
            for data_node_to_be_joined in filtered_candidates_pos_2:
                if data_node_to_be_joined not in partial_solution:

                    aux = copy.deepcopy(partial_solution)
                    aux.append(data_node_to_be_joined)
                    pos = aux.index(aux[-1])
                    if aux not in complete_solutions:

                        if data_node_to_be_joined not in positions[2]:
                            # print("node: " + str(node))
                            # print("positions[2]: " + str(positions[2]))

                            # if data_node_to_be_joined in list(nx.ego_graph(data_graph, partial_solution[0], radius=1, center=True, undirected=True, distance=None).nodes()):

                            # print("Checking if second leaf has edge with root.")
                            # print("Root: " + str(positions[0][len(positions[0]) - 1]))
                            # print("Potential leaf: " + str(data_node_to_be_joined))
                            # print("Potential leaf label: " + str(data_node_label))
                            if data_graph.has_edge(positions[0][len(positions[0]) - 1], data_node_to_be_joined):

                                # if data_graph.node[data_node_to_be_joined]['label'] == query_stwig_as_dict[list(query_stwig_as_dict.keys())[2]]:

                                # print("Label of the second leaf of the query STwig: " + str(list(query_stwig_as_dict.items())[2][1]))
                                # print("Label of data node verified: " + str(data_node_label))
                                if matched_true_false_data_nodes_pos_2_dict[data_node_to_be_joined] == False:
                                    found = True
                                    if aux[-1] not in positions[pos]:
                                        positions[pos].append(aux[-1])
                                    matched_true_false_data_nodes_pos_2_dict[data_node_to_be_joined] = True
                                    break
                                    # print("Positions log: " + str(list(positions.items())))
                                    # print()

        # pt al patrulea element la prima executie:
        # if len(partial_solution) <= len(list(query_stwig_as_dict.items())):
        if len(partial_solution) == 3:
            for data_node_to_be_joined in filtered_candidates_pos_3:
                if data_node_to_be_joined not in partial_solution:

                    aux = copy.deepcopy(partial_solution)
                    aux.append(data_node_to_be_joined)
                    pos = aux.index(aux[-1])
                    if aux not in complete_solutions:

                        if data_node_to_be_joined not in positions[3]:
                            # print("node: " + str(node))
                            # print("positions[2]: " + str(positions[2]))

                            # if data_node_to_be_joined in list(nx.ego_graph(data_graph, partial_solution[0], radius=1, center=True, undirected=True, distance=None).nodes()):

                            if data_graph.has_edge(positions[0][len(positions[0]) - 1], data_node_to_be_joined):

                                # if data_graph.node[data_node_to_be_joined]['label'] == query_stwig_as_dict[list(query_stwig_as_dict.keys())[3]]:

                                if matched_true_false_data_nodes_pos_3_dict[data_node_to_be_joined] == False:
                                    found = True
                                    if aux[-1] not in positions[pos]:
                                        positions[pos].append(aux[-1])
                                    matched_true_false_data_nodes_pos_3_dict[data_node_to_be_joined] = True
                                    break
                                    # print("Positions log: " + str(list(positions.items())))
                                    # print()

    if len(complete_solutions) > 0:
        # for sol in complete_solutions:
        sol = complete_solutions[-1]
            # print("complete solution selected for comparison: " + str(sol))
            # print(node)

        # pt primul element, dupa mai multe executii. Trebuie schimbata radacina pentru noul STwig.
        if len(partial_solution) == 0:
            for data_node_to_be_joined in filtered_candidates_pos_0:
                if data_node_to_be_joined not in partial_solution:

                    # if node not in sol:

                        # aux = copy.deepcopy(partial_solution)
                        # aux.append(node)
                        # pos = aux.index(aux[-1])
                        # if aux not in complete_solutions:

                    if data_node_to_be_joined not in positions[0]:
                        if matched_true_false_data_nodes_pos_0_dict[data_node_to_be_joined] == False:
                            found = True
                            positions[0].append(data_node_to_be_joined)
                            matched_true_false_data_nodes_pos_0_dict[data_node_to_be_joined] = True
                            break
                            # print("Positions log: " + str(list(positions.items())))
                            # print()

        # pt al doilea element(prima frunza):
        if len(partial_solution) == 1:
            # print("We entered the execution for the second element (the first leaf)")
            for data_node_to_be_joined in filtered_candidates_pos_1:
                if data_node_to_be_joined not in partial_solution:

                    aux = copy.deepcopy(partial_solution)
                    aux.append(data_node_to_be_joined)
                    pos = aux.index(aux[-1])
                    if aux not in complete_solutions:

                        if data_node_to_be_joined not in positions[1]:
                            # root_label = query_stwig_as_dict[1]
                            # if data_graph.node[node]['label'] == root_label:

                            # if data_node_to_be_joined in list(nx.ego_graph(data_graph, partial_solution[0], radius=1, center=True, undirected=True, distance=None).nodes()):

                            # Verificam daca label-ul primei frunze al STwig-ului query are aceeasi valoare ca si label-ul nodului data primit ca si parametru
                            # si care sa cauta pentru pozitia primei frunze.

                            # Trebuie sa existe muchie intre nodul de pe prima poz a sol partiale actuale(radacina), deci tot timpul ultimul nod
                            # din log-ul nodurilor care se afla pe prima pozitie
                            if data_graph.has_edge(positions[0][len(positions[0])-1], data_node_to_be_joined):

                                if matched_true_false_data_nodes_pos_1_dict[data_node_to_be_joined] == False:

                                    # print("Label of the first leaf of the query STwig: " + str(list(query_stwig_as_dict.items())[1][1]))
                                    # print("Label of data node verified: " + str(data_node_label))
                                    if matched_true_false_data_nodes_pos_1_dict[data_node_to_be_joined] == False:
                                        found = True
                                        if aux[-1] not in positions[pos]:
                                            positions[pos].append(aux[-1])
                                        matched_true_false_data_nodes_pos_1_dict[data_node_to_be_joined] = True
                                        break
                                        # print("Positions log: " + str(list(positions.items())))
                                        # print()

        # pt al treilea element(a doua frunza):
            if len(partial_solution) == 2:
                # print("We entered the execution for the third element (the second leaf)")
                for data_node_to_be_joined in filtered_candidates_pos_2:
                    if data_node_to_be_joined not in partial_solution:

                        aux = copy.deepcopy(partial_solution)
                        aux.append(data_node_to_be_joined)
                        pos = aux.index(aux[-1])
                        if aux not in complete_solutions:

                            if data_node_to_be_joined not in positions[2]:
                            # print("node: " + str(node))
                            # print("positions[2]: " + str(positions[2]))

                                # if data_node_to_be_joined in list(nx.ego_graph(data_graph, partial_solution[0], radius=1, center=True, undirected=True, distance=None).nodes()):

                                # print("Checking if second leaf has edge with root.")
                                # print("Root: " + str(positions[0][len(positions[0]) - 1]))
                                # print("Potential leaf: " + str(data_node_to_be_joined))
                                # print("Potential leaf label: " + str(data_node_label))
                                if data_graph.has_edge(positions[0][len(positions[0]) - 1], data_node_to_be_joined):

                                    # if data_graph.node[data_node_to_be_joined]['label'] == query_stwig_as_dict[list(query_stwig_as_dict.keys())[2]]:

                                    # print("Label of the second leaf of the query STwig: " + str(list(query_stwig_as_dict.items())[2][1]))
                                    # print("Label of data node verified: " + str(data_node_label))
                                    if matched_true_false_data_nodes_pos_2_dict[data_node_to_be_joined] == False:
                                        found = True

                                        # remove_used_node_from_node_list(node)

                                        if aux[-1] not in positions[pos]:
                                            positions[pos].append(aux[-1])
                                        matched_true_false_data_nodes_pos_2_dict[data_node_to_be_joined] = True
                                        break
                                        # print("Positions log: " + str(list(positions.items())))
                                        # print()

        # pt al patrulea element:
        if len(partial_solution) == 3:
            for data_node_to_be_joined in filtered_candidates_pos_3:
                if data_node_to_be_joined not in partial_solution:

                    aux = copy.deepcopy(partial_solution)
                    aux.append(data_node_to_be_joined)
                    pos = aux.index(aux[-1])
                    if aux not in complete_solutions:

                        if data_node_to_be_joined not in positions[2]:
                        # print("node: " + str(node))
                        # print("positions[2]: " + str(positions[2]))

                            # if data_node_to_be_joined in list(nx.ego_graph(data_graph, partial_solution[0], radius=1, center=True, undirected=True, distance=None).nodes()):

                            if data_graph.has_edge(positions[0][len(positions[0]) - 1], data_node_to_be_joined):

                                # if data_graph.node[data_node_to_be_joined]['label'] == query_stwig_as_dict[list(query_stwig_as_dict.keys())[3]]:

                                if matched_true_false_data_nodes_pos_3_dict[data_node_to_be_joined] == False:
                                    found = True

                                    # remove_used_node_from_node_list(node)

                                    if aux[-1] not in positions[pos]:
                                        positions[pos].append(aux[-1])
                                    matched_true_false_data_nodes_pos_3_dict[data_node_to_be_joined] = True
                                    break
                                    # print("Positions log: " + str(list(positions.items())))
                                    # print()

# Cand trecem la o pozitie precedenta, frunzele de pe pozitia pt care am cautat in data trebuie sa fie marcate ca fiind matched=False.

    if found == True:
        return data_node_to_be_joined

    return None


    # for node in list(data_graph.nodes()):
        # print("data node id: " + str(node))
        # data_node_label = data_graph.node[node]['label']
        # print("data node label: " + str(data_node_label))
        # print("is joinable, true/false:")
        # print(is_joinable(node, partial_solution, data_graph, query_stwig_dict))
        # if is_joinable(node, partial_solution, data_graph, query_stwig_dict):
            # print("next_data_vertex exec end")
            # return node
    # return None

def subgraph_search(partial_solution, query_stwig_dict, current_node, data_graph):
    print()
    print("Started subgraph search: ")
    print(Back.WHITE + Fore.LIGHTBLUE_EX + Style.BRIGHT + "Partial solution given: " + str(partial_solution) + Style.RESET_ALL)
    i = False
    if len(partial_solution) == len(list(query_stwig_dict.items())):
        if partial_solution not in complete_solutions:
            i = True
            # if partial_solution not in complete_solutions:
            c_sol = copy.deepcopy(partial_solution)
            # print(is_joinable(3, [1,2], data_graph, query_stwig_dict))
            complete_solutions.append(c_sol)
            for c_sol_elem in c_sol:
                f1.write(str(c_sol_elem) + " ")
            f1.write("\n")
            print("One complete solution found!")
            print(Fore.GREEN + Style.BRIGHT + "List of complete solutions: ")
            for cs in complete_solutions:
                print(cs)
            print(Style.RESET_ALL)
            partial_solution = copy.deepcopy(restore_state(partial_solution))
            print("Restored state: " + str(partial_solution))

            print()
            # partial_solution = []

            # print("Sliced partial solution: " + str(partial_solution))
            # print("Old current node: " + str(current_node))

            current_node = copy.deepcopy(partial_solution[-1])
            # current_node = []

            # print("New current node: " + str(current_node))
            # print("Next query vertex for new current node: " + str(next_query_vertex(current_node, query_stwig_dict)))
            # print("OK")
            # print()

            # next_d = next_data_vertex(partial_solution, data_graph, query_stwig_dict)

            # print("Next data vertex: " + str(next_d))
            # print(is_joinable(next_d, partial_solution, data_graph, query_stwig_dict))


            # return partial_solution
            # partial_solution = []
            # candidate = []
            # restore_state(partial_solution)
            subgraph_search(partial_solution, query_stwig_dict, current_node, data_graph)

        # if partial_solution in complete_solutions:
        #     print("Already found.")
        #     # HOW MUCH DO WE BACKTRACK?
        #     partial_solution = copy.deepcopy(partial_solution[:1])
        #     print(partial_solution)
        #     current_node = copy.deepcopy(partial_solution[-1])
        #     print(current_node)
        #     subgraph_search(partial_solution, query_stwig_dict, current_node, data_graph)

    else:
        # if len(partial_solution) == 2:

        i = True
        candidate = next_data_vertex(partial_solution, data_graph)
        if candidate is not None:
            print("Candidate (data node id): " + str(candidate))
            print("Candidate (data node label): " + str(data_graph.node[candidate]['label']))
            print("Positions log after choosing candidate: " + str(list(positions.items())))

        if candidate is None:  # go back a position with restore position()



            print("Candidate: " + Fore.LIGHTRED_EX + str(candidate) + Style.RESET_ALL)
            # print()

            if partial_solution == []:
                # i = False

                print("\n" + Fore.GREEN + Style.BRIGHT + "Backtracking results: ")
                for cs in complete_solutions:
                    print(cs)
                print(Style.RESET_ALL)
                print("Finished. Press 'Enter' to close the window.")
                input()
                exit(0)

            # go back a position with restore position()
            print("Going back a position.")
            # input("Continue execution?")
            partial_solution = copy.deepcopy(restore_state(partial_solution)) #partial_solution[:1])
            print("Restored partial solution: " + str(partial_solution))
            if len(partial_solution) == 0:  # poz 0 = []
                current_node = []
                positions[1] = [] # poz 1 = []
                # positions[2] = []
            # else:
            #     current_node = copy.deepcopy(partial_solution[-1])

            if len(partial_solution) == 1: # poz 0 = [x]
                current_node = copy.deepcopy(partial_solution[0])
                # positions[1] = []
                positions[2] = [] # poz 1 = []

            if len(partial_solution) == 2: # poz 0 = [x], poz 1 = [y]
                current_node = copy.deepcopy(partial_solution[-1])
                positions[3] = []

            print("Current node: " + str(current_node))
            subgraph_search(partial_solution, query_stwig_dict, current_node, data_graph)


        partial_solution = copy.deepcopy(update_state(candidate, partial_solution))
        print("PARTIAL SOLUTION: " + str(partial_solution))

        subgraph_search(partial_solution, query_stwig_dict, candidate, data_graph)
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

def renew_node_list(old_node_list):
    old_node_list = copy.deepcopy(list(small_graph.nodes()))
    print(old_node_list)
    return old_node_list

# Va prelua din graful data nodurile pentru fiecare pozitie al solutiei partiale.
# Astfel cautarea nu se va mai face direct in graful data, ci in multimea de refined candidates.
def filterCandidates(query_node_label):
        candidates = []
        # if query_node is None:
        #     exit(0)
        for data_node in dataGraph.nodes():
            if query_node_label == dataGraph.node[data_node]['label']:
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
                if self.dataGraph.node[data_node]['matched'] == True:
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
                for yy in Cq[-1]:
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
# query_stwig_1 = ['1773', '1488', '1898', '2285']
# print("Query STwig: " + str(query_stwig_1))
# # Label-ul radacinii
# root_label = graph_for_bactracking_search.node[query_stwig_1[0]]['label']
# # Label-urile vecinilor din lista
# neighbor_labels = []
# for n in query_stwig_1[1:]:
#     neighbor_labels.append(graph_for_bactracking_search.node[n]['label'])
#
# query_stwig_1_as_labels = []
# query_stwig_1_as_labels.append(root_label)
# for nl in neighbor_labels:
#     query_stwig_1_as_labels.append(nl)
# print("query_stwig_1_as_labels: " + str(query_stwig_1_as_labels))

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

# GRAFUL DATA DIN NEO4J
# neograph_data = Graph("bolt://127.0.0.1:7690", auth=("neo4j", "changeme")) # Data Graph RI - Cluster Neo4J
neograph_data = Graph("bolt://127.0.0.1:7687", auth=("neo4j", "changeme"))  # Data Graph RI - O singura instanta de Neo4J

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

dataGraph = nx.Graph()
dataGraph.add_edges_from(sorted(edge_list_integer_ids))
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
# query_stwig_1 = [1, 2, 3, 4]
# # query_stwig_1 = [1, 2, 3]
# # query_stwig_1 = [2, 3, 4]
# # query_stwig_1 = [1, 2]
# # query_stwig_1 = [3, 10]
# # query_stwig_1 = [4, 10]
#
#
# print("Query STwig: " + str(query_stwig_1))
# # Label-ul radacinii
# root_label = small_graph.node[query_stwig_1[0]]['label']
# # Label-urile vecinilor din lista
# neighbor_labels = []
# for n in query_stwig_1[1:]:
#     neighbor_labels.append(small_graph.node[n]['label'])
#
# query_stwig_1_as_labels = []
# query_stwig_1_as_labels.append(root_label)
# for nl in neighbor_labels:
#     query_stwig_1_as_labels.append(nl)
# print("query_stwig_1_as_labels: " + str(query_stwig_1_as_labels))
# print()
# query_stwig_1_as_labels_source = copy.deepcopy(query_stwig_1_as_labels)
#
# query_stwig1_dict = OrderedDict(zip(query_stwig_1, query_stwig_1_as_labels_source))
# print("query_stwig1_dict: ")
# print(query_stwig1_dict.items())
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
# Pentru conditiile VF2:
nx.set_node_attributes(query_graph, False, 'matched')

query_stwig_1 = list(query_graph.nodes())
print("Query STwig node id's: " + str(query_stwig_1))
query_matched_attributes = []
for n1 in list(query_graph.nodes()):
    query_matched_attributes.append(query_graph.node[n1]['matched'])
print("Query STwig node 'matched' attributes: " + str(query_matched_attributes))

# Label-ul radacinii
# root_label = dataGraph.node[query_stwig_1[0]]['label']
root_label = query_graph.node[query_stwig_1[0]]['label']
# Label-urile vecinilor din lista
neighbor_labels = []
for n2 in query_stwig_1[1:]:
    # neighbor_labels.append(dataGraph.node[n]['label'])
    neighbor_labels.append(query_graph.node[n2]['label'])

query_stwig_1_as_labels = []
query_stwig_1_as_labels.append(root_label)
for nl in neighbor_labels:
    query_stwig_1_as_labels.append(nl)
print("query_stwig_1_as_labels: " + str(query_stwig_1_as_labels))
print()
query_stwig_1_as_labels_source = copy.deepcopy(query_stwig_1_as_labels)
query_stwig_1_matched_attribute_source = copy.deepcopy(query_matched_attributes)

query_stwig1_dict = OrderedDict(zip(query_stwig_1, query_stwig_1_as_labels_source))
query_stwig1_dict_matched_attribute = OrderedDict(zip(query_stwig_1, query_stwig_1_matched_attribute_source))
print("query_stwig1_dict: ")
print(list(query_stwig1_dict.items()))
print("query_stwig1_dict_matched_attribute: ")
print(list(query_stwig1_dict_matched_attribute.items()))
print()
p_solution = []
complete_solutions = []
positions = OrderedDict().fromkeys([0,1,2,3])
positions[0] = []
positions[1] = []
positions[2] = []
positions[3] = []
print("Positions log before first iteration: " + str(list(positions.items())))
node_list_aux = copy.deepcopy(list(dataGraph.nodes()))
####################################################################################

# Fisier text:
f1 = open("f1.txt", "w+")

# Executia algoritmului Backtracking:
try:
    # subgraph_search(p_solution, query_stwig1_dict, [], small_graph)
    start_time = timer()
    subgraph_search(p_solution, query_stwig1_dict, [], dataGraph)
    total_time = timer() - start_time
    print("Timp total de executare algoritm Backtracking: " + str(total_time) + " secunde.")
except IndexError:
    tb = traceback.format_exc()
    print(tb)
except SystemExit:
    exit(0)


# finally:
#     input("End execution?")

# complete_solutions = []
# b = Backtracking_STwig_Matching()
# b.subgraph_search([], query_stwig1_dict, [], small_graph)

# print(list(query_stwig1_dict.keys())[0])
# print(query_stwig1_dict[1])
# current_node_pos = list(query_stwig1_dict.keys()).index(2)
# print(current_node_pos)
# next_node_pos = current_node_pos + 1
# print(next_node_pos)
# print("Next element:")
# print(next_query_vertex(2, query_stwig1_dict))
# print(is_joinable(3, [1,2], small_graph, query_stwig1_dict))



# print("Backtracking start: ")
# complete_solutions = []
# match_stwig_backtracking(query_stwig_1, query_stwig_1_as_labels, small_graph, 1, [])
# print("\nComplete solutions list: ")
# for c in complete_solutions:
#     print(c)


# r = '1773'
# solution = [r, []]
# leaf_sol = []
# leaf_label = query_stwig_1_as_labels[1][0]
# for leaf_label in query_stwig_1_as_labels[1]:
#
#     print("leaf_label selectat: " + str(leaf_label))
#     for leaf in data_graph.nodes():
#         # print("--leaf: " + str(leaf))
#         if data_graph.node[leaf]['label'] == leaf_label:  # and leaf not in solution[1]: # Avem un nod te tipul unui leaf
#             print("     " + str(leaf))
#             # print("---leaf label: " + str(leaf_label))
#             if data_graph.has_edge(solution[0], leaf):  # Verificam daca este vecinatate de ordinul 1
#                 solution[1].append(leaf)
#                 # solution[1] = leaf_sol
#                 print("     ^---Is neighbor => " + str(solution))

        #         solution[1].append(leaf)
        #         # solution[1].append(leaf_label)
        #         # print("     solution[1]: " + str(solution[1]))
        #         print("     partial solution: " + str(solution))





# root_label_nodes_dict = {}
# for node in graph_for_bactracking_search.nodes():
#     if graph_for_bactracking_search.node[node]['label'] == query_stwig_1_as_labels[0]:
#         root_label_nodes_dict[query_stwig_1_as_labels[0]] = node
#
#
# leaf_labels_nodes_dict = {}
# if len(query_stwig_1_as_labels[1]) == 1:
#     leaf_label_1_nodes = []
#
#     for node in graph_for_bactracking_search.nodes():
#         if graph_for_bactracking_search.node[node]['label'] == query_stwig_1_as_labels[1][0]:
#             leaf_label_1_nodes.append(node)
#     leaf_labels_nodes_dict[query_stwig_1_as_labels[1][0]] = leaf_label_1_nodes
#
# elif len(query_stwig_1_as_labels[1]) == 2:
#     leaf_label_1_nodes = []
#     leaf_label_2_nodes = []
#     for node in graph_for_bactracking_search.nodes():
#         if graph_for_bactracking_search.node[node]['label'] == query_stwig_1_as_labels[1][0]:
#             leaf_label_1_nodes.append(node)
#         elif graph_for_bactracking_search.node[node]['label'] == query_stwig_1_as_labels[1][1]:
#             leaf_label_2_nodes.append(node)
#     leaf_labels_nodes_dict[query_stwig_1_as_labels[1][0]] = leaf_label_1_nodes
#     leaf_labels_nodes_dict[query_stwig_1_as_labels[1][1]] = leaf_label_2_nodes
#
#
# elif len(query_stwig_1_as_labels[1]) == 3:
#     leaf_label_1_nodes = []
#     leaf_label_2_nodes = []
#     leaf_label_3_nodes = []
#     for node in graph_for_bactracking_search.nodes():
#         if graph_for_bactracking_search.node[node]['label'] == query_stwig_1_as_labels[1][0]:
#             leaf_label_1_nodes.append(node)
#         elif graph_for_bactracking_search.node[node]['label'] == query_stwig_1_as_labels[1][1]:
#             leaf_label_2_nodes.append(node)
#         elif graph_for_bactracking_search.node[node]['label'] == query_stwig_1_as_labels[1][2]:
#             leaf_label_3_nodes.append(node)
#     leaf_labels_nodes_dict[query_stwig_1_as_labels[1][0]] = leaf_label_1_nodes
#     leaf_labels_nodes_dict[query_stwig_1_as_labels[1][1]] = leaf_label_2_nodes
#     leaf_labels_nodes_dict[query_stwig_1_as_labels[1][2]] = leaf_label_3_nodes
#
#
# elif len(query_stwig_1_as_labels[1]) == 4:
#     leaf_label_1_nodes = []
#     leaf_label_2_nodes = []
#     leaf_label_3_nodes = []
#     leaf_label_4_nodes = []
#     for node in graph_for_bactracking_search.nodes():
#         if graph_for_bactracking_search.node[node]['label'] == query_stwig_1_as_labels[1][0]:
#             leaf_label_1_nodes.append(node)
#         elif graph_for_bactracking_search.node[node]['label'] == query_stwig_1_as_labels[1][1]:
#             leaf_label_2_nodes.append(node)
#         elif graph_for_bactracking_search.node[node]['label'] == query_stwig_1_as_labels[1][2]:
#             leaf_label_3_nodes.append(node)
#         elif graph_for_bactracking_search.node[node]['label'] == query_stwig_1_as_labels[1][3]:
#             leaf_label_4_nodes.append(node)
#     leaf_labels_nodes_dict[query_stwig_1_as_labels[1][0]] = leaf_label_1_nodes
#     leaf_labels_nodes_dict[query_stwig_1_as_labels[1][1]] = leaf_label_2_nodes
#     leaf_labels_nodes_dict[query_stwig_1_as_labels[1][2]] = leaf_label_3_nodes
#     leaf_labels_nodes_dict[query_stwig_1_as_labels[1][3]] = leaf_label_4_nodes


