[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)

# IEEE 754 floating point functions

Synthesiseable IEEE 754 floating point library in Verilog.

- Fully pipelined, high performance
- Arithmetic: Divider, Multiplier, Adder, Subtracter and Square Root
- Conversions: float_to_int and int_to_float
- Rounding Functions: floor, ceil, truncate and nearest
- Supports Denormal Numbers
- Round-to-nearest (ties to even)
- Double and single precision versions of each function

# IP Cores

The library uses a python script to automatically generate and pipeline logic 
functions.  Pre-generated IP cores written in Verilog can be found in the components 
folder. Each component is fully pipelined and the output value is expected after a 
fixed number of clock cycles. The latency of each block can be found in a comment in 
the Verilog code.

# Run Test Suite

Requires Python 3 and Icarus Verilog. On Ubuntu based systems these can be installed as follows: 

``` bash
sudo apt-get install python iverilog
```

To run the full test suite, run the following:

``` bash
cd components
python test_cores.py # for the single precision test suite
...
python test_double_cores.py # for the double precision test suite
...
```
