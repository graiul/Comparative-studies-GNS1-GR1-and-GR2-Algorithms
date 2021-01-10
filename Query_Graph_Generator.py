import networkx as nx

class Query_Graph_Generator(object):
    # Zhaosun Query Graph
    def gen_zhaosun_query_graph(self):
        query_graph = nx.Graph()
        query_graph_edges = [["a1", "b1"], ["a1", "c1"], ["c1", "d1"], ["c1", "f1"], ["f1", "d1"], ["d1", "b1"], ["d1", "e1"], ["e1", "b1"]]
        # query_graph_edges = [["a", "b"], ["a", "c"], ["c", "d"], ["c", "f"], ["f", "d"], ["d", "b"], ["d", "e"], ["e", "b"]]
        query_graph.add_edges_from(query_graph_edges)
        node_attr = ["a", "b", "c", "d", "e", "f"]
        node_attr_dict = dict(zip(sorted(query_graph.nodes()), node_attr)) # ATENTIE: daca se incurca asocierea dintre id-urile nodurilor cu label-urile corespunzatoare, trebuie scoasa sortarea crescatoare al id-urilor nodurilor. Aici lucram cu string-uri pentru id-urile nodurilor. Label-urile vor fi tot timpul de tipul str.
        nx.set_node_attributes(query_graph, node_attr_dict, 'label')
        return query_graph

    def gen_RI_query_graph(self):
        query_graph = nx.Graph()

        # query_graph_edges = [[1773, 1488]]
        # node_attr = ["25", "28"]

        # query_graph_edges = [[1773, 1488], [1773, 1898]]
        # node_attr = ["25", "28", "29"]

        # query_graph_edges = [[2462,4829], [2462,5730]]
        # node_attr = ["18", "5", "7"]

        # query_graph_edges = [[1773, 1488], [1773, 1898], [1773, 2285]]
        # node_attr = ["25", "28", "29", "27"]

        # query_graph_edges = [[1488, 7465]]
        # node_attr = ["28", "18"]

        # query_graph_edges = [[1898,1347], [1898,5596]]
        # node_attr = ["29", "31", "9"]

        # query_graph_edges = [[0,1773],[0,1817]]
        # node_attr = ["29", "25", "19"]

        # query_graph_edges = [[0, 1773], [0, 1817],[0,4426]]
        # node_attr = ["29", "25", "19", "13"]

        # query_graph_edges = [[7190,137], [7190,419], [7190,450]]
        # node_attr = ["3", "2", "11", "3"]

        # query_graph_edges = [[1773, 1488], [1773, 1898], [1773, 2285]]
        # node_attr = ["25", "28", "29", "27"]

        # query_graph_edges = [[1488, 7465]]
        # node_attr = ["28", "18"]


        # A doua serie de grafuri query pentru testare - fiecare este cate un STwig.
        # STwig Alg si VF2 Alg, pentru Articolul 2
        # Grafuri query cu 3 noduri:

        # ok
        # query_graph_edges = [[7711, 2243], [7711, 2259]]
        # node_attr = ["16", "2", "17"]

        # ok
        # query_graph_edges = [[2670, 10109], [2670, 10387]]
        # node_attr = ["29", "30", "20"]

        # ok
        # query_graph_edges = [[4164, 3526], [4164, 5687]]
        # node_attr = ["10", "26", "2"]

        # ok
        # query_graph_edges = [[5636, 2904], [5636, 3414]]
        # node_attr = ["16", "6", "30"]

        # ok
        # query_graph_edges = [[11965, 1278], [11965, 1291]]
        # node_attr = ["16", "13", "9"]


        # Grafuri query cu 6 noduri:

        # ok
        # query_graph_edges = [[11041, 2467], [11041, 2607], [11041, 2650], [11041, 2904], [11041, 3414]]
        # node_attr = ["18", "23", "11", "9", "6", "30"]

        # ok
        # query_graph_edges = [[7563, 5755], [7563, 6256], [7563, 6784], [7563, 7289], [7563, 7308]]
        # node_attr = ["18", "23", "3", "15", "26", "2"]

        # ok
        # query_graph_edges = [[6880, 5687], [6880, 6392], [6880, 9094], [6880, 12206], [6880, 11000]]
        # node_attr = ["9", "2", "23", "10", "22", "24"]

        # nu a fost gata nici dupa o executie de cinci ore si jumatate
        # query_graph_edges = [[7190, 3586], [7190, 3857], [7190, 3937], [7190, 4344], [7190, 4396]]
        # node_attr = ["3", "14", "8", "16", "11", "13"]

        # ok
        # query_graph_edges =[[58, 1870], [58, 1878], [58, 1982], [58, 3396], [58, 4819]]
        # node_attr = ["20", "13", "32", "4", "14", "11"]

        # ok
        # query_graph_edges = [[979, 4337], [979, 4341], [979, 4419], [979, 4736], [979, 4888]]
        # node_attr = ["14", "13", "3", "28", "8", "18"]


        # Grafuri query cu 9 noduri:

        # Acest graf blocheaza laptop-ul - STwig alg
        # query_graph_edges = [[10881, 8738], [10881, 8962], [10881, 9854], [10881, 10074], [10881, 10527], [10881, 10699], [10881, 11131], [10881, 12422]]
        # node_attr = ["18", "32", "1", "29", "20", "8", "17", "21", "2"]

        # Dupa 12 ore nu a terminat executia - STwig alg. Acesta este graful 11 din articolul 2.
        # Am incercat o noua executie: 28 apr 2020 ora 930 - 30 apr 2020 ora 1533 si a dat MemoryError la sfarsit. Mesajul complet de eroare cat si acest STwig input este aflat intr-un fisier text in directorul articolului 2.
        # Am rulat apoi cu VF2 cu succes si in timp fezabil de ~190 secunde.
        # query_graph_edges = [[3719, 850], [3719, 1287], [3719, 2035], [3719, 2611], [3719, 2764], [3719, 3366], [3719, 3482], [3719, 4005]]
        # node_attr = ["29", "32", "21", "19", "28", "17", "8", "6", "27"]


        # ------------------------------------------------------------------------------------------------------------------------------------
        # STwig Alg: Am testat cu 9 si cu 8 noduri, fara sa returneze rezultate in timp fezabil.
        # query_graph_edges = [[8214, 2598], [8214, 2614], [8214, 2670], [8214, 3238], [8214, 3253], [8214, 3366], [8214, 3620]] #, [8214, 3963]]
        # node_attr = ["15", "19", "32", "29", "11", "13", "8", "27"] #, "18"]

        # ------------------------------------------------------------------------------------------------------------------------------------

        # Urmatoarele nu sunt valabile pentru STwig Alg si VF2 Alg.
        # query_graph_edges = [[531,5399], [531,5671], [531,6393], [531,6702], [531,7289], [531,7421], [531,7438], [531,8066]]
        # node_attr = ["20", "32", "20", "22", "31", "26", "9", "16", "18"]

        # query_graph_edges = [[831,4915], [831,4924], [831,4976], [831,5144], [831,5157], [831,5164], [831,5272], [831,5399]]
        # node_attr = ["17", "24", "22", "14", "12", "32", "25", "2", "32"]

        # query_graph_edges = [[5414,1300], [5414,1341], [5414,1349], [5414,1365], [5414,1466], [5414,1519], [5414,1546], [5414,1547]]
        # node_attr = ["14", "3", "30", "20", "25", "8", "7", "24", "7"]

        # query_graph_edges = [[7020,2430], [7020,2473], [7020,2508], [7020,2540], [7020,2560], [7020,2573], [7020,2724], [7020,2771]]
        # node_attr = ["21", "9", "18", "24", "16", "26", "21", "6", "21"]

        # query_graph_edges = [[11000,8269], [11000,8429], [11000,8507], [11000,9430], [11000,10327], [11000,10426], [11000,11319], [11000,11783]]
        # node_attr = ["24", "19", "32", "25", "32", "24", "26", "11", "12"]


        # A treia serie de teste
        # STwig Alg si VF2 Alg, pentru Articolul 2

        # ok
        # query_graph_edges = [[7711, 2243], [7711, 2259]]
        # node_attr = ["16", "2", "17"]

        # ok
        # query_graph_edges = [[11041, 2467], [11041, 2607], [11041, 2650]]
        # node_attr = ["18", "23", "11", "9"]

        # ok
        # query_graph_edges =[[58, 1870], [58, 1878], [58, 1982], [58, 3396]]
        # node_attr = ["20", "13", "32", "4", "14"]

        # Dupa 1h jum STwig Alg, inca mai rula
        # query_graph_edges = [[10881, 8738], [10881, 8962], [10881, 9854], [10881, 10074]]
        # node_attr = ["18", "32", "1", "29", "20"]

        # Dupa 3h si jumatate cu STwig Alg, inca nu s-a terminat rularea
        # query_graph_edges = [[11041, 2467], [11041, 2607], [11041, 2650], [11041, 2904], [11041, 3414]]
        # node_attr = ["18", "23", "11", "9", "6", "30"]



        # ##############################################################################################################
        # Grafuri pentru testarea algoritmilor VF2 si GNS2v1 pentru Articolul 3.

        # query_graph_edges = [[1, 2], [3, 4], [5, 6], [7, 8]] # GNS ca si da rezultat o gasire, dar nu stiu daca  mai sunt si alte gasiri existente in graful RI cu 10000 muchii si 4652 de noduri.
                                                               # STwig Alg si VF2 Alg nu pot lucra cu grafuri query non-STwig.
                                                               # Comparatia atunci ar putea fi facuta cu un alt algoritm luat de pe net si rulat - pt grafuri query non-STwig
        # -------------------
        # query_graph_edges = [[1, 4], [3, 4], [5, 6], [7, 8]] - defect
        # query_graph.add_node(2)
        # -------------------

        # node_attr = ["24", "19", "32", "25", "32", "24", "26", "11"]

        # GNS2v1 da bucla infinita, chiar si pentru trei muchii ale acestui graf query cu forma de STwig.
        # query_graph_edges = [[11041, 2467], [11041, 2607], [11041, 2650]] #, [11041, 2904]] #, [11041, 3414]]
        # node_attr = ["18", "23", "11", "9"] #, "6"] #, "30"]

        # GNS2v1 bucla infinita pentru patru muchii DAR arata parte din rezultatele returnate de VF2.
        # Nu stocheaza timpii executiei partiale.
        # GNS2v1 functional pentru primele trei muchii.
        # query_graph_edges = [[8028, 3850], [8028, 58], [8028, 7465], [8028, 9294]]
        # node_attr = ["6", "4", "20", "18", "9"]

        # GNS2v1 Bucla infinita si un singur rezultat.
        # query_graph_edges = [[2850, 979], [2850, 3526], [2850, 5591]]
        # node_attr = ["27", "14", "26", "3"]

        # ok
        # query_graph_edges = [[8028, 3850], [8028, 58], [8028, 7465]]
        # node_attr = ["6", "4", "20", "18"]

        # ok
        # query_graph_edges = [[1773, 1488], [1773, 1898], [1773, 2285]]
        # node_attr = ["25", "28", "29", "27"]
        # ##############################################################################################################




        # Grafuri query cu forma STwig cu patru noduri si trei muchii pentru
        # testarea algoritmilor  STwig, VF2 si GNS1 pentru Articolul 3.

        # 1
        # GNS1 ruleaza fara bucla infinita
        # Ruleaza ok GNS1 si VF2.
        # Ruleaza ok si cu STwig Algorithm.
        # query_graph_edges = [[11041, 2467], [11041, 2607], [11041, 2650]]
        # node_attr = ["18", "23", "11", "9"]

        # 2
        # GNS1 ruleaza fara bucla infinita
        # Ruleaza ok GNS1 si VF2.
        # Ruleaza ok si cu STwig Algorithm.
        # query_graph_edges = [[8028, 3850], [8028, 58], [8028, 7465]]
        # node_attr = ["6", "4", "20", "18"]

        # 3
        # GNS1 ruleaza fara bucla infinita
        # Ruleaza ok GNS1 si VF2.
        # Ruleaza ok si cu STwig Algorithm.
        # query_graph_edges = [[2850, 979], [2850, 3526], [2850, 5591]]
        # node_attr = ["27", "14", "26", "3"]

        # 4
        # GNS1 ruleaza fara bucla infinita
        # Ruleaza ok GNS1 si VF2.
        # Ruleaza ok si cu STwig Algorithm.
        # query_graph_edges = [[1773, 1488], [1773, 1898], [1773, 2285]]
        # node_attr = ["25", "28", "29", "27"]

        # 5
        # GNS1 ruleaza fara bucla infinita
        # Ruleaza ok GNS1 si VF2.
        # Ruleaza ok si cu STwig Algorithm.
        # query_graph_edges = [[0, 1773], [0, 1817],[0,4426]]
        # node_attr = ["29", "25", "19", "13"]


        # Grafuri query cu forma STwig cu trei noduri si doua muchii pentru testarea algoritmilor VF2 si GNS1 pentru Articolul 3.

        # 6
        # Ruleaza ok GNS1 si VF2.
        # GNS1 ruleaza fara bucla infinita
        # Ruleaza ok si cu STwig Algorithm.
        # query_graph_edges = [[2462,4829], [2462,5730]]
        # node_attr = ["18", "5", "7"]

        # 7
        # Ruleaza ok GNS1 si VF2.
        # GNS1 ruleaza fara bucla infinita
        # Ruleaza ok si cu STwig Algorithm.
        # query_graph_edges = [[11000, 10426], [11000, 11319]]
        # node_attr = ["24", "26", "11"]

        # 8
        # Ruleaza ok GNS1 si VF2.
        # GNS1 ruleaza fara bucla infinita
        # Ruleaza ok si cu STwig Algorithm.
        # query_graph_edges = [[5157, 580], [5157, 734]]
        # node_attr = ["32", "18", "17"]

        # 9
        # Ruleaza ok GNS1 si VF2.
        # GNS1 ruleaza fara bucla infinita
        # Ruleaza ok si cu STwig Algorithm.
        # query_graph_edges = [[6954, 7970], [6954, 8161]]
        # node_attr = ["14", "22", "25"]

        # 10
        # Ruleaza ok GNS1 si VF2.
        # GNS1 ruleaza fara bucla infinita
        # Ruleaza ok si cu STwig Algorithm.
        # query_graph_edges = [[3842, 7591], [3842, 7596]]
        # node_attr = ["31", "6", "20"]


        # Grafuri query pentru testarea GR1_Algorithm

        # nr 1
        # ok - graf data RI 12,575 nodes si 86,890 relationships, un producator si doi consumatori
        # Cinci rulari
        # query_graph_edges = [[7711, 2243], [7711, 2259]]
        # node_attr = ["16", "2", "17"]

        # nr 2
        # ok - graf data RI 12,575 nodes si 86,890 relationships, un producator si doi consumatori
        # Cinci rulari
        # query_graph_edges = [[4164, 3526], [4164, 5687]]
        # node_attr = ["10", "26", "2"]

        # nr 3
        # ok - graf data RI 12,575 nodes si 86,890 relationships, un producator si doi consumatori
        # Cinci rulari
        # query_graph_edges = [[2670, 10109], [2670, 10387]]
        # node_attr = ["29", "30", "20"]

        # nr 4
        # ok - graf data RI 12,575 nodes si 86,890 relationships, un producator si doi consumatori
        # Cinci rulari
        # query_graph_edges = [[5636, 2904], [5636, 3414]]
        # node_attr = ["16", "6", "30"]

        # nr 5
        # ok - graf data RI 12,575 nodes si 86,890 relationships, un producator si doi consumatori
        # Cinci rulari
        # query_graph_edges = [[11965, 1278], [11965, 1291]]
        # node_attr = ["16", "13", "9"]

        # nr 6
        # ok - graf data RI 12,575 nodes si 86,890 relationships, un producator si trei consumatori
        # Cinci rulari
        # query_graph_edges = [[11041, 2467], [11041, 2607], [11041, 2650]]
        # node_attr = ["18", "23", "11", "9"]

        # nr 7
        # ok - graf data RI 12,575 nodes si 86,890 relationships, un producator si trei consumatori
        # Cinci rulari
        # query_graph_edges = [[8028, 3850], [8028, 58], [8028, 7465]]
        # node_attr = ["6", "4", "20", "18"]

        # nr 8
        # ok - graf data RI 12,575 nodes si 86,890 relationships, un producator si trei consumatori
        # Cinci rulari
        # query_graph_edges = [[2850, 979], [2850, 3526], [2850, 5591]]
        # node_attr = ["27", "14", "26", "3"]

        # nr 9
        # ok - graf data RI 12,575 nodes si 86,890 relationships, un producator si trei consumatori
        # Cinci rulari
        # query_graph_edges = [[1773, 1488], [1773, 1898], [1773, 2285]]
        # node_attr = ["25", "28", "29", "27"]

        # se tot blocheaza de la a doua rulare. Prima a avut urm timp: 178.9057435
        # query_graph_edges = [[0, 1773], [0, 1817],[0,4426]]
        # node_attr = ["29", "25", "19", "13"]

        # nr 10
        # ok - graf data RI 12,575 nodes si 86,890 relationships, un producator si trei consumatori
        # Cinci rulari
        # query_graph_edges = [[7190,137], [7190,419], [7190,450]]
        # node_attr = ["3", "2", "11", "3"]

        # nr 11
        # ok - graf data RI 12,575 nodes si 86,890 relationships, un producator si patru consumatori
        # fara print-uri ale rezultatelor in timpul rularii.
        # Cinci rulari. Dask scatter broadcast=False, un sg graf data, distribuire round-robin facuta de dask; distributed.dask.org/en/latest/locality.html
        # query_graph_edges =[[58, 1870], [58, 1878], [58, 1982], [58, 3396]]
        # node_attr = ["20", "13", "32", "4", "14"]

        # nr 12
        # ok - graf data RI 12,575 nodes si 86,890 relationships, un producator si patru consumatori
        # fara print-uri ale rezultatelor in timpul rularii.
        # Cinci rulari. Dask scatter broadcast=False, un sg graf data, distribuire round-robin facuta de dask; distributed.dask.org/en/latest/locality.html
        # query_graph_edges = [[10881, 8738], [10881, 8962], [10881, 9854], [10881, 10074]]
        # node_attr = ["18", "32", "1", "29", "20"]

        # nr 13
        # ok - graf data RI 12,575 nodes si 86,890 relationships, un producator si patru consumatori
        # fara print-uri ale rezultatelor in timpul rularii.
        # Cinci rulari. Dask scatter broadcast=False, un sg graf data, distribuire round-robin facuta de dask; distributed.dask.org/en/latest/locality.html
        # query_graph_edges = [[8379,8306], [8379,8374], [8379,8676], [8379,9219]]
        # node_attr = ["12", "24", "19", "6", "9"]

        # nr 14
        # ok - graf data RI 12,575 nodes si 86,890 relationships, un producator si patru consumatori
        # fara print-uri ale rezultatelor in timpul rularii.
        # Cinci rulari. Dask scatter broadcast=False, un sg graf data, distribuire round-robin facuta de dask; distributed.dask.org/en/latest/locality.html
        # query_graph_edges = [[9467,7395], [9467,7407], [9467,7465], [9467,7522]]
        # node_attr = ["28", "30", "1", "18", "11"]

        # nr 15
        # ok - graf data RI 12,575 nodes si 86,890 relationships, un producator si patru consumatori
        # fara print-uri ale rezultatelor in timpul rularii.
        # Cinci rulari. Dask scatter broadcast=False, un sg graf data, distribuire round-robin facuta de dask; distributed.dask.org/en/latest/locality.html
        # query_graph_edges = [[10095,4634], [10095,4723], [10095,4778], [10095,4858]]
        # node_attr = ["25", "28", "15", "10", "6"]

        # nr 16
        # ok - graf data RI 12,575 nodes si 86,890 relationships, un producator si cinci consumatori
        # fara print-uri ale rezultatelor in timpul rularii.
        # Cinci rulari. Dask scatter broadcast=False, un sg graf data, distribuire round-robin facuta de dask; distributed.dask.org/en/latest/locality.html
        # query_graph_edges = [[11041, 2467], [11041, 2607], [11041, 2650], [11041, 2904], [11041, 3414]]
        # node_attr = ["18", "23", "11", "9", "6", "30"]

        # nr 17
        # ok - graf data RI 12,575 nodes si 86,890 relationships, un producator si cinci consumatori
        # fara print-uri ale rezultatelor in timpul rularii.
        # Cinci rulari. Dask scatter broadcast=False, un sg graf data, distribuire round-robin facuta de dask; distributed.dask.org/en/latest/locality.html
        # query_graph_edges = [[7563, 5755], [7563, 6256], [7563, 6784], [7563, 7289], [7563, 7308]]
        # node_attr = ["18", "23", "3", "15", "26", "2"]

        # dureaza prea mult
        # query_graph_edges = [[6880, 5687], [6880, 6392], [6880, 9094], [6880, 12206], [6880, 11000]]
        # node_attr = ["9", "2", "23", "10", "22", "24"]

        # nr 18
        # ok - graf data RI 12,575 nodes si 86,890 relationships, un producator si cinci consumatori
        # fara print-uri ale rezultatelor in timpul rularii.
        # Cinci rulari. Dask scatter broadcast=False, un sg graf data, distribuire round-robin facuta de dask; distributed.dask.org/en/latest/locality.html
        # query_graph_edges = [[7190, 3586], [7190, 3857], [7190, 3937], [7190, 4344], [7190, 4396]]
        # node_attr = ["3", "14", "8", "16", "11", "13"]

        # nr 19
        # ok - graf data RI 12,575 nodes si 86,890 relationships, un producator si cinci consumatori
        # fara print-uri ale rezultatelor in timpul rularii.
        # Cinci rulari. Dask scatter broadcast=False, un sg graf data, distribuire round-robin facuta de dask; distributed.dask.org/en/latest/locality.html
        # query_graph_edges =[[58, 1870], [58, 1878], [58, 1982], [58, 3396], [58, 4819]]
        # node_attr = ["20", "13", "32", "4", "14", "11"]

        # nr 20
        # ok - graf data RI 12,575 nodes si 86,890 relationships, un producator si cinci consumatori
        # fara print-uri ale rezultatelor in timpul rularii.
        # Cinci rulari. Dask scatter broadcast=False, un sg graf data, distribuire round-robin facuta de dask; distributed.dask.org/en/latest/locality.html
        # query_graph_edges = [[979, 4337], [979, 4341], [979, 4419], [979, 4736], [979, 4888]]
        # node_attr = ["14", "13", "3", "28", "8", "18"]

        # ############################ Nu le folosesc #########################################
        # Preluat de la graful query nr 20 si despartit in 2 bucati:
        # Bucata 1:
        # query_graph_edges = [[979, 4337], [979, 4341]]
        # node_attr = ["14", "13", "3"]

        # Bucata 2:
        # query_graph_edges = [[979, 4419], [979, 4736], [979, 4888]]
        # node_attr = ["14", "28", "8", "18"]

        # NU. nr 21
        # query_graph_edges = [[979, 4337], [979, 4341], [979, 4419], [979, 4736], [979, 4888], [979, 5042]]
        # node_attr = ["14", "13", "3", "28", "8", "18", "15"]

        # NU. nr 26 vechi. Nr 22 noua numerotare.
        # Refolosit un graf query cu 6 noduri si am adaugat inca doua noduri
        # query_graph_edges = [[979, 4337], [979, 4341], [979, 4419], [979, 4736], [979, 4888], [979, 5042], [979, 5086]]
        # node_attr = ["14", "13", "3", "28", "8", "18", "15", "30"]
        # ############################ Nu le folosesc #########################################


        # ##################################################################################################
        # De aici incolo este necesara despartirea in bucati.
        # ##################################################################################################

        # nr 21
        # Dureaza prea mult intreg. Va fi despartit in bucati.
        # ok
        # query_graph_edges = [[7867,6217], [7867,6369], [7867,6419], [7867,6828], [7867,9155], [7867,9764]]
        # node_attr = ["10", "19", "16", "27", "26", "30", "12"]

        # nr 22
        # Dureaza prea mult intreg. Va fi despartit in bucati.
        # ok
        # query_graph_edges = [[10196,2551], [10196,2800], [10196,3083], [10196,3223], [10196,3318], [10196,3482]]
        # node_attr = ["27", "22", "20", "3", "8", "26", "6"]

        # ############################ Nu le folosesc #########################################
        # NU l-am mai folosit. Pentru testarea GR1 Algorithm cu bucati, vreau doar cate doua grafuri din fiecare nr de noduri de la sapte pana la zece.
        # query_graph_edges = [[10881, 8738], [10881, 8962], [10881, 9854], [10881, 10074], [10881, 10527], [10881, 10699]]
        # node_attr = ["18", "32", "1", "29", "20", "8", "17"]

        # nr 21
        # 25 min si nu s-a terminat prima rulare
        # Refolosit un graf query cu 6 noduri si am adaugat inca un nod
        # query_graph_edges = [[979, 4337], [979, 4341], [979, 4419], [979, 4736], [979, 4888], [979, 5042]]
        # node_attr = ["14", "13", "3", "28", "8", "18", "15"]

        # Graf nr 21
        # Il impart in doua bucati:
        # Bucata 1:
        # query_graph_edges = [[979, 4337], [979, 4341], [979, 4419]]
        # node_attr = ["14", "13", "3", "28"]

        # Bucata 2:
        # query_graph_edges = [[979, 4736], [979, 4888], [979, 5042]]
        # node_attr = ["14", "8", "18", "15"]
        # ############################ Nu le folosesc #########################################

        # nr 23
        # ok
        # query_graph_edges = [[2835,6770], [2835,6906], [2835,7465],
        #                      [2835,7707], [2835,7819], [2835,7916], [2835,8123]]
        # node_attr = ["12", "11", "17", "18",
        #              "24", "15", "21", "27"]

        # nr 24
        # ok
        # query_graph_edges = [[2840,1127], [2840,1322], [2840,1481],
        #                      [2840,1728], [2840,1744], [2840,1883], [2840,2105]]
        # node_attr = ["2", "23", "4", "32",
        #              "25", "19", "3", "6"]

        # # nr 25
        # # ok
        # query_graph_edges = [[2844,834], [2844,1127], [2844,1481],
        #                      [2844,1602],[2844,1747],[2844,1752],
        #                      [2844,1851],[2844,1871]]
        # node_attr = ["15", "1", "23", "32", "10", "16", "9", "21", "13"]

        # # nr 26
        # # ok
        # query_graph_edges = [[2844,1879], [2844,1943], [2844,2438],
        #                      [2844,2612], [2844,3160], [2844,3222],
        #                      [2844,3332], [2844,3343]]
        # node_attr = ["15", "11", "27",
        #              "9", "18", "3",
        #              "16", "6", "23"]

        # # nr 27
        # # ok
        # query_graph_edges = [[2844,3541], [2844,3787], [2844,4068],
        #                      [2844,4619], [2844,4731], [2844,4915],
        #                      [2844,5747], [2844,6149], [2844,6434]]
        # node_attr = ["15", "23", "27",
        #              "5", "22", "8",
        #              "24", "1", "12",
        #              "14"]

        # # nr 28
        # # ok
        # query_graph_edges = [[2844,6523], [2844,7387], [2844,7477],
        #                      [2844,7711], [2844,7844], [2844,7990],
        #                      [2844,8032], [2844,8281], [2844,8370]]
        # node_attr = ["15", "20", "25", "9", "16", "12", "5", "7", "22", "19"]

        # # nr 29
        # # ok
        # query_graph_edges = [[2846,84], [2846,128], [2846,288],
        #                      [2846,300], [2846,403], [2846,471],
        #                      [2846,522], [2846,557], [2846,617],
        #                      [2846,1032], [2846,1758], [2846,2079],
        #                      [2846,2259], [2846,2302], [2846,2329],
        #                      [2846,4060], [2846,4161], [2846,4592],
        #                      [2846,5079]]
        # node_attr = ["14", "11", "8", "22", "19", "6",
        #              "31", "18", "24","30", "10", "20",
        #              "13", "17", "3", "15", "29", "25",
        #              "26", "32"]

        # nr 30
        # ok
        # query_graph_edges = [[2846,5396], [2846,5451], [2846,5486],
        #                      [2846,5532], [2846,5797], [2846,6170],
        #                      [2846,6448], [2846,7020], [2846,7441],
        #                      [2846,7448], [2846,7711], [2846,8257],
        #                      [2846,8309], [2846,9145], [2846,9183],
        #                      [2846,9422], [2846,9738], [2846,11597],
        #                      [2846,11910]]
        # node_attr = ["14", "30", "3", "15", "27", "25",
        #              "22", "29", "21", "1", "20", "16",
        #              "11", "12", "5", "7", "18", "19",
        #              "31", "10"]

        # Testari algoritm GNS2v1 Algorithm si GR2 Algorithm

        # graf query STwig
        # nr 6 luat de la GR1 Algorithm
        # - graf data RI 12,575 nodes si 86,890 relationships, un producator si trei consumatori
        # x rulari
        # query_graph_edges = [[11041, 2467], [11041, 2607], [11041, 2650]]
        # node_attr = ["18", "23", "11", "9"]

        # ##################################
        # Rulare si cu graf query non-STwig
        # query_graph_edges = [[1, 2], [3, 4], [5, 6], [7, 8]] # GNS ca si da rezultat o gasire, dar nu stiu daca  mai sunt si alte gasiri existente in graful RI cu 10000 muchii si 4652 de noduri.
        # STwig Alg si VF2 Alg nu pot lucra cu grafuri query non-STwig.
        # Comparatia atunci ar putea fi facuta cu un alt algoritm luat de pe net si rulat - pt grafuri query non-STwig
        # -------------------
        # query_graph_edges = [[1, 4], [3, 4], [5, 6], [7, 8]] # - defect
        # query_graph.add_node(2)
        # -------------------

        # node_attr = ["24", "19", "32", "25", "32", "24", "26", "11"]
        # ##################################

        # Graf pentru a verifica daca GNS2v1 tine cont de ID-urile nodurilor.
        # TINE CONT de ID-urile nodurilor.
        # query_graph_edges = [[2871,9857], [9857,212], [212,114]]
        # # query_graph_edges = [[11, 22], [33, 44], [55, 66]]
        # node_attr = ["1", "18", "19", "10"]
        # # 2871,9857
        # # 9857,212
        # # 212,114

        # Graf query pentru procesul cu rol de producator din GR2 Algorithm.
        # query_graph_edges = [[2871, 9857]]
        # node_attr = ["1", "18"]

        # Graf query pentru procesul cu rol de producator si un
        # proces cu rol de consumator din GR2 Algorithm.
        query_graph_edges = [[2871, 9857], [9857,212],]
        node_attr = ["1", "18", "19"]

        query_graph.add_edges_from(query_graph_edges)

        node_attr_dict = dict(zip(query_graph.nodes(), node_attr)) # Am scos sortarea crescatoare al id-urilor nodurilor. Astfel se face corect asocierea intre noduri si label-uri.
        nx.set_node_attributes(query_graph, node_attr_dict, 'label')
        return query_graph

    def gen_small_graph_query_graph(self):
        small_graph = nx.Graph()
        small_graph_nodes = [1, 2, 3, 4]
        # Sortarea ascendenta la string este diferita de cea a de la tipul int
        small_graph_nodes.sort()
        small_graph_edges = [[1, 2], [1, 3], [1, 4]]
        small_graph.add_nodes_from(small_graph_nodes)
        small_graph.add_edges_from(small_graph_edges)
        node_attr = ["a", "b", "c", "d"]
        node_attr_dict = dict(zip(sorted(small_graph.nodes()), node_attr)) # ATENTIE: daca se incurca asocierea dintre id-urile nodurilor cu label-urile corespunzatoare, trebuie scoasa sortarea crescatoare al id-urilor nodurilor. Aici lucram cu string-uri pentru id-urile nodurilor. Label-urile vor fi tot timpul de tipul str.
                                                                            # Aici este o exceptie, ordinea crescatoare al nodurilor pastreaza ordinea originala a nodurilor. Ele coincid in acest caz.

        # print(node_attr_dict.items())
        nx.set_node_attributes(small_graph, node_attr_dict, 'label')
        # print(small_graph.nodes(data=True))
        # print(small_graph.edges())
        return small_graph
