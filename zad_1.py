def hello(*, name: str, last_name: str) -> str:
    return f"Cześć {name} {last_name}!"


if __name__ == '__main__':
    przywitanie = hello(name='Jan', last_name='Kowalski')
    print(przywitanie)

"""
Cześć Jan Kowalski!
"""
