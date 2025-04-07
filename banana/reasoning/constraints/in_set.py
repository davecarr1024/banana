from typing import Iterable, override

from banana.reasoning.constraint import Constraint


class InSet(Constraint):
    def __init__(self, words: Iterable[str]) -> None:
        self._words = frozenset(words)

    @override
    def filter(self, words: Iterable[str]) -> Iterable[str]:
        return filter(self._words.__contains__, words)
