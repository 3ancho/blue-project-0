#!/usr/bin/env python
import numpy as np
import sys
import re

# TO-DO use OO
# TO-TO use argparse

class InputFormatError(IOError):
    """User defined Exception for formatting errors"""
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return repr(self.message)

class MatrixNotInvertibleError(RuntimeError):
    """User defined Exception for RuntimeErrors"""
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return repr(self.message)
        
def parse_array(raw_data):
    """87.6549491771;59.8682503025;52.3886621673;44.5125050557;67.4679478072\n"""
    b = []
    a = []
    last = None
    first_row = True
    length = 0
    re_split = re.split
    for row in raw_data:
        a_row = re_split(r"\s*;\s*", row)
        last = a_row[len(a_row) - 1]    # this handles the trailing delimiter
        if not last: a_row.remove(last)
        # a_row -> ["1","2","3","4"]
        b.append(a_row.pop(len(a_row)-1))
        a.append(a_row)
        if first_row:
            first_row = False
            length = len(a_row)
        elif length != len(a_row):
            raise InputFormatError("Matrix row size error")
        
    if len(a) != len(a[0]):
        sys.stderr.write("Matrix size error\n") 
        sys.exit(1)

    return a, b
    # two dimentinal python list a, b

def solve(a, b, p = False):
    try:
        x = np.linalg.solve(a, b)
    except ValueError:
        raise InputFormatError("Matrix value format error")
    except np.linalg.linalg.LinAlgError:
        raise MatrixNotInvertibleError("Matrix singular error, no sulution")
    if p:
        for i in range(x.size):
            print '%6.3f' % x.item(i)

def main():
    global test_raw_data, raw_A, raw_b
    N = 10

    if len(sys.argv) > 1:
        if sys.argv[1] == "cProfile":
            if len(sys.argv) > 2:
                N = int(sys.argv[2])
            import cProfile
            from generate import generate2

            # First Generate the data 
            test_raw_data = generate2(N) # replace this with the one from professor

            # Then test 

            # 1. get profile
            cProfile.runctx("parse_array(test_raw_data)", globals(), locals())

            # 2. the actual run
            raw_A, raw_b = parse_array(test_raw_data)
            raw_b = raw_b * -1

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
                from generate import generate2
                test_raw_data = generate2(i) # replace this with the one from professor

                # Then test 

                # 1. get profile
                parse_time = Timer("parse_array(test_raw_data)", 
                      "from __main__ import parse_array, test_raw_data").timeit(10)

                # 2. the actual run
                raw_A, raw_b = parse_array(test_raw_data)

                # 1. get profile
                solve_time = Timer("solve(raw_A, raw_b)", 
                      "from __main__ import solve, raw_A, raw_b").timeit(10)
                # 2. the actual run
                solve(raw_A, raw_b)

                print "%3d, %8f, %8f" % (i, parse_time, solve_time)
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
