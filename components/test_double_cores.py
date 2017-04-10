import sys
sys.path.append("..")

import subprocess
import random
import cores
import struct
from numpy import float32
from itertools import permutations
from random import randint
from multiprocessing import Process

def trace(response, n):
    for name, values in response.iteritems():
        print name, values[n]

def asdouble(x):
    string = ""
    for i in range(8):
        byte = x >> 56
        byte &= 0xff
        string += chr(byte)
        x <<= 8
    return struct.unpack(">d", string)[0]

def failure(a, b, actual, expected):
    print "a        b        actual   expected"
    print "======== ======== ======== ========"
    print "%16x %16x %16x %16x fail"%(a, b, actual, expected)
    print "a", asdouble(a)
    print "b", asdouble(b)
    print "actual", asdouble(actual)
    print "expected", asdouble(expected)

def get_expected(core_name):
    subprocess.call("./reference_tests/"+core_name)
    inf = open("stim/%s_z_expected"%core_name)
    return [int(i) for i in inf]

def test_convert(core_name, core, a):
    print "testing", core_name, "..."
    stimulus = {core_name+'_a':a}

    response = core.test(stimulus, name=core_name)
    actual = response[core_name+"_z"]
    expected = get_expected(core_name)

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

def test_unary(core_name, core, a, b):
    print "testing", core_name, "..."
    stimulus = {
        core_name+'_a':a, 
    }

    response = core.test(stimulus, name=core_name)
    actual = response[core_name+"_z"]
    expected = get_expected(core_name)

    n = 0
    for a, b, i, j in zip(a, b, actual, expected):
        if(j != i):
            j_mantissa = j & 0xfffffffffffff
            j_exponent = ((j & 0x7ff0000000000000) >> 52) - 1023
            j_sign = ((j & 0x8000000000000000) >> 63)
            i_mantissa = i & 0xfffffffffffff
            i_exponent = ((i & 0x7ff0000000000000) >> 52) - 1023
            i_sign = ((i & 0x8000000000000000) >> 63)

            if j_exponent == 1024 and j_mantissa != 0:
                if(i_exponent == 1024):
                    result = True
                else:
                    result = False
            else:
                result = False
        else:
             result = True
        if not result:
            failure(a, b, i, j)
            print "failed in vector", n
            trace(response, n)
            #append failures to regression test file
            of = open("regression_tests", "a")
            of.write("%i %i\n"%(a, b))
            of.close()
            sys.exit(1)
        n += 1

def test_comparator(core_name, core, a, b):
    print "testing", core_name, "..."
    stimulus = {
        core_name+'_a':a, 
        core_name+'_b':b
    }

    response = core.test(stimulus, name=core_name)
    actual = response[core_name+"_z"]
    expected = get_expected(core_name)

    n = 0
    for a, b, i, j in zip(a, b, actual, expected):
        if(j != i):
            result = False
        else:
            result = True
        if not result:
            failure(a, b, i, j)
            print n
            trace(response, n)
            #append failures to regression test file
            of = open("regression_tests", "a")
            of.write("%i %i\n"%(a, b))
            of.close()
            sys.exit(1)
        n += 1

def test_binary(core_name, core, a, b):
    print "testing", core_name, "..."
    stimulus = {
        core_name+'_a':a, 
        core_name+'_b':b
    }

    response = core.test(stimulus, name=core_name)
    actual = response[core_name+"_z"]
    expected = get_expected(core_name)

    n = 0
    for a, b, i, j in zip(a, b, actual, expected):
        if(j != i):
            j_mantissa = j & 0xfffffffffffff
            j_exponent = ((j & 0x7ff0000000000000) >> 52) - 1023
            j_sign = ((j & 0x8000000000000000) >> 63)
            i_mantissa = i & 0xfffffffffffff
            i_exponent = ((i & 0x7ff0000000000000) >> 52) - 1023
            i_sign = ((i & 0x8000000000000000) >> 63)

            if j_exponent == 1024 and j_mantissa != 0:
                if(i_exponent == 1024):
                    result = True
                else:
                    result = False
            else:
                result = False
        else:
             result = True
        if not result:
            failure(a, b, i, j)
            print "failed in vector", n
            trace(response, n)
            #append failures to regression test file
            of = open("double_regression_tests", "a")
            of.write("%i %i\n"%(a, b))
            of.close()
            sys.exit(1)
        n += 1

def test_cores(stimulus_a, stimulus_b):
    binary_cores = {
        "double_mul":cores.double_mul, 
        "double_add":cores.double_add, 
        "double_div":cores.double_div, 
    }
    processes = []
    for core_name, core in binary_cores.iteritems():
        processes.append(
            Process(
                target=test_binary, 
                args=[core_name, core, stimulus_a, stimulus_b]
            )
        )

    converter_cores = {
        "double_to_int":cores.to_int, 
        #"to_float":cores.to_float, 
    }
    for core_name, core in converter_cores.iteritems():
        processes.append(
            Process(
                target = test_convert,
                args=[core_name, core, stimulus_a]
            )
        )

    unary_cores = {
        "double_sqrt":cores.double_sqrt, 
    }
    for core_name, core in unary_cores.iteritems():
        processes.append(
            Process(
                target = test_unary,
                args=[core_name, core, stimulus_a, stimulus_b]
            )
        )
    comparator_cores = {
        "double_gt":cores.double_gt, 
        "double_lt":cores.double_lt, 
        "double_le":cores.double_le, 
        "double_ge":cores.double_ge, 
        "double_eq":cores.double_eq, 
        "double_ne":cores.double_ne, 
    }
    for core_name, core in comparator_cores.iteritems():
        processes.append(
            Process(
                target = test_comparator,
                args=[core_name, core, stimulus_a, stimulus_b]
            )
        )

    for i in processes:
        i.daemon=True
        i.start()

    for i in processes:
        i.join()
        if i.exitcode:
            exit(i.exitcode)

###############################################################################
#tests start here
###############################################################################

count = 0

#regression tests
inf = open("double_regression_tests")
stimulus_a = []
stimulus_b = []
for line in inf.read().splitlines():
    a, b = line.strip().split()
    stimulus_a.append(int(a))
    stimulus_b.append(int(b))
test_cores(stimulus_a, stimulus_b)
count += len(stimulus_a)
print count, "vectors passed"


#corner cases
from itertools import permutations
stimulus_a = [i[0] for i in permutations(
    [0x8000000000000000, 0x0000000000000000, 0x7ff0000000000000, 
     0xfff0000000000000, 0x7ff8000000000000, 0xfff8000000000000], 2)]
stimulus_b = [i[1] for i in permutations(
    [0x8000000000000000, 0x0000000000000000, 0x7ff0000000000000, 
     0xfff0000000000000, 0x7ff8000000000000, 0xfff8000000000000], 2)]
test_cores(stimulus_a, stimulus_b)
count += len(stimulus_a)
print count, "vectors passed"

#edge cases
stimulus_a = [0x8000000000000000 for i in xrange(1000)]
stimulus_b = [randint(0, 1<<64) for i in xrange(1000)]
test_cores(stimulus_a, stimulus_b)
count += len(stimulus_a)
print count, "vectors passed"

stimulus_a = [0x0000000000000000 for i in xrange(1000)]
stimulus_b = [randint(0, 1<<64) for i in xrange(1000)]
test_cores(stimulus_a, stimulus_b)
count += len(stimulus_a)
print count, "vectors passed"

stimulus_b = [0x8000000000000000 for i in xrange(1000)]
stimulus_a = [randint(0, 1<<64) for i in xrange(1000)]
test_cores(stimulus_a, stimulus_b)
count += len(stimulus_a)
print count, "vectors passed"

stimulus_b = [0x0000000000000000 for i in xrange(1000)]
stimulus_a = [randint(0, 1<<64) for i in xrange(1000)]
test_cores(stimulus_a, stimulus_b)
count += len(stimulus_a)
print count, "vectors passed"

stimulus_a = [0x7FF0000000000000 for i in xrange(1000)]
stimulus_b = [randint(0, 1<<64) for i in xrange(1000)]
test_cores(stimulus_a, stimulus_b)
count += len(stimulus_a)
print count, "vectors passed"

stimulus_a = [0xFFF0000000000000 for i in xrange(1000)]
stimulus_b = [randint(0, 1<<64) for i in xrange(1000)]
test_cores(stimulus_a, stimulus_b)
count += len(stimulus_a)
print count, "vectors passed"

stimulus_b = [0x7FF0000000000000 for i in xrange(1000)]
stimulus_a = [randint(0, 1<<64) for i in xrange(1000)]
test_cores(stimulus_a, stimulus_b)
count += len(stimulus_a)
print count, "vectors passed"

stimulus_b = [0xFFF0000000000000 for i in xrange(1000)]
stimulus_a = [randint(0, 1<<64) for i in xrange(1000)]
test_cores(stimulus_a, stimulus_b)
count += len(stimulus_a)
print count, "vectors passed"

stimulus_a = [0x7FF8000000000000 for i in xrange(1000)]
stimulus_b = [randint(0, 1<<64) for i in xrange(1000)]
test_cores(stimulus_a, stimulus_b)
count += len(stimulus_a)
print count, "vectors passed"

stimulus_a = [0xFFF8000000000000 for i in xrange(1000)]
stimulus_b = [randint(0, 1<<64) for i in xrange(1000)]
test_cores(stimulus_a, stimulus_b)
count += len(stimulus_a)
print count, "vectors passed"

stimulus_b = [0x7FF8000000000000 for i in xrange(1000)]
stimulus_a = [randint(0, 1<<64) for i in xrange(1000)]
test_cores(stimulus_a, stimulus_b)
count += len(stimulus_a)
print count, "vectors passed"

stimulus_b = [0xFFF8000000000000 for i in xrange(1000)]
stimulus_a = [randint(0, 1<<64) for i in xrange(1000)]
test_cores(stimulus_a, stimulus_b)
count += len(stimulus_a)
print count, "vectors passed"

#seed(0)
for i in xrange(1000000):
    stimulus_a = [randint(0, 1<<64) for i in xrange(5000)]
    stimulus_b = [randint(0, 1<<64) for i in xrange(5000)]
    test_cores(stimulus_a, stimulus_b)
    count += 5000
    print count, "vectors passed"
