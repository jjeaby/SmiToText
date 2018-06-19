import re
import sys
from optparse import OptionParser

from langdetect import detect

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-i", "--input", help="input file setting", metavar="input file")
    parser.add_option("-o", "--output", help="output file setting", metavar="output file")
    (options, args) = parser.parse_args()
    input_file_path = options.input
    output_file_path = options.output
    if not input_file_path or not output_file_path:
        parser.print_help()
        sys.exit(1)

    input_filename = input_file_path
    output_filename = output_file_path
    read_file = open(input_filename, mode='r', encoding='utf-8')
    write_file = open(output_filename, mode='w', encoding='utf-8')

    linenum = 0
    temp_line = ""
    for line in read_file.readlines():
        line = line.strip()
        line = line.strip('\t')
        line = line.strip('<KW>')
        linenum += 1


        if len(line) > 0:
            try:
                if not line.endswith("."):
                    temp_line = temp_line + " " + line
                else:
                    temp_line = temp_line + " " + line

                    rm_line_count = 0

                    rm_line_count = rm_line_count + len(re.findall(r"<KW>", temp_line))
                    rm_line_count = rm_line_count + len(re.findall(r"<h", temp_line))
                    rm_line_count = rm_line_count + len(re.findall(r">", temp_line))
                    rm_line_count = rm_line_count + len(re.findall(r"@", temp_line))
                    rm_line_count = rm_line_count + len(re.findall(r"=", temp_line))
                    rm_line_count = rm_line_count + len(re.findall(r"\W+기자 {0,}$", temp_line))
                    rm_line_count = rm_line_count + len(re.findall(r"\\\W+기자 {0,}$", temp_line))
                    rm_line_count = rm_line_count + len(re.findall(r"#", temp_line))

                    if rm_line_count == 0 :
                        print("SUCESS : ",  linenum, temp_line)
                        write_file.writelines(temp_line + '\n')
                        temp_line = ""
                    else :
                        temp_line = ""
                    temp_line=""
            except Exception as e:
                print("ERROR : ", linenum, line, str(e))
                continue

    # for idx, ko in enumerate(ko_line):
    #     print(ko, en_line[idx])
    write_file.close()
    read_file.close()
