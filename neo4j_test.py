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

    def init_session(self, label):
        with self._driver.session() as session:
            session.write_transaction(self.Index_getID, str(label))

    @staticmethod
    def create_neo4j_graph_node(tx, graph):
        # for node in list(graph.nodes(data=True)):
            # tx.run("CREATE (a:Node {id: $id, label: $label})", id=node[0], label=list(list(node[1].values())))
            # print(str(list(list(node[1].values()))[0]))
            # cqlQuery = "CREATE (a:`" + str(list(list(node[1].values()))[0]) + "` {id: " + str(node[0]) + "})"
            # tx.run(cqlQuery)

        for edge in graph.edges():
            cqlQuery = "MATCH(a:`" + str(graph.node[edge[0]]['label']) + "`), (b:`" + str(graph.node[edge[1]]['label']) \
                       + "`) WHERE a.id=" + str(edge[0]) + " AND b.id=" + str(edge[1]) + " CREATE(a)-[:PPI]->(b)" # Se blocheaza la inserarea unui arc anume: MATCH(a:`32`), (b:`15`) WHERE a.id=12036 AND b.id=12174 CREATE(a)-[:PPI]->(b)
            # print(cqlQuery)
            try:
                tx.run(cqlQuery)
                print("Inserare arc cu succes!")
                print(cqlQuery)
            except:
                print("Nu a fost inserat arcul!")

    @staticmethod
    def Cloud_Load(tx, id): # Pot rula inca o metoda?
        cqlQuery = "MATCH (n) WHERE n.id = " + str(id) + " RETURN n" # Merge cautarea unui nod dupa id.
        result = tx.run(cqlQuery)
        nodes_loaded = []
        nodes_loaded.append(result)
        cqlQuery = "match(n:`1`{id:825})--(c) return c" # ??? https://maxdemarzi.com/2018/10/01/finding-your-neighbors-using-neo4j/
        return result

    @staticmethod
    def Index_getID(tx, label):
        l = str(label)
        cqlQuery = "MATCH (n:`" + l + "`) RETURN n.id"
        result = tx.run(cqlQuery)
        return result
