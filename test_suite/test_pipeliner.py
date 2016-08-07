import sys
sys.path.append("..")

import ip_generator.pipeliner
import ip_generator.float
Input = ip_generator.pipeliner.Input
Output = ip_generator.pipeliner.Output
trace = ip_generator.test_probe.trace
Component = ip_generator.pipeliner.Component
single_to_float = ip_generator.float.single_to_float
float_to_single = ip_generator.float.float_to_single

import subprocess
import random
from numpy import float32
from itertools import permutations
from random import randint

def test_function(a, b):

    stimulus = {
        'a':a, 
        'b':b
    }

    response = ip_generator.pipeliner.component.test(stimulus)
    actual = response["z"]
    expected = [i//j for i, j in zip(a, b)]

    n = 0
    for a, b, i, j in zip(a, b, actual, expected):
        if actual != expected:
            print "%08x %08x %08x %08x fail"%(a, b, i, j)
            print n
            trace(response, n)
            #append failures to regression test file
            of = open("regression_tests", "a")
            of.write("%i %i\n"%(a, b))
            of.close()
            sys.exit(1)
        n += 1



ip_generator.pipeliner.component = Component()
Output('z', Input(32, 'a') // Input(32, 'b'))

count = 0

#regression tests
inf = open("regression_tests")
stimulus_a = [10, 20, 30, 40, 50]
stimulus_b = [5, 5, 5, 5, 5]
test_function(stimulus_a, stimulus_b)
count += len(stimulus_a)
print count, "vectors passed"

