from neo4j_test import neo4j_test
import networkx as nx

# test = neo4j_test()
# test._create_and_return_greeting()

# f = open('Homo_sapiens_udistr_32.gfd', "w+")
# print(f.)
with open('Homo_sapiens_udistr_32.gfd') as f:
    lines = f.readlines()
# for line in lines:
#     print(line)
print(lines[0])
input_graph = nx.Graph()
num_nodes = int(lines[1])
print(num_nodes)
nodes_attr_list = []
for i in range(2, num_nodes + 2):
    spl = lines[i].split(sep="\n")[0]
    nodes_attr_list.append(spl)
for attr in nodes_attr_list:
    print(attr)
num_edges = int(lines[num_nodes + 2])
print(num_edges)
edge_list = []
for i in range(num_nodes+3, len(lines)):
    line = [lines[i].split(sep="\n")[0], lines[i].split(sep="\n")[1]]
    new_edge = tuple(line[0].split(sep=" "), )
    edge_list.append(new_edge)
print(edge_list)

