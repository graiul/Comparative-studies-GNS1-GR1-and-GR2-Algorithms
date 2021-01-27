with open('RI_data_graph_edges_for_csv.txt') as f:
    lines = f.readlines()
f = open('RI_data_graph_edges.csv', "w+")
f.write("from,to\n")
for line in lines:
    new_line = line.split(" ")
    # print(new_line)
    # print(str(new_line[0]) + "," + str(new_line[1]))
    f.write(str(new_line[0]) + "," + str(new_line[1]))
