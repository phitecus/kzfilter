# O3
import csv
from statistics import mean
import numpy as np
from kolzur_filter import kz_filter, kzft, kzp, _kz_coeffs
import matplotlib.pyplot as plt
import functions
import os
filelist = ['Eastern', 'Kwai Chung', 'Tung Chung', 'YL', 'Kwun Tong', 'Macau', 'Sha Tin', 'ShamShuiPo', 'Tap Mun', 'Tsuen Wan']
# Put Your input between 0 and 9
input = 9
test = filelist[input]
if input < 4:
    file = "Supplement/O3-KZ/" + test + ".csv"
else:
    file = "Supplement/O3-KZ/O3-supplement/" + test + "-1.csv"
    file2 = "Supplement/O3-KZ/O3-supplement/" + test + "-2.csv"
subplot_matrix = []
print(test)


def detrend(file):
    hours = 24
    timestamp = []
    height = []
    o3 = []
    source = []
    status = []
    details = []
    delete_index = []
    with open(file) as infile:
        reader = csv.reader(infile)
        for rows, value in enumerate(reader):
            if rows > 3:
                timestamp.append(value[0])
                height.append(float(value[1]))
                o3.append(float(value[2]))
                source.append(value[3])
                status.append(float(value[4]))
                details.append(float(value[5]))
    if input > 3:
        with open(file2) as infile:
            reader = csv.reader(infile)
            for rows, value in enumerate(reader):
                if rows > 3:
                    timestamp.append(value[0])
                    height.append(float(value[1]))
                    o3.append(float(value[2]))
                    source.append(value[3])
                    status.append(float(value[4]))
                    details.append(float(value[5]))

    # Macau: For Macau, please just study 2003-2015
    if input == 5:
        timestamp = timestamp[:-17543]
        o3 = o3[:-17543]
    # Tsuen Wan: Delete from 2003/08/19 (2003/02/12 [973] ~ 2003/08/19 [5574])
    if input == 9:
        o3 = o3[5574:]
        timestamp = timestamp[5574:]
    numberofelements = len(timestamp)  # 157800
    numberofday = int(numberofelements/hours)  # 6575 days
    daily_timestamp = []
    for i in range(numberofelements):
        if i % 24 == 23:
            today = timestamp[i].split()[0]
            daily_timestamp.append(today)
    print(daily_timestamp)

    for i in range(len(timestamp)):
        if o3[i] < 0:
            delete_index.append(i)
    print(numberofday, "days")
    print("Delete:", delete_index)
    for j in range(len(delete_index)):
        o3[delete_index[j]] = functions.findPositive(o3, delete_index[j])
    print("First Row:", timestamp[0], height[0], o3[0], source[0], status[0], details[0])
    print("Mean", round(mean(o3), 4))

    # Plot Graph
    k = 3
    m = 365
    #dt = 1
    #t = np.arange(0, numberofelements, dt)
    #t = np.array(daily_timestamp)
    #plt.plot(t, o3, label = "Hourly Original Data")
    #x = np.array(o3)
    #w = int(k * (m - 1) / 2)
    #plt.plot(t[w:-w], kz_filter(x, m, k), label='m={}'.format(m) + ', k={}'.format(k))
    #plt.xlabel('Time Index')
    #plt.ylabel('O3')
    #plt.legend()
    #plt.show()

    # Convert to daily output
    daily = functions.Daily(o3)
    x = np.array(daily)
    #t = np.arange(0, numberofday, dt)
    t = np.array(daily_timestamp)
    #plt.plot(t, daily, label="Daily Data")
    #ax = plt.axes()  # Create axis
    #ax.plot(t[w:-w], kz_filter(x, m, k), label='m={}'.format(m) + ', k={}'.format(k))
    #ax.xaxis.set_major_locator(plt.MaxNLocator(5))  # Set Maximum number of x-axis values to show
    #plt.xlabel('Number of Day')
    #plt.ylabel('O3')
    #plt.legend()
    # plt.show()

    # KZ(29,3) to create baseline: o3_bl
    m = 29
    k = 3
    daily = np.array(daily)
    daily = np.log(daily)
    o3_bl = kz_filter(daily, m, k)
    # Adjust time
    w = int(k * (m - 1) / 2)
    daily_timestamp2 = daily_timestamp[w:-w]
    subplot_matrix.append([daily_timestamp, daily, daily_timestamp2, o3_bl])

    # W(t) = O(t) – KZ15,5: Short term component
    m = 15
    k = 5
    w = int(k*(m-1)/2)
    original = x[w:-w]
    short = original - kz_filter(x, 15, 5)
    #plt.plot(t[w:-w], short, label="Short term component")
    subplot_matrix.append([t[w:-w], short])
    #ax = plt.axes()  # Create axis
    #ax.xaxis.set_major_locator(plt.MaxNLocator(5))  # Set Maximum number of x-axis values to show
    #plt.xlabel('Number of Day')
    #plt.ylabel('O3')
    #plt.legend()
    #plt.show()

    # S(t) = KZ15,5 – KZ365,3: Seasonal component
    m = 365
    k = 3
    long = kz_filter(x, 365, 3)
    w = int(k * (m - 1) / 2)
    window = int((len(short)-len(long))/2)
    #seasonal = short[window:-window] - long
    seasonal = kz_filter(x, 15, 5)[window:-window] - long
    #plt.plot(t[w:-w], seasonal, label="Seasonal Component")
    subplot_matrix.append([t[w:-w], seasonal])
    #ax = plt.axes()  # Create axis
    #ax.xaxis.set_major_locator(plt.MaxNLocator(5))  # Set Maximum number of x-axis values to show
    #plt.xlabel('Number of Day')
    #plt.ylabel('O3')
    #plt.legend()
    #plt.show()

    # e(t) = KZ365,3: Long term component
    #plt.plot(t[w:-w], long, label="Long term Component")
    subplot_matrix.append([t[w:-w], long])
    #ax = plt.axes()  # Create axis
    #ax.xaxis.set_major_locator(plt.MaxNLocator(5))  # Set Maximum number of x-axis values to show
    #plt.xlabel('Number of Day')
    #plt.ylabel('O3')
    #plt.legend()
    #plt.show()


# Tap Mun: Detrend
detrend(file)
# Subplot
fig = plt.figure(figsize=(20, 8))
plt.suptitle(filelist[input], fontsize=20)
for count in range(len(subplot_matrix)):
    data = subplot_matrix[count]
    ax = plt.subplot(2, 2, count + 1)
    ax.grid(True)
    if count == 0:
        ax.plot(data[0], data[1], label='Daily Data')
        ax.plot(data[2], data[3], label='Baseline (O3 BL)')
        ax.legend(loc='best')
    else:
        ax.plot(data[0], data[1])
    ax.xaxis.set_major_locator(plt.MaxNLocator(5))  # Set Maximum number of x-axis values to show
    if count == 0:
        titles = 'Log-transformed O3'
        plt.ylabel("ppb (log-scaled)", fontsize=15)
    elif count == 1:
        titles = 'O3 Short Term Component'
        plt.ylabel("[O3 ST]", fontsize=15)
    elif count == 2:
        titles = 'O3 Seasonal Term Component'
        plt.ylabel("[O3 SEASON]", fontsize=15)
    else:
        titles = 'O3 Long Term Component'
        plt.ylabel("[O3 LT]", fontsize=15)
    plt.title(titles, fontsize=18)
plt.tight_layout()
plt.subplots_adjust(wspace=0.15, top=0.9)
#plt.show()

# Set Directory
directory = "detrend/"
if not os.path.exists(directory):
    os.makedirs(directory)
fig.savefig(directory + filelist[input] + '.png')
