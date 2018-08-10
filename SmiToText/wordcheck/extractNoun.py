# -*- coding: utf-8 -*-
import re

from konlpy.tag import Hannanum
from konlpy.tag import Kkma
from konlpy.tag import Komoran
from konlpy.tag import Twitter


class extractNoun(object):

    def __init__(self):
        pass

    def findNoun(self, sentence):
        hannanum = Hannanum()
        # print(hannanum.analyze(sentence))
        hannanumNoun = hannanum.nouns(sentence)

        kkma = Kkma()
        # print(kkma.analyze(sentence))
        kkmaNoun = kkma.nouns(sentence)

        komoran = Komoran()
        # print(komoran.analyze(sentence))
        komaranNoun = komoran.nouns(sentence)

        twitter = Twitter()
        # print(twitter.analyze(sentence))
        twitterNoun = twitter.nouns(sentence)

        nounSet = set([])

        nounSet.update(hannanumNoun)
        nounSet.update(kkmaNoun)
        nounSet.update(komaranNoun)
        nounSet.update(twitterNoun)

        norm_noun = []
        exception_nount = []

        for nounItem in nounSet:
            if len(nounItem) > 1:
                numList = re.findall(r'\d+', nounItem)
                if len(numList) == 0:
                    print(linenum, nounItem)
                    nounItem = nounItem.replace("(", "\n")
                    nounItem = nounItem.replace(")", "\n")
                    nounItem = nounItem.replace("ㆍ", "\n")
                    nounItem = nounItem.replace("·", "\n")
                    nounItem = nounItem.replace("「", "\n")
                    nounItem = nounItem.replace("」", "\n")
                    nounItem = nounItem.replace(",", "\n")
                    nounItem = nounItem.replace(":", "\n")
                    nounItem = nounItem.replace(";", "\n")
                    nounItem = nounItem.replace(".", "\n")
                    nounItem = nounItem.replace("\"", "\n")
                    nounItemList = nounItem.split("\n")

                    for item in nounItemList:
                        if len(item) > 1:
                            removejosa = ["은", "는", "이", "가", "을", "를", "의", "또한", "에", "에게", "등", "거나", "하다", "자로",
                                          "이하", "관이"]
                            if not str(item).endswith(tuple(removejosa)):
                                norm_noun.add(item)
                            else:
                                exception_nount(item)

        return_noun = [norm_noun, exception_nount]
        return return_noun


if __name__ == '__main__':
    extractnoun = extractNoun()

    # input_filename = "/home/jjeaby/Dev/06.rosamia/SmiToText/SmiToText/wordcheck/input.txt"
    input_filename = "./law.go.kr.txt"
    output_filename = "./output.txt"
    error_filename = "./error.txt"

    read_file = open(input_filename, mode='r', encoding='utf-8')
    write_file = open(output_filename, mode='w', encoding='utf-8')
    write_file.close()
    error_file = open(error_filename, mode='w', encoding='utf-8')
    error_file.close()

    linenum = 0
    while True:
        line = read_file.readline()
        line = line.strip()
        isLastChar = 0
        linenum += 1
        if not line:
            print("NOT LINE : ", '\'' + line + '\'', linenum)
            break

        nounList = extractnoun.findNoun(line)
        for nounItem in nounList:
            if len(nounItem) > 1:
                numList = re.findall(r'\d+', nounItem)
                if len(numList) == 0:
                    print(linenum, nounItem)
                    nounItem = nounItem.replace("(", "\n")
                    nounItem = nounItem.replace(")", "\n")
                    nounItem = nounItem.replace("ㆍ", "\n")
                    nounItem = nounItem.replace("·", "\n")
                    nounItem = nounItem.replace("「", "\n")
                    nounItem = nounItem.replace("」", "\n")
                    nounItem = nounItem.replace(",", "\n")
                    nounItem = nounItem.replace(":", "\n")
                    nounItem = nounItem.replace(";", "\n")
                    nounItem = nounItem.replace(".", "\n")
                    nounItem = nounItem.replace("\"", "\n")

                    nounItemList = nounItem.split("\n")

                    for item in nounItemList:
                        if len(item) > 1:
                            removejosa = ["은", "는", "이", "가", "을", "를", "의", "또한", "에", "에게", "등", "거나", "하다", "자로",
                                          "이하", "관이"]
                            if not str(item).endswith(tuple(removejosa)):
                                write_file = open(output_filename, mode='a', encoding='utf-8')
                                write_file.writelines(item + "\n")
                                write_file.close()
                            else:
                                error_file = open(error_filename, mode='a', encoding='utf-8')
                                error_file.writelines(item + "\n")
                                error_file.close()

    read_file.close()
