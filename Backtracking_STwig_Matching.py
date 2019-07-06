from Graph_Format import Graph_Format
import networkx as nx

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


def match_stwig_backtracking(query_stwig, query_stwig_as_labels, data_graph, index, solution):
# Cate o lista cu noduri din graf pentru fiecare tip de nod din STwig. Atunci lucram doar cu cateva liste.


# Verificam daca exista solutie
#   Cum returnam mai multe solutii? Cum facem intoarcerea?
# Punem criteriul de validitate
# In caz de validitate, apelam din nou si construim astfel solutia


    # if solution == [[]] or len(solution[1]) == len(query_stwig[1]):

    # Verficam daca am gasit o solutie completa.
    if len(solution) > 1:
        if len(solution[1]) == len(query_stwig[1]):
            # print(solution[1][:2])
            if solution not in complete_solutions:
                print("Complete solution: " + str(solution))
                complete_solutions.append(solution)

            # for i in range(1, len(query_stwig_1[1])):
            #     # print(i)
            #     solution[1] = solution[1][:i]

            # return solution
    else:
        # Pentru radacina STwig-ului:
        if len(solution) == 1:
            # print(len(solution))
            for root in data_graph.nodes():
                # print("root: " + str(root))
                if data_graph.node[root]['label'] == query_stwig_1_as_labels[0]: # Avem un root al unei solutii
                    solution.insert(0,root)
                    print("root: " + str(query_stwig_1[0]))
                    print("root label: " + str(query_stwig_1_as_labels[0]))
                    # solution.append([])
                    print("-solution start: " + str(solution))
                    # match_stwig_backtracking(query_stwig, query_stwig_as_labels, data_graph, index, solution)
                    break
                    # La urma vom sterge radacina, si vom intra din nou pe ramura aceasta.
                    # Trebuie facut ca sa nu ia aceeasi radacina din nou.

        # Pentru frunzele STwig-ului:
        if len(solution) > 1:
            if len(solution[1]) < len(query_stwig_1[1]):
                for leaf_label in query_stwig_as_labels[1]:
                    valid_root = find_valid_leaf_with_label(leaf_label, solution, data_graph)
                    print("valid_root: " + valid_root)
                    solution[1].append(valid_root)
                    # print(solution)

                    # Trece la urmatoarea frunza
                    # solution[1] = solution[1][:3] # .append(valid_root)
                    print("solution before next rec call: " + str(solution))
                    match_stwig_backtracking(query_stwig_1, query_stwig_1_as_labels, data_graph, index, solution)

                    # Remove and replace last elem
                    # solution[1] = solution[1][:2]

                    # print("leaf_label selectat: " + str(leaf_label))
                    # for leaf in data_graph.nodes():
                    #     # print("--leaf: " + str(leaf))
                    #     if data_graph.node[leaf]['label'] == leaf_label:  # and leaf not in solution[1]: # Avem un nod te tipul unui leaf
                    #         print("     " + str(leaf))
                    #         # print("---leaf label: " + str(leaf_label))
                    #         if data_graph.has_edge(solution[0], leaf):  # Verificam daca este vecinatate de ordinul 1
                    #             solution[1].append(leaf)
                    #             # solution[1] = leaf_sol
                    #             print("     ^---Is neighbor => " + str(solution))





                # leaf_label = query_stwig_1_as_labels[1][0]
                # print("leaf_label selectat: " + str(leaf_label))
                #
                # for leaf in data_graph.nodes():
                #     print("--leaf: " + str(leaf))
                #     if data_graph.node[leaf]['label'] == leaf_label: # and leaf not in solution[1]: # Avem un nod te tipul unui leaf
                #         # print("---leaf label: " + str(leaf_label))
                #         # print("Same label")
                #         if data_graph.has_edge(solution[0], leaf): # Verificam daca este vecinatate de ordinul 1
                #         #     # print("----Is neighbor.")
                #
                #             solution[1].append(leaf)
                #             # solution[1].append(leaf_label)
                #             # print("     solution[1]: " + str(solution[1]))
                #             print("     partial solution: " + str(solution))
                        #
                        #     solution[1] = solution[1][:1] # Cu asta putem face intoarcerea

                                # for i in range(1, len(query_stwig_1[1])):
                                #     print(i)
                                #     solution[1] = solution[1][:i]
                                #     print(solution[1])
                                # index = index + 1
                                # match_stwig_backtracking(query_stwig, query_stwig_as_labels, data_graph, index, solution)
                            # else:
                            #     break
                                # return solution



def find_valid_leaf_with_label(leaf_label, solution, data_graph):
    for leaf in data_graph.nodes():
        if len(complete_solutions) != 0 and leaf not in complete_solutions[-1][1][-1]:
            if data_graph.node[leaf]['label'] == leaf_label:  # and leaf not in solution[1]: # Avem un nod te tipul unui leaf
                if data_graph.has_edge(solution[0], leaf):  # Verificam daca este vecinatate de ordinul 1
                    return leaf
        else:
            if data_graph.node[leaf]['label'] == leaf_label:  # and leaf not in solution[1]: # Avem un nod te tipul unui leaf
                if data_graph.has_edge(solution[0], leaf):  # Verificam daca este vecinatate de ordinul 1
                    return leaf

# Cream graful de 1000 de muchii.
# Il inseram in NetworkX
# Adaugam label-urile nodurilor

# Inseram in graful nx graful RI
graph_format = Graph_Format("Homo_sapiens_udistr_32.gfd")
graph_format.create_graph_from_RI_file()
nx_ri_graph = graph_format.get_graph()
# print(nx_ri_graph.nodes())
# print(list(nx_ri_graph.edges())[2])

# Noduri pentru 1000 de muchii, apoi 1000 muchii.

# Cream un graf nou cu 1000 de muchii din graful RI
nx_ri_graph_1000edges = nx.Graph()
# nodes_for_1000_edges =
nx_ri_graph_1000edges.add_edges_from(list(nx_ri_graph.edges())[:1000])
# nodes_and_labels_dict = {}
nodes_for_selected_1000_edges = list(nx_ri_graph_1000edges.nodes())

aux_graph = nx.Graph()
for node in nodes_for_selected_1000_edges:
    aux_graph.add_node(node, label=nx_ri_graph.node[node]['label'])
# for n in aux_graph.nodes(data=True):
#     print(n)
aux_graph.add_edges_from(list(nx_ri_graph.edges())[:1000])
print(len(aux_graph.edges()))
print(aux_graph.nodes(data=True))
print(len(aux_graph.nodes(data=True)))

graph_for_bactracking_search = aux_graph
data_graph = aux_graph


query_stwig_1 = ['1773', ['1488', '1898', '2285']]
# Label-ul radacinii
root_label = graph_for_bactracking_search.node[query_stwig_1[0]]['label']
# Label-urile vecinilor din lista
neighbor_labels = []
for n in query_stwig_1[1]:
    neighbor_labels.append(graph_for_bactracking_search.node[n]['label'])
query_stwig_1_as_labels = [root_label, neighbor_labels]
print("query_stwig_1_as_labels: " + str(query_stwig_1_as_labels))
print("Backtracking start: ")
complete_solutions = []
match_stwig_backtracking(query_stwig_1, query_stwig_1_as_labels, graph_for_bactracking_search, 0, [[]])
print("\nComplete solutions list: ")
for c in complete_solutions:
    print(c)
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


