from itertools import chain
from typing import Iterable, Iterator, Sized, override

from banana.board import Board, Word
from banana.reasoning.constraint import Constraint


class And(Constraint, Sized, Iterable[Constraint]):
    def __init__(self, constraints: Iterable[Constraint]) -> None:
        self._constraints = list(constraints)

    @override
    def __len__(self) -> int:
        return len(self._constraints)

    @override
    def __iter__(self) -> Iterator[Constraint]:
        return iter(self._constraints)

    @override
    def filter(self, words: Iterable[str]) -> Iterable[str]:
        for constraint in self:
            words = constraint.filter(words)
        return words

    @override
    def create_candidates(self, board: Board, word: str) -> Iterable[Word]:
        return chain.from_iterable(
            constraint.create_candidates(board, word) for constraint in self
        )
