import copy
from collections import OrderedDict
import networkx as nx
from py2neo import Graph

from Query_Graph_Generator import Query_Graph_Generator

# stackoverflow.com/questions/752308/split-list-into-smaller-lists-split-in-half
def split_list(alist, wanted_parts=1):
    length = len(alist)
    return [alist[i*length // wanted_parts: (i+1)*length // wanted_parts]
            for i in range(wanted_parts)]

############################ Din GNS1_Backtracking_STwig_Matching_with_txt_file_printing si GR1_Algorithm ##########################################################
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
############################ Din GNS1_Backtracking_STwig_Matching_with_txt_file_printing si GR1_Algorithm ##########################################################

############################ Din GNS1_Backtracking_STwig_Matching_with_txt_file_printing si GR1_Algorithm ##########################################################
# GRAFUL DATA DIN NEO4J
# neograph_data = Graph("bolt://127.0.0.1:7690", auth=("neo4j", "changeme")) # Data Graph RI - Cluster Neo4J
neograph_data = Graph("bolt://127.0.0.1:7687", auth=("neo4j", "password"))  # Data Graph RI - O singura instanta de Neo4J

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
############################ Din GNS1_Backtracking_STwig_Matching_with_txt_file_printing si GR1_Algorithm ##########################################################


############################ GR1_Algorithm ##########################################################

query_stwig = list(query_stwig_1_dict.items())
data_graph_edges = copy.deepcopy(sorted(edge_list_integer_ids))
node_attributes_dictionary = OrderedDict(sorted(node_ids_as_integers_with_string_labels))

query_stwig_root_node = query_stwig[0]
query_stwig_root_node_label = query_stwig[0][1]
############################ GR1_Algorithm ##########################################################
# print(query_stwig)
parts =split_list(query_stwig, wanted_parts=2)
print(parts)
# print(query_stwig_1_as_labels)
l_parts = split_list(query_stwig_1_as_labels, wanted_parts=2)
print(l_parts)
aux = (None, l_parts[0][0])
del l_parts[0][0]
del l_parts[1][0]
l_parts[0].insert(0, aux)
l_parts[1].insert(0, parts[1][0])
print(l_parts)