import pickle
import codecs
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktTrainer
from nltk.corpus import gutenberg
import os.path


class Punket_tokenizer:
    def __init__(self):
        self.modelfile = 'punket_tokenizer.pk'

        if os.path.exists(self.modelfile):
            self.tokenizer = self.punkt_tokenize_load()


        else:
            self.trainer = PunktTrainer()
            text = ""
            for file_id in gutenberg.fileids():
                text += gutenberg.raw(file_id)
            self.trainer.INCLUDE_ALL_COLLOCS = True
            self.trainer.train(text)
            self.tokenizer = PunktSentenceTokenizer(self.trainer.get_params())

            self.tokenizer._params.abbrev_types.add('dr')
            self.tokenizer._params.abbrev_types.add('mr')
            self.tokenizer._params.abbrev_types.add('mrs')
            self.tokenizer._params.abbrev_types.add('miss')
            self.tokenizer._params.abbrev_types.add('ms')
            self.tokenizer._params.abbrev_types.add('no')

            self.tokenizer._params.abbrev_types.add('jan')
            self.tokenizer._params.abbrev_types.add('feb')
            self.tokenizer._params.abbrev_types.add('mar')
            self.tokenizer._params.abbrev_types.add('apr')
            self.tokenizer._params.abbrev_types.add('may')
            self.tokenizer._params.abbrev_types.add('jun')
            self.tokenizer._params.abbrev_types.add('aug')
            self.tokenizer._params.abbrev_types.add('sep')
            self.tokenizer._params.abbrev_types.add('oct')
            self.tokenizer._params.abbrev_types.add('nov')
            self.tokenizer._params.abbrev_types.add('dec')



            with open(self.modelfile, mode='wb') as fout:
                pickle.dump(self.tokenizer, fout, protocol=pickle.HIGHEST_PROTOCOL)


    def punkt_tokenize_load(self):
        with open(self.modelfile, mode='rb') as fin:
            punket_tokenizer = pickle.load(fin)

        return punket_tokenizer

    def puket_tokenizer_add_rule(self, word):
        self.tokenizer._params.abbrev_types.add(word)

    def punket_sentence_tokenizer(self, sentences):
        return self.tokenizer.tokenize(sentences)
