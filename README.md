# Using KZ filter to detrend O3 and Applications

## Overview
* KZ filter

* Regression

* Wind Direction

* Primary Pollutants

* Future Data

* Spark


## 1. KZ filter

I highly recommend to read the following examples:

[kolmogorov-zurbenko-filter](https://github.com/MathieuSchopfer/kolmogorov-zurbenko-filter)



### detrend.py

This code detrends O3 data from 'Eastern', 'Kwai Chung', 'Tung Chung', 'YL', 'Kwun Tong', 'Macau', 'Sha Tin', 'ShamShuiPo', 'Tap Mun', 'Tsuen Wan' into short-term, seasonal-term, and long-term trends.

It will save graphs into detrend folder

This process can be visualized as the following figure:

<img src="./detrend/Eastern.png" width="450">

Raw data provided from Supplement folder

### mkz.py

It prevents drawbacks of cutting heads and tails of data, followed by KZ filter.


## 2. Regression

### meteorological.py

This function is to preprocess data (O3 and meteorological variables) and save them in preprocessed folder

### Regression.py

This code finds a linear relationship between baseline data of O3 and meteorological variables (temperature, relative humidity, pressure, and wind speed)

It will save graphs into Regression Result Folder.

This process can be visualized as the following figure:

<img src="./Regression Result/A Combined Subplot.png" width="450">

Input data provided from preprocessed folder


## 3. Wind Direction
### wind_direction.py
This code finds the relationship between short-term trend of O3 and wind direction.

It will save graphs into ST Variation and WD folder.

This process can be visualized as the following figure:

<img src="./ST Variation and WD/A Combined Subplot.png" width="450">

Input data provided from Regression Result folder (wind direction data from csv files)



## 4. Primary Pollutants
### primary.py
This code preprocesses primary pollutants data (NO2 and SO2).

It will save csv files into Primary Pollutant folder, which will be later used in Long Term Relation.py



### Long Term Relation.py

This code finds the relationship between long-term trend of O3 and wind direction.

It will save graphs into Long Term Result folder.

This process can be visualized as the following figure:

<img src="./ST Variation and WD/A Combined Subplot.png" width="450">

Input data provided from Regression Result folder (wind direction data from csv files)



## 5. Future Data


## 6. Spark


## References



