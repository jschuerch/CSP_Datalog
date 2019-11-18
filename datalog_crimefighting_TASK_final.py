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

pyDatalog.create_terms('X, Y, Z, get_all_paths, P, P2, get_short_paths, L, L2')
# Task 1: Knowing someone is a bi-directional relationship -> define the predicate accordingly
knows(X, Y) <= knows(Y, X)

###output
#print("%s knows Y" % (suspect))
#print(knows(suspect, Y))

# Task 2: Define the predicate has_link in a way that it is true if a connection exists (path of people knowing the next link)
has_link(X,Y) <= knows(X,Y)
has_link(X,Y) <= knows(X,Z) & has_link(Z,Y) & (X!=Y)

###output
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

#paths(X,Y,P) <= paths(X,Z,P2) & knows(Z,Y) & (X!=Y) & Z._not_in(P2) & (P==P2 + [Z]) # für paths isch das gange, aber für with len nöd...
#vode hilfsssite... ?? werum X und Y nöd in P2?? paths(X, Y, P) <= paths(X, Z, P2) & knows(Z, Y) & (X != Y) & (X._not_in(P2)) & (Y._not_in(P2)) & (P == P2 + [Z])

get_all_paths(X, Y, P) <= get_all_paths(X, Z, P2) & knows(Z, Y) & (X != Y) & X._not_in(P2) & Y._not_in(P2) & (P == P2 + [Z])
get_all_paths(X, Y, P) <= knows(X, Y) & (P == [])

###output
"""for i in range(0,len(company_Board)):
    print(company_Board[i])
    print(get_all_paths(suspect, company_Board[i], P))"""
# all together
#print(get_all_paths(suspect, Y, P) & (Y.in_(company_Board)))

# Task 4: There are too many paths. We are only interested in short paths.
# Find all the paths between the suspect and the company board that contain five people or less

get_short_paths(X, Y, P, L) <= (get_short_paths(X, Z, P2, L2)
                                & knows(Z, Y)
                                & (X != Y)
                                & X._not_in(P2)
                                & Y._not_in(P2)
                                & (P == P2 + [Z])
                                & (L == L2 + 1)
                                )
get_short_paths(X, Y, P, L) <= knows(X, Y) & (P == []) & (L == 0)

###output
"""for i in range(0,len(company_Board)):
    print(company_Board[i])
    print(get_short_paths(suspect, company_Board[i], P, L) & (L<=5))"""
print(get_short_paths(suspect, X, P, L) & (L<=5) & (X.in_(company_Board)))

# ---------------------------------------------------------------------------
# Call-Data analysis:
# Now we use the text and the calls data together with their corresponding dates
# ---------------------------------------------------------------------------
date_board_decision = '12.2.2017'
date_shares_bought = '23.2.2017'
pyDatalog.create_terms('called,texted')
pyDatalog.clear()

print ("------ Dragnet (dated) ------")

for i in range(0,len(calls)): # calls
    +called(calls.iloc[i,1], calls.iloc[i,2],calls.iloc[i,3])

for i in range(0,len(texts)): # texts
    +texted(texts.iloc[i,1], texts.iloc[i,2],texts.iloc[i,3])

called(X,Y,Z) <= called(Y,X,Z) # calls are bi-directional

# Task 5: Again we are interested in links, but this time a connection is only valid if the links are descending in date; 
#         find out who could have actually sent the information by adding this new restriction
# Hints:
#   You are allowed to naively compare the dates lexicographically using ">" and "<";
#   it works in this example (but is evil in general)
pyDatalog.create_terms('datapath, A, A2, D, D2')
pyDatalog.create_terms('dated_links, get_dated_paths, PD, PD2')

knows(X,Y,D) <= called(X,Y,D)
knows(X,Y,D) <= texted(X,Y,D)
#print (knows(suspect,Y,D))

has_link(X,Y,D) <= knows(X,A,D) & has_link(A,Y,D2) & (X!=Y) & (D>D2)
has_link(X,Y,D) <= knows(X,Y,D)
#print (has_link(suspect,Y,Z))

# Task 6: Find all the communication paths that lead to the suspect (with the restriction that the dates have to be ordered correctly)
get_dated_paths(X,Y,D,P,A) <= (get_dated_paths(X,Z,D2,P2,A2)
                                & knows(Z,Y,D)
                                & (D>=D2)
                                & X._not_in(P2)
                                #& Z._not_in(P2)
                                & Y._not_in(P2)
                                & (X!=Y)
                                & (D>= date_board_decision)
                                & (D <= date_shares_bought)
                                & (P==P2 + [Z])
                                & (A==A2 + [D2])
                                )
get_dated_paths(X,Y,D,P,A) <= (knows(X,Y,D)
                                & (D >= date_board_decision)
                                & (D <= date_shares_bought)
                                & (P==[])
                                & (A==[])
                                )
print(get_dated_paths(X, suspect, D, P, A) & X._in(company_Board))

# General hint (only use on last resort!): 
#   if nothing else helped, have a look at https://github.com/pcarbonn/pyDatalog/blob/master/pyDatalog/examples/graph.py
