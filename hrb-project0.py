#!/usr/bin/env python
import numpy as np
import sys
import re
from generate import generate, generate2
import time

## depreciated 
#def parse(raw_data):
#    b = []
#    a = []
#    re_split = re.split
#    for row in raw_data:
#        a_row = re_split(r"\s*;\s*", row)
#        b.append(a_row.pop(len(a_row)-1))
#        a.append(" ".join(a_row))
#    
#    a = ";".join(a)
#    b = ";".join(b)
#    return a, b
#
## depreciated
#def create(a, b):
#    # join the list with ";" (that's what numpy looking for)
#    try:
#        a = np.matrix(a)
#        # Check if matrix is N by N+1
#        if a.shape[0] != a.shape[1]:
#            print "Matrix shape error"
#            sys.exit(1)
#        
#        b = np.matrix(b)
#        return a, b
#    except SyntaxError:
#        print "your matrix doesn't look right!"

def parse_array(raw_data):
    """87.6549491771;59.8682503025;52.3886621673;44.5125050557;67.4679478072\n"""
    start = time.time()
    b = []
    a = []
    first_row = True
    length = 0
    re_split = re.split
    for row in raw_data:
        a_row = re_split(r"\s*;\s*", row)
        # a_row -> ["1","2","3","4"]
        b.append(a_row.pop(len(a_row)-1))
        a.append(a_row)
        if first_row:
            first_row = False
            length = len(a_row)
        elif length != len(a_row):
            print "Matrix row size error"
            sys.exit(1)
        
    if len(a) != len(a[0]):
        print "Matrix size error"
        sys.exit(1)

    print "parse_array(): ", str(time.time() - start)
    return a, b
    # two dimentinal python list a, b

def create_array(a, b):
    start = time.time()
    array_a = np.array(a)
    array_b = np.array(b)
    print "create_array(): ", str(time.time() - start)
    return array_a, array_b 

def solve(a, b, p = False):
    start = time.time()
    try:
        x = np.linalg.solve(a, b)
    except ValueError:
        print "Matrix value error"
        sys.exit(1)
    except np.linalg.linalg.LinAlgError:
        print "There is no solution"
        sys.exit(0)

    if p:
        for i in range(x.size):
            print '%6.3f' % x.item(i)
    print "solve(): ", str(time.time() - start)

def test():
    global test_raw_data
    raw_A, raw_b = parse_array(test_raw_data)
    A, b = create_array(raw_A, raw_b)
    solve(A, b)

def main():
    global test_raw_data
    TIME_TO_TEST = 10

    if len(sys.argv) > 1:
        if sys.argv[1] == "test":
            if len(sys.argv) > 2:
                TIME_TO_TEST = int(sys.argv[2])
            from timeit import Timer
            import cProfile
            for i in xrange(1, TIME_TO_TEST):
                # First Generate the data 
                test_raw_data = generate2(i)
                # Then test 
                cProfile.runctx("parse_array(test_raw_data)", globals(), locals())
                raw_A, raw_b = parse_array(test_raw_data)

                cProfile.runctx("solve(raw_A, raw_b)", globals(), locals())
                solve(raw_A, raw_b)
                
                
                print "{0} {1}".format(str(i).ljust(8), str(t.timeit(1)).ljust(8))
        else:
            print "option error"
        # Testing block ends
    else:
        raw_data = sys.stdin.readlines()
        raw_A, raw_b = parse_array(raw_data)

        solve(raw_A, raw_b, True)

if __name__ == "__main__":
    main()
