import sys

sys.path.append("..")

from ip_generator.pipeliner import Input, Output, Component
from ip_generator.float import single_to_float, float_to_single
from ip_generator.float import double_to_float, float_to_double
import ip_generator.float
import ip_generator.pipeliner

# divider
div = Component()
Output(
    div,
    "div_z",
    float_to_single(
        single_to_float(Input(div, 32, "div_a"))
        / single_to_float(Input(div, 32, "div_b"))
    ),
)

# mul
mul = Component()
Output(
    mul,
    "mul_z",
    float_to_single(
        single_to_float(Input(mul, 32, "mul_a")).__mul__(
            single_to_float(Input(mul, 32, "mul_b")), mul
        )
    ),
)

# add
add = Component()
Output(
    add,
    "add_z",
    float_to_single(
        single_to_float(Input(add, 32, "add_a"))
        + single_to_float(Input(add, 32, "add_b"))
    ),
)

# max
single_max = Component()
Output(
    single_max,
    "single_max_z",
    float_to_single(
        single_to_float(Input(single_max, 32, "single_max_a")).max(
            single_to_float(Input(single_max, 32, "single_max_b"))
        )
    ),
)

# min
single_min = Component()
Output(
    single_min,
    "single_min_z",
    float_to_single(
        single_to_float(Input(single_min, 32, "single_min_a")).min(
            single_to_float(Input(single_min, 32, "single_min_b"))
        )
    ),
)

# sqrt
sqrt = Component()
Output(
    sqrt,
    "sqrt_z",
    float_to_single(single_to_float(Input(sqrt, 32, "sqrt_a")).sqrt(debug=sqrt)),
)

abs = Component()
Output(abs, "abs_z", float_to_single(single_to_float(Input(abs, 32, "abs_a")).abs()))

neg = Component()
Output(neg, "neg_z", float_to_single(single_to_float(Input(neg, 32, "neg_a")).neg()))

trunc = Component()
Output(
    trunc,
    "trunc_z",
    float_to_single(single_to_float(Input(trunc, 32, "trunc_a")).trunc(debug=trunc)),
)

ceil = Component()
Output(
    ceil,
    "ceil_z",
    float_to_single(single_to_float(Input(ceil, 32, "ceil_a")).ceil(debug=ceil)),
)

floor = Component()
Output(
    floor,
    "floor_z",
    float_to_single(single_to_float(Input(floor, 32, "floor_a")).floor(debug=floor)),
)

# gt
gt = Component()
Output(
    gt,
    "gt_z",
    single_to_float(Input(gt, 32, "gt_a")).__gt__(
        single_to_float(Input(gt, 32, "gt_b")), debug=gt
    ),
)

# lt
lt = Component()
Output(
    lt,
    "lt_z",
    single_to_float(Input(lt, 32, "lt_a")).__lt__(
        single_to_float(Input(lt, 32, "lt_b")), debug=lt
    ),
)

# le
le = Component()
Output(
    le,
    "le_z",
    single_to_float(Input(le, 32, "le_a")).__le__(
        single_to_float(Input(le, 32, "le_b")), debug=le
    ),
)

# ge
ge = Component()
Output(
    ge,
    "ge_z",
    single_to_float(Input(ge, 32, "ge_a")).__ge__(
        single_to_float(Input(ge, 32, "ge_b")), debug=ge
    ),
)

# eq
eq = Component()
Output(
    eq,
    "eq_z",
    single_to_float(Input(eq, 32, "eq_a")).__eq__(
        single_to_float(Input(eq, 32, "eq_b")), debug=eq
    ),
)

# ne
ne = Component()
Output(
    ne,
    "ne_z",
    single_to_float(Input(ne, 32, "ne_a")).__ne__(
        single_to_float(Input(ne, 32, "ne_b")), debug=ne
    ),
)

# float_to_int
single_to_int = Component()
Output(
    single_to_int,
    "single_to_int_z",
    single_to_float(Input(single_to_int, 32, "single_to_int_a")).to_int(),
)

# float_to_unsigned
single_to_unsigned_int = Component()
Output(
    single_to_unsigned_int,
    "single_to_unsigned_int_z",
    single_to_float(
        Input(single_to_unsigned_int, 32, "single_to_unsigned_int_a")
    ).to_unsigned(),
)

# int_to_float
int_to_single = Component()
Output(
    int_to_single,
    "int_to_single_z",
    float_to_single(
        ip_generator.float.int_to_float(Input(int_to_single, 32, "int_to_single_a"))
    ),
)

# unsigned_to_float
unsigned_int_to_single = Component()
Output(
    unsigned_int_to_single,
    "unsigned_int_to_single_z",
    float_to_single(
        ip_generator.float.unsigned_to_float(
            Input(unsigned_int_to_single, 32, "unsigned_int_to_single_a")
        )
    ),
)

# div
double_div = Component()
Output(
    double_div,
    "double_div_z",
    float_to_double(
        double_to_float(Input(double_div, 64, "double_div_a"))
        / double_to_float(Input(double_div, 64, "double_div_b"))
    ),
)

# mul
double_mul = Component()
Output(
    double_mul,
    "double_mul_z",
    float_to_double(
        double_to_float(Input(double_mul, 64, "double_mul_a")).__mul__(
            double_to_float(Input(double_mul, 64, "double_mul_b")), double_mul
        )
    ),
)

# add
double_add = Component()
Output(
    double_add,
    "double_add_z",
    float_to_double(
        double_to_float(Input(double_add, 64, "double_add_a"))
        + double_to_float(Input(double_add, 64, "double_add_b"))
    ),
)

# max
double_max = Component()
Output(
    double_max,
    "double_max_z",
    float_to_double(
        double_to_float(Input(double_max, 64, "double_max_a")).max(
            double_to_float(Input(double_max, 64, "double_max_b"))
        )
    ),
)

# min
double_min = Component()
Output(
    double_min,
    "double_min_z",
    float_to_double(
        double_to_float(Input(double_min, 64, "double_min_a")).min(
            double_to_float(Input(double_min, 64, "double_min_b"))
        )
    ),
)

# sqrt
double_sqrt = Component()
Output(
    double_sqrt,
    "double_sqrt_z",
    float_to_double(
        double_to_float(
            Input(double_sqrt, 64, "double_sqrt_a"), debug=double_sqrt
        ).sqrt(debug=double_sqrt)
    ),
)

double_abs = Component()
Output(
    double_abs,
    "double_abs_z",
    float_to_double(double_to_float(Input(double_abs, 64, "double_abs_a")).abs()),
)

double_neg = Component()
Output(
    double_neg,
    "double_neg_z",
    float_to_double(double_to_float(Input(double_neg, 64, "double_neg_a")).neg()),
)

double_trunc = Component()
Output(
    double_trunc,
    "double_trunc_z",
    float_to_double(
        double_to_float(Input(double_trunc, 64, "double_trunc_a")).trunc(
            debug=double_trunc
        )
    ),
)

double_ceil = Component()
Output(
    double_ceil,
    "double_ceil_z",
    float_to_double(
        double_to_float(Input(double_ceil, 64, "double_ceil_a")).ceil(debug=double_ceil)
    ),
)

double_floor = Component()
Output(
    double_floor,
    "double_floor_z",
    float_to_double(
        double_to_float(Input(double_floor, 64, "double_floor_a")).floor(
            debug=double_floor
        )
    ),
)

# gt
double_gt = Component()
Output(
    double_gt,
    "double_gt_z",
    double_to_float(Input(double_gt, 64, "double_gt_a")).__gt__(
        double_to_float(Input(double_gt, 64, "double_gt_b")), debug=double_gt
    ),
)

# lt
double_lt = Component()
Output(
    double_lt,
    "double_lt_z",
    double_to_float(Input(double_lt, 64, "double_lt_a")).__lt__(
        double_to_float(Input(double_lt, 64, "double_lt_b")), debug=double_lt
    ),
)

# le
double_le = Component()
Output(
    double_le,
    "double_le_z",
    double_to_float(Input(double_le, 64, "double_le_a")).__le__(
        double_to_float(Input(double_le, 64, "double_le_b")), debug=double_le
    ),
)

# ge
double_ge = Component()
Output(
    double_ge,
    "double_ge_z",
    double_to_float(Input(double_ge, 64, "double_ge_a")).__ge__(
        double_to_float(Input(double_ge, 64, "double_ge_b")), debug=double_ge
    ),
)

# eq
double_eq = Component()
Output(
    double_eq,
    "double_eq_z",
    double_to_float(Input(double_eq, 64, "double_eq_a")).__eq__(
        double_to_float(Input(double_eq, 64, "double_eq_b")), debug=double_eq
    ),
)

# ne
double_ne = Component()
Output(
    double_ne,
    "double_ne_z",
    double_to_float(Input(double_ne, 64, "double_ne_a")).__ne__(
        double_to_float(Input(double_ne, 64, "double_ne_b")), debug=double_ne
    ),
)

# float_to_int
double_to_int = Component()
Output(
    double_to_int,
    "double_to_int_z",
    double_to_float(Input(double_to_int, 64, "double_to_int_a")).to_int(64),
)

# float_to_unsigned
double_to_unsigned_int = Component()
Output(
    double_to_unsigned_int,
    "double_to_unsigned_int_z",
    double_to_float(
        Input(double_to_unsigned_int, 64, "double_to_unsigned_int_a")
    ).to_unsigned(64),
)

# int_to_float
int_to_double = Component()
Output(
    int_to_double,
    "int_to_double_z",
    float_to_double(
        ip_generator.float.int_to_float(
            Input(int_to_double, 64, "int_to_double_a"), 11, 53
        )
    ),
)

# unsigned_to_float
unsigned_int_to_double = Component()
Output(
    unsigned_int_to_double,
    "unsigned_int_to_double_z",
    float_to_double(
        ip_generator.float.unsigned_to_float(
            Input(unsigned_int_to_double, 64, "unsigned_int_to_double_a"), 11, 53
        )
    ),
)

# mul
complex_mul = Component()
real_in_a = single_to_float(Input(complex_mul, 32, "real_in_a"))
real_in_b = single_to_float(Input(complex_mul, 32, "real_in_b"))
imag_in_a = single_to_float(Input(complex_mul, 32, "imag_in_a"))
imag_in_b = single_to_float(Input(complex_mul, 32, "imag_in_b"))
Output(
    complex_mul,
    "real_out",
    float_to_single(real_in_a * real_in_b + imag_in_a + imag_in_b),
)
Output(
    complex_mul,
    "imag_out",
    float_to_single(real_in_a * real_in_b + imag_in_a + imag_in_b),
)
