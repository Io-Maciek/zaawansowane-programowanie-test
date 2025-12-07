def check_parity(number: float) -> bool:
    return number % 2 == 0


def formatted_parity(b: bool) -> str:
    return "Liczba parzysta" if b else "Liczba nieparzysta"


wynik1 = check_parity(2)
wynik2 = check_parity(37)

print(formatted_parity(wynik1))
print(formatted_parity(wynik2))

"""
Liczba parzysta
Liczba nieparzysta
"""
