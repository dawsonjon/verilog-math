import sys
sys.path.append("..")

from ip_generator.pipeliner import Input, Output, Component
from ip_generator.float import single_to_float, float_to_single, int_to_float
from ip_generator.float import double_to_float, float_to_double
import ip_generator.pipeliner

#divider
div = Component()
Output(div, 'div_z', 
    float_to_single(
        single_to_float(Input(div, 32, 'div_a')) 
        / 
        single_to_float(Input(div, 32, 'div_b'))
    )
)

#mul
mul = Component()
Output(mul, 'mul_z', 
    float_to_single(
        single_to_float(Input(mul, 32, 'mul_a')) 
        * 
        single_to_float(Input(mul, 32, 'mul_b'))
    )
)

#add
add = Component()
Output(add, 'add_z', 
    float_to_single(
        single_to_float(Input(add, 32, 'add_a')) 
        + 
        single_to_float(Input(add, 32, 'add_b'))
    )
)

#sqrt
sqrt = Component()
Output(sqrt, 'sqrt_z', 
    float_to_single(
        single_to_float(Input(sqrt, 32, 'sqrt_a'), debug=sqrt).sqrt(debug=sqrt)
    )
)

#gt
gt = Component()
Output(gt, 'gt_z', 
    single_to_float(Input(gt, 32, 'gt_a')).__gt__(
    single_to_float(Input(gt, 32, 'gt_b')), debug=gt)
)

#lt
lt = Component()
Output(lt, 'lt_z', 
    single_to_float(Input(lt, 32, 'lt_a')).__lt__(
    single_to_float(Input(lt, 32, 'lt_b')), debug=lt)
)

#le
le = Component()
Output(le, 'le_z', 
    single_to_float(Input(le, 32, 'le_a')).__le__(
    single_to_float(Input(le, 32, 'le_b')), debug=le)
)

#ge
ge = Component()
Output(ge, 'ge_z', 
    single_to_float(Input(ge, 32, 'ge_a')).__ge__(
    single_to_float(Input(ge, 32, 'ge_b')), debug=ge)
)

#eq
eq = Component()
Output(eq, 'eq_z', 
    single_to_float(Input(eq, 32, 'eq_a')).__eq__(
    single_to_float(Input(eq, 32, 'eq_b')), debug=eq)
)

#ne
ne = Component()
Output(ne, 'ne_z', 
    single_to_float(Input(ne, 32, 'ne_a')).__ne__(
    single_to_float(Input(ne, 32, 'ne_b')), debug=ne)
)

#float_to_int
to_int = Component()
Output(to_int, 'to_int_z', 
    single_to_float(
        Input(to_int, 32, 'to_int_a')
    ).to_int()
)

#int_to_float
to_float = Component()
Output(to_float, 'to_float_z', 
    float_to_single(
        int_to_float(
            Input(to_float, 32, 'to_float_a')
        )
    )
)

#div
double_div = Component()
Output(double_div, 'double_div_z', 
    float_to_double(
        double_to_float(Input(double_div, 64, 'double_div_a')) 
        / 
        double_to_float(Input(double_div, 64, 'double_div_b'))
    )
)

#mul
double_mul = Component()
Output(double_mul, 'double_mul_z', 
    float_to_double(
        double_to_float(Input(double_mul, 64, 'double_mul_a')) 
        * 
        double_to_float(Input(double_mul, 64, 'double_mul_b'))
    )
)

#add
double_add = Component()
Output(double_add, 'double_add_z', 
    float_to_double(
        double_to_float(Input(double_add, 64, 'double_add_a')) 
        + 
        double_to_float(Input(double_add, 64, 'double_add_b'))
    )
)
