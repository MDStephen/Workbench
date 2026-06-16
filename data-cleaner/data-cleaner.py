# Data Cleaner
import csv
import sys
import re

# catch no argument case
if len(sys.argv) < 4:
    print("3 arguments are required, [input file path, output file path, mode]")
    sys.exit(0)

input_file_path = sys.argv[1]
output_file_path = sys.argv[2]
mode_input = sys.argv[3]

modes = ["word-opt", "title-date", "title-author", "stripped-link-description", "checkmark-description"]
mode = 0

for m in modes:
    mode += 1
    if m == mode_input:
        break
else:
    print("Incorrect mode: choose from " + str(modes))
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

            if word.strip():
                writer.writerow([id, word, opt])
                id += 1
            elif line:
                print(line)

    # Mode 2, Input Parse rules
        # for the string:
        # remove: {# - ( )}
        # keep: {, : ! '}
        # format: string with spaces (date)
        # include spaces only between words, not on the ends or in the year
        # date must be in a separate field but is not necessary, some lines will be missing years which should still be written just as nulls
        # follow as closely the parsing rules for the singular word list to csv
    elif mode == 2:
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
            elif line:
                print(line)

    # Mode 3, title-author
        # the date section is optional
        # strings are deliminated by dashes
    elif mode == 3:
        writer.writerow(["id", "title", "author"])

        for line in infile:
            title = ""
            author = ""
            deliminater = ['-', '—']
            author_flag = False

            if line[0] != '#':
                for char in line:
                    if char in deliminater:
                        author_flag = True
                    elif not author_flag:
                        title += char
                    else:
                        author += char

            if title.strip() and author.strip():
                writer.writerow([id, title, author])
                id += 1
            elif line:
                print(line)

    # Mode 4, stripped-link-description
        # strip all markdown styling
        # format compatible with links
        # output id, link, description
        # link can be null
    elif mode == 4:
        writer.writerow(["id", "link", "description"])
        link_pattern = re.compile(r'https?://[^\s)]+')

        for line in infile:
            line = line.strip()

            if not line:
                continue

            match = link_pattern.search(line)

            if match:
                link = match.group(0)
                if '(' in link:
                    link += ')'
            else:
                link = ""

            description = line
            description = re.sub(r'\[(.*?)\]\(https?://[^\s)]+\)', r'\1', description)
            description = description.replace(link, "")
            for char in ['>', '-', '–', '*', '<', '>', '[', ']', ';']:
                description = description.replace(char, '')

            description = re.sub(r'\(\s*\)', '', description)
            description = ' '.join(description.split())
            if description.strip():
                writer.writerow([id, link, description])
                id += 1
            elif line:
                print(line)

    # Mode 5, checkmark-description
        # strip all markdown styling
        # return the checkmark status [true, false] and the description
    elif mode == 5:
        writer.writerow(["id", "completed", "description"])

        for line in infile:
            check = "false"
            description = ""

            if line[0] == '#':
                continue

            if "[x]" in line:
                check = "true"

            description = line[5:]

            if description:
                writer.writerow([id, check, description])
                id += 1
            elif line:
                print(line)

print("Successfully exported ", id, " lines to ", output_file_path, " in mode ", mode, ".")
















