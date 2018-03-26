# Markov Text Generator

### Overview

This is a simple text generator based on the implementation of a basic Markov model.

It includes:

- `markov.py` -- core module with the model implementation
- `train.py` -- script with CLI building a model from the files in the user-specified directory
- `generate.py` -- script with CLI loading model from the specified destination and generating random word sequence based on the model
- `test_train.py` and `test_generate.py` attempt testing the above scripts part-by-part

The final testing is done by primitive bash scripts:

1. `launch_tests.sh` -- script runs over biblical texts in English and Yiddish``
2. `asimov.sh`-- runs over the collection of Isaac Asimov's texts in Russian