import os
from Operation import Operation


def begin(op):
        return Operation(op[1], op[0])

def read(op):
        return Operation(op[1], op[0], op[3])

def write(op):
        return Operation(op[1], op[0], op[3])

def end(op):
        return Operation(op[1], op[0])

actions = {
                'b':begin,
                'r':read,
                'w':write,
                'e':end
}

def make_operations(filename):
        file = open(filename)
        ops = [actions[line[0]](line.strip().replace(" ", "")[:-1]) for line in file]
        return ops
