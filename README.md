IEEE 754 floating point functions
==================================

Synthesiseable IEEE 754 floating point library in Verilog.

	+ Fully pipelined, high performance
	+ Arithmetic: Divider, Multiplier, Adder, Subtracter and Square Root
	+ Conversions: float_to_int and int_to_float
        + Rounding Functions: floor, ceil, truncate and nearest
	+ Supports Denormal Numbers
	+ Round-to-nearest (ties to even)
        + Double and single precision versions of each function

IP Cores

The library uses a python script to automatically generate and pipeline logic 
functions.  Pre-generated IP cores written in Verilog can be found in the components 
folder. Each component is fully pipelined and the output value is expected after a 
fixed number of clock cycles. The latency of each block can be found in a comment in 
the Verilog code.

Run Test Suite

Requires python2 and Icarus Verilog

..bash:
	cd components
	python2 test_cores.py
	...
	python2 test_double_cores.py
