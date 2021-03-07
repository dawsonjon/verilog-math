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
from math import isnan, isinf


def trace(response, n):
    for name, values in response.items():
        print(name, values[n])


def asfloat(x):
    string = []
    for i in range(4):
        byte = x >> 24
        byte &= 0xFF
        string.append(byte)
        x <<= 8
    string = bytes(string)
    return struct.unpack(">f", string)[0]


def failure(a, b, actual, expected):
    print("a        b        actual   expected")
    print("======== ======== ======== ========")
    print("%08x %08x %08x %08x fail" % (a, b, actual, expected))
    print("a", asfloat(a))
    print("b", asfloat(b))
    print("actual", asfloat(actual))
    print("expected", asfloat(expected))


def get_expected(core_name):
    subprocess.call("./reference_tests/" + core_name)
    inf = open("stim/%s_z_expected" % core_name)
    return [int(i) for i in inf]


def get_mantissa(x):
    return 0x7FFFFF & x


def get_exponent(x):
    return ((x & 0x7F800000) >> 23) - 127


def get_sign(x):
    return (x & 0x80000000) >> 31


def is_nan(x):
    return get_exponent(x) == 128 and get_mantissa(x) != 0


def is_inf(x):
    return get_exponent(x) == 128 and get_mantissa(x) == 0


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


def test_convert(core_name, core, a):
    print("testing", core_name, "...")
    stimulus = {core_name + "_a": a}

    response = core.test(stimulus, name=core_name)
    actual = response[core_name + "_z"]
    expected = get_expected(core_name)

    n = 0
    for a, i, j in zip(a, actual, expected):
        if asfloat(a) < 0 and "to_unsigned" in core_name:
            result = True
        elif asfloat(a) > (2 ** 32) - 1 and "to_unsigned" in core_name:
            result = True
        elif asfloat(a) > (2 ** 31) - 1 and "to_int" in core_name:
            result = True
        elif asfloat(a) < -(2 ** 31) and "to_int" in core_name:
            result = True
        elif isnan(asfloat(a)):
            result = True
        else:
            if j != i:
                result = False
            else:
                result = True
        if not result:
            trace(response, n)
            print("input actual expected")
            print("%08x %08x %08x fail" % (a, i, j))
            print(asfloat(a), asfloat(i), asfloat(j))
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
        result = match(i, j)
        if not result:
            print("%08x %08x %08x %08x fail" % (a, b, i, j))
            print("a:", asfloat(a))
            print("b:", asfloat(b))
            print("actual", asfloat(i))
            print("expected", asfloat(j))
            print(n)
            trace(response, n)
            # append failures to regression test file
            of = open("regression_tests", "a")
            of.write("%i %i\n" % (a, b))
            of.close()
            sys.exit(1)
        n += 1


def test_cores(stimulus_a, stimulus_b):
    binary_cores = {
        "mul": cores.mul,
        # "div":cores.div,
        "add": cores.add,
        "single_max": cores.single_max,
        "single_min": cores.single_min,
    }
    processes = []
    for core_name, core in binary_cores.items():
        processes.append(
            Process(target=test_binary, args=[core_name, core, stimulus_a, stimulus_b])
        )

    converter_cores = {
        "single_to_int": cores.single_to_int,
        "single_to_unsigned_int": cores.single_to_unsigned_int,
        "int_to_single": cores.int_to_single,
        "unsigned_int_to_single": cores.unsigned_int_to_single,
    }
    for core_name, core in converter_cores.items():
        processes.append(
            Process(target=test_convert, args=[core_name, core, stimulus_a])
        )

    unary_cores = {
        "sqrt": cores.sqrt,
        "abs": cores.abs,
        "neg": cores.neg,
        "trunc": cores.trunc,
        "ceil": cores.ceil,
        "floor": cores.floor,
    }
    for core_name, core in unary_cores.items():
        processes.append(
            Process(target=test_unary, args=[core_name, core, stimulus_a, stimulus_b])
        )
    comparator_cores = {
        "gt": cores.gt,
        "lt": cores.lt,
        "le": cores.le,
        "ge": cores.ge,
        "eq": cores.eq,
        "ne": cores.ne,
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
inf = open("regression_tests")
stimulus_a = []
stimulus_b = []
for line in inf.read().splitlines():
    a, b = line.strip().split()
    stimulus_a.append(int(a))
    stimulus_b.append(int(b))
test_cores(stimulus_a, stimulus_b)
count += len(stimulus_a)
print(count, "vectors passed")

# regression tests
stimulus_a = [
    0xAF860E03,
    0x22CB525A,
    0x40000000,
    0x83E73D5C,
    0xBF9B1E94,
    0x34082401,
    0x5E8EF81,
    0x5C75DA81,
    0x2B017,
]
stimulus_b = [
    0x0681DB7F,
    0xADD79EFA,
    0xC0000000,
    0x1C800000,
    0xC038ED3A,
    0xB328CD45,
    0x114F3DB,
    0x2F642A39,
    0xFF3807AB,
]
test_cores(stimulus_a, stimulus_b)
count += len(stimulus_a)
print(count, "vectors passed")

# corner cases
special_values = [
    0x80000000,
    0x00000000,
    0x7F800000,
    0xFF800000,
    0x7FC00000,
    0xFFC00000,
    0x00000001,
    0x00400000,
    0x007FFFFF,
    0x80000001,
    0x80400000,
    0x807FFFFF,
]
vectors = list(product(special_values, special_values))
stimulus_a = [a for a, b in vectors]
stimulus_b = [b for a, b in vectors]
test_cores(stimulus_a, stimulus_b)
count += len(stimulus_a)
print(count, "vectors passed")

# edge cases
stimulus_a = [0x80000000 for i in range(1000)]
stimulus_b = [randint(0, 1 << 32) for i in range(1000)]
test_cores(stimulus_a, stimulus_b)
count += len(stimulus_a)
print(count, "vectors passed")

stimulus_a = [0x00000000 for i in range(1000)]
stimulus_b = [randint(0, 1 << 32) for i in range(1000)]
test_cores(stimulus_a, stimulus_b)
count += len(stimulus_a)
print(count, "vectors passed")

stimulus_b = [0x80000000 for i in range(1000)]
stimulus_a = [randint(0, 1 << 32) for i in range(1000)]
test_cores(stimulus_a, stimulus_b)
count += len(stimulus_a)
print(count, "vectors passed")

stimulus_b = [0x00000000 for i in range(1000)]
stimulus_a = [randint(0, 1 << 32) for i in range(1000)]
test_cores(stimulus_a, stimulus_b)
count += len(stimulus_a)
print(count, "vectors passed")

stimulus_a = [0x7F800000 for i in range(1000)]
stimulus_b = [randint(0, 1 << 32) for i in range(1000)]
test_cores(stimulus_a, stimulus_b)
count += len(stimulus_a)
print(count, "vectors passed")

stimulus_a = [0xFF800000 for i in range(1000)]
stimulus_b = [randint(0, 1 << 32) for i in range(1000)]
test_cores(stimulus_a, stimulus_b)
count += len(stimulus_a)
print(count, "vectors passed")

stimulus_b = [0x7F800000 for i in range(1000)]
stimulus_a = [randint(0, 1 << 32) for i in range(1000)]
test_cores(stimulus_a, stimulus_b)
count += len(stimulus_a)
print(count, "vectors passed")

stimulus_b = [0xFF800000 for i in range(1000)]
stimulus_a = [randint(0, 1 << 32) for i in range(1000)]
test_cores(stimulus_a, stimulus_b)
count += len(stimulus_a)
print(count, "vectors passed")

stimulus_a = [0x7FC00000 for i in range(1000)]
stimulus_b = [randint(0, 1 << 32) for i in range(1000)]
test_cores(stimulus_a, stimulus_b)
count += len(stimulus_a)
print(count, "vectors passed")

stimulus_a = [0xFFC00000 for i in range(1000)]
stimulus_b = [randint(0, 1 << 32) for i in range(1000)]
test_cores(stimulus_a, stimulus_b)
count += len(stimulus_a)
print(count, "vectors passed")

stimulus_b = [0x7FC00000 for i in range(1000)]
stimulus_a = [randint(0, 1 << 32) for i in range(1000)]
test_cores(stimulus_a, stimulus_b)
count += len(stimulus_a)
print(count, "vectors passed")

stimulus_b = [0xFFC00000 for i in range(1000)]
stimulus_a = [randint(0, 1 << 32) for i in range(1000)]
test_cores(stimulus_a, stimulus_b)
count += len(stimulus_a)
print(count, "vectors passed")

stimulus_b = [0x00000001 for i in range(1000)]
stimulus_a = [randint(0, 1 << 32) for i in range(1000)]
test_cores(stimulus_a, stimulus_b)
count += len(stimulus_a)
print(count, "vectors passed")

stimulus_b = [0x00400000 for i in range(1000)]
stimulus_a = [randint(0, 1 << 32) for i in range(1000)]
test_cores(stimulus_a, stimulus_b)
count += len(stimulus_a)
print(count, "vectors passed")

stimulus_b = [0x007FFFFF for i in range(1000)]
stimulus_a = [randint(0, 1 << 32) for i in range(1000)]
test_cores(stimulus_a, stimulus_b)
count += len(stimulus_a)
print(count, "vectors passed")

stimulus_b = [0x80000001 for i in range(1000)]
stimulus_a = [randint(0, 1 << 32) for i in range(1000)]
test_cores(stimulus_a, stimulus_b)
count += len(stimulus_a)
print(count, "vectors passed")

stimulus_b = [0x80400000 for i in range(1000)]
stimulus_a = [randint(0, 1 << 32) for i in range(1000)]
test_cores(stimulus_a, stimulus_b)
count += len(stimulus_a)
print(count, "vectors passed")

stimulus_b = [0x807FFFFF for i in range(1000)]
stimulus_a = [randint(0, 1 << 32) for i in range(1000)]
test_cores(stimulus_a, stimulus_b)
count += len(stimulus_a)
print(count, "vectors passed")

stimulus_b = [randint(0, 1) << 31 | randint(0, 0x7FFFFF) for i in range(1000)]
stimulus_a = [randint(0, 1 << 32) for i in range(1000)]
test_cores(stimulus_a, stimulus_b)
count += len(stimulus_a)
print(count, "vectors passed")

# seed(0)
for i in range(1000000):
    stimulus_a = [randint(0, 1 << 32) for i in range(5000)]
    stimulus_b = [randint(0, 1 << 32) for i in range(5000)]
    test_cores(stimulus_a, stimulus_b)
    count += 5000
    print(count, "vectors passed")
