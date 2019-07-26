#!/usr/bin/env python
# coding: utf-8

# In[26]:


# Combine detrend values in csv file (stored in China detrend csv)
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv
import os
from kolzur_filter import kz_filter, kzft, kzp, _kz_coeffs
import functions
import glob
import netCDF4
import math


# In[4]:


# Import Files (china): daily data
directory_import = 'china/'
filelist = []

# Read csv files from folder
for files in glob.glob(directory_import + '*.csv'):
    print(files)
    filelist.append(files)


# In[6]:


pblh_import = 'UROP_files/PBLH/'
rad_import = 'UROP_files/Rad/'
met_import = 'UROP_files/Tem-Wind-P-RH/'
pblhlist = []
radlist = []
metlist = []

# Read nc files from PBLH folder
for files in glob.glob(pblh_import + '*.nc'):
    pblhlist.append(files)
for files in glob.glob(rad_import + '*.nc'):
    radlist.append(files)
for files in glob.glob(met_import + '*.nc'):
    metlist.append(files)
print(len(pblhlist), len(radlist), len(metlist))


# In[7]:


timestamp_met = []
met_data = []
for i in range(len(metlist)):
    nc = netCDF4.Dataset(metlist[i], mode='r')
    ps = nc.variables['PS'][0] # surface pressure
    rh = nc.variables['QV10M'][0] # 10-meter_specific_humidity
    t = nc.variables['T10M'][0] # 10-meter_air_temperature
    wsu = abs(nc.variables['U10M'][0]) # 10-meter_eastward_wind
    wsv = abs(nc.variables['V10M'][0]) # 10-meter_northward_wind
    time_var = nc.variables['time']
    dtime = netCDF4.num2date(time_var[:],time_var.units)
    timestamp_met.append(dtime)
    met_data.append([dtime, ps, rh, t, wsu, wsv])


# In[8]:


timestamp_pblh = []
pblh_data = []

for i in range(len(pblhlist)):
    nc = netCDF4.Dataset(pblhlist[i], mode='r')
    pblh = nc.variables['PBLH'][0] # planetary boundary layer height
    time_var = nc.variables['time']
    dtime = netCDF4.num2date(time_var[:],time_var.units)
    timestamp_pblh.append(dtime)
    pblh_data.append([dtime, pblh])


# In[9]:


timestamp_rad = []
rad_data = []

for i in range(len(radlist)):
    nc = netCDF4.Dataset(radlist[i], mode='r')
    rad = nc.variables['SWGDN'][0] # surface_incoming_shortwave_flux
    time_var = nc.variables['time']
    dtime = netCDF4.num2date(time_var[:],time_var.units)
    timestamp_rad.append(dtime)
    rad_data.append([dtime, rad])


# In[10]:


# Sorting MET data according to time
met_data = sorted(met_data,key=lambda x: (x[0],x[1]))
timestamp_met = sorted(timestamp_met)
# Sorting PBLH data according to time
pblh_data = sorted(pblh_data,key=lambda x: (x[0],x[1]))
timestamp_pblh = sorted(timestamp_pblh)
# Sorting RAD data according to time
rad_data = sorted(rad_data,key=lambda x: (x[0],x[1]))
timestamp_rad = sorted(timestamp_rad)


# In[11]:


# 2013/1/1 ~ 2018/12/31 data
# adjust length by excluding first and last one
timestamp_met_adj = timestamp_met[1:-1]
met_data_adj = met_data[1:-1]
# adjust length of pblh data
timestamp_pblh_adj = timestamp_pblh[8:]
pblh_data_adj = pblh_data[8:]
# adjust length of rad data
timestamp_rad_adj = timestamp_rad[1:]
rad_data_adj = rad_data[1:]

#print(met_data[0][1][30][30])
print(len(timestamp_met_adj), len(timestamp_pblh_adj), len(timestamp_rad_adj))
print(timestamp_met_adj[0], timestamp_met_adj[-1])
print(timestamp_pblh_adj[0], timestamp_pblh_adj[-1])
print(timestamp_rad_adj[0], timestamp_rad_adj[-1])


# In[23]:


def get_weather(lon, lat):
    # -180 + 0.625y = longitude (-180 to 180)
    y = int((lon + 180) / 0.625)
    # -90 + 0.5x = latitude (-90 to 90)
    x = int((lat + 90) / 0.5)
    ps = []
    rh = []
    t = []
    wsu = []
    wsv = []
    pblh = []
    rad = []
    
    for time in range(len(met_data_adj)):
        ps.append(met_data_adj[time][1][x][y])
        rh.append(met_data_adj[time][2][x][y])
        t.append(met_data_adj[time][3][x][y])
        wsu.append(met_data_adj[time][4][x][y])
        wsv.append(met_data_adj[time][5][x][y])
        pblh.append(pblh_data_adj[time][1][x][y])
        rad.append(rad_data_adj[time][1][x][y])
    print(len(ps), len(rh), len(t), len(wsu), len(wsv), len(pblh), len(rad))
    return [ps, rh, t, wsu, wsv, pblh, rad]


# In[24]:


header = ['Timestamp', 'FSPMC', 'RSPMC', 'O3', 'pressure', 'humidity', 'temperature', 'wind speed', 'PBLH', 'RAD']


# In[41]:


# Make Directory
directory = 'China Detrend csv/'
if not os.path.exists(directory):
    os.makedirs(directory)


# In[42]:


m = 29
k = 3
w = int(k*(m-1)/2)


# In[76]:


for f in range(len(filelist)):
    if f==1 or f==2 or f==4:
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

        if f==1 or f==2 or f==4: #FSPMC, RSPMC, O3
            # Detrend station by station
            values = np.array(values)
            values = np.asfarray(values, 'float')
            
            for s in range(len(station)):
                print(s+1, station[s], variable)
                
                data = values[:,s] # data of air pollutants
                
                time = timestamp
                time_met = timestamp_met_adj
                # Find location and its province
                lat = round(float(latitude[s]), 2)
                lon = round(float(longitude[s]), 2)
                print(lon,lat)

                ##############
                # Get Weather Data
                w_data = get_weather(lon, lat)
                ps = w_data[0]
                rh = w_data[1]
                t = w_data[2]
                wsu = w_data[3]
                wsv = w_data[4]
                ws = [math.sqrt(wsu[x]**2+wsv[x]**2) for x in range(len(wsu))]
                pblh = w_data[5]
                rad = w_data[6]
                ##############

                # Find negative values of air pollutants
                delete_index = []
                non_delete = []
                minimum_len = 0
                for i in range(len(data)):
                    if data[i] < 0:
                        delete_index.append(i)
                        minimum_len += 1
                    else:
                        non_delete.append(i)
                
                last_index = len(data) - 1
                first_index = 0
                if len(delete_index) != 0:
                    # Cut the tail if necessary
                    if delete_index[-1] + 1 == len(data):
                        last_index = non_delete[-1]
                        data = data[:last_index+1]
                        time = time[:last_index+1]
                        # adjust the length of weather data
                        time_met = time_met[:last_index+1]
                        ps = ps[:last_index+1]
                        rh = rh[:last_index+1]
                        t = t[:last_index+1]
                        ws = ws[:last_index+1]
                        pblh = pblh[:last_index+1]
                        rad = rad[:last_index+1]

                        # Find negative values again with new data
                        delete_index = []
                        for i in range(len(data)):
                            if data[i] < 0:
                                delete_index.append(i)

                    # Cut the head if necessary
                    if len(delete_index) !=0 and delete_index[0] == 0:
                        first_index = non_delete[0]
                        data = data[first_index:]
                        time = time[first_index:]
                        # adjust the length of weather data
                        time_met = time_met[first_index:]
                        ps = ps[first_index:]
                        rh = rh[first_index:]
                        t = t[first_index:]
                        ws = ws[first_index:]
                        pblh = pblh[first_index:]
                        rad = rad[first_index:]
                        # Find negative values again with new data
                        delete_index = []
                        for i in range(len(data)):
                            if data[i] < 0:
                                delete_index.append(i)

                    # Make Positive
                    if len(delete_index) != 0:
                        for j in range(len(delete_index)):
                            data[delete_index[j]] = functions.findPositive(data, delete_index[j])

                print('\n')
                #print(s+1, station[s], variable, len(data), len(time), len(time_met))
                #print(time[0], time[-1], time_met[0], time_met[-1])

                # Get the Baseline data
                if minimum_len < 0.2*len(data): # negative values smaller than 20% of the whole data
                    m = 29
                    k = 3
                    w = int(k*(m-1)/2)
                    data = np.array(data)
                    ps = np.array(ps)
                    rh = np.array(rh)
                    t = np.array(t)
                    ws = np.array(ws)
                    pblh = np.array(pblh)
                    rad = np.array(rad)

                    #x = data # original data
                    #data = np.log(data)
                    #ps = np.log(ps)
                    #rh = np.log(rh)
                    #t = np.log(t)
                    #ws = np.log(ws)
                    #pblh = np.log(pblh)
                    #rad = np.log(rad)

                    baseline = kz_filter(data, m, k)
                    ps_bl = kz_filter(ps, m, k)
                    rh_bl = kz_filter(rh, m, k)
                    temp_bl = kz_filter(t, m, k)
                    ws_bl = kz_filter(ws, m, k)
                    pblh_bl = kz_filter(pblh, m, k)
                    rad_bl = kz_filter(rad, m, k)

                    time = np.array(time)
                    time_bl = time[w:-w]

                    # Check whether the csv file exists
                    csvfile = directory + station[s] + '.csv'

                    # if exists, import
                    if os.path.exists(csvfile):
                        df = pd.read_csv(csvfile)
                        df = np.array(df)
                        df = df[:,1:] # Delete the first column with index number 0, 1, 2,,

                    # if not, make new one
                    else:
                        df = [[0 for x in range(len(header))] for y in range(len(timestamp[w:-w])+1)]
                        df[0] = header
                        df = np.array(df)
                        df[:,0][1:] = timestamp[w:-w]
                    
                    #print('check', first_index,last_index,timestamp[w:-w][first_index:first_index+len(time_bl)][0], time_bl[0])
                    #print('check', first_index,last_index,timestamp[w:-w][first_index:last_index+len(time_bl)][-1], time_bl[-1])

                    # fill the air pollutants
                    if f==1:
                        df[:,1][1:][first_index:first_index+len(baseline)] = baseline
                    if f==2:
                        df[:,2][1:][first_index:first_index+len(baseline)] = baseline
                    if f==4:
                        df[:,3][1:][first_index:first_index+len(baseline)] = baseline
                    
                    # fill in the meteorologcal values
                    df[:,4][1:][first_index:first_index+len(ps_bl)] = ps_bl
                    df[:,5][1:][first_index:first_index+len(rh_bl)] = rh_bl
                    df[:,6][1:][first_index:first_index+len(temp_bl)] = temp_bl
                    df[:,7][1:][first_index:first_index+len(ws_bl)] = ws_bl
                    df[:,8][1:][first_index:first_index+len(pblh_bl)] = pblh_bl
                    df[:,9][1:][first_index:first_index+len(rad_bl)] = rad_bl
                    
                    # Export
                    pd.DataFrame(df).to_csv(csvfile)


# In[ ]:




