def print_second_el(*, liczby:list[int] = []):
    for i in range(len(liczby)):
        if i%2==1:
            print(liczby[i])

if(__name__ == "__main__"):
    print_second_el(liczby = range(0, 10*9, 9))

"""
9
27
45
63
81
"""