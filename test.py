import pandas as pd
import numpy as np
import utility_functions as uf
import data_clean as dc
import data_analysis as da

# cleaning data

print('Cleaning data', end='\n\n')

# importing euro file
euro_file_name = '/Users/joshpaik/Downloads/TS_sample_data_euro(Sheet1)-2.csv'

try:
    euro_file = pd.read_csv(euro_file_name, encoding='utf-8')
except UnicodeDecodeError:
    try:
        euro_file = pd.read_csv(euro_file_name, encoding='latin-1')
    except UnicodeDecodeError:
        euro_file = pd.read_csv(euro_file_name, encoding='cp1252')

print('Original data: ', end='\n')
print(euro_file, end='\n\n')

# cleaning euro file
euro_file_df = dc.convert_input(target_file=euro_file, date_col_name='Date') # note that convert_input converts
print('Data after converting entries data type: ', end='\n')                 # target_file into dataframe
print(euro_file_df, end='\n\n')

euro_file_df = dc.check_for_missing(target_file=euro_file_df)

euro_file_df = dc.check_outliers(target_file=euro_file_df, date_col_name='Date')
print('')

euro_file_df = dc.arrange_file_date(target_file=euro_file_df, target_col_name='Date')
print('')

euro_file_df = dc.check_duplicates(target_file=euro_file_df, date_col_name='Date')
print('')

euro_file_df = dc.normalize_data(target_file=euro_file_df, date_col_name='Date')
print('')



# importing dollar file
dollar_file_name = '/Users/joshpaik/Downloads/TS_sample_data_dollar(Sheet1)-2.csv'

try:
    dollar_file = pd.read_csv(dollar_file_name, encoding='utf-8')
except UnicodeDecodeError:
    try:
        dollar_file = pd.read_csv(dollar_file_name, encoding='latin-1')
    except UnicodeDecodeError:
        dollar_file = pd.read_csv(dollar_file_name, encoding='cp1252')

# cleaning dollar file
print('Original data: ', end='\n')
print(dollar_file, end='\n\n')

dollar_file_df = dc.convert_input(target_file=dollar_file, date_col_name='Date') # note that convert_input converts
print('Data after converting entries data type: ', end='\n')                     # target_file into dataframe
print(dollar_file_df, end='\n\n')

dollar_file_df = dc.check_for_missing(target_file=dollar_file_df)

# estimating value for missing sale amount by taking average
oct_sale = []
for i in range(0, len(dollar_file)):
    if (dollar_file_df['Date'].dt.month[i] == 10 and
            dollar_file_df['Date'].dt.year[i] == 2025 and
            dollar_file_df.isnull().iloc[i, 1] == False):
        oct_sale.append(dollar_file_df['Revenue'][i])

average = sum(oct_sale) / len(oct_sale)
dollar_file_df.at[9, 'Revenue'] = average

print('Data after estimating for missing data on row 9: ', end='\n')
print(dollar_file_df, end='\n\n')

dollar_file_df = dc.check_outliers(target_file=dollar_file_df, date_col_name='Date')
print('')

dollar_file_df = dc.arrange_file_date(target_file=dollar_file_df, target_col_name='Date')
print('')

dollar_file_df = dc.check_duplicates(target_file=dollar_file_df, date_col_name='Date')
print('')

dollar_file_df = dc.normalize_data(target_file=dollar_file_df, date_col_name='Date')
print('')

#----------------------------------------------------------------------------------------------------------------------------------------------
# Analyzing data

print('Analyzing data', end='\n\n')

# comparing two datasets
da.stat_measures(target_file=euro_file_df, target_file_name='euro_file', date_col_name='Date')
print('')
da.stat_measures(target_file=dollar_file_df, target_file_name='dollar_file', date_col_name='Date')
print('')

# forcasting measures on euro_file
da.arima(euro_file_df, 'Revenue',10)

euro_file_station = dc.convert_stationarity(euro_file_df, 'Date')

da.var(euro_file_station, 10)



# forcasting measures on dollar_file
da.arima(dollar_file_df, 'Revenue',10)

dollar_file_station = dc.convert_stationarity(dollar_file_df, 'Date')

da.var(dollar_file_station, 10)
