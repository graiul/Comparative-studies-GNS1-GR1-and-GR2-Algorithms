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

def is_joinable(node, partial_solution, data_graph, query_stwig_as_dict):

    found = False

    print("\nis_joinable exec:")
    print("input node: " + str(node))
    print("query_stwig_as_dict: ")
    print(query_stwig_as_dict.items())
    print("first query stwig node id: " + str(list(query_stwig_as_dict.items())[0][0]))
    print("first query stwig node label: " + str(list(query_stwig_as_dict.items())[0][1]))


    if len(complete_solutions) > 0:
        # for sol in complete_solutions:
        sol = complete_solutions[-1]
            # print("complete solution selected for comparison: " + str(sol))
            # print(node)

        # pt al patrulea element:
        if len(partial_solution) <= len(list(query_stwig_as_dict.items())):
            if len(partial_solution) == 3:
                if node not in partial_solution:

                    # if node != sol[2]:

                    aux = copy.deepcopy(partial_solution)
                    aux.append(node)
                    pos = aux.index(aux[-1])
                    if aux not in complete_solutions:

                        if node not in positions[2]:
                        # print("node: " + str(node))
                        # print("positions[2]: " + str(positions[2]))

                            if node in list(nx.ego_graph(data_graph, partial_solution[0], radius=1, center=True, undirected=True, distance=None).nodes()):
                                if data_graph.node[node]['label'] == query_stwig_as_dict[list(query_stwig_as_dict.keys())[3]]:
                                    found = True

                                    # remove_used_node_from_node_list(node)

                                    if aux[-1] not in positions[pos]:
                                        positions[pos].append(aux[-1])
                                    print(positions.items())

        # pt ultima pos
        if len(partial_solution) <= len(list(query_stwig_as_dict.items())):
            if len(partial_solution) == 2:
                if node not in partial_solution:

                    # if node != sol[2]:

                    aux = copy.deepcopy(partial_solution)
                    aux.append(node)
                    pos = aux.index(aux[-1])
                    if aux not in complete_solutions:

                        if node not in positions[2]:
                        # print("node: " + str(node))
                        # print("positions[2]: " + str(positions[2]))

                            if node in list(nx.ego_graph(data_graph, partial_solution[0], radius=1, center=True, undirected=True, distance=None).nodes()):
                                if data_graph.node[node]['label'] == query_stwig_as_dict[list(query_stwig_as_dict.keys())[2]]:
                                    found = True

                                    # remove_used_node_from_node_list(node)

                                    if aux[-1] not in positions[pos]:
                                        positions[pos].append(aux[-1])
                                    print(positions.items())

        # pt mijloc
        if len(partial_solution) <= len(list(query_stwig_as_dict.items())):
            if len(partial_solution) == 1:

                if node not in partial_solution:

                    # if node != sol[1]:

                    aux = copy.deepcopy(partial_solution)
                    aux.append(node)
                    pos = aux.index(aux[-1])
                    if aux not in complete_solutions:

                        if node not in positions[1]:
                            # root_label = query_stwig_as_dict[1]
                            # if data_graph.node[node]['label'] == root_label:

                            if node in list(nx.ego_graph(data_graph, partial_solution[0], radius=1, center=True, undirected=True, distance=None).nodes()):
                                if data_graph.node[node]['label'] == query_stwig_as_dict[list(query_stwig_as_dict.keys())[1]]:
                                    found = True
                                    if aux[-1] not in positions[pos]:
                                        positions[pos].append(aux[-1])
                                    print(positions.items())

        # pt primul element, dupa mai multe executii. Trebuie schimbata radacina pentru noul STwig.
        if len(partial_solution) <= len(list(query_stwig_as_dict.items())):
            if len(partial_solution) == 0:
                if node not in partial_solution:

                    # if node not in sol:

                        # aux = copy.deepcopy(partial_solution)
                        # aux.append(node)
                        # pos = aux.index(aux[-1])
                        # if aux not in complete_solutions:

                    if node not in positions[0]:

                        # if node in list(nx.ego_graph(data_graph, list(query_stwig_as_dict.keys())[0], radius=1, center=True, undirected=True, distance=None).nodes()):

                        if data_graph.node[node]['label'] == query_stwig_as_dict[list(query_stwig_as_dict.keys())[len(partial_solution)]]:
                            found = True
                            # if node not in positions[0]:
                            positions[0].append(node)
                            print(positions.items())

    # Pentru prima solutie la executie.
    if len(complete_solutions) == 0:
        if len(partial_solution) <= len(list(query_stwig_as_dict.items())):
            if node not in partial_solution:
                # Aici facem verificarea dupa id-ul nodurilor. Trebuie modificat pentru a verifica dupa label, fara noduri.
                # if node in list(nx.ego_graph(data_graph, list(query_stwig_as_dict.keys())[0], radius=1, center=True, undirected=True, distance=None).nodes()):
                for data_node in list(dataGraph.nodes()):

                    if dataGraph.has_edge(node, data_node):
                        if query_graph.node[node]['label'] == query_stwig_as_dict[list(query_stwig_as_dict.keys())[len(partial_solution)]]:
                            found = True

                            aux = copy.deepcopy(partial_solution)
                            aux.append(node)
                            pos = aux.index(aux[-1])

                            if node not in positions[pos]:
                                positions[pos].append(node)
                            # print(positions.items())

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

def next_data_vertex(partial_solution, data_graph, query_stwig_dict):
    print()
    print("next_data_vertex exec : ")
    print("complete_solutions: " + str(complete_solutions))
    print("partial_solution: " + str(partial_solution))
    for node in list(data_graph.nodes()):
        print("data node id: " + str(node))
        data_node_label = data_graph.node[node]['label']
        print("data node label: " + str(data_node_label))
        print("is joinable, true/false:")
        print(is_joinable(node, partial_solution, data_graph, query_stwig_dict))
        if is_joinable(node, partial_solution, data_graph, query_stwig_dict):
            # print("next_data_vertex exec end")
            return node
    return None

def subgraph_search(partial_solution, query_stwig_dict, current_node, data_graph):
    print()
    print("Started subgraph search: ")
    print(Back.WHITE + Fore.LIGHTBLUE_EX + Style.BRIGHT + "Partial solution given: " + str(partial_solution))
    print(Style.RESET_ALL)
    i = False
    if len(partial_solution) == len(list(query_stwig_dict.items())):
        if partial_solution not in complete_solutions:
            i = True
            # if partial_solution not in complete_solutions:
            c_sol = copy.deepcopy(partial_solution)
            # print(is_joinable(3, [1,2], data_graph, query_stwig_dict))
            complete_solutions.append(c_sol)
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
        candidate = next_data_vertex(partial_solution, data_graph, query_stwig_dict)
        if candidate is not None:
            print("Candidate: " + str(candidate))
            # print(candidate)

        if candidate is None:  # go back a position with restore position()



            print("Candidate: " + Fore.LIGHTRED_EX + str(candidate))
            print(Style.RESET_ALL) # go back a position with restore position()

            if partial_solution == []:
                # i = False
                print("Finished. \nPress 'Enter' to close the window.")
                input()
                exit(0)

            print("Going back a position.")
            # input("Continue execution?")
            partial_solution = copy.deepcopy(restore_state(partial_solution)) #partial_solution[:1])
            print(partial_solution)
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




            print(current_node)
            subgraph_search(partial_solution, query_stwig_dict, current_node, data_graph)


        partial_solution = copy.deepcopy(update_state(candidate, partial_solution))


        print("PARTIAL SOLUTION: ")
        print(partial_solution)
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

# FUNCTIONAL:
# query_stwig_1 = [1773, 1488, 1898, 2285]

# Aici cream un obiect graf query:
query_graph_gen = Query_Graph_Generator()
query_graph = query_graph_gen.gen_RI_query_graph()
query_stwig_1 = list(query_graph.nodes())
print("Query STwig: " + str(query_stwig_1))
# Label-ul radacinii
# root_label = dataGraph.node[query_stwig_1[0]]['label']
root_label = query_graph.node[query_stwig_1[0]]['label']
# Label-urile vecinilor din lista
neighbor_labels = []
for n in query_stwig_1[1:]:
    # neighbor_labels.append(dataGraph.node[n]['label'])
    neighbor_labels.append(query_graph.node[n]['label'])

query_stwig_1_as_labels = []
query_stwig_1_as_labels.append(root_label)
for nl in neighbor_labels:
    query_stwig_1_as_labels.append(nl)
print("query_stwig_1_as_labels: " + str(query_stwig_1_as_labels))
print()
query_stwig_1_as_labels_source = copy.deepcopy(query_stwig_1_as_labels)

query_stwig1_dict = OrderedDict(zip(query_stwig_1, query_stwig_1_as_labels_source))
print("query_stwig1_dict: ")
print(query_stwig1_dict.items())
print()
p_solution = []
complete_solutions = []
positions = OrderedDict().fromkeys([0,1,2,3])
positions[0] = []
positions[1] = []
positions[2] = []
positions[3] = []
print("Positions log: ")
print(positions.items())
node_list_aux = copy.deepcopy(list(dataGraph.nodes()))
####################################################################################

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


