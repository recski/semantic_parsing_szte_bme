from sklearn.feature_extraction.text import CountVectorizer
from nltk.tokenize import sent_tokenize
from xml.etree import ElementTree
import numpy as np
from nltk import word_tokenize
import math
import pickle

import warnings

warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
import gensim

stoplist = set('a of and . ! , to \'s'.split())

vectorizer = CountVectorizer(stop_words="english")


class MyData(object):
    def __init__(self):
        self.data = []
        self.target = []
        self.wv_sim = []


def get_features_bow(train, dev, outfile="features_bow.pickle"):
    global vectorizer
    global clf
    vocabulary, data_list = get_vocabulary_and_data(train, dev)
    vectorizer = CountVectorizer(stop_words="english", vocabulary=vocabulary)
    X = haromsoros(data_list[0])
    hatar = len(X)
    X += haromsoros(data_list[1])
    print("feature szám: ", len(X[0]))
    X = feature_reduction(X)
    print("feature szám: ", len(X[0]))

    with open(outfile, "wb") as f:
        pickle.dump([X[:hatar], data_list[0].target, X[hatar:], data_list[1].target], f)
    del vectorizer
    return X[:hatar], data_list[0].target, X[hatar:], data_list[1].target


"""
    Full 0 feature-öket kitörli
"""


def feature_reduction(X):
    print("Feature reduction...")
    for column in reversed(range(len(X[0]))):
        osszeg = 0
        for row in X:
            osszeg += abs(row[column])
        osszeg = osszeg / len(X)
        if osszeg == 0:
            for row in X:
                row.pop(column)

    print("Done.")
    return X


"""
    A két válasz vektorból 1 vektort csinál
"""


def haromsoros(data):
    X = []
    for answer_pair_list in data.data:
        temp_X = vectorizer.fit_transform(answer_pair_list)
        X.append((temp_X[0] - temp_X[1]).toarray()[0].tolist())
    return X


"""
    Beolvassa az adatokat + vocabulary-t kigyűjti
"""


def get_vocabulary_and_data(*args):
    vocabulary = set()
    datas = []

    global vectorizer
    analyze = vectorizer.build_analyzer()

    for elem in args:
        data = MyData()
        print(elem)
        parser = ElementTree.parse(elem)
        instances = parser.findall('instance')

        for inst in instances:
            text = inst.find('text').text
            corpus = [text]
            questions = inst.find('questions').findall('question')

            for q in questions:
                data_answer = []
                ans = q.findall('answer')
                targ = ans[0].attrib['correct']
                if targ == "True":
                    targ = 1
                else:
                    targ = 0
                data.target.append(targ)
                corpus.append(ans[0].attrib['text'])
                corpus.append(ans[1].attrib['text'])

                data_answer.append(ans[0].attrib['text'])
                data_answer.append(ans[1].attrib['text'])
                data.data.append(data_answer)

            for line in corpus:
                tmp_voc = analyze(line)
                vocabulary.update(tmp_voc)

        datas.append(data)

    print("Vocabulary Done")

    return vocabulary, datas


def get_features_wordvec(train, dev, model_path, outfile="data_features_wv.pickle"):
    global model
    model = gensim.models.KeyedVectors.load_word2vec_format(model_path, binary=True)

    data_list = get_data_wordvec(train, dev)

    with open(outfile, "wb") as f:
        pickle.dump([data_list[0].wv_sim, data_list[0].target, data_list[1].wv_sim, data_list[1].target], f)
    del model
    return data_list[0].wv_sim, data_list[0].target, data_list[1].wv_sim, data_list[1].target


"""
    input -> szavak
    Vektorrá alakítja a szavakat
"""


def get_word_vectors(words):
    global stoplist
    temp = []
    for word in words:
        try:
            if word not in stoplist:
                temp.append(model.wv[word])
        except Exception as e:
            print("Missing word: ", e)
    if len(temp) == 0:
        temp.append(np.zeros(len(model.wv['apple'])).tolist())
    return temp


"""
    input -> mondat szavai vektorként
    Átlagolja őket, 1 vektorként adja vissza
"""


def simplify(words):
    temp = []
    for position in range(len(words[0])):
        osszeg = 0
        for word in words:
            osszeg += float(word[position])
        osszeg = osszeg / len(words)
        temp.append(osszeg)
    return temp


"""
    Text és answer hasonlóságát számolja
    a legnagyobb simalirity-jű vector és mondat vector különbségét adja vissza
"""


def similarity(wordvec, texts):
    sim_val = -1
    vec = []

    for text in texts:

        osszeg = 0
        for index in range(len(wordvec)):
            try:
                osszeg += wordvec[index] * text[index]
            except Exception as e:
                print("Text1 <==> Text2")
                print(wordvec)
                print(text)
                print(e)

        if osszeg == 0.0:
            if sim_val < 0:
                sim_val = 0
                vec = wordvec
        else:
            calc_sim = math.fabs(osszeg / (fro_norm(wordvec) * fro_norm(text)))
            if sim_val < calc_sim:
                sim_val = calc_sim
                vec = np.subtract(wordvec, text)

    return vec


"""
    Frobenius norma
"""


def fro_norm(vector):
    temp = 0
    for item in vector:
        temp += item ** 2

    return math.sqrt(temp)


"""
    args -> train/test data FILE nevek
    Vissza tér [train_data, test_data] <- belső elemek MyData type
"""


def get_data_wordvec(*args):
    datas = []

    for elem in args:
        data = MyData()
        print(elem)
        parser = ElementTree.parse(elem)
        instances = parser.findall('instance')

        for inst in instances:
            corpus_temp = sent_tokenize(inst.find('text').text)
            corpus_temp = [simplify(get_word_vectors(word_tokenize(sent))) for sent in corpus_temp]
            questions = inst.find('questions').findall('question')

            for q in questions:
                ans = q.findall('answer')
                targ = ans[0].attrib['correct']
                if targ == "True":
                    targ = 1
                else:
                    targ = 0
                data.target.append(targ)

                a1 = simplify(get_word_vectors(word_tokenize(ans[0].attrib['text'])))
                a2 = simplify(get_word_vectors(word_tokenize(ans[1].attrib['text'])))

                a1_sim = similarity(a1, corpus_temp)
                a2_sim = similarity(a2, corpus_temp)

                data.wv_sim.append(np.subtract(a1_sim, a2_sim))

        datas.append(data)

    return datas
