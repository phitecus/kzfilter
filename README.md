# Using KZ filter to detrend O3 and Applications

## Overview
* KZ filter

* Regression

* Wind Direction

* Primary Pollutants

* Future Data

* China

* Spark


## 1. KZ filter

I highly recommend to read the following examples:

[kolmogorov-zurbenko-filter](https://github.com/MathieuSchopfer/kolmogorov-zurbenko-filter)



### detrend.py

```  
python detrend.py     
```  

This code detrends O3 data from 'Eastern', 'Kwai Chung', 'Tung Chung', 'YL', 'Kwun Tong', 'Macau', 'Sha Tin', 'ShamShuiPo', 'Tap Mun', 'Tsuen Wan' into short-term, seasonal-term, and long-term trends.

It will save graphs into detrend folder

This process can be visualized as the following figure:

<img src="./detrend/Eastern.png" width="450">

Raw data provided from Supplement folder

### mkz.py

It prevents drawbacks of cutting heads and tails of data, followed by KZ filter (but not really useful)


## 2. Regression

### meteorological.py

This function is to preprocess data (O3 and meteorological variables) and save them in preprocessed folder

### Regression.py

This code finds a linear relationship between baseline data of O3 and meteorological variables (temperature, relative humidity, pressure, and wind speed)

It will save graphs into Regression Result Folder.

This process can be visualized as the following figure:

<img src="./Regression Result/A Combined Subplot.png" width="450">

Input data provided from preprocessed folder

### Regression_5years.py

Similar to Regression.py code. But this version is for the recent 5 years of data (2013-2017).

<img src="./5 Year Regression Result/5 Year Combined Subplot.png" width="450">



## 3. Wind Direction

### wind_direction.py
This code finds the relationship between short-term trend of O3 and wind direction.

It will save graphs into ST Variation and WD folder.

This process can be visualized as the following figure:

<img src="./ST Variation and WD/A Combined Subplot.png" width="450">

Input data provided from Regression Result folder (wind direction data from csv files)



## 4. Primary Pollutants

### primary.py
This code preprocesses primary pollutants data (from NO2, SO2, and Supplement).

It will save csv files into Primary Pollutant folder, which will be later used in Long Term Relation.py

### Long Term Relation.py

This code finds the relationship between long-term trend of O3 and primary pollutants data (NO2 and SO2).

It will save graphs into Long Term Result folder.

This process can be visualized as the following figure:

<img src="./Long Term Result/A Combined Subplot.png" width="450">

Input data provided from Primary Pollutant folder 



## 5. Future Data

If we could have future climate data, can we predict future concentration levels of O3? 

Download future meteorological data (2045-2050 and 2095-2100) from [World Climate Research Programme](https://esgf-node.llnl.gov/search/cmip5/)

- These are the following models: MRI-CGCM3, MIROC5, HadGEM2-ES, IPSL-CM5A-MR, NorESM1-M, CSIRO-MK3.6, GFDL-ESM2M, GFDL-ESM2G

- 4 experiments: rcp26, rcp45, rcp60, rcp85

- Time Frequency: day

- Ensemble: r1i1p1

- Variable: tasmax (max temperature), rhs (relative humidity), sfcwind (wind speed), psl (pressure)

#### Future Data Process.py + Future Regression.py

Testing one model


### Future convert to csv.py

First convert NC files to csv files, by choosing appropriate latitude and longitude.

The saving directory: 'Future Data Average' folder (+ exp + '_' + model + '_' + variable + '_' + time + '.csv')

### Future Data Combine.py

Combine the csv files from 'Future Data Average'

Models: MRI-CGCM3, MIROC5, HadGEM2-ES, IPSL-CM5A-MR, NorESM1-M, CSIRO-MK3.6, GFDL-ESM2M, GFDL-ESM2G, then take an average.

Save them to 'Future Data Preprocess' folder.

Then, I organized the files in 'Model Combine' folder.

### Final Regression.py

Import future climate data from 'Model Combine'

Import regression coefficients from 'Regression Coefficients'

Use KZ filter to detrend O3 and climate data to implement linear regression, which results in future O3 baseline.

New O3 baseline is calculated from 'Subtraction Result' by considering each month.

Save graphs into Future Regression.

#### One Example of rcp26 scenario in Eastern:

<img src="./Future Regression/Eastern 2046-2050 rcp26.png" width="450">


### Subplot.py

Make subplot of different regions to compare (one example of rcp26)

<img src="./Future Regression/rcp26average comparison.png" width="450">



## 6. China

Now we extend to Chinese provinces. 'China' folder.

<img src="./China/China Detrend/O3/province/Beijing_O3 detrend.png" width="450">




## 7. Spark

We can use Spark and Databricks to extend this concept.

[1] Databricks notebook for combining different weather files: https://goo.gl/eVFJVf

[2] Databricks notebook for drawing scatterplots: https://goo.gl/3RTe1t

[3] Databricks notebook for filtering using KZ filter: https://goo.gl/mr6MZa

[4] Databricks notebook for modeling and predicting: https://goo.gl/fyMFuu


## References


1. *Lu, X., Lin, C., Li, Y., Yao, T., Fung, J. C., &amp; Lau, A. K. (2017). Assessment of health burden caused by
particulate matter in southern China using high-resolution satellite observation. Environment
international, 98, 160-170.
2. *Human-level control through deep reinforcement learning*, Mnih et al., 2015

[1] *Lu, X., Lin, C., Li, Y., Yao, T., Fung, J. C., &amp; Lau, A. K. (2017). Assessment of health burden caused by
particulate matter in southern China using high-resolution satellite observation. Environment
international, 98, 160-170.
[2] Lu, X., &amp; Fung, J. C. (2016). Source apportionment of sulfate and nitrate over the Pearl River Delta region in
China. Atmosphere, 7(8), 98.
[3] World Health Organization, &quot;Ambient air pollution: a global assessment of exposure and burden of disease,&quot;
2016.
[4] “Guangdong-Hong Kong-Macao Pearl River Delta Regional Air Quality Monitoring Network,” Quality
Management Committee of Guangdong-Hong Kong-Macao Pearl River Delta Regional Air Quality
Monitoring Network, 2016.
[5] CAAC (Clean Air Alliance of China), &quot;Air Pollution Prevention and Control Action Plan,&quot; 2013.

[6] AQHI (Air Quality Health Index), &quot;Air Quality Trends in Hong Kong,&quot; [Online]. Available:
http://www.aqhi.gov.hk/api_history/english/report/files/aqt15e.pdf.
[7] Seo, J., Youn, D., Kim, J. Y., &amp; Lee, H. (2014). Extensive spatiotemporal analyses of surface ozone and
related meteorological variables in South Korea for the period 1999–2010. Atmospheric Chemistry and
Physics, 14(12), 6395-6415.
[8] Li, P., Wang, Y., &amp; Dong, Q. (2017). The analysis and application of a new hybrid pollutants forecasting
model using modified Kolmogorov–Zurbenko filter. Science of the Total Environment, 583, 228-240.
[9] Rao, S. T., Zurbenko, I. G., Neagu, R., Porter, P. S., Ku, J. Y., &amp; Henry, R. F. (1997). Space and time scales
in ambient ozone data. Bulletin of the American Meteorological Society, 78(10), 2153-2166.
[10] Environmental Protection Department, Hong Kong, “Guidelines on the Estimation of PM2.5 for Air Quality
Assessment in Hong Kong,” 21 07 2018. [Online]. Available:
https://www.epd.gov.hk/epd/english/environmentinhk/air/guide_ref/guide_aqa_model_g5.html.

