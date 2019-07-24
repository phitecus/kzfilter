import csv
import functions
import os
import matplotlib.pyplot as plt
import numpy as np
mkz = functions.mkz
pm25 = functions.pm25

m = 365
k = 3
hours = 24
# Central [0]
# Tap Mun [1]
# Tsuen Wan [2]
# Tung Chung [3]
# Yuen Long [4]
filelist = ["Central", "Tap Mun", "Tsuen Wan", "Tung Chung", "Yuen Long"]


def graph_mkz(fileindex):
    file = filelist[fileindex]

    timestamp = pm25(file, m, k)[0]
    x = pm25(file, m, k)[1]

    numberofday = len(timestamp)  # 157800 / 24 = 6209

    # w = int(k * (m - 1) / 2) # w = 546 when m = 365, k = 3
    # Half the size of KZ window = N - k*(m-1)
    w = int((len(x) - k*(m-1))/2)  # 1828

    A = mkz(x, m, k)  # 1st iteration
    B = mkz(A, m, k)  # 2nd iteration
    C = mkz(B, m, k)  # 3rd iteration
    ticker = ["x", "mkz", "mkz2", "mkz3"]

    resultMatrix = [[0 for x in range(len(ticker)+1)] for y in range(int(len(timestamp)/24)+1)]
    # Change the first row of result matrix to show headers
    firstrow = resultMatrix[0]
    for i in range(len(firstrow)):
        if i == 0:
            firstrow[i] = ""
        elif i < len(ticker)+1:
            firstrow[i] = ticker[i-1]

    # Change the first column of result matrix to show time index
    for i in range(len(resultMatrix)):
        if i == 0:
            resultMatrix[i][0] = ""
        else:
            resultMatrix[i][0] = timestamp[i]
            resultMatrix[i][1] = x[i-1]
            resultMatrix[i][2] = A[i-1]
            resultMatrix[i][3] = B[i-1]
            resultMatrix[i][4] = C[i-1]

    # We will save the results in mkz folder
    directory = "MKZ_Result/"
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Write csv file of result matrix inside result folder
    with open('MKZ_Result/' + file + ' mkz.csv', "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        for val in resultMatrix:
            writer.writerow(val)

    # Plot Graph after 3rd iterations
    #outlier = 15
    fig = plt.figure()  # Create a figure
    ax = plt.axes()  # Create axis
    #dt = 1
    #t = np.arange(0, numberofday, dt)
    #plt.plot(t[outlier:-outlier], C[outlier:-outlier], label="MKZ after 3rd iterations")
    plt.plot(timestamp, C)
    ax.xaxis.set_major_locator(plt.MaxNLocator(5))  # Set Maximum number of x-axis values to show
    fig.autofmt_xdate()  # Rotate values to see more clearly
    plt.title(file)
    plt.xlabel('Number of Day')
    plt.ylabel('PM2.5')
    plt.show()
    fig.savefig(directory + file)


for i in range(len(filelist)):
    graph_mkz(i)
