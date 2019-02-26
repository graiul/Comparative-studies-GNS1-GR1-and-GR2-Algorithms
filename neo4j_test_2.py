from py2neo import Graph, Node, Relationship
import networkx as nx
import copy
import numpy
import itertools

class neo4j_test_2(object):

    neograph = Graph(port="7687", user="neo4j", password="graph")
    # neograph = Graph(port="11004", user="neo4j", password="graph")


    def Cloud_Load(self, RI_id):  # Pot rula inca o metoda?
        print("Cloud_Load:")
        tx = self.neograph.begin()
        # cqlQuery = "MATCH (n) WHERE n.RI_id = " + str(RI_id) + " RETURN n"  # Merge cautarea unui nod dupa id.
        cqlQuery = "MATCH (n) WHERE n.id = " + str(RI_id) + " RETURN n"  # Merge cautarea unui nod dupa id.
        # print(cqlQuery)
        # Pentru Zhaosun:
        biglist = []
        print("id=" + str(RI_id))
        cqlQuery = "MATCH (n) WHERE n.id = '" + str(RI_id) + "' RETURN n"
        # print(cqlQuery)
        result = tx.run(cqlQuery).to_ndarray()
        nodes_loaded = []
        nodes_loaded.append(result)
        # cqlQuery2 = "MATCH(n{RI_id: " + str(RI_id) + "})--(m) return m"
        cqlQuery2 = "MATCH(n{id: '" + str(RI_id) + "'})--(m) return m"
        # print(cqlQuery2)

        # result2 = list(tx.run(cqlQuery2).to_subgraph().nodes)
        result2 = list(tx.run(cqlQuery2).to_ndarray())
        # print(result2) # Nu imi afiseaza vecinii.

        nodes_loaded.append(result2)
        biglist.append(nodes_loaded)

        # VARIANTA CORECTA VECINATATE DE ORDINUL 1 AL UNUI NOD: MATCH(n{RI_id: 1})--(m) return m
        # print("Vecinatate, primul elem root=")
        # for b in biglist:
        #     for bb in b:
        #         print(bb)
        #     print("---")
        return biglist

    def Index_getID(self, label):
        tx = self.neograph.begin()
        # cqlQuery = "MATCH (n:`" + str(label) + "`) RETURN n.RI_id"
        cqlQuery = "MATCH (n:`" + str(label) + "`) RETURN n.id" # IF a IN a1! Graf Zhaosun

        result = tx.run(cqlQuery).to_ndarray()
        nodes_loaded = []
        for r in result:
            nodes_loaded.append(r[0])
        return nodes_loaded

    # def Index_hasLabel(self, RI_id, label):
    def Index_hasLabel(self, id, label):
        tx = self.neograph.begin()
        # cqlQuery = "MATCH (n:`" + str(label) + "`) WHERE n.RI_id=" + str(RI_id) + " RETURN n"
        cqlQuery = "MATCH (n:`" + str(label) + "`) WHERE n.id='" + str(id) + "' RETURN n"

        print(cqlQuery)
        result = tx.run(cqlQuery).to_ndarray()
        print("Index_hasLabel query result= ")
        print(list(result))
        if len(list(result)) > 0:
            return True
        else:
            return False

    def MatchSTwig(self, q): # q 1 = (a,{b,c})
        r = str(q[0]) # Root node label
        L1 = str(q[1][0])
        L2 = str(q[1][1])
        L = [L1, L2] # Root children labels
        print("r=" + str(r))
        print("L=" + str(L))
        Sr = self.Index_getID(r) # Aici trebuie obtinut ce trebuie pentru graful Zhaosun.
        print("Sr=" + str(Sr))
        R = []
        Sli = []
        for n in Sr:
            print("---n=" + str(n))
            c = self.Cloud_Load(n)
            print("c=" + str(c))
            # for li in L:
            print("L1, trebuie sa fie 'b'= " + str(L1))
            print("L2, trebuie sa fie 'c'= " + str(L2))

            root = c[0][0]
            children = c[0][1]
            print("root=" + str(root))
            print("children=" + str(children))

            # S = ["0" for i in range(len(L))]
            S = []
            print("S= " + str(S))
            S_formatted_elems = []
            S_child_lists = []

            for li in L:
                print("li= " + str(li))
                print(type(li))
                for m in children:
                    if m not in S_child_lists:
                        print("m= " + str(m)) # Child, sau vecinii de ordinul 1.
                        aux = str(m).split("id: '")[1]
                        child_id = str(aux).split("'}")[0]
                        print("child_id= " + str(child_id))
                        aux2 = str(m).split(" {")[0]
                        child_label = str(aux2.split(":")[1])
                        print("child_label= " + child_label)
                        has_label = self.Index_hasLabel(child_id, child_label)
                        print(has_label)
                        if has_label:
                            # S[S.index(li)] = m
                            S_child_lists.append(child_id)
                # print("S[li]= " + str(S[S.index(li)]))
            print("S_child_lists= " + str(S_child_lists))
            S.append(S_child_lists) # Sli, lista de children, pentru fiecare li care respecta conditia, adaugam in S
            # S_child_lists = []
            print("S= ")
            for s in S:
                print(s)
    #     for elem in itertools.product():
    #         R.append(elem)

# #BIG DATA GRAPH FROM RI DB############################################
# with open('Homo_sapiens_udistr_32.gfd') as f:
#     lines = f.readlines()
# # for line in lines:
# #     print(line)
# # print(lines[0])
# input_graph = nx.Graph()
# num_nodes = int(lines[1])
# # print(num_nodes)
# nodes_attr_list = []
# for i in range(2, num_nodes + 2):
#     spl = lines[i].split(sep="\n")[0]
#     nodes_attr_list.append(spl)
# # for attr in nodes_attr_list:
# #     print(attr)
# num_edges = int(lines[num_nodes + 2])
# # print(num_edges)
# edge_list = []
# for i in range(num_nodes+3, len(lines)):
#     line = [lines[i].split(sep="\n")[0], lines[i].split(sep="\n")[1]]
#     new_edge = tuple(line[0].split(sep=" "), )
#     edge_list.append(new_edge)
# # print(edge_list)
# # Graf neorientat
# graph = nx.Graph()
# graph.add_edges_from(edge_list)
# # print(graph.edges())
# node_attr_dict = dict(zip(graph.nodes(), nodes_attr_list))
# nx.set_node_attributes(graph, node_attr_dict, 'label')
# # print(list(list(graph.nodes(data=True))[0][1].values()))
# # print(list(graph.nodes(data=True))[0][0])

# tx = neograph.begin()
# neonodes = []
# for node in list(graph.nodes(data=True)):
#     cqlQuery = "CREATE (a:`" + str(list(list(node[1].values()))[0]) + "` {RI_id: " + str(node[0]) + "})"
#     neograph.run(cqlQuery)

# edges_without_warning_edge = copy.deepcopy(graph.edges())
# l = list(edges_without_warning_edge)
# l.remove(('12036', '12174'))
# l.remove(('11868', '11915'))
# l.remove(('11680', '11841'))
# l.remove(('11023', '11706'))
#
# for edge in l:
#     cqlQuery = "MATCH(a:`" + str(graph.node[edge[0]]['label']) + "`), (b:`" + str(graph.node[edge[1]]['label']) \
#                + "`) WHERE a.RI_id=" + str(edge[0]) + " AND b.RI_id=" + str(edge[1]) + " CREATE(a)-[:PPI]->(b)"
#     print(cqlQuery)
#     neograph.run(cqlQuery)
#     print(edge)
# #BIG DATA GRAPH FROM RI DB############################################


# SMALL DATA GRAPH FROM ZHAOSUN############################################
# Comenzi Cypher
# CREATE (n:c { id: 'c3' })
# match (n:a) where n.id='a1' return n
# MATCH (n:a),(m:b) WHERE n.id = 'a1' AND m.id = 'b1' CREATE (n)-[r:RELTYPE]->(m)
# Mai ramane de adaugat M2 si M3 din graful de la fig 5
# SMALL DATA GRAPH FROM ZHAOSUN############################################

test2 = neo4j_test_2()
# print(test2.Cloud_Load(1)) # VECINTTATE DE GRADUL 1, toate nodurile indeg/outdeg?
# print(test2.Index_getID(1))
# print(test2.Index_hasLabel(1, 3322))
# MATCH (n) RETURN n LIMIT 25
q = ['a', ['b','c']]
test2.MatchSTwig(q)