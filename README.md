# Joshua Paik Python Coding Sample
For this project, I have written codes in Python that cleans and performs basic analysis on time series data.

Descriptions of files in this repo:
  1) File titled "data_clean.py" contains a series of codes that cleans time series data.
  2) File titled "data_analysis.py" contains a series of codes that performs time series analysis.
  3) File titled "test.py" is where I have implemented codes that are on both files described above by using sample data of "TS_sample_data_euro(Sheet1)-2.csv" and "TS_sample_data_dollar(Sheet1)-2.csv"

All Python files in this repo contain descriptions of codes that I’ve written. However, all of them lack my thought process that went into writing those codes. Hence, I’ll use the space below to talk about that. 

convert_data_type(target_file)
-----
When the data is initially imported to Python, all entries are type string since they contain at least one symbol. But they must be in numerical form in order to clean and perform analysis. So, all non-date columns must be in type string, while date columns must convert to type datetime. That function was written to achieve such a task.

Note that this function first converts target_file into dataframe. This action was necessary since the data type for the date column and all other columns are different after converting and converting data into dataframe allows for different columns to have different data types.

In addition, note that this function converts some integers into type float. Of course, this isn’t the best practice since doing that decreases the computing efficiency. However, I have made this choice because when performing certain analysis, inputs may have to be in type float.

check_for_missing(target_file)
-----
The idea behind this function was to first check if missing data exists in any parts of the data, then give the user a chance to delete identified missing values. Giving the user a choice to deal with missing values is an important part of this function since removing missing values might not be the best way to deal with them. For example, if one can reasonably assume that a value is missing at random (MAR), then it is a good idea to perform an imputation to deal with that missing value.

check_outliers(target_file, date_col_name)
-----
This function was to detect outliers. When doing this, I thought it was a good idea to first create a visual representation of data before conducting formal outlier tests. This was because I thought making visual representation was a more intuitive way of understanding the distribution of the data and how certain data points fall into that distribution. So, the purpose of this was to allow for the user to first find outliers by looking at visual representation of their data, then they can conduct formal tests if they still feel the need to do that after looking at the visual representation.

