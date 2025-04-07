from typing import Iterable, override

from banana.reasoning.constraint import Constraint
from banana.validation import validate_word


class InSet(Constraint):
    def __init__(self, words: Iterable[str]) -> None:
        self._words = frozenset(map(validate_word, words))
        print(f"InSet: {self._words}")

    @override
    def filter(self, words: Iterable[str]) -> Iterable[str]:
        print(f"filtering {words} with {self._words}")
        return filter(self._words.__contains__, map(validate_word, words))
