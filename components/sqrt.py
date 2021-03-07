import sys

sys.path.append("..")

from ip_generator.pipeliner import *

st = Component()
Output(st, "z", sqrt_rounded(Input(st, 51, "a")))

stimulus = {"a": [447109115412480]}
response = st.test(stimulus)
for a, actual in zip(stimulus["a"], response["z"]):
    print(a, actual, math.sqrt(a))
