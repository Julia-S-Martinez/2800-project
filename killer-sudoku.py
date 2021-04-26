#!/usr/bin/env python3
import sys
import json
from z3 import *
import argparse


"""
-----------
00 01 02 03
10 11 12 13
20 21 22 23
30 31 32 33
-----------
"""

parser = argparse.ArgumentParser(description='take input for solver')
parser.add_argument('--file_path', help='json filepath for solver setup')
args = parser.parse_args()

#initialization of variables
BOARD_FILE_PATH = args.file_path
LENGTH = 0
data = []
board = []
boxes = []
s = Solver()

# represents a box of cells w/ a given total sum
class Box:
    def __init__(self, cells, sum):
        self.cells = cells
        self.sum = sum

try:
    # parse JSON board file
    with open(BOARD_FILE_PATH) as f:
        data = json.load(f)
except:
    print("Could not open and load expected JSON file {}".format(BOARD_FILE_PATH))
    sys.exit()

try:
    LENGTH = data["length"]
    if not isinstance(LENGTH, int):
        print("LENGTH should be int, is instead {}".format(type(LENGTH)))
        sys.exit()
except KeyError:
    print("Bad input file {}: missing 'length' keyword".format(BOARD_FILE_PATH))
    sys.exit()

# init board
for r in range(LENGTH):
    board.append([])        #list for each row

    # initialize cells as z3 Int types
    for c in range(LENGTH):
        board[r].append(Int('{}{}'.format(r, c)))  # every item is an integer
        # every item is > 0 and <= length
        s.add(And(board[r][c] > 0, board[r][c] <= LENGTH))

#add disctinction rules to verify that there are no repeated values in each row and column
for r in range(LENGTH):
    # every item in a row is distinct
    d = Distinct([board[r][c] for c in range(LENGTH)])
    # every item in a column is distinct
    dc = Distinct([board[c][r] for c in range(LENGTH)])
    s.add(d)
    s.add(dc)


# setup sum boxes
# ok to not have boxes
try:
    for b in data["boxes"]:
        try:
            cells = b["cells"]
            sum = b["sum"]
            if (not isinstance(cells, list)) or (not isinstance(sum, int)):
                print("Cells and sum for {} should be list and int, are instead {} and {}".format(b, type(cells), type(sum)))
                pass
            else:
                box = Box(b["cells"], b["sum"])
                boxes.append(box)
        except KeyError:
            print("Box {} was malformed when trying to read; continuing without it".format(b))
            pass
except KeyError:
    pass

#add rules to z3 solver based on the sums of each box
def sumboxes():
    for b in boxes:
        cells = b.cells
        sum = Sum([board[cells[c][0]][cells[c][1]] for c in range(len(cells))])
        s.add(sum == b.sum)


sumboxes()

sat = s.check()  # checks for satisfiability
if sat == z3.sat:
    res = s.model()
    #pretty print to see the values as they would be on a board
    for r in range(LENGTH):
        print('\n')
        for c in range(LENGTH):
            print('{} \t'.format(res[board[r][c]]), end =' ')
    #print(res)  # prints model if sat
else:
    print(sat)  # prints sat value if unsat
