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

        # query_graph_edges = [[1773, 1488]]
        # node_attr = ["25", "28"]

        # query_graph_edges = [[1773, 1488], [1773, 1898]]
        # node_attr = ["25", "28", "29"]

        # query_graph_edges = [[2462,4829], [2462,5730]]
        # node_attr = ["18", "5", "7"]

        # query_graph_edges = [[1773, 1488], [1773, 1898], [1773, 2285]]
        # node_attr = ["25", "28", "29", "27"]

        # query_graph_edges = [[1488, 7465]]
        # node_attr = ["28", "18"]

        # query_graph_edges = [[1898,1347], [1898,5596]]
        # node_attr = ["29", "31", "9"]

        # query_graph_edges = [[0,1773],[0,1817]]
        # node_attr = ["29", "25", "19"]

        # query_graph_edges = [[0, 1773], [0, 1817],[0,4426]]
        # node_attr = ["29", "25", "19", "13"]

        # query_graph_edges = [[7190,137], [7190,419], [7190,450]]
        # node_attr = ["3", "2", "11", "3"]

        # query_graph_edges = [[1773, 1488], [1773, 1898], [1773, 2285]]
        # node_attr = ["25", "28", "29", "27"]

        # query_graph_edges = [[1488, 7465]]
        # node_attr = ["28", "18"]

        # A doua serie de grafuri query pentru testare - fiecare este cate un STwig.

        # Grafuri query cu 3 noduri:

        # query_graph_edges = [[7711, 2243], [7711, 2259]]
        # node_attr = ["16", "2", "17"]

        # query_graph_edges = [[2670, 10109], [2670, 10387]]
        # node_attr = ["29", "30", "20"]

        # query_graph_edges = [[4164, 3526], [4164, 5687]]
        # node_attr = ["10", "26", "2"]

        # query_graph_edges = [[5636, 2904], [5636, 3414]]
        # node_attr = ["16", "6", "30"]

        # query_graph_edges = [[10553, 7888], [10553, 8186]]
        # node_attr = ["3", "27", "27"]


        # Grafuri query cu 6 noduri:

        # query_graph_edges = [[11041, 2467], [11041, 2607], [11041, 2650], [11041, 2904], [11041, 3414]]
        # node_attr = ["18", "23", "11", "9", "6", "30"]

        # query_graph_edges = [[7563, 5755], [7563, 6256], [7563, 6784], [7563, 7289], [7563, 7308]]
        # node_attr = ["18", "23", "3", "15", "26", "2"]

        # query_graph_edges = [[6880, 5687], [6880, 6392], [6880, 9094], [6880, 12206], [6880, 11000]]
        # node_attr = [["9", "2", "23", "10", "22", "24"]]

        # query_graph_edges = [[7190, 2900], [7190, 3255], [7190, 3258], [7190, 3411], [7190, 3586]]
        # node_attr = ["3", "5", "24", "11", "5", "14"]

        # query_graph_edges = [[12472, 10543], [12472, 10688], [12472, 10752], [12472, 10808], [12472, 10978]]
        # node_attr = ["8", "8", "5", "25", "15", "14"]


        # Grafuri query cu 9 noduri:

        # query_graph_edges = [[531,5399], [531,5671], [531,6393], [531,6702], [531,7289], [531,7421], [531,7438], [531,8066]]
        # node_attr = ["20", "32", "20", "22", "31", "26", "9", "16", "18"]

        # query_graph_edges = [[831,4915], [831,4924], [831,4976], [831,5144], [831,5157], [831,5164], [831,5272], [831,5399]]
        # node_attr = ["17", "24", "22", "14", "12", "32", "25", "2", "32"]

        # query_graph_edges = [[5414,1300], [5414,1341], [5414,1349], [5414,1365], [5414,1466], [5414,1519], [5414,1546], [5414,1547]]
        # node_attr = ["14", "3", "30", "20", "25", "8", "7", "24", "7"]

        # query_graph_edges = [[7020,2430], [7020,2473], [7020,2508], [7020,2540], [7020,2560], [7020,2573], [7020,2724], [7020,2771]]
        # node_attr = ["21", "9", "18", "24", "16", "26", "21", "6", "21"]

        query_graph_edges = [[11000,8269], [11000,8429], [11000,8507], [11000,9430], [11000,10327], [11000,10426], [11000,11319], [11000,11783]]
        node_attr = ["24", "19", "32", "25", "32", "24", "26", "11", "12"]


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
