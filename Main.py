from neo4j_test import neo4j_test
import networkx as nx

with open('Homo_sapiens_udistr_32.gfd') as f:
    lines = f.readlines()
# for line in lines:
#     print(line)
# print(lines[0])
input_graph = nx.Graph()
num_nodes = int(lines[1])
# print(num_nodes)
nodes_attr_list = []
for i in range(2, num_nodes + 2):
    spl = lines[i].split(sep="\n")[0]
    nodes_attr_list.append(spl)
# for attr in nodes_attr_list:
#     print(attr)
num_edges = int(lines[num_nodes + 2])
# print(num_edges)
edge_list = []
for i in range(num_nodes+3, len(lines)):
    line = [lines[i].split(sep="\n")[0], lines[i].split(sep="\n")[1]]
    new_edge = tuple(line[0].split(sep=" "), )
    edge_list.append(new_edge)
# print(edge_list)
# Graf neorientat
graph = nx.Graph()
graph.add_edges_from(edge_list)
print(graph.edges())
node_attr_dict = dict(zip(graph.nodes(), nodes_attr_list))
nx.set_node_attributes(graph, node_attr_dict, 'label')
print(list(list(graph.nodes(data=True))[0][1].values()))
print(list(graph.nodes(data=True))[0][0])
# for node in graph.nodes(data=True):
#     print(node)
test = neo4j_test("bolt://localhost:7687", "neo4j", "graph")
test.insert_graph_in_db(graph)