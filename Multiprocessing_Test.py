# from multiprocessing import Pool, Process, Queue
from pathos.multiprocessing import ProcessingPool as Pool

# from py2neo import Graph, Node, Relationship
from DB_Access_Test import DB_Access_Test
from timeit import default_timer as timer


class Foo():
    # @staticmethod
    def work(self, query):
        from py2neo import Graph
        from timeit import default_timer as timer

        neograph_data = Graph("bolt://127.0.0.1:7690", auth=("neo4j", "changeme"))
        tx = neograph_data.begin()
        cqlQuery = query
        start_time = timer()
        result = tx.run(cqlQuery).to_ndarray()
        total_time_sec = timer() - start_time
        total_time_millis = total_time_sec * 1000
        print()
        print('\x1b[0;30;45m' + 'DB_Access_Test multiple procs exec time: ' + str(
            total_time_millis) + ' ms' + '\x1b[0m')
        string_result = []
        for r in result:
            string_result.append(str(r))
        return string_result
        # queue.put(str(result))
        # return queue


if __name__ == '__main__':
    foo = Foo()
    db = DB_Access_Test()
    queries = ["MATCH (n) RETURN n", "MATCH (n) RETURN n", "MATCH (n) RETURN n"]
    p = Pool(3)
    print("Pool result:")
    start_time = timer()
    res = p.map(foo.work, queries)
    # res = p.map(db.multiple_processes_access_to_one_read_replica, queries)
    total_time_sec = timer() - start_time
    total_time_millis = total_time_sec * 1000
    # print(res)
    for r in res:
        for rr in r:
            print(rr)
        print()
    print()
    print('\x1b[0;30;45m' + 'DB_Access_Test multiple procs exec time: ' + str(
        total_time_millis) + ' ms' + '\x1b[0m')

