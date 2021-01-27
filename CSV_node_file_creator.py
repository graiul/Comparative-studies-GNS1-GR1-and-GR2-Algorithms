# def create_RI_data_graph_nodes_csv_file(self, nx_RI_data_graph):
import networkx as nx
from Toolbox_Gheorghica_Radu_Iulian import Toolbox_Gheorghica_Radu_Iulian as tgri

with open('DATASET RI Caenorhabditis elegans PPI/Caenorhabditis_elegans_PPI_udistr_32_edges_for_CSV.txt') as f:
    lines = f.readlines()
f = open('DATASET RI Caenorhabditis elegans PPI/Caenorhabditis_elegans_PPI_udistr_32_nodes.csv', "w+")
lines_as_int_id_pairs = []
for line in lines:
    new_line = line.split(" ")
    # realpython.com/convert-python-string-to-int/
    new_line_int_ids = [int(new_line[0]), int(new_line[1].split("\n")[0])]
    lines_as_int_id_pairs.append(new_line_int_ids)
    # print(new_line_int_ids)
# exit(0)
nx_RI_data_graph = nx.DiGraph()
# print(lines[1])
nx_RI_data_graph.add_edges_from(lines_as_int_id_pairs)
f.write("node_label,node_id\n")
node_list = list(nx_RI_data_graph.nodes())
with open('DATASET RI Caenorhabditis elegans PPI/Caenorhabditis_elegans_PPI_udistr_32_node_labels_for_CSV.txt') as g:
    label_list = g.readlines()
    for i in range(len(label_list) - 1):
        label_and_id_line = [label_list[i].split("\n")[0], node_list[i]]
        f.write(label_and_id_line[0] + "," + str(label_and_id_line[1]) + "\n")
# node_list_without_last_element = node_list[:-1]
# print(node_list[1][0])
# print(str(node_list[0][1]).split(": ")[1])
# for node in node_list_without_last_element:
#     RI_node_label_aux = str(node[1]).split(": '")[1]
#     RI_node_label = RI_node_label_aux.split("'}")[0]
#     f.write(RI_node_label + "," + str(node[0]) + "\n")
#
# last_node = node_list[len(node_list) - 1]
# RI_node_label_aux = str(last_node[1]).split(": '")[1]
# RI_node_label = RI_node_label_aux.split("'}")[0]
# f.write(RI_node_label + "," + str(last_node[0]))