from Graph_File_Generator import Graph_File_Generator
from Local_Cluster_Access_Test import Local_Cluster_Access_Test
from Dataset_Operator import Dataset_Operator
from neo4j_test_2 import neo4j_test_2

print("   _____ _______       _                  _                  _ _   _                 _____ _____ ")
print("  / ____|__   __|     (_)           /\   | |                (_) | | |               |_   _|_   _|")
print(" | (___    | |_      ___  __ _     /  \  | | __ _  ___  _ __ _| |_| |__  _ __ ___     | |   | |  ")
print("  \___ \   | \ \ /\ / / |/ _` |   / /\ \ | |/ _` |/ _ \| '__| | __| '_ \| '_ ` _ \    | |   | |  ")
print("  ____) |  | |\ V  V /| | (_| |  / ____ \| | (_| | (_) | |  | | |_| | | | | | | | |  _| |_ _| |_ ")
print(" |_____/   |_| \_/\_/ |_|\__, | /_/    \_\_|\__, |\___/|_|  |_|\__|_| |_|_| |_| |_| |_____|_____|")
print("                          __/ |              __/ |                                               ")
print("                         |___/              |___/                                                ")

menu = [
    ["\n\n1. Graph generator tool"],
    ["2. Insert data into cluster"],
    ["3. Delete data from cluster"],
    ["4. View graph data"],
    ["5. Run parallel db access test"],
    ["6. Run STwig Algorithm II"],
    ["7. Configure cluster"],
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
        dataset_operator.delete_data_from_cluster()
        print()
        for m in menu:
            print(m)
    elif option == 5:
        print("\n================= Option 5 commencing... =================")
        test = Local_Cluster_Access_Test()
        test.run_test()
        print("\n============== End of Option 5 execution =================")
        print()
        for m in menu:
            print(m)
    elif option == 6:
        print("\n================= Option 6 commencing... =================")
        print("STwig_Order_Selection: ")
        test2 = neo4j_test_2()
        query_graph_gen = Graph_File_Generator()
        query_graph = query_graph_gen.gen_zhaosun_query_graph()
        print(test2.STwig_Order_Selection(query_graph))
        print("\n============== End of Option 6 execution =================")
        print()
        for m in menu:
            print(m)

    elif option == 0:
        exit(code=0)
