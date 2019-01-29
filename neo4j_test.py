from neo4j.v1 import GraphDatabase
import networkx as nx

class neo4j_test(object):
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()

    def print_greeting(self, message):
        with self._driver.session() as session:
            greeting = session.write_transaction(self._create_and_return_greeting, message)
            print(greeting)

    @staticmethod
    def _create_and_return_greeting(tx, message):
        result = tx.run("CREATE (a:Greeting) "
                        "SET a.message = $message "
                        "RETURN a.message + ', from node ' + id(a)", message=message)
        return result.single()[0]

    def insert_graph_in_db(self, graph):
        with self._driver.session() as session:
            session.write_transaction(self.create_neo4j_graph_node, graph)

    @staticmethod
    def create_neo4j_graph_node(tx, graph):
        for node in list(graph.nodes(data=True)):
            # tx.run("CREATE (a:Node {id: $id, label: $label})", id=node[0], label=list(list(node[1].values())))
            # print(str(list(list(node[1].values()))[0]))
            cqlQuery = "CREATE (a:`" + str(list(list(node[1].values()))[0]) + "` {id: " + str(node[0]) + "})"
            tx.run(cqlQuery)

    @staticmethod
    def create_neo4j_graph_edges(tx, graph):
        for edge in graph.edges():
            cqlQuery = "MATCH(a:`" + str(graph.node[edge[0]]['label']) + "`), (b:`" + str(graph.node[edge[1]]['label']) + "`) WHERE a.id=" + str(edge[0]) + " AND b." + str(edge[1]) + " CREATE(a)-[:PPI]->(b)"
            print(cqlQuery)
            tx.run(cqlQuery)
            # MATCH(a:`29`), (b:`25`) WHERE a.id=0 AND b.id=1773 CREATE(a)-[:PPI]->(b)