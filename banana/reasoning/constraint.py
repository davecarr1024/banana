from typing import Iterable

from banana.board import Board, Word


class Constraint:
    def filter(self, words: Iterable[str]) -> Iterable[str]:
        return words

    def create_candidates(self, board: Board, word: str) -> Iterable[Word]:
        return []
