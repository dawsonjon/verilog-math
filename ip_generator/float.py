from math import log, floor, ceil

from . import pipeliner
from .pipeliner import *


def fselect(t, f, sel):
    assert t.e_bits == f.e_bits
    assert t.m_bits == f.m_bits
    s = select(t.s, f.s, sel)
    e = select(t.e, f.e, sel)
    m = select(t.m, f.m, sel)
    inf = select(t.inf, f.inf, sel)
    nan = select(t.nan, f.nan, sel)
    return Float(s, e, m, inf, nan, t.e_bits, t.m_bits)


class Float:
    def __init__(self, sign, exponent, mantissa, inf, nan, ebits=8, mbits=24):
        self.s = sign
        self.e = exponent
        self.m = mantissa
        self.inf = inf
        self.nan = nan
        self.e_bits = ebits
        self.m_bits = mbits
        self.e_min = -(1 << (ebits - 1)) + 2
        self.e_max = (1 << (ebits - 1)) - 1

    def sqrt(self, debug=None):

        # add a bit to e so that we can test for overflow
        a_e = s_resize(self.e, self.e_bits + 2)
        a_m = self.m
        a_s = self.s
        a_inf = self.inf
        a_nan = self.nan

        a_m, a_e = normalise(a_m, a_e, self.e_min * 2)
        a_m = resize(a_m, self.m_bits * 2 + 3)

        # if a_e is not even, rescale e and m
        odd = a_e[0]
        a_e = select(a_e - 1, a_e, odd)
        a_m = select(a_m << 1, a_m, odd)

        # pre-multiply m so that we get the useful bits, add 1 bit for rounding
        a_m = a_m << self.m_bits + 1
        z_m = sqrt(a_m)
        z_m = z_m[self.m_bits : 0]
        z_s = a_s

        # sqrt of 2^e == s^0.5*e
        z_e = s_sr(a_e, Constant(a_e.bits, 1))

        # handle underflow
        z_e = Register(z_e)
        shift_amount = Constant(z_e.bits, self.e_min) - z_e
        shift_amount = select(0, shift_amount, shift_amount[z_e.bits - 1])
        shift_amount = Register(shift_amount)
        z_m >>= shift_amount
        z_e += shift_amount
        z_m = Register(z_m)
        z_e = Register(z_e)

        # normalise
        z_m, z_e = normalise(z_m, z_e, self.e_min)
        g = z_m[0]
        z_m = z_m[self.m_bits : 1]
        z_m, z_e = fpround(z_m, z_e, g, Constant(1, 1), Constant(1, 0))

        z_e = z_e[self.e_bits - 1 : 0]
        z_inf = a_inf
        z_nan = a_nan | (a_s & (z_m != 0))

        return Float(z_s, z_e, z_m, z_inf, z_nan, self.e_bits, self.m_bits)

    def __truediv__(self, other):

        # add a bit to e so that we can test for overflow
        a_e = s_resize(self.e, self.e_bits + 2)
        b_e = s_resize(other.e, self.e_bits + 2)
        a_m = self.m
        b_m = other.m
        a_s = self.s
        b_s = other.s
        a_inf = self.inf
        b_inf = other.inf
        a_nan = self.nan
        b_nan = other.nan

        a_m, a_e = normalise(a_m, a_e, self.e_min * 2)
        b_m, b_e = normalise(b_m, b_e, self.e_min * 2)

        a_m = resize(a_m, self.m_bits + 3) << 3
        b_m = resize(b_m, self.m_bits + 3) << 3

        z_s = a_s ^ b_s
        z_e = a_e - b_e
        z_m, remainder = fraction_divide(a_m, b_m)

        # handle underflow
        z_e = Register(z_e)
        shift_amount = Constant(z_e.bits, self.e_min) - z_e
        shift_amount = Register(shift_amount)
        shift_amount = select(0, shift_amount, shift_amount[z_e.bits - 1])
        shift_amount = Register(shift_amount)
        z_m >>= shift_amount
        z_e += shift_amount
        z_m = Register(z_m)
        z_e = Register(z_e)

        z_m, z_e = normalise(z_m, z_e, self.e_min)
        g = z_m[2]
        r = z_m[1]
        s = z_m[0] | (remainder != 0)
        z_m = (z_m >> 3)[self.m_bits - 1 : 0]
        s = Register(s)
        z_m, z_e = fpround(z_m, z_e, g, r, s)

        overflow = s_gt(z_e, Constant(self.e_bits + 1, self.e_max))
        z_e = z_e[self.e_bits - 1 : 0]
        z_inf = overflow | a_inf | Register(b_m == 0)
        z_nan = a_nan | b_nan

        # handle divide by inf
        z_m = select(0, z_m, b_inf)
        z_inf = select(0, z_inf, b_inf)
        z_nan = a_nan | b_nan | (a_inf & b_inf) | ((a_m == 0) & (b_m == 0))

        return Float(z_s, z_e, z_m, z_inf, z_nan, self.e_bits, self.m_bits)

    def __mul__(self, other, debug=None):

        # add a bit to e so that we can test for overflow
        a_e = s_resize(self.e, self.e_bits + 2)
        b_e = s_resize(other.e, self.e_bits + 2)
        a_m = self.m
        b_m = other.m
        a_s = self.s
        b_s = other.s
        a_inf = self.inf
        b_inf = other.inf
        a_nan = self.nan
        b_nan = other.nan

        z_s = a_s ^ b_s
        z_e = a_e + b_e + 1
        z_m = pipelined_mul(a_m, b_m)

        # handle underflow
        shift_amount = Constant(z_e.bits, self.e_min) - z_e
        shift_amount = select(0, shift_amount, shift_amount[z_e.bits - 1])
        z_m, carry = lshift_with_carry(z_m, shift_amount)
        z_e += shift_amount
        z_m = Register(z_m)
        z_e = Register(z_e)
        s = carry != 0

        z_m, z_e = normalise(z_m, z_e, self.e_min)

        g = z_m[self.m_bits - 1]
        r = z_m[self.m_bits - 2]
        s = (z_m[self.m_bits - 3 : 0] != Constant(self.m_bits, 0)) | s
        s = Register(s)
        z_m = z_m[self.m_bits * 2 - 1 : self.m_bits]
        z_m, z_e = fpround(z_m, z_e, g, r, s)

        overflow = s_gt(z_e, Constant(self.e_bits + 1, self.e_max))
        z_e = z_e[self.e_bits - 1 : 0]
        z_inf = overflow | a_inf | b_inf
        z_nan = a_nan | b_nan | (a_inf & (b_m == 0)) | (b_inf & (a_m == 0))

        return Float(z_s, z_e, z_m, z_inf, z_nan, self.e_bits, self.m_bits)

    def __add__(self, other):

        # add a bit to e so that we can test for overflow
        a_e = s_resize(self.e, self.e_bits + 1)
        b_e = s_resize(other.e, self.e_bits + 1)
        a_m = self.m
        b_m = other.m
        a_s = self.s
        b_s = other.s
        a_inf = self.inf
        b_inf = other.inf
        a_nan = self.nan
        b_nan = other.nan

        # swap operands so that larger contains the operand with larger exponent
        a_gt_b = (s_gt(a_e, b_e) | a_inf) & ~b_inf
        larger_m = select(a_m, b_m, a_gt_b)
        larger_e = select(a_e, b_e, a_gt_b)
        larger_s = select(a_s, b_s, a_gt_b)
        smaller_m = select(b_m, a_m, a_gt_b)
        smaller_e = select(b_e, a_e, a_gt_b)
        smaller_s = select(b_s, a_s, a_gt_b)
        smaller_m = (
            resize(smaller_m, self.m_bits + 4) << 3
        )  # add 3 bits for guard, round and sticky
        larger_m = (
            resize(larger_m, self.m_bits + 4) << 3
        )  # and a fourth bit for overflow in mantissa

        # increase exponent of smaller operand to match larger operand
        difference = larger_e - smaller_e
        mask = Constant(smaller_m.bits, smaller_m.bits) - difference
        smaller_e = smaller_e + difference
        sticky = smaller_m << mask
        smaller_m = smaller_m >> difference
        sticky = sticky != 0
        smaller_m |= sticky

        # swap operands so that larger contains the operand with larger mantissa
        a_ge_b = larger_m >= smaller_m
        larger_m_1 = select(larger_m, smaller_m, a_ge_b)
        larger_e_1 = select(larger_e, smaller_e, a_ge_b)
        larger_s_1 = select(larger_s, smaller_s, a_ge_b)
        smaller_m = select(smaller_m, larger_m, a_ge_b)
        smaller_e = select(smaller_e, larger_e, a_ge_b)
        smaller_s = select(smaller_s, larger_s, a_ge_b)
        larger_m = larger_m_1
        larger_e = larger_e_1
        larger_s = larger_s_1

        # if the signs differ perform a subtraction instead
        add_sub = a_s == b_s
        negative_smaller_m = Constant(smaller_m.bits, 0) - smaller_m
        smaller_m = select(smaller_m, negative_smaller_m, add_sub)
        smaller_m = Register(smaller_m)
        larger_m = Register(larger_m)

        # perform the addition
        # Add one to the exponent, assuming that mantissa overflow
        # has occurred. If it hasn't the msb of the result will be zero
        # and the exponent will be reduced again accordingly.
        z_m = larger_m + smaller_m
        z_s = select(a_s & b_s, larger_s, Register(z_m) == 0)
        z_e = larger_e + 1
        z_m = Register(z_m)
        z_e = Register(z_e)

        # normalise the result
        z_m, z_e = normalise(z_m, z_e, self.e_min)

        # perform rounding
        g = z_m[3]
        r = z_m[2]
        s = z_m[1] | z_m[0]
        z_m = z_m[self.m_bits + 3 : 4]
        s = Register(s)
        z_m, z_e = fpround(z_m, z_e, g, r, s)

        # handle special cases
        overflow = s_gt(z_e, Constant(self.e_bits, self.e_max))
        z_e = z_e[self.e_bits - 1 : 0]
        z_inf = overflow | a_inf | b_inf
        z_s = select(larger_s, z_s, z_inf)
        z_nan = a_nan | b_nan | (a_inf & b_inf & (a_s ^ b_s))

        return Float(z_s, z_e, z_m, z_inf, z_nan, self.e_bits, self.m_bits)

    def __sub__(self, other):
        f = other
        f = Float(~f.s, f.e, f.m, f.inf, f.nan, f.e_bits, f.m_bits)
        return self + f

    def __gt__(self, other, debug=None):
        result = other - self
        return (result.m != 0) & result.s & ~self.nan & ~other.nan

    def __lt__(self, other, debug=None):
        result = self - other
        return (result.m != 0) & result.s & ~self.nan & ~other.nan

    def __ge__(self, other, debug=None):
        result = self - other
        return ((result.m == 0) | ~result.s) & ~self.nan & ~other.nan

    def __le__(self, other, debug=None):
        result = other - self
        return ((result.m == 0) | ~result.s) & ~self.nan & ~other.nan

    def __eq__(self, other, debug=None):
        return (
            ((self.s == other.s) & (self.e == other.e) & (self.m == other.m))
            | (
                # (self.e==0) &
                # (other.e==0) &
                (self.m == 0)
                & (other.m == 0)
            )
        ) & ~(self.nan | other.nan)

    def __ne__(self, other, debug=None):
        return ~(self == other)

    def trunc(self, debug=None):
        s = self.s
        e = self.e
        m = self.m

        big_number = s_ge(e, Constant(self.e_bits, self.m_bits))
        less_than_one = s_lt(e, Constant(self.e_bits, 0))

        fraction_bits = Constant(self.e_bits, self.m_bits - 1) - e
        fraction_bits = select(Constant(self.e_bits, 0), fraction_bits, big_number)

        m &= Constant(self.m_bits, -1) << fraction_bits
        m = select(Constant(self.m_bits, 0), m, less_than_one)

        inf = self.inf
        nan = self.nan
        return Float(s, e, m, inf, nan, self.e_bits, self.m_bits)

    def ceil(self, debug=None):
        integer_part = self.trunc()
        exact = integer_part == self
        result = fselect(
            integer_part, integer_part + FPConstant(self.e_bits, self.m_bits, 1), self.s
        )
        result = fselect(self, result, exact)
        return result

    def floor(self, debug=None):
        integer_part = self.trunc()
        exact = integer_part == self
        result = fselect(
            FPConstant(self.e_bits, self.m_bits, -1) + integer_part,
            integer_part,
            self.s,
        )
        # Output(debug, 'resultsign', result.s)
        # Output(debug, 'resultm', result.m)
        result = fselect(self, result, exact)
        # Output(debug, 'integer_partinf', integer_part.inf)
        # Output(debug, 'integer_partsign', integer_part.s)
        return result

    def max(self, other):
        ge = self >= other
        s = select(self.s, other.s, ge)
        e = select(self.e, other.e, ge)
        m = select(self.m, other.m, ge)
        inf = select(self.inf, other.inf, ge)
        nan = self.nan | other.nan
        return Float(s, e, m, inf, nan, self.e_bits, self.m_bits)

    def min(self, other):
        lt = self < other
        s = select(self.s, other.s, lt)
        e = select(self.e, other.e, lt)
        m = select(self.m, other.m, lt)
        inf = select(self.inf, other.inf, lt)
        nan = self.nan | other.nan
        return Float(s, e, m, inf, nan, self.e_bits, self.m_bits)

    def abs(self):
        return Float(
            Constant(1, 0), self.e, self.m, self.inf, self.nan, self.e_bits, self.m_bits
        )

    def neg(self):
        return Float(
            ~self.s, self.e, self.m, self.inf, self.nan, self.e_bits, self.m_bits
        )

    def to_int(self, bits=32):

        integer = cat(self.m, Constant(bits - self.m_bits, 0))
        integer >>= Constant(self.e_bits, bits) - self.e - 1
        integer = Register(integer)

        negative_integer = Register(-integer)
        integer = select(negative_integer, integer, self.s)
        Register(integer)

        return integer

    def to_unsigned(self, bits=32):

        integer = cat(self.m, Constant(bits - self.m_bits, 0))
        integer >>= Constant(self.e_bits, bits) - self.e - 1
        integer = Register(integer)

        return integer


class FPConstant(Float):
    def __init__(self, e_bits, m_bits, value):
        s = 1 if float(value) < 0 else 0
        value = abs(float(value))
        e = int(floor(log(value, 2)))
        m = value / (2 ** e)
        m *= 2 ** (m_bits - 1)
        m = int(round(m))
        Float.__init__(
            self,
            Constant(1, s),
            Constant(e_bits, e),
            Constant(m_bits, m),
            Constant(1, 0),
            Constant(1, 0),
            e_bits,
            m_bits,
        )


def int_to_float(integer, e_bits=8, m_bits=24):
    bits = integer.bits
    s = integer[bits - 1]
    integer = select(-integer, integer, s)
    integer = Register(integer)
    lz = leading_zeros(integer)
    lz = Register(lz)
    e = Constant(e_bits, integer.bits - 1) - lz
    m = integer << lz
    m = Register(m)
    guard = m[bits - m_bits - 1]
    round_bit = m[bits - m_bits - 2]
    sticky = m[bits - m_bits - 3 : 0] != 0
    sticky = Register(sticky)
    m = m[bits - 1 : bits - m_bits]
    m, e = fpround(m, e, guard, round_bit, sticky)
    return Float(s, e, m, Constant(1, 0), Constant(1, 0), e_bits, m_bits)


def unsigned_to_float(integer, e_bits=8, m_bits=24):
    bits = integer.bits
    integer = Register(integer)
    lz = leading_zeros(integer)
    lz = Register(lz)
    e = Constant(e_bits, integer.bits - 1) - lz
    m = integer << lz
    m = Register(m)
    guard = m[bits - m_bits - 1]
    round_bit = m[bits - m_bits - 2]
    sticky = m[bits - m_bits - 3 : 0] != 0
    sticky = Register(sticky)
    m = m[bits - 1 : bits - m_bits]
    m, e = fpround(m, e, guard, round_bit, sticky)
    return Float(Constant(1, 0), e, m, Constant(1, 0), Constant(1, 0), e_bits, m_bits)


def single_to_float(a, debug=None):
    s = a[31]
    e = a[30:23] - 127
    m = a[22:0]
    inf = (e == Constant(8, 128)) & (m == Constant(23, 0))
    nan = (e == Constant(8, 128)) & (m != Constant(23, 0))
    denormal = e == Constant(8, -127)
    e = select(Constant(8, -126), e, denormal)
    m = cat(select(Constant(1, 0), Constant(1, 1), denormal), m)
    return Float(s, e, m, inf, nan, 8, 24)


def double_to_float(a, debug=None):
    s = a[63]
    e = a[62:52] - 1023
    m = a[51:0]
    inf = (e == Constant(11, 1024)) & (m == Constant(52, 0))
    nan = (e == Constant(11, 1024)) & (m != Constant(52, 0))
    denormal = e == Constant(11, -1023)
    e = select(Constant(11, -1022), e, denormal)
    m = cat(select(Constant(1, 0), Constant(1, 1), denormal), m)
    return Float(s, e, m, inf, nan, 11, 53)


def float_to_single(f):

    # normal numbers
    result = cat(cat(f.s, f.e + 127), f.m[22:0])

    # denormal numbers
    denormal = (f.e == Constant(8, -126)) & ~f.m[23]
    denormal_result = cat(cat(f.s, Constant(8, 0)), f.m[22:0])
    result = select(denormal_result, result, denormal)

    # zeros
    zero = cat(f.s, Constant(31, 0))
    result = select(zero, result, f.m == Constant(24, 0))

    # infs
    inf = cat(f.s, Constant(31, 0x7F800000))
    result = select(inf, result, f.inf)

    # nans
    nan = cat(f.s, Constant(31, 0x7FC00000))
    result = select(nan, result, f.nan)

    return result


def float_to_double(f):

    # normal numbers
    result = cat(cat(f.s, f.e + 1023), f.m[51:0])

    # denormal numbers
    denormal = (f.e == Constant(11, -1022)) & ~f.m[52]
    denormal_result = cat(cat(f.s, Constant(11, 0)), f.m[51:0])
    result = select(denormal_result, result, denormal)

    # zeros
    zero = cat(f.s, Constant(63, 0))
    result = select(zero, result, f.m == Constant(53, 0))

    # infs
    inf = cat(f.s, Constant(63, 0x7FF0000000000000))
    result = select(inf, result, f.inf)

    # nans
    nan = cat(f.s, Constant(63, 0x7FF8000000000000))
    result = select(nan, result, f.nan)

    return result


def normalise(m, e, e_min):

    # try to normalise, but not if it would make the exponent less than the
    # minimum in this case leave the number denormalised
    lz = leading_zeros(m)
    lz = Register(lz)
    max_shift = e - Constant(e.bits, e_min)
    shift_amount = select(lz, max_shift, resize(lz, e.bits) <= max_shift)
    shift_amount = Register(shift_amount)
    m = m << shift_amount
    e = e - shift_amount

    return Register(m), Register(e)


def fpround(m, e, g, r, s):

    roundup = g & (r | s | m[0])
    m_plus_1 = resize(m, m.bits + 1) + 1
    m = select(m_plus_1, m, roundup)

    # correct for overflow in rounding
    overflow = m[m.bits - 1]
    m = select(m[m.bits - 1 : 1], m[m.bits - 2 : 0], overflow)
    e = e + overflow
    return Register(m), Register(e)


def leading_zeros(x):
    if x.bits == 2:
        return cat(~x[1] & ~x[0], ~x[1] & x[0])
    else:

        next_power_2 = 0
        while 2 ** next_power_2 < x.bits:
            next_power_2 += 1

        while x.bits < 2 ** next_power_2:
            x = cat(x, Constant(1, 1))

        msbs, lsbs = x[x.bits - 1 : x.bits // 2], x[x.bits // 2 - 1 : 0]
        lsb_zeros = leading_zeros(lsbs)
        msb_zeros = leading_zeros(msbs)

        lsbs_are_zero = lsb_zeros[lsb_zeros.bits - 1]
        msbs_are_zero = msb_zeros[msb_zeros.bits - 1]
        lsb_zeros = lsb_zeros[lsb_zeros.bits - 2 : 0]
        msb_zeros = msb_zeros[msb_zeros.bits - 2 : 0]

        return cat(
            msbs_are_zero & lsbs_are_zero,
            cat(
                msbs_are_zero & ~lsbs_are_zero,
                select(lsb_zeros, msb_zeros, msbs_are_zero),
            ),
        )


def pipelined_add(a, b, width):

    """Create a pipelined adder, width is the maximum number of bits
    to add before a pipeline register is added"""

    bits = max([a.bits, b.bits])
    a = resize(a, bits)
    b = resize(b, bits)
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
    return z[bits - 1 : 0]


def pipelined_mul(a, b):

    """Create a pipelined multiplier, width is the maximum number of bits
    to add before a pipeline register is added"""

    bits = max([a.bits, b.bits])

    num_parts = int(ceil(float(bits) / 17))
    a = resize(a, 17 * num_parts)
    b = resize(b, 17 * num_parts)
    a_parts = [(lsb, a[lsb + 16 : lsb]) for lsb in range(0, bits, 17)]
    b_parts = [(lsb, b[lsb + 16 : lsb]) for lsb in range(0, bits, 17)]
    partial_products = [
        (a_lsb + b_lsb, a, b) for a_lsb, a in a_parts for b_lsb, b in b_parts
    ]
    partial_products.sort(key=lambda x: x[0])

    old_lsb, a_part, b_part = partial_products[0]
    total = resize(a_part, 34) * b_part
    z = None
    for lsb, a_part, b_part in partial_products[1:]:
        product = resize(a_part, 34) * b_part
        if lsb > old_lsb:
            if z is None:
                z = total[16:0]
            else:
                z = cat(total[16:0], z)
            total = product + (total >> 17)
            total = resize(total, total.bits + 1)
            total = Register(total)
        else:
            total = product + total
            total = resize(total, total.bits + 1)
            total = Register(total)
        old_lsb = lsb
    z = cat(total[16:0], z)

    return z[(bits * 2) - 1 : 0]


def pipelined_sub(a, b, width):

    """Create a pipelined subtractor, width is the maximum number of bits
    to add before a pipeline register is added"""

    bits = max([a.bits, b.bits])
    a = resize(a, bits)
    b = resize(b, bits)
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
    return z[bits - 1 : 0]


def pipelined_lshift(a, b, depth):

    """Create a pipelined shifter, depth is the maximum number of 2-way
    multiplexors needed before pipeline registers are needed"""

    bits = max([a.bits, b.bits])
    a = resize(a, bits)
    b = resize(b, bits)

    shift_amount = 1
    z = a
    depth_count = 0
    for i in range(bits):
        z = select(z << shift_amount, z, b[i])
        shift_amount *= 2
        if depth_count == depth:
            depth_count = 0
            z = Register(z)
        else:
            depth_count += 1

    return z


def pipelined_rshift(a, b, depth):

    """Create a pipelined shifter, depth is the maximum number of 2-way
    multiplexors needed before pipeline registers are needed"""

    bits = max([a.bits, b.bits])
    a = resize(a, bits)
    b = resize(b, bits)

    shift_amount = 1
    z = a
    depth_count = 0
    for i in range(bits):
        z = select(z >> shift_amount, z, b[i])
        shift_amount *= 2
        if depth_count == depth:
            depth_count = 0
            z = Register(z)
        else:
            depth_count += 1

    return z


def lshift_with_carry(x, shift_amount):

    """shift left, but also return the bits that were shifted off the left"""

    bits = x.bits
    x = cat(x, Constant(bits, 0))
    x >>= shift_amount
    carry = x[bits - 1 : 0]
    x = x[bits * 2 - 1 : bits]
    return x, carry


def fraction_divide(dividend, divisor):
    bits = max([dividend.bits, divisor.bits])
    shifter = dividend
    quotient = Constant(bits, 0)
    for i in range(bits):
        difference = resize(shifter, bits + 1) - divisor
        negative = difference[bits]
        remainder = select(shifter, difference, negative)
        quotient = quotient << 1
        quotient = select(quotient, quotient | 1, negative)
        quotient = Register(quotient)
        remainder = Register(remainder)
        shifter = remainder << 1 | Constant(1, 0)

    return quotient, remainder
