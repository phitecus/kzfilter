import csv
import os
import functions
import numpy as np
replace = functions.replace

filelist = ['Eastern', 'Tap Mun', 'Tsuen Wan', 'Tung Chung', 'Yuen Long', 'Kwai Chung', 'Kwun Tong', 'Macau', 'Sha Tin', 'ShamShuiPo']
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


# This function is to clear data and save it in preprocessed folder
def meterological(station):
    # Initialization
    file1 = ''
    file2 = ''
    pressure = []
    rh = []
    temperature = []
    replace_temperature = []
    wind = []
    replace_wind1 = []
    replace_wind2 = []
    wd = []
    replace_wd1 = []
    replace_wd2 = []
    timestamp = []
    header = ["Pressure", "RH", "Temperature", "Wind Speed", "Wind Direction"]

    # Pressure
    if station < 6:
        directory_pressure = 'Pressure/'
    else:
        directory_pressure = 'Supplement/supplement-Pressure/'
    if station == 0:  # Central / Eastern
        file1 = 'HKO --1'
        file2 = 'HKO --- 2'
    if station == 1:  # Tap Mun is only for detrending
        file1 = ''
        file2 = ''
    if station == 2:  # Tseun Wan
        file1 = "Tate's Cairn --1"
        file2 = "Tate's Cairn ---2"
    if station == 3:  # Tung Chung
        file1 = 'Sha lo Wan --1'
        file2 = 'Sha lo Wan ---2'
    if station == 4:  # Yuen Long
        file1 = 'Lau Fau Shan --1'
        file2 = 'Lau Fau Shan ---2'
    if station == 5:  # Kwai Chung
        file1 = "Tate's Cairn --1"
        file2 = "Tate's Cairn ---2"
    if station == 6:  # Kwun Tong
        file1 = "Tate's Cairn-1"
        file2 = "Tate's Cairn-2"
    if station == 7:  # Macau
        file1 = "Macau-1"
        file2 = "Macau-2"
    if station == 8:  # Sha Tin
        file1 = "Sha Tin-1"
        file2 = "Sha Tin-2"
    if station == 9:  # Sham Shui Po
        file1 = "King's Park-1"
        file2 = "King's Park-2"

    if file1 != '':
        with open(directory_pressure+file1+".csv") as infile:
            reader = csv.reader(infile)
            for rows, value in enumerate(reader):
                if rows > 3:
                    timestamp.append(value[0])
                    pressure.append([value[0], float(value[2])])  # timestamp, value
    if file2 != '':
        with open(directory_pressure+file2+".csv") as infile:
            reader = csv.reader(infile)
            for rows, value in enumerate(reader):
                if rows > 3:
                    timestamp.append(value[0])
                    pressure.append([value[0], float(value[2])])  # timestamp, value

    # RH
    if station < 6:
        directory_rh = 'RH/'
    else:
        directory_rh = 'Supplement/Supplement-RH/'
    if station == 0:  # Central / Eastern
        file1 = 'HKO ----1'
        file2 = 'HKO ----2'
    if station == 1:  # Tap Mun is only for detrending
        file1 = ''
        file2 = ''
    if station == 2:  # Tseun Wan
        file1 = "Tsing Yi ---1"
        file2 = "Tsing Yi ---2"
    if station == 3:  # Tung Chung
        file1 = 'Tung Chung ---1'
        file2 = 'Tung Chung ---2'
    if station == 4:  # Yuen Long
        file1 = 'Lau Fau Shan ---1'
        file2 = 'Lau Fau Shan ---2'
    if station == 5:  # Kwai Chung
        file1 = "Tsing Yi ---1"
        file2 = "Tsing Yi ---2"
    if station == 6:  # Kwun Tong
        file1 = "Kwun Tong-1"
        file2 = "Kwun Tong-2"
    if station == 7:  # Macau
        file1 = "Macau-1"
        file2 = "Macau-2"
    if station == 8:  # Sha Tin
        file1 = "Sha Tin-1"
        file2 = "Sha Tin-2"
    if station == 9:  # Sham Shui Po
        file1 = "Sham Shui Po-1"
        file2 = "Sham Shui Po-2"

    if file1 != '':
        with open(directory_rh+file1+".csv") as infile:
            reader = csv.reader(infile)
            for rows, value in enumerate(reader):
                if rows > 3:
                    rh.append([value[0], float(value[2])])  # timestamp, value
    if file2 != '':
        with open(directory_rh+file2+".csv") as infile:
            reader = csv.reader(infile)
            for rows, value in enumerate(reader):
                if rows > 3:
                    rh.append([value[0], float(value[2])])  # timestamp, value

    # Temperature
    if station < 6:
        directory_temperature = 'Temperature/'
    else:
        directory_temperature = 'Supplement/Supplement-Temperature/'
    if station == 0:  # Central / Eastern
        file1 = 'HKO-1'
        file2 = 'HKO-2'
    if station == 1:  # Tap Mun is only for detrending
        file1 = ''
        file2 = ''
    if station == 2:  # Tseun Wan
        file1 = "TsingYi-1"
        file2 = "TsingYi-2"
    if station == 3:  # Tung Chung
        file1 = 'Tung Chung-1'
        file2 = 'Tung Chung-2'
    if station == 4:  # Yuen Long
        file1 = 'Yuen Long-2'
        file2 = 'Yuen Long-3'
    if station == 5:  # Kwai Chung
        file1 = "TsingYi-1"
        file2 = "TsingYi-2"
    if station == 6:  # Kwun Tong
        file1 = "Kwun Tong-1"
        file2 = "Kwun Tong-2"
    if station == 7:  # Macau
        file1 = "Macau-1"
        file2 = "Macau-2"
    if station == 8:  # Sha Tin
        file1 = "ShaTin-1"
        file2 = "ShaTin-2"
    if station == 9:  # Sham Shui Po
        file1 = "ShamShuiPo-1"
        file2 = "ShamShuiPo-2"

    if file1 != '':
        with open(directory_temperature + file1 + ".csv") as infile:
            reader = csv.reader(infile)
            for rows, value in enumerate(reader):
                if rows > 3:
                    temperature.append([value[0], float(value[2])])  # timestamp, value
    if file2 != '':
        with open(directory_temperature + file2 + ".csv") as infile:
            reader = csv.reader(infile)
            for rows, value in enumerate(reader):
                if rows > 3:
                    temperature.append([value[0], float(value[2])])  # timestamp, value

    # Use Yuen Long-2 and Yuen Long-3 to do the regression.
    # However, large amount of data missing in Yuen Long-2 from 4/1/2010 2010 until 24/10/2011 17:00.
    # Use the data in Yuen Long-1 to replace the missing data in Yuen Long-2.
    if station == 4:  # Yuen Long
        with open(directory_temperature + 'Yuen Long-1' + ".csv") as infile:
            reader = csv.reader(infile)
            for rows, value in enumerate(reader):
                if rows > 3:
                    replace_temperature.append([value[0], float(value[2])])  # timestamp, value
        # From 4/1/2010 2010 until 24/10/2011 17:00
        replace(temperature, replace_temperature, 2010, 1, 2011, 10)

    # Use the Kwun Tong-3 to fill the missing data in Kwun Tong-2 after 2013.12.31
    if station == 6:  # Kwun Tong
        with open(directory_temperature + 'Kwun Tong-3' + ".csv") as infile:
            reader = csv.reader(infile)
            for rows, value in enumerate(reader):
                if rows > 3:
                    replace_temperature.append([value[0], float(value[2])])  # timestamp, value
        # From 26/6/2014 until end
        replace(temperature, replace_temperature, 2014, 6, 0, 0)

    # Use the ShamShuiPo-3 to fill the missing data in ShamShuiPo-2 after 2013.12.31
    if station == 9:  # Sham Shui Po
        with open(directory_temperature + 'ShamShuiPo-3' + ".csv") as infile:
            reader = csv.reader(infile)
            for rows, value in enumerate(reader):
                if rows > 3:
                    replace_temperature.append([value[0], float(value[2])])  # timestamp, value
        # From 12/6/2014 10:00 until end
        replace(temperature, replace_temperature, 2014, 6, 0, 0)

    # Wind
    if station < 6:
        directory_wind = 'Wind/'
    else:
        directory_wind = 'Supplement/Supplement-Wind/'
    if station == 0:  # Central / Eastern
        file1 = 'HKO-1'
        file2 = 'HKO-2'
    if station == 1:  # Tap Mun is only for detrending
        file1 = ''
        file2 = ''
    if station == 2:  # Tseun Wan
        file1 = "Tsuen Wan-1"  # Use TsingYi-1 wind data to fill the missing data in Tsuen Wan-1 around 2003.04
        file2 = "Tsuen Wan-2"   # Use Tuen Mun-2 wind data to fill the missing data in Tsuen Wan-2 after Dec.2013
    if station == 3:  # Tung Chung
        file1 = 'Tung Chung-1'
        file2 = 'Tung Chung-2'  # Use Siu Ho Wan-2 to fill the missing data in Tung Chung-2 after 2014.
    if station == 4:  # Yuen Long
        file1 = 'YuenLong-1'
        file2 = 'YuenLong-2'  # LauFauShan-2 to fill the missing data in Yuen Long-2 after Dec.2013 + beginning of 2010
    if station == 5:  # Kwai Chung
        file1 = "Kwai Chung-1"  # Use TsingYi-1 wind data to fill the missing data in Kwai Chung-1 around 2003.04
        file2 = "Kwai Chung-2"  # Use Tuen Mun-2 wind data to fill the missing data in Kwai Chung-2 after Dec.2013
    if station == 6:  # Kwun Tong
        file1 = "Kwun Tong-1"  # Use TKO's 2003.01, 2004.05 (TKO-1),
        file2 = "Kwun Tong-2"  # after 2014.06.26 (TKO-2) to replace the missing data in Kwun Tong
    if station == 7:  # Macau
        file1 = "Macau-1"
        file2 = "Macau-2"
    if station == 8:  # Sha Tin
        file1 = "Sha Tin -1"
        file2 = "Sha Tin-2"
    if station == 9:  # Sham Shui Po
        file1 = "Sham Shui Po -1"  # Use King's Park's 2003.12.05-2004.03.09 (King's Park-1)
        file2 = "Sham Shui Po-2"  # after 2014.06.12 (King's Park-2) to replace the missing data in Sham Shui Po

    if file1 != '':
        with open(directory_wind + file1 + ".csv") as infile:
            reader = csv.reader(infile)
            for rows, value in enumerate(reader):
                if rows > 3:
                    wind.append([value[0], float(value[2])])  # timestamp, value
    if file2 != '':
        with open(directory_wind + file2 + ".csv") as infile:
            reader = csv.reader(infile)
            for rows, value in enumerate(reader):
                if rows > 3:
                    wind.append([value[0], float(value[2])])  # timestamp, value
    if station == 2:  # Tseun Wan
        # Use Tsing Yi-1 wind data to fill the missing data in Tsuen Wan-1 around 2003.04
        with open(directory_wind + 'Tsing Yi-1' + ".csv") as infile:
            reader = csv.reader(infile)
            for rows, value in enumerate(reader):
                if rows > 3:
                    replace_wind1.append([value[0], float(value[2])])  # timestamp, value
        # 10/02/2003 14:00 to 20/08/2003 23:00
        replace(wind, replace_wind1, 2003, 2, 2003, 8)

        # Use Tuen Mun-2 wind data to fill the missing data in Tsuen Wan-2 after Dec.2013
        with open(directory_wind + 'Tuen Mun-2' + ".csv") as infile:
            reader = csv.reader(infile)
            for rows, value in enumerate(reader):
                if rows > 3:
                    replace_wind2.append([value[0], float(value[2])])  # timestamp, value
        # 01/06/2014 0:00 to end
        replace(wind, replace_wind2, 2014, 6, 0, 0)

    # Use Siu Ho Wan-2 wind data to fill the missing data in Tung Chung-2 after 2014.
    if station == 3:  # Tung Chung
        with open(directory_wind + 'Siu Ho Wan-2' + ".csv") as infile:
            reader = csv.reader(infile)
            for rows, value in enumerate(reader):
                if rows > 3:
                    replace_wind1.append([value[0], float(value[2])])  # timestamp, value
        # 02/07/2014 14:00 to end
        replace(wind, replace_wind1, 2014, 7, 0, 0)

    # Use LauFauShan-2 wind data to fill the missing data in Yuen Long-2 after Dec.2013 / Also at the beginning of 2010
    if station == 4:  # Yuen Long
        with open(directory_wind + 'Lau Fau Shan-2' + ".csv") as infile:
            reader = csv.reader(infile)
            for rows, value in enumerate(reader):
                if rows > 3:
                    replace_wind1.append([value[0], float(value[2])])  # timestamp, value
        # From 02/03/2014 12:00 to end
        replace(wind, replace_wind1, 2014, 3, 0, 0)
        # From 1/1/2010 0:00 to 12/02/2010 10:00
        replace(wind, replace_wind1, 2010, 1, 2010, 2)

    if station == 5:  # Kwai Chung
        # Use TsingYi-1 wind data to fill the missing data in Kwai Chung-1 around 2003.04
        with open(directory_wind + 'Tsing Yi-1' + ".csv") as infile:
            reader = csv.reader(infile)
            for rows, value in enumerate(reader):
                if rows > 3:
                    replace_wind1.append([value[0], float(value[2])])  # timestamp, value
        # 04/04/2003 11:00 to 15/08/2003 11:00
        replace(wind, replace_wind1, 2003, 4, 2003, 8)

        # Use Tuen Mun-2 wind data to fill the missing data in Kwai Chung-2 after Dec.2013
        with open(directory_wind + 'Tuen Mun-2' + ".csv") as infile:
            reader = csv.reader(infile)
            for rows, value in enumerate(reader):
                if rows > 3:
                    replace_wind2.append([value[0], float(value[2])])  # timestamp, value
        # 04/06/2014 0:00 to end
        replace(wind, replace_wind2, 2014, 6, 0, 0)

    if station == 6:  # Kwun Tong
        # Use TKO's 2003.01, 2004.05 (TKO-1)
        with open(directory_wind + 'TKO -1' + ".csv") as infile:
            reader = csv.reader(infile)
            for rows, value in enumerate(reader):
                if rows > 3:
                    replace_wind1.append([value[0], float(value[2])])  # timestamp, value
        # 01/01/2003 00:00 to 07/02/2003 12:00
        replace(wind, replace_wind1, 2003, 1, 2003, 2)
        # 08/05/2004 16:00 to 08/06/2004 10:00
        replace(wind, replace_wind1, 2004, 5, 2004, 6)

        # after 2014.06.26 (TKO-2) to replace the missing data in Kwun Tong
        with open(directory_wind + 'TKO-2' + ".csv") as infile:
            reader = csv.reader(infile)
            for rows, value in enumerate(reader):
                if rows > 3:
                    replace_wind2.append([value[0], float(value[2])])  # timestamp, value
        # 26/06/2014 12:00 to end
        replace(wind, replace_wind2, 2014, 6, 0, 0)

    if station == 9:  # Sham Shui Po
        # Use King's Park's 2003.12.05-2004.03.09 (King's Park-1)
        with open(directory_wind + "King's Park-1" + ".csv") as infile:
            reader = csv.reader(infile)
            for rows, value in enumerate(reader):
                if rows > 3:
                    replace_wind1.append([value[0], float(value[2])])  # timestamp, value
        # 05/12/2003 08:00 to 09/03/2004 00:00
        replace(wind, replace_wind1, 2003, 12, 2004, 3)

        # after 2014.06.12 (King's Park-2) to replace the missing data in Sham Shui Po
        with open(directory_wind + "King's Park-2" + ".csv") as infile:
            reader = csv.reader(infile)
            for rows, value in enumerate(reader):
                if rows > 3:
                    replace_wind2.append([value[0], float(value[2])])  # timestamp, value
        # 12/06/2014 09:00 to end
        replace(wind, replace_wind2, 2014, 6, 0, 0)

    # Wind Direction
    if station == 0:  # Central / Eastern
        file1 = 'HKO-1'
        file2 = 'HKO-2'
    if station == 1:  # Tap Mun is only for detrending
        file1 = ''
        file2 = ''
    if station == 2:  # Tseun Wan
        file1 = "Tsuen Wan-1"  # Use TsingYi-1 wind data to fill the missing data in Tsuen Wan-1 around 2003.04
        file2 = "Tsuen Wan-2"   # Use Tuen Mun-2 wind data to fill the missing data in Tsuen Wan-2 after Dec.2013
    if station == 3:  # Tung Chung
        file1 = 'Tung Chung-1'
        file2 = 'Tung Chung-2'  # Use Siu Ho Wan-2 to fill the missing data in Tung Chung-2 after 2014.
    if station == 4:  # Yuen Long
        file1 = 'YuenLong-1'
        file2 = 'YuenLong-2'  # LauFauShan-2 to fill the missing data in Yuen Long-2 after Dec.2013 + beginning of 2010
    if station == 5:  # Kwai Chung
        file1 = "Kwai Chung-1"  # Use TsingYi-1 wind data to fill the missing data in Kwai Chung-1 around 2003.04
        file2 = "Kwai Chung-2"  # Use Tuen Mun-2 wind data to fill the missing data in Kwai Chung-2 after Dec.2013
    if station == 6:  # Kwun Tong
        file1 = "Kwun Tong-1"  # Use TKO's 2003.01, 2004.05 (TKO-1),
        file2 = "Kwun Tong-2"  # after 2014.06.26 (TKO-2) to replace the missing data in Kwun Tong
    if station == 7:  # Macau
        file1 = "Macau-1"
        file2 = "Macau-2"
    if station == 8:  # Sha Tin
        file1 = "Sha Tin -1"
        file2 = "Sha Tin-2"
    if station == 9:  # Sham Shui Po
        file1 = "Sham Shui Po -1"  # Use King's Park's 2003.12.05-2004.03.09 (King's Park-1)
        file2 = "Sham Shui Po-2"  # after 2014.06.12 (King's Park-2) to replace the missing data in Sham Shui Po

    if file1 != '':
        with open(directory_wind + file1 + ".csv") as infile:
            reader = csv.reader(infile)
            for rows, value in enumerate(reader):
                if rows > 3:
                    wd.append([value[0], float(value[3])])  # timestamp, value
    if file2 != '':
        with open(directory_wind + file2 + ".csv") as infile:
            reader = csv.reader(infile)
            for rows, value in enumerate(reader):
                if rows > 3:
                    wd.append([value[0], float(value[3])])  # timestamp, value

    if station == 2:  # Tseun Wan
        # Use Tsing Yi-1 wind data to fill the missing data in Tsuen Wan-1 around 2003.04
        with open(directory_wind + 'Tsing Yi-1' + ".csv") as infile:
            reader = csv.reader(infile)
            for rows, value in enumerate(reader):
                if rows > 3:
                    replace_wd1.append([value[0], float(value[3])])  # timestamp, value
        # 10/02/2003 14:00 to 20/08/2003 23:00
        replace(wd, replace_wd1, 2003, 2, 2003, 8)

        # Use Tuen Mun-2 wind data to fill the missing data in Tsuen Wan-2 after Dec.2013
        with open(directory_wind + 'Tuen Mun-2' + ".csv") as infile:
            reader = csv.reader(infile)
            for rows, value in enumerate(reader):
                if rows > 3:
                    replace_wd2.append([value[0], float(value[3])])  # timestamp, value
        # 01/06/2014 0:00 to end
        replace(wd, replace_wd2, 2014, 6, 0, 0)

    # Use Siu Ho Wan-2 wind data to fill the missing data in Tung Chung-2 after 2014.
    if station == 3:  # Tung Chung
        with open(directory_wind + 'Siu Ho Wan-2' + ".csv") as infile:
            reader = csv.reader(infile)
            for rows, value in enumerate(reader):
                if rows > 3:
                    replace_wd1.append([value[0], float(value[3])])  # timestamp, value
        # 02/07/2014 14:00 to end
        replace(wd, replace_wd1, 2014, 7, 0, 0)

    # Use LauFauShan-2 wind data to fill the missing data in Yuen Long-2 after Dec.2013 / Also at the beginning of 2010
    if station == 4:  # Yuen Long
        with open(directory_wind + 'Lau Fau Shan-2' + ".csv") as infile:
            reader = csv.reader(infile)
            for rows, value in enumerate(reader):
                if rows > 3:
                    replace_wd1.append([value[0], float(value[3])])  # timestamp, value
        # From 02/03/2014 12:00 to end
        replace(wd, replace_wd1, 2014, 3, 0, 0)
        # From 1/1/2010 0:00 to 12/02/2010 10:00
        replace(wd, replace_wd1, 2010, 1, 2010, 2)

    if station == 5:  # Kwai Chung
        # Use TsingYi-1 wind data to fill the missing data in Kwai Chung-1 around 2003.04
        with open(directory_wind + 'Tsing Yi-1' + ".csv") as infile:
            reader = csv.reader(infile)
            for rows, value in enumerate(reader):
                if rows > 3:
                    replace_wd1.append([value[0], float(value[3])])  # timestamp, value
        # 04/04/2003 11:00 to 15/08/2003 11:00
        replace(wd, replace_wd1, 2003, 4, 2003, 8)

        # Use Tuen Mun-2 wind data to fill the missing data in Kwai Chung-2 after Dec.2013
        with open(directory_wind + 'Tuen Mun-2' + ".csv") as infile:
            reader = csv.reader(infile)
            for rows, value in enumerate(reader):
                if rows > 3:
                    replace_wd2.append([value[0], float(value[3])])  # timestamp, value
        # 04/06/2014 0:00 to end
        replace(wd, replace_wd2, 2014, 6, 0, 0)

    if station == 6:  # Kwun Tong
        # Use TKO's 2003.01, 2004.05 (TKO-1)
        with open(directory_wind + 'TKO -1' + ".csv") as infile:
            reader = csv.reader(infile)
            for rows, value in enumerate(reader):
                if rows > 3:
                    replace_wd1.append([value[0], float(value[3])])  # timestamp, value
        # 01/01/2003 00:00 to 07/02/2003 12:00
        replace(wd, replace_wd1, 2003, 1, 2003, 2)
        # 08/05/2004 16:00 to 08/06/2004 10:00
        replace(wd, replace_wd1, 2004, 5, 2004, 6)

        # after 2014.06.26 (TKO-2) to replace the missing data in Kwun Tong
        with open(directory_wind + 'TKO-2' + ".csv") as infile:
            reader = csv.reader(infile)
            for rows, value in enumerate(reader):
                if rows > 3:
                    replace_wd2.append([value[0], float(value[3])])  # timestamp, value
        # 26/06/2014 12:00 to end
        replace(wd, replace_wd2, 2014, 6, 0, 0)

    if station == 9:  # Sham Shui Po
        # Use King's Park's 2003.12.05-2004.03.09 (King's Park-1)
        with open(directory_wind + "King's Park-1" + ".csv") as infile:
            reader = csv.reader(infile)
            for rows, value in enumerate(reader):
                if rows > 3:
                    replace_wd1.append([value[0], float(value[3])])  # timestamp, value
        # 05/12/2003 08:00 to 09/03/2004 00:00
        replace(wd, replace_wd1, 2003, 12, 2004, 3)

        # after 2014.06.12 (King's Park-2) to replace the missing data in Sham Shui Po
        with open(directory_wind + "King's Park-2" + ".csv") as infile:
            reader = csv.reader(infile)
            for rows, value in enumerate(reader):
                if rows > 3:
                    replace_wd2.append([value[0], float(value[3])])  # timestamp, value
        # 12/06/2014 09:00 to end
        replace(wd, replace_wd2, 2014, 6, 0, 0)

    ##########################

    if station == 1:  # Skip Tap Mun
        return
    else:
        directory = "preprocessed/"
        if not os.path.exists(directory):
            os.makedirs(directory)
        # Initialize matrix full of zeros
        resultMatrix = [[0 for x in range(len(header) + 1)] for y in range(len(timestamp) + 1)]

    ticker = [pressure, rh, temperature, wind, wd]
    # Change the first row of result matrix to show headers
    firstrow = resultMatrix[0]
    for i in range(len(firstrow)):
        if i == 0:
            firstrow[i] = filelist[station]
        elif i < len(header)+1:
            firstrow[i] = header[i-1]

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
        # Match the timestamp
        while b <= len(timestamp):
            if column[a][0] != timestamp[b-1]:
                a -= 1
            else:
                resultMatrix[b][variable+1] = column[a][1]  # Fill in the result matrix
            a += 1
            b += 1

    # For Tsuen Wan, Yuen Long, Kwai Chung sites, work on 2005-2017
    if station == 2 or station == 4 or station == 5:  # Tsuen Wan, Yuen Long, Kwai Chung
        answer = []
        for i in range(len(resultMatrix)):
            if i == 0:
                answer.append(resultMatrix[i])  # header
            else:
                date = resultMatrix[i][0]
                year = int(date.split("/")[0])
                if year > 2004:  # 2005-2017
                    answer.append(resultMatrix[i])

    elif station == 7:  # Macau: 2003-2015
        answer = []
        for i in range(len(resultMatrix)):
            if i == 0:
                answer.append(resultMatrix[i])  # header
            else:
                date = resultMatrix[i][0]
                year = int(date.split("/")[0])
                if 2002 < year < 2016:  # 2003-2015
                    answer.append(resultMatrix[i])

    # For other stations, work on 2003-2017
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

    # Convert negative values to positive
    answer = np.array(answer)
    for variable in range(len(ticker)):  # Pressure, RH, Temperature, Wind Speed, Wind Direction
        functions.makePositive(answer[:, variable+1][1:])  # Take each column (except header)
        # Wind Direction <= 360
        if variable == 4:
            functions.make360(answer[:, variable+1][1:])

    # Write csv file of result matrix inside preprocessed folder
    with open(directory + str(filelist[station])+' data.csv', "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        for val in answer:
            writer.writerow(val)
    print("Complete Function: preprocessed " + filelist[station])


# Use for loop to pre-process all the files
for files in range(len(filelist)):
    meterological(files)

