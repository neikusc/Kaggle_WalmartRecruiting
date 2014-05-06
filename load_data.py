
import gzip
import pickle
import numpy as np


def load_data(filename, shuffle_train=False):
    
    f = gzip.open(filename)
    all_data = pickle.load(f)    
    test = all_data['rawtest']
    train = all_data['rawtrain']
    
    if shuffle_train:
        train.reindex(np.random.permutation(train.index))

    return train, test

