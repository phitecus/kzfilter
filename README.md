# Using KZ filter to detrend O3 and Applications

## Overview
* KZ filter

* Regression

* Wind Direction

* Primary Pollutants

* Future Data

* Spark


## KZ filter

I highly recommend to read the following examples:

[kolmogorov-zurbenko-filter](https://github.com/MathieuSchopfer/kolmogorov-zurbenko-filter)



### detrend.py

This code detrends O3 data from 'Eastern', 'Kwai Chung', 'Tung Chung', 'YL', 'Kwun Tong', 'Macau', 'Sha Tin', 'ShamShuiPo', 'Tap Mun', 'Tsuen Wan' into short-term, seasonal-term, and long-term trends.

It will save graphs into detrend folder

This process can be visualized as the following figure:

<img src="./detrend/Eastern.png" width="450">

Raw data provided from Supplement folder


## Regression

### Regression.py

This code finds a linear relationship between baseline data of O3 and meteorological variables (temperature, relative humidity, pressure, and wind speed)

It will save graphs into Regression Result Folder.

This process can be visualized as the following figure:

<img src="./Regression Result/A Combined Subplot.png" width="450">

Raw data provided from preprocessed folder


## Wind Direction


## Primary Pollutants


## Future Data


## Spark


## References



