import re

def is_palindrome(text: str) -> bool: return text.lower().replace(" ", "") == text.lower().replace(" ", "")[::-1]

def fibonacci(n: int) -> int:
    if n < 0:
        raise NotImplementedError()
    
    if n == 0:
        return 0
    elif n == 1 or n == 2:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)

def count_vowels(text: str) -> int:
    return len(list(filter(lambda x: x.lower() in ['a', 'e', 'i', 'o', 'u', 'y'], text)))

def calculate_discount(price: float, discount: float) -> float:
    if 0.0 <= discount <= 1.0:
        return price*(1 - discount)
    else:
        raise ValueError()    

def flatten_list(nested_list: list|int) -> list:
    l = []
    if type(nested_list) is list:
        for e in nested_list:
            for f in flatten_list(e):
                l.append(f)
    else:
        l.append(nested_list)

    return l

def word_frequencies(text: str) -> dict:
    d = {}
    for character in filter(lambda c: re.match("[a-zA-Z]", c), text):
        d[character] = d.get(character, 0) + 1

    return d

def is_prime(n: int) -> bool:
    if n < 2:
        return False
    else:
        _is_prime = True
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                _is_prime = False
                break
        return _is_prime
