# Markov Text Generator

### Overview

##### master and simple-features branches -- basic generation

##### NOTE: currently master and simple-features branch are alike. simple-features branch is intended to reflect the past state of work.

This is a simple text generator based on the implementation of a basic Markov model.

It includes:

- `markov.py` -- core module with the model implementation
- `train.py` -- script with CLI building a model from the files in the user-specified directory
- `generate.py` -- script with CLI loading model from the specified destination and generating random word sequence based on the model
- `test_train.py` and `test_generate.py` attempt testing the above scripts part-by-part

The final testing is done by primitive bash scripts:

1. `launch_tests.sh` -- script runs over biblical texts in English and Yiddish``
2. `asimov.sh`-- runs over the collection of Isaac Asimov's texts in Russian

##### advanced branch -- Russian grammar with pymorphy2 was added

##### **NOTE: No backward compatibility with model files from the branches above is provided!!!**

In this branch the scripts are capable of some grammar forms morphological checks. They are done after the "lexical" Markov chain has generated some random sequence. A Markov model holding "grammar morphological states"  is constructed and applied to all bigrams in the newly generated random word sequence.

To trigger generation with grammar use CLI argument `--grammar`with `ru` specifier which triggers Russian grammar processing.