import markov as mk
import pickle
import argparse
import os
import pymorphy2 as pm


def console():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", help="Path to the binary with the model")
    parser.add_argument("--seed", help="Seed word for the model")
    parser.add_argument("--length", help="Length of the generated sequence",
                        type=int)
    parser.add_argument("--output", help="Path to file to save sequence")
    parser.add_argument("--grammar", help="if some grammar support is intended, enable this argument;"
                                          "the valid options are 'ru' and 'uk': russian and ukrainian. "
                                          "TO USE the grammar"
                                          "model you have to specify this argument. Otherwise no-grammar"
                                          "generation would take place")

    args_parsed = parser.parse_args()
    return args_parsed


class SentenceGenerator():
    """
    This class generates the sentences. Everything is parameterized for
    the sake of unittesting.
    """
    def __init__(self, model, length, seed, output, lang):
        self.analyzer = pm.MorphAnalyzer()
        self.model_filename = model
        self.length = length
        self.seed = seed
        self.output = output
        self.joint = mk.JointModel(mk.MarkovModel(), mk.GrammarModel(lang=None))
        self.sentence = ""
        self.user_lang = lang

    def load_model(self):
        """
        Loads a model from the binary file
        :param model_file_name: path to file with model
        :return: loaded model
        """
        model_file = None
        try:
            model_file = open(self.model_filename, "rb")
        except:
            raise RuntimeError("Please, sprecify file with model correctly")
        model = None
        try:
            model = pickle.load(model_file)
        except:
            raise RuntimeError("Problems loading the model from the file")
        self.joint = model

    def gen_sent(self):
        if self.joint is None:
            raise RuntimeError("Model was not loaded")
        if type(self.length) is not int or self.length < 0:
            raise RuntimeError("Length of the random sequence is not specified"
                               " or is incorrect")

        if self.seed is not None and (self.seed,) \
                not in set(self.joint.lex):
            print("Your seed is not valid or specified. Choosing random")
            self.seed = None
        self.sentence = self.joint.lex.random_sent(length=self.length,
                                                   seed_word=self.seed)

    def save_sentence(self):
        if self.output is None:
            print(" ".join(self.sentence))
            return
        _, extension = os.path.splitext(self.output)

        if extension != ".txt":
            raise RuntimeWarning("The recommended dist is  a .txt file!!!")

        dist = None
        try:
            dist = open(self.output, "w+")
        except:
            print("Destination doesn't exist. Creating file")
            dir = os.path.dirname(self.output)
            if not os.path.exists(dir):
                print("Directory does not exist. Creating directory")
                os.mkdir(dir)
            os.mknod(self.output)
            dist = open(self.output, "w+")
        dist.write(" ".join(self.sentence))

    def verify_words(self, pre, post):
        pre_form = (self.analyzer.parse(pre)[0].tag,)
        if pre_form not in self.joint.gramm:
            return post
        post_form_parsed = self.analyzer.parse(post)
        post_form = (post_form_parsed[0].tag,)
        post_freq = self.joint.gramm[pre_form].frequency(post_form)
        if post_freq is None:
            return post
        max_freq, optimal_word = post_freq, ""
        for item in self.joint.gramm[pre_form]:
            cur_freq = self.joint.gramm[pre_form].frequency(item)
            if cur_freq > max_freq:
                optimal_word, max_freq = cur_freq, optimal_word
        return post_form_parsed[0].inflect(optimal_word).word

    def adjust_grammar(self):
        for pos in range(len(self.sentence) - 1):
            self.sentence[pos + 1] = self.verify_words(self.sentence[pos],
                                                       self.sentence[pos + 1])


def main():
    args = console()
    generator = SentenceGenerator(length=args.length, model=args.model,
                                  seed=args.seed, output=args.output, lang=args.grammar)
    generator.load_model()
    generator.gen_sent()
    if generator.joint.gramm != mk.GrammarModel.no_grammar:
        generator.adjust_grammar()
    generator.save_sentence()

if __name__ == "__main__":
    main()
