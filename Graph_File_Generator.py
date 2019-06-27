import networkx as nx

class Graph_File_Generator(object):
    # Zhaosun Query Graph
    def gen_zhaosun_query_graph(self):
        query_graph = nx.Graph()
        query_graph_edges = [["a1", "b1"], ["a1", "c1"], ["c1", "d1"], ["c1", "f1"], ["f1", "d1"], ["d1", "b1"], ["d1", "e1"], ["e1", "b1"]]
        # query_graph_edges = [["a", "b"], ["a", "c"], ["c", "d"], ["c", "f"], ["f", "d"], ["d", "b"], ["d", "e"], ["e", "b"]]
        query_graph.add_edges_from(query_graph_edges)
        node_attr = ["a", "b", "c", "d", "e", "f"]
        node_attr_dict = dict(zip(sorted(query_graph.nodes()), node_attr))
        nx.set_node_attributes(query_graph, node_attr_dict, 'label')
        return query_graph

    def gen_RI_query_graph(self):
        query_graph = nx.Graph()
        # query_graph_edges = [["0","1773"],["0","1817"],["0","2428"],["0","3719"],["0","4426"],["0","8214"],["0","9148"]]
        query_graph_edges = [["1773","1488"], ["1773","1898"], ["1773", "2285"]]
        query_graph.add_edges_from(query_graph_edges)
        # node_attr = ["29", "25", "19", "6", "29", "13", "15", "20"]
        node_attr = ["25", "28", "29", "27"]
        node_attr_dict = dict(zip(sorted(query_graph.nodes()), node_attr))
        nx.set_node_attributes(query_graph, node_attr_dict, 'label')
        return query_graph
