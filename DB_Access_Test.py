import multiprocessing
import sys
import threading
# from multiprocessing import Pool
from pathos.multiprocessing import ProcessingPool as Pool
from py2neo import Graph
from timeit import default_timer as timer

class DB_Access_Test(object):
    neograph_data = Graph("bolt://127.0.0.1:7691", auth=("neo4j", "changeme"))

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
        from py2neo import Graph
        neograph_data = Graph("bolt://127.0.0.1:7690", auth=("neo4j", "changeme"))
        tx = neograph_data.begin()
        cqlQuery = query
        # print(cqlQuery)
        result = tx.run(cqlQuery).to_ndarray()
        string_result = []
        for r in result:
            string_result.append(str(r))
        return string_result
    #
    # def run_test_multiple_processes(self):
    #     # if __name__ == '__main__':
    #     # foo = Foo()
    #     queries = ["MATCH (n) RETURN n", "MATCH (n) RETURN n", "MATCH (n) RETURN n"]
    #     p = Pool(3)
    #     print("Pool result:")
    #     res = p.map(self.multiple_processes_access_to_one_read_replica, queries)
    #     # print(res)
    #     for r in res:
    #         for rr in r:
    #             print(rr)
    #         print()
    #     p.close()


    # def get_overview(self):
    #     neograph_overview = Graph()


    def match_finding_process(self, query_stwig, return_dict):
        # print("--------Iteration number: " + str(iteration_number) + str("-----------"))
        from neo4j_test_2 import neo4j_test_2
        from Query_Graph_Generator import Query_Graph_Generator
        query_graph_gen = Query_Graph_Generator()
        query_graph = query_graph_gen.gen_zhaosun_query_graph()
        test2 = neo4j_test_2(query_graph)
        test2.STwig_query_neighbor_labels = query_stwig[1]
        matches = test2.MatchSTwig(query_stwig, 0)
        test2.matches_dict[repr(query_stwig)] = matches

        print("Matches dictionary: ")
        print("First key: ")
        print(list(test2.matches_dict.keys())[0])
        print('\x1b[0;30;45m' + "First values attached to the first key; matches: " + '\x1b[0m')
        for match in list(test2.matches_dict.values())[0]:
            print('\x1b[0;30;45m' + str(match) + '\x1b[0m')
        return_dict[0] = list(test2.matches_dict.values())[0]
        return list(test2.matches_dict.values())[0]
        # print("--------Iteration end-----------------")

    def match_finding_process_filtered(self, query_stwig, return_dict, STwig_query_neighbor_labels, query_graph, iter_num, used_stwigs):
        from STwig_Algorithm import STwig_Algorithm
        STwig_query_neighbor_labels = query_stwig[1]
        STwig_algorithm = STwig_Algorithm(query_graph, return_dict, used_stwigs, STwig_query_neighbor_labels)
        matches = STwig_algorithm.MatchSTwig(query_stwig, iter_num) # Ca filtrarea sa mearga, trebuie sa dam si numarul iteratiilor!
        # print(matches)
        return_dict[repr(query_stwig)] = matches
