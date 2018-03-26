#!/bin/bash

python train.py --input-dir ./test_src/samples/asimov --model ./test_src/model/asimov.bin
python generate.py --model ./test_src/model/asimov.bin --length 8
