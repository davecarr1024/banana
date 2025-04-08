from abc import ABC, abstractmethod
from collections import Counter
from typing import Iterable

from banana.board import Board
from banana.reasoning.constraint import Constraint
from banana.reasoning.constraints import InSet
from banana.validation import validate_letter, validate_word


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
        letter_counts = Counter(map(validate_letter, letters))
        print(f"letter_counts: {letter_counts}")
        words = list(words)
        for word in map(validate_word, words):
            print(
                "ConstraintGenerator.filter_can_build: "
                f"word: {word} "
                f"counter: {Counter(word)} "
                f"<= letter_counts: {(Counter(word) <= letter_counts)}"
            )
        return InSet(
            filter(
                lambda word: Counter(word) <= letter_counts,
                map(validate_word, words),
            )
        )
