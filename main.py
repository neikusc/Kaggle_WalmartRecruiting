# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

# ============***================ #
# Author: Kien Trinh, Physics PhD #
# ============***================ #

import time
import numpy as np
import pandas as pd
import pickle, gzip

from datetime import datetime
from sklearn.ensemble import ExtraTreesRegressor

# user-defined functions
from funcs import *
from load_data import *

# <codecell>

vars = {'var1'   :   ['IsHoliday','beHoliday','afHoliday','Size','Temperature','Fuel_Price','CPI','Unemployment', 
                      'TypeA','TypeB','TypeC','store_weight','store_std','store_month_weight','store_month_std','haveMarkDown',
                      'MarkDown1','MarkDown2','MarkDown3','MarkDown4','MarkDown5','Feb','Apr','Oct','Nov','Dec','Other_Month']}

# <codecell>

''''Load merged data and do build new features such as types of stores, months with high sales, ...'''

train, test = rawProcess()

all_data = {"rawtrain": train,
            "rawtest": test}
print "Saving dataset."
pickle.dump(all_data, gzip.open('dataMerged00.pickle.gz','w'), protocol=pickle.HIGHEST_PROTOCOL)

# <codecell>

if __name__ == '__main__':
    t0 = time.clock()
    seed = 2014
    
    rawtrain, rawtest = load_data('dataMerged00.pickle.gz', shuffle_train = seed)
    
    rawtrain = rawtrain.set_index('Id')
    rawtest = rawtest.set_index('Id')
    rawtrain['predWeekly_Sales'] = 0.
    rawtest['Weekly_Sales'] = 0.
    
    w = rawtrain['IsHoliday'].values
    
    globalDept_Weight_Dict, globalDept_std_Dict = globalDeptWeight(rawtrain)
    global_dept_month_WeightDict, global_dept_month_stdDict = globalDeptWeight_by_Month(rawtrain)

    
    for dept in np.sort(rawtest['Dept'].unique()):
        finetrain, finetest =  fineProcess(rawtrain, rawtest, dept,
                                    globalDept_Weight_Dict, globalDept_std_Dict,
                                    global_dept_month_WeightDict, global_dept_month_stdDict)
    
        target = finetrain['Weekly_Sales'].values
        train = finetrain[vars['var1']].values
        test = finetest[vars['var1']].values
        
        model = ExtraTreesRegressor(n_estimators = 20, n_jobs=-1, bootstrap=True, oob_score=True)
        
        # fit log of weekly sales
        model.fit(train, fw_log_transform(target) )
        pred_test = bw_log_transform(model.predict(test))
        pred_train = bw_log_transform(model.oob_prediction_)
        
        rawtest.ix[finetest.index,'Weekly_Sales'] = np.round(pred_test,2)
        rawtrain.ix[finetrain.index,'predWeekly_Sales'] = np.round(pred_train,2)
        
        print 'Local WMAE: ', wmae(finetrain['Weekly_Sales'], pred_train, finetrain['IsHoliday']),' at Dept: ', dept
    
    print 'Global WMAE on training set: ', wmae(rawtrain['Weekly_Sales'], rawtrain['predWeekly_Sales'], w)
    
    rawtest['Id'] = rawtest.index
    rawtest[['Id','Weekly_Sales']].to_csv("submission.csv", index=False)

    print 'Running time = ' + str(time.clock() - t0)

# <codecell>


