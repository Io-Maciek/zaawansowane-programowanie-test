def create_list(a: list, b: list)->list: return [x**3 for x in list(set(a+b))]

print(create_list([1,2,3], [2,3,5,6,7]))