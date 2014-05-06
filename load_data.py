# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import gzip
import pickle
import numpy as np

def load_weights(filename='all_weights.pickle.gz'):
    
    f = gzip.open(filename)
    all_weights = pickle.load(f)
    store_dept_weightDict = all_weights['store_dept_weightDict']
    store_dept_stdDict = all_weights['store_dept_stdDict']
    store_monthWeightDict = all_weights['store_monthWeightDict']
    store_month_stdDict = all_weights['store_month_stdDict']
    dept_monthWeightDict= all_weights['dept_monthWeightDict']
    dept_month_stdDict= all_weights['dept_month_stdDict']
    store_dept_monthWeightDict= all_weights['store_dept_monthWeightDict']
    store_dept_month_stdDict= all_weights['store_dept_month_stdDict']
    return store_dept_weightDict, store_dept_stdDict, store_monthWeightDict, store_month_stdDict, \
            dept_monthWeightDict, dept_month_stdDict, store_dept_monthWeightDict, store_dept_month_stdDict

def load_data(filename, shuffle_train=False):
    
    f = gzip.open(filename)
    all_data = pickle.load(f)    
    test = all_data['rawtest']
    train = all_data['rawtrain']
    
    if shuffle_train:
        train.reindex(np.random.permutation(train.index))

    return train, test

