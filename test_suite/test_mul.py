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

def get_expected():
    subprocess.call("./reference_tests/mul")
    inf = open("z_expected")
    return [int(i) for i in inf]

def test_function(a, b):

    stimulus = {
        'a':a, 
        'b':b
    }

    response = ip_generator.pipeliner.component.test(stimulus)
    actual = response["z"]
    expected = get_expected()

    n = 0
    for a, b, i, j in zip(a, b, actual, expected):
        if(j != i):
            j_mantissa = j & 0x7fffff
            j_exponent = ((j & 0x7f800000) >> 23) - 127
            j_sign = ((j & 0x80000000) >> 31)
            i_mantissa = i & 0x7fffff
            i_exponent = ((i & 0x7f800000) >> 23) - 127
            i_sign = ((i & 0x80000000) >> 31)
            if j_exponent == 128 and j_mantissa != 0:
                if(i_exponent == 128):
                    result = True
            else:
                result = False
        else:
             result = True
        if not result:
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
Output('z', float_to_single(single_to_float(Input(32, 'a')) * single_to_float(Input(32, 'b'))))

count = 0

#regression tests
inf = open("regression_tests")
stimulus_a = []
stimulus_b = []
for line in inf.read().splitlines():
    a, b = line.strip().split()
    stimulus_a.append(int(a))
    stimulus_b.append(int(b))
test_function(stimulus_a, stimulus_b)
count += len(stimulus_a)
print count, "vectors passed"

#regression tests
stimulus_a = [0x22cb525a, 0x40000000, 0x83e73d5c, 0xbf9b1e94, 0x34082401, 0x5e8ef81, 0x5c75da81, 0x2b017]
stimulus_b = [0xadd79efa, 0xC0000000, 0x1c800000, 0xc038ed3a, 0xb328cd45, 0x114f3db, 0x2f642a39, 0xff3807ab]
test_function(stimulus_a, stimulus_b)
count += len(stimulus_a)
print count, "vectors passed"

#corner cases
from itertools import permutations
stimulus_a = [i[0] for i in permutations([0x80000000, 0x00000000, 0x7f800000, 0xff800000, 0x7fc00000, 0xffc00000], 2)]
stimulus_b = [i[1] for i in permutations([0x80000000, 0x00000000, 0x7f800000, 0xff800000, 0x7fc00000, 0xffc00000], 2)]
test_function(stimulus_a, stimulus_b)
count += len(stimulus_a)
print count, "vectors passed"

#edge cases
stimulus_a = [0x80000000 for i in xrange(1000)]
stimulus_b = [randint(0, 1<<32) for i in xrange(1000)]
test_function(stimulus_a, stimulus_b)
count += len(stimulus_a)
print count, "vectors passed"

stimulus_a = [0x00000000 for i in xrange(1000)]
stimulus_b = [randint(0, 1<<32) for i in xrange(1000)]
test_function(stimulus_a, stimulus_b)
count += len(stimulus_a)
print count, "vectors passed"

stimulus_b = [0x80000000 for i in xrange(1000)]
stimulus_a = [randint(0, 1<<32) for i in xrange(1000)]
test_function(stimulus_a, stimulus_b)
count += len(stimulus_a)
print count, "vectors passed"

stimulus_b = [0x00000000 for i in xrange(1000)]
stimulus_a = [randint(0, 1<<32) for i in xrange(1000)]
test_function(stimulus_a, stimulus_b)
count += len(stimulus_a)
print count, "vectors passed"

stimulus_a = [0x7F800000 for i in xrange(1000)]
stimulus_b = [randint(0, 1<<32) for i in xrange(1000)]
test_function(stimulus_a, stimulus_b)
count += len(stimulus_a)
print count, "vectors passed"

stimulus_a = [0xFF800000 for i in xrange(1000)]
stimulus_b = [randint(0, 1<<32) for i in xrange(1000)]
test_function(stimulus_a, stimulus_b)
count += len(stimulus_a)
print count, "vectors passed"

stimulus_b = [0x7F800000 for i in xrange(1000)]
stimulus_a = [randint(0, 1<<32) for i in xrange(1000)]
test_function(stimulus_a, stimulus_b)
count += len(stimulus_a)
print count, "vectors passed"

stimulus_b = [0xFF800000 for i in xrange(1000)]
stimulus_a = [randint(0, 1<<32) for i in xrange(1000)]
test_function(stimulus_a, stimulus_b)
count += len(stimulus_a)
print count, "vectors passed"

stimulus_a = [0x7FC00000 for i in xrange(1000)]
stimulus_b = [randint(0, 1<<32) for i in xrange(1000)]
test_function(stimulus_a, stimulus_b)
count += len(stimulus_a)
print count, "vectors passed"

stimulus_a = [0xFFC00000 for i in xrange(1000)]
stimulus_b = [randint(0, 1<<32) for i in xrange(1000)]
test_function(stimulus_a, stimulus_b)
count += len(stimulus_a)
print count, "vectors passed"

stimulus_b = [0x7FC00000 for i in xrange(1000)]
stimulus_a = [randint(0, 1<<32) for i in xrange(1000)]
test_function(stimulus_a, stimulus_b)
count += len(stimulus_a)
print count, "vectors passed"

stimulus_b = [0xFFC00000 for i in xrange(1000)]
stimulus_a = [randint(0, 1<<32) for i in xrange(1000)]
test_function(stimulus_a, stimulus_b)
count += len(stimulus_a)
print count, "vectors passed"

#seed(0)
for i in xrange(100000):
    stimulus_a = [randint(0, 1<<32) for i in xrange(1000)]
    stimulus_b = [randint(0, 1<<32) for i in xrange(1000)]
    test_function(stimulus_a, stimulus_b)
    count += 1000
    print count, "vectors passed"
