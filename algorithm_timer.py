import csv
import ctypes
import datetime
import os
import time
from collections import defaultdict

import matplotlib.pyplot as plt
import numpy as np


def generate_array(order, input_size):
    if order == "Reverse":  # reverse order
        numpy_list_to_be_sorted = np.arange(input_size, 0, -1)
    elif order == "Random":  # random order
        # numpy_list_to_be_sorted = np.random.randint(2147483647, size=input_size)
        numpy_list_to_be_sorted = np.random.randint(2147483647, size=input_size)
    elif order == "Pre-sorted":  # in order
        numpy_list_to_be_sorted = np.arange(0, input_size, 1)
    else:
        raise ValueError("Invalid order parameter")
    int_array = ctypes.c_int * input_size
    return int_array(*numpy_list_to_be_sorted)


def time_sorting_algorithm(order_name, input_size, algo_name, *args):
    is_sorted, functions = setup()  # gets access to the C library

    algo = functions[algo_name]  # finds the C function
    parameter_array = generate_array(order_name, input_size)  # generates the input array

    # times how long it takes to run the algorithm
    start = time.perf_counter_ns()
    algo(parameter_array, input_size)
    end = time.perf_counter_ns()

    # checks the array was sorted successfully
    if not is_sorted(parameter_array, input_size) and algo_name != "NoSort":
        raise Exception(f"list not sorted, {order_name}, {input_size}, {algo_name}")

    return end - start


def average_runtime_calculator(algo_name, order, repeats, input_sizes):
    total_times_dict = defaultdict(int)
    for repeat in range(repeats):
        print(repeat, algo_name, order) # helps see how the program is progressing

        for input_size in input_sizes:
            # adds the runtime to the correct counter
            total_times_dict[input_size] += time_sorting_algorithm(order, input_size, algo_name)

    list_of_times = []
    for total_time_taken in total_times_dict.values():
        list_of_times.append(total_time_taken / repeats)  # calculates the average runtime
    return list_of_times


def plot_graph(title, x_label, y_label, y_values, input_sizes, labels=None, markers=None):
    fig = plt.figure()
    fig.suptitle(title)

    if labels is None:
        labels = [f"y{i + 1}" for i in range(len(y_values))]

    if markers is None:
        markers = [','] * len(y_values)

    for y, label, marker in zip(y_values, labels, markers):
        plt.plot(input_sizes, y, label=label, marker=marker)

    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.grid(True)
    plt.legend()
    plt.draw()
    return fig


def save_to_csv(file_path, header, *args):
    try:
        file_path = "results\\" + file_path + "__" + datetime.datetime.now().strftime("%d.%m.%y.%H-%M-%S") + ".csv"
        data = list(zip(*args))

        with open(file_path, "w", newline="") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(header)  # write header as first row
            csv_writer.writerows(data)
        return file_path
    except OSError:
        return "Invalid_file_name"


# runs every algorithm with the a fixed input order
def run_with_fixed_order(order_name):
    algo_names = functions_names_to_c_functions_map.keys()
    y_values = [sort_function(algo, order_name, repeats, input_sizes) for algo in algo_names]

    plot_graph(
        title=order_name + " Order",
        x_label="Size of List",
        y_label="Time (NanoSeconds)",
        y_values=y_values,
        input_sizes=input_sizes,
        labels=algo_names
    )

    save_to_csv(f"{order_name}" + file_title, ("Input Size", *algo_names), input_sizes, *y_values)


# runs every input order with the a fixed algorithm
def run_with_fixed_algorithm(algo):
    y_values = [sort_function(algo, order, repeats, input_sizes) for order in orders]

    plot_graph(
        title=algo,
        x_label="Size of List",
        y_label="Time (NanoSeconds)",
        y_values=y_values,
        input_sizes=input_sizes,
        labels=orders,
    )

    save_to_csv(f"{algo}" + file_title, ("Input Size", *orders), input_sizes, *y_values)


def setup():
    c = ctypes.CDLL(
        os.getcwd() + "\\clib.so")
    is_sorted = c.is_sorted
    functions_names_to_c_functions_map = {
        "QuickSort": c.quickSortC,
        "MergeSort": c.mergeSortC,
        "HeapSort": c.heapSort,
        "BubbleSort": c.bubbleSort,
        "NoSort": c.emptyFunction
    }
    return is_sorted, functions_names_to_c_functions_map


def sanitize_input(prompt, input_type):
    while True:
        user_input = input(prompt)
        try:
            # ensures the input can be casted to the correct type
            sanitized_input = input_type(user_input) 
            user_input[0]
            return sanitized_input
        except (ValueError, IndexError):
            print(f"Invalid input. Please enter a valid {input_type.__name__}.")


def user_input():
    # Asks the user which algorithms they wish to run
    function_names_to_run = []
    for func in functions_names_to_c_functions_map:
        answer = sanitize_input(f"Would you like to run {func} (y/n): ", str)
        if answer.lower() == "y":
            function_names_to_run.append(func)

    # Asks the user what fixed orders the want to run
    orders_to_run = []
    for order in orders:
        answer = sanitize_input(f"Would you like to run {order} (y/n): ", str)
        if answer.lower() == "y":
            orders_to_run.append(order)

    # Asks for additional information
    Exponent = sanitize_input("Max input size: 10^", float)
    Repeats = sanitize_input("Number of repeats: ", int)
    Interval = sanitize_input("Interval: ", int)

    return function_names_to_run, orders_to_run, Exponent, Repeats, Interval


if __name__ == '__main__':

    _, functions_names_to_c_functions_map = setup()
    orders = ["Reverse", "Random", "Pre-sorted"]
    function_names_to_run, orders_to_run, Exponent, repeats, interval = user_input()

    start_total = time.perf_counter()

    # Generates the list of input sizes
    input_sizes = [input_size for input_size in range(0, int(10 ** Exponent) + 1, interval)]

    sort_function = average_runtime_calculator

    file_title = f"_upto_{input_sizes[-1]}_interval_{interval}_repeats_{repeats}"

    #############################################
    for function in function_names_to_run:
        run_with_fixed_algorithm(function)

    for order in orders_to_run:
        run_with_fixed_order(order)
    ####################################################

    end_total = time.perf_counter()
    print("Total time: ", end_total - start_total)
    plt.show()
