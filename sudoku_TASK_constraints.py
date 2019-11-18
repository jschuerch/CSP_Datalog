# -*- coding: utf-8 -*-
"""
Created on Wed Jan 04 08:13:32 2017

Formulates sudoku as a CSP, solving the riddle from
https://www.sudoku.ws/hard-1.htm as an example.

@author: stdm
@modif: tugg
"""

import sys
sys.path.append("./python-constraint-1.2")
import constraint as csp
import numpy as np
import time

# ------------------------------------------------------------------------------
# sudoku to solve (add "0" where no number is given)
# ------------------------------------------------------------------------------
riddle_default = [[0,0,0,2,0,0,0,6,3],
             [3,0,0,0,0,5,4,0,1],
             [0,0,1,0,0,3,9,8,0],
             [0,0,0,0,0,0,0,9,0],
             [0,0,0,5,3,8,0,0,0],
             [0,3,0,0,0,0,0,0,0],
             [0,2,6,3,0,0,5,0,0],
             [5,0,3,7,0,0,0,0,8],
             [4,7,0,0,0,1,0,0,0]]
riddle = [[8,0,0,0,0,0,0,0,0],
          [0,0,3,6,0,0,0,0,0],
          [0,7,0,0,9,0,2,0,0],
          [0,5,0,0,0,7,0,0,0],
          [0,0,0,0,4,5,7,0,0],
          [0,0,0,1,0,0,0,3,0],
          [0,0,1,0,0,0,0,6,8],
          [0,0,8,5,0,0,0,1,0],
          [0,9,0,0,0,0,4,0,0]]
"""riddle_nur_eis_leer = [[5,3,4,6,7,8,9,1,2],
          [6,7,2,1,9,5,3,4,8],
          [1,9,8,3,4,2,5,6,7],
          [8,5,9,7,6,1,4,2,3],
          [4,2,6,8,5,3,7,9,1],
          [7,1,3,9,2,4,8,5,6],
          [9,6,1,5,3,7,2,8,4],
          [2,8,7,4,1,9,6,3,5],
          [3,4,5,2,8,6,1,7,0]]"""

# ------------------------------------------------------------------------------
# create helpful lists of variable names
# ------------------------------------------------------------------------------
rownames = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]
colnames = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
domains = list(range(1,10))

rows = []
for i in rownames:
    row = []
    for j in colnames:
        row.append(i+j)
    rows.append(row)

cols = []
for j in colnames:
    col = []
    for i in rownames:
        col.append(i+j)
    cols.append(col)

boxes = []
for x in range(3):  # over rows of boxes
    for y in range(3):  # over columns of boxes
        box = []
        for i in range(3):  # over variables in rows (in a box)
            for j in range(3):  # over variables in cols (in a box)
                box.append(rownames[x*3 + i] + colnames[y*3 + j])
        boxes.append(box)


# ------------------------------------------------------------------------------
# formulate sudoku as CSP
# ------------------------------------------------------------------------------
iterations = 1
start = time.time()
for i in range(iterations):

    sudoku = csp.Problem()
    sudoku.addVariables([i + j for i in rownames for j in colnames], domains)

    for index, x in np.ndenumerate(riddle):
        if x != 0:
            sudoku.addConstraint(lambda a, x = x: a == x, [str(rownames[index[0]] + colnames[index[1]])])

    for i in range(9):
        sudoku.addConstraint(csp.AllDifferentConstraint(), rows[i])
        sudoku.addConstraint(csp.AllDifferentConstraint(), cols[i])
        sudoku.addConstraint(csp.AllDifferentConstraint(), boxes[i])

    # ------------------------------------------------------------------------------
    # solve CSP
    # ------------------------------------------------------------------------------
    solutions = sudoku.getSolutions()

duration = time.time() - start
print("Average time (%d iterations): %f seconds" % (iterations, (duration/iterations)))

for solution in solutions:
    print("===============================")
    i = 0
    for row in rows:
        i += 1
        print("| %d  %d  %d | %d  %d  %d | %d  %d  %d |" % tuple(solution[x] for x in row))
        if i % 3 == 0 and i < 9:
            print("|---------|---------|---------|")
    print("===============================\n")

