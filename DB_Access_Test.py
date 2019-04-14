import threading
from py2neo import Graph, Node, Relationship
from timeit import default_timer as timer

class DB_Access_Test(object):
    neograph_data = Graph("bolt://127.0.0.1:7693", auth=("neo4j", "changeme"))
    def parallel_access_to_one_read_replica(self, query):
        tx = self.neograph_data.begin()
        # cqlQuery = "MATCH (n) WHERE n.name = 'Andy' RETURN n"
        # cqlQuery = "MATCH (n) RETURN n"
        cqlQuery = query
        result = tx.run(cqlQuery).to_ndarray()
        print(result)

    def run_test(self):
        start_time = timer()
        thread_list = []
        queries = [["MATCH (n) WHERE n.name = 'Andy' RETURN n"], ["MATCH (n) RETURN n"]]
        for q in queries:
            thread = threading.Thread(target=self.parallel_access_to_one_read_replica, args=q, name="Thread " + str(q[0]))
            thread_list.append(thread)

        for thread in thread_list:
            print()
            print(thread.name)
            thread.start()
            thread.join()
        total_time_sec = timer() - start_time
        total_time_millis = total_time_sec * 1000

        print("\nDB_Access_Test exec time -> sec: " + str(total_time_sec))
        print("\nDB_Access_Test exec time -> millis: " + str(total_time_millis))

    # def get_overview(self):
    #     neograph_overview = Graph()