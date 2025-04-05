import pytest
from pytest_subtests import SubTests

from banana.dictionary import Dictionary

test_words = [
    "apple",  # A, E
    "bat",  # B, T
    "cat",  # C
    "dog",  # D, G
    "egg",  # E, G
    "fig",  # F, I
    "gum",  # G, M
    "hat",  # H
    "ice",  # I, C, E
    "jam",  # J, M
    "kite",  # K, T, E
    "log",  # L, G
    "mud",  # M, U
    "nap",  # N, P
    "oak",  # O, K
    "pet",  # P, T
    "quiz",  # Q, U, I, Z
    "rat",  # R, T
    "sun",  # S, N
    "top",  # T, O
    "urn",  # U, R
    "vet",  # V, E, T
    "wax",  # W, A, X
    "yak",  # Y, A, K
    "zoo",  # Z, O
]


def test_invalid():
    with pytest.raises(Dictionary.ValueError):
        Dictionary(["123"])


def test_contains():
    d = Dictionary(test_words)
    assert "WAX" in d
    assert "oak" in d
    assert "FOO" not in d
    assert "foo" not in d


def test_contains_invalid(subtests: SubTests):
    for value in list[str](["1", ""]):
        with subtests.test(value=value):
            with pytest.raises(Dictionary.ValueError):
                Dictionary(test_words).__contains__(value)


def test_iter():
    assert set(Dictionary(test_words)) == {word.upper() for word in test_words}


def test_len():
    assert len(Dictionary(test_words)) == len(test_words)


def test_words_that_contain_letter_invalid(subtests: SubTests):
    for value in list[str](["", "1", "abc"]):
        with subtests.test(value=value):
            with pytest.raises(Dictionary.ValueError):
                Dictionary(test_words).words_that_contain_letter(value)


def test_words_that_contain_letter():
    d = Dictionary(test_words)
    assert d.words_that_contain_letter("a") == {
        "APPLE",
        "BAT",
        "CAT",
        "HAT",
        "JAM",
        "NAP",
        "OAK",
        "RAT",
        "WAX",
        "YAK",
    }


def test_words_that_contain_letters():
    d = Dictionary(test_words)
    assert d.words_that_contain_letters(["a", "E"]) == {
        "APPLE",
    }
