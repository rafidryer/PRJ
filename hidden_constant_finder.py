import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


# Define the objective function with O(n*log(n)) time complexity.
def objective_constant(x, a):
    return 0*x+a

# Define the objective function with O(n^2) time complexity.
def objective_n(x, a):
    return x * a


# Define the objective function with O(n*log(n)) time complexity.
def objective_n_log(x, a):
    return a * np.log(x)


# Define the objective function with O(n*log(n)) time complexity.
def objective_n_log_n(x, a):
    return x * a * np.log(x)


# Define the objective function with O(n^2) time complexity.
def objective_n_squared(x, a):
    return x * a * x

# Define the objective function with O(n^2) time complexity.
def objective_exponential(x, a):
    return a ** x


# Calculate root mean square error.
def calculate_rmse(predictions, targets):
    return np.sqrt(((predictions - targets) ** 2).mean())


# Plot the curve fit.
def plot_curve_fit(x, y, objective, best_fit_coefficient, upper_bound_coefficient, shape, column_name, x0):
    fig = plt.figure()
    fig.suptitle(column_name)
    plt.plot(x, y, label="Data") # plots actual data
    #plots line of best fit
    x_line = np.arange(min(x), max(x), 1)
    y_line = objective(x_line, best_fit_coefficient)
    plt.plot(x_line, y_line, "--", color="red", label=f"Best fit: {str(round(best_fit_coefficient[0], 2))}*{shape}")
    # plots upper bounds line
    y_line2 = objective(x_line, [upper_bound_coefficient])
    plt.plot(x_line, y_line2, "--", color="green", label=f"Upper Bound: {str(round(upper_bound_coefficient, 2))}*{shape}")
    plt.axvline(x=x0, linestyle="--", color='y')
    plt.grid(True)
    plt.xlabel("Size of List")
    plt.ylabel("Time (NanoSeconds)")
    plt.legend()

    plt.draw()


def find_parameters(x, y):
    # define objective functions
    objectives = [objective_constant, objective_n_log, objective_n, objective_n_log_n, objective_n_squared, objective_exponential ]

    # perform curve fits and calculate RMSEs
    rmse_values = []
    coefficient_values = []
    for objective in objectives:
        coefficients, _ = curve_fit(objective, x, y)
        y_fit = objective(x, coefficients)
        rmse = calculate_rmse(y, y_fit)
        rmse_values.append(rmse)
        coefficient_values.append(coefficients)

    # determine the smallest RMSE and return the corresponding parameters
    min_index = rmse_values.index(min(rmse_values))
    
    #returns values depending on the time complexity of the data
    if min_index == 5:
        return "2^n", coefficient_values[min_index], objectives[min_index]
    elif min_index == 4:
        return "n^2", coefficient_values[min_index], objectives[min_index]
    elif min_index == 3:
        return "n log n", coefficient_values[min_index], objectives[min_index]
    elif min_index == 2:
        return "n", coefficient_values[min_index], objectives[min_index]
    elif min_index == 1:
        return "log n", coefficient_values[min_index], objectives[min_index]
    else:
        return "Constant", coefficient_values[min_index], objectives[min_index]


def find_upper_bound(x, y, bigO):
    upper_bound = 0
    for x_val, y_val in zip(x, y):
        # finds the coefficient for that one data point
        calculated_coefficient = y_val / bigO(x_val, 1)
        #ensures the data point is within the upper bound
        if calculated_coefficient > upper_bound:
            upper_bound = calculated_coefficient
    return upper_bound


def format_data():
    file_name = input("Enter file name: ")
    title = file_name[:file_name.find("_")]
    url = os.path.join(os.getcwd(), "results", f"{file_name}.csv")
    return title, pd.read_csv(url)


# Main function that fits O(n^2) and O(n*log(n)) curves to data.
def main():
    title, dataframe = format_data()

    # change smallest input size from 0 to 1 as there is no result for log(0)
    if dataframe.iloc[0, 0] == 0:
        dataframe.iloc[0, 0] = 1

    for column in dataframe.columns[1:]:
        x, y = dataframe.iloc[:, 0], dataframe[column]

        shape, coefficient, objective = find_parameters(x, y)

        # only finds upper bound of values after the 20% mark
        twenty_percent_mark = len(x) // 5
        coefficient2 = find_upper_bound(x[twenty_percent_mark:], y[twenty_percent_mark:], objective)

        plot_curve_fit(x, y, objective, coefficient, coefficient2, shape, title + " " +column, x[twenty_percent_mark])
    plt.show()


if __name__ == '__main__':
    main()
