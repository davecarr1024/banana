from collections import defaultdict
from collections.abc import Mapping
from typing import Iterable, Iterator, override


class Error(Exception): ...


class ValueError(Error, ValueError): ...


def _validate_word(word: str) -> str:
    if not word.isalpha():
        raise ValueError(f"Word must be alpha, not {word!r}")
    return word.upper()


def _validate_letter(letter: str) -> str:
    if len(letter) != 1 or not letter.isalpha():
        raise ValueError(f"Letter must be a single alpha character, not {letter!r}")
    return letter.upper()


def words_that_contain_letter(words: Iterable[str], letter: str) -> Iterable[str]:
    if len(letter) != 1 or not letter.isalpha():
        raise ValueError(f"Letter must be a single alpha character, not {letter!r}")
    letter = _validate_letter(letter)
    return filter(
        lambda word: letter in word,
        (_validate_word(word) for word in words),
    )


def words_that_contain_letters(
    words: Iterable[str],
    letters: Iterable[str],
) -> Iterable[str]:
    letters = [_validate_letter(letter) for letter in letters]
    return filter(
        lambda word: all(letter in word for letter in letters),
        (_validate_word(word) for word in words),
    )


class LetterHistogram(Mapping[str, float]):
    class Error(Error): ...

    class ValueError(Error, ValueError): ...

    class KeyError(Error, KeyError): ...

    def __init__(self, words: Iterable[str]) -> None:
        freq = defaultdict[str, int](int)
        for word in words:
            try:
                for letter in _validate_word(word):
                    freq[letter] += 1
            except ValueError as e:
                raise self.ValueError(f"Invalid letter in word {word!r}") from e
        total = sum(freq.values())
        self._histogram: Mapping[str, float] = {
            letter: value / total for letter, value in freq.items()
        }

    @override
    def __getitem__(self, letter: str) -> float:
        try:
            return self._histogram[_validate_letter(letter)]
        except ValueError as e:
            raise self.ValueError(f"Invalid letter {letter!r}") from e
        except KeyError as e:
            raise self.KeyError(f"Letter {letter!r} not in histogram") from e

    @override
    def __iter__(self) -> Iterator[str]:
        return iter(self._histogram)

    @override
    def __len__(self) -> int:
        return len(self._histogram)

    def word_frequency(self, word: str) -> Iterable[float]:
        return (self[letter] for letter in word)

    def total_word_frequency(self, word: str) -> float:
        return sum(self.word_frequency(word))

    def average_word_frequency(self, word: str) -> float:
        return self.total_word_frequency(word) / len(word)

    def max_word_frequency(self, word: str) -> float:
        return max(self.word_frequency(word))
