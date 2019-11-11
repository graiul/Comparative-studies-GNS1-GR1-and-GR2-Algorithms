from collections import OrderedDict

test_list = [(6523, 269, 9382, 12230), (6523, 269, 12230, 9382)] # Chei pentru dictionar
test_list2 = [(6523, 269, 9382, 12230), (6523, 269, 12230, 9382), (1, 2, 3, 4)] # Ambele sunt valori pentru fiecare cheie din dict

test_list_dict = OrderedDict().fromkeys(test_list)
for key in test_list_dict.keys():
    test_list_dict[key] = []
# for elem in test_list_dict.keys():
#     print(elem)
# test_result = all(elem in (6523, 269, 9382, 12230) for elem in (6523, 269, 9382, 12230))
# print(test_result)

for key in test_list_dict.keys():
    print("key:" + str(key))
    for el2 in test_list2:
        print("el2: " + str(el2))
        result = all(elem in key for elem in el2)
        print("result: " + str(result))
        if result == True:
            test_list_dict[key].append(el2)
        #     test_list2.remove(el)
print()
print(test_list_dict[(6523, 269, 9382, 12230)])

        # NU MAI TREB:Numara aparitiile primului stwig in a doua lista, indiferent de ordinea frunzelor
        # Fa un dictionar cu toate aparitiile lui, indiferent daca frunzele sunt permutate sau nu.
        # UPDATE: Ramane valoarea care este egala cu cheia. Alege o valoare pe care sa o pastrezi, din toate valorile asociate cheii. Restul elimina-le din lista a doua.
        # Cand iterez apoi in continuare prima lista, verific daca vreun element din aceasta se afla printre valorile eliminate care
        # au avut ca si cheie un element precedent. Daca ele sunt egale, trecem la urmatorul element din prima lista.
# print(test_list2)