def contains(list:list, x)->bool: return x in list

print(contains(list(range(0,100,2)), 50))                           # true
print(contains(['a', 'b', 'c'], 'c'))                               # true
print(contains(['a', 8, type(4.5), str], type('testowy string')))   # true
print(contains([1,2,3], 0))                                         # false