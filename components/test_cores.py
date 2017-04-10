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
from math import isnan, isinf

def trace(response, n):
    for name, values in response.iteritems():
        print name, values[n]

def asfloat(x):
    string = ""
    for i in range(4):
        byte = x >> 24
        byte &= 0xff
        string += chr(byte)
        x <<= 8
    return struct.unpack(">f", string)[0]

def failure(a, b, actual, expected):
    print "a        b        actual   expected"
    print "======== ======== ======== ========"
    print "%08x %08x %08x %08x fail"%(a, b, actual, expected)
    print "a", asfloat(a)
    print "b", asfloat(b)
    print "actual", asfloat(actual)
    print "expected", asfloat(expected)

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
        if asfloat(a) < 0 and "unsigned" in core_name:
            result = True
        elif asfloat(a) > (2**32)-1 and "unsigned" in core_name:
            result = True
        elif asfloat(a) > (2**31)-1:
            result = True
        elif asfloat(a) < -(2**31):
            result = True
        elif isnan(asfloat(a)):
            result = True
        else:
            if(j != i):
                result = False
            else:
                result = True
        if not result:
            trace(response, n)
            print "input actual expected"
            print "%08x %08x %08x fail"%(a, i, j)
            print asfloat(a), asfloat(i), asfloat(j)
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

def test_cores(stimulus_a, stimulus_b):
    binary_cores = {
        "mul":cores.mul, 
        "div":cores.div, 
        "add":cores.add
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
        "single_to_int":cores.single_to_int, 
        "single_to_unsigned_int":cores.single_to_unsigned_int, 
        "int_to_single":cores.int_to_single, 
        "unsigned_int_to_single":cores.unsigned_int_to_single, 
    }
    for core_name, core in converter_cores.iteritems():
        processes.append(
            Process(
                target = test_convert,
                args=[core_name, core, stimulus_a]
            )
        )

    unary_cores = {
        "sqrt":cores.sqrt, 
    }
    for core_name, core in unary_cores.iteritems():
        processes.append(
            Process(
                target = test_unary,
                args=[core_name, core, stimulus_a, stimulus_b]
            )
        )
    comparator_cores = {
        "gt":cores.gt, 
        "lt":cores.lt, 
        "le":cores.le, 
        "ge":cores.ge, 
        "eq":cores.eq, 
        "ne":cores.ne, 
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
inf = open("regression_tests")
stimulus_a = []
stimulus_b = []
for line in inf.read().splitlines():
    a, b = line.strip().split()
    stimulus_a.append(int(a))
    stimulus_b.append(int(b))
test_cores(stimulus_a, stimulus_b)
count += len(stimulus_a)
print count, "vectors passed"

#regression tests
stimulus_a = [0x22cb525a, 0x40000000, 0x83e73d5c, 0xbf9b1e94, 0x34082401, 0x5e8ef81, 0x5c75da81, 0x2b017]
stimulus_b = [0xadd79efa, 0xC0000000, 0x1c800000, 0xc038ed3a, 0xb328cd45, 0x114f3db, 0x2f642a39, 0xff3807ab]
test_cores(stimulus_a, stimulus_b)
count += len(stimulus_a)
print count, "vectors passed"

#corner cases
from itertools import permutations
stimulus_a = [i[0] for i in permutations([0x80000000, 0x00000000, 0x7f800000, 0xff800000, 0x7fc00000, 0xffc00000], 2)]
stimulus_b = [i[1] for i in permutations([0x80000000, 0x00000000, 0x7f800000, 0xff800000, 0x7fc00000, 0xffc00000], 2)]
test_cores(stimulus_a, stimulus_b)
count += len(stimulus_a)
print count, "vectors passed"

#edge cases
stimulus_a = [0x80000000 for i in xrange(1000)]
stimulus_b = [randint(0, 1<<32) for i in xrange(1000)]
test_cores(stimulus_a, stimulus_b)
count += len(stimulus_a)
print count, "vectors passed"

stimulus_a = [0x00000000 for i in xrange(1000)]
stimulus_b = [randint(0, 1<<32) for i in xrange(1000)]
test_cores(stimulus_a, stimulus_b)
count += len(stimulus_a)
print count, "vectors passed"

stimulus_b = [0x80000000 for i in xrange(1000)]
stimulus_a = [randint(0, 1<<32) for i in xrange(1000)]
test_cores(stimulus_a, stimulus_b)
count += len(stimulus_a)
print count, "vectors passed"

stimulus_b = [0x00000000 for i in xrange(1000)]
stimulus_a = [randint(0, 1<<32) for i in xrange(1000)]
test_cores(stimulus_a, stimulus_b)
count += len(stimulus_a)
print count, "vectors passed"

stimulus_a = [0x7F800000 for i in xrange(1000)]
stimulus_b = [randint(0, 1<<32) for i in xrange(1000)]
test_cores(stimulus_a, stimulus_b)
count += len(stimulus_a)
print count, "vectors passed"

stimulus_a = [0xFF800000 for i in xrange(1000)]
stimulus_b = [randint(0, 1<<32) for i in xrange(1000)]
test_cores(stimulus_a, stimulus_b)
count += len(stimulus_a)
print count, "vectors passed"

stimulus_b = [0x7F800000 for i in xrange(1000)]
stimulus_a = [randint(0, 1<<32) for i in xrange(1000)]
test_cores(stimulus_a, stimulus_b)
count += len(stimulus_a)
print count, "vectors passed"

stimulus_b = [0xFF800000 for i in xrange(1000)]
stimulus_a = [randint(0, 1<<32) for i in xrange(1000)]
test_cores(stimulus_a, stimulus_b)
count += len(stimulus_a)
print count, "vectors passed"

stimulus_a = [0x7FC00000 for i in xrange(1000)]
stimulus_b = [randint(0, 1<<32) for i in xrange(1000)]
test_cores(stimulus_a, stimulus_b)
count += len(stimulus_a)
print count, "vectors passed"

stimulus_a = [0xFFC00000 for i in xrange(1000)]
stimulus_b = [randint(0, 1<<32) for i in xrange(1000)]
test_cores(stimulus_a, stimulus_b)
count += len(stimulus_a)
print count, "vectors passed"

stimulus_b = [0x7FC00000 for i in xrange(1000)]
stimulus_a = [randint(0, 1<<32) for i in xrange(1000)]
test_cores(stimulus_a, stimulus_b)
count += len(stimulus_a)
print count, "vectors passed"

stimulus_b = [0xFFC00000 for i in xrange(1000)]
stimulus_a = [randint(0, 1<<32) for i in xrange(1000)]
test_cores(stimulus_a, stimulus_b)
count += len(stimulus_a)
print count, "vectors passed"

#seed(0)
for i in xrange(1000000):
    stimulus_a = [randint(0, 1<<32) for i in xrange(5000)]
    stimulus_b = [randint(0, 1<<32) for i in xrange(5000)]
    test_cores(stimulus_a, stimulus_b)
    count += 5000
    print count, "vectors passed"
