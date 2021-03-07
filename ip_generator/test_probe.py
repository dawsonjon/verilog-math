from .pipeliner import *

probes = []
sn = 0


def test_probe(pipe, label):
    global sn, probes
    print("probe", pipe, label)
    probes.append(label + str(sn))
    Output(label + str(sn), pipe)
    sn += 1


def trace(response, n):
    global probes
    for i in probes:
        if i in response:
            print(i, ":", response[i][n])
