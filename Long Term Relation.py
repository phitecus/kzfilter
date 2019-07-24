from kolzur_filter import kz_filter
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv
import functions
import statsmodels.formula.api as sm
header = ["NO2 LT", "SO2 LT", "O3 LT"]
filelist = ['Eastern', 'Tap Mun', 'Tsuen Wan', 'Tung Chung', 'Yuen Long', 'Kwai Chung', 'Kwun Tong', 'Macau', 'Sha Tin', 'ShamShuiPo']
subplot_matrix = []


# KZ Filter to get Long Term Variations
def LT(station):
    print(filelist[station])
    # Import NO2, SO2 data
    directory = 'Primary Pollutant/'
    df = pd.read_csv(directory + filelist[station] + ' data.csv')
    df = np.array(df)
    timestamp_raw = df[:, 0]
    timestamp = []
    no2 = df[:, 1]
    so2 = df[:, 2]
    # Change to Daily Data
    for i in range(len(timestamp_raw)):
        if i % 24 == 23:
            day = timestamp_raw[i].split()[0]
            timestamp.append(day)

    data_frame = [[0 for x in range(len(header) + 1)] for y in range(len(timestamp) + 1)]
    # Change the first row of result matrix to show headers
    firstrow = data_frame[0]
    for i in range(len(firstrow)):
        if i == 0:
            firstrow[i] = filelist[station]
        elif i < len(header) + 1:
            firstrow[i] = header[i - 1]

    # Fill the values in result matrix
    for i in range(len(data_frame)):
        if i != 0:
            # Change the first column of result matrix into time index
            data_frame[i][0] = timestamp[i - 1]

    no2_daily = functions.Daily_two(no2)
    so2_daily = functions.Daily_two(so2)

    # KZ Filter on NO2, SO2
    m = 365
    k = 3
    # Adjust time
    w = int(k * (m - 1) / 2)
    pollutants = [no2_daily, so2_daily]
    data_frame = np.array(data_frame)
    for variable in range(len(pollutants)):
        pollutant = pollutants[variable]
        pollutant = np.array(pollutant)
        lt = kz_filter(pollutant, m, k)
        data_frame[:, variable+1][w+1:-w] = lt

    # O3 LT
    o3 = []
    time_o3 = []
    time_lt = []
    file = filelist[station]
    # Import O3 Data
    if file == 'Eastern' or file == 'Kwai Chung' or file == 'Tung Chung' or file == 'Yuen Long':
        directory_o3 = "Supplement/O3-KZ/"
        with open(directory_o3 + file + ".csv") as infile:
            reader = csv.reader(infile)
            for rows, value in enumerate(reader):
                if rows > 3:
                    time_o3.append(value[0])
                    o3.append(float(value[2]))
    else:
        directory_o3 = "Supplement/O3-KZ/O3-supplement/"
        with open(directory_o3 + file + "-1.csv") as infile:
            reader = csv.reader(infile)
            for rows, value in enumerate(reader):
                if rows > 3:
                    time_o3.append(value[0])
                    o3.append(float(value[2]))
        with open(directory_o3 + file + "-2.csv") as infile:
            reader = csv.reader(infile)
            for rows, value in enumerate(reader):
                if rows > 3:
                    time_o3.append(value[0])
                    o3.append(float(value[2]))

    # Macau: 2003-2015
    if station == 7:
        time_o3 = time_o3[:-17543]
        o3 = o3[:-17543]

    functions.makePositive(o3)
    # Change to Daily Data
    for i in range(len(time_o3)):
        if i % 24 == 23:
            day = time_o3[i].split()[0]
            time_lt.append(day)
    o3 = functions.Daily_two(o3)
    o3 = np.array(o3)
    lt = kz_filter(o3, m, k)
    time_lt = time_lt[w:-w]
    # Match the timestamp and fill O3 data in len(header)th column
    a = 0  # O3 Row
    b = 0  # Timestamp's Row
    if station == 2 or station == 6 or station == 7 or station == 8 or station == 9:  # Tsuen Wan, Kwun Tong, Macau, Sha Tin
        while b < len(timestamp) and a < len(time_lt):
            if time_lt[a] != timestamp[b]:
                a -= 1
            else:
                data_frame[b + 1][len(header)] = lt[a]  # b+1 because of headers
            a += 1
            b += 1
    else:
        while b < len(timestamp) and a < len(time_lt):
            if time_lt[a] != timestamp[b]:
                b -= 1
            else:
                data_frame[b + 1][len(header)] = lt[a]  # b+1 because of headers
            a += 1
            b += 1

    # Delete the rows with zero
    delete_front = []
    for column in range(1, len(data_frame[0])):
        delete_index = 0
        col = np.asfarray(data_frame[:, column][1:], float)
        while col[delete_index] == 0:
            delete_index += 1
        delete_front.append(delete_index)
    delete_front = functions.findMax(delete_front) + 1
    data_frame = data_frame[delete_front:]
    # Back Rows with zero
    delete_back = []
    for column in range(1, len(data_frame[0])):
        delete_index = 0
        col = np.asfarray(data_frame[:, column][1:], float)
        while col[delete_index] != 0:
            delete_index += 1
        delete_back.append(delete_index)
    delete_back = functions.findMin(delete_back) + 1
    data_frame = data_frame[:delete_back]  # Time, NO2, SO2, O3

    # Set Directory
    directory = "Long Term Result/"
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Write csv file of result matrix inside primary pollutant folder
    with open(directory + str(filelist[station]) + '.csv', "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        for val in data_frame:
            writer.writerow(val)

    # Normalize
    o3_lt = np.asfarray(data_frame[:, len(header)], float)
    no2_lt = np.asfarray(data_frame[:, 1], float)
    so2_lt = np.asfarray(data_frame[:, 2], float)
    average_o3 = np.mean(o3_lt)
    average_no2 = np.mean(no2_lt)
    average_so2 = np.mean(so2_lt)
    std_o3 = np.std(o3_lt)
    std_no2 = np.std(no2_lt)
    std_so2 = np.std(so2_lt)
    o3_lt = [(float(i) - average_o3) / std_o3 for i in o3_lt]
    no2_lt = [(float(i) - average_no2) / std_no2 for i in no2_lt]
    so2_lt = [(float(i) - average_so2) / std_so2 for i in so2_lt]

    # Plot Graphs
    fig = plt.figure()  # Create a figure
    ax = plt.axes()  # Create axis
    ax.grid(True)
    x_axis = data_frame[:, 0]
    title = str(filelist[station])
    subplot_matrix.append([x_axis, o3_lt, no2_lt, so2_lt])
    plt.plot(x_axis, o3_lt, label='O3 Long Term')
    plt.plot(x_axis, no2_lt, label='NO2 Long Term')
    plt.plot(x_axis, so2_lt, label='SO2 Long Term')
    ax.xaxis.set_major_locator(plt.MaxNLocator(5))  # Set Maximum number of x-axis values to show
    fig.autofmt_xdate()  # Rotate values to see more clearly
    plt.title(title)
    plt.xlabel("Time Series")
    plt.ylabel("Normalized Unit")
    plt.legend(loc='best')
    fig.savefig(directory + title + ".png")


for file in range(len(filelist)):
    LT(file)

# subplot
fig = plt.figure(figsize=(20, 10))
for file in range(len(filelist)):
    titles = filelist[file]
    data = subplot_matrix[file]
    ax = plt.subplot(3, 4, file+1)
    ax.plot(data[0], data[1], label='O3 Long Term')
    ax.plot(data[0], data[2], label='NO2 Long Term')
    ax.plot(data[0], data[3], label='SO2 Long Term')
    ax.xaxis.set_major_locator(plt.MaxNLocator(5))  # Set Maximum number of x-axis values to show
    ax.grid(True)
    plt.title(titles, fontsize=20)
    plt.xlabel("Time Series", fontsize=8)
    plt.ylabel("Normalized Unit", fontsize=8)
    if file == 0:
        fig.legend(loc='lower right', fontsize=20)
    # Regression
    MET = pd.DataFrame({"O3": data[1], "NO2": data[2],
                        "SO2": data[3]})
    result = sm.ols(formula="O3~NO2", data=MET).fit()
    print("\n")
    print(filelist[file])
    print("NO2 r-squared", round(result.rsquared, 4))
    result = sm.ols(formula="O3~SO2", data=MET).fit()
    print("SO2 r-squared", round(result.rsquared, 4))

plt.tight_layout()
fig.savefig("Long Term Result/" + 'A Combined Subplot.png')
