#!/usr/bin/env python
# coding: utf-8

# In[1]:


# 3. detrend_china after update_province (according to each province)
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv
import os
from kolzur_filter import kz_filter, kzft, kzp, _kz_coeffs
import functions
import glob
import netCDF4


# In[6]:


# Import Files (china): daily data
directory_import = 'china/'
filelist = []


# In[7]:


# Read csv files from folder
for files in glob.glob(directory_import + '*.csv'):
    print(files)
    filelist.append(files)


# In[5]:


# Group of provinces
grid_import = 'grid_entire_china/'
gridlist = []
# Read txt files from folder
for files in glob.glob(grid_import + '*.txt'):
    txtfile = files.split('/')[1]
    gridlist.append(txtfile[:-4])
print(len(gridlist))
print(gridlist)


# In[4]:


# Import province list which is after regression
#df = pd.read_csv('China Regression/O3 regression results.csv')
#province_list = df['province']


# In[21]:


minimum_len = 3*365 # 3 years
for f in range(len(filelist)): 
    #if f == 1 or f == 2 or f == 4: # FSPMC, RSPMC, O3
    if f < 5: # except PRE and CO 
        # Make lists for each group of provinces
        result_dic = {}
        count_dic = {}
        for i in range(len(gridlist)):
            name = gridlist[i] # name = province
            result_dic[name] = [0]
            count_dic[name] = 0

        print(filelist[f])
        file = filelist[f]
        timestamp = []
        station = []
        latitude = []
        longitude = []
        values = []
        variable = file.split('_')[1]
        print('Variable: ', variable)
        
        # Import province list which is after regression
        df = pd.read_csv('China Regression/' + variable  + ' regression results.csv')
        province_list = df['province']

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


        # Detrend station by station
        values = np.array(values)
        values = np.asfarray(values, 'float')
        
        # Make Directory
        directory = 'China Detrend/' + variable + '/'
        if not os.path.exists(directory):
             os.makedirs(directory)
        
        # Start loop for each station: len(station)
        for s in range(len(station)):
            subplot_matrix = []
            data = values[:,s]
            time = timestamp
            # Find location and its province
            lat = round(float(latitude[s]), 2)
            lon = round(float(longitude[s]), 2)
            print(lon,lat)
            correction = 0
            # Find the province
            province_answer = province_list[s]
            # Count the province
            print(province_answer)
            count_dic[province_answer] += 1
            result_dic[province_answer].append(s+1) # avoid the first column

            # Find negative values
            delete_index = []
            non_delete = []
            for i in range(len(data)):
                if data[i] < 0:
                    delete_index.append(i)
                else:
                    non_delete.append(i)

            if len(delete_index) != 0:
                # Cut the tail if necessary
                last_index = len(data) - 1
                if delete_index[-1] + 1 == len(data):
                    last_index = non_delete[-1]
                    data = data[:last_index+1]
                    time = time[:last_index+1]
                    # Find negative values again with new data
                    delete_index = []
                    for i in range(len(data)):
                        if data[i] < 0:
                            delete_index.append(i)

                # Cut the head if necessary
                first_index = 0
                if len(delete_index) !=0 and delete_index[0] == 0:
                    first_index = non_delete[0]
                    data = data[first_index:]
                    time = time[first_index:]
                    # Find negative values again with new data
                    delete_index = []
                    for i in range(len(data)):
                        if data[i] < 0:
                            delete_index.append(i)

                # Make Positive
                if len(delete_index) != 0:
                    for j in range(len(delete_index)):
                        data[delete_index[j]] = functions.findPositive(data, delete_index[j])

            print(s+1, station[s], len(data), len(time), time[0])



            # KZ Filter
            if len(data) > minimum_len: # at least 3 years
                m = 29
                k = 3
                w = int(k*(m-1)/2)
                data = np.array(data)
                x = data # original data
                data = np.log(data)
                baseline = kz_filter(data, m, k)
                #fig = plt.figure()
                #ax = plt.axes()  # Create axis
                #ax.grid(True)
                t = np.array(time)
                t_bl = t[w:-w]
                subplot_matrix.append([t, data, t_bl, baseline])

                # W(t) = O(t) – KZ15,5: Short term component
                m = 15
                k = 5
                w = int(k*(m-1)/2)
                original = x[w:-w]
                short = original - kz_filter(x, m, k)
                #plt.plot(t[w:-w], short, label="Short term component")
                subplot_matrix.append([t[w:-w], short])

                # S(t) = KZ15,5 – KZ365,3: Seasonal component
                m = 365
                k = 3
                long = kz_filter(x, m, k)
                w = int(k * (m - 1) / 2)
                window = int((len(short)-len(long))/2)
                seasonal = kz_filter(x, 15, 5)[window:-window] - long
                #plt.plot(t[w:-w], seasonal, label="Seasonal Component")
                subplot_matrix.append([t[w:-w], seasonal])

                # e(t) = KZ365,3: Long term component
                subplot_matrix.append([t[w:-w], long])

                # Subplot
                fig = plt.figure(figsize=(20, 9))
                for count in range(len(subplot_matrix)):
                    data = subplot_matrix[count]
                    plt.subplot(2, 2, count + 1)
                    ax = fig.add_subplot(2, 2, count + 1)
                    if count == 0:
                        plt.plot(data[0], data[1], label= variable)
                        plt.plot(data[2], data[3], label='Baseline')
                        plt.legend(loc='best')
                    else:
                        plt.plot(data[0], data[1])
                    ax.xaxis.set_major_locator(plt.MaxNLocator(5))  # Set Maximum number of x-axis values to show
                    fig.autofmt_xdate()
                    if count == 0:
                        titles = 'Log-transformed daily ' + variable
                        plt.ylabel('ln(' + unit + ')', fontsize=15)
                    elif count == 1:
                        titles = 'Short Term Component'
                        plt.ylabel("Short Term", fontsize=15)
                    elif count == 2:
                        titles = 'Seasonal Term Component'
                        plt.ylabel("Seasonal Term", fontsize=15)
                    else:
                        titles = 'Long Term Component'
                        plt.ylabel("Long Term", fontsize=15)
                    plt.title(titles, fontsize=18)

                plt.tight_layout()
                fig.suptitle(station[s] + ' (' + province_answer + '), ' + variable, fontsize=18)
                fig.savefig(directory + station[s] + ' (' + province_answer + '), ' + variable + ' detrend.png')
                #plt.show()
                plt.close()
                print('\n')

        ### End loop for station

        # Group for each Province
        directory_province = directory + 'province/'
        if not os.path.exists(directory_province):
            os.makedirs(directory_province)
        #print(count_dic)
        #print(result_dic)

        # Loop for each Province
        for p in range(len(gridlist)):
            key = gridlist[p] # key is the name of province
            if count_dic[key] != 0: # if not empty

                # Make dataframe with certain column
                # 1. Make the dataframe
                df = pd.read_csv(filelist[f], skiprows = 5, low_memory=False)

                # 2. Choose only the given columns
                column_list = result_dic[key]
                df = df.iloc[:, column_list]

                # 3. Save the data into directory_province
                df.to_csv(directory_province + key + '.csv')

                # 4. Make average if not less than zero for each row
                #mean_col = [x+1 for x in range(len(column_list)-1)] # calculate mean except first column
                #df['mean'] = df.iloc[:,mean_col][3:].mean(axis=1, skipna = True) # calculate mean for rows > 3 (value > 0)
                #print(df['mean'])
                df = np.array(df)
                df = df[3:]
                #print(df)
                data = [] # list of mean
                for rows in range(len(df)):
                    mean = 0
                    count = 0
                    for cols in range(1, len(df[rows])):
                        value = float(df[rows][cols])
                        if value > 0:
                            mean += value
                            count += 1
                    if count != 0:
                        mean = mean / count
                    else:
                        mean = 0
                    data.append(mean)
                
                # Make positive data
                delete_index2 = []
                for i in range(len(data)):
                    if data[i] == 0:
                        delete_index2.append(i)
                if len(delete_index2) != 0:
                    for j in range(len(delete_index2)):
                        data[delete_index2[j]] = functions.findPositive(data, delete_index2[j])
                
                # Start Detrend
                ######
                subplot_matrix = []
                m = 29
                k = 3
                w = int(k*(m-1)/2)
                data = np.array(data)
                data = np.log(data)
                baseline = kz_filter(data, m, k)
                #fig = plt.figure()
                #ax = plt.axes()  # Create axis
                #ax.grid(True)
                t = np.array(time)
                t_bl = t[w:-w]
                subplot_matrix.append([t, data, t_bl, baseline])

                # W(t) = O(t) – KZ15,5: Short term component
                m = 15
                k = 5
                w = int(k*(m-1)/2)
                original = data[w:-w]
                short = original - kz_filter(data, m, k)
                #plt.plot(t[w:-w], short, label="Short term component")
                subplot_matrix.append([t[w:-w], short])

                # S(t) = KZ15,5 – KZ365,3: Seasonal component
                m = 365
                k = 3
                long = kz_filter(data, m, k)
                w = int(k * (m - 1) / 2)
                window = int((len(short)-len(long))/2)
                seasonal = kz_filter(data, 15, 5)[window:-window] - long
                #plt.plot(t[w:-w], seasonal, label="Seasonal Component")
                subplot_matrix.append([t[w:-w], seasonal])

                # e(t) = KZ365,3: Long term component
                subplot_matrix.append([t[w:-w], long])

                # Subplot
                fig = plt.figure(figsize=(20, 9))
                for count in range(len(subplot_matrix)):
                    data = subplot_matrix[count]
                    plt.subplot(2, 2, count + 1)
                    ax = fig.add_subplot(2, 2, count + 1)
                    if count == 0:
                        plt.plot(data[0], data[1], label= variable)
                        plt.plot(data[2], data[3], label='Baseline')
                        plt.legend(loc='best')
                    else:
                        plt.plot(data[0], data[1])
                    ax.xaxis.set_major_locator(plt.MaxNLocator(5))  # Set Maximum number of x-axis values to show
                    fig.autofmt_xdate()
                    if count == 0:
                        titles = 'Log-transformed daily ' + variable
                        plt.ylabel('ln(' + unit + ')', fontsize=15)
                    elif count == 1:
                        titles = 'Short Term Component'
                        plt.ylabel("Short Term", fontsize=15)
                    elif count == 2:
                        titles = 'Seasonal Term Component'
                        plt.ylabel("Seasonal Term", fontsize=15)
                    else:
                        titles = 'Long Term Component'
                        plt.ylabel("Long Term", fontsize=15)
                    plt.title(titles, fontsize=18)

                plt.tight_layout()
                fig.suptitle(key + '_' + variable, fontsize=18)
                fig.savefig(directory_province + key + '_' + variable + ' detrend.png')
                plt.show()
                plt.close()
                print('\n')




# In[ ]:




