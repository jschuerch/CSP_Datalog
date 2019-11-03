from pyDatalog import pyDatalog
import pandas as pd
import math

from pyDatalog import pyDatalog
pyDatalog.create_terms('X,Y,Z')
"""

# give me all the X so that X is in the range 0..4
print(X.in_((0,1,2,3,4)))

print()

# here is the procedural equivalent
for x in range(5):
    print (x)

print(X.in_(range(5)).data)
print(X.in_(range(5)) == set([(0,), (1,), (2,), (3,), (4,)]))
"""
X.in_(range(5))
#X.in_((4,3,2,1,0))

print("Data : ",X.data)
print("First value : ",  X.v())
# below, '>=' is a variable extraction operator
print("Extraction of first value of X: ", X.in_(range(5)) >= X)


# give me all X in range 0..4 that are below 2
print(X.in_(range(5)) & (X<4))

# give me all X, Y and Z so that X and Y are in 0..4, Z is their sum, and Z is below 3
"""
print(X.in_(range(5)) &
          Y.in_(range(5)) &
              (Z==X+Y) &
              (Z<3))
"""

print(X.in_(range(5)) & Y.in_(range(5)))


