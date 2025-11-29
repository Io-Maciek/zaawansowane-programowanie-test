def print_even(*, liczby:list[int] = []):
    print(list(filter(lambda l: l%2==0, liczby)))

if(__name__ == "__main__"):
    print_even(liczby = range(0, 10))

"""
[0, 2, 4, 6, 8] 
"""