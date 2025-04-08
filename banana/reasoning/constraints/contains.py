from typing import Iterable, override

from banana.reasoning.constraint import Constraint


class Contains(Constraint):
    class Error(Exception): ...

    class ValueError(Error, ValueError): ...

    def __init__(self, letters: Iterable[str]) -> None:
        self._letters = frozenset(letters)
        if len(self._letters) < 1:
            raise self.ValueError("Must contain at least one letter")

    @override
    def __repr__(self) -> str:
        return f"Contains({self._letters})"

    @override
    def filter(self, words: Iterable[str]) -> Iterable[str]:
        return filter(
            lambda word: all(letter in word for letter in self._letters),
            words,
        )
