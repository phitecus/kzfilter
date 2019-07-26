#!/usr/bin/env python
# coding: utf-8

# In[90]:


# 2. update_province
# This is to update province column from regression result
import os
import numpy as np
import pandas as pd
import csv
import matplotlib.pyplot as plt
import glob


# In[91]:


# Import Files (china): daily data
directory_import = 'china/'
filelist = []

# Read csv files from folder
for files in glob.glob(directory_import + '*.csv'):
    print(files)
    filelist.append(files)


# In[92]:


grid_import = 'grid_entire_china/'
gridlist = []
location_dic = {}

# Read txt files from folder
for files in glob.glob(grid_import + '*.txt'):
    txtfile = files.split('/')[1]
    gridlist.append(txtfile)
print(len(gridlist))
print(gridlist)


# In[93]:


def province(file):
    x = [] # latitude: 73-135E
    y = [] # longitude: 18-54N
    finalrow = 0
    finalcol = 0
    degree = 0.01

    with open(grid_import + file) as f:
        lines = f.readlines()
        for rows, value in enumerate(lines):
            finalrow += 1
            value = value.split()
            #print(rows, len(value))
            value = np.array(value)
            value = np.asfarray(value, 'int')
            #print(rows, value[1])
            for col in range(len(value)):
                #print(rows, col, value[col])
                finalcol = col
                if value[col] < 1: # if equal to zero
                    #print('Hi')
                    x.append(col)
                    y.append(rows)

    #x_degree = (135-73)/finalcol = 0.01
    #y_degree = (54-18)/finalrow = 0.01

    x = [73 + x*degree for x in x]
    y = [54 - y*degree for y in y]
    #print(len(x), len(y), finalrow, finalcol, x_degree, y_degree)
    
    name_province = file[:-4]
    # Update location dictionary
    location_dic[name_province] = [(x[0], y[0])]
    for t in range(len(x)):
        location_dic[name_province].append((x[t], y[t]))

    #fig = plt.figure()
    #plt.title(name_province, fontsize=20)
    #plt.plot(x, y, label = file[:-4])
    #plt.show()
    #fig.savefig(grid_import + name_province + '.png')
    #plt.close()
    # Guangdong: 23° 7' 44.3784'' N and 113° 15' 11.7000'' E


# In[95]:


turn = 0
for grid in range(len(gridlist)):
    turn += 1
    if grid != 8:  # exclude china
        print(turn, gridlist[grid])
        province(gridlist[grid])


# In[96]:


print(location_dic.keys())


# In[97]:


def find_province(lon, lat):
    bool = False
    for key, value in location_dic.items():
        if (lon, lat) in location_dic[key]:
            bool = True
            if bool == True:
                return key
    return 1


# In[101]:


# for each station, find province
for f in range(len(filelist)):
    if f==5 or f==6: #
        new_column = []
        print(filelist[f])
        file = filelist[f]
        timestamp = []
        station = []
        latitude = []
        longitude = []
        values = []
        variable = file.split('_')[1]
        print('Variable: ', variable)

        with open(file) as infile:
            reader = csv.reader(infile)
            for rows, value in enumerate(reader):
                if rows == 0:
                    print(value)
                if rows == 4:
                    unit = value[0]
                if rows == 5:
                    station.append(value)
                if rows == 6:
                    latitude.append(value)
                if rows == 7:
                    longitude.append(value)
                if rows > 8:
                    date = value[0].split()[0]
                    timestamp.append(date)
                    values.append(value[1:])
        station = station[0][1:]
        latitude = latitude[0][1:]
        longitude = longitude[0][1:]
        print(station[0], latitude[0], longitude[0], timestamp[0], values[0][0], unit) #[time][station]
        print('Total stations:', len(station), '; Total number of days:', len(timestamp))
        print("\n")


        # Check station by station
        values = np.array(values)
        values = np.asfarray(values, 'float')
        #### start the loop: len(station)
        for s in range(len(station)):
            subplot_matrix = []
            data = values[:,s]
            time = timestamp
            # Find location and its province
            lat = round(float(latitude[s]), 2)
            lon = round(float(longitude[s]), 2)
            print(lon,lat)
            correction = 0
            province_answer = find_province(lon, lat)
            #print(province_answer)
            #print("\n")

            # If cannot find the province, approximate
            correction = 0
            if province_answer == 1:
                #lat = round(lat)
                #lon = round(lon)
                #print(lon, lat, correction)
                #province_answer = find_province(lon, lat)

                while province_answer == 1:
                    # 1st correction
                    if province_answer == 1:
                        #print('1st', lon + correction, lat, correction)
                        province_answer = find_province(lon + correction, lat)
                    # 2nd
                    if province_answer == 1:
                        #print('2nd', lon, lat + correction, correction)
                        province_answer = find_province(lon, lat + correction)
                    # 3rd
                    if province_answer == 1:
                        #print('3rd', lon + correction, lat + correction, correction)
                        province_answer = find_province(lon + correction, lat + correction)
                    # 4th
                    if province_answer == 1:
                        #print('4th', lon, lat - correction, correction)
                        province_answer = find_province(lon, lat - correction)
                    # 5th
                    if province_answer == 1:
                        #print('5th', lon - correction, lat, correction)
                        province_answer = find_province(lon - correction, lat)
                    # 6th
                    if province_answer == 1:
                        #print('6th', lon - correction, lat - correction, correction)
                        province_answer = find_province(lon - correction, lat - correction)
                    correction += 0.01
                #print("\n")

            # End Approximation
            new_column.append(province_answer)
            print(s+1, variable, station[s], province_answer)
            print("\n")
        ### End of Loop of stations ###

        # Check Directory to import csv files and make new directory
        directory_import = 'China Regression/' + variable + '/'
        directory = 'China Regression/'
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Import Result Matrix
        df = pd.read_csv(directory_import + variable + ' regression results.csv')

        # Update regression province
        new_column = pd.Series(new_column, name = 'province', index = [x for x in range(len(new_column))])
        df.update(new_column)

        # save matrix
        #print(df)
        df.to_csv(directory + variable + ' regression results.csv')


# In[102]:


# Analyze distribution of coefficients
for f in range(len(filelist)):
    #if f==1 or f==2 or f==4: #FSPMC, RSPMC, O3
    #if f==1:
    print(filelist[f])
    file = filelist[f]
    variable = file.split('_')[1]
    print('Variable: ', variable)

    # Make Directory
    directory = 'China Regression/'
    directory_save = directory + 'distribution/' + variable + '/'
    if not os.path.exists(directory_save):
        os.makedirs(directory_save)

    # Read files
    df = pd.read_csv(directory + variable + ' regression results.csv')
    header = list(df)
    header = header[2:]

    # Intercept & regression coefficients
    df = np.array(df)
    for d in range(2, len(df[0])-1): # Except the first two columns and last column
        coef = pd.Series(df[:,d])
        coef = coef[coef<1000]
        coef = coef[coef>-1000]
        coef = coef[coef!=0]
        coef.plot.hist(grid=True, bins=20, rwidth=0.9, color='#607c8e')
        #fig = plt.figure(figsize=(20, 9))
        plt.title(header[d-2])
        plt.xlabel('Regression Coefficients')
        plt.ylabel('Counts')
        plt.grid(axis='y', alpha=0.75)
        plt.savefig(directory_save + header[d-2] + ' distribution.png')
        plt.show()
        plt.close()

    # Last Column is province
    prov = pd.Series(df[:,-1])
    print(prov.value_counts())
    prov.value_counts().plot.bar(color='#607c8e')
    plt.title('Province Distribution')
    plt.xlabel('Province')
    plt.ylabel('Counts')
    plt.grid(axis='y', alpha=0.75)
    plt.savefig(directory_save + 'province count' + ' distribution.png')
    plt.show()
    plt.close()


# In[ ]:




