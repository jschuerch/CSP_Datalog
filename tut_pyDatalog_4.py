from pyDatalog import pyDatalog
pyDatalog.create_terms('X,Y,manager, count_of_direct_reports, X, Y, Z')

# the manager of Mary is John
+(manager['Mary'] == 'John')
+(manager['Sam']  == 'Mary')
+(manager['Tom']  == 'Mary')

(count_of_direct_reports[X]==len_(Y)) <= (manager[Y]==X)
print(count_of_direct_reports['Mary']==Z)




