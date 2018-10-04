import argparse
from SmiToText.mecab.mecabDictGenerate import mecabDictGenerate

mecabDictGen = mecabDictGenerate()

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description="Mecab Dict Generator")
    parser.add_argument('--input', type=str, required=True, default='', help='Input File')
    parser.add_argument('--output', type=str, required=True, default='', help='Output File')
    args = parser.parse_args()

    if not args.input:
        print("input file is invalid!")
        exit(1)

    if not args.output:
        print("output file is invalid!")
        exit(1)

    mecabDictGen.mecab_dict_gen_from_file(str(args.input), str(args.output))
