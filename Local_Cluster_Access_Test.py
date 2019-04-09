import threading

from py2neo import Graph, Node, Relationship

class Local_Cluster_Access_Test(object):
    neograph_data = Graph("bolt://127.0.0.1:7693", auth=("neo4j", "changeme"))
    def parallel_access_to_one_read_replica(self, query):
        tx = self.neograph_data.begin()
        # cqlQuery = "MATCH (n) WHERE n.name = 'Andy' RETURN n"
        # cqlQuery = "MATCH (n) RETURN n"
        cqlQuery = query
        result = tx.run(cqlQuery).to_ndarray()
        print(result)

test = Local_Cluster_Access_Test()
thread_list = []
queries = [["MATCH (n) WHERE n.name = 'Andy' RETURN n"], ["MATCH (n) RETURN n"]]
for q in queries:
    thread = threading.Thread(target=test.parallel_access_to_one_read_replica, args=q, name="Thread " + str(q[0]))
    thread_list.append(thread)

for thread in thread_list:
    print()
    print(thread.name)
    thread.start()
    thread.join()