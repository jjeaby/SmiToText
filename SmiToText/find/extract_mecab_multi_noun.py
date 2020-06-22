import argparse
import copy
import itertools
import os
import re
from datetime import date

import nltk
from konlpy.tag import Mecab
from krwordrank.word import KRWordRank

from SmiToText.tokenizer.nltk import nltkSentTokenizer
from SmiToText.util.util import Util

all_stop_word = ['가령', '각각', '각자', '각종', '같다', '같이', '거니와', '거바', '거의', '것들', '게다가', '게우다', '겨우', '결국', '경우', '고로',
                 '곧바로', '과연', '관하여', '관한', '그동안', '그들', '그때', '그래', '그래도', '그래서', '그러나', '그러니', '그러면', '그런데', '그런즉',
                 '그럼', '그렇지', '그리고', '그위에', '그저', '근거로', '기대여', '기타', '까악', '까지', '까지도', '꽈당', '끙끙', '끼익', '남들',
                 '남짓', '너희', '너희들', '놀라다', '누구', '니다', '다른', '다만', '다소', '다수', '다음', '다음에', '단지', '답다', '당신', '당장',
                 '대하면', '대하여', '대한', '대해서', '댕그', '더구나', '더라도', '더불어', '더욱더', '동시에', '동안', '된이상', '둥둥', '뒤따라',
                 '뒤이어', '든간에', '등등', '딩동', '따라', '따라서', '따위', '때론', '때문', '때문에', '또한', '뚝뚝', '로부터', '로써', '마저',
                 '마저도', '마치', '만약', '만약에', '만일', '만큼', '매번', '몇몇', '모두', '모든', '무렵', '무슨', '무엇', '물론', '바로', '반대로',
                 '반드시', '버금', '보다더', '보드득', '본대로', '봐라', '부터', '붕붕', '비교적', '비로소', '비록', '비하면', '뿐이다', '삐걱', '설령',
                 '설마', '설사', '소생', '소인', '습니까', '습니다', '시각', '시간', '시초에', '시키다', '실로', '심지어', '아니', '아니면', '아래윗',
                 '아무도', '아야', '아울러', '아이', '아이고', '아이구', '아이야', '아이쿠', '아하', '알았어', '앞에서', '앞의것', '약간', '양자', '어느',
                 '어느것', '어느곳', '어느때', '어느쪽', '어느해', '어디', '어때', '어떠한', '어떤', '어떤것', '어떻게', '어떻해', '어이', '어째서',
                 '어쨋든', '어찌', '언제', '언젠가', '얼마', '얼마간', '얼마나', '얼마큼', '없는', '엉엉', '에게', '에서', '여기', '여러분', '여보시오',
                 '여부', '여전히', '여차', '연관되다', '연이서', '영차', '옆사람', '예컨대', '예하면', '오로지', '오르다', '오자마자', '오직', '오호',
                 '오히려', '와르르', '와아', '왜냐하면', '외에도', '요만큼', '요만한걸', '요컨대', '우르르', '우리', '우리들', '우선', '운운', '위하여',
                 '위해서', '윙윙', '으로', '으로서', '으로써', '응당', '의거하여', '의지하여', '의해', '의해되다', '의해서', '이 되다', '이 밖에', '이 외에',
                 '이것', '이곳', '이다', '이때', '이라면', '이래', '이러한', '이런', '이렇구나', '이리하여', '이만큼', '이번', '이봐', '이상', '이어서',
                 '이었다', '이외에도', '이용하여', '이젠', '이지만', '이쪽', '이후', '인젠', '일것이다', '일단', '일때', '일지라도', '입각하여', '입장에서',
                 '잇따라', '있다', '자기', '자기집', '자마자', '자신', '잠깐', '잠시', '저것', '저것만큼', '저기', '저쪽', '저희', '전부', '전자',
                 '전후', '제각기', '제외하고', '조금', '조차', '조차도', '졸졸', '좋아', '좍좍', '주룩주룩', '중에서', '중의하나', '즈음하여', '즉시',
                 '지든지', '지만', '지말고', '진짜로', '쪽으로', '차라리', '참나', '첫번째로', '총적으로', '최근', '콸콸', '쾅쾅', '타다', '타인', '탕탕',
                 '토하다', '통하여', '통해', '틈타', '펄렁', '하게하다', '하겠는가', '하구나', '하기에', '하나', '하느니', '하는것도', '하는바', '하더라도',
                 '하도다', '하든지', '하마터면', '하면된다', '하면서', '하물며', '하여금', '하여야', '하자마자', '하지마', '하지마라', '하지만', '하하',
                 '한 후', '한다면', '한데', '한마디', '한편', '한항목', '할때', '할만하다', '할망정', '할뿐', '할수있다', '할수있어', '할줄알다', '할지라도',
                 '할지언정', '함께', '해도된다', '해도좋다', '해봐요', '해야한다', '해요', '했어요', '향하다', '향하여', '향해서', '허걱', '허허', '헉헉',
                 '혹시', '혹은', '혼자', '훨씬', '휘익', '힘입어', '네이버 메인', '말했다', '못했다는', '대해', '현산', '위한', '충분히', '\\n', '것도',
                 '했다', '있는', '제공받지', '없다', '이날오전', '이날만기', '배포금지', '함수추가', '무단전재', '본문내용', 'news', '머니투데이', '네이버연합뉴스',
                 '구독클릭', '부여스마트', '공감언론', '소재나이스'
                 ]


def in_dict(dict_data, key):
    try:
        if dict_data[key] >= 0:
            return True
    except:
        return False


def expect_multi_noun_text(sentence):
    # Define a chunk grammar, or chunking rules, then chunk

    grammar = """
    복합명사1: {<SL>*<S.*>}
    복합명사1: {<SN>*<S.*>}

    복합명사1: {<NNG>*<NNG>?}
    복합명사2: {<SN><NN.*>*<X.*>?}
    복합명사3: {<NNG>*<X.*>?}
    복합명사4: {<N.*>*<Suffix>?}   
 

    동사구: {<NP\+VCP\+EF>}
    동사구: {<NP><VCP\+EF>}
    형용사: {<MA.*>*}
    """
    mecab = Mecab()

    postagged_sentence = mecab.pos(sentence)
    nltk_rexp_parser = nltk.RegexpParser(grammar)
    chunks_sentence = nltk_rexp_parser.parse(postagged_sentence)

    extract_noun = []
    extract_noun_score = {}
    for subtree in chunks_sentence.subtrees():
        if subtree.label().startswith('복합명사'):
            if len(' '.join((e[0] for e in list(subtree)))) > 1:
                noun = ' '.join((e[0] for e in list(subtree)))
                if re.search(r"\s", noun):
                    extract_noun.append(noun)
                    # extract_noun_score[noun] = 0.75
                    if in_dict(extract_noun_score, noun) == False:
                        extract_noun_score[noun] = 0.75
                    else:
                        extract_noun_score[noun] += 0.75

    return sorted_dict(extract_noun_score)


def cleaning_multi_noun(multi_noun_list=[], multi_noun_list_score=[], cleaning_count=2):
    multi_noun_list = copy.deepcopy(multi_noun_list)
    cleaning_multi_noun_result = []
    cleaning_multi_noun_result_score = {}

    cleaning_multi_noun_result_score
    for multi_noun in multi_noun_list:
        isOnlyEngNum = re.sub('[a-zA-Z0-9]', '', multi_noun)
        # print(multi_noun)
        if len(isOnlyEngNum.strip()) == 0:
            multi_noun = re.sub("[\s]+", " ", multi_noun)
            cleaning_multi_noun_result.append(multi_noun)
            if len(multi_noun_list_score) == 0:
                if in_dict(cleaning_multi_noun_result_score, multi_noun) == False:
                    cleaning_multi_noun_result_score[multi_noun] = 0.75
                else:
                    cleaning_multi_noun_result_score[multi_noun] += 0.75
                continue
            else:
                if in_dict(cleaning_multi_noun_result_score, multi_noun) == False:
                    cleaning_multi_noun_result_score[multi_noun] = multi_noun_list_score[multi_noun]
                else:
                    cleaning_multi_noun_result_score[multi_noun] += multi_noun_list_score[multi_noun]
                continue

        multi_noun_space_splitter = multi_noun.split(" ")
        if len(multi_noun_space_splitter) >= 2:
            candidate_multi_noun = ""
            for index in range(cleaning_count):
                if len(multi_noun_space_splitter[-1]) == 1:
                    candidate_multi_noun = ' '.join(multi_noun_space_splitter[:-1])
                else:
                    candidate_multi_noun = ' '.join(multi_noun_space_splitter)

            for index in range(cleaning_count):
                multi_noun_space_splitter = candidate_multi_noun.split(" ")
                if len(multi_noun_space_splitter[0]) == 1:
                    candidate_multi_noun = ' '.join(multi_noun_space_splitter[1:])
                else:
                    candidate_multi_noun = ' '.join(multi_noun_space_splitter)
                candidate_multi_noun = re.sub("[\s]+", " ", candidate_multi_noun)

            if re.search(r"\s", candidate_multi_noun):
                cleaning_multi_noun_result.append(candidate_multi_noun)
                # cleaning_multi_noun_result_score[candidate_multi_noun] = 0.75

                if len(multi_noun_list_score) == 0:
                    if in_dict(cleaning_multi_noun_result_score, candidate_multi_noun) == False:
                        cleaning_multi_noun_result_score[candidate_multi_noun] = 0.75
                    else:
                        cleaning_multi_noun_result_score[candidate_multi_noun] += 0.75
                else:
                    if in_dict(cleaning_multi_noun_result_score, candidate_multi_noun) == False:
                        cleaning_multi_noun_result_score[candidate_multi_noun] = multi_noun_list_score[
                            candidate_multi_noun]
                    else:
                        cleaning_multi_noun_result_score[candidate_multi_noun] += multi_noun_list_score[
                            candidate_multi_noun]

    return sorted_dict(cleaning_multi_noun_result_score)


def krwordrank_noun(sentence_list=[], min_count=5, max_length=10, beta=0.85, max_iter=10, verbose=False):
    krword_rank_noun = []
    krword_rank_noun_score = {}

    wordrank_extractor = KRWordRank(min_count, max_length, verbose)
    try:
        keywords, rank, graph = wordrank_extractor.extract(sentence_list, beta, max_iter)
        for word, r in sorted(keywords.items(), key=lambda x: x[1], reverse=True)[:len(keywords)]:
            # print(r, word)
            word = re.sub("[\s]+", " ", word)
            if len(word) > 1:
                word_cleansing = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!”』\\‘|\(\)\[\]\<\>`\'…》\^\)\(]', '', word)
                if len(word_cleansing) == len(word):
                    krword_rank_noun.append(word)
                    krword_rank_noun_score[word] = r
        return sorted_dict(krword_rank_noun_score)
    except:
        krword_rank_noun = []
        krword_rank_noun_score = {}
        return sorted_dict(krword_rank_noun_score)


def remove_stopword(multi_noun, multi_noun_score, stop_word=[]):
    if len(stop_word) == 0 or stop_word == None:
        stop_word = all_stop_word

    check_multi_noun = []
    check_multi_noun_score = {}

    for noun in multi_noun:
        if noun not in stop_word \
                and not Util().is_int(noun) \
                and not str(noun).endswith('니다') \
                and not str(noun).endswith('이다'):
            check_multi_noun.append(noun)
            check_multi_noun_score[noun] = multi_noun_score[noun]

    return sorted_dict(check_multi_noun_score)


def check_stopword(multi_noun, multi_noun_score, stop_word=[]):
    if len(stop_word) == 0 or stop_word == None:
        stop_word = all_stop_word
    check_multi_noun = []
    check_multi_noun_score = {}

    for noun in multi_noun:
        # print(noun.replace(' ', ''))
        # print(len(
        #         set(stop_word).difference(noun.replace(' ', ''))) == len(stop_word))

        if len(set(stop_word).difference(noun.split())) == len(stop_word) \
                and len(set(stop_word).difference([noun.replace(' ', '')])) == len(stop_word) \
                and not Util().is_int(noun) \
                and not str(noun).endswith('니다') \
                and not str(noun).endswith('이다'):
            check_multi_noun.append(noun)
            check_multi_noun_score[noun] = multi_noun_score[noun]

    return sorted_dict(check_multi_noun_score)


def remove_last_one_char(multi_noun, multi_noun_score):
    check_multi_noun = []
    check_multi_noun_score = {}

    for noun in multi_noun:
        temp_noun = noun.split(' ')
        if len(temp_noun[0]) == 1:
            check_multi_noun.append(' '.join(temp_noun[1:]))
            check_multi_noun_score[str(' '.join(temp_noun[1:]))] = multi_noun_score[noun]
        elif len(temp_noun[-1]) == 1:
            check_multi_noun.append(' '.join(temp_noun[:-1]))
            check_multi_noun_score[str(' '.join(temp_noun[:-1]))] = multi_noun_score[noun]
        else:
            check_multi_noun.append(noun)
            check_multi_noun_score[noun] = multi_noun_score[noun]

    return sorted_dict(check_multi_noun_score)


def sorted_dict(multi_noun_score):
    ret_check_multi_noun = []
    ret_check_multi_noun_score = {}
    for noun, r in sorted(multi_noun_score.items(), key=lambda x: x[1], reverse=True)[
                   :len(multi_noun_score)]:
        # print(r, word)
        if r > 0:
            ret_check_multi_noun.append(noun)
            ret_check_multi_noun_score[noun] = r

    return ret_check_multi_noun, ret_check_multi_noun_score


def multi_noun_score_add(multi_noun_score, krword_rank_once_noun_score):
    tem_add_noun_score = {}
    for multi_noun in multi_noun_score.keys():
        temp_multi_noun = re.sub("[\s]+", " ", multi_noun)
        for krword_noun in krword_rank_once_noun_score.keys():
            temp_krword_noun = re.sub("[\s]+", " ", krword_noun)

            if len(temp_multi_noun) > len(temp_krword_noun):
                temp_multi_noun_eng_check = re.sub('[ㄱ-힗]', '', temp_multi_noun)
                if temp_multi_noun_eng_check.strip().lower() == temp_krword_noun.strip().lower():
                    tem_add_noun_score[krword_noun] = krword_rank_once_noun_score[krword_noun] + multi_noun_score[
                        multi_noun]
                    multi_noun_score[multi_noun] = 0
                elif len(temp_multi_noun.replace(temp_krword_noun, "")) < len(temp_multi_noun):
                    multi_noun_score[multi_noun] += krword_rank_once_noun_score[krword_noun]
            else:
                if len(temp_krword_noun.replace(temp_multi_noun, "")) < len(temp_krword_noun):
                    multi_noun_score[multi_noun] += krword_rank_once_noun_score[krword_noun]
    multi_noun_score.update(tem_add_noun_score)
    return sorted_dict(multi_noun_score)


def text_in_mult_noun_finder(multi_noun, multi_noun_score, text):
    text_in_multi_noun = []
    text_in_multi_noun_score = {}
    for noun in multi_noun:
        max_try = len(noun.split(' '))
        for try_count_1 in range(0, max_try):
            try_count_1_text = ' '.join(noun.split(' ')[:try_count_1])
            try_count_2_text = ' '.join(noun.split(' ')[try_count_1:])
            for try_count_2 in range(0, (max_try - try_count_1)):

                find_multi_noun = try_count_1_text + str(try_count_2_text).replace(" ", "", try_count_2)
                if text.find(find_multi_noun) >= 0:
                    text_in_multi_noun.append(find_multi_noun)
                    text_in_multi_noun_score[find_multi_noun] = multi_noun_score[noun]

    text_in_noun_result = copy.deepcopy(text_in_multi_noun)
    text_in_noun_result_score = copy.deepcopy(text_in_multi_noun_score)

    for noun in text_in_multi_noun:
        start_position = text.find(noun)
        if start_position > 0 and text[start_position - 1] != ' ':
            print(text[start_position - 1])
            prefix_char = text[start_position - 1]
            if re.sub('[가-힣]', '', prefix_char) == '':
                text_in_noun_result_score[prefix_char + noun] = text_in_multi_noun_score[noun]
                text_in_noun_result_score[noun] = 0
            else:
                text_in_noun_result_score[noun] = text_in_multi_noun_score[noun]
        else:
            text_in_noun_result_score[noun] = text_in_multi_noun_score[noun]

    text_in_multi_noun_result, text_in_multi_noun_result_score = sorted_dict(text_in_noun_result_score)

    for noun in text_in_multi_noun_result:
        if noun.find(' ') < 0:
            remove_flag = False
            for multi_noun in text_in_multi_noun_result:
                if len(noun) < len(multi_noun) and multi_noun.find(noun) >= 0:
                    # text_in_multi_noun_result(noun)
                    # print(multi_noun)
                    # print(noun)
                    text_in_multi_noun_result_score[multi_noun] += text_in_noun_result_score[noun]
                    remove_flag = True
            if remove_flag:
                text_in_multi_noun_result_score[noun] = 0

    return sorted_dict(text_in_multi_noun_result_score)


def extract_mecab_multi_noun(text, item_counter=0):
    text = text.strip()

    multi_noun = []
    multi_noun_score = {}
    krword_rank_noun = []
    krword_rank_noun_score = {}
    krword_rank_once_noun = []
    krword_rank_once_noun_score = {}

    if text:
        sentence_list = nltkSentTokenizer(text)

        # print(sentence_list)

        for sentence in sentence_list:
            sentence = sentence.strip()
            if sentence:
                first_multi_noun_list, _ = expect_multi_noun_text(sentence)
                second_multi_noun_list, second_multi_noun_list_score = cleaning_multi_noun(first_multi_noun_list,
                                                                                           cleaning_count=2)
                # second_multi_noun_list, second_multi_noun_list_score = check_stopword(second_multi_noun_list, second_multi_noun_list_score)

                # print("origin : ", sentence)
                # print(second_multi_noun_list, second_multi_noun_list_score)

                multi_noun.extend(second_multi_noun_list)
                multi_noun_score.update(second_multi_noun_list_score)

        krword_rank_noun, krword_rank_noun_score = krwordrank_noun(sentence_list=sentence_list, min_count=5)
        krword_rank_once_noun, krword_rank_once_noun_score = krwordrank_noun(sentence_list=sentence_list,
                                                                             min_count=2)

    # print(multi_noun, multi_noun_score)
    # print(krword_rank_noun, krword_rank_noun_score)
    # print(krword_rank_once_noun, krword_rank_once_noun_score)

    multi_noun.extend(krword_rank_noun)
    multi_noun_score.update(krword_rank_noun_score)
    # multi_noun = multi_noun.extend(krword_rank_once_noun)
    # print(multi_noun, multi_noun_score)

    # print("-" * 100)
    multi_noun, multi_noun_score = check_stopword(multi_noun, multi_noun_score)
    # krword_rank_noun, krword_rank_noun_score = check_stopword(krword_rank_noun, krword_rank_noun_score)
    krword_rank_once_noun, krword_rank_once_noun_score = check_stopword(krword_rank_once_noun,
                                                                        krword_rank_once_noun_score)

    # print(multi_noun, multi_noun_score)
    multi_noun, multi_noun_score = remove_last_one_char(multi_noun, multi_noun_score)
    krword_rank_noun, krword_rank_noun_score = remove_last_one_char(krword_rank_noun, krword_rank_noun_score)
    krword_rank_noun, krword_rank_noun_score = remove_last_one_char(krword_rank_noun, krword_rank_noun_score)

    # print(multi_noun, multi_noun_score)
    # print(krword_rank_noun, krword_rank_noun_score)
    # print(krword_rank_once_noun, krword_rank_once_noun_score)

    multi_noun, multi_noun_score = check_stopword(multi_noun, multi_noun_score)

    # print("0" * 100)
    # print(multi_noun_score)
    multi_noun, multi_noun_score = multi_noun_score_add(multi_noun_score,
                                                        krword_rank_once_noun_score)

    # print("0" * 100)
    # print(multi_noun, multi_noun_score)
    multi_noun, multi_noun_score = remove_stopword(multi_noun, multi_noun_score)

    return_multi_noun, return_multi_noun_score = text_in_mult_noun_finder(multi_noun, multi_noun_score, text)

    if item_counter == 0:
        return return_multi_noun, return_multi_noun_score
    else:
        return return_multi_noun[:item_counter], dict(itertools.islice(return_multi_noun_score.items(), item_counter))


# if __name__ == '__main__':
#
#     test_data = open(__ROOT_DIR__ + "/data/article-text.txt", mode='r', encoding='utf-8')
#
#     lines = test_data.readlines()
#
#     for line in lines:
#         multi_noun, multi_noun_score = extract_mecab_multi_noun(line, item_counter=10)
#         print(multi_noun, multi_noun_score)
#

def extract_file_multi_noun(input, output, item_counter=0):
    input_file = open(input, mode='r', encoding='utf-8')
    open(output, mode='w', encoding='utf-8')
    output_file = open(output, mode='a', encoding='utf-8')
    line_number = 1
    while (True):
        line = input_file.readline()
        if not line:
            break;

        line = line.strip()

        for line_array in line.split("\n"):
            line_array = line_array.strip()

            line_array_multi_noun_score = {}
            multi_noun_list, multi_noun_list_score = extract_mecab_multi_noun(line_array, item_counter=item_counter)

            if len(multi_noun_list):
                for index, word in enumerate(multi_noun_list):
                    if Util().check_email(word):
                        continue
                    else:
                        add_flag = True
                        for char in word:
                            if char in ["'", "`", ",", "'", "\"", "|", "!", "@", "#", "$", "%", "^", "&", "*", "(",
                                        ")",
                                        "-", "_", "=", "+", "<", ">", ".", ";", ":",
                                        "ㄱ", "ㄴ", "ㄲ", "ㅂ", "ㅃ", "ㅈ", "ㅉ", "ㄷ", "ㄸ", "ㄱ", "ㅁ", "ㅇ", "ㄹ", "ㅎ", "ㅅ",
                                        "ㅆ",
                                        "ㅍ", "ㅊ", "ㅌ", "ㅋ", "ㅛ", "ㅕ", "ㅑ", "ㅐ", "ㅔ", "ㅗ", "ㅓ", "ㅏ", "ㅣ", "ㅠ", "ㅜ",
                                        "ㅡ", " "]:
                                add_flag = False

                        if word == '기자' or word == str(date.today().day) + '일':
                            add_flag = False

                        if add_flag:
                            word_score = {word: multi_noun_list_score[word]}
                            line_array_multi_noun_score.update(word_score)
                        # print(line_number, word)

        _, line_array_multi_noun_score_sorted = sorted_dict(line_array_multi_noun_score)
        output_file.write(str(line_array_multi_noun_score_sorted) + os.linesep)
        print(line_number, line_array_multi_noun_score)
        line_number += 1


def extract_multi_noun(text, item_counter=0):
    line = text.strip()
    line_array_multi_noun_score = {}
    line_array = line.strip()

    multi_noun_list, multi_noun_list_score = extract_mecab_multi_noun(line_array, item_counter=item_counter)

    if len(multi_noun_list):
        for index, word in enumerate(multi_noun_list):
            if Util().check_email(word):
                continue
            else:
                add_flag = True
                for char in word:
                    if char in ["'", "`", ",", "'", "\"", "|", "!", "@", "#", "$", "%", "^", "&", "*", "(",
                                ")",
                                "-", "_", "=", "+", "<", ">", ".", ";", ":",
                                "ㄱ", "ㄴ", "ㄲ", "ㅂ", "ㅃ", "ㅈ", "ㅉ", "ㄷ", "ㄸ", "ㄱ", "ㅁ", "ㅇ", "ㄹ", "ㅎ", "ㅅ",
                                "ㅆ",
                                "ㅍ", "ㅊ", "ㅌ", "ㅋ", "ㅛ", "ㅕ", "ㅑ", "ㅐ", "ㅔ", "ㅗ", "ㅓ", "ㅏ", "ㅣ", "ㅠ", "ㅜ",
                                "ㅡ", " "]:
                        add_flag = False

                if word == '기자' or word == str(date.today().day) + '일':
                    add_flag = False

                if add_flag:
                    word_score = {word: multi_noun_list_score[word]}
                    line_array_multi_noun_score.update(word_score)
                # print(line_number, word)
    return sorted_dict(line_array_multi_noun_score)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Extract File Noun word")
    parser.add_argument('--input', type=str, required=True, default='', help='Input File')
    parser.add_argument('--output', type=str, required=True, default='', help='Output File')
    parser.add_argument('--count', type=int, required=False, default=0, help='Item Count Number')
    args = parser.parse_args()

    if not args.input:
        print("input file is invalid!")
        exit(1)

    if not args.output:
        print("output file is invalid!")
        exit(1)

    input = str(args.input)
    output = str(args.output)
    item_counter = args.count

    extract_file_multi_noun(input, output, item_counter=item_counter)

    # _, a = extract_multi_noun(
    #     "3억원 초과 아파트 구입시 전세대출 금지...전입의무 6개월 ∥ \n \n \n\n\n\n// flash 오류를 우회하기 위한 함수 추가\nfunction _flash_removeCallback() {}\n\n \n [파이낸셜뉴스] 투기·투기과열 지구 내 3억원 초과 아파트를 신규 구입하는 경우 전세대출을 받을 수 없다. 주택구입을 위해 주택담보대출을 받은 후 전입의무는 6개월로 단축된다.정부가 17일 관계부처 합동으로 발표한 \'주택시장 안정을 위한 관리방안\'에 따라 이 같은 내용으로 주택 대출 규제가 강화된다.우선 투기지역·투기과열지구 내 시가 3억원 초과 아파트를 신규 구입하는 경우 전세대출 보증이 제한된다. 전세대출을 받은 후 투기지역·투기과열지구 내 3억원 초과 아파트를 구입하는 경우 전세대출은 즉시 회수해야한다. 규제시행 전 전세대출 차주가 규제시행 후 투기·투기과열지구내 3억원 초과 아파트를 신규 구입했다면 대출 연장이 제한된다. 기존 전세대출 만기까지만 인정된다. 보증기관 내규 개정 후 시행할 예정이며 생활안정자금 목적 주택담보대출은 적용되지 않는다. 또 주택도시보증공사(HUG) 전세대출 보증한도는 1주택자 대상 2억원으로 축소된다.전입 의무도 강화된다. 투기지역, 투기과열지구, 조정대상지역 등 규제지역 내 주택 구입을 위해 주택담보대출을 받는 경우 주택가격과 관계없이 6개월내 전입 의무를 부과한다. 중도금·이주비 대출의 경우 신규 주택 소유권 이전 등기일로부터 6개월이 적용된다.이어 주택구입을 위해 보금자리론을 받는 경우 3개월 내 전입 및 1년 이상 실거주 유지 의무를 부과하고, 의무 위반 시 대출금을 회수한다. 7월 1일 이후 보금자리론 신청 분부터 적용된다. 주택금융공사는 대출실행 후 일정기간이 지나면 전입여부를 조사할 수 있으며, 약정을 위반해 전출한 것이 확인된 경우 기한이익 상실 조치를 시행한다.규제지역과 비규제지역 모두 주택 매매·임대 사업자에 대한 주담대는 금지한다. 법인과 개인이 모두 포함되며 주택구입용 자금인 시설자금뿐만 아니라, 주택수리비 등 운전자금용으로도 주담대를 받을 수 없다. 행정지도가 시행되는 7월 1일 이후 신규대출 신청 분부터 적용된다.jiany@fnnews.com 연지안 기자▶ 헉! 소리나는 스!토리 뉴스 [헉스]▶ \'아는 척\'하고 싶은 당신을 위한 [두유노우]※ 저작권자 ⓒ 파이낸셜뉴스. 무단 전재-재배포 금지\n \n")
    # print('---')
    # print(a)
