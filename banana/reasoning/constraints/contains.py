from typing import Iterable, override

from banana.dictionary.utils import (
    words_that_contain_letter,
    words_that_contain_letters,
)
from banana.reasoning.constraint import Constraint


class Contains(Constraint):
    class Error(Exception): ...

    class ValueError(Error, ValueError): ...

    def __init__(self, letters: Iterable[str]) -> None:
        self._letters = frozenset(letters)
        if len(self._letters) < 1:
            raise self.ValueError("Must contain at least one letter")

    @override
    def filter(self, words: Iterable[str]) -> Iterable[str]:
        if len(self._letters) == 1:
            return words_that_contain_letter(words, next(iter(self._letters)))
        else:
            return words_that_contain_letters(words, self._letters)
