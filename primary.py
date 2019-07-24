import csv
import os
import functions
import numpy as np

# O3 LT and NO2, SO2 LT
# Eastern / Central [0]
# Tap Mun [1]
# Tsuen Wan [2]
# Tung Chung [3]
# Yuen Long [4]
# Kwai Chung [5]
######################
# Kwun Tong [6]
# Macau [7]
# Sha Tin [8]
# Sham Shui Po [9]
filelist = ['Eastern', 'Tap Mun', 'Tsuen Wan', 'Tung Chung', 'Yuen Long', 'Kwai Chung', 'Kwun Tong', 'Macau', 'Sha Tin', 'ShamShuiPo']


def NO2(station):
    # Initialization
    file1 = ''
    file2 = ''
    no2 = []
    so2 = []
    timestamp = []
    header = ["NO2", "SO2"]

    # NO2
    if station < 6:
        directory_no2 = 'NO2/'
    else:
        directory_no2 = 'Supplement/Supplement-NO2/'
    if station == 0:  # Eastern
        file1 = 'Eastern-1'
        file2 = 'Eastern-2'
    if station == 1:  # Tap Mun
        file1 = 'Tap Mun-1'
        file2 = 'Tap Mun-2'
    if station == 2:  # Tsuen Wan
        file1 = "Tsuen Wan-1"
        file2 = "Tsuen Wan-2"
    if station == 3:  # Tung Chung
        file1 = 'Tung Chung-1'
        file2 = 'Tung Chung-2'
    if station == 4:  # Yuen Long
        file1 = 'Yuen Long-1'
        file2 = 'Yuen Long-2'
    if station == 5:  # Kwai Chung
        file1 = 'Kwai Chung-1'
        file2 = 'Kwai Chung-2'
    if station == 6:  # Kwun Tong
        file1 = 'Kwun Tong-1'
        file2 = 'Kwun Tong-2'
    if station == 7:  # Macau
        file1 = 'Macau-1'
        file2 = 'Macau-2'
    if station == 8:  # Sha Tin
        file1 = 'Sha Tin-1'
        file2 = 'Sha Tin-2'
    if station == 9:  # ShamShuiPo
        file1 = 'Sham Shui Po-1'
        file2 = 'Sham Shui Po-2'

    if file1 != '':
        with open(directory_no2+file1+".csv") as infile:
            reader = csv.reader(infile)
            for rows, value in enumerate(reader):
                if rows > 3:
                    timestamp.append(value[0])
                    no2.append([value[0], float(value[2])])  # timestamp, value
    if file2 != '':
        with open(directory_no2+file2+".csv") as infile:
            reader = csv.reader(infile)
            for rows, value in enumerate(reader):
                if rows > 3:
                    timestamp.append(value[0])
                    no2.append([value[0], float(value[2])])  # timestamp, value

    # SO2
    if station < 6:
        directory_so2 = 'SO2/'
    else:
        directory_so2 = 'Supplement/Supplement-SO2/'
    if station == 0:  # Eastern
        file1 = 'Eastern-1'
        file2 = 'Eastern-2'
    if station == 1:  # Tap Mun
        file1 = 'Tap Mun-1'
        file2 = 'Tap Mun-2'
    if station == 2:  # Tsuen Wan
        file1 = "Tsuen Wan-1"
        file2 = "Tsuen Wan-2"
    if station == 3:  # Tung Chung
        file1 = 'Tung Chung-1'
        file2 = 'Tung Chung-2'
    if station == 4:  # Yuen Long
        file1 = 'Yuen Long-1'
        file2 = 'Yuen Long-2'
    if station == 5:  # Kwai Chung
        file1 = 'Kwai Chung-1'
        file2 = 'Kwai Chung-2'
    if station == 6:  # Kwun Tong
        file1 = 'Kwun Tong-1'
        file2 = 'Kwun Tong-2'
    if station == 7:  # Macau
        file1 = 'Macau-1'
        file2 = 'Macau-2'
    if station == 8:  # Sha Tin
        file1 = 'Sha Tin-1'
        file2 = 'Sha Tin-2'
    if station == 9:  # ShamShuiPo
        file1 = 'Sham Shui Po-1'
        file2 = 'Sham Shui Po-2'

    if file1 != '':
        with open(directory_so2 + file1 + ".csv") as infile:
            reader = csv.reader(infile)
            for rows, value in enumerate(reader):
                if rows > 3:
                    so2.append([value[0], float(value[2])])  # timestamp, value
    if file2 != '':
        with open(directory_so2 + file2 + ".csv") as infile:
            reader = csv.reader(infile)
            for rows, value in enumerate(reader):
                if rows > 3:
                    so2.append([value[0], float(value[2])])  # timestamp, value

    # Macau: 2003-2015
    if station == 7:
        no2 = no2[:-17543]
        so2 = so2[:-17543]

    directory = "Primary Pollutant/"
    if not os.path.exists(directory):
        os.makedirs(directory)
    # Initialize matrix full of zeros
    resultMatrix = [[0 for x in range(len(header) + 1)] for y in range(len(timestamp) + 1)]

    ticker = [no2, so2]
    # Change the first row of result matrix to show headers
    firstrow = resultMatrix[0]
    for i in range(len(firstrow)):
        if i == 0:
            firstrow[i] = filelist[station]
        elif i < len(header) + 1:
            firstrow[i] = header[i - 1]

    # Fill the values in result matrix
    for i in range(len(resultMatrix)):
        if i != 0:
            # Change the first column of result matrix into time index
            resultMatrix[i][0] = timestamp[i - 1]

    # Loop through x-direction (column by column)
    for variable in range(len(ticker)):
        a = 0  # Ticker's row
        b = 0  # Timestamp's row
        column = ticker[variable]  # [timestamp, value]
        column = np.array(column)
        col = column[:, 1]
        col = np.asfarray(col, float)
        functions.makePositive(col)  # Make Positive
        column[:, 1] = col
        # Match the timestamp
        while b <= len(timestamp) and a < len(col):
            if column[a][0] != timestamp[b - 1]:
                a -= 1
            else:
                resultMatrix[b][variable + 1] = column[a][1]  # Fill in the result matrix
            a += 1
            b += 1

    # For Tsuen Wan and Tap Mun sites, please begin from 2004 and 2005 respectively.
    if station == 1:  # Tap Mun
        answer = []
        for i in range(len(resultMatrix)):
            if i == 0:
                answer.append(resultMatrix[i])  # header
            else:
                date = resultMatrix[i][0]
                year = int(date.split("/")[0])
                if year > 2004:  # 2005-2017
                    answer.append(resultMatrix[i])
    elif station == 2:  # Tsuen Wan
        answer = []
        for i in range(len(resultMatrix)):
            if i == 0:
                answer.append(resultMatrix[i])  # header
            else:
                date = resultMatrix[i][0]
                year = int(date.split("/")[0])
                if year > 2003:  # 2004-2017
                    answer.append(resultMatrix[i])
    elif station == 7:  # Macau
        answer = []
        for i in range(len(resultMatrix)):
            if i == 0:
                answer.append(resultMatrix[i])  # header
            else:
                date = resultMatrix[i][0]
                year = int(date.split("/")[0])
                if 2002 < year < 2016:  # 2003-2015
                    answer.append(resultMatrix[i])
    else:  # 2003-2017
        answer = []
        for i in range(len(resultMatrix)):
            if i == 0:
                answer.append(resultMatrix[i])  # header
            else:
                date = resultMatrix[i][0]
                year = int(date.split("/")[0])
                if year > 2002:  # 2003-2017
                    answer.append(resultMatrix[i])

    # Write csv file of result matrix inside primary pollutant folder
    with open(directory + str(filelist[station])+' data.csv', "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        for val in answer:
            writer.writerow(val)
    print(filelist[station])


# Use for loop to pre-process all the files
for files in range(len(filelist)):
    NO2(files)
