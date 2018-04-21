import argparse as arg
import markov as markov
import sys
import re
import os
import pickle
"""
    This module processes the text and builds Markov
    model. The interaction is through CLI
"""


def process_console():
    """
    sets arguments for the CLI
    :return: parser
    """
    parser = arg.ArgumentParser()
    parser.add_help = False
    parser.add_argument("--model", help="path to store the model as bin")
    parser.add_argument("--input-dir",
                        help="specifies the input dir"
                        "with source .txt UTF-8 files, optional")
    parser.add_argument("--lc",
                        help="lowercase the input",
                        action="store_true")
    parser.add_argument("--order", help="specifies model order. Max is seven"
                                        "For natural languages more than 7 "
                                        "is not optimal.",
                        default=7, type=int)
    parser.add_argument("--grammar", help="if some grammar support is intended, enable this argument;"
                                          "the valid options are 'ru'")
    args_list = parser.parse_args()
    return args_list


class ModelTrainer:
    """
    This class contains all the operations to train the model.
    Its fields define key parameters for unit-testing
    """
    def __init__(self, model_dir, input_dir, lang, model_order=7, is_lower=False):
        self.model_dir = model_dir  # specifies where to store the model
        self.input_dir = input_dir  # input directory with sources
        self.is_lower = is_lower  # is there a need to lowercase?
        self.files_list = []  # sources to build the model

        model = markov.MarkovModel()  # Markov model dictionary
        self.model_order = model_order

        grammar = markov.GrammarModel(lang = lang)  # Markov grammar model
        self.grammar_order = 1
        self.joint = markov.JointModel(model, grammar)  # convenience wrapper

    def process_sources(self):
        # input. Scripts accepts only UTF8 .txt fils

        if self.input_dir is not None:
            path = self.input_dir
            for i in os.listdir(path):
                if i.endswith('.txt'):
                    self.files_list.append(i)
            if len(self.files_list) == 0:
                raise RuntimeError("Empty sources directory!!!")
        else:
            # Console input is triggered
            self.files_list.append(sys.stdin)

    def build_model(self):
        for file_name in self.files_list:
            if self.files_list[0] is not sys.stdin:
                try:
                    file = open(self.input_dir +
                                "/" + file_name, "r")
                except:
                    raise RuntimeError("Problems with sources input")
            else:
                file = self.files_list[0]
            while True:
                try:
                    line = file.readline()
                except:
                    raise RuntimeError("Failed to read the line in " +
                                       str(file_name))
                if not line:
                    break
                if self.is_lower:
                    line = line.lower()
                raw_data = re.findall("[А-Яа-яa-zA-Zא-ת']+", line)

                # updating lexical model
                for order in range(self.model_order):
                    self.joint.lex.update_model(data=raw_data,
                                                model_order=order)
                # updating grammar model
                if self.joint.gramm != markov.GrammarModel.no_grammar:
                    for gorder in range(1, self.grammar_order + 1):
                        self.joint.gramm.update_model(data=raw_data,
                                                      model_order=gorder)

    def save_model(self):
        """
        This method was not removed for sustainability of old tests
        """
        try:
            model_file = open(str(self.model_dir), "wb+")
            pickle.dump(self.joint, model_file, pickle.HIGHEST_PROTOCOL)
        except FileNotFoundError:
            print("There are some problems with your mode file path")
            model_dir = os.path.dirname(self.input_dir)
            if not os.path.exists(model_dir):
                print("Directory does not exist. Creating directory")
                os.mkdir(model_dir)


def main():
    args_list = process_console()

    trainer = ModelTrainer(model_dir=args_list.model,
                           input_dir=args_list.input_dir,
                           is_lower=args_list.lc,
                           model_order=args_list.order,
                           lang=args_list.grammar)
    trainer.process_sources()
    trainer.build_model()
    trainer.save_model()

if __name__ == "__main__":
    main()
