import copy

# https://stackoverflow.com/questions/743806/how-to-split-a-string-into-a-list
# https://stackoverflow.com/questions/7368789/convert-all-strings-in-a-list-to-int
def convert_str_line_to_list_of_ints(text_file_path):
    f1 = open(text_file_path, "r")
    # f2 = open("text_2", "r")
    lines_1 = []
    # lines_2 = []
    roots_1 = []
    lines_1_int = []

    for line_1 in f1:
        # f1.readline()
        aux = copy.deepcopy(line_1.split("\n")[0].split("[")[1].split("]")[0])
        # print(aux)
        # https://stackoverflow.com/questions/743806/how-to-split-a-string-into-a-list
        aux2 = copy.deepcopy(aux.split(", "))
        # print(aux2)
        # https://stackoverflow.com/questions/7368789/convert-all-strings-in-a-list-to-int
        aux3 = copy.deepcopy([int(i) for i in aux2])
        # print(aux3)
        lines_1_int.append(aux3)
    # print(aux3)
    f1.close()
    return lines_1_int

# def reunion_of_query_STwig_parts_results(list_of_paths):
#     for path in
def reunion_of_query_STwig_parts_results(list_of_query_STwig_parts_results_lists): # De generalizat.
    reunited_results = []
    # Doar pentru doua liste de rezultate pentru bucati query STwig
    # for r1 in results1:
    #     # print(r1)
    #     root_r1 = r1[0]
    #     # print(root_r1)
    #     for r2 in results2:
    #         root_r2 = r2[0]
    #         if root_r1 == root_r2:
    #             # print([r1, r2])
    #             del r2[0]
    #             # https://stackoverflow.com/questions/1720421/how-do-i-concatenate-two-lists-in-python
    #             reunited_results.append(r1 + r2)

    reunited_results_dict = {}
    # Generalizare
    for list_res in list_of_query_STwig_parts_results_lists: # !!!
        if list_of_query_STwig_parts_results_lists.index(list_res) == 0:
            # print(list_of_query_STwig_parts_results_lists.index(list_res))
            for res in list_res:
                reunited_results.append(res)

        else:
            # print(list_of_query_STwig_parts_results_lists.index(list_res))
            for res in list_res:
                for rr in reunited_results:
                    if res[0] == rr[0]:
                        # del res[0]
                        # print(rr+res)
                        for node_id in res[1:]:
                            rr.append(node_id)

    return reunited_results


results1 = convert_str_line_to_list_of_ints("text_1")
results2 = convert_str_line_to_list_of_ints("text_2")
results3 = convert_str_line_to_list_of_ints("text_3")

all_results = [results1, results2, results3]
for re in reunion_of_query_STwig_parts_results(all_results):
    print(re)

    # aux2 = copy.deepcopy(aux.split(", ")[0].split("[")[1])
    # print(aux2)
    # roots_1.append(int(aux2))
    # print(line)
    # lines_1.append(aux)
# print(lines_1)
# print(roots_1)
# for l in lines_1:
#     print(l)
#     lines_1_int.append(list(map(int, l)))
# for line_2 in f2:
#     # f1.readline()
#     aux = copy.deepcopy(line_2.split("\n")[0])
#     # print(line)
#     lines_2.append(aux)
# print(lines_2)

# for l1 in lines_1:
#     for l2 in lines_2:
#         print(l1[1])

