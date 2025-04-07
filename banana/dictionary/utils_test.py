import pytest
from pytest_subtests import SubTests

from banana.dictionary.utils import (
    LetterHistogram,
    ValueError,
    words_that_contain_letter,
    words_that_contain_letters,
)


def test_words_that_contain_letter_invalid_letter(subtests: SubTests) -> None:
    for value in list[str](["", "1", "ab"]):
        with subtests.test(value=value):
            with pytest.raises(ValueError):
                words_that_contain_letter(["abc", "def"], value)


def test_words_that_contain_letter_invalid_word(subtests: SubTests) -> None:
    for word in list[str](["", "1"]):
        with subtests.test(word=word):
            with pytest.raises(ValueError):
                list(words_that_contain_letter([word], "a"))


def test_words_that_contain_letter(subtests: SubTests) -> None:
    for words, letter, expected in list[tuple[list[str], str, list[str]]](
        [
            (
                [],
                "a",
                [],
            ),
            (
                ["b"],
                "a",
                [],
            ),
            (
                ["a", "b"],
                "a",
                ["A"],
            ),
            (
                ["ab", "ac", "bc"],
                "a",
                ["AB", "AC"],
            ),
        ]
    ):
        with subtests.test(words=words, letter=letter, expected=expected):
            assert list(words_that_contain_letter(words, letter)) == expected


def test_words_that_contain_letters_invalid_letter(subtests: SubTests) -> None:
    for value in list[str](["", "1", "ab"]):
        with subtests.test(value=value):
            with pytest.raises(ValueError):
                words_that_contain_letters(
                    ["abc", "def"],
                    ["a", value],
                )


def test_words_that_contain_letters_invalid_word(subtests: SubTests) -> None:
    for word in list[str](["", "1"]):
        with subtests.test(word=word):
            with pytest.raises(ValueError):
                list(
                    words_that_contain_letters(
                        [word],
                        ["a", "b"],
                    )
                )


def test_words_that_contain_letters(subtests: SubTests) -> None:
    for words, letters, expected in list[tuple[list[str], list[str], list[str]]](
        [
            (
                [],
                [],
                [],
            ),
            (
                ["c"],
                ["a", "b"],
                [],
            ),
            (
                ["ab", "ba", "ac"],
                ["a", "b"],
                ["AB", "BA"],
            ),
        ]
    ):
        with subtests.test(words=words, letters=letters, expected=expected):
            assert list(words_that_contain_letters(words, letters)) == expected


def test_letter_histogram_ctor() -> None:
    assert LetterHistogram([]) == dict()
    assert LetterHistogram(["aab", "bc"]) == {
        "A": 0.4,
        "B": 0.4,
        "C": 0.2,
    }
    with pytest.raises(LetterHistogram.ValueError):
        LetterHistogram([""])
    with pytest.raises(LetterHistogram.ValueError):
        LetterHistogram(["1"])


def test_letter_histogram_getitem() -> None:
    lh = LetterHistogram(["aab", "bc"])
    assert lh["a"] == 0.4
    assert lh["b"] == 0.4
    assert lh["c"] == 0.2
    with pytest.raises(LetterHistogram.ValueError):
        lh[""]
    with pytest.raises(LetterHistogram.ValueError):
        lh["1"]
    with pytest.raises(LetterHistogram.KeyError):
        lh["d"]


def test_letter_histogram_len() -> None:
    assert len(LetterHistogram([])) == 0
    assert len(LetterHistogram(["aab", "bc"])) == 3


def test_letter_histogram_word_frequency() -> None:
    lh = LetterHistogram(["aab", "bc"])
    assert list(lh.word_frequency("a")) == [0.4]
    assert list(lh.word_frequency("ab")) == [0.4, 0.4]


def test_letter_histogram_total_word_frequency() -> None:
    lh = LetterHistogram(["aab", "bc"])
    assert lh.total_word_frequency("a") == 0.4
    assert lh.total_word_frequency("ab") == 0.8


def test_letter_histogram_average_word_frequency() -> None:
    lh = LetterHistogram(["aab", "bc"])
    assert lh.average_word_frequency("a") == 0.4
    assert lh.average_word_frequency("ab") == 0.4
    assert lh.average_word_frequency("ac") == pytest.approx(0.3)  # type:ignore


def test_letter_histogram_max_word_frequency() -> None:
    lh = LetterHistogram(["aab", "bc"])
    assert lh.max_word_frequency("a") == 0.4
    assert lh.max_word_frequency("ac") == 0.4
    assert lh.max_word_frequency("c") == 0.2
