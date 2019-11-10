from asyncio import wait

f1 = open("f1.txt", "r+")
f2 = open("f2.txt", "r+")

# https://www.techbeamers.com/python-read-file-line-by-line/
# https://www.techbeamers.com/python-read-file-line-by-line/#reading-file-using-python-context-manager
f1_string_lines = []
f2_string_lines = []
with open("f1.txt", "r") as rd:
    # Read lines in loop
    for line in rd:
        # All lines (besides the last) will include  newline, so strip it
        f1_string_lines.append(line.strip())
with open("f2.txt", "r") as rd2:
    # Read lines in loop
    for line in rd2:
        # All lines (besides the last) will include  newline, so strip it
        f2_string_lines.append(line.strip())

f1_int_lines = []
int_backtracking_line = []
for backtracking_line in f1_string_lines:
    # https://www.geeksforgeeks.org/python-string-split/
    string_backtracking_line = backtracking_line.split(" ")
    for string_backtracking_line_element in string_backtracking_line:
        int_backtracking_line.append(int(string_backtracking_line_element))
    f1_int_lines.append(int_backtracking_line)
    int_backtracking_line = []

for item in f1_int_lines:
    print(item)


f2_int_lines = []
int_stwig_line = []
for stwig_line in f2_string_lines:
    string_stwig_line = stwig_line.split(" ")
    for string_stwig_line_element in string_stwig_line:
        int_stwig_line.append(int(string_stwig_line_element))
    f2_int_lines.append(int_stwig_line)
    int_stwig_line = []

print()
for item2 in f2_int_lines:
    print(item2)
counter = 0

# https://thispointer.com/python-check-if-a-list-contains-all-the-elements-of-another-list/
for stwig_line in f2_int_lines:
    # print("STwig line: " + str(stwig_line))
    for backtracking_line in f1_int_lines:
        # print("Backtracking line: " + str(backtracking_line))
        result = all(elem in stwig_line for elem in backtracking_line)
        if result:
            print("STwig line: " + str(stwig_line) + " | Backtracking line: " + str(backtracking_line) + " | " + str(result))
            counter += 1
print()
print(counter)
# print()
# print(all(elem in [6523, 269, 1481, 6107] for elem in [6523, 269, 1481, 12230]))
