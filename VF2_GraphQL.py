import copy
from collections import OrderedDict

import networkx as nx
from networkx.algorithms import isomorphism
from py2neo import Graph, Subgraph

from GenericQueryProc import GenericQueryProc
from Query_Graph_Generator import Query_Graph_Generator
from Graph_Format import Graph_Format
from timeit import default_timer as timer

# https://stackoverflow.com/questions/6537487/changing-shell-text-color-windows
# https://pypi.org/project/colorama/
from colorama import init
from colorama import Fore, Back, Style
init()

class VF2Algorithm_GraphQL():

    queryGraphFile = None
    dataGraphFile = None
    queryGraph = None
    dataGraph = None

    start_time = None
    total_time = None

    respectare_conditie_1 = False
    respectare_conditie_2 = False
    respectare_conditie_3 = False

    respectare_conditie_graphql_1 = False
    respectare_conditie_graphql_2 = False

    results_dict = OrderedDict()

    M_list = []

    def __init__(self, M):
        self.start_time = timer()
        query_graph_gen = Query_Graph_Generator()
        self.queryGraph = query_graph_gen.gen_RI_query_graph()
        nx.set_node_attributes(self.queryGraph, False, 'matched')
        neograph_data = Graph("bolt://127.0.0.1:7687", auth=("neo4j", "password")) # Data Graph RI - O singura instanta de Neo4J

        cqlQuery = "MATCH p=(n)-[r:PPI]->(m) return n.node_id, m.node_id"
        result = neograph_data.run(cqlQuery).to_ndarray()
        edge_list = result.tolist()
        edge_list_integer_ids = []
        for string_edge in edge_list:
            edge_list_integer_ids.append([int(i) for i in string_edge])
        self.dataGraph = nx.Graph()
        self.dataGraph.add_edges_from(sorted(edge_list_integer_ids))
        cqlQuery2 = "MATCH (n) return n.node_id, n.node_label"
        result2 = neograph_data.run(cqlQuery2).to_ndarray()
        node_ids_as_integers_with_string_labels = []
        for node in result2:
            # print(node[0])
            node_ids_as_integers_with_string_labels.append([int(node[0]), node[1]])
        node_attr_dict = OrderedDict(sorted(node_ids_as_integers_with_string_labels))
        nx.set_node_attributes(self.dataGraph, node_attr_dict, 'label')
        nx.set_node_attributes(self.dataGraph, False, 'matched')
        if len(M) > 0:
            self.queryGraph.nodes[M[0][0]]['matched'] = True
            self.dataGraph.nodes[M[0][1]]['matched'] = True

    # Regula GraphQL nr 1: neighborhood signature based pruning, p133-han.pdf, pagina 6.
    def sig_GraphQL_query_graph(self, vertex):
        vertex_neighbors = list(self.queryGraph.neighbors(vertex))
        # print(vertex_neighbors)
        signature = []
        for vertex_neighbor in vertex_neighbors:
            label = self.queryGraph.nodes[vertex_neighbor]['label']
            # print(label)
            # print(type(label))
            signature.append(label)
        return signature

    def sig_GraphQL_data_graph(self, node_id):
        signature2 = []
        neograph_data = Graph("bolt://127.0.0.1:7687",
                              auth=("neo4j", "password"))  # Data Graph RI - O singura instanta de Neo4J
        cqlQuery2 = "MATCH(n{node_id: '" + str(node_id) + "'})--(m) return m"
        result2 = list(neograph_data.run(cqlQuery2).to_ndarray())

        for neighbor in result2:
            # print(neighbor)

            aux = str(neighbor).split("id: '")[1]
            neighbor_id = int(str(aux).split("',")[0])

            aux2 = str(neighbor).split("node_label: ")[1]
            # print(aux2)
            neighbor_label = str(aux2).split("})]")[0]
            # print(type(neighbor_label))

            # print(neighbor_id)
            # print(neighbor_label)
            signature2.append(neighbor_label)
        return signature2

    # networkx.github.io/documentation/networkx-1.10/reference/generated/networkx.algorithms.traversal.breadth_first_search.bfs_tree.html
    def breadth_first_search_tree_for_query_graph_node(self, node_id, depth_r):
        return list(nx.bfs_tree(self.queryGraph, node_id, depth_r))

    # networkx.github.io/documentation/networkx-1.10/reference/generated/networkx.algorithms.traversal.breadth_first_search.bfs_tree.html
    def breadth_first_search_tree_for_data_graph_node(self, node_id, depth_r):
        return list(nx.bfs_tree(self.dataGraph, node_id, depth_limit=depth_r))



M = []
vf2grql = VF2Algorithm_GraphQL(M)

# print(vf2grql.sig_GraphQL_query_graph(3842))
# print(vf2grql.sig_GraphQL_data_graph(11000))
print(vf2grql.breadth_first_search_tree_for_query_graph_node(3842, 0))
print(vf2grql.breadth_first_search_tree_for_data_graph_node(11000, 0))
