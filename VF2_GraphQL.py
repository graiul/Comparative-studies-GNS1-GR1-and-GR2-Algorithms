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
