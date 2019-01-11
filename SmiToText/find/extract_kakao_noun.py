from khaiii import KhaiiiApi

'''
카카오 한글 형태소 분석기를 이용한 명사 추출기

'''


class extract_kakao_Noun(object):

    def __init__(self):
        pass

    def kakao_postagger_nn_finder(self, summay_text):
        api = KhaiiiApi()
        api.open()
        nn_word_list = []
        for word in api.analyze(summay_text):
            morphs_str = ' + '.join([(m.lex + '/' + m.tag) for m in word.morphs])
            # print(f'{word.lex}\t{morphs_str}')

            morphs_str_list = morphs_str.split(" + ")

            complex_morphs = ""
            for mophs_item in morphs_str_list:
                if mophs_item.split("/")[1].startswith("N") or mophs_item.split("/")[1].startswith("MM") or \
                        mophs_item.split("/")[1].startswith("SN") or mophs_item.split("/")[1].startswith("SL"):
                    complex_morphs = complex_morphs + mophs_item.split("/")[0]

            if len(complex_morphs) > 1:
                # print("->", complex_morphs)
                nn_word_list.append(complex_morphs)

        return nn_word_list

if __name__ == '__main__':
    extract_kakao_Noun_a = extract_kakao_Noun()
    a  = extract_kakao_Noun_a.kakao_postagger_nn_finder("안녕하세요")
    print(a)
