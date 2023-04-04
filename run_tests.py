import re
import unittest

import pytest
from hypothesis import given
from hypothesis.strategies import integers, floats, sampled_from, one_of, just, lists, from_regex

from algorithm_timer import *


class TestGenerateArray(unittest.TestCase):

    @given(sampled_from(["Reverse", "Random", "Pre-sorted"]), floats(min_value=0, max_value=5))
    def test_correct_length(self, order, size):
        size = int(10 ** size)
        arr = generate_array(order, size)
        assert len(arr) == size

    @given(floats(min_value=0, max_value=5))
    def test_invalid_order(self, size):
        with pytest.raises(ValueError):
            generate_array("Invalid", size)

    @given(one_of(just("Reverse"), just("Pre-sorted"), just("Random")), floats(min_value=0, max_value=5))
    def test_order_and_size(self, order, size):
        size = int(10 ** size)
        arr = generate_array(order, size)
        if order == "Reverse":
            self.assertTrue(all(arr[i] >= arr[i + 1] for i in range(size - 1)))
        elif order == "Pre-sorted":
            self.assertTrue(all(arr[i] <= arr[i + 1] for i in range(size - 1)))

    @given(one_of(just("Reverse"), just("Pre-sorted"), just("Random")),
           floats(min_value=0, max_value=5))
    def test_range(self, order, size):
        size = int(10 ** size)
        arr = generate_array(order, size)
        if size > 0:
            self.assertGreaterEqual(min(arr), 0)
            self.assertLessEqual(max(arr), 2147483647)
            self.assertTrue(all(isinstance(x, int) for x in arr))


class TestSetup(unittest.TestCase):
    def testSetUp(self):
        sorted_function, dictionary_of_sorting_algorithms = setup()
        self.assertTrue(callable(sorted_function))
        self.assertTrue(
            list(dictionary_of_sorting_algorithms.keys()) == ['QuickSort', 'MergeSort', 'HeapSort', 'BubbleSort',
                                                              'NoSort'])
        self.assertTrue(all(isinstance(i, str) for i in dictionary_of_sorting_algorithms.keys()))
        self.assertTrue(all(callable(i) for i in dictionary_of_sorting_algorithms.values()))

    @given(lists(integers(min_value=0, max_value=2147483647)))
    def test_is_sorted_returns_true_for_sorted_list(self, lst):
        sorted_function, dictionary_of_sorting_algorithms = setup()
        lst.sort()
        int_array = ctypes.c_int * len(lst)
        arr = int_array(*lst)
        self.assertTrue(bool(sorted_function(arr, len(lst))))

    # @given(lists(integers()))
    def test_is_sorted_returns_true_for_empty_list(self):
        sorted_function, dictionary_of_sorting_algorithms = setup()
        int_array = ctypes.c_int * 0
        arr = int_array(*[])
        self.assertTrue(bool(sorted_function(arr, 0)))

    @given(lists(integers(min_value=0, max_value=2147483647), min_size=2))
    def test_is_sorted_returns_false_for_unsorted_list(self, lst):
        sorted_function, dictionary_of_sorting_algorithms = setup()
        if len(set(lst)) > 1:
            lst.sort()
            lst[0], lst[-1] = lst[-1], lst[0]
            int_array = ctypes.c_int * len(lst)
            arr = int_array(*lst)
            self.assertFalse(bool(sorted_function(arr, len(lst))))


class TestTimeAlgo(unittest.TestCase):
    @given(one_of(just("Reverse"), just("Pre-sorted"), just("Random")), integers(min_value=0, max_value=1000),
           sampled_from(['QuickSort', 'MergeSort', 'HeapSort', 'BubbleSort', 'NoSort']))
    def testTimeAlgo(self, order_name, input_size, algo_name):
        time = time_sorting_algorithm(order_name, input_size, algo_name)
        self.assertTrue(isinstance(time, int))
        self.assertGreaterEqual(time, 0)


class TestSortWith(unittest.TestCase):
    @given(
        sampled_from([average_runtime_calculator]),
        sampled_from(['QuickSort', 'MergeSort', 'HeapSort', 'BubbleSort', 'NoSort']),
        sampled_from(['Reverse', 'Random', 'Pre-sorted']),
        integers(min_value=1, max_value=10),
        lists(integers(min_value=1, max_value=500), unique=True)
    )
    def test_sort_with_order_repeat_after(self, sort_manager, algo_name, order, repeats, input_sizes):
        # Compute the actual result using the function under test
        actual_result = sort_manager(algo_name, order, repeats, input_sizes)

        # Assert that the actual result is a list of floats
        self.assertTrue(isinstance(actual_result, list))
        self.assertTrue(all(isinstance(x, float) or isinstance(x, int) for x in actual_result))

        # Assert that the actual result has the same length as the input sizes
        self.assertEqual(len(actual_result), len(input_sizes))


class TestSaveCSV(unittest.TestCase):
    windows_regex = re.compile(r'^(?!^(CON|PRN|AUX|NUL|COM\d|LPT\d|\..*|.*\s\.|\.$))[^\x00-\x1f\\<>:"/|?*]+$')
    header_regex = re.compile(r'^[a-zA-Z0-9]+$')

    @given(file_path=from_regex(windows_regex), header=lists(from_regex(header_regex)),
           data=lists(lists(floats())))
    def test_file_creation(self, file_path, header, data):
        path = ""
        try:
            path = save_to_csv(file_path, header, *data)
            if path != "Invalid_file_name":
                self.assertTrue(os.path.exists(path))
        finally:
            try:
                os.remove(path)
            except FileNotFoundError:
                pass

    @given(file_path=from_regex(windows_regex), header=lists(from_regex(header_regex)),
           data=lists(lists(floats())))
    def test_header_written_first_row(self, file_path, header, data):
        path = ""
        try:
            path = save_to_csv(file_path, header, *data)
            if path != "Invalid_file_name":
                with open(path, "r") as csv_file:
                    csv_reader = csv.reader(csv_file)
                    self.assertEqual(next(csv_reader), header)
        finally:
            try:
                os.remove(path)
            except FileNotFoundError:
                pass


if __name__ == '__main__':
    unittest.main()
