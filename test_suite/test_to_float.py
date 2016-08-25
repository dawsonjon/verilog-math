import sys
sys.path.append("..")

import ip_generator.pipeliner
import ip_generator.float
trace = ip_generator.test_probe.trace
Input = ip_generator.pipeliner.Input
Output = ip_generator.pipeliner.Output
Component = ip_generator.pipeliner.Component
single_to_float = ip_generator.float.single_to_float
float_to_single = ip_generator.float.float_to_single
int_to_float = ip_generator.float.int_to_float

import subprocess
import random
from numpy import float32
from itertools import permutations
from random import randint

def get_expected():
    subprocess.call("./reference_tests/to_float")
    inf = open("stim/to_float_z_expected")
    return [int(i) for i in inf]

def test_function(a):

    stimulus = {
        'to_float_a':a, 
    }

    response = ip_generator.pipeliner.component.test(stimulus, name="to_float")
    actual = response["to_float_z"]
    expected = get_expected()

    n = 0
    for a, i, j in zip(a, actual, expected):
        if(j != i):
            result = False
        else:
            result = True
        if not result:
            trace(response, n)
            print "%08x %08x %08x fail"%(a, i, j)
            sys.exit(1)
        n += 1



ip_generator.pipeliner.component = Component()
Output('to_float_z', float_to_single(int_to_float(Input(32, 'to_float_a'))))

count = 0

#regression tests
stimulus_a = [0x22cb525a, 0x40000000, 0x83e73d5c, 0xbf9b1e94, 0x34082401, 0x5e8ef81, 0x5c75da81, 0x2b017]
test_function(stimulus_a)
count += len(stimulus_a)
print count, "vectors passed"

#corner cases
from itertools import permutations
stimulus_a = [0x80000000, 0x00000000, 0x7f800000, 0xff800000, 0x7fc00000, 0xffc00000]
test_function(stimulus_a)
count += len(stimulus_a)
print count, "vectors passed"

for i in xrange(100000):
    stimulus_a = [randint(0, 1<<32) for i in xrange(1000)]
    test_function(stimulus_a)
    count += 1000
    print count, "vectors passed"
