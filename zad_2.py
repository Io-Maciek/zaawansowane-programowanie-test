def zadanie_petla(*, liczby: list[int] = []) -> list[int]:
    nowa_lista = []
    for liczba in liczby:
        nowa_lista.append(liczba * 2)
    
    return nowa_lista

def zadanie_lista(*, liczby: list[int] = []) -> list[int]:
    return [l*2 for l in liczby]

if(__name__ == "__main__"):
    print(zadanie_petla(liczby = [5,10,23,1,100]))
    print(zadanie_lista(liczby = [5,10,23,1,100]))

"""
[10, 20, 46, 2, 200]
[10, 20, 46, 2, 200]
"""