f1 = open("file_VF2 Algorithm execution times.txt", "r+")

# f1 = open("file_STwig Algorithm execution times.txt", "r+")
# f1 = open("file_GNS1_Backtracking_STwig_Matching_Algorithm_execution_times.txt", "r+")

list_of_execution_times = []
times_sum = 0
result = 0
f1_string_lines = []

with open("file_VF2 Algorithm execution times.txt", "r") as rd:

# with open("file_STwig Algorithm execution times.txt", "r") as rd:
# with open("file_GNS1_Backtracking_STwig_Matching_Algorithm_execution_times.txt", "r") as rd:

    # Read lines in loop
    for line in rd:
        # All lines (besides the last) will include  newline, so strip it
        f1_string_lines.append(line.strip())

f1_int_lines = []
float_val_lines = []
for string_line in f1_string_lines:
    # https://www.geeksforgeeks.org/python-string-split/
    split_string_line = string_line.split(" ")
    for string_backtracking_line_element in split_string_line:
        float_val_lines.append(float(string_backtracking_line_element))

print(float_val_lines)
times_sum = float(0)
result = float(0)
length = len(float_val_lines)
for t in float_val_lines:
    times_sum = times_sum + t
result = times_sum / length
print(result)
