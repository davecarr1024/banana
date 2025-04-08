from typing import Iterable, override

from banana.reasoning.constraint import Constraint
from banana.validation import validate_word


class InSet(Constraint):
    def __init__(self, words: Iterable[str]) -> None:
        self._words = frozenset(map(validate_word, words))

    @override
    def __repr__(self) -> str:
        return f"InSet({self._words})"

    @override
    def filter(self, words: Iterable[str]) -> Iterable[str]:
        return self._words
