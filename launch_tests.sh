#!/bin/bash

# bible text launch
python train.py --input-dir ./test_src/samples --model ./test_src/model/bible.bin
python generate.py --model ./test_src/model/bible.bin --length 8
echo -- bible text processing is over

# bible text generation with seed
python generate.py --model ./test_src/model/bible.bin --length 8 --seed Saul
echo -- bible text generation with seed is over

# bible text hard generation
python generate.py --model ./test_src/model/bible.bin --length 100 --output ./test_src/output/bible_shit.txt
echo -- bible text generation with file output is over

# yiddish text
python train.py --input-dir ./test_src/samples/yiddish --model ./test_src/model/torah.bin
python generate.py --model ./test_src/model/torah.bin --length 8
echo -- yiddish text generation is voer

# testing model order parameter
for ord in {1..7}
do 
	echo --- testing order $ord
	python train.py --input-dir ./test_src/samples --model ./test_src/model/bible.bin --order $ord
	python generate.py --model ./test_src/model/bible.bin --length 8 --seed Saul
done
echo -- order argument testing is over

