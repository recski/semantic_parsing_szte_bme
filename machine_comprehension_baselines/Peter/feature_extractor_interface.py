from feature_extractor import get_features_wordvec as gfw
from feature_extractor import get_features_bow as gfb


def get_features_bow(train, dev, outfile="features_bow.pickle"):
    return gfb(train, dev, outfile)


def get_features_wordvec(train, dev, model_path, outfile="features_wv.pickle"):
    return gfw(train, dev, model_path, outfile)
