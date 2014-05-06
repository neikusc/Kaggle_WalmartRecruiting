# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import numpy as np
import pandas as pd
from datetime import datetime

# <codecell>

def rawProcess():
    '''    Markdowns were filled with median from R program. Type is converted to 3 binary types: A, B, C.    '''
    
    cols = ['Id','Store','Dept','Store_Dept','Month','Store_Month','Dept_Month','StoreDept_Month','IsHoliday','beHoliday',
            'afHoliday','Type','TypeA','TypeB','TypeC','Size','Temperature','Fuel_Price','CPI','Unemployment','haveMarkDown',        
            'MarkDown1','MarkDown2','MarkDown3','MarkDown4','MarkDown5','Feb','Apr','Oct','Nov','Dec','Other_Month']
    
    rawtrain = pd.read_csv('/home/neik/Kaggle/WalmartRecruiting/CSV/trainMerged.csv')
    
    rawtrain['Id'] = rawtrain.Store.map(str)+'_'+ rawtrain.Dept.map(str)+'_'+rawtrain.Date.map(str)
    rawtrain['beHoliday'] = np.roll(rawtrain['IsHoliday'],-1)
    rawtrain['afHoliday'] = np.roll(rawtrain['IsHoliday'], 1)
    rawtrain['TypeA'] = (rawtrain['Type']=='A').astype(int)
    rawtrain['TypeB'] = (rawtrain['Type']=='B').astype(int)
    rawtrain['TypeC'] = (rawtrain['Type']=='C').astype(int)
    
    rawtrain['Month'] = [datetime.strptime(x,"%Y-%m-%d").month for x in rawtrain['Date']]
    rawtrain['Feb'] = (rawtrain['Month']==2).astype(int)
    rawtrain['Apr'] = (rawtrain['Month']==4).astype(int)
    rawtrain['Oct'] = (rawtrain['Month']==10).astype(int)
    rawtrain['Nov'] = (rawtrain['Month']==11).astype(int)
    rawtrain['Dec'] = (rawtrain['Month']==12).astype(int)
    rawtrain['Other_Month'] = [1 if x not in [2,4,10,11,12] else 0 for x in rawtrain['Month']]
    
    rawtrain['Store_Dept'] = rawtrain.Store.map(str)+'_'+rawtrain.Dept.map(str)
    rawtrain['Dept_Month'] = rawtrain.Dept.map(str)+'_'+rawtrain.Month.map(str)
    rawtrain['Store_Month'] = rawtrain.Store.map(str)+'_'+rawtrain.Month.map(str)
    rawtrain['StoreDept_Month'] = rawtrain.Store.map(str)+'_'+rawtrain.Dept_Month.map(str)
    
    rawtest = pd.read_csv('/home/neik/Kaggle/WalmartRecruiting/CSV/testMerged.csv')
    
    rawtest['Id'] = rawtest.Store.map(str)+'_'+ rawtest.Dept.map(str)+'_'+rawtest.Date.map(str)
    rawtest['beHoliday'] = np.roll(rawtest['IsHoliday'],-1)
    rawtest['afHoliday'] = np.roll(rawtest['IsHoliday'], 1)
    rawtest['TypeA'] = (rawtest['Type']=='A').astype(int)
    rawtest['TypeB'] = (rawtest['Type']=='B').astype(int)
    rawtest['TypeC'] = (rawtest['Type']=='C').astype(int)
    
    rawtest['Month'] = [datetime.strptime(x,"%Y-%m-%d").month for x in rawtest['Date']]
    rawtest['Feb'] = (rawtest['Month']==2).astype(int)
    rawtest['Apr'] = (rawtest['Month']==4).astype(int)
    rawtest['Oct'] = (rawtest['Month']==10).astype(int)
    rawtest['Nov'] = (rawtest['Month']==11).astype(int)
    rawtest['Dec'] = (rawtest['Month']==12).astype(int)
    rawtest['Other_Month'] = [1 if x not in [2,4,10,11,12] else 0 for x in rawtest['Month']]

    rawtest['Store_Dept'] = rawtest.Store.map(str)+'_'+rawtest.Dept.map(str)
    rawtest['Dept_Month'] = rawtest.Dept.map(str)+'_'+rawtest.Month.map(str)
    rawtest['Store_Month'] = rawtest.Store.map(str)+'_'+rawtest.Month.map(str)
    rawtest['StoreDept_Month'] = rawtest.Store.map(str)+'_'+rawtest.Dept_Month.map(str)
    
    rawtrain = rawtrain[cols + ['Weekly_Sales']]
    rawtest = rawtest[cols]
    
    return rawtrain, rawtest

# <codecell>

def localDeptWeight(data_train, dept_numb):
    '''This weight is for single store by department'''
    
    rawdata = data_train.ix[data_train['Dept']==dept_numb]
    store = rawdata['Store'].unique()
    storeSale = [np.mean(rawdata.ix[rawdata['Store']==i,'Weekly_Sales']) for i in store]
    store_Weight_Dict = dict(zip(store, storeSale/np.mean(storeSale)))
    
    store_stdSale = [np.std(rawdata.ix[rawdata['Store']==i,'Weekly_Sales']) for i in store]
    store_std_Dict = dict(zip(store, store_stdSale/np.mean(store_stdSale)))
    return store_Weight_Dict, store_std_Dict

def localDeptWeight_by_Month(data_train, dept_numb):
    '''This weight is for single store in a month by department'''
    
    rawdata = data_train.ix[data_train['Dept']==dept_numb]
        
    # unique store_month
    store_month = rawdata['Store_Month'].unique()
    store_month_Sale = [np.mean(rawdata.ix[rawdata['Store_Month']==i,'Weekly_Sales']) for i in store_month]
    store_month_WeightDict = dict(zip(store_month, store_month_Sale/np.mean(store_month_Sale)))
    
    store_month_stdSale = [np.std(rawdata.ix[rawdata['Store_Month']==i,'Weekly_Sales']) for i in store_month]
    store_month_stdDict = dict(zip(store_month, store_month_stdSale/np.mean(store_month_stdSale)))
    
    return store_month_WeightDict, store_month_stdDict

def globalDeptWeight(rawdata):
    '''This global weight for single store by department'''
    
    store = rawdata['Store'].unique()
    storeSale = [np.mean(rawdata.ix[rawdata['Store']==i,'Weekly_Sales']) for i in store]
    globalStore_Weight_Dict = dict(zip(store, storeSale/np.mean(storeSale)))
    
    store_stdSale = [np.std(rawdata.ix[rawdata['Store']==i,'Weekly_Sales']) for i in store]
    globalStore_std_Dict = dict(zip(store, store_stdSale/np.mean(store_stdSale)))
    return globalStore_Weight_Dict, globalStore_std_Dict

def globalDeptWeight_by_Month(rawdata):
    '''This weight is for single store in a month by department'''
    
    # unique store_month
    store_month = rawdata['Store_Month'].unique()
    store_month_Sale = [np.mean(rawdata.ix[rawdata['Store_Month']==i,'Weekly_Sales']) for i in store_month]
    global_store_month_WeightDict = dict(zip(store_month, store_month_Sale/np.mean(store_month_Sale)))
    
    store_month_stdSale = [np.std(rawdata.ix[rawdata['Store_Month']==i,'Weekly_Sales']) for i in store_month]
    global_store_month_stdDict = dict(zip(store_month, store_month_stdSale/np.mean(store_month_stdSale)))
    
    return global_store_month_WeightDict, global_store_month_stdDict

def fineProcess(data_train, data_test, dept_numb,
                globalStore_Weight_Dict, globalStore_std_Dict,
                global_store_month_WeightDict, global_store_month_stdDict):
    '''--- Calculate the weights of stores and departments ---'''
    
    cols = ['IsHoliday','beHoliday','afHoliday','Size','Temperature','Fuel_Price','CPI','Unemployment', 
            'TypeA','TypeB','TypeC','store_weight','store_std','store_month_weight','store_month_std','haveMarkDown',
            'MarkDown1','MarkDown2','MarkDown3','MarkDown4','MarkDown5','Feb','Apr','Oct','Nov','Dec','Other_Month']            

    store_weight_Dict, store_std_Dict = localDeptWeight(data_train, dept_numb)
    store_month_weightDict, store_month_stdDict = localDeptWeight_by_Month(data_train, dept_numb)
    
    # Cleaning training set        
    rawtrain = data_train.ix[data_train['Dept']==dept_numb]

    rawtrain['store_weight']=[store_weight_Dict[i] for i in rawtrain['Store']]
    rawtrain['store_std']=[store_std_Dict[i] for i in rawtrain['Store']]
    rawtrain['store_month_weight']=[store_month_weightDict[i] for i in rawtrain['Store_Month']]
    rawtrain['store_month_std']=[store_month_stdDict[i] for i in rawtrain['Store_Month']]
       
    # cleaning testing set    
    rawtest = data_test.ix[data_test['Dept']==dept_numb]

    sw = [];    ss = []
    store_keys = store_weight_Dict.keys()
    for i in rawtest['Store']:
        if i in store_keys:
            sw += [store_weight_Dict[i]]
            ss += [store_std_Dict[i]]
        else:
            sw += [globalStore_Weight_Dict[i]]
            ss += [globalStore_std_Dict[i]]  
    rawtest['store_weight'] = sw
    rawtest['store_std'] = ss
    
    smw = [];    sms = []
    store_month_keys = store_month_weightDict.keys()
    for i in rawtest['Store_Month']:
        if i in store_month_keys:
            smw += [store_month_weightDict[i]]
            sms += [store_month_stdDict[i]]
        else:
            smw += [global_store_month_WeightDict[i]]
            sms += [global_store_month_stdDict[i]]        
    rawtest['store_month_weight']=smw
    rawtest['store_month_std']=sms
    
    rawtrain = rawtrain[cols + ['Weekly_Sales']]
    rawtest = rawtest[cols]
    
    return rawtrain, rawtest

# <codecell>

def wmae(y0,y,wx):
    ''' Weighted Mean Absolute Value'''
    w = 4.*wx + 1.
    temp = np.absolute(y-y0)
    result = 1.0*np.dot(temp, w)/np.sum(w)
    return result

# <codecell>

def fw_transform(target,lbd):
    '''Box-Cox forward transformation'''
    target[target<-1000] = -1000
    temp = target+1001
    target = (np.power(temp,lbd)-1)/lbd
    return target
def bw_transform(target,lbd):
    '''Box-Cox backward transformation'''
    temp = np.power(lbd*target,1./lbd)    
    target = temp-1001
    return target

# <codecell>

def fw_log_transform(target):
    '''Log forward transformation'''
    temp = target/500. + 10.
    target = np.log(temp)
    return target

def bw_log_transform(target):
    '''Log backward transformation'''
    temp = np.exp(target)
    target = 500*(temp-10.)
    return target

