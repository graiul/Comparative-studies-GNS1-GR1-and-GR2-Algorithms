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


# def permute(list, s):
#     if list == 1:
#         return s
#     else:
#         return [ y + x
#                  for y in permute(1, s)
#                  for x in permute(list - 1, s)
#                  ]


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




