import sys
sys.path.append("..")

from ip_generator.pipeliner import *
import ip_generator.pipeliner
import ip_generator.float
trace = ip_generator.test_probe.trace
Component = ip_generator.pipeliner.Component

def leading_zeros(x):
    if x.bits == 2:
        return cat(~x[1] & ~x[0], ~x[1] & x[0])
    else:

        next_power_2 = 0
        while 2**next_power_2 < x.bits:
            next_power_2 += 1

        while x.bits < 2**next_power_2:
            x = cat(x, Constant(1, 1))

        msbs, lsbs = x[x.bits-1:x.bits//2], x[x.bits//2-1:0]
        Output("msb", msbs)
        Output("lsb", lsbs)
        lsb_zeros = leading_zeros(lsbs)
        msb_zeros = leading_zeros(msbs)

        lsbs_are_zero = lsb_zeros[lsb_zeros.bits-1]
        msbs_are_zero = msb_zeros[msb_zeros.bits-1]
        Output("msbs_are_zero", msbs_are_zero)
        Output("lsbs_are_zero", lsbs_are_zero)
        lsb_zeros = lsb_zeros[lsb_zeros.bits-2:0]
        msb_zeros = msb_zeros[msb_zeros.bits-2:0]
            
        return cat(
            msbs_are_zero & lsbs_are_zero, 
            cat(
                msbs_are_zero & ~lsbs_are_zero,
                select(
                    lsb_zeros,
                    msb_zeros,
                    msbs_are_zero
                )
            )
        )

ip_generator.pipeliner.component = Component()
#Output('z', ip_generator.float.leading_zeros(Input(4, 'a')))
Output('z', leading_zeros(Input(3, 'a')))



stimulus = {"a":[0, 1, 2, 3]}

response = ip_generator.pipeliner.component.test(stimulus, name="lz")

print response
