from math import log, floor

import pipeliner
from pipeliner import *

from test_probe import test_probe, trace

class Float:
    def __init__(self, sign, exponent, mantissa, inf, nan, ebits=8, mbits=24):
        self.s = sign
        self.e = exponent
        self.m = mantissa
        self.inf = inf
        self.nan = nan
        self.e_bits = ebits
        self.m_bits = mbits
        self.e_min = -(1<<(ebits-1))+2
        self.e_max = (1<<(ebits-1))-1

    def __mul__(self, other):

        #add a bit to e so that we can test for overflow
        a_e = s_resize(a.e, self.e_bits+1)
        b_e = s_resize(b.e, self.e_bits+1)
        a_m = resize(a.m, self.m_bits*2)
        b_m = resize(b.m, self.m_bits*2)
        a_s = self.s
        b_s = other.s
        a_inf = self.inf
        b_inf = other.inf
        a_nan = self.nan
        b_nan = other.nan

        z_s = a_s ^ b_s
        z_e = a_e + b_e + 1
        z_m = a_m * b_m

        z_m, z_e, normalise(z_m, z_e, self.e_min)
        z_m = z_m[self.m_bits*2-1:self.m_bits]
        g = z_m[self.m_bits-1]
        r = z_m[self.m_bits-2]
        s = z_m[self.m_bits-3:0] != Constant(self.m_bits, 0)
        z_m, z_e = fpround(z_m, z_e, g, r, s)

        overflow = z_e[self.e_bits]
        z_e = z_e[self.e_bits-1:0]
        z_inf = overflow | a_inf | b_inf
        z_nan = a_nan | b_nan

        return Float(z_s, z_e, z_m, z_inf, z_nan, self.e_bits, self.m_bits)

    def __add__(self, other):

        #add a bit to e so that we can test for overflow
        a_e = s_resize(self.e, self.e_bits+1)
        b_e = s_resize(other.e, self.e_bits+1)
        a_m = self.m
        b_m = other.m
        a_s = self.s
        b_s = other.s
        a_inf = self.inf
        b_inf = other.inf
        a_nan = self.nan
        b_nan = other.nan

        #swap operands so that larger contains the operand with larger exponent
        a_gt_b = (s_gt(a_e, b_e) | a_inf) & ~b_inf
        larger_m  = select(a_m, b_m, a_gt_b)
        larger_e  = select(a_e, b_e, a_gt_b)
        larger_s  = select(a_s, b_s, a_gt_b)
        smaller_m = select(b_m, a_m, a_gt_b)
        smaller_e = select(b_e, a_e, a_gt_b)
        smaller_s = select(b_s, a_s, a_gt_b)
        smaller_m = resize(smaller_m, self.m_bits+4) << 3 #add 3 bits for guard, round and sticky
        larger_m  = resize(larger_m, self.m_bits+4) << 3 #and a fourth bit for overflow in mantissa

        #increase exponent of smaller operand to match larger operand
        difference = larger_e - smaller_e
        mask = Constant(smaller_m.bits, smaller_m.bits) - difference

        #pipeline stage 1
        larger_m  = Register(larger_m)
        larger_e  = Register(larger_e)
        larger_s  = Register(larger_s)
        smaller_m = Register(smaller_m)
        smaller_e = Register(smaller_e)
        smaller_s = Register(smaller_s)
        difference = Register(difference)
        mask = Register(mask)

        smaller_e = smaller_e + difference
        sticky = smaller_m << mask
        smaller_m = smaller_m >> difference
        sticky = sticky != 0
        smaller_m |= sticky

        #pipeline stage 2
        smaller_m = Register(smaller_m)
        smaller_e = Register(smaller_e)
        sticky = Register(sticky)

        #swap operands so that larger contains the operand with larger mantissa
        a_ge_b    = larger_m >= smaller_m
        larger_m_1  = select(larger_m, smaller_m, a_ge_b)
        larger_e_1  = select(larger_e, smaller_e, a_ge_b)
        larger_s_1  = select(larger_s, smaller_s, a_ge_b)
        smaller_m = select(smaller_m, larger_m, a_ge_b)
        smaller_e = select(smaller_e, larger_e, a_ge_b)
        smaller_s = select(smaller_s, larger_s, a_ge_b)
        larger_m  = larger_m_1
        larger_e  = larger_e_1
        larger_s  = larger_s_1

        #pipeline stage 3
        larger_m  = Register(larger_m)
        larger_e  = Register(larger_e)
        larger_s  = Register(larger_s)
        smaller_m = Register(smaller_m)
        smaller_e = Register(smaller_e)
        smaller_s = Register(smaller_s)

        add_sub = a_s == b_s
        smaller_m = select(smaller_m, -smaller_m, add_sub)


        #pipeline stage 4
        smaller_m = Register(smaller_m)

        z_s = larger_s
        z_m = larger_m + smaller_m
        #Add one to the exponent, assuming that mantissa overflow
        #has occurred. If it hasn't the msb of the result will be zero
        #and the exponent will be reduced again accordingly.
        z_e = larger_e + 1 

        #pipeline stage 5
        z_m = Register(z_m)
        z_e = Register(z_e)

        z_m, z_e = normalise(z_m, z_e, self.e_min)

        #pipeline stage 6
        z_m = Register(z_m)
        z_e = Register(z_e)


        g = z_m[3]
        r = z_m[2]
        s = z_m[1] | z_m[0]
        z_m = z_m[self.m_bits+3:4]
        z_m, z_e = fpround(z_m, z_e, g, r, s)


        overflow = s_gt(z_e, Constant(self.e_bits, self.e_max))
        z_e = z_e[self.e_bits-1:0]
        z_inf = overflow | a_inf | b_inf
        z_nan = a_nan | b_nan | (a_inf & b_inf)

        
        z_s    = Register(z_s  )
        z_e    = Register(z_e  )
        z_m    = Register(z_m  )
        z_inf  = Register(z_inf)
        z_nan  = Register(z_nan)

        return Float(z_s, z_e, z_m, z_inf, z_nan, self.e_bits, self.m_bits)

class FPConstant(Float):
    def __init__(self, ebits, mbits, value):
        s = 1 if float(value) < 0 else 0
        value = abs(float(value))
        e = int(floor(log(value, 2)))
        m = value/(2**e)
        m *= (2**(mbits-1))
        m = int(round(m))

def single_to_float(a):
    s = a[31]
    e = a[30:23] - 127
    m = a[22:0]
    inf = (e==Constant(8, 128)) & (m==Constant(23, 0))
    nan = (e==Constant(8, 128)) & (m!=Constant(23, 0))
    denormal = e==Constant(8, -127)
    e = select(Constant(8, -126), e, denormal)
    m = cat(select(Constant(1, 0), Constant(1, 1), denormal), m)
    return Float(s, e, m, inf, nan, 8, 24)

def float_to_single(f):

    #normal numbers
    result = cat(cat(f.s, f.e+127), f.m[22:0])

    #denormal numbers
    denormal = (f.e==Constant(8, -126)) & ~f.m[23]
    denormal_result = cat(cat(f.s, Constant(8, 0)), f.m[22:0])
    result = select(denormal_result, result, denormal)

    #zeros
    zero = Constant(32, 0)
    result = select(zero, result, f.m==Constant(24, 0))

    #infs
    inf = cat(f.s, Constant(31, 0x7f800000))
    result = select(inf, result, f.inf)

    #nans
    nan = cat(f.s, Constant(31, 0x7fc00000))
    result = select(nan, result, f.nan)

    return result
    

def normalise(m, e, e_min):

    #try to normalise, but not if it would make the exponent less than the 
    #minimum in this case leave the number denormalised
    
    lz = leading_zeros(m)
    max_shift = e - Constant(e.bits, e_min)

    shift_amount = select(lz, max_shift, lz <= max_shift)
    m = m << shift_amount
    e = e - shift_amount

    return m, e

def fpround(m, e, g, r, s):

    roundup = g & (r | s | m[0])
    m = resize(m, m.bits+1) + roundup

    #correct for overflow in rounding
    overflow = m[m.bits-1]
    m = select(m[m.bits-1:1], m[m.bits-2:0], overflow)
    e = select(e + 1, e, overflow)
    return m, e

def leading_zeros(stream):
    out = stream.bits
    for i in range(stream.bits):
        out=select(stream.bits -1-i, out, stream[i])
    return out

def pipelined_add(a, b, width):
    bits = max([a.bits, b.bits])
    for lsb in range(0, bits, width):
        msb = min([lsb + width - 1, bits-1])
        a_part = a[msb:lsb]
        b_part = b[msb:lsb]
        if lsb:
            part_sum = resize(a_part, width+1)+b_part+carry
            z = cat(part_sum[width-1:0], z)
        else:
            part_sum = resize(a_part, width+1)+b_part
            z = part_sum[width-1:0]
        carry = part_sum[width]
        carry = Register(carry)
    return z

def pipelined_sub(a, b, width):
    bits = max([a.bits, b.bits])
    for lsb in range(0, bits, width):
        msb = min([lsb + width - 1, bits-1])
        a_part = a[msb:lsb]
        b_part = b[msb:lsb]
        if lsb:
            part_sum = resize(a_part, width+1)+(~b_part)+carry
            z = cat(part_sum[width-1:0], z)
        else:
            part_sum = resize(a_part, width+1)-b_part
            z = part_sum[width-1:0]
        carry = ~part_sum[width]
        carry = Register(carry)
    return z
