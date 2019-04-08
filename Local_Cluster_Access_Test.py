from py2neo import Graph, Node, Relationship

class Local_Cluster_Access_Test(object):
    neograph_data = Graph("bolt://127.0.0.1:7693", auth=("neo4j", "changeme"))  # Data Graph Zhaosun
    tx = neograph_data.begin()
    cqlQuery = "MATCH (n) WHERE n.name = 'Andy' RETURN n"
    result = tx.run(cqlQuery).to_ndarray()
    print(result)