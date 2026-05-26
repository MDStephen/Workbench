# Data Cleaner, dirty markdown to clean csv

import csv
import sys

# catch no argument case
if len(sys.argv) < 3:
    print("2 arguments are required, [input file path, output file path]")
    sys.exit(0)

# word-list.md to word-list.csv
input_file_path = sys.argv[1]
output_file_path = sys.argv[2]

with open(input_file_path, "r", encoding="utf-8") as infile, \
    open(output_file_path, "w", newline="", encoding="utf-8") as outfile:

    writer = csv.writer(outfile)
    writer.writerow(["id", "word", "optional"])
    
    id = 0
    
    for line in infile:
        # Parse logic, either the line contains no usable information and is skipped,
        # written to the csv file 
        # Strip all non-letter characters before the first letter.
        # Input e.g.
        # word (optional information)
        # Output e.g.
        # 1, word, optional information,
        
        word = ""
        opt = ""
        seen_first_letter = False
        opt_flag = False
        
        for char in line:
            if char.isalpha():
                seen_first_letter = True
                if opt_flag:
                    opt += char
                else:
                    word += char
            elif opt_flag and char not in {"\n", ")"}:
                opt += char # optional information is formatted in sentences, spaces allowed
            elif seen_first_letter and char == "(":
                opt_flag = True
            elif not seen_first_letter and char == "#":
                break # prevents titles or headers from being added

        if word != "":
            writer.writerow([id, word, opt])
            id += 1


