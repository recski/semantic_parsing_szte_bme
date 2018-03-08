import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')

from gensim.models import KeyedVectors
import jsonlines
import sys
import math
import numpy as np
import argparse
from sklearn.linear_model import LogisticRegression

def get_wv_model(google_model):
    try:
        if not google_model:
            model = KeyedVectors.load('text8.model')
            model = model.wv
        else:
            # model available at: https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/edit
            model = KeyedVectors.load_word2vec_format('model\GoogleNews-vectors-negative300.bin', binary=True)
        return model
    except IOError:
        sys.stderr.write('ERROR: Cannot open word2vec model.\n')
        sys.exit(1)

def get_json(file):
    try:
        return jsonlines.open(file)
    except IOError:
        sys.stderr.write('ERROR: Cannot open %s.\n' % file)
        sys.exit(1)

def product_similarity(sent1, sent2):
    sent1 = sent1.strip().split(" ")
    sent2 = sent2.strip().split(" ")

    hypothesis_dict = {}
    sent22 = [word2.lower() for word2 in sent2 if word2.lower() in model.vocab]
    sent11 = [word1.lower() for word1 in sent1 if word1.lower() in model.vocab]

    for word2 in sent22:
        sim = 0
        for word1 in sent11:
            currsim = model.similarity(word2, word1)
            if currsim > sim:
                sim = currsim
                hypothesis_dict[word2] = (word1, currsim)

    product = 1
    for k, (v1, v2) in hypothesis_dict.items():
        product *= v2
    return product

def mean_similarity(sent1, sent2):
    sent1 = sent1.strip().split(" ")
    sent2 = sent2.strip().split(" ")

    hypothesis_dict = {}
    sent22 = [word2.lower() for word2 in sent2 if word2.lower() in model.vocab]
    sent11 = [word1.lower() for word1 in sent1 if word1.lower() in model.vocab]

    for word2 in sent22:
        sim = 0
        for word1 in sent11:
            currsim = model.similarity(word2, word1)
            if currsim > sim:
                sim = currsim
                hypothesis_dict[word2] = (word1, currsim)

    sum = 0
    for k, (v1, v2) in hypothesis_dict.items():
        sum += v2
    if len(hypothesis_dict.items()) > 0:
        return sum/len(hypothesis_dict.items()) # normalize sum
    else:
        return 0

def train_model(similarity_function):
    reader_train = get_json(file_train)

    element = 0
    feat = []
    y = []
    for obj in reader_train:
        if element < TRAIN:
            sent1 = obj["sentence1"]
            sent2 = obj["sentence2"]
            product = similarity_function(sent1, sent2)
            logprob = math.log(product + 1)
            if obj["gold_label"] == "neutral":
                y.append(1.0)
            else:
                y.append(0.0)

            feat.append(logprob)
            element += 1
        else:
            break
    one_vec = [1.0 for i in feat]
    X = np.matrix([one_vec, feat])
    X = X.transpose()
    logisticRegr = LogisticRegression()
    logisticRegr.fit(X, y)
    score = logisticRegr.score(X, y)
    print("Logreg score on train: ", score)
    return logisticRegr

def predict(logisticRegr,similarity_function):
    reader_dev = get_json(file_dev)
    feat_test = []
    y_test = []
    element = 0
    for obj in reader_dev:
        if element < DEV:
            sent1 = obj["sentence1"]
            sent2 = obj["sentence2"]
            product = similarity_function(sent1, sent2)
            logprob = math.log(product + 1)
            if obj["gold_label"] == "neutral":
                y_test.append(1.0)
            else:
                y_test.append(0.0)
            feat_test.append(logprob)
            element += 1
    one_vec = [1.0 for i in feat_test]
    X_test = np.matrix([one_vec, feat_test])
    X_test = X_test.transpose()
    predictions = logisticRegr.predict(X_test)
    score = logisticRegr.score(X_test, y_test)
    print("Logreg score on dev: ", score)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='word2vec baseline for nli-task made by Zsaknadrag')
    parser.add_argument('-googlemodel', action='store_true', help = 'use (larger) google model, default value: False')
    parser.add_argument('-number', metavar='number', type=int, help='number of analyzed (train + dev together) sentence pairs, default value: 1000')
    parser.add_argument('-train', metavar='train', type=str, help='input train file in jsonl format')
    parser.add_argument('-dev', metavar='dev', type=str, help='input dev file in jsonl format')
    args = parser.parse_args()

    MAX_PEEK = 1000
    if args.number:
        MAX_PEEK = args.number
    TRAIN = 0.75 * MAX_PEEK
    DEV = MAX_PEEK - TRAIN

    GOOGLE_MODEL = False
    if args.googlemodel:
        GOOGLE_MODEL = True

    file_train = "multinli/multinli_1.0_train.jsonl"
    if args.train:
        file_train = args.train

    file_dev = "multinli/multinli_1.0_dev_mismatched.jsonl"
    if args.dev:
        file_dev = args.dev

    model = get_wv_model(GOOGLE_MODEL)
    print("Product Similarity results")
    logreg_model = train_model(product_similarity)
    predict(logreg_model, product_similarity)
    print("Mean Similarity results")
    logreg_model = train_model(mean_similarity)
    predict(logreg_model, mean_similarity)