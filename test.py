import pytest
import zad


def test_sum():
    assert True is True


def test_kajak_palindrom():
    assert zad.is_palindrome('kajak') is True


def test_kobyla_palindrom():
    assert zad.is_palindrome('Kobyła ma mały bok') is True


def test_python_not_palindrom():
    assert zad.is_palindrome('python') is False


def test_empty_palindrom():
    assert zad.is_palindrome('') is True


def test_a_palindrom():
    assert zad.is_palindrome('A') is True


def test_fibonacci0():
    assert zad.fibonacci(0) == 0


def test_fibonacci1():
    assert zad.fibonacci(1) == 1


def test_fibonacci5():
    assert zad.fibonacci(5) == 5


def test_fibonacci10():
    assert zad.fibonacci(10) == 55


def test_fibonacciminus1():
    with pytest.raises(NotImplementedError):
        zad.fibonacci(-1)


def test_vowels():
    assert zad.count_vowels("Python") == 2
    assert zad.count_vowels("AEIOUY") == 6
    assert zad.count_vowels("bcd") == 0
    assert zad.count_vowels("") == 0
    assert zad.count_vowels("Próba żółwia") == 5


def test_calculate_discount():
    assert zad.calculate_discount(100, .2) == 80.0
    assert zad.calculate_discount(50, .0) == 50.0
    assert zad.calculate_discount(200, 1.0) == 0.0
    with pytest.raises(ValueError):
        assert zad.calculate_discount(100, -.1)
        assert zad.calculate_discount(100, 1.5)


def test_flatten_list():
    assert zad.flatten_list([1, 2, 3]) == [1, 2, 3]
    assert zad.flatten_list([1, [2, 3], [4, [5]]]) == [1, 2, 3, 4, 5]
    assert zad.flatten_list([]) == []
    assert zad.flatten_list([[[1]]]) == [1]
    assert zad.flatten_list([1, [2, [3, [4]]]]) == [1, 2, 3, 4]


def test_word_frequencies():
    assert zad.word_frequencies("To be or not to be") == {"to": 2, "be": 2, "or": 1, "not": 1}
    assert zad.word_frequencies("Hello, hello!") == {"hello": 2}
    assert zad.word_frequencies("") == {}
    assert zad.word_frequencies("Python Python python") == {"python": 3}
    assert zad.word_frequencies("Ala ma kota, a kot ma Ale.") == {'ala': 1, "ma": 2, "kota": 1, "a": 1, "kot": 1, "ale": 1}


def test_prime():
    assert zad.is_prime(2) is True
    assert zad.is_prime(3) is True
    assert zad.is_prime(4) is False
    assert zad.is_prime(0) is False
    assert zad.is_prime(1) is False
    assert zad.is_prime(5) is False
    assert zad.is_prime(97) is True
