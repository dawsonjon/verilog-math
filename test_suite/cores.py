import sys
sys.path.append("..")

from ip_generator.pipeliner import Input, Output, Component
from ip_generator.float import single_to_float, float_to_single, int_to_float
import ip_generator.pipeliner

#divider
ip_generator.pipeliner.component = Component()
Output('div_z', 
    float_to_single(
        single_to_float(Input(32, 'div_a')) 
        / 
        single_to_float(Input(32, 'div_b'))
    )
)
div = ip_generator.pipeliner.component

#mul
ip_generator.pipeliner.component = Component()
Output('mul_z', 
    float_to_single(
        single_to_float(Input(32, 'mul_a')) 
        * 
        single_to_float(Input(32, 'mul_b'))
    )
)
mul = ip_generator.pipeliner.component

#add
ip_generator.pipeliner.component = Component()
Output('add_z', 
    float_to_single(
        single_to_float(Input(32, 'add_a')) 
        + 
        single_to_float(Input(32, 'add_b'))
    )
)
add = ip_generator.pipeliner.component

#float_to_int
ip_generator.pipeliner.component = Component()
Output('to_int_z', 
    single_to_float(
        Input(32, 'to_int_a')
    ).to_int()
)
to_int = ip_generator.pipeliner.component

#int_to_float
ip_generator.pipeliner.component = Component()
Output('to_float_z', 
    float_to_single(
        int_to_float(
            Input(32, 'to_float_a')
        )
    )
)
to_float = ip_generator.pipeliner.component