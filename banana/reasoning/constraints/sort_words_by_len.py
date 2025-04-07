from typing import Iterable, override

from banana.reasoning.constraint import Constraint


class SortWordsByLen(Constraint):
    def __init__(self, *, reverse: bool = False) -> None:
        self.reverse = reverse

    @override
    def filter(self, words: Iterable[str]) -> Iterable[str]:
        return sorted(words, key=len, reverse=self.reverse)
