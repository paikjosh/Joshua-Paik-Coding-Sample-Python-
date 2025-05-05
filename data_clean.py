import pandas as pd
import numpy as np
import re
from scipy import stats
import matplotlib.pyplot as plt
import utility_functions as uf

# Converting data type

# Requires: All inputs of the data should be in type str.
# Modifies: target_file.
# Effects: 1st, remove all unnecessary characters in all non-date inputs of the data, then convert them into type float
#
#          2nd, convert date inputs into datetime
# Example: $100,000.01 -> 100,000.01
def convert_input(target_file, date_col_name):
    target_file_df = pd.DataFrame(target_file)

    non_date_col_list = target_file.columns.values.tolist()
    non_date_col_list.remove(date_col_name)

    for i in non_date_col_list:
        # removing all characters except for dot and numbers in columns that aren't the date column
        target_file_df[i] = target_file_df[i].replace(r'[^\d.]', '', regex=True).astype(float)

    target_file_df[date_col_name] = pd.to_datetime(target_file_df[date_col_name], format='%m/%d/%Y')

    return target_file_df



# Requires: None.
# Modifies: target_file.
# Effects: set dates to be indices
def dates_to_index(target_file, date_col_name):
    target_file.set_index(target_file[date_col_name], inplace=True)
    target_file = target_file.drop(date_col_name, axis=1)

    return target_file



# Requires: 1st, all date inputs should be in type datetime
#
#           2nd, all non-date inputs should be in type int or float
# Modifies: target_file.
# Effects: 1st, insert symbols and commas to financial inputs
#
#          2nd, convert datetime into specific format
def convert_money_input_to_str(target_file, date_col_name, currency_unit):
    non_date_col_list = target_file.columns.values.tolist()
    non_date_col_list.remove(date_col_name)

    for i in non_date_col_list:
        target_file[i] = target_file[i].apply(lambda x: "{:,.2f}".format(x)).astype(str).radd(currency_unit)
        #target_file[i] = target_file[i].astype(str).radd(currency_unit)

    target_file[date_col_name] = target_file[date_col_name].dt.strftime('%-m/%-d/%Y')

    return target_file

#----------------------------------------------------------------------------------------------------------------------------------------------
# Checking for missing data entries

# Requires: None.
# Modifies: Possibly target_file.
# Effects: Checks for all missing inputs on target_file, then gives a chance for the user to remove the missing data.
def check_for_missing(target_file):
    # checking for missing data
    nan_row = target_file[target_file.isnull().any(axis = 1)]
    # giving choice to remove missing inputs if they exist
    if len(nan_row) >= 1:
        print('Row/s that contain missing value:', end = '\n')
        print(nan_row)
        print("Do you wish to remove any missing data? Type yes or no.", end = '\n')

        while True:
            user_input = ''
            del user_input
            user_input = input()
            user_input = user_input.lower()
            user_input = user_input.replace(' ', '')

            if user_input == 'yes':
                print(
                    'Type row index or indices of input that you wish to remove.',
                    end='\n')
                print('Each indices must to separated by a comma', end = '\n')
                print('Row index is located at left side missing values displayed above', end='\n')
                target_file = uf.del_file_data(target_file=target_file)
                target_file.reset_index(drop=True, inplace=True)
                break
            elif user_input == 'no':
                break
            else:
                print('Invalid input. Please type yes or no.')

    else:
        print('No missing data found.', end='\n')

    print('Data after removing: ', end='\n')
    print(target_file, end='\n\n')

    return target_file

#----------------------------------------------------------------------------------------------------------------------------------------------
# Checking outliers

# Requires: all non-date inputs should be in type int or float
# Modifies: Possibly target_file.
# Effects: Identify outliers in a data using Z-score method with threshold given by the user and give a chance to the
# user regarding removing identified outliers.
def out_z_score(target_file, date_col_name):
    outlier_z = []
    non_date_col_list = arget_file.columns.values.tolist()
    non_date_col_list.remove(date_col_name)

    print(
        'Type an absolute value of a threshold for Z-score (ex: 3 should be entered if you want threshold to be ±3):',
        end='\n')
    # taking user input for threshold
    while True:
        threshold_input = ''
        del threshold_input
        threshold_input = input()
        threshold_input = threshold_input.replace(' ', '')

        try:
            threshold_input = int(threshold_input)
        except ValueError:
            print('Invalid threshold input. Please type again.')
        # outlier test based on user provided threshold
        else:
            z_score = stats.zscore(target_file[non_date_col_list])
            outlier = target_file[np.abs(z_score) > threshold_input]
            break
    # appending Z-score to data
    for i in range(0, len(outlier)):
        outlier_index = outlier.index[i]
        outlier_z.append(z_score[outlier_index])

    outlier = outlier.copy()
    outlier['Z-score'] = outlier_z
    # giving user the choice to remove outliers if they exist
    if outlier.empty == False:
        print('Outlier found using Z-score method: ', end='\n')
        print(outlier, end='\n')
        print('Do you wish to remove any outliers identified? Type yes or no', end='\n')

        while True:
            outlier_dec_input = ''
            del outlier_dec_input
            outlier_dec_input = input()
            outlier_dec_input = outlier_dec_input.lower()
            outlier_dec_input = outlier_dec_input.replace(' ', '')

            if outlier_dec_input == 'yes':
                print(
                    'Type row index or indices of outlier that you wish to remove. Each indices must to separated by a comma. ',
                    end='\n')
                print('Note that row index is located at the left most area of outliers displayed above.', end='\n')

                target_file = uf.del_file_data(target_file=target_file)
                break
            elif outlier_dec_input == 'no':
                break
            else:
                print('Invalid input. Please type yes or no.')
    else:
        print('No outlier in this data', end='\n\n')

    return target_file



# Requires: all non-date inputs should be in type int or float
# Modifies: Possibly target_file.
# Effects: Identify outliers in a data using IQR method with threshold given by the user and give a chance to the
# user regarding removing identified outliers.
def out_iqr(target_file, date_col_name):
    outlier = []
    non_date_col_list = target_file.columns.values.tolist()
    non_date_col_list.remove(date_col_name)

    for i in non_date_col_list:
        q1 = target_file[i].quantile(0.25)
        q3 = target_file[i].quantile(0.75)
        iqr = q3 - q1

        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        # outlier test
        outlier.append(target_file[(target_file[i] < lower_bound) | (target_file[i] > upper_bound)])
    # giving user the choice to remove outliers if they exist
    if outlier:
        print('Outlier found using IQR method: ', end='\n')
        print(outlier, end='\n')
        print('Do you wish to remove any outliers identified? Type yes or no', end='\n')

        while True:
            outlier_dec_input = ''
            del outlier_dec_input
            outlier_dec_input = input()
            outlier_dec_input = outlier_dec_input.lower()
            outlier_dec_input = outlier_dec_input.replace(' ', '')

            if outlier_dec_input == 'yes':
                print('Type row index or indices of outlier that you wish to remove. Each indices must be separated by a comma. ', end='\n')
                print('Note that row index is located at the left most area of outliers displayed above.',
                      end='\n')

                target_file = uf.del_file_data(target_file=target_file)
                break
            elif outlier_dec_input == 'no':
                break
            else:
                print('Invalid input. Please type yes or no.')
        target_file.reset_index(drop=True, inplace=True)
    else:
        print('No outlier in this data', end='\n\n')

    return target_file



# Requires: 1st, data should be a matrix with real number entries
#
#           2nd, mean should be a vector with real number entries
#
#           3rd, cov should be an invertible matrix with real number entries.
# Modifies: None.
# Effects: Calculates Mahalanobis distance
def mahalanobis_dist(data, mean, cov):
    from scipy.spatial.distance import mahalanobis

    mah_dist = []
    data = pd.DataFrame(data)

    try:
        inverse_cov = np.linalg.inv(cov)
    except np.linalg.LinAlgError:
        cov += np.eye(cov.shape[0]) * 1e-6
        inverse_cov = np.linalg.inv(cov)

    for i in range(data.shape[0]):
        mah_dist.append(mahalanobis(data.iloc[i], mean, inverse_cov))

    return mah_dist



# Requires: 1st, all non-date inputs should be in type int or float
#
#           2nd, 0 < alpha < 1
# Modifies: Possibly target_file.
# Effects: Determine outliers using Mahalanobis distance with threshold for Mahalanobis distance given by the user.
#          Then, gives a choice to users regarding removing identified outliers.
def out_mahalanobis_dist(target_file, date_col_name, alpha):
    outliers = []

    data = target_file.drop(date_col_name, axis=1)

    mean = data.mean().values
    cov = data.cov().values
    # calculating Mahalanobis distance
    m_dist = mahalanobis_dist(data, mean, cov)
    # calculating chi-square so that is can be used as a threshold if user wants to
    degree_of_freedom = data.shape[1]
    chi_square = stats.chi2.ppf(1 - alpha, degree_of_freedom)

    data['Mahalanobis distance'] = m_dist

    print('Type a threshold for Mahalanobis Distance (note that chi-square value calculated', end = '\n')
    print('using significance level (alpha) of ', alpha, ' is ', chi_square, ')', sep = '', end = '\n')
    print('You can type "chi2" is you want your threshold to be the chi-square value calculated above', end = '\n')
    # taking user input for threshold
    while True:
        m_threshold_input = ''
        del m_threshold_input
        m_threshold_input = input()
        m_threshold_input = m_threshold_input.replace(' ', '')
        if m_threshold_input == 'chi2':
            m_threshold_input = chi_square
        try:
            m_threshold = float(m_threshold_input)
        except ValueError:
            print('Invalid input. Please type a real number.', end='\n')
        # identifying outliers using calculated Mahalanobis distance
        else:
            outliers = data[data['Mahalanobis distance'] > m_threshold]
            break
    # giving user the choice to remove outliers if they exist
    if outliers.empty == False:
        print('Outlier found using mahalanobis method: ', end='\n')
        print(outliers, end='\n')

        print('Do you wish to remove any outliers identified? Type yes or no.', end='\n')
        while True:
            outlier_dec_input = ''
            del outlier_dec_input
            outlier_dec_input = input()
            outlier_dec_input = outlier_dec_input.lower()
            outlier_dec_input = outlier_dec_input.replace(' ', '')

            if outlier_dec_input == 'yes':
                print('Type row index or indices of outlier that you wish to remove. Each indices must be separated by a comma. ', end='\n')
                print('Note that row index is located at the left most area of outliers displayed above.',
                      end='\n')

                target_file = uf.del_file_data(target_file = target_file)
                break
            elif outlier_dec_input == 'no':
                break
            else:
                print('Invalid input. Please type yes or no.')
        target_file.reset_index(drop=True, inplace=True)
    else:
        print('No outlier in this data', end='\n\n')

    return target_file



# Requires: 1st, column that contains dates should be in type datetime.
#
#           2nd, all other columns except for a column that contains data should either be in type float or int.
# Modifies: Possibly target_file.
# Effects: 1st, plot the data and gives a chance for the user to identify and remove outliers based
#          on the plotted data. If there are 2 variables, including time variable, then this function generates
#          scatter plot. Otherwise (i.e. more than 2 variables), it plots Mahalanobis distance.
#
#          2nd, run statistical tests to identify outliers, then gives a chance for the user to remove identified
#          outliers. If there are 2 variable, including time variable, then this function runs IQR and Z-score tests
#          to identify outliers. Otherwise, it uses Mahalanobis distance.
def check_outliers(target_file, date_col_name):
    non_date_col_list = target_file.columns.values.tolist()
    non_date_col_list.remove(date_col_name)

    # 1st plotting to get some sense of outliers
    # plotting 2d graph when there are only 2 variables in the data
    if len(target_file.columns) == 2:

        print('Identifying outliers:', end='\n')
        print('First, scatter plot of data is plotted on the right hand side of this screen.', end = '\n')

        sal_col = non_date_col_list[0]

        plt.scatter(target_file[date_col_name], target_file[sal_col])
        # Putting row indices to plotted data
        for i, txt in enumerate(target_file.index):
            plt.annotate(txt, (target_file[date_col_name][i], target_file[sal_col][i]))

        plt.xlabel(date_col_name)
        plt.ylabel(sal_col)
        plt.title('Sale Data Scatter Plot with Row Index')
        plt.grid(True)
        plt.show()

        print('Do you wish to remove outliers based on plotted data? Type yes or no.', end='\n')
        while True:
            plot_out_del_input = ''
            del plot_out_del_input
            plot_out_del_input = input()
            plot_out_del_input = plot_out_del_input.lower()
            plot_out_del_input = plot_out_del_input.replace(' ', '')
            if plot_out_del_input == 'yes':
                print('Provide row index or indices of outliers that you wish to remove.')
                target_file = uf.del_file_data(target_file=target_file)
                break
            elif plot_out_del_input == 'no':
                break
            else:
                print('Invalid input. Please type yes or no.')
    # plotting Mahalanobis distance when there are more than 2 variables in the data
    elif len(target_file.columns) > 2:
        print('Identifying outliers:', end='\n')
        print('First, bar garph that show mahalanobis distance of each data points is plotted on the right hand side of this screen.',
              end='\n')
        print('For your reference, normality tests will be conducted to determine if your data is normal or not.', end='\n')
        uf.normal_test(target_file=target_file, date_col_name=date_col_name, alpha=0.05)

        data = target_file.drop(date_col_name, axis=1)

        mean = data.mean().values
        cov = data.cov().values
        m_dist = mahalanobis_dist(data, mean, cov)

        plt.bar(target_file.index, m_dist, color = 'deepskyblue')

        plt.title('Mahalanobis distance')
        plt.xlabel('row index of data points')
        plt.ylabel('Mahalanobis distance')

        plt.show()

        print('Do you wish to remove outliers based on plotted data? Type yes or no.', end='\n')
        while True:
            plot_out_del_input = ''
            del plot_out_del_input
            plot_out_del_input = input()
            plot_out_del_input = plot_out_del_input.lower()
            plot_out_del_input = plot_out_del_input.replace(' ', '')
            if plot_out_del_input == 'yes':
                print('Provide row index or indices of outliers that you wish to remove.')
                target_file = uf.del_file_data(target_file=target_file)
                break
            elif plot_out_del_input == 'no':
                break
            else:
                print('Invalid input. Please type yes or no.')


    # 2nd running tests to find outlier
    if len(target_file.columns) == 2:
        print('In addition to scatter plot, outliers can be determined using 2 statistical methods: '
              'Z-score and interquartile range (IQR).', end = '\n')
        print('For your reference, normality tests will be conducted to determine if your data is normal or not.', end = '\n')
        uf.normal_test(target_file=target_file, date_col_name=date_col_name, alpha=0.05)
        print('Do you wish to use either statistical methods mentioned above to identify outliers? Type yes or no', end = '\n')
    elif len(target_file.columns) > 2:
        print('Now, precise Mahalanobis distance can be calculated to identify outliers.', end='\n')
        print('Do you wish to do that? Type yes or no', end='\n')

    while True:
        stat_method_dec_input = ''
        del stat_method_dec_input
        stat_method_dec_input = input()
        stat_method_dec_input = stat_method_dec_input.lower()
        stat_method_dec_input = stat_method_dec_input.replace(' ', '')
        # running test in 2 variables case
        if stat_method_dec_input == 'yes' and len(target_file.columns) == 2:
            print('Choose and type in a desired method (you may type IQR for Interquartile Range):', end = '\n')

            while True:
                outlier_method_input = ''
                del outlier_method_input
                outlier_method_input = input()
                outlier_method_input = outlier_method_input.lower()
                outlier_method_input = outlier_method_input.replace(' ', '')

                if outlier_method_input == 'z-score' or outlier_method_input == 'zscore':
                    target_file = out_z_score(target_file, date_col_name)
                    break
                elif outlier_method_input == 'interquartilerange' or outlier_method_input == 'iqr':
                    target_file = out_iqr(target_file, date_col_name)
                    break
                else:
                    print('Invalid input. Please try again.', end = '\n')
            break
        # running test in more than 2 variables case
        elif stat_method_dec_input == 'yes' and len(target_file.columns) > 2:
            target_file = out_mahalanobis_dist(target_file, date_col_name, 0.05)
            break
        elif stat_method_dec_input == 'no':
            break
        else:
            print('Invalid input. Please type yes or no.')

    target_file.reset_index(drop=True, inplace=True)

    return target_file

#----------------------------------------------------------------------------------------------------------------------------------------------
# Arranging file by certain criteria

# Requires: column that contains dates should be in type datetime.
# Modifies: target_file.
# Effects: Arrange data based on content of target_col_name in the order smallest to greatest or oldest to newest.
# Example: if target_col_name = 'Date', then this function arranges file based on dates, where the oldest date
# comes first.
def arrange_file_date(target_file, target_col_name):
    sorted_file = target_file.sort_values(by=[target_col_name])

    sorted_file.reset_index(drop=True, inplace=True)

    print('Data after arranging data by date: ', end = '\n')
    print(sorted_file)

    return sorted_file

#----------------------------------------------------------------------------------------------------------------------------------------------

# Requires: none
# Modifies: Possibly target_file.
# Effects: 1st, check for duplicates that have the same value throughout all columns and remove one them right away.
#
#          2nd, check for duplicates that have the same data value, then gives a chance to th user regarding removing
#          one of them.
def check_duplicates(target_file, date_col_name):
    print('Checking for duplicates.', end = '\n')

    # 1st dealing with duplicates that have the same value throughout all columns
    all_val_dup = target_file.duplicated()
    all_val_dup_index = []
    no_all_val_dup_indicator = False

    # obtaining row index for duplicates.
    for i in range(0, len(all_val_dup)):
        if all_val_dup[i]:
            all_val_dup_index.append(i)

    # removing duplicates
    if any(all_val_dup): # if there exists at least one True in all_val_dup
        print('Exact duplicates: ', end = '\n')
        print(target_file[all_val_dup], end = '\n')
        print('All duplicates above will be removed', end = '\n\n')
        target_file.drop(index=all_val_dup_index, inplace=True)
    else:
        no_all_val_dup_indicator = True

    # 2nd dealing with duplicates that has the same date.
    date_val_dup = target_file[date_col_name].duplicated(keep=False)  # keep = False since I wish to display all
    no_date_val_dup_indicator = False                                 # duplicated data in this case.

    # giving user the choice to deal with data that has the same date if it exists
    if any(date_val_dup):
        print('Date duplicates: ', end='\n')
        print(target_file[date_val_dup], end = '\n')
        print('Do you wish to remove any duplicated data above? Type yes or no.', end = '\n')
        while True:
            date_dup_remove_input = ''
            del date_dup_remove_input
            date_dup_remove_input = input()
            date_dup_remove_input = date_dup_remove_input.replace(' ', '').lower()
            if date_dup_remove_input == 'yes':
                print('Type in row index of data that you wish to remove', end = '\n')
                target_file = uf.del_file_data(target_file=target_file)
                break
            elif date_dup_remove_input == 'no':
                break
            else:
                print('Invalid input. Type again.', end = '\n')
    else:
        no_date_val_dup_indicator = True

    if no_all_val_dup_indicator and no_date_val_dup_indicator:
        print('No duplicates in this data.', end = '\n')

    target_file.reset_index(drop=True, inplace=True)

    print('Data after taking care of duplicates:', end='\n')
    print(target_file)

    return target_file

#----------------------------------------------------------------------------------------------------------------------------------------------
# Normalizing data

# Requires: All non-date inputs should be in type int or float
# Modifies: target_file.
# Effects: normalize data using min-max scaling
def normalize_min_max(target_file, date_col_name):
    from sklearn.preprocessing import MinMaxScaler

    scaler = MinMaxScaler()
    date_col = target_file[date_col_name]
    # dropping date column before normalizing since it shouldn't be normalized
    target_file = target_file.drop(date_col_name, axis=1)

    target_file = pd.DataFrame(scaler.fit_transform(target_file), columns=target_file.columns)
    # inserting back dropped date column before displaying normalized data
    target_file.insert(0, date_col_name, date_col)

    return target_file



# Requires: All non-date inputs should be in type int or float
# Modifies: target_file.
# Effects: normalize data using Z-score scaling
def normalize_z_score(target_file, date_col_name):
    from sklearn.preprocessing import StandardScaler

    scaler = StandardScaler()
    date_col = target_file[date_col_name]
    # dropping date column before normalizing since it shouldn't be normalized
    target_file = target_file.drop(date_col_name, axis=1)

    target_file = pd.DataFrame(scaler.fit_transform(target_file), columns = target_file.columns)
    # inserting back dropped date column before displaying normalized data
    target_file.insert(0, date_col_name, date_col)

    return target_file



# Requires: All other columns except for a column that contains data should either be in type float or int.
# Modifies: target_file.
# Effects: Normalize data using one of 2 methods: min-max scaling and Z-score standardization. User can pick the method.
def normalize_data(target_file, date_col_name):
    print('Normalizing data:', end = '\n')
    print('There are 2 methods for normalizing data: min-max scaling and Z-score standardization.', end = '\n')
    print('For your reference, normality tests will be conducted to determine if your data is normal or not.', end='\n')
    uf.normal_test(target_file=target_file, date_col_name=date_col_name, alpha=0.05)
    print('Type in the method that you want to use.' , end = '\n')
    print('Type "minmax" for min-max scaling and "zscore" for Z-score standardization', end = '\n')

    while True:
        normalize_method_input = ''
        del normalize_method_input
        normalize_method_input = input()
        normalize_method_input = normalize_method_input.lower()
        normalize_method_input = normalize_method_input.replace(' ', '').replace('-', '').replace('_', '')

        if normalize_method_input == 'minmax':
            target_file = normalize_min_max(target_file, date_col_name)
            print('Data after min-max normalization: ', end = '\n')
            print(target_file, end = '\n\n')
            break
        elif normalize_method_input == 'zscore':
            target_file = normalize_z_score(target_file, date_col_name)
            print('Data after Z-score normalization: ', end='\n')
            print(target_file, end='\n\n')
            break
        else:
            print('Invalid normalization method input. Type again.', end = '\n')

    return target_file

#----------------------------------------------------------------------------------------------------------------------------------------------
# Convert data to be stationary

# Requires: All other columns except for a column that contains data should either be in type float or int.
# Modifies: target_file.
# Effects: make data stationarity through differencing.
def convert_stationarity(target_file, date_col_name):
    print('Converting data to stationarity:', end = '\n')

    from statsmodels.tsa.stattools import adfuller

    non_date_col_list = target_file.columns.values.tolist()
    non_date_col_list.remove(date_col_name)
    station_target_file = []
    station_df = pd.DataFrame(station_target_file)
    # differencing
    for i in non_date_col_list:
        print('Augmented Dickey-Fuller (ADF) test using significant level (alpha) of 0.05: ')
        temp_data = target_file[i].copy()
        d = 0
        while True:
            adf_test_result = adfuller(temp_data.dropna(how='all'))
            if adf_test_result[1] < 0.05:
                # data is stationary
                print('data is stationary at d =', d, end='\n')
                break
            else:
                # data is non stationary
                temp_data = temp_data.diff()
                d += 1
        station_df[i] = temp_data.dropna(how='all')

    station_df.reset_index(drop=True, inplace=True)
    # removing Nan values that was created as a result of differencing
    print('Checking for missing values when converting data to stationarity:', end='\n')
    station_df = check_for_missing(station_df)

    return station_df
