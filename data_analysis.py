import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import math
import utility_functions as uf


# Requires: All other columns except for a column that contains data should either be in type float or int.
# Modifies: target_file.
# Effects: Shows number of entries, average, standard deviation, min, and max of all columns except for the date column
def stat_measures(target_file, target_file_name, date_col_name):
    print('Statistical measures for ', target_file_name,':', sep='', end='\n')
    non_date_col_list = target_file.columns.values.tolist()
    non_date_col_list.remove(date_col_name)
    for i in non_date_col_list:
        N = len(target_file[i])
        average = target_file[i].mean()
        std = target_file[i].std()
        min = target_file[i].min()
        max = target_file[i].max()

        print('For', i, 'column:','[Number of entries = ', N,', Average = ',average,', STD = ',std,', Min = ',min,', Max = ', max,']', end='\n')
        

# -----------------------------------------------------------------------------------------------------------------------------
# Building autoregressive integrated moving average (ARIMA)

# Requires: All other columns except for a column that contains data should either be in type float or int.
# Modifies: None.
# Effects: Builds ARIMA and graph the result.
def arima(target_file,target_col_name, steps):
    from statsmodels.tsa.arima.model import ARIMA
    from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
    from statsmodels.tsa.stattools import adfuller

    print('ARIMA:', end='\n')

    # Running Augmented Dickey-Fuller test to determine d value
    print('Augmented Dickey-Fuller (ADF) test using significant level (alpha) of 0.05: ')
    temp_data = target_file[target_col_name].copy()
    d = 0
    while True:
        adf_test_result = adfuller(temp_data.dropna())
        if adf_test_result[1] < 0.05:
            # Data is stationary
            print('data is stationary at d =', d, end='\n')
            print('This d value will be used for ARIMA', end='\n\n')
            break
        else:
            # Data is non stationary
            temp_data = temp_data.diff()
            d += 1

    # Plotting PACF and ACF to determine q and p
    # Setting lags for PACF and ACF to be at most 50% of sample size of target_file
    tf_lags = math.floor(0.5 * len(target_file))
    plot_pacf(target_file[target_col_name], lags=tf_lags)
    plt.title('PACF')
    plt.xlabel('lags')
    plt.show()
    plot_acf(target_file[target_col_name], lags=tf_lags)
    plt.title('ACF')
    plt.xlabel('lags')
    plt.show()

    print('Now using PACF and ACF plotted on the right hand side, type in p and q values.', end='\n')
    print('Type p first, then q. They must be seperated by a comma', end='\n')
    pdq_input = uf.input_indices()

    # Fitting ARIMA model
    model = ARIMA(target_file[target_col_name], order=(pdq_input[0], d, pdq_input[1]))
    result = model.fit()

    print(result.summary())

    # Making predictions
    predictions = result.get_forecast(steps=steps)
    predicted_values = predictions.predicted_mean

    print('ARIMA results:', end='\n')
    print(predicted_values)

    # Graphing ARIMA results
    plt.plot(target_file[target_col_name], label='Observed')
    plt.plot(predicted_values, label='Predicted')
    plt.xlabel('time t (t = 0 is base time)')
    plt.title('ARIMA Graph')
    plt.legend()
    plt.show()


# -----------------------------------------------------------------------------------------------------------------------------
# Building vector autoregression (VAR)

# Requires: 1st, all other columns except for a column that contains data should either be in type float or int.
#
#           2nd, target_file must be stationarity.
# Modifies: None.
# Effects: Performs VAR using OLS and graph the result.
def var(target_file, steps):
    from statsmodels.tsa.api import VAR

    model = VAR(target_file)
    result = model.fit(ic='aic')
    print('Lag order:', result.k_ar)

    # Fitting
    fitted_model = model.fit(result.k_ar)
    print(fitted_model.summary())

    # Making predictions
    lag = target_file.values[-result.k_ar:]
    predictions = fitted_model.forecast(y=lag, steps=steps)
    predictions_index = range(len(target_file), len(target_file) + steps)
    predictions_df = pd.DataFrame(predictions, columns=target_file.columns, index=predictions_index)

    print('VAR predictions:', end='\n')
    print(predictions_df, end='\n')
    print('Note that index above represents time, where index 0 is the base period', end = '\n\n')

    # Graphing results
    for i in target_file.columns.values.tolist():
        plt.plot(target_file[i], label=i + ' Observed')
        plt.plot(predictions_df[i], label=i + ' Predicted')
    plt.xlabel('time t (t = 0 is base time)')
    plt.title('VAR Graph')
    plt.legend()
    plt.show()
