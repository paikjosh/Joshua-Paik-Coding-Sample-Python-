# Joshua Paik Python Coding Sample
The objective of the project was to write functions in Python that can be used to clean and analyze different types of time series data. More specifically, I have first written functions that perform the task of data cleaning, including identifying missing values, finding outliers, and normalizing data. To demonstrate functionalities of these functions, I have applied them into a sample data that I have created. Using this cleaned sample data, I have moved on to performing two basic time series analyses of autoregressive integrated moving average (ARIMA) and vector autoregression (VAR). The operation that I have described can be seen using all files attached in this repository.

Descriptions of files in this repository are:
| File Name | Description |
| --- | --- |
| data_clean.py | Contains functions that clean time series data |
| data_analysis.py | Contains functions that perform time series analysis |
| utility_functions.py | Contains utility functions used throughout "data_clean.py" and "data_analysis.py" |
| test.py | Cleans and analyzes a sample time series data that is on "euro_file.csv" using all three files described above |
| reference | Contains references to sources that I have used for this project |


Codes in this project utilizes multiple Python libraries, which are:
  1) pandas
  2) numpy
  4) scipy
  5) matplotlib
  6) statsmodels
  7) math
  8) re

| 1 | pandas |

I have made a Youtube video in which I run all codes in "test.py". The link to that video:
You can also try to implement functions yourself.

All Python files in this repo as well as the video attached above contain descriptions of functions that I’ve written. However, all of them lack my thought process that went into writing those functions. Hence, I’ll use the space below to talk about that. I will only cover important, and perhaps complicated, functions that I feel the need to talk further.


$${\color{red}convert \textunderscore data \textunderscore type(target \textunderscore file)}$$
-----
When the data is initially imported to Python, all entries are type string since they contain at least one symbol. But they must be in numerical form in order to clean and perform analysis. So, all non-date columns must be in type string, while date columns must convert to type datetime. That function was written to achieve such a task.

Note that this function first converts target_file into dataframe. This action was necessary since the data type for the date column and all other columns are different after converting and converting data into dataframe allows for different columns to have different data types.

In addition, note that this function converts some integers into type float. Of course, this isn’t the best practice since doing that decreases the computing efficiency. However, I have made this choice because when performing certain analysis, inputs may have to be in type float.


$${\color{red}check \textunderscore for \textunderscore missing(target \textunderscore file)}$$
-----
The idea behind this function was to first check if missing data exists in any parts of the data, then give the user a chance to delete identified missing values. Giving the user a choice to deal with missing values is an important part of this function since removing missing values might not be the best way to deal with them. For example, if one can reasonably assume that a value is missing at random (MAR), then it is a good idea to perform an imputation to deal with that missing value.


$${\color{red}check \textunderscore outliers(target \textunderscore file, \space date \textunderscore col \textunderscore name)}$$
-----
This function was to detect outliers. When doing this, I thought it was a good idea to first create a visual representation of data before conducting formal outlier tests. This was because I thought making visual representation was a more intuitive way of understanding the distribution of the data and how certain data points fall into that distribution. So, the purpose of this was to allow for the user to first find outliers by looking at visual representation of their data, then they can conduct formal tests if they still feel the need to do that after looking at the visual representation.

Also, if target_file has more than 2 variables, this function only uses Mahalanobis distance both when graphing and conducting tests. This means it plots Mahalanobis distance as opposed to scatter plot of data and runs an outlier test using Mahalanobis distance as opposed to running Z-score or IQR tests. This choice was made because: 1st) when graphing data, creating visual representation of multivariate data other than plotting Mahalanobis distance may be difficult, especially if there are too many variables (ex: 40 variables). 2nd) when conducting outlier tests, the Z-score outlier test may not be appropriate depending on context since it assumes that all variables are independent of each other and running IQR test is simply not appropriate in multivariate cases by design of the test.

Another important element of this function is when the user is deciding between Z-score and IQR tests to identify outliers, the function runs a normality test to help the user's decision. Generally, the user would choose a Z-score if their data is normal and choose IQR otherwise.

Final part of this function that I want to highlight is that it lets the user decide their own threshold for running all outlier tests. I felt that this was necessary since the ideal threshold when running outlier tests varies by context. However, for all tests, I have written a typical threshold used.


$${\color{red}check \textunderscore duplicates(target \textunderscore file, \space date \textunderscore col \textunderscore name)}$$
-----
This function is straightforward. However, I do want to point out that this function gives the user the choice to remove duplicates with the same date entries as opposed to removing them without asking. This choice was made because these type of duplicates are likely to arise from misinterpretation. For example, if data collecting frequency is different throughout different data points, then there is a possibility that these duplicates aren’t actually duplicates and they are data collected in different time frames that just weren’t specified in the data (ex: 1pm of 1/1/2025 and 2pm of 1/1/2025, but they were both recorded as 1/1/2025).


$${\color{red}normalize \textunderscore data(target \textunderscore file, \space date \textunderscore col \textunderscore name)}$$
-----
This is another straightforward function. But, I just want to say that just like the function check_outliers, this function runs normality tests to help the user’s decision between using min-max scaling or Z-score normalization to normalize their data.
