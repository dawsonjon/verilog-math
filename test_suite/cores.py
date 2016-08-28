import sys
sys.path.append("..")

from ip_generator.pipeliner import Input, Output, Component
from ip_generator.float import single_to_float, float_to_single, int_to_float
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
