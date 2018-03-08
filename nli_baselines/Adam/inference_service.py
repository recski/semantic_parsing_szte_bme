import json
import logging
import os
import re
import sys
import pygraphviz as pgv

from text_to_4lang import TextTo4lang
from flask import Flask
from flask import jsonify
from corenlp_wrapper import CoreNLPWrapper
from dep_to_4lang import DepTo4lang
from lexicon import Lexicon
from magyarlanc_wrapper import Magyarlanc
from utils import ensure_dir, get_cfg, print_text_graph

assert Lexicon  # silence pyflakes (Lexicon must be imported for cPickle)

__LOGLEVEL__ = 'INFO'
__MACHINE_LOGLEVEL__ = 'INFO'

app = Flask(__name__)


class MyServer:
    def __init__(self):
        cfg = get_cfg(None)
        self.textto4lang = TextTo4lang(cfg)
        self.textto4lang.graphs_dir = '/home/adaamko/4lang/data'
        self.test = {}
        self.test['0'] = "I like dogs ."
        with open("multinli_1.0_train.jsonl", "r+") as f:
            self.premise = {}
            self.hypothesis = {}
            self.labels = {}
            count = 0
            for line in f:
#                print(count)
                count=count+1
                j = json.loads(line)
                pairId = j["pairID"]
                self.premise[pairId] = j["sentence1"]
                self.hypothesis[pairId] = j["sentence2"]
                self.labels[pairId] = j["gold_label"]
                
                
               # print("dot fajlok elkeszitese")
               # pair_id = pairId
               # filehyp = '/home/adaamko/4lang/data/' + pair_id + '_hypothesis' + '.sens'
               # fileprem = '/home/adaamko/4lang/data/' + pair_id + '_premise' + '.sens'
               # hyp = self.hypothesis[pair_id]
               # prem = self.premise[pair_id]
               # hyp_pro = self.textto4lang.preprocess_text(hyp)
               # prem_pro = self.textto4lang.preprocess_text(prem)
               # with open(filehyp, 'w') as f:
               #     f.write(hyp_pro.encode("utf8"))
               # with open(fileprem, 'w') as f:
               #     f.write(prem_pro.encode("utf8"))
               # self.textto4lang.input_sens = filehyp
               # self.textto4lang.process_file(filehyp, pair_id + 'hyp')

               # self.textto4lang.input_sens = fileprem
               # self.textto4lang.process_file(fileprem, pair_id + 'prem')
                
        print("beolvasas kesz")        

    def asim_jac(self, seq1, seq2):
        set1, set2 = map(set, (seq1, seq2))
        intersection = set1 & set2
        if not intersection:
            return 0
        else:
            sim = float(len(intersection)) / len(set2)
            return sim


my_server = MyServer()

@app.route('/pair_abstract/<pair_abstract_id>')
def pair_abstract(pair_abstract_id):
    my_server.textto4lang.expand = True
    my_server.textto4lang.dep_to_4lang.lexicon.lexicon = {}

    print(pair_abstract_id)
    filehyp = '/home/adaamko/4lang/data/' + pair_abstract_id + '_hypothesis_abstract' + '.sens'
    fileprem = '/home/adaamko/4lang/data/' + pair_abstract_id + '_premise_abstract' + '.sens'
    hyp = my_server.hypothesis[pair_abstract_id]	
    prem = my_server.premise[pair_abstract_id]
    hyp_pro = my_server.textto4lang.preprocess_text(hyp)
    prem_pro = my_server.textto4lang.preprocess_text(prem)
    with open(filehyp, 'w') as f:
        f.write(hyp_pro.encode("utf8"))
    with open(fileprem, 'w') as f:
        f.write(prem_pro.encode("utf8"))
    my_server.textto4lang.input_sens = filehyp
    my_server.textto4lang.process_file(filehyp, pair_abstract_id + 'hyp_abstract')

    my_server.textto4lang.input_sens = fileprem
    my_server.textto4lang.process_file(fileprem, pair_abstract_id + 'prem_abstract')
    return jsonify(hyp)

@app.route('/sym_abstract/<sym_abstract_id>')
def sym_abstract(sym_abstract_id):
    try:
        G1 = pgv.AGraph('/home/adaamko/4lang/data/' + sym_abstract_id + 'prem_abstract' + '.dot')
        G2 = pgv.AGraph('/home/adaamko/4lang/data/' + sym_abstract_id + 'hyp_abstract' + '.dot')
    except Exception as e:
        print("doterror volt abstract" + str(e))
        return jsonify("0")

    prem = []
    hyp = []

    for i in G1.edges():
        prem.append((i[0].split("_")[0], i[1].split("_")[0]))
    for i in G2.edges():
        hyp.append((i[0].split("_")[0], i[1].split("_")[0]))
    a =  my_server.asim_jac(prem, hyp)
    return jsonify(str(a))



@app.route('/test/<test_id>')
def test(test_id):
    my_server.textto4lang.expand = True
    my_server.textto4lang.dep_to_4lang.lexicon.lexicon = {}
    test_file = '/home/adaamko/4lang/data/' + 'test' + '.sens'
    test = my_server.test[test_id]	
    test_pro = my_server.textto4lang.preprocess_text(test)
    with open(test_file, 'w') as f:
        f.write(test_pro.encode("utf8"))
    my_server.textto4lang.input_sens = test_file
    my_server.textto4lang.process_file(test_file, 'test')

    return jsonify(test)



@app.route('/pair/<pair_id>')
def pair(pair_id):
    my_server.textto4lang.expand = False
    filehyp = '/home/adaamko/4lang/data/' + pair_id + '_hypothesis' + '.sens'
    fileprem = '/home/adaamko/4lang/data/' + pair_id + '_premise' + '.sens'
    hyp = my_server.hypothesis[pair_id]	
    prem = my_server.premise[pair_id]
    hyp_pro = my_server.textto4lang.preprocess_text(hyp)
    prem_pro = my_server.textto4lang.preprocess_text(prem)
    with open(filehyp, 'w') as f:
        f.write(hyp_pro.encode("utf8"))
    with open(fileprem, 'w') as f:
        f.write(prem_pro.encode("utf8"))
    my_server.textto4lang.input_sens = filehyp
    my_server.textto4lang.process_file(filehyp, pair_id + 'hyp')

    my_server.textto4lang.input_sens = fileprem
    my_server.textto4lang.process_file(fileprem, pair_id + 'prem')
    return jsonify(hyp)

@app.route('/sym/<sym_id>')
def sym(sym_id):
    try:
        G1 = pgv.AGraph('/home/adaamko/4lang/data/' + sym_id + 'prem' + '.dot')    
        G2 = pgv.AGraph('/home/adaamko/4lang/data/' + sym_id + 'hyp' + '.dot')
    except:
        print("doterror volt")
        return jsonify("0")

    prem = []
    hyp = []
    
    for i in G1.edges():
        prem.append((i[0].split("_")[0], i[1].split("_")[0]))    
    for i in G2.edges():
        hyp.append((i[0].split("_")[0], i[1].split("_")[0]))
    a =  my_server.asim_jac(prem, hyp)
    return jsonify(str(a))    


@app.route('/pairexp/<pair_id>')
def pairexp(pair_id):
    my_server.textto4lang.expand = True
    #TESZT
    my_server.textto4lang.dep_to_4lang.lexicon.lexicon = {}
    filehyp = '/home/adaamko/4lang/data/' + pair_id + '_hypothesis_expand' + '.sens'
    fileprem = '/home/adaamko/4lang/data/' + pair_id + '_premise_expand' + '.sens'
    hyp = my_server.hypothesis[pair_id]
    prem = my_server.premise[pair_id]
    hyp_pro = my_server.textto4lang.preprocess_text(hyp)
    prem_pro = my_server.textto4lang.preprocess_text(prem)
    with open(filehyp, 'w') as f:
        f.write(hyp_pro.encode("utf8"))
    with open(fileprem, 'w') as f:
        f.write(prem_pro.encode("utf8"))
    my_server.textto4lang.input_sens = filehyp
    my_server.textto4lang.process_file(filehyp, pair_id + 'hyp_expand')

    my_server.textto4lang.input_sens = fileprem
    my_server.textto4lang.process_file(fileprem, pair_id + 'prem_expand')
    return jsonify(hyp)

@app.route('/symexp/<sym_id>')
def symexp(sym_id):
    try:
        G1 = pgv.AGraph('/home/adaamko/4lang/data/' + sym_id + 'prem_expand' + '.dot')
        G2 = pgv.AGraph('/home/adaamko/4lang/data/' + sym_id + 'hyp_expand' + '.dot')
    except:
        print("doterror volt")
        return jsonify("0")

    prem = []
    hyp = []

    for i in G1.edges():
        prem.append((i[0].split("_")[0], i[1].split("_")[0]))
    for i in G2.edges():
        hyp.append((i[0].split("_")[0], i[1].split("_")[0]))
    a =  my_server.asim_jac(prem, hyp)
    return jsonify(str(a))


@app.route("/")
def hello():
    return "Hello World!"


if __name__ == '__main__':
    app.run(debug=True)
