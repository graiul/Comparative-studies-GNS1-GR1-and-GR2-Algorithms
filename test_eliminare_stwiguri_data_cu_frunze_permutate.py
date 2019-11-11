import copy
from collections import OrderedDict

test_list = [(6523, 269, 9382, 12230), (6523, 269, 12230, 9382)] # Chei pentru dictionar
test_list2 = [(6523, 269, 9382, 12230), (6523, 269, 12230, 9382), (1, 2, 3, 4)] # Se vor alege doar valorile care sunt analoage cu cheile.
                                                                                # Aceasta diferentiere este importanta in cazul in care in lista avem
                                                                                # rezultatele de la mai multe STwig-uri query.
test_list2_for_removal = copy.deepcopy(test_list2)

test_list_dict = OrderedDict().fromkeys(test_list)
for key in test_list_dict.keys():
    test_list_dict[key] = []

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
print("test_list_dict[(6523, 269, 9382, 12230)] values: " + str(test_list_dict[(6523, 269, 9382, 12230)]))
print("test_list_dict[(6523, 269, 12230, 9382)] values: " + str(test_list_dict[(6523, 269, 12230, 9382)]))

to_remove = []
for key in test_list_dict.keys():
    for value in test_list_dict[key]:
        if key in to_remove:
            continue
        else:
            if value != key:
                for el2 in test_list2:
                    if value == el2:
                        test_list2_for_removal.remove(value)
                        to_remove.append(value)
print()
print("List of data STwigs without permutated leafs: ")
print(test_list2_for_removal)

        # NU MAI TREB:Numara aparitiile primului stwig in a doua lista, indiferent de ordinea frunzelor
        # Fa un dictionar cu toate aparitiile lui, indiferent daca frunzele sunt permutate sau nu.
        # UPDATE: Ramane valoarea care este egala cu cheia. Alege o valoare pe care sa o pastrezi, din toate valorile asociate cheii. Restul elimina-le din lista a doua.
        # Cand iterez apoi in continuare prima lista (urmatoarele chei), verific daca vreun STwig din aceasta este egal cu unul din cele eliminate care
        # au avut ca si cheie un STwig precedent din prima lista. Daca ele sunt egale, trecem la urmatorul element din prima lista, deoarece el deja va lipsi din lista a doua.
