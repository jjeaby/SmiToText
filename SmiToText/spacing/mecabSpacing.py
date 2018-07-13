# -*- coding: utf-8 -*-
from jpype import unicode

import SmiToText.tokenizer.mecab as mecab


def rreplace(s, old, new, occurrence):
    li = s.rsplit(old, occurrence)
    return new.join(li)


def mecabSpacing(sentence, DEBUG=False):
    mecabAnalizeWord = mecab.mecabAnalize(sentence)

    stich_type_1 = [
        "START"
        , "JKS", "JKC", "JKG", "JKO", "JKB", "JKV", "JKQ", "JX", "JC"
        , "ETM", "ETN+JX"
        , "EC", "EF", "EP", "EC"
        , "VV", "VV+ETM", "VV+EC", "VV+EP"
        , "VX"
        , "VCP+ETM", "VCP+EC"
        , "NNG", "NNB", "NNBC", "NNP", "NP"
        , "MM", "MAG"
        , "XSN", "XSV+ETM", "XSV+EF"
        , "XSA+ETM"
        , "XSV+EC", "XSV+EP"
        , "IC"
    ]

    split_type = [
        "SN", "SL", "SF", "SSO", "SSC", "SC", "SY"]

    josa_type = ["JKS", "JKC", "JKG", "JKO", "JKB", "JKV", "JKQ", "JX", "JC"
        , "NNBC", "NR", "VCP+EC"

                 ]
    # append_type = ["('거', 'NNB')", "('라', 'VCP+EC')", "('비', 'NNG')", "('번', 'NNBC')", "('째', 'XSN')", "('부터', 'JX')",
    #                "('는', 'JX')", "('가', 'JKS')"
    #                "('으로', 'JKB')", "('과', 'JC')", "('를', 'JKO')", "('가', 'JKS')",
    #                "('에', 'JKB')", "('의', 'JKG')", "('들', 'XSN')", "('을', 'JKO')",
    #                "('된', 'XSV+ETM')", "('스러운', 'XSA+ETM')", "('라고', 'VCP+EC')", "('한다', 'XSV+EC')",
    #                "('했', 'VV+EP')", "('다', 'EF')",
    #                "('한', 'XSA+ETM')", "('적', 'XSN')", "('인', 'VCP+ETM')", "('할', 'XSV+ETM')",
    #                "('했', 'XSV+EP')", "('습니다', 'EF')",
    #                "('에서', 'JKB')", "('하', 'XSV')", "('고', 'EC')", "('도', 'JX')",
    #                "('달', 'NNG')", "('이', 'JKS')", "('게', 'EC')" , "('되', 'VV')", "('어', 'EC')",
    #                "('보', 'VX')", "('려고요', 'EC')", "('은', 'JX')", "('어요', 'EF')",
    #                "('었', 'EP')", "('되', 'VV')", "('다고', 'EC')", "('해요', 'XSV+EF')",
    #                "('면', 'EC')", "('에', 'JKB')" ,"('가', 'JKS')"
    #                ]
    type_history = []

    mecabSpacingSentence = ""
    prevDict_word = "('', '')"

    for dict_word_idx, dict_word in enumerate(mecabAnalizeWord):

        if DEBUG == True:
            print(dict_word)
            print(type_history)

        if dict_word[1] in stich_type_1:
            # if str(dict_word) in append_type and prevDict_word[1] not in split_type and prevDict_word[1] not in josa_type:
            if prevDict_word[1] not in split_type and prevDict_word[1] not in josa_type:
                mecabSpacingSentence = rreplace(mecabSpacingSentence, " ", "", 1)
                mecabSpacingSentence = mecabSpacingSentence + str(dict_word[0]) + " "
            else:
                mecabSpacingSentence = mecabSpacingSentence + str(dict_word[0]) + " "
        elif dict_word[1] in split_type:
            mecabSpacingSentence = mecabSpacingSentence + " " + str(dict_word[0]) + " "

        else:
            mecabSpacingSentence = mecabSpacingSentence + str(dict_word[0])

        if dict_word[1] in josa_type:
            type_history.clear()
            mecabSpacingSentence = mecabSpacingSentence + " "
        else:
            type_history.append(dict_word[1])

        prevDict_word = dict_word
        mecabSpacingSentence = str(mecabSpacingSentence).replace("  ", " ")
    return mecabSpacingSentence.strip()


if __name__ == '__main__':
    # while True:
    #     try:
    #         inputText = input("\n\n문장을 입력하세요?: \n")
    #         inputText = unicode(inputText)
    #     except UnicodeDecodeError:
    #         print("다시 입력하세요\n")
    #         continue
    #
    #     if inputText == 'exit':
    #         exit(1)
    #     print(inputText)
    #     print(mecab.mecabTokenizer(inputText))
    #     print(mecabSpacing(inputText))

    # inputText = []
    # inputText.append("협정의 발효일후1 년이내에 채택하기로 한대한민국의 계획을 환영한다.")
    # inputText.append("한국어 맞춤법/문법 검사기는 부산")
    # inputText.append("한국어 맞춤법/문법 검사기는 부산대학교 인공지능연구실과 (주)나라인포테크가 공동으로 만들고 있습니다.")
    # inputText.append("SK이노베이션, GS, S-Oil, 대림산업, 현대중공업등대규모적자를 내 던")
    # inputText.append(
    #     "만약시공자가9.2조항[설계-시공준공기한 ]에 따른 요구조건들에 따라설계-시공을 준공하지못하면, 시공자는 9.6조항[설계-시공과 관련된 지연배상금]에 규정된 상세내용에 따라지연배상금을 지급하여야 한다.")
    # inputText.append("네 추천서가 정말 기대되는구나.")
    # inputText.append("처음에 판매자가 배송비 잘못 설정했을거라 생각했는데 오긴 왔네요.")
    # inputText.append("두 번째 신청부터 상기의 복수입국비자가 발급되는 것임을 확인한다.")
    # inputText.append("문화체육관광부는 두 번째 신청부터 상기의 복수입국비자가 발급되는 것임을 확인한다.")
    # inputText.append("\"나는그녀가 사랑 스러운여우 라고 생각 한다\" 라고 26 세의 여배우가 말 했다 .")
    # for text in inputText:
    #     # print(text.replace(" ", ""))
    #     # print(mecab.mecabTokenizer(text))
    #     print("--------------------------------")
    #     print(mecabSpacing(text, DEBUG=True))
    #     print("--------------------------------")

    readfile = open("/home/jjeaby/Dev/06.rosamia/SmiToText/data/koDetokenizerData/pure_ko.txt", mode="r",
                    encoding="utf-8")
    linenum = 1
    while True:
        linenum += 1
        line = readfile.readline()
        if linenum == 92:
            break

        text = line.strip()

        # print(text.replace(" ", ""))
        # print(mecab.mecabTokenizer(text))
        print(linenum, "--------------------------------")
        print(mecabSpacing(text, DEBUG=True))
        print(linenum, "--------------------------------")
