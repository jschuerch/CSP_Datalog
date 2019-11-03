from pyDatalog import pyDatalog
import pandas as pd
import math

pyDatalog.create_terms('X,Y')

print(X==1)
print((X==True) & (Y==False))

#print((X==raw_input('Please enter your name : ')) & (Y=='Hello ' + X[0]))

print((X==(1,2)+(3,)) & (Y==X[2]))

def twice(a):
    return a+a

pyDatalog.create_terms('twice')
print((X==1) & (Y==twice(X)))


pyDatalog.create_terms('math')
print((X==2) & (Y==math.sqrt(X)))
