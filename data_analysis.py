import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import utility_functions as uf

# Looking at average and std of data containd in a specfic column

# Requires: All other columns except for a column that contains data should either be in type float or int.
# Modifies: target_file.
# Effects: Show average and standard deviation of all columns except for the date column
def stat_measures(target_file, target_file_name, date_col_name):
    print('Statistical measures for', target_file_name, end = '\n')
    non_date_col_list = target_file.columns.values.tolist()
    non_date_col_list.remove(date_col_name)
    for i in non_date_col_list:
        average = target_file[i].mean()
        std = target_file[i].std()

        print('For', i, 'column:','[average: ',average,', std:',std,']', end='\n')


# -----------------------------------------------------------------------------------------------------------------------------
# Building autoregressive integrated moving average (ARIMA)

# Requires: All other columns except for a column that contains data should either be in type float or int.
# Modifies: None.
# Effects: Build ARIMA and graph the result.
def arima(target_file,target_col_name, steps):
    from statsmodels.tsa.arima.model import ARIMA
    from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
    from statsmodels.tsa.stattools import adfuller

    print('ARIMA:', end='\n')

    # running Augmented Dickey-Fuller test to determine d value
    print('Augmented Dickey-Fuller (ADF) test using significant level (alpha) of 0.05: ')
    temp_data = target_file[target_col_name].copy()
    d = 0
    while True:
        adf_test_result = adfuller(temp_data.dropna())
        if adf_test_result[1] < 0.05:
            # data is stationary
            print('data is stationary at d =', d, end='\n')
            print('This d value will be used for ARIMA', end='\n\n')
            break
        else:
            # data is non stationary
            temp_data = temp_data.diff()
            d += 1

    # plotting acf and pacf to determine q and p
    plot_pacf(target_file[target_col_name], lags=4)
    plt.title('PACF')
    plt.xlabel('lags')
    plt.show()
    plot_acf(target_file[target_col_name], lags=4)
    plt.title('ACF')
    plt.xlabel('lags')
    plt.show()

    print('Now using PACF and ACF plotted on the right hand side, identify big spikes in each graphs.', end='\n')
    print(
        'Then, set p and q value equal to the value of lag in which PACF and ACF respectively experienced a big spike',
        end='\n')
    print('Type in p and q values below. Type p first, then q. They must be seperated by a comma', end='\n')
    pdq_input = uf.input_indices()

    # fit ARIMA model
    model = ARIMA(target_file[target_col_name], order=(pdq_input[0], d, pdq_input[1]))
    result = model.fit()

    print(result.summary())

    # predictions
    predictions = result.get_forecast(steps=steps)
    predicted_values = predictions.predicted_mean

    print('ARIMA results:', end='\n')
    print(predicted_values)

    # graphing ARIMA results
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
# Effects: Performs VAR and graph the result.
def var(target_file, steps):
    from statsmodels.tsa.api import VAR

    model = VAR(target_file)
    result = model.fit(ic='aic')
    print('Lag order:', result.k_ar)

    # fitting
    fitted_model = model.fit(result.k_ar)
    print(fitted_model.summary())

    # predictions
    lag = target_file.values[-result.k_ar:]
    predictions = fitted_model.forecast(y=lag, steps=steps)
    predictions_index = range(len(target_file), len(target_file) + steps)
    predictions_df = pd.DataFrame(predictions, columns=target_file.columns, index=predictions_index)

    print('VAR predictions:', end='\n')
    print(predictions_df, end='\n')
    print('Note that index above represents time, where index 0 is the base period', end = '\n\n')

    # graphing results
    for i in target_file.columns.values.tolist():
        plt.plot(target_file[i], label=i + ' Observed')
        plt.plot(predictions_df[i], label=i + ' Predicted')
    plt.xlabel('time t (t = 0 is base time)')
    plt.title('VAR Graph')
    plt.legend()
    plt.show()
