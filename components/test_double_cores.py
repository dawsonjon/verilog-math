import sys

sys.path.append("..")

import subprocess
import random
import cores
import struct
from numpy import float32
from itertools import product
from random import randint
from multiprocessing import Process
from math import isnan


def trace(response, n):
    for name, values in response.items():
        print(name, values[n])


def get_mantissa(x):
    return x & 0x000FFFFFFFFFFFFF


def get_exponent(x):
    return ((x & 0x7FF0000000000000) >> 52) - 1023


def get_sign(x):
    return (x & 0x8000000000000000) >> 63


def is_nan(x):
    return get_exponent(x) == 1024 and get_mantissa(x) != 0


def is_inf(x):
    return get_exponent(x) == 1024 and get_mantissa(x) == 0


def is_pos_inf(x):
    return is_inf(x) and not get_sign(x)


def is_neg_inf(x):
    return is_inf(x) and get_sign(x)


def match(x, y):
    return (
        (is_pos_inf(x) and is_pos_inf(y))
        or (is_neg_inf(x) and is_neg_inf(y))
        or (is_nan(x) and is_nan(y))
        or (x == y)
    )


def asdouble(x):
    string = []
    for i in range(8):
        byte = x >> 56
        byte &= 0xFF
        string.append(byte)
        x <<= 8
    string = bytes(string)
    return struct.unpack(">d", string)[0]


def failure(a, b, actual, expected):
    print("a        b        actual   expected")
    print("======== ======== ======== ========")
    print("%16x %16x %16x %16x fail" % (a, b, actual, expected))
    print("a", asdouble(a))
    print("b", asdouble(b))
    print("actual", asdouble(actual))
    print("expected", asdouble(expected))


def get_expected(core_name):
    subprocess.call("./reference_tests/" + core_name)
    inf = open("stim/%s_z_expected" % core_name)
    return [int(i) for i in inf]


def test_convert(core_name, core, a):
    print("testing", core_name, "...")
    stimulus = {core_name + "_a": a}

    response = core.test(stimulus, name=core_name)
    actual = response[core_name + "_z"]
    expected = get_expected(core_name)

    n = 0
    for a, i, j in zip(a, actual, expected):
        if asdouble(a) < 0 and "to_unsigned" in core_name:
            result = True
        elif asdouble(a) > (2 ** 64) - 1 and "to_unsigned" in core_name:
            result = True
        elif asdouble(a) > (2 ** 63) - 1 and "to_int" in core_name:
            result = True
        elif asdouble(a) < -(2 ** 63) and "to_int" in core_name:
            result = True
        elif isnan(asdouble(a)):
            result = True
        else:
            if j != i:
                result = False
            else:
                result = True
        if not result:
            trace(response, n)
            print("%08x %08x %08x fail" % (a, i, j))
            sys.exit(1)
        n += 1


def test_unary(core_name, core, a, b):
    print("testing", core_name, "...")
    stimulus = {
        core_name + "_a": a,
    }

    response = core.test(stimulus, name=core_name)
    actual = response[core_name + "_z"]
    expected = get_expected(core_name)

    n = 0
    for a, b, i, j in zip(a, b, actual, expected):
        result = match(i, j)
        if not result:
            failure(a, b, i, j)
            print("failed in vector", n)
            trace(response, n)
            # append failures to regression test file
            of = open("regression_tests", "a")
            of.write("%i %i\n" % (a, b))
            of.close()
            sys.exit(1)
        n += 1


def test_comparator(core_name, core, a, b):
    print("testing", core_name, "...")
    stimulus = {core_name + "_a": a, core_name + "_b": b}

    response = core.test(stimulus, name=core_name)
    actual = response[core_name + "_z"]
    expected = get_expected(core_name)

    n = 0
    for a, b, i, j in zip(a, b, actual, expected):
        if j != i:
            result = False
        else:
            result = True
        if not result:
            failure(a, b, i, j)
            print(n)
            trace(response, n)
            # append failures to regression test file
            of = open("regression_tests", "a")
            of.write("%i %i\n" % (a, b))
            of.close()
            sys.exit(1)
        n += 1


def test_binary(core_name, core, a, b):
    print("testing", core_name, "...")
    stimulus = {core_name + "_a": a, core_name + "_b": b}

    response = core.test(stimulus, name=core_name)
    actual = response[core_name + "_z"]
    expected = get_expected(core_name)

    n = 0
    for a, b, i, j in zip(a, b, actual, expected):
        result = match(j, i)
        if not result:
            failure(a, b, i, j)
            print("failed in vector", n)
            trace(response, n)
            # append failures to regression test file
            of = open("double_regression_tests", "a")
            of.write("%i %i\n" % (a, b))
            of.close()
            sys.exit(1)
        n += 1


def test_cores(stimulus_a, stimulus_b):
    binary_cores = {
        "double_mul": cores.double_mul,
        "double_add": cores.double_add,
        "double_div": cores.double_div,
        "double_max": cores.double_max,
        "double_min": cores.double_min,
    }
    processes = []
    for core_name, core in binary_cores.items():
        processes.append(
            Process(target=test_binary, args=[core_name, core, stimulus_a, stimulus_b])
        )

    converter_cores = {
        "double_to_int": cores.double_to_int,
        "double_to_unsigned_int": cores.double_to_unsigned_int,
        "int_to_double": cores.int_to_double,
        "unsigned_int_to_double": cores.unsigned_int_to_double,
    }
    for core_name, core in converter_cores.items():
        processes.append(
            Process(target=test_convert, args=[core_name, core, stimulus_a])
        )

    unary_cores = {
        "double_sqrt": cores.double_sqrt,
        "double_abs": cores.double_abs,
        "double_neg": cores.double_neg,
        "double_trunc": cores.double_trunc,
        "double_ceil": cores.double_ceil,
        "double_floor": cores.double_floor,
    }
    for core_name, core in unary_cores.items():
        processes.append(
            Process(target=test_unary, args=[core_name, core, stimulus_a, stimulus_b])
        )
    comparator_cores = {
        "double_gt": cores.double_gt,
        "double_lt": cores.double_lt,
        "double_le": cores.double_le,
        "double_ge": cores.double_ge,
        "double_eq": cores.double_eq,
        "double_ne": cores.double_ne,
    }
    for core_name, core in comparator_cores.items():
        processes.append(
            Process(
                target=test_comparator, args=[core_name, core, stimulus_a, stimulus_b]
            )
        )

    for i in processes:
        i.daemon = True
        i.start()

    for i in processes:
        i.join()
        if i.exitcode:
            exit(i.exitcode)


###############################################################################
# tests start here
###############################################################################

count = 0

# regression tests
inf = open("double_regression_tests")
stimulus_a = []
stimulus_b = []
for line in inf.read().splitlines():
    a, b = line.strip().split()
    stimulus_a.append(int(a))
    stimulus_b.append(int(b))
test_cores(stimulus_a, stimulus_b)
count += len(stimulus_a)
print(count, "vectors passed")


# corner cases
from itertools import permutations

special_values = [
    0x8000000000000000,
    0x0000000000000000,
    0x7FF0000000000000,
    0xFFF0000000000000,
    0x7FF8000000000000,
    0xFFF8000000000000,
]
vectors = list(product(special_values, special_values))
stimulus_a = [a for a, b in vectors]
stimulus_b = [b for a, b in vectors]
test_cores(stimulus_a, stimulus_b)
count += len(stimulus_a)
print(count, "vectors passed")

# edge cases
stimulus_a = [0x8000000000000000 for i in range(1000)]
stimulus_b = [randint(0, 1 << 64) for i in range(1000)]
test_cores(stimulus_a, stimulus_b)
count += len(stimulus_a)
print(count, "vectors passed")

stimulus_a = [0x0000000000000000 for i in range(1000)]
stimulus_b = [randint(0, 1 << 64) for i in range(1000)]
test_cores(stimulus_a, stimulus_b)
count += len(stimulus_a)
print(count, "vectors passed")

stimulus_b = [0x8000000000000000 for i in range(1000)]
stimulus_a = [randint(0, 1 << 64) for i in range(1000)]
test_cores(stimulus_a, stimulus_b)
count += len(stimulus_a)
print(count, "vectors passed")

stimulus_b = [0x0000000000000000 for i in range(1000)]
stimulus_a = [randint(0, 1 << 64) for i in range(1000)]
test_cores(stimulus_a, stimulus_b)
count += len(stimulus_a)
print(count, "vectors passed")

stimulus_a = [0x7FF0000000000000 for i in range(1000)]
stimulus_b = [randint(0, 1 << 64) for i in range(1000)]
test_cores(stimulus_a, stimulus_b)
count += len(stimulus_a)
print(count, "vectors passed")

stimulus_a = [0xFFF0000000000000 for i in range(1000)]
stimulus_b = [randint(0, 1 << 64) for i in range(1000)]
test_cores(stimulus_a, stimulus_b)
count += len(stimulus_a)
print(count, "vectors passed")

stimulus_b = [0x7FF0000000000000 for i in range(1000)]
stimulus_a = [randint(0, 1 << 64) for i in range(1000)]
test_cores(stimulus_a, stimulus_b)
count += len(stimulus_a)
print(count, "vectors passed")

stimulus_b = [0xFFF0000000000000 for i in range(1000)]
stimulus_a = [randint(0, 1 << 64) for i in range(1000)]
test_cores(stimulus_a, stimulus_b)
count += len(stimulus_a)
print(count, "vectors passed")

stimulus_a = [0x7FF8000000000000 for i in range(1000)]
stimulus_b = [randint(0, 1 << 64) for i in range(1000)]
test_cores(stimulus_a, stimulus_b)
count += len(stimulus_a)
print(count, "vectors passed")

stimulus_a = [0xFFF8000000000000 for i in range(1000)]
stimulus_b = [randint(0, 1 << 64) for i in range(1000)]
test_cores(stimulus_a, stimulus_b)
count += len(stimulus_a)
print(count, "vectors passed")

stimulus_b = [0x7FF8000000000000 for i in range(1000)]
stimulus_a = [randint(0, 1 << 64) for i in range(1000)]
test_cores(stimulus_a, stimulus_b)
count += len(stimulus_a)
print(count, "vectors passed")

stimulus_b = [0xFFF8000000000000 for i in range(1000)]
stimulus_a = [randint(0, 1 << 64) for i in range(1000)]
test_cores(stimulus_a, stimulus_b)
count += len(stimulus_a)
print(count, "vectors passed")

# seed(0)
for i in range(1000000):
    stimulus_a = [randint(0, 1 << 64) for i in range(5000)]
    stimulus_b = [randint(0, 1 << 64) for i in range(5000)]
    test_cores(stimulus_a, stimulus_b)
    count += 5000
    print(count, "vectors passed")
