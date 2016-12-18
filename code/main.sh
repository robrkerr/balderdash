
mkdir -p data/cv

# prepare summaries
python clean_summaries.py

## Torch-RNN: https://github.com/jcjohnson/torch-rnn
## Dockerised: https://github.com/crisbal/docker-torch-rnn

docker run --rm -ti -v `pwd`:/data crisbal/torch-rnn:base bash
# --- inside docker container vvvv

python scripts/preprocess.py --input_txt /data/data/summaries.txt --output_h5 /data/data/summaries.h5 --output_json /data/data/summaries.json

# train generator
th train.lua -input_h5 /data/data/summaries.h5 -input_json /data/data/summaries.json -checkpoint_name /data/data/cv/checkpoint -gpu -1

# train generator (from checkpoint)
th train.lua -input_h5 /data/data/summaries.h5 -input_json /data/data/summaries.json -checkpoint_name /data/data/cv/checkpoint -gpu -1 -init_from /data/data/cv/checkpoint_4000.t7

# generate artifical summaries - 1000000 ~= 16mins
th sample.lua -checkpoint /data/data/cv/checkpoint_7000.t7 -length 100000 -gpu -1 > /data/data/generated_summaries.txt
# --- inside docker container ^^^^

# prepare actual and artifical summaries for a classifier
python prepare_for_supervised.py

## FastText: https://github.com/facebookresearch/fastText (f8bea68)

# train classifier
./fastText/fasttext supervised -input data/summaries.train -output data/summaries_fasttext -dim 12 -lr 0.1 -wordNgrams 2 -minCount 1 -bucket 10000000 -epoch 20 -thread 4

# test classifier
./fastText/fasttext test data/summaries_fasttext.bin data/summaries.test

# predict with classifier
./fastText/fasttext predict-prob data/summaries_fasttext.bin data/generated_summaries.txt > data/generated_summary_predictions.txt

python choose_best_summaries.py


# To explore: https://github.com/hughperkins/pytorch
# Dataset from: http://www.cs.cmu.edu/~ark/personas/
# Intro to char RNN blog: http://karpathy.github.io/2015/05/21/rnn-effectiveness/

# Also maybe useful: https://github.com/tensorflow/models/tree/master/syntaxnet
# Dataset missing from FastText: https://github.com/Yelp/dataset-examples
# Worth looking at others ^^
