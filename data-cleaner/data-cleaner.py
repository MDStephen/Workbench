# Data Cleaner
import csv
import sys

# catch no argument case
if len(sys.argv) < 4:
    print("3 arguments are required, [input file path, output file path, mode]")
    sys.exit(0)

input_file_path = sys.argv[1]
output_file_path = sys.argv[2]
mode = sys.argv[3]

if "word-opt" in mode:
    mode = 1
elif "title-date" in mode:
    mode = 2
else:
    print("Argument 3, incorrect mode")
    sys.exit(1)

with open(input_file_path, "r", encoding="utf-8") as infile, \
    open(output_file_path, "w", newline="", encoding="utf-8") as outfile:

    writer = csv.writer(outfile)
    id = 0

    # Mode 1, Parse logic either the line contains no usable information and is skipped,
        # written to the csv file 
        # Strip all non-letter characters before the first letter.
        # Input e.g.
        # word (optional information)
        # Output e.g.
        # 1, word, optional information,
    if mode == 1:
        writer.writerow(["id", "word", "optional"])
        for line in infile:
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

            if not word.strip():
                writer.writerow([id, word, opt])
                id += 1

    # Mode 2, Input Parse rules
        # for the string:
        # remove: {# - ( )}
        # keep: {, : ! '}
        # format: string with spaces (date)
        # include spaces only between words, not on the ends or in the year
        # date must be in a separate field but is not necessary, some lines will be missing years which should still be written just as nulls
        # follow as closely the parsing rules for the singular word list to csv
    if mode == 2:
        writer.writerow(["id", "title", "year"])

        #keep = {",", ":", "!", "'", "."}
        remove = {"#", "-", "(", ")", "\n"}

        for line in infile:
            title = ""
            year = ""
            seen_first_keep = False
            year_flag = False

            for char in line:
                if char not in remove and not year_flag:
                    seen_first_keep = True
                    title += char
                elif year_flag and char.isdigit():
                    year += char # year must only be numbers and no longer than 4 characters in length
                elif seen_first_keep and char == "(":
                    year_flag = True
                elif not seen_first_keep and char == "#":
                    break # prevents titles or headers from being added in case of markdown files

            if title.strip():
                writer.writerow([id, title, year])
                id += 1

print("Successfully exported ", id, " lines to ", output_file_path, " in mode ", mode, ".")
















