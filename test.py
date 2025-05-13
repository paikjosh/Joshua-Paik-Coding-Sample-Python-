import pandas as pd
import numpy as np
import utility_functions as uf
import data_clean as dc
import data_analysis as da

# Cleaning data

print('Cleaning data', end='\n\n')

# Cleaning euro file
print('Cleaning euro file:', end='\n')

# Importing file
euro_file_name = '/Users/joshpaik/Downloads/TS_sample_data_euro(Sheet1)-4.csv'

try:
    euro_file = pd.read_csv(euro_file_name, encoding='utf-8')
except UnicodeDecodeError:
    try:
        euro_file = pd.read_csv(euro_file_name, encoding='latin-1')
    except UnicodeDecodeError:
        euro_file = pd.read_csv(euro_file_name, encoding='cp1252')

print('Original data: ', end='\n')
print(euro_file, end='\n\n')

euro_file_df = dc.convert_input(target_file=euro_file, date_col_name='Date') # note that convert_input converts
print('Euro file after converting entries data type: ', end='\n')                 # target_file into dataframe
print(euro_file_df, end='\n\n')

euro_file_df = dc.check_for_missing(target_file=euro_file_df)

euro_file_df = dc.check_duplicates(target_file=euro_file_df, date_col_name='Date')
print('')

euro_file_df = dc.check_outliers(target_file=euro_file_df, date_col_name='Date')
print('')

euro_file_df = dc.arrange_file(target_file=euro_file_df, target_col_name='Date')
print('')

euro_file_df = dc.normalize_data(target_file=euro_file_df, date_col_name='Date')
print('')
print('')

#----------------------------------------------------------------------------------------------------------------------------------------------
# Analyzing data
print('----------------------------------------------------------------------------------------------------------------------------------------------', end='\n')
print('Analyzing data', end='\n\n')

da.stat_measures(target_file=euro_file_df, target_file_name='euro_file', date_col_name='Date')
print('')

# Forcasting measures on euro_file
da.arima(euro_file_df, 'Revenue',10)

euro_file_station = dc.convert_stationarity(euro_file_df, 'Date')

da.var(euro_file_station, 10)
