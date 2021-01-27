with open('DATASET RI Caenorhabditis elegans PPI/Caenorhabditis_elegans_PPI_udistr_32_edges_for_CSV.txt') as f:
    lines = f.readlines()
f = open('DATASET RI Caenorhabditis elegans PPI/Caenorhabditis_elegans_PPI_udistr_32_edges.csv', "w+")
f.write("from,to\n")
for line in lines:
    new_line = line.split(" ")
    # print(new_line)
    # print(str(new_line[0]) + "," + str(new_line[1]))
    f.write(str(new_line[0]) + "," + str(new_line[1]))
