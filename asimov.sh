#!/bin/bash

python train.py --input-dir ./test_src/samples/asimov --model ./test_src/model/asimov.bin --grammar ru
python generate.py --model ./test_src/model/asimov.bin --length 8 --grammar ru
