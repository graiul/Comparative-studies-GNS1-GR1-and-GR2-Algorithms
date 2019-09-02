import networkx as nx

class Query_Graph_Generator(object):
    # Zhaosun Query Graph
    def gen_zhaosun_query_graph(self):
        query_graph = nx.Graph()
        query_graph_edges = [["a1", "b1"], ["a1", "c1"], ["c1", "d1"], ["c1", "f1"], ["f1", "d1"], ["d1", "b1"], ["d1", "e1"], ["e1", "b1"]]
        # query_graph_edges = [["a", "b"], ["a", "c"], ["c", "d"], ["c", "f"], ["f", "d"], ["d", "b"], ["d", "e"], ["e", "b"]]
        query_graph.add_edges_from(query_graph_edges)
        node_attr = ["a", "b", "c", "d", "e", "f"]
        node_attr_dict = dict(zip(sorted(query_graph.nodes()), node_attr)) # ATENTIE: daca se incurca asocierea dintre id-urile nodurilor cu label-urile corespunzatoare, trebuie scoasa sortarea crescatoare al id-urilor nodurilor. Aici lucram cu string-uri pentru id-urile nodurilor. Label-urile vor fi tot timpul de tipul str.
        nx.set_node_attributes(query_graph, node_attr_dict, 'label')
        return query_graph

    def gen_RI_query_graph(self):
        query_graph = nx.Graph()

        # query_graph_edges = [[1773, 1488], [1773, 1898], [1773, 2285], [1488, 7465], [1898,1347], [1898,5596]]
        # node_attr = ["25", "28", "29", "27", "18", "31", "9"]

        # query_graph_edges = [[0,1773],[0,1817],[0,2428],[0,3719],[0,4426],[0,8214],[0,9148]]
        # node_attr = ["29", "25", "19", "6", "29", "13", "15", "20"]

        # OK - STWIG SI VF2 dau la fel - data graf RI cu 10000 muchii
        query_graph_edges = [[0,1773],[0,1817],[0,2428],[0,3719]]
        node_attr = ["29", "25", "19", "6", "29"] # - Avem doua noduri care au acelasi label, nodurile 0 si 3719 au label-ul 29.

        # OK - STWIG SI VF2 dau la fel - data graf RI cu 10000 muchii
        # query_graph_edges = [[0, 1773], [0, 1817], [0, 2428],[0,4426]]
        # node_attr = ["29", "25", "19", "6", "13"] # - Label-urile sunt diferite!

        # OK - STWIG SI VF2 dau la fel - data graf RI cu 10000 muchii
        # query_graph_edges = [[0,1773],[0,1817],[0,2428]]
        # node_attr = ["29", "25", "19", "6"]

        # OK - STWIG SI VF2 dau la fel - data graf RI cu 10000 muchii
        # query_graph_edges = [[1898,1347], [1898,5596]]
        # node_attr = ["29", "31", "9"]


        # OK - STWIG SI VF2 dau la fel - data graf RI cu 10000 muchii
        # query_graph_edges = [[1773, 1488], [1773, 1898], [1773, 2285]]
        # node_attr = ["25", "28", "29", "27"]

        # OK - STWIG SI VF2 dau la fel - data graf RI cu 10000 muchii
        # query_graph_edges = [[1488, 7465]]
        # node_attr = ["28", "18"]

        query_graph.add_edges_from(query_graph_edges)

        node_attr_dict = dict(zip(query_graph.nodes(), node_attr)) # Am scos sortarea crescatoare al id-urilor nodurilor. Astfel se face corect asocierea intre noduri si label-uri.
        nx.set_node_attributes(query_graph, node_attr_dict, 'label')
        return query_graph

    def gen_small_graph_query_graph(self):
        small_graph = nx.Graph()
        small_graph_nodes = [1, 2, 3, 4]
        # Sortarea ascendenta la string este diferita de cea a de la tipul int
        small_graph_nodes.sort()
        small_graph_edges = [[1, 2], [1, 3], [1, 4]]
        small_graph.add_nodes_from(small_graph_nodes)
        small_graph.add_edges_from(small_graph_edges)
        node_attr = ["a", "b", "c", "d"]
        node_attr_dict = dict(zip(sorted(small_graph.nodes()), node_attr)) # ATENTIE: daca se incurca asocierea dintre id-urile nodurilor cu label-urile corespunzatoare, trebuie scoasa sortarea crescatoare al id-urilor nodurilor. Aici lucram cu string-uri pentru id-urile nodurilor. Label-urile vor fi tot timpul de tipul str.
                                                                            # Aici este o exceptie, ordinea crescatoare al nodurilor pastreaza ordinea originala a nodurilor. Ele coincid in acest caz.

        # print(node_attr_dict.items())
        nx.set_node_attributes(small_graph, node_attr_dict, 'label')
        # print(small_graph.nodes(data=True))
        # print(small_graph.edges())
        return small_graph
