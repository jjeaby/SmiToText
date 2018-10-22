import argparse
import os

from SmiToText.util.util import Util

util = Util()


def expect_noun_text(text):
    word_list = []

    replace_char_list = ['[', ']', '\'', '\"', ')', '(', '「', '」', '-', '」', '「', '’', ':', '/', '”', '“', '?', '!',
                         '~', '-', ',', 'ㆍ', '◇', '△', '〃', '〈', '〉',
                         '·',
                         '+',
                         '”', '○', '…']

    check_word_end = [ ',', '.', ':', ';', '!', '?', '\"', '\'']

    end_char_exclude_list = ['나오는', '나오다', '내고는', '내기', '내는', '넘기', '넘는', '넘다',
                             '넘을', '다고', '다는', '다를',
                             '다와', '되는', '되었기', '되었다', '되었을', '되었', '드는', '들리다에', '들리고', '들리는', '들어지', '들', '때로는', '또는',
                             '뛰어드', '뛰어드는', '라는',
                             '랬냐고', '랬냐는', '려고', '려는', '르는', '리는데', '리려는', '리고', '리는', '리다', '리려', '만은', '만을', '만이',
                             '만큼', '말까', '받고', '보이기',
                             '보이는', '보이다', '본격적', '봤', '쉬움', '시키고', '시키는', '시키다', '시키러', '아치고', '아치는', '아치다', '어지',
                             '어지는',

                             '있음을', '였음과', '였음을', '였음', '있음', '있음에도', '였음에도',
                             '있기를', '였기를', '있기에,' '있기', '였기에', '였기',
                             '키우기', '키우는', '키우고',
                             '비추면', '비추는', '비추어', '비추어볼',

                             '오기만', '오기', '오는데', '오는', '오는', '오다', '으로는', '으로',
                             '이냐', '이',
                             '이제는', '있고', '있는', '있다', '있을', '있', '잡았고', '잡았기', '잡았기', '잡았는', '잡았다', '잡았을', '잡았'  '주기는',
                             '주기로', '주기를', '주고', '주기',
                             '주는', '주다', '지고는', '지고', '지기', '지는', '지는',
                             '지는데', '지는', '지다', '지를', '진다', '진다', '트리고', '트리는',
                             '트리러', '하는', '하려고는', '하려고는', '하려고', '하려고', '하려는', '함', '함을', '했느가는', '했느냐는', '했는가는',
                             '했는가를', '했는냐는',
                             '해서와', '해주기', '해주는', '해주다', '해서는', '해서를', '했음을', '했기에', '했다', '했을', '했음', '해서', '했',

                             '느냐는',
                             '내리쬐는']

    start_char_exclue_list = [
        '만들어', '있음', '였음', '게다가', '건내받은', '이후', '이후에', '이후에', '걸맞은', '걸맞게',
        '키우기', '키우는', '키우고', '키우다', '키우면서', '키우도록', '키우길', '키우면', '들어', '움직이',
        '만나다',
        '가져다', '가져가는', '가져온', '가져갈', '가져다가', '가져야', '가져간다', '가져야한다고', '가져다', '가져가', '가져오는', '가져왔다','가져와',
        '나아가',
        '내려받을', '내려받는', '내려받은', '내려받아', '내려받기'
        '낮추기', '낮추고', '낮추고', '낮추면', '낮추는', '낮추면서',
        '수놓은'
    ]

    end_char_include_list = [
                             '받아야', '받아', '받을', '인가요', '인지요', '인가', '인지',
                             '까지는', '까지를', '까지와', '에게는', '에는','에도', '에서는', '에서도', '에서를', '에와', '만큼은',
                             '했다는', '했다고는', '했다고', '했다가','했다', '했음에도', '했',
                             '들을', '들은',
                             '들과', '들이', '과는', '으로', '으로는', '이었다가',
                             '로는',
                                '바꾸고', '바꾸는', '바꾸지', '바꾸어가며', '바꾸기로',
                             '가는', '기는', '가', '임을', '을', '를', '은', '이었다가는', '는', '과', '와']

    true_char_list = {
        '무허가',
    }
    for word in text.split():

        if word.endswith(tuple(check_word_end)):
            word = word[:len(word) - 1]

        for item in replace_char_list:
            word = word.replace(item, ' ')

        word = word.strip()

        if not word.startswith(tuple(start_char_exclue_list)) and not word.endswith(tuple(end_char_exclude_list)) \
                and word.endswith(tuple(end_char_include_list)):

            for item in end_char_include_list:
                if word.endswith(item):
                    if not word in (tuple(true_char_list)):
                        # word = word.replace(item, '')
                        word = word.strip()
                        word = util.rreplace(word, item, '', 1)

                    word_split = word.split(' ')
                    for append_word in word_split:
                        if len(append_word) >= 2 and len(append_word) < 15:
                            # if not util.is_int(append_word) and not util.is_alpha(append_word):
                            word_list.append(append_word)
                    break;

    return word_list


def extract_file_noun(input, output):
    input_file = open(input, mode='r', encoding='utf-8')
    open(output, mode='w', encoding='utf-8')
    output_file = open(output, mode='a', encoding='utf-8')
    line_number = 1
    while (True):
        line = input_file.readline()
        if not line:
            break;

        line = line.strip()
        word_list = expect_noun_text(line)

        if len(word_list):
            print(line_number, word_list)
            for word in word_list:
                output_file.write(word + os.linesep)
        line_number += 1


if __name__ == '__main__':
    print("A")

    parser = argparse.ArgumentParser(description="Extract File Noun word")
    parser.add_argument('--input', type=str, required=True, default='', help='Input File')
    parser.add_argument('--output', type=str, required=True, default='', help='Output File')
    args = parser.parse_args()

    if not args.input:
        print("input file is invalid!")
        exit(1)

    if not args.output:
        print("output file is invalid!")
        exit(1)

    input = str(args.input)
    output = str(args.output)

    extract_file_noun(input, output)
