from collections.abc import Mapping, Set
from string import ascii_uppercase
from typing import Iterable, Iterator, override


class Dictionary(Set[str]):
    class Error(Exception): ...

    class ValueError(Error, ValueError): ...

    @staticmethod
    def _validate_word(word: str) -> str:
        if not word.isalpha():
            raise Dictionary.ValueError(f"Word must be alpha, not {word!r}")
        return word.upper()

    def __init__(self, words: Iterable[str]) -> None:
        self._words = frozenset(Dictionary._validate_word(word) for word in words)
        self._words_by_letter: Mapping[str, frozenset[str]] = {
            letter: frozenset(word for word in self._words if letter in word)
            for letter in ascii_uppercase
        }

    @override
    def __contains__(self, word: object) -> bool:
        return isinstance(word, str) and Dictionary._validate_word(word) in self._words

    @override
    def __iter__(self) -> Iterator[str]:
        return iter(self._words)

    @override
    def __len__(self) -> int:
        return len(self._words)

    def words_that_contain_letter(self, letter: str) -> frozenset[str]:
        if len(letter) != 1 or not letter.isalpha():
            raise self.ValueError(
                f"Letter must be a single alpha character, not {letter!r}"
            )
        return self._words_by_letter[letter.upper()]

    def words_that_contain_letters(self, letters: Iterable[str]) -> frozenset[str]:
        letters = list(letters)
        if not letters:
            return self._words
        return frozenset[str].intersection(
            *[self.words_that_contain_letter(letter) for letter in letters]
        )
