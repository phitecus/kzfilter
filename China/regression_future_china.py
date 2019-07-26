#!/usr/bin/env python
# coding: utf-8

# In[6]:


# Input the future climate variables into the relationship and predict future 
# 2045-2050 and 2095-2100


# In[10]:


# 1. Regression_china
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv
import os
import math
from kolzur_filter import kz_filter, kzft, kzp, _kz_coeffs
import functions
import glob
import netCDF4
import statsmodels.formula.api as smf


# In[7]:


model1 = 'MRI-CGCM3'
model2 = 'MIROC5'
model3 = 'HadGEM2-ES'
model4 = 'IPSL-CM5A-MR'
model5 = 'NorESM1-M'
model6 = 'CSIRO-MK3.6'
model7 = 'GFDL-ESM2M'
model8 = 'GFDL-ESM2G'
modellist = [model1, model2, model3, model4, model5, model6, model7, model8]


# In[11]:


# Import Files (china): daily data
directory_import = 'china/'
filelist = []

# Read csv files from folder
for files in glob.glob(directory_import + '*.csv'):
    print(files)
    filelist.append(files)


# In[8]:


# Experiments
# rcp26, rcp45, rcp60, rcp85
exp1 = 'rcp26'
exp2 = 'rcp45'
exp3 = 'rcp60'
exp4 = 'rcp85'
explist = [exp1, exp2, exp3, exp4]


# In[12]:


# Pressure, Relative humidity, Tmax, Wind Speed, PBLH, Rad
variablelist = ['psl', 'rhs', 'tasmax', 'uas', 'vas', 'pblh', 'swgdn']


# In[ ]:




