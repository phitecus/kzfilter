import numpy as np
import pandas as pd
import os
import math
import matplotlib.pyplot as plt
import csv
import functions

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
subplot_matrix = []
o3_standard = 60  # ppbv


def Wind_Direction(station):
    if station == 1:  # Tap Mun
        return
    file = filelist[station]
    directory = "Regression Result/"
    N = []
    NE = []
    E = []
    SE = []
    S = []
    SW = []
    W = []
    NW = []
    df = pd.read_csv(directory + filelist[station] + '.csv')  # No headers
    df = df.sort_values(by='Wind Direction')
    df = np.array(df)
    timestamp = df[:, 0]
    if station != 0:  # Skip Central
        # May - October
        indices = []
        for time in range(len(timestamp)):
            month = int(timestamp[time].split('/')[1])
            if month < 5 or month > 10:
                indices.append(time)
        df = np.delete(df, indices, axis=0)  # Delete Rows if not May - October
    wd = df[:, 5]
    pm_short = df[:, -1]
    print("\n")
    print(filelist[station])
    print('min', min(wd), 'max', max(wd))
    x_axis = wd
    y = pm_short

    # Scatter Plot
    plt.scatter(x_axis, y)
    # plt.show()

    for count in range(len(x_axis)):
        adjust = 45/2
        if x_axis[count] < 45 - adjust:
            x_axis[count] = 'N'
            N.append(y[count])
        elif x_axis[count] < 90 - adjust:
            x_axis[count] = 'NE'
            NE.append(y[count])
        elif x_axis[count] < 135 - adjust:
            x_axis[count] = 'E'
            E.append(y[count])
        elif x_axis[count] < 180 - adjust:
            x_axis[count] = 'SE'
            SE.append(y[count])
        elif x_axis[count] < 225 - adjust:
            x_axis[count] = 'S'
            S.append(y[count])
        elif x_axis[count] < 270 - adjust:
            x_axis[count] = 'SW'
            SW.append(y[count])
        elif x_axis[count] < 315 - adjust:
            x_axis[count] = 'W'
            W.append(y[count])
        elif x_axis[count] < 360 - adjust:
            x_axis[count] = 'NW'
            NW.append(y[count])
        else:
            x_axis[count] = 'N'
            N.append(y[count])

    # Calculate Probability
    direction = [N, NE, E, SE, S, SW, W, NW]
    x_axis = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
    y_axis = []
    for i in range(len(direction)):
        number = 0
        total = len(direction[i])
        for j in range(len(direction[i])):
            if math.exp(direction[i][j]) > 1:
                number += 1
        if total == 0:
            probability = 0
        else:
            probability = number/total
        y_axis.append(probability)
        print(x_axis[i], round(probability * 100, 4), '%')

    # Import Preprocessed WD Data
    df2 = pd.read_csv('preprocessed/' + filelist[station] + ' data.csv')
    df2 = np.array(df2)
    wd_raw = df2[:, -1]
    wd_time = df2[:, 0]
    o3_time = []
    o3_raw = []
    # Import Raw O3 Data
    if file == 'Eastern' or file == 'Kwai Chung' or file == 'Tung Chung' or file == 'Yuen Long':
        directory_o3 = "Supplement/O3-KZ/"
        with open(directory_o3 + file + ".csv") as infile:
            reader = csv.reader(infile)
            for rows, value in enumerate(reader):
                if rows > 3:
                    o3_time.append(value[0])
                    o3_raw.append(float(value[2]))
    else:
        directory_o3 = "Supplement/O3-KZ/O3-supplement/"
        with open(directory_o3 + file + "-1.csv") as infile:
            reader = csv.reader(infile)
            for rows, value in enumerate(reader):
                if rows > 3:
                    o3_time.append(value[0])
                    o3_raw.append(float(value[2]))
        with open(directory_o3 + file + "-2.csv") as infile:
            reader = csv.reader(infile)
            for rows, value in enumerate(reader):
                if rows > 3:
                    o3_time.append(value[0])
                    o3_raw.append(float(value[2]))
    # Macau: 2003-2015
    if station == 7:
        o3_time = o3_time[:-17543]
        o3_raw = o3_raw[:-17543]
    # Make Positive
    functions.makePositive(o3_raw)
    print("WD", min(wd_raw), max(wd_raw), "Ozone (O3)", min(o3_raw), max(o3_raw))

    # Initialize matrix full of zeros
    data_frame = [[0 for x in range(3)] for y in range(len(o3_time))]
    # First Column
    for row in range(len(data_frame)):
        data_frame[row][0] = o3_time[row]
    data_frame = np.array(data_frame)
    data_frame[:, 1] = o3_raw
    a = 0  # WD Timestamp's row
    b = 0  # O3 row
    column = wd_time  # [timestamp, value]
    # Match the timestamp between pm and wd
    while b < len(o3_time) and a < len(column):
        if column[a] != o3_time[b]:
            a -= 1
        else:
            data_frame[b][2] = wd_raw[a]  # Fill in the result matrix
        a += 1
        b += 1

    # Delete unnecessary rows in data frame
    delete_index = 0
    while float(data_frame[delete_index][2]) <= 0:
        delete_index += 1
    data_frame = data_frame[delete_index:]
    # May - October
    indices = []
    timestamp = data_frame[:, 0]
    for time in range(len(data_frame)):
        month = int(timestamp[time].split('/')[1])
        if month < 5 or month > 10:
            indices.append(time)
    data_frame = np.delete(data_frame, indices, axis=0)  # Delete Rows if not May - October

    # Set the directory
    directory = "ST Variation and WD/"
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Write csv file of result matrix inside preprocessed folder
    with open(directory + str(filelist[station]) + ' WD data.csv', "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        for val in data_frame:
            writer.writerow(val)

    N = []
    NE = []
    E = []
    SE = []
    S = []
    SW = []
    W = []
    NW = []
    x_axis = data_frame[:, 2]
    y = np.asfarray(data_frame[:, 1], float)
    for count in range(len(data_frame)):
        adjust = 45/2
        if float(x_axis[count]) < 45 - adjust:
            x_axis[count] = 'N'
            N.append(y[count])
        elif float(x_axis[count]) < 90 - adjust:
            x_axis[count] = 'NE'
            NE.append(y[count])
        elif float(x_axis[count]) < 135 - adjust:
            x_axis[count] = 'E'
            E.append(y[count])
        elif float(x_axis[count]) < 180 - adjust:
            x_axis[count] = 'SE'
            SE.append(y[count])
        elif float(x_axis[count]) < 225 - adjust:
            x_axis[count] = 'S'
            S.append(y[count])
        elif float(x_axis[count]) < 270 - adjust:
            x_axis[count] = 'SW'
            SW.append(y[count])
        elif float(x_axis[count]) < 315 - adjust:
            x_axis[count] = 'W'
            W.append(y[count])
        elif float(x_axis[count]) < 360 - adjust:
            x_axis[count] = 'NW'
            NW.append(y[count])
        else:
            x_axis[count] = 'N'
            N.append(y[count])

    # Calculate Probability
    direction = [N, NE, E, SE, S, SW, W, NW]
    x_axis = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
    y_axis2 = []
    for i in range(len(direction)):
        number = 0
        total = len(direction[i])
        for j in range(len(direction[i])):
            if direction[i][j] > o3_standard:
                number += 1
        if total == 0:
            probability = 0
        else:
            probability = number / total
        y_axis2.append(probability)
        # print(x_axis[i], round(probability * 100, 4), '%')

    # Draw Graphs
    fig = plt.figure()  # Create a figure
    title = filelist[station]
    plt.plot(x_axis, y_axis, label='exp[O3 ST] > 1')
    plt.plot(x_axis, y_axis2, label='O3 > ' + str(o3_standard) + 'ppbv')
    plt.grid(True)
    subplot_matrix.append([x_axis, y_axis, y_axis2])
    plt.title(title)
    plt.xlabel("Wind Direction")
    plt.ylabel("Probability")
    plt.legend(loc='best')
    fig.savefig(directory + title + ".png")
    # plt.show()


for file in range(len(filelist)):
    Wind_Direction(file)

# subplot
fig = plt.figure(figsize=(13, 10))
for file in range(len(filelist)):
    titles = filelist[file]
    if file < 1:
        print("\n")
        print(titles)
        data = subplot_matrix[file]
        ax = plt.subplot(3, 3, file+1)
    elif file != 1:
        print(titles)
        data = subplot_matrix[file-1]
        ax = plt.subplot(3, 3, file)
    if file != 1:
        ax.plot(data[0], data[1], label='exp[O3 ST] > 1')
        ax.plot(data[0], data[2], label='O3 > ' + str(o3_standard) + 'ug/m3')
        # ax.xaxis.set_major_locator(plt.MaxNLocator(5))  # Set Maximum number of x-axis values to show
        plt.title(titles, fontsize=16)
        plt.xlabel("Wind Direction")
        plt.ylabel("Probability")
        ax.legend(loc='best')
        ax.grid(True)

plt.tight_layout()
directory = "ST Variation and WD/"
fig.savefig(directory + 'A Combined Subplot.png')
