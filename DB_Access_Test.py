import sys
import threading
from multiprocessing import Process
from py2neo import Graph, Node, Relationship
from timeit import default_timer as timer

class DB_Access_Test(object):
    neograph_data = Graph("bolt://127.0.0.1:7690", auth=("neo4j", "changeme"))

    def single_thread_access_to_one_read_replica(self):
        start_time = timer()
        tx = self.neograph_data.begin()
        # cqlQuery = "MATCH (n) WHERE n.name = 'Andy' RETURN n"
        cqlQuery = "MATCH (n) RETURN n"
        print(cqlQuery)
        # cqlQuery = query
        result = tx.run(cqlQuery).to_ndarray()
        print(result)
        total_time_sec = timer() - start_time
        total_time_millis = total_time_sec * 1000

        # print("\nDB_Access_Test single thread exec time -> sec: " + str(total_time_sec))
        # print("\nDB_Access_Test single thread exec time -> millis: " + str(total_time_millis))
        print()
        print('\x1b[0;30;45m' + 'DB_Access_Test single thread exec time: ' + str(total_time_millis) + ' ms' + '\x1b[0m')

    def multiple_thread_access_to_one_read_replica(self, query):
        tx = self.neograph_data.begin()
        # cqlQuery = "MATCH (n) WHERE n.name = 'Andy' RETURN n"
        # cqlQuery = "MATCH (n) RETURN n"
        cqlQuery = query
        result = tx.run(cqlQuery).to_ndarray()
        print(result)

    def run_test_multiple_threads(self):
        print("Three queries, three threads: time test")
        start_time = timer()
        thread_list = []
        queries = [["MATCH (n) RETURN n"], ["MATCH (n) RETURN n"], ["MATCH (n) RETURN n"]]
        # print(enumerate(queries))
        # for q in queries:
        for i in [i for i in enumerate(queries)]:
            print(i)
            pos = i[0]
            query = i[1]
            thread = threading.Thread(target=self.multiple_thread_access_to_one_read_replica, args=query, name="Thread "  + str(pos)  + " - Executed query: " + str(query))
            thread_list.append(thread)

        for thread in thread_list:
            print()
            print(thread.name)
            thread.start()
            thread.join()
        total_time_sec = timer() - start_time
        total_time_millis = total_time_sec * 1000

        # print("\nDB_Access_Test threaded exec time -> sec: " + str(total_time_sec))
        # print("\nDB_Access_Test threaded exec time -> millis: " + str(total_time_millis))
        print()
        print('\x1b[0;30;45m' + 'DB_Access_Test multiple threads exec time: ' + str(total_time_millis) + ' ms' + '\x1b[0m')

    def multiple_processes_access_to_one_read_replica(self, query):
        tx = self.neograph_data.begin()
        # cqlQuery = "MATCH (n) WHERE n.name = 'Andy' RETURN n"
        # cqlQuery = "MATCH (n) RETURN n"
        cqlQuery = query
        result = tx.run(cqlQuery).to_ndarray()
        print(result)
        sys.stdout.flush()

    def run_test_multiple_processes(self):
        print("Three processes, three processes: time test")
        start_time = timer()
        process_list = []
        queries = [["MATCH (n) RETURN n"], ["MATCH (n) RETURN n"], ["MATCH (n) RETURN n"]]
        for i in [i for i in enumerate(queries)]:
            # print(i)
            pos = i[0]
            query = i[1][0]
            # print(query)
            process = Process(target=self.multiple_processes_access_to_one_read_replica, args=(query,))
            process_list.append(process)
            process.start()

        map(lambda p: p.join(), process_list)

        # print(process_list)
        # process_list[0].start()
        # process_list[0].join()

        # for process in process_list:
        #     print()
        #     process.start()
        #     process.join()

        total_time_sec = timer() - start_time
        total_time_millis = total_time_sec * 1000
        print('\x1b[0;30;45m' + 'DB_Access_Test multiple processes exec time: ' + str(total_time_millis) + ' ms' + '\x1b[0m')

    # def get_overview(self):
    #     neograph_overview = Graph()