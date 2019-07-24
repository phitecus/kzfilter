#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv
import os
import netCDF4
from kolzur_filter import kz_filter, kzft, kzp, _kz_coeffs


# In[2]:


variablelist = ['psl', 'rhs', 'tas', 'sfcWind']


# In[3]:


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


# In[4]:


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


# In[5]:


# Experiments
# rcp26, rcp45, rcp60, rcp85
exp1 = 'rcp26'
exp2 = 'rcp45'
exp3 = 'rcp60'
exp4 = 'rcp85'
explist = [exp1, exp2, exp3, exp4]


# In[6]:


# latitude = 100 # Latitude range from -90 to 90: len(lat) = 160
# longitude = 102 # Longitude range from 0 to 360: len(lon) = 320
# Eastern: 22.3036, 114.1719
# Tap Mun: 22.3036, 114.1719
# Tsuen Wan: 22.3594, 114.2153 ###
# Tung Chung: 22.2911, 113.9069
# Yuen Long: 22.4706, 113.9811
# Kwai Chung: 22.3594, 114.2153 ###
# Kwun Tong: 22.3147, 114.2233 ###
# Macau: 22.1600, 113.5650
# Sha Tin: 22.3036, 114.1719
# Sham Shui Po: 22.3315, 114.1567

location = [[99,101],[79,81],[90,61],[89,46],[59,46],[100,102],[56,45],[56,45]] # Order follows model


# In[7]:


# Set the directory
directory = "Future Data Average/"
if not os.path.exists(directory):
    os.makedirs(directory)


# In[8]:


def future(variable, time, model, exp):
    # Model5 does not have wind data
    if model == model5 and variable == 'sfcWind':
        return
    
    path = exp + '/' + model + '/' + variable + '_day_' + model + '_' + exp + '_r1i1p1_' + time + '.nc'
    print(path)
    # Set the directory
    directory_save = "Future Data Average/" + exp + '/' + model + '/'
    if not os.path.exists(directory_save):
        os.makedirs(directory_save)
    # Read nc files
    nc = netCDF4.Dataset(path, mode='r')
    nc.variables.keys()
    
    lat = nc.variables['lat'][:]
    lon = nc.variables['lon'][:]
    time_var = nc.variables['time']
    dtime = netCDF4.num2date(time_var[:], time_var.units)
    if variable == 'psl':
        var = nc.variables['psl'][:]
        units = 'Pa'
    elif variable == 'rhs':
        var = nc.variables['rhs'][:]
        units = '%'
    elif variable == 'tas':
        var = nc.variables['tas'][:] - 273
        units = 'Celcius'
    else:
        var = nc.variables['sfcWind'][:]
        units = 'm/s'
    # Eastern: 22.3036, 114.1719
    #latitude = 100 # Latitude range from -90 to 90: len(lat) = 160
    #longitude = 102 # Longitude range from 0 to 360: len(lon) = 320
    print('Latitude =', lat[latitude], '; Longitude =', lon[longitude])
    y = []
    for i in range(len(var)):
        y.append(var[i][latitude][longitude])
    x = dtime
    
    # Write csv files into 'Future Data Average/'
    matrix = pd.Series(y, index=x) 
    matrix.to_csv(directory_save + exp + '_' + model + '_' + variable + '_' + time + '.csv', index=True, header=True)
    
    # KZ Filter and Graph
    #m = 29
    #k = 3
    #y = np.array(y)
    #y = kz_filter(y, m ,k)
    #w = int(k * (m - 1) / 2)
    #x = x[w:-w]
    #plt.plot(x,y)
    #plt.xlabel('Time')
    #plt.ylabel(variable + ' (' + units + ')')
    #plt.title(exp + '_' + model + '_' + variable + '_' + time)
    #plt.show()


# In[9]:


# Testing
for j in range(len(variablelist)):
    for k in range(len(timelist4)):
        variable = variablelist[j]
        time = timelist4[k]
        latitude = location[3][0]  # [i][0]
        longitude = location[3][1] # [i][1]
        future(variable, time, model4, exp1)


# In[ ]:




