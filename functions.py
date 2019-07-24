from kolzur_filter import kz_filter, kzft, kzp, _kz_coeffs
import numpy as np
import csv


def findMax(list):
    maximum = 0
    for value in list:
        if value > maximum:
            maximum = value
    return maximum


def findMin(list):
    if len(list) == 0:
        return 0
    else:
        minimum = list[0]
        for value in list:
            if value < minimum:
                minimum = value
        return minimum


def MaxConsecutive(datalist):
    answer=0
    list = []
    for i in range(len(datalist)):
        if datalist[i] < 0:
            answer += 1
            list.append(answer)
        if datalist[i] >= 0:
            answer = 0
    if list == []:
        key = 0
    else:
        key = findMax(list)
    return key


def findPositive(list, index):
    i = index
    j = index
    while float(list[i]) <= 0:
        i -= 1
    while float(list[j]) <= 0 and j < len(list)-1:
        j += 1

    if j == len(list)-1:  # when j reached the end of the list
        j = i

    a = float(list[i])
    b = float(list[j])
    return (a+b)/2


# Array Version
def findPositive2(array, index):  # [timestamp, value]
    i = index
    j = index
    while float(array[i][1]) <= 0:
        i -= 1
    while float(array[j][1]) <= 0:
        j += 1

    a = float(array[i][1])
    b = float(array[j][1])
    return (a+b)/2


def makePositive(list):
    deleteindex = []
    for i in range(len(list)):
        if float(list[i]) <= 0:
            deleteindex.append(i)
    if len(deleteindex) != 0:
        for j in range(len(deleteindex)):
            list[deleteindex[j]] = findPositive(list, deleteindex[j])


def find360(list, index):
    i = index
    j = index
    while float(list[i]) > 360:
        i -= 1
    while float(list[j]) > 360 and j < len(list) - 1:
        j += 1
    if j == len(list) - 1:  # when j reached the end of the list
        j = i
    a = float(list[i])
    b = float(list[j])
    return (a + b) / 2


def make360(list):
    deleteindex = []
    for i in range(len(list)):
        if float(list[i]) > 360:
            deleteindex.append(i)
    if len(deleteindex) != 0:
        for j in range(len(deleteindex)):
            list[deleteindex[j]] = find360(list, deleteindex[j])


def findaverage(list):
    numberofday = 0
    sum = 0
    for i, value in enumerate(list):
        sum += value
        numberofday += 1
    if numberofday == 0:
        answer = 0
    else:
        answer = sum/numberofday
    return answer


def Daily(data):  # Take Average
    answer = []
    for i in range(len(data)):
        if i % 24 == 23:
            j = i-23
            calculatelist = []
            while j <= i:
                calculatelist.append(data[j])
                j += 1
            answer.append(findaverage(calculatelist))
    return answer


def Daily_two(data):  # Take Maximum
    answer = []
    for i in range(len(data)):
        if i % 24 == 23:
            j = i-23
            calculatelist = []
            while j <= i:
                calculatelist.append(float(data[j]))
                j += 1
            answer.append(findMax(calculatelist))
    return answer


def Daily_8h(data):  # daily maximum 8h average
    answer = []


def pm25(file, m, k):  # Return [timestamp, x, short, seasonal, long]
    timestamp = []
    daytime = []
    pm = []
    delete_index = []
    # Import PM2.5 Data
    directory_pm = "PM2.5/"
    with open(directory_pm + file + ".csv") as infile:
        reader = csv.reader(infile)
        for rows, value in enumerate(reader):
            if rows > 3:
                timestamp.append(value[0])
                pm.append(float(value[2]))
    for i in range(len(timestamp)):
        if pm[i] < 0:
            delete_index.append(i)
        if i % 24 == 0:
            daytime.append(timestamp[i][:-9])
    for j in range(len(delete_index)):
        pm[delete_index[j]] = findPositive(pm, delete_index[j])
    # Convert to daily output
    #daily = Daily(pm)  # average
    daily = Daily_two(pm)  # maximum
    x = np.array(daily)
    # W(t) = O(t) – KZ15,5: Short term component
    m = 15
    k = 5
    w = int(k * (m - 1) / 2)
    original = x[w:-w]
    short = original - kz_filter(x, 15, 5)

    # e(t) = KZ365,3: Long term component
    m = 365
    k = 3
    long = kz_filter(x, 365, 3)

    # S(t) = KZ15,5 – KZ365,3: Seasonal component
    window = int((len(short) - len(long)) / 2)
    #seasonal = short[window:-window] - long
    seasonal = kz_filter(x, 15, 5)[window:-window] - long

    return [daytime, x, short, seasonal, long]


def detrend(file):
    timestamp = []
    o3 = []
    delete_index = []
    # Import O3 Data
    if file == 'Eastern' or file == 'Kwai Chung' or file == 'Tung Chung' or file == 'Yuen Long':
        directory_o3 = "Supplement/O3-KZ/"
        with open(directory_o3 + file + ".csv") as infile:
            reader = csv.reader(infile)
            for rows, value in enumerate(reader):
                if rows > 3:
                    timestamp.append(value[0])
                    o3.append(float(value[2]))
    else:
        directory_o3 = "Supplement/O3-KZ/O3-supplement/"
        with open(directory_o3 + file + "-1.csv") as infile:
            reader = csv.reader(infile)
            for rows, value in enumerate(reader):
                if rows > 3:
                    timestamp.append(value[0])
                    o3.append(float(value[2]))
        with open(directory_o3 + file + "-2.csv") as infile:
            reader = csv.reader(infile)
            for rows, value in enumerate(reader):
                if rows > 3:
                    timestamp.append(value[0])
                    o3.append(float(value[2]))

    # Macau: For Macau, please just study 2003-2015
    if file == 'Macau':
        timestamp = timestamp[:-17543]
        o3 = o3[:-17543]
    # Tsuen Wan: Start from 2003/08/19 (2003/02/12 [973] ~ 2003/08/19 [5574])
    if file == 'Tsuen Wan':
        o3 = o3[5574:]
        timestamp = timestamp[5574:]

    # Make Positive
    numberofelements = len(timestamp)
    daily_timestamp = []
    for i in range(numberofelements):
        if i % 24 == 23:
            today = timestamp[i].split()[0]
            daily_timestamp.append(today)
    for i in range(len(timestamp)):
        if o3[i] < 0:
            delete_index.append(i)
    for j in range(len(delete_index)):
        o3[delete_index[j]] = findPositive(o3, delete_index[j])

    # Convert to daily output
    daily = Daily_two(o3)
    x = np.array(daily)

    # W(t) = O(t) – KZ15,5: Short term component
    m = 15
    k = 5
    w = int(k*(m-1)/2)
    original = x[w:-w]
    short = original - kz_filter(x, 15, 5)

    # S(t) = KZ15,5 – KZ365,3: Seasonal component
    long = kz_filter(x, 365, 3)
    window = int((len(short)-len(long))/2)
    seasonal = kz_filter(x, 15, 5)[window:-window] - long
    return [daily_timestamp, x, short, seasonal, long]


def pm10(file, m, k):  # Return [timestamp, x, short, seasonal, long]
    timestamp = []
    daytime = []
    pm = []
    delete_index = []
    # Import PM10 Data
    directory_pm = "PM10/"
    with open(directory_pm + file + ".csv") as infile:
        reader = csv.reader(infile)
        for rows, value in enumerate(reader):
            if rows > 3:
                timestamp.append(value[0])
                pm.append(float(value[2]))

    # Macau: For Macau, please just study 2003-2015
    if file == 'Macau':
        timestamp = timestamp[:-17543]
        pm = pm[:-17543]

    # Make Positive
    for i in range(len(timestamp)):
        if pm[i] < 0:
            delete_index.append(i)
        if i % 24 == 0:
            daytime.append(timestamp[i][:-9])
    for j in range(len(delete_index)):
        pm[delete_index[j]] = findPositive(pm, delete_index[j])

    # Convert to daily output
    daily = Daily_two(pm)  # maximum
    x = np.array(daily)
    # W(t) = O(t) – KZ15,5: Short term component
    m = 15
    k = 5
    w = int(k * (m - 1) / 2)
    original = x[w:-w]
    short = original - kz_filter(x, 15, 5)

    # e(t) = KZ365,3: Long term component
    long = kz_filter(x, 365, 3)

    # S(t) = KZ15,5 – KZ365,3: Seasonal component
    window = int((len(short) - len(long)) / 2)
    seasonal = kz_filter(x, 15, 5)[window:-window] - long

    return [daytime, x, short, seasonal, long]


# Pseudo Code Index - 1
def mkz(list, m, k):
    # Half the size of KZ window = N - k*(m-1) = 1828
    w = int((len(list) - k * (m - 1)) / 2)
    z1 = []
    z2 = []
    z3 = []
    z = []
    z1.append(list[0])  # index 0
    z.append(list[0])
    for i in range(1, w):  # index from 1 to w-1
        z.append(sum(list[0:2*i-1])/(2*i+1))
        z1.append(sum(list[0:2 * i - 1]) / (2 * i + 1))
    for j in range(w, len(list)-w):  # index from w to len(x)-w-1
        z.append(sum(list[j-w:j+w])/(2*w+1))
        z2.append(sum(list[j - w:j + w]) / (2 * w + 1))
    for k in range(len(list)-w, len(list)):  # index from len(x)-w to len(x)-1
        z.append(sum(list[k-(len(list)-k)+1:len(list)])/(2*(len(list)-k)+1))
        z3.append(sum(list[k - (len(list) - k) + 1:len(list)]) / (2 * (len(list) - k) + 1))
        # z[len(x)-1] = z[-1]
    if len(z) != len(z1)+len(z2)+len(z3):
        print("Error")
    return z


def replace(original, new, start_year, start_month, end_year, end_month):
    # Find where to replace
    a = 0
    store_replace_index = []
    for index_wind in range(len(original)):
        today_wind = original[index_wind][0]
        year_wind = int(today_wind.split('/')[0])
        month_wind = int(today_wind.split('/')[1])
        if start_year == end_year:  # if years are same
            if year_wind == start_year and month_wind >= start_month and month_wind <= end_month:
                if original[index_wind][1] < 0:
                    store_replace_index.append(index_wind)
        elif end_year == 0:  # There is no end
            if year_wind >= start_year and month_wind >= start_month:
                if original[index_wind][1] < 0:
                    store_replace_index.append(index_wind)
        else:
            if (year_wind == start_year and month_wind >= start_month) or (year_wind == end_year and month_wind <= end_month):
                if original[index_wind][1] < 0:
                    store_replace_index.append(index_wind)

    # Find the first index and last index to replace
    beginning = store_replace_index[0]
    end = store_replace_index[-1]

    # Find the correct date
    for index_wind_replace in range(len(new)):
        if new[index_wind_replace][0] == original[beginning][0]:
            a = index_wind_replace

    # Replace
    for index_wind in range(beginning, end + 1):
        original[index_wind][1] = new[a + index_wind - beginning][1]


