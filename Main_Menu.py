from Graph_File_Generator import Graph_File_Generator
from Local_Cluster_Access_Test import Local_Cluster_Access_Test
from neo4j_test_2 import neo4j_test_2

print("   _____ _______       _                  _                  _ _   _                 _____ _____ ")
print("  / ____|__   __|     (_)           /\   | |                (_) | | |               |_   _|_   _|")
print(" | (___    | |_      ___  __ _     /  \  | | __ _  ___  _ __ _| |_| |__  _ __ ___     | |   | |  ")
print("  \___ \   | \ \ /\ / / |/ _` |   / /\ \ | |/ _` |/ _ \| '__| | __| '_ \| '_ ` _ \    | |   | |  ")
print("  ____) |  | |\ V  V /| | (_| |  / ____ \| | (_| | (_) | |  | | |_| | | | | | | | |  _| |_ _| |_ ")
print(" |_____/   |_| \_/\_/ |_|\__, | /_/    \_\_|\__, |\___/|_|  |_|\__|_| |_|_| |_| |_| |_____|_____|")
print("                          __/ |              __/ |                                               ")
print("                         |___/              |___/                                                ")
print("\n\n1. Graph generator tool")
print("2. View graph data")
print("3. Run db access test")
print("4. Run STwig Algorithm II")
print("0. Exit")
while(True):
    option = int(input('\nPlease choose option: '))
    if option == 3:
        print("\n================= Option 3 commencing... =================")
        test = Local_Cluster_Access_Test()
        test.run_test()
        print("\n============== End of Option 3 execution =================")
    elif option == 4:
        print("\n================= Option 4 commencing... =================")
        print("STwig_Order_Selection: ")
        test2 = neo4j_test_2()
        query_graph_gen = Graph_File_Generator()
        query_graph = query_graph_gen.gen_zhaosun_query_graph()
        print(test2.STwig_Order_Selection(query_graph))
        print("\n============== End of Option 4 execution =================")

    elif option == 0:
        exit(code=0)
