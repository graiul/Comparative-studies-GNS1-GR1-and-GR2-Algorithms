from asyncio import wait

f1 = open("file_GNS1_Backtracking_STwig_Matching_Algorithm_output.txt", "r+")
# f1 = open("file_STwig Algorithm output.txt", "r+")

f2 = open("file_VF2 Algorithm output.txt", "r+")
# f2 = open("file_GNS1_Backtracking_STwig_Matching_Algorithm_output.txt", "r+")


# https://www.techbeamers.com/python-read-file-line-by-line/
# https://www.techbeamers.com/python-read-file-line-by-line/#reading-file-using-python-context-manager
f1_string_lines = []
f2_string_lines = []

with open("file_GNS1_Backtracking_STwig_Matching_Algorithm_output.txt", "r") as rd:
# with open("file_STwig Algorithm output.txt", "r") as rd:
    # Read lines in loop
    for line in rd:
        # All lines (besides the last) will include  newline, so strip it
        f1_string_lines.append(line.strip())
with open("file_VF2 Algorithm output.txt", "r") as rd2:
    # Read lines in loop
    for line in rd2:
        # All lines (besides the last) will include  newline, so strip it
        f2_string_lines.append(line.strip())

f1_int_lines = []
int_stwig_alg_line = []
for stwig_line in f1_string_lines:
    # https://www.geeksforgeeks.org/python-string-split/
    string_backtracking_line = stwig_line.split(" ")
    for string_backtracking_line_element in string_backtracking_line:
        int_stwig_alg_line.append(int(string_backtracking_line_element))
    f1_int_lines.append(int_stwig_alg_line)
    int_stwig_alg_line = []

# for item in f1_int_lines:
#     print(item)


f2_int_lines = []
int_stwig_line = []
for stwig_line in f2_string_lines:
    string_stwig_line = stwig_line.split(" ")
    for string_stwig_line_element in string_stwig_line:
        int_stwig_line.append(int(string_stwig_line_element))
    f2_int_lines.append(int_stwig_line)
    int_stwig_line = []

# print()
# for item2 in f2_int_lines:
#     print(item2)
# print()

counter_stwig = 0
counter_vf2 = 0
counter = 0
for stwig_line in f1_int_lines:
    counter_stwig += 1
for vf2_line in f2_int_lines:
    counter_vf2 += 1

# https://thispointer.com/python-check-if-a-list-contains-all-the-elements-of-another-list/
for vf2_line1 in f2_int_lines:
    # print("STwig line: " + str(stwig_line))
    for stwig_line1 in f1_int_lines:
        # print("Backtracking line: " + str(backtracking_line))
        # counter += 1
        result = all(elem in vf2_line1 for elem in stwig_line1)
        if result:
            print("STwig line: " + str(stwig_line1) + " | VF2 line: " + str(vf2_line1) + " | " + str(result))
            counter = counter + 1
print()
print("counter_stwig: " + str(counter_stwig))
print("counter_vf2: " + str(counter_vf2))
print("total count: " + str(counter))

