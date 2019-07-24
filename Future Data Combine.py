#!/usr/bin/env python
# coding: utf-8

# In[3]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv
import os
import netCDF4
from kolzur_filter import kz_filter, kzft, kzp, _kz_coeffs


# In[4]:


variablelist = ['psl', 'rhs', 'tas', 'sfcWind']


# In[5]:


time1 = '20360101-20451231'
time2 = '20460101-20551231'
time3 = '20860101-20951231'
time4 = '20960101-21001231'
time5 = '20400101-20491231'
time6 = '20500101-20591231'
time7 = '20900101-20991231'
time8 = '21000101-21001231'
time9 = '20351201-20451130'
time10 = '20451201-20551130'
time11 = '20851201-20951130'
time12 = '20951201-20991130'
time13 = '20951201-20991030'
time14 = '20991101-20991230'
time15 = '20401201-20451130'
time16 = '20451201-20501130'
time17 = '20411201-20511130'
time18 = '20911201-20991230'
time19 = '20991201-20991230'
time20 = '20060101-20551231'
time21 = '20560101-21001231'
time22 = '20410101-20451231'
time23 = '20460101-20501231'
time24 = '20910101-20951231'
time25 = '20960101-21001231'
time26 = '20060101-20151231'
time27 = '20160101-20251231'
time28 = '20110101-20151231'
time29 = '20160101-20201231'

#timelist = [time1, time2, time3, time4] #4
#timelist2 = [time5, time6, time7, time8] #4
#timelist3 = [time9, time10, time11, time12] #4
#timelist3a = [time9, time10, time11, time13, time14] #2+3
#timelist3b = [time17, time18] #2
#timelist3c = [time15, time16, time11, time12, time19] #2+3
#timelist4 = [time20, time21] #2
#timelist5 = [time22, time23, time24, time25]
timelist = [time26, time27]
timelist4 = [time20]
timelist5 = [time28, time29]


# In[6]:


# Models
# MRI-CGCM3, MIROC5, HadGEM2-ES, IPSL-CM5A-MR, NorESM1-M, CSIRO-MK3.6, GFDL-ESM2M, GFDL-ESM2G, then take an average.
model1 = 'MRI-CGCM3'
model2 = 'MIROC5'
model3 = 'HadGEM2-ES'
model4 = 'IPSL-CM5A-MR'
model5 = 'NorESM1-M'
model6 = 'CSIRO-MK3.6'
model7 = 'GFDL-ESM2M'
model8 = 'GFDL-ESM2G'
modellist = [model1, model2, model3, model4, model5, model6, model7, model8]


# In[7]:


# Experiments
# rcp26, rcp45, rcp60, rcp85
exp1 = 'rcp26'
exp2 = 'rcp45'
exp3 = 'rcp60'
exp4 = 'rcp85'
explist = [exp1, exp2, exp3, exp4]


# In[8]:


# Set the directory
directory = "Future Data Preprocess/"
if not os.path.exists(directory):
    os.makedirs(directory)


# In[9]:


def future_combine(variable, model, exp):
    directory_import = 'Future Data Average/' + exp + '/' + model + '/'
    if model == model1:
        times = timelist
    elif model == model2:
        times = timelist2
    elif model == model3:
        if exp == exp1:
            times = timelist3
        elif exp == exp2:
            times = timelist3a
        elif exp == exp3:
            times = timelist3b
        else:
            times = timelist3c
    elif model == model4:
        times = timelist4
    elif model == model5:
        times = timelist4
    elif model == model7:
        times = timelist5
    elif model == model8:
        times = timelist5
    
    # Model5 doesn't have wind data
    if (model == model5) and (variable == 'sfcWind'):
        return
            
    if len(times) == 4:
        timeA = times[0]
        timeB = times[1]
        ################
        timeC = times[2]
        timeD = times[3]
    elif len(times) == 2:
        timeA = times[0]
        ################
        timeB = times[1]
    elif len(times) == 1:
        timeA = times[0]
    else: # len = 5
        timeA = times[0]
        timeB = times[1]
        ################
        timeC = times[2]
        timeD = times[3]
        timeE = times[4]
    
    
    timestamp = []
    answer = []
    
    if len(times) == 5:
        path1 = directory_import + exp + '_' + model + '_' + variable + '_' + timeA + '.csv'
        path2 = directory_import + exp + '_' + model + '_' + variable + '_' + timeB + '.csv'
        path3 = directory_import + exp + '_' + model + '_' + variable + '_' + timeC + '.csv'
        path4 = directory_import + exp + '_' + model + '_' + variable + '_' + timeD + '.csv'
        path5 = directory_import + exp + '_' + model + '_' + variable + '_' + timeE + '.csv'
        pathlist = [path1, path2, path3, path4, path5]
        
    if len(times) == 4:
        path1 = directory_import + exp + '_' + model + '_' + variable + '_' + timeA + '.csv'
        path2 = directory_import + exp + '_' + model + '_' + variable + '_' + timeB + '.csv'
        path3 = directory_import + exp + '_' + model + '_' + variable + '_' + timeC + '.csv'
        path4 = directory_import + exp + '_' + model + '_' + variable + '_' + timeD + '.csv'
        pathlist = [path1, path2, path3, path4]
        
    if len(times) == 2:
        path1 = directory_import + exp + '_' + model + '_' + variable + '_' + timeA + '.csv'
        path2 = directory_import + exp + '_' + model + '_' + variable + '_' + timeB + '.csv'
        pathlist = [path1, path2]
    if len(times) == 1:
        path1 = directory_import + exp + '_' + model + '_' + variable + '_' + timeA + '.csv'
        pathlist = [path1]
    
    for p in range(len(pathlist)):
        path = pathlist[p]
        print(path)
        value = pd.read_csv(path, 'r')
        value = np.array(value)
        for v in range(len(value)):
            add = value[v][0].split(',')[1]
            time = value[v][0].split(',')[0]
            timestamp.append(time)
            answer.append(add)
    
    # 2013-2017
    cut1 = 0
    year = int(timestamp[cut1].split('-')[0])
    while(year < 2013):
        year = int(timestamp[cut1].split('-')[0])
        cut1 += 1
    cut1 -= 1
    cut2 = cut1
    while(year < 2018):
        year = int(timestamp[cut2].split('-')[0])
        cut2 += 1
    cut2 -= 1
    timestamp1 = timestamp[cut1:cut2]
    answer1 = answer[cut1:cut2]
    print(timestamp1[0], timestamp1[-1])
    
    resultMatrix1 = [[0 for x in range(2)] for y in range(len(timestamp1))]
    for t in range(len(resultMatrix1)):
        resultMatrix1[t][0] = timestamp1[t]
        resultMatrix1[t][1] = answer1[t]
    
    # Write csv file of 2013-2017
    with open(directory + exp + '_' + model + '_' + variable + '_' + ' 2013-2017.csv', "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        for val in resultMatrix1:
            writer.writerow(val)
    
    
    # 2045-2050
    #cut1 = 0
    #year = int(timestamp[cut1].split('-')[0])
    #while(year < 2045):
    #    year = int(timestamp[cut1].split('-')[0])
    #    cut1 += 1
    #cut1 -= 1
    #cut2 = cut1
    #while(year < 2051):
    #    year = int(timestamp[cut2].split('-')[0])
    #    cut2 += 1
    #cut2 -= 1
    #timestamp1 = timestamp[cut1:cut2]
    #answer1 = answer[cut1:cut2]
    #print(timestamp1[0], timestamp1[-1])
    
    
    #resultMatrix1 = [[0 for x in range(2)] for y in range(len(timestamp1))]
    #for t in range(len(resultMatrix1)):
    #    resultMatrix1[t][0] = timestamp1[t]
    #    resultMatrix1[t][1] = answer1[t]
    
    # 2095-2100
    #while(year < 2095):
    #    year = int(timestamp[cut2].split('-')[0])
    #    cut2 += 1
    #cut2 -= 1
    #timestamp2 = timestamp[cut2:]
    #answer2 = answer[cut2:]
    #print(timestamp2[0], timestamp2[-1])
    
    #resultMatrix2 = [[0 for x in range(2)] for y in range(len(timestamp2))]
    #for t in range(len(resultMatrix2)):
    #    resultMatrix2[t][0] = timestamp2[t]
    #    resultMatrix2[t][1] = answer2[t]
    
    # Write csv file of 2045-2050
    #with open(directory + exp + '_' + model + '_' + variable + '_' + ' 2045-2050.csv', "w") as output:
    #    writer = csv.writer(output, lineterminator='\n')
    #    for val in resultMatrix1:
    #        writer.writerow(val)
    
    # Write csv file of 2095-2100
    #with open(directory + exp + '_' + model + '_' + variable + '_' + ' 2095-2100.csv', "w") as output:
    #    writer = csv.writer(output, lineterminator='\n')
    #    for val in resultMatrix2:
    #        writer.writerow(val)


# In[13]:


# Testing
for i in range(len(variablelist)):
    variable = variablelist[i]
    future_combine(variable, model4, exp4)


# In[ ]:




