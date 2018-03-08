# Baseline for NLI-task
- made by Zsaknadrag,
- using [word2vec](https://code.google.com/p/word2vec/) to distinguish between neutral and non-neutral sentence pairs
- and  [logistic regression](https://en.wikipedia.org/wiki/Logistic_regression) as classifier
## Install
make sure you install *gensim* and *jsonlines* modules with:
```
pip install gensim
pip install jsonlines
```
## Similarity of premise and hypothesis
- hypothesis is denoted with *h*, and premise is dentoted with *p*
- each word in *h* is matched to the word in *p* to which it is most similar based on cosine similarity
- the overall sentence similarity of *h* and *p* is calculated in two separate ways: the first method (*prodsim*) takes the product of word similarities, the second (*meansim*) takes the mean of the similarites
- sententce similarity is taken as a feature in logistic regression
## Usage
To run the script with the text8 word2vec model simply type:
```
python baseline_vanda.py
```
Specifying the jsonl files containing the train and the development set type:
```
python baseline_vanda.py -train <train_file> -dev <dev_file>
```
Running the script with `<number>` sentence pairs, where size of the training and development set is 0.75 * `<number>` and 0.25*`<number>` , respectively:
```
python baseline_vanda.py -number <number>
```
Using [google word2vec model](https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/edit):
```
python baseline_vanda.py -googlemodel
```
# Results
Scores with *prodsim* and *meansim*:
- train: 0.716, 0.712
- dev_matched: 0.696, 0.692
- dev_mismatched 0.684, 0.68


