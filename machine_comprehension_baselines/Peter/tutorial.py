from feature_extractor_interface import get_features_wordvec
from feature_extractor_interface import get_features_bow
from combine import combinator
from machine_learning import train_and_test
from sklearn import svm
import pickle


train = "train-data.xml"
dev = "dev-data.xml"
filename_bow = "bow.pickle"
filename_wv = "wv.pickle"
# only once
get_features_bow(train, dev, filename_bow)

"""
    https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/edit
"""
model_path = 'GoogleNews-vectors-negative300.bin'

# only once
get_features_wordvec(train, dev, model_path, filename_wv)

combined = "combined_features.pickle"
# only once
combinator(combined, filename_bow, filename_wv)

clf = svm.SVC(kernel='linear')

"""Change which file to use for learning"""
with open(combined, "rb") as f:
    all = pickle.load(f)
    train_x = all[0]
    train_y = all[1]
    test_x = all[2]
    test_y = all[3]

train_and_test(train_x, train_y, test_x, test_y, clf)
