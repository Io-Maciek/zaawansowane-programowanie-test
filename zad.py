def is_palindrome(text: str) -> bool: return text == text[::-1]

def fibonacci(n: int) -> int:
    if n < 0:
        raise NotImplementedError()
    
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return 1 + fibonacci(n-1)
    # todo

def count_vowels(text: str) -> int:
    return len(list(filter(lambda x: x.lower() in ['a', 'e', 'i', 'o', 'u', 'y'], text)))

def calculate_discount(price: float, discount: float) -> float:
    if 0.0 <= discount <= 1.0:
        return price*(1 - discount)
    else:
        raise ValueError()    

def flatten_list(nested_list: list) -> list:
    pass
    # todo

def word_frequencies(text: str) -> dict:
    d = {}
    

print(flatten_list([1,4,[6,4]]))