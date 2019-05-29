# from multiprocessing import Pool, Process, Queue
from pathos.multiprocessing import ProcessingPool as Pool
# from py2neo import Graph, Node, Relationship

class Foo():
    # @staticmethod
    def work(self, query):
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
        # queue.put(str(result))
        # return queue


    def process(self):
        if __name__ == '__main__':
            # foo = Foo()
            queries = ["MATCH (n) RETURN n", "MATCH (n) RETURN n", "MATCH (n) RETURN n"]
            p = Pool(3)
            print("Pool result:")
            res = p.map(self.work, queries)
            # print(res)
            for r in res:
                for rr in r:
                    print(rr)
                print()
            p.close()

foo = Foo()
foo.process()