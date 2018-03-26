#!/bin/bash

# bible text launch
python train.py --input-dir ./test_src/samples --model ./test_src/model/bible.bin
python generate.py --model ./test_src/model/bible.bin --length 8

# bible text generation with seed
python generate.py --model ./test_src/model/bible.bin --length 8 --seed Saul

# bible text hard generation
python generate.py --model ./test_src/model/bible.bin --length 100 --output ./test_src/output/bible_shit.txt

# yiddish text
python train.py --input-dir ./test_src/samples/yiddish --model ./test_src/model/torah.bin
python generate.py --model ./test_src/model/torah.bin --length 8
