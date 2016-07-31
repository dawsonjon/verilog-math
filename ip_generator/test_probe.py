from pipeliner import Output

test_probes = []
sn = 0

def test_probe(signal, name):
    global sn
    name = name + str(sn)
    Output(name, signal)
    test_probes.append(name)
    sn+=1

def trace(responses, n=None):
    print responses
    for test_probe in test_probes:
        if n is not None:
            print test_probe, responses[test_probe][n]
        else:
            print test_probe, responses[test_probe]
