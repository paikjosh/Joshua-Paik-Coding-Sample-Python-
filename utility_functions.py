from scipy import stats


# Requires: none.
# Modifies: target_file.
# Effects: Takes multiple indices from user and delete inputted indies from the data
#Example: '11,12,13' -> 1st index to delete = 11, 2nd index to delete = 12, 3rd index to delete = 13
def del_file_data(target_file):
    while True:
        del_index = ''
        del del_index
        del_index = input()
        del_index = del_index.replace(' ', '')
        error_stat = False
        i = 0
        j = 0

        while j < len(del_index):
            # Finding position on comma in string inputted by the user
            if del_index[j] != ',' and j != len(del_index) - 1:
                j += 1
            # If position of comma is located, then make all inputs in between start of the user input and a located
            # comma or between previous located comma and current located comma to be the index to delete
            elif del_index[j] == ',':
                try:
                    temp = int(del_index[i:j])
                except ValueError:
                    print('Invalid row index input. Please type again.')
                    error_stat = True
                    break
                else:
                    target_file.drop(index=temp, inplace=True)
                    i = j + 1
                    j += 1
                    error_stat = False
            # If the end of user input is reached, then make all inputs in between the last located comma and the end of
            # the user input to be the index to delete.
            elif j == len(del_index) - 1:
                try:
                    temp = int(del_index[i:j + 1])
                except ValueError:
                    print('Invalid row index input. Please type again.')
                    error_stat = True
                    break
                else:
                    target_file.drop(index=temp, inplace=True)
                    j += 1
                    error_stat = False

        if error_stat == False:
            break

    target_file.reset_index(drop=True, inplace=True)

    return target_file



# Requires: None.
# Modifies: None.
# Effects: Takes user int input separated by a comma, then convert that into a int list
def input_indices():
    input_index = []
    while True:
        user_input = ''
        del user_input
        user_input = input()
        user_input = user_input.replace(' ', '')
        error_stat = False
        i = 0
        j = 0

        while j < len(user_input):
            # Finding position on comma in string inputted by the user
            if user_input[j] != ',' and j != len(user_input) - 1:
                j += 1
            # If position of comma is located, then make all inputs in between start of the user input and a located
            # comma or between previous located comma and current located comma to be the index to delete
            elif user_input[j] == ',':
                try:
                    temp = int(user_input[i:j])
                except ValueError:
                    print('Invalid values inputted. Please type again.')
                    error_stat = True
                    break
                else:
                    input_index.append(temp)
                    i = j + 1
                    j += 1
                    error_stat = False
            # If the end of user input is reached, then make all inputs in between the last located comma and the end of
            # the user input to be the index to delete.
            elif j == len(user_input) - 1:
                try:
                    temp = int(user_input[i:j + 1])
                except ValueError:
                    print('Invalid  values inputted. Please type again.')
                    error_stat = True
                    break
                else:
                    input_index.append(temp)
                    j += 1
                    error_stat = False

        if error_stat == False:
            break

    return input_index



# Requires: 1st, all non-date inputs should be in type int or float
#
#           2nd, 0 < alpha < 1
# Modifies: none.
# Effects: Tests normality of data. If there are more than 1 non-date columns (variables), then this
#          function uses Henze-Zirkler. Otherwise (i.e. 1 non-date column), it uses Shapiro-Wilk, Kolmogorov-Smirnov,
#          and Jarque-Bera test
def normal_test(target_file, date_col_name, alpha):
    import pingouin as pg

    target_file = target_file.drop(date_col_name, axis=1)

    print('------------------------------------------------------------------------------------------------',
          end='\n')
    print('Normality tests:', end='\n')
    if len(target_file.columns) > 1:
        # Henze-Zirkler test
        HZ_pval = pg.multivariate_normality(target_file)[1]
        if HZ_pval < alpha:
            print('Distribution is normal based on Henze-Zirkler test with significance level (alpha) of', alpha,
                  end='\n')
        else:
            print('Distribution is not normal based on Henze-Zirkler test with significance level (alpha) of', alpha,
                  end='\n')

    elif len(target_file.columns) == 1:
        # Shapiro-Wilk test
        SW_pval = stats.shapiro(target_file)[1]
        if SW_pval < alpha:
            print('Distribution is normal based on Shapiro-Wilk test with significance level (alpha) of', alpha,
                  end='\n')
        else:
            print('Distribution is not normal based on Shapiro-Wilk test with significance level (alpha) of', alpha,
                  end='\n')
        # Kolmogorov-Smirnov test
        KS_pval = stats.kstest(target_file, 'norm')[1]
        if KS_pval < alpha:
            print('Distribution is normal based on Kolmogorov-Smirnov test with significance level (alpha) of', alpha,
                  end='\n')
        else:
            print('Distribution is not normal based on Kolmogorov-Smirnov test with significance level (alpha) of', alpha,
                  end='\n')
        # Jarque-Bera test
        JB_pval = stats.jarque_bera(target_file)[1]
        if JB_pval < alpha:
            print('Distribution is normal based on Jarque-Bera test with significance level (alpha) of', alpha,
                  end='\n')
        else:
            print('Distribution is not normal based on Jarque-Bera test with significance level (alpha) of',
                  alpha,
                  end='\n')

    print('------------------------------------------------------------------------------------------------',
          end='\n')
