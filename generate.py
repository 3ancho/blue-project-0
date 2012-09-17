#!/usr/bin/env python
import random, sys

def generate(m=10):
    matrix = []
    for i in range(m):
        matrix.append(";".join([ str(random.random()+random.randint(0,100)) for i in range(m+1)]))
    matrix = "\n".join(matrix)
    return matrix

def generate2(m=10):
    matrix = []
    for i in range(m):
        matrix.append(";".join([ str(random.random()+random.randint(0,100)) for i in range(m+1)]))
    return matrix

if __name__ == "__main__":
    m = len(sys.argv) > 1 and int(sys.argv[1]) or 10
    print generate(m)
