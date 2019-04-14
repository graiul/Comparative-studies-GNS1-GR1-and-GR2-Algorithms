from py2neo import Graph, Node, Relationship

class Dataset_Operator(object):
    dataset_nodes_url = None
    dataset_edges_url = None
    leader_core_bolt_address = None
    username = None
    passwd = None
    def __init__(self, dataset_nodes_url, dataset_edges_url, leader_core_bolt_address, username, passwd):
        self.dataset_nodes_url = dataset_nodes_url
        self.dataset_edges_url = dataset_edges_url
        self.leader_core_bolt_address = leader_core_bolt_address
        self.username = username
        self.passwd = passwd

    def insert_nodes(self):
        neograph_data = Graph(self.leader_core_bolt_address, auth=(self.username, self.passwd))
        # tx = neograph_data.begin() # LA VARIANTA CU NEO4J CA SI C NU MERGE, NEO4j VER 3.3.1
        cqlQuery = "LOAD CSV WITH HEADERS FROM '" + str(self.dataset_nodes_url) + "' AS line" \
                   " CREATE (:Node {  zhaosun_id: line.zhaosun_id, zhaosun_label: line.zhaosun_label})"
        # tx.run(cqlQuery)
        neograph_data.run(cqlQuery)

    def insert_edges(self):
        neograph_data = Graph(self.leader_core_bolt_address, auth=(self.username, self.passwd))
        # tx = neograph_data.begin()
        cqlQuery = "LOAD CSV WITH HEADERS FROM '" + str(self.dataset_edges_url) + "' AS line" \
                   " MERGE (n:Node {zhaosun_id: line.zhaosun_from})" \
                   " MERGE (m:Node {zhaosun_id: line.zhaosun_to})" \
                   " MERGE (n)-[:PPI]-(m)"
        # tx.run(cqlQuery)
        neograph_data.run(cqlQuery)

    def delete_data_from_db(self):
        neograph_data = Graph(self.leader_core_bolt_address, auth=(self.username, self.passwd))
        # tx = neograph_data.begin()
        cqlQuery = "MATCH (n) DETACH DELETE n"
        # tx.run(cqlQuery)
        neograph_data.run(cqlQuery)