import copy
import re

import nltk
from konlpy.tag import Mecab
from krwordrank.word import KRWordRank

from SmiToText import __ROOT_DIR__


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

    return extract_noun, extract_noun_score


def cleaning_multi_noun(multi_noun_list=[], cleaning_count=2):
    multi_noun_list = copy.deepcopy(multi_noun_list)
    cleaning_multi_noun_result = []
    cleaning_multi_noun_result_score = {}

    cleaning_multi_noun_result_score
    for multi_noun in multi_noun_list:
        isOnlyEngNum = re.sub('[a-zA-Z0-9가-힣]', '', multi_noun)
        # print(multi_noun)
        if len(isOnlyEngNum.strip()) == 0:
            multi_noun = re.sub("[\s]+", " ", multi_noun)
            cleaning_multi_noun_result.append(multi_noun)
            if in_dict(cleaning_multi_noun_result_score, multi_noun) == False:
                cleaning_multi_noun_result_score[multi_noun] = 0.75
            else:
                cleaning_multi_noun_result_score[multi_noun] += 0.75
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
                if in_dict(cleaning_multi_noun_result_score, candidate_multi_noun) == False:
                    cleaning_multi_noun_result_score[candidate_multi_noun] = 0.75
                else:
                    cleaning_multi_noun_result_score[candidate_multi_noun] += 0.75

    return cleaning_multi_noun_result, cleaning_multi_noun_result_score


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
                word_cleansing = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》\^\)\(]', '', word)
                if len(word_cleansing) == len(word):
                    krword_rank_noun.append(word)
                    krword_rank_noun_score[word] = r
        return krword_rank_noun, krword_rank_noun_score
    except:
        krword_rank_noun = []
        krword_rank_noun_score = {}
        return krword_rank_noun, krword_rank_noun_score


def levenshtein(s1, s2, debug=False):
    if len(s1) < len(s2):
        return levenshtein(s2, s1, debug)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))

        if debug:
            print(current_row[1:])

        previous_row = current_row

    return previous_row[-1]


test_data = open(__ROOT_DIR__ + "/data/article-text.txt", mode='r', encoding='utf-8')

lines = test_data.readlines()


def check_stopword(multi_noun, multi_noun_score, stop_word=[]):
    if len(stop_word) == 0 or stop_word == None:
        stop_word = ['가령', '각각', '각자', '각종', '같다', '같이', '거니와', '거바', '거의', '것들', '게다가', '게우다', '겨우', '결국', '경우', '고로',
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
                     '혹시', '혹은', '혼자', '훨씬', '휘익', '힘입어']

    check_multi_noun = []
    check_multi_noun_score = {}

    for noun in multi_noun:
        if len(set(stop_word).difference(noun.split())) == len(stop_word) \
                and not str(noun).endswith('니다') \
                and not str(noun).endswith('이다'):
            check_multi_noun.append(noun)
            check_multi_noun_score[noun] = multi_noun_score[noun]

    return check_multi_noun, check_multi_noun_score

if __name__ == '__main__':
    for line in lines:
        line = line.strip()
        multi_noun = []
        multi_noun_score = {}
        krword_rank_noun = []
        krword_rank_noun_score = {}
        krword_rank_once_noun = []
        krword_rank_once_noun_score = {}

        if line:
            sentence_list = line.split(".")
            # print(sentence_list)

            for sentence in sentence_list:
                sentence = sentence.strip()
                if sentence:
                    first_multi_noun_list, _ = expect_multi_noun_text(sentence)
                    second_multi_noun_list, second_multi_noun_list_score = cleaning_multi_noun(first_multi_noun_list,
                                                                                               cleaning_count=2)
                    print("origin : ", sentence)
                    print("first : ", first_multi_noun_list)
                    print("second : ", second_multi_noun_list)
                    print("second score : ", second_multi_noun_list_score)
                    multi_noun = second_multi_noun_list
                    multi_noun_score = second_multi_noun_list_score
                    print("multi noun scpre : ", multi_noun_score)

            krword_rank_noun, krword_rank_noun_score = krwordrank_noun(sentence_list=sentence_list, min_count=3)
            krword_rank_noun, krword_rank_noun_score = cleaning_multi_noun(krword_rank_noun,
                                                                                       cleaning_count=1)
            krword_rank_once_noun, krword_rank_once_noun_score = krwordrank_noun(sentence_list=sentence_list, min_count=2)
            krword_rank_once_noun, krword_rank_once_noun_score = cleaning_multi_noun(krword_rank_once_noun,
                                                                                       cleaning_count=1)
        print(multi_noun, multi_noun_score)
        print(krword_rank_noun, krword_rank_noun_score)
        print(krword_rank_once_noun, krword_rank_once_noun_score)

        multi_noun.extend(krword_rank_noun)
        multi_noun_score.update(krword_rank_noun_score)
        # multi_noun = multi_noun.extend(krword_rank_once_noun)
        print(multi_noun, multi_noun_score)

        print("-" * 100)
        multi_noun, multi_noun_score = check_stopword(multi_noun, multi_noun_score)
        krword_rank_noun, krword_rank_noun_score = check_stopword(krword_rank_noun, krword_rank_noun_score)
        krword_rank_once_noun, krword_rank_once_noun_score = check_stopword(krword_rank_once_noun,
                                                                            krword_rank_once_noun_score)

        print(multi_noun, multi_noun_score)
        print(krword_rank_noun, krword_rank_noun_score)
        print(krword_rank_once_noun, krword_rank_once_noun_score)
