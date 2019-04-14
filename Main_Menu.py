from Graph_File_Generator import Graph_File_Generator
from DB_Access_Test import DB_Access_Test
from Dataset_Operator import Dataset_Operator
from neo4j_test_2 import neo4j_test_2
import os

menu = [
    ["\n\n1. Graph generator tool"],
    ["2. Insert data into db"],
    ["3. Delete data from db"],
    ["4. View graph data"],
    ["5. Run parallel db access test"],
    ["6. Run MatchSTwig"],
    ["7. Run STwig_Order_Selection"],
    ["8. Query graph zhaosun split prototype, single threaded"],
    ["9. Configure db"],
    ["0. Exit"]
]
print()
for m in menu:
    print(m)
while(True):
    option = int(input('\nPlease choose option: '))
    if option == 2:
        node_dataset_url = str(input('\nDataset nodes URL: '))
        edge_dataset_url = str(input('\nDataset edges URL: '))
        leader_core_bolt_address = str(input('\nLeader core bolt address: '))
        username = str(input('\nUsername of core: '))
        passwd = str(input('\nPassword of core: '))
        dataset_operator = Dataset_Operator(node_dataset_url, edge_dataset_url, leader_core_bolt_address, username, passwd)
        dataset_operator.insert_nodes()
        dataset_operator.insert_edges()
        print()
        for m in menu:
            print(m)
    elif option == 3:
        leader_core_bolt_address = str(input('\nLeader core bolt address: '))
        username = str(input('\nUsername of core: '))
        passwd = str(input('\nPassword of core: '))
        dataset_operator = Dataset_Operator(None, None, leader_core_bolt_address, username, passwd)
        dataset_operator.delete_data_from_db()
        print()
        for m in menu:
            print(m)
    elif option == 5:
        print("\n================= Option 5 commencing... =================")
        test = DB_Access_Test()
        test.run_test()
        print("\n============== End of Option 5 execution =================")
        print()
        for m in menu:
            print(m)

    elif option == 6:
        print("\n================= Option 6 commencing... =================")
        q = ['a', ['b', 'c']]  # De facut din fisier, nu hardcoded
        test2 = neo4j_test_2()
        print("Searcing given STwigs from query graph in the data graph: ")
        STwigs = test2.MatchSTwig(q)
        print("\nSTwigs from data graph corresponding to the query STwig given: ")
        for stwig in STwigs:
            print(stwig)
        print("\n============== End of Option 6 execution =================")

    elif option == 7:
        print("\n================= Option 7 commencing... =================")
        print("STwig_Order_Selection: ")
        test2 = neo4j_test_2()
        query_graph_gen = Graph_File_Generator()
        query_graph = query_graph_gen.gen_zhaosun_query_graph()
        print(test2.STwig_Order_Selection(query_graph))
        print("\n============== End of Option 7 execution =================")
        print()
        for m in menu:
            print(m)


    elif option == 8:
        print("\n================= Option 8 commencing... =================")
        print("Are these the query graph STWIGS?")
        test2 = neo4j_test_2()
        query_graph_gen = Graph_File_Generator()
        query_graph = query_graph_gen.gen_zhaosun_query_graph()
        splits = test2.Query_Graph_Split(query_graph)
        for s in splits:
            print(str(splits))
        print("\n============== End of Option 8 execution =================")

    elif option == 9:
        file = "notepad.exe neo4j_db\\docker-compose.yml"
        os.system(file)



    elif option == 0:
        exit(code=0)
