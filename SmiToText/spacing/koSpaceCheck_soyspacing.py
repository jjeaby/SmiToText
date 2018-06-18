from soyspacing.countbase import RuleDict, CountSpace
from SmiToText.util.util import Util
import os

class koSpaceCheck_soyspacing(object):

    def __init__(self):
        self.util = Util()

    def train(self, filename):
        verbose = False
        mc = 10  # min_count
        ft = 0.3  # force_abs_threshold
        nt = -0.3  # nonspace_threshold
        st = 0.3  # space_threshold

        model = CountSpace()
        model.load_model("/home/jjeaby/Dev/06.rosamia/soyspacing/demo_model/test.model", json_format=False)
        #
        # curDirPath = self.util.getCurDirPath(__file__)
        # corpus_fname = curDirPath + os.path.sep + "koSpaceCheckData" + os.path.sep + "all2.txt"
        # model_fname = curDirPath + os.path.sep + "koSpaceCheckData" + os.path.sep + "all2.model"
        # model = CountSpace()
        # model.train(corpus_fname)
        # model.save_model(model_fname, json_format=False)
        # model.load_model(model_fname, json_format=False)

        #sent = '이건진짜좋은영화 라라랜드진짜좋은영화'
        sent = '그일단그구성원인사람들과,,'

        # with parameters
        sent_corrected_1, tags = model.correct(
            doc=sent,
            verbose=verbose,
            force_abs_threshold=ft,
            nonspace_threshold=nt,
            space_threshold=st,
            min_count=mc)

        # without parameters
        sent_corrected_2, tags = model.correct(sent)

        print(sent_corrected_1)
        print(sent_corrected_2)


if __name__ == '__main__':
    ksc = koSpaceCheck_soyspacing()
    ksc.train('norm_1.txt')
