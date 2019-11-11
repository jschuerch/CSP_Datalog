#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 14:38:21 2017

@author: tugg
update: vissejul, bachmdo2, stdm (Nov 27, 2018)
"""
import pandas as pa
from pyDatalog import pyDatalog

# ---------------------------------------------------------------------------
# Social graph analysis:
# work through this code from top to bottom (in the way you would use a R or Jupyter notebook as well...) and write datalog clauses
# and python code in order to solve the respective tasks. Overall, there are 7 tasks.
# ---------------------------------------------------------------------------
calls = pa.read_csv('calls.csv', sep='\t', encoding='utf-8')
texts = pa.read_csv('texts.csv', sep='\t', encoding='utf-8')

suspect = 'Quandt Katarina'
company_Board = ['Soltau Kristine', 'Eder Eva', 'Michael Jill']

pyDatalog.create_terms('knows','has_link','many_more_needed')
pyDatalog.clear()

# First, treat calls as simple social links (denoted as knows), that have no date
for i in range(0,50):
    +knows(calls.iloc[i,1], calls.iloc[i,2])


# Task 1: Knowing someone is a bi-directional relationship -> define the predicate accordingly
pyDatalog.create_terms('X, Y')
knows(X, Y) <= knows(Y, X)

# ze output
#print("%s knows Y" % (suspect))
#print(knows(suspect, Y))

# Task 2: Define the predicate has_link in a way that it is true if a connection exists (path of people knowing the next link)
pyDatalog.create_terms('Z')
has_link(X,Y) <= knows(X,Y)
has_link(X,Y) <= knows(X,Z) & has_link(Z,Y) & (X!=Y)

#print (has_link(suspect,Y))

# Hints:
#   check if your predicate works: at least 1 of the following asserts should be true (2 if you read in all 150 communication records)
#   (be aware of the unusual behaviour that if an assert evaluates as true, an exception is thrown)
#assert (has_link('Quandt Katarina', company_Board[0]) == ()) # --> false []
#assert (has_link('Quandt Katarina', company_Board[1]) == ()) # --> true  [()]
#assert (has_link('Quandt Katarina', company_Board[2]) == ()) # --> true  [()]


# Task 3: You already know that a connection exists; now find the concrete paths between the board members and the suspect
# Hints:
#   if a knows b, there is a path between a and b
#   (X._not_in(P2)) is used to check whether x is not in path P2
#   (P==P2+[Z]) declares P as a new path containing P2 and Z

pyDatalog.create_terms('paths, P, P2')

# The most general definition of the function is given first.
# When searching for possible answers, pyDatalog begins with the last rule defined,
# i.e. the more specific, and stops as soon as a valid answer is found for the function.
# --> umgekehrt wie in prolog?

#paths(X,Y,P) <= paths(X,Z,P2) & knows(Z,Y) & (X!=Y) & Z._not_in(P2) & (P==P2 + [Z]) # für paths isch das gange, aber für with len nöd...
#vode hilfsssite... ?? werum X und Y nöd in P2?? paths(X, Y, P) <= paths(X, Z, P2) & knows(Z, Y) & (X != Y) & (X._not_in(P2)) & (Y._not_in(P2)) & (P == P2 + [Z])

paths(X,Y,P) <= paths(X,Z,P2) & knows(Z,Y) & (X!=Y) & Y._not_in(P2) & Z._not_in(P2) & (P==P2 + [Z])
paths(X,Y,P) <= knows(X,Y) & (P==[])

# ze output
"""for i in range(0,len(company_Board)):
    print(company_Board[i])
    print(paths(suspect, company_Board[i], P))"""

# Task 4: There are too many paths. We are only interested in short paths.
# Find all the paths between the suspect and the company board that contain five people or less
pyDatalog.create_terms('paths_with_len, L, L2')

#paths_with_len(X,Y,P,L) <= knows(X,Y) & paths_with_len(Z,Y,P2,L2) & (X!=Y) & Z._not_in(P2) & (P==[Z] + P2) & (L==L2 + 1) # gaht nöd?? :(
#paths_with_len(X,Y,P,L) <= paths_with_len(X,Z,P2,L2) & knows(Z,Y) & (X!=Y) & X._not_in(P2) & Y._not_in(P2) & (P==P2 + [Z]) & (L==L2 + 1) # wenis übernimm

paths_with_len(X,Y,P,L) <= paths_with_len(X,Z,P2,L2) & knows(Z,Y) & (X!=Y) & Y._not_in(P2) & Z._not_in(P2) & (P==P2 + [Z]) & (L==L2 + 1)
paths_with_len(X,Y,P,L) <= knows(X,Y) & (P==[]) & (L==0)

# ze output
"""for i in range(0,len(company_Board)):
    print(company_Board[i])
    print(paths_with_len(suspect, company_Board[i], P, L) & (L<=5))"""

# ---------------------------------------------------------------------------
# Call-Data analysis:
# Now we use the text and the calls data together with their corresponding dates
# ---------------------------------------------------------------------------
date_board_decision = '12.2.2017'
date_shares_bought = '23.2.2017'
pyDatalog.create_terms('called,texted')
pyDatalog.clear()

for i in range(0,50): # calls
    +called(calls.iloc[i,1], calls.iloc[i,2],calls.iloc[i,3])

for i in range(0,50): # texts
    +texted(texts.iloc[i,1], texts.iloc[i,2],texts.iloc[i,3])

called(X,Y,Z) <= called(Y,X,Z) # calls are bi-directional



# Task 5: Again we are interested in links, but this time a connection is only valid if the links are descending in date; 
#         find out who could have actually sent the information by adding this new restriction
# Hints:
#   You are allowed to naively compare the dates lexicographically using ">" and "<";
#   it works in this example (but is evil in general)
pyDatalog.create_terms('A, Z1, Z2')

has_link(X,Y,Z) <= texted(X,Y,Z)
#has_link(X,Y,Z) <= called(X,Y,Z)
has_link(X,Y,Z) <= texted(X,A,Z) & has_link(A,Y,Z2) & (X!=Y) & (Z<Z2)
#has_link(X,Y,Z) <= called(X,A,Z) & has_link(A,Y,Z2) & (X!=Y) & (Z<Z2)

print (has_link(suspect,Y,Z))

# Task 6: Find all the communication paths that lead to the suspect (with the restriction that the dates have to be ordered correctly)

paths_with_len(X,Y,Z,P,L) <= paths_with_len(X,A,Z,P2,L2) & texted(A,Y,Z2) & (X!=Y) & (Z<Z2) & Y._not_in(P2) & A._not_in(P2) & (P==P2 + [A] + [Z2]) & (L==L2 + 1)
#paths_with_len(X,Y,Z,P,L) <= paths_with_len(X,A,Z,P2,L2) & called(A,Y,Z2) & (X!=Y) & (Z<Z2) & Y._not_in(P2) & A._not_in(P2) & (P==P2 + [A] + [Z2]) & (L==L2 + 1)
paths_with_len(X,Y,Z,P,L) <= texted(X,Y,Z) & (P==[]) & (L==0)
#paths_with_len(X,Y,Z,P,L) <= called(X,Y,Z) & (P==[]) & (L==0)

print("\n\nSuspicious Trace:")
# ze output
for i in range(0,len(company_Board)):
    print()
    print(company_Board[i])
    print(paths_with_len(suspect, company_Board[i], Z, P, L))


# Final task: after seeing this information, who, if anybody, do you think gave a tip to the suspect?


"""
Das isch ez mit je 25 wills so verdammt lang gaht...
Wenn (Z>Z2)
Soltau Kristine
[]

Eder Eva
[]

Michael Jill
Z        | P  | L
---------|----|--
3.2.2017 | () | 0

Wenn (Z<Z2)
Soltau Kristine
[]

Eder Eva
[]

Michael Jill
Z        | P  | L
---------|----|--
3.2.2017 | () | 0

mit dem:
for i in range(0,50): # calls
for i in range(0,25): # texts

häts für Eder Eva und Michael Jill zviel übereinstimmige gäh...
"""



# General hint (only use on last resort!): 
#   if nothing else helped, have a look at https://github.com/pcarbonn/pyDatalog/blob/master/pyDatalog/examples/graph.py
