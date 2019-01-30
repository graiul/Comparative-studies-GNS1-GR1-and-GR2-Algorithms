from neo4j_test import neo4j_test
import networkx as nx

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
print(graph.edges())
node_attr_dict = dict(zip(graph.nodes(), nodes_attr_list))
nx.set_node_attributes(graph, node_attr_dict, 'label')
print(list(list(graph.nodes(data=True))[0][1].values()))
print(list(graph.nodes(data=True))[0][0])
# for node in graph.nodes(data=True):
#     print(node)
# for edge in graph.edges:
#     print(edge)
test = neo4j_test("bolt://localhost:7687", "neo4j", "graph")
test.insert_graph_in_db(graph)
# test.create_neo4j_graph_edges(graph)

# Sterge tot:
# Cypher: MATCH (n) DETACH DELETE n
# Afiseaza tot
# MATCH (n) RETURN (n)
# Insereaza un arc:
# MATCH(a:`29`), (b:`25`) WHERE a.id=0 AND b.id=1773 CREATE(a)-[:PPI]->(b)
# Sterge toate arcele:
# MATCH ()-[r:PPI]-() DELETE r

# Incercare de returnare noduri adiacente unui nod dat - pt Cloud.Load din p788.zhaosun.
# call apoc.neighbors.tohop(call apoc.node.id(1431), 'PPI', 1)
# call apoc.nodes.get(1431), neo4j id...

# Pot rula inca o metoda in care am acces prin tranzactia tx.run la baza de date? Nu puteam crea o metoda noua care sa poata rula, spunand ca are un parametru lipsa, dar cealalta functiona...
# La un moment dat nu mai adauga arce in timpul rularii
# Incerc sa returnez nodurile adiacente, dar deocamdata pot returna doar un nod cautand id-ul RI - Cloud.Load din p788.zhaosun. A nu se face confuzie intre id-uri ale nodurilor grafului RI si id-urile date nodurilor de catre Neo4j la inserare.
#   Aici am incercat si cu biblioteca APOC - call apoc.neighbors.tohop()