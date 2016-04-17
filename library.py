import pipeliner
from pipeliner import *

def leading_zeros(stream):
    out = stream.bits
    for i in range(stream.bits):
        out=select(stream.bits-1-i, out, getbit(stream, i))
    return out

def normalise(mantissa, exponent):
    mantissa = shift_left(mantissa, leading_zeros)
    exponent = sub(exponent, leading_zeros)
    return mantissa, exponent

def absolute(x):
    return select(x, negate(x), getbit(x, x.bits-1))

def divide(dividend, divisor):
    bits = max([dividend.bits, divisor.bits])

    remainder = Constant(bits, 0)
    quotient = Constant(bits, 0)
    for i in range(bits):
        shifter = remainder << 1 | getbit(dividend, bits-1-i)
        difference = resize(shifter, bits+1) - divisor
        negative = getbit(difference, bits)
        remainder = select(shifter, difference, negative)
        quotient = quotient << 1
        quotient = select(quotient, quotient | 1, negative)
        quotient = Register(quotient)
        remainder = Register(remainder)

    return quotient, remainder

def s_divide(dividend, divisor):
    divisor_sign = getbit(divisor, divisor.bits-1)
    dividend_sign = getbit(dividend, dividend.bits-1)
    sign = dividend_sign, divisor_sign
    quotient, remainder = divide(absolute(dividend), absolute(divisor))
    quotient = select(negate(quotient), quotient, sign)
    remainder = select(negate(remainder), remainder, dividend_sign)
    return quotient, remainder

def fp_add(a, b):

    bits = 32
    mbits = 24
    bias = 127
    minimum_exponent = -126

    #extract bits
    a_sign = getbit(a, bits-1)
    b_sign = getbit(b, bits-1)
    a_exponent = getbits(a, bits-2, mbits-1) - bias
    b_exponent = getbits(b, bits-2, mbits-1) - bias
    a_mantissa = cat(Constant(1, 1), getbits(a, mbits-2, 0))
    b_mantissa = cat(Constant(1, 1), getbits(b, mbits-2, 0))

    #give a and b the same exponent
    a_gt_b = s_gt(a_exponent, b_exponent)
    difference = a_exponent - b_exponent
    b_exponent = select(b_exponent + difference, b_exponent, a_gt_b)
    b_mantissa = select(b_mantissa >> difference, b_mantissa, a_gt_b)
    a_exponent = select(a_exponent + difference, a_exponent, bnot(a_gt_b))
    a_mantissa = select(a_mantissa >> difference, a_mantissa, bnot(a_gt_b))
    a_mantissa = resize(a_mantissa, mbits+4) << 3
    b_mantissa = resize(b_mantissa, mbits+4) << 3

    #add
    a_plus_b  = a_mantissa + b_mantissa
    a_minus_b = a_mantissa + b_mantissa
    b_minus_a = b_mantissa + a_mantissa
    a_gt_b = a_mantissa > b_mantissa
    add_sub = a_sign == b_sign
    z_mantissa = select(
        a_plus_b, 
        select(
            a_minus_b, 
            b_minus_a, 
            a_gt_b), 
        add_sub)
    z_sign = select(
        a_sign, 
        select(
            a_sign, 
            b_sign, 
            a_gt_b), 
        add_sub)
    z_exponent = a_exponent + 1

    #normalise
    lz = leading_zeros(z_mantissa)
    max_shift = z_exponent - minimum_exponent
    shift_amount = select(lz, max_shift, lz <= max_shift)
    z_mantissa = z_mantissa << shift_amount
    z_exponent = z_exponent - shift_amount
    
    #round
    z_mantissa = get_bits(z_mantissa, mbits+3, 4)
    g = get_bit(z_mantissa, 3)
    r = get_bit(z_mantissa, 2)
    s = get_bit(z_mantissa, 1) | get_bit(z_mantissa, 0)
    roundup = g & (round_bit | sticky | get_bit(z_mantissa, 0))
    z_exponent = select(z_exponent + 1, z_exponent, z_mantissa == 0xffffff)
    z_mantissa = z_mantissa + roundup

    #pack
    z_exponent(
        exponent-1, 
        z_exponent, 
        band(
            z_exponent == minimum_exponent,
            bnot(getbit(z_mantissa, mbits-1)))


Output("z", leading_zeros(Input(8, "a")))
print test(component, {'a':[0, 1, 3, 7, 15]})
print test(component, {'a':[0, 1, 2, 4, 8]})

pipeliner.component = Component()
div, rem = divide(Input(8, "a"), Input(8, "b"))
Output("d", div)
Output("r", rem)
print test(pipeliner.component, {'a':[12, 100, 35, 5], 'b':[4, 10, 35, 2]})
