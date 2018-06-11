# -*- coding: utf-8 -*-

import MeCab
import copy

from jpype import unicode

mecab = MeCab.Tagger('-d /usr/local/lib/mecab/dic/mecab-ko-dic')


def mecabTokenizer(sentence, DEBUG=False):
    sentence = sentence.lower()
    tempSentence = []
    mecabTokenizedSentence = []
    mecabConvertSentence = ""

    if DEBUG == True:
        print("*" * 100)
        print("mecabTokenizer Input Sentence : " + sentence)
        print("*" * 100)

    # mecab-ko 로 형태소 분석을 시작
    if len(sentence.strip()) > 0:
        mecabToken = mecab.parse(sentence).split("\n")
        for index, word in enumerate(mecabToken):
            wordAnalys = word.split("\t")
            # 불필요한 EOS, 공백 문자 제거
            if wordAnalys[0] != "EOS" and len(wordAnalys[0]) > 0:
                if wordAnalys[1].split(",")[0].startswith("VV") and wordAnalys[1].split(",")[7].split("/")[0] != "*":
                    mecabTokenizedSentence.append(wordAnalys[1].split(",")[7].split("/")[0]);
                else:
                    mecabTokenizedSentence.append(wordAnalys[0])

                tempSentence.append(copy.deepcopy(mecabTokenizedSentence))

    # print("-"*100)
    # 형태소가 분석되어 나눠진 단어를 문장으로 합쳐서 배열에 입력
    # 합칠때 ' ' 으로 구분하여 합쳐짐
    for line in tempSentence:
        mecabConvertSentence = (' '.join(str(e) for e in line))

    return mecabConvertSentence


if __name__ == '__main__':

    while True:
        try:
            inputText = input("\n\n문장을 입력하세요?: \n")
            inputText = unicode(inputText)
        except UnicodeDecodeError:
            print("다시 입력하세요\n")
            continue

        if inputText == 'exit':
            exit(1)
        print(mecabTokenizer(inputText))

        # print(twitterStemmer(inputText))
