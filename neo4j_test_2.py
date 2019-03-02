import threading
from concurrent.futures.thread import ThreadPoolExecutor
from multiprocessing.dummy import Pool as ThreadPool

from py2neo import Graph, Node, Relationship
import networkx as nx
import copy
import numpy
import itertools

class neo4j_test_2(object):

    neograph = Graph(port="7687", user="neo4j", password="graph")
    # neograph = Graph(port="11004", user="neo4j", password="graph")


    def Cloud_Load(self, RI_id):  # Pot rula inca o metoda?
        # print("Cloud_Load:")
        tx = self.neograph.begin()
        # cqlQuery = "MATCH (n) WHERE n.RI_id = " + str(RI_id) + " RETURN n"  # Merge cautarea unui nod dupa id.
        cqlQuery = "MATCH (n) WHERE n.id = " + str(RI_id) + " RETURN n"  # Merge cautarea unui nod dupa id.
        # print(cqlQuery)
        # Pentru Zhaosun:
        biglist = []
        # print("     id=" + str(RI_id))
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
        # print(cqlQuery)
        result = tx.run(cqlQuery).to_ndarray()
        # print("Index_hasLabel query result= ")
        # print(list(result))
        if len(list(result)) > 0:
            return True
        else:
            return False

    def MatchSTwig(self, q): # q 1 = (a,{b,c})
        print("STwig query: " + str(q))
        r = str(q[0]) # Root node label
        L = [q[1][0], q[1][1]] # Root children labels
        print("Root node label: " + str(r))
        print("Root children labels: " + str(L))

        #  (1) Find the set of root nodes by calling Index.getID(r);
        Sr = self.Index_getID(r)
        print("Set of root nodes for label " + str(r) + ": " + str(Sr))
        R = []
        Sli = []

        # (2) Foreach root node, find its child nodes using Cloud.Load();
        for root_node in Sr:
            print("---Root node: " + str(root_node))
            c = self.Cloud_Load(root_node)
            print("     Children for selected root, first elem is selected root: " + str(c))
            # print("End Cloud_Load\n")
            # root = c[0][0]
            children = c[0][1]
            # print("root=" + str(root))
            # print("children=" + str(children))

            # (3) Find its child nodes that match the labels in L by calling Index.hasLabel()
            S = []
            S_child_lists = []
            for root_child_label in L:
                print("     Root_child_label: " + str(root_child_label))
                # print("     " + str(type(root_child_label)))
                for child in children:
                    if child not in S_child_lists:
                        # print("     child= " + str(child)) # Child, sau vecinii de ordinul 1.
                        aux = str(child).split("id: '")[1]
                        child_id = str(aux).split("'}")[0]
                        print("     child_id= " + str(child_id))
                        # aux2 = str(child).split(" {")[0]
                        # child_label = str(aux2.split(":")[1])
                        # print("     child_label= " + child_label)
                        has_label = self.Index_hasLabel(child_id, root_child_label)
                        # print(has_label)
                        if has_label:
                            # S[S.index(li)] = child
                            S_child_lists.append(child_id)
                # print("S[li]= " + str(S[S.index(li)]))
                print("     S_child_lists= " + str(S_child_lists))
                S.append(S_child_lists) # Sli, lista de children, pentru fiecare li care respecta conditia, adaugam in S
                S_child_lists = []
            print("     Sets of children(for selected root " + str(root_node) + ") with labels  " + str(L) + ": ")
            S_one_elems = []
            for s in S:
                print("     " + str(s))
                for s_temp in s:
                    S_one_elems.append(s_temp)
            S_one_elems.insert(0, root_node)
            # print("Cartesian product: ")
            combinations = list(itertools.combinations(S_one_elems, 3))
            elem_labels = []
            elem_labels_total = []
            for elem in combinations:
                for el in elem:
                    elem_labels.append(el[0])
                elem_labels_total.append(elem_labels)
                elem_labels = []
            combinations_dict = dict(zip(combinations, elem_labels_total))
            combinations_dict_final = copy.deepcopy(combinations_dict)
            # vals = list(combinations_dict.values())[0]
            for val in combinations_dict.items():
                # print(val[1])
                for lb in val[1]:
                    # print(lb)
                    if val[1].count(lb) > 1:
                        # print("More than once ^")
                        combinations_dict_final.pop(val[0])
                        break
            for stwig in combinations_dict_final.keys():
                # print(stwig)
                R.append(stwig)
        print("STWIGS: ")
        for stwig in sorted(R):
            print(stwig)
        # Am schimbat graful astfel: am inlaturat muchia a3,b3: MATCH (n:a)-[r:RELTYPE]-(m:b) WHERE n.id = 'a3' AND m.id = 'b3' DELETE r
        #                            am adaugat muchia a3,c3: # MATCH (n:a),(m:c) WHERE n.id = 'a3' AND m.id = 'c3' CREATE (n)-[r:RELTYPE]->(m)
        # Astfel am obtinur rezultatele din p788_Zhaosun, pag 5, G(q1) = ...


    def Query_Graph_Split(self, query_graph):

        splits = []
        for node in query_graph.nodes():
            print("Selected node: " + str(node))
            edges = list(query_graph.edges(node))
            # if len(edges) == 2:
            #     splits.append([node, edges])
            print(edges)
            for stop in range(2, len(edges)+1):
                splits.append([node, edges[0:stop]])
        print()
        # return splits
        print(splits)

    def Query_Graph_Split_Parallel(self, nodes_chunk):

        splits = []
        for node in nodes_chunk:
            print("Selected node: " + str(node))
            edges = list(query_graph.edges(node))
            # if len(edges) == 2:
            #     splits.append([node, edges])
            print(edges)
            for stop in range(2, len(edges)+1):
                splits.append([node, edges[0:stop]])
        print("Splits: ")
        print(splits)



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
# print(test2.Cloud_Load(1)) # VECINATATE DE GRADUL 1, toate nodurile indeg/outdeg?
# print(test2.Index_getID(1))
# print(test2.Index_hasLabel(1, 3322))

# q = ['a', ['b','c']]
# test2.MatchSTwig(q)

query_graph = nx.Graph()
query_graph_edges = [["a1", "b1"], ["a1", "c1"], ["c1", "d1"], ["d1", "f1"], ["f1", "e1"], ["e1", "b1"], ["b1", "d1"], ["b1", "f1"]]
query_graph.add_edges_from(query_graph_edges)
node_attr = ["a", "b", "c", "d", "e", "f"]
node_attr_dict = dict(zip(sorted(query_graph.nodes()), node_attr))
nx.set_node_attributes(query_graph, node_attr_dict, 'label')
# print(query_graph.nodes(data=True))

# for split in test2.Query_Graph_Split(query_graph):
#     print(split)

# test2.Query_Graph_Split(query_graph)

query_graph_nodes = list(query_graph.nodes())
print(query_graph_nodes)
start = 0
nodes_chunk = 2
chunks = []
# for node in query_graph_nodes:
while start<len(query_graph_nodes):
    chunks.append(query_graph_nodes[start:nodes_chunk])
    start = start + 2
    nodes_chunk = nodes_chunk + 2
print(chunks)
threads = []
for i in range(len(chunks)):
    thread = threading.Thread(target=test2.Query_Graph_Split_Parallel, args=[chunks[i]], name="Thread " + str(i))
    threads.append(thread)

for thread in threads:
    print()
    print(thread.name)
    thread.start()
    thread.join()



# th1 = threading.Thread(target=test2.Query_Graph_Split_Parallel, args=[query_graph_nodes, 0, len(query_graph.edges())], name="Thread 1")
# print(th1.name)
# th1.start()
