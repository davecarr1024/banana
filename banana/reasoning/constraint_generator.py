from abc import ABC, abstractmethod
from collections import Counter
from typing import Iterable

from banana.board import Board
from banana.reasoning.constraint import Constraint
from banana.reasoning.constraints import InSet


class ConstraintGenerator(ABC):
    @abstractmethod
    def generate(
        self, board: Board, letters: Iterable[str]
    ) -> Iterable[Constraint]: ...

    @staticmethod
    def filter_can_build(
        words: Iterable[str],
        letters: Iterable[str],
    ) -> Constraint:
        letter_counts = Counter(letters)
        return InSet(
            filter(
                lambda word: Counter(word) <= letter_counts,
                words,
            )
        )
