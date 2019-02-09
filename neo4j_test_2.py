from py2neo import Graph, Node, Relationship
import networkx as nx
import copy
import numpy

class neo4j_test_2(object):

    neograph = Graph(port="7687", user="neo4j", password="graph")

    def Cloud_Load(self, RI_id):  # Pot rula inca o metoda?
        tx = self.neograph.begin()
        cqlQuery = "MATCH (n) WHERE n.RI_id = " + str(RI_id) + " RETURN n"  # Merge cautarea unui nod dupa id.
        result = tx.run(cqlQuery).to_subgraph()
        nodes_loaded = []
        nodes_loaded.append(result)
        cqlQuery2 = "MATCH(n{RI_id: " + str(RI_id) + "})--(m) return m"
        result2 = list(tx.run(cqlQuery2).to_subgraph().nodes)
        nodes_loaded.append(result2)


        # cqlQuery = "match(n:`1`{id:825})--(c) return c"  # ??? https://maxdemarzi.com/2018/10/01/finding-your-neighbors-using-neo4j/
        # Neighbors: MATCH (:`16` { RI_id: 17 })--(`16`)
        #            RETURN `16`.RI_id

        # MATCH(n: `16`)--({RI_id: 17}), asociaza nodul n cu label dat ca si input
        # RETURN n

        # MATCH(n: `1`{RI_id: 9377})-[:PPI]->(m) Return n

        # VARIANTA CORECTA VECINATATE DE ORDINUL 1 AL UNUI NOD: MATCH(n{RI_id: 1})--(m) return m
        return nodes_loaded

    def Index_getID(self, label):
        tx = self.neograph.begin()
        cqlQuery = "MATCH (n:`" + str(label) + "`) RETURN n.RI_id"
        result = tx.run(cqlQuery).to_ndarray()
        nodes_loaded = []
        for r in result:
            nodes_loaded.append(r[0])
        return nodes_loaded




#############################################
with open('Homo_sapiens_udistr_32.gfd') as f:
    lines = f.readlines()
# for line in lines:
#     print(line)
# print(lines[0])
input_graph = nx.Graph()
num_nodes = int(lines[1])
# print(num_nodes)
nodes_attr_list = []
for i in range(2, num_nodes + 2):
    spl = lines[i].split(sep="\n")[0]
    nodes_attr_list.append(spl)
# for attr in nodes_attr_list:
#     print(attr)
num_edges = int(lines[num_nodes + 2])
# print(num_edges)
edge_list = []
for i in range(num_nodes+3, len(lines)):
    line = [lines[i].split(sep="\n")[0], lines[i].split(sep="\n")[1]]
    new_edge = tuple(line[0].split(sep=" "), )
    edge_list.append(new_edge)
# print(edge_list)
# Graf neorientat
graph = nx.Graph()
graph.add_edges_from(edge_list)
# print(graph.edges())
node_attr_dict = dict(zip(graph.nodes(), nodes_attr_list))
nx.set_node_attributes(graph, node_attr_dict, 'label')
# print(list(list(graph.nodes(data=True))[0][1].values()))
# print(list(graph.nodes(data=True))[0][0])
####################################################################

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

test2 = neo4j_test_2()
print(test2.Cloud_Load(1))
print(test2.Index_getID(1))
# MATCH (n) RETURN n LIMIT 25