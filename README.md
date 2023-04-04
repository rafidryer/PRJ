# Raphael Dryer k2035989 

## King's college London 6CCS3PRJ Final Year Project: The Constants Hidden in Big O Notation

This repository contains the code used for the final project along with the CSV files of the data used in the final analysis.

There are 3 python scripts which require Python version 3.9+. 
Run the following commands into the commandline to ensure the correct libraries are installed:

```
pip install numpy
pip install matplotlib
pip install hypothesis
pip install pandas
pip install scipy
pip install pytest
```

Additionally, ensure the `clib.so` file is present. If it is not there, or the `clib.c` file 
has been edited, run the command `cc -fPIC -shared -o clib.so clib.c` to generate a new shared `.so` file.

To run `algorithm_timer.py` to run the algorithms and measure their run-times, run the command:
`python algorithm_timer.py`
and enter the information while prompted. 
Note that `Max input size: 10^` can be a non-integer number. The number entered is rounded to an integer, so 10^3.5 --> 3162
The run-times will be plotted on graphs and stored in CSV files in the `results/` folder, named based on the parameters given by the user.

To run the `hidden_constant_finder.py` script to plot a graph with the line of best fit and the upperbound of the data, enter the command:
`python hidden_constantt_finder.py` and enter the name of the CSV file when prompted. Do not include the `.csv` file extension. 
Ensure the file is in the `results/` folder.

To run the unit tests, run the command `python run_tests.py`.
