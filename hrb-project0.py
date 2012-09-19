#!/usr/bin/env python
import numpy as np
import sys
import re
from generate import generate, generate2
import time

def parse_array(raw_data):
    """87.6549491771;59.8682503025;52.3886621673;44.5125050557;67.4679478072\n"""
    # TO-DO, handle trailing delimiter
    b = []
    a = []
    last = None
    first_row = True
    length = 0
    re_split = re.split
    for row in raw_data:
        a_row = re_split(r"\s*;\s*", row)
        last = a_row[len(a_row) - 1]
        if not last: a_row.remove(last)
        print a_row
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

    return a, b
    # two dimentinal python list a, b

def create_array(a, b):
    array_a = np.array(a)
    array_b = np.array(b)
    return array_a, array_b 

def solve(a, b, p = False):
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

def test():
    global test_raw_data
    raw_A, raw_b = parse_array(test_raw_data)
    A, b = create_array(raw_A, raw_b)
    solve(A, b)

def main():
    global test_raw_data, raw_A, raw_b
    N = 10

    if len(sys.argv) > 1:
        if sys.argv[1] == "cProfile":
            if len(sys.argv) > 2:
                N = int(sys.argv[2])
            import cProfile

            # First Generate the data 
            test_raw_data = generate2(N) # replace this with the one from professor

            # Then test 

            # 1. get profile
            cProfile.runctx("parse_array(test_raw_data)", globals(), locals())

            # 2. the actual run
            raw_A, raw_b = parse_array(test_raw_data)

            # 1. get profile
            cProfile.runctx("solve(raw_A, raw_b)", globals(), locals())
            # 2. the actual run
            solve(raw_A, raw_b)
        # end of cProfile

        if sys.argv[1] == "timeit":
            from timeit import Timer

            if len(sys.argv) > 2: N = int(sys.argv[2])

            # the size of marix will increase from 1 to N
            for i in xrange(1, N):
                # First Generate the data 
                test_raw_data = generate2(i) # replace this with the one from professor

                # Then test 

                # 1. get profile
                parse_time = Timer("parse_array(test_raw_data)", 
                      "from __main__ import parse_array, test_raw_data").timeit(1)

                # 2. the actual run
                raw_A, raw_b = parse_array(test_raw_data)

                # 1. get profile
                solve_time = Timer("solve(raw_A, raw_b)", 
                      "from __main__ import solve, raw_A, raw_b").timeit(1)
                # 2. the actual run
                solve(raw_A, raw_b)

                print "%d    %f    %f" % (i, parse_time, solve_time)
            # end of Timeit
        else:
            print "hrb-project0.py [cProfile N | timeit N]"
    # Testing block ends

    # non-testing mode
    else: 
        raw_data = sys.stdin.readlines()
        raw_A, raw_b = parse_array(raw_data)
        solve(raw_A, raw_b, True)

if __name__ == "__main__":
    main()
