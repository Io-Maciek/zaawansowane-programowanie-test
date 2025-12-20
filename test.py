import pytest
import zad

def test_sum():
    assert True is True

def kajak_palindrom():
    assert zad.is_palindrome('kajak') is True

def kobyla_palindrom():
    assert zad.is_palindrome('Kobyła ma mały bok') is True

def python_not_palindrom():
    assert zad.is_palindrome('python') is False

def empty_palindrom():
    assert zad.is_palindrome('') is True

def a_palindrom():
    assert zad.is_palindrome('A') is True