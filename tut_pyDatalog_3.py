from pyDatalog import pyDatalog
pyDatalog.create_terms('X,Y,Z, salary, tax_rate, tax_rate_for_salary_above, net_salary')

salary['foo'] = 60
salary['bar'] = 110
salary['asdf'] = 110

# Python equivalent
_salary = dict()
_salary['foo'] = 60
_salary['bar'] = 110


print(salary[X]==Y)
print
# python equivalent
print(_salary.items())
print(_salary['foo'])

# foo now has a salary of 70
salary['foo'] = 70
print(salary[X]==Y)
print

print(salary[X]==110)


print((salary[X]==Y) & ~(Y==110))

# the standard tax rate is 33%
+(tax_rate[None]==0.33)

# give me the net salary for all X
print((Z==salary[X]*(1-tax_rate[None])))

# the net salary of X is Y if Y is the salary of X, reduced by the tax rate
net_salary[X] = salary[X]*(1-tax_rate[None])

print(net_salary[X]==Y)
print

# give me the net salary of foo
print(net_salary['foo']==Y)
print
print(net_salary[Y]<50)

# the tax rate for salaries above 0 is 33%, and above 100 is 50 %
(tax_rate_for_salary_above[X] == 0.33) <= (0 <= X)
(tax_rate_for_salary_above[X] == 0.50) <= (100 <= X)
print(tax_rate_for_salary_above[70]==Y)
print
print(tax_rate_for_salary_above[150]==Y)

# retract our previous definition of net_salary
del net_salary[X]

net_salary[X] = salary[X]*(1-tax_rate_for_salary_above[salary[X]])
# give me all X and Y so that Y is the net salary of X
print(net_salary[X]==Y)

pyDatalog.create_terms('factorial, N')

factorial[N] = N*factorial[N-1]
factorial[1] = 1

print(factorial[5]==N)
