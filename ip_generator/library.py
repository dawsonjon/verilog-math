from . import pipeliner
from .pipeliner import *


class FPType:
    def __init__(self, _type):
        if _type == "single":
            self.bits = 32
            self.mbits = 24
            self.ebits = 8
            self.bias = 127
            self.minimum_e = -126
        elif _type == "double":
            self.bits = 64
            self.mbits = 53
            self.ebits = 10
            self.bias = 1023
            self.minimum_e = -1022


def leading_zeros(stream):
    out = stream.bits
    for i in range(stream.bits):
        out = select(stream.bits - 1 - i, out, stream[i])
    return out


def nan(x=None, t=FPType("single")):
    if x is None:
        x = Constant(t.bits, 0)
    return cat(x[t.bits - 1], Constant(t.bits - 1, 0x7F800000))


def inf(x=None, t=FPType("single")):
    if x is None:
        x = Constant(bits, 0)
    return cat(x[t.bits - 1], Constant(t.bits - 1, 0x7FC00000))


def zero(x=None, t=FPType("single")):
    if x is None:
        x = Constant(bits, 0)
    return cat(x[t.bits - 1], Constant(t.bits - 1, 0))


def isnan(x, t=FPType("single")):
    return (x[t.bits - 2 : t.mbits - 1] == 255) & (x[t.mbits - 2 : 0] != 0)


def isinf(x, t=FPType("single")):
    return (x[t.bits - 2 : t.mbits - 1] == 255) & (x[t.mbits - 2 : 0] == 0)


def iszero(x, t=FPType("single")):
    return x[t.bits - 2 : 0] == 0


def fp_add(a, b, t=FPType("single")):

    bits = t.bits
    mbits = t.mbits
    ebits = t.ebits
    bias = t.bias
    minimum_e = t.minimum_e

    # unpack
    # ======

    a_s = a[bits - 1]
    b_s = b[bits - 1]
    a_e = a[bits - 2 : mbits - 1] - bias
    b_e = b[bits - 2 : mbits - 1] - bias
    a_m = a[mbits - 2 : 0]
    b_m = b[mbits - 2 : 0]

    # handle denormal numbers
    # =======================

    # if e is -127 that's really -126 but denormal
    a_denormal = a_e == (minimum_e - 1)
    b_denormal = b_e == (minimum_e - 1)
    a_e = select(Constant(ebits, minimum_e), a_e, a_denormal)
    b_e = select(Constant(ebits, minimum_e), b_e, b_denormal)
    a_m = cat(select(Constant(1, 0), Constant(1, 1), a_denormal), a_m)
    b_m = cat(select(Constant(1, 0), Constant(1, 1), b_denormal), b_m)

    # add a bit to e so that we can test for overflow
    a_e = resize(a_e, ebits + 1)
    b_e = resize(b_e, ebits + 1)

    # align operands
    # ==============

    # give a and b the same e
    a_gt_b = s_gt(a_e, b_e)
    difference = a_e - b_e
    b_e = select(b_e + difference, b_e, a_gt_b)
    b_m = select(b_m >> difference, b_m, a_gt_b)
    a_e = select(a_e + difference, a_e, ~a_gt_b)
    a_m = select(a_m >> difference, a_m, ~a_gt_b)
    a_m = resize(a_m, mbits + 4) << 3  # add 3 bits for guard, round and sticky
    b_m = resize(b_m, mbits + 4) << 3  # and a fourth bit to for overflow in mantissa

    # add
    # ====

    # if a and b have the same sign perform an addition
    # elif the signs are different perform a subtraction:
    #  if a > b
    #    subtract b from a
    #  else:
    #    subtract a from b

    a_plus_b = a_m + b_m
    a_minus_b = a_m - b_m
    b_minus_a = b_m - a_m
    a_gt_b = a_m > b_m
    add_sub = a_s == b_s
    z_m = select(a_plus_b, select(a_minus_b, b_minus_a, a_gt_b), add_sub)
    z_s = select(a_s, select(a_s, b_s, a_gt_b), add_sub)
    z_e = a_e + 1  # Add one to the exponent, assuming that mantissa overflow
    # has occurred. If it hasn't the msb of the result will be zero
    # and the exponent will be reduced again accordingly.

    # normalise
    # =========
    lz = leading_zeros(z_m)
    max_shift = z_e - minimum_e
    # try to normalise, but not if it would make the exponent less than the minimum
    # in this case leave the number denormalised
    shift_amount = select(lz, max_shift, lz <= max_shift)
    z_m = z_m << shift_amount
    z_e = z_e - shift_amount

    z_m = Register(z_m)

    # round
    # =====

    z_m = z_m[mbits + 3 : 4]
    g = z_m[3]
    r = z_m[2]
    s = z_m[1] | z_m[0]
    roundup = g & (r | s | z_m[0])
    z_m = resize(z_m, mbits + 1) + roundup

    # correct for overflow in rounding
    overflow = z_m[mbits]
    z_e = select(z_e + 1, z_e, overflow)
    z_m = select(z_m[mbits:1], z_m[mbits - 1 : 0], overflow)

    # pack
    # ====

    # check the exponent for overflow and denormal
    overflow = z_e[ebits]
    denormal = (z_e == Constant(ebits, minimum_e)) & ~z_m[mbits - 1]
    # reconstruct the result in ieee format
    result = cat(cat(z_s, z_e + bias), z_m[mbits - 2 : 0])
    # if exponent overflow occurred, the result is inf of the correct sign
    result = select(inf(result), result, overflow)
    # if result is denormal correct exponent bits
    denormal_result = cat(cat(z_s, Constant(8, 0)), z_m[mbits])
    result = select(denormal_result, result, denormal)

    # Override output for special input values
    # ========================================

    # if b is zero return a
    result = select(a, result, iszero(b))
    # if a is zero return b
    result = select(b, result, iszero(a))
    # if a and b are both zero, return zero with the right sign
    result = select(zero(a & b), result, iszero(a) & iszero(b))
    # if b is inf return inf with s of b
    result = select(inf(b), result, isinf(b))
    # if a is inf return inf with s of a
    result = select(inf(a), result, isinf(a))
    # if a  or b is a nan return nan
    result = select(nan(), result, isnan(a) | isnan(b))
    return result


def pipelined_add(a, b, width):
    bits = max([a.bits, b.bits])
    for lsb in range(0, bits, width):
        msb = min([lsb + width - 1, bits - 1])
        a_part = a[msb:lsb]
        b_part = b[msb:lsb]
        if lsb:
            part_sum = resize(a_part, width + 1) + b_part + carry
            z = cat(part_sum[width - 1 : 0], z)
        else:
            part_sum = resize(a_part, width + 1) + b_part
            z = part_sum[width - 1 : 0]
        carry = part_sum[width]
        carry = Register(carry)
    return z


def pipelined_sub(a, b, width):
    bits = max([a.bits, b.bits])
    for lsb in range(0, bits, width):
        msb = min([lsb + width - 1, bits - 1])
        a_part = a[msb:lsb]
        b_part = b[msb:lsb]
        if lsb:
            part_sum = resize(a_part, width + 1) + (~b_part) + carry
            z = cat(part_sum[width - 1 : 0], z)
        else:
            part_sum = resize(a_part, width + 1) - b_part
            z = part_sum[width - 1 : 0]
        carry = ~part_sum[width]
        carry = Register(carry)
    return z


from matplotlib.pyplot import plot, show
from numpy import zeros, ones

pipeliner.component = Component()
Output("z", pipelined_add(Input(8, "a"), Input(8, "b"), 4))
response = pipeliner.component.test({"a": list(range(256)), "b": list(range(256))})
print(response)

pipeliner.component = Component()
Output("z", pipelined_sub(Input(8, "a"), Input(8, "b"), 4))
stimulus = {"a": list(ones(256) * 255), "b": list(range(256))}
response = pipeliner.component.test(stimulus)
print(response)

pipeliner.component = Component()
Output("z", fp_add(Input(32, "a"), Input(32, "b")))
stimulus = {
    "a": [0x3F800000, 0x3F800000, 0x40000000, 0x41D00000],
    "b": [0x80000000, 0x3F800000, 0x3F800000, 0x3F800000],
}
response = pipeliner.component.test(stimulus)
print([hex(i) for i in response["z"]])


# Output("z", leading_zeros(Input(8, "a")))
# print test(component, {'a':[0, 1, 3, 7, 15]})
# print test(component, {'a':[0, 1, 2, 4, 8]})
#
# pipeliner.component = Component()
# div, rem = divide(Input(8, "a"), Input(8, "b"))
# Output("d", div)
# Output("r", rem)
# print test(pipeliner.component, {'a':[12, 100, 35, 5], 'b':[4, 10, 35, 2]})
