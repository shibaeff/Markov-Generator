from numpy import random as rand
import random
"""
    The core model with the Markov model implementation.
    Contains:
        - Histogram class storing frequencies distribution for some unique entry
        - Markov model class holding the Histograms
         
"""

class Histogram(dict):
    """
    The data structure is based on the standard dictionary.
    Thus amortized operations (add, read) time is provided.
    """
    def __init__(self, iterable=None):
        """
        Initialize the structure
        :param iterable: some abstract iterable obj with data to
        construct the chain
        """
        assert  iterable
        super().__init__()
        self.num_of_distinct = 0  # number of distinct types in distribution
        self.tokens_num = 0  # overall number of tokens
        if iterable:
            self.update(iterable)

    def update(self, iterable):
        """
        This method overrides standard dict.update(). Adds new words from
        iterable.
        :param iterable: some abstract iterable obj with data
        :return:
        """
        for token in iterable:
            if token in self:
                self[token] += 1
                self.tokens_num += 1
            else:
                self[token] = 1
                self.num_of_distinct += 1
                self.tokens_num += 1

    def frequency(self, token):
        """
        :param token: query token
        :return: frq of the token
        """
        res = self.get(token)
        assert res
        return res

    def get_random(self):
        """
        :return: some random word from the keys set
        """
        return rand.sample(self, 1)[0]

    def get_weighted_random(self):
        """
        :return: random word with respect to its weight
        """
        tokens_list = self.keys()
        rand_weight = rand.randint(0, self.tokens_num, 1)
        for token in tokens_list:
            rand_weight = rand_weight - self[token]
            if rand_weight <= 0:
                return token


class MarkovModel(dict):
    def __init__(self):
        """
        class is based on the built-on dict
        :param model_order:
        """
        dict().__init__(self)

    def update_model(self, model_order, data):
        """
        Updates model by analyzing the provided piece of data
        Data is split in tokens. Token is a word or combination of words.
        :param model_order: defiens the size of the tokens.
        :param data: data to analyze
        :return:
        """
        for i in range(0, len(data) - model_order):
            # slider is a currently analyzed token of model size
            slider = tuple(data[i:i + model_order])
            # default dict is also possible, but it can be costly for large models
            if slider in self:
                self[slider].update([data[i + model_order]])
            else:
                self[slider] = Histogram([data[i + model_order]])

    def random_sent(self, length, seed_word):
        """
        Generates random sentence based on given Markov model
        :param length: length of the sentence
        :param gen_model: base Model
        :return: random sentence
        """
        keys = set(self)
        seed = None
        if seed_word is None:
            seed = rand.choice(list(keys))
        else:
            seed = (seed_word,)
        sent = [*seed]
        while(len(sent) < length):
            current_hist = self[seed]
            gen = current_hist.get_weighted_random()
            sent.append(gen)
            seed = gen if gen in keys else rand.choice(list(keys))
        return " ".join(sent)

    def output(self):
        """
        Output is used for debug perposes
        :return:
        """
        for h in self.items():
            print("------\n", h)